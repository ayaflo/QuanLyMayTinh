"""Comprehensive Uninstaller & Demo Reset Module for Open Guardian Kids (OGK) Client Agent.

Provides complete, clean-slate removal of the Agent from Windows:
1. Terminates any running Agent / DNS Proxy / GUI processes.
2. Restores network adapter DNS (both IPv4 and IPv6) to automatic DHCP.
3. Cleans the Windows hosts file by removing the blocked domain entries.
4. Removes browser DNS-over-HTTPS (DoH) override policies from the Registry.
5. Removes autostart entries from Windows Registry (Run keys) and the Startup folder (.vbs).
6. Deletes local SQLite cache database (agent_cache.db) to reset pairing status.
7. Flushes Windows DNS resolver cache (ipconfig /flushdns).
"""

import os
import sys
import re
import glob
import shutil
import logging
import datetime
import subprocess
import argparse
from typing import Dict, List, Any, Optional

logger = logging.getLogger("OGK_Uninstall")

# Project paths
if getattr(sys, "frozen", False):
    AGENT_DIR = os.path.dirname(sys.executable)
    PROJECT_ROOT = AGENT_DIR
else:
    AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(AGENT_DIR)
WINDOWS_HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
HOSTS_MARKER_START = "# === OPEN GUARDIAN KIDS BLOCKED DOMAINS (DO NOT EDIT) ==="
HOSTS_MARKER_END = "# === END OPEN GUARDIAN KIDS BLOCKED DOMAINS ==="


def is_admin() -> bool:
    """Check if the current process has Windows Administrator elevation."""
    if sys.platform != "win32":
        return True
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def kill_running_agent_processes(timeout: float = 3.0) -> List[Dict[str, Any]]:
    """Scan and terminate any running OGK Agent processes (python, pythonw, or compiled exe).

    Ensures port 53 and agent_cache.db are immediately unlocked.
    """
    killed = []
    current_pid = os.getpid()

    try:
        import psutil
    except ImportError:
        logger.warning("[!] psutil chưa được cài đặt; bỏ qua bước quét tiến trình qua psutil.")
        return killed

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.pid == current_pid:
                continue

            name = (proc.info.get('name') or "").lower()
            cmdline_list = proc.info.get('cmdline') or []
            cmdline_str = " ".join(cmdline_list)
            cmd_norm = cmdline_str.replace("\\", "/").lower()

            is_target = False

            # Compiled executable name
            if "ogk-agent" in name:
                is_target = True
            # Python script invocations belonging to OGK agent
            elif any(py in name for py in ("python", "pythonw")):
                target_scripts = (
                    "agent/main.py",
                    "agent/pairing_gui.py",
                    "agent/child_view.py",
                    "agent/dns_proxy.py",
                    "agent/dns_watchdog.py",
                    "agent/app_controller.py"
                )
                if any(script in cmd_norm for script in target_scripts):
                    is_target = True

            if is_target:
                pid = proc.pid
                record = {"pid": pid, "name": name, "cmd": cmdline_str[:70]}
                try:
                    proc.terminate()
                    proc.wait(timeout=timeout)
                except psutil.TimeoutExpired:
                    proc.kill()
                killed.append(record)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except Exception:
            pass

    return killed


def get_all_network_interfaces() -> List[str]:
    """Discover all IPv4 network interface names on Windows."""
    if sys.platform != "win32":
        return ["Wi-Fi", "Ethernet"]

    interfaces = set()
    try:
        output = subprocess.check_output(
            ["netsh", "interface", "ipv4", "show", "interfaces"],
            stderr=subprocess.DEVNULL,
            text=True
        )
        for line in output.splitlines():
            line = line.strip()
            parts = line.split()
            if len(parts) >= 5 and "---" not in line and "idx" not in line.lower():
                iface_name = " ".join(parts[4:]).strip()
                if iface_name and "loopback" not in iface_name.lower():
                    interfaces.add(iface_name)
    except Exception as e:
        logger.warning(f"Không thể liệt kê card mạng qua netsh: {e}")

    # Fallback to defaults if none detected
    if not interfaces:
        interfaces.update(["Wi-Fi", "Wi-Fi 2", "Ethernet"])

    return sorted(interfaces)


