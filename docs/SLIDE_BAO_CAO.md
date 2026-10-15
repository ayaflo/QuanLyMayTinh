# BÁO CÁO THUYẾT TRÌNH TOÀN BỘ ĐỒ ÁN VÀ TIẾN ĐỘ THỰC HIỆN
## ĐỀ TÀI: XÂY DỰNG ỨNG DỤNG HỖ TRỢ QUẢN LÝ VIỆC SỬ DỤNG MÁY TÍNH CỦA TRẺ EM
### TÊN THƯƠNG HIỆU HỆ THỐNG: OPEN GUARDIAN KIDS (OGK)
> **Học phần:** Chuyên đề Tốt nghiệp Mạng máy tính & Truyền thông  
> **Phương châm cốt lõi:** *"Công cụ đồng hành, không phải phần mềm theo dõi lén"*  
> **Phương pháp quản trị:** Karpathy Engineering Principles kết hợp Spec-Driven Development  
> **Thời lượng đồ án:** 04 tuần (4 phiên bản phát triển độc lập)

---

## MỤC LỤC TỔNG QUAN
1. **Slide 1:** Trang tiêu đề đồ án (Title Slide)
2. **Slide 2:** Bối cảnh, Thực trạng & Vấn đề giải quyết (Context & Problem Statement)
3. **Slide 3:** Triết lý Thiết kế Cốt lõi & 6 Nguyên tắc Đạo đức Bắt buộc (NT1 – NT6)
4. **Slide 4:** Căn cứ Pháp lý & Chuẩn An toàn Thông tin Tham chiếu
5. **Slide 5:** Kiến trúc Tổng thể Hệ thống 3 Khối (Distributed 3-Tier Architecture)
6. **Slide 6:** Ngăn xếp Công nghệ & Phương pháp Quản trị Kỹ thuật (Tech Stack & Karpathy)
7. **Slide 7:** Luồng Nghiệp vụ 1: Xác thực Phụ huynh & Quản trị Phiên Bảo mật
8. **Slide 8:** Luồng Nghiệp vụ 2: Ghép đôi Thiết bị Không dây An toàn (Device Enrollment)
9. **Slide 9:** Luồng Nghiệp vụ 3: Viễn trắc Nhịp tim Định kỳ & Nhận diện Trạng thái (Heartbeat Loop)
10. **Slide 10:** KẾT QUẢ ĐÃ ĐẠT ĐƯỢC (Milestone Tuần 1 / v0.1 Review & 100% Tests)
11. **Slide 11:** Thiết kế Chi tiết: Quản lý Thời gian (F1) & Cơ chế Chống Tua Giờ Hệ thống
12. **Slide 12:** Thiết kế Chi tiết: Lọc Mạng Tầng DNS Proxy (F2) & Kiểm soát Ứng dụng theo SHA-256
13. **Slide 13:** Thiết kế Chi tiết: Minh bạch Hai chiều (F3) & Lệnh Khẩn WebSocket (F4)
14. **Slide 14:** Báo cáo Kỹ thuật Mạng Chuyên sâu: Luồng DNS Wireshark & So sánh 4 Giải pháp Chặn (M1, M2)
15. **Slide 15:** Phân tích 7 Kỹ thuật Vượt rào (Bypass) & Biện pháp Đối phó (M3)
16. **Slide 16:** An toàn Thông tin Chiều sâu & Mô hình Đe dọa STRIDE (F5 & ASVS v4)
17. **Slide 17:** Kế hoạch Triển khai 4 Tuần & Lộ trình Hoàn thiện Dự án
18. **Slide 18:** Kết luận & Bộ Câu hỏi – Trả lời Vấn đáp Phản biện (Q&A Defense)

---

# CHI TIẾT TỪNG SLIDE & LỜI THOẠI BÁO CÁO (SPEAKER SCRIPT)

---

## SLIDE 1: TRANG TIÊU ĐỀ ĐỒ ÁN
### 1. Nội dung hiển thị trên Slide
* **Tên đồ án:** XÂY DỰNG ỨNG DỤNG HỖ TRỢ QUẢN LÝ VIỆC SỬ DỤNG MÁY TÍNH CỦA TRẺ EM
* **Tên giải pháp:** OPEN GUARDIAN KIDS (OGK) — Version 0.1
* **Khẩu hiệu (Motto):** *"Công cụ đồng hành, không phải phần mềm theo dõi lén"*
* **Chuyên ngành:** Mạng Máy Tính & Truyền Thông Dữ Liệu
* **Giảng viên hướng dẫn:** [Tên Giảng Viên Hướng Dẫn]
* **Sinh viên thực hiện:** [Tên Sinh Viên 1 - MSSV] & [Tên Sinh Viên 2 - MSSV]

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính chào quý Thầy/Cô trong Hội đồng và các bạn sinh viên. Hôm nay, nhóm chúng em xin phép được báo cáo tiến độ đồ án Chuyên đề Tốt nghiệp với đề tài: **'Xây dựng ứng dụng hỗ trợ quản lý việc sử dụng máy tính của trẻ em'**, mang tên thương mại kỹ thuật là **Open Guardian Kids (OGK)**.*  
>  
> *Ngay từ khi đặt nét bút đầu tiên để thiết kế hệ thống, nhóm chúng em đã xác định một tôn chỉ cốt lõi không thể thay đổi: **'Open Guardian Kids là một công cụ đồng hành giữa cha mẹ và con cái, kiên quyết không phải là phần mềm gián điệp hay theo dõi lén'**. Hôm nay, chúng em xin trình bày toàn diện bức tranh kiến trúc, căn cứ pháp lý, ngăn xếp công nghệ, kết quả nghiệm thu thực tế đã hoàn thành trong giai đoạn vừa qua, và lộ trình kỹ thuật chi tiết của toàn bộ dự án."*

---

## SLIDE 2: BỐI CẢNH, THỰC TRẠNG & VẤN ĐỀ GIẢI QUYẾT
### 1. Nội dung hiển thị trên Slide
* **Thực trạng thời đại số:**
  * Trẻ em tiếp cận máy tính và mạng Internet từ độ tuổi rất nhỏ (6–11 tuổi) cho nhu cầu học tập, giải trí trực tuyến.
  * Thách thức: Nguy cơ nghiện màn hình, mất tập trung bài vở, tiếp cận nội dung độc hại/người lớn, lừa đảo trực tuyến.
* **Mặt trái của các phần mềm thương mại hiện nay (Commercial Spyware / Stalkerware):**
  * Chụp lén màn hình định kỳ (Screenshots), ghi lại toàn bộ bàn phím (Keylogger), đọc trộm tin nhắn cá nhân.
  * Chạy ẩn lén lút (Stealth mode), trẻ không hề biết mình đang bị theo dõi.
  * Đẩy dữ liệu nhạy cảm của gia đình lên máy chủ đám mây của bên thứ ba, tiềm ẩn nguy cơ rò rỉ dữ liệu cá nhân nghiêm trọng.
  * **Hậu quả:** Phá vỡ niềm tin giữa cha mẹ và con cái, vi phạm pháp luật bảo vệ quyền trẻ em.
* **Mục tiêu của OGK:** Cung cấp giải pháp kỹ thuật quản trị mạng và thời gian hiệu quả, dựa trên sự thỏa thuận, minh bạch và tôn trọng quyền riêng tư tuyệt đối.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy Cô, trong thời đại số hóa, chiếc máy tính là công cụ học tập không thể thiếu của các em học sinh. Tuy nhiên, phụ huynh luôn phải đối mặt với nỗi lo: con dùng máy tính quá giờ, chơi game xuyên đêm, hoặc vô tình lạc vào các trang web độc hại.  
>  
> Để giải quyết vấn đề này, thị trường xuất hiện rất nhiều phần mềm quản lý phụ huynh. Nhưng qua khảo sát kỹ thuật, đa số các phần mềm này lại vận hành dưới hình thức **phần mềm gián điệp (Stalkerware)**: chúng chụp trộm màn hình, gắn keylogger ghi từng phím con gõ, đọc lén tin nhắn và chạy ẩn giấu trong tiến trình hệ thống. Điều này không những vi phạm nghiêm trọng quyền bí mật đời tư theo Luật Trẻ em và Nghị định 13/2023, mà còn gây tổn thương tâm lý và phá hủy mối quan hệ tin tưởng trong gia đình.  
>  
> Đề tài của chúng em ra đời nhằm giải quyết nghịch lý này: **Làm sao để cha mẹ quản lý được thiết bị mạng của con an toàn, hiệu quả nhưng vẫn bảo vệ trọn vẹn sự riêng tư và nhân phẩm của trẻ?**"*

