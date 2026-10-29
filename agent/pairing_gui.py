"""Child-Friendly GUI for Device Pairing (Open Guardian Kids).
Provides a beautiful, intuitive Tkinter window for children and parents
to easily pair a computer with the parent account using an 8-character code.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Tuple

try:
    from .config import SERVER_URL, DEVICE_NAME, APP_TITLE, APP_VERSION
    from .fingerprint import get_device_fingerprint
    from .enrollment_client import pair_with_server
except ImportError:
    from config import SERVER_URL, DEVICE_NAME, APP_TITLE, APP_VERSION
    from fingerprint import get_device_fingerprint
    from enrollment_client import pair_with_server


class PairingWindow:
    """Friendly, modern pairing wizard GUI for children and parents."""

    def __init__(self, server_url: str = SERVER_URL, default_device_name: str = DEVICE_NAME):
        self.server_url = server_url.rstrip("/")
        self.default_device_name = default_device_name
        self.success = False
        self.root: Optional[tk.Tk] = None

    def _enable_high_dpi(self):
        """Enable crisp font rendering on high-DPI Windows displays."""
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    def run(self) -> bool:
        """Launch the pairing GUI and block until finished. Returns True if paired."""
        self._enable_high_dpi()

        self.root = tk.Tk()
        self.root.title(f"{APP_TITLE} — Ghép Đôi Cùng Ba Mẹ")
        self.root.geometry("600x560")
        self.root.minsize(560, 500)
        self.root.configure(bg="#000000")

        # Center on screen
        self.root.update_idletasks()
        w = max(600, self.root.winfo_width())
        h = max(560, self.root.winfo_height())
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = max(0, (sw - w) // 2)
        y = max(0, (sh - h) // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        self._build_ui()

        # Keyboard shortcuts
        self.root.bind("<Return>", lambda event: self._on_submit())
        self.root.bind("<Escape>", lambda event: self.root.destroy())

        self.root.mainloop()
        return self.success

    def _build_ui(self):
        # 1. Header Frame (xai247 Glass Header)
        header = tk.Frame(
            self.root,
            bg="#0c0d12",
            padx=20,
            pady=16,
            highlightbackground="#1e2230",
            highlightthickness=1
        )
        header.pack(fill=tk.X)

        header_top = tk.Frame(header, bg="#0c0d12")
        header_top.pack(fill=tk.X)

        # Brand Badge (White Pill style)
        brand_badge = tk.Label(
            header_top,
            text="OGK",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#000000",
            padx=10,
            pady=5
        )
        brand_badge.pack(side=tk.LEFT, padx=(0, 14))

        title_box = tk.Frame(header_top, bg="#0c0d12")
        title_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        title_lbl = tk.Label(
            title_box,
            text="Kết Nối Cùng Ba Mẹ",
            font=("Segoe UI", 14, "bold"),
            fg="#ffffff",
            bg="#0c0d12"
        )
        title_lbl.pack(anchor=tk.W)

        sub_lbl = tk.Label(
            title_box,
            text="Đồng hành, yêu thương và bảo vệ máy tính của em",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#0c0d12",
            wraplength=540,
            justify=tk.LEFT
        )
        sub_lbl.pack(anchor=tk.W, pady=(2, 0))

        # 2. Main Content Body
        body = tk.Frame(self.root, bg="#000000", padx=24, pady=16)
        body.pack(fill=tk.BOTH, expand=True)

        # Guide Card (3 Steps)
        guide_card = tk.Frame(
            body,
            bg="#0d0e14",
            padx=16,
            pady=14,
            highlightbackground="#1e2230",
            highlightthickness=1
        )
        guide_card.pack(fill=tk.X, pady=(0, 14))

        guide_title = tk.Label(
            guide_card,
            text="📖 Hướng dẫn 3 bước đơn giản:",
            font=("Segoe UI", 10, "bold"),
            fg="#38bdf8",
            bg="#0d0e14"
        )
        guide_title.pack(anchor=tk.W, pady=(0, 6))

        steps = [
            ("1️⃣", "Ba mẹ mở trang quản trị Dashboard trên điện thoại hoặc máy tính."),
            ("2️⃣", "Bấm nút '+ Thêm thiết bị' để lấy Mã kết nối 8 ký tự."),
            ("3️⃣", "Nhập 8 ký tự vào ô bên dưới rồi bấm nút 'Kết Nối Ngay'.")
        ]
        for icon, txt in steps:
            row = tk.Frame(guide_card, bg="#0d0e14")
            row.pack(fill=tk.X, pady=3)
            tk.Label(row, text=icon, font=("Segoe UI", 9), bg="#0d0e14", fg="#ffffff").pack(side=tk.LEFT, padx=(0, 8))
            lbl = tk.Label(row, text=txt, font=("Segoe UI", 8), bg="#0d0e14", fg="#cbd5e1", wraplength=500, justify=tk.LEFT)
            lbl.pack(side=tk.LEFT, anchor=tk.W)

        # 3. Code Input Section
        code_section = tk.Frame(body, bg="#000000")
        code_section.pack(fill=tk.X, pady=(0, 10))

        code_header = tk.Frame(code_section, bg="#000000")
        code_header.pack(fill=tk.X, pady=(0, 5))

        code_lbl = tk.Label(
            code_header,
            text="🔑 Nhập Mã Ghép Đôi (8 Ký Tự):",
            font=("Segoe UI", 10, "bold"),
            fg="#ffffff",
            bg="#000000"
        )
        code_lbl.pack(side=tk.LEFT)

        self.counter_lbl = tk.Label(
            code_header,
            text="0 / 8 ký tự",
            font=("Segoe UI", 9, "bold"),
            fg="#64748b",
            bg="#000000"
        )
        self.counter_lbl.pack(side=tk.RIGHT)

        # Entry row with paste button
        entry_row = tk.Frame(code_section, bg="#000000")
        entry_row.pack(fill=tk.X)

        self.code_var = tk.StringVar()
        self.code_var.trace_add("write", self._on_code_changed)

        paste_btn = tk.Button(
            entry_row,
            text="📋 Dán",
            font=("Segoe UI", 10, "bold"),
            bg="#181c28",
            fg="#ffffff",
            activebackground="#252c3f",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=16,
            command=self._paste_clipboard,
            cursor="hand2",
            highlightbackground="#2d344d",
            highlightthickness=1
        )
        paste_btn.pack(side=tk.RIGHT, padx=(10, 0), ipady=7)

        self.code_entry = tk.Entry(
            entry_row,
            textvariable=self.code_var,
            font=("Consolas", 20, "bold"),
            justify="center",
            bg="#121520",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            highlightbackground="#222838",
            highlightcolor="#38bdf8",
            highlightthickness=2
        )
        self.code_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.code_entry.focus_set()

        # 4. Device Name Section
        name_section = tk.Frame(body, bg="#000000")
        name_section.pack(fill=tk.X, pady=(0, 10))

        name_lbl = tk.Label(
            name_section,
            text="💻 Tên Máy Tính Của Em (tùy chọn):",
            font=("Segoe UI", 9, "bold"),
            fg="#cbd5e1",
            bg="#000000"
        )
        name_lbl.pack(anchor=tk.W, pady=(0, 4))

        self.name_var = tk.StringVar(value=self.default_device_name)
        self.name_entry = tk.Entry(
            name_section,
            textvariable=self.name_var,
            font=("Segoe UI", 10),
            bg="#121520",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            highlightbackground="#222838",
            highlightthickness=1
        )
        self.name_entry.pack(fill=tk.X, ipady=5)

        # 5. Action Button (ALWAYS VISIBLE & PACKED ABOVE STATUS)
        self.submit_btn = tk.Button(
            body,
            text="🚀 Kết Nối Ngay",
            font=("Segoe UI", 11, "bold"),
            bg="#ffffff",
            fg="#000000",
            activebackground="#f1f5f9",
            activeforeground="#000000",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._on_submit
        )
        self.submit_btn.pack(fill=tk.X, pady=(12, 6))

        # 6. Status Message Box (PACKED BELOW BUTTON - NEVER PUSHES BUTTON OFF-SCREEN)
        self.status_box = tk.Label(
            body,
            text="",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#000000",
            wraplength=520,
            justify=tk.CENTER
        )
        self.status_box.pack(fill=tk.X, pady=(2, 6))

        # 7. Ethical Footer
        footer = tk.Frame(self.root, bg="#000000", padx=16, pady=8)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        fp = get_device_fingerprint()[:16]
        info_lbl = tk.Label(
            footer,
            text=f"Hệ thống đồng hành cùng con  •  Mã thiết bị: {fp}...",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#000000"
        )
        info_lbl.pack()

    def _on_code_changed(self, *args):
        """Filter input to uppercase alphanumeric, limit to 8 chars, and update badge."""
        val = self.code_var.get()
        # Keep only alphanumeric
        clean = "".join(ch for ch in val if ch.isalnum()).upper()[:8]
        if clean != val:
            self.code_var.set(clean)

        length = len(clean)
        if length == 8:
            self.counter_lbl.config(text="8 / 8 ký tự — Sẵn sàng!", fg="#10b981")
            self.code_entry.config(highlightcolor="#10b981", highlightbackground="#10b981")
        elif length > 0:
            self.counter_lbl.config(text=f"{length} / 8 ký tự", fg="#38bdf8")
            self.code_entry.config(highlightcolor="#38bdf8", highlightbackground="#0284c7")
        else:
            self.counter_lbl.config(text="0 / 8 ký tự", fg="#64748b")
            self.code_entry.config(highlightcolor="#38bdf8", highlightbackground="#0284c7")

        # Automatically clear any error status and reset submit button when typing or modifying code
        if not self.success and self.status_box.cget("text"):
            self._set_status("")
            self.submit_btn.config(
                text="🚀 Kết Nối Ngay",
                bg="#ffffff",
                fg="#000000",
                state=tk.NORMAL
            )

    def _paste_clipboard(self):
        """Paste text from system clipboard into pairing code entry."""
        try:
            clip = self.root.clipboard_get()
            if clip:
                clean = "".join(ch for ch in clip.strip() if ch.isalnum()).upper()[:8]
                self.code_var.set(clean)
        except Exception:
            pass

    def _on_submit(self):
        """Handle submit button click."""
        code = self.code_var.get().strip().upper()
        if len(code) != 8:
            self._set_status("⚠️ Vui lòng nhập đầy đủ 8 ký tự mã kết nối.", color="#f59e0b")
            self.code_entry.focus_set()
            return

        device_name = self.name_var.get().strip() or self.default_device_name

        # Loading state
        self.submit_btn.config(
            text="⏳ Đang kết nối đến máy chủ...",
            state=tk.DISABLED,
            bg="#475569",
            fg="#ffffff"
        )
        self._set_status("Đang gửi yêu cầu xác thực lên máy chủ...", color="#38bdf8")

        # Run connection in background thread to avoid freezing Tkinter GUI
        def _worker():
            success, msg, _ = pair_with_server(
                code=code,
                device_name=device_name,
                server_url=self.server_url
            )
            # Post back to Tkinter thread
            if self.root and self.root.winfo_exists():
                self.root.after(0, lambda: self._handle_result(success, msg))

        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    def _handle_result(self, success: bool, msg: str):
        """Process pairing response on main GUI thread."""
        if success:
            self.success = True
            self._set_status(
                "🎉 Ghép đôi thành công! Cảm ơn em, máy tính đã được kết nối cùng Ba Mẹ.",
                color="#10b981"
            )
            self.submit_btn.config(
                text="✅ Đã Kết Nối Thành Công",
                bg="#10b981",
                fg="#ffffff",
                state=tk.DISABLED
            )
            # Auto-close after 1.5 seconds so child sees success celebration
            self.root.after(1500, self._close_success)
        else:
            self.success = False
            self.submit_btn.config(
                text="🚀 Thử Lại",
                bg="#ffffff",
                fg="#000000",
                state=tk.NORMAL
            )
            self._set_status(f"❌ {msg}\n(Ba mẹ có thể tạo mã mới nếu mã cũ đã hết hạn)", color="#ef4444")
            self.code_entry.focus_set()

    def _close_success(self):
        """Close window upon success."""
        if self.root and self.root.winfo_exists():
            self.root.destroy()

    def _set_status(self, text: str, color: str = "#94a3b8"):
        """Update status message label."""
        self.status_box.config(text=text, fg=color)


def prompt_pairing_gui(server_url: str = SERVER_URL, default_device_name: str = DEVICE_NAME) -> bool:
    """Helper function to show GUI pairing wizard. Fallback to False if GUI fails."""
    try:
        app = PairingWindow(server_url=server_url, default_device_name=default_device_name)
        return app.run()
    except Exception as e:
        print(f" [!] Không thể khởi động giao diện đồ họa: {e}")
        return False


if __name__ == "__main__":
    print("Khởi chạy thử giao diện ghép đôi...")
    res = prompt_pairing_gui()
    print("Kết quả ghép đôi:", res)