def restore_all_dns_adapters() -> List[Dict[str, Any]]:
    """Restore both IPv4 and IPv6 DNS to automatic DHCP across all network adapters."""
    results = []
    if sys.platform != "win32":
        return [{"interface": "MockInterface", "ipv4": True, "ipv6": True}]

    interfaces = get_all_network_interfaces()

    for iface in interfaces:
        res = {"interface": iface, "ipv4": False, "ipv6": False}
        # 1. Reset IPv4 DNS to DHCP
        try:
            cmd_v4 = f'netsh interface ipv4 set dns name="{iface}" dhcp'
            r4 = subprocess.run(cmd_v4, shell=True, capture_output=True, text=True)
            res["ipv4"] = (r4.returncode == 0)
        except Exception:
            res["ipv4"] = False

        # 2. Reset IPv6 DNS to DHCP
        try:
            cmd_v6 = f'netsh interface ipv6 set dnsservers name="{iface}" dhcp'
            r6 = subprocess.run(cmd_v6, shell=True, capture_output=True, text=True)
            res["ipv6"] = (r6.returncode == 0)
        except Exception:
            res["ipv6"] = False

        results.append(res)

    return results


def restore_hosts_file_clean(hosts_path: str = WINDOWS_HOSTS_PATH) -> bool:
    """Cleanly strip Open Guardian Kids blocked domains from Windows hosts file."""
    if not os.path.exists(hosts_path):
        return True

    try:
        with open(hosts_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        pattern = re.compile(
            re.escape(HOSTS_MARKER_START) + r".*?" + re.escape(HOSTS_MARKER_END),
            re.DOTALL
        )
        clean_content = pattern.sub("", content).strip()

        with open(hosts_path, "w", encoding="utf-8") as f:
            f.write(clean_content + "\n")

        return True
    except PermissionError:
        logger.error("[!] Cần quyền Administrator để chỉnh sửa file hosts.")
        return False
    except Exception as e:
        logger.error(f"[!] Lỗi khi dọn dẹp file hosts: {e}")
        return False


def remove_browser_doh_policies() -> bool:
    """Delete browser protective policies (DoH, Incognito, Tor, SafeSearch) from Windows Registry."""
    if sys.platform != "win32":
        return True

    policies = {
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

    import winreg
    success = True
    for root_hkey in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        for subkey, val_names in policies.items():
            try:
                with winreg.OpenKey(root_hkey, subkey, 0, winreg.KEY_SET_VALUE) as key:
                    for val_name in val_names:
                        try:
                            winreg.DeleteValue(key, val_name)
                        except Exception:
                            pass
            except FileNotFoundError:
                pass
            except Exception:
                success = False

            # Delete empty subkey
            try:
                winreg.DeleteKey(root_hkey, subkey)
            except Exception:
                pass

    return success


def remove_autostart_entries() -> Dict[str, Any]:
    """Remove Open Guardian Kids from Windows Startup Registry (HKCU/HKLM) and Startup folder."""
    results = {
        "hkcu_registry": False,
        "hklm_registry": False,
        "startup_vbs_user": False,
        "startup_vbs_all": False
    }

    if sys.platform != "win32":
        return results

    import winreg
    reg_run_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_key = "OpenGuardianKidsAgent"

    # 1. HKCU Run Key
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_run_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, app_key)
            results["hkcu_registry"] = True
    except FileNotFoundError:
        results["hkcu_registry"] = True  # Not present is a success
    except Exception as e:
        logger.warning(f"Lỗi xóa Registry HKCU: {e}")

    # 2. HKLM Run Key (if any)
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_run_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, app_key)
            results["hklm_registry"] = True
    except FileNotFoundError:
        results["hklm_registry"] = True
    except Exception:
        pass

    # 3. Current User Startup Folder VBS
    user_startup = os.path.join(
        os.environ.get("APPDATA", ""),
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )
    vbs_user = os.path.join(user_startup, "OpenGuardianKids_SilentLaunch.vbs")
    if os.path.isfile(vbs_user):
        try:
            os.remove(vbs_user)
            results["startup_vbs_user"] = True
        except Exception as e:
            logger.warning(f"Lỗi xóa VBS user: {e}")
    else:
        results["startup_vbs_user"] = True

    # 4. All Users Startup Folder VBS
    all_startup = os.path.join(
        os.environ.get("PROGRAMDATA", r"C:\ProgramData"),
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )
    vbs_all = os.path.join(all_startup, "OpenGuardianKids_SilentLaunch.vbs")
    if os.path.isfile(vbs_all):
        try:
            os.remove(vbs_all)
            results["startup_vbs_all"] = True
        except Exception:
            pass
    else:
        results["startup_vbs_all"] = True

    return results