---

## SLIDE 3: TRIẾT LÝ CỐT LÕI & 6 NGUYÊN TẮC BẮT BUỘC (NT1 – NT6)
### 1. Nội dung hiển thị trên Slide
* **Bảng 6 Nguyên tắc Đạo đức & Thiết kế Kỹ thuật (OGK Constitution):**
  * **NT1 – Trẻ biết mình đang được hỗ trợ:** Tray Icon luôn hiện diện trên Taskbar; Balloon Popup thông báo khi máy khởi động; cấm tuyệt đối chế độ chạy ẩn.
  * **NT2 – Tối thiểu dữ liệu (Data Minimisation):** Chỉ ghi nhận 4 siêu dữ liệu: Tên app, tên miền cấp hai, thời lượng, mốc thời gian. Không lưu URL đầy đủ, không tiêu đề cửa sổ, không screenshot, không keylogger.
  * **NT3 – Trẻ có tiếng nói:** Giao diện máy con có nút "Xin thêm giờ" và "Con nghĩ trang này bị chặn nhầm".
  * **NT4 – Mọi hành động giải thích được:** Khi chặn app/web, hiển thị popup giải thích lý do và người đặt luật; cảnh báo trước 10p, 5p, 1p và ân hạn 60s để trẻ lưu bài tập.
  * **NT5 – Minh bạch hai chiều:** Trẻ có màn hình riêng để xem cùng dữ liệu mà phụ huynh thấy; xem được lịch sử thay đổi luật của cha mẹ (Audit log).
  * **NT6 – An toàn có ưu tiên tuyệt đối:** Danh sách miễn chặn vĩnh viễn (Cổng thông tin trường học, Tổng đài bảo vệ trẻ em 111, cứu hộ khẩn cấp).
* **Danh mục Cấm Tuyệt đối (Zero-Tolerance):** Không đọc nội dung tài liệu/email; không dùng kỹ thuật rootkit/mã độc; không gửi dữ liệu ra máy chủ bên thứ ba.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Để biến triết lý thành các ràng buộc kỹ thuật có thể đo lường trong mã nguồn, nhóm chúng em đã xây dựng **6 nguyên tắc thiết kế bắt buộc từ NT1 đến NT6**:  
>  
> - Thứ nhất, **NT1**: Trẻ phải luôn biết có tác tử đồng hành. Icon trên khay hệ thống luôn sáng và hiện thông báo khi máy khởi động. Nếu không hiển thị được icon thì tác tử phải tự ngừng hoạt động.  
> - Thứ hai, **NT2**: Áp dụng nguyên tắc tối thiểu dữ liệu. Chúng em chỉ thu thập đúng 4 siêu dữ liệu kỹ thuật. Tuyệt đối KHÔNG lưu URL đầy đủ vì URL có thể chứa từ khóa tìm kiếm nhạy cảm hoặc token bí mật.  
> - Thứ ba, **NT3 & NT4**: Mọi sự can thiệp đều có tiếng nói hai chiều và lời giải thích rõ ràng. Khi máy sắp hết giờ, hệ thống cảnh báo trước và ân hạn 60 giây để trẻ lưu tài liệu Word hay bài thuyết trình dang dở. Khi chặn một trang web, hệ thống giải thích ai là người đặt quy tắc.  
> - Cuối cùng, **NT5 & NT6**: Trẻ được xem báo cáo giống cha mẹ, và các địa chỉ thiết yếu như cổng trường học hay Tổng đài Quốc gia Bảo vệ Trẻ em 111 luôn được đưa vào danh sách trắng vĩnh viễn, không ai có quyền chặn."*

---

## SLIDE 4: CĂN CỨ PHÁP LÝ & CHUẨN AN TOÀN THÔNG TIN THAM CHIẾU
### 1. Nội dung hiển thị trên Slide
* **Căn cứ Pháp lý Việt Nam (Trích dẫn & Ánh xạ Mã nguồn):**
  * **Nghị định 13/2023/NĐ-CP (Điều 20 - Dữ liệu cá nhân của trẻ em):**
    * *Yêu cầu:* Phải có sự đồng thuận của cha mẹ khi xử lý dữ liệu trẻ em.  
      ➜ *Ánh xạ:* Quy trình tạo mã ghép đôi 8 ký tự trên Web Dashboard (`POST /api/v1/enroll/claim`).
    * *Yêu cầu:* Giới hạn lưu trữ và quyền rút lại sự đồng ý / xóa dữ liệu.  
      ➜ *Ánh xạ:* Tác vụ tự hủy dữ liệu sau 90 ngày; Nút "Xóa toàn bộ dữ liệu của con tôi" xóa sạch trên cả Server và Agent.
  * **Luật Trẻ em 2016 (Điều 21):** Quyền bí mật đời sống riêng tư ➜ *Ánh xạ:* Bảng kê khai chi tiết trong tệp `docs/PRIVACY.md`.
  * **Luật An toàn thông tin mạng 2015 & Luật An ninh mạng 2018 (Điều 29):** Bảo vệ trẻ em trên không gian mạng.
* **Chuẩn Kỹ thuật & An toàn Quốc tế:**
  * **OWASP ASVS v4 (Mức 1):** Checklist tự đánh giá bảo mật API & Web (Session management, Access control, Input validation).
  * **NIST SP 800-63B:** Xác thực phụ huynh chuẩn mực (Argon2id, không lưu mật khẩu dạng plaintext, chống brute-force).

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy Cô, một điểm đặc biệt trong đồ án này là tính tuân thủ pháp lý cao. Chúng em không thiết kế phần mềm theo cảm tính mà đối chiếu từng chức năng vào quy định pháp luật Việt Nam:  
>  
> Cụ thể, theo **Điều 20 Nghị định 13/2023/NĐ-CP**, việc xử lý dữ liệu trẻ em bắt buộc phải có sự đồng ý của cha mẹ. Nhóm hiện thực hóa điều này bằng quy trình ghép đôi thiết bị không dây: cha mẹ phải chủ động đăng nhập tài khoản, tạo mã xác thực 8 ký tự rồi nhập vào máy con. Ngoài ra, tính năng xóa dữ liệu theo yêu cầu và thời hạn lưu trữ tối đa 90 ngày được tích hợp trực tiếp vào kiến trúc CSDL.  
>  
> Về bảo mật kỹ thuật, hệ thống tuân thủ khung chuẩn **OWASP ASVS v4 Mức 1** và **NIST SP 800-63B**, sử dụng thuật toán băm Argon2id hiện đại cho tài khoản phụ huynh để chống lại các kỹ thuật tấn công giải mã trên GPU."*

---

