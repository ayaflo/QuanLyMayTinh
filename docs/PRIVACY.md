# CAM KẾT BẢO VỆ DỮ LIỆU CÁ NHÂN & QUYỀN RIÊNG TƯ (PRIVACY & ETHICS POLICY)
## DỰ ÁN: OPEN GUARDIAN KIDS (OGK) — PHIÊN BẢN 0.4 (FINAL RELEASE)

> **Căn cứ pháp lý & Chuẩn mực đạo đức:**  
> - **Nghị định số 13/2023/NĐ-CP** của Chính phủ về Bảo vệ dữ liệu cá nhân (đặc biệt là **Điều 20: Xử lý dữ liệu cá nhân của trẻ em**).  
> - **Luật Trẻ em năm 2016** (**Điều 21:** Quyền bí mật đời sống riêng tư; **Điều 54:** Trách nhiệm bảo vệ trẻ em trên môi trường mạng).  
> - **Luật An toàn thông tin mạng năm 2015**.  
> - **Nguyên tắc đạo đức công nghệ (Karpathy Governance & Ethical AI):** Tôn trọng nhân phẩm và quyền tự chủ của trẻ em; không biến giải pháp giáo dục thành công cụ giám sát độc hại.  
>  
> **Tuyên ngôn triết lý cốt lõi:**  
> *"Open Guardian Kids là phần mềm đồng hành giáo dục giữa cha mẹ và con cái. Chúng tôi kiên quyết KHÔNG PHẢI là phần mềm gián điệp, KHÔNG theo dõi lén lút, và KHÔNG xâm phạm thế giới riêng tư của trẻ nhỏ."*

---

## 1. HỆ THỐNG 6 NGUYÊN TẮC QUẢN TRỊ ĐẠO ĐỨC (NT1 — NT6)

Hệ thống mã nguồn OGK được xây dựng trên nền tảng 6 nguyên tắc bất biến, được kiểm chứng chặt chẽ ở mọi tầng kiến trúc:

| Mã | Tên nguyên tắc | Biểu hiện kỹ thuật bắt buộc trong mã nguồn |
| :---: | :--- | :--- |
| **NT1** | **Trẻ biết mình đang được hỗ trợ (Visible Presence)** | Biểu tượng khay hệ thống (System Tray) luôn hiện diện thường trực. Tác tử gửi thông báo Windows Notification chào đón rõ ràng ngay khi máy tính khởi động. Tuyệt đối không chạy ẩn dạng Rootkit hay Stealth Service. |
| **NT2** | **Tối thiểu hóa dữ liệu (Data Minimisation)** | Áp dụng triệt để nguyên tắc *Need-to-Know*: Chỉ thu thập 4 trường siêu dữ liệu tối thiểu. Tuyệt đối từ chối thu thập nội dung giao tiếp hoặc thông tin nhạy cảm. |
| **NT3** | **Trẻ có tiếng nói và quyền phản hồi (Child Agency)** | Cung cấp hộp thoại tương tác hai chiều: Trẻ có thể bấm nút "Xin thêm thời gian" hoặc "Yêu cầu mở trang web học tập" kèm lý do chính đáng để cha mẹ phê duyệt trên Dashboard. |
| **NT4** | **Không gián đoạn an toàn học tập (Fair Enforcement)** | Cảnh báo trước khi hết giờ (10 phút, 5 phút, 1 phút) và cấp ân hạn 60 giây để trẻ kịp lưu bài vở; tự động dừng đếm giờ khi trẻ rời máy tính (Idle Detection > 5 phút). |
| **NT5** | **Minh bạch hai chiều & Nhật ký kiểm toán (Mutual Transparency)** | Trẻ em có quyền mở giao diện xem thời gian đã dùng và quy định của cha mẹ. Mọi hành vi can thiệp của phụ huynh đều được lưu vết trong nhật ký kiểm toán (Audit Log). |
| **NT6** | **Tự chủ gia đình & Danh sách trắng bất biến (Local Sovereignty)** | Dữ liệu lưu trữ nội bộ tại gia đình (SQLite WAL), không bán hay gửi dữ liệu sang máy chủ đám mây thương mại của bên thứ ba. Danh sách trường học (`.edu.vn`) và Tổng đài Quốc gia 111 được bảo vệ miễn trừ khóa vĩnh viễn. |

---

## 2. DANH MỤC TUYỆT ĐỐI KHÔNG THU THẬP (ABSOLUTE DATA BLACKLIST)

Tuân thủ nghiêm ngặt Điều 20 Nghị định 13/2023/NĐ-CP và Điều 21 Luật Trẻ em 2016, kiến trúc phần mềm OGK **LOẠI BỎ HOÀN TOÀN TỪ THIẾT KẾ** các hành vi sau:

* ❌ **KHÔNG chụp ảnh màn hình (No Screen Capture / Screenshots):** Tác tử không tích hợp bất kỳ hàm chụp màn hình nào. Thế giới hình ảnh của trẻ được bảo vệ tuyệt đối.
* ❌ **KHÔNG ghi lại thao tác bàn phím (No Keylogger):** Không cài đặt hook bàn phím, không ghi nhận các phím bấm, mật khẩu hay nội dung tin nhắn của trẻ.
* ❌ **KHÔNG kích hoạt Camera / Microphone (No Audio/Video Surveillance):** Không bao giờ truy cập webcam hoặc ghi âm micro của máy tính.
* ❌ **KHÔNG thu thập đường dẫn URL đầy đủ (No Full URL Query Parameters):** Tuyệt đối không thu thập chuỗi URL sau dấu gạch chéo `/` (ví dụ: `https://youtube.com/watch?v=XYZ` $\rightarrow$ Hệ thống chỉ ghi nhận tên miền cấp cao `youtube.com`). Điều này ngăn chặn triệt để nguy cơ lộ từ khóa tìm kiếm nhạy cảm, mã token định danh hay sở thích cá nhân.
* ❌ **KHÔNG đọc nội dung tài liệu, tin nhắn hay email (No Content Inspection):** Không quét tệp tin cá nhân trên ổ đĩa, không đọc tin nhắn Zalo, Messenger, Discord hay hòm thư của trẻ.

---

## 3. BẢNG KÊ KHAI 4 TRƯỜNG DỮ LIỆU VIỄN TRẮC TỐI THIỂU (F3 SCHEMA)

Mọi bản ghi nhật ký hoạt động được gửi từ máy tính con lên máy chủ chỉ bao gồm đúng **4 trường thông tin kỹ thuật cơ bản** nhằm phục vụ bài toán quản lý an toàn:

| STT | Tên trường dữ liệu | Kiểu dữ liệu | Ý nghĩa kỹ thuật | Ví dụ giá trị thực tế | Căn cứ pháp lý (Nghị định 13/2023) |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **1** | `ts` | `DateTime` (UTC) | Dấu thời gian ghi nhận sự kiện theo chuẩn quốc tế ISO-8601 | `2026-10-24T06:58:00Z` | Điều 16 (Nhật ký xử lý dữ liệu) |
| **2** | `device_id` | `Integer` | Mã số định danh thiết bị máy tính con trong gia đình | `1` | Điều 20 (Nhận diện thiết bị được cha mẹ ủy quyền) |
| **3** | `type` | `String(50)` | Phân loại hành vi kỹ thuật | `app_usage`, `web_access`, `blocked_app`, `blocked_domain`, `tamper_attempt` | Khoản 1 Điều 9 (Tính chính xác và mục đích sử dụng) |
| **4** | `subject` | `String(255)` | Tên miền FQDN hoặc Tên file tiến trình nhị phân (**KHÔNG URL, KHÔNG Tiêu đề cửa sổ**) | `hcmus.edu.vn`, `Code.exe`, `Cloudflare WARP.exe` | Điểm c Khoản 1 Điều 20 (Thu thập tối thiểu) |

---

## 4. CHÍNH SÁCH LƯU TRỮ 90 NGÀY & QUYỀN YÊU CẦU XÓA TOÀN BỘ DỮ LIỆU (RIGHT TO ERASURE)

### 4.1. Chu kỳ tiêu hủy tự động sau 90 ngày (90-Day Automated Retention Purge)
- Căn cứ theo Điều 20 Nghị định 13/2023/NĐ-CP về giới hạn thời gian lưu trữ dữ liệu cá nhân của trẻ em, hệ thống OGK tích hợp cơ chế tự động dọn dẹp định kỳ ([`server/services/retention_service.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/services/retention_service.py)):
  - Toàn bộ các bản ghi `activity_events` và `heartbeat_logs` **cũ hơn 90 ngày tính từ thời điểm hiện tại sẽ tự động bị xóa vĩnh viễn** khỏi cơ sở dữ liệu.
  - Tác vụ dọn dẹp nền được khởi chạy tự động **mỗi 24 giờ một lần** trong vòng đời của máy chủ trung tâm ([`server/main.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/server/main.py)).

