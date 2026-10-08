# KẾ HOẠCH PHÁT TRIỂN DỰ ÁN 04 TUẦN (4 VERSIONS)
## ĐỀ TÀI: XÂY DỰNG ỨNG DỤNG HỖ TRỢ QUẢN LÝ VIỆC SỬ DỤNG MÁY TÍNH CỦA TRẺ EM (OGK - OPEN GUARDIAN KIDS)
> **Phương châm cốt lõi:** "Công cụ đồng hành, không phải phần mềm theo dõi lén"  
> **Khung phương pháp luận:** Spec-Driven Development (`speckit-plan`) kết hợp Nguyên tắc Kỹ thuật Karpathy (`karpathy-guidelines`)

---

## I. NGUYÊN TẮC QUẢN TRỊ KỸ THUẬT (KARPATHY GOVERNANCE)

1. **Think Before Coding**:
   - Trước khi code bất kỳ module nào, phải xác định rõ ràng ranh giới hệ thống trên Windows (đặc biệt là sự cô lập giữa Session 0 của Windows Service và Session người dùng của Tray UI; nguy cơ xung đột cổng UDP 53 của DNS Proxy; và độ trễ truyền thông).
   - Tuyệt đối không giả định ngầm. Mọi quyết định kỹ thuật phải bám sát 6 nguyên tắc đạo đức bắt buộc (NT1 đến NT6) và Danh mục Cấm.
2. **Simplicity First (Tối giản là trên hết)**:
   - Kiến trúc phẳng, chỉ viết lượng code tối thiểu cần thiết để thỏa mãn tiêu chí nghiệm thu của giáo viên.
   - Không vẽ thêm tính năng ngoài tài liệu (YAGNI). Không dựng microservices, không dùng Docker/Kubernetes hay cơ sở dữ liệu cồng kềnh; sử dụng **FastAPI + SQLite (WAL mode) + Python tiêu chuẩn (`pywin32`, `psutil`, `dnslib`)**.
   - Vượt qua "Senior Engineer Test": Một kỹ sư giàu kinh nghiệm nhìn vào thấy giải pháp sạch, trực diện và dễ bảo trì trong 15 phút.
3. **Surgical Changes (Phẫu thuật & Chia ranh giới nghiêm ngặt)**:
   - Chia dự án thành 4 phiên bản tăng trưởng ổn định (Vertical Slices). Mỗi tuần chỉ code đúng phạm vi của tuần đó. Không code trước tính năng của tuần sau.
   - Giữ mã nguồn gọn gàng, diff nhỏ, xóa bỏ ngay các hàm thừa và câu lệnh debug tạm thời.
4. **Goal-Driven Execution (Thực nghiệm & Tiêu chí nghiệm thu rõ ràng)**:
   - Mỗi tuần phải có một "Định nghĩa Hoàn thành" (Definition of Done - DoD) có thể demo thực tế và đo lường bằng số liệu hoặc hành vi cụ thể trước giảng viên.

---

## II. LỘ TRÌNH 4 PHIÊN BẢN (4 VERSIONS ROADMAP)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ TUẦN 1 (v0.1) │ The Backbone: Dựng khung Client-Server, Đăng nhập, Ghép đôi & Nhịp tim │
│ TUẦN 2 (v0.2) │ Time Governance: Quản lý thời gian F1, Chống tua giờ & Lõi đồng bộ F4  │
│ TUẦN 3 (v0.3) │ Deep Network Filtering: DNS Proxy F2, Kiểm soát App & Minh bạch F3     │
│ TUẦN 4 (v0.4) │ Security Hardening F5, Chống Bypass M3, Đo hiệu năng M4 & Đóng gói     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### PHIÊN BẢN 1 (v0.1) — TUẦN 1: BỘ KHUNG KẾT NỐI VÀ HẠ TẦNG CƠ BẢN
> **Mục tiêu:** Thiết lập khung chạy được đầu–cuối kết nối 3 khối (Agent — Server — Dashboard), xác thực phụ huynh, ghép đôi thiết bị và duy trì nhịp tim (Heartbeat).

