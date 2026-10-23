"""Application Control Module for Open Guardian Kids (F2 & NT4).
Monitors running processes every 3-5 seconds, verifies binary SHA-256 hashes
to prevent rename-bypass, terminates unauthorized applications, and displays explanatory notices.
"""

import os
import time
import hashlib
import threading
import logging
from typing import Optional, Dict, Callable
import psutil

logger = logging.getLogger("OGK_AppController")


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


class AppController:
    """Monitors and enforces application execution rules by SHA-256 hash (F2)."""

    def __init__(
        self,
        rules_provider: Optional[Callable[[], Dict[str, Dict[str, str]]]] = None,
        on_blocked_callback: Optional[Callable[[str, str, str], None]] = None,
        scan_interval_sec: float = 3.0
    ):
        self.rules_provider = rules_provider
        self.on_blocked_callback = on_blocked_callback
        self.scan_interval_sec = scan_interval_sec

        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._hash_cache: Dict[str, tuple[float, str]] = {}  # {filepath: (mtime, hash)}
        self._recently_notified: Dict[str, float] = {}       # {app_name: last_notified_ts}

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

        # Target set of blocked SHA-256 hashes
        blocked_hashes = {
            h.lower(): info for h, info in rules.items() if info.get("action") == "block"
        }
        if not blocked_hashes:
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

                if not exe_path:
                    continue

                # SHA-256 detection defeats binary renaming (T3_041)
                file_hash = self._get_cached_sha256(exe_path)
                if not file_hash:
                    continue

                if file_hash in blocked_hashes:
                    rule_info = blocked_hashes[file_hash]
                    reason = rule_info.get("description") or "Quy định của cha mẹ"
                    logger.warning(
                        f"[APP BLOCKED] Terminating PID {pid} ({app_name}) | Hash: {file_hash[:12]}... | Reason: {reason}"
                    )

                    # Terminate process (T3_040)
                    try:
                        proc.terminate()
                    except Exception:
                        try:
                            proc.kill()
                        except Exception:
                            pass

                    terminated_apps.append({
                        "pid": pid,
                        "app_name": app_name,
                        "exe": exe_path,
                        "hash": file_hash,
                        "reason": reason
                    })

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
