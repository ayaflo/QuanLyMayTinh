"""Child Transparency & Voice Window for Open Guardian Kids (NT3 & NT5 - T3_044, T3_045).
Gives the child full visibility into what the agent records ("Hôm nay em đã dùng gì")
and provides a 2-way communication channel to request extra time or report false-positive blocks.
"""

import sys
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timezone
import requests
import logging

try:
    from .storage import load_credentials, get_daily_usage, load_policy_cache
    from .config import SERVER_URL, REQUEST_TIMEOUT
except ImportError:
    from storage import load_credentials, get_daily_usage, load_policy_cache
    from config import SERVER_URL, REQUEST_TIMEOUT

logger = logging.getLogger("OGK_ChildView")


class ChildViewWindow:
    """Tkinter window providing two-way transparency for children (NT3 & NT5)."""

    def __init__(self, server_url: str = SERVER_URL):
        self.server_url = server_url.rstrip("/")
        self.root = None
        self.notified_req_ids = set()

    def show(self):
        """Display the child transparency window."""
        if self.root and self.root.winfo_exists():
            self.root.lift()
            self.root.focus_force()
            return

        self.root = tk.Tk()
        self.root.title("Open Guardian Kids — Hôm Nay Em Đã Dùng Gì")
        self.root.geometry("520x620")
        self.root.configure(bg="#0f172a")

        # Header Title
        header_frame = tk.Frame(self.root, bg="#1e293b", padx=16, pady=14)
        header_frame.pack(fill=tk.X)

        title_lbl = tk.Label(
            header_frame,
            text="🛡️ Bảng Minh Bạch Hai Chiều Cùng Ba Mẹ",
            font=("Segoe UI", 12, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        )
        title_lbl.pack(anchor=tk.W)

        sub_lbl = tk.Label(
            header_frame,
            text="Nguyên tắc NT5: Em và phụ huynh nhìn thấy cùng một dữ liệu. Không theo dõi lén.",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#1e293b"
        )
        sub_lbl.pack(anchor=tk.W, pady=(2, 0))

        # Main scrollable/padded container
        content = tk.Frame(self.root, bg="#0f172a", padx=16, pady=12)
        content.pack(fill=tk.BOTH, expand=True)

        # 1. Screen Time Usage Box
        self.today_str = datetime.now().strftime("%Y-%m-%d")
        stat_card = tk.Frame(content, bg="#1e293b", padx=12, pady=10, relief=tk.FLAT)
        stat_card.pack(fill=tk.X, pady=(0, 10))

        self.stat_title = tk.Label(
            stat_card,
            text="⏱️ Đang tải thời gian sử dụng...",
            font=("Segoe UI", 10, "bold"),
            fg="#38bdf8",
            bg="#1e293b"
        )
        self.stat_title.pack(anchor=tk.W)

        self.rem_lbl = tk.Label(
            stat_card,
            text="",
            font=("Segoe UI", 9),
            fg="#10b981",
            bg="#1e293b"
        )
        self.rem_lbl.pack(anchor=tk.W, pady=(2, 0))
        self._update_usage_display()

        # 2. Privacy Commitment Box (NT1 & NT2)
        privacy_card = tk.Frame(content, bg="#1e293b", padx=12, pady=8)
        privacy_card.pack(fill=tk.X, pady=(0, 10))

        p_title = tk.Label(
            privacy_card,
            text="🔒 Cam Kết Tôn Trọng Quyền Riêng Tư (NT2)",
            font=("Segoe UI", 9, "bold"),
            fg="#34d399",
            bg="#1e293b"
        )
        p_title.pack(anchor=tk.W)

        p_desc = tk.Label(
            privacy_card,
            text="• KHÔNG lưu URL chi tiết, KHÔNG chụp màn hình\n• KHÔNG đọc tin nhắn hay ghi bàn phím (keylogger)\n• Danh sách trường học & Tổng đài 111 luôn được bảo vệ",
            font=("Segoe UI", 8),
            fg="#cbd5e1",
            bg="#1e293b",
            justify=tk.LEFT
        )
        p_desc.pack(anchor=tk.W, pady=(4, 0))

        # 3. Actions Section: Voice of the child (NT3)
        actions_card = tk.LabelFrame(
            content,
            text=" 📢 Tiếng Nói Của Em (NT3 — Gửi Yêu Cầu Cho Cha Mẹ) ",
            font=("Segoe UI", 9, "bold"),
            fg="#f8fafc",
            bg="#0f172a",
            padx=10,
            pady=8
        )
        actions_card.pack(fill=tk.X, pady=(0, 10))

        req_frame = tk.Frame(actions_card, bg="#0f172a")
        req_frame.pack(fill=tk.X)

        btn_add_time = tk.Button(
            req_frame,
            text="➕ Xin Thêm 15 Phút",
            font=("Segoe UI", 9, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            padx=8,
            pady=6,
            relief=tk.FLAT,
            command=self._dialog_request_time
        )
        btn_add_time.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        btn_unblock = tk.Button(
            req_frame,
            text="🌐 Báo Chặn Nhầm Web / App",
            font=("Segoe UI", 9, "bold"),
            bg="#d97706",
            fg="#ffffff",
            activebackground="#b45309",
            padx=8,
            pady=6,
            relief=tk.FLAT,
            command=self._dialog_unblock_request
        )
        btn_unblock.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        # 4. Action Buttons (Refresh & Close)
        btn_box = tk.Frame(content, bg="#0f172a")
        btn_box.pack(side=tk.BOTTOM, fill=tk.X, pady=(6, 0))

        btn_refresh = tk.Button(
            btn_box,
            text="🔄 Làm Mới Dữ Liệu",
            font=("Segoe UI", 9),
            bg="#0369a1",
            fg="#ffffff",
            pady=4,
            relief=tk.FLAT,
            command=self._manual_refresh
        )
        btn_refresh.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        btn_close = tk.Button(
            btn_box,
            text="Đóng Cửa Sổ",
            font=("Segoe UI", 9),
            bg="#334155",
            fg="#ffffff",
            pady=4,
            relief=tk.FLAT,
            command=self.root.destroy
        )
        btn_close.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        # Start periodic background refresh every 2.5 seconds
        self._schedule_periodic_refresh()

        self.root.mainloop()

    def _update_usage_display(self):
        """Update screen time metrics on the UI."""
        self.today_str = datetime.now().strftime("%Y-%m-%d")
        usage = get_daily_usage(self.today_str)
        used_min = round(usage.get("used_seconds", 0) / 60, 1)
        bonus_min = usage.get("bonus_minutes", 0)

        policy = load_policy_cache()
        quota_min = 90
        if policy:
            weekday = datetime.now().weekday()
            quota_min = policy["weekend_quota_minutes"] if weekday >= 5 else policy["weekday_quota_minutes"]

        total_allowed = quota_min + bonus_min
        remaining_min = max(0, total_allowed - int(used_min))

        if self.stat_title:
            self.stat_title.config(text=f"⏱️ Thời Gian Dùng Máy Hôm Nay: {used_min} / {total_allowed} phút")
        if self.rem_lbl:
            bonus_info = f" (Được cộng thêm {bonus_min} phút từ cha mẹ)" if bonus_min > 0 else ""
            self.rem_lbl.config(
                text=f"Còn lại: {remaining_min} phút{bonus_info}",
                fg="#10b981" if remaining_min > 0 else "#ef4444"
            )

    def _manual_refresh(self):
        """Manual refresh triggered by child."""
        self._update_usage_display()
        # Also check server for any newly approved requests
        self._check_server_requests()

    def _schedule_periodic_refresh(self):
        if self.root and self.root.winfo_exists():
            self._update_usage_display()
            self.root.after(2500, self._schedule_periodic_refresh)

    def _check_server_requests(self):
        """Check if pending request was reviewed and alert the child."""
        try:
            creds = load_credentials()
            if not creds:
                return
            dev_id = creds.get("device_id", 1)
            token = creds.get("access_token")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            res = requests.get(f"{self.server_url}/api/v1/requests?device_id={dev_id}", headers=headers, timeout=5)
            if res.status_code == 200:
                requests_data = res.json()
                for req in requests_data:
                    req_id = req.get("id")
                    status = req.get("status")
                    req_type = req.get("request_type")
                    target = req.get("target")

                    if req_id and req_id in self.notified_req_ids:
                        continue

                    if status == "rejected":
                        if req_id:
                            self.notified_req_ids.add(req_id)
                        if req_type == "unblock_domain":
                            messagebox.showwarning(
                                "Thông Báo Từ Phụ Huynh",
                                f"Phụ huynh chưa đồng ý mở trang web '{target}'. Hãy tập trung học tập con nhé!"
                            )
                        elif req_type == "unblock_app":
                            messagebox.showwarning(
                                "Thông Báo Từ Phụ Huynh",
                                f"Phụ huynh chưa đồng ý mở ứng dụng '{target}'. Hãy tập trung học tập con nhé!"
                            )
                        elif req_type == "add_time":
                            messagebox.showwarning(
                                "Thông Báo Từ Phụ Huynh",
                                "Phụ huynh chưa đồng ý cộng thêm giờ sử dụng máy tính."
                            )

                    elif status == "approved":
                        if req_type == "add_time":
                            usage = get_daily_usage(self.today_str)
                            current_bonus = usage.get("bonus_minutes", 0)
                            if current_bonus == 0:
                                from .storage import update_daily_usage
                                update_daily_usage(
                                    date_str=self.today_str,
                                    used_seconds=usage.get("used_seconds", 0),
                                    bonus_minutes=15,
                                    is_locked=0
                                )
                                self._update_usage_display()
                                if req_id:
                                    self.notified_req_ids.add(req_id)
                                messagebox.showinfo("Tuyệt Vời!", "Cha mẹ đã đồng ý thưởng thêm 15 phút cho em học tập!")
                        elif req_type in ("unblock_domain", "unblock_app"):
                            if req_id:
                                self.notified_req_ids.add(req_id)
                            label = "trang web" if req_type == "unblock_domain" else "ứng dụng"
                            messagebox.showinfo(
                                "Đã Mở Chặn Thành Công",
                                f"Ba mẹ đã đồng ý mở {label} '{target}'. Em có thể sử dụng được rồi nhé!"
                            )
        except Exception:
            pass

    def _send_request(self, request_type: str, target: str, reason: str):
        """Submit access request to the central server (NT3)."""
        creds = load_credentials()
        device_id = creds["device_id"] if creds else 1
        token = creds["access_token"] if creds else None

        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        payload = {
            "device_id": device_id,
            "child_id": None,
            "request_type": request_type,
            "target": target,
            "reason": reason
        }

        try:
            url = f"{self.server_url}/api/v1/requests"
            resp = requests.post(url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)
            if resp.status_code in (200, 201):
                messagebox.showinfo(
                    "Đã Gửi Thành Công",
                    "Yêu cầu của em đã được gửi trực tiếp tới máy của cha mẹ!\nCha mẹ sẽ xem và phê duyệt trên Bảng điều khiển."
                )
            else:
                messagebox.showerror(
                    "Lỗi Gửi Yêu Cầu",
                    f"Máy chủ phản hồi: {resp.status_code} - {resp.text}"
                )
        except Exception as e:
            messagebox.showerror(
                "Lỗi Kết Nối",
                f"Không thể kết nối tới máy chủ của cha mẹ: {e}"
            )

    def _dialog_request_time(self):
        """Prompt child for reason to request extra 15 minutes."""
        dlg = tk.Toplevel(self.root)
        dlg.title("Xin Thêm Giờ Học Tập")
        dlg.geometry("380x200")
        dlg.configure(bg="#0f172a", padx=14, pady=14)
        dlg.transient(self.root)
        dlg.grab_set()

        lbl = tk.Label(
            dlg,
            text="Lý do em xin thêm 15 phút (để làm bài tập, đọc sách...):",
            font=("Segoe UI", 9),
            fg="#fff",
            bg="#0f172a"
        )
        lbl.pack(anchor=tk.W)

        reason_entry = tk.Entry(dlg, font=("Segoe UI", 10), width=40)
        reason_entry.insert(0, "Em cần thêm thời gian hoàn thành bài tập toán.")
        reason_entry.pack(fill=tk.X, pady=8)

        def on_submit():
            reason = reason_entry.get().strip()
            dlg.destroy()
            self._send_request(request_type="add_time", target="15", reason=reason)

        btn_submit = tk.Button(
            dlg,
            text="Gửi Cho Cha Mẹ",
            font=("Segoe UI", 9, "bold"),
            bg="#0284c7",
            fg="#fff",
            pady=4,
            relief=tk.FLAT,
            command=on_submit
        )
        btn_submit.pack(fill=tk.X, pady=(6, 0))

    def _dialog_unblock_request(self):
        """Prompt child for target domain/app to report false-positive block."""
        dlg = tk.Toplevel(self.root)
        dlg.title("Báo Chặn Nhầm Web / Ứng Dụng")
        dlg.geometry("400x240")
        dlg.configure(bg="#0f172a", padx=14, pady=14)
        dlg.transient(self.root)
        dlg.grab_set()

        lbl1 = tk.Label(
            dlg,
            text="Tên Website hoặc Ứng dụng em cần dùng:",
            font=("Segoe UI", 9),
            fg="#fff",
            bg="#0f172a"
        )
        lbl1.pack(anchor=tk.W)

        target_entry = tk.Entry(dlg, font=("Segoe UI", 10), width=40)
        target_entry.pack(fill=tk.X, pady=(2, 8))

        lbl2 = tk.Label(
            dlg,
            text="Lý do trang web/ứng dụng này an toàn và cần thiết:",
            font=("Segoe UI", 9),
            fg="#fff",
            bg="#0f172a"
        )
        lbl2.pack(anchor=tk.W)

        reason_entry = tk.Entry(dlg, font=("Segoe UI", 10), width=40)
        reason_entry.insert(0, "Đây là trang tài liệu học tập của trường học em.")
        reason_entry.pack(fill=tk.X, pady=(2, 10))

        def on_submit():
            target = target_entry.get().strip()
            reason = reason_entry.get().strip()
            if not target:
                messagebox.showwarning("Thiếu Thông Tin", "Vui lòng nhập tên website hoặc app.")
                return
            dlg.destroy()
            req_type = "unblock_app" if target.lower().endswith(".exe") else "unblock_domain"
            self._send_request(request_type=req_type, target=target, reason=reason)

        btn_submit = tk.Button(
            dlg,
            text="Gửi Yêu Cầu Cho Cha Mẹ",
            font=("Segoe UI", 9, "bold"),
            bg="#d97706",
            fg="#fff",
            pady=4,
            relief=tk.FLAT,
            command=on_submit
        )
        btn_submit.pack(fill=tk.X)


if __name__ == "__main__":
    app = ChildViewWindow()
    app.show()
