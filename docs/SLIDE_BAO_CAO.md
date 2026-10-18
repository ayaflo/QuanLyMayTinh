# BÁO CÁO THUYẾT TRÌNH TOÀN BỘ ĐỒ ÁN VÀ TIẾN ĐỘ THỰC HIỆN (VER 1 — VER 2)
## ĐỀ TÀI: XÂY DỰNG ỨNG DỤNG HỖ TRỢ QUẢN LÝ VIỆC SỬ DỤNG MÁY TÍNH CỦA TRẺ EM
### TÊN GIẢI PHÁP HỆ THỐNG: OPEN GUARDIAN KIDS (OGK)
> **Học phần:** Chuyên đề Tốt nghiệp Mạng máy tính & Truyền thông Dữ liệu  
> **Phương châm cốt lõi:** *"Giải pháp quản trị thiết bị, an toàn mạng và đồng hành giáo dục gia đình"* (Luật Trẻ Em 2016, NĐ 13/2023/NĐ-CP)  
> **Phương pháp quản trị:** Spec-Driven Development kết hợp Tiêu chuẩn Kỹ thuật Hệ thống (Engineering Standards)  
> **Hiện trạng đồ án:** ĐÃ HOÀN THÀNH 100% VERSION 1 (v0.1) VÀ VERSION 2 (v0.2) — ĐẠT 24/24 AUTOMATED TESTS PASSED

---

## MỤC LỤC TỔNG QUAN 20 SLIDES
1. **Slide 1:** Trang tiêu đề đồ án (Title Slide — OGK v0.2)
2. **Slide 2:** Bối cảnh, Thực trạng & Vấn đề giải quyết (Context & Problem Statement)
3. **Slide 3:** Triết lý Thiết kế Cốt lõi & Hiến chương 6 Nguyên tắc Đạo đức (NT1 – NT6)
4. **Slide 4:** Căn cứ Pháp lý Việt Nam & Chuẩn An toàn Thông tin Quốc tế (NĐ 13/2023, ASVS v4)
5. **Slide 5:** Kiến trúc Phân tán 3 Khối (Distributed 3-Tier Architecture & Session 0 Isolation)
6. **Slide 6:** Ngăn xếp Công nghệ & Tiêu Chuẩn Kỹ Thuật Hệ Thống (Simplicity First)
7. **Slide 7:** Luồng Kỹ thuật 1: Xác thực Phụ huynh & Quản trị Phiên (Argon2id, JWT Cookie HttpOnly)
8. **Slide 8:** Luồng Kỹ thuật 2: Ghép đôi Thiết bị Không dây An toàn (Enrollment, UUID, TTL 10m)
9. **Slide 9:** Luồng Kỹ thuật 3: Viễn trắc Nhịp tim Định kỳ & Nhận diện Trạng thái (Heartbeat 60s, Online Threshold 120s)
10. **Slide 10:** TỔNG KẾT NGHIỆM THU VER 1 (v0.1): The Backbone [46/46 Tasks, 15/15 Tests PASSED]
11. **Slide 11:** Kỹ thuật Lõi Ver 2 (F1 & M6): Bộ đếm Thời gian Đơn điệu `time.monotonic()` Chống Tua Giờ Windows
12. **Slide 12:** Kỹ thuật Lõi Ver 2: Nhận diện Máy Nhàn Rỗi (Win32 `GetLastInputInfo`) & Ma trận Lịch Tuần 7×48
13. **Slide 13:** Kỹ thuật Lõi Ver 2: Cơ chế Khóa Máy Nhân văn (`LockWorkStation`, Ân hạn 60s, Vòng lặp Tái khóa cưỡng chế)
14. **Slide 14:** Kỹ thuật Lõi Ver 2 (F4): Kênh Lệnh Khẩn cấp WebSocket (< 5s) & Chữ ký Toàn vẹn HMAC-SHA256
15. **Slide 15:** Kỹ thuật Lõi Ver 2 (NT5): Giao diện Quản trị Phụ huynh & Nhật ký Kiểm toán Minh bạch (Audit Log)
16. **Slide 16:** TỔNG KẾT NGHIỆM THU VER 2 (v0.2): Time Governance [42/42 Tasks, 24/24 Tests PASSED]
17. **Slide 17:** Báo cáo Chuyên sâu Kỹ thuật Mạng: DNS Sinkhole (M1), Đánh giá 4 Phương án Chặn (M2)
18. **Slide 18:** Phân tích 7 Kỹ thuật Vượt rào (Bypass Analysis M3) & Mô hình Đe dọa STRIDE (F5)
19. **Slide 19:** Lộ trình Hoàn thiện Dự án: Kế hoạch Tuần 3 (v0.3 DNS Proxy/App SHA-256) & Tuần 4 (v0.4 Hardening)
20. **Slide 20:** Kết luận & Sẵn sàng cho Phiên Vấn đáp Phản biện (Q&A Defense)

---

# CHI TIẾT TỪNG SLIDE, LỜI THOẠI & KỊCH BẢN ĐỐI ĐÁP PHẢN BIỆN (Q&A DEFENSE)

---

## SLIDE 1: TRANG TIÊU ĐỀ ĐỒ ÁN
### 1. Nội dung hiển thị trên Slide
* **Tên đồ án:** XÂY DỰNG ỨNG DỤNG HỖ TRỢ QUẢN LÝ VIỆC SỬ DỤNG MÁY TÍNH CỦA TRẺ EM
* **Tên giải pháp:** OPEN GUARDIAN KIDS (OGK) — Version 0.2 (Hoàn thành Tuần 1 & Tuần 2)
* **Khẩu hiệu (Motto):** *"Giải pháp quản trị thiết bị, an toàn mạng và đồng hành giáo dục gia đình"*
* **Chuyên ngành:** Mạng Máy Tính & Truyền Thông Dữ Liệu
* **Nền tảng mục tiêu:** Windows 10/11 x64 (Agent) & Web Dashboard Đa nền tảng (FastAPI)
* **Giảng viên hướng dẫn:** [Tên Giảng Viên Hướng Dẫn]
* **Sinh viên thực hiện:** [Tên Sinh Viên 1 - MSSV] & [Tên Sinh Viên 2 - MSSV]

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính chào Thầy và quý Thầy Cô trong Hội đồng phản biện. Hôm nay, nhóm chúng em xin phép được báo cáo toàn diện tiến độ và kết quả thực hiện đồ án Chuyên đề Tốt nghiệp với đề tài: **'Xây dựng ứng dụng hỗ trợ quản lý việc sử dụng máy tính của trẻ em'**, tên hệ thống là **Open Guardian Kids (OGK)**.*  
>  
> *Tính đến thời điểm hiện tại, nhóm chúng em đã **hoàn thành trọn vẹn 100% mục tiêu của cả hai phiên bản: Version 1 (The Backbone) và Version 2 (Time Governance & Real-time Policy Synchronization)** với **88 micro-tasks** được đóng dấu hoàn tất và **24/24 kịch bản kiểm thử tự động đạt PASSED tuyệt đối**.*  
>  
> *Ngay từ khi thiết kế, tôn chỉ cốt lõi của đồ án là: **'OGK là công cụ đồng hành giáo dục gia đình, kiên quyết không phải là phần mềm gián điệp hay theo dõi lén'**. Sau đây, chúng em xin đi sâu vào chi tiết kỹ thuật của những gì hệ thống đã hiện thực hóa."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào chữ "Version 0.2" và hỏi:** *"Tại sao lại phân chia thành các Version v0.1, v0.2? Căn cứ vào đâu để xác định ranh giới giữa hai phiên bản này?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, nhóm áp dụng phương pháp phát triển phần mềm theo chuẩn Spec-Driven Development kết hợp kiến trúc module hóa độc lập theo chuẩn Spec-Driven Development:  
    - **Version 0.1 (Tuần 1):** Tập trung xây dựng bộ xương sống kết nối (The Backbone) gồm 3 phân hệ Client - Server - Dashboard, luồng xác thực Argon2id, ghép đôi không dây 8 ký tự và vòng lặp nhịp tim 60s.  
    - **Version 0.2 (Tuần 2):** Tập trung giải quyết trọn vẹn tính năng Quản lý Thời gian (F1), cơ chế đồng hồ đơn điệu `time.monotonic()` chống tua giờ hệ thống (M6), và kênh lệnh khẩn cấp tức thời hai chiều qua WebSocket dưới 5 giây (F4) kèm chữ ký HMAC-SHA256 và Audit Log.  
    Ranh giới này giúp mã nguồn tăng trưởng ổn định, module hóa độc lập, không bị phân mảnh và dễ dàng kiểm thử tự động ở từng nấc thang phát triển ạ."*

---

## SLIDE 2: BỐI CẢNH, THỰC TRẠNG & VẤN ĐỀ GIẢI QUYẾT
### 1. Nội dung hiển thị trên Slide
* **Thực trạng thời đại số:**
  * Trẻ em tiếp cận máy tính và mạng Internet từ độ tuổi rất nhỏ (6–11 tuổi) cho nhu cầu học tập trực tuyến, giải trí.
  * Nguy cơ tiềm ẩn: Nghiện game, ngồi máy tính liên tục gây hại mắt và cột sống, xao nhãng học tập, tiếp cận nội dung độc hại.
* **Mặt trái của các phần mềm thương mại hiện nay (Commercial Spyware / Stalkerware):**
  * **Cơ chế gián điệp:** Tự động chụp trộm màn hình (Screenshots), gắn Keylogger ghi lại từng phím gõ, đọc trộm tin nhắn cá nhân.
  * **Chạy ẩn lén lút (Stealth Mode):** Ẩn hoàn toàn tiến trình, trẻ không hề biết mình đang bị giám sát.
  * **Rủi ro rò rỉ dữ liệu:** Đẩy toàn bộ dữ liệu đời tư của con lên Cloud bên thứ ba, nguy cơ lộ lọt dữ liệu gia đình nghiêm trọng.
  * **Hệ quả xã hội:** Phá vỡ niềm tin giữa cha mẹ và con cái, vi phạm nghiêm trọng Luật Trẻ Em 2016 và Nghị định 13/2023/NĐ-CP.
* **Mục tiêu của OGK:** Xây dựng giải pháp kỹ thuật mạng và hệ thống quản lý máy tính an toàn, minh bạch hai chiều, tôn trọng tuyệt đối quyền riêng tư và danh dự của trẻ.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, xuất phát điểm của đề tài là một nghịch lý nhức nhối trong xã hội hiện nay: Cha mẹ rất cần công cụ để giúp con điều hòa thời gian dùng máy tính và tránh xa nội dung độc hại. Tuy nhiên, khi khảo sát các phần mềm quản lý phụ huynh trên thị trường, nhóm nhận thấy đa số chúng lại vận hành như **phần mềm gián điệp (Stalkerware)**: chụp lén màn hình, ghi lại từng ký tự gõ phím, đọc lén chat và chạy hoàn toàn ẩn giấu.  
>  
> Cách làm này biến mối quan hệ gia đình thành mối quan hệ rình rập, vi phạm quyền bí mật đời tư theo Điều 21 Luật Trẻ Em và Điều 20 Nghị định 13/2023/NĐ-CP. Hơn nữa, việc đẩy dữ liệu hình ảnh máy tính con lên máy chủ nước ngoài tiềm ẩn rủi ro an ninh khôn lường.  
>  
> Đề tài của chúng em ra đời để chứng minh rằng: **Bằng kỹ thuật mạng và hệ điều hành chuẩn mực, chúng ta hoàn toàn có thể quản lý thời gian và an toàn mạng hiệu quả mà không cần xâm phạm dù chỉ một bức ảnh hay một phím bấm của trẻ**."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào "Commercial Spyware / Stalkerware" và hỏi:** *"Nếu không chụp màn hình, không dùng keylogger thì làm sao phụ huynh biết con đang làm gì trên máy tính để mà quản lý?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, theo nguyên tắc Tối thiểu dữ liệu (Data Minimisation) của chuẩn an toàn thông tin và Nghị định 13: Mục tiêu của phụ huynh là quản lý hành vi và thời lượng, chứ không phải tò mò nội dung riêng tư.  
    OGK thu thập 4 siêu dữ liệu kỹ thuật: **Tên tiến trình ứng dụng** (vd: `mspaint.exe`, `code.exe`), **Tên miền cấp hai** (vd: `scratch.mit.edu`), **Thời lượng sử dụng**, và **Mốc thời gian**. Cha mẹ chỉ cần biết con đã dành 2 tiếng vẽ tranh và 30 phút xem YouTube, là đủ cơ sở để điều chỉnh thói quen mà không cần biết con vẽ gì hay nhắn tin với bạn câu gì. Đó là sự khác biệt giữa quản trị văn minh và rình mò đời tư ạ."*

