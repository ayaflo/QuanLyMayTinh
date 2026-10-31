"""Local DNS Proxy Server for Open Guardian Kids (F2, NT2, NT6).
Listens on UDP 127.0.0.1:53 to enforce DNS Sinkholing, SafeSearch rewriting,
DoH Canary domain blocking, and permanent educational/111 hotline whitelisting.
"""

import socket
import threading
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Set, Callable, Dict, Any, Tuple, Iterable
from dnslib import DNSRecord, DNSQuestion, RR, QTYPE, A, AAAA, RCODE

logger = logging.getLogger("OGK_DNSProxy")

# SafeSearch Canonical Destination IPs (IPv4 & IPv6 VIPs)
SAFESEARCH_GOOGLE_IP = "216.239.38.120"      # forcesafesearch.google.com (IPv4)
SAFESEARCH_GOOGLE_IPV6 = "2001:4860:4806::78" # forcesafesearch.google.com (IPv6)
SAFESEARCH_BING_IP = "204.79.197.220"        # strict.bing.com (IPv4)
SAFESEARCH_YOUTUBE_IP = "216.239.38.120"     # restrict.youtube.com (IPv4)
SAFESEARCH_YOUTUBE_IPV6 = "2001:4860:4806::78" # restrict.youtube.com (IPv6)

DOH_CANARY_DOMAIN = "use-application-dns.net"

# Default fallback upstream DNS servers
DEFAULT_UPSTREAM_DNS = "8.8.8.8"  # Google Public DNS (tính sẵn sàng cao nhất)
DEFAULT_FALLBACK_DNS = "1.1.1.1"  # Cloudflare Public DNS


def normalize_domain(domain_str: str) -> str:
    """Normalize domain name by stripping whitespace, trailing dots, and lowercasing."""
    return domain_str.strip().rstrip(".").lower()


def match_domain(query_domain: str, target_rules: Set[str]) -> bool:
    """Check if query domain matches exactly or is a subdomain of any target rule (T3_030).
    For example: 'm.youtube.com' matches 'youtube.com'.
    """
    clean_query = normalize_domain(query_domain)
    for rule in target_rules:
        clean_rule = normalize_domain(rule)
        if clean_query == clean_rule or clean_query.endswith("." + clean_rule):
            return True
    return False


def is_google_search_domain(domain: str) -> bool:
    """Check if query domain is Google web search."""
    clean = normalize_domain(domain)
    return (
        clean == "google.com"
        or clean == "www.google.com"
        or clean == "google.com.vn"
        or clean == "www.google.com.vn"
        or clean.startswith("www.google.")
    )


def is_bing_search_domain(domain: str) -> bool:
    """Check if query domain is Bing search."""
    clean = normalize_domain(domain)
    return clean == "bing.com" or clean == "www.bing.com"


def is_youtube_domain(domain: str) -> bool:
    """Check if query domain is YouTube (T3_032)."""
    clean = normalize_domain(domain)
    return clean in ("youtube.com", "www.youtube.com", "m.youtube.com", "youtube-nocookie.com")


def get_system_dns_servers() -> list:
    """Truy xuất các máy chủ DNS gốc của máy trước khi trỏ về 127.0.0.1 để tránh mất mạng."""
    servers = []
    try:
        from agent.dns_watchdog import get_adapter_dns_servers
        from agent.dns_configurator import get_active_interfaces
    except ImportError:
        try:
            from dns_watchdog import get_adapter_dns_servers
            from dns_configurator import get_active_interfaces
        except ImportError:
            return servers

    try:
        for iface in get_active_interfaces():
            for s in get_adapter_dns_servers(iface):
                if s and not s.startswith("127.") and s not in servers:
                    servers.append(s)
    except Exception:
        pass
    return servers