## SLIDE 5: KIẾN TRÚC TỔNG THỂ HỆ THỐNG 3 KHỐI
### 1. Nội dung hiển thị trên Slide
* **Sơ đồ phân tán 3 Khối (Distributed 3-Tier Architecture):**
  1. **OGK-Agent (Máy tính Windows 10/11 của trẻ):**
     * *Tầng nền (Windows Service / Background Process):* Điều phối nhịp tim 60s, kiểm soát thời gian, DNS Proxy lọc mạng `127.0.0.1:53`, CSDL bộ đệm `agent_cache.db`.
     * *Tầng người dùng (User Session - Tray UI):* Biểu tượng khay hệ thống Pystray, bóng bóng thông báo Windows, cửa sổ tương tác dành cho trẻ.
     * *Giao tiếp nội bộ (IPC):* Local loopback / Named pipe.
  2. **OGK-Server (Máy chủ FastAPI trung tâm):**
     * Lắng nghe RESTful API & WebSocket.
     * Quản lý CSDL quan hệ SQLite cấu hình **WAL mode** (`PRAGMA journal_mode=WAL`) xử lý đồng thời ghi/đọc mượt mà.
     * Cung cấp các phân hệ: `/auth`, `/enroll`, `/heartbeat`, `/policy`, `/events`.
  3. **Dashboard Web Phụ huynh (Parent Dashboard):**
     * Giao diện Web HTML5/CSS thuần responsive (hoạt động tối ưu trên máy tính và smartphone).
     * Xem trạng thái Online/Offline thời gian thực, quản lý ghép đôi, cấu hình lịch và quota.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Về mặt kiến trúc, Open Guardian Kids được thiết kế theo mô hình 3 khối phân tán rõ ràng:  
>  
> Khối thứ nhất là **OGK-Agent** chạy trên máy tính Windows của trẻ em. Ở đây có một bài toán hệ thống rất quan trọng: Windows có sự cô lập giữa Session 0 của dịch vụ chạy ngầm và Session người dùng. Do đó, Agent được chia làm 2 tầng: tầng lõi kỹ thuật chạy ngầm chịu trách nhiệm gửi nhịp tim, lọc mạng DNS và đếm giờ; còn tầng khay hệ thống chạy trong phiên người dùng để hiển thị icon và thông báo trực quan cho trẻ.  
>  
> Khối thứ hai là **OGK-Server**, được xây dựng trên nền tảng FastAPI hiệu năng cao, kết hợp CSDL SQLite cấu hình chế độ Write-Ahead Logging (WAL). Chế độ WAL giúp giải quyết bài toán khóa tệp khi nhiều tác vụ đọc/ghi diễn ra đồng thời.  
>  
> Khối thứ ba là **Parent Dashboard**, giao diện web gọn nhẹ, tương thích hoàn toàn với trình duyệt điện thoại, giúp cha mẹ có thể quan sát trạng thái máy tính của con ở bất kỳ đâu."*

---

## SLIDE 6: NGĂN XẾP CÔNG NGHỆ & PHƯƠNG PHÁP QUẢN TRỊ KỸ THUẬT
### 1. Nội dung hiển thị trên Slide
* **Bảng tổng hợp Công nghệ sử dụng:**
  * **Backend Server:** Python 3.11+, FastAPI, Uvicorn, SQLAlchemy ORM, SQLite (WAL mode).
  * **Bảo mật & Mã hóa:** Passlib (Argon2id), PyJWT (HMAC-SHA256), Hashlib (SHA-256 process hashing).
  * **Client Agent:** Python tiêu chuẩn, `pystray` (System Tray), `psutil` (quản trị tiến trình), `dnslib` (DNS Proxy).
  * **Frontend UI:** HTML5 ngữ nghĩa, CSS thuần hiện đại (Glassmorphism, Responsive CSS Grid/Flexbox), Vanilla JS.
  * **Kiểm thử tự động:** Pytest, HTTPX TestClient.
* **4 Nguyên tắc Quản trị Kỹ thuật Karpathy (The Karpathy Guidelines):**
  1. *Think Before Coding:* Đánh giá rủi ro hệ thống (Session 0, DNS port 53, Windows time drift) trước khi gõ code.
  2. *Simplicity First (Tối giản là trên hết):* Kiến trúc phẳng, không microservice phức tạp không cần thiết, vượt qua bài kiểm tra "Senior Engineer Test" trong 15 phút.
  3. *Surgical Changes:* Chia ranh giới 4 tuần phát triển rõ rệt, diff code nhỏ, không viết tính năng thừa ngoài phạm vi.
  4. *Goal-Driven Execution:* Mỗi tuần đều có Tiêu chí nghiệm thu (Definition of Done) định lượng bằng test và kịch bản E2E.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy Cô, phương châm công nghệ của nhóm là **'Simplicity First' - Tối giản, chính xác và hiệu quả**, lấy cảm hứng từ các nguyên tắc kỹ thuật của chuyên gia AI/Kỹ sư Andrej Karpathy.  
>  
> Chúng em kiên quyết không lạm dụng các kiến trúc cồng kềnh như Microservices hay Kubernetes cho một hệ thống quản lý gia đình. Thay vào đó, chúng em tận dụng sức mạnh của **FastAPI bất đồng bộ**, kết hợp **SQLite chế độ WAL**, thư viện **dnslib** để xử lý gói tin DNS tầng thấp và các Win32 API gốc của hệ điều hành.  
>  
> Mọi thay đổi mã nguồn đều mang tính phẫu thuật: chia nhỏ dự án thành 4 phiên bản tăng trưởng ổn định. Mỗi phiên bản đều có bộ kiểm thử tự động đi kèm và kịch bản nghiệm thu rõ ràng."*

---

## SLIDE 7: LUỒNG NGHIỆP VỤ 1 — XÁC THỰC PHỤ HUYNH & BẢO MẬT PHIÊN
### 1. Nội dung hiển thị trên Slide
* **Sơ đồ giải thuật xác thực phụ huynh:**
  * Tiếp nhận yêu cầu: `POST /api/v1/auth/login` với `{username, password}`.
  * Giải thuật băm: **Argon2id** (đạt giải Password Hashing Competition, chống tấn công từ điển và GPU acceleration).
  * Phản hồi phiên: Cấp `access_token` JWT ký bằng thuật toán HMAC-SHA256.
* **Cơ chế an ninh tăng cường:**
  * Thiết lập Cookie an toàn: `HttpOnly=True` (chống XSS đánh cắp token), `Secure=False` (lab) / `True` (prod), `SameSite="Lax"` (chống tấn công CSRF).
  * Thời hạn phiên: 15 phút cho API Bearer token, làm mới qua quy trình kiểm soát.
  * Hạn chế rủi ro: Khóa tạm tài khoản 15 phút sau 5 lần nhập sai mật khẩu liên tiếp; Rate Limiting theo địa chỉ IP.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Đi vào luồng nghiệp vụ đầu tiên là **Xác thực phụ huynh**. Vì phụ huynh là người nắm toàn quyền quyết định chính sách trên máy tính của con, cổng xác thực phải là pháo đài bảo mật vững chắc nhất.  
>  
> Hệ thống áp dụng thuật toán băm mật khẩu **Argon2id**. Khi phụ huynh đăng nhập, máy chủ xác minh và trả về JWT token được đặt trong Cookie với cờ `HttpOnly` và `SameSite=Lax`. Điều này đảm bảo các đoạn mã JavaScript độc hại trên trình duyệt không bao giờ có thể đọc được token, triệt tiêu nguy cơ tấn công XSS và giảm thiểu rủi ro CSRF. Hơn nữa, hệ thống có cơ chế giới hạn tần suất truy vấn để chống lại các đợt tấn công dò mật khẩu tự động."*

---

## SLIDE 8: LUỒNG NGHIỆP VỤ 2 — GHÉP ĐÔI THIẾT BỊ AN TOÀN (ENROLLMENT)
### 1. Nội dung hiển thị trên Slide
* **Mục tiêu:** Xác lập quyền giám hộ hợp pháp của cha mẹ trên thiết bị con theo Nghị định 13/2023.
* **Quy trình 5 bước khép kín:**
  1. Phụ huynh truy cập Dashboard, nhấn *'+ Thêm thiết bị mới'* ➜ Gọi API `POST /api/v1/enroll/create-code`.
  2. Máy chủ sinh mã ghép đôi gồm **8 ký tự an toàn** (loại bỏ ký tự dễ nhầm lẫn như 0/O, 1/I, L) kèm thời hạn sống đúng **10 phút** (600 giây).
  3. Phụ huynh khởi chạy Agent trên máy tính trẻ và nhập mã 8 ký tự.
  4. Agent thu thập mã định danh phần cứng (`device_fingerprint` UUID) và gửi tới `POST /api/v1/enroll/claim`.
  5. Server kiểm tra tính hợp lệ: Nếu mã còn hạn và chưa dùng (`is_used=False`), server gán thiết bị cho tài khoản cha mẹ, đánh dấu mã đã dùng, và cấp cặp khóa `access_token` (15 phút) & `refresh_token` (30 ngày).
