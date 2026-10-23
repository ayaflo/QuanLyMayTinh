"""Local DNS Proxy Server for Open Guardian Kids (F2, NT2, NT6).
Listens on UDP 127.0.0.1:53 to enforce DNS Sinkholing, SafeSearch rewriting,
DoH Canary domain blocking, and permanent educational/111 hotline whitelisting.
"""

import socket
import threading
import logging
from typing import Optional, Set, Callable, Dict, Any
from dnslib import DNSRecord, DNSQuestion, RR, QTYPE, A, RCODE

logger = logging.getLogger("OGK_DNSProxy")

# SafeSearch Canonical Destination IPs
SAFESEARCH_GOOGLE_IP = "216.239.38.120"   # forcesafesearch.google.com
SAFESEARCH_BING_IP = "204.79.197.220"     # strict.bing.com
SAFESEARCH_YOUTUBE_IP = "216.239.38.120"  # restrict.youtube.com

DOH_CANARY_DOMAIN = "use-application-dns.net"

# Default fallback upstream DNS servers
DEFAULT_UPSTREAM_DNS = "1.1.1.3"  # Cloudflare Families (Malware + Adult block)
DEFAULT_FALLBACK_DNS = "8.8.8.8"  # Google Public DNS


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



class DNSProxyServer:
    """Lightweight UDP DNS Proxy Server running on 127.0.0.1 (F2)."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 53,
        upstream_ip: str = DEFAULT_UPSTREAM_DNS,
        upstream_port: int = 53,
        on_event_callback: Optional[Callable[[str, str], None]] = None
    ):
        self.host = host
        self.port = port
        self.upstream_ip = upstream_ip
        self.upstream_port = upstream_port
        self.on_event_callback = on_event_callback

        self.blocked_domains: Set[str] = set()
        self.permanent_whitelist: Set[str] = {
            "tongdai111.vn",
            "moet.gov.vn",
            "hcmus.edu.vn",
            "vnuhcm.edu.vn"
        }
        self.enforce_safesearch: bool = True

        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._sock: Optional[socket.socket] = None

    def update_rules(
        self,
        blocked: Set[str],
        whitelist: Optional[Set[str]] = None,
        enforce_safesearch: bool = True
    ):
        """Update live memory rules for instantaneous rule application (< 1s)."""
        self.blocked_domains = {normalize_domain(d) for d in blocked}
        if whitelist:
            self.permanent_whitelist.update({normalize_domain(d) for d in whitelist})
        self.enforce_safesearch = enforce_safesearch

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
            return self.forward_upstream(data)

        # 3. DNS Sinkholing (T3_031): Intercept blocked domains & subdomains (T3_030)
        if match_domain(clean_domain, self.blocked_domains):
            logger.info(f"[DNS SINKHOLE] Blocked domain queried: {clean_domain}")
            if self.on_event_callback:
                self.on_event_callback("blocked_domain", clean_domain)

            reply.header.rcode = RCODE.NOERROR
            if qtype in (QTYPE.A, QTYPE.ANY):
                reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A("0.0.0.0"), ttl=60))
            return reply.pack()

        # 4. SafeSearch DNS Rewrite (T3_032)
        if self.enforce_safesearch and qtype in (QTYPE.A, QTYPE.ANY):
            if is_google_search_domain(clean_domain):
                reply.header.rcode = RCODE.NOERROR
                reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(SAFESEARCH_GOOGLE_IP), ttl=60))
                return reply.pack()
            elif is_bing_search_domain(clean_domain):
                reply.header.rcode = RCODE.NOERROR
                reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(SAFESEARCH_BING_IP), ttl=60))
                return reply.pack()
            elif is_youtube_domain(clean_domain):
                reply.header.rcode = RCODE.NOERROR
                reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(SAFESEARCH_YOUTUBE_IP), ttl=60))
                return reply.pack()

        # 5. Normal Domain: Forward Upstream (T3_034) & Record Minimal FQDN Access (NT2)
        if self.on_event_callback:
            self.on_event_callback("web_access", clean_domain)

        return self.forward_upstream(data)

    def forward_upstream(self, data: bytes) -> bytes:
        """Forward raw DNS query packet to upstream recursive resolver with timeout (T3_034)."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2.0)
        try:
            sock.sendto(data, (self.upstream_ip, self.upstream_port))
            response, _ = sock.recvfrom(4096)
            return response
        except (socket.timeout, Exception):
            try:
                # Fallback to secondary upstream
                sock.sendto(data, (DEFAULT_FALLBACK_DNS, 53))
                response, _ = sock.recvfrom(4096)
                return response
            except Exception:
                try:
                    req = DNSRecord.parse(data)
                    fail_reply = req.reply()
                    fail_reply.header.rcode = RCODE.SERVFAIL
                    return fail_reply.pack()
                except Exception:
                    return b""
        finally:
            sock.close()

    def _serve_loop(self):
        """Worker loop receiving UDP packets."""
        while self._running:
            try:
                data, addr = self._sock.recvfrom(4096)
                if not data:
                    continue
                resp = self.process_dns_query(data)
                if resp and self._sock:
                    self._sock.sendto(resp, addr)
            except (socket.error, OSError):
                break
            except Exception as e:
                logger.error(f"Error handling DNS packet: {e}")

    def start(self):
        """Bind socket and start background listening thread (T3_029)."""
        if self._running:
            return

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        self._running = True

        self._thread = threading.Thread(target=self._serve_loop, daemon=True, name="OGK_DNS_Proxy")
        self._thread.start()
        logger.info(f"[*] DNS Proxy Server started on {self.host}:{self.port}")

    def stop(self):
        """Stop proxy server and close socket gracefully."""
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        logger.info("[*] DNS Proxy Server stopped.")
