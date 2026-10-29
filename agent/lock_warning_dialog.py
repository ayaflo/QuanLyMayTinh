"""Lock warning dialog with countdown for Open Guardian Kids.
Displays a prominent, topmost floating notification when parent triggers a lock command,
giving the child sufficient time (default: 30 seconds) to save work before the computer locks.
"""

import sys
import time
import threading
import logging
from typing import Optional, Callable

logger = logging.getLogger("OGK_LockWarning")


class LockWarningController:
    """Manages lock countdown with floating UI and fallback timer."""

    def __init__(self):
        self._active_dialog: Optional['LockCountdownWindow'] = None
        self._timer_thread: Optional[threading.Thread] = None
        self._cancelled = False
        self._lock = threading.RLock()

    def start_countdown(
        self,
        seconds: int = 30,
        reason: str = "Phụ huynh đã yêu cầu khóa máy",
        on_lock_callback: Optional[Callable[[], None]] = None,
        on_tick_callback: Optional[Callable[[int], None]] = None,
        show_gui: bool = True
    ) -> None:
        """Start countdown with visible floating window."""
        with self._lock:
            self.cancel()  # Cancel any existing countdown
            self._cancelled = False

        logger.info(f"[LOCK_WARNING] Bắt đầu đếm ngược {seconds}s trước khi khóa: {reason}")

        # Start GUI in background thread
        if show_gui:
            def _run_gui():
                try:
                    import tkinter as tk
                    self._active_dialog = LockCountdownWindow(
                        seconds=seconds,
                        reason=reason,
                        on_lock=self._trigger_lock,
                        controller=self
                    )
                    self._active_dialog.show()
                except Exception as e:
                    logger.warning(f"[LOCK_WARNING] Could not display GUI countdown ({e}), using console/fallback timer.")

            gui_thread = threading.Thread(target=_run_gui, daemon=True, name="OGK_LockCountdownGUI")
            gui_thread.start()

        # Fallback watchdog thread to guarantee lock even if Tkinter hangs or is closed
        def _watchdog():
            rem = seconds
            while rem > 0:
                time.sleep(1.0)
                with self._lock:
                    if self._cancelled:
                        logger.info("[LOCK_WARNING] Countdown was cancelled.")
                        return
                rem -= 1
                if on_tick_callback:
                    try:
                        on_tick_callback(rem)
                    except Exception:
                        pass

            with self._lock:
                if not self._cancelled:
                    logger.info("[LOCK_WARNING] Countdown finished -> Cưỡng chế khóa máy!")
                    if on_lock_callback:
                        on_lock_callback()

        self._timer_thread = threading.Thread(target=_watchdog, daemon=True, name="OGK_LockWatchdog")
        self._timer_thread.start()

    def cancel(self) -> None:
        """Cancel active countdown (e.g. if parent unlocks before timer expires)."""
        with self._lock:
            self._cancelled = True
            if self._active_dialog:
                try:
                    self._active_dialog.close()
                except Exception:
                    pass
                self._active_dialog = None

    def _trigger_lock(self):
        # GUI requested lock on 0
        pass


class LockCountdownWindow:
    """Tkinter topmost countdown alert window."""

    def __init__(self, seconds: int, reason: str, on_lock: Callable[[], None], controller: LockWarningController):
        self.remaining = seconds
        self.reason = reason
        self.on_lock = on_lock
        self.controller = controller
        self.root = None
        self.timer_label = None

    def show(self):
        import tkinter as tk

        self.root = tk.Tk()
        self.root.title("⚠️ CẢNH BÁO TỪ PHỤ HUYNH")
        self.root.geometry("480x260")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        # Stay on top of all windows
        self.root.attributes("-topmost", True)

        # Center on screen
        try:
            self.root.eval('tk::PlaceWindow . center')
        except Exception:
            pass

        # Header Frame
        header = tk.Frame(self.root, bg="#ef4444", padx=16, pady=10)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="⚠️ THÔNG BÁO TỪ CHA MẸ: SẮP KHÓA MÁY TÍNH",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#ef4444"
        )
        title.pack(anchor=tk.CENTER)

        # Body Frame
        body = tk.Frame(self.root, bg="#1e293b", padx=20, pady=16)
        body.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        desc = tk.Label(
            body,
            text=f"{self.reason}\nMáy tính sẽ tự động khóa màn hình sau:",
            font=("Segoe UI", 10),
            fg="#f8fafc",
            bg="#1e293b",
            justify=tk.CENTER
        )
        desc.pack(anchor=tk.CENTER, pady=(0, 6))

        # Huge Countdown Label
        self.timer_label = tk.Label(
            body,
            text=f"{self.remaining} GIÂY",
            font=("Segoe UI", 26, "bold"),
            fg="#ef4444",
            bg="#1e293b"
        )
        self.timer_label.pack(anchor=tk.CENTER, pady=(0, 6))

        subtext = tk.Label(
            body,
            text="⚠️ Em hãy nhanh chóng LƯU BÀI TẬP và các tài liệu đang làm dở!",
            font=("Segoe UI", 9, "italic"),
            fg="#fbbf24",
            bg="#1e293b",
            justify=tk.CENTER
        )
        subtext.pack(anchor=tk.CENTER)

        # Disable close button (X) so child cannot just dismiss the lock countdown
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

        self._tick()
        self.root.mainloop()

    def _tick(self):
        if not self.root:
            return

        if self.controller._cancelled:
            self.close()
            return

        if self.remaining <= 0:
            self.close()
            return

        if self.timer_label:
            self.timer_label.config(text=f"{self.remaining} GIÂY")

        self.remaining -= 1
        self.root.after(1000, self._tick)

    def close(self):
        if self.root:
            try:
                self.root.destroy()
            except Exception:
                pass
            self.root = None


# Global controller instance
lock_warning_controller = LockWarningController()