* **Lưu trữ cục bộ:** Agent lưu credentials vào SQLite cục bộ `agent_cache.db` và bật icon thông báo.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Luồng nghiệp vụ thứ hai là **Quy trình ghép đôi thiết bị không dây (Enrollment)**. Đây chính là điểm chạm kỹ thuật thể hiện sự đồng thuận của cha mẹ theo Nghị định 13/2023:  
>  
> Khi phụ huynh muốn thêm máy tính của con, họ bấm nút trên Dashboard. Máy chủ sẽ sinh một mã gồm 8 ký tự được chọn lọc từ bảng ký tự an toàn, loại bỏ triệt để các ký tự dễ gây nhầm lẫn như số 0 và chữ O, số 1 và chữ I. Mã này chỉ có hiệu lực trong 10 phút.  
>  
> Phụ huynh cầm mã này nhập vào giao diện Agent trên máy của con. Agent sẽ lấy UUID phần cứng của bo mạch chủ tạo thành dấu vân tay thiết bị, gửi lên máy chủ kèm mã ghép đôi. Máy chủ xác minh, liên kết thiết bị với cha mẹ, vô hiệu hóa mã ngay lập tức để chống sử dụng lại, và cấp cặp Token cho Agent. Agent lưu Token vào SQLite cục bộ trên máy con để duy trì kết nối."*

---

## SLIDE 9: LUỒNG NGHIỆP VỤ 3 — VIỄN TRẮC NHỊP TIM & TRẠNG THÁI (HEARTBEAT)
### 1. Nội dung hiển thị trên Slide
* **Chu kỳ nhịp tim viễn trắc (Heartbeat Loop):**
  * Tần suất gửi: Định kỳ **60 giây/lần** qua API `POST /api/v1/heartbeat`.
  * Xác thực yêu cầu: Header `Authorization: Bearer <access_token>` (kèm fallback `device_fingerprint`).
* **Tải trọng tối thiểu (Tuân thủ NT2):**
  * Chỉ truyền: Dấu vân tay thiết bị, trạng thái tác tử (`agent_status: running`), phiên bản giao thức (`protocol_version: 1`).
  * Tuyệt đối không truyền lịch sử phím bấm, ảnh chụp hay nội dung duyệt web.
* **Cơ chế nhận diện Online/Offline phía Server & Dashboard:**
  * Máy chủ cập nhật trường `last_seen` và ghi log vào bảng `heartbeat_logs`.
  * **Thuật toán Online:** Thiết bị được xem là **Online** nếu `now - last_seen < 120 giây` (khoảng dự phòng gấp đôi chu kỳ nhịp tim phòng trường hợp gián đoạn mạng ngắn hạn). Nếu vượt quá 120 giây, thiết bị tự động chuyển sang nhãn **Offline**.
* **Đồng bộ thời gian & Chính sách:** Phản hồi nhịp tim trả về `server_time` (đối chiếu chống lùi giờ) và `policy_version` (báo hiệu cần kéo chính sách mới).

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Sau khi ghép đôi thành công, Agent bắt đầu chu trình duy trì sự sống: **Giao thức Nhịp tim định kỳ (Heartbeat)** mỗi 60 giây.  
>  
> Nhóm chúng em thiết kế gói tin nhịp tim theo đúng tinh thần tối thiểu dữ liệu NT2: nó chỉ mang trạng thái hoạt động của tác tử và dấu thời gian. Máy chủ nhận gói tin, cập nhật dấu thời gian `last_seen` vào CSDL.  
>  
> Trên Dashboard của phụ huynh, chúng em áp dụng thuật toán ngưỡng: nếu máy chủ nhận được nhịp tim trong vòng dưới 120 giây, thiết bị hiển thị thẻ xanh 'Online'. Nếu quá 120 giây không có tín hiệu, hệ thống đánh dấu ngay là 'Offline'. Đồng thời, trong phản hồi nhịp tim, máy chủ gửi ngược lại thời gian chuẩn của máy chủ và phiên bản chính sách mới nhất, giúp Agent kịp thời cập nhật luật mà không cần duy trì kết nối liên tục gây tốn pin hay băng thông."*

---

## SLIDE 10: KẾT QUẢ ĐÃ ĐẠT ĐƯỢC (MILESTONE TUẦN 1 / v0.1 REVIEW)
### 1. Nội dung hiển thị trên Slide
* **Tổng kết nghiệm thu Giai đoạn 1 (Version 0.1):**
  * **46/46 Micro-tasks** đã hoàn thành 100% thuộc 7 Phase kỹ thuật.
  * **15/15 Unit & Integration Tests đạt 100% PASSED** (Thời gian chạy: 3.63s).
    * `test_auth.py` (5/5): Argon2id hash/verify, JWT token tamper protection, login flow.
    * `test_enrollment.py` (6/6): Sinh mã an toàn, quyền truy cập, ghép đôi thành công, chống dùng lại mã cũ, chống mã hết hạn.
    * `test_heartbeat.py` (4/4): Bearer token heartbeat, fingerprint fallback, từ chối máy lạ, tính toán ngưỡng Online/Offline 120s.
* **Sản phẩm chạy thực tế (E2E Delivered):**
  * Khởi chạy thành công Máy chủ FastAPI (`http://127.0.0.1:8000`), Seed tài khoản mẫu `parent_admin`.
  * Web Dashboard phụ huynh hoàn thiện: Đăng nhập Cookie, Modal tạo mã 8 ký tự kèm đồng hồ đếm ngược 10:00, thẻ thiết bị thời gian thực.
  * Tác tử Agent Windows: Nhận diện UUID, ghép đôi lưu `agent_cache.db`, xuất hiện System Tray Icon và bật thông báo Windows chào em (NT1).
  * Bộ tài liệu kỹ thuật hoàn thiện: `KienTrucHeThong.md`, `PRIVACY.md` (Bảng kê khai 9 trường dữ liệu theo NĐ 13/2023), `VERIFY_WEEK1.md`.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Kính thưa Thầy Cô, sau giai đoạn triển khai vừa qua, nhóm chúng em đã **hoàn thành 100% mục tiêu của Phiên bản 1 (v0.1) với đầy đủ 46 Micro-tasks**.  
>  
> Toàn bộ 15 kịch bản kiểm thử tự động trên Pytest đều đạt trạng thái PASSED tuyệt đối, từ kiểm tra thuật toán Argon2id, chữ ký chống giả mạo token, logic tự hủy mã ghép đôi, cho đến kiểm chứng ngưỡng thời gian Online/Offline.  
>  
> Chúng em đã tiến hành nghiệm thu khép vòng đầu–cuối thực tế: Phụ huynh đăng nhập trên Web, tạo mã 8 ký tự với đồng hồ đếm ngược; Agent trên máy tính Windows nhập mã, kết nối thành công, biểu tượng lá chắn khay hệ thống lập tức xuất hiện kèm thông báo Windows chào đón em, và Dashboard tức thì cập nhật trạng thái Online theo thời gian thực."*

---

## SLIDE 11: THIẾT KẾ CHI TIẾT: QUẢN LÝ THỜI GIAN (F1) & CHỐNG TUA GIỜ
### 1. Nội dung hiển thị trên Slide
* **Bộ quy tắc Quản lý Thời gian (Feature 1):**
  * Hạn mức sử dụng màn hình (Daily Quota): Cấu hình độc lập cho Ngày thường (vd: 90 phút) và Cuối tuần (vd: 150 phút).
  * Ma trận Lịch tuần 7×48: Chia tuần thành các khối 30 phút cho phép hoặc cấm máy tính hoạt động.
