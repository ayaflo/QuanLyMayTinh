# KẾ HOẠCH CÁC BƯỚC SIÊU NHỎ — TUẦN 4 (VERSION 0.4 — PHIÊN BẢN CUỐI CÙNG)
## ĐỀ TÀI: OPEN GUARDIAN KIDS (OGK)
> **Mục tiêu phiên bản 4 (Final Release):** Gia cố bảo mật toàn diện **F5 (Security Hardening & ASVS Level 1)**; Khắc chế và phân tích **7 kỹ thuật vượt rào mạng M3 (Anti-Bypass Guard)**; Đo lường hiệu năng thực nghiệm **M4 (Benchmark CPU/RAM/DNS/WebSocket latency)**; Kiểm chứng khả năng chịu lỗi **M5 (Fault Tolerance & Offline recovery)**; Tuân thủ pháp lý **Nghị định 13/2023 & Luật Trẻ em 2016** (Xóa dữ liệu 90 ngày, Quyền yêu cầu xóa dữ liệu); Đạt chuẩn **100% test tự động** và **Đóng gói trọn bộ hồ sơ tốt nghiệp**.  
> **Nguyên tắc Karpathy:** Tối giản (Simplicity First), Phẫu thuật chính xác (Surgical Changes), Cô lập ranh giới (Think Before Coding), Không vẽ tính năng ngoài phạm vi (No Speculative Code / YAGNI).

---

## I. TỔNG HỢP RÀNG BUỘC KỸ THUẬT & QUẢN TRỊ ĐẠO ĐỨC (KARPATHY GOVERNANCE)

1. **Ranh giới công nghệ tối giản (Simplicity First)**:
   - Giữ vững kiến trúc phẳng: Không bổ sung framework nặng, không dựng Docker/Redis; sử dụng cấu trúc sẵn có của **FastAPI + SQLite WAL mode + Python tiêu chuẩn (`pywin32`, `psutil`, `dnslib`)**.
   - Tuyệt đối không cài đặt cơ chế kiểu rootkit/malware để chống gỡ cài đặt; trung thực phân tích ranh giới kỹ thuật trong báo cáo phản biện.
2. **Tuân thủ Tiêu chuẩn Bảo mật & Pháp lý**:
   - **NIST SP 800-63B & OWASP ASVS v4 (Level 1):** Mật khẩu băm Argon2id >= 10 ký tự, khóa tài khoản 15 phút sau 5 lần sai, cookie phiên `HttpOnly, SameSite=Lax`, thu hồi phiên khi đăng xuất, phân quyền chống IDOR ở tầng truy vấn CSDL.
   - **Nghị định 13/2023/NĐ-CP (Điều 20) & Luật Trẻ em 2016:** Tự động xóa dữ liệu hoạt động cũ hơn 90 ngày; cung cấp chức năng "Xóa toàn bộ dữ liệu của con tôi" xóa đồng bộ cả Server và Agent.
3. **Thực nghiệm đo đạc khoa học (Goal-Driven Execution)**:
   - Thu thập số liệu đo lường thực tế (tối thiểu 30 mẫu đo) về CPU, RAM, độ trễ phân giải DNS p50/p95 và độ trễ đẩy lệnh WebSocket để đưa vào phụ lục kỹ thuật M4.

---

## II. BẢNG MA TRẬN MICRO-TASKS TUẦN 4 (VERSION 0.4)