### 4.2. Quyền yêu cầu xóa dữ liệu của cha mẹ (Right to Erasure / "Xóa Toàn Bộ Dữ Liệu Con Tôi")
- Phụ huynh có toàn quyền yêu cầu xóa sạch toàn bộ lịch sử sử dụng máy tính của con bất kỳ lúc nào thông qua nút bấm **"🗑️ Xóa Dữ Liệu Con (NĐ 13)"** trên giao diện Web Dashboard:
  1. **Xác thực bảo vệ nghiêm ngặt:** Hệ thống bắt buộc phụ huynh nhập lại mật khẩu tài khoản để ngăn ngừa việc trẻ nghịch ngợm hoặc thao tác nhầm.
  2. **Xóa sạch đa tầng (Multi-tier Erasure):**
     - Tại máy chủ: Xóa toàn bộ sự kiện hoạt động, nhật ký nhịp tim, lịch sử xin duyệt giờ của thiết bị.
     - Tại máy khách: Máy chủ gửi lệnh qua WebSocket `purge_local_data` ra lệnh cho tác tử Client xóa sạch bộ đệm ngoại tuyến (`pending_events`, `daily_usage`, `app_rules_cache`, `dns_rules_cache`).
  3. **Lưu vết pháp lý:** Hành động xóa được ghi nhận vào `audit_logs` để phục vụ công tác thanh tra tuân thủ bảo vệ dữ liệu.

---

## 5. BẢN CAM KẾT DÀNH RIÊNG CHO TRẺ EM (CHILD-FRIENDLY PRIVACY PLEDGE)
*(Phần tài liệu được soạn thảo bằng ngôn ngữ thân thiện, ấm áp dành riêng cho các em học sinh)*

---

### GỬI NGƯỜI BẠN NHỎ ĐANG SỬ DỤNG CHIẾC MÁY TÍNH NÀY! 👋

Chào em! Khi em nhìn thấy biểu tượng chiếc khiên xanh **Open Guardian Kids** ở góc màn hình, có thể em sẽ thắc mắc: *"Phần mềm này có đang theo dõi lén mình không?"*. 

Chúng tôi muốn giải thích thật rõ ràng và chân thành với em:

1. **CHÚNG TÔI KHÔNG THEO DÕI EM:**
   - Phần mềm **HOÀN TOÀN KHÔNG BIẾT** em đang nhắn tin gì với bạn bè, không biết mật khẩu của em, và tuyệt đối **KHÔNG BAO GIỜ** chụp ảnh màn hình hay bật camera của máy tính.
   - Khi em vào mạng, phần mềm chỉ giúp ba mẹ biết em đã vào trang web học tập nào (ví dụ: `scratch.mit.edu`), chứ không đọc được nội dung chi tiết bên trong.

2. **CHÚNG TÔI Ở ĐÂY ĐỂ GIÚP EM CÂN BẰNG:**
   - Ngồi trước máy tính quá lâu sẽ làm mắt em bị mỏi và ảnh hưởng đến giấc ngủ. Phần mềm giống như chiếc đồng hồ nhắc nhở thân thiện: Khi sắp hết giờ chơi, phần mềm sẽ báo trước 10 phút và 5 phút để em kịp lưu ván game hoặc bài tập đang làm dở.
   - Nếu em đang bận làm bài tập gấp, em có thể bấm nút **"Xin thêm thời gian"** để nhắn gửi lời nhắn dễ thương đến ba mẹ.

3. **BẢO VỆ EM TRƯỚC NHỮNG ĐIỀU ĐỘC HẠI:**
   - Trên mạng có rất nhiều trang web cờ bạc, lừa đảo hoặc chứa virus nguy hiểm. Phần mềm giống như một chiếc áo giáp chắn trước cửa, tự động chặn đứng những trang web xấu để máy tính của em luôn an toàn và sạch sẽ.

4. **EM LUÔN CÓ QUYỀN ĐƯỢC BIẾT:**
   - Em có thể nhấp vào biểu tượng bất cứ lúc nào để xem hôm nay mình đã học và chơi được bao nhiêu phút. Mọi quy định đều được ba mẹ đặt ra công khai để đồng hành cùng em lớn khôn, không có bất kỳ bí mật lén lút nào cả!

> *Chúc em có những giờ học tập thật vui vẻ, sáng tạo và an toàn bên chiếc máy tính của mình!* ❤️

---

## 6. KẾT LUẬN TUÂN THỦ ĐẠO ĐỨC & PHÁP LÝ

Tài liệu này là cam kết có hiệu lực pháp lý và đạo đức cao nhất của nhóm phát triển Open Guardian Kids. Dự án kiên quyết chứng minh rằng: **Bảo vệ trẻ em trên môi trường mạng hoàn toàn có thể song hành cùng sự tôn trọng tuyệt đối quyền riêng tư và nhân phẩm của trẻ**.