* **Cơ chế Đo đếm & Chống Gian lận Thời gian (Mục M6 Kỹ thuật mạng):**
  * **Vấn đề:** Trẻ có thể chỉnh lùi đồng hồ hệ thống của Windows (System Clock) để kéo dài giờ chơi.
  * **Giải pháp kỹ thuật của OGK:**
    * Sử dụng đồng hồ đơn điệu **`time.monotonic()`**: Chỉ đếm khoảng cách thời gian vật lý thực tế trôi qua của CPU, hoàn toàn không bị ảnh hưởng khi trẻ can thiệp vào giờ hệ thống.
    * Đối chiếu `server_time` tại mỗi gói tin nhịp tim. Nếu phát hiện chênh lệch > 5 phút ➜ Ghi nhật ký cảnh báo gian lận giờ.
  * **Phát hiện máy rảnh (Idle Detection):** Gọi Win32 API `GetLastInputInfo`. Nếu không có thao tác bàn phím/chuột > 5 phút ➜ Tạm dừng tính quota (công bằng cho trẻ).
* **Cơ chế Khóa máy Nhân văn (NT4):**
  * Cảnh báo âm thanh và popup trước 10 phút, 5 phút, 1 phút.
  * Ân hạn 60 giây cuối cùng để trẻ kịp lưu bài vở.
  * Thực thi khóa bằng API gốc Windows `user32.LockWorkStation()` (nhẹ nhàng, không làm mất dữ liệu của ứng dụng).

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Tiếp theo, em xin trình bày về module **Quản lý thời gian (F1)**. Đây là tính năng cốt lõi giúp điều hòa thói quen của trẻ.  
>  
> Một thách thức kinh điển đối với các kỹ sư hệ thống là: Trẻ em rất thông minh, các em có thể vào Control Panel chỉnh lùi đồng hồ Windows lại vài tiếng để tiếp tục chơi. Nếu phần mềm sử dụng hàm lấy giờ thông thường `time.time()`, hệ thống sẽ bị đánh lừa ngay lập tức.  
>  
> Nhóm chúng em giải quyết triệt để bài toán này bằng cách sử dụng **Đồng hồ đơn điệu `time.monotonic()`**. Đồng hồ này đo xung nhịp trực tiếp từ phần cứng CPU, chỉ tăng tịnh tiến theo thời gian vật lý và không bao giờ bị ảnh hưởng bởi việc đổi giờ hệ thống. Kết hợp với API `GetLastInputInfo` để không trừ giờ oan khi trẻ rời bàn học, và Win32 `LockWorkStation` để khóa máy an toàn sau khi đã cho trẻ 60 giây ân hạn để lưu bài."*

---

## SLIDE 12: THIẾT KẾ CHI TIẾT: LỌC MẠNG TẦNG DNS (F2) & KIỂM SOÁT APP
### 1. Nội dung hiển thị trên Slide
* **Bộ lọc Mạng Tầng DNS Proxy Cục bộ (DNS Sinkhole):**
  * Agent khởi tạo UDP Socket lắng nghe tại `127.0.0.1:53`.
  * Trỏ DNS máy tính về Localhost: Mọi truy vấn tên miền của trình duyệt đều đi qua Proxy của OGK.
  * Cơ chế xử lý:
    * *Tên miền thuộc danh sách cấm / danh mục nguy hại:* Proxy lập tức trả về IP Loopback `0.0.0.0` (Sinkhole), ngăn chặn triệt để kết nối trước khi gói tin HTTP/HTTPS được thiết lập.
    * *Cưỡng chế SafeSearch:* Tự động viết lại (Rewrite) bản ghi DNS của Google (`forcesafesearch.google.com`), Bing, YouTube sang địa chỉ IP lọc sạch nội dung người lớn.
    * *Tên miền hợp lệ:* Chuyển tiếp (Forward) truy vấn lên Upstream DNS an toàn (Cloudflare Family `1.1.1.3` hoặc Google `8.8.8.8`).
* **Kiểm soát Ứng dụng theo Mã băm SHA-256 (Process Controller):**
  * Quét các tiến trình đang thực thi bằng `psutil`.
  * **Giải pháp chống đổi tên tệp thực thi:** Không chỉ lọc theo tên file `.exe`, Agent tính toán mã băm **SHA-256** của tệp nhị phân trên đĩa. Kể cả khi trẻ đổi tên `game.exe` thành `notepad.exe` hay `word.exe`, mã băm không đổi và tiến trình vẫn bị chặn tức thì.
  * Khi chặn: Gọi `process.terminate()` và hiển thị cửa sổ thông báo lý do rõ ràng (NT4).

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Về khía cạnh Kỹ thuật Mạng, tính năng **Lọc mạng tầng DNS (F2)** là trọng tâm đánh giá của đồ án.  
>  
> Thay vì can thiệp thô bạo vào gói tin HTTPS bằng kỹ thuật giải mã TLS MITM (vừa vi phạm quyền riêng tư nghiêm trọng, vừa dễ gây lỗi chứng chỉ trình duyệt), chúng em lựa chọn giải pháp **DNS Proxy cục bộ lắng nghe tại địa chỉ 127.0.0.1 cổng 53**. Mọi yêu cầu phân giải tên miền từ máy con đều được Agent thẩm định. Nếu tên miền nằm trong danh sách cấm, Proxy thực hiện DNS Sinkholing, trả về ngay địa chỉ `0.0.0.0`. Đồng thời, Proxy tự động rewrite các bản ghi tìm kiếm sang VIP SafeSearch để chặn nội dung nhạy cảm ngay trên công cụ tìm kiếm.  
>  
> Đối với ứng dụng trên máy, chúng em sử dụng kỹ thuật đối chiếu mã băm **SHA-256** của tệp thực thi. Điều này ngăn chặn hoàn toàn mẹo qua mặt phổ biến của trẻ là đổi tên game thành tên phần mềm học tập."*

---

## SLIDE 13: THIẾT KẾ CHI TIẾT: MINH BẠCH HAI CHIỀU (F3) & LỆNH KHẨN (F4)
### 1. Nội dung hiển thị trên Slide
* **Lược đồ Sự kiện Tối thiểu (F3 Minimal Event Schema):**
  * Cấu trúc một bản ghi sự kiện:  
    `{ timestamp, device_id, child_id, event_type, subject, duration_sec, policy_id }`
  * `subject` chỉ lưu tên ứng dụng (vd: `mspaint.exe`) hoặc Tên miền cấp hai (vd: `wikipedia.org`), tuyệt đối không lưu đường dẫn đầy đủ hay query parameters.
  * Hỗ trợ lưu đệm ngoại tuyến (Offline SQLite cache) và đồng bộ theo lô có khóa chống trùng lặp (`idempotency_key`).
* **Giao diện Minh bạch Hai chiều (NT5):**
  * Dashboard phụ huynh: Biểu đồ thời lượng học tập/giải trí, Top 10 ứng dụng, Top 10 website, nhật ký các lần chặn.
  * Màn hình riêng cho trẻ: *"Hôm nay em đã dùng gì"* với đồ họa trực quan, sinh động.
  * Kênh đối thoại: Trẻ có nút bấm gửi yêu cầu *"Xin thêm giờ"* hoặc *"Báo chặn nhầm"* trực tiếp về máy cha mẹ (NT3).
