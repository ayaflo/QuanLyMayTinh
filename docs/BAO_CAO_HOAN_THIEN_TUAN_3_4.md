# BÁO CÁO TIẾN ĐỘ VÀ KẾT QUẢ HOÀN THIỆN ĐỒ ÁN (TUẦN 3 & TUẦN 4)
## ĐỀ TÀI: XÂY DỰNG ỨNG DỤNG HỖ TRỢ QUẢN LÝ VIỆC SỬ DỤNG MÁY TÍNH CỦA TRẺ EM
### TÊN GIẢI PHÁP HỆ THỐNG: OPEN GUARDIAN KIDS (OGK) — VERSION 0.3 & VERSION 0.4 (FINAL RELEASE)

> **Chuyên ngành:** Mạng Máy Tính & Truyền Thông Dữ Liệu  
> **Sinh viên thực hiện:** Nhóm sinh viên thực hiện đề tài  
> **Giảng viên hướng dẫn:** Giảng viên hướng dẫn chuyên đề  
> **Thời gian báo cáo:** Giai đoạn 2 (Tuần 3 & Tuần 4 — Hoàn tất và Đóng gói toàn diện)  
> **Trạng thái đồ án:** ĐÃ HOÀN THÀNH 100% CẢ 4 TUẦN — 61/61 AUTOMATED TESTS PASSED (100%)

---

## I. TỔNG QUAN GIAI ĐOẠN TIẾP NỐI (TỪ TUẦN 2 SANG TUẦN 3 & TUẦN 4)

Sau khi hoàn thành xuất sắc **Version 0.1 (Tuần 1: Khung xương sống kết nối Client - Server)** và **Version 0.2 (Tuần 2: Quản trị thời gian đơn điệu `time.monotonic()` và lệnh khẩn cấp WebSocket)**, đề tài tiếp tục triển khai hai giai đoạn nâng cao mang tính cốt lõi của chuyên ngành Mạng Máy Tính & An Toàn Thông Tin:

1. **Tuần 3 — Version 0.3 (Network Filtering, Process Control & Child Transparency):**
   - Hiện thực hóa Tác tử Lọc mạng DNS Sinkhole tại cổng UDP 53 trên máy con.
   - Cơ chế chặn theo danh mục tên miền (Giáo dục, Giải trí, Mạng xã hội, Game, Nội dung không phù hợp).
   - Cơ chế cưỡng bức SafeSearch (Google, Bing, DuckDuckGo) và YouTube Content Filtering bằng kỹ thuật ghi đè CNAME / VIP.
   - Vô hiệu hóa DoH (DNS over HTTPS) bằng NXDOMAIN Canary Domain `use-application-dns.net`.
   - Kiểm soát ứng dụng trên Windows bằng đối soát mã băm nhị phân SHA-256 trên đĩa chống đổi tên tệp thực thi.
   - Giao diện dành riêng cho trẻ em (Tray UI, xem số giờ, xin thêm giờ, báo chặn nhầm) hiện thực hóa Hiến chương NT3, NT5.

2. **Tuần 4 — Version 0.4 (Security Hardening, Anti-Bypass, Benchmarking, Compliance & Packaging):**
   - Gia cố an ninh cấp cao F5 theo chuẩn NIST SP 800-63B và OWASP ASVS v4 Level 1 (Mật khẩu $\ge 10$ ký tự, khóa tài khoản 15 phút sau 5 lần sai, IP rate limiting 10 req/phút, bảo vệ cookie, chống tấn công IDOR 100% các API, mã hóa dữ liệu tĩnh AES-256-GCM AEAD).
   - Tuân thủ pháp lý theo Nghị định 13/2023/NĐ-CP: Tự động tiêu hủy dữ liệu quá 90 ngày và chức năng "Xóa toàn bộ dữ liệu của con" (Right to Erasure) với xác nhận mật khẩu.
   - Tác tử bảo vệ chống vượt rào M3 (`DNSWatchdog` 20s tự động phục hồi DNS card mạng về `127.0.0.1` và bộ chặn tiến trình VPN: WARP, ProtonVPN, Psiphon, UltraSurf).
   - Đo đạc hiệu năng thực nghiệm M4 (RAM 25.13 MB, CPU 0.0%, DNS 0.83 ms, WebSocket 5.91 ms qua $\ge 30$ mẫu đo).
   - Kiểm chứng khả năng chịu lỗi M5 (Mất mạng đệm SQLite, Máy chủ ngừng vẫn đếm giờ và tự khóa offline, Khởi động lại khôi phục số phút dùng).
   - Hoàn thiện trọn bộ 6 Phụ lục Kỹ thuật Mạng (M1 đến M6), Mô hình đe dọa STRIDE, Bản minh bạch AI và Kịch bản nghiệm thu 5 DoD.

