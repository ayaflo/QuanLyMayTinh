# BẢN THẢO CAM KẾT BẢO VỆ DỮ LIỆU CÁ NHÂN & QUYỀN RIÊNG TƯ (PRIVACY POLICY)
## DỰ ÁN: OPEN GUARDIAN KIDS (OGK) — PHIÊN BẢN 1 (v0.1)

> **Căn cứ pháp lý:**  
> - **Nghị định số 13/2023/NĐ-CP** ngày 17/04/2023 của Chính phủ về Bảo vệ dữ liệu cá nhân (đặc biệt là **Điều 20: Xử lý dữ liệu cá nhân của trẻ em**).  
> - **Luật Trẻ em năm 2016** (Điều 21 về Quyền bí mật đời sống riêng tư; Điều 54 về Trách nhiệm bảo vệ trẻ em trên môi trường mạng).  
> - **Luật An toàn thông tin mạng năm 2015**.  
>  
> **Tuyên ngôn:** *"Open Guardian Kids là công cụ đồng hành giữa cha mẹ và con cái, kiên quyết KHÔNG PHẢI là phần mềm theo dõi lén hay gián điệp."*

---

## 1. NGUYÊN TẮC BẢO VỆ DỮ LIỆU BẮT BUỘC (6 NGUYÊN TẮC OGK)

| Mã | Tên nguyên tắc | Biểu hiện kỹ thuật bắt buộc trong mã nguồn |
| :---: | :--- | :--- |
| **NT1** | **Trẻ biết mình đang được hỗ trợ** | Biểu tượng khay hệ thống (System Tray) luôn hiển thị thường trực khi Agent chạy. Thông báo Windows hiển thị rõ ràng khi máy tính khởi động. |
| **NT2** | **Tối thiểu dữ liệu (Data Minimisation)** | Chỉ thu thập dữ liệu kỹ thuật và siêu dữ liệu tối thiểu phục vụ quản lý thiết bị. Tuyệt đối tôn trọng quyền riêng tư nội dung của trẻ. |
| **NT3** | **Trẻ có tiếng nói** | Thiết kế tương tác có kênh phản hồi hai chiều (kênh xin thêm thời lượng, kênh báo cáo chặn nhầm sẽ tích hợp ở các tuần kế tiếp). |
| **NT4** | **Không gián đoạn an toàn học tập** | Không khóa máy đột ngột; có cơ chế cảnh báo trước để trẻ kịp lưu bài vở đang thực hiện. |
| **NT5** | **Minh bạch hai chiều & Nhật ký kiểm toán** | Trẻ em có quyền được biết cha mẹ đã thiết lập các quy tắc gì và những dữ liệu nào đang được ghi nhận. |
| **NT6** | **Tự chủ gia đình (Local Sovereignty)** | Mọi dữ liệu lưu trữ trực tiếp trên hệ thống do gia đình quản lý (Local SQLite), không gửi dữ liệu ra máy chủ bên thứ ba thương mại. |

---

## 2. DANH MỤC CẤM THU THẬP TUYỆT ĐỐI (BLACKLISTED DATA)

Tuân thủ nghiêm ngặt Điều 20 Nghị định 13/2023/NĐ-CP, hệ thống OGK **TUYỆT ĐỐI KHÔNG BAO GIỜ** thu thập, xử lý hay lưu trữ các danh mục dữ liệu sau:
* ❌ **Không chụp ảnh màn hình (No screenshots)** của máy tính trẻ.
* ❌ **Không ghi lại thao tác bàn phím (No keylogger)** dưới bất kỳ hình thức nào.
* ❌ **Không kích hoạt Webcam hoặc Microphone (No audio/video surveillance)** lén lút.
* ❌ **Không thu thập URL đầy đủ (No full URL query parameters)** nhằm tránh lộ thông tin tìm kiếm cá nhân nhạy cảm, tài khoản hoặc token trong chuỗi URL.
* ❌ **Không đọc nội dung tin nhắn, email cá nhân hoặc tài liệu riêng tư** của trẻ.

---

## 3. BẢNG ĐỐI CHIẾU TRƯỜNG DỮ LIỆU THU THẬP TRONG TUẦN 1 (VERSION 0.1)

Dưới đây là bản kê khai chi tiết toàn bộ các trường dữ liệu được lưu trữ trong cơ sở dữ liệu `ogk.db` và `agent_cache.db` ở Giai đoạn Tuần 1:

| STT | Tên trường dữ liệu | Bảng lưu trữ | Loại dữ liệu | Mục đích xử lý | Căn cứ pháp lý (NĐ 13/2023) | Thời hạn lưu trữ | Quyền xem / Truy cập |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `username` | `parents` | Dữ liệu cá nhân cơ bản | Nhận diện tài khoản phụ huynh để đăng nhập hệ thống. | Điểm a Khoản 1 Điều 20 (Được sự đồng ý của cha mẹ) | Đến khi phụ huynh xóa tài khoản. | Chỉ phụ huynh sở hữu. |
| 2 | `password_hash` | `parents` | Dữ liệu bảo mật kỹ thuật | Xác thực phiên đăng nhập an toàn (băm bằng Argon2id, không lưu mật khẩu thô). | Khoản 2 Điều 39 (Biện pháp bảo vệ kỹ thuật) | Đến khi đổi mật khẩu hoặc xóa tài khoản. | Không ai được xem (chỉ giải thuật toán verify). |
| 3 | `device_fingerprint` | `devices` | Dữ liệu kỹ thuật thiết bị | Mã UUID phần cứng máy tính dùng để liên kết thiết bị với tài khoản cha mẹ. | Khoản 1 Điều 20 (Sự đồng thuận của phụ huynh khi ghép đôi) | Duy trì theo chu kỳ ghép đôi thiết bị. | Phụ huynh xem dưới dạng mã tóm tắt. |
| 4 | `device_name` | `devices` | Tên gợi nhớ kỹ thuật | Hiển thị tên máy tính ("PC Bàn", "Laptop Con") trên giao diện cha mẹ. | Khoản 1 Điều 20 | Duy trì theo chu kỳ ghép đôi thiết bị. | Phụ huynh và trẻ. |
| 5 | `status` | `devices` | Dữ liệu trạng thái viễn trắc | Hiển thị máy tính đang "Online" hay "Offline" trên Dashboard. | Khoản 1 Điều 9 (Tính chính xác và cập nhật) | Ghi đè liên tục theo thời gian thực. | Phụ huynh và trẻ. |
| 6 | `last_seen` | `devices` | Dấu thời gian hệ thống | Ghi nhận thời điểm nhận tín hiệu nhịp tim gần nhất (phát hiện mất kết nối). | Khoản 1 Điều 20 | Ghi đè liên tục theo nhịp tim (mỗi 60s). | Phụ huynh và trẻ. |
| 7 | `code` & `expires_at` | `pairing_codes` | Mã ủy quyền tạm thời | Cấp quyền ghép đôi từ cha mẹ tới tác tử trẻ em trong phạm vi 10 phút. | Điều 20 (Quy trình xác lập sự đồng thuận phụ huynh) | Tự hủy sau 10 phút hoặc ngay sau khi sử dụng (`is_used=True`). | Phụ huynh tạo mã và nhập vào máy tính con. |
| 8 | `timestamp` | `heartbeat_logs` | Dấu thời gian hệ thống | Lưu vết lịch sử nhịp tim kiểm toán. | Điều 16 (Nhật ký xử lý dữ liệu) | Tự động dọn dẹp sau 30 ngày (Tuần 4). | Phụ huynh xem trong mục kiểm toán. |
| 9 | `status_payload` | `heartbeat_logs` | Siêu dữ liệu kỹ thuật tối thiểu | Chứa trạng thái tác tử (`agent_status: running`, `protocol_version: 1`). Tuyệt đối không chứa lịch sử duyệt web hay thao tác riêng tư. | Điều 9 & Điều 20 (Nguyên tắc thu thập tối thiểu) | Tự động dọn dẹp sau 30 ngày. | Phụ huynh xem trong mục kiểm toán. |

---

## 4. QUYỀN CỦA CHỦ THỂ DỮ LIỆU & CƠ CHẾ THỰC THI

Theo quy định tại Điều 9 và Điều 20 Nghị định 13/2023/NĐ-CP:
1. **Quyền được biết và Quyền truy cập (Right to Access):**  
   Cả phụ huynh và trẻ em đều có quyền xem toàn bộ dữ liệu đang được hệ thống ghi nhận thông qua bảng điều khiển hoặc tệp CSDL SQLite nội bộ.
2. **Quyền rút lại sự đồng ý & Xóa dữ liệu (Right to Erasure):**  
   Phụ huynh có quyền bấm "Hủy ghép đôi" hoặc xóa tài khoản bất cứ lúc nào. Khi đó toàn bộ dữ liệu thiết bị, mã ghép đôi và nhật ký viễn trắc liên quan sẽ được xóa sạch khỏi cơ sở dữ liệu (`cascade="all, delete-orphan"`).
3. **Biện pháp bảo đảm an toàn dữ liệu (Security Safeguards):**  
   - Mã hóa mật khẩu một chiều bằng Argon2id.
   - Giao thức truyền thông cục bộ với Token xác thực HMAC có thời hạn ngắn (15 phút).
   - Cơ sở dữ liệu SQLite cục bộ được bảo vệ bởi phân quyền tập tin của hệ điều hành Windows.
