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
- [PHẦN 7: TẦNG LỌC MẠNG DNS SINKHOLE, SAFESEARCH & KHẮC CHẾ DoH/DoT](#phần-7-tầng-lọc-mạng-dns-sinkhole-safesearch--khắc-chế-dohdot)
  - [7.1. Cấu trúc bản tin DNS nhị phân (RFC 1035): Header 12 byte & Các trường dữ liệu](#71-cấu-trúc-bản-tin-dns-nhị-phân-rfc-1035-header-12-byte--các-trường-dữ-liệu)
  - [7.2. So sánh Synthetic IP: Tại sao trả về 0.0.0.0 thay vì 127.0.0.1?](#72-so-sánh-synthetic-ip-tại-sao-trả-về-0000-thay-vì-127001)
  - [7.3. Kỹ thuật DNS VIP Rewriting: Cưỡng chế Google SafeSearch & YouTube Restricted Mode](#73-kỹ-thuật-dns-vip-rewriting-cưỡng-chế-google-safesearch--youtube-restricted-mode)
  - [7.4. Khắc chế DoH (DNS-over-HTTPS) & DoT (DNS-over-TLS) qua Canary Domain NXDOMAIN](#74-khắc-chế-doh-dns-over-https--dot-dns-over-tls-qua-canary-domain-nxdomain)
  - [7.5. Lập trình DNS Proxy Socket UDP 53 Non-blocking & Xử lý xung đột Windows Dnscache](#75-lập-trình-dns-proxy-socket-udp-53-non-blocking--xử-lý-xung-đột-windows-dnscache)
  - [7.6. Thuật toán phân giải tên miền: Domain Trie vs Regex vs Set Matching & Immunity Whitelist (NT6)](#76-thuật-toán-phân-giải-tên-miền-domain-trie-vs-regex-vs-set-matching--immunity-whitelist-nt6)
- [PHẦN 8: KIỂM SOÁT ỨNG DỤNG BẰNG MÃ BĂM SHA-256 & TỐI ƯU HÓA mtime CACHE](#phần-8-kiểm-soát-ứng-dụng-bằng-mã-băm-sha-256--tối-ưu-hóa-mtime-cache)
  - [8.1. Hạn chế chí mạng của lọc theo tên tiến trình (process.name) & Kỹ thuật đổi tên file](#81-hạn-chế-chí-mạng-của-lọc-theo-tên-tiến-trình-processname--kỹ-thuật-đổi-tên-file)
  - [8.2. Giải thuật băm nhị phân SHA-256 theo khối (Chunked Reading 64KB)](#82-giải-thuật-băm-nhị-phân-sha-256-theo-khối-chunked-reading-64kb)
  - [8.3. Tối ưu hóa hiệu năng bằng bộ nhớ đệm mtime (os.path.getmtime Cache): Giảm 450ms xuống 0.02ms](#83-tối-ưu-hóa-hiệu-năng-bằng-bộ-nhớ-đệm-mtime-ospathgetmtime-cache-giảm-450ms-xuống-002ms)
  - [8.4. Xử lý ngoại lệ nhân hệ điều hành: AccessDenied, NoSuchProcess, ZombieProcess](#84-xử-lý-ngoại-lệ-nhân-hệ-điều-hành-accessdenied-nosuchprocess-zombieprocess)
  - [8.5. Cơ chế cách ly và hạ gục tiến trình vi phạm: terminate() vs kill() trong Win32](#85-cơ-chế-cách-ly-và-hạ-gục-tiến-trình-vi-phạm-terminate-vs-kill-trong-win32)
- [PHẦN 9: BẢO MẬT CẤP CAO F5, MÃ HÓA AES-256-GCM AEAD & TRIỆT TIÊU IDOR](#phần-9-bảo-mật-cấp-cao-f5-mã-hóa-aes-256-gcm-aead--triệt-tiêu-idor)
  - [9.1. Mã hóa xác thực dữ liệu kết hợp AEAD & Tiêu chuẩn AES-256-GCM](#91-mã-hóa-xác-thực-dữ-liệu-kết-hợp-aead--tiêu-chuẩn-aes-256-gcm)
  - [9.2. Mổ xẻ cấu trúc bản tin mã hóa: Nonce 12 byte, Ciphertext & Auth Tag 16 byte (Chống Bit-Flipping)](#92-mổ-xẻ-cấu-trúc-bản-tin-mã-hóa-nonce-12-byte-ciphertext--auth-tag-16-byte-chống-bit-flipping)
  - [9.3. Lỗ hổng IDOR (Insecure Direct Object Reference) trong ứng dụng giám sát](#93-lỗ-hổng-idor-insecure-direct-object-reference-trong-ứng-dụng-giám-sát)
  - [9.4. Cơ chế phòng thủ IDOR 2 lớp: Scope JWT + Ownership Check trong CSDL](#94-cơ-chế-phòng-thủ-idor-2-lớp-scope-jwt--ownership-check-trong-csdl)
  - [9.5. Phòng chống tấn công Brute-force & DoS: Khóa tài khoản 15 phút & IP Rate Limiting](#95-phòng-chống-tấn-công-brute-force--dos-khóa-tài-khoản-15-phút--ip-rate-limiting)
- [PHẦN 10: PHÁP LÝ NGHỊ ĐỊNH 13/2023/NĐ-CP, QUYỀN XÓA DỮ LIỆU & CHỊU LỖI NGOẠI TUYẾN M5](#phần-10-pháp-lý-nghị-định-132023nđ-cp-quyền-xóa-dữ-liệu--chịu-lỗi-ngoại-tuyến-m5)
  - [10.1. Chu kỳ lưu trữ dữ liệu (Data Retention Lifecycle) 90 ngày & Cron Job tự động Prune](#101-chu-kỳ-lưu-trữ-dữ-liệu-data-retention-lifecycle-90-ngày--cron-job-tự-động-prune)
  - [10.2. Quyền được lãng quên (Right to Erasure): Quy trình xóa đồng bộ 2 chiều Server - Agent](#102-quyền-được-lãng-quên-right-to-erasure-quy-trình-xóa-đồng-bộ-2-chiều-server---agent)
  - [10.3. Khả năng chịu lỗi và tự phục hồi M5: Mất mạng, Server crash & DNS Watchdog Netsh](#103-khả-năng-chịu-lỗi-và-tự-phục-hồi-m5-mất-mạng-server-crash--dns-watchdog-netsh)
- [PHẦN 11: THỰC NGHIỆM ĐO LƯỜNG HIỆU NĂNG M4 & KHẮC CHẾ 7 KỸ THUẬT VƯỢT RÀO M3](#phần-11-thực-nghiệm-đo-lường-hiệu-năng-m4--khắc-chế-7-kỹ-thuật-vượt-rào-m3)
  - [11.1. Phương pháp đo kiểm thực nghiệm hiệu năng hệ thống M4 (RAM, CPU, DNS Latency, WebSocket)](#111-phương-pháp-đo-kiểm-thực-nghiệm-hiệu-năng-hệ-thống-m4-ram-cpu-dns-latency-websocket)
  - [11.2. Phân tích kết quả thực nghiệm M4: So sánh mục tiêu ban đầu vs Kết quả thực tế](#112-phân-tích-kết-quả-thực-nghiệm-m4-so-sánh-mục-tiêu-ban-đầu-vs-kết-quả-thực-tế)
  - [11.3. Ma trận khắc chế toàn diện 7 kỹ thuật vượt rào kinh điển của học sinh (Anti-Bypass M3)](#113-ma-trận-khắc-chế-toàn-diện-7-kỹ-thuật-vượt-rào-kinh-điển-của-học-sinh-anti-bypass-m3)


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


---

# PHẦN 7: TẦNG LỌC MẠNG DNS SINKHOLE, SAFESEARCH & KHẮC CHẾ DoH/DoT

### 7.1. Cấu trúc bản tin DNS nhị phân (RFC 1035): Header 12 byte & Các trường dữ liệu

Trong tầng giao vận mạng, bản tin DNS mặc định truyền tải qua giao thức **UDP trên cổng 53**. Mọi gói tin DNS (cả truy vấn Request lẫn phản hồi Response) đều tuân thủ chặt chẽ định dạng nhị phân theo chuẩn quốc tế **RFC 1035**:

```
+-------------------------------------------------------------------+
|                        DNS MESSAGE HEADER (12 Bytes)              |
|  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15                   |
+-------------------------------------------------------------------+
|                         ID (16 bits)                              |
+----+--------+----+----+----+----+----+----+----+------------------+
| QR | Opcode | AA | TC | RD | RA | Z  | AD | CD |    RCODE (4)     |
+----+--------+----+----+----+----+----+----+----+------------------+
|                    QDCOUNT / Question Count (16)                  |
+-------------------------------------------------------------------+
|                    ANCOUNT / Answer Count (16)                    |
+-------------------------------------------------------------------+
|                    NSCOUNT / Authority Count (16)                 |
+-------------------------------------------------------------------+
|                    ARCOUNT / Additional Count (16)                |
+-------------------------------------------------------------------+
|                        QUESTION SECTION                           |
|  - QNAME: Tên miền dạng nhãn độ dài (vd: \x03www\x06google\x03com\x00) |
|  - QTYPE: Loại bản ghi truy vấn (vd: 0x0001 = A, 0x001C = AAAA)   |
|  - QCLASS: Lớp mạng (0x0001 = IN / Internet)                      |
+-------------------------------------------------------------------+
|                        ANSWER SECTION (Nếu có)                    |
|  - NAME: Con trỏ nén tên miền (0xC00C trỏ về QNAME)               |
|  - TYPE (16) | CLASS (16) | TTL (32 bits) | RDLENGTH (16 bits)    |
|  - RDATA: Dữ liệu địa chỉ IP trả về (vd: 4 bytes cho IPv4)        |
+-------------------------------------------------------------------+
```

* **Mổ xẻ từng bit trong 12 bytes Header:**
  1. **ID (16 bits / 2 bytes):** Định danh duy nhất của gói tin, do Client sinh ngẫu nhiên. Khi Server phản hồi, bắt buộc phải sao chép nguyên vẹn ID này để Client ghép đôi kết quả truy vấn.
  2. **QR (Query/Response Flag - 1 bit):** Bit 0 = Bản tin truy vấn (Request); Bit 1 = Bản tin phản hồi (Response).
  3. **Opcode (4 bits):** Loại truy vấn (0 = Standard Query / Truy vấn chuẩn; 1 = Inverse Query; 2 = Server Status).
  4. **AA (Authoritative Answer - 1 bit):** Cờ xác nhận máy chủ DNS trả về có nắm giữ thẩm quyền chính thức của tên miền hay chỉ là bộ nhớ đệm (Cache).
  5. **TC (Truncation Flag - 1 bit):** Cờ báo gói tin bị cắt cụt do vượt quá kích thước tối đa 512 bytes của gói UDP.
  6. **RD (Recursion Desired - 1 bit):** Client yêu cầu máy chủ phân giải đệ quy (hỏi tiếp các DNS root/tld nếu không có sẵn).
  7. **RA (Recursion Available - 1 bit):** Server báo có hỗ trợ giải đệ quy hay không.
  8. **RCODE (Response Code - 4 bits):** Mã kết quả phản hồi của truy vấn:
     * `RCODE = 0 (NOERROR):` Truy vấn thành công rực rỡ, có bản ghi trả về.
     * `RCODE = 3 (NXDOMAIN):` Tên miền không tồn tại trên Internet (Non-Existent Domain). OGK sử dụng mã này để đánh lừa tính năng DoH của trình duyệt.
     * `RCODE = 2 (SERVFAIL):` Máy chủ DNS gặp sự cố nội bộ.
     * `RCODE = 5 (REFUSED):` Máy chủ DNS từ chối phục vụ truy vấn vì lý do chính sách.
  9. **QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT (mỗi trường 16 bits):** Số lượng câu hỏi, số lượng câu trả lời, số bản ghi quản trị, và số bản ghi phụ trợ đính kèm.

* **Cơ chế nén con trỏ (Name Compression - Pointer 0xC0):**  
  Để tiết kiệm băng thông mạng 512 bytes của gói UDP, RFC 1035 quy định nếu tên miền ở Answer trùng lặp với tên miền ở Question, DNS Server không ghi lại chuỗi ký tự mà chỉ ghi 2 bytes: `0xC00C` (Trong đó `0xC0` là 2 bit đầu `11` báo hiệu đây là một Offset Pointer, và `0x0C = 12` trỏ đúng vào byte thứ 12 của gói tin — nơi bắt đầu chuỗi QNAME trong phần Question).

---

### 7.2. So sánh Synthetic IP: Tại sao trả về `0.0.0.0` thay vì `127.0.0.1`?

Khi một tên miền nằm trong danh sách đen (Blacklist) bị Agent chặn, DNS Sinkhole Proxy sẽ can thiệp và phản hồi một bản ghi Synthetic A Record (Địa chỉ IP tổng hợp giả lập). Trong thực tế thiết kế mạng, có hai lựa chọn phổ biến là `127.0.0.1` (Localhost) và `0.0.0.0` (Unspecified Address).

| Tiêu chí kỹ thuật | Trả về `127.0.0.1` (Localhost Loopback) | Trả về `0.0.0.0` (RFC 3513 / RFC 5735) [OGK CHỌN] |
| :--- | :--- | :--- |
| **Bản chất địa chỉ** | Địa chỉ lặp nội bộ (Loopback Adapter). Gói tin được định tuyến ngược vào chính máy tính của trẻ. | Địa chỉ không xác định (Unspecified/Non-routable Address), mang ý nghĩa "không có máy chủ đích nào ở đây". |
| **Hành vi bắt tay TCP** | Trình duyệt cố gắng gửi gói tin `TCP SYN` đến cổng 80 hoặc 443 của `127.0.0.1` trên máy con. | Kernel mạng Windows nhận diện `0.0.0.0` là địa chỉ bất hợp lệ cho gói tin gửi đi, lập tức từ chối ngay ở tầng Socket. |
| **Hậu quả độ trễ (Latency)** | Nếu máy con không mở web server, Windows gửi gói `TCP RST` hoặc chờ timeout 20 - 30 giây khiến trình duyệt quay vòng đơ lag. Nếu máy con có cài web server ngầm (như IIS, XAMPP, Skype), trang web đen bị biến tướng thành giao diện nội bộ gây xung đột nghiêm trọng! | **Thời gian phản hồi bằng 0 mili-giây (0 ms).** Trình duyệt lập tức báo lỗi `ERR_ADDRESS_INVALID` hoặc `ERR_CONNECTION_REFUSED` ngay lập tức, không tiêu tốn CPU, không lag mạng. |
| **Quy chuẩn quốc tế** | Phương pháp cũ thời kỳ Hosts file thập niên 1990 (đã lỗi thời). | **Khuyến nghị hiện đại của IETF, Pi-hole, AdGuard Home** và các hệ thống tường lửa doanh nghiệp chuyên nghiệp. |

---

### 7.3. Kỹ thuật DNS VIP Rewriting: Cưỡng chế Google SafeSearch & YouTube Restricted Mode

Các bộ máy tìm kiếm như Google, Bing và nền tảng video YouTube đều hỗ trợ chế độ tìm kiếm an toàn cho trẻ em (SafeSearch / Restricted Mode) nhằm loại bỏ tự động 100% hình ảnh bạo lực, nội dung khiêu dâm và kinh dị. Tuy nhiên, nếu dựa vào việc cài đặt trên giao diện trình duyệt, trẻ hoàn toàn có thể vào phần Settings hoặc dùng chế độ Ẩn danh (Incognito) để tự tay tắt tính năng này.

* **Cơ chế DNS VIP Rewriting của OGK:**
  Thay vì dựa vào người dùng, OGK can thiệp ở mức độ mạng hạ tầng:
  1. Khi trình duyệt của trẻ phân giải tên miền tìm kiếm, ví dụ `www.google.com`, truy vấn DNS rơi vào `dns_proxy.py`.
  2. Proxy phát hiện đây là domain tìm kiếm thuộc diện quản lý.
  3. Proxy không gửi truy vấn ra ngoài Internet để lấy IP thật của Google, mà **thay thế trực tiếp (Rewrite)** bằng IP của máy chủ VIP cưỡng chế SafeSearch do chính Google/Microsoft công bố:
     * **Google SafeSearch:** Mọi tên miền `*.google.com`, `*.google.com.vn` $ightarrow$ Trả về CNAME `forcesafesearch.google.com` hoặc Synthetic IP `216.239.38.120`.
     * **Bing SafeSearch:** Mọi tên miền `*.bing.com` $ightarrow$ Trả về CNAME `strict.bing.com` hoặc Synthetic IP `204.79.197.220`.
     * **YouTube Restricted Mode:** Mọi tên miền `*.youtube.com`, `youtubei.googleapis.com` $ightarrow$ Trả về CNAME `restrict.youtube.com`.
  4. Trình duyệt kết nối đến cụm máy chủ VIP của Google qua IP `216.239.38.120`. Cụm máy chủ này được cấu hình phần cứng để **luôn luôn kích hoạt SafeSearch ở mức độ nghiêm ngặt nhất (Strict Mode)**, ngay cả khi trẻ dùng trình duyệt ẩn danh hoặc tài khoản khách. Trẻ không có bất kỳ nút bấm nào để vô hiệu hóa!

---

### 7.4. Khắc chế DoH (DNS-over-HTTPS) & DoT (DNS-over-TLS) qua Canary Domain NXDOMAIN

* **DoH (RFC 8484) & DoT (RFC 7858) là gì?**
  * Bình thường, DNS chạy trên cổng UDP 53 không mã hóa.
  * DoT mã hóa truy vấn DNS bằng TLS chạy trên cổng riêng **TCP 853**.
  * DoH tinh vi hơn rất nhiều: Đóng gói toàn bộ truy vấn DNS vào trong gói tin HTTPS chuẩn (cổng TCP 443), trộn lẫn hoàn toàn với lưu lượng lướt web thông thường.
  * **Mối đe dọa:** Trình duyệt Chrome, Edge, Firefox hiện nay tự ý kích hoạt DoH trỏ về các máy chủ DNS công cộng của bên thứ ba (như Cloudflare `1.1.1.1` hay Google `8.8.8.8`). Khi DoH hoạt động, mọi truy vấn đều bị mã hóa qua TLS 1.3, khiến DNS Sinkhole Proxy trên cổng 53 của OGK hoàn toàn "bị mù", không thể bắt và lọc web được nữa!

* **Chiến lược khắc chế 2 lớp của OGK:**
  1. **Khắc chế DoT:** Thiết lập luật Windows Firewall chặn đứng hoàn toàn cổng TCP ra ngoài `Outbound Port 853`.
  2. **Khắc chế DoH bằng cơ chế Canary Domain Quốc Tế:**
     * Tổ chức Mozilla Firefox và các nhà phát triển Chromium (Google, Microsoft) đã thống nhất một tiêu chuẩn an toàn cho mạng gia đình và trường học: Trước khi trình duyệt tự động kích hoạt tính năng DoH, nó **bắt buộc phải gửi một truy vấn thăm dò (Canary Query)** bằng DNS thông thường đến tên miền chim báo bão đặc biệt:  
       $$	ext{Canary Domain} = 	extbf{use-application-dns.net}$$
     * **Thuật toán xử lý của OGK:**  
       Khi gói tin hỏi `use-application-dns.net` tới `dns_proxy.py`, Agent lập tức chặn lại và gửi trả về gói tin DNS với mã phản hồi:  
       $$	extbf{RCODE = 3 (NXDOMAIN - Non-Existent Domain)}$$
     * **Kết quả:** Nhận được tín hiệu `NXDOMAIN`, trình duyệt hiểu rằng mạng máy tính này đang có chính sách giám sát phụ huynh nội bộ hợp pháp. Trình duyệt sẽ **ngay lập tức vô hiệu hóa tính năng DoH ngầm**, quay trở lại sử dụng DNS phân giải cổng UDP 53 của hệ điều hành — nơi mà OGK Sinkhole đang kiểm soát 100%!

---

### 7.5. Lập trình DNS Proxy Socket UDP 53 Non-blocking & Xử lý xung đột Windows Dnscache

* **Lập trình Socket UDP Non-blocking:**
  * Khác với kết nối TCP luồng (Stream), UDP là giao thức phi kết nối (Datagram).
  * Proxy khởi tạo Socket UDP gắn vào cổng nội bộ: `sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)`.
  * Gắn cờ non-blocking `sock.setblocking(False)` hoặc chạy trong vòng lặp bất đồng bộ của `asyncio` thông qua `asyncio.DatagramProtocol`.
  * Cơ chế xử lý luồng: Khi nhận gói tin từ máy tính con qua `recvfrom(512)`, Proxy giải mã tiêu đề nhị phân. Nếu tên miền hợp lệ, Proxy sử dụng bộ nhớ đệm (Cache) hoặc chuyển tiếp nhanh (Forward) qua Socket UDP thứ hai tới Upstream DNS (Cloudflare `1.1.1.1` hoặc Google `8.8.8.8`), sau đó chuyển tiếp kết quả trả về cho máy tính con. Độ trễ toàn trình đo đạc thực tế chỉ **0.83 ms**.

* **Bài toán xung đột dịch vụ Windows DNS Client (`Dnscache`):**
  * Trên Windows, dịch vụ hệ thống `Dnscache` (DNS Client Service) có nhiệm vụ quản lý đệm DNS cho hệ điều hành. Tuy nhiên, `Dnscache` hoạt động ở vai trò Client phân giải, **không lắng nghe (listen) cổng UDP 53 trên địa chỉ Loopback `127.0.0.1`**.
  * Do đó, OGK Proxy có thể bind cổng `127.0.0.1:53` hoàn toàn trơn tru mà không sợ xung đột cổng (`WSAEADDRINUSE`).
  * Sau khi Proxy khởi động thành công, Agent sử dụng thư viện `ctypes` hoặc công cụ dòng lệnh `netsh` của Windows để đổi cấu hình DNS của card mạng chính:
    ```cmd
    netsh interface ip set dns name="Wi-Fi" source=static addr=127.0.0.1
    ```
  * Mọi ứng dụng trên Windows (Chrome, Edge, Game, Torrent) khi gọi hàm API Windows Socket (`getaddrinfo` / `DnsQuery`) đều tự động chuyển hướng gói tin vào `127.0.0.1:53` để OGK thẩm tra.

---

### 7.6. Thuật toán phân giải tên miền: Domain Trie vs Regex vs Set Matching & Immunity Whitelist (NT6)

* **So sánh các cấu trúc dữ liệu đối soát tên miền:**
  * **Regex (Biểu thức chính quy):** Quá chậm ($O(N 	imes L)$), gây nghẽn cổ chai CPU khi danh sách đen lên đến hàng chục ngàn tên miền.
  * **Hash Set ($O(1)$ lookup):** Tốc độ cực nhanh cho tên miền chính xác (Exact match), nhưng không xử lý được tên miền phụ con (Subdomain wildcard như `*.tiktok.com`).
  * **Cấu trúc Cây tiền tố đảo ngược (Reverse Domain Trie) [OGK KẾT HỢP HASH SET]:**
    * Tên miền được phân rã ngược từ đuôi: `m.tiktok.com` $ightarrow$ `['com', 'tiktok', 'm']`.
    * Kiểm tra nhanh qua bảng băm rút gọn các cấp domain cha: Kiểm tra `m.tiktok.com`, nếu không có kiểm tra tiếp `tiktok.com`. Độ phức tạp trung bình chỉ là $O(K)$ với $K$ là số cấp của tên miền (thường $K \le 4$), tốc độ xử lý dưới $0.01	ext{ ms}$.

* **Danh mục Miễn nhiễm Vĩnh viễn (Immunity Whitelist - Nguyên tắc NT6):**
  * Nhằm đảm bảo quyền được học tập và kết nối thiết yếu của trẻ em, OGK quy định một danh sách bất khả xâm phạm ở mức lõi cứng (Hardcoded Immunity):
    * Cổng dịch vụ học tập quốc gia: `moet.gov.vn`, `edu.vn`.
    * Nền tảng học trực tuyến: `zoom.us`, `teams.microsoft.com`, `classroom.google.com`.
    * Cập nhật hệ điều hành thiết yếu: `windowsupdate.com`, `update.microsoft.com`.
    * Hạ tầng phân giải mạng cơ bản: `use-application-dns.net` (Canary domain trả về NXDOMAIN).
  * **Nguyên tắc kỹ thuật:** Bất kể phụ huynh có nhập tên miền học tập vào danh sách cấm hoặc giờ giới nghiêm kích hoạt, thuật toán kiểm tra tính miễn nhiễm (Immunity Check) luôn được chạy đầu tiên. Nếu thuộc Whitelist, gói tin lập tức được cho qua, ngăn chặn hoàn toàn việc phụ huynh lạm quyền cắt đứt liên lạc học tập khẩn cấp của con.

---

# PHẦN 8: KIỂM SOÁT ỨNG DỤNG BẰNG MÃ BĂM SHA-256 & TỐI ƯU HÓA mtime CACHE

### 8.1. Hạn chế chí mạng của lọc theo tên tiến trình (`process.name`) & Kỹ thuật đổi tên file

Hầu hết các phần mềm quản lý máy tính sơ sài trên thị trường hiện nay áp dụng cách tiếp cận ngây thơ: Lấy danh sách tiến trình đang chạy qua lệnh `psutil.process_iter()` và so sánh chuỗi tên tệp nhị phân (`proc.name() == "League of Legends.exe"` hay `"RobloxPlayerBeta.exe"`).

* **Lỗ hổng chết người của cơ chế này:**
  * Học sinh và trẻ em chỉ cần vào thư mục cài đặt game, bấm phím `F2` đổi tên tệp thực thi từ `Roblox.exe` thành `Winword.exe`, `Calculator.exe` hoặc `Chrome.exe`.
  * Khi tiến trình khởi chạy, Windows tải file vào bộ nhớ với tên mới `Winword.exe`.
  * Bộ lọc ngây thơ hoàn toàn bị qua mặt vì so sánh chuỗi thấy tên hợp lệ, cho phép game chạy thỏa thích!

---

### 8.2. Giải thuật băm nhị phân SHA-256 theo khối (Chunked Reading 64KB)

Để triệt tiêu hoàn toàn kỹ thuật đổi tên file, OGK định danh ứng dụng dựa trên **Mã băm nhị phân SHA-256 (Cryptographic Binary Hash)** của chính tệp thực thi đó trên ổ đĩa cứng. Dù tệp có bị đổi tên thành bất cứ thứ gì, nội dung nhị phân (Machine Code) bên trong không đổi, giá trị băm SHA-256 tạo ra vẫn là duy nhất tuyệt đối ($2^{256}$ khả năng, xác suất trùng lặp bằng 0).

* **Vấn đề bộ nhớ khi băm tệp nhị phân lớn:**
  * Các tựa game hiện đại thường có tệp thực thi `.exe` dung lượng từ vài trăm Megabytes đến hàng Gigabytes.
  * Nếu dùng `open(path, 'rb').read()` để đọc trọn gói vào RAM, máy tính con sẽ lập tức cạn kiệt bộ nhớ (Out-Of-Memory Crash), gây giật lag máy tính nghiêm trọng.
* **Giải pháp băm theo khối 64KB (Chunked Streaming):**
  ```python
  import hashlib

  def calculate_sha256(filepath: str, chunk_size: int = 65536) -> str:
      hasher = hashlib.sha256()
      with open(filepath, 'rb') as f:
          while chunk := f.read(chunk_size):
              hasher.update(chunk)
      return hasher.hexdigest().lower()
  ```
  * Tệp nhị phân được đọc tuần tự từng khối đệm nhỏ đúng **64 KB (65,536 bytes)** và nạp vào bộ băm trực tiếp. Dung lượng RAM chiếm dụng của Agent luôn cố định dưới **1 MB** dù tệp game có dung lượng lớn đến đâu!

---

### 8.3. Tối ưu hóa hiệu năng bằng bộ nhớ đệm mtime (`os.path.getmtime` Cache): Giảm 450ms xuống 0.02ms

Mặc dù băm theo khối đã giải quyết bài toán RAM, nhưng việc đọc ổ cứng liên tục (I/O Disk Read) sau mỗi 5 giây quét tiến trình sẽ khiến ổ đĩa quá tải (Disk 100%), gây sụt giảm tuổi thọ ổ SSD và tiêu tốn CPU.

* **Thuật toán mtime Caching của OGK:**
  1. Trong hệ điều hành Windows (NTFS), mỗi tệp tin đều có một thuộc tính siêu dữ liệu gọi là **Last Modified Time (`mtime`)** — thời điểm tệp bị chỉnh sửa lần cuối cùng.
  2. Việc đọc siêu dữ liệu `mtime` thông qua hàm gọi hệ điều hành `os.path.getmtime(filepath)` chỉ tốn một thao tác đọc chỉ mục trong bảng Master File Table (MFT) của ổ đĩa, tiêu tốn **0.02 mili-giây**, hoàn toàn không phải đọc nội dung tệp!
  3. **Cấu trúc bộ nhớ đệm trong RAM:**
     $$	ext{Cache} = \{ 	ext{filepath} : (	ext{mtime}, 	ext{sha256\_digest}) \}$$
  4. **Quy trình thẩm tra tiến trình:**
     * Agent lấy đường dẫn tệp thực thi của tiến trình: `proc.exe()`.
     * Kiểm tra thời gian sửa đổi hiện tại của tệp: $T_{	ext{current}} = 	ext{os.path.getmtime}(path)$.
     * Đối chiếu với Cache: Nếu đường dẫn đã tồn tại và $T_{	ext{current}} == T_{	ext{cached}}$, Agent lấy ngay mã SHA-256 từ RAM ra dùng mà **không cần đọc lại đĩa cứng**!
     * Chỉ khi tệp bị ghi đè, cập nhật bản vá hoặc lần đầu tiên phát hiện, Agent mới thực hiện băm nhị phân lại một lần duy nhất.
  * **Kết quả đo lường thực tế:** Thời gian quét danh sách 150 tiến trình giảm từ **450 ms** xuống còn **0.8 ms**, mức chiếm dụng CPU của Agent đo đạc duy trì ở mức **0.0%** (xem Báo cáo M4).

---

### 8.4. Xử lý ngoại lệ nhân hệ điều hành: AccessDenied, NoSuchProcess, ZombieProcess

Trong quá trình duyệt qua bảng tiến trình của hệ điều hành Windows bằng thư viện `psutil`, Agent chắc chắn sẽ gặp các tình huống đặc biệt của nhân hệ điều hành. Nếu không bắt ngoại lệ chuẩn xác, tiến trình Agent sẽ bị sập bất ngờ:

1. **`psutil.AccessDenied` (Truy cập bị từ chối):**
   * Xảy ra khi Agent cố gắng truy vấn đường dẫn thực thi `proc.exe()` của các tiến trình hệ thống cấp nhân (Kernel System Processes) chạy ở Session 0 như `System (PID 4)`, `smss.exe`, `csrss.exe`, hoặc các phần mềm diệt virus có cơ chế tự vệ (Anti-Cheat/EDR).
   * **Cách xử lý:** Bắt riêng ngoại lệ `except psutil.AccessDenied: pass` và bỏ qua, đánh dấu đây là tiến trình hệ thống miễn nhiễm, tuyệt đối không can thiệp.
2. **`psutil.NoSuchProcess` (Tiến trình không tồn tại):**
   * Xảy ra trong môi trường đa nhiệm: Một tiến trình vừa xuất hiện trong danh sách duyệt nhưng đã kịp thoát hoặc bị người dùng đóng lại trước khi Agent kịp gọi hàm băm hoặc kết liễu.
   * **Cách xử lý:** Bắt `except psutil.NoSuchProcess: pass` và loại bỏ PID đó khỏi danh sách theo dõi.
3. **`psutil.ZombieProcess` (Tiến trình thây ma):**
   * Tiến trình đã dừng hoạt động nhưng tiến trình cha chưa đọc mã thoát (Exit Code), vẫn còn chiếm giữ một mục trong bảng tiến trình hệ điều hành.
   * **Cách xử lý:** Bắt ngoại lệ, giải phóng tài nguyên và bỏ qua.

---

### 8.5. Cơ chế cách ly và hạ gục tiến trình vi phạm: `terminate()` vs `kill()` trong Win32

Khi phát hiện một ứng dụng có mã băm SHA-256 hoặc tên nằm trong danh mục cấm tại thời điểm hiện tại (ví dụ game trong giờ học), Agent tiến hành cưỡng chế đóng ứng dụng theo quy trình 2 pha:

* **Pha 1: `proc.terminate()` (Yêu cầu đóng lịch sự):**
  * Ánh xạ xuống Win32 API: Gửi thông điệp `WM_CLOSE` hoặc tín hiệu `SIGTERM` tới hàng đợi cửa sổ của ứng dụng.
  * Ứng dụng có cơ hội lưu dữ liệu đang làm dở và dọn dẹp bộ nhớ trước khi thoát.
  * Agent chờ tối đa 2.0 giây (`proc.wait(timeout=2.0)`).
* **Pha 2: `proc.kill()` (Hạ gục cưỡng chế - Chặn đứng lươn lẹo):**
  * Nếu sau 2.0 giây ứng dụng cố tình phớt lờ, treo đơ hoặc hiện hộp thoại câu giờ hỏi "Bạn có chắc muốn thoát không?", Agent lập tức gọi Win32 API gốc:
    $$	extbf{TerminateProcess(hProcess, uExitCode = 1)}$$
  * Hệ điều hành Windows lập tức thu hồi toàn bộ phân vùng bộ nhớ (Virtual Memory), giải phóng Handle và tiêu diệt tiến trình ngay lập tức ở mức nhân, không cho phép ứng dụng phản kháng!

---

# PHẦN 9: BẢO MẬT CẤP CAO F5, MÃ HÓA AES-256-GCM AEAD & TRIỆT TIÊU IDOR

### 9.1. Mã hóa xác thực dữ liệu kết hợp AEAD & Tiêu chuẩn AES-256-GCM

* **Hạn chế của các chế độ mã hóa cổ điển (ECB, CBC):**
  * Các chế độ mã hóa khối truyền thống như AES-CBC chỉ cung cấp tính **Bảo mật (Confidentiality)** — biến dữ liệu thành chuỗi vô nghĩa.
  * Tuy nhiên, chúng **không có tính Toàn vẹn (Integrity)**: Kẻ tấn công đứng ở giữa đường truyền có thể thực hiện tấn công lật bit (Bit-Flipping Attack) hoặc tấn công giải mã qua thông báo lỗi (Padding Oracle Attack) để thay đổi nội dung gói tin mà bên nhận không hề phát hiện!
* **Chuẩn AEAD (Authenticated Encryption with Associated Data) & AES-256-GCM:**
  * **AEAD** là tiêu chuẩn mật mã hiện đại bậc nhất, kết hợp đồng thời cả 2 mục tiêu: Vừa mã hóa bảo mật dữ liệu, vừa tạo ra một mã xác thực toàn vẹn (Authentication Tag).
  * **AES-256-GCM (Galois/Counter Mode):** Sử dụng khóa đối xứng độ dài 256 bits kết hợp thuật toán đếm Counter và phép nhân trường nhị phân Galois (Galois Field Multiplication). Tốc độ xử lý cực nhanh nhờ hỗ trợ tập lệnh tăng tốc phần cứng của CPU (Intel AES-NI) và miễn nhiễm hoàn toàn với các cuộc tấn công thám mã cổ điển.

---

### 9.2. Mổ xẻ cấu trúc bản tin mã hóa: Nonce 12 byte, Ciphertext & Auth Tag 16 byte (Chống Bit-Flipping)

Trong module `server/crypto_utils.py` của OGK, mọi dữ liệu viễn trắc nhạy cảm trước khi lưu đệm hoặc chuyển tiếp đều được đóng gói theo định dạng nhị phân chuẩn quốc tế:

```
+------------------+----------------------------------+-------------------+
|  Nonce (12 Bytes)|       Ciphertext (N Bytes)       | Auth Tag (16 Bytes)|
+------------------+----------------------------------+-------------------+
```

1. **Khóa bí mật Master Key ($K$ - 32 Bytes / 256 bits):** Lưu an toàn trong biến môi trường hệ thống của Server/Agent, không bao giờ gửi qua mạng.
2. **Số ngẫu nhiên dùng một lần Nonce / IV (12 Bytes / 96 bits):**
   * Được sinh ngẫu nhiên độc lập bằng bộ sinh số ngẫu nhiên an toàn mật mã của hệ điều hành: `os.urandom(12)`.
   * **Nguyên tắc sống còn của GCM:** Không bao giờ được dùng lại cùng một Nonce với cùng một Khóa bí mật. Việc dùng ngẫu nhiên 12 bytes đảm bảo xác suất trùng lặp là $rac{1}{2^{96}}$ (gần như bằng 0 trong suốt vòng đời vũ trụ).
3. **Bản mã Ciphertext ($N$ Bytes):** Nội dung dữ liệu gốc sau khi đi qua thuật toán mã hóa khối Counter.
4. **Mã xác thực toàn vẹn Authentication Tag (16 Bytes / 128 bits):**
   * Được tính toán dựa trên toàn bộ Bản mã và Nonce qua hàm nhân Galois.
   * **Cơ chế chống Bit-Flipping:** Khi bên nhận tiến hành giải mã, nếu kẻ tấn công sửa đổi dù chỉ **duy nhất 1 bit** trong Nonce hoặc Ciphertext, thuật toán tính lại Auth Tag sẽ cho kết quả sai lệch. Hàm giải mã lập tức ném ra ngoại lệ `InvalidTag` và hủy bỏ toàn bộ gói tin, ngăn chặn triệt để mọi hành vi tiêm mã độc hoặc giả mạo dữ liệu!

---

### 9.3. Lỗ hổng IDOR (Insecure Direct Object Reference) trong ứng dụng giám sát

* **Bản chất lỗ hổng IDOR:**
  * Xảy ra khi lập trình viên tin tưởng mù quáng vào định danh tài nguyên (như `device_id`, `kid_id`) do người dùng gửi lên từ Client mà không kiểm tra xem người dùng đó có thực sự sở hữu tài nguyên đó hay không.
  * **Kịch bản tấn công thực tế trong phần mềm gia đình:**
    * Phụ huynh A đăng nhập hợp lệ, nhận được JWT Token của Phụ huynh A.
    * Phụ huynh A mở giao diện xem máy con mình có `device_id = 1`.
    * Phụ huynh A sửa request trên thanh công cụ thành `GET /api/devices/2/activity-logs`.
    * Nếu Server chỉ kiểm tra "Người gửi có token JWT hợp lệ hay không?" $ightarrow$ Server trả về toàn bộ lịch sử lướt web của bé nhà Phụ huynh B! Đây là vi phạm nghiêm trọng luật riêng tư và chuẩn an toàn thông tin!

---

### 9.4. Cơ chế phòng thủ IDOR 2 lớp: Scope JWT + Ownership Check trong CSDL

OGK triệt tiêu 100% lỗ hổng IDOR trên mọi Endpoint nhạy cảm (`routes/devices.py`, `routes/rules.py`, `routes/alerts.py`) bằng mô hình kiểm soát truy cập dựa trên mối quan hệ (Relationship-Based Access Control):

```
Client Request -> [ LỚP 1: JWT Verification ] -> [ LỚP 2: CSDL Ownership Check ] -> Response
                  - Giải mã chữ ký Token          - device = db.get(device_id)
                  - Lấy parent_id từ payload      - IF device.parent_id != parent_id:
                  - Token hết hạn? -> 401           RAISE HTTPException(403 FORBIDDEN)
```

* **Mã nguồn thực thi chuẩn mẫu trong OGK:**
  ```python
  @router.get("/devices/{device_id}/rules")
  async def get_device_rules(
      device_id: int, 
      db: Session = Depends(get_db), 
      current_parent: Parent = Depends(get_current_parent)
  ):
      device = db.query(Device).filter(Device.id == device_id).first()
      if not device:
          raise HTTPException(status_code=404, detail="Thiết bị không tồn tại")
      
      # KIỂM TRA QUYỀN SỞ HỮU TRIỆT TIÊU IDOR
      if device.parent_id != current_parent.id:
          raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN, 
              detail="Truy cập bị từ chối: Thiết bị không thuộc tài khoản của bạn"
          )
      return device.rules
  ```
  * Nhờ cơ chế này, dù kẻ tấn công có đoán được toàn bộ ID của các máy con khác trong hệ thống, mọi yêu cầu can thiệp đều bị chặn đứng ở mức mã trạng thái `403 Forbidden` kèm ghi nhận cảnh báo an ninh vào Audit Log.

---

### 9.5. Phòng chống tấn công Brute-force & DoS: Khóa tài khoản 15 phút & IP Rate Limiting

* **Khóa tài khoản lũy tiến (Account Lockout Policy - Chuẩn NIST SP 800-63B):**
  * Kẻ tấn công sử dụng danh sách từ điển mật khẩu phổ biến để dò mật khẩu phụ huynh trên API `/api/auth/login`.
  * **Thuật toán xử lý của OGK:**
    * Bảng `parents` trong CSDL lưu 2 trường: `failed_login_attempts (int)` và `locked_until (datetime)`.
    * Mỗi lần đăng nhập thất bại, `failed_login_attempts += 1`.
    * Khi số lần sai chạm ngưỡng **5 lần liên tiếp**, hệ thống lập tức khóa tài khoản:  
      $$	ext{locked\_until} = 	ext{datetime.utcnow}() + 	ext{timedelta(minutes=15)}$$
    * Trong 15 phút này, mọi nỗ lực đăng nhập đúng hay sai đều bị từ chối ngay lập tức với mã lỗi `403 Account Locked`, làm nản lòng hoàn toàn các công cụ tấn công tự động.
* **Bộ đệm giới hạn tần suất theo IP (IP Rate Limiting Middleware):**
  * Sử dụng thuật toán Bộ xô rò rỉ (Leaky Bucket / Sliding Window) trên tầng Middleware của FastAPI.
  * Giới hạn tối đa **60 requests/phút** đối với mỗi địa chỉ IP Client. Nếu vượt ngưỡng, hệ thống trả về mã `429 Too Many Requests`, ngăn chặn triệt để tấn công từ chối dịch vụ (DoS) làm sập máy chủ.

---

# PHẦN 10: PHÁP LÝ NGHỊ ĐỊNH 13/2023/NĐ-CP, QUYỀN XÓA DỮ LIỆU & CHỊU LỖI NGOẠI TUYẾN M5

### 10.1. Chu kỳ lưu trữ dữ liệu (Data Retention Lifecycle) 90 ngày & Cron Job tự động Prune

* **Căn cứ pháp lý:**
  * **Điều 20 & Điều 21 Nghị định 13/2023/NĐ-CP:** Dữ liệu cá nhân của trẻ em chỉ được phép lưu trữ trong khoảng thời gian cần thiết để thực hiện mục đích đã đăng ký với cha mẹ; khi hết thời hạn bắt buộc phải xóa bỏ không thể khôi phục.
* **Cơ chế kỹ thuật trong OGK:**
  * Hệ thống thiết lập chu kỳ vòng đời dữ liệu tối đa là **90 ngày**.
  * Bảng `activity_logs`, `alert_logs` và `heartbeat_logs` được định kỳ quét dọn bằng một Cron Job chạy ngầm (hoặc hàm kích hoạt định kỳ trong `server/routes/retention.py`):
    ```sql
    DELETE FROM activity_logs WHERE timestamp < datetime('now', '-90 days');
    DELETE FROM alert_logs WHERE timestamp < datetime('now', '-90 days');
    ```
  * Sau lệnh xóa, hệ thống tự động kích hoạt lệnh `VACUUM;` trong SQLite để giải phóng dung lượng phân mảnh ổ cứng và ghi đè các sector bộ nhớ cũ, đảm bảo dữ liệu quá hạn không bao giờ bị trích xuất lại bằng các phần mềm phục hồi dữ liệu chuyên dụng.

---

### 10.2. Quyền được lãng quên (Right to Erasure): Quy trình xóa đồng bộ 2 chiều Server - Agent

* **Căn cứ pháp lý:**
  * Quyền được xóa dữ liệu cá nhân là một trong những quyền cơ bản của chủ thể dữ liệu theo Nghị định 13 và chuẩn GDPR. Khi cha mẹ cảm thấy con đã đủ lớn hoặc không muốn tiếp tục giám sát, hệ thống phải cung cấp cơ chế xóa sạch triệt để.
* **Quy trình xóa đồng bộ 2 chiều (2-Way Synchronous Purge):**
  1. **Bước 1 (Phụ huynh xác nhận):** Trên Dashboard, phụ huynh bấm nút *"Xóa toàn bộ dữ liệu thiết bị"* và nhập lại mật khẩu tài khoản để xác thực danh tính cấp cao.
  2. **Bước 2 (Gửi tín hiệu cưỡng chế qua WebSocket):** Server gửi gói tin sự kiện khẩn `{ "event": "DEVICE_PURGE", "device_id": X }` tới máy con đang kết nối.
  3. **Bước 3 (Thao tác dọn sạch trên Agent):**
     * Agent nhận lệnh, lập tức hủy phiên làm việc.
     * Xóa sạch tệp cơ sở dữ liệu đệm ngoại tuyến `agent_offline.db`.
     * Xóa bỏ khóa máy và hủy bỏ token ghép đôi `pairing_token`.
     * Tự động khôi phục cấu hình card mạng DNS về mặc định của nhà mạng (DHCP động).
  4. **Bước 4 (Cascade Delete dứt điểm trên Server):**
     * CSDL SQLite trên Server thực hiện xóa lan truyền (`ON DELETE CASCADE`): Xóa sạch bảng thiết bị `devices`, các bản ghi quy tắc `rules`, toàn bộ nhật ký `activity_logs` và lịch sử vi phạm.
     * Không giữ lại bất kỳ bản sao đệm ẩn nào (No Hidden Shadows).

---

### 10.3. Khả năng chịu lỗi và tự phục hồi M5: Mất mạng, Server crash & DNS Watchdog Netsh

Trong báo cáo chuyên đề mạng **M5 (Fault Tolerance & Network Resilience)**, OGK chứng minh khả năng vận hành bền bỉ qua 3 kịch bản sự cố thực tế:

* **Kịch bản M5.1: Mất kết nối mạng Internet hoặc mạng LAN (Network Disconnect):**
  * **Sự cố:** Dây mạng bị rút, router Wi-Fi bị tắt hoặc đường truyền Internet gia đình bị đứt.
  * **Cơ chế chịu lỗi của OGK:**
    * Vòng lặp đếm giờ đơn điệu `time.monotonic()` và tầng DNS Sinkhole Proxy trên Agent hoàn toàn **độc lập cục bộ (Local-Autonomous)**, không phụ thuộc vào Internet.
    * Mọi quy tắc cấm web, cấm game và giới hạn thời gian vẫn thực thi chuẩn xác từng giây.
    * Các bản ghi hoạt động thay vì gửi lên Server sẽ được lưu an toàn vào hàng đợi ngoại tuyến SQLite WAL cục bộ `agent_cache.db`.
    * Khi mạng có trở lại, Agent tự động kích hoạt cơ chế đồng bộ lũy tiến (Reconciliation Sync), đẩy toàn bộ dữ liệu đệm lên Server mà không làm mất một bản tin nào.

* **Kịch bản M5.2: Máy chủ bị treo hoặc đột ngột khởi động lại (Server Crash/Reboot):**
  * **Sự cố:** Máy tính phụ huynh bị tắt nguồn, dịch vụ FastAPI bị ngắt đột ngột.
  * **Thuật toán tự phục hồi (Exponential Backoff with Jitter):**
    * Kết nối WebSocket bị đứt (`ConnectionResetError`).
    * Agent không gửi request dồn dập làm nghẽn mạng (tránh bão kết nối Thundering Herd), mà áp dụng thuật toán lùi thời gian hàm mũ:
      $$T_{	ext{wait}} = \min(2^k + 	ext{random}(0, 1), 60	ext{ seconds})$$
      (Thử lại sau 2s, 4s, 8s, 16s... tối đa 60s).
    * Ngay khi Server khởi động lại thành công, Agent tự động tái kết nối, xác thực lại phiên và tiếp tục hoạt động trơn tru.

* **Kịch bản M5.3: Trẻ can thiệp cố tình đổi DNS card mạng về 8.8.8.8:**
  * **Sự cố:** Trẻ vào Network Adapter Settings của Windows hoặc chạy lệnh CMD để đổi DNS về Google `8.8.8.8` hòng vô hiệu hóa Sinkhole Proxy.
  * **Cơ chế tự phục hồi của DNS Watchdog (Chu kỳ 20s):**
    * Một luồng dịch vụ chạy ngầm `dns_watchdog.py` thức dậy mỗi **20 giây**.
    * Dùng lệnh `netsh interface ip show dns` để kiểm tra IP DNS hiện tại của các card mạng đang hoạt động.
    * Nếu phát hiện DNS bị trôi khỏi `127.0.0.1`, Watchdog lập tức:
      1. Kích hoạt quyền quản trị gọi lệnh cưỡng chế đặt lại:
         ```cmd
         netsh interface ip set dns name="Wi-Fi" static 127.0.0.1
         ```
      2. Xóa sạch bộ nhớ đệm DNS của Windows: `ipconfig /flushdns`.
      3. Phát sinh cảnh báo an ninh vi phạm gửi về Server lưu vào Audit Log.
    * Thời gian tối đa trẻ có thể "tận hưởng" mạng vượt rào chỉ là **20 giây** trước khi toàn bộ hệ thống bị cưỡng chế khóa lại!

---

# PHẦN 11: THỰC NGHIỆM ĐO LƯỜNG HIỆU NĂNG M4 & KHẮC CHẾ 7 KỸ THUẬT VƯỢT RÀO M3

### 11.1. Phương pháp đo kiểm thực nghiệm hiệu năng hệ thống M4 (RAM, CPU, DNS Latency, WebSocket)

Để đảm bảo tính khoa học và thuyết phục tuyệt đối trước Hội đồng chấm tốt nghiệp, mọi thông số hiệu năng của OGK không được ước lượng bằng lý thuyết mà phải được đo đạc bằng phương pháp thực nghiệm thống kê trên máy tính chạy Windows 11 thực tế:

* **Môi trường đo kiểm:**
  * Hệ điều hành: Microsoft Windows 11 Pro 64-bit.
  * Phần cứng: CPU Intel Core i5 / AMD Ryzen 5, RAM 16 GB, Ổ cứng NVMe SSD.
  * Công cụ đo: Thư viện `psutil` của Python, hàm bấm giờ chính xác cao `time.perf_counter_ns()`, công cụ bắt gói tin `Wireshark` và kịch bản đo đạc tự động `scripts/benchmark_performance.py`.
* **Phương pháp thu thập:**
  * Mỗi chỉ số được lấy mẫu lặp lại liên tục **30 lần độc lập ($N = 30$)** trong trạng thái hệ thống chịu tải thông thường và khi có sự kiện đẩy lệnh khẩn cấp.
  * Tính toán trung bình cộng ($\mu$), phương sai và độ lệch chuẩn ($\sigma$) để loại trừ các điểm dị biệt (Outliers).

---

### 11.2. Phân tích kết quả thực nghiệm M4: So sánh mục tiêu ban đầu vs Kết quả thực tế

Bảng tổng hợp đối soát số liệu thực nghiệm đo đạc trong Báo cáo chuyên đề M4:

| Chỉ số hiệu năng (Metrics) | Tiêu chuẩn cam kết đồ án (DoD Target) | Kết quả đo thực nghiệm thực tế ($N = 30$) | Đánh giá kỹ thuật & Kết luận |
| :--- | :--- | :--- | :--- |
| **Dung lượng RAM chiếm dụng (RSS)** | Phải nhỏ hơn $100	ext{ MB}$ | **25.13 MB** (Agent)<br>**38.40 MB** (Server) | **Vượt xa mục tiêu 4 lần.** Cực kỳ nhẹ, không ảnh hưởng đến việc học và chơi game của máy con. |
| **Mức tiêu thụ CPU trung bình** | Phải nhỏ hơn $5.0\%$ | **0.0%** (Lý tưởng)<br>*Đỉnh ngắn 0.12% khi quét tiến trình* | **Vượt mục tiêu 40 lần.** Nhờ giải thuật mtime Caching triệt tiêu hoàn toàn I/O đĩa đọc lặp lại. |
| **Độ trễ phân giải DNS nội bộ** | Phải nhỏ hơn $20	ext{ ms}$ | **0.83 ms** (Sinkhole Proxy)<br>*12.4 ms nếu Forward ra Internet* | **Nhanh gấp 24 lần cam kết.** Trải nghiệm lướt web của trẻ hoàn toàn mượt mà, không cảm nhận được độ trễ. |
| **Độ trễ truyền lệnh WebSocket** | Phải nhỏ hơn $1.0	ext{ giây}$ ($1000	ext{ ms}$) | **5.91 ms** (Trong mạng LAN)<br>**42.5 ms** (Qua mạng Internet) | **Phản hồi tức thì (Near Real-time).** Bấm nút trên Dashboard là máy con lập tức phản ứng ngay. |
| **Thời gian tự phục hồi DNS Watchdog**| Phải nhỏ hơn $30	ext{ giây}$ | **20.0 giây** (Chu kỳ quét đồng hồ) | Đảm bảo tính sẵn sàng cao, dập tắt mọi ý định chỉnh sửa card mạng của trẻ. |

---

### 11.3. Ma trận khắc chế toàn diện 7 kỹ thuật vượt rào kinh điển của học sinh (Anti-Bypass M3)

Trong báo cáo chuyên đề **M3 (Anti-Bypass Strategy)**, OGK chứng minh giải pháp đã dự liệu và vô hiệu hóa triệt để toàn bộ 7 chiêu trò lách luật tinh vi nhất mà học sinh thường dùng:

```
+----------------------------------------------------------------------------------------------------+
|                      MA TRẬN KHẮC CHẾ 7 KỸ THUẬT VƯỢT RÀO KINH ĐIỂN (M3)                           |
+----+----------------------------------+----------------------------------+-------------------------+
| STT| CHIÊU TRÒ VƯỢT RÀO CỦA TRẺ      | CƠ CHẾ BẢO VỆ CỦA OGK            | MODULE PHỤ TRÁCH        |
+----+----------------------------------+----------------------------------+-------------------------+
| 1  | Đổi tên file nhị phân (.exe)     | Băm nhị phân SHA-256 nội dung    | agent/app_monitor.py    |
|    | (vd: roblox.exe -> winword.exe)  | tệp trên đĩa cứng; tên đổi nhưng | (mtime cache 0.02ms)    |
|    |                                  | mã băm không đổi.                |                         |
+----+----------------------------------+----------------------------------+-------------------------+
| 2  | Chỉnh DNS card mạng Windows      | Dịch vụ ngầm DNS Watchdog quét   | agent/dns_watchdog.py   |
|    | (Chuyển sang 8.8.8.8 hoặc 1.1.1.1)| chu kỳ 20s, dùng netsh cưỡng chế | (Windows netsh utility) |
|    |                                  | đặt lại 127.0.0.1 và flushdns.   |                         |
+----+----------------------------------+----------------------------------+-------------------------+
| 3  | Bật DNS mã hóa DoH / DoT trong   | Trả về NXDOMAIN cho Canary Domain| agent/dns_proxy.py      |
|    | trình duyệt (Chrome, Edge, Fire) | use-application-dns.net, cưỡng   | (RFC 1035 NXDOMAIN code)|
|    |                                  | chế trình duyệt tắt DoH.         |                         |
+----+----------------------------------+----------------------------------+-------------------------+
| 4  | Dùng phần mềm VPN / UltraSurf    | Danh mục mã băm SHA-256 cấm VPN; | agent/app_monitor.py &  |
|    | để đổi IP và vượt tường lửa      | Chặn cổng DoT 853; khóa máy nếu  | agent/dns_proxy.py      |
|    |                                  | phát hiện card mạng TAP/TUN ảo.  |                         |
+----+----------------------------------+----------------------------------+-------------------------+
| 5  | Tua lùi đồng hồ hệ thống Windows | Lõi đếm giờ dùng time.monotonic()| agent/time_tracker.py   |
|    | (Clock Tampering lúc 21h -> 15h) | từ phần cứng CPU, độc lập 100%   | (Hardware Tick Counter) |
|    |                                  | với đồng hồ lịch máy tính.       |                         |
+----+----------------------------------+----------------------------------+-------------------------+
| 6  | Mở Task Manager bấm "End Task"   | Chạy tiến trình nền dưới quyền   | agent/service_manager.py|
|    | hoặc tắt tiến trình Agent        | LocalSystem ở Session 0, Standard| (Session 0 Isolation &  |
|    |                                  | User bị Windows Access Denied.   | Service Auto-Recovery)  |
+----+----------------------------------+----------------------------------+-------------------------+
| 7  | Dùng tab Ẩn danh (Incognito)     | DNS Sinkhole can thiệp ở tầng    | agent/dns_proxy.py      |
|    | hoặc đổi sang tài khoản phụ      | Socket OS cổng 53; mọi tab ẩn danh| (Cưỡng chế SafeSearch   |
|    |                                  | vẫn phải đi qua 127.0.0.1:53.    | Google/YouTube VIP)     |
+----+----------------------------------+----------------------------------+-------------------------+
```

* **Kết luận khoa học:** Toàn bộ hệ thống tạo thành một mạng lưới bảo vệ khép kín đa tầng (Defense-in-Depth). Không có bất kỳ kẽ hở đơn lẻ nào có thể giúp một đứa trẻ dù am hiểu máy tính có thể tự ý phá rào mà không có sự đồng thuận chính thức từ phụ huynh.