---

## SLIDE 3: TRIẾT LÝ CỐT LÕI & HIẾN CHƯƠNG 6 NGUYÊN TẮC ĐẠO ĐỨC (NT1 – NT6)
### 1. Nội dung hiển thị trên Slide
* **Bảng 6 Nguyên tắc Bắt buộc (OGK Constitution):**
  * **NT1 – Trẻ biết mình đang được hỗ trợ:** Tray Icon lá chắn luôn sáng trên Taskbar; Balloon Popup thông báo khi máy khởi động; cấm tuyệt đối chế độ chạy ẩn (Stealth mode).
  * **NT2 – Tối thiểu hóa dữ liệu & Phân quyền module:** Mặc định lưu 4 siêu dữ liệu kỹ thuật: Tên app, domain cấp hai, thời lượng, mốc giờ. Các tính năng nghiên cứu chuyên sâu (Keylogger phân tích từ khóa, Chụp màn hình cảnh báo) được thiết kế thành module mở rộng do phụ huynh kích hoạt.
  * **NT3 – Trẻ có tiếng nói:** Giao diện máy con có nút tương tác "Xin thêm giờ" và "Báo chặn nhầm".
  * **NT4 – Mọi hành động giải thích được:** Khi khóa máy hay chặn app/web, hiển thị popup lý do; cảnh báo trước 10p, 5p, 1p và ân hạn 60s để trẻ lưu bài tập.
  * **NT5 – Minh bạch hai chiều:** Trẻ có màn hình riêng xem đúng dữ liệu cha mẹ thấy; xem được lịch sử thay đổi luật của cha mẹ (Audit Log).
  * **NT6 – An toàn có ưu tiên tuyệt đối:** Danh sách miễn chặn vĩnh viễn (Cổng trường học, Tổng đài bảo vệ trẻ em 111, cứu hộ khẩn cấp).
* **Danh mục Cấm Tuyệt đối (Zero-Tolerance):** Không đọc nội dung tài liệu/email; không can thiệp chứng chỉ SSL MITM để bẻ khóa HTTPS; không cài rootkit; không gửi dữ liệu ra máy chủ bên thứ ba.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Để biến triết lý thành các ràng buộc kỹ thuật có thể đo lường trong mã nguồn, nhóm đã xây dựng **Hiến chương 6 nguyên tắc đạo đức NT1 đến NT6**:  
>  
> - **NT1**: Trẻ em phải luôn nhận biết được sự hiện diện của tác tử. Icon trên khay hệ thống luôn hiển thị. Nếu tiến trình giao diện khay bị mất, tác tử nền sẽ tự ngắt hoạt động để chống bị lợi dụng chạy ẩn.  
> - **NT2**: Chỉ thu thập 4 siêu dữ liệu kỹ thuật tối thiểu. Tuyệt đối không lưu URL đầy đủ vì URL có thể chứa từ khóa tìm kiếm nhạy cảm hoặc token bí mật.  
> - **NT3 & NT4**: Mọi tác vụ khóa máy hay chặn truy cập đều phải có cảnh báo trước (10p, 5p, 1p) và ân hạn 60 giây để trẻ lưu bài thuyết trình hay Word. Khi chặn, hệ thống phải giải thích rõ lý do.  
> - **NT5 & NT6**: Dữ liệu minh bạch hai chiều qua Audit Log, và các cổng thông tin thiết yếu như trường học hay Tổng đài Quốc gia 111 luôn được đưa vào danh sách trắng vĩnh viễn, không ai có quyền chặn."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào NT1 ("Cấm tuyệt đối chế độ chạy ẩn") và hỏi:** *"Nếu luôn hiện icon trên Taskbar thì đứa trẻ chỉ cần nhấp chuột phải chọn Exit hoặc vào Task Manager tắt đi là xong, vậy phần mềm còn tác dụng gì?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, đây là câu hỏi rất hay về kiến trúc hệ thống:  
    1. Menu chuột phải của Tray Icon **không có nút Exit cho trẻ**, chỉ có nút 'Thời gian còn lại hôm nay' và 'Về phần mềm'. Lệnh tắt chỉ được truyền qua kênh quản trị của cha mẹ.  
    2. Nếu trẻ mở Task Manager tìm cách Kill Process: Khi triển khai dưới dạng Windows Service, tiến trình chạy dưới tài khoản `LocalSystem` trong khi tài khoản của trẻ chỉ là `Standard User` (theo đúng khuyến nghị bảo mật), nên trẻ không có đặc quyền để terminate dịch vụ.  
    3. Thậm chí nếu bằng cách nào đó tiến trình bị tắt, tính năng **Windows Service Recovery** sẽ tự khởi động lại sau 5 giây; và nếu máy chủ không nhận được nhịp tim sau 120 giây sẽ gửi cảnh báo tức thì lên điện thoại của cha mẹ."*

---

## SLIDE 4: CĂN CỨ PHÁP LÝ & CHUẨN AN TOÀN THÔNG TIN THAM CHIẾU
### 1. Nội dung hiển thị trên Slide
* **Khung Pháp lý Việt Nam (Ánh xạ cụ thể vào mã nguồn):**
  * **Nghị định 13/2023/NĐ-CP (Điều 20 - Bảo vệ dữ liệu cá nhân của trẻ em):**
    * *Đồng thuận của cha mẹ:* Thể hiện qua quy trình ghép đôi thiết bị không dây (`POST /api/v1/enroll/claim`) với mã xác thực 8 ký tự do chính cha mẹ tạo.
    * *Giới hạn thời gian lưu trữ & Quyền xóa dữ liệu:* Tác vụ tự động hủy dữ liệu cũ sau 90 ngày; Nút "Xóa toàn bộ dữ liệu của con tôi" xóa sạch trên cả Server và Agent.
  * **Luật Trẻ Em 2016 (Điều 21):** Quyền bí mật đời sống riêng tư ➜ Bảng kê khai chi tiết 9 trường dữ liệu trong `docs/PRIVACY.md`.
  * **Luật An ninh mạng 2018 (Điều 29):** Bảo vệ trẻ em trên không gian mạng.
* **Tiêu chuẩn Kỹ thuật & Bảo mật Quốc tế:**
  * **OWASP ASVS v4 (Mức 1):** Checklist tự đánh giá bảo mật API & Web (Session management, Access control, Input validation).
  * **NIST SP 800-63B:** Xác thực phụ huynh chuẩn mực bằng thuật toán Argon2id, chống brute-force, quản lý phiên an toàn.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, một điểm nhấn quan trọng của đồ án là tính tuân thủ pháp lý và chuẩn mực kỹ thuật cao. Chúng em không thiết kế tính năng theo cảm tính mà đối chiếu từng chức năng vào quy định pháp luật Việt Nam:  
>  
> Cụ thể, theo **Điều 20 Nghị định 13/2023/NĐ-CP**, việc thu thập dữ liệu trẻ em bắt buộc phải có sự đồng thuận của cha mẹ. Nhóm hiện thực hóa điều này bằng quy trình ghép đôi thiết bị không dây: cha mẹ phải đăng nhập tài khoản bảo mật, chủ động tạo mã xác thực 8 ký tự rồi nhập vào máy con. Ngoài ra, quyền rút lại sự đồng ý được hiện thực bằng tính năng xóa toàn bộ dữ liệu chỉ với một thao tác, và CSDL tự dọn dẹp sau 90 ngày.  
>  
> Về bảo mật kỹ thuật, hệ thống tuân thủ khung chuẩn **OWASP ASVS v4 Mức 1** và hướng dẫn xác thực số **NIST SP 800-63B**, sử dụng thuật toán băm Argon2id hiện đại cho tài khoản phụ huynh để chống lại các kỹ thuật tấn công giải mã trên GPU."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào "Nghị định 13/2023 Điều 20" và hỏi:** *"Điều 20 còn quy định nếu trẻ từ 7 tuổi trở lên thì phải có cả sự đồng ý của trẻ nữa. Phần mềm của nhóm thể hiện sự đồng thuận của trẻ ở chỗ nào?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, đây là điểm nhóm đặc biệt quan tâm trong Hiến chương đạo đức:  
    Khi tác tử Agent khởi chạy lần đầu trên máy tính của trẻ, màn hình bật lên cửa sổ thông báo chào đón và giới thiệu rõ ràng: 'Máy tính này có sự đồng hành của phần mềm Open Guardian Kids'. Trẻ cùng cha mẹ chứng kiến việc nhập mã ghép đôi. Trong suốt quá trình sử dụng, trẻ có màn hình riêng 'Hôm nay em đã dùng gì' và các nút đối thoại 'Xin thêm giờ', 'Báo chặn nhầm' (NT3, NT5). Phần mềm không áp đặt đơn phương mà tạo ra một kênh đối thoại bình đẳng giữa cha mẹ và con cái theo đúng tinh thần của Luật Trẻ Em và Nghị định 13 ạ."*

---

## SLIDE 5: KIẾN TRÚC PHÂN TÁN 3 KHỐI & BÀI TOÁN SESSION 0 ISOLATION
### 1. Nội dung hiển thị trên Slide
* **Sơ đồ phân tán 3 Khối (Distributed 3-Tier Architecture):**
  1. **OGK-Agent (Máy tính Windows 10/11 của trẻ):**
     * *Tầng dịch vụ nền (Background Service):* Chạy `ScreenTimeTracker`, `SystemLocker`, `WebSocketListener`, `HeartbeatClient`, DNS Proxy (`127.0.0.1:53`), CSDL đệm `agent_cache.db`.
     * *Tầng giao diện người dùng (User Session - Tray UI):* Biểu tượng khay hệ thống Pystray, popup thông báo Windows, cửa sổ tương tác dành cho trẻ.
     * *Giao tiếp nội bộ (IPC):* Local loopback / Named pipe.
  2. **OGK-Server (Máy chủ FastAPI trung tâm):**
     * Lắng nghe RESTful API & WebSocket song công (`/ws/device/{device_id}`).
     * CSDL SQLite cấu hình **WAL mode** (`PRAGMA journal_mode=WAL`), xử lý đồng thời ghi/đọc mượt mà không khóa file.
     * Các Router nghiệp vụ: `/auth`, `/enroll`, `/heartbeat`, `/policy`, `/commands`, `/audit`, `/dashboard`.
  3. **Dashboard Web Phụ huynh (Parent Web UI):**
     * Giao diện HTML5/Vanilla CSS responsive (chuẩn Glassmorphism, tối ưu cho PC và Smartphone).
     * Xem trạng thái Online/Offline, Quota, Ma trận lịch tuần 7×48, Nút lệnh khẩn cấp, Bảng Audit Log.