class DNSProxyServer:
    """High-performance multi-threaded UDP DNS Proxy Server running on 127.0.0.1 & [::1] (F2)."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 53,
        upstream_ip: str = DEFAULT_UPSTREAM_DNS,
        upstream_port: int = 53,
        on_event_callback: Optional[Callable[[str, str], None]] = None,
        max_workers: int = 32
    ):
        self.host = host
        self.port = port
        self.upstream_ip = upstream_ip
        self.upstream_port = upstream_port
        self.on_event_callback = on_event_callback
        self.max_workers = max_workers

        self.blocked_domains: Set[str] = set()
        self.permanent_whitelist: Set[str] = {
            "tongdai111.vn",
            "moet.gov.vn",
            "hcmus.edu.vn",
            "vnuhcm.edu.vn"
        }
        self.enforce_safesearch: bool = True
        self.system_dns_servers: list = get_system_dns_servers()
        self._active_upstream: Optional[Tuple[str, int]] = None

        self._running = False
        self._threads: list[threading.Thread] = []
        self._sock: Optional[socket.socket] = None
        self._sock_v6: Optional[socket.socket] = None
        self._executor: Optional[ThreadPoolExecutor] = None
        self._cache: Dict[Tuple[str, int], Tuple[float, bytes]] = {}
        self._cache_lock = threading.Lock()

    def update_rules(
        self,
        blocked: Iterable[str],
        whitelist: Optional[Set[str]] = None,
        enforce_safesearch: bool = True
    ):
        """Update live memory rules for instantaneous rule application (< 1s)."""
        self.blocked_domains = {normalize_domain(d) for d in blocked}
        statutory_whitelist = {
            "tongdai111.vn",
            "moet.gov.vn",
            "hcmus.edu.vn",
            "vnuhcm.edu.vn"
        }
        if whitelist:
            self.permanent_whitelist = statutory_whitelist | {normalize_domain(d) for d in whitelist}
        else:
            self.permanent_whitelist = set(statutory_whitelist)
        self.enforce_safesearch = enforce_safesearch
        with self._cache_lock:
            self._cache.clear()

    def process_dns_query(self, data: bytes) -> bytes:
        """Parse incoming DNS packet, evaluate rules, and return response bytes."""
        try:
            request = DNSRecord.parse(data)
        except Exception:
            return b""

        if not getattr(request, "q", None):
            return b""

        reply = request.reply()
        qname_str = str(request.q.qname).rstrip(".")
        clean_domain = normalize_domain(qname_str)
        qtype = request.q.qtype

        # 1. DoH Canary Domain (T3_033): Return NXDOMAIN to disable browser DoH bypass
        if clean_domain == DOH_CANARY_DOMAIN:
            reply.header.rcode = RCODE.NXDOMAIN
            return reply.pack()

        # 2. NT6: Permanent Whitelist has absolute priority over blocklists (T3_035)
        if match_domain(clean_domain, self.permanent_whitelist):
            if self.on_event_callback:
                self.on_event_callback("web_access", clean_domain)
            return self._forward_with_cache(clean_domain, qtype, data)

        # 3. DNS Sinkholing (T3_031): Intercept blocked domains & subdomains (T3_030)
        if match_domain(clean_domain, self.blocked_domains):
            logger.info(f"[DNS SINKHOLE] Blocked domain queried: {clean_domain}")
            if self.on_event_callback:
                self.on_event_callback("blocked_domain", clean_domain)

            reply.header.rcode = RCODE.NOERROR
            if qtype in (QTYPE.A, QTYPE.ANY):
                reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A("0.0.0.0"), ttl=1))
            return reply.pack()

        # 4. SafeSearch DNS Rewrite (T3_032 - Enforce both IPv4 & IPv6 SafeSearch VIPs)
        if self.enforce_safesearch:
            if is_google_search_domain(clean_domain):
                reply.header.rcode = RCODE.NOERROR
                if qtype in (QTYPE.A, QTYPE.ANY):
                    reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(SAFESEARCH_GOOGLE_IP), ttl=60))
                if qtype in (QTYPE.AAAA, QTYPE.ANY):
                    reply.add_answer(RR(request.q.qname, QTYPE.AAAA, rdata=AAAA(SAFESEARCH_GOOGLE_IPV6), ttl=60))
                return reply.pack()
            elif is_bing_search_domain(clean_domain):
                reply.header.rcode = RCODE.NOERROR
                if qtype in (QTYPE.A, QTYPE.ANY):
                    reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(SAFESEARCH_BING_IP), ttl=60))
                # For Bing AAAA queries, return NODATA (NOERROR, 0 records) to force stub resolver to use IPv4 VIP
                return reply.pack()
            elif is_youtube_domain(clean_domain):
                reply.header.rcode = RCODE.NOERROR
                if qtype in (QTYPE.A, QTYPE.ANY):
                    reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(SAFESEARCH_YOUTUBE_IP), ttl=60))
                if qtype in (QTYPE.AAAA, QTYPE.ANY):
                    reply.add_answer(RR(request.q.qname, QTYPE.AAAA, rdata=AAAA(SAFESEARCH_YOUTUBE_IPV6), ttl=60))
                return reply.pack()

        # 5. Normal Domain: Forward Upstream (T3_034) & Record Minimal FQDN Access (NT2)
        if self.on_event_callback:
            self.on_event_callback("web_access", clean_domain)

        return self._forward_with_cache(clean_domain, qtype, data)

    def _forward_with_cache(self, clean_domain: str, qtype: int, data: bytes) -> bytes:
        """Resolve query via short-lived in-memory cache or upstream servers with fast failover."""
        now = time.time()
        cache_key = (clean_domain, qtype)

        with self._cache_lock:
            if cache_key in self._cache:
                exp, cached_raw = self._cache[cache_key]
                if now < exp and len(cached_raw) >= 12 and len(data) >= 2:
                    # Rewrite the 16-bit query ID in the cached answer to match caller request ID (RFC 1035)
                    return data[:2] + cached_raw[2:]

        resp = self.forward_upstream(data)
        if resp and len(resp) >= 12 and (resp[3] & 0x0F) == 0:
            with self._cache_lock:
                self._cache[cache_key] = (now + 60.0, resp)
        return resp

    def forward_upstream(self, data: bytes) -> bytes:
        """Forward raw DNS query packet to upstream recursive resolver with fast multi-server failover (T3_034)."""
        candidates = []
        if self._active_upstream:
            candidates.append(self._active_upstream)

        # Ưu tiên các DNS gốc từ router/nhà mạng của máy trước khi trỏ loopback
        for s in self.system_dns_servers:
            candidates.append((s, 53))

        candidates.extend([
            (self.upstream_ip, self.upstream_port),
            (DEFAULT_FALLBACK_DNS, 53),
            ("8.8.4.4", 53),
            ("1.0.0.1", 53),
            ("1.1.1.3", 53)
        ])

        seen = set()
        targets = []
        for u in candidates:
            if u not in seen:
                seen.add(u)
                targets.append(u)

        for target_ip, target_port in targets:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(0.8)
            try:
                sock.sendto(data, (target_ip, target_port))
                response, _ = sock.recvfrom(4096)
                if response:
                    self._active_upstream = (target_ip, target_port)
                    return response
            except Exception:
                continue
            finally:
                try:
                    sock.close()
                except Exception:
                    pass

        try:
            req = DNSRecord.parse(data)
            fail_reply = req.reply()
            fail_reply.header.rcode = RCODE.SERVFAIL
            return fail_reply.pack()
        except Exception:
            return b""

    def _handle_packet(self, sock: socket.socket, data: bytes, addr: tuple):
        """Worker thread handler to process incoming DNS queries in parallel without blocking."""
        try:
            resp = self.process_dns_query(data)
            if resp and self._running:
                sock.sendto(resp, addr)
        except Exception as e:
            logger.debug(f"Error handling DNS packet from {addr}: {e}")

    def _serve_loop(self, sock: socket.socket):
        """Worker loop receiving UDP packets and dispatching to ThreadPoolExecutor."""
        while self._running:
            try:
                data, addr = sock.recvfrom(4096)
                if not data:
                    continue
                if self._executor and self._running:
                    self._executor.submit(self._handle_packet, sock, data, addr)
                else:
                    resp = self.process_dns_query(data)
                    if resp and self._running:
                        try:
                            sock.sendto(resp, addr)
                        except Exception:
                            pass
            except (socket.error, OSError):
                # Bắt và bỏ qua lỗi WSAECONNRESET (10054) trên Windows khi client ngắt kết nối
                # TUYỆT ĐỐI không break khỏi vòng lặp khi self._running vẫn True!
                if not self._running:
                    break
                time.sleep(0.005)
                continue
            except Exception as e:
                if not self._running:
                    break
                logger.error(f"Error handling DNS packet: {e}")
                time.sleep(0.005)

    def start(self):
        """Bind sockets and start concurrent background listening threads (T3_029)."""
        if self._running:
            return

        self._running = True
        self._executor = ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="DNSWorker")

        # 1. Bind IPv4 Loopback (127.0.0.1:53)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        t4 = threading.Thread(target=self._serve_loop, args=(self._sock,), daemon=True, name="OGK_DNS_Proxy_v4")
        t4.start()
        self._threads.append(t4)
        logger.info(f"[*] DNS Proxy Server started on IPv4 {self.host}:{self.port}")

        # 2. Bind IPv6 Loopback ([::1]:53) to eliminate IPv6 resolution blackholes on Windows
        try:
            self._sock_v6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            self._sock_v6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock_v6.bind(("::1", self.port))
            t6 = threading.Thread(target=self._serve_loop, args=(self._sock_v6,), daemon=True, name="OGK_DNS_Proxy_v6")
            t6.start()
            self._threads.append(t6)
            logger.info(f"[*] DNS Proxy Server started on IPv6 [::1]:{self.port}")
        except Exception as e:
            logger.debug(f"[*] IPv6 loopback [::1]:53 not available or bound: {e}")

    def is_ipv6_listening(self) -> bool:
        """Kiểm tra cổng IPv6 [::1]:53 có đang mở và nhận gói tin hay không."""
        return bool(self._sock_v6 is not None and self._running)

    def stop(self):
        """Stop proxy server, close sockets, and gracefully terminate thread pool."""
        self._running = False
        for s in (self._sock, self._sock_v6):
            if s:
                try:
                    s.close()
                except Exception:
                    pass
        self._sock = None
        self._sock_v6 = None

        if self._executor:
            self._executor.shutdown(wait=False, cancel_futures=True)
            self._executor = None

        for t in self._threads:
            if t and t.is_alive():
                t.join(timeout=0.5)
        self._threads.clear()
        logger.info("[*] DNS Proxy Server stopped.")
