# BÁO CÁO THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN — PHẦN 2: TUẦN 3 & TUẦN 4 (VERSION 0.3 & VERSION 0.4)
## ĐỀ TÀI: XÂY DỰNG ỨNG DỤNG HỖ TRỢ QUẢN LÝ VIỆC SỬ DỤNG MÁY TÍNH CỦA TRẺ EM
### TÊN GIẢI PHÁP HỆ THỐNG: OPEN GUARDIAN KIDS (OGK) — PHIÊN BẢN HOÀN THIỆN ĐỒ ÁN TỐT NGHIỆP
> **Học phần:** Chuyên đề Tốt nghiệp Mạng máy tính & Truyền thông Dữ liệu  
> **Tiếp nối:** Phần 1 (Slide 1 – Slide 20: Version 0.1 & Version 0.2)  
> **Hiện trạng đồ án:** ĐÃ HOÀN THÀNH 100% CẢ 4 TUẦN — ĐẠT **61/61 AUTOMATED TESTS PASSED (100%)**

---

## MỤC LỤC TỔNG QUAN 20 SLIDES TIẾP NỐI (SLIDE 21 – SLIDE 40)

* **PHẦN A: VERSION 0.3 (TUẦN 3 — NETWORK FILTERING, PROCESS CONTROL & TRANSPARENCY)**
  * **Slide 21:** Trang Tiêu Đề Báo Cáo Giai Đoạn 2 (Version 0.3 & Version 0.4 — Final Graduation Release)
  * **Slide 22:** Tổng Quan Khối Lượng Đồ Án: Bước Chuyển Từ Quản Trị Thời Gian Sang Kiểm Soát Mạng & An Ninh
  * **Slide 23:** Kỹ Thuật Lõi 1 (F2 & M1): Kiến Trúc DNS Sinkhole Proxy Cổng UDP 53 Nội Bộ
  * **Slide 24:** Kỹ Thuật Lõi 2 (F2): Thuật Toán Khớp Tên Miền, Subdomain Wildcard & Danh Mục Miễn Nhiễm Vĩnh Viễn (NT6)
  * **Slide 25:** Kỹ Thuật Lõi 3 (F2): Cưỡng Chế SafeSearch (Google, Bing, DuckDuckGo) & YouTube Content Filtering
  * **Slide 26:** Kỹ Thuật Lõi 4 (F2 & M3): Vô Hiệu Hóa DoH (DNS over HTTPS) Bằng NXDOMAIN Canary Domain
  * **Slide 27:** Kỹ Thuật Lõi 5 (F2): Kiểm Soát Ứng Dụng Bằng Mã Băm SHA-256 Nhị Phân & Tối Ưu Hóa CPU 0.0%
  * **Slide 28:** Kỹ Thuật Lõi 6 (NT3 & NT5): Tiếng Nói Trẻ Em — Giao Diện Xin Thêm Giờ, Báo Chặn Nhầm & Đồng Bộ Hai Chiều
  * **Slide 29:** TỔNG KẾT NGHIỆM THU VER 3 (v0.3): Network Filtering & Process Control [45 Tasks, 38/38 Tests PASSED]

* **PHẦN B: VERSION 0.4 (TUẦN 4 — SECURITY HARDENING, ANTI-BYPASS, BENCHMARKING & FINAL RELEASE)**
  * **Slide 30:** Tổng Quan Version 0.4: Gia Cố Bảo Mật Cấp Cao F5, Pháp Lý NĐ 13, Khắc Chế Vượt Rào M3 & Đo Lường M4
  * **Slide 31:** Bảo Mật Cấp Cao F5 (NIST SP 800-63B & ASVS v4): Mật Khẩu $\ge 10$ Ký Tự, Khóa Brute-Force 15 Phút, IP Rate Limiting
  * **Slide 32:** Bảo Mật Cấp Cao F5: Mã Hóa AES-256-GCM AEAD & Triệt Tiêu Hoàn Toàn Lỗ Hổng IDOR Trên Mọi API
  * **Slide 33:** Tuân Thủ Pháp Lý & Đạo Đức: Nghị Định 13/2023/NĐ-CP — Xóa Tự Động 90 Ngày & Quyền Xóa Dữ Liệu Con (Right to Erasure)
  * **Slide 34:** Báo Cáo Kỹ Thuật Mạng M3 (Anti-Bypass Guard): Khắc Chế 7 Kỹ Thuật Vượt Rào — DNS Watchdog & Process Killer
  * **Slide 35:** Báo Cáo Kỹ Thuật Mạng M4 (Đo Lường Hiệu Năng Thực Nghiệm): RAM 25.13 MB, CPU 0.0%, DNS 0.83 ms, WebSocket 5.91 ms
  * **Slide 36:** Báo Cáo Kỹ Thuật Mạng M5 (Khả Năng Chịu Lỗi & Phục Hồi Mạng): Đệm Ngoại Tuyến SQLite & Tự Khóa Khi Sập Mạng
  * **Slide 37:** Hồ Sơ Đồ Án & An Ninh: Mô Hình Đe Dọa STRIDE (8 Threats), OWASP ASVS v4 Level 1 & Bản Minh Bạch AI
  * **Slide 38:** TỔNG KẾT NGHIỆM THU ĐẦU-CUỐI VER 4 (v0.4): Đạt Trọn Vẹn 5/5 Tiêu Chuẩn DoD (DoD 1 đến DoD 5)
  * **Slide 39:** Toàn Cảnh Kiểm Thử Tự Động Toàn Hệ Thống: 61/61 Test Cases PASSED 100% & 8/8 Kịch Bản Nghiệm Thu Trực Tiếp
  * **Slide 40:** Kết Luận Toàn Diện Đồ Án Tốt Nghiệp, Khả Năng Mở Rộng Thương Mại & Sẵn Sàng Cho Phiên Bảo Vệ Chính Thức

---

# CHI TIẾT TỪNG TRANG SLIDE (SLIDE 21 ĐẾN SLIDE 40)

---

## SLIDE 21: TRANG TIÊU ĐỀ BÁO CÁO GIAI ĐOẠN 2 (TUẦN 3 & TUẦN 4)
### 1. Nội dung hiển thị trên Slide
* **Tên đồ án:** XÂY DỰNG ỨNG DỤNG HỖ TRỢ QUẢN LÝ VIỆC SỬ DỤNG MÁY TÍNH CỦA TRẺ EM
* **Tên giải pháp:** OPEN GUARDIAN KIDS (OGK) — Version 0.4 (Final Graduation Release)
* **Nội dung báo cáo:** GIAI ĐOẠN 2: HOÀN THIỆN TOÀN DIỆN TUẦN 3 & TUẦN 4
* **Các trụ cột công nghệ:**
  * DNS Sinkhole Proxy UDP 53 & Cưỡng chế SafeSearch Google/YouTube (F2)
  * Kiểm soát ứng dụng Windows bằng mã băm nhị phân SHA-256 (F2)
  * Bảo mật cấp cao F5: Argon2id, Chống IDOR 100%, AES-256-GCM AEAD
  * Tuân thủ Nghị định 13/2023/NĐ-CP: Xóa dữ liệu 90 ngày & Right to Erasure
  * Chống vượt rào mạng M3: DNS Watchdog 20s & Chặn tiến trình VPN
  * Thực nghiệm hiệu năng M4 & Khả năng chịu lỗi ngoại tuyến M5
* **Kết quả kiểm thử:** 61/61 Automated Tests PASSED (100%) — Đạt 5/5 Definition of Done (DoD).

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy và quý Thầy Cô trong Hội đồng phản biện.  
> Ở phần 1, nhóm chúng em đã trình bày hai phiên bản nền móng v0.1 và v0.2 giải quyết bài toán cốt lõi về Bộ khung kết nối và Quản trị thời gian đơn điệu `time.monotonic()`.  
>  
> Hôm nay, chúng em xin phép được báo cáo phần quan trọng và chuyên sâu nhất của Đồ án Tốt nghiệp chuyên ngành Mạng Máy Tính: **Giai đoạn 2 (Tuần 3 & Tuần 4)** — hiện thực hóa trọn vẹn **Tầng lọc mạng DNS Sinkhole tại cổng UDP 53, Kiểm soát ứng dụng bằng mã băm SHA-256, Gia cố an ninh cấp cao F5 theo chuẩn NIST/ASVS v4, Tuân thủ pháp lý Nghị định 13/2023 và Thực nghiệm đo lường hiệu năng chuyên ngành M4/M5**.  
>  
> Toàn bộ 4 tuần phát triển đã được đóng gói hoàn thiện với **61/61 kịch bản kiểm thử tự động đạt 100% Pass** và **8/8 bước nghiệm thu thực tế thành công xuất sắc**."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Điểm khác biệt căn bản nhất giữa giai đoạn 1 (Tuần 1-2) và giai đoạn 2 (Tuần 3-4) là gì?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    - Giai đoạn 1 tập trung vào **Quản trị Thời gian và Thiết bị** (Time & Device Governance): giải quyết bài toán đếm giờ không gian lận và phát lệnh khóa khẩn cấp qua WebSocket.  
    - Giai đoạn 2 nâng tầm lên **An Toàn Không Gian Mạng & Pháp Lý Chuyên Sâu** (Network Security & Privacy Compliance): can thiệp trực tiếp vào tầng giao thức phân giải tên miền DNS cổng 53, vô hiệu hóa DoH, đối soát mã băm nhị phân SHA-256, gia cố mã hóa AES-256-GCM, chống vượt rào mạng và tuân thủ Luật Trẻ Em cùng Nghị định 13/2023/NĐ-CP ạ."*