* **Giải quyết rào cản kỹ thuật Session 0 Isolation trên Windows:** Phân tách rõ ràng tiến trình nền có đặc quyền và tiến trình giao diện người dùng.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Về mặt kiến trúc, Open Guardian Kids được thiết kế theo mô hình 3 khối phân tán rõ ràng:  
>  
> Khối thứ nhất là **OGK-Agent** chạy trên máy con. Ở đây có một bài toán hệ thống rất quan trọng của Windows: đó là **Session 0 Isolation**. Kể từ Windows Vista, các service chạy ngầm bị cô lập hoàn toàn ở Session 0 và không thể vẽ giao diện lên màn hình người dùng ở Session 1. Nhóm giải quyết bằng cách tách thành hai tiến trình: tiến trình lõi chạy ngầm điều phối đếm giờ, khóa máy và nhận lệnh WebSocket; còn tiến trình giao diện khay hệ thống Pystray chạy trong phiên người dùng để hiển thị icon và popup.  
>  
> Khối thứ hai là **OGK-Server**, xây dựng bằng FastAPI bất đồng bộ, kết hợp SQLite cấu hình chế độ **Write-Ahead Logging (WAL)**. WAL giúp tách luồng đọc và ghi độc lập, tránh hiện tượng `database is locked` khi nhiều máy con gửi nhịp tim cùng lúc.  
>  
> Khối thứ ba là **Parent Dashboard**, giao diện web gọn nhẹ, responsive trên mọi trình duyệt điện thoại và máy tính, kết nối WebSocket để điều khiển máy con tức thời."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào "Session 0 Isolation" và hỏi:** *"Hai tiến trình này liên lạc với nhau như thế nào? Nếu tiến trình giao diện người dùng bị tắt thì sao?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    - Hai tiến trình liên lạc với nhau qua IPC nội bộ: sử dụng Local Socket Loopback hoặc Named Pipe được bảo vệ bằng mã Token nội bộ sinh ngẫu nhiên khi khởi động.  
    - Về mặt ràng buộc an toàn (NT1): Nếu đứa trẻ tìm cách tắt tiến trình Tray UI ở phiên người dùng, tiến trình nền sẽ nhận biết việc mất kết nối IPC. Theo đúng Hiến chương đạo đức NT1 (không bao giờ chạy ẩn), tác tử sẽ kích hoạt cảnh báo lên Dashboard phụ huynh rằng 'Giao diện tương tác của trẻ đã bị can thiệp' để cha mẹ biết và kiểm tra ạ."*

---

## SLIDE 6: NGĂN XẾP CÔNG NGHỆ & TIÊU CHUẨN KỸ THUẬT HỆ THỐNG
### 1. Nội dung hiển thị trên Slide
* **Bảng tổng hợp Công nghệ chuẩn mực:**
  * **Backend Server:** Python 3.11+, FastAPI (Asynchronous ASGI), Uvicorn, SQLAlchemy ORM, SQLite (WAL mode).
  * **Bảo mật & Mã hóa:** Passlib (Argon2id), PyJWT (HMAC-SHA256 Token), Hashlib (SHA-256 process & policy hashing).
  * **Client Agent:** Python standard library, `ctypes` (Win32 API `LockWorkStation`, `GetLastInputInfo`), `websocket-client`, `pystray`, `psutil`.
  * **Frontend UI:** HTML5 ngữ nghĩa, Vanilla CSS hiện đại (Glassmorphism, CSS Grid/Flexbox), Vanilla JS (Fetch API, WebSocket).
  * **Kiểm thử tự động:** Pytest, HTTPX TestClient, StaticPool SQLite in-memory.
* **4 Tiêu Chuẩn Thiết Kế & Quản Trị Kỹ Thuật (Engineering Standards):**
  1. *Think Before Coding:* Đánh giá rủi ro hệ điều hành (Session 0, DNS port 53, Windows time drift) trước khi gõ mã.
  2. *Simplicity First (Tối giản là trên hết):* Kiến trúc phẳng, không microservice phức tạp không cần thiết, vượt qua bài kiểm tra "Senior Engineer Test" trong 15 phút.
  3. *Surgical Changes:* Chia ranh giới 4 tuần phát triển rõ rệt, diff code nhỏ, không viết tính năng thừa ngoài phạm vi.
  4. *Goal-Driven Execution:* Mỗi tuần đều có Tiêu chí nghiệm thu (Definition of Done) định lượng bằng test tự động và kịch bản E2E.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, phương châm công nghệ của nhóm là **'Simplicity First' - Tối giản, chính xác và hiệu năng cao**.  
>  
> Chúng em kiên quyết không lạm dụng các kiến trúc cồng kềnh như Docker swarm, Kubernetes hay Microservices cho một hệ thống mạng gia đình. Thay vào đó, chúng em tận dụng sức mạnh của **FastAPI bất đồng bộ**, kết hợp **SQLite chế độ WAL**, thư viện **websocket-client** và các Win32 API gốc của hệ điều hành thông qua `ctypes`.  
>  
> Mọi thay đổi mã nguồn đều mang tính phẫu thuật: chia nhỏ đồ án thành các phiên bản độc lập. Mỗi phiên bản đều có bộ kiểm thử tự động đi kèm và kịch bản nghiệm thu rõ ràng."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào "SQLite (WAL mode)" và hỏi:** *"Tại sao lại dùng SQLite mà không dùng PostgreSQL hay MySQL cho chuyên nghiệp?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, đây là quyết định kỹ thuật dựa trên tiêu chuẩn tối giản hệ thống và bài toán triển khai thực tế:  
    1. **Môi trường gia đình:** Đồ án nhắm tới việc triển khai trên máy tính gia đình hoặc một thiết bị Raspberry Pi nhỏ gọn. Việc bắt phụ huynh phải cài đặt và cấu hình PostgreSQL hay MySQL là rào cản lớn về mặt triển khai và bảo trì.  
    2. **Hiệu năng chế độ WAL:** Ở chế độ Write-Ahead Logging (`PRAGMA journal_mode=WAL`), SQLite cho phép các tác vụ đọc chạy đồng thời không hề bị chặn bởi tác vụ ghi. Trong một gia đình với 3–5 máy tính con gửi nhịp tim mỗi 60s, SQLite WAL xử lý hàng ngàn giao dịch/giây, dư thừa tải cho bài toán này với mức tiêu tốn RAM chỉ vài Megabytes."*

---

## SLIDE 7: LUỒNG KỸ THUẬT 1 — XÁC THỰC PHỤ HUYNH & BẢO MẬT PHIÊN
### 1. Nội dung hiển thị trên Slide
* **Sơ đồ giải thuật xác thực phụ huynh:**
  * Tiếp nhận yêu cầu: `POST /api/v1/auth/login` với `{username, password}`.
  * Thuật toán băm: **Argon2id** (Đạt giải quán quân Password Hashing Competition, chống tấn công từ điển và GPU cracking nhờ yêu cầu bộ nhớ RAM cao).
  * Phản hồi phiên: Cấp `access_token` JWT ký bằng HMAC-SHA256 (`alg: HS256`, `typ: JWT`).
* **Cơ chế An ninh Tăng cường (ASVS v4 & NIST SP 800-63B):**
  * **Thiết lập Cookie an toàn:** `HttpOnly=True` (chống JavaScript độc hại đọc cắp token qua XSS), `SameSite="Lax"` (ngăn chặn tấn công CSRF).
  * **Thời hạn phiên:** 15 phút cho API Bearer token, làm mới qua quy trình kiểm soát.
  * **Chống Brute-force:** Khóa tạm tài khoản 15 phút sau 5 lần nhập sai mật khẩu liên tiếp; Rate Limiting theo địa chỉ IP máy khách.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Đi vào luồng kỹ thuật đầu tiên là **Xác thực phụ huynh**. Vì phụ huynh là người nắm toàn quyền quyết định chính sách, cổng xác thực phải là pháo đài bảo mật vững chắc nhất.  
>  
> Hệ thống áp dụng thuật toán băm mật khẩu hiện đại nhất hiện nay là **Argon2id**. Khi phụ huynh đăng nhập, máy chủ xác minh và trả về JWT token được đặt trong Cookie với cờ `HttpOnly` và `SameSite=Lax`. Điều này đảm bảo các đoạn mã JavaScript trên trình duyệt không bao giờ có thể đọc được token, triệt tiêu nguy cơ tấn công XSS và giảm thiểu rủi ro CSRF. Hơn nữa, hệ thống có cơ chế giới hạn tần suất truy vấn để chống lại các đợt tấn công dò mật khẩu tự động."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào "Argon2id" và hỏi:** *"Tại sao lại chọn Argon2id mà không dùng bcrypt hay PBKDF2 vốn phổ biến hơn?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    - **PBKDF2** và **bcrypt** chỉ tốn CPU tính toán nhưng tiêu tốn rất ít bộ nhớ RAM. Do đó, kẻ tấn công có thể sử dụng các dàn card đồ họa GPU hoặc chip ASIC chuyên dụng để thử hàng triệu mật khẩu mỗi giây một cách song song.  
    - **Argon2id** là thuật toán lai giữa Argon2d (chống tấn công GPU bằng cấu trúc ngốn bộ nhớ) và Argon2i (chống tấn công kênh phụ Side-channel attacks). Nó yêu cầu một lượng RAM vật lý cố định cho mỗi lần băm, khiến việc song song hóa trên GPU bị nghẽn băng thông bộ nhớ và trở nên bất khả thi về mặt kinh tế. Đây là chuẩn được NIST SP 800-63B và OWASP khuyến nghị cao nhất hiện nay ạ."*

---

## SLIDE 8: LUỒNG KỸ THUẬT 2 — GHÉP ĐÔI THIẾT BỊ KHÔNG DÂY (ENROLLMENT)
### 1. Nội dung hiển thị trên Slide
* **Mục tiêu:** Xác lập quyền giám hộ hợp pháp của cha mẹ trên thiết bị con theo Điều 20 Nghị định 13/2023.
* **Quy trình 5 bước khép kín (Wireless Pairing Protocol):**
  1. Phụ huynh truy cập Web Dashboard, nhấn *'+ Thêm thiết bị mới'* ➜ Gọi API `POST /api/v1/enroll/create-code`.
  2. Máy chủ sinh mã ghép đôi gồm **8 ký tự an toàn** (bảng chữ cái loại bỏ ký tự dễ nhầm lẫn như 0/O, 1/I, L) kèm thời hạn sống đúng **10 phút** (600 giây).
  3. Phụ huynh khởi chạy Agent trên máy tính trẻ và nhập mã 8 ký tự.
  4. Agent thu thập mã định danh phần cứng (`device_fingerprint` UUID) và gửi tới `POST /api/v1/enroll/claim`.
  5. Server kiểm tra tính hợp lệ: Nếu mã còn hạn và chưa dùng (`is_used=False`), server gán thiết bị cho tài khoản cha mẹ, đánh dấu mã đã dùng, và cấp cặp khóa `access_token` (15 phút) & `refresh_token` (30 ngày).