---

## II. CHI TIẾT KỸ THUẬT TUẦN 3 — VERSION 0.3: KIỂM SOÁT MẠNG & ỨNG DỤNG

### 1. Kiến trúc DNS Sinkhole Proxy (Cổng UDP 53)
* **Nguyên lý vận hành:**
  - Card mạng máy con (Wi-Fi/Ethernet) được cấu hình trỏ DNS chính về `127.0.0.1`.
  - Tác tử `OGK-Agent` khởi chạy một luồng Socket UDP lắng nghe tại `127.0.0.1:53`.
  - Khi ứng dụng hoặc trình duyệt gửi yêu cầu DNS Query:
    - **Nếu tên miền thuộc danh mục cấm:** DNS Proxy lập tức đóng gói phản hồi DNS Response với địa chỉ IP `0.0.0.0` (Sinkhole), thời gian sống TTL = 60s. Thời gian phản hồi nội bộ chỉ **0.83 ms**, nhanh hơn gấp 40 lần so với truy vấn Internet.
    - **Nếu tên miền hợp lệ:** DNS Proxy chuyển tiếp (Forward) tới DNS Upstream gia đình an toàn (`1.1.1.3` - Cloudflare Families chặn mã độc) và trả kết quả về cho client.

* **Thuật toán Khớp tên miền (Domain Matching & Subdomain Wildcard):**
  - Hỗ trợ đối soát cả tên miền chính xác và mọi tên miền phụ cấp con:
  $$\text{Match}(Q, D) \iff (Q = D) \lor (Q \text{ kết thúc bằng } .D)$$
  - Đảm bảo khi phụ huynh cấm `tiktok.com`, toàn bộ `vt.tiktok.com`, `api.tiktok.com`, `v16.tiktokcdn.com` đều bị chặn đồng loạt.

* **Bảo vệ Danh mục Vĩnh viễn (Nguyên tắc NT6 - Immutable Whitelist):**
  - Các tên miền phục vụ học tập và cứu nạn khẩn cấp (`moet.gov.vn`, `tongdai111.vn`, `chinhphu.vn`, `edu.vn`) được gắn cờ `is_permanent_whitelist = True`.
  - Mã nguồn máy chủ và tác tử kiểm tra cưỡng chế: Bất kỳ luật cấm nào nhắm vào danh mục này đều bị từ chối với ngoại lệ `NT6ViolationError`.

### 2. Cưỡng bức SafeSearch & YouTube Content Filtering
* **Vấn đề thực tế:** Trẻ không vào trang web đen trực tiếp nhưng tìm kiếm hình ảnh nhạy cảm trên Google/Bing hoặc xem video độc hại trên YouTube.
* **Giải pháp kỹ thuật của OGK:**
  - **Google SafeSearch:** Khi phát hiện truy vấn tới `google.com`, `google.com.vn`, DNS Proxy tự động ghi đè bản ghi A trả về IP của `forcesafesearch.google.com` (`216.239.38.120`).
  - **Bing SafeSearch:** Ghi đè `bing.com` trỏ về `strict.bing.com` (`204.79.197.220`).
  - **YouTube Restricted Mode:** Ghi đè các tên miền `youtube.com`, `m.youtube.com`, `youtubei.googleapis.com` trả về địa chỉ VIP của `restrict.youtube.com` (`216.239.38.119`), kích hoạt chế độ kiểm duyệt nội dung nghiêm ngặt nhất cho trẻ em ở cấp độ mạng.

### 3. Vô hiệu hóa DoH (DNS over HTTPS) bằng NXDOMAIN Canary Domain
* **Nguy cơ vượt rào:** Trình duyệt hiện đại (Chrome, Firefox, Edge) tự động kích hoạt DoH để mã hóa gói tin DNS qua cổng HTTPS 443, làm mất tác dụng của DNS Proxy cổng 53.
* **Biện pháp đối phó mạng chuẩn RFC:**
  - DNS Proxy bắt gói tin truy vấn tên miền Canary chuẩn của Mozilla/Google: `use-application-dns.net`.
  - DNS Proxy phản hồi mã trạng thái `NXDOMAIN` (Non-Existent Domain).
  - Trình duyệt nhận được mã `NXDOMAIN` trên mạng nội bộ sẽ tự động tắt tính năng DoH và quay trở về phân giải qua DNS Socket cổng 53 của hệ điều hành.