---

## SLIDE 22: TỔNG QUAN KHỐI LƯỢNG ĐỒ ÁN (TUẦN 3 & TUẦN 4)
### 1. Nội dung hiển thị trên Slide
* **Sơ đồ tiến trình phát triển Spec-Driven Development 4 Tuần:**
  * **Tuần 1 (v0.1):** The Backbone [46 Tasks, 15 Tests] $\rightarrow$ *Hoàn thành 100%*
  * **Tuần 2 (v0.2):** Time Governance [42 Tasks, 24 Tests] $\rightarrow$ *Hoàn thành 100%*
  * **Tuần 3 (v0.3):** Network & Process Filtering [45 Tasks, 38 Tests] $\rightarrow$ *Hoàn thành 100%*
  * **Tuần 4 (v0.4):** Hardening, Benchmarking & Release [31 Tasks, 61 Tests] $\rightarrow$ *Hoàn thành 100%*
* **Tổng kết quy mô mã nguồn đồ án hoàn chỉnh:**
  * **164 Tasks chi tiết** được phân rã kỹ thuật và kiểm chứng độc lập.
  * **61 Automated Test Cases** phủ kín mọi module Client và Server.
  * **6 Báo cáo Chuyên sâu Kỹ thuật Mạng** (M1 đến M6).
  * **Tệp dữ liệu thực nghiệm Benchmark:** 30 mẫu đo độc lập (JSON output).
  * **Hồ sơ Pháp lý & An ninh:** Bảng kê khai 4 trường viễn trắc tối thiểu, Cam kết NT1/NT2 cho trẻ, Mô hình đe dọa STRIDE và 22 tiêu chí ASVS v4.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, để đảm bảo tính kỷ luật kỹ thuật cao nhất của một Đồ án Tốt nghiệp chuyên ngành Mạng, nhóm không hề code theo cảm tính mà tuân thủ phương pháp luận Spec-Driven Development:  
> Mỗi tính năng đều bắt đầu từ tài liệu đặc tả, kế hoạch phân rã micro-tasks, bộ kiểm thử tự động rồi mới đến mã nguồn thực thi.  
>  
> Trong 2 tuần cuối, nhóm đã hoàn thành thêm **76 tasks kỹ thuật**, mở rộng bộ test suite từ 24 test lên **61 test cases tự động**. Mọi kịch bản rớt mạng, sập server, vượt rào DNS hay can thiệp trái phép cơ sở dữ liệu đều được kiểm chứng và ghi lại trong các báo cáo chuyên đề từ M1 đến M6."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Tại sao số lượng bài test tăng mạnh từ 24 test lên 61 test trong hai tuần cuối?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, vì tầng lọc mạng (DNS Sinkhole) và an ninh bảo mật (F5) có rất nhiều trường hợp ngoại lệ (Edge Cases):  
    Ví dụ: Gói tin DNS bị phân mảnh (Malformed Packet), bản ghi IPv6 (AAAA), ghi đè SafeSearch, kiểm tra quyền sở hữu chống IDOR trên từng endpoint, tấn công Brute-force 5 lần, mã hóa AES-256-GCM bị sửa 1 bit dữ liệu, và 3 kịch bản chịu lỗi mất mạng. Mỗi trường hợp biên đều phải có ít nhất một bài unit test độc lập để đảm bảo hệ thống không bao giờ bị sập (crash) trong môi trường thực tế ạ."*

---

## SLIDE 23: KỸ THUẬT LÕI TUẦN 3 (F2 & M1) — KIẾN TRÚC DNS SINKHOLE PROXY UDP 53
### 1. Nội dung hiển thị trên Slide
* **Tại sao can thiệp ở tầng DNS thay vì dùng HTTP Proxy / TLS Interception?**
  * **Không xâm phạm riêng tư:** Không cần giải mã TLS/HTTPS, không cần cài đặt Root Certificate vào máy tính của trẻ, không thể đọc trộm mật khẩu hay tin nhắn.
  * **Hiệu năng vượt trội:** Xử lý trực tiếp trên các gói tin UDP 53 siêu nhẹ, không tiêu tốn RAM làm bộ nhớ đệm luồng dữ liệu web.
* **Nguyên lý luồng gói tin (DNS Packet Flow - M1):**
  1. Card mạng Wi-Fi/Ethernet được cấu hình DNS trỏ về `127.0.0.1`.
  2. `DNSProxy` lắng nghe trên cổng UDP 53 nội bộ (`dnspython` + Socket).
  3. Khi phát sinh DNS Query:
     * **Trùng danh mục cấm:** Phản hồi ngay lập tức `0.0.0.0` (Sinkhole), TTL = 60s. Độ trễ chỉ **0.83 ms**.
     * **Tên miền an toàn:** Chuyển tiếp (Forward) tới DNS an toàn `1.1.1.3` (Cloudflare Families) để lọc mã độc từ gốc Internet.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy, đây là điểm sáng kỹ thuật mạng tiêu biểu của đồ án (Module M1):  
> Thay vì chọn con đường cài đặt proxy trung gian (Man-In-The-Middle) với chứng chỉ SSL giả mạo để đọc lén dữ liệu của trẻ — một hành vi tiềm ẩn lỗ hổng bảo mật nghiêm trọng và vi phạm đạo đức, nhóm quyết định can thiệp ở **tầng phân giải tên miền (DNS)**.  
>  
> Mọi ứng dụng trước khi muốn gửi gói tin TCP đều bắt buộc phải hỏi DNS xem IP của máy chủ ở đâu. Bằng cách thiết lập DNS Proxy cục bộ trên cổng UDP 53, hệ thống đón đầu mọi yêu cầu này.  
> Nếu trẻ vào trang web đen hay game cấm, Agent trả về địa chỉ Sinkhole `0.0.0.0` ngay trong **0.83 mili-giây**. Trình duyệt nhận được IP `0.0.0.0` sẽ từ chối kết nối ngay lập tức mà không tiêu tốn một byte băng thông Internet nào."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Tại sao lại trả về địa chỉ `0.0.0.0` mà không trả về `127.0.0.1` hay `127.0.0.2`?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    Nếu trả về `127.0.0.1`, hệ điều hành sẽ cố gắng kết nối tới cổng 80/443 của chính máy tính con. Nếu trên máy con đang chạy web server nội bộ (ví dụ IIS, Apache hoặc chính OGK Dashboard), nó sẽ gây xung đột dịch vụ hoặc gây ra hiện tượng treo kết nối (Connection Timeout) làm đơ trình duyệt.  
    Theo chuẩn RFC 1122 và quy ước bảo mật hiện đại của Pi-hole hay AdGuard, `0.0.0.0` là địa chỉ Non-routable meta-address: Ngăn xếp TCP/IP của Windows khi nhận `0.0.0.0` sẽ lập tức từ chối kết nối ở cấp độ Socket (Connection Refused), giúp trình duyệt báo lỗi ngay mà không phải chờ timeout ạ."*

---

## SLIDE 24: KỸ THUẬT LÕI TUẦN 3 (F2) — THUẬT TOÁN KHỚP TÊN MIỀN & MIỄN NHIỄM VĨNH VIỄN (NT6)
### 1. Nội dung hiển thị trên Slide
* **Thuật toán Khớp Tên miền (Domain Matching Algorithm):**
  * Hỗ trợ khớp chính xác tên miền gốc và mọi tên miền phụ (Subdomain Wildcard):
  $$\text{Matched} \iff (Q = D) \lor (Q \text{ kết thúc bằng } .D)$$
  * Ví dụ: Khi cấm `tiktok.com`, bộ lọc tự động bao quát `vt.tiktok.com`, `api.tiktok.com`, `v16.tiktokcdn.com`.
  * Bộ nhớ đệm tra cứu Set Lookups đạt độ phức tạp thời gian **$O(1)$**, đảm bảo xử lý hàng ngàn tên miền mà không gây trễ.
* **Nguyên tắc NT6 — Danh mục Miễn nhiễm Vĩnh viễn (Immutable Whitelist):**
  * Luật bảo vệ trẻ em quy định: Không bao giờ được phép chặn các cổng cứu nạn và giáo dục.
  * Danh mục cứng trong mã nguồn: `tongdai111.vn`, `moet.gov.vn`, `chinhphu.vn`, `*.edu.vn`.
  * Ràng buộc logic: Nếu phụ huynh cố tình nhập luật cấm `moet.gov.vn`, hệ thống lập tức ném ngoại lệ `NT6ViolationError` và từ chối lưu vào Database.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, một trong những thách thức của việc lọc tên miền là các dịch vụ giải trí lớn sở hữu hàng trăm tên miền phụ thay đổi liên tục. Nếu chỉ so sánh chuỗi bằng phép bằng thông thường, hệ thống sẽ bị qua mặt ngay.  