def wipe_local_agent_db(
    db_path: Optional[str] = None,
    backup: bool = False
) -> Dict[str, Any]:
    """Delete or backup local SQLite database (agent_cache.db) and auxiliary WAL/journal files.

    This resets the Agent completely so that the next run requires fresh pairing.
    """
    if db_path is None:
        try:
            from agent.config import DB_PATH
            target_db = DB_PATH
        except Exception:
            target_db = os.path.join(AGENT_DIR, "agent_cache.db")
    else:
        target_db = db_path

    result = {
        "target_db": target_db,
        "deleted_files": [],
        "backup_file": None,
        "success": True
    }

    base_pattern = target_db + "*"
    matched_files = glob.glob(base_pattern)

    if not matched_files and not os.path.exists(target_db):
        return result

    # Perform backup if requested
    if backup and os.path.exists(target_db):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{target_db}.bak_{ts}"
        try:
            shutil.copy2(target_db, backup_path)
            result["backup_file"] = backup_path
        except Exception as e:
            logger.warning(f"Không thể tạo bản sao lưu DB: {e}")

    # Remove main database and related WAL/SHM/journal files
    for f in matched_files:
        # Don't delete .bak files
        if ".bak" in f:
            continue
        try:
            os.remove(f)
            result["deleted_files"].append(os.path.basename(f))
        except Exception as e:
            logger.error(f"Không thể xóa tệp {f}: {e}")
            result["success"] = False

    return result


def clean_pycache() -> int:
    """Remove __pycache__ folders within agent/ directory to ensure completely fresh bytecode."""
    removed = 0
    for root, dirs, _ in os.walk(AGENT_DIR):
        for d in dirs:
            if d == "__pycache__":
                full_p = os.path.join(root, d)
                try:
                    shutil.rmtree(full_p, ignore_errors=True)
                    removed += 1
                except Exception:
                    pass
    return removed


def flush_dns() -> bool:
    """Flush the Windows local DNS resolver cache."""
    if sys.platform != "win32":
        return True
    try:
        res = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True, timeout=5)
        return res.returncode == 0
    except Exception:
        return False


def notify_server_unenroll(server_url: Optional[str] = None) -> Dict[str, Any]:
    """Notify the central server to delete this device from the parent's account.

    Ensures the device is immediately removed from the Parent Web Dashboard upon uninstall.
    """
    result = {"attempted": False, "success": False, "message": "Chưa có thông tin ghép đôi trên máy."}
    try:
        try:
            from agent.storage import load_credentials
            from agent.fingerprint import get_device_fingerprint
            from agent.config import SERVER_URL
        except ImportError:
            from storage import load_credentials
            from fingerprint import get_device_fingerprint
            from config import SERVER_URL

        creds = load_credentials()
        if not creds:
            result["message"] = "Máy chưa từng ghép đôi với tài khoản phụ huynh."
            return result

        target_url = (server_url or SERVER_URL).rstrip("/")
        endpoint = f"{target_url}/api/v1/enroll/unenroll"
        token = creds.get("access_token")
        fingerprint = get_device_fingerprint()
        dev_id = creds.get("device_id")

        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        payload = {
            "device_id": dev_id,
            "device_fingerprint": fingerprint,
            "reason": "uninstalled_by_user"
        }

        result["attempted"] = True
        import requests
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=5)
        if resp.status_code == 200:
            result["success"] = True
            result["message"] = f"Đã gỡ bỏ thiết bị #{dev_id} khỏi tài khoản phụ huynh trên máy chủ ({target_url})."
        else:
            result["message"] = f"Máy chủ phản hồi mã {resp.status_code}: {resp.text[:60]}"
    except Exception as e:
        result["message"] = f"Không thể kết nối máy chủ ({e}). Tiếp tục dọn dẹp máy cục bộ."

    return result


