# PHỤ LỤC M2: BÁO CÁO KỸ THUẬT MẠNG — SO SÁNH 4 PHƯƠNG ÁN KIỂM SOÁT TRUY CẬP WEBSITE
## ĐỀ TÀI: OPEN GUARDIAN KIDS (OGK) — VERSION 0.3
> **Chuyên ngành:** Mạng máy tính & Truyền thông dữ liệu  
> **Mục đích:** Luận chứng cơ sở khoa học và kỹ thuật cho việc lựa chọn giải pháp **DNS Proxy Cục Bộ (127.0.0.1:53)** thay thế cho các phương án truyền thống.

---

## 1. BẢNG MA TRẬN SO SÁNH ĐA TIÊU CHÍ (MULTI-CRITERIA COMPARISON)

| Tiêu chí Đánh giá | Phương án 1: Tệp `hosts` Windows | Phương án 2: DNS Proxy Cục bộ 127.0.0.1:53 (OGK) | Phương án 3: Proxy HTTP/HTTPS (MITM) | Phương án 4: Bộ lọc WFP (Kernel Driver) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Hiệu năng & Tiêu tốn tài nguyên** | ⭐⭐⭐⭐ Tốt (Tra bảng tĩnh của OS), nhưng gây giật lag DNS Client cache nếu tệp quá 10.000 dòng. | ⭐⭐⭐⭐⭐ **Cực tốt** (~15MB RAM, độ trễ xử lý < 2ms với thư viện `dnslib` bất đồng bộ). | ⭐⭐ Kém (Phải giải mã TLS handshake, đệm toàn bộ luồng stream dữ liệu mạng). | ⭐⭐⭐⭐⭐ Cực nhanh (Xử lý trực tiếp tại Network Layer trong nhân hệ điều hành). |
| **2. Độ ổn định & Rủi ro Crash** | ⭐⭐⭐ Khá, nhưng dễ bị phần mềm diệt virus (AV) cảnh báo hoặc phục hồi đè file. | ⭐⭐⭐⭐⭐ **Rất cao** (Chạy hoàn toàn ở không gian người dùng User-mode, không thể làm xanh màn hình BSOD). | ⭐⭐ Dễ lỗi chứng chỉ SSL/TLS, xung đột pinning cert của ứng dụng ngân hàng, game. | ⭐ Rủi ro cực cao (Lỗi logic trong Kernel Driver dẫn tới lỗi Blue Screen of Death - BSOD sập máy). |
| **3. Tôn trọng Quyền riêng tư (NT2)** | ⭐⭐⭐⭐⭐ Tốt (Không đọc nội dung dữ liệu). | ⭐⭐⭐⭐⭐ **Tuyệt đối** (Chỉ biết FQDN tên miền; tuyệt đối không xem được đường dẫn URL chi tiết hay nội dung trao đổi). | ❌ **Vi phạm nghiêm trọng** (Đọc toàn bộ nội dung chat, form, mật khẩu; tiềm ẩn nguy cơ lộ lọt dữ liệu). | ⭐⭐⭐ Tốt (Lọc theo IP/Port/Header gói tin). |
| **4. Khả năng Chặn Subdomain (Wildcard) & SafeSearch** | ❌ **Không hỗ trợ** (Bắt buộc phải liệt kê từng subdomain đơn lẻ; không thể cưỡng chế SafeSearch linh hoạt). | ⭐⭐⭐⭐⭐ **Hoàn hảo** (Hỗ trợ regex/wildcard `*.domain.com`, tự động rewrite VIP SafeSearch, vô hiệu hóa DoH). | ⭐⭐⭐⭐ Tốt (Can thiệp được URL và header HTTP). | ⭐⭐ Khó khăn (WFP lọc IP tầng thấp, tên miền HTTPS nằm trong extension SNI phải parse phức tạp). |
| **5. Tính Khả thi & Bảo trì Dự án** | ⭐⭐⭐ Dễ làm nhưng khó duy trì cập nhật quy tắc động theo thời gian thực. | ⭐⭐⭐⭐⭐ **Tối ưu nhất** (Mã nguồn Python thuần, dễ kiểm thử tự động, tích hợp SQLite cache). | ⭐ Phức tạp (Cần quản lý chứng thư số CA, cài đặt vào Trusted Root của Windows). | ❌ Cực kỳ phức tạp (Yêu cầu ký số Driver EV Certificate đắt đỏ của Microsoft, lập trình C++ WDK). |

---

## 2. PHÂN TÍCH CHUYÊN SÂU TỪNG PHƯƠNG ÁN

