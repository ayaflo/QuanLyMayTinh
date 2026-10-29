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


def set_dns_to_localhost(interface_name: Optional[str] = None) -> bool:
    """Configure network adapter DNS to 127.0.0.1 (IPv4) and ::1 (IPv6) (T3_036)."""
    if sys.platform != "win32":
        logger.info(f"[SIMULATED] Set DNS to 127.0.0.1 on {interface_name or 'MockInterface'}")
        return True

    targets = [interface_name] if interface_name else get_active_interfaces()
    success = False

    for iface in targets:
        # 1. Set IPv4 DNS to 127.0.0.1
        try:
            cmd = f'netsh interface ipv4 set dns name="{iface}" static 127.0.0.1 primary'
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                logger.info(f"[DNS] Đã trỏ IPv4 DNS trên '{iface}' về 127.0.0.1.")
                success = True
            else:
                logger.warning(f"[DNS] netsh ipv4 trả về mã {res.returncode} cho '{iface}': {res.stderr.strip()}")
        except Exception as e:
            logger.error(f"[DNS] Lỗi cấu hình IPv4 DNS cho '{iface}': {e}")

        # 2. Set IPv6 DNS to ::1 (loopback) to prevent IPv6 DNS bypass
        try:
            cmd_v6 = f'netsh interface ipv6 set dnsservers name="{iface}" static ::1 primary'
            subprocess.run(cmd_v6, shell=True, capture_output=True, text=True)
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

    # Clean up browser policies and hosts file
    restore_browser_doh()
    restore_hosts_file()
    flush_dns_cache()

    return success


def disable_browser_doh() -> bool:
    """Apply browser protective policies (Disable Incognito, Disable Tor, Disable DoH, Enforce SafeSearch).
    Enforces policies across Chrome, Edge, Brave, Firefox, and CocCoc in both HKLM and HKCU.
    """
    if sys.platform != "win32":
        return True

    try:
        import winreg

        browser_policies = {
            r"SOFTWARE\Policies\Google\Chrome": {
                ("DnsOverHttpsMode", winreg.REG_SZ): "off",
                ("IncognitoModeAvailability", winreg.REG_DWORD): 1,  # 1 = Disabled
                ("ForceGoogleSafeSearch", winreg.REG_DWORD): 1,
                ("ForceYouTubeSafetyMode", winreg.REG_DWORD): 2,
            },
            r"SOFTWARE\Policies\Microsoft\Edge": {
                ("DnsOverHttpsMode", winreg.REG_SZ): "off",
                ("InPrivateModeAvailability", winreg.REG_DWORD): 1,  # 1 = Disabled
                ("ForceGoogleSafeSearch", winreg.REG_DWORD): 1,
                ("ForceBingSafeSearch", winreg.REG_DWORD): 1,
                ("ForceYouTubeSafetyMode", winreg.REG_DWORD): 2,
            },
            r"SOFTWARE\Policies\BraveSoftware\Brave": {
                ("DnsOverHttpsMode", winreg.REG_SZ): "off",
                ("IncognitoModeAvailability", winreg.REG_DWORD): 1,  # 1 = Disabled
                ("TorDisabled", winreg.REG_DWORD): 1,               # 1 = Disable Tor Window
                ("ForceGoogleSafeSearch", winreg.REG_DWORD): 1,
                ("ForceYouTubeSafetyMode", winreg.REG_DWORD): 2,
            },
            r"SOFTWARE\Policies\Mozilla\Firefox": {
                ("DisablePrivateBrowsing", winreg.REG_DWORD): 1,
            },
            r"SOFTWARE\Policies\CocCoc\Browser": {
                ("DnsOverHttpsMode", winreg.REG_SZ): "off",
                ("IncognitoModeAvailability", winreg.REG_DWORD): 1,
                ("ForceGoogleSafeSearch", winreg.REG_DWORD): 1,
            }
        }

        for root_hkey in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            for subkey, values in browser_policies.items():
                try:
                    key = winreg.CreateKeyEx(root_hkey, subkey, 0, winreg.KEY_SET_VALUE)
                    for (val_name, val_type), val_data in values.items():
                        try:
                            winreg.SetValueEx(key, val_name, 0, val_type, val_data)
                        except Exception:
                            pass
                    winreg.CloseKey(key)
                except Exception:
                    pass
        return True
    except Exception as e:
        logger.debug(f"[DNS] Could not write browser protective policies: {e}")
        return False


def restore_browser_doh() -> bool:
    """Remove browser protective policy overrides from Windows Registry upon agent shutdown."""
    if sys.platform != "win32":
        return True

    try:
        import winreg
        browser_policies = {
            r"SOFTWARE\Policies\Google\Chrome": [
                "DnsOverHttpsMode", "IncognitoModeAvailability", "ForceGoogleSafeSearch", "ForceYouTubeSafetyMode"
            ],
            r"SOFTWARE\Policies\Microsoft\Edge": [
                "DnsOverHttpsMode", "InPrivateModeAvailability", "ForceGoogleSafeSearch", "ForceBingSafeSearch", "ForceYouTubeSafetyMode"
            ],
            r"SOFTWARE\Policies\BraveSoftware\Brave": [
                "DnsOverHttpsMode", "IncognitoModeAvailability", "TorDisabled", "ForceGoogleSafeSearch", "ForceYouTubeSafetyMode"
            ],
            r"SOFTWARE\Policies\Mozilla\Firefox": [
                "DisablePrivateBrowsing"
            ],
            r"SOFTWARE\Policies\CocCoc\Browser": [
                "DnsOverHttpsMode", "IncognitoModeAvailability", "ForceGoogleSafeSearch"
            ]
        }

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
            if not d.startswith("www."):
                block_lines.append(f"0.0.0.0 www.{d}")
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