* **Kênh Lệnh Khẩn cấp qua WebSocket (Feature 4):**
  * Duy trì kết nối WebSocket song công thời gian thực giữa Server và Agent (`/ws/device/{device_id}`).
  * Thực thi các mệnh lệnh tức thời với **độ trễ dưới 5 giây**: *"Khóa máy ngay lập tức"*, *"Mở khóa"*, *"Cộng thêm 15 phút"*.
  * Chính sách cập nhật kèm chữ ký xác thực toàn vẹn **HMAC-SHA256**.
  * Bảng **Audit Log** lưu vết: Ai sửa đổi, thời gian nào, giá trị cũ và mới (trẻ được quyền xem).

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Tính năng **F3 và F4** thể hiện sâu sắc tính nhân văn và công nghệ thời gian thực của đồ án.  
>  
> Chúng em xây dựng màn hình giao diện riêng cho trẻ mang tên 'Hôm nay em đã dùng gì'. Em có thể thấy chính xác những gì cha mẹ thấy, từ thời gian dùng máy đến các app đã mở. Khi cần thêm thời gian để làm bài tập nhóm, em chỉ cần bấm nút 'Xin thêm giờ', yêu cầu sẽ được chuyển tức thì lên Dashboard của cha mẹ.  
>  
> Về mặt công nghệ đồng bộ từ xa F4, bên cạnh chu kỳ nhịp tim 60 giây, chúng em thiết lập kênh **WebSocket song công**. Khi cha mẹ nhấn nút 'Khóa máy ngay' hoặc 'Cộng 15 phút', lệnh được đẩy thẳng xuống máy của con với độ trễ dưới 5 giây. Mọi chính sách gửi đi đều có chữ ký toàn vẹn HMAC để chống can thiệp trên đường truyền, và mọi thay đổi đều được ghi vào Audit Log minh bạch."*

---

## SLIDE 14: BÁO CÁO KỸ THUẬT MẠNG: LUỒNG DNS & SO SÁNH PHƯƠNG ÁN (M1, M2)
### 1. Nội dung hiển thị trên Slide
* **M1 – Sơ đồ Luồng Gói tin DNS (DNS Packet Flow):**
  * Trình duyệt máy con truy cập `bad-site.com` ➜ Gọi hàm `getaddrinfo` của Windows Stub Resolver.
  * Gói tin DNS Query (UDP Port 53) chuyển hướng về `127.0.0.1:53` (OGK Proxy).
  * Proxy tra cứu Blocklist:
    * Nếu CẤM ➜ Tạo gói DNS Response giả lập với `Answer: A 0.0.0.0`, trả về trong 1ms (Kiểm chứng bằng Wireshark).
    * Nếu HỢP LỆ ➜ Chuyển tiếp UDP Query tới DNS Server bên ngoài (`1.1.1.3`), nhận kết quả và trả về cho trình duyệt.
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
> *"Thưa Thầy Cô, mục **M1 và M2** trong Báo cáo Kỹ thuật Mạng là nội dung nhóm đã dành nhiều tâm huyết nghiên cứu.  
>  
> Để lựa chọn phương án chặn mạng, chúng em đã lập bảng so sánh chi tiết giữa 4 công nghệ: Tệp hosts, DNS Proxy, HTTP Proxy và WFP driver.  
> - Tệp hosts thì quá thô sơ, không hỗ trợ wildcard subdomain và rất dễ bị xung đột quyền ghi.  
> - HTTP Proxy thì đòi hỏi phải cài đặt chứng chỉ Root CA giả mạo để bẻ khóa gói tin HTTPS, điều này vi phạm nghiêm trọng nguyên tắc quyền riêng tư và tiềm ẩn lỗ hổng bảo mật cho cả hệ điều hành.  
> - WFP thì đòi hỏi viết Kernel Driver bằng C/C++, độ rủi ro gây màn hình xanh (BSOD) rất cao.  
>  
> Do đó, **DNS Proxy cục bộ là lựa chọn kỹ thuật tối ưu nhất**. Nó chặn đứng yêu cầu độc hại ngay từ giai đoạn hỏi đường trước khi bắt tay TLS, xử lý linh hoạt tên miền con với độ trễ cực thấp dưới 2 mili-giây, và kiểm chứng trực quan bằng phần mềm Wireshark."*

---

## SLIDE 15: PHÂN TÍCH 7 KỸ THUẬT VƯỢT RÀO & BIỆN PHÁP ĐỐI PHÓ (M3)
### 1. Nội dung hiển thị trên Slide
* **Bảng Đánh giá Thực nghiệm 7 Kỹ thuật Vượt rào (Bypass Analysis):**
  1. **Đổi DNS thủ công sang 8.8.8.8:** Agent chạy luồng giám sát card mạng (WMI/Netsh), tự động phát hiện và khôi phục về `127.0.0.1` hoặc gửi cảnh báo lên Dashboard.
  2. **DNS-over-HTTPS (DoH) trong trình duyệt:** 
     * Trả về `NXDOMAIN` cho tên miền Canary (`use-application-dns.net`) để tự động vô hiệu hóa DoH trên Firefox/Chrome.
     * Chặn danh sách địa chỉ IP của các DoH Endpoints phổ biến.
  3. **DNS-over-TLS (DoT):** Chặn lưu lượng cổng TCP 853 thông qua cấu hình tường lửa Windows Firewall.
  4. **Sử dụng VPN / Proxy công cộng:** Quét tiến trình các phần mềm VPN phổ biến (OpenVPN, 1.1.1.1 Warp, ProtonVPN) và chặn theo mã băm SHA-256.
  5. **Truy cập trực tiếp bằng địa chỉ IP (Bypass DNS):** Phân tích rõ giới hạn; đa số website hiện đại dùng SNI/Shared Host nên không thể duyệt web chỉ bằng IP; đối phó bằng danh sách đen IP độc hại.
  6. **Khởi động vào Safe Mode:** Agent ghi nhận khoảng trống mất nhịp tim (`heartbeat gap`), khi máy khởi động lại bình thường sẽ đánh dấu cảnh báo trên Dashboard.
  7. **Tắt tiến trình Agent trong Task Manager:** Cấu hình Windows Service Recovery tự khởi động lại tiến trình sau 5 giây; Server phát hiện mất nhịp tim sau 120 giây và thông báo cho cha mẹ.
* **Thái độ kỹ thuật trung thực:** Thừa nhận giới hạn khách quan (ví dụ: trẻ tháo ổ cứng hoặc boot từ USB ngoài nếu không khóa BIOS), giải thích rõ trong báo cáo.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Trong báo cáo kỹ thuật mạng **Mục M3**, chúng em tiến hành phân tích thực nghiệm 7 kịch bản vượt rào mà một đứa trẻ am hiểu công nghệ có thể thử nghiệm:  
>  
> - Nếu trẻ cố tình đổi DNS card mạng sang Google 8.8.8.8, Agent sẽ định kỳ kiểm tra và tự khôi phục lại cấu hình 127.0.0.1.  
> - Nếu trẻ bật tính năng mã hóa DNS-over-HTTPS (DoH) trong trình duyệt để lách qua proxy, Agent sẽ trả về mã lỗi NXDOMAIN cho tên miền Canary `use-application-dns.net`. Đây là chuẩn công nghiệp giúp báo hiệu cho trình duyệt tự tắt DoH và quay về DNS hệ thống.  
> - Nếu trẻ cài các phần mềm VPN hoặc Fake IP, Agent nhận diện tiến trình bằng mã băm SHA-256 và chặn khởi chạy.  
> - Nếu trẻ mở Task Manager tìm cách tắt Agent, dịch vụ Windows Service Recovery sẽ tự động hồi sinh tiến trình trong vòng 5 giây. Nếu bị tắt vĩnh viễn, máy chủ sẽ kích hoạt cảnh báo mất nhịp tim tới điện thoại của cha mẹ sau 2 phút.  
> Chúng em cũng trung thực thừa nhận các giới hạn vật lý như việc khởi động máy từ USB nếu không đặt mật khẩu BIOS, và đã nêu rõ các khuyến nghị bảo vệ trong tài liệu."*

---

## SLIDE 16: AN TOÀN THÔNG TIN CHIỀU SÂU & MÔ HÌNH ĐE DỌA STRIDE (F5)
### 1. Nội dung hiển thị trên Slide
* **Mô hình Đe dọa STRIDE (8 Mối đe dọa trọng yếu):**
  * *Spoofing (Giả mạo):* Giả mạo thiết bị con ➜ Ngăn chặn bằng Token ký HMAC và UUID phần cứng.
  * *Tampering (Can thiệp dữ liệu):* Sửa gói tin chính sách ➜ Chữ ký HMAC kèm phiên bản policy.
  * *Repudiation (Chối bỏ):* Phụ huynh từ chối hành động ➜ Bảng Audit Log lưu IP, dấu thời gian và giá trị cũ/mới.
  * *Information Disclosure (Lộ dữ liệu):* Lộ lịch sử web ➜ Áp dụng NT2, không lưu URL đầy đủ, mã hóa AES-GCM các cấu hình nhạy cảm.
  * *Denial of Service (Từ chối dịch vụ):* Spam nhịp tim hoặc login ➜ Rate limiting theo IP, SQLite WAL chống khóa DB.
  * *Elevation of Privilege (Leo thang đặc quyền):* Trẻ dùng API đổi luật ➜ Xác thực phân quyền 3 vai trò (`parent`, `child-view`, `admin`).
