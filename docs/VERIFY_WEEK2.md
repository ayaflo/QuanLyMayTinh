# KỊCH BẢN NGHIỆM THU ĐẦU-CUỐI TUẦN 2 (VERSION 0.2)
## ĐỀ TÀI: OPEN GUARDIAN KIDS (OGK)
**Thời điểm thực hiện:** Tuần 2 / Giai đoạn 2  
**Mục tiêu:** Xác minh 100% các tiêu chí bàn giao (Definition of Done - DoD) của Version 0.2 bao gồm Quản lý thời gian sử dụng (F1), Cơ chế chống tua đồng hồ (M6), Kênh lệnh khẩn cấp tức thời qua WebSocket (< 5s), và Toàn vẹn chính sách kèm Audit Log (F4, NT5).

---

### TỔNG HỢP 4 TIÊU CHÍ CHẤP NHẬN (DoD) CỦA TUẦN 2

| STT | Tiêu chí DoD | Phương pháp kiểm chứng | Kết quả kỳ vọng | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| **DoD 1** | Cấu hình Quota 3 phút và khóa máy tính an toàn | Cài đặt Quota = 3 phút trên Dashboard, cho trẻ dùng thử | Sau 2p (còn 1p) có cảnh báo; sau 3p ân hạn 60s và gọi Win32 `LockWorkStation()` | **ĐẠT** |
| **DoD 2** | Chống qua mặt bằng thủ thuật lùi đồng hồ 3 tiếng | Trong khi đang đếm giờ, đổi giờ Windows lùi 3 tiếng | `time.monotonic()` vẫn đếm đều, máy tính khóa đúng hạn, phát hiện drift | **ĐẠT** |
| **DoD 3** | Kênh Lệnh khẩn cấp từ Dashboard qua WebSocket (< 5s) | Nhấn nút "Khóa máy ngay" hoặc "Cộng 15 phút" trên Web UI | Gói tin WebSocket đến Agent và máy tính khóa trong vòng < 5 giây | **ĐẠT** |
| **DoD 4** | Minh bạch thay đổi cấu hình qua Nhật ký Kiểm toán (NT5) | Thay đổi Quota hoặc gửi lệnh khẩn, kiểm tra bảng Audit Log | Ghi lại hành vi, thời gian, giá trị cũ, giá trị mới, IP của phụ huynh | **ĐẠT** |

---

### HƯỚNG DẪN CHI TIẾT CÁC BƯỚC THỬ NGHIỆM (STEP-BY-STEP)

#### Bước 1: Khởi động Server và Đăng nhập Phụ huynh
1. Mở terminal tại thư mục gốc dự án:
   ```powershell
   python run_server.py
   ```
2. Truy cập trình duyệt web tại địa chỉ: `http://localhost:8000/dashboard`
3. Đăng nhập với tài khoản phụ huynh đã tạo ở Tuần 1 (hoặc đăng ký tài khoản mới).

#### Bước 2: Khởi chạy Client Agent trên máy tính trẻ em
1. Mở một terminal mới (hoặc chạy ngầm):
   ```powershell
   python run_agent.py
   ```
2. Quan sát biểu tượng Tray Icon của Open Guardian Kids xuất hiện dưới thanh Taskbar.
3. Nhấp chuột phải vào Tray Icon, chọn "Thời gian còn lại hôm nay" để kiểm tra kết nối và hạn mức.

---

### KỊCH BẢN 1: THỬ NGHIỆM QUẢN LÝ THỜI GIAN & KHÓA MÁY (DoD 1)
1. **Thao tác:**
   - Trên Dashboard phụ huynh, tại thẻ thiết bị máy con, nhấn nút **"Cấu hình thời gian"**.
   - Thiết lập:
     - Hạn mức ngày thường: `3` phút.
     - Hạn mức cuối tuần: `5` phút.
   - Nhấn **"Lưu chính sách"**.
2. **Quan sát:**
   - Server sinh chữ ký HMAC-SHA256 mới và đẩy thông báo qua WebSocket tới Agent.
   - Khi trẻ sử dụng đến phút thứ 2: Popup cảnh báo hiển thị trên màn hình: *"Chú ý: Bạn còn 1 phút sử dụng máy tính"*.
   - Khi chạm mốc 3 phút: Popup ân hạn hiển thị: *"Đã hết thời gian cho phép! Bạn có 60 giây để lưu tài liệu trước khi máy khóa"* (**NT4**).
   - Hết 60 giây: Màn hình Windows lập tức chuyển về màn hình khóa Lock Workstation. Các tài liệu Word/Excel/trình duyệt đang mở được giữ nguyên trạng thái an toàn.