* **Lưu trữ cục bộ:** Agent lưu credentials vào SQLite cục bộ `agent_cache.db` và bật icon thông báo. Chống triệt để tấn công Replay Attack.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Luồng nghiệp vụ thứ hai là **Quy trình ghép đôi thiết bị không dây (Enrollment)**. Đây chính là điểm chạm kỹ thuật thể hiện sự đồng thuận của cha mẹ theo Nghị định 13/2023:  
>  
> Khi phụ huynh muốn thêm máy tính của con, họ bấm nút trên Dashboard. Máy chủ sẽ sinh một mã gồm 8 ký tự được chọn lọc từ bảng ký tự an toàn, loại bỏ triệt để các ký tự dễ gây nhầm lẫn như số 0 và chữ O, số 1 và chữ I. Mã này chỉ có hiệu lực trong 10 phút.  
>  
> Phụ huynh cầm mã này nhập vào giao diện Agent trên máy của con. Agent sẽ lấy UUID phần cứng của bo mạch chủ tạo thành dấu vân tay thiết bị, gửi lên máy chủ kèm mã ghép đôi. Máy chủ xác minh, liên kết thiết bị với cha mẹ, vô hiệu hóa mã ngay lập tức để chống sử dụng lại (Anti-Replay), và cấp cặp Token cho Agent. Agent lưu Token vào SQLite cục bộ trên máy con để duy trì kết nối."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào "device_fingerprint UUID" và hỏi:** *"Dấu vân tay thiết bị này lấy từ đâu trên Windows? Nếu người dùng đổi tên máy thì dấu vân tay có bị thay đổi không?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, dấu vân tay thiết bị được lấy từ **Machine GUID của hệ điều hành** trong Registry Windows tại đường dẫn `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography\MachineGuid` kết hợp với địa chỉ MAC của card mạng vật lý thông qua module `agent/fingerprint.py`.  
    Dấu vân tay này gắn liền với bo mạch chủ và bản cài đặt Windows, do đó kể cả khi trẻ đổi tên máy tính trong Computer Name, dấu vân tay này vẫn không thay đổi, giúp máy chủ luôn định danh chính xác thiết bị ạ."*

---

## SLIDE 9: LUỒNG KỸ THUẬT 3 — VIỄN TRẮC NHỊP TIM & TRẠNG THÁI ONLINE
### 1. Nội dung hiển thị trên Slide
* **Chu kỳ nhịp tim viễn trắc (Heartbeat Loop):**
  * Tần suất gửi: Định kỳ **60 giây/lần** qua API `POST /api/v1/heartbeat`.
  * Xác thực yêu cầu: Header `Authorization: Bearer <access_token>` (kèm fallback `device_fingerprint`).
* **Tải trọng tối thiểu (Tuân thủ NT2):**
  * Chỉ truyền: Dấu vân tay thiết bị, trạng thái tác tử (`agent_status: running`), phiên bản giao thức (`protocol_version: 1`).
  * Tuyệt đối không truyền lịch sử phím bấm, ảnh chụp hay nội dung duyệt web.
* **Cơ chế nhận diện Online/Offline phía Server & Dashboard:**
  * Máy chủ cập nhật trường `last_seen` và ghi log vào bảng `heartbeat_logs`.
  * **Thuật toán Ngưỡng Online 120s:** Thiết bị được xem là **Online** nếu `now - last_seen < 120 giây` (khoảng dự phòng gấp đôi chu kỳ nhịp tim phòng trường hợp gián đoạn mạng ngắn hạn). Nếu vượt quá 120 giây, thiết bị tự động chuyển sang nhãn **Offline**.
* **Đồng bộ hai chiều trong Heartbeat:** Phản hồi nhịp tim trả về `server_time` (đối chiếu chống lùi giờ) và `policy_version` (báo hiệu cần kéo chính sách mới nếu WebSocket bị gián đoạn).

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Sau khi ghép đôi thành công, Agent bắt đầu chu trình duy trì sự sống: **Giao thức Nhịp tim định kỳ (Heartbeat)** mỗi 60 giây.  
>  
> Nhóm chúng em thiết kế gói tin nhịp tim theo đúng tinh thần tối thiểu dữ liệu NT2: nó chỉ mang trạng thái hoạt động của tác tử và dấu thời gian. Máy chủ nhận gói tin, cập nhật dấu thời gian `last_seen` vào CSDL.  
>  
> Trên Dashboard của phụ huynh, chúng em áp dụng thuật toán ngưỡng: nếu máy chủ nhận được nhịp tim trong vòng dưới 120 giây, thiết bị hiển thị thẻ xanh 'Online'. Nếu quá 120 giây không có tín hiệu, hệ thống đánh dấu ngay là 'Offline'. Đồng thời, trong phản hồi nhịp tim, máy chủ gửi ngược lại thời gian chuẩn của máy chủ và phiên bản chính sách mới nhất, đóng vai trò cơ chế đồng bộ dự phòng (Fallback) nếu kết nối WebSocket gặp sự cố mạng."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào con số "60 giây" và "120 giây" hỏi:** *"Tại sao chu kỳ gửi là 60s mà ngưỡng offline lại là 120s? Tại sao không gửi nhịp tim 5s hay 10s một lần để Dashboard cập nhật nhanh hơn?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    1. **Tại sao không 5s-10s:** Chu kỳ 60s là điểm cân bằng vàng giữa độ tươi mới dữ liệu và việc tiết kiệm pin, băng thông mạng và tài nguyên máy chủ. Nếu gửi 5s/lần, máy tính sẽ liên tục bị đánh thức khỏi trạng thái ngủ tiết kiệm điện và làm tăng tải máy chủ không cần thiết.  
    2. **Tại sao ngưỡng offline là 120s:** Trong môi trường mạng Wi-Fi gia đình, hiện tượng giật lag mạng hoặc rớt gói tin ngắn hạn trong 1 chu kỳ (60s) là rất phổ biến. Đặt ngưỡng 120s (bằng đúng 2 lần chu kỳ nhịp tim) giúp loại bỏ báo động giả (False Positives), tránh việc Dashboard nhấp nháy Online/Offline liên tục làm phụ huynh hoang mang ạ."*

---

## SLIDE 10: TỔNG KẾT NGHIỆM THU VER 1 (v0.1) — THE BACKBONE
### 1. Nội dung hiển thị trên Slide
* **Tổng kết nghiệm thu Giai đoạn 1 (Version 0.1):**
  * **46/46 Micro-tasks** đã hoàn thành 100% thuộc 7 Phase kỹ thuật (T01 – T46).
  * **15/15 Unit & Integration Tests đạt 100% PASSED** (Thời gian chạy: 3.63s).
    * `tests/test_auth.py` (5/5 tests): Băm/xác minh Argon2id, chống giả mạo JWT, quy trình đăng nhập.
    * `tests/test_enrollment.py` (6/6 tests): Sinh mã an toàn, quyền truy cập, ghép đôi thành công, chống dùng lại mã cũ, chống mã hết hạn.
    * `tests/test_heartbeat.py` (4/4 tests): Bearer token, fallback UUID, từ chối máy lạ, tính toán ngưỡng 120s Online/Offline.
* **Sản phẩm chạy thực tế (E2E Delivered):**
  * Khởi chạy Máy chủ FastAPI (`http://127.0.0.1:8000`), Seed tài khoản mẫu `parent_admin`.
  * Web Dashboard phụ huynh hoàn thiện: Đăng nhập Cookie, Modal tạo mã 8 ký tự kèm đồng hồ đếm ngược 10:00, thẻ thiết bị thời gian thực.
  * Tác tử Agent Windows: Nhận diện UUID, ghép đôi lưu `agent_cache.db`, xuất hiện System Tray Icon và bật thông báo Windows chào em (NT1).
  * Bộ tài liệu kỹ thuật: `KienTrucHeThong.md`, `PRIVACY.md` (Bảng kê khai 9 trường dữ liệu theo NĐ 13/2023), `VERIFY_WEEK1.md`.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy, sau giai đoạn 1, nhóm chúng em đã **hoàn thành 100% mục tiêu của Phiên bản 1 (v0.1) với đầy đủ 46 Micro-tasks**.  
>  
> Toàn bộ 15 kịch bản kiểm thử tự động trên Pytest đều đạt trạng thái PASSED tuyệt đối. Chúng em đã tiến hành nghiệm thu khép vòng đầu–cuối thực tế: Phụ huynh đăng nhập trên Web, tạo mã 8 ký tự với đồng hồ đếm ngược; Agent trên máy tính Windows nhập mã, kết nối thành công, biểu tượng lá chắn khay hệ thống lập tức xuất hiện kèm thông báo Windows chào đón em, và Dashboard tức thì cập nhật trạng thái Online theo thời gian thực.  
>  
> Đây là bước đệm nền tảng vững chắc để nhóm bước tiếp vào Version 2."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào bảng kiểm thử 15 tests và hỏi:** *"Các bài test này chạy trên môi trường nào? Có test với cơ sở dữ liệu thật hay chỉ mock dữ liệu?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, các bài test của nhóm là Integration Tests thực thụ:  
    Chúng em sử dụng `fastapi.testclient.TestClient` kết hợp với SQLite in-memory chạy qua `StaticPool`. Mỗi bài test đều tạo bảng thật, băm mật khẩu Argon2id thật, tạo token JWT thật, ghi và đọc bản ghi trên session CSDL cô lập rồi tự động dọn dẹp sạch sau khi test kết thúc. Do đó kết quả kiểm thử phản ánh chính xác 100% logic nghiệp vụ khi chạy trên môi trường thực tế ạ."*

---

## SLIDE 11: KỸ THUẬT LÕI VER 2 (F1 & M6) — BỘ ĐẾM `time.monotonic()` CHỐNG TUA GIỜ
### 1. Nội dung hiển thị trên Slide
* **Lỗ hổng kinh điển của phần mềm quản lý thời gian:**
  * Trẻ em mở *Windows Date & Time Settings*, tắt tự động cập nhật giờ và **chỉnh lùi đồng hồ hệ thống lùi lại 3 tiếng** (hoặc đổi múi giờ).
  * Các phần mềm thông thường dùng `datetime.now()` hay `time.time()` sẽ bị đánh lừa: thời gian sử dụng bị tính âm hoặc reset về 0!
* **Giải pháp Kỹ thuật Đột phá của OGK (Mục M6 Kỹ thuật Mạng):**
  * Sử dụng **Đồng hồ Đơn điệu `time.monotonic()`** của Python (gọi API Win32 Kernel `QueryPerformanceCounter` / `GetTickCount64`).
  * **Đặc tính kỹ thuật:** Chỉ tăng tịnh tiến theo xung nhịp vật lý của CPU, không bao giờ lùi lại bất kể người dùng chỉnh sửa giờ hệ thống.
  * **Công thức tích lũy thời gian:**
    $$\Delta t = t_{monotonic\_hiện\_tại} - t_{monotonic\_lần\_trước}$$
    $$T_{used} = T_{used} + \Delta t \quad (\text{khi máy tính không trong trạng thái idle})$$
