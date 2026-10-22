# KẾ HOẠCH CÁC BƯỚC SIÊU NHỎ — TUẦN 3 (VERSION 0.3)
## ĐỀ TÀI: OPEN GUARDIAN KIDS (OGK)
> **Mục tiêu phiên bản 3:** Hiện thực trọn vẹn **Bộ lọc Website bằng DNS Proxy cục bộ 127.0.0.1:53 & Cưỡng chế SafeSearch (F2)**; **Kiểm soát ứng dụng theo mã băm SHA-256 (F2)**; **Ghi nhận sự kiện tối thiểu F3 với bộ đệm ngoại tuyến (F3, NT2)**; **Cơ chế trẻ có tiếng nói — Nút xin thêm giờ & Báo chặn nhầm (NT3)**; **Màn hình minh bạch hai chiều cho trẻ & phụ huynh (NT5)**; cùng **Phụ lục Kỹ thuật Mạng M1 & M2**.  
> **Nguyên tắc Karpathy:** Tối giản (Simplicity First), Phẫu thuật chính xác (Surgical Changes), Cô lập ranh giới (Think Before Coding), Không vẽ tính năng ngoài phạm vi (No Speculative Code).

---

## I. TỔNG HỢP RÀNG BUỘC KỸ THUẬT & DANH MỤC ĐẠO ĐỨC (KARPATHY GOVERNANCE)

1. **Ranh giới công nghệ tối giản**:
   - Sử dụng thư viện chuẩn `dnslib` (Python) để xử lý UDP Socket cổng 53, không dựng BIND hay Unbound cồng kềnh.
   - Sử dụng `psutil` kết hợp thư viện chuẩn `hashlib.sha256` để kiểm soát tiến trình.
   - Giao tiếp nội bộ giữa DNS Proxy, App Controller và Server tuân thủ schema F3 tối thiểu.
2. **Tuân thủ 6 Nguyên tắc Đạo đức (NT1 - NT6) & Nghị định 13/2023**:
   - **NT2 (Tối thiểu dữ liệu):** Chỉ lưu FQDN/domain và tên app. Tuyệt đối KHÔNG lưu URL đầy đủ, KHÔNG tiêu đề cửa sổ, KHÔNG keylogger, KHÔNG chụp màn hình.
   - **NT3 (Trẻ có tiếng nói):** Nút "Xin thêm giờ" và "Báo chặn nhầm" kết nối 2 chiều tới phụ huynh.
   - **NT4 (Mọi hành động phải giải thích được):** Khi chặn web/app, hiển thị rõ lý do và ai đặt luật, không giả lập lỗi mạng.
   - **NT5 (Minh bạch hai chiều):** Màn hình "Hôm nay em đã dùng gì" cho trẻ xem cùng dữ liệu với phụ huynh.
   - **NT6 (An toàn có ưu tiên tuyệt đối):** Danh sách trắng vĩnh viễn không bao giờ chặn: Cổng thông tin trường học và Tổng đài Quốc gia Bảo vệ Trẻ em 111 (`tongdai111.vn`).
3. **Quy tắc an toàn dữ liệu kiểm thử**:
   - Bộ dữ liệu 200 tên miền kiểm thử dùng địa chỉ công khai, an toàn, tên miền thử nghiệm trung tính. Tuyệt đối không dùng tên miền có nội dung người lớn thật.

---

## II. BẢNG MA TRẬN 50 MICRO-TASKS TUẦN 3