> Nhóm đã hiện thực hóa thuật toán đối soát hậu tố tên miền với cấu trúc dữ liệu Set tối ưu: Chỉ cần lưu tên miền cấp hai, toàn bộ hệ sinh thái tên miền phụ của trang web đó đều bị chặn đồng loạt.  
>  
> Đặc biệt, để hiện thực hóa **Nguyên tắc Đạo đức NT6 trong Hiến chương OGK**, chúng em thiết kế cơ chế **Danh mục Miễn nhiễm Vĩnh viễn**. Dù phụ huynh có vô tình hay cố ý đặt luật cấm Tổng đài Quốc gia Bảo vệ Trẻ em 111 hay Cổng thông tin Bộ Giáo Dục, hệ thống sẽ kiên quyết từ chối để đảm bảo quyền được học tập và quyền được bảo vệ an toàn của trẻ luôn được ưu tiên cao nhất."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Nếu trẻ truy cập một trang web học tập nhưng trang đó có nhúng quảng cáo từ một tên miền bị cấm thì sao? Trang web có bị hỏng giao diện không?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, đây chính là ưu điểm vượt trội của cơ chế DNS Sinkhole:  
    Trang web học tập (nằm trong danh mục cho phép) vẫn được tải bình thường từ máy chủ của trường. Chỉ riêng các iframe hay banner quảng cáo trỏ tới tên miền cấm (ví dụ `doubleclick.net` hay web game) sẽ nhận phản hồi `0.0.0.0` và bị loại bỏ cục bộ. Nhờ đó, trẻ vừa xem được bài giảng mà hoàn toàn không bị phân tâm bởi quảng cáo độc hại ạ."*

---

## SLIDE 25: KỸ THUẬT LÕI TUẦN 3 (F2) — CƯỠNG CHẾ SAFESEARCH & YOUTUBE RESTRICTED MODE
### 1. Nội dung hiển thị trên Slide
* **Thực trạng vấn đề:**
  * Trẻ không vào trang web cấm trực tiếp, nhưng gõ từ khóa tìm kiếm trên Google/Bing để xem ảnh/video nhạy cảm.
  * Trẻ có thể tự do tắt nút SafeSearch trong phần Cài đặt của trình duyệt.
* **Cơ chế Cưỡng chế SafeSearch ở Cấp độ Mạng (DNS VIP Rewriting):**
  * **Google:** Ghi đè mọi truy vấn `google.com`, `google.com.vn` trỏ về IP của `forcesafesearch.google.com` (`216.239.38.120`).
  * **Bing:** Ghi đè `bing.com` trỏ về IP của `strict.bing.com` (`204.79.197.220`).
  * **DuckDuckGo:** Ghi đè `duckduckgo.com` trỏ về `safe.duckduckgo.com` (`52.142.124.215`).
  * **YouTube Content Filtering:** Ghi đè `youtube.com`, `m.youtube.com`, `youtubei.googleapis.com` trỏ về VIP `restrict.youtube.com` (`216.239.38.119`).
* **Hiệu quả thực tế:** Tính năng SafeSearch bị khóa cứng ở mức "Bật nghiêm ngặt" (Strict). Trẻ không thể tự tắt trong cài đặt trình duyệt!

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, một trong những 'kẽ hở' lớn nhất mà các phần mềm lọc thông thường hay bỏ quên là công cụ tìm kiếm và YouTube. Trẻ hoàn toàn có thể vào Google gõ từ khóa và bấm sang tab Hình ảnh để xem các nội dung người lớn.  
>  
> OGK giải quyết bài toán này một cách triệt để bằng kỹ thuật **Ghi đè địa chỉ IP dịch vụ an toàn (DNS VIP Rewriting)**:  
> Các tập đoàn công nghệ lớn như Google, Microsoft đã cung cấp sẵn các cụm máy chủ SafeSearch chuyên dụng. Khi tác tử phát hiện yêu cầu tìm kiếm, nó tự động đổi địa chỉ IP đích trỏ thẳng về cụm máy chủ an toàn `forcesafesearch.google.com` và `restrict.youtube.com`.  
> Kết quả là trên máy tính con, giao diện tìm kiếm luôn hiển thị dòng chữ: 'Chế độ tìm kiếm an toàn đã được quản trị viên mạng khóa bật'. Dù trẻ có cố tình vào cài đặt để tắt đi thì trang web vẫn tự động lọc sạch các nội dung nhạy cảm."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Nếu Google đổi địa chỉ IP của cụm máy chủ SafeSearch thì phần mềm của nhóm có bị lỗi thời không?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, các địa chỉ IP của cụm VIP này là các địa chỉ Anycast IP chuẩn toàn cầu được Google và Microsoft công bố trong tài liệu chính thức cho các tổ chức giáo dục và trường học, và chúng được duy trì cố định qua nhiều năm.  
    Tuy nhiên, để phòng ngừa rủi ro hạ tầng thay đổi, trong kiến trúc của OGK, các địa chỉ IP SafeSearch được nạp từ tệp cấu hình động trên máy chủ thông qua kênh đồng bộ chính sách. Khi các nhà cung cấp cập nhật địa chỉ mới, phụ huynh chỉ cần cập nhật danh mục trên máy chủ là toàn bộ các máy con tự động áp dụng bản ghi mới mà không cần biên dịch lại phần mềm ạ."*

---

## SLIDE 26: KỸ THUẬT LÕI TUẦN 3 (F2 & M3) — VÔ HIỆU HÓA DoH BẰNG CANARY DOMAIN
### 1. Nội dung hiển thị trên Slide
* **Kỹ thuật vượt rào DNS over HTTPS (DoH):**
  * Các trình duyệt hiện đại (Chrome, Edge, Firefox) tự động kích hoạt tính năng "Secure DNS" (DoH).
  * DoH mã hóa các truy vấn DNS thành các gói tin HTTPS bình thường qua cổng 443, khiến DNS Proxy ở cổng 53 bị "mù" và mất khả năng kiểm soát.
* **Cơ chế Khắc chế Mạng Chuẩn RFC (Canary Domain Defense):**
  * Các tổ chức tiêu chuẩn Internet (IETF, Mozilla, Google) đã thiết kế một tên miền chim báo bão (Canary Domain):
  $$\text{Canary Domain} = \text{use-application-dns.net}$$
  * Khi khởi động, trình duyệt sẽ gửi một truy vấn thăm dò tới tên miền này để kiểm tra xem mạng nội bộ có áp dụng chính sách lọc gia đình/trường học hay không.
  * **Giải pháp của OGK:** Khi phát hiện truy vấn tới `use-application-dns.net`, DNS Proxy lập tức trả về mã trạng thái **NXDOMAIN** (Tên miền không tồn tại).
  * **Kết quả:** Trình duyệt nhận được mã `NXDOMAIN` sẽ hiểu rằng mạng này có chính sách bảo vệ gia đình, và tự động tắt DoH, quay trở về phân giải qua DNS Socket cổng 53 của hệ điều hành!

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy, đây là một điểm kỹ thuật mạng rất sâu mà nhóm đặc biệt tâm đắc:  
> Khi xây dựng DNS Proxy, khó khăn lớn nhất là các trình duyệt hiện nay mặc định bật DNS over HTTPS (DoH). Nếu không xử lý DoH, đứa trẻ chỉ cần mở Chrome hay Firefox là toàn bộ cơ chế lọc mạng đều trở nên vô hiệu.  
>  
> Thay vì dùng các biện pháp thô bạo như can thiệp sâu vào Registry hay chặn toàn bộ cổng 443 làm hỏng kết nối web, nhóm đã nghiên cứu sâu tiêu chuẩn RFC và áp dụng cơ chế **Canary Domain (use-application-dns.net)**.  
> Bằng cách cấu hình DNS Proxy phản hồi mã `NXDOMAIN`, hệ thống kích hoạt đúng chuẩn quy ước nội tại của trình duyệt, khiến trình duyệt tự nguyện tắt DoH một cách văn minh, an toàn và bảo vệ được trọn vẹn khả năng kiểm soát tên miền."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Nếu trẻ tự tay vào Cài đặt trình duyệt, bật DoH thủ công và chọn một nhà cung cấp lạ (ví dụ Custom DoH Server IP) thì cơ chế Canary Domain có còn tác dụng không?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    Cơ chế Canary Domain xử lý triệt để 90% trường hợp DoH tự động của trình duyệt.  
    Trong trường hợp trẻ cố tình cấu hình thủ công một máy chủ DoH tùy chỉnh: Trình duyệt vẫn bắt buộc phải phân giải tên miền của máy chủ DoH đó trước. Danh mục cấm của OGK đã gieo mầm sẵn toàn bộ các tên miền DoH phổ biến (`cloudflare-dns.com`, `dns.google`, `dns.quad9.net`) trong danh mục cấm. Do đó, yêu cầu kết nối tới máy chủ DoH tùy chỉnh sẽ bị chặn ngay từ bước phân giải đầu tiên ạ."*

---

## SLIDE 27: KỸ THUẬT LÕI TUẦN 3 (F2) — KIỂM SOÁT ỨNG DỤNG BẰNG MÃ BĂM SHA-256
### 1. Nội dung hiển thị trên Slide
* **Lỗ hổng của việc lọc theo tên tiến trình:**
  * Nếu phần mềm cấm `RobloxPlayerBeta.exe`, đứa trẻ chỉ cần vào thư mục cài đặt đổi tên thành `winword.exe` là vượt rào thành công.
* **Giải pháp Kiểm soát bằng Chữ ký Nhị phân SHA-256 (T3_038 & T3_039):**
  * Tác tử `AppController` định kỳ quét danh sách tiến trình đang chạy mỗi 3 giây.
  * Lấy đường dẫn tệp thực thi gốc trên ổ đĩa thông qua `proc.exe()` và băm nội dung nhị phân bằng SHA-256:
  $$\text{Hash} = \text{SHA-256}(\text{Binary Bytes})$$
  * Dù trẻ có đổi tên file thành bất kỳ tên gì, mã băm SHA-256 của file nhị phân vẫn không thay đổi.