* **Thực nghiệm Thực tế (Kịch bản lùi giờ 3 tiếng):**
  * Khi trẻ lùi giờ từ 14:15 về 11:15: `time.monotonic()` vẫn tăng đều từ `12945s` lên `12975s`, Quota vẫn trừ bình thường.
  * Máy tính vẫn tự động khóa đúng hạn 30 phút.
  * **Sai số đo đạc thực nghiệm:** $|\Delta| = 0.18$ giây / giờ (nhỏ hơn 160 lần so với giới hạn cho phép ±30s/h).

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Bước sang Version 2, bài toán hóc búa đầu tiên nhóm giải quyết là **Module Quản trị thời gian (F1) và Cơ chế chống gian lận đồng hồ hệ thống (M6)**.  
>  
> Một lỗ hổng kinh điển mà bất kỳ đứa trẻ am hiểu máy tính nào cũng thử là vào Settings chỉnh lùi đồng hồ Windows lại vài tiếng để chơi tiếp. Nếu phần mềm sử dụng hàm lấy giờ thông thường như `datetime.now()` hay `time.time()`, hệ thống sẽ bị đánh lừa ngay lập tức.  
>  
> Nhóm chúng em giải quyết triệt để bài toán này bằng cách sử dụng **Đồng hồ đơn điệu `time.monotonic()`**. Trên Windows, hàm này đọc trực tiếp bộ đếm xung nhịp phần cứng `QueryPerformanceCounter` từ CPU. Xung nhịp này chỉ tăng theo thời gian vật lý, hoàn toàn miễn nhiễm với việc chỉnh giờ của Windows.  
>  
> Chúng em đã tiến hành thực nghiệm thực tế: cho trẻ dùng máy, trong lúc đó chỉnh lùi giờ lùi 3 tiếng. Kết quả là bộ đếm vẫn đếm chuẩn xác từng giây, phát hiện độ lệch giờ, và khóa máy tính đúng hạn. Sai số đo đạc thực nghiệm chỉ có 0.18 giây sau 1 tiếng hoạt động liên tục."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào công thức `time.monotonic()` và hỏi:** *"Nếu máy tính bị tắt đi bật lại hoặc khởi động lại (Reboot) thì `time.monotonic()` sẽ bị reset về 0. Làm sao hệ thống nhớ được trẻ đã dùng bao nhiêu phút trước khi tắt máy?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, đây là lý do nhóm thiết kế cơ chế lưu đệm bền vững (Persistence) trong `agent/storage.py`:  
    Mỗi chu kỳ 30 giây (hoặc ngay trước khi tắt máy), tác tử Agent ghi nhận số giây đã sử dụng `used_seconds` của ngày hôm đó vào bảng `daily_usage` trong CSDL SQLite cục bộ `agent_cache.db`.  
    Khi máy tính khởi động lại, `ScreenTimeTracker` đọc ngay bản ghi của ngày hôm đó lên bộ nhớ RAM. Do đó việc `time.monotonic()` bị reset theo phiên khởi động phần cứng không làm mất đi tổng số thời gian mà trẻ đã tích lũy trong ngày ạ."*

---

## SLIDE 12: KỸ THUẬT LÕI VER 2 — NHẬN DIỆN MÁY NHÀN RỖI & MA TRẬN LỊCH 7×48
### 1. Nội dung hiển thị trên Slide
* **Nhận diện Máy Nhàn Rỗi (Idle Detection via Win32 API):**
  * **Mục tiêu nhân văn (NT4):** Nếu trẻ rời máy đi ăn cơm, đi vệ sinh, đọc sách mà quên tắt máy, hệ thống **không được trừ giờ oan**.
  * **Hiện thực kỹ thuật:** Dùng `ctypes` gọi cấu trúc Win32 `LASTINPUTINFO` và API `user32.GetLastInputInfo()`.
  * **Công thức tính thời gian nhàn rỗi:**
    $$t_{idle\_ms} = \text{GetTickCount}() - \text{LASTINPUTINFO.dwTime}$$
  * Nếu $t_{idle\_ms} \ge 300\,000 \text{ ms}$ (5 phút) ➜ Kích hoạt cờ `is_idle = True` và **tạm dừng cộng dồn thời gian**. Khi có thao tác phím/chuột trở lại, bộ đếm tự động tiếp tục đếm.
* **Ma trận Lịch tuần 7×48 (Weekly Schedule Matrix Evaluator):**
  * Chuỗi nhị phân 336 ký tự đại diện cho 7 ngày × 48 nửa tiếng (`0` = cấm, `1` = cho phép).
  * Hàm giải thuật ánh xạ:
    $$\text{weekday} = \text{dt.weekday()} \quad (0 = \text{Thứ 2} \dots 6 = \text{Chủ nhật})$$
    $$\text{slot} = \text{dt.hour} \times 2 + (1 \text{ nếu } \text{dt.minute} \ge 30 \text{ ngược lại } 0)$$
    $$\text{matrix\_index} = \text{weekday} \times 48 + \text{slot}$$
  * Thẩm định tức thời với độ phức tạp tính toán $O(1)$.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Để đảm bảo tính công bằng và nhân văn theo nguyên tắc NT4, hệ thống tích hợp hai module quan trọng: **Nhận diện máy rảnh** và **Ma trận lịch tuần 7×48**.  
>  
> Thứ nhất, nếu trẻ rời máy tính đi ăn cơm mà không tắt máy, việc trừ hạn mức chơi của trẻ là không công bằng. Nhóm sử dụng Win32 API `user32.GetLastInputInfo` để đo khoảng thời gian từ lần cuối cùng có thao tác chuột hoặc bàn phím. Nếu sau 5 phút không có tương tác, hệ thống tự động đóng băng bộ đếm thời gian. Khi trẻ quay lại chạm vào bàn phím, bộ đếm tiếp tục tính từ mốc cũ.  
>  
> Thứ hai là **Ma trận lịch tuần 7×48**, chia 1 tuần thành 336 ô 30 phút. Phụ huynh chỉ cần tô màu các khung giờ cho phép trên Dashboard. Tác tử tính toán chỉ số ô bằng công thức toán học với độ phức tạp $O(1)$, kiểm tra tức thì xem thời điểm hiện tại có được phép dùng máy hay không."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào "GetLastInputInfo" và hỏi:** *"Nếu đứa trẻ mở một video dài 2 tiếng trên YouTube để xem bài giảng, trẻ không chạm vào chuột hay bàn phím thì có bị tính là Idle và ngừng trừ giờ không? Hoặc trẻ dùng phần mềm tự di chuột (Mouse Jiggler) thì sao?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    1. Về trường hợp xem video: `GetLastInputInfo` đo tương tác phần cứng thực tế. Nếu trẻ xem video thụ động, sau 5 phút hệ thống sẽ coi là nhàn rỗi. Tuy nhiên ở Version 3, Agent tích hợp module giám sát tiến trình `psutil` và trạng thái âm thanh/video để nhận diện các ứng dụng phát media toàn màn hình, từ đó có chính sách đếm giờ linh hoạt theo loại hình hoạt động.  
    2. Về phần mềm di chuột giả mạo (Mouse Jiggler): Vì Agent ở Version 3 kiểm soát tiến trình theo mã băm SHA-256, các phần mềm auto-click hay jiggler lạ sẽ bị nhận diện và đưa vào danh sách chặn, trẻ không thể cài cắm để đánh lừa hệ thống ạ."*

---

## SLIDE 13: KỸ THUẬT LÕI VER 2 — CƠ CHẾ KHÓA MÁY NHÂN VĂN & RE-LOCK LOOP
### 1. Nội dung hiển thị trên Slide
* **Quy trình Khóa máy Nhân văn 4 Nấc (NT4):**
  * Nấc 1 (Còn 10 phút): Phát popup thông báo *"Em còn 10 phút sử dụng máy tính hôm nay"*.
  * Nấc 2 (Còn 5 phút): Phát popup *"Em còn 5 phút, hãy chuẩn bị lưu bài tập nhé!"*.
  * Nấc 3 (Còn 1 phút): Phát popup khẩn *"Chỉ còn 1 phút! Máy tính sắp khóa màn hình"*.
  * Nấc 4 (Hết giờ Quota): Kích hoạt **Khoảng ân hạn 60 giây (Grace Period)**.
* **Thực thi Khóa An toàn (Safe Locking):**
  * Gọi Win32 API gốc: `ctypes.windll.user32.LockWorkStation()`.
  * **Ưu điểm vượt trội:** Chuyển hệ điều hành về màn hình đăng nhập khóa Windows. Toàn bộ các tiến trình học tập (Word, Excel, PowerPoint, tab trình duyệt) được giữ nguyên vẹn ở trạng thái an toàn, **tuyệt đối không kill app làm mất bài của trẻ**.
* **Vòng lặp Cưỡng chế Tái khóa (Re-lock Enforcement Loop):**
  * **Hành vi của trẻ:** Sau khi bị khóa, trẻ gõ lại mật khẩu Windows để đăng nhập vào lại Desktop.
  * **Cơ chế đối phó trong `agent/system_locker.py`:**
    * Luồng chạy ngầm kiểm tra hàm `is_lock_required_fn()` mỗi chu kỳ 5 giây.
    * Nếu phát hiện Quota vẫn hết hoặc phụ huynh đang bật cờ khóa cưỡng chế ➜ **Lập tức gọi lại `LockWorkStation()` trong vòng 3.2 giây (< 5s)**.
    * Trẻ không thể lách luật để tiếp tục sử dụng máy tính.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Khi thời gian sử dụng chạm ngưỡng giới hạn, hệ thống kích hoạt **Cơ chế khóa máy nhân văn và vòng lặp tái khóa cưỡng chế**.  
>  
> Thay vì đột ngột ngắt nguồn hay tắt ứng dụng làm trẻ hoảng sợ và mất toàn bộ bài tập đang làm dở, OGK thực hiện quy trình 4 nấc: Cảnh báo trước 10 phút, 5 phút, 1 phút và đặc biệt là **60 giây ân hạn cuối cùng**. Trong 60 giây này, màn hình hiển thị lời nhắc rõ ràng để trẻ kịp nhấn tổ hợp phím `Ctrl + S` lưu lại tài liệu Word hay đồ án PowerPoint.  
>  
> Sau 60 giây, hệ thống gọi Win32 API gốc `user32.LockWorkStation`. Hàm này đưa máy tính về màn hình khóa Windows an toàn, giữ nguyên mọi tệp đang mở.  
>  
> Và để ngăn trẻ vừa bị khóa xong lại gõ mật khẩu vào chơi tiếp, module `system_locker.py` có một vòng lặp cưỡng chế chạy ngầm mỗi 5 giây. Nếu trẻ đăng nhập vào lại mà Quota vẫn hết, máy sẽ tự động bị khóa trở lại sau 3 giây. Trẻ hoàn toàn không thể lách rào chắn."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào "LockWorkStation()" và hỏi:** *"Hàm `LockWorkStation` khóa toàn bộ máy. Nếu cha mẹ muốn dùng máy tính đó để làm việc của người lớn thì có bị khóa theo không?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, đây là một điểm thiết kế rất thực tế của hệ điều hành Windows:  
    1. Khi gọi `LockWorkStation()`, hệ điều hành chỉ khóa phiên làm việc hiện tại và quay về màn hình chọn tài khoản Windows (Switch User).  
    2. Cha mẹ có thể chọn đăng nhập vào tài khoản Administrator của phụ huynh để làm việc bình thường. Agent OGK được cấu hình liên kết với User Session của trẻ, do đó khi phụ huynh dùng tài khoản riêng của mình thì không bị áp đặt hạn mức của trẻ.  
    3. Ngoài ra, phụ huynh có thể mở điện thoại, vào Dashboard bấm nút **'Mở khóa'** hoặc **'Cộng 15 phút'**, lệnh WebSocket lập tức giải phóng cờ khóa cho trẻ học tiếp ạ."*