| STT | Mã Task | Thao tác duy nhất | Đường dẫn tệp mục tiêu | Tiêu chí hoàn thành (DoD) |
| :---: | :---: | :--- | :--- | :--- |
| **GIAI ĐOẠN 1: BẢO MẬT NÂNG CAO F5 — XÁC THỰC, CHỐNG BRUTE-FORCE & QUẢN LÝ PHIÊN (ASVS LEVEL 1)** | | | | |
| 1 | `T4_01` | Mở rộng model `Parent` thêm trường kiểm soát khóa tài khoản trong `server/models.py` | [`server/models.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/models.py) | Bổ sung `failed_login_attempts` (mặc định 0) và `locked_until` (DateTime, nullable) vào bảng `parents`. |
| 2 | `T4_02` | Gia cố quy tắc mật khẩu tối thiểu 10 ký tự trong `server/schemas.py` | [`server/schemas.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/schemas.py) | Ràng buộc `ParentCreate` và `ParentLogin` yêu cầu mật khẩu tối thiểu 10 ký tự theo NIST SP 800-63B. |
| 3 | `T4_03` | Cập nhật logic đăng nhập chống Brute-Force (Lockout 15 phút) trong `server/routes/auth.py` | [`server/routes/auth.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/auth.py) | Nếu đăng nhập sai 5 lần liên tiếp: Khóa tài khoản 15 phút (`locked_until`); reset số lần thử về 0 khi đăng nhập thành công. |
| 4 | `T4_04` | Đồng bộ logic khóa tài khoản cho giao diện HTML Login trong `server/routes/dashboard.py` | [`server/routes/dashboard.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/dashboard.py) | Form đăng nhập web hiển thị thông báo rõ ràng thời gian còn lại khi tài khoản bị tạm khóa do nhập sai nhiều lần. |
| 5 | `T4_05` | Hiện thực cơ chế Rate Limiting theo địa chỉ IP cho API xác thực trong `server/security.py` | [`server/security.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/security.py) | Giới hạn tối đa 10 yêu cầu đăng nhập/phút trên mỗi địa chỉ IP để chống tấn công phân tán từ chối dịch vụ. |
| 6 | `T4_06` | Cấu hình cờ Cookie phiên an toàn (`HttpOnly, SameSite=Lax`) & Cơ chế Đăng xuất hủy phiên | [`server/routes/dashboard.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/dashboard.py) | Đảm bảo cookie phiên không thể bị đọc qua Javascript (chống XSS) và xóa phiên sạch sẽ khi phụ huynh bấm Đăng xuất. |
| **GIAI ĐOẠN 2: BẢO MẬT NÂNG CAO F5 — MÃ HÓA CẤU HÌNH & KIỂM SOÁT PHÂN QUYỀN CHỐNG IDOR** | | | | |
| 7 | `T4_07` | Tạo module mã hóa đối xứng AES-256-GCM `server/crypto_utils.py` | [`server/crypto_utils.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/crypto_utils.py) | Cung cấp hàm `encrypt_data()` và `decrypt_data()` bằng AES-256-GCM với Nonce 12-byte và Tag xác thực 16-byte phục vụ mã hóa lúc nghỉ (Encryption at Rest). |
| 8 | `T4_08` | Gia cố kiểm tra quyền sở hữu thiết bị chống IDOR trong `server/routes/commands.py` | [`server/routes/commands.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/commands.py) | Xác thực `device.parent_id == current_parent.id` trước khi cho phép gửi lệnh khẩn cấp (Khóa máy / Thêm giờ). |
| 9 | `T4_09` | Gia cố kiểm tra quyền sở hữu thiết bị chống IDOR trong `server/routes/policy.py` | [`server/routes/policy.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/policy.py) | Đảm bảo phụ huynh chỉ có thể xem và cập nhật chính sách hạn mức thời gian của thiết bị thuộc quyền quản lý của mình. |
| 10 | `T4_10` | Gia cố kiểm tra quyền sở hữu chống IDOR trong `server/routes/reports.py` và `requests.py` | [`server/routes/reports.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/reports.py) | Ngăn chặn việc truy cập trái phép xem báo cáo sử dụng hoặc duyệt yêu cầu của con thuộc tài khoản phụ huynh khác. |
| **GIAI ĐOẠN 3: PHÁP LÝ & ĐẠO ĐỨC — LƯU TRỮ 90 NGÀY & QUYỀN XÓA TOÀN BỘ DỮ LIỆU (NGHỊ ĐỊNH 13/2023)** | | | | |
| 11 | `T4_11` | Hiện thực dịch vụ dọn dẹp dữ liệu quá hạn 90 ngày `server/services/retention_service.py` | [`server/services/retention_service.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/services/retention_service.py) | Hàm `purge_expired_activity_data(db, days=90)` tự động xóa sạch các bản ghi `activity_events` và `heartbeat_logs` cũ hơn 90 ngày theo quy định pháp lý. |
| 12 | `T4_12` | Tích hợp tác vụ tự động dọn dẹp 90 ngày vào startup lifespan trong `server/main.py` | [`server/main.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/main.py) | Khởi động chu kỳ kiểm tra và dọn dẹp dữ liệu cũ mỗi 24 giờ một cách tự động khi máy chủ chạy nền. |
| 13 | `T4_13` | Hiện thực nghiệp vụ "Xóa toàn bộ dữ liệu của con tôi" (Right to Erasure) trong `server/services/retention_service.py` | [`server/services/retention_service.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/services/retention_service.py) | Xóa toàn diện dữ liệu thiết bị: Xóa sự kiện, nhịp tim, lịch sử yêu cầu, cấu hình app/policy; đồng thời phát lệnh xóa bộ đệm tới Agent. |
| 14 | `T4_14` | Tạo endpoint `DELETE /api/v1/devices/{device_id}/data` trong `server/routes/retention.py` | [`server/routes/retention.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/retention.py) | Yêu cầu xác thực mật khẩu phụ huynh trước khi thực hiện xóa vĩnh viễn dữ liệu thiết bị. |
| 15 | `T4_15` | Thêm chức năng xóa trắng bộ đệm cục bộ `purge_local_data()` trong `agent/storage.py` | [`agent/storage.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/storage.py) | Xóa sạch bảng `pending_events`, `daily_usage`, `dns_rules_cache`, `app_rules_cache` khi nhận được lệnh xóa từ phụ huynh. |
| 16 | `T4_16` | Xây dựng giao diện nút "🗑️ Xóa Toàn Bộ Dữ Liệu Con" trên `dashboard/templates/devices.html` | [`dashboard/templates/devices.html`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/dashboard/templates/devices.html) | Hộp thoại xác nhận đạo đức: Cảnh báo hành động không thể hoàn tác, yêu cầu nhập mật khẩu phụ huynh để phê duyệt xóa. |
| **GIAI ĐOẠN 4: ĐỐI PHÓ KỸ THUẬT VƯỢT RÀO M3 TRÊN CLIENT AGENT (ANTI-BYPASS GUARD)** | | | | |
| 17 | `T4_17` | Xây dựng watchdog kiểm tra DNS Adapter `agent/dns_watchdog.py` | [`agent/dns_watchdog.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/dns_watchdog.py) | Quét định kỳ mỗi 20s: Kiểm tra xem card mạng có bị người dùng đổi DNS thủ công khỏi `127.0.0.1` hay không. |
| 18 | `T4_18` | Hiện thực cơ chế tự phục hồi DNS và phát cảnh báo can thiệp trong `agent/dns_watchdog.py` | [`agent/dns_watchdog.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/dns_watchdog.py) | Nếu phát hiện DNS bị đổi: Tự động gọi `set_dns_to_localhost()` để phục hồi và kích hoạt sự kiện cảnh báo `tamper_attempt` gửi về máy chủ. |
| 19 | `T4_19` | Bổ sung danh mục nhận diện các tiến trình VPN phổ biến vào `server/seed_domains.py` | [`server/seed_domains.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/seed_domains.py) | Nạp sẵn danh sách quy tắc kiểm soát ứng dụng VPN thông dụng (Cloudflare WARP, ProtonVPN, Psiphon, UltraSurf) để AppController tự động nhận diện. |
| 20 | `T4_20` | Tích hợp `dns_watchdog` vào quy trình khởi chạy tác tử trong `agent/main.py` | [`agent/main.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/main.py) | Khởi chạy luồng giám sát card mạng song song với DNS Proxy, App Controller và Heartbeat Client; dọn dẹp khi tắt. |
| **GIAI ĐOẠN 5: ĐO LƯỜNG HIỆU NĂNG THỰC NGHIỆM M4 & KHẢ NĂNG CHỊU LỖI M5 (BENCHMARK & FAULT TOLERANCE)** | | | | |
| 21 | `T4_21` | Xây dựng script đo đạc hiệu năng tự động `scripts/benchmark_performance.py` | [`scripts/benchmark_performance.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/scripts/benchmark_performance.py) | Tự động đo: Mức chiếm dụng CPU & RAM của Agent khi nghỉ vs khi tải; Độ trễ phân giải DNS p50, p95 qua 50 truy vấn so với 1.1.1.3; Độ trễ WebSocket (< 500ms). |
| 22 | `T4_22` | Tạo tệp kiểm thử tự động khả năng chịu lỗi `tests/test_fault_tolerance.py` | [`tests/test_fault_tolerance.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/tests/test_fault_tolerance.py) | Kiểm chứng 3 kịch bản M5: 1) Mất mạng (đệm vào SQLite); 2) Máy chủ tạm ngừng (Agent vẫn đếm giờ và khóa theo chính sách cục bộ); 3) Khởi động lại máy (khôi phục số phút đã dùng trong ngày). |
| **GIAI ĐOẠN 6: SOẠN THẢO BÁO CÁO KỸ THUẬT MẠNG CHUYÊN SÂU (NETWORK TECHNICAL REPORTS M3, M4, M5)** | | | | |
| 23 | `T4_23` | Soạn thảo Phụ lục Kỹ thuật Mạng mục M3 `docs/M3_PHAN_TICH_DOI_PHO_BYPASS.md` | [`docs/M3_PHAN_TICH_DOI_PHO_BYPASS.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M3_PHAN_TICH_DOI_PHO_BYPASS.md) | Luận chứng và phân tích thực nghiệm 7 kỹ thuật vượt rào mạng: Đổi DNS card mạng, DoH, DoT, VPN, Direct IP access, Safe Mode, Kill tiến trình; cơ chế phát hiện & khắc chế cụ thể của OGK. |
| 24 | `T4_24` | Soạn thảo Phụ lục Kỹ thuật Mạng mục M4 `docs/M4_DO_LUONG_HIEU_NANG.md` | [`docs/M4_DO_LUONG_HIEU_NANG.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M4_DO_LUONG_HIEU_NANG.md) | Bảng dữ liệu thực nghiệm >= 30 mẫu đo CPU (< 1%), RAM (< 25MB), biểu đồ độ trễ phân giải DNS p50/p95, độ trễ phát lệnh WebSocket < 500ms. |
| 25 | `T4_25` | Soạn thảo Phụ lục Kỹ thuật Mạng mục M5 `docs/M5_KHA_NANG_CHIU_LOI.md` | [`docs/M5_KHA_NANG_CHIU_LOI.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M5_KHA_NANG_CHIU_LOI.md) | Phân tích cơ chế chịu lỗi, tính toàn vẹn bộ đệm ngoại tuyến SQLite, cơ chế chống mất mát dữ liệu và phục hồi khi kết nối mạng được tái lập. |
| **GIAI ĐOẠN 7: SOẠN THẢO HỒ SƠ ĐẠO ĐỨC, PHÁP LÝ & MÔ HÌNH ĐE DỌA (ETHICS, COMPLIANCE & THREAT MODEL)** | | | | |
| 26 | `T4_26` | Hoàn thiện tài liệu Pháp lý & Quyền riêng tư `docs/PRIVACY.md` | [`docs/PRIVACY.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/PRIVACY.md) | Bảng giải trình 4 trường dữ liệu tối thiểu theo Nghị định 13/2023 & Bản cam kết quyền riêng tư bằng ngôn ngữ thân thiện dành riêng cho trẻ em (NT1, NT2). |
| 27 | `T4_27` | Soạn thảo Mô hình đe dọa STRIDE & ASVS v4 `docs/THREATMODEL.md` | [`docs/THREATMODEL.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/THREATMODEL.md) | Phân tích 8 mối đe dọa an ninh mạng theo mô hình STRIDE + Bảng kiểm soát đánh giá an toàn OWASP ASVS v4 Level 1 (>= 20 tiêu chí). |
| 28 | `T4_28` | Soạn thảo Bản minh bạch ứng dụng AI `docs/AI_USAGE.md` | [`docs/AI_USAGE.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/AI_USAGE.md) | Báo cáo minh bạch các thành phần có sự hỗ trợ của AI, nguyên tắc kiểm chứng chéo và trách nhiệm học thuật theo chuẩn mực đồ án tốt nghiệp. |
| **GIAI ĐOẠN 8: BỘ KIỂM THỬ TỰ ĐỘNG BẢO MẬT, TÀI LIỆU CÀI ĐẶT & KỊCH BẢN NGHIỆM THU ĐẦU-CUỐI** | | | | |
| 29 | `T4_29` | Tạo bộ kiểm thử tự động bảo mật `tests/test_security_f5.py` | [`tests/test_security_f5.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/tests/test_security_f5.py) | Kiểm thử: Khóa tài khoản sau 5 lần sai; Quy tắc mật khẩu >= 10 ký tự; Phân quyền chống IDOR; Mã hóa AES-256-GCM; Tự động xóa dữ liệu 90 ngày; Quyền xóa dữ liệu (Right to Erasure). |
| 30 | `T4_30` | Cập nhật hướng dẫn cài đặt & vận hành sạch trong `README.md` | [`README.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/README.md) | Hướng dẫn cài đặt sạch từ đầu và chạy thử toàn bộ hệ thống (Server + Dashboard + Agent) trong vòng 15 phút trên máy Windows sạch. |
| 31 | `T4_31` | Soạn thảo Kịch bản nghiệm thu đầu-cuối Version 4 `docs/VERIFY_WEEK4.md` | [`docs/VERIFY_WEEK4.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/VERIFY_WEEK4.md) | Hướng dẫn kiểm chứng 5 tiêu chí DoD của Version 4: Đăng nhập khóa 15p sau 5 lần sai; Anti-IDOR; Nút xóa dữ liệu con; Kết quả benchmark M4; 100% tests pass. |