#### 1. Áp dụng quy tắc Karpathy:
- **Tập trung vào:** Luồng kết nối mạng cơ bản giữa Client và Server.
- **Ranh giới nghiêm ngặt:** TUYỆT ĐỐI CHƯA viết bộ lọc DNS, chưa viết logic khóa màn hình hay kill tiến trình. Chỉ đảm bảo Agent kết nối được Server và nhận biết phiên bản chính sách.
- **Nhận diện bẫy kỹ thuật:** Cơ chế cấp phát mã ghép đôi (Pairing Code) 8 ký tự có thời hạn 10 phút để xác lập sự đồng ý của cha mẹ theo Nghị định 13/2023.

#### 2. Chi tiết các thành phần kỹ thuật:
- **`OGK-Server` (FastAPI)**:
  - Khởi tạo cấu trúc dự án `/server` với FastAPI và SQLite WAL (`ogk.db`).
  - Lược đồ cơ sở dữ liệu: Bảng `Parent` (tài khoản phụ huynh, băm mật khẩu Argon2id), `Child` (hồ sơ trẻ), `Device` (thiết bị ghép đôi, `device_fingerprint`), `HeartbeatLog`.
  - API Endpoints:
    - `POST /api/v1/auth/login`: Xác thực phụ huynh, trả về Cookie/Session token.
    - `POST /api/v1/enroll/create-code`: Phụ huynh tạo mã ghép 8 ký tự (hạn 10 phút).
    - `POST /api/v1/enroll/claim`: Agent gửi mã kèm device fingerprint, server cấp `device_id`, `access_token` (15 phút) và `refresh_token`.
    - `POST /api/v1/heartbeat`: Nhận trạng thái máy, trả về `policy_version` hiện tại.
- **`OGK-Agent` (Python)**:
  - Khởi tạo thư mục `/agent` với cấu trúc module tối giản.
  - Module `config_store.py`: Lưu trữ `device_id`, token và `policy_version` vào SQLite cục bộ (`agent_cache.db`).
  - Module `heartbeat_client.py`: Vòng lặp gửi nhịp tim định kỳ 60 giây lên Server.
  - Khung `tray_app.py`: Icon khay hệ thống cơ bản hiển thị thông báo "Open Guardian Kids đang hoạt động" khi khởi động (NT1).
- **`Dashboard` (Web responsive)**:
  - Khởi tạo thư mục `/dashboard`: Giao diện web nhẹ, thân thiện trên cả PC và trình duyệt di động.
  - Màn hình Đăng nhập phụ huynh.
  - Màn hình Quản lý Thiết bị: Nút "Thêm thiết bị mới" (sinh mã 8 ký tự) và bảng danh sách thiết bị kèm trạng thái "Online / Offline" dựa trên nhịp tim.
- **Tài liệu hoàn thành trong tuần**:
  - `docs/KienTrucHeThong.md`: Sơ đồ kiến trúc tổng thể và đặc tả giao thức ghép đôi/nhịp tim.
  - `docs/PRIVACY.md` (Bản thảo v1): Bảng giải trình 4 trường dữ liệu tối thiểu ban đầu theo Nghị định 13/2023.

#### 3. Tiêu chí nghiệm thu (Definition of Done - DoD Week 1):
- [x] Phụ huynh đăng nhập vào Dashboard thành công.
- [x] Tạo mã ghép đôi 8 ký tự trên Dashboard; chạy Agent nhập mã này; Server xác nhận ghép đôi và cấp token thành công.
- [x] Agent gửi nhịp tim mỗi 60 giây; Dashboard tự cập nhật trạng thái thiết bị là "Online".

---

