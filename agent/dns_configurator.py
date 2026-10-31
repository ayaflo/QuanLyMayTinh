"""Windows DNS Adapter & Web Filtering Configurator for Open Guardian Kids (T3_036).
Directs primary network interface DNS to 127.0.0.1 during active agent session,
disables browser DoH bypass, synchronizes blocked domains to Windows hosts file as defense-in-depth,
flushes DNS cache, and cleanly restores DHCP/original state upon termination.
"""

import os
import re
import sys
import subprocess
import logging
from typing import Optional, List, Set, Iterable

logger = logging.getLogger("OGK_DNSConfig")

HOSTS_MARKER_START = "# === OPEN GUARDIAN KIDS BLOCKED DOMAINS (DO NOT EDIT) ==="
HOSTS_MARKER_END = "# === END OPEN GUARDIAN KIDS BLOCKED DOMAINS ==="
WINDOWS_HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"


def get_active_interfaces() -> List[str]:
    """Discover names of active physical network interfaces (e.g. 'Wi-Fi', 'Ethernet') on Windows.
    Strictly filters out virtual adapters, VPN tunnels (Tailscale, TAP/TUN), WSL, and Wi-Fi Direct.
    """
    if sys.platform != "win32":
        return ["MockInterface"]

    interfaces = []
    try:
        output = subprocess.check_output(
            ["netsh", "interface", "ipv4", "show", "interfaces"],
            stderr=subprocess.DEVNULL,
            text=True
        )
        for line in output.splitlines():
            line = line.strip()
            if "connected" in line.lower():
                parts = line.split()
                if len(parts) >= 5:
                    iface_name = " ".join(parts[4:])
                    lower_name = iface_name.lower()
                    if "*" in iface_name or any(v in lower_name for v in [
                        "loopback", "tailscale", "tap", "tun", "wsl", "hyper-v",
                        "virtual", "vmware", "vethernet", "pseudo", "direct"
                    ]):
                        continue
                    if iface_name and iface_name not in interfaces:
                        interfaces.append(iface_name)
    except Exception as e:
        logger.warning(f"Could not discover network interfaces via netsh: {e}")
        interfaces = ["Wi-Fi", "Ethernet"]

    return interfaces or ["Wi-Fi"]


def flush_dns_cache() -> bool:
    """Flush the Windows local DNS resolver cache to clear pre-existing IP records."""
    if sys.platform != "win32":
        return True

    try:
        res = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True, timeout=5)
        logger.info("[DNS] Đã làm mới bộ nhớ đệm DNS hệ thống (ipconfig /flushdns).")
        return res.returncode == 0
    except Exception as e:
        logger.warning(f"[DNS] Không thể flush DNS cache: {e}")
        return False