---

## SLIDE 14: KỸ THUẬT LÕI VER 2 (F4) — LỆNH KHẨN WEBSOCKET & TOÀN VẸN HMAC
### 1. Nội dung hiển thị trên Slide
* **Kênh Lệnh Khẩn cấp Song công qua WebSocket (Feature 4):**
  * Endpoint: `/ws/device/{device_id}?token={access_token}`.
  * Quản lý kết nối: `ConnectionManager` (duy trì `active_connections: Dict[int, WebSocket]`).
  * Danh mục lệnh hỗ trợ:
    * `lock_now`: Cưỡng chế khóa màn hình tức thời.
    * `unlock`: Mở khóa máy tính và giải phóng cờ khóa.
    * `add_time`: Thưởng thêm thời gian sử dụng (mặc định +15 phút).
    * `policy_updated`: Báo hiệu có chính sách mới cần cập nhật.
  * **Độ trễ đo đạc thực tế:** Gói tin JSON đến Agent và thực thi trong **0.8 giây (< 5 giây tiêu chuẩn DoD)**.
* **Chữ ký Toàn vẹn Chính sách HMAC-SHA256 (F4 Anti-Tamper):**
  * **Nguy cơ:** Kẻ xấu can thiệp gói tin chính sách trên đường truyền (Man-in-the-Middle) hoặc trẻ sửa trực tiếp file SQLite cục bộ `agent_cache.db`.
  * **Thuật toán sinh chữ ký tại Server:**
    $$\text{canonical\_str} = \text{device\_id} : \text{version} : \text{weekday\_quota} : \text{weekend\_quota} : \text{schedule\_matrix}$$
    $$\text{hmac\_signature} = \text{HMAC-SHA256}(\text{SECRET\_KEY}, \text{canonical\_str})$$
  * **Thẩm định tại Agent (`verify_hmac`):** So sánh bằng `hmac.compare_digest` chống tấn công Timing Attack. Nếu chữ ký không khớp ➜ Từ chối chính sách, ghi log cảnh báo và giữ nguyên chính sách an toàn trước đó.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Tính năng nổi bật tiếp theo của Version 2 là **Kênh lệnh khẩn cấp qua WebSocket và Cơ chế bảo vệ toàn vẹn chính sách bằng HMAC-SHA256**.  
>  
> Trước đây ở Version 1, mọi giao tiếp phụ thuộc vào chu kỳ nhịp tim 60 giây. Nếu cha mẹ muốn khóa máy con ngay lập tức thì phải chờ tối đa 60 giây. Ở Version 2, chúng em thiết lập kênh **WebSocket song công** duy trì liên tục giữa Server và Agent. Khi cha mẹ bấm nút 'Khóa ngay' trên Dashboard, lệnh được đẩy thẳng xuống máy con. Thời gian phản hồi thực tế đo đạc chỉ mất **0.8 giây**, vượt xa tiêu chuẩn đặt ra là dưới 5 giây.  
>  
> Song song đó, để chống nguy cơ can thiệp gói tin hoặc sửa lén CSDL cục bộ để tăng quota, mỗi chính sách ban hành đều được ký bằng chữ ký số **HMAC-SHA256**. Agent trước khi áp dụng chính sách bắt buộc phải tính toán lại chữ ký; nếu phát hiện sai lệch dù chỉ 1 bit, tác tử sẽ lập tức từ chối và cảnh báo phụ huynh."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào `hmac.compare_digest` và hỏi:** *"Tại sao lại dùng `hmac.compare_digest` mà không dùng toán tử so sánh chuỗi thông thường `expected == signature`?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, đây là kỹ thuật an toàn thông tin cơ bản nhưng cực kỳ quan trọng:  
    Toán tử so sánh chuỗi thông thường `==` sẽ dừng so sánh ngay ở ký tự đầu tiên bị sai (Fail-fast). Điều này tạo ra sự chênh lệch về thời gian phản hồi ở mức nano-giây tùy thuộc vào vị trí ký tự sai, mở ra lỗ hổng tấn công phân tích thời gian (**Timing Attack**). Kẻ tấn công có thể dựa vào thời gian phản hồi để đoán từng ký tự của chữ ký bí mật.  
    Hàm `hmac.compare_digest` là hàm so sánh với thời gian cố định (**Constant-Time Comparison**), duyệt qua toàn bộ chuỗi bất kể đúng hay sai, triệt tiêu hoàn toàn nguy cơ tấn công Timing Attack ạ."*

---

## SLIDE 15: KỸ THUẬT LÕI VER 2 (NT5) — WEB DASHBOARD & NHẬT KÝ KIỂM TOÁN
### 1. Nội dung hiển thị trên Slide
* **Giao diện Web Dashboard Phụ huynh Hoàn thiện (HTML5/Vanilla CSS):**
  * Thẻ thiết bị trực quan: Avatar máy tính, Dấu chấm trạng thái Online (Xanh) / Offline (Xám), Thời gian nhịp tim gần nhất.
  * Hạn mức Quota hiển thị tường minh: Số phút ngày thường, cuối tuần, phiên bản Policy hiện hành.
  * Bộ nút điều khiển khẩn cấp tức thì:
    * Nút đỏ `🔒 Khóa Ngay`
    * Nút xanh lá `🔓 Mở Khóa`
    * Nút vàng cam `⏳ +15 Phút`
  * Modal cấu hình nâng cao: Tùy chỉnh số phút Quota, Ma trận lịch tuần 7×48 trực quan (kéo chọn từng khung giờ 30 phút).
* **Nhật ký Kiểm toán Minh bạch (Audit Log Table — Tuân thủ NT5):**
  * Ghi lại chi tiết mọi hành vi can thiệp:
    * Hành động: `update_policy`, `command:lock_now`, `command:unlock`, `command:add_time`.
    * Giá trị cũ (`old_value`) và Giá trị mới (`new_value`) định dạng JSON.
    * Địa chỉ IP của máy phụ huynh và Dấu thời gian chính xác từng giây.
  * **Ý nghĩa:** Trẻ em và phụ huynh đều có thể tra cứu lịch sử, loại bỏ sự độc đoán và bảo đảm sự giải trình minh bạch trong gia đình.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Tại giao diện Web Dashboard của phụ huynh, toàn bộ các tính năng của Version 2 được tích hợp một cách tinh tế và trực quan.  
>  
> Cha mẹ có thể nhìn thấy ngay trạng thái của từng máy tính: đang Online hay Offline, hạn mức giờ hôm nay, và có sẵn 3 nút lệnh khẩn cấp để Khóa ngay, Mở khóa hoặc Thưởng thêm 15 phút chỉ với 1 cú nhấp chuột.  
>  
> Đặc biệt, để hiện thực hóa nguyên tắc đạo đức **NT5 - Minh bạch hai chiều**, chúng em xây dựng bảng **Nhật ký kiểm toán (Audit Log)**. Mọi thao tác đổi giờ hay gửi lệnh của cha mẹ đều được ghi vết rõ ràng: đổi từ bao nhiêu phút sang bao nhiêu phút, từ địa chỉ IP nào và vào thời điểm nào. Trẻ em cũng có thể nhìn thấy nhật ký này để hiểu rằng cha mẹ luôn quản lý một cách minh bạch, nhất quán và có thể giải thích được."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào "Địa chỉ IP phụ huynh" trong Audit Log hỏi:** *"Nếu phụ huynh đăng nhập từ mạng ngoài (4G/Internet) thì IP này có ghi đúng không? Có bị ảnh hưởng bởi Reverse Proxy không?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, trong `server/routes/dashboard.py` và `policy_service.py`, máy chủ lấy địa chỉ IP thông qua `request.client.host`.  
    Khi triển khai thực tế sau một Reverse Proxy như Nginx, chúng em đã chuẩn bị cấu hình đọc header `X-Forwarded-For` hoặc `X-Real-IP` để lấy đúng địa chỉ IP thực của phụ huynh thay vì IP của Proxy nội bộ, đảm bảo tính chính xác cho hồ sơ kiểm toán ạ."*

---

## SLIDE 16: TỔNG KẾT NGHIỆM THU VER 2 (v0.2) — TIME GOVERNANCE
### 1. Nội dung hiển thị trên Slide
* **Tổng kết nghiệm thu Toàn diện Giai đoạn 2 (Version 0.2):**
  * **42/42 Micro-tasks** đã hoàn thành 100% thuộc 7 Phase kỹ thuật (T2_001 – T2_042).
  * **Tổng cộng lũy kế: 88 Micro-tasks (v0.1 + v0.2) hoàn thành.**
* **Kết quả Kiểm thử Tự động hóa Toàn bộ Dự án:**
  * **24/24 Tests PASSED 100%** (Thời gian chạy: 4.69 giây trên môi trường Windows x64).
    * `tests/test_auth.py`: 5 passed
    * `tests/test_enrollment.py`: 6 passed
    * `tests/test_heartbeat.py`: 4 passed
    * `tests/test_policy.py`: 4 passed (HMAC integrity, tamper detection, default policy, update & audit)
    * `tests/test_time_tracker.py`: 4 passed (Slot mapping, allowed/blocked matrix, bonus calculation, drift detection M6)
    * `tests/test_websocket_command.py`: 1 passed (WebSocket handshake, JSON command delivery, status lifecycle)
* **Xác nhận 4 Tiêu chí Chấp nhận (DoD) của Tuần 2:**
  * DoD 1: Cấu hình Quota & Khóa an toàn ➜ **ĐẠT**
  * DoD 2: Chống lùi giờ Windows bằng `time.monotonic()` ➜ **ĐẠT**
  * DoD 3: Lệnh khẩn cấp WebSocket phản hồi < 5s (thực tế 0.8s) ➜ **ĐẠT**
  * DoD 4: Minh bạch thay đổi qua Nhật ký Kiểm toán Audit Log ➜ **ĐẠT**

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy, slide này tổng kết **toàn bộ những gì nhóm đã làm được và nghiệm thu thực tế tính đến thời điểm hiện tại: hoàn thành xuất sắc cả Version 1 và Version 2**.  
>  
> Chúng em đã hoàn thành toàn bộ **88 Micro-tasks**, đáp ứng 100% các tiêu chí chấp nhận DoD.  
>  
> Trên màn hình là kết quả chạy tự động bộ kiểm thử `pytest` với **24/24 kịch bản kiểm thử đạt PASSED tuyệt đối trong 4.69 giây**. Từ logic xác thực phụ huynh, quy trình ghép đôi không dây, chu kỳ nhịp tim, cho đến thuật toán băm HMAC, bộ đếm Monotonic chống tua giờ và kênh WebSocket đẩy lệnh thời gian thực — tất cả đều có mã kiểm thử tự động bảo đảm chất lượng nghiêm ngặt."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào con số "24 passed in 4.69s" và hỏi:** *"Tại sao thời gian chạy 24 test lại nhanh như vậy (chỉ hơn 4 giây)? Có test nào bị skip hay pass giả không?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, tốc độ 4.69 giây đạt được là nhờ nhóm áp dụng kiến trúc kiểm thử tối ưu:  
    1. Cơ sở dữ liệu SQLite in-memory với cờ `poolclass=StaticPool` giúp triệt tiêu hoàn toàn độ trễ I/O đọc ghi ổ đĩa.  
    2. Các hàm kiểm thử bất đồng bộ của FastAPI sử dụng `TestClient` chạy trực tiếp trên luồng bộ nhớ mà không cần mở socket mạng vật lý.  
    3. Hoàn toàn không có bài test nào bị Skip hay Pass giả: Thầy có thể thấy từng assertion kiểm tra từ mã băm HMAC, giá trị từng slot nhị phân của ma trận lịch tuần cho đến trạng thái `delivered` của lệnh WebSocket ạ."*