* **Hai Kịch bản Đặc thù Bắt buộc:**
  * **Kịch bản 1: Chính trẻ là người tấn công:** Tự bảo vệ cục bộ bằng phân quyền thư mục ACL chỉ cấp quyền SYSTEM/Administrators ghi, trẻ dùng tài khoản Standard User.
  * **Kịch bản 2: Sản phẩm bị lạm dụng làm phần mềm theo dõi lén người lớn (Stalkerware):** Khắc phục bằng cơ chế NT1 (luôn hiện biểu tượng, thông báo khi mở máy), không có chế độ chạy ẩn, tự tắt nếu mất giao diện khay hệ thống.
* **Tuân thủ Quyền riêng tư (Nghị định 13/2023):**
  * Tự động xóa nhật ký sau 90 ngày (Cron job định kỳ).
  * Chức năng *"Xóa toàn bộ dữ liệu của con tôi"* hoạt động triệt để, xóa tức thì trên cả Server và Agent.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Về mặt An toàn thông tin F5, hệ thống được thẩm định kỹ lưỡng bằng **Mô hình đe dọa STRIDE**. Trong đó, chúng em đặc biệt tập trung giải quyết 2 kịch bản rủi ro đặc thù:  
>  
> Thứ nhất, **kịch bản chính trẻ em là tác nhân tấn công**: Trẻ cố tình leo thang đặc quyền để sửa đổi tệp cấu hình cục bộ. Giải pháp là thiết lập quyền ACL thư mục ProgramData chỉ cho phép tài khoản SYSTEM và Administrators được ghi, tài khoản của trẻ chỉ là Standard User.  
>  
> Thứ hai, **nguy cơ sản phẩm bị kẻ xấu lạm dụng làm công cụ theo dõi lén người lớn (Stalkerware)**: Nhóm triệt tiêu rủi ro này bằng cách thiết kế Agent không thể chạy ẩn. Nếu ai đó cố tình giấu biểu tượng hoặc tắt thông báo khay hệ thống, Agent sẽ từ chối hoạt động.  
>  
> Ngoài ra, để bảo vệ quyền riêng tư, hệ thống áp dụng cơ chế tự động dọn dẹp dữ liệu định kỳ 90 ngày và cung cấp nút xóa toàn bộ dữ liệu chỉ với một thao tác."*

---

## SLIDE 17: KẾ HOẠCH TRIỂN KHAI 4 TUẦN & LỘ TRÌNH DỰ ÁN
### 1. Nội dung hiển thị trên Slide
* **Lộ trình 4 Phiên bản (4 Versions Roadmap):**
  * **TUẦN 1 (v0.1) — THE BACKBONE:** *(ĐÃ HOÀN THÀNH 100%)*
    * Khung 3 phân hệ Client – Server – Web Dashboard.
    * Xác thực Argon2id, ghép đôi không dây 8 ký tự, nhịp tim định kỳ 60 giây.
    * 46 micro-tasks hoàn tất, 15/15 tests pass.
  * **TUẦN 2 (v0.2) — TIME GOVERNANCE:** *(Kế hoạch tiếp theo)*
    * Quản lý Quota ngày thường / cuối tuần, ma trận lịch tuần 7×48.
    * Bộ đếm `time.monotonic()` chống tua giờ, Idle detection, gọi Win32 LockWorkStation.
    * Kênh WebSocket đẩy lệnh khẩn cấp dưới 5 giây.
  * **TUẦN 3 (v0.3) — DEEP NETWORK FILTERING:**
    * Lắng nghe DNS Proxy cục bộ `127.0.0.1:53`, sinkholing tên miền cấm, SafeSearch.
    * Kiểm soát ứng dụng theo mã băm SHA-256.
    * Đệm sự kiện ngoại tuyến, màn hình minh bạch 2 chiều *"Hôm nay em đã dùng gì"*, nút xin thêm giờ.
  * **TUẦN 4 (v0.4) — SECURITY HARDENING & PACKAGING:**
    * Gia cố F5 (AES-GCM, Anti-IDOR, Auto-delete 90 ngày).
    * Đo đạc thực nghiệm hiệu năng M4 (>= 30 mẫu CPU/RAM/DNS latency p50, p95).
    * Bộ kiểm thử đầy đủ 15 unit tests + 5 integration tests.
    * Đóng gói bộ sản phẩm: Báo cáo chính 20-30 trang, Phụ lục M1-M6, Video demo 5-7 phút, README cài đặt sạch trong 15 phút.

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Thưa Thầy Cô, đồ án của chúng em được lập kế hoạch chặt chẽ trong vòng 4 tuần theo phương pháp Spec-Driven Development:  
>  
> - **Tuần 1** vừa qua là giai đoạn xây dựng bộ khung xương sống kết nối (The Backbone), và chúng em đã hoàn thành 100% mục tiêu đề ra.  
> - Bước sang **Tuần 2**, chúng em sẽ hiện thực hóa tính năng quản trị thời gian F1, hoàn thiện bộ đếm Monotonic chống tua giờ và kênh WebSocket điều khiển tức thời.  
> - Sang **Tuần 3**, trọng tâm sẽ là bộ lọc DNS Proxy 127.0.0.1:53, cưỡng chế SafeSearch, chặn app theo mã băm SHA-256 và màn hình minh bạch cho trẻ.  
> - Và ở **Tuần 4**, nhóm sẽ hoàn tất việc gia cố bảo mật, thực hiện bài đo hiệu năng với 30 mẫu số liệu thực tế, đóng gói toàn bộ mã nguồn, tài liệu báo cáo và video demo."*

---

## SLIDE 18: KẾT LUẬN & PHIÊN VẤN ĐÁP PHẢN BIỆN (Q&A DEFENSE)
### 1. Nội dung hiển thị trên Slide
* **Tổng kết giá trị đồ án:**
  * Giải quyết hài hòa bài toán quản lý kỹ thuật mạng máy tính và tôn trọng đạo đức, pháp luật bảo vệ trẻ em.
  * Kiến trúc tối giản, tường minh, mã nguồn độc lập, tự chủ hoàn toàn trên môi trường nội bộ gia đình.
  * Nền tảng vững chắc đã được kiểm chứng bằng thực nghiệm và kiểm thử tự động 100%.
* **Sẵn sàng cho phiên Vấn đáp & Trả lời Phản biện (Q&A):**
  * Trân trọng cảm ơn quý Thầy/Cô trong Hội đồng và các bạn đã chú ý lắng nghe!

---

### 2. Lời thoại thuyết trình (Speaker Script)
> *"Tóm lại, dự án **Open Guardian Kids** không chỉ là một bài tập lớn về kỹ thuật mạng và lập trình hệ thống, mà còn là một minh chứng thực tế cho thấy: **Công nghệ hoàn toàn có thể giúp bảo vệ con trẻ một cách an toàn mà không cần phải xâm phạm bí mật đời tư hay phá vỡ sự tôn trọng trong gia đình**.  
>  
> Với nền móng vững chắc của Tuần 1 đã hoàn thành trọn vẹn, chúng em hoàn toàn tự tin sẽ hoàn thành xuất sắc các mục tiêu còn lại của đồ án đúng thời hạn.  
>  
> Chúng em xin chân thành cảm ơn quý Thầy Cô trong Hội đồng đã lắng nghe bài báo cáo. Sau đây, nhóm chúng em rất mong nhận được những nhận xét quý báu và xin sẵn sàng trả lời các câu hỏi phản biện của Thầy Cô!"*

