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

    @property
    def is_cancelled(self) -> bool:
        with self._lock:
            return self._cancelled

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
                dialog = None
                try:
                    import tkinter as tk
                    dialog = LockCountdownWindow(
                        seconds=seconds,
                        reason=reason,
                        on_lock=self._trigger_lock,
                        controller=self
                    )
                    with self._lock:
                        self._active_dialog = dialog
                    dialog.show()
                except Exception as e:
                    logger.warning(f"[LOCK_WARNING] Could not display GUI countdown ({e}), using console/fallback timer.")
                finally:
                    with self._lock:
                        if self._active_dialog == dialog:
                            self._active_dialog = None

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


def _enable_high_dpi():
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


class LockCountdownWindow:
    """Tkinter topmost countdown alert window."""

    def __init__(self, seconds: int, reason: str, on_lock: Callable[[], None], controller: LockWarningController):
        self.total_seconds = seconds
        self.remaining = seconds
        self.reason = reason
        self.on_lock = on_lock
        self.controller = controller
        self.root = None
        self.timer_label = None
        self._should_close = False
        self.start_monotonic = 0.0

    def show(self):
        import tkinter as tk
        _enable_high_dpi()

        self.root = tk.Tk()
        self.start_monotonic = time.monotonic()
        self.root.title("⚠️ CẢNH BÁO TỪ PHỤ HUYNH")
        self.root.geometry("560x320")
        self.root.minsize(520, 280)
        self.root.configure(bg="#0f172a")

        # Stay on top of all windows
        self.root.attributes("-topmost", True)

        # Center on screen
        self.root.update_idletasks()
        w = max(560, self.root.winfo_width())
        h = max(320, self.root.winfo_height())
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = max(0, (sw - w) // 2)
        y = max(0, (sh - h) // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        # Header Frame
        header = tk.Frame(self.root, bg="#ef4444", padx=18, pady=12)
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
        body = tk.Frame(self.root, bg="#1e293b", padx=22, pady=16)
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        desc = tk.Label(
            body,
            text=f"{self.reason}\nMáy tính sẽ tự động khóa màn hình sau:",
            font=("Segoe UI", 10),
            fg="#f8fafc",
            bg="#1e293b",
            justify=tk.CENTER,
            wraplength=480
        )
        desc.pack(anchor=tk.CENTER, pady=(0, 6))

        # Huge Countdown Label
        self.timer_label = tk.Label(
            body,
            text=f"{self.remaining} GIÂY",
            font=("Segoe UI", 28, "bold"),
            fg="#ef4444",
            bg="#1e293b"
        )
        self.timer_label.pack(anchor=tk.CENTER, pady=(0, 8))

        subtext = tk.Label(
            body,
            text="⚠️ Em hãy nhanh chóng LƯU BÀI TẬP và các tài liệu đang làm dở!",
            font=("Segoe UI", 9, "italic"),
            fg="#fbbf24",
            bg="#1e293b",
            justify=tk.CENTER,
            wraplength=480
        )
        subtext.pack(anchor=tk.CENTER)

        # Disable close button (X) so child cannot just dismiss the lock countdown
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

        self._tick()
        try:
            self.root.mainloop()
        except Exception:
            pass
        finally:
            self._destroy_on_gui_thread()

    def _tick(self):
        if not self.root:
            return

        # Check cancellation or request to close
        if self._should_close or self.controller.is_cancelled:
            self._destroy_on_gui_thread()
            return

        elapsed = int(time.monotonic() - self.start_monotonic)
        self.remaining = max(0, self.total_seconds - elapsed)

        if self.timer_label:
            try:
                self.timer_label.config(text=f"{self.remaining} GIÂY")
            except Exception:
                pass

        if self.remaining <= 0:
            self._destroy_on_gui_thread()
            return

        try:
            self.root.after(150, self._tick)
        except Exception:
            self._destroy_on_gui_thread()

    def _destroy_on_gui_thread(self):
        """Destroy the Tk window strictly on the GUI thread."""
        if self.root:
            r = self.root
            self.root = None
            try:
                r.destroy()
            except Exception:
                pass

    def close(self):
        """Thread-safe request to close the countdown window.
        Sets a boolean flag so destruction is carried out exclusively on the GUI thread.
        Prevents Tcl_AsyncDelete / wrong thread crashes.
        """
        self._should_close = True


# Global controller instance
lock_warning_controller = LockWarningController()
