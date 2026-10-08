# OGK (Open Guardian Kids) Project Constitution
<!-- Hệ thống hỗ trợ quản lý việc sử dụng máy tính của trẻ em -->

## Core Principles

### I. Triết lý Thiết kế Bắt buộc: "Đồng hành, không theo dõi lén"
Sản phẩm là công cụ hỗ trợ phụ huynh đồng hành cùng con, tuyệt đối không phải phần mềm gián điệp. Mọi quyết định thiết kế và mã nguồn phải tuân thủ 6 nguyên tắc đạo đức & pháp lý:
- **NT1 - Trẻ biết mình đang được hỗ trợ**: Tray icon luôn hiển thị rõ ràng khi Agent chạy; thông báo bật lên khi Agent khởi động; tuyệt đối không có chế độ chạy ẩn (stealth mode).
- **NT2 - Tối thiểu dữ liệu (Data Minimisation)**: Chỉ thu thập 4 siêu dữ liệu cần thiết: tên ứng dụng, tên miền cấp hai, thời lượng sử dụng, dấu thời gian. Tuyệt đối KHÔNG lưu URL đầy đủ, KHÔNG lưu tiêu đề cửa sổ, KHÔNG keylogger, KHÔNG chụp ảnh màn hình, KHÔNG đọc nội dung tin nhắn/email/tài liệu.
- **NT3 - Trẻ có tiếng nói**: Luôn cung cấp nút "Xin thêm giờ" và "Con nghĩ trang này bị chặn nhầm" trên giao diện của trẻ; mọi yêu cầu phải được chuyển đến phụ huynh để phản hồi.
- **NT4 - Mọi hành động giải thích được**: Khi chặn ứng dụng hoặc trang web, hiển thị thông báo rõ ràng: lý do chặn là gì và ai đặt ra luật đó (phụ huynh hay chính sách mặc định theo độ tuổi); không im lặng hoặc giả vờ lỗi mạng.
- **NT5 - Minh bạch hai chiều**: Trẻ được xem cùng bộ dữ liệu báo cáo mà phụ huynh thấy (qua giao diện thân thiện với trẻ) và được xem nhật ký thay đổi chính sách của phụ huynh.
- **NT6 - An toàn có ưu tiên tuyệt đối**: Danh sách miễn chặn vĩnh viễn (cổng thông tin trường học, Tổng đài bảo vệ trẻ em 111, dịch vụ cứu hộ khẩn cấp). Cơ chế khóa máy không bao giờ chặn cuộc gọi khẩn cấp của hệ điều hành.

### II. Danh mục Hành vi Nghiêm cấm (Zero-Tolerance)
1. Không đọc nội dung tin nhắn, email, tài liệu cá nhân.
2. Không sử dụng kỹ thuật ẩn tiến trình, ẩn dịch vụ, rootkit hoặc cơ chế chống gỡ cài đặt kiểu mã độc.
3. Không gửi bất kỳ dữ liệu nào tới máy chủ của bên thứ ba.
4. Không thử nghiệm trên trẻ em thật hoặc máy tính của người khác mà không có sự đồng ý bằng văn bản.

### III. Triết lý Kỹ thuật Karpathy (The Karpathy Guidelines)
1. **Think Before Coding**: Không đoán mò. Xác định rõ ràng các giả định, đánh giá rủi ro hệ thống (Windows Session 0 Isolation, DNS port 53 conflict, time drift).
2. **Simplicity First**: Cung cấp lượng mã tối thiểu để giải quyết trọn vẹn yêu cầu. Không tạo cấu trúc trừu tượng rườm rà, không vẽ tính năng ngoài đặc tả của giáo viên (YAGNI). Vượt qua "Senior Engineer Test".
3. **Surgical Changes**: Chỉnh sửa chính xác, diff nhỏ gọn, giữ vững phong cách code nhất quán. Tuân thủ ranh giới giữa 4 phiên bản phát triển độc lập.
4. **Goal-Driven Execution**: Mỗi phiên bản phải có tiêu chí nghiệm thu (Acceptance Criteria) và kịch bản đo lường/kiểm thử thực nghiệm rõ ràng trước khi chuyển sang phiên bản tiếp theo.

## Technology Stack & Architecture Constraints
- **Agent**: Python 3.11+ chạy trên Windows 10/11 x64. Tách biệt rõ ràng 2 tầng:
  - `OGK-Service` (chạy nền quyền LocalSystem): Xử lý Policy Enforcer, Time Counter, Process Killer, DNS Proxy (127.0.0.1:53), Local SQLite Cache.
  - `OGK-Tray` (chạy trong User Session quyền hạn chế): Hiển thị đồng hồ thời gian còn lại, giao diện minh bạch cho trẻ, nhận thông báo chặn.
  - IPC nội bộ: Named Pipe hoặc HTTP Localhost có local token xác thực.
- **Server**: FastAPI + Uvicorn + SQLAlchemy + SQLite (chế độ WAL). Hỗ trợ RESTful API và WebSocket cho lệnh khẩn cấp (< 5 giây).
- **Dashboard**: Web responsive (dùng tốt trên trình duyệt máy tính và điện thoại), giao diện trực quan cho phụ huynh và màn hình riêng cho trẻ.

## Governance & Compliance
- Tuân thủ Luật Trẻ em 2016 (Điều 21), Luật An ninh mạng 2018 (Điều 29), Nghị định 13/2023/NĐ-CP (quy định bảo vệ dữ liệu cá nhân của trẻ em, thời hạn lưu trữ 90 ngày, cơ chế xóa dữ liệu theo yêu cầu).
- Tuân thủ tiêu chuẩn OWASP ASVS v4 (Mức 1) và NIST SP 800-63B cho xác thực và quản lý phiên.

**Version**: 1.0.0 | **Ratified**: 2026-10-08 | **Author**: Đồ án Chuyên đề Tốt nghiệp MMT
