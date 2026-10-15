"""System locker module for Open Guardian Kids.
Safely locks Windows workstation using user32.LockWorkStation without crashing running apps,
and enforces periodic re-locking if child attempts to log back in while locked.
"""

import sys
import time
import ctypes
import threading
from typing import Optional, Callable


def lock_windows_workstation() -> bool:
    """Call native Windows user32.LockWorkStation API to lock the workstation immediately.
    
    Returns True if successfully triggered.
    """
    if sys.platform != "win32":
        # Safe fallback on non-Windows test environments
        return True

    try:
        result = ctypes.windll.user32.LockWorkStation()
        return bool(result)
    except Exception as e:
        print(f"[LOCKER] Error calling LockWorkStation: {e}")
        return False


class SystemLocker:
    """Manages system locking and enforces re-lock within 5 seconds if quota is exhausted."""

    def __init__(self, is_lock_required_fn: Optional[Callable[[], bool]] = None):
        self.is_lock_required_fn = is_lock_required_fn
        self.running = False
        self._thread: Optional[threading.Thread] = None

    def lock_now(self, reason: str = "Hết thời gian cho phép") -> bool:
        """Immediately trigger workstation lock."""
        print(f"[LOCKER] Khóa máy tính: {reason}")
        return lock_windows_workstation()

    def start_enforcement(self) -> None:
        """Start enforcement loop to re-lock workstation every 5s if lock condition persists."""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._enforce_loop, daemon=True, name="SystemLockerEnforce")
        self._thread.start()

    def stop_enforcement(self) -> None:
        """Stop enforcement loop."""
        self.running = False

    def _enforce_loop(self) -> None:
        """Periodically check lock condition and re-lock within 5s if child logged back in."""
        while self.running:
            time.sleep(5.0)
            if self.is_lock_required_fn and self.is_lock_required_fn():
                # Re-lock if still out of quota or locked by parent
                lock_windows_workstation()
