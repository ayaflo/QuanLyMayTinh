# CẨM NANG KIẾN THỨC TOÀN DIỆN VỀ HỆ THỐNG OPEN GUARDIAN KIDS (OGK)
## TÀI LIỆU BÁCH KHOA CHUYÊN ĐỀ TỐT NGHIỆP: MẠNG MÁY TÍNH & TRUYỀN THÔNG DỮ LIỆU

> **Mục đích tài liệu:**  
> Cung cấp nền tảng kiến thức lý thuyết và thực tiễn chuyên sâu bao trùm toàn bộ 20 slide báo cáo đồ án tốt nghiệp. Giúp sinh viên nắm vững từng khái niệm kỹ thuật cốt lõi (VPN, Tường lửa, DNS, WebSocket, Session 0, Argon2id, SQLite WAL, Win32 Hook...), hiểu rõ vai trò và ý nghĩa của chúng trong dự án, tự tin giải trình và bảo vệ xuất sắc trước Hội đồng phản biện.

---

# MỤC LỤC TỔNG QUAN

- [PHẦN 1: MẠNG MÁY TÍNH & CÁC CƠ CHẾ ĐIỀU PHỐI GÓI TIN](#phần-1-mạng-máy-tính--các-cơ-chế-điều-phối-gói-tin)
  - [1.1. DNS (Domain Name System) & Cơ chế phân giải tên miền](#11-dns-domain-name-system--cơ-chế-phân-giải-tên-miền)
  - [1.2. DNS Sinkholing (Hố đen DNS) - Trọng tâm lọc web của OGK](#12-dns-sinkholing-hố-đen-dns---trọng-tâm-lọc-web-của-ogk)
  - [1.3. DoH (DNS-over-HTTPS) & DoT (DNS-over-TLS)](#13-doh-dns-over-https--dot-dns-over-tls)
  - [1.4. Canary Domain (`use-application-dns.net`) - Cơ chế khắc chế DoH](#14-canary-domain-use-application-dnsnet---cơ-chế-khắc-chế-doh)
  - [1.5. Cổng truyền thông (Ports): Cổng 53, 853, 443, 8000](#15-cổng-truyền-thông-ports-cổng-53-853-443-8000)
  - [1.6. Wireshark & Kỹ thuật bắt gói tin kiểm chứng thực nghiệm](#16-wireshark--kỹ-thuật-bắt-gói-tin-kiểm-chứng-thực-nghiệm)
  - [1.7. Tường lửa (Firewall) & Vai trò trong dự án](#17-tường-lửa-firewall--vai-trò-trong-dự-án)
  - [1.8. VPN (Virtual Private Network) & Cơ chế chặn VPN bằng SHA-256](#18-vpn-virtual-private-network--cơ-chế-chặn-vpn-bằng-sha-256)
- [PHẦN 2: GIAO THỨC TRUYỀN THÔNG ỨNG DỤNG (REST API vs WEBSOCKET)](#phần-2-giao-thức-truyền-thông-ứng-dụng-rest-api-vs-websocket)
  - [2.1. RESTful API (HTTP/1.1) là gì?](#21-restful-api-http11-là-gì)
  - [2.2. WebSocket là gì?](#22-websocket-là-gì)
  - [2.3. BÀI TOÁN CỐT LÕI: Tại sao kết hợp cả REST API và WebSocket mà không dùng 1 cái?](#23-bài-toán-cốt-lõi-tại-sao-kết-hợp-cả-rest-api-và-websocket-mà-không-dùng-1-cái)
  - [2.4. FastAPI & Kiến trúc bất đồng bộ (Asynchronous / Event Loop)](#24-fastapi--kiến-trúc-bất-đồng-bộ-asynchronous--event-loop)
- [PHẦN 3: KIẾN TRÚC LƯU TRỮ CƠ SỞ DỮ LIỆU & BỘ ĐỆM](#phần-3-kiến-trúc-lưu-trữ-cơ-sở-dữ-liệu--bộ-đệm)
  - [3.1. BÀI TOÁN CỐT LÕI: Dữ liệu được lưu ở đâu? (Server DB vs Client Cache DB vs Dashboard)](#31-bài-toán-cốt-lõi-dữ-liệu-được-lưu-ở-đâu-server-db-vs-client-cache-db-vs-dashboard)
  - [3.2. CSDL SQLite: Tại sao chọn SQLite mà không dùng PostgreSQL/MySQL?](#32-csdl-sqlite-tại-sao-chọn-sqlite-mà-không-dùng-postgresqlmysql)
  - [3.3. SQLite WAL Mode (Write-Ahead Logging) là gì?](#33-sqlite-wal-mode-write-ahead-logging-là-gì)
  - [3.4. Cơ chế lưu đệm ngoại tuyến (Offline-First Storage) của Agent](#34-cơ-chế-lưu-đệm-ngoại-tuyến-offline-first-storage-của-agent)
- [PHẦN 4: LẬP TRÌNH HỆ ĐIỀU HÀNH WINDOWS & WIN32 KERNEL](#phần-4-lập-trình-hệ-điều-hành-windows--win32-kernel)
  - [4.1. Rào cản Session 0 Isolation trên Windows là gì?](#41-rào-cản-session-0-isolation-trên-windows-là-gì)
  - [4.2. IPC (Inter-Process Communication) & Token bảo mật nội bộ](#42-ipc-inter-process-communication--token-bảo-mật-nội-bộ)
  - [4.3. Đồng hồ đơn điệu `time.monotonic()` vs `time.time()` & Lỗ hổng tua giờ](#43-đồng-hồ-đơn-điệu-timemonotonic-vs-timetime--lỗ-hổng-tua-giờ)
  - [4.4. Win32 API `GetLastInputInfo` & Thuật toán nhận diện máy rảnh (Idle Detection)](#44-win32-api-getlastinputinfo--thuật-toán-nhận-diện-máy-rảnh-idle-detection)
  - [4.5. Win32 API `LockWorkStation` & Triết lý khóa máy an toàn](#45-win32-api-lockworkstation--triết-lý-khóa-máy-an-toàn)
  - [4.6. Phân quyền tài khoản Windows: LocalSystem vs Standard User](#46-phân-quyền-tài-khoản-windows-localsystem-vs-standard-user)
  - [4.7. Win32 Hook `SetWindowsHookEx`: Cơ chế Keylogger an toàn phục vụ phân tích từ khóa nguy cơ](#47-win32-hook-setwindowshookex-cơ-chế-keylogger-an-toàn-phục-vụ-phân-tích-từ-khóa-nguy-cơ)
- [PHẦN 5: MẬT MÃ HỌC & BẢO MẬT HỆ THỐNG THỜI GIAN THỰC](#phần-5-mật-mã-học--bảo-mật-hệ-thống-thời-gian-thực)
  - [5.1. Thuật toán băm mật khẩu Argon2id](#51-thuật-toán-băm-mật-khẩu-argon2id)
  - [5.2. Chữ ký toàn vẹn HMAC-SHA256 (Anti-Tamper)](#52-chữ-ký-toàn-vẹn-hmac-sha256-anti-tamper)
  - [5.3. Tấn công phân tích thời gian (Timing Attack) & So sánh hằng số thời gian](#53-tấn-công-phân-tích-thời-gian-timing-attack--so-sánh-hằng-số-thời-gian)
  - [5.4. JSON Web Token (JWT) & Quản lý phiên](#54-json-web-token-jwt--quản-lý-phiên)
  - [5.5. Cờ bảo mật Cookie: `HttpOnly` và `SameSite=Lax`](#55-cờ-bảo-mật-cookie-httponly-và-samesitelax)
  - [5.6. Chống tấn công phát lại (Anti-Replay Attack) & TTL](#56-chống-tấn-công-phát-lại-anti-replay-attack--ttl)
  - [5.7. Mô hình đe dọa STRIDE trong dự án OGK](#57-mô-hình-đe-dọa-stride-trong-dự-án-ogk)
- [PHẦN 6: PHÁP LÝ & ĐẠO ĐỨC CÔNG NGHỆ BẢO VỆ TRẺ EM](#phần-6-pháp-lý--đạo-đức-công-nghệ-bảo-vệ-trẻ-em)
  - [6.1. Nghị định 13/2023/NĐ-CP (Điều 20)](#61-nghị-định-132023nđ-cp-điều-20)
  - [6.2. Luật Trẻ Em 2016 (Điều 21) & Quyền riêng tư](#62-luật-trẻ-em-2016-điều-21--quyền-riêng-tư)
  - [6.3. Chuẩn mực NIST SP 800-63B & OWASP ASVS v4](#63-chuẩn-mực-nist-sp-800-63b--owasp-asvs-v4)

---

# PHẦN 1: MẠNG MÁY TÍNH & CÁC CƠ CHẾ ĐIỀU PHỐI GÓI TIN

### 1.1. DNS (Domain Name System) & Cơ chế phân giải tên miền
* **Khái niệm cơ bản:** DNS là "danh bạ điện thoại" của mạng Internet. Con người nhớ địa chỉ trang web bằng tên miền dễ đọc (ví dụ `google.com`, `facebook.com`), nhưng các thiết bị mạng giao tiếp với nhau bằng địa chỉ IP (ví dụ `142.250.190.46`). DNS có nhiệm vụ ánh xạ tên miền thành địa chỉ IP.
* **Quy trình chuẩn khi duyệt web:**
  1. Người dùng gõ `vnexpress.net` trên trình duyệt.
  2. Hệ điều hành kiểm tra DNS cache cục bộ và tệp `hosts`.
  3. Nếu không có, máy tính gửi gói tin DNS Query (qua cổng UDP 53) đến DNS Server cấu hình trên máy.
  4. DNS Server trả về gói tin DNS Response chứa địa chỉ IP của web server.
  5. Trình duyệt gửi gói tin TCP SYN đến IP đó trên cổng 443 để bắt tay TLS (HTTPS) và tải trang web.
* **Ý nghĩa trong dự án OGK:**  
  DNS là "cửa ngõ đầu tiên" mà bất kỳ ứng dụng nào (Chrome, Firefox, Game, Discord...) cũng phải đi qua trước khi có thể kết nối Internet. Do đó, kiểm soát DNS là phương pháp tối ưu nhất để lọc web mà không cần giải mã nội dung HTTPS.

---

### 1.2. DNS Sinkholing (Hố đen DNS) - Trọng tâm lọc web của OGK
* **Khái niệm:** DNS Sinkholing là kỹ thuật đánh chặn truy vấn DNS và trả về một địa chỉ IP giả mạo hoặc địa chỉ vô hiệu hóa (Sinkhole) thay vì địa chỉ IP thật của máy chủ mục tiêu.
* **Cách OGK hiện thực (Module M1):**
  * OGK cấu hình card mạng Windows trỏ DNS chính về địa chỉ nội bộ `127.0.0.1:53`.
  * Trên máy con, tác tử Agent lắng nghe cổng UDP 53 bằng thư viện `dnslib`.
  * Khi có truy vấn DNS:
    * Nếu tên miền **HỢP LỆ**: Agent chuyển tiếp (forward) truy vấn lên DNS tin cậy của phụ huynh (hoặc 1.1.1.1) và trả kết quả cho trình duyệt.
    * Nếu tên miền **BỊ CẤM** (nằm trong Blacklist): Agent lập tức đóng gói một phản hồi DNS giả mạo với địa chỉ IP `0.0.0.0` (hoặc `127.0.0.1`).
* **Tại sao trả về `0.0.0.0`?**
  * `0.0.0.0` là địa chỉ IP không định tuyến được (Non-routable meta-address). Khi trình duyệt nhận IP này, nó lập tức nhận lỗi kết nối trong vòng chưa đầy **1 mili-giây**, không tiêu tốn tài nguyên mạng và không thể tải bất kỳ nội dung nào từ web đen.
  * Toàn bộ quá trình chặn diễn ra **TRƯỚC KHI** bắt tay mã hóa TLS/HTTPS, do đó không cần cài đặt chứng chỉ bảo mật giả mạo (Root CA) và không xâm phạm quyền riêng tư của trẻ (tuân thủ nguyên tắc NT2).

---

### 1.3. DoH (DNS-over-HTTPS) & DoT (DNS-over-TLS)
* **Khái niệm:**
  * **DNS truyền thống:** Truyền tải dưới dạng văn bản thuần (Clear-text) qua giao thức UDP trên cổng 53, rất dễ bị bắt gói tin và can thiệp.
  * **DoT (DNS-over-TLS):** Đóng gói truy vấn DNS trong đường hầm mã hóa TLS trên cổng riêng **TCP 853**.
  * **DoH (DNS-over-HTTPS):** Đóng gói truy vấn DNS vào các bản tin HTTP/2 hoặc HTTP/3 mã hóa HTTPS trên cổng **TCP 443** (trùng với cổng duyệt web thông thường).
* **Mặt trái của DoH đối với phần mềm quản lý gia đình:**
  * Trình duyệt như Google Chrome và Mozilla Firefox hiện nay có tính năng tự động bật DoH (Secure DNS).
  * Khi DoH được bật, trình duyệt bỏ qua hoàn toàn DNS của hệ điều hành (bỏ qua `127.0.0.1:53` của OGK), gửi thẳng truy vấn DNS mã hóa qua cổng 443 đến máy chủ Cloudflare (`1.1.1.1`) hoặc Google (`8.8.8.8`). Điều này khiến bộ lọc DNS thông thường bị vô hiệu hóa hoàn toàn (trẻ vượt rào dễ dàng).

---

### 1.4. Canary Domain (`use-application-dns.net`) - Cơ chế khắc chế DoH
* **Khái niệm:** Để giải quyết bài toán các mạng nội bộ doanh nghiệp và trường học bị mất kiểm soát chính sách khi trình duyệt tự ý bật DoH, tổ chức **Mozilla Firefox** (2019) và **Google Chromium** đã ban hành tiêu chuẩn tên miền chim yến (Canary Domain): `use-application-dns.net`.
* **Cơ chế hoạt động:**
  * Khi trình duyệt khởi động, trước khi tự động kích hoạt DoH, nó sẽ gửi một truy vấn DNS thông thường (qua cổng UDP 53) để hỏi IP của tên miền `use-application-dns.net`.
  * Nếu DNS Server trả về mã lỗi **`NXDOMAIN` (Non-Existent Domain - Tên miền không tồn tại)**: Trình duyệt hiểu rằng mạng máy tính này có chính sách quản trị riêng và **TỰ ĐỘNG TẮT DoH**, quay trở về sử dụng DNS cổng 53 của hệ điều hành!
* **Ý nghĩa trong dự án OGK (Module M3):**
  * Module DNS Proxy của OGK được lập trình để chặn bắt tên miền `use-application-dns.net` và luôn luôn trả về mã lỗi `NXDOMAIN`.
  * Nhờ vậy, ngay khi đứa trẻ mở Chrome hoặc Firefox, trình duyệt sẽ tự động vô hiệu hóa DoH mà không cần phụ huynh phải can thiệp thủ công vào phần cài đặt phức tạp của trình duyệt.

---

### 1.5. Cổng truyền thông (Ports): Cổng 53, 853, 443, 8000
Trong mạng máy tính, Cổng (Port) là điểm cuối logic để phân biệt các dịch vụ mạng khác nhau chạy trên cùng một địa chỉ IP:
* **Cổng 53 (UDP/TCP) - DNS chuẩn:**
  * Sử dụng cho truy vấn DNS thông thường. OGK-Agent chiếm dụng cổng này trên loopback (`127.0.0.1:53`) để làm DNS Sinkhole.
* **Cổng 853 (TCP) - DNS-over-TLS (DoT):**
  * Dùng cho DNS mã hóa TLS. OGK xử lý nguy cơ trẻ dùng DoT bằng cách cấu hình Windows Firewall chặn toàn bộ lưu lượng ra ngoài qua cổng TCP 853.
* **Cổng 443 (TCP) - HTTPS & DoH:**
  * Cổng duyệt web an toàn. Mọi dữ liệu web được mã hóa TLS.
* **Cổng 8000 (TCP) - OGK Server API & WebSocket:**
  * Cổng dịch vụ của FastAPI trên máy chủ gia đình, phục vụ cả REST API (đăng nhập, ghép đôi, nhịp tim) và kết nối WebSocket song công (`/ws/device/{id}`).

---

### 1.6. Wireshark & Kỹ thuật bắt gói tin kiểm chứng thực nghiệm
* **Wireshark là gì?** Wireshark là công cụ phân tích giao thức mạng (Packet Sniffer) tiêu chuẩn công nghiệp, cho phép bắt và mổ xẻ chi tiết từng byte của các gói tin truyền qua card mạng.
* **Vai trò trong đề tài tốt nghiệp:**
  * Khẳng định tính khoa học thực nghiệm: Nhóm không chỉ "nói bằng miệng" là đã chặn được mạng, mà dùng Wireshark bắt gói tin thực tế trên card mạng máy con (Adapter loopback & Wi-Fi).
  * Minh chứng rõ ràng: Khi trẻ gõ tên miền cấm, Wireshark ghi nhận gói `DNS Standard Query` gửi đi và gói `DNS Standard Response` trả về địa chỉ IP `0.0.0.0` chỉ sau 1.2ms. Bắt tay TLS bị dập tắt ngay từ đầu.

---

### 1.7. Tường lửa (Firewall) & Vai trò trong dự án
* **Khái niệm:** Tường lửa là rào chắn an ninh mạng kiểm soát và lọc các luồng dữ liệu vào/ra (Inbound/Outbound traffic) dựa trên bộ quy tắc đã thiết lập (IP nguồn, IP đích, Cổng, Giao thức).
* **Ứng dụng trong OGK:**
  * OGK-Agent sử dụng công cụ dòng lệnh `netsh advfirewall` để thiết lập các quy tắc tường lửa tự động của Windows:
    1. Chặn cổng TCP 853 để cấm tuyệt đối DoT.
    2. Chặn các dải IP của các máy chủ DNS công cộng nổi tiếng (như `8.8.8.8`, `1.1.1.1`) khi gửi trực tiếp qua cổng 53 để ngăn trẻ tự ý sửa cấu hình mạng máy con sang DNS ngoài.

---

### 1.8. VPN (Virtual Private Network) & Cơ chế chặn VPN bằng SHA-256
* **VPN là gì?** Mạng riêng ảo (VPN) tạo ra một đường hầm mã hóa (Encrypted Tunnel) từ máy tính của người dùng đến một máy chủ VPN ở xa. Mọi gói tin (kể cả truy vấn DNS và dữ liệu web) đều bị mã hóa và đóng gói (Encapsulation) chui qua cổng 443 hoặc cổng UDP ngẫu nhiên.
* **Tại sao VPN qua mặt được DNS Proxy?**
  * Khi bật VPN, phần mềm VPN cài một card mạng ảo (Virtual TAP/TUN Adapter). Toàn bộ dữ liệu của máy con được đẩy thẳng vào đường hầm VPN ra nước ngoài mà không đi qua socket `127.0.0.1:53` của OGK.
* **Giải pháp của OGK (Tuần 3 & Slide 18):**
  * Vì lưu lượng VPN đã bị mã hóa nên không thể lọc ở tầng gói tin mạng thông thường; OGK tiếp cận bài toán từ **Tầng Hệ Điều Hành**:
  * Agent giám sát danh sách tiến trình đang chạy bằng `psutil`. Khi phát hiện các tệp thực thi của VPN (hoặc mã băm SHA-256 trùng với danh sách phần mềm VPN như Hotspot Shield, ProtonVPN, 1.1.1.1 Warp...), Agent lập tức gọi API `process.terminate()` để chấm dứt ngay tiến trình, vô hiệu hóa đường hầm VPN.

---

# PHẦN 2: GIAO THỨC TRUYỀN THÔNG ỨNG DỤNG (REST API vs WEBSOCKET)

### 2.1. RESTful API (HTTP/1.1) là gì?
* **Đặc tính:** Hoạt động theo mô hình Yêu cầu - Phản hồi (Request - Response). Client chủ động gửi yêu cầu, Server xử lý và trả về kết quả rồi đóng hoặc tái sử dụng kết nối. Có tính chất phi trạng thái (Stateless).
* **Ưu điểm:** Chuẩn hóa cao, dễ dàng kiểm thử, tích hợp bộ nhớ đệm (Caching), dễ phân quyền với JWT và Cookie HttpOnly, tài nguyên được giải phóng ngay sau mỗi request.

---

### 2.2. WebSocket là gì?
* **Đặc tính:** Giao thức truyền thông hai chiều song công (Full-Duplex), bắt đầu bằng một cú bắt tay HTTP Upgrade và sau đó duy trì một kết nối TCP liên tục giữa Client và Server.
* **Ưu điểm:** Độ trễ cực thấp (dưới vài chục mili-giây), cả Server và Client đều có thể chủ động đẩy (Push) dữ liệu cho nhau bất kỳ lúc nào mà không cần bên kia phải gửi yêu cầu trước.

---

### 2.3. BÀI TOÁN CỐT LÕI: Tại sao kết hợp cả REST API và WebSocket mà không dùng 1 cái?
* **❓ Câu hỏi của Thầy:** *"Tại sao không dùng luôn WebSocket cho tất cả mọi thứ từ đăng nhập, gửi nhịp tim cho đến khóa máy cho nhanh, mà lại phải vừa dùng REST API vừa dùng WebSocket?"*
* **💡 Luận chứng kỹ thuật chuyên sâu:**
  1. **Tối ưu tài nguyên Server & Khả năng chịu tải (Scalability):**
     * Kết nối WebSocket yêu cầu Server phải duy trì một Socket TCP mở liên tục trong bộ nhớ RAM (Connection State). Nếu dùng WebSocket cho hàng ngàn máy con gửi những tác vụ định kỳ đơn giản, Server sẽ bị tiêu tốn RAM để duy trì các kết nối nhàn rỗi.
     * REST API là Stateless: Gói tin gửi nhịp tim (Heartbeat 60s/lần) chỉ tốn một kết nối trong khoảng 10ms rồi giải phóng ngay, giúp Server phục vụ hàng ngàn thiết bị một cách nhẹ nhàng.
  2. **Bảo mật xác thực & Chuẩn hóa giao thức (Authentication & Security):**
     * REST API có các tiêu chuẩn bảo mật phiên cực kỳ hoàn chỉnh: Xác thực đa tầng với Cookie `HttpOnly=True`, `SameSite=Lax`, cơ chế Refresh Token, Rate Limiting (giới hạn 5 lần/phút chống Brute-Force) và kiểm soát lỗi HTTP Status Code chuẩn (401 Unauthorized, 403 Forbidden).
     * Bắt đầu phiên bằng REST API (Đăng nhập, Ghép đôi 8 ký tự) giúp bảo vệ hệ thống vững chắc theo chuẩn OWASP ASVS v4.
  3. **Đúng vai trò - Đúng công cụ:**
     * **REST API:** Đảm nhận các tác vụ nghiệp vụ có chu kỳ hoặc cần xác thực cao (Đăng nhập, Tạo mã ghép đôi, Gửi nhịp tim 60s, Lấy danh sách thiết bị).
     * **WebSocket:** Chỉ mở cho kênh khẩn cấp tức thời (`/ws/device/{id}`) để phục vụ các tình huống phụ huynh cần **ra lệnh tức thời** (Bấm nút "Khóa ngay", "Mở khóa", "Thêm 15 phút"). Nhờ đó lệnh đến máy con chỉ mất **0.8 giây** thay vì phải đợi 60 giây của chu kỳ nhịp tim tiếp theo!

---

### 2.4. FastAPI & Kiến trúc bất đồng bộ (Asynchronous / Event Loop)
* **FastAPI là gì?** Là framework backend hiện đại bậc nhất của Python, dựa trên Starlette và Pydantic, hỗ trợ lập trình bất đồng bộ (`async`/`await`) gốc trên nền tảng ASGI Web Server (Uvicorn).
* **Cơ chế Event Loop:**
  * Trong các framework truyền thống (như Django hay Flask chuẩn WSGI), mỗi request đến sẽ chiếm dụng một Thread riêng (Thread-per-request). Khi Thread đó phải đợi I/O (chờ ghi file, chờ database), Thread bị đóng băng (blocking), dẫn đến nghẽn cổ chai khi số lượng kết nối tăng cao.
  * FastAPI sử dụng Event Loop đơn luồng bất đồng bộ: Khi một request đang chờ I/O, Event Loop lập tức chuyển sang phục vụ request khác. Nhờ vậy, một tiến trình FastAPI có thể xử lý hàng ngàn kết nối WebSocket và HTTP đồng thời với lượng RAM chỉ khoảng **30MB**!

---

# PHẦN 3: KIẾN TRÚC LƯU TRỮ CƠ SỞ DỮ LIỆU & BỘ ĐỆM

### 3.1. BÀI TOÁN CỐT LÕI: Dữ liệu được lưu ở đâu? (Server DB vs Client Cache DB vs Dashboard)
Hệ thống OGK phân tách rõ ràng **3 cấp độ lưu trữ** tương ứng với 3 thành phần kiến trúc:

| Vị trí lưu trữ | Công nghệ | Dữ liệu quản lý | Mục đích & Đặc tính |
| :--- | :--- | :--- | :--- |
| **1. Máy chủ Server** | SQLite (WAL mode) `server/ogk_server.db` | Tài khoản phụ huynh (Argon2id), Danh sách thiết bị ghép đôi, Mã pairing, Chính sách tổng thể (Quota, Ma trận 7×48), Toàn bộ nhật ký kiểm toán (Audit Logs). | **Nguồn chân lý duy nhất (Single Source of Truth).** Dữ liệu được bảo vệ an toàn, chỉ phụ huynh có quyền truy cập qua JWT. |
| **2. Máy con của trẻ (Agent)** | SQLite cục bộ `agent/agent_cache.db` | Device ID, Access Token riêng, Bản sao chính sách mới nhất kèm chữ ký HMAC, Số giây đã dùng trong ngày (`used_seconds`), Hàng đợi sự kiện ngoại tuyến (Offline Event Queue). | **Lưu trữ đệm bền vững (Persistent Cache).** Đảm bảo Agent vẫn thực thi luật đếm giờ và khóa máy chuẩn xác ngay cả khi bị mất mạng hoặc khởi động lại máy tính. |
| **3. Trình duyệt Phụ huynh (Dashboard)** | HTML5 SessionStorage / Cookie | Access Token phiên làm việc (HttpOnly Cookie), Bộ đệm giao diện hiển thị tức thời (UI State). | Không lưu dữ liệu dài hạn; toàn bộ số liệu được kéo từ Server về mỗi khi mở trang hoặc nhận qua WebSocket. |

---

### 3.2. CSDL SQLite: Tại sao chọn SQLite mà không dùng PostgreSQL/MySQL?
* **❓ Câu hỏi của Thầy:** *"Tại sao đồ án tốt nghiệp không dùng hệ quản trị CSDL chuyên nghiệp như PostgreSQL hay MySQL mà lại dùng SQLite?"*
* **💡 Luận chứng kỹ thuật:**
  1. **Triết lý triển khai tại gia đình (Zero-Configuration):**
     * Mục tiêu của OGK là một ứng dụng gia đình mà một người phụ huynh bình thường có thể cài đặt sạch trong vòng 1 phút. Nếu dùng PostgreSQL hay MySQL, phụ huynh phải cài thêm dịch vụ CSDL nặng nề, cấu hình cổng mạng, tài khoản `root`, phân quyền người dùng... cực kỳ phức tạp và dễ phát sinh lỗi.
  2. **Hiệu năng vượt trội trong môi trường nhúng/cục bộ:**
     * SQLite là một thư viện C tự chứa (In-process database), không có độ trễ truyền thông liên tiến trình (IPC) hay mạng (Network socket overhead) như PostgreSQL/MySQL. Mọi truy vấn diễn ra trực tiếp trên bộ nhớ và tệp tin đĩa với tốc độ hàng micro-giây.
  3. **Tài nguyên siêu nhẹ:**
     * SQLite chỉ tốn vài MB bộ nhớ RAM, hoàn toàn phù hợp để chạy bền bỉ 24/7 trên máy chủ gia đình hoặc cả máy tính con mà không làm chậm máy.

---

### 3.3. SQLite WAL Mode (Write-Ahead Logging) là gì?
* **Vấn đề của SQLite mặc định (Rollback Journal):**
  * Ở chế độ mặc định, khi một tiến trình đang ghi dữ liệu vào CSDL, toàn bộ tệp database bị khóa độc quyền (Exclusive Lock). Mọi tiến trình khác muốn đọc dữ liệu đều phải chờ (gây lỗi `database is locked`).
* **Đột phá của chế độ WAL (`PRAGMA journal_mode=WAL`):**
  * Thay vì ghi trực tiếp vào tệp chính, các thao tác ghi mới được ghi nối tiếp vào một tệp nhật ký riêng (`.wal`).
  * **Đọc và ghi hoàn toàn song song:** Các tiến trình đọc dữ liệu đọc từ bản snapshot ổn định và tệp WAL mà không hề bị chặn bởi tiến trình đang ghi, và ngược lại.
  * Giúp Server OGK xử lý nhịp tim từ nhiều máy con gửi về cùng lúc mà không bao giờ gặp hiện tượng nghẽn CSDL.

---

### 3.4. Cơ chế lưu đệm ngoại tuyến (Offline-First Storage) của Agent
* Khi trẻ rút dây mạng hoặc ngắt Wi-Fi, Agent không bị tê liệt.
* Agent tiếp tục đếm giờ bằng `time.monotonic()`, lưu tiến độ vào bảng `daily_usage` trong `agent_cache.db`.
* Nếu có sự kiện vi phạm (như trẻ cố tình đổi giờ hoặc cố truy cập tệp cấm), sự kiện được lưu vào bảng `offline_events`.
* Ngay khi có mạng trở lại, Agent tự động kích hoạt luồng đồng bộ đẩy các sự kiện ngoại tuyến lên Server theo cơ chế lũy đẳng (Idempotent), bảo đảm không bị mất dữ liệu viễn trắc.

---

# PHẦN 4: LẬP TRÌNH HỆ ĐIỀU HÀNH WINDOWS & WIN32 KERNEL

### 4.1. Rào cản Session 0 Isolation trên Windows là gì?
* **Lịch sử & Bản chất:** Kể từ Windows Vista và Windows Server 2008, Microsoft áp dụng kiến trúc **Session 0 Isolation** để ngăn chặn các cuộc tấn công Shatter Attack. Theo đó, tất cả các Windows Service chạy nền được đưa vào **Session 0**, trong khi các phiên người dùng đăng nhập tương tác (Desktop, màn hình làm việc) chạy từ **Session 1 trở đi**.
* **Hậu quả kỹ thuật:** Một tiến trình chạy dưới dạng Windows Service trong Session 0 **HOÀN TOÀN KHÔNG THỂ** vẽ giao diện đồ họa, không thể hiện cửa sổ, không thể hiện Icon khay hệ thống (System Tray) lên màn hình của người dùng ở Session 1.
* **Giải pháp kiến trúc 2 tiến trình của OGK:**
  1. **Tiến trình Dịch vụ Nền (Background Service - Session 0):** Chạy quyền `LocalSystem`, thực hiện các tác vụ nặng: Lắng nghe cổng mạng 53, đếm giờ phần cứng, gọi API khóa máy, nhận lệnh WebSocket.
  2. **Tiến trình Giao diện Khay (Tray UI - Session 1):** Chạy trong phiên làm việc của người dùng bằng thư viện `Pystray`, có nhiệm vụ hiển thị Icon lá chắn, hiển thị thông báo Balloon và cửa sổ tương tác cho trẻ.

---

### 4.2. IPC (Inter-Process Communication) & Token bảo mật nội bộ
* Để hai tiến trình (Tiến trình nền ở Session 0 và Tiến trình giao diện ở Session 1) phối hợp nhịp nhàng, chúng cần một kênh liên lạc nội bộ (IPC).
* OGK sử dụng **Local Loopback Socket** (`127.0.0.1:ngẫu_nhiên`) hoặc **Named Pipe** của Windows.
* Để chống việc các phần mềm độc hại khác trên máy con gửi lệnh giả mạo vào kênh IPC này, khi khởi động, Service nền sinh ra một mã bí mật ngẫu nhiên (Local IPC Token) lưu vào bộ nhớ chia sẻ an toàn; tiến trình giao diện bắt buộc phải kèm Token này trong mỗi bản tin IPC thì mới được chấp nhận.

---

### 4.3. Đồng hồ đơn điệu `time.monotonic()` vs `time.time()` & Lỗ hổng tua giờ
* **Hàm `time.time()` / `datetime.now()`:**
  * Đọc thời gian đồng hồ tường (Wall-clock time) của hệ điều hành.
  * **Lỗ hổng chết người:** Khi trẻ em vào Windows Settings chỉnh lùi giờ máy tính lại 3 tiếng (ví dụ từ 17:00 về 14:00), giá trị `time.time()` bị giảm đi 10,800 giây. Hệ thống dùng hàm này sẽ bị tính thời gian sử dụng âm hoặc reset về 0, trẻ có thể chơi game vô hạn!
* **Hàm `time.monotonic()` (Module M6):**
  * Đồng hồ đơn điệu (Monotonic Clock) là bộ đếm xung nhịp vật lý xuất phát từ phần cứng CPU (Windows gọi API `QueryPerformanceCounter` hoặc `GetTickCount64`).
  * Bộ đếm này bắt đầu từ mốc khởi động máy và **CHỈ CÓ THỂ TĂNG THEO THỜI GIAN VẬT LÝ**, hoàn toàn miễn nhiễm và không bị tác động bởi bất kỳ thao tác chỉnh giờ nào trong Windows.
  * OGK tính thời lượng sử dụng theo công thức vi phân:
    $$\Delta t = time.monotonic() - last\_monotonic$$
    $$T_{used} = T_{used} + \Delta t$$
  * Thực nghiệm kiểm chứng: Khi trẻ lùi giờ 3 tiếng, `time.monotonic()` vẫn đếm chuẩn xác từng giây với sai số chỉ **0.18 giây sau 1 tiếng**!

---

### 4.4. Win32 API `GetLastInputInfo` & Thuật toán nhận diện máy rảnh (Idle Detection)
* **Ý nghĩa nhân văn:** Nếu trẻ rời máy đi ăn cơm mà máy vẫn mở, việc tiếp tục trừ giờ chơi của trẻ là bất công.
* **Cơ chế kỹ thuật:**
  * OGK dùng thư viện `ctypes` để gọi hàm Win32 API nguyên bản: `user32.GetLastInputInfo`.
  * Hàm này đọc cấu trúc `LASTINPUTINFO` từ Windows Kernel, cho biết chính xác mốc thời gian (tính bằng mili-giây) của **thao tác bàn phím hoặc di chuột cuối cùng** trên toàn bộ hệ thống.
  * Công thức tính thời gian rảnh:
    $$t_{idle} = GetTickCount() - plii.dwTime$$
  * Nếu $t_{idle} \ge 300,000 \text{ ms}$ (5 phút không có thao tác): Hệ thống tự động kích hoạt cờ **Đóng băng hạn mức** (Freeze Quota). Khi trẻ quay lại chạm vào phím/chuột, bộ đếm tự động tiếp tục tính giờ từ mốc cũ.

---

### 4.5. Win32 API `LockWorkStation` & Triết lý khóa máy an toàn
* **Tại sao không dùng `shutdown /s` hoặc `taskkill`?**
  * Đột ngột tắt máy hay tắt tiến trình sẽ làm trẻ hoảng loạn, ức chế và đặc biệt là làm mất toàn bộ bài tập Word, PowerPoint đang làm dở mà chưa kịp lưu.
* **Win32 API `user32.LockWorkStation()`:**
  * Đây là hàm API gốc của Windows (tương đương tổ hợp phím **Windows + L**).
  * Hàm này đưa máy tính về **Màn hình khóa bảo vệ của Windows** (Lock Screen). Mọi ứng dụng, tài liệu đang mở đều được giữ nguyên vẹn trong bộ nhớ RAM, trẻ chỉ cần xin phụ huynh mở khóa là tiếp tục làm việc bình thường.
* **Vòng lặp tái khóa cưỡng chế (Re-lock Enforcement Loop):**
  * Nếu trẻ biết mật khẩu tài khoản Windows và cố tình gõ mật khẩu vào lại khi hạn mức chơi đã hết, module `system_locker.py` chạy vòng lặp ngầm 5s phát hiện Quota vẫn hết sẽ lập tức gọi lại `LockWorkStation()` sau 3.2 giây. Trẻ hoàn toàn không thể lách luật.

---

### 4.6. Phân quyền tài khoản Windows: LocalSystem vs Standard User
* Trong mô hình an toàn thông tin của OGK:
  * **Tài khoản của trẻ:** Được cấu hình là tài khoản người dùng chuẩn (**Standard User**), không có quyền quản trị (Non-Admin). Trẻ không thể chỉnh sửa tệp hệ thống, không thể chỉnh sửa Windows Service.
  * **OGK-Agent Service:** Chạy dưới quyền đặc quyền cao nhất của hệ điều hành (**LocalSystem**). Nhờ đó, trẻ không thể vào Task Manager để nhấn "End Task" tiến trình Agent. Thư mục cài đặt được phân quyền ACL (Access Control List) chỉ cho phép SYSTEM có quyền ghi, ngăn trẻ xóa hoặc sửa mã nguồn.

---

### 4.7. Win32 Hook `SetWindowsHookEx`: Cơ chế Keylogger an toàn phục vụ phân tích từ khóa nguy cơ
* **Bản chất kỹ thuật:** Trong hệ điều hành Windows, hàm Win32 API `SetWindowsHookEx` với tham số `WH_KEYBOARD_LL` (Low-Level Keyboard Hook) cho phép cài đặt một hàm chặn bắt (Hook Procedure) nằm trong chuỗi xử lý thông điệp bàn phím của hệ thống trước khi thông điệp đó được gửi đến cửa sổ ứng dụng mục tiêu.
* **Ứng dụng nghiên cứu trong đề tài OGK:**
  * Đây là cơ chế nền tảng để hiện thực hóa tính năng **Keylogger phục vụ an toàn (Safety Keyword Monitor)**:
  * Agent lắng nghe chuỗi ký tự gõ phím và đối chiếu với từ điển từ khóa nguy cơ cục bộ (ví dụ: các từ khóa về bạo lực học đường, tự hại, truy cập web đen).
  * **Điểm khác biệt mang tính đạo đức & an toàn của OGK:** Hệ thống không lưu trữ toàn bộ văn bản con gõ (không ghi lại mật khẩu hay nhật ký chat), mà chỉ kích hoạt cờ cảnh báo gửi về điện thoại cha mẹ khi phát hiện chuỗi phím trùng khớp với từ khóa cảnh báo nguy cơ cao!

---

# PHẦN 5: MẬT MÃ HỌC & BẢO MẬT HỆ THỐNG THỜI GIAN THỰC

### 5.1. Thuật toán băm mật khẩu Argon2id
* **Khái niệm:** Argon2id là thuật toán băm mật khẩu đạt giải quán quân cuộc thi Password Hashing Competition (PHC), được chuẩn hóa trong **RFC 9106** và được NIST khuyến nghị sử dụng.
* **Tại sao không dùng MD5 hay SHA-256 để lưu mật khẩu?**
  * MD5 và SHA-256 là các hàm băm thông điệp (Message Digest), được thiết kế để tính toán cực nhanh. Các dàn máy đào sử dụng chip GPU hoặc ASIC có thể thử hàng tỷ mật khẩu mỗi giây để bẻ khóa mật khẩu (Brute-force).
* **Đặc tính ngốn bộ nhớ (Memory-Hard) của Argon2id:**
  * Argon2id bắt buộc mỗi phép tính băm phải chiếm dụng một dung lượng RAM vật lý cố định (OGK cấu hình tốn hàng chục MB RAM và nhiều vòng lặp). Điều này làm các dàn GPU bị nghẽn băng thông bộ nhớ và không thể tính toán song song, triệt tiêu hoàn toàn khả năng dò mật khẩu của hacker.

---

### 5.2. Chữ ký toàn vẹn HMAC-SHA256 (Anti-Tamper)
* **HMAC là gì?** HMAC (Hash-based Message Authentication Code) là cơ chế tạo mã xác thực thông điệp kết hợp giữa một hàm băm mật mã (SHA-256) và một **khóa bí mật dùng chung (Shared Secret Key)**.
* **Vai trò trong OGK (Module F4 Anti-Tamper):**
  * Khi Server ban hành một chính sách (Hạn mức thời gian ngày thường, ngày nghỉ, Ma trận lịch tuần), Server nối các giá trị lại thành chuỗi chuẩn tắc (Canonical String) và ký ra chữ ký số HMAC:
    $$\text{signature} = \text{HMAC-SHA256}(K_{secret}, \text{canonical\_string})$$
  * Khi Agent nhận chính sách, nó dùng khóa bí mật của thiết bị để tính toán lại chữ ký.
  * Nếu một đứa trẻ am hiểu công nghệ tìm cách mở file SQLite cục bộ `agent_cache.db` và sửa quota từ 60 phút thành 600 phút, chữ ký tính lại sẽ bị sai lệch hoàn toàn so với chữ ký gốc. Agent lập tức từ chối chính sách đã bị sửa lén và khóa máy an toàn.

---

### 5.3. Tấn công phân tích thời gian (Timing Attack) & So sánh hằng số thời gian
* **Lỗ hổng so sánh chuỗi thông thường (`==`):**
  * Trong hầu hết các ngôn ngữ (kể cả Python/C), toán tử `a == b` so sánh từng ký tự từ trái qua phải. Khi gặp ký tự đầu tiên bị sai, hàm lập tức trả về `False` (Fail-fast).
  * Điều này tạo ra sự chênh lệch thời gian phản hồi ở mức nano-giây: chuỗi đoán đúng 5 ký tự đầu sẽ mất nhiều thời gian hơn chuỗi chỉ đúng 1 ký tự đầu. Kẻ tấn công có thể đo thời gian để giải mã dần từng ký tự của chữ ký bí mật.
* **Giải pháp trong OGK:**
  * OGK sử dụng hàm `hmac.compare_digest(a, b)`: Hàm này luôn luôn duyệt qua toàn bộ độ dài chuỗi bất kể đúng hay sai, đảm bảo **thời gian thực thi là một hằng số cố định (Constant-Time)**, triệt tiêu 100% nguy cơ tấn công Timing Attack.

---

### 5.4. JSON Web Token (JWT) & Quản lý phiên
* **Cấu trúc JWT:** Gồm 3 phần phân tách bằng dấu chấm: `Header.Payload.Signature`.
  * **Header:** Chứa thuật toán ký (HS256).
  * **Payload:** Chứa thông tin người dùng (`sub`), vai trò (`role: parent`), và thời điểm hết hạn (`exp`).
  * **Signature:** Chữ ký số bảo đảm Payload không bị kẻ xấu sửa đổi trên đường truyền.
* **Quy định phiên trong OGK:**
  * Token truy cập (Access Token) của phụ huynh có thời hạn ngắn (15 phút). Hết 15 phút, người dùng phải xác thực lại để ngăn chặn việc bị chiếm quyền điều khiển khi bỏ quên máy tính.

---

### 5.5. Cờ bảo mật Cookie: `HttpOnly` và `SameSite=Lax`
* **`HttpOnly=True`:**
  * Báo cho trình duyệt biết: Tuyệt đối không cho phép bất kỳ đoạn mã JavaScript nào (kể cả qua console hay mã độc XSS) được đọc hoặc sao chép giá trị của Cookie này.
  * Nhờ vậy, ngay cả khi trang web bị chèn mã độc XSS, kẻ tấn công cũng không thể đánh cắp được token phiên làm việc của cha mẹ.
* **`SameSite="Lax"`:**
  * Ngăn chặn trình duyệt gửi kèm cookie trong các yêu cầu gửi từ trang web bên ngoài (Cross-site requests), triệt tiêu hoàn toàn nguy cơ tấn công giả mạo yêu cầu từ phía người dùng (CSRF).

---

### 5.6. Chống tấn công phát lại (Anti-Replay Attack) & TTL
* **Tấn công phát lại (Replay Attack):** Kẻ tấn công bắt lén gói tin đăng ký hợp lệ trong quá khứ và gửi lại gói tin đó lên máy chủ để cố gắng tạo thêm phiên làm việc mới.
* **Cách OGK chống lại:**
  * Mã ghép đôi 8 ký tự chỉ có hiệu lực trong vòng **10 phút (TTL = 600 giây)**.
  * Ngay khi mã được sử dụng lần đầu tiên, Server đánh dấu cờ `is_used = True` trong CSDL. Mọi nỗ lực gửi lại mã đó lần thứ hai đều bị từ chối với mã lỗi `HTTP 400 Bad Request`.

---

### 5.7. Mô hình đe dọa STRIDE trong dự án OGK
STRIDE là mô hình đánh giá rủi ro an ninh mạng chuẩn do Microsoft phát triển:
1. **S - Spoofing (Giả mạo danh tính):** Kẻ xấu giả làm phụ huynh hoặc máy con ➜ *Khắc chế bằng JWT ký bí mật và Hardware UUID duy nhất.*
2. **T - Tampering (Can thiệp sửa đổi dữ liệu):** Trẻ sửa file DB cục bộ hoặc sửa gói tin trên mạng ➜ *Khắc chế bằng Chữ ký HMAC-SHA256.*
3. **R - Repudiation (Chối bỏ trách nhiệm):** Phụ huynh đổi luật nhưng không thừa nhận ➜ *Khắc chế bằng Bảng Audit Log lưu đầy đủ IP, mốc giờ, giá trị cũ và mới.*
4. **I - Information Disclosure (Lộ lọt thông tin):** Rò rỉ dữ liệu đời tư trẻ em ➜ *Khắc chế bằng nguyên tắc NT2 (chỉ lưu 4 siêu dữ liệu tối thiểu, không lưu full URL, xử lý Local-First).*
5. **D - Denial of Service (Từ chối dịch vụ):** Trẻ cố tình làm sập Agent ➜ *Khắc chế bằng Windows Service Recovery tự khởi động lại sau 5 giây.*
6. **E - Elevation of Privilege (Leo thang đặc quyền):** Trẻ lấy quyền Admin để tắt phần mềm ➜ *Khắc chế bằng tài khoản Standard User và phân quyền ACL thư mục chỉ cho phép SYSTEM can thiệp.*

---

# PHẦN 6: PHÁP LÝ & ĐẠO ĐỨC CÔNG NGHỆ BẢO VỆ TRẺ EM

### 6.1. Nghị định 13/2023/NĐ-CP (Điều 20)
* **Quy định cốt lõi:** Việc xử lý dữ liệu cá nhân của trẻ em bắt buộc phải có sự đồng ý của cha mẹ hoặc người giám hộ; và nếu trẻ từ 7 tuổi trở lên thì phải có sự đồng thuận của cả trẻ.
* **Ánh xạ vào OGK:**
  * Quy trình ghép đôi thiết bị không dây 8 ký tự chính là "điểm chạm kỹ thuật" thể hiện sự đồng thuận giữa cha mẹ và con cái.
  * Phụ huynh có quyền rút lại sự đồng ý bất kỳ lúc nào bằng tính năng "Xóa toàn bộ dữ liệu thiết bị".

---

### 6.2. Luật Trẻ Em 2016 (Điều 21) & Quyền riêng tư
* **Quy định cốt lõi:** Trẻ em có quyền bất khả xâm phạm về đời sống riêng tư, bí mật cá nhân và bí mật gia đình.
* **Ánh xạ vào OGK:**
  * OGK kiên quyết loại bỏ cơ chế chụp lén màn hình tràn lan và đọc trộm tin nhắn riêng tư.
  * Hệ thống chỉ ghi nhận 4 siêu dữ liệu kỹ thuật ở mức tổng quan: Tên tiến trình, Tên miền cấp 2, Thời lượng và Mốc giờ. Cha mẹ biết con dành bao nhiêu thời gian cho học tập và giải trí mà không xâm phạm vào nội dung cá nhân của con.

---

### 6.3. Chuẩn mực NIST SP 800-63B & OWASP ASVS v4
* **NIST SP 800-63B:** Hướng dẫn định danh và xác thực số của Viện Tiêu chuẩn và Kỹ thuật Quốc gia Hoa Kỳ, đặt ra các tiêu chuẩn chống tấn công dò mật khẩu và quy định độ phức tạp mật khẩu.
* **OWASP ASVS v4 (Application Security Verification Standard):** Tiêu chuẩn kiểm thử bảo mật ứng dụng web của tổ chức an ninh mạng toàn cầu OWASP, đặt ra các tiêu chuẩn kiểm tra phiên, cờ cookie và mã hóa dữ liệu khi truyền tải.
