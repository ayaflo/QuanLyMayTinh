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
        self.root.geometry("540x660")
        self.root.minsize(500, 620)
        self.root.configure(bg="#0f172a")

        # Center on screen
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
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
        # 1. Header Frame
        header = tk.Frame(self.root, bg="#1e293b", padx=20, pady=16)
        header.pack(fill=tk.X)

        header_top = tk.Frame(header, bg="#1e293b")
        header_top.pack(fill=tk.X)

        logo_lbl = tk.Label(header_top, text="🛡️", font=("Segoe UI", 28), bg="#1e293b")
        logo_lbl.pack(side=tk.LEFT, padx=(0, 12))

        title_box = tk.Frame(header_top, bg="#1e293b")
        title_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        title_lbl = tk.Label(
            title_box,
            text="Kết Nối Cùng Ba Mẹ",
            font=("Segoe UI", 15, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        )
        title_lbl.pack(anchor=tk.W)

        sub_lbl = tk.Label(
            title_box,
            text="Đồng hành, yêu thương và bảo vệ máy tính của em",
            font=("Segoe UI", 9),
            fg="#38bdf8",
            bg="#1e293b"
        )
        sub_lbl.pack(anchor=tk.W)

        # 2. Main Content Body
        body = tk.Frame(self.root, bg="#0f172a", padx=24, pady=16)
        body.pack(fill=tk.BOTH, expand=True)

        # Guide Card (3 Steps)
        guide_card = tk.Frame(body, bg="#1e293b", padx=16, pady=12, highlightbackground="#334155", highlightthickness=1)
        guide_card.pack(fill=tk.X, pady=(0, 14))

        guide_title = tk.Label(
            guide_card,
            text="📖 Hướng dẫn 3 bước đơn giản:",
            font=("Segoe UI", 10, "bold"),
            fg="#38bdf8",
            bg="#1e293b"
        )
        guide_title.pack(anchor=tk.W, pady=(0, 6))

        steps = [
            ("1️⃣", f"Ba mẹ mở trang quản lý trên điện thoại/máy tính: {self.server_url}"),
            ("2️⃣", "Bấm nút '+ Thêm thiết bị' để lấy Mã kết nối 8 ký tự."),
            ("3️⃣", "Nhập 8 ký tự vào ô bên dưới rồi bấm nút 'Kết Nối Ngay'.")
        ]
        for icon, txt in steps:
            row = tk.Frame(guide_card, bg="#1e293b")
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=icon, font=("Segoe UI", 9), bg="#1e293b", fg="#f8fafc").pack(side=tk.LEFT, padx=(0, 6))
            tk.Label(row, text=txt, font=("Segoe UI", 8), bg="#1e293b", fg="#cbd5e1", wraplength=420, justify=tk.LEFT).pack(side=tk.LEFT, anchor=tk.W)

        # 3. Code Input Section
        code_section = tk.Frame(body, bg="#0f172a")
        code_section.pack(fill=tk.X, pady=(0, 10))

        code_header = tk.Frame(code_section, bg="#0f172a")
        code_header.pack(fill=tk.X, pady=(0, 4))

        code_lbl = tk.Label(
            code_header,
            text="🔑 Nhập Mã Ghép Đôi (8 Ký Tự):",
            font=("Segoe UI", 10, "bold"),
            fg="#f8fafc",
            bg="#0f172a"
        )
        code_lbl.pack(side=tk.LEFT)

        self.counter_lbl = tk.Label(
            code_header,
            text="0 / 8 ký tự",
            font=("Segoe UI", 9, "bold"),
            fg="#64748b",
            bg="#0f172a"
        )
        self.counter_lbl.pack(side=tk.RIGHT)

        # Entry row with paste button
        entry_row = tk.Frame(code_section, bg="#0f172a")
        entry_row.pack(fill=tk.X)

        self.code_var = tk.StringVar()
        self.code_var.trace_add("write", self._on_code_changed)

        self.code_entry = tk.Entry(
            entry_row,
            textvariable=self.code_var,
            font=("Consolas", 20, "bold"),
            justify="center",
            bg="#1e293b",
            fg="#38bdf8",
            insertbackground="#38bdf8",
            relief=tk.FLAT,
            highlightbackground="#0284c7",
            highlightcolor="#38bdf8",
            highlightthickness=2
        )
        self.code_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        self.code_entry.focus_set()

        paste_btn = tk.Button(
            entry_row,
            text="📋 Dán",
            font=("Segoe UI", 10, "bold"),
            bg="#334155",
            fg="#f8fafc",
            activebackground="#475569",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            command=self._paste_clipboard,
            cursor="hand2"
        )
        paste_btn.pack(side=tk.RIGHT, padx=(8, 0), ipady=8)

        # 4. Device Name Section
        name_section = tk.Frame(body, bg="#0f172a")
        name_section.pack(fill=tk.X, pady=(10, 10))

        name_lbl = tk.Label(
            name_section,
            text="💻 Tên Máy Tính Của Em (tùy chọn):",
            font=("Segoe UI", 9, "bold"),
            fg="#cbd5e1",
            bg="#0f172a"
        )
        name_lbl.pack(anchor=tk.W, pady=(0, 4))

        self.name_var = tk.StringVar(value=self.default_device_name)
        self.name_entry = tk.Entry(
            name_section,
            textvariable=self.name_var,
            font=("Segoe UI", 10),
            bg="#1e293b",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            relief=tk.FLAT,
            highlightbackground="#334155",
            highlightthickness=1
        )
        self.name_entry.pack(fill=tk.X, ipady=4)

        # 5. Status / Message Box
        self.status_box = tk.Label(
            body,
            text="",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#0f172a",
            wraplength=460,
            justify=tk.CENTER
        )
        self.status_box.pack(fill=tk.X, pady=(6, 8))

        # 6. Action Button
        self.submit_btn = tk.Button(
            body,
            text="🚀 Kết Nối Ngay",
            font=("Segoe UI", 12, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._on_submit
        )
        self.submit_btn.pack(fill=tk.X, pady=(4, 8))

        # 7. Ethical Footer
        footer = tk.Frame(self.root, bg="#0f172a", padx=16, pady=8)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        fp = get_device_fingerprint()[:16]
        info_lbl = tk.Label(
            footer,
            text=f"Máy chủ: {self.server_url}  •  Thiết bị: {fp}...",
            font=("Segoe UI", 7),
            fg="#64748b",
            bg="#0f172a"
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
            bg="#475569"
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
                state=tk.DISABLED
            )
            # Auto-close after 1.5 seconds so child sees success celebration
            self.root.after(1500, self._close_success)
        else:
            self.success = False
            self.submit_btn.config(
                text="🚀 Thử Lại",
                bg="#0284c7",
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
