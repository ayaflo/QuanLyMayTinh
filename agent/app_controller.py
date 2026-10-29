"""Application Control Module for Open Guardian Kids (F2 & NT4).
Monitors running processes every 3-5 seconds, verifies binary SHA-256 hashes
to prevent rename-bypass, terminates unauthorized applications, and displays explanatory notices.
"""

import os
import sys
import time
import hashlib
import threading
import logging
from typing import Optional, Dict, Callable
import psutil

try:
    from .idle_detector import is_user_idle
except ImportError:
    try:
        from idle_detector import is_user_idle
    except ImportError:
        is_user_idle = lambda threshold=300.0: False

logger = logging.getLogger("OGK_AppController")


def get_foreground_process_name() -> Optional[str]:
    """Retrieve executable name of foreground window process on Windows.
    Adheres strictly to Principle NT2: only captures binary name (e.g. chrome.exe),
    NEVER accesses window titles, URLs, or screen contents.
    """
    if sys.platform != "win32":
        return None
    try:
        import ctypes
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        if not hwnd:
            return None
        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if pid.value and pid.value > 4:
            proc = psutil.Process(pid.value)
            return proc.name()
    except Exception:
        return None
    return None


def get_file_sha256(filepath: str) -> Optional[str]:
    """Calculate lowercase hexadecimal SHA-256 hash of an executable binary (T3_038)."""
    if not filepath or not os.path.isfile(filepath):
        return None
    try:
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest().lower()
    except (PermissionError, OSError, Exception) as e:
        logger.debug(f"Could not hash file {filepath}: {e}")
        return None


def stop_associated_windows_service(app_name: str):
    """Stop auto-restarting Windows services for known VPNs to prevent infinite respawn loops."""
    if sys.platform != "win32":
        return
    import subprocess
    KNOWN_SERVICES = {
        "warp-svc.exe": ["CloudflareWARP"],
        "cloudflare warp.exe": ["CloudflareWARP"],
        "protonvpn.launcher.exe": ["ProtonVPN Service"],
        "protonvpn.exe": ["ProtonVPN Service"],
    }
    svc_list = KNOWN_SERVICES.get(app_name.lower(), [])
    for svc in svc_list:
        try:
            subprocess.run(["sc.exe", "stop", svc], capture_output=True, timeout=2)
        except Exception:
            pass