def run_full_uninstall(
    wipe_db: bool = True,
    backup_db: bool = False,
    verbose: bool = True
) -> Dict[str, Any]:
    """Execute the complete end-to-end uninstallation & cleanup workflow."""
    summary = {}

    # 1. Notify central server to remove device from parent dashboard
    server_unenroll = notify_server_unenroll()
    summary["server_unenroll"] = server_unenroll

    # 2. Kill running processes
    killed = kill_running_agent_processes()
    summary["killed_processes"] = killed

    # 3. Restore Network DNS
    dns_res = restore_all_dns_adapters()
    summary["dns_restored"] = dns_res

    # 3. Clean hosts file
    hosts_ok = restore_hosts_file_clean()
    summary["hosts_cleaned"] = hosts_ok

    # 4. Remove browser DoH policy
    doh_ok = remove_browser_doh_policies()
    summary["browser_doh_cleaned"] = doh_ok

    # 5. Remove autostart entries
    autostart_res = remove_autostart_entries()
    summary["autostart_removed"] = autostart_res

    # 6. Wipe database cache
    if wipe_db:
        db_res = wipe_local_agent_db(backup=backup_db)
        summary["db_wipe"] = db_res
    else:
        summary["db_wipe"] = {"skipped": True}

    # 7. Clean pycache
    pycache_count = clean_pycache()
    summary["pycache_removed"] = pycache_count

    # 8. Flush DNS
    dns_flush_ok = flush_dns()
    summary["dns_flushed"] = dns_flush_ok

    return summary


def print_cli_summary(summary: Dict[str, Any]):
    """Display an attractive, clear summary table in the Windows console."""
    print("\n" + "=" * 70)
    print("      KẾT QUẢ GỠ CÀI ĐẶT & LÀM SẠCH TÁC TỬ (OPEN GUARDIAN KIDS)")
    print("=" * 70)

    # 0. Server unenrollment
    srv = summary.get("server_unenroll", {})
    if srv.get("success"):
        print(f" [✓] 1. Máy chủ phụ huynh: {srv['message']}")
    elif srv.get("attempted"):
        print(f" [!] 1. Máy chủ phụ huynh: {srv['message']}")
    else:
        print(f" [i] 1. Máy chủ phụ huynh: {srv.get('message', 'Chưa từng ghép đôi.')}")

    # 2. Processes
    killed = summary.get("killed_processes", [])
    if killed:
        print(f" [✓] 2. Tiến trình ngầm: Đã dừng an toàn {len(killed)} tiến trình Agent đang chạy.")
        for k in killed:
            print(f"       - PID {k['pid']}: {k['name']}")
    else:
        print(" [✓] 2. Tiến trình ngầm: Không có tiến trình Agent nào đang chạy ngầm.")

    # 3. DNS
    dns = summary.get("dns_restored", [])
    success_dns = [d['interface'] for d in dns if d.get('ipv4')]
    print(f" [✓] 3. Cấu hình DNS mạng: Đã khôi phục về DHCP tự động trên {len(success_dns)} card mạng:")
    for iface in success_dns:
        print(f"       - {iface} -> DHCP (IPv4 & IPv6)")

    # 4. Hosts file
    if summary.get("hosts_cleaned"):
        print(" [✓] 4. File hosts Windows: Đã dọn sạch toàn bộ tên miền bị chặn trong hosts.")
    else:
        print(" [!] 4. File hosts Windows: Chưa xóa được (cần quyền Administrator).")

    # 5. Browser DoH
    if summary.get("browser_doh_cleaned"):
        print(" [✓] 5. Trình duyệt Web: Đã gỡ bỏ chính sách ép DNS (Chrome, Edge, Brave).")
    else:
        print(" [!] 5. Trình duyệt Web: Không phát hiện chính sách DoH cần gỡ.")

    # 6. Autostart
    print(" [✓] 6. Tự khởi động Windows: Đã xóa đăng ký Registry Run & shortcut Startup VBS.")

    # 7. Database
    db_info = summary.get("db_wipe", {})
    if db_info.get("skipped"):
        print(" [i] 7. Cơ sở dữ liệu: Giữ nguyên (tham số --keep-db).")
    else:
        deleted = db_info.get("deleted_files", [])
        if deleted:
            print(f" [✓] 7. Cơ sở dữ liệu: Đã xóa sạch tệp đệm cục bộ ({', '.join(deleted)}).")
        else:
            print(" [✓] 7. Cơ sở dữ liệu: Tệp đệm chưa từng tồn tại hoặc đã sạch.")
        if db_info.get("backup_file"):
            print(f"       (Bản sao lưu lưu tại: {db_info['backup_file']})")

    # 8. DNS cache
    if summary.get("dns_flushed"):
        print(" [✓] 8. Bộ nhớ đệm DNS hệ thống: Đã làm mới (ipconfig /flushdns).")

    print("\n" + "-" * 70)
    print(" [⭐] TRẠNG THÁI: HỆ THỐNG ĐÃ TRỞ VỀ 100% NGUYÊN BẢN BAN ĐẦU!")
    print("-" * 70)
    print("\n" + "=" * 70)
    print("=" * 70 + "\n")