* **Tối ưu hóa Hiệu năng bằng Bộ nhớ đệm thời gian sửa đổi (mtime Cache):**
  * Việc băm các tệp game nặng (hàng trăm MB) liên tục sẽ gây nghẽn CPU và giật lag máy tính.
  * **Giải pháp:** Lưu cache bộ nhớ cặp `(mtime, sha256_hash)`. Chỉ tính toán lại mã băm khi thuộc tính ngày giờ sửa đổi của file (`os.path.getmtime`) thay đổi.
  * **Kết quả đo lường M4:** Mức chiếm dụng CPU trung bình đạt **0.0%**!

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, sang đến tầng kiểm soát ứng dụng, một câu hỏi lớn đặt ra là: Làm sao ngăn chặn được trẻ em qua mặt bằng cách đổi tên file?  
>  
> Câu trả lời kỹ thuật của OGK là **Kiểm soát bằng mã băm SHA-256 của tệp nhị phân trên đĩa**.  
> Khi một tiến trình khởi chạy, tác tử không tin tưởng tên file mà đọc cấu trúc nhị phân của nó để đối soát mã băm. Nếu trùng khớp với danh sách game cấm, tác tử lập tức gọi API `process.terminate()` để chấm dứt ứng dụng.  
>  
> Để giải quyết bài toán hiệu năng — tránh việc đọc đĩa và tính toán SHA-256 liên tục làm chậm máy con, nhóm áp dụng kỹ thuật **Bộ nhớ đệm theo mtime**: Tác tử chỉ tính mã băm một lần duy nhất cho mỗi tệp; các chu kỳ quét sau chỉ kiểm tra ngày sửa đổi tệp mất vài micro-giây. Nhờ đó, hiệu năng CPU đo được luôn ở mức 0.0%."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Nếu một game được cập nhật phiên bản mới (Patch Update), mã băm SHA-256 bị thay đổi thì bộ lọc có bị qua mặt không?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, đây là một câu hỏi thực tế rất hay!  
    Để giải quyết vấn đề game update làm thay đổi mã băm, OGK áp dụng **cơ chế phòng vệ chiều sâu kép (Dual-Defense)**:  
    1. Khi game vừa cập nhật, mã băm mới chưa kịp bổ sung vào database, nhưng tên tệp thực thi mặc định vẫn là tên game gốc ➜ Hệ thống chặn ngay bằng quy tắc Tên tệp.  
    2. Nếu trẻ đổi tên tệp để lách quy tắc tên ➜ Hệ thống kiểm tra mã băm.  
    Đồng thời, máy chủ hỗ trợ phụ huynh thêm mã băm mới chỉ bằng một cú nhấp chuột trên Web Dashboard, chính sách mới được đồng bộ tức thì xuống máy con qua WebSocket chưa đầy 1 giây ạ."*

---

## SLIDE 28: KỸ THUẬT LÕI TUẦN 3 (NT3 & NT5) — TIẾNG NÓI CỦA TRẺ & MINH BẠCH HAI CHIỀU
### 1. Nội dung hiển thị trên Slide
* **Hiện thực hóa Nguyên tắc Đạo đức NT3 & NT5:**
  * **NT3 — Trẻ có tiếng nói:** Trẻ không phải là đối tượng bị áp đặt thụ động, mà có quyền trao đổi dân chủ với cha mẹ.
  * **NT5 — Minh bạch hai chiều:** Trẻ có quyền nhìn thấy toàn bộ dữ liệu mà cha mẹ đang quan sát trên máy tính của mình.
* **Các tính năng trên Giao diện Tác tử Máy Con (Child Tray UI):**
  * **Đồng hồ trực quan:** Hiển thị số phút đã dùng và thời gian còn lại trong ngày; đếm ngược cảnh báo trước 10 phút, 5 phút, 1 phút.
  * **Hộp thoại "Xin Thêm Giờ":** Trẻ chọn các mức 15 phút, 30 phút, 60 phút kèm lý do (ví dụ: 'Con cần làm bài tập nhóm môn Tin học').
  * **Hộp thoại "Báo Chặn Nhầm":** Khi một trang web học tập bị bộ lọc chặn, trẻ bấm nút báo chặn nhầm để phụ huynh xem xét đưa vào Whitelist.
* **Xử lý Thời gian thực qua WebSocket:**
  * Phụ huynh nhận được thông báo ngay trên điện thoại/laptop; khi phụ huynh bấm "Đồng ý", máy con được cộng thêm giờ tức thì mà không cần khởi động lại.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy, điều làm nên sự khác biệt văn minh của Open Guardian Kids so với các phần mềm quản lý khác trên thị trường chính là sự **tôn trọng tiếng nói của con trẻ (Nguyên tắc NT3)**.  
>  
> Chúng em xây dựng một giao diện khay hệ thống thân thiện dành riêng cho con. Trẻ luôn biết rõ mình còn bao nhiêu phút để chủ động sắp xếp thời gian làm bài tập.  
> Khi hết giờ mà bài tập chưa xong, trẻ có quyền gửi yêu cầu 'Xin thêm giờ' kèm lý do chính đáng. Trên điện thoại, phụ huynh nhận được thông báo đẩy và có thể bấm duyệt tặng con 15 phút chỉ bằng một chạm.  
>  
> Mọi hành vi quản lý trở thành một cuộc đối thoại tin cậy và giáo dục, thay vì là những lệnh ngắt mạng đột ngột gây ức chế tâm lý cho trẻ."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Nếu trẻ spam liên tục hàng chục yêu cầu 'Xin thêm giờ' để làm phiền phụ huynh thì sao?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, trong mã nguồn `server/routes/requests.py`, nhóm đã cài đặt cơ chế kiểm soát trạng thái:  
    Mỗi thiết bị chỉ được phép có **tối đa 1 yêu cầu ở trạng thái 'pending' (chờ duyệt)** cho mỗi loại yêu cầu. Khi trẻ vừa gửi một yêu cầu xin thêm giờ, nút gửi sẽ bị khóa lại cho đến khi phụ huynh đưa ra quyết định (Chấp thuận hoặc Từ chối). Điều này ngăn chặn triệt để hành vi spam gây phiền toái cho cha mẹ ạ."*

---

## SLIDE 29: TỔNG KẾT NGHIỆM THU TUẦN 3 (VERSION 0.3)
### 1. Nội dung hiển thị trên Slide
* **Bảng tổng kết bàn giao Version 0.3:**
  * **Số tasks kỹ thuật hoàn thành:** 45/45 tasks (`T3_001` đến `T3_045`).
  * **Test Suite tự động tích lũy:** **38/38 tests PASSED (100%)**.
* **Các thành phần cốt lõi đã nghiệm thu:**
  1. DNS Proxy Socket UDP 53 (`agent/dns_proxy.py`) chạy ổn định trên localhost.
  2. Cơ chế chặn tên miền cấm với Sinkhole `0.0.0.0` và Synthetic Records.
  3. SafeSearch Google/Bing và YouTube Restricted Mode CNAME rewrite.
  4. Triệt tiêu DoH bằng NXDOMAIN Canary Domain `use-application-dns.net`.
  5. Giám sát ứng dụng bằng SHA-256 (`agent/app_controller.py`) với mtime cache CPU 0%.
  6. Giao diện trẻ em tương tác 2 chiều (Yêu cầu thêm giờ, Báo chặn nhầm).
  7. Báo cáo Chuyên sâu Kỹ thuật Mạng M1 (DNS Packet Flow) và M2 (So sánh 4 phương án chặn).

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, khép lại Tuần 3, nhóm đã hoàn thành toàn diện 45 tasks kỹ thuật và nâng tổng số bài kiểm thử tự động lên **38/38 tests Passed 100%**.  
> Toàn bộ các cơ chế kiểm soát mạng ở tầng DNS và kiểm soát ứng dụng bằng mã băm SHA-256 đã vận hành trơn tru, tạo bước đệm hoàn hảo để bước vào Tuần 4 — tuần cuối cùng đóng gói toàn bộ đồ án và gia cố bảo mật cấp cao."*

---

## SLIDE 30: TỔNG QUAN VERSION 0.4 (TUẦN 4) — HOÀN THIỆN ĐỒ ÁN TỐT NGHIỆP
### 1. Nội dung hiển thị trên Slide
* **Mục tiêu của Tuần 4 (Final Release):**
  * Nâng cấp hệ thống từ mức "Chạy được tính năng" lên mức **"Chuẩn mực An toàn Thông tin & Tuân thủ Pháp luật Việt Nam"**.
* **4 Nhóm Trọng tâm Kỹ thuật Tuần 4:**
  1. **Bảo mật Cấp cao F5 (ASVS Level 1 & NIST SP 800-63B):** Khóa tài khoản 15 phút sau 5 lần sai, Mật khẩu $\ge 10$ ký tự, Chống IDOR 100%, Mã hóa AES-256-GCM.
  2. **Tuân thủ Nghị định 13/2023/NĐ-CP:** Tự động tiêu hủy dữ liệu 90 ngày, Quyền xóa toàn bộ dữ liệu của con (Right to Erasure).
  3. **Khắc chế 7 Kỹ thuật Vượt rào M3 (Anti-Bypass Guard):** `DNSWatchdog` 20s tự phục hồi `127.0.0.1` & Chặn các tiến trình VPN.
  4. **Thực nghiệm Đo lường M4 & Chịu lỗi M5:** Đo đạc 30 mẫu số liệu thực tế (RAM, CPU, DNS p50/p95, WebSocket) & Kiểm chứng chịu lỗi mất mạng.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy, một đồ án tốt nghiệp chuyên ngành Mạng Máy Tính không thể chỉ dừng lại ở việc phần mềm chạy được, mà phải chứng minh được: **Hệ thống có an toàn trước các cuộc tấn công không? Có bảo vệ dữ liệu người dùng theo đúng luật pháp không? Và hiệu năng thực tế đo đạc được là bao nhiêu?**  
