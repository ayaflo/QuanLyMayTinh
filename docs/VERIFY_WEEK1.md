# KỊCH BẢN NGHIỆM THU ĐẦU–CUỐI TUẦN 1 (VERIFICATION & DEMO WALKTHROUGH)
## ĐỀ TÀI: OPEN GUARDIAN KIDS (OGK) — VERSION 0.1

> **Mục tiêu nghiệm thu:** Kiểm chứng tính toàn vẹn của luồng hoạt động khép vòng giữa 3 phân hệ:  
> **OGK-Agent (Máy con) ⟷ OGK-Server (FastAPI) ⟷ Dashboard (Web Phụ huynh)**.  
> Xác nhận hoàn thành đầy đủ 46 Micro-tasks của Tuần 1 trước khi tiến hành bước sang Tuần 2.

---

## 1. ĐIỀU KIỆN TIÊN QUYẾT (PREREQUISITES)

1. Máy tính chạy Windows 10/11 x64 với Python 3.11+.
2. Đã khởi tạo môi trường ảo `.venv` và cài đặt đầy đủ các gói:
   ```powershell
   # Kích hoạt môi trường ảo
   .\.venv\Scripts\Activate.ps1
   ```
3. Đảm bảo tệp `.env` đã được cấu hình (sao chép từ `.env.example`):
   ```env
   SECRET_KEY=change-this-secret-key-in-production
   SERVER_HOST=127.0.0.1
   SERVER_PORT=8000
   DATABASE_URL=sqlite:///./ogk.db
   ```

---

## 2. KỊCH BẢN CHẠY THỬ NGHIỆM TỪNG BƯỚC (STEP-BY-STEP E2E)

### Bước 1: Khởi tạo dữ liệu mẫu và chạy Máy chủ Server

1. Nạp tài khoản phụ huynh mẫu vào cơ sở dữ liệu `ogk.db`:
   ```powershell
   python server/seed.py
   ```
   *Kết quả kỳ vọng:* Xuất hiện thông báo:  
   `[SEED] Tạo tài khoản phụ huynh mẫu thành công: parent_admin / Admin@123456`

2. Khởi chạy máy chủ FastAPI:
   ```powershell
   python server/main.py
   # hoặc: uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   *Kết quả kỳ vọng:* Máy chủ lắng nghe tại `http://127.0.0.1:8000`. Kiểm tra API docs tại `http://127.0.0.1:8000/docs`.

---

### Bước 2: Đăng nhập Bảng điều khiển Phụ huynh (Dashboard)

1. Mở trình duyệt web truy cập: `http://127.0.0.1:8000/login`
2. Nhập thông tin đăng nhập:
   * **Tên đăng nhập:** `parent_admin`
   * **Mật khẩu:** `Admin@123456`
3. Nhấn **"Đăng nhập"**.
   * *Kết quả kỳ vọng:* Đăng nhập thành công, trình duyệt nhận Cookie `access_token` và tự động chuyển hướng sang trang quản lý thiết bị `http://127.0.0.1:8000/devices`.

---

### Bước 3: Tạo mã ghép đôi 8 ký tự (Pairing Code)

1. Tại giao diện **"Quản lý thiết bị"**, nhấn nút **"+ Thêm thiết bị mới"**.
2. Một bảng popup xuất hiện:
   * Hiển thị mã ghép đôi gồm đúng 8 ký tự in hoa/chữ số (ví dụ: `H7M9K2XB`).
   * Đồng hồ đếm ngược thời gian hiệu lực 10:00 (600 giây).
   * Hướng dẫn phụ huynh nhập mã này vào ứng dụng Agent trên máy tính của trẻ.

---

### Bước 4: Khởi chạy Tác tử Agent trên máy tính trẻ

1. Mở một cửa sổ PowerShell mới (với môi trường `.venv` đã kích hoạt) và chạy:
   ```powershell
   python agent/main.py
   ```
2. Nếu máy tính chưa từng ghép đôi, ứng dụng sẽ yêu cầu nhập mã:
   ```text
   === OPEN GUARDIAN KIDS - THIẾT LẬP THIẾT BỊ ===
   Chưa tìm thấy thông tin ghép đôi trên máy tính này.
   Vui lòng nhập mã ghép đôi 8 ký tự từ Dashboard phụ huynh:
   > 
   ```
3. Nhập chính xác mã 8 ký tự đã tạo ở **Bước 3** và nhấn Enter.

---

### Bước 5: Kiểm tra kết quả ghép đôi và nguyên tắc NT1

1. **Trên màn hình console của Agent:**
   * Xuất hiện thông báo thành công:  
     `[ENROLL] Ghép đôi thành công! Thiết bị ID: 1, Token được lưu vào agent_cache.db`
2. **Khay hệ thống (System Tray) & Thông báo Windows (NT1):**
   * Biểu tượng khay hệ thống của Open Guardian Kids xuất hiện bên góc phải thanh Taskbar.
   * Thông báo Windows Popup hiện lên:  
     *"Open Guardian Kids đang hoạt động và đồng hành cùng em."*