### PHIÊN BẢN 2 (v0.2) — TUẦN 2: QUẢN LÝ THỜI GIAN VÀ ĐỒNG BỘ CHÍNH SÁCH (F1 & LÕI F4)
> **Mục tiêu:** Kiểm soát toàn bộ ngân sách thời gian (F1), ma trận lịch tuần 7×48, cơ chế chống tua giờ, khóa máy đúng hạn, và kênh đẩy chính sách khẩn cấp qua WebSocket (< 5s).

#### 1. Áp dụng quy tắc Karpathy:
- **Tập trung vào:** Độ chính xác của bộ đếm thời gian và tính tức thời của cơ chế khóa máy.
- **Ranh giới nghiêm ngặt:** Chỉ tập trung vào quản lý thời gian sử dụng màn hình chung. Chưa can thiệp vào gói tin mạng hay phân giải tên miền.
- **Nhận diện bẫy kỹ thuật:**
  - Trẻ có thể chỉnh lùi giờ hệ thống của Windows để kéo dài thời gian: Bắt buộc dùng `time.monotonic()` để tính delta giây thực và đối chiếu `server_time` tại mỗi nhịp tim.
  - Trẻ rời máy (không dùng): Dùng API `GetLastInputInfo` của Windows. Nếu không có thao tác bàn phím/chuột > 5 phút thì ngừng đếm quota.
  - Khóa máy: Dùng API chuẩn `LockWorkStation()` (nhẹ, an toàn, không gây crash Windows).

#### 2. Chi tiết các thành phần kỹ thuật:
- **`OGK-Agent`**:
  - Module `screen_time_tracker.py`:
    - Đếm thời gian sử dụng thực bằng đồng hồ đơn điệu `monotonic`.
    - Gọi Win32 `GetLastInputInfo` để phát hiện Idle time (> 300 giây không đếm).
    - Cảnh báo âm thanh/popup trước 10 phút, 5 phút, 1 phút và cho ân hạn 60 giây để lưu bài.
  - Module `system_locker.py`: Kích hoạt khóa máy (`user32.LockWorkStation`). Nếu trẻ cố mở lại mà đã hết quota, tự động khóa lại trong vòng 5 giây.
  - Module `policy_syncer.py`:
    - Nhận diện `policy_version` mới từ nhịp tim để kéo policy đầy đủ (`GET /api/v1/policy`).
    - Kiểm tra mã xác thực toàn vẹn HMAC của policy trước khi áp dụng.
  - Module `ws_listener.py`: Kết nối WebSocket tới server để nhận lệnh khẩn cấp (Khóa ngay / Cộng 15 phút).
- **`OGK-Server`**:
  - Lược đồ CSDL: Bảng `Policy` (phiên bản, quota ngày thường, quota cuối tuần, ma trận lịch tuần 7×48, HMAC), `CommandQueue`, `AuditLog`.
  - API Endpoints:
    - `GET /api/v1/policy`: Trả về chính sách mới nhất kèm chữ ký HMAC.
    - `POST /api/v1/policy`: Phụ huynh cập nhật chính sách từ Dashboard (ghi AuditLog: ai, lúc nào, giá trị cũ/mới).
    - `WebSocket /ws/device/{device_id}`: Kênh đẩy lệnh khẩn cấp từ phụ huynh tới Agent (< 5 giây).
- **`Dashboard`**:
  - Trình cấu hình Quota: Đặt số phút cho Ngày thường và Cuối tuần.
  - Ma trận Lịch tuần 7×48: Giao diện kéo/chọn trực quan các khung giờ 30 phút cho phép hoặc khóa.
  - Nút bấm Lệnh khẩn: "Khóa máy ngay", "Mở khóa", "Cộng thêm 15 phút".
  - Bảng Nhật ký kiểm toán (Audit Log): Hiển thị mọi lịch sử phụ huynh đổi luật (NT5).