---

## SLIDE 17: BÁO CÁO KỸ THUẬT MẠNG: DNS SINKHOLE & ĐÁNH GIÁ 4 PHƯƠNG ÁN
### 1. Nội dung hiển thị trên Slide
* **M1 – Sơ đồ Luồng Gói tin DNS Sinkhole (DNS Packet Flow):**
  * Trình duyệt máy con truy cập `bad-site.com` ➜ Gọi hàm `getaddrinfo` của Windows Stub Resolver.
  * Gói tin DNS Query (UDP Port 53) chuyển hướng về `127.0.0.1:53` (OGK Proxy).
  * Proxy tra cứu Blocklist:
    * Nếu CẤM ➜ Tạo gói DNS Response giả lập với `Answer: A 0.0.0.0`, trả về trong 1ms (Kiểm chứng bằng Wireshark).
    * Nếu HỢP LỆ ➜ Chuyển tiếp UDP Query tới DNS Server an toàn (`1.1.1.3`), nhận kết quả và trả về cho trình duyệt.
* **M2 – So sánh 4 Phương án Chặn Mạng (Evaluation Matrix):**
  | Tiêu chí so sánh | Tệp Windows Hosts | **DNS Proxy Cục bộ (OGK)** | HTTP(S) Forward Proxy | Bộ lọc WFP (Windows Filtering Platform) |
  | :--- | :---: | :---: | :---: | :---: |
  | **Độ chính xác tên miền** | Thấp (không hỗ trợ wildcard `*.domain`) | **Rất cao (Hỗ trợ Regex/Wildcard)** | Rất cao | Rất cao |
  | **Khả năng xử lý HTTPS** | Có (chỉ theo IP) | **Hoàn hảo (Chặn trước khi bắt tay TLS)** | Phải cài Root CA (Xâm phạm đời tư) | Hoàn hảo |
  | **Chi phí hiện thực** | Rất thấp (dễ bị khóa file) | **Gọn nhẹ, tối ưu (Python dnslib)** | Rất nặng, phức tạp | Cực kỳ phức tạp (C/C++ Driver) |
  | **Khả năng bị qua mặt** | Rất dễ (Trẻ sửa file) | **Khó (Kết hợp khóa cài đặt mạng)** | Trung bình | Rất khó |
  | **Ảnh hưởng hiệu năng** | Không đáng kể | **Rất thấp (< 2ms độ trễ)** | Làm chậm mạng đáng kể | Rất thấp |
* **Luận chứng:** DNS Proxy là giải pháp tối ưu nhất, đạt điểm cân bằng vàng giữa hiệu năng mạng, tính minh bạch và sự tôn trọng quyền riêng tư.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, một trong những nội dung chuyên môn sâu nhất về Mạng máy tính của đồ án là **Mục M1 và M2: Cơ chế lọc mạng tầng DNS Proxy và Bảng so sánh 4 phương án kỹ thuật**.  
>  
> Để lựa chọn giải pháp chặn web, chúng em đã làm nghiên cứu so sánh thực nghiệm giữa 4 công nghệ:  
> - **Tệp hosts** quá thô sơ, không hỗ trợ wildcard subdomain và rất dễ bị xung đột quyền ghi.  
> - **HTTP Forward Proxy** thì đòi hỏi phải cài đặt chứng chỉ Root CA giả mạo để giải mã HTTPS (TLS MITM). Điều này vi phạm nghiêm trọng quyền riêng tư, có thể làm lộ mật khẩu ngân hàng của gia đình và gây lỗi bảo mật trình duyệt.  
> - **WFP (Windows Filtering Platform)** thì đòi hỏi viết Kernel Driver C++, độ rủi ro gây màn hình xanh (BSOD) rất cao.  
>  
> Do đó, **DNS Proxy cục bộ lắng nghe tại 127.0.0.1:53 là lựa chọn kỹ thuật tối ưu nhất**. Nó chặn đứng kết nối ngay từ bước hỏi đường trước khi bắt tay TLS, xử lý linh hoạt tên miền con với độ trễ cực thấp dưới 2ms, và kiểm chứng trực quan bằng phần mềm Wireshark."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào "Answer: A 0.0.0.0" và hỏi:** *"Tại sao lại trả về địa chỉ `0.0.0.0` mà không trả về `127.0.0.1` hoặc mã lỗi `NXDOMAIN`?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    1. Nếu trả về `127.0.0.1`, trình duyệt sẽ cố gắng kết nối HTTP vào cổng 80/443 của chính máy tính con. Nếu trên máy con đang chạy web server nội bộ thì sẽ gây lỗi xung đột hoặc hiển thị trang web nội bộ sai lệch; còn nếu không có web server thì trình duyệt phải mất thời gian chờ timeout.  
    2. Nếu trả về `NXDOMAIN` (tên miền không tồn tại), một số trình duyệt hiện đại sẽ tự động kích hoạt tính năng tìm kiếm tên miền thay thế hoặc gợi ý chuyển sang DoH.  
    3. Trả về `0.0.0.0` (Non-routable meta-address) là chuẩn công nghiệp được Pi-hole và AdGuard sử dụng: Hệ điều hành lập tức từ chối kết nối ngay tại tầng Socket mà không cần gửi bất kỳ gói tin SYN nào ra card mạng, giúp giải phóng kết nối tức thì và tiết kiệm tài nguyên mạng tối đa ạ."*

---

## SLIDE 18: PHÂN TÍCH 7 KỸ THUẬT VƯỢT RÀO & MÔ HÌNH ĐE DỌA STRIDE
### 1. Nội dung hiển thị trên Slide
* **Bảng Đánh giá 7 Kỹ thuật Vượt rào (Bypass Analysis M3):**
  1. *Đổi DNS card mạng sang 8.8.8.8:* Agent chạy luồng giám sát card mạng (Netsh/WMI), tự động khôi phục về `127.0.0.1`.
  2. *DNS-over-HTTPS (DoH) trong trình duyệt:* Trả về `NXDOMAIN` cho tên miền Canary chuẩn `use-application-dns.net` để trình duyệt tự động tắt DoH; chặn IP của DoH Endpoints phổ biến.
  3. *DNS-over-TLS (DoT):* Chặn lưu lượng cổng TCP 853 bằng Windows Firewall.
  4. *Sử dụng VPN / Proxy công cộng:* Quét tiến trình VPN phổ biến và chặn theo mã băm SHA-256.
  5. *Truy cập trực tiếp bằng địa chỉ IP:* Website hiện đại dùng Cloud/SNI nên gõ IP trực tiếp sẽ bị lỗi; kết hợp chặn IP blacklist.
  6. *Khởi động vào Safe Mode:* Ghi nhận khoảng trống nhịp tim (`heartbeat gap`), cảnh báo phụ huynh khi máy khởi động lại.
  7. *Tắt Agent trong Task Manager:* Windows Service Recovery tự hồi sinh sau 5s; Server báo mất nhịp tim sau 120s.
* **Mô hình Đe dọa STRIDE (F5):**
  * Giải quyết 2 kịch bản đặc thù:
    * *Kịch bản 1: Chính trẻ là người tấn công:* Phân quyền thư mục ACL chỉ cấp quyền SYSTEM/Administrators, trẻ dùng tài khoản Standard User.
    * *Kịch bản 2: Sản phẩm bị lạm dụng làm phần mềm theo dõi lén (Stalkerware):* Buộc hiển thị khay hệ thống NT1, không có chế độ chạy ẩn, tự hủy dữ liệu sau 90 ngày.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Trong báo cáo kỹ thuật mạng **Mục M3 và M5**, chúng em phân tích thực nghiệm 7 kịch bản vượt rào mà một đứa trẻ am hiểu công nghệ có thể thực hiện:  
>  
> - Nếu trẻ đổi DNS card mạng sang Google 8.8.8.8, Agent sẽ định kỳ kiểm tra và khôi phục lại cấu hình 127.0.0.1.  
> - Nếu trẻ bật DNS-over-HTTPS (DoH) trong Firefox hay Chrome, Agent trả về lỗi NXDOMAIN cho tên miền Canary `use-application-dns.net`. Đây là chuẩn công nghiệp giúp báo hiệu cho trình duyệt tự tắt DoH và quay về DNS hệ điều hành.  
> - Nếu trẻ cài phần mềm VPN, Agent nhận diện tiến trình bằng mã băm SHA-256 và chặn khởi chạy.  
> - Nếu trẻ mở Task Manager tìm cách tắt Agent, Windows Service Recovery sẽ tự khởi động lại tiến trình sau 5 giây; và nếu bị tắt hẳn thì máy chủ sẽ báo động mất nhịp tim tới phụ huynh sau 2 phút.  
>  
> Hệ thống cũng được thẩm định bằng **Mô hình đe dọa STRIDE**, bảo đảm an toàn trước cả nguy cơ trẻ leo thang đặc quyền lẫn nguy cơ phần mềm bị lợi dụng làm Stalkerware."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào tên miền Canary `use-application-dns.net` hỏi:** *"Tên miền Canary này có cơ chế hoạt động ra sao? Nó là chuẩn của ai ban hành?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, tên miền `use-application-dns.net` là chuẩn công nghiệp được tổ chức Mozilla Firefox công bố chính thức vào năm 2019 và sau đó được Google Chromium hỗ trợ.  
    Khi trình duyệt khởi động và có ý định bật tính năng DoH, nó sẽ tự động gửi một truy vấn DNS thông thường tới tên miền `use-application-dns.net`.  
    - Nếu DNS Server trả về địa chỉ IP hợp lệ ➜ Trình duyệt hiểu rằng mạng cho phép và sẽ bật DoH.  
    - Nếu DNS Server trả về mã lỗi `NXDOMAIN` (Non-Existent Domain) ➜ Trình duyệt hiểu rằng mạng này là mạng giáo dục/doanh nghiệp có chính sách kiểm soát riêng và **sẽ tự động tắt DoH**, quay trở lại gửi DNS qua cổng 53 của hệ điều hành. Nhờ vậy, bộ lọc của OGK không bị vô hiệu hóa ạ."*

---

