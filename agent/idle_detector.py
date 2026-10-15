"""User inactivity and idle detection for Open Guardian Kids.
Uses Windows API GetLastInputInfo to pause screen time quota when child is away (> 5 minutes).
"""

import sys
import ctypes


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("dwTime", ctypes.c_uint),
    ]


def get_idle_duration_seconds() -> float:
    """Return number of seconds elapsed since last keyboard or mouse input on Windows."""
    if sys.platform != "win32":
        return 0.0

    try:
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
            # GetTickCount() returns milliseconds elapsed since system started
            current_ticks = ctypes.windll.kernel32.GetTickCount()
            idle_millis = current_ticks - lii.dwTime
            return max(0.0, idle_millis / 1000.0)
    except Exception:
        pass

    return 0.0


def is_user_idle(threshold_seconds: float = 300.0) -> bool:
    """Return True if user has been inactive for longer than threshold (default 300s = 5m)."""
    return get_idle_duration_seconds() >= threshold_seconds