- **Tài liệu hoàn thành trong tuần**:
  - `docs/BaoCaoKyThuatMang.pdf` - Soạn mục **M6 (Đồng bộ thời gian và chống chỉnh đồng hồ)**: Phân tích cơ chế monotonic clock và thực nghiệm lùi giờ hệ thống.

#### 3. Tiêu chí nghiệm thu (Definition of Done - DoD Week 2):
- [x] Đặt thử nghiệm quota 3 phút: Đúng 3 phút hệ thống phát cảnh báo và khóa màn hình máy tính trẻ.
- [x] Chỉnh lùi đồng hồ Windows 3 tiếng: Thời gian còn lại không bị tăng thêm, phát hiện và log cảnh báo lệch giờ.
- [x] Bấm nút "Khóa máy ngay" trên Dashboard: Máy của trẻ lập tức bị khóa trong vòng dưới 5 giây.
- [x] Trẻ xem được nhật ký thay đổi chính sách của cha mẹ (Audit log).

---

### PHIÊN BẢN 3 (v0.3) — TUẦN 3: LỌC MẠNG TẦNG DNS, KIỂM SOÁT APP VÀ MINH BẠCH (F2 & F3)
> **Mục tiêu:** Hiện thực bộ lọc website bằng DNS Proxy nội bộ 127.0.0.1:53 kèm SafeSearch, kiểm soát ứng dụng theo mã băm SHA-256, thu thập sự kiện tối thiểu và cung cấp màn hình minh bạch 2 chiều.

#### 1. Áp dụng quy tắc Karpathy:
- **Tập trung vào:** Cơ chế bắt gói tin DNS và kiểm soát tiến trình bằng Python gọn gàng (`dnslib` + `psutil`).
- **Ranh giới nghiêm ngặt:** Không can thiệp sâu vào HTTPS proxy (không giải mã TLS / MITM vì rủi ro vi phạm quyền riêng tư và dễ hỏng mạng của máy). Sử dụng DNS sinkholing (trả lời IP loopback hoặc NXDOMAIN) để chặn tên miền.
- **Nhận diện bẫy kỹ thuật:**
  - Lọc domain phải xử lý cả wildcard subdomain (ví dụ chặn `example.com` thì phải tự động chặn cả `sub.example.com`).
  - Danh sách trắng vĩnh viễn (NT6): Luôn bypass các cổng thông tin trường học và tổng đài bảo vệ trẻ em 111.
  - Phân loại ứng dụng bằng SHA-256 để chống trẻ đổi tên file thực thi (`notepad.exe` đổi thành `game.exe`).

#### 2. Chi tiết các thành phần kỹ thuật:
- **`OGK-Agent`**:
  - Module `dns_proxy.py`:
    - Lắng nghe UDP socket trên `127.0.0.1:53`.
    - Kiểm tra domain truy vấn: Nếu thuộc danh sách chặn -> trả về `0.0.0.0` hoặc IP hiển thị trang thông báo chặn.
    - Cưỡng chế SafeSearch: Tự động rewrite bản ghi của Google, Bing, YouTube về VIP forcesafesearch.
    - Trả lời NXDOMAIN cho tên miền Canary của DoH (`use-application-dns.net`) để tắt DoH tự động của trình duyệt.
    - Các domain hợp lệ khác: Chuyển tiếp (forward) lên DNS an toàn (1.1.1.3 hoặc 8.8.8.8) và trả kết quả về cho hệ điều hành.
  - Module `app_controller.py`:
    - Dùng `psutil` theo dõi các tiến trình đang chạy định kỳ (quét mỗi 3-5 giây).
    - Tính mã băm SHA-256 của file thực thi, đối chiếu với Blocklist/Allowlist.
    - Khi phát hiện app cấm: Kết thúc tiến trình (`process.terminate()`) và bật cửa sổ popup giải thích rõ lý do chặn và người đặt luật (NT4).
  - Module `event_collector.py`:
    - Đệm các sự kiện theo đúng lược đồ F3: `ts, device_id, child_id, type, subject, duration_sec, policy_id`.
    - Lưu vào SQLite đệm cục bộ khi mất mạng; đẩy theo lô (batch sync) lên Server có khóa chống trùng lặp (`idempotency_key`).
  - Giao diện `child_view.py`:
    - Màn hình dành cho trẻ: "Hôm nay em đã dùng gì" (biểu đồ trực quan, danh sách app/web đã dùng).
    - Nút "Xin thêm giờ" và nút "Con nghĩ trang này bị chặn nhầm".