def reset_browser_connections() -> int:
    """Reset active HTTP/HTTPS browser sockets and internal DNS cache.
    
    When parent updates domain blocklist while a child has a site open, modern browsers
    (Chrome, Edge, Brave, CocCoc, Opera) keep open persistent HTTP/2 and HTTP/3 (QUIC) sockets
    and maintain their own internal DNS cache inside their dedicated NetworkService utility process.
    
    Terminating ONLY the Chromium network utility process (network.mojom.NetworkService):
    1. Instantly clears all persistent HTTP/1.1, HTTP/2, HTTP/3 (QUIC) sockets and internal DNS cache.
    2. Does NOT close or crash any tabs or browser windows (the browser automatically and silently
       spawns a fresh NetworkService process in milliseconds).
    3. Guarantees that on the very next refresh (F5), the browser is forced to perform a new DNS lookup
       and immediately hits the DNS sinkhole / hosts file (0.0.0.0 / ::1).
       
    Also executes Windows iphlpapi.SetTcpEntry for any remaining TCP connections and flushes
    the Windows DNS resolver cache.
    """
    if sys.platform != "win32":
        return 0

    count = 0
    browser_names = ("chrome", "msedge", "brave", "coccoc", "opera", "firefox")
    browser_executables = {"chrome.exe", "msedge.exe", "brave.exe", "coccoc.exe", "opera.exe"}

    # 1. Reset Chromium internal network sockets & DNS cache via NetworkService termination
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = (proc.info.get('name') or '').lower()
                if proc_name in browser_executables:
                    cmd_list = proc.cmdline() or []
                    cmd_str = ' '.join(cmd_list).lower()
                    if 'network.mojom.networkservice' in cmd_str:
                        proc.kill()
                        count += 1
                        logger.info(f"[DNS] Đã làm mới NetworkService của '{proc_name}' (PID {proc.pid}) để xóa sạch socket/cache.")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            except Exception:
                pass
    except Exception as e:
        logger.debug(f"[DNS] Lỗi khi làm mới Chromium NetworkService: {e}")

    # 2. Reset active TCP entries using iphlpapi.SetTcpEntry (for other browsers / TCP sockets)
    try:
        import ctypes
        import socket
        from ctypes import wintypes

        class MIB_TCPROW(ctypes.Structure):
            _fields_ = [
                ("dwState", wintypes.DWORD),
                ("dwLocalAddr", wintypes.DWORD),
                ("dwLocalPort", wintypes.DWORD),
                ("dwRemoteAddr", wintypes.DWORD),
                ("dwRemotePort", wintypes.DWORD),
            ]

        MIB_TCP_STATE_DELETE_TCB = 12
        set_tcp_entry = ctypes.windll.iphlpapi.SetTcpEntry

        browser_pids = set()
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name']):
                name = (proc.info.get('name') or '').lower()
                if any(b in name for b in browser_names):
                    browser_pids.add(proc.info['pid'])

            for conn in psutil.net_connections(kind='tcp'):
                if conn.pid in browser_pids and conn.status == 'ESTABLISHED' and conn.raddr:
                    if conn.raddr.port in (80, 443, 8080, 8443):
                        try:
                            row = MIB_TCPROW(
                                dwState=MIB_TCP_STATE_DELETE_TCB,
                                dwLocalAddr=int.from_bytes(socket.inet_aton(conn.laddr.ip), 'little'),
                                dwLocalPort=socket.htons(conn.laddr.port),
                                dwRemoteAddr=int.from_bytes(socket.inet_aton(conn.raddr.ip), 'little'),
                                dwRemotePort=socket.htons(conn.raddr.port)
                            )
                            if set_tcp_entry(ctypes.byref(row)) == 0:
                                count += 1
                        except Exception:
                            pass
        except Exception:
            pass
    except Exception as e:
        logger.debug(f"[DNS] Không thể reset socket trình duyệt: {e}")

    # 3. Always flush Windows DNS cache
    flush_dns_cache()

    if count > 0:
        logger.info(f"[DNS] Đã làm mới {count} tiến trình/socket mạng trình duyệt để áp dụng chặn tức thì.")

    return count


SAVED_SYSTEM_DNS: List[str] = []


