# CẨM NANG KIẾN THỨC TOÀN DIỆN VỀ HỆ THỐNG OPEN GUARDIAN KIDS (OGK)
## GIÁO TRÌNH BÁCH KHOA CHUYÊN ĐỀ TỐT NGHIỆP: MẠNG MÁY TÍNH & AN TOÀN HỆ THỐNG

> **Mục đích tài liệu:**  
> Tài liệu này được biên soạn như một **giáo trình bách khoa chuyên sâu từ gốc rễ (First-Principles)**, phục vụ bảo vệ đồ án tốt nghiệp ngành Mạng máy tính & An toàn thông tin.  
> **Nguyên tắc biên soạn:** Tuyệt đối không giả định người đọc đã biết trước các khái niệm nền tảng. Mọi thuật ngữ chuyên ngành, từ viết tắt tiếng Anh, giao thức mạng, cấu trúc từng byte bản tin, giải thuật mật mã và hàm nhân hệ điều hành đều được giải thích tường tận từ con số 0, kèm ví dụ đời thường trực quan, cơ chế hoạt động từng bước và vai trò thực tế trong dự án Open Guardian Kids (OGK).

---

# MỤC LỤC TỔNG QUAN

- [PHẦN 1: NỀN TẢNG MẠNG MÁY TÍNH & GIAO THỨC TRUYỀN DẪN DỮ LIỆU](#phần-1-nền-tảng-mạng-máy-tính--giao-thức-truyền-dẫn-dữ-liệu)
  - [1.1. Địa chỉ IP, Tên miền (Domain), Cổng mạng (Port) & Socket là gì?](#11-địa-chỉ-ip-tên-miền-domain-cổng-mạng-port--socket-là-gì)
  - [1.2. So sánh giao thức truyền tải: UDP vs TCP & Bắt tay 3 bước (3-Way Handshake)](#12-so-sánh-giao-thức-truyền-tải-udp-vs-tcp--bắt-tay-3-bước-3-way-handshake)
  - [1.3. Giao thức DNS (Domain Name System) & Quy trình phân giải tên miền](#13-giao-thức-dns-domain-name-system--quy-trình-phân-giải-tên-miền)
  - [1.4. MÃ HÓA TLS/HTTPS TỪ GỐC RỄ: Mã hóa đối xứng, Bất đối xứng, Chứng chỉ số & Quy trình Bắt tay TLS 1.3](#14-mã-hóa-tlshttps-từ-gốc-rễ-mã-hóa-đối-xứng-bất-đối-xứng-chứng-chỉ-số--quy-trình-bắt-tay-tls-13)
  - [1.5. SỰ TIẾN HÓA CỦA BẢN TIN WEB: Mổ xẻ cấu trúc bản tin HTTP/1.1 vs HTTP/2 (Binary Framing) vs HTTP/3 (QUIC)](#15-sự-tiến-hóa-của-bản-tin-web-mổ-xẻ-cấu-trúc-bản-tin-http11-vs-http2-binary-framing-vs-http3-quic)
  - [1.6. Kỹ thuật DNS Sinkholing (Hố đen DNS) - Trọng tâm lọc web của OGK](#16-kỹ-thuật-dns-sinkholing-hố-đen-dns---trọng-tâm-lọc-web-của-ogk)
  - [1.7. DoH (DNS-over-HTTPS) & DoT (DNS-over-TLS) là gì? Tại sao DoH qua mặt được tường lửa?](#17-doh-dns-over-https--dot-dns-over-tls-là-gì-tại-sao-doh-qua-mặt-được-tường-lửa)
  - [1.8. Canary Domain (`use-application-dns.net`) - Cơ chế quốc tế khắc chế DoH](#18-canary-domain-use-application-dnsnet---cơ-chế-quốc-tế-khắc-chế-doh)
  - [1.9. Tường lửa (Firewall) & Lệnh Netsh trong Windows](#19-tường-lửa-firewall--lệnh-netsh-trong-windows)
  - [1.10. Mạng riêng ảo (VPN), Card mạng ảo TUN/TAP & Cơ chế chặn VPN bằng SHA-256](#110-mạng-riêng-ảo-vpn-card-mạng-ảo-tuntap--cơ-chế-chặn-vpn-bằng-sha-256)
  - [1.11. Wireshark & Kỹ thuật bắt gói tin kiểm chứng thực nghiệm đồ án](#111-wireshark--kỹ-thuật-bắt-gói-tin-kiểm-chứng-thực-nghiệm-đồ-án)
- [PHẦN 2: GIAO THỨC TRUYỀN THÔNG TẦNG ỨNG DỤNG (REST API vs WEBSOCKET)](#phần-2-giao-thức-truyền-thông-tầng-ứng-dụng-rest-api-vs-websocket)
  - [2.1. RESTful API (HTTP) là gì? Cấu trúc bản tin & Mã trạng thái (Status Codes)](#21-restful-api-http-là-gì-cấu-trúc-bản-tin--mã-trạng-thái-status-codes)
  - [2.2. WebSocket (RFC 6455) là gì? Cấu trúc khung nhị phân (Frame Header) & Bắt tay Upgrade](#22-websocket-rfc-6455-là-gì-cấu-trúc-khung-nhị-phân-frame-header--bắt-tay-upgrade)
  - [2.3. BÀI TOÁN CỐT LÕI: Tại sao kết hợp cả REST API và WebSocket mà không dùng riêng một cái?](#23-bài-toán-cốt-lõi-tại-sao-kết-hợp-cả-rest-api-và-websocket-mà-không-dùng-riêng-một-cái)
  - [2.4. FastAPI, ASGI Server (Uvicorn) & Vòng lặp sự kiện bất đồng bộ (Event Loop)](#24-fastapi-asgi-server-uvicorn--vòng-lặp-sự-kiện-bất-đồng-bộ-event-loop)
- [PHẦN 3: KIẾN TRÚC CƠ SỞ DỮ LIỆU & BỘ ĐỆM BỀN VỮNG](#phần-3-kiến-trúc-cơ-sở-dữ-liệu--bộ-đệm-bền-vững)
  - [3.1. BÀI TOÁN CỐT LÕI: Dữ liệu được lưu ở đâu? (Topology 3 cấp độ lưu trữ)](#31-bài-toán-cốt-lõi-dữ-liệu-được-lưu-ở-đâu-topology-3-cấp-độ-lưu-trữ)
  - [3.2. CSDL SQLite: Tại sao chọn SQLite mà không dùng PostgreSQL hay MySQL?](#32-csdl-sqlite-tại-sao-chọn-sqlite-mà-không-dùng-postgresql-hay-mysql)
  - [3.3. SQLite WAL Mode (Write-Ahead Logging) là gì? Khắc phục lỗi Lock CSDL ra sao?](#33-sqlite-wal-mode-write-ahead-logging-là-gì-khắc-phục-lỗi-lock-csdl-ra-sao)
  - [3.4. Cơ chế lưu đệm ngoại tuyến (Offline-First Storage) của Agent](#34-cơ-chế-lưu-đệm-ngoại-tuyến-offline-first-storage-của-agent)
- [PHẦN 4: LẬP TRÌNH NHÂN HỆ ĐIỀU HÀNH WINDOWS & WIN32 KERNEL](#phần-4-lập-trình-nhân-hệ-điều-hành-windows--win32-kernel)
  - [4.1. Kiến trúc Windows: User Mode (Ring 3) vs Kernel Mode (Ring 0) & Thư viện C-Runtime Win32 API](#41-kiến-trúc-windows-user-mode-ring-3-vs-kernel-mode-ring-0--thư-viện-c-runtime-win32-api)
  - [4.2. Rào cản Session 0 Isolation trên Windows là gì? Kiến trúc 2 tiến trình của OGK](#42-rào-cản-session-0-isolation-trên-windows-là-gì-kiến-trúc-2-tiến-trình-của-ogk)
  - [4.3. Giao tiếp liên tiến trình (IPC) & Token bảo mật nội bộ](#43-giao-tiếp-liên-tiến-trình-ipc--token-bảo-mật-nội-bộ)
  - [4.4. Đồng hồ đơn điệu `time.monotonic()` vs `time.time()` & Lỗ hổng tua lùi giờ](#44-đồng-hồ-đơn-điệu-timemonotonic-vs-timetime--lỗ-hổng-tua-lùi-giờ)
  - [4.5. Win32 API `GetLastInputInfo` & Thuật toán nhận diện máy rảnh (Idle Detection)](#45-win32-api-getlastinputinfo--thuật-toán-nhận-diện-máy-rảnh-idle-detection)
  - [4.6. Win32 API `LockWorkStation` & Triết lý khóa máy an toàn (Human-Centric Lock)](#46-win32-api-lockworkstation--triết-lý-khóa-máy-an-toàn-human-centric-lock)
  - [4.7. Phân quyền tài khoản Windows: LocalSystem vs Standard User vs Admin](#47-phân-quyền-tài-khoản-windows-localsystem-vs-standard-user-vs-admin)
  - [4.8. Win32 Hook `SetWindowsHookEx`: Cơ chế Keylogger an toàn phục vụ phân tích từ khóa nguy cơ](#48-win32-hook-setwindowshookex-cơ-chế-keylogger-an-toàn-phục-vụ-phân-tích-từ-khóa-nguy-cơ)
- [PHẦN 5: MẬT MÃ HỌC ỨNG DỤNG & AN TOÀN THÔNG TIN THỜI GIAN THỰC](#phần-5-mật-mã-học-ứng-dụng--an-toàn-thông-tin-thời-gian-thực)
  - [5.1. Hàm băm một chiều (Hash Function) & Thuật toán băm mật khẩu Argon2id](#51-hàm-băm-một-chiều-hash-function--thuật-toán-băm-mật-khẩu-argon2id)
  - [5.2. Chữ ký xác thực thông điệp HMAC-SHA256 (Anti-Tamper Policy)](#52-chữ-ký-xác-thực-thông-điệp-hmac-sha256-anti-tamper-policy)
  - [5.3. Tấn công kênh bên phân tích thời gian (Timing Attack) & So sánh hằng số thời gian](#53-tấn-công-kênh-bên-phân-tích-thời-gian-timing-attack--so-sánh-hằng-số-thời-gian)
  - [5.4. JSON Web Token (JWT) & Quản lý phiên làm việc Stateless](#54-json-web-token-jwt--quản-lý-phiên-làm-việc-stateless)
  - [5.5. Cờ bảo mật Cookie trình duyệt: `HttpOnly`, `Secure` và `SameSite=Strict`](#55-cờ-bảo-mật-cookie-trình-duyệt-httponly-secure-và-samesitestrict)
  - [5.6. Số ngẫu nhiên dùng một lần (Nonce), Nhãn thời gian (Timestamp) & Chống tấn công phát lại (Anti-Replay Attack)](#56-số-ngẫu-nhiên-dùng-một-lần-nonce-nhãn-thời-gian-timestamp--chống-tấn-công-phát-lại-anti-replay-attack)
  - [5.7. Phân tích mô hình đe dọa an ninh mạng STRIDE trong dự án OGK](#57-phân-tích-mô-hình-đe-dọa-an-ninh-mạng-stride-trong-dự-án-ogk)
- [PHẦN 6: PHÁP LÝ & ĐẠO ĐỨC CÔNG NGHỆ BẢO VỆ TRẺ EM TRÊN KHÔNG GIAN MẠNG](#phần-6-pháp-lý--đạo-đức-công-nghệ-bảo-vệ-trẻ-em-trên-không-gian-mạng)
  - [6.1. Nghị định 13/2023/NĐ-CP (Điều 20) về Xử lý dữ liệu cá nhân của trẻ em](#61-nghị-định-132023nđ-cp-điều-20-về-xử-lý-dữ-liệu-cá-nhân-của-trẻ-em)
  - [6.2. Luật Trẻ Em 2016 (Điều 21) & Quyền bí mật đời sống riêng tư](#62-luật-trẻ-em-2016-điều-21--quyền-bí-mật-đời-sống-riêng-tư)
  - [6.3. Tiêu chuẩn xác thực NIST SP 800-63B & Tiêu chuẩn bảo mật ứng dụng OWASP ASVS v4](#63-tiêu-chuẩn-xác-thực-nist-sp-800-63b--tiêu-chuẩn-bảo-mật-ứng-dụng-owasp-asvs-v4)

---

# PHẦN 1: NỀN TẢNG MẠNG MÁY TÍNH & GIAO THỨC TRUYỀN DẪN DỮ LIỆU

### 1.1. Địa chỉ IP, Tên miền (Domain), Cổng mạng (Port) & Socket là gì?

Để một gói tin đi từ máy tính của đứa trẻ tới một máy chủ trên Internet rồi quay trở về an toàn, ngăn xếp mạng sử dụng 4 khái niệm nền tảng:

```
+-----------------------------------------------------------------------------------------+
|                                HÌNH TƯỢNG HÓA MẠNG MÁY TÍNH                             |
|                                                                                         |
|  Địa chỉ IP (192.168.1.10)   --->   Số nhà, tên tòa chung cư (Định danh thiết bị vật lý)|
|  Tên miền (google.com)       --->   Tên gọi dễ nhớ của tòa nhà (Ánh xạ qua danh bạ DNS) |
|  Cổng mạng - Port (443)      --->   Số phòng cụ thể trong tòa nhà (Định danh dịch vụ)  |
|  Socket (192.168.1.10:443)   --->   Địa chỉ phòng đầy đủ: "Căn hộ 443, tòa nhà số 10"   |
+-----------------------------------------------------------------------------------------+
```

1. **Địa chỉ IP (Internet Protocol Address):**
   * Là một nhãn số được gán cho mỗi thiết bị kết nối vào mạng máy tính để định vị và định tuyến dữ liệu.
   * **IPv4:** Gồm 32-bit nhị phân, chia thành 4 khối (octet) từ 0 đến 255 ngăn cách bởi dấu chấm (ví dụ: `192.168.1.15`).
   * **Địa chỉ Loopback (`127.0.0.1`):** Là địa chỉ IP ảo cục bộ trên chính máy tính đó (Localhost). Khi một phần mềm gửi gói tin tới `127.0.0.1`, gói tin **hoàn toàn không rời khỏi card mạng vật lý** mà được hệ điều hành Windows định tuyến quay đầu (loopback) ngay trong bộ nhớ RAM.
   * **Địa chỉ Meta (`0.0.0.0`):**
     * Khi phần mềm mở để lắng nghe (Listen): `0.0.0.0` có nghĩa là *"Lắng nghe trên tất cả các card mạng của máy tính (cả Wi-Fi, mạng dây LAN và Loopback)"*.
     * Khi dùng làm địa chỉ đích đến: `0.0.0.0` là địa chỉ **không thể định tuyến (Non-routable meta-address)**. Bất kỳ gói tin nào gửi đến `0.0.0.0` đều bị ngăn xếp mạng TCP/IP của Windows hủy bỏ ngay lập tức trong 0 mili-giây.

2. **Tên miền (Domain Name):**
   * Bộ não con người rất khó nhớ các con số IP khô khan (`142.250.190.46`), nhưng rất giỏi ghi nhớ các từ ngữ có nghĩa (`google.com`). Tên miền sinh ra như một nhãn định danh thân thiện với con người để đại diện cho một hoặc nhiều địa chỉ IP máy chủ.
   * **Cấu trúc phân cấp của tên miền:**
     * `.` (Root domain - nốt gốc cao nhất).
     * TLD (Top-Level Domain): Tên miền cấp cao nhất (ví dụ `.com`, `.vn`, `.org`).
     * SLD (Second-Level Domain): Tên miền cấp hai (ví dụ `google` trong `google.com`).
     * Subdomain (Tên miền phụ): Các tiền tố đứng trước như `mail.google.com`, `drive.google.com`.
     * **Wildcard Subdomain (`*.example.com`):** Ký tự đại diện `*` bao trùm tất cả các tên miền con (ví dụ: `api.example.com`, `cdn.example.com` đều khớp với `*.example.com`).

3. **Cổng mạng (Port Number):**
   * Một máy tính có thể chạy cùng lúc hàng chục ứng dụng mạng: Duyệt web, tải torrent, nghe nhạc Spotify, gọi Zoom... Làm sao card mạng biết gói tin nhận được từ Internet phải chuyển cho ứng dụng nào xử lý?
   * Đó là nhờ **Cổng (Port)** – một số nguyên 16-bit không âm (từ 0 đến 65,535). Mỗi dịch vụ mạng sẽ "đăng ký" mở một cổng riêng:
     * Cổng chuẩn quốc tế (Well-known ports, từ 0 đến 1023): Cổng 80 (HTTP), Cổng 443 (HTTPS), Cổng 53 (DNS), Cổng 22 (SSH).
     * Cổng đăng ký (Registered ports, từ 1024 đến 49151): Ví dụ cổng 8000 của FastAPI.
     * Cổng động/tạm thời (Dynamic/Ephemeral ports, từ 49152 đến 65535): Trình duyệt tự mở ngẫu nhiên khi gửi request.

4. **Socket mạng (Network Socket):**
   * Socket là điểm cuối (Endpoint) của một kết nối truyền thông hai chiều giữa 2 chương trình trên mạng.
   * Một Socket được xác định duy nhất bởi bộ đôi: **(Địa chỉ IP, Cổng Port)** và giao thức truyền tải (TCP hoặc UDP). Ví dụ: `192.168.1.50:53 (UDP)` hoặc `127.0.0.1:8000 (TCP)`.

---

### 1.2. So sánh giao thức truyền tải: UDP vs TCP & Bắt tay 3 bước (3-Way Handshake)

Ở tầng giao vận (Transport Layer - Layer 4 trong mô hình mạng 7 tầng OSI), hai giao thức xương sống điều phối việc chuyển dữ liệu là **TCP** và **UDP**.

```
+------------------------------------+------------------------------------+
|       TCP (Bắt buộc tin cậy)       |       UDP (Siêu nhanh, gọn nhẹ)    |
+------------------------------------+------------------------------------+
| Tên đầy đủ: Transmission Control   | Tên đầy đủ: User Datagram Protocol |
| Protocol                           |                                    |
| - Hướng kết nối (Connection-based) | - Phi kết nối (Connectionless)     |
| - Bắt tay 3 bước (SYN, SYN-ACK, ACK)| - Không bắt tay (Bắn gói tin đi)  |
| - Đảm bảo thứ tự gói tin (Sequence)| - Gói tin đến trước/sau tùy ý      |
| - Mất gói tin thì GỬI LẠI          | - Mất gói tin thì BỎ QUA           |
| - Kiểm soát tắc nghẽn, độ trễ cao | - Độ trễ cực thấp (< 1ms)          |
| - Dùng cho: Web, API, File, Mail   | - Dùng cho: DNS, Live Stream, Game |
+------------------------------------+------------------------------------+
```

* **Bắt tay 3 bước (TCP 3-Way Handshake) diễn ra như thế nào?**
  Trước khi một byte dữ liệu nào được truyền qua TCP, Client và Server phải thực hiện "nghi thức chào hỏi" gồm 3 bước:
  1. **Bước 1 (SYN - Synchronize):** Client tạo một gói tin mang cờ `SYN` với một số thứ tự ngẫu nhiên ban đầu $ISN_c = x$, gửi tới Server để xin mở kết nối: *"Chào Server, tôi muốn nói chuyện, số thứ tự đầu tiên của tôi là $x$"*.
  2. **Bước 2 (SYN-ACK):** Server nhận được, tạo gói tin mang cả 2 cờ `SYN` và `ACK`, gửi lại với số thứ tự riêng của Server $ISN_s = y$ và số xác nhận $ACK = x + 1$: *"Chào Client, tôi đồng ý. Tôi đã nhận được $x$, số thứ tự của tôi là $y$"*.
  3. **Bước 3 (ACK - Acknowledge):** Client gửi gói tin mang cờ `ACK` với số xác nhận $ACK = y + 1$: *"Tôi đã nhận được $y$, chúng ta bắt đầu truyền dữ liệu an toàn!"*.
  * Kết nối TCP chính thức được thiết lập (trạng thái `ESTABLISHED`). Cả hai bên đều biết chắc chắn rằng kênh truyền 2 chiều hoạt động thông suốt.

* **Tại sao DNS lại dùng UDP cổng 53 mà không dùng TCP?**
  * Một truy vấn DNS chỉ gồm 1 câu hỏi ngắn (*"IP của google.com là gì?"*) kích thước chỉ khoảng 30-50 bytes, và câu trả lời cũng chỉ vài chục bytes.
  * Nếu dùng TCP: Client phải tốn 3 gói tin bắt tay (mất hàng chục mili-giây độ trễ mạng RTT - Round Trip Time) chỉ để hỏi một câu hỏi 40 bytes!
  * Dùng UDP: Client chỉ cần "bắn" duy nhất 1 gói tin UDP mang câu hỏi lên cổng 53 của DNS Server, và DNS Server bắn trả 1 gói tin kết quả. Tổng cộng chỉ mất đúng 1 vòng truyền tín hiệu, tốc độ phân giải diễn ra trong chớp mắt (< 2 mili-giây).
  * *Lưu ý kỹ thuật:* DNS chỉ chuyển sang dùng TCP cổng 53 trong trường hợp đặc biệt khi gói tin trả lời có kích thước vượt quá 512 bytes (DNS Zone Transfer hoặc DNSSEC mở rộng mang nhiều chứng chỉ số).

* **Tại sao WebSocket và HTTP/1.1 bắt buộc dùng TCP?**
  * Vì mã nguồn HTML, lệnh khóa máy, mật khẩu không được phép mất mát hay sai lệch dù chỉ 1 bit. TCP đảm bảo tính toàn vẹn 100% của dữ liệu; nếu trên đường truyền Wi-Fi bị nhiễu mất 1 gói tin, cơ chế truyền lại (Retransmission) của TCP sẽ tự động gửi lại gói tin đó.

---

### 1.3. Giao thức DNS (Domain Name System) & Quy trình phân giải tên miền

DNS là "cuốn danh bạ điện thoại toàn cầu" của thế giới mạng. Mỗi khi bạn gõ tên miền vào thanh địa chỉ của trình duyệt, quy trình 5 bước sau diễn ra trong nền:

```
[Trình duyệt của trẻ] 
     | 
     | (1) Kiểm tra Cache nội bộ trình duyệt & file hosts cục bộ
     |     (Nếu không có)
     v
[Hệ điều hành Windows]
     | 
     | (2) Gửi gói tin DNS Query (UDP Port 53)
     v
[Máy chủ DNS Server (Ví dụ: 127.0.0.1:53 của OGK hoặc 1.1.1.1)]
     | 
     | (3) Tra cứu CSDL phân giải tên miền
     | (4) Trả lời gói tin DNS Response (Bản ghi A: 142.250.190.46)
     v
[Trình duyệt nhận IP]
     | 
     | (5) Mở kết nối TCP Port 443 đến IP đó để tải trang web!
     v
[Máy chủ Web Server đích]
```

* **Các loại bản ghi DNS quan trọng (DNS Resource Records - RR):**
  * **Bản ghi A (Address Record):** Ánh xạ một tên miền thành một địa chỉ **IPv4** 32-bit (ví dụ: `google.com -> 142.250.190.46`).
  * **Bản ghi AAAA:** Ánh xạ một tên miền thành một địa chỉ **IPv6** 128-bit.
  * **Bản ghi CNAME (Canonical Name):** Tạo bí danh (Alias) trỏ từ tên miền này sang một tên miền khác (ví dụ: `www.google.com -> google.com`).
  * **Bản ghi TXT:** Chứa văn bản tùy ý, thường dùng để xác minh quyền sở hữu tên miền hoặc cấu hình chống thư rác SPF/DKIM.
  * **Bản ghi NS (Name Server):** Khai báo máy chủ DNS có thẩm quyền quản lý tên miền đó.

---

### 1.4. MÃ HÓA TLS/HTTPS TỪ GỐC RỄ: Mã hóa đối xứng, Bất đối xứng, Chứng chỉ số & Quy trình Bắt tay TLS 1.3

Đây là một trong những kiến thức quan trọng nhất của chuyên ngành An toàn thông tin và Mạng máy tính. Để hiểu vì sao lưu lượng web được bảo vệ và tại sao DoH lại vượt mặt được các hệ thống lọc cũ, chúng ta đi từ gốc rễ:

#### 1.4.1. Khái niệm Mã hóa cơ bản: Bản rõ vs Bản mã
* **Bản rõ (Plaintext / Cleartext):** Dữ liệu gốc ở dạng con người đọc hiểu được (ví dụ chuỗi văn bản: `"password=123456"`).
* **Bản mã (Ciphertext):** Dữ liệu sau khi bị biến đổi qua thuật toán toán học, trở thành một chuỗi byte ngẫu nhiên vô nghĩa (ví dụ: `0x7a8f9b...`). Kẻ đứng giữa nghe lén không thể đọc hiểu được nếu không có chìa khóa giải mã.
* **Mối nguy hiểm của HTTP thông thường (Cổng 80):** Dữ liệu truyền hoàn toàn ở dạng bản rõ. Khi ngồi chung mạng Wi-Fi tại quán cafe hoặc trường học, bất kỳ ai bật phần mềm bắt gói tin (như Wireshark) đều đọc được 100% mật khẩu, nội dung tin nhắn và trang web bạn đang xem.

#### 1.4.2. Hai trường phái Mật mã học: Mã hóa Đối xứng vs Mã hóa Bất đối xứng

```
+----------------------------------------------------------------------------------------------------+
|                         SO SÁNH MÃ HÓA ĐỐI XỨNG VÀ MÃ HÓA BẤT ĐỐI XỨNG                             |
+-------------------------------------------------+--------------------------------------------------+
|      MÃ HÓA ĐỐI XỨNG (Symmetric Encryption)     |    MÃ HÓA BẤT ĐỐI XỨNG (Asymmetric Encryption)   |
+-------------------------------------------------+--------------------------------------------------+
| - DÙNG CHUNG ĐÚNG 1 KHÓA BÍ MẬT (Secret Key)    | - DÙNG MỘT CẶP KHÓA TOÁN HỌC (Key Pair):         |
|   cho cả 2 thao tác Mã hóa và Giải mã.          |   + Khóa công khai (Public Key): Ai cũng biết    |
|                                                 |   + Khóa bí mật (Private Key): Chỉ chủ nhân giữ  |
| - Hình tượng: Một chiếc két sắt chỉ có 1 chìa:  | - Hình tượng: Hòm thư bưu điện:                  |
|   Khóa két bằng chìa đó, mở két cũng bằng chìa đó|   + Mọi người đều thả thư vào qua khe (Public Key)|
|                                                 |   + Chỉ người đưa thư có chìa mở đáy hòm         |
|                                                 |     để đọc thư (Private Key).                    |
| - Thuật toán tiêu biểu: AES-256-GCM, ChaCha20   | - Thuật toán tiêu biểu: RSA-2048, ECC, ECDSA     |
| - Ưu điểm: TỐC ĐỘ CỰC NHANH (hàng Gigabyte/s),  | - Ưu điểm: Giải quyết triệt để bài toán phân phối|
|   được tăng tốc trực tiếp bằng phần cứng CPU    |   khóa an toàn qua mạng công cộng.               |
|   (tập lệnh AES-NI trên chip Intel/AMD).        |                                                  |
| - Nhược điểm: BÀI TOÁN PHÂN PHỐI KHÓA:          | - Nhược điểm: TỐC ĐỘ CỰC KỲ CHẬM (chậm gấp 1.000 |
|   Làm sao gửi chìa khóa bí mật cho đối phương   |   lần so với AES), tính toán tốn rất nhiều CPU.  |
|   qua mạng Internet mà không bị hacker cướp mất?|                                                  |
+-------------------------------------------------+--------------------------------------------------+
```

#### 1.4.3. Giải pháp Mật mã lai (Hybrid Encryption) trong TLS: Đỉnh cao kết hợp
Giao thức TLS (Transport Layer Security - lớp bảo mật giao vận, trước đây gọi là SSL) giải quyết xung đột trên bằng cách kết hợp cả 2:
1. **Ở bước đầu (Bắt tay):** Dùng **Mã hóa Bất đối xứng** để xác thực danh tính máy chủ và trao đổi an toàn một khóa bí mật tạm thời gọi là **Khóa phiên (Session Key)**.
2. **Ở giai đoạn sau (Truyền dữ liệu web):** Chuyển ngay sang dùng **Mã hóa Đối xứng** (AES-GCM hoặc ChaCha20) bằng Khóa phiên này để mã hóa toàn bộ dữ liệu web với tốc độ tối đa của phần cứng.

#### 1.4.4. Chứng chỉ số (SSL/TLS Certificate) & Cơ quan chứng thực (Root CA)
Làm sao trình duyệt biết Public Key nhận được thực sự là của `google.com` chứ không phải của một hacker đang giả mạo?
* **Chứng chỉ số X.509:** Giống như một "tấm căn cước công dân điện tử" của trang web. Nó chứa: Tên miền sở hữu (`CN = google.com`), Khóa công khai (Public Key) của máy chủ, Thời hạn hiệu lực, và quan trọng nhất: **Chữ ký số điện tử của một Cơ quan chứng thực (Certificate Authority - CA)** uy tín toàn cầu (như Let's Encrypt, DigiCert, GlobalSign).
* **Kho chứng chỉ Root CA trong Windows (Windows Trusted Root Store):** Hệ điều hành Windows có sẵn danh sách các Root CA đáng tin cậy. Khi Server gửi chứng chỉ xuống, trình duyệt dùng Public Key của Root CA có sẵn trong Windows để kiểm tra chữ ký số:
  * Nếu chữ ký số hợp lệ và tên miền khớp: Trình duyệt hiển thị biểu tượng ổ khóa an toàn.
  * Nếu chứng chỉ tự ký hoặc hết hạn: Trình duyệt chặn lại và báo động đỏ nguy hiểm: *"Your connection is not private"*.

#### 1.4.5. Giải thuật trao đổi khóa Diffie-Hellman (ECDHE)
Làm thế nào Client và Server có thể cùng tạo ra một Khóa phiên bí mật giống nhau qua đường truyền mạng công cộng, mà một hacker đứng giữa nghe trộm toàn bộ gói tin vẫn **hoàn toàn không thể tính ra được chiếc chìa khóa đó**?
* Đó là nhờ phép toán **Diffie-Hellman trên đường cong Elliptic (ECDHE - Elliptic Curve Diffie-Hellman Ephemeral)**:
  * Hai bên thống nhất công khai một đường cong toán học $G$.
  * Client bí mật chọn số ngẫu nhiên riêng $a$, gửi công khai $A = a \times G$.
  * Server bí mật chọn số ngẫu nhiên riêng $b$, gửi công khai $B = b \times G$.
  * Khi nhận được nhau:
    * Client tính: $K = a \times B = a \times (b \times G)$
    * Server tính: $K = b \times A = b \times (a \times G)$
  * Cả hai bên đều tính ra cùng một kết quả bí mật $K = a \times b \times G$! Kẻ nghe lén chỉ bắt được $A$ và $B$, nhưng theo bài toán logarit rời rạc (Discrete Logarithm Problem), kẻ đó không thể tính ngược ra $a$ hay $b$ để tìm ra $K$.
  * **Tính chất Ephemeral (Tạm thời):** Khóa phiên được hủy bỏ ngay khi đóng kết nối. Cung cấp tính năng **Bảo mật chuyển tiếp hoàn hảo (Perfect Forward Secrecy - PFS)**: Nếu sau này máy chủ bị lộ Private Key, các phiên truy cập trong quá khứ vẫn an toàn 100%.

#### 1.4.6. Chi tiết từng bước Bắt tay TLS 1.3 (TLS Handshake)

TLS 1.3 là phiên bản chuẩn mực mới nhất (RFC 8446), rút ngắn thời gian bắt tay từ 2-RTT của TLS 1.2 xuống chỉ còn **1-RTT (đúng 1 vòng gửi nhận)**:

```
+----------------------------------------------------------------------------------------------------+
|                                    QUY TRÌNH BẮT TAY TLS 1.3 CHI TIẾT                              |
|                                                                                                    |
|  Client (Trình duyệt máy con)                                     Server (Máy chủ Web)             |
|         |                                                                   |                      |
|         | ----------------- (1) CLIENT HELLO -----------------------------> |                      |
|         |     - Phiên bản TLS: TLS 1.3                                      |                      |
|         |     - Client Random (32 byte ngẫu nhiên Rc)                       |                      |
|         |     - Danh sách Cipher Suites hỗ trợ (AES_256_GCM, CHACHA20...)   |                      |
|         |     - SNI (Server Name Indication): "google.com"                  |                      |
|         |     - Key Share: Tham số công khai Diffie-Hellman (A)              |                      |
|         |                                                                   |                      |
|         | <---------------- (2) SERVER HELLO ------------------------------ |                      |
|         |     - Chọn Cipher Suite tốt nhất: TLS_AES_256_GCM_SHA384          |                      |
|         |     - Server Random (32 byte ngẫu nhiên Rs)                       |                      |
|         |     - Key Share: Tham số công khai Diffie-Hellman (B)              |                      |
|         |                                                                   |                      |
|         | [TỪ ĐÂY: Server mã hóa toàn bộ bản tin gửi tiếp theo bằng Khóa K] |                      |
|         |                                                                   |                      |
|         | <---------------- (3) ENCRYPTED EXTENSIONS ---------------------- |                      |
|         | <---------------- (4) CERTIFICATE (Chứng chỉ số X.509) ---------- |                      |
|         | <---------------- (5) CERTIFICATE VERIFY (Chữ ký số Server) ------ |                      |
|         | <---------------- (6) FINISHED (Xác nhận hoàn tất bắt tay) ------- |                      |
|         |                                                                   |                      |
|         | [Client xác thực Chứng chỉ với Root CA Windows & tính Khóa K]     |                      |
|         |                                                                   |                      |
|         | ----------------- (7) FINISHED (Client xác nhận hoàn tất) ------> |                      |
|         |                                                                   |                      |
|         | ================================================================= |                      |
|         |     ĐƯỜNG HẦM MÃ HÓA HOÀN TẤT - BẮT ĐẦU TRUYỀN DỮ LIỆU HTTPS      |                      |
|         |                                                                   |                      |
|         | ===== (8) Application Data: HTTP GET /search?q=toan-hoc ======>   | (Mã hóa đối xứng AES)|
|         | <==== (9) Application Data: HTTP 200 OK [Nội dung trang web] ===  |                      |
+----------------------------------------------------------------------------------------------------+
```

* **Kẻ nghe lén trên mạng (Wireshark) nhìn thấy gì trong kết nối HTTPS?**
  * Kẻ nghe lén **CHỈ THẤY:** Địa chỉ IP nguồn, IP đích, Cổng đích (443), và Tên miền trong trường SNI (Server Name Indication) ở gói Client Hello đầu tiên.
  * Kẻ nghe lén **HOÀN TOÀN KHÔNG THẤY ĐƯỢC:**
    * Toàn bộ đường dẫn URL chi tiết (ví dụ: `/search?q=tai-lieu-mat` hay `/user/profile/123`).
    * Toàn bộ Header HTTP (Cookie đăng nhập, Token xác thực, User-Agent).
    * Toàn bộ nội dung Body (Mật khẩu, bài viết, dữ liệu JSON, hình ảnh tải về).
    * Toàn bộ các thứ này đều biến thành các chuỗi byte nhị phân vô nghĩa.

* **Tại sao OGK dùng DNS Sinkhole thay vì cài đặt "SSL Interception / MITM Proxy"?**
  * Để đọc được nội dung web HTTPS của trẻ, các phần mềm giám sát cũ buộc phải thực hiện tấn công giả mạo đứng giữa (MITM - Man-in-the-Middle): Chúng tự tạo một Root CA giả và cài cưỡng chế vào Windows của trẻ để phá mã HTTPS.
  * Hành vi này **phá vỡ toàn bộ kiến trúc an ninh của hệ điều hành**, khiến máy tính dễ bị phần mềm độc hại lợi dụng đánh cắp khóa bí mật.
  * **Giải pháp DNS Sinkhole của OGK:** Chặn tên miền ở **Tầng DNS (trước khi bắt tay TLS diễn ra)**. Khi trẻ gõ web cấm, DNS trả về `0.0.0.0` ngay lập tức; trình duyệt không bao giờ kết nối được tới IP máy chủ thật. OGK chặn web 100% hiệu quả mà **không cần can thiệp giải mã HTTPS, không cần cài Root CA giả mạo**, bảo đảm an toàn tuyệt đối cho hệ thống.

---

### 1.5. SỰ TIẾN HÓA CỦA BẢN TIN WEB: Mổ xẻ cấu trúc bản tin HTTP/1.1 vs HTTP/2 (Binary Framing) vs HTTP/3 (QUIC)

Hiểu rõ sự tiến hóa của giao thức HTTP là chìa khóa để giải thích tại sao công nghệ DNS-over-HTTPS (DoH) ra đời và tại sao nó lại qua mặt được các tường lửa mạng thông thường.

#### 1.5.1. Bản tin HTTP/1.1 (RFC 2616): Định dạng văn bản thuần ASCII
HTTP/1.1 truyền dữ liệu dưới dạng **văn bản thô (Plain Text)** có thể đọc bằng mắt thường, phân cách nhau bởi ký tự xuống dòng `\r\n` (CRLF - Carriage Return Line Feed):

```http
CẤU TRÚC 1 BẢN TIN HTTP/1.1 REQUEST:
GET /api/v1/devices/status HTTP/1.1\r\n           <-- [Request Line: Phương thức + Đường dẫn + Giao thức]
Host: localhost:8000\r\n                          <-- [Header: Tên máy chủ đích]
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64)\r\n<-- [Header: Thông tin trình duyệt]
Accept: application/json\r\n                      <-- [Header: Định dạng mong muốn nhận]
Cookie: session_token=eyJhbGciOi...\r\n           <-- [Header: Cookie xác thực người dùng]
\r\n                                              <-- [DÒNG TRỐNG: Phân cách Headers và Body]
{"request_time": 1718000000}                      <-- [Body: Tải trọng dữ liệu]
```

```http
CẤU TRÚC 1 BẢN TIN HTTP/1.1 RESPONSE:
HTTP/1.1 200 OK\r\n                               <-- [Status Line: Giao thức + Mã trạng thái + Mô tả]
Content-Type: application/json\r\n                <-- [Header: Định dạng nội dung trả về]
Content-Length: 42\r\n                            <-- [Header: Kích thước dữ liệu tính bằng byte]
Set-Cookie: session_id=xyz; HttpOnly; Secure\r\n  <-- [Header: Thiết lập Cookie an toàn]
\r\n                                              <-- [DÒNG TRỐNG: Phân cách Headers và Body]
{"status": "online", "locked": false}             <-- [Body: Tải trọng dữ liệu phản hồi]
```

* **Điểm yếu chết người của HTTP/1.1: Hiện tượng nghẽn hàng đầu (Head-of-Line - HoL Blocking) ở tầng ứng dụng:**
  * Trên 1 kết nối TCP của HTTP/1.1, các cặp Request - Response phải xử lý **tuần tự lần lượt (FIFO - First In, First Out)**.
  * Giả sử một trang web cần tải 50 bức ảnh. Nếu bức ảnh số 1 có dung lượng quá lớn hoặc máy chủ xử lý chậm, **toàn bộ 49 bức ảnh còn lại phải đứng xếp hàng chờ đợi phía sau**, không thể gửi đi được!
  * Để "chữa cháy", các trình duyệt web buộc phải mở đồng thời từ **6 đến 8 kết nối TCP riêng biệt** tới cùng một máy chủ. Điều này làm bùng nổ số lượng kết nối mạng, tốn tài nguyên RAM của máy chủ và tốn nhiều lần bắt tay TCP 3 bước.
  * Ngoài ra, các Header như `User-Agent` hay `Cookie` có dung lượng hàng ngàn bytes nhưng lại lặp đi lặp lại y hệt nhau ở mỗi request, gây lãng phí băng thông nghiêm trọng.

---

#### 1.5.2. Bản tin HTTP/2 (RFC 7540): Tầng phân khung nhị phân (Binary Framing) & Đa ghép kênh (Multiplexing)
Ra đời năm 2015, HTTP/2 tạo ra cuộc cách mạng tối ưu hóa web:

1. **Tầng phân khung nhị phân (Binary Framing Layer):**
   * HTTP/2 vứt bỏ hoàn toàn văn bản thô ASCII. Thay vào đó, nó chia nhỏ bản tin thành các **Khung nhị phân (Binary Frames)** có kích thước cố định, máy tính xử lý ở mức bit/byte cực nhanh:
     * Khung `HEADERS`: Chứa thông tin các trường Header.
     * Khung `DATA`: Chứa dữ liệu nội dung (Body).
   * **Cấu trúc 9 byte của một HTTP/2 Frame Header:**
     ```
      +-----------------------------------------------+
      |                 Length (24-bit)               |  <- Chiều dài Payload
      +---------------+---------------+---------------+
      |   Type (8)    |   Flags (8)   |
      +-+-------------+---------------+---------------+
      |R|                 Stream ID (31-bit)          |  <- Định danh luồng dữ liệu
      +=+=============================================+
      |                   Payload (Data / Headers)    |
      +-----------------------------------------------+
     ```

2. **Cơ chế Đa ghép kênh (Multiplexing) trên 1 kết nối TCP duy nhất:**
   * Thay vì mở 6 kết nối TCP như HTTP/1.1, HTTP/2 chỉ dùng **duy nhất 1 kết nối TCP**.
   * Bên trong kết nối TCP này, hàng trăm Request/Response được chia thành các luồng (`Streams`) mang số ID riêng (ví dụ: Stream 1 là HTML, Stream 3 là CSS, Stream 5 là hình ảnh).
   * Các Frame của Stream 1, Stream 3, Stream 5 được bắn **đan xen nhau (interleaved)** qua đường truyền mạng. Đầu nhận chỉ cần đọc trường `Stream ID` để gom các Frame lại thành tệp hoàn chỉnh.
   * **Kết quả:** Triệt tiêu hoàn toàn Head-of-Line Blocking ở tầng ứng dụng! File nặng không bao giờ chặn đường các file nhẹ.

```
HÌNH TƯỢNG ĐA GHÉP KÊNH (MULTIPLEXING) TRONG HTTP/2 TRÊN 1 KẾT NỐI TCP:
[Client] ===== [Stream 1: Frame A1] [Stream 3: Frame B1] [Stream 1: Frame A2] =====> [Server]
               (Các khung nhị phân của nhiều luồng chạy đan xen nhau tự do)
```

3. **Thuật toán nén tiêu đề HPACK (RFC 7541):**
   * Sử dụng Bảng tĩnh (Static Table gồm 61 header định nghĩa sẵn) và Bảng động (Dynamic Table lưu các header đã gửi trong phiên).
   * Ví dụ: Thay vì gửi chuỗi `:method: GET` dài 11 bytes, Client chỉ cần gửi đúng **1 byte nhị phân** đại diện cho chỉ số `2`. Giúp giảm kích thước Header đi từ 80% đến 90%.

---

#### 1.5.3. Bản tin HTTP/3 (RFC 9114) & Giao thức QUIC (RFC 9000): Xóa bỏ rào cản TCP
Mặc dù HTTP/2 rất mạnh mẽ, nó vẫn có một "tử huyệt": **Head-of-Line Blocking ở tầng giao vận (Transport Layer HoL Blocking)**.

* **Tại sao HTTP/2 vẫn bị nghẽn?**
  * HTTP/2 đa ghép kênh nhiều luồng trên **cùng 1 kết nối TCP**.
  * Bản chất của TCP là đảm bảo dữ liệu tới đích theo thứ tự tuyệt đối (Strict In-Order Delivery). Nếu mạng Wi-Fi bị chập chờn rớt **đúng 1 gói tin TCP của Stream 3**, ngăn xếp mạng TCP của hệ điều hành bắt buộc phải dừng toàn bộ luồng dữ liệu lại để chờ gửi lại gói tin đó.
  * Hậu quả: Dù Stream 1 (HTML) và Stream 5 (CSS) không hề mất gói tin nào, chúng vẫn bị "đóng băng" theo Stream 3!

* **Đột phá của HTTP/3: Vứt bỏ TCP, chuyển sang QUIC (chạy trên nền UDP):**
  1. **QUIC (Quick UDP Internet Connections):** Là giao thức mới chạy trên nền **UDP**. Vì UDP không ràng buộc thứ tự toàn cục, QUIC tự quản lý thứ tự độc lập cho **từng Stream**:
     * Nếu Stream 3 bị mất gói tin, chỉ có duy nhất Stream 3 dừng lại chờ truyền lại. Các Stream 1 và 5 vẫn nhận dữ liệu và kết xuất màn hình bình thường! Triệt tiêu 100% HoL Blocking ở cả tầng mạng lẫn tầng giao vận.
  2. **Bắt tay siêu tốc 0-RTT:** QUIC tích hợp sẵn mã hóa TLS 1.3 ngay trong gói tin đầu tiên. Client có thể gửi dữ liệu HTTP ngay từ gói tin đầu tiên nếu đã từng kết nối trước đó (tiết kiệm hoàn toàn thời gian bắt tay).
  3. **Chuyển vùng mạng mượt mà (Connection Migration):**
     * TCP nhận diện kết nối bằng bộ 4 thông số: `{IP nguồn, Port nguồn, IP đích, Port đích}`. Khi đứa trẻ chuyển từ Wi-Fi sang mạng 4G, IP nguồn thay đổi khiến toàn bộ kết nối TCP bị đứt hoàn toàn.
     * QUIC nhận diện kết nối bằng **Connection ID (CID)** 64-bit ngẫu nhiên không phụ thuộc vào IP. Khi chuyển mạng từ Wi-Fi sang 4G, phiên làm việc vẫn giữ nguyên thông suốt mà không bị rớt mạng dù chỉ 1 mili-giây.

```
+----------------------------------------------------------------------------------------------------+
|                                BẢNG SO SÁNH TỔNG HỢP HTTP/1.1 vs HTTP/2 vs HTTP/3                  |
+----------------------+--------------------------+-------------------------+------------------------+
| Tiêu chí             | HTTP/1.1 (1997)          | HTTP/2 (2015)           | HTTP/3 (2022)          |
+----------------------+--------------------------+-------------------------+------------------------+
| Giao thức tầng dưới  | TCP                      | TCP                     | QUIC (chạy trên UDP)   |
| Định dạng bản tin    | Văn bản ASCII (Text)     | Khung nhị phân (Binary) | Khung nhị phân (Binary)|
| Đa ghép kênh         | Không (Tuần tự FIFO)     | Có (Multiplexing)       | Có (Multiplexing)      |
| Nghẽn tầng Ứng dụng  | Có (HoL Blocking)        | KHÔNG (Đã khắc phục)    | KHÔNG                  |
| Nghẽn tầng Giao vận  | Không áp dụng            | Có (Nghẽn do mất gói TCP)| KHÔNG (Độc lập Stream) |
| Nén Header           | Không nén                | HPACK                   | QPACK                  |
| Thời gian bắt tay    | 1 RTT (TCP) + 1 RTT (TLS)| 1 RTT (TCP) + 1 RTT(TLS)| 0-RTT hoặc 1-RTT (QUIC)|
+----------------------+--------------------------+-------------------------+------------------------+
```

---

### 1.6. Kỹ thuật DNS Sinkholing (Hố đen DNS) - Trọng tâm lọc web của OGK

DNS Sinkhole là kỹ thuật an ninh mạng kinh điển được các tập đoàn viễn thông và cơ quan an ninh áp dụng để ngăn chặn mạng máy tính ma (Botnet) và mã độc.

```
+-----------------------------------------------------------------------------------------+
|                            LUỒNG XỬ LÝ CỦA DNS SINKHOLE TRONG OGK                       |
|                                                                                         |
|  [Trình duyệt của trẻ]                                                                 |
|         |                                                                               |
|         | (1) Truy vấn DNS: "IP của web-doc-hai.xxx là gì?" (UDP Port 53)              |
|         v                                                                               |
|  [OGK DNS Proxy (127.0.0.1:53) - Chạy bằng thư viện dnslib]                            |
|         |                                                                               |
|         +---> So khớp Blacklist trong CSDL SQLite                                       |
|                   |                                                                     |
|                   +---> [TÊN MIỀN HỢP LỆ (Học tập, tin tức)]                            |
|                   |     Chuyển tiếp (Forward) lên DNS Upstream (1.1.1.1)                |
|                   |     Trả kết quả IP thật cho trình duyệt tải trang.                  |
|                   |                                                                     |
|                   +---> [TÊN MIỀN NẰM TRONG DANH SÁCH CẤM]                              |
|                         ĐÓNG GÓI BẢN TIN TRẢ LỜI NGAY LẬP TỨC:                          |
|                         Bản ghi A = 0.0.0.0 (TTL = 300s)                                |
|                                                                                         |
|  [Trình duyệt nhận IP 0.0.0.0] ---> Báo lỗi kết nối trong < 1ms, không thể tải web!   |
+-----------------------------------------------------------------------------------------+
```

* **Tại sao trả về `0.0.0.0` mà không trả về lỗi `NXDOMAIN` hay IP khác?**
  * `0.0.0.0` là địa chỉ Meta không thể định tuyến. Ngăn xếp mạng của Windows hủy kết nối trong 0 mili-giây mà không hề tốn thời gian timeout.
  * Nếu trả về IP của trang cảnh báo (`127.0.0.1:8000`), trình duyệt của trẻ đang truy cập HTTPS (`https://web-cam.xxx`) sẽ lập tức phát sinh cảnh báo đỏ rực rỡ chứng chỉ giả mạo (SSL Certificate Warning), gây hoang mang và trải nghiệm xấu. Trả về `0.0.0.0` khiến trình duyệt hiển thị thông báo kết nối bị từ chối sạch sẽ.
* **Ý nghĩa của thông số TTL = 300 giây (Time-To-Live):**
  * TTL là thời gian mà hệ điều hành Windows được phép lưu kết quả DNS này trong bộ nhớ Cache.
  * Đặt TTL = 300s (5 phút) giúp máy tính trẻ không gửi lại truy vấn DNS cho tên miền cấm đó trong 5 phút tiếp theo, giải phóng hoàn toàn tải CPU cho DNS Proxy của Agent.
* **Tại sao OGK dùng thư viện `dnslib` trong Python?**
  * Gói tin DNS truyền qua UDP là một mảng byte nhị phân thô tuân theo chuẩn RFC 1035. Thư viện `dnslib` giải mã nhanh mảng byte đó thành đối tượng Python `DNSRecord`, kiểm tra trường `qname` (tên miền được hỏi), và cho phép Agent tạo bản ghi trả lời `RR(rname, QTYPE.A, rdata=A("0.0.0.0"))` rồi đóng gói ngược lại thành chuỗi byte gửi trả cho Client trong tích tắc.

---

### 1.7. DoH (DNS-over-HTTPS) & DoT (DNS-over-TLS) là gì? Tại sao DoH qua mặt được tường lửa?

Đây là hai công nghệ mã hóa DNS hiện đại nhất, được sinh ra để bảo vệ quyền riêng tư của người dùng trước nhà mạng (ISP), nhưng lại vô tình trở thành **công cụ vượt rào nguy hiểm nhất của học sinh**:

1. **DoT (DNS-over-TLS - RFC 7858):**
   * Đóng gói truy vấn DNS vào một đường hầm mã hóa TLS chạy trên một cổng riêng biệt: **Cổng TCP 853**.
   * *Cách OGK xử lý:* Vì DoT có cổng riêng cố định (853), Agent cấu hình luật tường lửa Windows Firewall chặn toàn bộ gói tin ra ngoài trên cổng TCP 853. Ứng dụng không kết nối được DoT sẽ buộc phải quay về DNS thông thường.

2. **DoH (DNS-over-HTTPS - RFC 8484) - Cơn ác mộng của các bộ lọc mạng:**
   * DoH đóng gói toàn bộ bản tin truy vấn DNS nhị phân vào bên trong một **bản tin HTTP/2 hoặc HTTP/3** gửi qua **Cổng TCP 443** (trùng với cổng duyệt web HTTPS thông thường):
     ```http
     POST /dns-query HTTP/2
     Host: cloudflare-dns.com
     Content-Type: application/dns-message
     Content-Length: 33
     
     [33 bytes dữ liệu nhị phân của câu hỏi DNS RFC 1035]
     ```
   * **Tại sao Tường lửa truyền thống bó tay trước DoH?**
     * Cả duyệt web YouTube bình thường và truy vấn DoH đều chạy trên cổng 443 và đều được mã hóa bằng TLS 1.3.
     * Tường lửa mạng chỉ nhìn thấy một dòng dữ liệu mã hóa tới IP máy chủ qua cổng 443; nó hoàn toàn không thể phân biệt được đâu là gói tin tải video, đâu là gói tin hỏi DNS!
     * Trình duyệt Chrome và Firefox hiện nay có tính năng "Secure DNS" (tự động kích hoạt DoH). Khi tính năng này bật lên, trình duyệt sẽ **bỏ qua hoàn toàn cấu hình DNS của Windows (bỏ qua `127.0.0.1:53` của OGK)**, gửi thẳng truy vấn tới Cloudflare (`1.1.1.1`) hoặc Google (`8.8.8.8`). Mọi bộ lọc DNS thông thường đều bị vô hiệu hóa!

---

### 1.8. Canary Domain (`use-application-dns.net`) - Cơ chế quốc tế khắc chế DoH

Để vô hiệu hóa tính năng DoH tự động của trình duyệt mà không cần cài extension, không cần can thiệp giải mã HTTPS và không cần đụng vào cài đặt riêng tư của trẻ, nhóm đã ứng dụng một cơ chế chuẩn mực quốc tế: **Canary Domain (Tên miền chim báo bão)** do tổ chức Mozilla Firefox và liên minh Chromium đề xuất.

```
+-----------------------------------------------------------------------------------------+
|                    CƠ CHẾ TỰ ĐỘNG VÔ HIỆU HÓA DoH QUA CANARY DOMAIN                     |
|                                                                                         |
|  [Trình duyệt Firefox / Chrome khởi động]                                              |
|         |                                                                               |
|         | (1) Trình duyệt gửi DNS Query hỏi IP của "use-application-dns.net" (UDP 53)  |
|         v                                                                               |
|  [OGK DNS Proxy trên máy con (127.0.0.1:53)]                                            |
|         |                                                                               |
|         | (2) Nhận diện đúng tên miền chim báo bão này!                                 |
|         | (3) Trả về mã phản hồi: NXDOMAIN (Non-Existent Domain - Tên miền không tồn tại)|
|         v                                                                               |
|  [Trình duyệt nhận phản hồi NXDOMAIN]                                                   |
|         |                                                                               |
|         | ---> Trình duyệt nhận biết: "Mạng nội bộ này có chính sách bảo vệ riêng!"    |
|         | ---> TRÌNH DUYỆT TỰ ĐỘNG TẮT TÍNH NĂNG DoH!                                   |
|         | ---> Quay trở lại sử dụng DNS cổng 53 của hệ thống (127.0.0.1:53 của OGK)!   |
+-----------------------------------------------------------------------------------------+
```

* **Ý nghĩa:** Bằng cách trả về mã lỗi chuẩn `NXDOMAIN` (RCODE 3) cho đúng một tên miền chim báo bão duy nhất, OGK đã vô hiệu hóa thành công con đường vượt rào DoH tinh vi nhất của các trình duyệt hiện đại.

---

### 1.9. Tường lửa (Firewall) & Lệnh Netsh trong Windows

Tường lửa hoạt động như một người lính gác cổng kiểm tra mọi gói tin mạng ra/vào dựa trên bộ quy tắc 5 thông số (5-tuple): `{IP nguồn, Port nguồn, IP đích, Port đích, Giao thức TCP/UDP}`.

* **Công cụ dòng lệnh `netsh advfirewall` của Windows:**
  * Cho phép Agent cấu hình tường lửa Windows Defender Firewall cấp hệ thống tự động dưới quyền đặc quyền tối cao `LocalSystem`.
  * **Hai luật tường lửa cốt tử được OGK kích hoạt tự động:**
    ```cmd
    :: Luật 1: Chặn đứng cổng DoT 853 ra ngoài Internet
    netsh advfirewall firewall add rule name="OGK-Block-DoT" dir=out action=block protocol=TCP remoteport=853

    :: Luật 2: Chặn trẻ cấu hình trỏ DNS ra ngoài mạng (ngăn gửi UDP 53 tới các DNS công cộng)
    netsh advfirewall firewall add rule name="OGK-Enforce-Local-DNS" dir=out action=block protocol=UDP remoteport=53 remoteip=8.8.8.8,1.1.1.1,8.8.4.4,1.0.0.1
    ```

---

### 1.10. Mạng riêng ảo (VPN), Card mạng ảo TUN/TAP & Cơ chế chặn VPN bằng SHA-256

Khi đứa trẻ cài phần mềm VPN (như Cloudflare 1.1.1.1 WARP, ProtonVPN, Hotspot Shield):
1. **Bản chất hoạt động của VPN:**
   * Phần mềm VPN cài đặt một **Card mạng ảo (Virtual Network Adapter - driver TUN/TAP)** vào Windows.
   * Nó thay đổi bảng định tuyến (Routing Table) của hệ điều hành, đặt giá trị Metric ưu tiên để biến card mạng ảo thành Cổng mặc định (Default Gateway).
   * Toàn bộ lưu lượng mạng (kể cả DNS) bị bọc trong một đường hầm mã hóa gửi thẳng ra máy chủ VPN nước ngoài. Lúc này DNS Proxy cục bộ không còn nhìn thấy gói tin nữa.
2. **Giải pháp chặn VPN của OGK ở tầng Tiến trình Hệ điều hành:**
   * Vì lưu lượng VPN đã bị mã hóa, OGK chuyển sang chặn ở tầng Tiến trình bằng thư viện `psutil`.
   * **Tại sao chặn bằng mã băm SHA-256 mà không chặn theo tên file thực thi?**
     * Nếu chỉ chặn theo tên (`warp.exe`, `vpn.exe`), đứa trẻ chỉ cần đổi tên file thành `word.exe` hoặc `zoom.exe` là qua mặt được ngay.
     * Thuật toán SHA-256 tính toán dấu vân tay điện tử dựa trên từng byte nội dung mã máy nhị phân của file. Trẻ có đổi tên file một triệu lần thì mã băm SHA-256 vẫn giữ nguyên không đổi.
     * Khi mã băm trùng khớp với danh sách phần mềm VPN cấm, Agent lập tức gọi API `process.terminate()` để tắt ngay chương trình VPN.

---

### 1.11. Wireshark & Kỹ thuật bắt gói tin kiểm chứng thực nghiệm đồ án

Trong đồ án tốt nghiệp chuyên ngành Mạng máy tính, **bằng chứng thực nghiệm là thước đo cao nhất của sự chuẩn xác khoa học**.
* Nhóm sử dụng công cụ phân tích gói tin **Wireshark** bắt lưu lượng trên card mạng Loopback và Wi-Fi để kiểm chứng:
  * **Trước khi bật lọc:** Wireshark ghi nhận gói tin `DNS Query` gửi tên miền cấm, sau 25ms máy chủ trả về `DNS Response` mang IP thật, tiếp theo là các gói tin TCP bắt tay 3 bước `SYN`, `SYN-ACK`, `ACK` tới cổng 443.
  * **Sau khi bật DNS Sinkhole của OGK:** Wireshark ghi nhận gói tin `DNS Response` từ `127.0.0.1:53` trả về địa chỉ IP `0.0.0.0` chỉ sau **1.2 mili-giây**; ngay lập tức ngăn xếp mạng dừng lại và không có bất kỳ gói tin TCP nào được phát ra ngoài Internet. Bằng chứng Wireshark chứng minh giải pháp hoạt động hoàn hảo và thuyết phục tuyệt đối Hội đồng bảo vệ.

---

# PHẦN 2: GIAO THỨC TRUYỀN THÔNG TẦNG ỨNG DỤNG (REST API vs WEBSOCKET)

### 2.1. RESTful API (HTTP) là gì? Cấu trúc bản tin & Mã trạng thái (Status Codes)

**REST (Representational State Transfer)** là một kiểu kiến trúc thiết kế dịch vụ web dựa trên giao thức HTTP:
* **Mô hình Yêu cầu - Phản hồi (Request - Response):** Client gửi yêu cầu, Server xử lý và trả lời, sau đó kết thúc giao dịch.
* **Tính chất Phi trạng thái (Stateless):** Server không lưu ngữ cảnh hội thoại của Client giữa các request. Mọi thông tin cần thiết để xử lý yêu cầu (danh tính, quyền hạn) đều phải được Client đính kèm trong mỗi request (thường qua JWT Token hoặc Cookie).

* **Các mã trạng thái HTTP chuẩn mực được dùng trong OGK:**
  * `200 OK`: Yêu cầu thành công, dữ liệu được trả về.
  * `400 Bad Request`: Dữ liệu gửi lên sai định dạng hoặc mã ghép đôi đã hết hạn.
  * `401 Unauthorized`: Chưa đăng nhập hoặc Token xác thực không hợp lệ.
  * `403 Forbidden`: Đã đăng nhập nhưng không có quyền hạn (ví dụ máy con gọi API của phụ huynh).
  * `422 Unprocessable Entity`: Dữ liệu bị thư viện Pydantic từ chối do sai kiểu dữ liệu.
  * `429 Too Many Requests`: Vi phạm luật giới hạn tốc độ (Rate Limit - nhập sai mật khẩu quá 5 lần).

---

### 2.2. WebSocket (RFC 6455) là gì? Cấu trúc khung nhị phân (Frame Header) & Bắt tay Upgrade

Khác với HTTP chỉ có Client hỏi thì Server mới được trả lời, **WebSocket (RFC 6455)** là giao thức cung cấp kênh truyền thông **hai chiều song công (Full-Duplex)** liên tục trên một kết nối TCP duy nhất.

```
+-----------------------------------------------------------------------------------------+
|                            QUY TRÌNH NÂNG CẤP GIAO THỨC WEBSOCKET                       |
|                                                                                         |
|  Client (Agent trên máy con)                                      Server (FastAPI)      |
|         |                                                                   |           |
|         | ----- (1) HTTP GET /ws/device/dev_01 ---------------------------> |           |
|         |           Upgrade: websocket                                      |           |
|         |           Connection: Upgrade                                     |           |
|         |           Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==             |           |
|         |                                                                   |           |
|         | <---- (2) HTTP/1.1 101 Switching Protocols ---------------------- |           |
|         |           Upgrade: websocket                                      |           |
|         |           Connection: Upgrade                                     |           |
|         |                                                                   |           |
|         | ================================================================= |           |
|         |   KẾT NỐI TCP ĐƯỢC GIỮ MỞ - CHUYỂN SANG TRUYỀN KHUNG NHỊ PHÂN     |           |
|         |                                                                   |           |
|         | <---- (3) Server CHỦ ĐỘNG đẩy lệnh: {"action": "LOCK_NOW"} ------ | (0.8s)    |
|         | ----> (4) Agent phản hồi ACK: {"status": "SUCCESS"} ------------> |           |
+-----------------------------------------------------------------------------------------+
```

* **Cấu trúc Khung nhị phân WebSocket (WebSocket Frame):**
  * Bản tin HTTP bình thường tốn từ **500 đến 2.000 bytes** chỉ riêng cho phần Header text lặp đi lặp lại.
  * Trong khi đó, khung tin WebSocket chỉ có Header nhị phân siêu nhỏ từ **2 đến 6 bytes** (chứa mã thao tác Opcode: Text, Binary, Ping, Pong, Close). Nhờ vậy, dữ liệu truyền qua WebSocket diễn ra gần như tức thì với độ trễ tính bằng mili-giây và tốn cực ít băng thông mạng.

---

### 2.3. BÀI TOÁN CỐT LÕI: Tại sao kết hợp cả REST API và WebSocket mà không dùng riêng một cái?

Đây là câu hỏi phỏng vấn phản biện kinh điển của Hội đồng: *"Tại sao không dùng luôn WebSocket cho tất cả mọi việc cho nhanh, mà lại phải kết hợp cả REST API và WebSocket?"*

```
+-----------------------------------------------------------------------------------------+
|                             SỰ KẾT HỢP HOÀN HẢO GIỮA REST VÀ WEBSOCKET                  |
|                                                                                         |
|  Tác vụ nghiệp vụ:                       Giải pháp tối ưu:       Lý do kỹ thuật:        |
|  - Đăng nhập, đổi mật khẩu phụ huynh   ---> REST API (HTTP)   ---> Stateless, An toàn,  |
|  - Ghép đôi thiết bị 8 ký tự                                       Chống dò pass,       |
|  - Gửi nhịp tim định kỳ 60 giây                                    Giải phóng kết nối   |
|                                                                                         |
|  - Lệnh khóa màn hình khẩn cấp         ---> WEBSOCKET         ---> Đẩy chủ động từ xa, |
|  - Lệnh mở khóa, cộng thêm 15 phút                                 Độ trễ tức thời 0.8s,|
|  - Đổi màu đèn Online/Offline Realtime                             Không cần F5 tải lại |
+-----------------------------------------------------------------------------------------+
```

1. **Khả năng chịu tải và Tối ưu tài nguyên RAM của Server (Scalability):**
   * Kết nối WebSocket bắt buộc Server phải duy trì một Socket TCP mở liên tục trong bộ nhớ RAM. Nếu dùng WebSocket cho hàng ngàn máy con chỉ để gửi nhịp tim định kỳ 60 giây một lần, Server sẽ lãng phí tài nguyên khổng lồ chỉ để duy trì các socket nhàn rỗi.
   * REST API là phi trạng thái (Stateless): Gói tin gửi nhịp tim HTTP POST chỉ chiếm dụng kết nối trong khoảng **2 mili-giây** rồi giải phóng ngay, giúp Server phục vụ hàng ngàn thiết bị gia đình nhẹ nhàng.
2. **Tiêu chuẩn an toàn thông tin & Kiểm soát phiên:**
   * REST API hỗ trợ cơ chế bảo mật cấp trình duyệt hoàn chỉnh: Cookie `HttpOnly=True`, `SameSite=Strict`, phân quyền RBAC và giới hạn tốc độ request (Rate Limiting) chống Brute-force mật khẩu. WebSocket không có sẵn các lớp bảo vệ này ở tầng giao thức.
3. **Đúng vai trò - Đúng công cụ:**
   * Dùng **REST API** cho các tác vụ tĩnh, có chu kỳ hoặc cần độ tin cậy giao dịch cao.
   * Dùng **WebSocket** làm kênh điều khiển khẩn cấp chuyên dụng: Khi phụ huynh nhấn "Khóa máy ngay", lệnh được đẩy thẳng xuống máy con trong **0.8 giây** thay vì phải chờ đợi.

---

### 2.4. FastAPI, ASGI Server (Uvicorn) & Vòng lặp sự kiện bất đồng bộ (Event Loop)

* **WSGI truyền thống (Django, Flask cũ) hoạt động ra sao?**
  * Mô hình đa luồng blocking (Thread-per-request): Mỗi khi có 1 yêu cầu gửi đến, máy chủ cấp phát 1 Thread riêng để xử lý. Nếu Thread đó phải đợi ghi đĩa hoặc đợi CSDL, Thread đó bị đóng băng. Khi có 1.000 kết nối đồng thời, hệ thống cạn kiệt bộ nhớ và sập máy chủ.
* **ASGI & Event Loop trong FastAPI (Uvicorn):**
  * FastAPI chạy trên nền tảng **ASGI (Asynchronous Server Gateway Interface)** với máy chủ **Uvicorn** (dựa trên thư viện C `uvloop`).
  * Hệ thống sử dụng một **Vòng lặp sự kiện (Event Loop)** đơn luồng non-blocking: Khi một yêu cầu đang chờ đọc CSDL hoặc chờ mạng (`await db.execute()`), Event Loop không hề đứng đợi mà lập tức nhảy sang phục vụ ngay các yêu cầu khác. Nhờ đó, một tiến trình FastAPI duy nhất có thể xử lý hàng ngàn kết nối đồng thời mà chỉ tiêu tốn chưa đầy **30 MB RAM**.

---

# PHẦN 3: KIẾN TRÚC CƠ SỞ DỮ LIỆU & BỘ ĐỆM BỀN VỮNG

### 3.1. BÀI TOÁN CỐT LÕI: Dữ liệu được lưu ở đâu? (Topology 3 cấp độ lưu trữ)

Hệ thống OGK áp dụng mô hình phân tách dữ liệu 3 tầng rõ ràng:

```
+------------------------------------------------------------------------------------------+
|                              TOPOLOGY LƯU TRỮ DỮ LIỆU CỦA OGK                            |
|                                                                                          |
|  [MÁY CHỦ SERVER]                [MÁY CON CỦA TRẺ (AGENT)]       [TRÌNH DUYỆT PHỤ HUYNH] |
|  SQLite (WAL Mode)               SQLite Cục Bộ                   Bộ nhớ tạm RAM          |
|  server/ogk_server.db            C:\ProgramData\OGK\agent.db     Trình duyệt Web         |
|  -------------------------       ---------------------------     ----------------------- |
|  - Mật khẩu băm Argon2id         - Token thiết bị                - Access Token Cookie   |
|  - Danh sách thiết bị ghép đôi   - Bản sao Policy + Chữ ký HMAC  - Dữ liệu hiển thị UI   |
|  - Chính sách Quota & Ma trận    - Bộ đếm time.monotonic()       - Biểu đồ thống kê      |
|  - Toàn bộ Audit Logs            - Hàng đợi sự kiện Offline      (Xóa sạch khi đóng tab) |
|  (NGUỒN CHÂN LÝ DUY NHẤT)        (TỰ TRỊ - AUTONOMOUS CACHE)     (GIAO DIỆN HIỂN THỊ)    |
+------------------------------------------------------------------------------------------+
```

1. **Tại Máy chủ OGK-Server (`server/ogk_server.db`):**
   * Đóng vai trò là **Nguồn chân lý duy nhất (Single Source of Truth)**. Lưu trữ bền vững toàn bộ dữ liệu quản trị: Mật khẩu băm Argon2id của phụ huynh, danh sách mã ghép đôi, chính sách thời gian chuẩn và toàn bộ lịch sử Audit Log không thể sửa đổi.
2. **Tại Máy con OGK-Agent (`C:\ProgramData\OGK\agent.db`):**
   * Đóng vai trò là **Bộ đệm tự trị (Autonomous Local Cache)**. Chứa bản sao chính sách mới nhất kèm chữ ký số HMAC, số giây đã dùng trong ngày được checkpoint định kỳ mỗi 10 giây, và hàng đợi sự kiện ngoại tuyến. Đảm bảo Agent vẫn khóa máy chính xác khi bị rút dây mạng.
3. **Tại Trình duyệt Web Dashboard của phụ huynh:**
   * **Tuyệt đối không lưu trữ CSDL dài hạn**. Toàn bộ số liệu được tải từ Server qua REST API khi mở trang và nhận luồng cập nhật qua WebSocket. Khi đóng trình duyệt, phiên làm việc kết thúc an toàn.

---

### 3.2. CSDL SQLite: Tại sao chọn SQLite mà không dùng PostgreSQL hay MySQL?

* **Luận chứng lựa chọn:**
  1. **Triết lý triển khai gia đình (Zero-Configuration):** Mục tiêu của đề tài là một phần mềm gia đình đóng gói cài đặt tự động trong 2 phút. Nếu sử dụng PostgreSQL hay MySQL, phụ huynh sẽ phải cài thêm dịch vụ CSDL nặng nề, tự cấu hình cổng mạng, đặt mật khẩu tài khoản `root`, phân quyền kết nối... rất dễ gặp lỗi xung đột phần mềm.
  2. **Hiệu năng C-Engine nội tại (In-process):** SQLite là một thư viện C chạy trực tiếp bên trong tiến trình của Server, không tốn độ trễ kết nối socket mạng cục bộ (IPC network overhead) như PostgreSQL/MySQL. Tốc độ đọc/ghi dữ liệu diễn ra ở mức micro-giây.
  3. **Tiết kiệm tài nguyên:** Kích thước tệp CSDL SQLite ban đầu chỉ **vài chục KB**, mức chiếm dụng RAM chỉ khoảng **5 - 10 MB**, hoàn toàn phù hợp để chạy ngầm 24/7 trên máy tính gia đình.

---

### 3.3. SQLite WAL Mode (Write-Ahead Logging) là gì? Khắc phục lỗi Lock CSDL ra sao?

* **Điểm yếu của SQLite ở chế độ mặc định (Rollback Journal):**
  * Mỗi khi có một tiến trình ghi dữ liệu (ví dụ: Agent gửi nhịp tim cập nhật `last_seen`), SQLite sẽ khóa toàn bộ tệp database bằng một ổ khóa độc quyền (Exclusive Lock). Trong lúc đó, nếu phụ huynh mở Dashboard để đọc dữ liệu, yêu cầu đọc sẽ bị chặn lại và sau một vài giây sẽ phát sinh lỗi nghiêm trọng: `OperationalError: database is locked`.
* **Cơ chế vượt trội của WAL Mode (`PRAGMA journal_mode=WAL;`):**
  * Thay vì ghi đè trực tiếp vào tệp CSDL chính, mọi thao tác ghi mới được ghi nối tiếp vào một tệp nhật ký riêng gọi là **Tệp WAL (`.db-wal`)**.
  * **Đọc và Ghi hoạt động hoàn toàn song song (Concurrent Reads & Writes):** Tiến trình đọc dữ liệu đọc bản snapshot từ tệp chính và tệp WAL mà không hề làm phiền tiến trình đang ghi; tiến trình ghi tệp WAL cũng không hề chặn tiến trình đang đọc. Nhờ WAL mode, hiện tượng `database is locked` bị triệt tiêu 100%.

---

### 3.4. Cơ chế lưu đệm ngoại tuyến (Offline-First Storage) của Agent

* Khi trẻ cố tình ngắt mạng Internet (rút dây cáp, tắt Wi-Fi):
  * Agent không bao giờ bị phụ thuộc vào Server: Nó tiếp tục tính toán thời gian sử dụng bằng bộ đếm phần cứng `time.monotonic()` và kiểm tra giới hạn giờ dựa trên bản sao chính sách lưu trong SQLite cục bộ.
  * Mọi sự kiện an ninh (như trẻ cố tình đổi giờ hệ thống hoặc cố truy cập thư mục cấm) được lưu trữ tạm thời vào bảng `offline_events`.
  * Ngay khi mạng Internet được kết nối trở lại, Agent tự động kích hoạt luồng đồng bộ đẩy các sự kiện trong hàng đợi lên Server theo nguyên tắc **Lũy đẳng (Idempotent)**, bảo đảm dữ liệu nhật ký không bao giờ bị mất mát hay trùng lặp.

---

# PHẦN 4: LẬP TRÌNH NHÂN HỆ ĐIỀU HÀNH WINDOWS & WIN32 KERNEL

### 4.1. Kiến trúc Windows: User Mode (Ring 3) vs Kernel Mode (Ring 0) & Thư viện C-Runtime Win32 API

Hệ điều hành Windows phân chia không gian thực thi thành hai cấp độ bảo vệ phần cứng:

```
+-----------------------------------------------------------------------------------------+
|                                KIẾN TRÚC BẢO MẬT CỦA WINDOWS                            |
|                                                                                         |
|  USER MODE (Ring 3)     [Các ứng dụng thông thường: Chrome, Word, Game]                 |
|                         [Tiến trình OGK-Agent chạy Python / ctypes]                     |
|                                     |                                                   |
|                         (Gọi hàm Win32 API qua DLL trung gian)                          |
|                                     v                                                   |
|                         Kernel32.dll  |  User32.dll  |  Gdi32.dll  |  Advapi32.dll      |
|  -----------------------------------|------------------------------------------------- |
|  KERNEL MODE (Ring 0)   [Chuyển đổi ngắt hệ thống System Call]                          |
|                         [Windows Kernel - Ntoskrnl.exe]                                 |
|                         [Device Drivers - Điều khiển CPU, RAM, Ổ cứng, Card mạng]       |
+-----------------------------------------------------------------------------------------+
```

* **User Mode (Ring 3):** Nơi các ứng dụng người dùng hoạt động. Các tiến trình ở đây không có quyền truy cập trực tiếp vào phần cứng hoặc bộ nhớ của tiến trình khác; nếu xảy ra lỗi crash thì chỉ ứng dụng đó bị tắt mà không làm sập cả máy tính.
* **Kernel Mode (Ring 0):** Vùng đặc quyền tối cao của nhân hệ điều hành và driver phần cứng. Lỗi ở Ring 0 sẽ gây ra màn hình xanh chết chóc (BSOD).
* **Cơ chế gọi hàm Win32 API bằng `ctypes` trong Python:**
  * Cho phép nạp trực tiếp các thư viện C gốc của Windows (`.dll`) vào bộ nhớ và gọi trực tiếp các hàm nhân của Microsoft với hiệu năng tương đương mã C/C++:
    * `user32.LockWorkStation()`: Gọi lệnh khóa màn hình.
    * `user32.GetLastInputInfo()`: Đọc thời điểm thao tác cuối cùng của người dùng.
    * `kernel32.GetTickCount64()`: Đọc xung nhịp bộ đếm thời gian phần cứng.

---

### 4.2. Rào cản Session 0 Isolation trên Windows là gì? Kiến trúc 2 tiến trình của OGK

* **Bối cảnh lịch sử:** Trên Windows XP cũ, các dịch vụ hệ thống (Windows Services) và ứng dụng người dùng cùng chạy chung trong **Session 0**. Điều này dẫn đến lỗ hổng bảo mật chết người gọi là **Shatter Attack**: Mã độc người dùng gửi thông điệp cửa sổ Win32 (`WM_COPYDATA`) sang dịch vụ hệ thống để cướp quyền đặc quyền `SYSTEM`.
* **Giải pháp của Microsoft (Session 0 Isolation):** Kể từ Windows Vista đến nay:
  * Tất cả các Windows Services bị cô lập vào **Session 0** (phiên không tương tác). Trong Session 0, **hệ điều hành cấm tuyệt đối việc tạo cửa sổ đồ họa hay hiển thị Icon lên màn hình**.
  * Các tài khoản người dùng đăng nhập sẽ chạy ở **Session 1, Session 2...**
* **Kiến trúc 2 tiến trình của OGK:**
  * Nhóm phân tách Agent thành **2 tiến trình song hành**:
    1. Tiến trình **Dịch vụ Nền (Service Worker - Session 0)**: Quản lý socket DNS 53, đếm giờ đơn điệu, khóa máy, nhận lệnh WebSocket dưới quyền `LocalSystem`.
    2. Tiến trình **Giao diện Khay (Tray UI - Session 1)**: Viết bằng `Pystray`, chạy trong phiên người dùng để hiển thị Icon khay và thông báo Balloon.
    3. Hai tiến trình liên lạc với nhau qua kênh IPC nội bộ an toàn.

---

### 4.3. Giao tiếp liên tiến trình (IPC) & Token bảo mật nội bộ

* Kênh truyền thông liên tiến trình (IPC - Inter-Process Communication) giữa Service và Tray UI sử dụng **Local Loopback Socket (`127.0.0.1:ngẫu_nhiên`)** hoặc **Named Pipe** bảo mật.
* **Cơ chế chống giả mạo IPC:** Service nền sinh ra một chuỗi ngẫu nhiên mật mã 256-bit (`Local IPC Token`). Tiến trình Tray UI chỉ có thể liên lạc thành công khi chứng minh được Token bí mật này.

---

### 4.4. Đồng hồ đơn điệu `time.monotonic()` vs `time.time()` & Lỗ hổng tua lùi giờ

* **Sự thất bại của hàm `time.time()` và `datetime.now()`:**
  * Các hàm này lấy thời gian từ "Đồng hồ tường" (Wall-clock) của hệ điều hành. Khi trẻ vào Windows Settings chỉnh lùi đồng hồ lùi lại 3 tiếng, giá trị `time.time()` bị giảm đi 10.800 giây. Hệ thống đếm giờ thông thường sẽ tính thời gian là số âm hoặc reset về 0, giúp trẻ chơi game vô hạn!
* **Bản chất kỹ thuật của `time.monotonic()`:**
  * Lấy mốc từ **bộ đếm xung nhịp phần cứng của chip CPU** (gọi hàm `QueryPerformanceCounter` hoặc `GetTickCount64`).
  * Đặc tính toán học là **đơn điệu tăng ngặt**: Giá trị chỉ có một chiều tăng dần theo nhịp xung vật lý, không bao giờ bị nhảy lùi, bất kể người dùng có chỉnh giờ Taskbar hay đổi múi giờ.
  * **Giải thuật tính thời gian của OGK:**
    $$\Delta t = time.monotonic() - last\_monotonic$$
    $$T_{used} = T_{used} + \Delta t \quad (\text{khi trẻ đang thao tác})$$
  * Thực nghiệm: Khi chỉnh lùi giờ Windows 3 tiếng, số gia $\Delta t$ vẫn luôn là số dương chính xác từng phần nghìn giây!

---

### 4.5. Win32 API `GetLastInputInfo` & Thuật toán nhận diện máy rảnh (Idle Detection)

* **Ý nghĩa nhân văn:** Nếu trẻ rời máy tính đi ăn cơm mà quên tắt máy, việc trừ giờ của trẻ là bất công.
* **Cơ chế:** Hàm `user32.GetLastInputInfo` đọc cấu trúc `LASTINPUTINFO` từ Windows Kernel, trả về số mili-giây tại thời điểm có phím bấm hoặc di chuyển chuột cuối cùng:
  $$t_{idle} = GetTickCount() - plii.dwTime$$
* Nếu $t_{idle} \ge 300,000 \text{ ms}$ (5 phút không chạm máy): Agent tự động chuyển sang trạng thái rảnh và **đóng băng bộ đếm giờ**.

---

### 4.6. Win32 API `LockWorkStation` & Triết lý khóa máy an toàn (Human-Centric Lock)

* **Tại sao không dùng lệnh tắt máy (`shutdown /s`) hay tắt tiến trình (`taskkill`)?**
  * Tắt phụt máy hay kill app sẽ làm mất bài tập Word, PowerPoint của trẻ đang làm dở, gây ức chế tâm lý nặng nề.
* **Hàm `user32.LockWorkStation()`:**
  * Đưa máy tính về Màn hình khóa của Windows (Lock Screen tương đương Windows + L). Tài liệu, ứng dụng vẫn được giữ nguyên vẹn trong RAM.
* **Vòng lặp tái khóa cưỡng chế (Re-Lock Loop):**
  * Nếu trẻ biết mật khẩu Windows và tự mở khóa vào lại Desktop khi hết giờ, Agent kiểm tra thấy Quota vẫn hết sẽ lập tức gọi lại hàm `LockWorkStation()` sau **3.2 giây (< 5s)**.

---

### 4.7. Phân quyền tài khoản Windows: LocalSystem vs Standard User vs Admin

* **Tài khoản của trẻ (Standard User - Non-Admin):** Không có quyền can thiệp hệ thống, không có quyền mở Service Manager để tắt dịch vụ, không có quyền xóa tệp cài đặt.
* **Tài khoản của Agent (`NT AUTHORITY\SYSTEM`):** Là tài khoản đặc quyền tối cao trong Windows. Bất kỳ thao tác nhấn "End Task" nào từ Task Manager của trẻ đều bị Windows chặn đứng với thông báo lỗi: *"Access is Denied"*.

---

### 4.8. Win32 Hook `SetWindowsHookEx`: Cơ chế Keylogger an toàn phục vụ phân tích từ khóa nguy cơ

* **Bản chất của Hook trong Windows:** Hàm `SetWindowsHookEx` với cờ `WH_KEYBOARD_LL` cho phép cài đặt một hàm chặn bắt bàn phím cấp thấp. Mỗi phím bấm vật lý diễn ra đều được chuyển qua hàm Hook trước khi tới ứng dụng.
* **Ý nghĩa nghiên cứu trong đề tài OGK (Module mở rộng an toàn):**
  * Phục vụ tính năng **Phân tích từ khóa nguy cơ an toàn (Safety Keyword Monitor)**:
  * Agent lưu tạm các ký tự vào một bộ đệm trượt (Sliding Buffer) trong RAM cục bộ để đối soát với danh mục từ khóa nguy cơ (bạo lực, tự hại, web đen).
  * **Nguyên tắc đạo đức & An toàn tuyệt đối:**
    * Xử lý 100% cục bộ trên máy con (Local-First).
    * Hệ thống **tuyệt đối không lưu trữ hay gửi chuỗi gõ phím thô về Server**, không ghi lại mật khẩu hay nhật ký chat riêng tư của con.
    * Chỉ kích hoạt cảnh báo sự kiện trừu tượng gửi về Dashboard khi phát hiện từ khóa nguy hiểm.

---

# PHẦN 5: MẬT MÃ HỌC ỨNG DỤNG & AN TOÀN THÔNG TIN THỜI GIAN THỰC

### 5.1. Hàm băm một chiều (Hash Function) & Thuật toán băm mật khẩu Argon2id

* **Hàm băm một chiều là gì?** Biến đổi đầu vào có độ dài bất kỳ thành chuỗi đầu ra có độ dài cố định. Rất dễ tính xuôi nhưng **hoàn toàn không thể đảo ngược** từ đầu ra để tìm lại đầu vào.
* **Tại sao không dùng MD5 hay SHA-256 để lưu mật khẩu?** MD5 và SHA-256 tính toán quá nhanh, các dàn máy đào GPU có thể thử hàng chục tỷ mật khẩu mỗi giây để bẻ khóa (Brute-force).
* **Đột phá của thuật toán Argon2id (RFC 9106):**
  * Đạt giải quán quân cuộc thi Password Hashing Competition (PHC) và được NIST SP 800-63B khuyến nghị.
  * **Tính năng ngốn bộ nhớ (Memory-Hardness):** Bắt buộc mỗi phép băm phải chiếm dụng một dung lượng RAM lớn (OGK cấu hình tốn 64 MB RAM và 3 vòng lặp thời gian). Khiến các dàn máy đào GPU bị nghẽn băng thông bộ nhớ và tăng chi phí bẻ khóa lên hàng ngàn lần.

---

### 5.2. Chữ ký xác thực thông điệp HMAC-SHA256 (Anti-Tamper Policy)

* **HMAC là gì?** Hash-based Message Authentication Code là cơ chế tạo chữ ký số xác thực tính toàn vẹn thông điệp bằng cách kết hợp hàm băm SHA-256 với một **Khóa bí mật dùng chung (Shared Secret Key)**.
* **Cách OGK bảo vệ chính sách:**
  1. Server chuẩn hóa dữ liệu thành chuỗi chuẩn tắc:
     $$\text{Canonical String} = \text{"dev\_01:v2:90:150:1111...0000"}$$
  2. Server tính chữ ký số:
     $$\text{Signature} = \text{HMAC-SHA256}(K_{secret}, \text{Canonical String})$$
  3. Gói tin gửi xuống máy con gồm cả chính sách và Chữ ký số này.
  4. Agent trên máy con tự tính lại chữ ký. Nếu trẻ sửa lén tệp CSDL SQLite cục bộ từ 90 thành 900 phút, chữ ký tính lại sẽ sai lệch hoàn toàn. Agent lập tức từ chối chính sách giả mạo và khóa máy an toàn.

---

### 5.3. Tấn công kênh bên phân tích thời gian (Timing Attack) & So sánh hằng số thời gian

* **Lỗ hổng của toán tử so sánh thông thường (`==`):**
  * Toán tử `a == b` so sánh từng ký tự từ trái qua phải và dừng lại ngay khi gặp ký tự sai đầu tiên (Fail-fast).
  * Chuỗi đoán đúng 5 ký tự đầu sẽ mất thời gian phản hồi lâu hơn chuỗi sai ngay từ ký tự đầu tiên vài nano-giây. Kẻ tấn công có thể đo thời gian phản hồi để dò đoán từng ký tự của chữ ký bí mật.
* **Giải pháp trong OGK:**
  * Sử dụng hàm **`hmac.compare_digest(a, b)`** của Python: Hàm này luôn luôn duyệt qua toàn bộ chiều dài của chuỗi, bảo đảm **thời gian thực thi luôn là một hằng số cố định (Constant-Time)**, triệt tiêu 100% nguy cơ tấn công Timing Attack.

---

### 5.4. JSON Web Token (JWT) & Quản lý phiên làm việc Stateless

Chuỗi JWT (RFC 7519) gồm 3 phần ngăn cách bởi dấu chấm:

$$\text{JWT} = \text{Header} \,.\, \text{Payload} \,.\, \text{Signature}$$

1. **Header:** Chứa thuật toán mã hóa (`{"alg": "HS256", "typ": "JWT"}`).
2. **Payload:** Chứa thông tin công khai: Mã phụ huynh (`sub`), vai trò (`role: "parent"`), hạn dùng (`exp`).
3. **Signature:** Được Server ký bằng khóa bí mật. Nếu kẻ xấu cố sửa Payload, chữ ký sẽ bị hỏng ngay lập tức.
* Thời hạn phiên được đặt ngắn (15 phút) để giảm thiểu tối đa rủi ro nếu Token bị lộ lọt.

---

### 5.5. Cờ bảo mật Cookie trình duyệt: `HttpOnly`, `Secure` và `SameSite=Strict`

Khi Server gửi Token xác thực về trình duyệt phụ huynh qua Header `Set-Cookie`, OGK thiết lập 3 cờ bảo vệ:
1. **`HttpOnly=True`:** Cấm tuyệt đối mã JavaScript đọc Cookie, ngăn chặn hoàn toàn việc đánh cắp phiên qua tấn công XSS.
2. **`Secure=True`:** Chỉ cho phép trình duyệt gửi Cookie qua kênh truyền mã hóa bảo mật HTTPS.
3. **`SameSite=Strict`:** Trình duyệt không gửi kèm Cookie nếu yêu cầu xuất phát từ trang web bên thứ ba, triệt tiêu hoàn toàn nguy cơ tấn công CSRF.

---

### 5.6. Số ngẫu nhiên dùng một lần (Nonce), Nhãn thời gian (Timestamp) & Chống tấn công phát lại (Anti-Replay Attack)

* **Tấn công phát lại (Replay Attack):** Kẻ tấn công bắt trộm một gói tin lệnh hợp lệ (như gói "Mở khóa máy") và phát lại nhiều lần để tự ý mở khóa.
* **Cách OGK hóa giải:**
  * Mỗi bản tin lệnh đều đính kèm: `timestamp` (thời điểm chuẩn UTC) và `nonce` (số ngẫu nhiên chỉ dùng 1 lần).
  * Agent kiểm tra: Nếu `timestamp` bị lệch quá 30 giây hoặc `nonce` đã từng xuất hiện trong bộ nhớ đệm, gói tin bị hủy bỏ ngay lập tức.

---

### 5.7. Phân tích mô hình đe dọa an ninh mạng STRIDE trong dự án OGK

| Thành phần STRIDE | Bản chất mối đe dọa | Giải pháp kỹ thuật khắc phục trong OGK |
| :--- | :--- | :--- |
| **S - Spoofing**<br>*(Giả mạo danh tính)* | Kẻ lạ giả danh phụ huynh để đổi luật; thiết bị lạ gửi dữ liệu rác. | - Phụ huynh: Xác thực Argon2id, Bearer Token JWT.<br>- Máy con: Token riêng gắn với Hardware Machine GUID lúc ghép đôi. |
| **T - Tampering**<br>*(Can thiệp sửa đổi)* | Trẻ sửa lén tệp CSDL SQLite cục bộ trên máy con để tăng giờ. | - Chữ ký toàn vẹn HMAC-SHA256 trên mọi chính sách.<br>- Phân quyền ACL thư mục chỉ cho phép tài khoản SYSTEM có quyền ghi. |
| **R - Repudiation**<br>*(Chối bỏ trách nhiệm)* | Phụ huynh vô tình đổi giờ hoặc khóa máy nhưng quên và cho rằng lỗi. | - Bảng nhật ký kiểm toán **Audit Log** cơ chế Append-Only lưu vết đầy đủ IP, mốc giờ, giá trị cũ và mới. |
| **I - Information Disclosure**<br>*(Lộ lọt thông tin)* | Rò rỉ lịch sử duyệt web hoặc dữ liệu nhạy cảm của trẻ ra ngoài Internet. | - Áp dụng triệt để nguyên tắc NT2: Không lưu full URL, không đọc chat.<br>- Mô hình 100% Local-First: Dữ liệu nằm trọn trong mạng gia đình. |
| **D - Denial of Service**<br>*(Từ chối dịch vụ)* | Trẻ cố tình làm sập dịch vụ Agent; gửi request ồ ạt làm treo máy chủ. | - Windows Service Recovery tự khởi động lại Agent sau 5s.<br>- Middleware Rate Limiting trên FastAPI giới hạn số request/phút. |
| **E - Elevation of Privilege**<br>*(Leo thang đặc quyền)* | Trẻ chiếm quyền Administrator trên Windows để gỡ phần mềm, tắt dịch vụ. | - Cấu hình tài khoản trẻ là Standard User.<br>- Agent chạy ở Session 0 dưới quyền LocalSystem, chặn đứng mọi thao tác End Task. |

---

# PHẦN 6: PHÁP LÝ & ĐẠO ĐỨC CÔNG NGHỆ BẢO VỆ TRẺ EM TRÊN KHÔNG GIAN MẠNG

### 6.1. Nghị định 13/2023/NĐ-CP (Điều 20) về Xử lý dữ liệu cá nhân của trẻ em

* **Quy định pháp lý cốt lõi:**
  * Việc xử lý dữ liệu cá nhân của trẻ em phải luôn bảo đảm nguyên tắc bảo vệ quyền và vì lợi ích tốt nhất của trẻ.
  * Bắt buộc phải có sự đồng ý của cha mẹ hoặc người giám hộ; và nếu trẻ từ đủ 7 tuổi trở lên, bắt buộc phải có thêm sự đồng thuận của chính đứa trẻ đó.
* **Ánh xạ vào thiết kế kỹ thuật của OGK:**
  * Quy trình ghép đôi không dây bằng mã PIN 8 ký tự là điểm chạm kỹ thuật thể hiện sự đồng thuận: Cha mẹ lấy mã từ Dashboard, cùng ngồi lại với con và nhập mã vào máy tính con để bắt đầu thiết lập quyền đồng hành.
  * Phụ huynh có toàn quyền thu hồi sự đồng thuận bất kỳ lúc nào thông qua tính năng *"Xóa toàn bộ dữ liệu thiết bị"* trên giao diện quản trị.

---

### 6.2. Luật Trẻ Em 2016 (Điều 21) & Quyền bí mật đời sống riêng tư

* **Quy định pháp lý cốt lõi:**
  * Trẻ em có quyền bất khả xâm phạm về đời sống riêng tư, bí mật cá nhân và bí mật gia đình. Mọi hành vi xâm phạm đời sống riêng tư của trẻ em trên môi trường mạng đều bị nghiêm cấm.
* **Ánh xạ vào thiết kế kỹ thuật của OGK:**
  * OGK kiên quyết loại bỏ cơ chế chụp lén màn hình liên tục và đọc trộm tin nhắn cá nhân.
  * Hệ thống chỉ ghi nhận 4 siêu dữ liệu kỹ thuật ở mức tổng quan: Tên tiến trình, Tên miền cấp 2, Thời lượng sử dụng và Mốc giờ. Cha mẹ biết con dành bao nhiêu thời gian cho học tập và giải trí mà hoàn toàn không xâm phạm vào nội dung bài viết hay các cuộc trò chuyện riêng tư của con.

---

### 6.3. Tiêu chuẩn xác thực NIST SP 800-63B & Tiêu chuẩn bảo mật ứng dụng OWASP ASVS v4

* **NIST SP 800-63B (Digital Identity Guidelines):**
  * Tiêu chuẩn hướng dẫn định danh số của Viện Tiêu chuẩn và Kỹ thuật Quốc gia Hoa Kỳ: Quy định bắt buộc sử dụng các thuật toán băm ngốn bộ nhớ như Argon2id để kháng cự tấn công bẻ khóa bằng phần cứng chuyên dụng, loại bỏ quy tắc bắt buộc đổi mật khẩu định kỳ vô nghĩa và thay bằng cơ chế kiểm tra mật khẩu yếu.
* **OWASP ASVS v4 (Application Security Verification Standard):**
  * Bộ tiêu chuẩn kiểm chứng bảo mật ứng dụng web của tổ chức an ninh mạng OWASP toàn cầu: Đặt ra các tiêu chí kiểm thử khắt khe về quản lý phiên làm việc, thiết lập đầy đủ các cờ bảo vệ Cookie (`HttpOnly`, `SameSite=Strict`), vô hiệu hóa hiển thị chi tiết lỗi máy chủ ra ngoài giao diện, và chuẩn hóa dữ liệu đầu vào chống các cuộc tấn công SQL Injection và Cross-Site Scripting (XSS).