- **`OGK-Server`**:
  - CSDL: Bảng `ActivityEvent`, `AccessRequest` (yêu cầu xin giờ / khiếu nại).
  - API Endpoints:
    - `POST /api/v1/events/batch`: Nhận danh sách sự kiện từ agent.
    - `GET /api/v1/reports/summary`: Tổng hợp thời lượng sử dụng, Top 10 app, Top 10 domain, số lần bị chặn.
    - `POST /api/v1/requests`: Tiếp nhận yêu cầu từ trẻ; `PUT /api/v1/requests/{id}`: Phụ huynh phê duyệt/từ chối.
- **`Dashboard`**:
  - Bảng thống kê Báo cáo: Biểu đồ thời lượng theo ngày/tuần, Top 10 ứng dụng, Top 10 tên miền.
  - Danh sách Quản lý danh mục 200 tên miền (Giáo dục, Giải trí, Mạng xã hội, Game, Không phù hợp).
  - Khu vực tiếp nhận và duyệt yêu cầu từ con (Xin thêm giờ, phản hồi chặn nhầm).
- **Tài liệu hoàn thành trong tuần**:
  - `docs/BaoCaoKyThuatMang.pdf` - Soạn mục **M1 (Sơ đồ luồng gói tin DNS kèm ảnh chụp Wireshark)** và mục **M2 (So sánh 4 phương án chặn: hosts, DNS proxy, HTTP proxy, WFP)**.

#### 3. Tiêu chí nghiệm thu (Definition of Done - DoD Week 3):
- [x] Chạy bộ test 50 tên miền kiểm thử: Chặn >= 95% tên miền cần chặn; 0 dương tính giả trên 20 tên miền giáo dục.
- [x] Đổi tên ứng dụng bị chặn thành tên khác: Hệ thống vẫn nhận diện đúng bằng mã băm SHA-256 và tắt ứng dụng kèm thông báo lý do.
- [x] Cưỡng chế SafeSearch thành công trên Google/Bing (kiểm chứng bằng `nslookup`).
- [x] Trẻ bấm nút "Xin thêm giờ" trên giao diện máy con; phụ huynh nhận được thông báo trên Dashboard và duyệt cộng giờ thành công.

---

### PHIÊN BẢN 4 (v0.4) — TUẦN 4: BẢO MẬT F5, CHỐNG BYPASS, ĐO HIỆU NĂNG VÀ ĐÓNG GÓI HỒ SƠ
> **Mục tiêu:** Gia cố toàn diện bảo mật (F5), hoàn thiện phân tích & đối phó 7 kỹ thuật vượt rào (M3), đo đạc hiệu năng thực nghiệm (M4), kiểm thử tự động, và hoàn thiện toàn bộ hồ sơ nộp đồ án.

#### 1. Áp dụng quy tắc Karpathy:
- **Tập trung vào:** Tính ổn định, bảo mật chiều sâu và bằng chứng thực nghiệm (không viết thêm tính năng mới).
- **Ranh giới nghiêm ngặt:** Chỉ refactor phẫu thuật, sửa các lỗi biên (edge cases), xóa sạch code rác/debug, bổ sung unit/integration tests.
- **Nhận diện bẫy kỹ thuật:**
  - Chống vượt rào (Bypass): Trung thực trong việc thừa nhận giới hạn (ví dụ không thể chống khởi động USB nếu không khóa BIOS, chấp nhận rủi ro và nêu biện pháp đối phó trong báo cáo thay vì cài rootkit).
  - Quyền riêng tư: Hoàn thiện tính năng "Xóa toàn bộ dữ liệu của con tôi" xóa đồng thời trên Server và bộ đệm Agent (Nghị định 13/2023).