>  
> Đó chính là lý do Tuần 4 ra đời với mục tiêu hoàn thiện Version 0.4: Biến OGK thành một giải pháp phần mềm chuyên nghiệp, đạt chuẩn kiểm định an toàn thông tin OWASP ASVS v4 Level 1 và tuân thủ nghiêm ngặt Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân của trẻ em trên không gian mạng."*

---

## SLIDE 31: BẢO MẬT CẤP CAO F5 — MẬT KHẨU $\ge 10$ KÝ TỰ, BRUTE-FORCE LOCKOUT & IP RATE LIMIT
### 1. Nội dung hiển thị trên Slide
* **Chuẩn Mật khẩu NIST SP 800-63B:**
  * Bắt buộc độ dài tối thiểu 10 ký tự. Từ chối các mật khẩu ngắn dễ đoán với mã lỗi `HTTP 422`.
  * Băm mật khẩu bằng thuật toán **Argon2id** (Memory-hard function), vô hiệu hóa hoàn toàn các giàn máy đào bẻ khóa bằng GPU hoặc ASIC.
* **Cơ chế Khóa Tài Khoản Chống Tấn Công Brute-Force (T4_003 & T4_004):**
  * Theo dõi số lần đăng nhập thất bại liên tiếp `failed_login_attempts`.
  * **Tại lần sai thứ 5:** Lập tức kích hoạt khóa tài khoản 15 phút (`locked_until = now + 15m`).
  * Phản hồi mã lỗi **HTTP 423 Locked** kèm đồng hồ đếm ngược.
  * Trong 15 phút này, dù kẻ tấn công có nhập đúng mật khẩu, hệ thống vẫn kiên quyết từ chối đăng nhập!
* **In-memory IP Rate Limiting (T4_005):**
  * Giới hạn tối đa **10 requests/phút** trên mỗi địa chỉ IP nguồn tại các endpoint nhạy cảm (`/api/v1/auth/login`, `/token`, `/pairing`). Ngăn chặn bot tự động dò quét.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, tài khoản của phụ huynh là nơi nắm giữ toàn bộ quyền điều khiển thiết bị của con. Nếu tài khoản cha mẹ bị tấn công dò mật khẩu (Brute-Force), toàn bộ hàng rào bảo vệ sẽ sụp đổ.  
>  
> Để đạt chuẩn an toàn OWASP ASVS v4 Level 1, nhóm đã hiện thực hóa trọn vẹn 3 lớp phòng ngự:  
> Thứ nhất, ép buộc mật khẩu tối thiểu 10 ký tự theo hướng dẫn mới nhất của NIST SP 800-63B và mã hóa bằng Argon2id.  
> Thứ hai, áp dụng cơ chế khóa tài khoản lũy tiến: Sau 5 lần nhập sai, tài khoản bị phong tỏa ngay trong 15 phút.  
> Thứ ba, tích hợp bộ lọc tần suất IP (Rate Limiter) giới hạn 10 lượt gọi/phút, bẻ gãy mọi công cụ dò quét tự động của tin tặc."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Tại sao lại dùng Argon2id mà không dùng SHA-256 hay MD5 để băm mật khẩu cho nhanh?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, trong bảo mật xác thực, hàm băm càng nhanh thì càng nguy hiểm!  
    SHA-256 hay MD5 là các hàm băm nhanh, một card đồ họa GPU hiện đại có thể thử hàng tỷ phép tính SHA-256 mỗi giây để phá khóa mật khẩu trong tích tắc.  
    Ngược lại, Argon2id là thuật toán chiến thắng trong cuộc thi băm mật khẩu thế giới (Password Hashing Competition): Nó được thiết kế ngốn bộ nhớ RAM (Memory-hard) và tốn tài nguyên xử lý có chủ đích. Để thử một mật khẩu trên Argon2id mất khoảng 50-100 mili-giây, khiến việc dùng GPU phá khóa trở nên bất khả thi về mặt kinh tế và thời gian ạ."*

---

## SLIDE 32: BẢO MẬT CẤP CAO F5 — MÃ HÓA AES-256-GCM & CHỐNG LỖ HỔNG IDOR
### 1. Nội dung hiển thị trên Slide
* **Mã hóa Dữ liệu Tĩnh AES-256-GCM AEAD (T4_007):**
  * Sử dụng thuật toán mã hóa đối xứng xác thực cao cấp nhất: **AES-256 trong chế độ Galois/Counter Mode (GCM)**.
  * Mỗi bản ghi được mã hóa với một **Nonce ngẫu nhiên 12 bytes** (duy nhất trên mỗi lượt mã hóa) và **Authentication Tag 16 bytes**.
  * Đảm bảo cả hai tiêu chí: **Tính bảo mật** (không thể đọc nội dung) và **Tính toàn vẹn** (nếu cơ sở dữ liệu bị chỉnh sửa dù chỉ 1 bit, hàm giải mã sẽ lập tức ném lỗi `InvalidTag` và từ chối nạp).
* **Triệt tiêu 100% Lỗ hổng IDOR (Insecure Direct Object References):**
  * Lỗ hổng IDOR xảy ra khi Phụ huynh A đổi `device_id=2` trên đường dẫn URL để xem trộm hoặc điều khiển máy tính con của Phụ huynh B.
  * **Cơ chế xác thực của OGK (T4_008 – T4_010):** Mọi API nhận `device_id` đều bắt buộc kiểm tra quan hệ sở hữu:
  $$\text{assert } \text{device.parent\_id} == \text{current\_parent.id}$$
  * Phụ huynh A cố tình thao tác trên thiết bị của Phụ huynh B lập tức bị từ chối với mã lỗi **HTTP 403 Forbidden**.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, một lỗ hổng bảo mật cực kỳ nguy hiểm trong các ứng dụng quản lý thiết bị là **lỗ hổng IDOR (Insecure Direct Object References)**. Hãy thử tưởng tượng một kẻ xấu tạo một tài khoản phụ huynh bình thường, sau đó thay đổi số ID thiết bị trên đường truyền mạng để ra lệnh khóa máy tính hoặc xem lịch sử hoạt động của con nhà người khác!  
>  
> Trong Version 0.4, nhóm đã rà soát 100% các endpoint từ API phát lệnh khẩn cấp, xem báo cáo, sửa chính sách đến duyệt yêu cầu: Bất kỳ request nào không chứng minh được quyền sở hữu chính chủ đối với thiết bị đều bị hệ thống chặn đứng với mã lỗi HTTP 403 Forbidden.  
> Đồng thời, các trường dữ liệu nhạy cảm được bảo vệ bằng mã hóa đối xứng xác thực AES-256-GCM, bảo đảm an toàn dữ liệu tĩnh theo đúng chuẩn ASVS v4."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Chế độ AES-GCM khác gì so với chế độ AES-CBC truyền thống?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    AES-CBC chỉ cung cấp tính bảo mật (Confidentiality) nhưng không có cơ chế xác thực toàn vẹn, do đó dễ bị tấn công sửa đổi bản mã (Padding Oracle Attack hay Bit-Flipping Attack).  
    Trong khi đó, AES-GCM là chuẩn mã hóa xác thực kết hợp (Authenticated Encryption with Associated Data - AEAD): Nó tạo ra một Authentication Tag 16 bytes đi kèm bản mã. Nếu kẻ tấn công can thiệp vào cơ sở dữ liệu để sửa đổi dù chỉ 1 bit, quá trình giải mã sẽ phát hiện sai lệch Tag ngay lập tức và từ chối dữ liệu, bảo vệ tính toàn vẹn tuyệt đối cho hệ thống ạ."*

---

## SLIDE 33: PHÁP LÝ & ĐẠO ĐỨC — TUÂN THỦ NGHỊ ĐỊNH 13/2023/NĐ-CP & QUYỀN XÓA DỮ LIỆU CON
### 1. Nội dung hiển thị trên Slide
* **Căn cứ Pháp lý Bắt buộc:**
  * **Nghị định 13/2023/NĐ-CP** (Bảo vệ dữ liệu cá nhân, đặc biệt là Dữ liệu cá nhân của trẻ em tại Điều 20).
  * **Luật Trẻ Em 2016** (Quyền được bảo vệ bí mật đời tư tại Điều 21).
* **2 Tính năng Pháp lý Đột phá Hiện thực trong Version 0.4:**
  1. **Tự động tiêu hủy dữ liệu sau 90 ngày (Data Retention Purge - T4_011):**
     * Tác vụ ngầm định kỳ 24h tự động quét và xóa vĩnh viễn các bản ghi sự kiện viễn trắc và nhịp tim cũ hơn 90 ngày khỏi máy chủ.
  2. **Quyền yêu cầu xóa toàn bộ dữ liệu của con (Right to Erasure - T4_013 – T4_016):**
     * Giao diện Dashboard trang bị nút đỏ: *"Xóa Toàn Bộ Dữ Liệu Con (NĐ 13)"*.
     * Hộp thoại xác nhận yêu cầu nhập mật khẩu phụ huynh để chống bấm nhầm.
     * Khi kích hoạt:
       - Xóa sạch 100% lịch sử hoạt động, nhịp tim trên máy chủ.
       - Gửi lệnh qua WebSocket `purge_local_data` ra lệnh cho máy con xóa sạch bộ nhớ đệm SQLite ngoại tuyến.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy, một trong những đóng góp mang tính xã hội và pháp lý lớn nhất của đồ án là **Sự tuân thủ nghiêm túc Nghị định 13/2023/NĐ-CP của Chính phủ về bảo vệ dữ liệu cá nhân của trẻ em**.  
