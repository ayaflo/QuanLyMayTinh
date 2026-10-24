# OPEN GUARDIAN KIDS (OGK) — VERSION 0.4 (FINAL RELEASE)
## HỆ THỐNG ĐỒNG HÀNH VÀ QUẢN LÝ MÁY TÍNH TRẺ EM TOÀN DIỆN
> **Đồ án Tốt nghiệp Chuyên ngành:** Mạng máy tính & Truyền thông dữ liệu  
> **Cơ sở đào tạo:** Khoa Mạng Máy tính & Truyền thông — Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM  
> **Căn cứ pháp lý:** Luật Trẻ em 2016 (Điều 21, 54) & Nghị định 13/2023/NĐ-CP (Điều 20)  
> **Tiêu chuẩn An toàn thông tin:** OWASP ASVS v4.0.3 Level 1 & NIST SP 800-63B  

---

```
   ____                     ____                     _ _             _  ___     _     
  / __ \                   / ___|                   | (_)           | |/ (_)   | |    
 | |  | |_ __   ___ _ __  | |  __ _   _  __ _ _ __  | |_  __| |___  | ' / _  __| |___ 
 | |  | | '_ \ / _ \ '_ \ | | |_ | | | |/ _` | '_ \ | | |/ _` / __| |  < | |/ _` / __|
 | |__| | |_) |  __/ | | || |__| | |_| | (_| | | | || | | (_| \__ \ | . \| | (_| \__ \
  \____/| .__/ \___|_| |_| \_____|\__,_|\__,_|_| |_||_|_|\__,_|___/ |_|\_\_|\__,_|___/
        | |                                                                           
        |_|   Triết lý: Đồng hành giáo dục, KHÔNG PHẢI phần mềm theo dõi lén!
```

---

## 1. GIỚI THIỆU TỔNG QUAN & TRIẾT LÝ DỰ ÁN

**Open Guardian Kids (OGK)** là giải pháp phần mềm quản lý và bảo vệ trẻ em khi sử dụng máy tính, được xây dựng với mục tiêu giải quyết triệt để vấn đề xung đột thế hệ giữa cha mẹ và con cái trong kỷ nguyên số. Thay vì áp dụng các kỹ thuật gián điệp (Spyware/Rootkit) độc hại, OGK tiên phong hiện thực hóa **6 Nguyên tắc Quản trị Đạo đức (NT1 — NT6)**:
- **Minh bạch hai chiều (NT1 & NT5):** Biểu tượng ứng dụng luôn hiển thị thường trực trên khay hệ thống; trẻ em có toàn quyền xem các quy định và thời gian đã sử dụng.
- **Tôn trọng quyền riêng tư (NT2):** Kiên quyết **KHÔNG** chụp màn hình, **KHÔNG** keylogger, **KHÔNG** ghi âm/webcam, **KHÔNG** lưu URL đầy đủ có query parameters.
- **Lắng nghe tiếng nói của con (NT3):** Tích hợp kênh tương tác xin thêm thời gian và duyệt yêu cầu mở web hai chiều thời gian thực.
- **An toàn công bằng (NT4 & NT6):** Cảnh báo trước khi hết giờ (10p, 5p, 1p), tạm dừng đếm giờ khi trẻ rời máy tính (> 5p), và miễn trừ khóa vĩnh viễn với các website trường học (`.edu.vn`) và Tổng đài Quốc gia 111.

---

## 2. KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

Hệ thống được tổ chức theo mô hình **Khách - Chủ phân tán hướng ngoại tuyến (Offline-First Client-Server)**:

```mermaid
graph TB
    subgraph ParentUI [Giao Diện Phụ Huynh]
        WebDash["Web Dashboard (HTML5 / Modern CSS / Chart.js)"]
    end

    subgraph ServerCore [Central Server Engine (FastAPI)]
        RouterAPI["REST API (Auth, Policy, Events, Retention)"]
        WSManager["WebSocket Channel (< 500ms Emergency Dispatch)"]
        CryptoService["AES-256-GCM & Argon2id Engine"]
        RetentionWorker["24h Retention Purge (Decree 13/2023)"]
        ServerDB[("Database (PostgreSQL / SQLite WAL)")]
    end

    subgraph ChildAgent [Client Agent (Windows 10/11)]
        TrayGUI["System Tray Icon & Toast Notification (NT1)"]
        TimeEngine["Monotonic Screen Time Tracker (M6)"]
        DNSProxy["Local DNS Sinkhole Proxy (127.0.0.1:53)"]
        DNSWatchdog["DNS Adapter Watchdog 20s (M3 Anti-Bypass)"]
        AppBlocker["SHA-256 App Controller & VPN Blocker (M3)"]
        OfflineBuffer[("Local SQLite WAL (agent_cache.db)")]
    end

    ParentUI <-->|HTTPS / REST API & Session Cookie| RouterAPI
    ParentUI <-->|WSS Real-time Push| WSManager
    RouterAPI <--> ServerDB
    WSManager <--> RouterAPI
    RetentionWorker <--> ServerDB

    WSManager <-->|WebSocket Commands (Lock / Add Time)| ChildAgent
    RouterAPI <-->|Batch Telemetry Ingestion (Idempotency)| ChildAgent
    TimeEngine <--> OfflineBuffer
    DNSProxy <--> OfflineBuffer
    AppBlocker <--> OfflineBuffer
```

---

## 3. BẢNG TÍNH NĂNG HOÀN THIỆN (VERSION 0.4 RELEASE)

| Nhóm tính năng | Mã | Mô tả kỹ thuật chi tiết | Trạng thái |
| :--- | :---: | :--- | :---: |
| **Quản trị Thời gian** | `F1` | Đồng hồ đơn điệu `time.monotonic()`, Ma trận lịch 7x48 khung giờ (30 phút/slot), Nhận diện máy rảnh (Win32 Idle > 300s), Cảnh báo 10p/5p/1p, Ân hạn 60s, Khóa máy `LockWorkStation`. | **100% [✓]** |
| **Lọc Mạng & Ứng dụng** | `F2` | DNS Sinkhole Proxy `127.0.0.1:53` (RFC 1035), 200 tên miền phân loại, Ép SafeSearch Google/Bing/YouTube, Chặn DoH Canary (`use-application-dns.net`), Kiểm soát nhị phân SHA-256. | **100% [✓]** |
| **Viễn trắc Tối thiểu** | `F3` | Thu thập tối thiểu 4 trường siêu dữ liệu (`ts`, `device_id`, `type`, `subject`), Bộ đệm ngoại tuyến SQLite WAL, Đồng bộ bù lũy kết với khóa UUID v4 (`idempotency_key`). | **100% [✓]** |
| **Tương tác & Lệnh Khẩn** | `F4` | Kênh hai chiều: Trẻ xin thêm giờ / Phụ huynh phê duyệt; Kênh WebSocket phát lệnh khẩn cấp tức thì (Khóa máy / Thêm giờ) với độ trễ thực tế **5.95 ms**. | **100% [✓]** |
| **Bảo mật Nâng cao F5** | `F5` | Mật khẩu Argon2id $\ge$ 10 ký tự (NIST SP 800-63B), Khóa tài khoản 15 phút sau 5 lần sai, Rate Limit 10 req/phút/IP, Cookie `HttpOnly, SameSite=Lax`, Phân quyền chống IDOR 100%, Mã hóa AES-256-GCM. | **100% [✓]** |
| **Khắc chế Vượt rào M3** | `M3` | `DNSWatchdog` quét 20s tự phục hồi `127.0.0.1`, Nạp sẵn danh mục chặn tiến trình VPN (Cloudflare WARP, ProtonVPN, Psiphon, UltraSurf) bằng đối soát kép SHA-256 + Tên file. | **100% [✓]** |
| **Đo lường Hiệu năng M4** | `M4` | RAM tác tử chỉ **25.2 MB**, CPU **0.0%**, Phân giải DNS tên miền cấm siêu tốc **0.81 ms**, Lệnh khẩn cấp phản hồi **5.95 ms** qua 30-50 mẫu thực nghiệm. | **100% [✓]** |
| **Chịu lỗi & Phục hồi M5** | `M5` | Đệm ngoại tuyến không rơi rớt sự kiện khi mất mạng, Cưỡng chế hạn mức độc lập khi máy chủ sập, Khôi phục nguyên vẹn thời gian đã dùng và cờ khóa máy sau khi khởi động lại máy tính. | **100% [✓]** |
| **Tuân thủ Nghị định 13** | `LAW` | Tự động tiêu hủy dữ liệu cũ hơn **90 ngày** (chu kỳ 24h); Chức năng "Xóa toàn bộ dữ liệu con tôi" (Right to Erasure) xóa đồng bộ Server và Agent với mật khẩu bảo vệ. | **100% [✓]** |

---

## 4. HƯỚNG DẪN CÀI ĐẶT & VẬN HÀNH SẠCH TRONG 15 PHÚT (QUICK START GUIDE)

Hệ thống được thiết kế theo nguyên tắc tối giản (Karpathy Style): Sử dụng hoàn toàn Python tiêu chuẩn, không yêu cầu cài đặt Docker, Redis, hay các phần mềm phụ thuộc phức tạp.

### 4.1. Yêu cầu tiên quyết (Prerequisites)
- Máy tính chạy hệ điều hành **Windows 10 hoặc Windows 11 (64-bit)**.
- Đã cài đặt **Python 3.10 trở lên** (Khuyến nghị Python 3.12, tích chọn *"Add python.exe to PATH"* khi cài).

---

### 4.2. Các bước triển khai chi tiết (5 Bước — 15 Phút)

#### BƯỚC 1: Tải mã nguồn và tạo môi trường ảo (2 phút)
Mở cửa sổ PowerShell tại thư mục làm việc:
```powershell
# Di chuyển vào thư mục dự án
cd "d:\CD TN MMT\QuanLyMayTinh"

# Tạo môi trường ảo Python cô lập
python -m venv .venv

# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1
```

#### BƯỚC 2: Cài đặt các gói thư viện phụ thuộc (3 phút)
Cài đặt các gói thư viện đã được tối ưu hóa:
```powershell
pip install fastapi uvicorn[standard] sqlalchemy pydantic jinja2 python-multipart requests cryptography argon2-cffi pyjwt psutil dnslib pywin32 pytest httpx
```

#### BƯỚC 3: Khởi động Máy chủ Trung tâm (Central Server) (2 phút)
Chạy máy chủ backend FastAPI:
```powershell
python -m uvicorn server.main:app --host 127.0.0.1 --port 8000 --reload
```
*Giao diện máy chủ sẽ tự động nạp CSDL SQLite WAL, chạy migration, nạp 200 tên miền phân loại và 7 ứng dụng VPN mẫu.*

#### BƯỚC 4: Đăng nhập Web Dashboard & Lấy mã ghép đôi (3 phút)
1. Mở trình duyệt web truy cập địa chỉ: [**http://127.0.0.1:8000**](http://127.0.0.1:8000)
2. Nếu chưa có tài khoản, nhấn **"Đăng ký tài khoản mới"**:
   - Tên đăng nhập: `admin_parent`
   - Mật khẩu: `ParentSecret@2026` (yêu cầu tối thiểu 10 ký tự theo NIST)
3. Tại trang **Quản Lý Thiết Bị**, nhấn nút **"+ Thêm Thiết Bị Mới"** để sinh mã ghép đôi gồm 8 ký tự (ví dụ: `A1B2C3D4`, có hiệu lực trong 10 phút).

#### BƯỚC 5: Khởi chạy Tác tử Máy Con (Client Agent) (5 phút)
Mở một cửa sổ PowerShell thứ hai (với quyền **Administrator** để tác tử tự động cấu hình DNS card mạng):
```powershell
# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Khởi chạy tác tử máy con
python agent/main.py
```
- Tác tử sẽ hiển thị thông báo chào đón và hỏi mã ghép đôi.
- Nhập mã 8 ký tự vừa lấy trên Dashboard.
- **Hoàn tất!** Biểu tượng chiếc khiên xanh sẽ xuất hiện trên khay hệ thống, card mạng được trỏ về `127.0.0.1`, và máy tính của con lập tức được bảo vệ an toàn.

---

## 5. HƯỚNG DẪN CHẠY BỘ KIỂM THỬ TỰ ĐỘNG & ĐO LƯỜNG HIỆU NĂNG

### 5.1. Chạy toàn bộ Test Suite (100% Pass)
Kiểm chứng tự động toàn bộ 59 kịch bản kiểm thử (Bảo mật F5, DNS Proxy, Hạn mức giờ, Ghép đôi, WebSocket, Chịu lỗi M5):
```powershell
pytest tests/ -v
```
*(Kết quả kỳ vọng: **59 passed, 0 failed** trong vòng ~9 giây).*

### 5.2. Chạy kịch bản đo đạc hiệu năng thực nghiệm M4
Chạy công cụ benchmark tự động thu thập tài nguyên CPU/RAM, độ trễ DNS và độ trễ WebSocket:
```powershell
python scripts/benchmark_performance.py --samples 30
```
*Kết quả sẽ được xuất ra bảng Markdown trên màn hình và lưu vào tệp [`docs/benchmark_results.json`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/benchmark_results.json).*

---

## 6. DANH MỤC HỒ SƠ TÀI LIỆU KỸ THUẬT (DOCUMENTATION INDEX)

Toàn bộ hệ thống báo cáo chuyên đề và phụ lục kỹ thuật được lưu trữ trong thư mục [`docs/`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/):

| Tệp tài liệu | Phân loại | Nội dung chính |
| :--- | :---: | :--- |
| [`docs/PRIVACY.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/PRIVACY.md) | Pháp lý & Đạo đức | Tuân thủ Nghị định 13/2023, 4 trường dữ liệu tối thiểu, Tiêu hủy 90 ngày, Quyền xóa dữ liệu, Bản cam kết cho trẻ. |
| [`docs/THREATMODEL.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/THREATMODEL.md) | An toàn thông tin | Mô hình đe dọa STRIDE (8 mối đe dọa) & Bảng kiểm soát 22 tiêu chí OWASP ASVS v4 Level 1. |
| [`docs/AI_USAGE.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/AI_USAGE.md) | Liêm chính học thuật | Tuyên bố minh bạch ứng dụng AI, Ranh giới trách nhiệm, Quy trình kiểm chứng chéo 4 bước. |
| [`docs/M1_LUONG_GOI_TIN_DNS.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M1_LUONG_GOI_TIN_DNS.md) | Chuyên ngành Mạng M1 | Phân tích luồng gói tin DNS RFC 1035, Sinkholing 0.0.0.0, SafeSearch, DoH Canary RCODE 3. |
| [`docs/M2_SO_SANH_PHUONG_AN_CHAN.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M2_SO_SANH_PHUONG_AN_CHAN.md) | Chuyên ngành Mạng M2 | So sánh định lượng 3 phương án: DNS Sinkholing vs MITM Proxy vs L7 Firewall (Ưu/Nhược/Hiệu năng). |
| [`docs/M3_PHAN_TICH_DOI_PHO_BYPASS.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M3_PHAN_TICH_DOI_PHO_BYPASS.md) | Chuyên ngành Mạng M3 | Luận chứng 7 kỹ thuật vượt rào mạng (Đổi DNS, DoH, DoT, VPN, Hosts file, Safe Mode, Kill process). |
| [`docs/M4_DO_LUONG_HIEU_NANG.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M4_DO_LUONG_HIEU_NANG.md) | Chuyên ngành Mạng M4 | Báo cáo thực nghiệm N=30–50 mẫu: RAM 25.2MB, CPU 0%, DNS p50 0.81ms, WebSocket 5.95ms. |
| [`docs/M5_KHA_NANG_CHIU_LOI.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M5_KHA_NANG_CHIU_LOI.md) | Chuyên ngành Mạng M5 | Kiểm chứng 3 kịch bản: Mất mạng (Đệm SQLite), Máy chủ sập (Khóa máy ngoại tuyến), Khởi động lại. |
| [`docs/M6_DONG_BO_THOI_GIAN.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/M6_DONG_BO_THOI_GIAN.md) | Chuyên ngành Mạng M6 | Cơ chế đồng hồ đơn điệu `time.monotonic()` chống chỉnh lùi giờ Windows, Nhận diện máy rảnh Win32. |
| [`docs/VERIFY_WEEK4.md`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/VERIFY_WEEK4.md) | Nghiệm thu đầu-cuối | Kịch bản kiểm chứng thực tế 5 tiêu chuẩn đầu ra Definition of Done (DoD) của đồ án tốt nghiệp. |

---

## 7. GIẤY PHÉP VÀ BẢN QUYỀN (LICENSE)

Dự án được phát hành dưới giấy phép mã nguồn mở **MIT License**. Mọi cá nhân, tổ chức giáo dục và phụ huynh đều có quyền tự do sử dụng, tùy biến và triển khai phi thương mại nhằm mục đích bảo vệ trẻ em trên không gian mạng.