#### 2. Chi tiết các thành phần kỹ thuật:
- **Gia cố bảo mật F5**:
  - Mật khẩu phụ huynh: Băm bằng Argon2id, tối thiểu 10 ký tự, khóa 15 phút sau 5 lần sai, rate limit theo IP.
  - Quản lý phiên: Cookie `HttpOnly`, `Secure`, `SameSite=Lax`, thời hạn 12 giờ, hủy phiên phía server, token CSRF cho mọi thao tác ghi.
  - Phân quyền chống IDOR: Kiểm tra quyền sở hữu (`parent_id`) ở tầng truy vấn DB (không chỉ ẩn nút giao diện).
  - Dữ liệu lưu trữ: Mã hóa các trường cấu hình nhạy cảm bằng AES-GCM (khóa lấy từ biến môi trường/DPAPI, không hardcode).
  - Tự động xóa dữ liệu sau 90 ngày (Cron job định kỳ). Nút "Xóa toàn bộ dữ liệu của con tôi" hoạt động hoàn hảo.
- **Phân tích và đối phó đường vòng (M3)**:
  - Thử nghiệm và hoàn thành báo cáo đối phó 7 kỹ thuật vượt rào:
    1. Đổi DNS card mạng thủ công (Agent tự khôi phục về 127.0.0.1 hoặc phát hiện cảnh báo).
    2. DNS-over-HTTPS (DoH) trong trình duyệt (Chặn DoH IP endpoints và Canary domain).
    3. DNS-over-TLS (Chặn cổng 853).
    4. VPN / Proxy công cộng (Chặn các tiến trình VPN phổ biến và ghi nhận log).
    5. Truy cập trực tiếp qua IP (Giải thích giới hạn và đối phó bằng blocklist IP).
    6. Safe Mode / Khởi động lại (Ghi nhận thời gian gián đoạn nhịp tim).
    7. Kill tiến trình Agent (Cấu hình Service Recovery của Windows tự restart trong 5s; cảnh báo máy chủ khi mất nhịp tim).
- **Đo lường hiệu năng thực nghiệm (M4 & M5)**:
  - Thu thập tối thiểu 30 mẫu đo:
    - Mức tiêu thụ CPU & RAM của Agent khi rảnh rỗi và cao điểm.
    - Độ trễ phân giải DNS (p50, p95) khi có Agent so với DNS thông thường.
    - Độ trễ áp dụng chính sách từ Dashboard xuống máy trẻ (qua WebSocket và qua Heartbeat).
  - Kiểm tra khả năng chịu lỗi (M5): Kịch bản mất mạng, server ngừng hoạt động, agent bị tắt tiến trình.
- **Bộ kiểm thử tự động (`/tests`)**:
  - Viết tối thiểu 15 Unit tests: DNS packet parser, monotonic time tracker, hash matcher, token validator, rate limiter,...
  - Viết 5 Integration tests: Quy trình ghép đôi (enrollment), đồng bộ chính sách (policy sync), đẩy sự kiện theo lô (event ingest), lệnh khẩn qua WebSocket, duyệt yêu cầu thêm giờ.