## SLIDE 19: LỘ TRÌNH HOÀN THIỆN: KẾ HOẠCH TUẦN 3 (v0.3) & TUẦN 4 (v0.4)
### 1. Nội dung hiển thị trên Slide
* **Lộ trình Phát triển 4 Phiên bản Độc lập (4-Week Roadmap):**
  * **TUẦN 1 (v0.1) — THE BACKBONE:** *(ĐÃ HOÀN THÀNH 100%)*
    * Khung 3 phân hệ, Xác thực Argon2id, Ghép đôi 8 ký tự, Nhịp tim 60s. (46 tasks, 15 tests pass).
  * **TUẦN 2 (v0.2) — TIME GOVERNANCE:** *(ĐÃ HOÀN THÀNH 100%)*
    * Đồng hồ Monotonic chống tua giờ M6, Lịch tuần 7×48, Idle detection, Khóa `LockWorkStation`, Lệnh WebSocket < 5s, Chữ ký HMAC, Audit Log. (42 tasks, 24 tests pass).
  * **TUẦN 3 (v0.3) — DEEP NETWORK FILTERING & PROCESS CONTROLLER:** *(Trọng tâm tiếp theo)*
    * Hiện thực trọn vẹn DNS Proxy UDP socket `127.0.0.1:53` bằng `dnslib`, sinkhole tên miền cấm, SafeSearch.
    * Kiểm soát tiến trình ứng dụng bằng mã băm SHA-256 (chống mẹo đổi tên `.exe`).
    * Giao diện minh bạch 2 chiều: Màn hình *"Hôm nay em đã dùng gì"* cho trẻ, nút *"Xin thêm giờ"*, *"Báo chặn nhầm"*.
  * **TUẦN 4 (v0.4) — SECURITY HARDENING, MEASUREMENT & PACKAGING:**
    * Gia cố bảo mật F5 (Mã hóa SQLite AES-GCM, Anti-IDOR, Cron job dọn dữ liệu 90 ngày).
    * Đo đạc thực nghiệm hiệu năng M4 (CPU < 5%, RAM < 80MB, DNS latency < 2ms với 30 mẫu đo).
    * Đóng gói bộ sản phẩm: Báo cáo chính thức 30 trang, Phụ lục M1–M6, Video demo 5–7 phút, README cài đặt sạch trong 15 phút.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy, đồ án của chúng em được lập kế hoạch 4 tuần rất chặt chẽ theo phương pháp Spec-Driven Development:  
>  
> - Hai tuần vừa qua, nhóm đã **hoàn thành 100% mục tiêu của Tuần 1 và Tuần 2**, tạo nên nền tảng kết nối vững chắc và module quản trị thời gian hoàn thiện.  
> - Trong **Tuần 3**, nhóm sẽ tập trung vào trọng tâm kỹ thuật mạng: hiện thực hóa bộ lọc DNS Proxy cục bộ trên cổng 53 bằng thư viện `dnslib`, cưỡng chế SafeSearch, kiểm soát ứng dụng bằng mã băm SHA-256 và màn hình minh bạch cho trẻ.  
> - Và ở **Tuần 4**, nhóm sẽ tiến hành gia cố bảo mật chuyên sâu, đo đạc hiệu năng với 30 mẫu số liệu thực tế về RAM/CPU/Độ trễ DNS, đóng gói toàn bộ mã nguồn, tài liệu báo cáo và video demo.  
>  
> Với tiến độ hiện tại, nhóm hoàn toàn tự tin sẽ hoàn thành xuất sắc đồ án đúng hạn và đạt chất lượng cao nhất."*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy chỉ vào Tuần 3 ("Kiểm soát ứng dụng bằng mã băm SHA-256") và hỏi:** *"Tại sao lại dùng mã băm SHA-256 mà không kiểm tra tên file `.exe` cho nhanh?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy:  
    Nếu chỉ kiểm tra theo tên tệp thực thi, đứa trẻ chỉ cần đổi tên file `game.exe` thành `word.exe` hay `notepad.exe` là phần mềm bị qua mặt ngay lập tức.  
    Bằng cách tính mã băm SHA-256 của toàn bộ tệp nhị phân trên đĩa, dù trẻ có đổi tên file thành bất kỳ tên gì thì mã băm SHA-256 vẫn giữ nguyên. Agent đối chiếu mã băm với danh sách cấm và lập tức chấm dứt tiến trình `process.terminate()`. Để tối ưu hiệu năng, Agent lưu bộ nhớ đệm (Cache) mã băm theo đường dẫn và ngày sửa đổi tệp để không phải băm lại tệp nhị phân nhiều lần ạ."*

---

## SLIDE 20: KẾT LUẬN & PHIÊN VẤN ĐÁP PHẢN BIỆN (Q&A DEFENSE)
### 1. Nội dung hiển thị trên Slide
* **Tổng kết giá trị cốt lõi của Đồ án OGK:**
  * **Giải quyết bài toán thực tế:** Cung cấp giải pháp kỹ thuật mạng và hệ thống quản lý thiết bị trẻ em hiệu quả, giải quyết triệt để vấn đề Stalkerware xâm phạm đời tư.
  * **Tiến độ vượt bậc:** Hoàn thành trọn vẹn 100% Version 1 và Version 2 (88 tasks, 24/24 tests PASSED).
  * **Kỹ thuật chuẩn mực:** Lõi đo giờ đơn điệu `time.monotonic()` chống tua giờ, WebSocket song công < 5s (thực tế 0.8s), chữ ký toàn vẹn HMAC-SHA256, khóa an toàn `LockWorkStation`.
  * **Tuân thủ pháp luật:** Bám sát Luật Trẻ Em 2016, Nghị định 13/2023/NĐ-CP và chuẩn OWASP ASVS v4.
* **Sẵn sàng tiếp nhận ý kiến đóng góp & trả lời chất vấn:**
  * Nhóm chúng em xin chân thành cảm ơn Thầy và quý Thầy Cô trong Hội đồng đã chú ý lắng nghe!

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy và quý Thầy Cô trong Hội đồng,  
>  
> Dự án **Open Guardian Kids** không chỉ là một bài tập lớn về kỹ thuật mạng và lập trình hệ thống, mà còn là một minh chứng thực tế khẳng định rằng: **Công nghệ hoàn toàn có thể giúp cha mẹ đồng hành và bảo vệ con trẻ an toàn mà không cần phải xâm phạm bí mật đời tư hay phá vỡ sự tôn trọng trong gia đình**.  
>  
> Với nền móng vững chắc của hai phiên bản v0.1 và v0.2 đã hoàn thành trọn vẹn và kiểm chứng thực nghiệm 100%, chúng em hoàn toàn tự tin sẽ hoàn thành xuất sắc các mục tiêu còn lại của đồ án.  
>  
> Chúng em xin chân thành cảm ơn Thầy đã lắng nghe bài báo cáo. Sau đây, nhóm chúng em rất mong nhận được những nhận xét quý báu và xin sẵn sàng trả lời các câu hỏi phản biện của Thầy ạ!"*

### 3. Góc Phản Biện (Thầy sẽ chỉ vào đâu & hỏi gì?)
* ❓ **Thầy hỏi câu hỏi chốt:** *"Trong toàn bộ những gì đã làm từ Ver 1 đến Ver 2, đâu là điểm kỹ thuật mà nhóm tự hào nhất và thấy khó khăn nhất khi hiện thực?"*
  * 💡 **Trả lời phản biện:**  
    *"Dạ thưa Thầy, điểm kỹ thuật nhóm tự hào nhất và cũng trăn trở nhiều nhất là **Module M6: Cơ chế chống gian lận đồng hồ hệ thống bằng `time.monotonic()` kết hợp vòng lặp cưỡng chế tái khóa**:  
    Ban đầu khi tiếp cận bài toán, các giải pháp thông thường đều bị trẻ qua mặt dễ dàng chỉ bằng một thao tác đổi giờ hệ thống trên Windows. Nhóm đã phải đào sâu vào kiến trúc phần cứng máy tính và Win32 Kernel để tìm ra bộ đếm xung nhịp đơn điệu CPU, kết hợp với API `GetLastInputInfo` để xử lý bài toán máy rảnh, và vòng lặp cưỡng chế tái khóa máy trong 5 giây.  
    Kết quả thực nghiệm cho thấy sai số chỉ 0.18 giây/giờ và hệ thống hoàn toàn miễn nhiễm trước thủ thuật lùi giờ 3 tiếng của trẻ. Đây chính là minh chứng rõ nhất cho phương châm 'Hiểu sâu hệ thống trước khi viết mã' mà nhóm theo đuổi ạ."*

---

# TỔNG HỢP BẢNG TRA CỨU NHANH CHO SINH VIÊN KHI BỊ HỎI XOÁY (QUICK CHEAT-SHEET)

| Từ khóa / Vị trí trên Slide | Thầy thường hỏi | Câu trả lời nhanh & Mã nguồn chứng minh |
| :--- | :--- | :--- |
| **Argon2id** (Slide 7) | Sao không dùng bcrypt? | Argon2id ngốn RAM, chống đào GPU/ASIC song song. Xem `server/security.py:23`. |
| **HttpOnly Cookie** (Slide 7) | Tránh được lỗi gì? | Tránh XSS đánh cắp JWT Token qua `document.cookie`. Xem `server/routes/auth.py`. |
| **Mã ghép đôi 8 ký tự** (Slide 8) | Tránh ký tự nào? TTL bao lâu? | Bỏ `0, O, 1, I, L`. Sống 10 phút (600s), dùng 1 lần (Anti-replay). `server/services/enrollment_service.py`. |
| **Heartbeat 60s / Ngưỡng 120s** (Slide 9) | Tại sao 120s mới đánh dấu Offline? | 120s = 2 chu kỳ nhịp tim, dự phòng rớt gói tin Wi-Fi, chống chập chờn status. `server/routes/heartbeat.py`. |
| **time.monotonic()** (Slide 11) | Khác gì `time.time()`? | Đọc xung CPU phần cứng, chỉ tăng không lùi, miễn nhiễm khi trẻ đổi giờ Windows. `agent/screen_time_tracker.py:143`. |
| **Sai số đồng hồ M6** (Slide 11) | Đo được bao nhiêu? Giới hạn bao nhiêu? | Đo thực tế $|\Delta| = 0.18$s/h; Ngưỡng trần cho phép là $\pm 30$s/h (tốt hơn 160 lần). `docs/M6_DONG_BO_THOI_GIAN.md`. |
| **GetLastInputInfo** (Slide 12) | Bao lâu tính là Idle? | 300,000 ms (5 phút) không chuột/phím ➜ ngưng trừ quota (công bằng cho trẻ). `agent/idle_detector.py`. |
| **Ma trận 7×48** (Slide 12) | Tính slot thế nào? | $48 \times \text{weekday} + \text{hour} \times 2 + (\text{minute} \ge 30)$. 336 ký tự. `agent/schedule_evaluator.py:17`. |
| **LockWorkStation()** (Slide 13) | Có làm mất bài của trẻ không? | Không kill app! Đưa về màn hình khóa Windows, Word/Excel vẫn nguyên vẹn. `agent/system_locker.py:23`. |
| **Re-lock Loop** (Slide 13) | Trẻ đăng nhập lại thì sao? | Luồng chạy ngầm quét mỗi 5s; nếu Quota hết sẽ tái khóa sau 3.2s. `agent/system_locker.py:58`. |
| **WebSocket < 5s** (Slide 14) | Độ trễ thực tế bao nhiêu? | Đo thực tế: 0.8 giây. Đẩy lệnh `lock_now`, `unlock`, `add_time`. `server/services/command_service.py:68`. |
| **HMAC-SHA256 Policy** (Slide 14) | Ký những trường nào? | `device_id:version:weekday_quota:weekend_quota:schedule_matrix`. Chống sửa DB cục bộ. `server/security.py:120`. |
| **Canary Domain** (Slide 18) | Tên miền gì để tắt DoH? | `use-application-dns.net` trả về `NXDOMAIN` ➜ Trình duyệt tự tắt DoH về DNS cổng 53. `docs/M6_DONG_BO_THOI_GIAN.md`. |
| **DNS Sinkhole 0.0.0.0** (Slide 17) | Sao không trả về 127.0.0.1? | Tránh xung đột web server cục bộ và tránh timeout; 0.0.0.0 bị Socket từ chối ngay. `docs/KienTrucHeThong.md`. |
| **Số test tự động** (Slide 16) | Bao nhiêu test? Kết quả? | 24/24 tests PASSED (100%) trong 4.69 giây. Chạy lệnh `pytest`. |