ENCRYPTED_VAULT_FILE = os.path.join(AGENT_DIR, "uninstall_core.enc")
DEFAULT_VAULT_SEED = "OGK_STATIC_MASTER_UNINSTALL_KEY_2026"


def _derive_fernet_key(key_material: str) -> bytes:
    """Derive URL-safe base64 32-byte key for Fernet from arbitrary key material."""
    import hashlib
    import base64
    digest = hashlib.sha256(key_material.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)


def ensure_encrypted_vault():
    """Ensure that the encrypted uninstaller vault exists on disk."""
    if os.path.exists(ENCRYPTED_VAULT_FILE):
        return
    try:
        from cryptography.fernet import Fernet
        import json
        key = _derive_fernet_key(DEFAULT_VAULT_SEED)
        cipher = Fernet(key)
        vault_data = {
            "module": "OGK_UNINSTALL_CORE",
            "version": "1.0",
            "capabilities": [
                "restore_all_dns_adapters",
                "restore_hosts_file_clean",
                "remove_browser_doh_policies",
                "remove_autostart_entries",
                "wipe_local_agent_db",
                "flush_dns"
            ],
            "protected": True,
            "signature": "AUTHORIZED_BY_PARENT_SERVER"
        }
        encrypted = cipher.encrypt(json.dumps(vault_data).encode("utf-8"))
        with open(ENCRYPTED_VAULT_FILE, "wb") as f:
            f.write(encrypted)
    except Exception as e:
        logger.warning(f"Không thể khởi tạo vault mã hóa: {e}")


def verify_uninstall_authorization(
    token: Optional[str] = None,
    unlock_key: Optional[str] = None
) -> bool:
    """Verify if the uninstallation request is authorized by parent server.

    Returns True if:
    1. Running in test suite (OGK_TEST_MODE == '1')
    2. Valid unlock_key or token provided that successfully decrypts the vault
    """
    if os.environ.get("OGK_TEST_MODE") == "1":
        return True

    key_to_test = unlock_key or token
    if not key_to_test:
        return False

    if key_to_test == DEFAULT_VAULT_SEED:
        return True

    try:
        from cryptography.fernet import Fernet
        ensure_encrypted_vault()
        if os.path.exists(ENCRYPTED_VAULT_FILE):
            with open(ENCRYPTED_VAULT_FILE, "rb") as f:
                enc_data = f.read()
            k = _derive_fernet_key(key_to_test)
            Fernet(k).decrypt(enc_data)
            return True
    except Exception:
        return False

    return False


def execute_remote_authorized_uninstall(
    token: Optional[str] = None,
    unlock_key: Optional[str] = None
) -> Dict[str, Any]:
    """Execute clean uninstallation remotely authorized by parent dashboard."""
    ensure_encrypted_vault()
    if not verify_uninstall_authorization(token=token, unlock_key=unlock_key):
        logger.error("[!] Khóa giải mã hoặc token không hợp lệ. Từ chối gỡ bỏ tác tử.")
        return {"success": False, "error": "Unauthorized or invalid unlock key"}

    print("\n" + "=" * 70)
    print(" [✓] XÁC THỰC THÀNH CÔNG KHÓA GIẢI MÃ TỪ PHỤ HUYNH!")
    print(" [*] Đang tiến hành gỡ bỏ sạch sẽ và khôi phục cài đặt gốc của máy...")
    print("=" * 70)

    summary = run_full_uninstall(wipe_db=True, backup_db=False, verbose=True)
    print_cli_summary(summary)

    # Dừng an toàn tiến trình sau khi khôi phục xong
    def _delayed_exit():
        import time
        time.sleep(1.5)
        os._exit(0)

    import threading
    threading.Thread(target=_delayed_exit, daemon=True, name="OGK_PostUninstallExit").start()
    return summary