---

## III. TIÊU CHÍ NGHIỆM THU ĐẦU-CUỐI TUẦN 4 (DEFINITION OF DONE - DoD WEEK 4)

1. **DoD 1 (Bảo mật nâng cao F5 & Quản lý phiên)**:
   - Thử nghiệm đăng nhập sai 5 lần: Tài khoản lập tức bị khóa 15 phút, phản hồi HTTP 423 Locked hoặc thông báo thời gian khóa còn lại.
   - Thử nghiệm IDOR: Cố ý dùng tài khoản phụ huynh A truy cập tài nguyên thiết bị của phụ huynh B -> Lập tức bị từ chối HTTP 403/404.
2. **DoD 2 (Tuân thủ Pháp lý & Quyền xóa dữ liệu)**:
   - Thử nghiệm kích hoạt API "Xóa toàn bộ dữ liệu của con tôi": Toàn bộ lịch sử sự kiện, nhịp tim và bộ đệm tại Server lẫn Agent bị xóa sạch sẽ; dữ liệu cũ hơn 90 ngày tự động bị dọn dẹp.
3. **DoD 3 (Khắc chế vượt rào M3 & Watchdog DNS)**:
   - Thử nghiệm đổi DNS card mạng sang `8.8.8.8`: Watchdog của Agent phát hiện trong <= 30 giây, tự động thiết lập lại về `127.0.0.1` và phát sinh cảnh báo can thiệp.
4. **DoD 4 (Số liệu đo lường hiệu năng M4 & Chịu lỗi M5)**:
   - Chạy script benchmark tự động: Thu thập đầy đủ bảng số liệu >= 30 mẫu đo CPU (< 1%), RAM (< 25MB), độ trễ DNS p50/p95, độ trễ WebSocket < 500ms đưa vào báo cáo `docs/M4_DO_LUONG_HIEU_NANG.md`.
   - Các kịch bản chịu lỗi rớt mạng và phục hồi ngoại tuyến đạt 100% yêu cầu.
5. **DoD 5 (Hồ sơ hoàn chỉnh & 100% Test Suite)**:
   - Toàn bộ test suite đạt **100% PASSED** (bao gồm toàn bộ tests từ v0.1 đến v0.4).
   - Đầy đủ toàn bộ 6 phụ lục Mạng (M1 đến M6) và các báo cáo `PRIVACY.md`, `THREATMODEL.md`, `AI_USAGE.md`, `README.md`.