def set_dns_to_localhost(interface_name: Optional[str] = None) -> bool:
    """Configure network adapter DNS to 127.0.0.1 (IPv4) with backup fallback (T3_036)."""
    if sys.platform != "win32":
        logger.info(f"[SIMULATED] Set DNS to 127.0.0.1 on {interface_name or 'MockInterface'}")
        return True

    targets = [interface_name] if interface_name else get_active_interfaces()
    success = False

    global SAVED_SYSTEM_DNS
    for iface in targets:
        # Ghi nhận DNS gốc của hệ thống trước khi trỏ loopback để làm fallback
        try:
            from .dns_watchdog import get_adapter_dns_servers
        except ImportError:
            try:
                from dns_watchdog import get_adapter_dns_servers
            except ImportError:
                get_adapter_dns_servers = None

        if get_adapter_dns_servers:
            try:
                for s in get_adapter_dns_servers(iface):
                    if s and not s.startswith("127.") and s not in SAVED_SYSTEM_DNS:
                        SAVED_SYSTEM_DNS.append(s)
            except Exception:
                pass

        # 1. Set IPv4 DNS to 127.0.0.1
        try:
            cmd = f'netsh interface ipv4 set dns name="{iface}" static 127.0.0.1 primary'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                logger.info(f"[DNS] Đã trỏ IPv4 DNS trên '{iface}' về 127.0.0.1.")
                success = True
                # Thêm DNS dự phòng (secondary) từ DNS router/8.8.8.8 để bảo hiểm máy con không bao giờ mất mạng
                backup_dns = SAVED_SYSTEM_DNS[0] if SAVED_SYSTEM_DNS else "8.8.8.8"
                try:
                    cmd_sec = f'netsh interface ipv4 add dns name="{iface}" {backup_dns} index=2 validate=no'
                    subprocess.run(cmd_sec, shell=True, capture_output=True, text=True)
                except Exception:
                    pass
            else:
                logger.warning(f"[DNS] netsh ipv4 trả về mã {res.returncode} cho '{iface}': {res.stderr.strip()}")
        except Exception as e:
            logger.error(f"[DNS] Lỗi cấu hình IPv4 DNS cho '{iface}': {e}")

        # 2. Xử lý IPv6: Chỉ trỏ ::1 nếu socket IPv6 53 có mở, tránh blackhole mạng
        try:
            import socket
            v6_ok = False
            try:
                s6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
                s6.connect(("::1", 53))
                s6.close()
                v6_ok = True
            except Exception:
                v6_ok = False

            if v6_ok:
                cmd_v6 = f'netsh interface ipv6 set dnsservers name="{iface}" static ::1 primary'
                subprocess.run(cmd_v6, shell=True, capture_output=True, text=True)
            else:
                cmd_v6_dhcp = f'netsh interface ipv6 set dnsservers name="{iface}" dhcp'
                subprocess.run(cmd_v6_dhcp, shell=True, capture_output=True, text=True)
        except Exception:
            pass

    # 3. Disable browser DoH and flush cache
    disable_browser_doh()
    flush_dns_cache()

    return success


def restore_dns_to_dhcp(interface_name: Optional[str] = None) -> bool:
    """Restore network adapter DNS to automatic DHCP (T3_036) and clean up policies."""
    if sys.platform != "win32":
        logger.info(f"[SIMULATED] Restore DNS to DHCP on {interface_name or 'MockInterface'}")
        return True

    targets = [interface_name] if interface_name else get_active_interfaces()
    success = False

    for iface in targets:
        try:
            cmd = f'netsh interface ipv4 set dns name="{iface}" dhcp'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                logger.info(f"[DNS] Đã khôi phục IPv4 DNS trên '{iface}' về DHCP.")
                success = True
        except Exception as e:
            logger.error(f"[DNS] Lỗi khôi phục DHCP IPv4 cho '{iface}': {e}")

        try:
            cmd_v6 = f'netsh interface ipv6 set dnsservers name="{iface}" dhcp'
            subprocess.run(cmd_v6, shell=True, capture_output=True, text=True)
        except Exception:
            pass

    # Clean up hosts file and DNS cache (Note: Browser policies remain locked until full uninstall)
    restore_hosts_file()
    flush_dns_cache()

    return success


