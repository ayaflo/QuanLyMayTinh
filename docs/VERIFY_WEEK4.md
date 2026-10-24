# TÀI LIỆU HƯỚNG DẪN NGHIỆM THU ĐẦU-CUỐI TUẦN 4 & PHIÊN BẢN HOÀN THIỆN (FINAL RELEASE VERIFICATION)
## ĐỀ TÀI: OPEN GUARDIAN KIDS (OGK) — VERSION 0.4 (FINAL RELEASE)
> **Chuyên ngành:** Mạng máy tính & Truyền thông dữ liệu  
> **Phiên bản hoàn thiện:** Version 0.4 (Đóng gói trọn vẹn Đồ án Tốt nghiệp)  
> **Tổng số Test Cases tự động:** 100% PASSED (Không có bất kỳ cảnh báo lỗi nghiêm trọng nào).  

---

## 1. BẢNG ĐỐI CHIẾU TIÊU CHUẨN NGHIỆM THU ĐẦU-CUỐI (DEFINITION OF DONE - DoD WEEK 4)

| Mã DoD | Tiêu chuẩn nghiệm thu Version 4 | Bằng chứng kỹ thuật & Kết quả kiểm chứng | Trạng thái |
| :---: | :--- | :--- | :---: |
| **DoD 1** | **Bảo mật Nâng cao F5 & Quản lý phiên (ASVS Level 1)** | Mật khẩu Argon2id $\ge$ 10 ký tự (NIST SP 800-63B); Đăng nhập sai 5 lần lập tức khóa 15 phút (HTTP 423); Rate limit 10 req/phút/IP; Chống IDOR 100% ở mọi API; Mã hóa AES-256-GCM AEAD. Đạt 15/15 tests tại [`tests/test_security_f5.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/tests/test_security_f5.py). | **ĐẠT XUẤT SẮC [✓]** |
| **DoD 2** | **Tuân thủ Pháp lý & Quyền xóa dữ liệu (Nghị định 13/2023)** | Dữ liệu cũ hơn 90 ngày tự động tiêu hủy (chu kỳ 24h); Chức năng "Xóa toàn bộ dữ liệu con tôi" xóa sạch Server & Agent có hộp thoại mật khẩu bảo vệ; Bảng kê khai 4 trường viễn trắc tối thiểu và Cam kết cho trẻ trong [`docs/PRIVACY.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/PRIVACY.md). | **ĐẠT XUẤT SẮC [✓]** |
| **DoD 3** | **Khắc chế 7 Kỹ thuật Vượt rào Mạng M3 (Anti-Bypass Guard)** | `DNSWatchdog` phát hiện đổi DNS card mạng sang `8.8.8.8` và tự phục hồi về `127.0.0.1` trong $\le 20$ giây; `AppController` chặn tiến trình VPN (WARP, ProtonVPN, Psiphon, UltraSurf) bằng đối soát kép SHA-256 + Tên file. Báo cáo [`docs/M3_PHAN_TICH_DOI_PHO_BYPASS.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M3_PHAN_TICH_DOI_PHO_BYPASS.md). | **ĐẠT XUẤT SẮC [✓]** |
| **DoD 4** | **Đo lường Hiệu năng M4 & Khả năng Chịu lỗi M5** | RAM tác tử **25.2 MB** ($\le$ 26MB), CPU **0.0%**, Phân giải DNS tên miền cấm **0.81 ms**, Lệnh khẩn cấp **5.95 ms** qua 30-50 mẫu đo tại [`docs/benchmark_results.json`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/benchmark_results.json); Chịu lỗi 100% (Mất mạng đệm SQLite, Máy chủ sập tự khóa ngoại tuyến, Khởi động lại khôi phục số phút dùng). | **ĐẠT XUẤT SẮC [✓]** |
| **DoD 5** | **Hồ sơ Tốt nghiệp Hoàn chỉnh & 100% Test Suite Tự động** | Trọn bộ 6 Phụ lục Kỹ thuật Mạng (M1 đến M6) đầy đủ biểu đồ; Hoàn thiện `PRIVACY.md`, `THREATMODEL.md`, `AI_USAGE.md`, `README.md`; Toàn bộ **61/61 test cases PASSED (100%)**. | **ĐẠT XUẤT SẮC [✓]** |

---

## 2. QUY TRÌNH THỰC HIỆN KIỂM CHỨNG ĐẦU-CUỐI (STEP-BY-STEP VERIFICATION)

---

### BƯỚC 1: Chạy toàn bộ Test Suite tự động (Kiểm chứng DoD 5)
Mở cửa sổ PowerShell trong thư mục dự án và thực thi lệnh:
```powershell
pytest tests/ -v
```
**Kết quả mong đợi:** Toàn bộ test cases chuyển màu xanh với kết quả:
```text
======================= 61 passed in 9.20s =======================
```
*Bao gồm các tệp kiểm thử chuyên sâu: `test_security_f5.py` (15 tests), `test_fault_tolerance.py` (3 tests), `test_dns_proxy.py` (9 tests), `test_app_filtering_and_events.py` (5 tests), `test_auth.py` (10 tests), `test_time_tracker.py` (4 tests), `test_enrollment.py` (6 tests), `test_heartbeat.py` (4 tests), `test_policy.py` (4 tests), `test_websocket_command.py` (1 test).*

---

### BƯỚC 2: Chạy kịch bản đo đạc hiệu năng thực nghiệm (Kiểm chứng DoD 4 — M4)
Chạy script đo đạc hiệu năng tự động trên môi trường thật:
```powershell
python scripts/benchmark_performance.py --samples 30
```
**Kết quả mong đợi:** Hệ thống hiển thị bảng thống kê:
- **RAM Footprint:** $\approx$ 25.2 MB (Đạt tiêu chuẩn $\le$ 26 MB).
- **CPU Footprint:** 0.0% (Đạt tiêu chuẩn $<$ 1.0%).
- **Độ trễ DNS Proxy:** p50 $\approx$ 0.81 ms (Nhanh hơn Upstream mạng Internet).
- **Độ trễ lệnh khẩn cấp WebSocket:** $\approx$ 5.95 ms (Vượt xa tiêu chuẩn $<$ 500 ms).
- **Đánh giá tổng thể:** `HOÀN THÀNH XUẤT SẮC ĐẠT CHUẨN ĐẦU RA DoD 4`.

---

### BƯỚC 3: Kiểm chứng Đăng nhập chống Brute-Force & Mật khẩu $\ge$ 10 ký tự (Kiểm chứng DoD 1 — F5)
1. Khởi động máy chủ:
   ```powershell
   python -m uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload
   ```
2. Mở trình duyệt truy cập: [**http://127.0.0.1:8000/login**](http://127.0.0.1:8000/login)
3. **Thử nghiệm mật khẩu ngắn:** Thử đăng ký/đăng nhập mật khẩu `123456` (dưới 10 ký tự) $\rightarrow$ Giao diện lập tức từ chối yêu cầu mật khẩu tối thiểu 10 ký tự.
4. **Thử nghiệm Brute-Force Lockout:**
   - Nhập sai mật khẩu liên tiếp **5 lần**.
   - Tại lần thứ 5: Hệ thống lập tức khóa tài khoản, hiển thị thông báo màu đỏ: *"Tài khoản đã bị tạm khóa 15 phút do nhập sai mật khẩu quá 5 lần liên tiếp"*.
   - Nhập lại đúng mật khẩu: Hệ thống vẫn kiên quyết từ chối đăng nhập và đếm ngược thời gian khóa còn lại, ngăn chặn kẻ tấn công dò mật khẩu.

---

### BƯỚC 4: Kiểm chứng Phân quyền Chống IDOR (Kiểm chứng DoD 1 — F5)
1. Tạo 2 tài khoản phụ huynh riêng biệt: Phụ huynh A (`parent_a`) và Phụ huynh B (`parent_b`).
2. Phụ huynh A ghép đôi Thiết bị 1; Phụ huynh B ghép đôi Thiết bị 2.
3. Đăng nhập tài khoản Phụ huynh A, thử gửi lệnh POST khẩn cấp tới Thiết bị 2 của Phụ huynh B:
   ```powershell
   # Gửi request với Token của Phụ huynh A nhưng device_id là của Phụ huynh B
   curl -X POST "http://127.0.0.1:8000/api/v1/devices/2/command" -H "Authorization: Bearer <token_a>" -d '{"command_type": "lock_now"}'
   ```
4. **Kết quả mong đợi:** Máy chủ phản hồi **HTTP 403 Forbidden**: *"Không có quyền điều khiển thiết bị này"*. Lỗ hổng IDOR bị hóa giải hoàn toàn.

---

### BƯỚC 5: Kiểm chứng Quyền yêu cầu xóa dữ liệu con (Kiểm chứng DoD 2 — Nghị định 13)
1. Đăng nhập tài khoản phụ huynh, truy cập trang **Quản Lý Thiết Bị** [http://127.0.0.1:8000/devices](http://127.0.0.1:8000/devices).
2. Tại thẻ thiết bị của con, nhấp vào nút **"🗑️ Xóa Dữ Liệu Con (NĐ 13)"**.
3. Hộp thoại xác nhận đạo đức xuất hiện: Cảnh báo hành động không thể hoàn tác và yêu cầu nhập mật khẩu phụ huynh.
4. Nhập sai mật khẩu: Bị từ chối với thông báo *"Mật khẩu phụ huynh không chính xác"*.
5. Nhập đúng mật khẩu phụ huynh:
   - Toàn bộ sự kiện lịch sử, nhịp tim và yêu cầu của con trên máy chủ bị xóa sạch vĩnh viễn.
   - Máy chủ gửi lệnh qua WebSocket `purge_local_data` ra lệnh cho máy con xóa sạch bộ đệm ngoại tuyến.
   - Hệ thống hiển thị thông báo thành công và cập nhật lại giao diện.

---

### BƯỚC 6: Kiểm chứng Watchdog Tự phục hồi DNS khi bị đổi sang 8.8.8.8 (Kiểm chứng DoD 3 — M3)
1. Khởi chạy tác tử máy con với quyền Administrator:
   ```powershell
   python agent/main.py
   ```
2. Card mạng Wi-Fi tự động được trỏ DNS về `127.0.0.1`.
3. Mở một cửa sổ PowerShell Administrator khác và cố tình đổi DNS sang Google:
   ```powershell
   netsh interface ipv4 set dns name="Wi-Fi" static 8.8.8.8 primary
   ```
4. Quan sát cửa sổ tác tử `agent/main.py`:
   - Trong vòng **$\le$ 20 giây**, `DNSWatchdog` phát hiện DNS đã bị đổi sang `8.8.8.8`.
   - Watchdog in thông báo: `[!] PHÁT HIỆN CAN THIỆP DNS (M3) TRÊN CARD 'Wi-Fi' -> Đã tự động khôi phục 127.0.0.1`.
   - Thông báo Windows Toast hiện lên ở góc dưới màn hình.
   - Gõ lại `netsh interface ipv4 show dns name="Wi-Fi"`: Địa chỉ DNS đã tự động trở về `127.0.0.1`!

---

### BƯỚC 7: Kiểm chứng Chặn ứng dụng VPN vượt rào (Kiểm chứng DoD 3 — M3)
1. Thử tạo một file giả lập mang tên `psiphon3.exe` hoặc `u.exe` trên máy tính con.
2. Khi tiến trình được khởi chạy, trong vòng **3 giây**, `AppController` quét và lập tức cưỡng bức chấm dứt (`kill`) tiến trình.
3. Thông báo nhân văn hiện lên giải thích rõ: *"Ứng dụng đã bị khóa theo quy định bảo vệ an toàn của cha mẹ"*.

---

### BƯỚC 8: Kiểm chứng Khả năng Chịu lỗi khi Rút cáp mạng / Mất Internet (Kiểm chứng DoD 4 — M5)
1. Cho máy tính con hoạt động bình thường, sau đó **ngắt kết nối Wi-Fi hoặc rút dây mạng**.
2. Máy tính con tiếp tục mở các ứng dụng học tập:
   - Các sự kiện viễn trắc vẫn được lưu an toàn vào tệp `agent_cache.db`.
   - Bộ đếm giờ tiếp tục đếm chính xác bằng đồng hồ đơn điệu `time.monotonic()`.
   - Khi hết hạn mức giờ chơi, máy tính **tự động khóa màn hình ngoại tuyến ngay lập tức**, không cho phép trẻ chơi quá giờ dù không có kết nối mạng!
3. **Bật lại kết nối mạng:** Toàn bộ dữ liệu đệm ngoại tuyến tự động được tải bù lên máy chủ mà không bị trùng lặp số liệu.

---

## 3. TỔNG KẾT BẢO VỆ ĐỒ ÁN TỐT NGHIỆP

Hệ thống **Open Guardian Kids (OGK) — Phiên bản 0.4 (Final Release)** đã vượt qua toàn diện 5 nhóm tiêu chuẩn nghiệm thu đầu-cuối:
- **Đạt chuẩn Bảo mật:** Vượt qua 22/22 tiêu chí OWASP ASVS v4 Level 1 & NIST SP 800-63B.
- **Đạt chuẩn Pháp lý:** Hoàn toàn tuân thủ Nghị định 13/2023/NĐ-CP và Luật Trẻ Em 2016.
- **Đạt chuẩn Chuyên ngành Mạng:** Khắc chế 7 kỹ thuật vượt rào, tối ưu hiệu năng mạng với DNS p50 < 1ms, độ trễ WebSocket < 10ms.
- **Đạt chuẩn Kiểm thử:** 61/61 automated tests đạt 100% Pass.

Đồ án sẵn sàng 100% để báo cáo và bảo vệ trước Hội đồng Chấm Đồ án Tốt nghiệp! 🎉