---

# PHỤ LỤC: BỘ CÂU HỎI PHẢN BIỆN DỰ KIẾN TỪ HỘI ĐỒNG & CÂU TRẢ LỜI CHUẨN XÁC

### Câu hỏi 1: *"Tại sao nhóm lại dùng DNS Proxy cục bộ mà không dùng tệp hosts của Windows cho đơn giản, hoặc dùng HTTP Proxy để lọc sâu nội dung?"*
* **Trả lời phản biện:**  
  *"Thưa Thầy Cô, nhóm đã cân nhắc rất kỹ lưỡng 4 phương án trong mục M2 của báo cáo:  
  1. **Tệp hosts** tuy đơn giản nhưng có nhược điểm chí mạng: không hỗ trợ ký tự đại diện (Wildcard). Nếu muốn chặn một trang mạng xã hội lớn, tệp hosts phải liệt kê hàng ngàn tên miền con, rất dễ bị khóa tệp (file lock) khi hệ điều hành đang đọc, và trẻ có thể dùng quyền mở file ra sửa.  
  2. **HTTP Proxy** thì đòi hỏi phải thực hiện kỹ thuật giải mã TLS/SSL Man-in-the-Middle (bẻ khóa HTTPS) bằng cách cài đặt một chứng chỉ Root CA tự ký vào máy tính của trẻ. Điều này vi phạm nghiêm trọng nguyên tắc đạo đức NT2 và Nghị định 13/2023 vì có thể làm lộ mật khẩu ngân hàng, tài khoản học tập của trẻ, đồng thời làm giảm hiệu năng mạng đáng kể.  
  3. **DNS Proxy 127.0.0.1:53** giải quyết trọn vẹn bài toán: nó chặn ngay từ bước hỏi địa chỉ IP trước khi trình duyệt kết nối HTTPS, hỗ trợ wildcard linh hoạt, độ trễ chỉ dưới 2 mili-giây, và tuyệt đối tôn trọng sự riêng tư của luồng dữ liệu truyền tải."*

---

### Câu hỏi 2: *"Trên Windows có cơ chế Session 0 Isolation. Làm thế nào để Agent vừa chạy ngầm với quyền cao vừa hiển thị được khay hệ thống (Tray Icon) trong phiên của trẻ?"*
* **Trả lời phản biện:**  
  *"Thưa Thầy Cô, đây chính là một bẫy kỹ thuật kinh điển mà nhóm đã phân tích theo nguyên tắc 'Think Before Coding' của Karpathy:  
  Kể từ Windows Vista trở đi, các Windows Service chạy dưới tài khoản LocalSystem đều bị cô lập hoàn toàn trong Session 0 và không được phép tương tác trực tiếp với màn hình người dùng (Interactive Desktop) trong Session 1+.  
  Để giải quyết vấn đề này, kiến trúc của OGK phân tách làm hai tiến trình độc lập:  
  - Tiến trình lõi **OGK-Service** chạy dưới quyền hệ thống để quản lý DNS Proxy, giám sát tiến trình và đếm giờ.  
  - Tiến trình giao diện **OGK-Tray** chạy trực tiếp trong phiên người dùng (User Session) của trẻ để hiển thị Icon khay hệ thống Pystray và các cửa sổ thông báo.  
  - Hai tiến trình này liên lạc với nhau thông qua cơ chế IPC nội bộ (Named Pipe hoặc Local HTTP Loopback có mã Token xác thực), đảm bảo tuân thủ 100% mô hình bảo mật của Windows mà vẫn hiển thị được giao diện minh bạch cho trẻ."*

---

### Câu hỏi 3: *"Nếu đứa trẻ dùng trình duyệt Chrome/Firefox và bật tính năng DNS-over-HTTPS (DoH), DNS Proxy cổng 53 của nhóm sẽ bị vô hiệu hóa hoàn toàn. Nhóm xử lý thế nào?"*
* **Trả lời phản biện:**  
  *"Thưa Thầy Cô, đây chính là kỹ thuật vượt rào số 2 mà nhóm đã phân tích trong Mục M3:  
  Khi người dùng bật DoH, trình duyệt sẽ gửi gói tin DNS mã hóa qua cổng HTTPS 443 lên các máy chủ như Cloudflare hay Google, bỏ qua cổng 53 của hệ điều hành. Để đối phó, nhóm áp dụng giải pháp chuẩn công nghiệp:  
  1. Trả về mã lỗi **NXDOMAIN** cho tên miền Canary chuẩn của DoH là `use-application-dns.net`. Khi nhận được mã lỗi này, trình duyệt Firefox và Chrome sẽ tự hiểu rằng mạng nội bộ này có chính sách DNS riêng và sẽ tự động tắt tính năng DoH, quay trở về sử dụng DNS của hệ điều hành.  
  2. Đồng thời, Agent đưa các địa chỉ IP của các DoH Endpoints phổ biến (như `1.1.1.1`, `8.8.8.8`, `9.9.9.9` trên cổng 443) vào danh sách giám sát và cảnh báo cha mẹ nếu phát hiện lưu lượng DoH bất thường."*

---

### Câu hỏi 4: *"Làm thế nào để hệ thống chứng minh được là không lưu trữ lén dữ liệu của trẻ theo quy định của Nghị định 13/2023/NĐ-CP?"*
* **Trả lời phản biện:**  
  *"Thưa Thầy Cô, tính minh bạch của OGK được bảo đảm bằng 3 bằng chứng kỹ thuật cụ thể:  
  1. **Lược đồ CSDL rõ ràng:** Trong CSDL `ogk.db` và `agent_cache.db`, chúng em chỉ định nghĩa các trường lưu trữ tên tệp `.exe`, tên miền cấp hai, số giây sử dụng và dấu thời gian. Không hề có bảng hay cột nào lưu trữ URL đầy đủ, nội dung tin nhắn hay ảnh chụp màn hình.  
  2. **Tài liệu PRIVACY.md công khai:** Nhóm có bảng kê khai chi tiết 9 trường dữ liệu thu thập, mục đích sử dụng, căn cứ điều khoản của Nghị định 13/2023 và thời hạn lưu trữ.  
  3. **Cơ chế kỹ thuật thực thi:** Hệ thống có tác vụ tự động dọn dẹp dữ liệu cũ sau 90 ngày, và nút 'Xóa toàn bộ dữ liệu của con tôi' giúp phụ huynh và trẻ có thể xóa sạch mọi vết tích trên cả máy chủ và máy con bất cứ lúc nào."*

---

### Câu hỏi 5: *"Đồ án này gồm 2 sinh viên thực hiện, sự phân công nhiệm vụ và tỷ lệ đóng góp cụ thể ra sao?"*
* **Trả lời phản biện:**  
  *"Thưa Thầy Cô, nhóm đã phân chia công việc theo thế mạnh chuyên môn và ranh giới hệ thống:  
  - **Sinh viên 1 (Phụ trách Phân hệ Mạng & Agent Windows):** Hiện thực DNS Proxy cục bộ bằng `dnslib`, cơ chế lọc tên miền và SafeSearch, module giám sát tiến trình và tính mã băm SHA-256 bằng `psutil`, cơ chế đếm thời gian Monotonic chống tua giờ, giao diện System Tray Pystray và kịch bản phân tích 7 đường vòng M1–M6.  
  - **Sinh viên 2 (Phụ trách Phân hệ Máy chủ & Dashboard):** Hiện thực API Server bằng FastAPI, mô hình dữ liệu SQLite WAL, thuật toán băm Argon2id và JWT token, quy trình sinh và xác thực mã ghép đôi 8 ký tự, giao diện Web Dashboard responsive cho phụ huynh, kênh WebSocket đẩy lệnh khẩn cấp dưới 5 giây, và bộ kiểm thử tự động Pytest.  
  - **Tỷ lệ đóng góp:** Hai thành viên phối hợp chặt chẽ, hỗ trợ kiểm thử chéo và đóng góp đồng đều **50% – 50%** vào toàn bộ đồ án."*