| STT | Mã Task | Thao tác duy nhất | Đường dẫn tệp mục tiêu | Tiêu chí hoàn thành (DoD) |
| :---: | :---: | :--- | :--- | :--- |
| **GIAI ĐOẠN 1: MỞ RỘNG CƠ SỞ DỮ LIỆU & LƯỢC ĐỒ PYDANTIC (DATABASE & SCHEMAS)** | | | | |
| 1 | `T3_01` | Tạo model `DomainRule` trong `server/models.py` | [`server/models.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/models.py) | Bảng `domain_rules` chứa: `id`, `category` (Giáo dục, Giải trí, Mạng xã hội, Game, Không phù hợp, DoH), `domain`, `action` (`allow`/`block`), `is_permanent_whitelist` (NT6), `created_at`. |
| 2 | `T3_02` | Tạo model `AppRule` trong `server/models.py` | [`server/models.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/models.py) | Bảng `app_rules` chứa: `id`, `device_id`, `app_name`, `sha256_hash`, `action` (`allow`/`block`), `description`, `created_at`. |
| 3 | `T3_03` | Tạo model `ActivityEvent` trong `server/models.py` | [`server/models.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/models.py) | Bảng `activity_events` chuẩn F3: `id`, `idempotency_key` (UNIQUE), `ts`, `device_id`, `child_id`, `type`, `subject`, `duration_sec`, `policy_id`. |
| 4 | `T3_04` | Tạo model `AccessRequest` trong `server/models.py` | [`server/models.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/models.py) | Bảng `access_requests` (NT3): `id`, `device_id`, `child_id`, `request_type` (`add_time`, `unblock_domain`, `unblock_app`), `target`, `reason`, `status`, `parent_response`, `created_at`. |
| 5 | `T3_05` | Khai báo schemas Pydantic cho Domain & App Rules trong `server/schemas.py` | [`server/schemas.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/schemas.py) | Khai báo các class: `DomainRuleCreate`, `DomainRuleResponse`, `AppRuleCreate`, `AppRuleResponse`, `DomainCategorySummary`. |
| 6 | `T3_06` | Khai báo schemas Pydantic cho Event Ingestion trong `server/schemas.py` | [`server/schemas.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/schemas.py) | Khai báo `EventItemSchema` (chỉ đúng 7 trường F3, validate type), `BatchEventIngestRequest`, `BatchEventIngestResponse`. |
| 7 | `T3_07` | Khai báo schemas Pydantic cho Access Request & Báo cáo trong `server/schemas.py` | [`server/schemas.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/schemas.py) | Khai báo `AccessRequestCreate`, `AccessRequestReview`, `AccessRequestResponse`, `ReportSummaryResponse`. |
| **GIAI ĐOẠN 2: BỘ DỮ LIỆU 200 TÊN MIỀN 6 NHÓM & CÁC DỊCH VỤ LÕI SERVER (CORE SERVICES)** | | | | |
| 8 | `T3_08` | Tạo tệp nạp dữ liệu phân loại 200 tên miền mẫu `server/seed_domains.py` | [`server/seed_domains.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/seed_domains.py) | Chèn 200 tên miền phân loại 6 nhóm: Giáo dục (>=20), Giải trí (>=10), Mạng xã hội (>=8), Game (>=7), Không phù hợp an toàn (>=10), DoH (>=5); bảo vệ Whitelist NT6. |
| 9 | `T3_09` | Tạo dịch vụ lọc quy tắc `server/services/filtering_service.py` | [`server/services/filtering_service.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/services/filtering_service.py) | Các hàm `get_active_domain_rules()`, `get_active_app_rules()`, `create_custom_rule()`, `delete_rule()`. |
| 10 | `T3_10` | Tạo dịch vụ tiếp nhận sự kiện theo lô `server/services/event_service.py` | [`server/services/event_service.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/services/event_service.py) | Hàm `ingest_batch_events()` kiểm tra `idempotency_key` chống trùng lặp, xử lý đệm sự kiện đẩy lên từ client khi có mạng. |
| 11 | `T3_11` | Tạo dịch vụ tổng hợp báo cáo `server/services/report_service.py` | [`server/services/report_service.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/services/report_service.py) | Hàm `generate_usage_summary()`, `get_top_apps()`, `get_top_domains()`, `get_blocked_counts()`, `get_timeline()`. |
| 12 | `T3_12` | Tạo dịch vụ quản lý yêu cầu trẻ `server/services/request_service.py` | [`server/services/request_service.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/services/request_service.py) | Hàm `create_child_request()`, `review_request()`; nếu phê duyệt cộng giờ thì kích hoạt `command_service.dispatch_command('add_time')` qua WebSocket (< 5s). |
| **GIAI ĐOẠN 3: ĐỊNH TUYẾN API SỰ KIỆN, BÁO CÁO & YÊU CẦU TRẺ (FASTAPI ROUTES)** | | | | |
| 13 | `T3_13` | Tạo `server/routes/filtering.py` và endpoint `GET /api/v1/filtering/rules` | [`server/routes/filtering.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/filtering.py) | Cung cấp danh sách tên miền cần chặn kèm wildcard và danh sách SHA-256 ứng dụng cho Agent tải về cache. |
| 14 | `T3_14` | Viết endpoints thêm/xóa luật trong `server/routes/filtering.py` | [`server/routes/filtering.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/filtering.py) | `POST /api/v1/filtering/domain-rules` và `POST /api/v1/filtering/app-rules` cho phụ huynh cập nhật từ Dashboard. |
| 15 | `T3_15` | Tạo `server/routes/events.py` và endpoint `POST /api/v1/events/batch` | [`server/routes/events.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/events.py) | Tiếp nhận mảng sự kiện tối thiểu F3 từ Agent, xác thực thiết bị và ghi nhận vào cơ sở dữ liệu. |
| 16 | `T3_16` | Tạo `server/routes/reports.py` và endpoint `GET /api/v1/reports/summary` | [`server/routes/reports.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/reports.py) | Trả về tổng hợp thời lượng sử dụng, Top 10 ứng dụng, Top 10 tên miền, số lượt chặn phục vụ Dashboard và Child View. |
| 17 | `T3_17` | Tạo `server/routes/requests.py` và endpoint `POST /api/v1/requests` | [`server/routes/requests.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/requests.py) | Tiếp nhận yêu cầu "Xin thêm giờ" hoặc "Báo chặn nhầm" từ Agent gửi lên (**NT3**). |
| 18 | `T3_18` | Viết endpoints `GET /api/v1/requests` và `PUT /api/v1/requests/{id}/review` | [`server/routes/requests.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/requests.py) | Cho phép phụ huynh xem danh sách yêu cầu đang chờ và bấm Duyệt / Từ chối kèm phản hồi. |
| 19 | `T3_19` | Đăng ký các router mới (`filtering`, `events`, `reports`, `requests`) vào `server/main.py` | [`server/main.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/main.py) | Tích hợp đầy đủ các tuyến dịch vụ lọc mạng, sự kiện và báo cáo vào ứng dụng FastAPI. |
| **GIAI ĐOẠN 4: BẢNG ĐIỀU KHIỂN BÁO CÁO, QUẢN LÝ LỌC & DUYỆT YÊU CẦU (DASHBOARD WEB UI)** | | | | |
| 20 | `T3_20` | Tích hợp thư viện Chart.js gọn nhẹ vào `dashboard/templates/base.html` | [`dashboard/templates/base.html`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/dashboard/templates/base.html) | Nhúng Chart.js (CDN hoặc file local) phục vụ trực quan hóa biểu đồ sử dụng máy tính. |
| 21 | `T3_21` | Xây dựng khu vực Biểu đồ Báo cáo sử dụng (F3) trong `dashboard/templates/devices.html` | [`dashboard/templates/devices.html`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/dashboard/templates/devices.html) | Biểu đồ cột thời lượng theo ngày/tuần, biểu đồ tròn Top 10 ứng dụng và Top 10 tên miền truy cập. |
| 22 | `T3_22` | Xây dựng khu vực Quản lý Danh mục 200 tên miền (F2) trong `dashboard/templates/devices.html` | [`dashboard/templates/devices.html`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/dashboard/templates/devices.html) | Bảng phân loại 6 nhóm với số lượng mục, công tắc Cho phép/Chặn nhanh, và form thêm tên miền tùy chỉnh. |
| 23 | `T3_23` | Xây dựng khu vực Quản lý Ứng dụng theo SHA-256 trong `dashboard/templates/devices.html` | [`dashboard/templates/devices.html`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/dashboard/templates/devices.html) | Bảng danh sách ứng dụng, mã hash SHA-256, trạng thái Cho phép/Chặn và lý do quy định. |
| 24 | `T3_24` | Xây dựng Hộp thư Yêu cầu của Trẻ (NT3) trong `dashboard/templates/devices.html` | [`dashboard/templates/devices.html`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/dashboard/templates/devices.html) | Thẻ hiển thị các yêu cầu xin thêm giờ / khiếu nại chặn nhầm với 2 nút "Phê duyệt" và "Từ chối". |
| 25 | `T3_25` | Cập nhật `server/routes/dashboard.py` nạp báo cáo, rules và requests cho UI | [`server/routes/dashboard.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/routes/dashboard.py) | Truyền dữ liệu `reports_summary`, `domain_rules`, `app_rules`, `pending_requests` vào template render. |
| 26 | `T3_26` | Cập nhật `dashboard/static/style.css` định kiểu biểu đồ và bảng lọc | [`dashboard/static/style.css`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/dashboard/static/style.css) | Tối ưu hiển thị responsive trên máy tính và mobile; badge trạng thái duyệt, màu sắc cảnh báo trực quan. |
| **GIAI ĐOẠN 5: TÁC TỬ CLIENT — BỘ LỌC DNS PROXY & CƯỠNG CHẾ SAFESEARCH (AGENT DNS SINKHOLE)** | | | | |
| 27 | `T3_27` | Bổ sung thư viện `dnslib` vào `agent/requirements.txt` | [`agent/requirements.txt`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/requirements.txt) | Thêm `dnslib` vào danh sách phụ thuộc nhẹ của Agent. |
| 28 | `T3_28` | Mở rộng `agent/storage.py` hỗ trợ bảng `dns_rules_cache` và `app_rules_cache` | [`agent/storage.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/storage.py) | Lưu bộ quy tắc lọc DNS và SHA-256 ứng dụng vào SQLite cục bộ để chạy mượt mà ngay cả khi mất mạng. |
| 29 | `T3_29` | Khởi tạo module máy chủ DNS Proxy `agent/dns_proxy.py` | [`agent/dns_proxy.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/dns_proxy.py) | Tạo lớp `DNSProxyServer` lắng nghe UDP Socket trên `127.0.0.1:53` bằng `dnslib`. |
| 30 | `T3_30` | Viết hàm khớp tên miền & wildcard `match_domain_rule()` trong `agent/dns_proxy.py` | [`agent/dns_proxy.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/dns_proxy.py) | Xử lý so khớp chính xác tên miền và tự động chặn mọi subdomain (ví dụ chặn `example.com` thì chặn cả `sub.example.com`). |
| 31 | `T3_31` | Viết cơ chế DNS Sinkholing trong `agent/dns_proxy.py` | [`agent/dns_proxy.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/dns_proxy.py) | Trả về `0.0.0.0` (hoặc `127.0.0.1`) cho các tên miền thuộc blocklist; tạo sự kiện `blocked_domain`. |
| 32 | `T3_32` | Viết hàm cưỡng chế SafeSearch bằng DNS Rewrite trong `agent/dns_proxy.py` | [`agent/dns_proxy.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/dns_proxy.py) | Ánh xạ Google sang `forcesafesearch.google.com` (216.239.38.120), Bing sang `strict.bing.com` (204.79.197.220), YouTube sang `restrict.youtube.com`. |
| 33 | `T3_33` | Viết cơ chế vô hiệu hóa DoH trình duyệt qua Canary Domain trong `agent/dns_proxy.py` | [`agent/dns_proxy.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/dns_proxy.py) | Trả về `NXDOMAIN` cho tên miền canary `use-application-dns.net` để tắt DoH tự động của Firefox/Chrome. |
| 34 | `T3_34` | Viết hàm chuyển tiếp upstream DNS `forward_upstream()` trong `agent/dns_proxy.py` | [`agent/dns_proxy.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/dns_proxy.py) | Chuyển tiếp UDP query lên Upstream an toàn (1.1.1.3 hoặc 8.8.8.8) với timeout ngắn (2s) và trả kết quả về cho client. |
| 35 | `T3_35` | Áp dụng Danh sách Trắng vĩnh viễn (NT6) trong `agent/dns_proxy.py` | [`agent/dns_proxy.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/dns_proxy.py) | Luôn chuyển tiếp, không bao giờ chặn cổng thông tin trường học và Tổng đài 111 (`tongdai111.vn`). |
| 36 | `T3_36` | Tạo helper cấu hình card mạng Windows `agent/dns_configurator.py` | [`agent/dns_configurator.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/dns_configurator.py) | Cấu hình DNS card mạng chính sang `127.0.0.1` qua lệnh `netsh` an toàn và tự khôi phục DHCP khi tắt tác tử. |
| **GIAI ĐOẠN 6: TÁC TỬ CLIENT — KIỂM SOÁT TIẾN TRÌNH THEO HASH SHA-256 (APP CONTROLLER)** | | | | |
| 37 | `T3_37` | Bổ sung thư viện `psutil` vào `agent/requirements.txt` | [`agent/requirements.txt`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/requirements.txt) | Đảm bảo `psutil` được cài đặt để giám sát tiến trình hệ thống. |
| 38 | `T3_38` | Khởi tạo module kiểm soát ứng dụng `agent/app_controller.py` | [`agent/app_controller.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/app_controller.py) | Tạo lớp `AppController` và hàm tính mã băm SHA-256 `get_file_sha256(filepath)` của tệp thực thi. |
| 39 | `T3_39` | Viết vòng lặp quét tiến trình định kỳ `scan_processes_loop()` trong `agent/app_controller.py` | [`agent/app_controller.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/app_controller.py) | Duyệt qua các tiến trình người dùng mỗi 3 - 5 giây, đối chiếu tên exe và mã hash SHA-256 với bảng `app_rules_cache`. |
| 40 | `T4_40` | Viết hàm kết thúc tiến trình và hiển thị popup giải thích theo NT4 trong `agent/app_controller.py` | [`agent/app_controller.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/app_controller.py) | Gọi `proc.terminate()`, hiển thị thông báo: "Ứng dụng [Tên] bị khóa theo quy định của cha mẹ kèm lý do" (**NT4**); ghi sự kiện `blocked_app`. |
| 41 | `T3_41` | Viết cơ chế chống vượt rào bằng đổi tên file thực thi trong `agent/app_controller.py` | [`agent/app_controller.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/app_controller.py) | Dù đổi tên tệp thực thi (ví dụ `notepad.exe` thành `game.exe`), hệ thống vẫn nhận diện đúng bằng mã băm SHA-256. |
| **GIAI ĐOẠN 7: TÁC TỬ CLIENT — BỘ ĐỆM SỰ KIỆN NGOẠI TUYẾN & GIAO DIỆN TRẺ (F3, NT3 & NT5)** | | | | |
| 42 | `T3_42` | Mở rộng `agent/storage.py` thêm bảng đệm sự kiện ngoại tuyến `pending_events` | [`agent/storage.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/storage.py) | Lưu sự kiện vào hàng đợi cục bộ với khóa chống trùng `idempotency_key` (UUID v4) và trường thời gian `ts`. |
| 43 | `T3_43` | Tạo module thu thập & đẩy sự kiện `agent/event_collector.py` | [`agent/event_collector.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/event_collector.py) | Hàm `record_event()` đệm sự kiện; vòng lặp `sync_events_loop()` đẩy theo lô (`POST /api/v1/events/batch`) khi có mạng và dọn sạch hàng đợi. |
| 44 | `T3_44` | Tạo giao diện minh bạch cho trẻ `agent/child_view.py` (NT5) | [`agent/child_view.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/child_view.py) | Cửa sổ giao diện "Hôm nay em đã dùng gì": hiển thị thời gian còn lại, top ứng dụng/web, danh sách chặn minh bạch. |
| 45 | `T3_45` | Tích hợp 2 nút "Xin thêm giờ" & "Báo chặn nhầm" vào `agent/child_view.py` (NT3) | [`agent/child_view.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/child_view.py) | Form cho trẻ gửi yêu cầu kèm lý do lên Server (`POST /api/v1/requests`), hiển thị phản hồi của cha mẹ khi được duyệt. |
| 46 | `T3_46` | Tích hợp menu mở giao diện trẻ vào `agent/tray.py` và khởi chạy các luồng mới trong `agent/main.py` | [`agent/main.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/main.py) | Khởi chạy đồng bộ: Luồng DNS Proxy, Luồng App Controller, Luồng Event Collector đồng hành cùng Luồng Nhịp tim & Screen Time. |
| **GIAI ĐOẠN 8: BÁO CÁO KỸ THUẬT MẠNG (M1, M2), BỘ KIỂM THỬ TỰ ĐỘNG & NGHIỆM THU (TESTS & DOCS)** | | | | |
| 47 | `T3_47` | Tạo tệp tài liệu Báo cáo Kỹ thuật Mạng mục M1 `docs/M1_LUONG_GOI_TIN_DNS.md` | [`docs/M1_LUONG_GOI_TIN_DNS.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M1_LUONG_GOI_TIN_DNS.md) | Sơ đồ tuần tự đường đi gói tin DNS từ Trình duyệt → Stub Resolver → DNS Proxy 127.0.0.1:53 → Sinkhole/Upstream kèm phân tích gói tin RFC 1035 & kịch bản Wireshark. |
| 48 | `T3_48` | Tạo tệp tài liệu Báo cáo Kỹ thuật Mạng mục M2 `docs/M2_SO_SANH_PHUONG_AN_CHAN.md` | [`docs/M2_SO_SANH_PHUONG_AN_CHAN.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M2_SO_SANH_PHUONG_AN_CHAN.md) | Bảng so sánh 4 phương án (tệp hosts, DNS proxy cục bộ, proxy HTTP/HTTPS, bộ lọc WFP) theo 5 tiêu chí bắt buộc và luận chứng lựa chọn DNS Proxy. |
| 49 | `T3_49` | Tạo bộ kiểm thử tự động DNS Proxy `tests/test_dns_proxy.py` | [`tests/test_dns_proxy.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/tests/test_dns_proxy.py) | Kiểm thử: Phân giải domain hợp lệ, Sinkhole domain cấm, chặn wildcard subdomain, SafeSearch rewrite Google/Bing, DoH canary NXDOMAIN, Whitelist NT6. |
| 50 | `T3_50` | Tạo bộ kiểm thử tự động App Controller & Sự kiện `tests/test_app_filtering_and_events.py` | [`tests/test_app_filtering_and_events.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/tests/test_app_filtering_and_events.py) | Kiểm thử: Tính toán SHA-256 tệp, phát hiện app cấm khi đổi tên; Batch sync sự kiện F3 với idempotency_key; Gửi và duyệt Access Request theo NT3. |
| 51 | `T3_51` | Tạo kịch bản nghiệm thu đầu-cuối Tuần 3 `docs/VERIFY_WEEK3.md` | [`docs/VERIFY_WEEK3.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/VERIFY_WEEK3.md) | Hướng dẫn kiểm chứng 4 tiêu chí chấp nhận DoD của Tuần 3: Chặn >= 95% tên miền mẫu; Bắt app cấm bằng SHA-256; SafeSearch qua nslookup; Trẻ xin giờ / duyệt tức thì. |

---

## III. TIÊU CHÍ NGHIỆM THU ĐẦU-CUỐI TUẦN 3 (DEFINITION OF DONE - DoD WEEK 3)

1. **DoD 1 (Lọc tên miền DNS Sinkhole & SafeSearch)**:
   - Chạy bộ kiểm thử 50 tên miền: Chặn >= 95% tên miền cần chặn; 0 dương tính giả trên 20 tên miền giáo dục.
   - Thử nghiệm lệnh `nslookup www.google.com 127.0.0.1` trả về IP SafeSearch `216.239.38.120`.
   - Truy vấn tên miền canary `use-application-dns.net` nhận phản hồi `NXDOMAIN`.
2. **DoD 2 (Kiểm soát ứng dụng bằng mã băm SHA-256)**:
   - Đổi tên tệp thực thi bị chặn (ví dụ `notepad.exe` đổi thành `game.exe`): Hệ thống nhận diện đúng bằng mã băm SHA-256, kết thúc tiến trình và bật popup giải thích lý do (NT4).
3. **DoD 3 (Bộ đệm sự kiện ngoại tuyến & Báo cáo F3)**:
   - Ngắt kết nối mạng: Sự kiện phát sinh được lưu vào bảng SQLite cục bộ `pending_events`. Khi có mạng trở lại, toàn bộ sự kiện được đồng bộ lên Server đầy đủ và không bị trùng lặp nhờ `idempotency_key`.
   - Dashboard phụ huynh hiển thị đầy đủ biểu đồ thời lượng ngày/tuần, Top 10 ứng dụng, Top 10 tên miền.
4. **DoD 4 (Minh bạch hai chiều & Quyền trẻ em NT3, NT5)**:
   - Trẻ mở giao diện "Hôm nay em đã dùng gì" trên máy con, thấy cùng dữ liệu với phụ huynh.
   - Trẻ bấm nút "Xin thêm giờ" (+15 phút) hoặc "Báo chặn nhầm"; Dashboard phụ huynh nhận thông báo và phụ huynh duyệt thành công, kích hoạt mở rộng thời gian tức thời qua WebSocket.
5. **DoD 5 (Kiểm thử tự động & Tài liệu M1, M2)**:
   - Toàn bộ test suite tự động (`pytest`) đạt 100% pass (tối thiểu 10 test cases mới cho DNS/App/Events, nâng tổng test case lên >= 34 tests).
   - Hoàn thành đầy đủ hai tài liệu chuyên sâu: `docs/M1_LUONG_GOI_TIN_DNS.md` và `docs/M2_SO_SANH_PHUONG_AN_CHAN.md`.