>  
> Đa số các phần mềm thương mại hiện nay thu thập dữ liệu của trẻ và lưu trữ vĩnh viễn trên Cloud để bán quảng cáo hoặc phân tích dữ liệu. Điều này vi phạm nghiêm trọng luật pháp Việt Nam.  
>  
> Trong OGK, chúng em hiện thực hóa hai cam kết pháp lý bằng mã nguồn:  
> Thứ nhất, **Chính sách tự động tiêu hủy sau 90 ngày**: Dữ liệu hoạt động cũ hơn 90 ngày sẽ tự động biến mất vĩnh viễn.  
> Thứ hai, **Quyền được xóa dữ liệu (Right to Erasure)**: Bất cứ lúc nào cha mẹ muốn, họ chỉ cần nhập mật khẩu là toàn bộ dữ liệu của con trên Server lẫn Agent máy con đều bị xóa sạch sẽ không để lại dấu vết."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Tại sao khi xóa dữ liệu của con lại cần phải phát lệnh WebSocket xuống xóa cả bộ nhớ đệm trên máy con?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    Bởi vì để đảm bảo khả năng chịu lỗi khi mất mạng (Fault Tolerance), tác tử máy con luôn có một tệp cơ sở dữ liệu SQLite cục bộ (`agent_cache.db`) để lưu trữ đệm các sự kiện offline.  
    Nếu chỉ xóa trên máy chủ mà không xóa trên máy con, thì ngay khi máy tính có kết nối mạng trở lại, tác tử sẽ tự động đẩy bù các sự kiện cũ này lên máy chủ ➜ Dẫn đến việc dữ liệu bị phục hồi trái với ý muốn của phụ huynh.  
    Do đó, quy trình xóa dữ liệu của OGK là **Quy trình xóa đồng bộ hai chiều (Synchronous Purge)**: Xóa trên Server đồng thời phát lệnh tiêu hủy tệp đệm ngoại tuyến của Agent ạ."*

---

## SLIDE 34: BÁO CÁO KỸ THUẬT MẠNG M3 — KHẮC CHẾ 7 KỸ THUẬT VƯỢT RÀO (ANTI-BYPASS GUARD)
### 1. Nội dung hiển thị trên Slide
* **Phân tích Thực nghiệm 7 Kỹ thuật Vượt rào Mạng của Trẻ (M3):**
  1. *Đổi DNS card mạng sang 8.8.8.8:* `DNSWatchdog` chạy ngầm chu kỳ 20s, phát hiện và tự hoàn nguyên về `127.0.0.1` bằng `netsh` trong $\le 20$ giây.
  2. *Bật DoH trong trình duyệt:* Bắt Canary Domain `use-application-dns.net` trả về `NXDOMAIN`, ép tắt DoH.
  3. *Sử dụng DoT (Cổng 853):* Tên miền máy chủ DoT bị chặn ngay từ bước phân giải DNS.
  4. *Cài phần mềm VPN / Proxy (WARP, Proton, Psiphon, UltraSurf):* `AppController` tiêu diệt tiến trình trong 3 giây bằng đối soát kép SHA-256 + Tên file.
  5. *Truy cập trực tiếp bằng địa chỉ IP:* Các website hiện đại dùng HTTPS chia sẻ IP kèm SNI, việc gõ IP thô sẽ bị máy chủ từ chối chứng chỉ TLS.
  6. *Khởi động Windows ở chế độ Safe Mode:* Yêu cầu phụ huynh đặt mật khẩu tài khoản Administrator, chỉ cấp tài khoản Standard cho trẻ.
  7. *Tắt tiến trình Agent trong Task Manager:* Agent chạy dưới dạng dịch vụ ngầm hệ thống (Session 0 Isolation), trẻ dùng tài khoản Standard không có quyền `kill` tiến trình (`Access Denied`).

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, một hệ thống quản lý có hay đến đâu nhưng nếu trẻ em có thể dễ dàng vượt qua chỉ bằng vài thủ thuật trên mạng thì hệ thống đó coi như thất bại.  
> Trong Phụ lục Kỹ thuật Mạng M3, nhóm đã lập danh mục và thực nghiệm tấn công vượt rào với **7 kỹ thuật phổ biến nhất của trẻ**: từ đổi DNS card mạng, dùng VPN, bật DoH cho đến việc mở Task Manager để tắt ứng dụng.  
>  
> Chúng em đã hiện thực hóa module **DNSWatchdog** chạy ngầm: Cứ 20 giây một lần, Watchdog kiểm tra card mạng; nếu trẻ vừa đổi DNS sang 8.8.8.8, Watchdog tự động thiết lập lại về 127.0.0.1 và gửi cảnh báo viễn trắc.  
> Đồng thời, các ứng dụng VPN vượt rào phổ biến như WARP hay Psiphon đều bị bộ quét tiến trình phát hiện và cưỡng bức chấm dứt trong vòng 3 giây."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Nếu trẻ rút dây mạng hoặc ngắt Wi-Fi rồi mới đổi DNS card mạng thì Watchdog có phục hồi được không?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, có ạ!  
    Lệnh `netsh interface ipv4 set dns` là lệnh cấu hình cục bộ của hệ điều hành Windows, hoàn toàn không phụ thuộc vào kết nối Internet. Dù máy đang offline, vòng lặp Watchdog vẫn quét đều đặn và tự động sửa DNS card mạng về `127.0.0.1`. Khi trẻ bật mạng trở lại, DNS vẫn đang trỏ vào Proxy của Agent và cơ chế kiểm soát tiếp tục vận hành bình thường ạ."*

---