def disable_browser_doh() -> bool:
    """Apply browser protective policies (Disable Incognito, Disable Tor, Disable DoH, Enforce SafeSearch).
    Enforces policies across Chrome, Edge, Brave, Firefox, and CocCoc in both HKLM and HKCU.
    Uses both winreg API and native reg.exe for 64-bit and 32-bit views.
    """
    if sys.platform != "win32":
        return True

    try:
        import winreg

        browser_policies = {
            r"SOFTWARE\Policies\Google\Chrome": {
                ("DnsOverHttpsMode", winreg.REG_SZ): "off",
                ("IncognitoModeAvailability", winreg.REG_DWORD): 1,  # 1 = Disabled
                ("QuicAllowed", winreg.REG_DWORD): 0,               # 0 = Disabled (forces standard TCP/TLS for instant DNS enforcement)
                ("ForceGoogleSafeSearch", winreg.REG_DWORD): 1,
                ("ForceYouTubeSafetyMode", winreg.REG_DWORD): 2,
            },
            r"SOFTWARE\Policies\Microsoft\Edge": {
                ("DnsOverHttpsMode", winreg.REG_SZ): "off",
                ("InPrivateModeAvailability", winreg.REG_DWORD): 1,  # 1 = Disabled
                ("QuicAllowed", winreg.REG_DWORD): 0,
                ("ForceGoogleSafeSearch", winreg.REG_DWORD): 1,
                ("ForceBingSafeSearch", winreg.REG_DWORD): 1,
                ("ForceYouTubeSafetyMode", winreg.REG_DWORD): 2,
            },
            r"SOFTWARE\Policies\BraveSoftware\Brave": {
                ("DnsOverHttpsMode", winreg.REG_SZ): "off",
                ("IncognitoModeAvailability", winreg.REG_DWORD): 1,  # 1 = Disabled
                ("TorDisabled", winreg.REG_DWORD): 1,               # 1 = Disable Tor Window
                ("QuicAllowed", winreg.REG_DWORD): 0,
                ("ForceGoogleSafeSearch", winreg.REG_DWORD): 1,
                ("ForceYouTubeSafetyMode", winreg.REG_DWORD): 2,
            },
            r"SOFTWARE\Policies\Mozilla\Firefox": {
                ("DisablePrivateBrowsing", winreg.REG_DWORD): 1,
            },
            r"SOFTWARE\Policies\CocCoc\Browser": {
                ("DnsOverHttpsMode", winreg.REG_SZ): "off",
                ("IncognitoModeAvailability", winreg.REG_DWORD): 1,
                ("QuicAllowed", winreg.REG_DWORD): 0,
                ("ForceGoogleSafeSearch", winreg.REG_DWORD): 1,
            }
        }

        # 1. Direct Windows API (winreg)
        for root_hkey in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            for subkey, values in browser_policies.items():
                key = None
                for access_flag in (winreg.KEY_WRITE, winreg.KEY_WRITE | getattr(winreg, "KEY_WOW64_64KEY", 0), winreg.KEY_SET_VALUE):
                    try:
                        key = winreg.CreateKeyEx(root_hkey, subkey, 0, access_flag)
                        break
                    except Exception:
                        pass
                if not key:
                    continue
                try:
                    for (val_name, val_type), val_data in values.items():
                        try:
                            winreg.SetValueEx(key, val_name, 0, val_type, val_data)
                        except Exception:
                            pass
                finally:
                    winreg.CloseKey(key)

        # 2. Native reg.exe fallback across both 64-bit and 32-bit hives
        for root_str in ("HKLM", "HKCU"):
            for subkey, values in browser_policies.items():
                for (val_name, val_type), val_data in values.items():
                    type_str = "REG_DWORD" if val_type == winreg.REG_DWORD else "REG_SZ"
                    for view_flag in ("/reg:64", "/reg:32"):
                        try:
                            subprocess.run(
                                f'reg add "{root_str}\\{subkey}" /v "{val_name}" /t {type_str} /d "{val_data}" /f {view_flag}',
                                shell=True,
                                capture_output=True
                            )
                        except Exception:
                            pass

        return True
    except Exception as e:
        logger.debug(f"[DNS] Could not write browser protective policies: {e}")
        return False