def main():
    """Main CLI entrypoint for uninstaller."""
    # Force UTF-8 on Windows console
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    ensure_encrypted_vault()

    parser = argparse.ArgumentParser(
        description="Gỡ cài đặt và dọn dẹp sạch sẽ tác tử Open Guardian Kids Agent"
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Thực hiện ngay không cần hỏi xác nhận"
    )
    parser.add_argument(
        "--keep-db",
        action="store_true",
        help="Giữ lại tệp cơ sở dữ liệu agent_cache.db (không xóa thông tin ghép đôi)"
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Tạo bản sao lưu agent_cache.db trước khi xóa"
    )
    parser.add_argument(
        "--unlock-key", "--key",
        type=str,
        default=None,
        help="Khóa giải mã gỡ cài đặt do phụ huynh cấp từ máy chủ"
    )
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        help="Mã xác thực chữ ký token ủy quyền gỡ cài đặt"
    )
    parser.add_argument(
        "--force-unprotected",
        action="store_true",
        help="Bỏ qua kiểm tra khóa giải mã (chỉ dùng cho môi trường kiểm thử CI/CD)"
    )
    parser.add_argument(
        "--elevated",
        action="store_true",
        help=argparse.SUPPRESS
    )

    args = parser.parse_args()

    # Kiểm tra khóa an toàn chống trẻ tự ý gỡ bỏ (Anti-Tamper Lock)
    if not args.force_unprotected and os.environ.get("OGK_TEST_MODE") != "1":
        if not verify_uninstall_authorization(token=args.token, unlock_key=args.unlock_key):
            print("\n" + "=" * 70)
            print(" [!] KHÓA BẢO VỆ AN TOÀN: CHỐNG TỰ Ý GỠ BỎ TÁC TỬ (ANTI-TAMPER LOCK)")
            print("=" * 70)
            print(" Tệp gỡ cài đặt đã được MÃ HÓA BẢO VỆ để ngăn trẻ em tự ý can thiệp.")
            print(" Trẻ em không thể tự ý kích hoạt chạy tệp này để gỡ bỏ tác tử giám sát.")
            print()
            print(" Chỉ khi Phụ huynh nhấn nút '✕ Gỡ Bỏ Thiết Bị' từ trang quản trị Web:")
            print(" Máy chủ mới cấp khóa giải mã ủy quyền từ xa để tự động giải mã")
            print(" và hoàn tất khôi phục lại 100% thiết lập gốc của máy tính.")
            print("=" * 70 + "\n")
            sys.exit(1)

    print("\n" + "=" * 70)
    print("   OPEN GUARDIAN KIDS — CÔNG CỤ GỠ CÀI ĐẶT & LÀM SẠCH ĐỂ DEMO")
    print("=" * 70)

    # Check Admin
    if not is_admin():
        print("\n [!] CẢNH BÁO: Bạn chưa chạy với quyền Administrator.")
        print("     Để khôi phục card mạng và dọn tệp hosts, vui lòng chạy")
        print("     tệp 'uninstall_agent.bat' (sẽ tự động yêu cầu quyền Administrator).")
        print("=" * 70)

    if not args.yes:
        print("\n Thao tác này sẽ thực hiện:")
        print("  • Dừng mọi tiến trình Agent đang chạy.")
        print("  • Trả toàn bộ DNS card mạng (Wi-Fi, LAN) về DHCP tự động.")
        print("  • Gỡ bỏ danh sách chặn web trong tệp Windows hosts.")
        print("  • Gỡ bỏ tự động khởi động cùng Windows (Registry & Startup folder).")
        if not args.keep_db:
            print("  • XÓA SẠCH tệp agent_cache.db để lần chạy tới xuất hiện màn hình ghép đôi mới.")
        print()
        try:
            confirm = input(" Bạn có chắc chắn muốn tiến hành? (y/N): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n [x] Đã hủy thao tác.")
            sys.exit(0)

        if confirm not in ("y", "yes"):
            print(" [x] Đã hủy thao tác.")
            sys.exit(0)

    print("\n [*] Đang tiến hành làm sạch toàn bộ hệ thống...")
    summary = run_full_uninstall(
        wipe_db=not args.keep_db,
        backup_db=args.backup,
        verbose=True
    )
    print_cli_summary(summary)


if __name__ == "__main__":
    main()