class AppController:
    """Monitors and enforces application execution rules by SHA-256 hash (F2)."""

    def __init__(
        self,
        rules_provider: Optional[Callable[[], Dict[str, Dict[str, str]]]] = None,
        on_blocked_callback: Optional[Callable[[str, str, str], None]] = None,
        on_usage_callback: Optional[Callable[[str, int], None]] = None,
        scan_interval_sec: float = 3.0
    ):
        self.rules_provider = rules_provider
        self.on_blocked_callback = on_blocked_callback
        self.on_usage_callback = on_usage_callback
        self.scan_interval_sec = scan_interval_sec

        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._hash_cache: Dict[str, tuple[float, str]] = {}  # {filepath: (mtime, hash)}
        self._recently_notified: Dict[str, float] = {}       # {app_name: last_notified_ts}
        self._recently_logged: Dict[str, float] = {}         # {app_name_lower: last_logged_ts}
        self._last_usage_sampled: float = time.time()

    def _get_cached_sha256(self, filepath: str) -> Optional[str]:
        """Fetch hash from cache if mtime is unchanged, otherwise recompute."""
        try:
            mtime = os.path.getmtime(filepath)
            if filepath in self._hash_cache:
                cached_mtime, cached_hash = self._hash_cache[filepath]
                if cached_mtime == mtime:
                    return cached_hash

            computed = get_file_sha256(filepath)
            if computed:
                self._hash_cache[filepath] = (mtime, computed)
            return computed
        except Exception:
            return None

    def scan_and_enforce(self) -> list[dict]:
        """Scan running processes and terminate any blocked binaries (T3_039 & T3_041)."""
        rules = self.rules_provider() if self.rules_provider else {}
        if not rules:
            return []

        # Target set of blocked SHA-256 hashes & blocked executable names (T3_041 & T4_019)
        blocked_hashes = {
            h.lower(): info for h, info in rules.items() if info.get("action") == "block"
        }
        blocked_names = {}
        for info in rules.values():
            if info.get("action") == "block" and info.get("name"):
                n = info["name"].lower().strip()
                blocked_names[n] = info
                if n.endswith(".exe"):
                    blocked_names[n[:-4]] = info
                else:
                    blocked_names[f"{n}.exe"] = info

        if not blocked_hashes and not blocked_names:
            return []

        terminated_apps = []
        current_pid = os.getpid()

        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                pid = proc.info.get('pid')
                if pid == current_pid or pid <= 4:
                    continue

                exe_path = proc.info.get('exe')
                app_name = proc.info.get('name') or "Unknown"

                if not exe_path and not app_name:
                    continue

                # SHA-256 detection defeats binary renaming (T3_041); name matching catches VPNs and apps (T4_019)
                file_hash = self._get_cached_sha256(exe_path) if exe_path else None
                rule_info = None

                name_clean = app_name.lower().strip()
                name_base = name_clean[:-4] if name_clean.endswith(".exe") else name_clean

                if file_hash and file_hash in blocked_hashes:
                    rule_info = blocked_hashes[file_hash]
                elif name_clean in blocked_names:
                    rule_info = blocked_names[name_clean]
                elif name_base in blocked_names:
                    rule_info = blocked_names[name_base]

                if rule_info:
                    reason = rule_info.get("description") or "Quy định của cha mẹ"

                    # Terminate process (T3_040)
                    try:
                        proc.terminate()
                    except Exception:
                        try:
                            proc.kill()
                        except Exception:
                            pass

                    # Stop Windows service if it's a persistent auto-restarting service (e.g. Cloudflare WARP)
                    stop_associated_windows_service(app_name)

                    terminated_apps.append({
                        "pid": pid,
                        "app_name": app_name,
                        "exe": exe_path,
                        "hash": file_hash,
                        "reason": reason
                    })

                    # Rate-limit console warning logs (prevent terminal flooding every 3s)
                    now = time.time()
                    last_log_ts = self._recently_logged.get(app_name.lower(), 0.0)
                    if (now - last_log_ts) >= 30.0:
                        self._recently_logged[app_name.lower()] = now
                        logger.warning(
                            f"[APP BLOCKED] Terminating PID {pid} ({app_name}) | Hash: {str(file_hash)[:12]}... | Reason: {reason}"
                        )
                    else:
                        logger.debug(
                            f"[APP BLOCKED] Terminating PID {pid} ({app_name}) | Hash: {str(file_hash)[:12]}... | Reason: {reason}"
                        )

                    # Trigger explanation popup / notification (NT4)
                    now = time.time()
                    last_time = self._recently_notified.get(app_name, 0)
                    if (now - last_time) > 10:  # Rate-limit notices to once every 10s per app
                        self._recently_notified[app_name] = now
                        if self.on_blocked_callback:
                            self.on_blocked_callback(app_name, reason, file_hash)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except Exception as e:
                logger.debug(f"Process check exception: {e}")

        return terminated_apps

    def _loop(self):
        """Background scan loop running every 3-5s (T3_039)."""
        while self._running:
            try:
                self.scan_and_enforce()

                # Periodically sample active foreground application usage (every ~15s, NT2)
                now = time.time()
                elapsed = now - self._last_usage_sampled
                if elapsed >= 15.0:
                    self._last_usage_sampled = now
                    if self.on_usage_callback and not is_user_idle(300.0):
                        active_app = get_foreground_process_name()
                        if active_app and active_app.lower() not in ("explorer.exe", "shellexperiencehost.exe"):
                            self.on_usage_callback(active_app, int(elapsed))

            except Exception as e:
                logger.error(f"Error in AppController scan loop: {e}")
            time.sleep(self.scan_interval_sec)

    def start(self):
        """Start the background process monitor."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True, name="OGK_AppController")
        self._thread.start()
        logger.info("[*] AppController process monitor started.")

    def stop(self):
        """Stop the background process monitor."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        logger.info("[*] AppController stopped.")