- **Đóng gói trọn bộ hồ sơ nộp đồ án**:
  - `README.md`: Hướng dẫn cài đặt sạch và chạy thử trong vòng 15 phút.
  - `docs/BaoCao.docx`: Báo cáo chính 20–30 trang (có tỷ lệ đóng góp của từng thành viên).
  - `docs/BaoCaoKyThuatMang.pdf`: Báo cáo chuyên sâu đầy đủ 6 mục M1 đến M6.
  - `docs/PRIVACY.md`: Bảng giải trình trường dữ liệu + phiên bản ngôn ngữ dành riêng cho trẻ.
  - `docs/THREATMODEL.md`: Mô hình đe dọa STRIDE (8 mối đe dọa) + Checklist ASVS v4 Level 1 (>= 20 mục).
  - `docs/AI_USAGE.md`: Minh bạch các phần dùng AI hỗ trợ và quy trình kiểm chứng.
  - `demo/KichBanDemo.md` & `demo/video.mp4`: Video clip demo 5–7 phút có phụ đề tiếng Việt.

#### 3. Tiêu chí nghiệm thu (Definition of Done - DoD Week 4):
- [x] Bộ kiểm thử tự động (`pytest`) đạt 100% pass (tối thiểu 15 unit tests, 5 integration tests).
- [x] Số liệu đo đạc thực tế M4 đầy đủ >= 30 mẫu có biểu đồ đối chiếu.
- [x] Máy ảo Windows sạch cài đặt và chạy thành công toàn bộ hệ thống trong vòng 15 phút theo đúng `README.md`.
- [x] Đầy đủ toàn bộ 10 hạng mục tệp/thư mục sản phẩm theo bảng quy định của giáo viên.

---

## III. BẢNG MA TRẬN PHÂN BỔ TÍNH NĂNG THEO TUẦN

| Tính năng / Hạng mục | Tuần 1 (v0.1) | Tuần 2 (v0.2) | Tuần 3 (v0.3) | Tuần 4 (v0.4) |
| :--- | :---: | :---: | :---: | :---: |
| **Xác thực phụ huynh & Ghép đôi (Enrollment)** | **Hoàn thành** | Hoàn thiện | Duy trì | Đạt chuẩn F5/ASVS |
| **Giao thức Nhịp tim (Heartbeat 60s)** | **Hoàn thành** | Đồng bộ version | Đẩy sự kiện | Kiểm thử chịu lỗi (M5) |
| **F1. Quản lý thời gian (Quota & Lịch tuần 7x48)** | Chưa làm | **Hoàn thành** | Duy trì | Đo đạc sai số |
| **F1. Chống tua giờ (Monotonic) & Khóa máy** | Chưa làm | **Hoàn thành** | Duy trì | Hoàn thiện M6 |
| **F4. Lệnh khẩn qua WebSocket (< 5s)** | Khung kết nối | **Hoàn thành** | Duy trì | Đo đạc độ trễ (M4) |
| **F2. Lọc DNS Proxy 127.0.0.1:53 & SafeSearch** | Chưa làm | Chưa làm | **Hoàn thành** | Tối ưu p50/p95 (M4) |
| **F2. Chặn ứng dụng theo hash SHA-256** | Chưa làm | Chưa làm | **Hoàn thành** | Duy trì |
| **F3. Ghi nhận sự kiện tối thiểu & Báo cáo** | Chưa làm | Chưa làm | **Hoàn thành** | Auto-delete 90 ngày |
| **F3. Giao diện minh bạch cho trẻ & Nút xin giờ** | Icon khay cơ bản | Popup cảnh báo | **Hoàn thành** | Duy trì |
| **F5. Bảo mật nâng cao (AES-GCM, Anti-IDOR, CSRF)** | Cơ bản | Cơ bản | Cơ bản | **Hoàn thiện 100%** |
| **M1-M6. Báo cáo Kỹ thuật Mạng** | Dự thảo | Viết M6 | Viết M1, M2 | **Hoàn thiện M3, M4, M5** |
| **Kiểm thử tự động (Unit & Integration tests)** | Test cơ bản | Test thời gian | Test DNS/App | **Đạt chuẩn 15+5 tests** |
| **Đóng gói báo cáo, video demo & README** | Dựng outline | Cập nhật | Cập nhật | **Hoàn tất 100%** |