### 4. Kiểm soát Ứng dụng bằng mã băm SHA-256 (Process Control)
* **Nguy cơ vượt rào:** Trẻ đổi tên file `roblox.exe` thành `winword.exe` hoặc `notepad.exe` để đánh lừa bộ lọc tên file.
* **Giải pháp kỹ thuật của OGK:**
  - Tác tử `AppController` quét các tiến trình đang chạy mỗi 3 giây.
  - Khi phát hiện một tiến trình mới, thay vì tin tưởng `proc.name()`, tác tử lấy đường dẫn nhị phân `proc.exe()` và tính mã băm SHA-256 của file trên đĩa:
  $$\text{Hash} = \text{SHA-256}(\text{Binary Content})$$
  - Cơ chế **Bộ nhớ đệm mtime (Cache Optimization):** Lưu trữ cặp `(mtime, sha256)`. Chỉ khi nào file bị chỉnh sửa ngày giờ thì mới tính lại mã băm, giúp mức chiếm dụng CPU duy trì ở mức **0.0%**.
  - Nếu mã băm trùng khớp với danh sách cấm: Tác tử gọi `process.terminate()` và hiển thị Balloon Notification thông báo lý do rõ ràng cho trẻ (Nguyên tắc NT4).

### 5. Tiếng nói Trẻ em & Minh bạch Hai chiều (NT3 & NT5)
* Tác tử cung cấp giao diện khay hệ thống cho trẻ:
  - Xem số phút đã dùng và số phút còn lại trong ngày.
  - Nút **"Xin thêm giờ"** (gửi yêu cầu 15 phút, 30 phút, 60 phút kèm lý do làm bài tập).
  - Nút **"Báo chặn nhầm"** (gửi tên miền hoặc ứng dụng bị chặn để phụ huynh xem xét mở khóa).
  - Lắng nghe phản hồi từ cha mẹ qua WebSocket trong thời gian thực.

---

## III. CHI TIẾT KỸ THUẬT TUẦN 4 — VERSION 0.4: BẢO MẬT F5, CHỊU LỖI M5 & NGHIỆM THU

### 1. Gia cố Bảo mật Cấp cao F5 (NIST SP 800-63B & OWASP ASVS v4)
* **Chính sách mật khẩu $\ge 10$ ký tự:** Enforce schema Pydantic kiểm tra độ dài tối thiểu 10 ký tự, kết hợp thuật toán băm Argon2id ngốn bộ nhớ chống bẻ khóa GPU.
* **Cơ chế chống Brute-Force & Khóa tài khoản:**
  - Ghi nhận `failed_login_attempts`. Khi sai liên tiếp 5 lần: Lập tức kích hoạt `locked_until = now + 15 phút`. Phản hồi HTTP 423 Locked.
  - Trong thời gian bị khóa, dù nhập đúng mật khẩu hệ thống vẫn từ chối và đếm ngược thời gian.
* **In-memory IP Rate Limiting:** Giới hạn 10 requests/phút/IP trên các endpoint nhạy cảm (`/login`, `/token`, `/pairing`).
* **Bảo vệ Cookie & Quản lý phiên:** Cookie `access_token` được gắn cờ `HttpOnly`, `SameSite=Lax`. Khi đăng xuất, token được thu hồi tức thì và đưa vào danh sách blacklist bộ nhớ.
* **Mã hóa dữ liệu tĩnh AES-256-GCM AEAD:** Tiện ích mã hóa đối xứng xác thực `server/crypto_utils.py` với Nonce 12 bytes và Auth Tag 16 bytes, tự động từ chối dữ liệu bị can thiệp (Tamper-proofing).
* **Triệt tiêu hoàn toàn lỗ hổng IDOR (Anti-IDOR Authorization):**
  - Mọi API nhận `device_id` (Phát lệnh, Cập nhật chính sách, Xem báo cáo, Duyệt yêu cầu của trẻ) đều đối soát:
  $$\text{assert } \text{device.parent\_id} == \text{current\_parent.id}$$
  - Phụ huynh A cố tình thao tác trên thiết bị của Phụ huynh B lập tức nhận mã lỗi **HTTP 403 Forbidden**.

### 2. Tuân thủ Pháp lý Nghị định 13/2023/NĐ-CP & Quyền Xóa Dữ Liệu
* **Tự động tiêu hủy dữ liệu 90 ngày (Data Retention Purge):**
  - Tác vụ ngầm chạy chu kỳ 24h quét và xóa toàn bộ các bản ghi `ActivityEvent`, `HeartbeatLog` có tuổi thọ lớn hơn 90 ngày.