def restore_browser_doh() -> bool:
    """Remove browser protective policy overrides from Windows Registry upon agent uninstallation."""
    if sys.platform != "win32":
        return True

    try:
        import winreg
        browser_policies = {
            r"SOFTWARE\Policies\Google\Chrome": [
                "DnsOverHttpsMode", "IncognitoModeAvailability", "QuicAllowed", "ForceGoogleSafeSearch", "ForceYouTubeSafetyMode"
            ],
            r"SOFTWARE\Policies\Microsoft\Edge": [
                "DnsOverHttpsMode", "InPrivateModeAvailability", "QuicAllowed", "ForceGoogleSafeSearch", "ForceBingSafeSearch", "ForceYouTubeSafetyMode"
            ],
            r"SOFTWARE\Policies\BraveSoftware\Brave": [
                "DnsOverHttpsMode", "IncognitoModeAvailability", "TorDisabled", "QuicAllowed", "ForceGoogleSafeSearch", "ForceYouTubeSafetyMode"
            ],
            r"SOFTWARE\Policies\Mozilla\Firefox": [
                "DisablePrivateBrowsing"
            ],
            r"SOFTWARE\Policies\CocCoc\Browser": [
                "DnsOverHttpsMode", "IncognitoModeAvailability", "QuicAllowed", "ForceGoogleSafeSearch"
            ]
        }

        # 1. Direct winreg delete
        for root_hkey in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            for subkey, val_names in browser_policies.items():
                try:
                    with winreg.OpenKey(root_hkey, subkey, 0, winreg.KEY_SET_VALUE) as key:
                        for val_name in val_names:
                            try:
                                winreg.DeleteValue(key, val_name)
                            except Exception:
                                pass
                except Exception:
                    pass

        # 2. Native reg.exe delete fallback across both 64-bit and 32-bit hives
        for root_str in ("HKLM", "HKCU"):
            for subkey, val_names in browser_policies.items():
                for val_name in val_names:
                    for view_flag in ("/reg:64", "/reg:32"):
                        try:
                            subprocess.run(
                                f'reg delete "{root_str}\\{subkey}" /v "{val_name}" /f {view_flag}',
                                shell=True,
                                capture_output=True
                            )
                        except Exception:
                            pass
        return True
    except Exception as e:
        return False


def sync_hosts_file(blocked_domains: Iterable[str], hosts_path: str = WINDOWS_HOSTS_PATH) -> bool:
    """Synchronize blocked domains into Windows hosts file as bulletproof defense-in-depth (F2).
    
    Guarantees that blocked domains resolve to 0.0.0.0 at the Windows OS socket layer,
    even before any network query is made.
    """
    if sys.platform != "win32" and hosts_path == WINDOWS_HOSTS_PATH:
        # Simulated environment
        return True

    if not os.path.exists(hosts_path):
        return False

    try:
        with open(hosts_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Remove existing OGK block if present
        pattern = re.compile(re.escape(HOSTS_MARKER_START) + r".*?" + re.escape(HOSTS_MARKER_END), re.DOTALL)
        clean_content = pattern.sub("", content).strip()

        # Build new OGK block
        unique_domains = sorted({d.strip().lower() for d in blocked_domains if d.strip()})
        if not unique_domains:
            # Nothing to add, just save clean content
            with open(hosts_path, "w", encoding="utf-8") as f:
                f.write(clean_content + "\n")
            return True

        block_lines = [HOSTS_MARKER_START]
        for d in unique_domains:
            block_lines.append(f"0.0.0.0 {d}")
            block_lines.append(f"::1 {d}")
            if not d.startswith("www."):
                block_lines.append(f"0.0.0.0 www.{d}")
                block_lines.append(f"::1 www.{d}")
        block_lines.append(HOSTS_MARKER_END)

        new_content = clean_content + "\n\n" + "\n".join(block_lines) + "\n"

        with open(hosts_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        flush_dns_cache()
        logger.info(f"[HOSTS] Đã ghi nhận {len(unique_domains)} tên miền chặn vào file hosts Windows.")
        return True
    except PermissionError:
        logger.warning("[HOSTS] Cần quyền Administrator để đồng bộ file hosts Windows.")
        return False
    except Exception as e:
        logger.error(f"[HOSTS] Lỗi cập nhật file hosts: {e}")
        return False


def restore_hosts_file(hosts_path: str = WINDOWS_HOSTS_PATH) -> bool:
    """Remove Open Guardian Kids blocked domain block from Windows hosts file."""
    if sys.platform != "win32" and hosts_path == WINDOWS_HOSTS_PATH:
        return True

    if not os.path.exists(hosts_path):
        return False

    try:
        with open(hosts_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        pattern = re.compile(re.escape(HOSTS_MARKER_START) + r".*?" + re.escape(HOSTS_MARKER_END), re.DOTALL)
        clean_content = pattern.sub("", content).strip()

        with open(hosts_path, "w", encoding="utf-8") as f:
            f.write(clean_content + "\n")

        flush_dns_cache()
        logger.info("[HOSTS] Đã khôi phục file hosts Windows về trạng thái ban đầu.")
        return True
    except Exception as e:
        logger.debug(f"[HOSTS] Lỗi khôi phục file hosts: {e}")
        return False