3. **Kiểm tra bộ nhớ cục bộ:**
   * Tệp `agent_cache.db` được tạo tự động chứa `device_id`, `access_token`, `refresh_token`.

---

### Bước 6: Kiểm tra Nhịp tim Viễn trắc & Trạng thái Online

1. Agent tự động kích hoạt tiến trình nền gửi nhịp tim định kỳ mỗi 60 giây lên `POST /api/v1/heartbeat`.
2. Quan sát bảng điều khiển phụ huynh `http://127.0.0.1:8000/devices`:
   * Thiết bị mới xuất hiện trong danh sách kèm tên máy (ví dụ: `Windows PC`).
   * Huy hiệu trạng thái chuyển sang **"Online"** (màu xanh lá cây sáng).
   * Cột "Nhịp tim gần nhất" hiển thị dấu thời gian thực tế vừa cập nhật.

---

### Bước 7: Kiểm chứng trạng thái ngắt kết nối (Offline Detection)

1. Tắt tiến trình `agent/main.py` (nhấn `Ctrl + C` hoặc chọn Thoát từ icon khay hệ thống).
2. Chờ sau 120 giây (ngưỡng 2 chu kỳ nhịp tim bị bỏ lỡ).
3. Tải lại trang Dashboard hoặc đợi tự động làm mới:
   * Trạng thái thiết bị tự động chuyển từ **"Online"** sang **"Offline"** (màu xám).
   * Điều này chứng minh thuật toán kiểm tra nhịp tim hoạt động chính xác và trung thực.

---

## 3. KIỂM THỬ TỰ ĐỘNG BẰNG PYTEST (AUTOMATED TEST SUITE)

Để kiểm chứng toàn bộ 100% các chức năng máy chủ mà không cần thao tác tay, chạy lệnh kiểm thử toàn diện:

```powershell
.\.venv\Scripts\pytest.exe -v
```

### Danh mục 15 Test cases tự động đã đạt:
* **`tests/test_auth.py` (5 tests):**
  - `test_argon2_hash_and_verify`: Băm Argon2id và kiểm tra đúng/sai mật khẩu.
  - `test_jwt_token_creation_and_tampering`: Tạo token HMAC-SHA256, kiểm tra thời hạn và từ chối chữ ký bị can thiệp.
  - `test_login_success`: Đăng nhập đúng, kiểm tra Token và Cookie.
  - `test_login_wrong_password`: Từ chối đăng nhập với mật khẩu sai.
  - `test_login_nonexistent_user`: Từ chối đăng nhập với tài khoản không tồn tại.
* **`tests/test_enrollment.py` (6 tests):**
  - `test_generate_code_format`: Sinh mã 8 ký tự, loại bỏ ký tự dễ nhầm lẫn.
  - `test_create_code_endpoint_unauthorized`: Chặn người dùng chưa xác thực tạo mã.
  - `test_create_code_endpoint_success`: Tạo mã và lưu vào CSDL với thời hạn 10 phút.
  - `test_claim_device_endpoint_success`: Agent ghép đôi thành công, gán máy tính cho phụ huynh.
  - `test_claim_device_reuse_code_rejected`: Chặn sử dụng lại mã ghép đôi đã dùng.
  - `test_claim_device_expired_code_rejected`: Chặn mã ghép đôi đã hết hạn.
* **`tests/test_heartbeat.py` (4 tests):**
  - `test_heartbeat_with_bearer_token`: Nhận nhịp tim kèm token, lưu log telemetry và cập nhật trạng thái Online.
  - `test_heartbeat_with_fingerprint_fallback`: Dự phòng nhận diện bằng mã fingerprint.
  - `test_heartbeat_unknown_device_rejected`: Chặn nhịp tim từ thiết bị lạ chưa đăng ký.
  - `test_online_status_threshold_calculation`: Kiểm tra công thức ngưỡng thời gian 120 giây phân định Online/Offline.

---

## 4. BẢNG TIÊU CHÍ HOÀN THÀNH TUẦN 1 (DEFINITION OF DONE CHECKLIST)

- [x] **DoD 1:** Phụ huynh đăng nhập vào Dashboard thành công với tài khoản đã seed.
- [x] **DoD 2:** Tạo mã ghép đôi 8 ký tự trên Dashboard; chạy Agent nhập mã; Server xác nhận ghép đôi và cấp token thành công.
- [x] **DoD 3:** Agent gửi nhịp tim mỗi 60 giây; Dashboard tự cập nhật trạng thái thiết bị là "Online".
- [x] **DoD 4:** Đảm bảo nguyên tắc minh bạch NT1 (khay hệ thống và thông báo khởi động).
- [x] **DoD 5:** Hoàn thành tài liệu kiến trúc kỹ thuật (`docs/KienTrucHeThong.md`) và cam kết bảo vệ dữ liệu theo Nghị định 13/2023 (`docs/PRIVACY.md`).
- [x] **DoD 6:** 15/15 bài kiểm thử tự động `pytest` vượt qua với tỷ lệ thành công 100%.