* **Quyền yêu cầu xóa dữ liệu của trẻ (Right to Erasure):**
  - Endpoint `DELETE /api/v1/devices/{device_id}/data` yêu cầu nhập lại mật khẩu phụ huynh.
  - Khi xác thực thành công:
    1. Tiêu hủy toàn bộ viễn trắc hoạt động, nhịp tim và yêu cầu của con trên cơ sở dữ liệu máy chủ.
    2. Gửi lệnh qua WebSocket `purge_local_data` tới tác tử máy con để xóa sạch bộ nhớ đệm SQLite ngoại tuyến.
    3. Ghi vết kiểm toán `AuditLog` phục vụ thanh tra.

### 3. Khắc chế 7 Kỹ thuật Vượt rào Mạng (M3 Anti-Bypass Guard)
| Kỹ thuật Vượt rào của Trẻ | Mức độ rủi ro | Cơ chế Phát hiện & Khắc chế của OGK |
| :--- | :---: | :--- |
| **1. Đổi DNS card mạng sang 8.8.8.8** | Rất cao | `DNSWatchdog` chạy ngầm chu kỳ 20s, phát hiện DNS khác `127.0.0.1` lập tức gọi `netsh` hoàn nguyên về `127.0.0.1` và phát sinh cảnh báo viễn trắc. |
| **2. Bật DoH trong trình duyệt** | Cao | Phản hồi `NXDOMAIN` với Canary Domain `use-application-dns.net`, ép trình duyệt quay về DNS cổng 53. |
| **3. Dùng DoT (DNS over TLS - Cổng 853)** | Trung bình | Tên miền máy chủ DoT bị chặn ngay từ bước phân giải DNS. |
| **4. Cài phần mềm VPN / Proxy** | Rất cao | `AppController` gieo mầm và tiêu diệt ngay các tiến trình VPN phổ biến (Cloudflare WARP, ProtonVPN, Psiphon, UltraSurf) bằng đối soát kép SHA-256 + Tên file trong $\le 3$ giây. |
| **5. Truy cập trực tiếp bằng địa chỉ IP** | Trung bình | Đa số các trang web hiện đại (YouTube, Facebook, Roblox) sử dụng CDN và HTTPS chia sẻ nhiều dịch vụ trên 1 IP kèm SNI, việc gõ IP thô sẽ bị máy chủ từ chối chứng chỉ TLS. |
| **6. Khởi động Windows ở chế độ Safe Mode** | Trung bình | Safe Mode with Networking bị khống chế quyền Admin; phụ huynh đặt mật khẩu tài khoản Administrator và chỉ cấp tài khoản Standard cho trẻ. |
| **7. Kill tiến trình Agent trong Task Manager** | Rất cao | Agent chạy dưới dạng Windows Service với tài khoản `SYSTEM` (Session 0 Isolation), tài khoản Standard của trẻ không có quyền `Access Denied` khi cố tình chấm dứt tiến trình. |

### 4. Báo cáo Thực nghiệm Đo lường Hiệu năng (M4 Benchmark)
Dữ liệu đo đạc thực nghiệm từ script tự động [`scripts/benchmark_performance.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/scripts/benchmark_performance.py) qua 30 mẫu đo độc lập trên môi trường Windows 10/11 x64:

```text
========================================================================================
CHỈ SỐ ĐO LƯỜNG              | KẾT QUẢ THỰC TẾ (OGK) | TIÊU CHUẨN ĐỒ ÁN (DoD) | ĐÁNH GIÁ
========================================================================================
RAM Footprint (Chế độ nghỉ)  | 25.13 MB             | <= 26.0 MB             | [✓] ĐẠT
RAM Footprint (Khi tải cao)  | 25.13 MB             | <= 26.0 MB             | [✓] ĐẠT
CPU Footprint (Trung bình)   | 0.0%                 | < 1.0%                 | [✓] ĐẠT
Độ trễ DNS Proxy (Median p50)| 0.83 ms              | Nhanh hơn Upstream     | [✓] ĐẠT (Upstream 35.75 ms)
Độ trễ DNS Proxy (p95)       | 104.43 ms            | < 200 ms               | [✓] ĐẠT
Độ trễ Lệnh Khẩn cấp (WS)    | 5.91 ms (p50)        | < 500 ms               | [✓] ĐẠT (Nhanh gấp 84 lần)
========================================================================================
```

### 5. Kiểm chứng Khả năng Chịu lỗi & Phục hồi Mạng (M5 Fault Tolerance)
Hệ thống đã trải qua 3 kịch bản kiểm thử khắc nghiệt tại [`tests/test_fault_tolerance.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/tests/test_fault_tolerance.py):
1. **Rút cáp mạng / Mất kết nối Internet:**
   - Toàn bộ sự kiện viễn trắc và nhịp tim được đệm an toàn vào tệp SQLite cục bộ `agent_cache.db`.
   - Khi mạng kết nối trở lại: Luồng đồng bộ tự động đẩy hàng loạt (Batch push) lên máy chủ kèm khóa `idempotency_key` chống trùng lặp.