### 2.1. Phương án 1: Ghi đè tệp `hosts` hệ thống (`C:\Windows\System32\drivers\etc\hosts`)
- **Cơ chế:** Thêm các dòng ánh xạ `0.0.0.0 badsite.com` vào tệp cấu hình tĩnh của hệ điều hành Windows.
- **Hạn chế mạng:**
  - Tệp `hosts` không hỗ trợ wildcard subdomain: Chặn `badsite.com` sẽ **không** chặn được `m.badsite.com` hay `sub.badsite.com`.
  - Windows DNS Client Service đọc toàn bộ tệp vào bộ nhớ; khi danh sách chặn vượt quá 10.000 dòng, dịch vụ `Dnscache` bị nghẽn (CPU 100%).
  - Các phần mềm chống mã độc (Windows Defender) thường xuyên khóa quyền truy cập hoặc tự động xóa các dòng sửa đổi tệp hosts vì nghi ngờ hành vi của Malware Hijacking.

### 2.2. Phương án 3: Proxy HTTP/HTTPS giải mã lưu lượng (Man-in-the-Middle - MITM)
- **Cơ chế:** Dựng proxy cục bộ lắng nghe cổng 8080/8443, cài đặt chứng thư số tự ký (Root CA) vào Certificate Store của máy tính để giải mã phiên TLS.
- **Nguy cơ Đạo đức & Pháp lý (Vi phạm NT2 & Nghị định 13/2023):**
  - Proxy MITM có khả năng đọc toàn bộ nội dung tin nhắn riêng tư của trẻ, mật khẩu đăng nhập, thẻ ngân hàng của phụ huynh. Điều này vi phạm trực tiếp nguyên tắc bảo vệ bí mật đời sống riêng tư của trẻ em theo Điều 21 Luật Trẻ em 2016.
  - Rất nhiều ứng dụng hiện đại (Discord, Steam, Game client) sử dụng kỹ thuật **SSL Certificate Pinning**; khi phát hiện proxy MITM, các ứng dụng này lập tức từ chối kết nối, khiến máy tính gặp lỗi mạng hàng loạt.

### 2.3. Phương án 4: Bộ lọc tầng mạng Windows Filtering Platform (WFP Kernel Driver)
- **Cơ chế:** Viết trình điều khiển nhân (Kernel-mode Driver) chặn gói tin ngay tại tầng mạng (Network Layer) và giao vận (Transport Layer).
- **Hạn chế triển khai:**
  - Cần chứng chỉ chữ ký số mở rộng Microsoft Extended Validation (EV Code Signing Certificate) với chi phí rất lớn và quy trình phê duyệt nghiêm ngặt.
  - Bất kỳ lỗi tràn bộ đệm (Buffer Overflow) hay Null Pointer nào cũng khiến toàn bộ hệ điều hành Windows bị sập ngay lập tức (màn hình xanh chết chóc BSOD), gây mất dữ liệu của người dùng.

---

## 3. KẾT LUẬN & LUẬN CHỨNG LỰA CHỌN PHƯƠNG ÁN DNS PROXY CỤC BỘ (OGK)

Hệ thống Open Guardian Kids lựa chọn **Phương án 2: DNS Proxy Cục Bộ (127.0.0.1:53)** làm nền tảng cốt lõi vì:

1. **Hiệu năng cao & An toàn tuyệt đối:** Chạy ở tầng người dùng (User-mode), bộ nhớ tiêu thụ siêu nhỏ (< 20MB), tốc độ phân giải tính bằng mili-giây, tuyệt đối không gây sập hệ điều hành.
2. **Tuân thủ đạo đức NT2:** Chỉ đọc thông tin FQDN (Fully Qualified Domain Name) của gói tin DNS để quyết định Cho phép/Chặn; tuyệt đối không xem được nội dung trang web hay thông tin truyền tải.
3. **Linh hoạt & Thông minh:**
   - Dễ dàng hỗ trợ wildcard subdomain: Chặn `domain.com` tự động chặn mọi subdomain con.
   - Hỗ trợ cưỡng chế **SafeSearch** bằng cách viết lại bản ghi A sang địa chỉ IP VIP của Google/Bing/YouTube.
   - Vô hiệu hóa tính năng lách luật DoH của trình duyệt bằng cơ chế **Canary Domain** (`use-application-dns.net`).
   - Tích hợp bộ đệm SQLite ngoại tuyến cho phép máy vẫn được bảo vệ ngay cả khi mất kết nối mạng Internet.