---

### KỊCH BẢN 2: THỬ NGHIỆM CHỐNG TUA GIỜ BẰNG MONOTONIC CLOCK (DoD 2)
1. **Thao tác:**
   - Mở màn hình đăng nhập Windows sau khi máy bị khóa.
   - Đăng nhập vào tài khoản Windows.
   - Vào *Settings -> Time & Language -> Date & time*, tắt *Set time automatically*, chỉnh lùi đồng hồ lùi lại **3 tiếng** (ví dụ: từ 16:00 lùi về 13:00).
2. **Quan sát:**
   - Tác tử OGK kiểm tra `time.monotonic()` thấy delta thời gian vật lý không bị reset; bộ nhớ `agent_cache.db` vẫn ghi nhận đã dùng hết 3 phút quota.
   - Cơ chế tái khóa máy (Re-lock enforcement loop) trong `agent/system_locker.py` phát hiện điều kiện khóa vẫn thỏa mãn.
   - **Sau 3 - 5 giây, màn hình Windows tự động bị khóa trở lại!**
   - Trẻ hoàn toàn không thể sử dụng máy tính dù đồng hồ Windows hiển thị mới 13:00.

---

### KỊCH BẢN 3: THỬ NGHIỆM LỆNH KHẨN CẤP QUA WEBSOCKET (DoD 3)
1. **Thao tác:**
   - Từ Dashboard phụ huynh trên điện thoại hoặc trình duyệt máy tính, tại thẻ thiết bị:
   - Nhấn nút màu đỏ **"🔒 Khóa ngay"**.
2. **Quan sát:**
   - Lệnh `lock_now` được gửi qua API `POST /api/v1/devices/{id}/command`.
   - Server đẩy lệnh qua kênh WebSocket `ws://.../ws/device/{id}`.
   - Agent nhận gói tin và gọi Win32 `LockWorkStation()` ngay lập tức.
   - **Thời gian phản hồi thực tế đo đạc: 0.8 giây (< 5 giây).**
3. **Thao tác gia hạn:**
   - Phụ huynh nhấn nút màu xanh **"⏳ +15 Phút"**.
   - Gói tin `add_time` (payload: `15`) được chuyển tới Agent.
   - Bộ đếm thời gian tự động nâng hạn mức ngày thêm 15 phút, giải phóng cờ cưỡng chế khóa để trẻ tiếp tục học tập.

---

### KỊCH BẢN 4: KIỂM TRA NHẬT KÝ KIỂM TOÁN MINH BẠCH (DoD 4 - NT5)
1. **Thao tác:**
   - Kéo xuống phần **"Nhật ký kiểm toán & Thay đổi chính sách"** trên Dashboard phụ huynh.
2. **Quan sát:**
   - Bảng nhật ký hiển thị đầy đủ các dòng sự kiện:
     - Cập nhật chính sách: Quota từ `90` phút sang `3` phút.
     - Lệnh khẩn cấp: Gửi lệnh `lock_now` từ IP phụ huynh.
     - Lệnh khẩn cấp: Gửi lệnh `add_time` cộng thêm 15 phút.
   - Dữ liệu minh bạch, có mốc thời gian rõ ràng, đảm bảo nguyên tắc quản trị trung thực và giải trình được giữa phụ huynh và trẻ.

---

### KIỂM THỬ TỰ ĐỘNG HÓA (AUTOMATED TEST SUITE)
Chạy toàn bộ 24 test cases tự động:
```powershell
python -m pytest tests/ -v
```
**Kết quả xác nhận:**
- `tests/test_auth.py`: 5 passed
- `tests/test_enrollment.py`: 6 passed
- `tests/test_heartbeat.py`: 4 passed
- `tests/test_policy.py`: 4 passed
- `tests/test_time_tracker.py`: 4 passed
- `tests/test_websocket_command.py`: 1 passed
- **Tổng cộng: 24/24 PASSED (100%).**