2. **Máy chủ trung tâm sập (Server Outage):**
   - Tác tử Client chuyển sang chế độ tự trị (Autonomous Mode).
   - Bộ đếm giờ tiếp tục đếm chính xác bằng `time.monotonic()`, khi hết hạn mức giờ chơi, máy con **tự động khóa màn hình ngoại tuyến ngay lập tức**, không cho phép trẻ lợi dụng lúc mất mạng để chơi quá giờ.
3. **Khởi động lại máy tính (Reboot Recovery):**
   - Số phút đã sử dụng trong ngày được ghi đều đặn vào SQLite.
   - Khi máy khởi động lại, tác tử đọc lại số phút cũ và tiếp tục cộng dồn, trẻ không thể reset giờ chơi bằng cách restart máy tính.

---

## IV. BẢNG TỔNG HỢP KIỂM THỬ TỰ ĐỘNG & NGHIỆM THU ĐẦU-CUỐI

### 1. Kết quả Toàn bộ 61 Test Cases Tự Động (100% PASSED)
```text
tests/test_app_filtering_and_events.py ...... [5 tests PASSED]
tests/test_auth.py .......................... [10 tests PASSED]
tests/test_dns_proxy.py ..................... [9 tests PASSED]
tests/test_enrollment.py .................... [6 tests PASSED]
tests/test_fault_tolerance.py ............... [3 tests PASSED]
tests/test_heartbeat.py ..................... [4 tests PASSED]
tests/test_policy.py ........................ [4 tests PASSED]
tests/test_security_f5.py ................... [15 tests PASSED]
tests/test_time_tracker.py .................. [4 tests PASSED]
tests/test_websocket_command.py ............. [1 test PASSED]
======================= 61 passed in 9.83s =======================
```

### 2. Nghiệm thu Thực nghiệm Trực tiếp (8 Bước VERIFY_WEEK4)
Toàn bộ 8 bước kiểm chứng thực tế tại [`scripts/verify_e2e_scenarios.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/scripts/verify_e2e_scenarios.py) đều đạt kết quả xuất sắc:
1. Mật khẩu $\ge 10$ ký tự chuẩn NIST SP 800-63B.
2. Khóa tài khoản 15 phút sau 5 lần đăng nhập sai.
3. Triệt tiêu 100% lỗ hổng IDOR trên toàn bộ APIs.
4. Xóa sạch dữ liệu của con theo đúng Nghị định 13 khi nhập đúng mật khẩu.
5. Tự động phục hồi DNS card mạng về `127.0.0.1` khi bị đổi sang `8.8.8.8` trong $\le 20$s.
6. Cưỡng bức chấm dứt các tiến trình VPN (WARP, Proton, Psiphon, UltraSurf) trong vòng 3s.
7. Chịu lỗi mất kết nối mạng, đệm ngoại tuyến SQLite và đồng bộ bù không trùng lặp.
8. Khóa ngoại tuyến tức thì khi hết giờ chơi dù không có máy chủ.

---

## V. KẾT LUẬN & ĐÁNH GIÁ ĐỒ ÁN TỐT NGHIỆP

Đồ án **Open Guardian Kids (OGK)** đã hoàn thành trọn vẹn 100% mục tiêu nghiên cứu và hiện thực hóa của cả 4 tuần:
* **Tính Khoa học & Chuẩn mực Kỹ thuật:** Áp dụng kiến trúc Socket mạng phân tán, giải quyết bài toán đồng hồ phần cứng và phân giải tên miền.
* **Tính Pháp lý & Nhân văn:** Tiên phong tuân thủ Nghị định 13/2023/NĐ-CP và Luật Trẻ Em 2016, loại bỏ hoàn toàn các cơ chế gián điệp Stalkerware.
* **Độ Tin Cậy Cao:** 61/61 kiểm thử tự động đạt 100% Pass, bộ đo lường M4 và tài liệu kỹ thuật M1 - M6 đầy đủ.

Đồ án đã sẵn sàng tuyệt đối để báo cáo và bảo vệ trước Hội đồng Chấm Đồ Án Tốt Nghiệp!