## SLIDE 35: BÁO CÁO KỸ THUẬT MẠNG M4 — THỰC NGHIỆM ĐO LƯỜNG HIỆU NĂNG HỆ THỐNG
### 1. Nội dung hiển thị trên Slide
* **Phương pháp Đo đạc Thực nghiệm (M4):**
  * Script tự động [`scripts/benchmark_performance.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/scripts/benchmark_performance.py).
  * Đo đạc trên môi trường Windows 10/11 x64 thực tế với **$\ge 30$ mẫu đo độc lập**.
* **Bảng Số Liệu Thực Nghiệm Chi Tiết (DoD 4):**
  * **RAM Footprint (Chế độ nghỉ & Tải cao):** **25.13 MB** (Đạt chuẩn DoD $\le 26.0$ MB).
  * **CPU Footprint (Trung bình):** **0.0%** (Đạt chuẩn DoD $< 1.0\%$).
  * **Độ trễ Phân giải DNS Proxy (Median p50):** **0.83 ms** (Nhanh hơn truy vấn trực tiếp Upstream 1.1.1.3: **35.75 ms** $\rightarrow$ Nhanh gấp 43 lần!).
  * **Độ trễ DNS Proxy (p95):** **104.43 ms** (Đạt chuẩn $< 200$ ms).
  * **Độ trễ Phát Lệnh Khẩn Cấp (WebSocket):** **5.91 ms** (Vượt xa tiêu chuẩn DoD $< 500$ ms $\rightarrow$ Nhanh gấp 84 lần!).
* **Kết luận:** Tác tử Client siêu nhẹ, hoàn toàn không gây giật lag máy tính của trẻ.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy, đây là bảng số liệu thực nghiệm khoa học của Phụ lục Kỹ thuật Mạng M4:  
> Nhóm đã xây dựng một kịch bản đo đạc tự động với hơn 30 mẫu đo độc lập trên môi trường Windows thật.  
>  
> Kết quả cho thấy:  
> Mức chiếm dụng bộ nhớ RAM của Agent chỉ vỏn vẹn **25.13 MB** và CPU ở mức **0.0%**, đáp ứng trọn vẹn tiêu chuẩn siêu nhẹ của đồ án.  
> Đặc biệt về độ trễ mạng: Khi trẻ truy cập các tên miền bị chặn, DNS Proxy xử lý và trả kết quả Sinkhole chỉ trong **0.83 mili-giây**, nhanh hơn gấp 43 lần so với việc gửi gói tin ra Internet tới máy chủ Cloudflare (35.75 ms).  
> Còn kênh lệnh khẩn cấp WebSocket, khi cha mẹ bấm khóa máy từ xa, thời gian lệnh truyền từ máy chủ tới máy con chỉ mất **5.91 mili-giây** — gần như là tức thời!"*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi:** *"Tại sao độ trễ DNS Proxy p50 là 0.83 ms nhưng p95 lại lên tới 104 ms?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    - Chỉ số **p50 (0.83 ms)** đại diện cho các truy vấn rơi vào tên miền cấm (được trả về Sinkhole `0.0.0.0` ngay trong bộ nhớ RAM máy con) hoặc các tên miền đã có trong DNS Cache nội bộ.  
    - Trong khi đó, chỉ số **p95 (104 ms)** rơi vào các trường hợp tên miền an toàn chưa có trong cache: Proxy bắt buộc phải gửi gói tin UDP qua mạng Internet đến máy chủ Upstream Cloudflare (`1.1.1.3`) và chờ phản hồi qua đường truyền mạng vật lý. Do độ trễ mạng Internet công cộng dao động từ 30 đến 100 ms nên kéo theo p95 cao hơn, nhưng vẫn nằm an toàn dưới ngưỡng chuẩn 200 ms của đồ án ạ."*

---

## SLIDE 36: BÁO CÁO KỸ THUẬT MẠNG M5 — KHẢ NĂNG CHỊU LỖI & PHỤC HỒI MẠNG (FAULT TOLERANCE)
### 1. Nội dung hiển thị trên Slide
* **3 Kịch bản Chịu lỗi Thực tế Khắc nghiệt Được Kiểm chứng:**
  1. **Kịch bản 1: Mất kết nối Internet / Rút cáp mạng:**
     * Sự kiện viễn trắc và nhịp tim được lưu an toàn vào tệp SQLite bộ đệm ngoại tuyến `agent_cache.db`.
     * Khi có mạng trở lại: Luồng đồng bộ tự động đẩy hàng loạt lên máy chủ; máy chủ sử dụng khóa `idempotency_key` để chống trùng lặp dữ liệu.
  2. **Kịch bản 2: Máy chủ trung tâm bị ngừng hoạt động (Server Outage):**
     * Tác tử chuyển sang chế độ tự trị (Autonomous Mode).
     * Tiếp tục đếm thời gian bằng `time.monotonic()`. Khi hết hạn mức giờ chơi, máy tính **tự động khóa màn hình ngay lập tức**, không cho phép trẻ chơi quá giờ dù mất kết nối máy chủ!
  3. **Kịch bản 3: Khởi động lại máy tính (Reboot Recovery):**
     * Số phút đã dùng trong ngày được ghi đều đặn vào SQLite.
     * Khi máy khởi động lại, tác tử đọc lại số phút cũ và tiếp tục cộng dồn, trẻ không thể reset giờ chơi bằng cách restart máy tính.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, một trong những tình huống thực tế hay xảy ra nhất là mạng Internet gia đình bị chập chờn hoặc đứa trẻ cố tình rút cáp mạng ra để chơi game thoải mái.  
>  
> Trong Phụ lục Kỹ thuật Mạng M5, chúng em đã thiết kế kiến trúc **Chịu lỗi tự trị (Autonomous Fault Tolerance)**:  
> Máy con không hề bị động phụ thuộc vào Server. Khi mất mạng, đồng hồ phần cứng vẫn đếm và máy tính vẫn khóa đúng giờ. Toàn bộ nhật ký hoạt động được đệm vào SQLite cục bộ và sẽ tự động đồng bộ bù khi có mạng trở lại mà không mất mát dù chỉ một dòng dữ liệu.  
> Cả 3 kịch bản này đều đã được kiểm thử tự động trong tệp `test_fault_tolerance.py` với kết quả đạt 100% ạ."*

---

## SLIDE 37: HỒ SƠ ĐỒ ÁN & AN NINH MẠNG — MÔ HÌNH STRIDE & OWASP ASVS v4
### 1. Nội dung hiển thị trên Slide
* **Mô hình Đe dọa STRIDE (8 Mối đe dọa an ninh mạng):**
  * *Spoofing (Giả mạo):* Giả mạo nhịp tim Agent ➜ Chặn bằng Bearer Token và Fingerprint phần cứng.
  * *Tampering (Can thiệp):* Sửa database chính sách cục bộ ➜ Chặn bằng chữ ký HMAC-SHA256.
  * *Repudiation (Chối bỏ):* Cha mẹ đổi luật rồi chối ➜ Chặn bằng Audit Log minh bạch không thể sửa.
  * *Information Disclosure (Lộ lọt thông tin):* Lộ dữ liệu con ➜ Chặn bằng Tối thiểu dữ liệu NT2 và AES-256-GCM.
  * *Denial of Service (Từ chối dịch vụ):* Tấn công DoS Server ➜ Chặn bằng IP Rate Limiting 10 req/phút.
  * *Elevation of Privilege (Leo thang đặc quyền):* Lỗ hổng IDOR ➜ Chặn bằng xác thực quyền sở hữu thiết bị.
* **Bảng Kiểm Soát An Toàn OWASP ASVS v4 Level 1:**
  * Hoàn thành trọn vẹn **22/22 tiêu chí** kiểm soát bảo mật ứng dụng web và API.
* **Bản Minh Bạch AI (AI Usage Disclosure):**
  * Công khai minh bạch trách nhiệm học thuật theo chuẩn mực đồ án tốt nghiệp.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, để nâng tầm đồ án thành một công trình nghiên cứu chuẩn mực, nhóm đã xây dựng **Mô hình đe dọa STRIDE** phân tích 8 nguy cơ tấn công mạng tiềm ẩn và đối sách tương ứng của OGK.  
> Hệ thống cũng được đối chiếu và đáp ứng đầy đủ **22 tiêu chí kiểm soát an toàn của chuẩn quốc tế OWASP ASVS v4 Level 1**.  
> Đồng thời, tuân thủ nguyên tắc trung thực khoa học, nhóm đã công bố **Bản minh bạch ứng dụng AI (AI_USAGE.md)**, giải trình rõ ràng các phần có sự hỗ trợ của trí tuệ nhân tạo và quy trình kiểm chứng chéo bằng kiểm thử tự động của nhóm."*

---

## SLIDE 38: TỔNG KẾT NGHIỆM THU ĐẦU-CUỐI VER 4 (v0.4) — ĐẠT TRỌN VẸN 5 TIÊU CHUẨN DoD
### 1. Nội dung hiển thị trên Slide
* **Bảng Đối chiếu 5 Tiêu chuẩn Nghiệm thu Đầu-cuối (Definition of Done - DoD Week 4):**
  * **DoD 1 (Bảo mật F5):** Mật khẩu $\ge 10$ ký tự, Khóa 15p sau 5 lần sai, Chống IDOR 100%, AES-256-GCM AEAD $\rightarrow$ **ĐẠT [✓]**
  * **DoD 2 (Pháp lý NĐ 13):** Tự động xóa dữ liệu 90 ngày, Chức năng xóa toàn bộ dữ liệu của con có mật khẩu $\rightarrow$ **ĐẠT [✓]**
  * **DoD 3 (Khắc chế M3):** `DNSWatchdog` phục hồi `127.0.0.1` trong $\le 20$s, Chặn VPN trong $\le 3$s $\rightarrow$ **ĐẠT [✓]**
  * **DoD 4 (Hiệu năng M4 & M5):** RAM 25.13 MB, CPU 0.0%, DNS 0.83 ms, WebSocket 5.91 ms, Chịu lỗi mất mạng $\rightarrow$ **ĐẠT [✓]**
  * **DoD 5 (Test Suite & Hồ sơ):** 61/61 Automated Tests PASSED (100%), Đầy đủ 6 báo cáo M1-M6 và tài liệu pháp lý $\rightarrow$ **ĐẠT [✓]**

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy, căn cứ theo Bản kế hoạch chi tiết Tuần 4 đã được thống nhất, toàn bộ **5 nhóm tiêu chuẩn nghiệm thu đầu-cuối (Definition of Done)** của đồ án đều đã được hoàn thành xuất sắc với đầy đủ bằng chứng kỹ thuật và kết quả đo đạc thực nghiệm. Không có bất kỳ hạng mục nào bị bỏ sót hay hoãn lại."*

---

## SLIDE 39: TOÀN CẢNH KIỂM THỬ TỰ ĐỘNG — 61/61 TESTS PASSED 100%
### 1. Nội dung hiển thị trên Slide
* **Kết quả thực thi Test Suite toàn hệ thống (pytest):**
  * `tests/test_security_f5.py`: **15/15 PASSED** (Lockout, Password policy, IDOR, AES-256, Purge 90-day, Watchdog)
  * `tests/test_fault_tolerance.py`: **3/3 PASSED** (Mất mạng đệm SQLite, Server sập, Reboot recovery)
  * `tests/test_dns_proxy.py`: **9/9 PASSED** (Domain matching, SafeSearch, DoH Canary, Whitelist NT6)
  * `tests/test_app_filtering_and_events.py`: **5/5 PASSED** (Băm SHA-256, Idempotency, Yêu cầu trẻ)
  * `tests/test_auth.py`: **10/10 PASSED** (Argon2id, JWT tamper, Brute-force, IP rate limit)
  * `tests/test_enrollment.py`: **6/6 PASSED** (Ghép đôi 8 ký tự, TTL 10 phút, Anti-replay)
  * `tests/test_heartbeat.py`: **4/4 PASSED** (Nhịp tim 60s, Ngưỡng 120s Online/Offline)
  * `tests/test_policy.py`: **4/4 PASSED** (HMAC-SHA256, Ma trận 7x48, Anti-IDOR)
  * `tests/test_time_tracker.py`: **4/4 PASSED** (time.monotonic, Chống tua giờ M6)
  * `tests/test_websocket_command.py`: **1/1 PASSED** (Kênh lệnh khẩn WebSocket < 500ms)
* **Tổng kết:** **61 passed in 9.83s — Pass Rate: 100% tuyệt đối!**

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, đây là bức tranh toàn cảnh về chất lượng phần mềm của đồ án:  
> Toàn bộ 61 bài kiểm thử tự động bao phủ trọn vẹn từ tầng mạng DNS, tầng lõi hệ điều hành, tầng cơ sở dữ liệu cho tới tầng bảo mật API đều chạy thành công 100% chỉ trong 9.83 giây.  
> Con số này khẳng định tính ổn định, độ tin cậy và khả năng triển khai thực tế của hệ thống Open Guardian Kids."*

---

## SLIDE 40: KẾT LUẬN TOÀN DIỆN ĐỒ ÁN TỐT NGHIỆP & PHIÊN VẤN ĐÁP PHẢN BIỆN
### 1. Nội dung hiển thị trên Slide
* **Tổng kết Giá trị Đạt được của Đồ án Open Guardian Kids:**
  1. *Giá trị Kỹ thuật Mạng & Hệ thống:* Làm chủ công nghệ DNS Sinkhole cổng 53, vô hiệu hóa DoH, đối soát SHA-256 tối ưu CPU 0%, đồng hồ đơn điệu `time.monotonic()` chống tua giờ, và lệnh khẩn cấp WebSocket 5.91 ms.
  2. *Giá trị An toàn Thông tin:* Đạt chuẩn OWASP ASVS v4 Level 1 và NIST SP 800-63B, triệt tiêu 100% lỗ hổng IDOR, mã hóa AES-256-GCM AEAD.
  3. *Giá trị Pháp lý & Xã hội:* Tiên phong tuân thủ Nghị định 13/2023/NĐ-CP và Luật Trẻ Em 2016, tạo ra một công cụ giáo dục đồng hành văn minh, kiên quyết bài trừ Stalkerware xâm phạm đời tư.
  4. *Khả năng Triển khai Thực tế:* Đã đóng gói file thực thi `ogk-agent.exe`, sẵn sàng triển khai trên Cloud (Render/Railway/Docker).
* **Lời cảm ơn & Khai mạc Phiên Vấn đáp Phản biện:**
  * Nhóm chúng em xin chân thành cảm ơn Thầy và quý Thầy Cô trong Hội đồng!
  * Chúng em xin sẵn sàng tiếp nhận các câu hỏi phản biện của Hội đồng.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy và quý Thầy Cô trong Hội đồng phản biện,  
>  
> Trải qua 4 tuần nghiên cứu và thực hiện nghiêm túc, đề tài **'Xây dựng ứng dụng hỗ trợ quản lý việc sử dụng máy tính của trẻ em' (Open Guardian Kids)** đã về đích thành công trọn vẹn.  
> Chúng em đã chứng minh được rằng: Bằng kiến thức chuyên sâu về mạng máy tính, hệ điều hành và an toàn thông tin, chúng ta hoàn toàn có thể xây dựng một giải pháp bảo vệ con trẻ an toàn trên không gian số mà vẫn giữ trọn sự tôn trọng và niềm tin trong gia đình.  
>  
> Nhóm chúng em xin chân thành cảm ơn Thầy đã luôn tận tình hướng dẫn và định hướng cho chúng em trong suốt quá trình thực hiện đồ án.  
> Sau đây, nhóm chúng em xin trân trọng kính mời quý Thầy Cô đưa ra những nhận xét và câu hỏi phản biện ạ!"*

### 3. Góc Phản Biện Chốt (Thầy sẽ hỏi câu gì?)
* ❓ **Thầy hỏi câu hỏi kết luận:** *"Nếu có thêm thời gian 3 tháng để phát triển sản phẩm này thương mại hóa, nhóm sẽ ưu tiên làm tính năng gì tiếp theo?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, nếu có thêm thời gian, nhóm sẽ tập trung vào 3 hướng phát triển chiến lược:  
    1. **Mở rộng Đa nền tảng:** Phát triển Tác tử Agent cho hệ điều hành **Android và iOS** (sử dụng Network Extension API và Local VPN Profile của hệ điều hành di động) để phụ huynh quản lý đồng bộ cả máy tính lẫn điện thoại của con trên cùng một Dashboard.  
    2. **Trí tuệ nhân tạo Cục bộ (Edge AI Content Safety):** Tích hợp mô hình AI nhẹ chạy cục bộ (on-device) phân loại mức độ an toàn của trang web dựa trên nội dung bài viết và ngôn từ mà không cần gửi dữ liệu ra máy chủ ngoài.  
    3. **Ứng dụng Mobile Native cho Phụ huynh:** Đóng gói ứng dụng di động Flutter/React Native có tính năng Push Notification thời gian thực (qua FCM/APNs) để cha mẹ nhận thông báo khẩn cấp ngay trên màn hình khóa điện thoại ạ."*

---

# TỔNG HỢP BẢNG TRA CỨU NHANH CHO TUẦN 3 & TUẦN 4 (QUICK CHEAT-SHEET PART 2)

| Khái niệm / Vị trí Slide | Thầy thường hỏi | Câu trả lời nhanh & Mã nguồn chứng minh |
| :--- | :--- | :--- |
| **DNS Sinkhole 0.0.0.0** (Slide 23) | Vì sao không trả về 127.0.0.1? | Tránh xung đột web server cục bộ và timeout; 0.0.0.0 bị Socket từ chối ngay lập tức. `agent/dns_proxy.py`. |
| **Độ trễ Sinkhole** (Slide 23) | Phản hồi trong bao lâu? | 0.83 ms nội bộ (nhanh hơn 40 lần so với truy vấn 1.1.1.3 tốn 35.75 ms). `docs/M4_DO_LUONG_HIEU_NANG.md`. |
| **Immutable Whitelist NT6** (Slide 24) | Chặn cổng 111 được không? | Bị từ chối cứng bằng ngoại lệ `NT6ViolationError`. Xem `agent/dns_proxy.py:88`. |
| **Canary Domain DoH** (Slide 26) | Tên miền gì? Trả về mã gì? | `use-application-dns.net`, trả về `NXDOMAIN` ➜ Trình duyệt tự tắt DoH về cổng 53. `agent/dns_proxy.py:145`. |
| **SafeSearch Google/YouTube** (Slide 25) | Ghi đè tới IP nào? | Google ➜ `216.239.38.120`; YouTube ➜ `216.239.38.119`. Xem `agent/dns_proxy.py:32`. |
| **Băm SHA-256 nhị phân** (Slide 27) | Tránh được thủ thuật gì? | Trẻ đổi tên file `game.exe` thành `winword.exe` vẫn bị phát hiện và kill trong 3s. `agent/app_controller.py:53`. |
| **Tối ưu CPU 0.0%** (Slide 27) | Băm file nặng có lag máy không? | Dùng `mtime cache`: Chỉ băm lại khi ngày sửa file đổi, chu kỳ quét chỉ tốn micro-giây. `agent/app_controller.py:85`. |
| **Mật khẩu >= 10 ký tự** (Slide 31) | Theo chuẩn nào? Dùng mã băm gì? | NIST SP 800-63B kết hợp Argon2id ngốn RAM chống GPU. Xem `server/schemas.py:28`. |
| **Brute-Force Lockout** (Slide 31) | Khóa bao lâu? Sau mấy lần sai? | Khóa 15 phút sau 5 lần sai liên tiếp, trả HTTP 423. Xem `server/routes/auth.py:65`. |
| **IP Rate Limiting** (Slide 31) | Giới hạn bao nhiêu? | 10 requests/phút/IP lưu trong bộ nhớ RAM. Xem `server/security.py:45`. |
| **Anti-IDOR** (Slide 32) | Chống cha mẹ A điều khiển máy con B thế nào? | Kiểm tra `device.parent_id == current_parent.id`, từ chối HTTP 403. `server/routes/commands.py:48`. |
| **AES-256-GCM AEAD** (Slide 32) | Nonce bao nhiêu bytes? Tag bao nhiêu? | 12 bytes Nonce, 16 bytes Auth Tag. Chống sửa đổi dữ liệu. `server/crypto_utils.py:45`. |
| **Xóa dữ liệu 90 ngày** (Slide 33) | Căn cứ luật nào? Chu kỳ quét bao lâu? | Nghị định 13/2023/NĐ-CP Điều 20; quét ngầm mỗi 24h. Xem `server/services/retention_service.py:25`. |
| **Right to Erasure** (Slide 33) | Xóa những gì? Cần mật khẩu không? | Cần mật khẩu phụ huynh; xóa sạch Database Server và gửi WebSocket xóa SQLite Agent. `server/routes/retention.py`. |
| **DNSWatchdog** (Slide 34) | Quét bao lâu 1 lần? Làm gì khi trẻ đổi 8.8.8.8? | Quét mỗi 20s; gọi `netsh` ép về 127.0.0.1 và tạo cảnh báo viễn trắc. `agent/dns_watchdog.py`. |
| **Chặn VPN** (Slide 34) | Chặn được những VPN nào? | Cloudflare WARP, ProtonVPN, Psiphon, UltraSurf (đối soát kép SHA-256 + tên). `server/seed_domains.py`. |
| **Mức chiếm dụng RAM** (Slide 35) | Đo thực tế bao nhiêu? Chuẩn đồ án? | Thực tế **25.13 MB** (chuẩn đồ án $\le 26$ MB). Xem `docs/benchmark_results.json`. |
| **Độ trễ WebSocket** (Slide 35) | Lệnh khẩn cấp mất bao lâu? | **5.91 ms** trung bình (chuẩn đồ án $< 500$ ms, nhanh hơn 84 lần). `scripts/benchmark_performance.py`. |
| **Chịu lỗi mất mạng M5** (Slide 36) | Trẻ rút cáp mạng có chơi quá giờ được không? | Không! `time.monotonic()` tự đếm giờ và tự khóa offline, sự kiện lưu đệm SQLite. `tests/test_fault_tolerance.py`. |
| **Tổng số bài test** (Slide 39) | Bao nhiêu test? Kết quả? | **61/61 tests PASSED (100%)** trong 9.83 giây. Chạy lệnh `pytest tests/ -v`. |
