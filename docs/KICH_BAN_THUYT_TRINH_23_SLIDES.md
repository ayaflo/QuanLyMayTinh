# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ CHUYÊN ĐỀ TỐT NGHIỆP
## ĐỀ TÀI: ỨNG DỤNG QUẢN LÝ MÁY TÍNH TRẺ EM (OPEN GUARDIAN KIDS)

* **Hệ đào tạo:** Đại học chính quy – Chuyên ngành Mạng máy tính & An toàn thông tin
* **Sinh viên thực hiện:**
  1. **Nguyễn Minh Hoàng** (MSSV: 23127368) — *Người trình bày 1 (SV1)*
  2. **Lê Văn Hoàng Tấn** (MSSV: 23127471) — *Người trình bày 2 (SV2)*
* **Tài liệu trình chiếu:** [Open_Guardian_Kids_Complete_25_Slides.pptx.pdf](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/docs/Open_Guardian_Kids_Complete_25_Slides.pptx.pdf) (Bộ 23 slide chuẩn)
* **Tổng thời lượng dự kiến:** 18 – 20 phút (Mỗi slide từ 40 – 60 giây)

---

## PHÂN CÔNG THUYẾT TRÌNH GỢI Ý (TEAM 2 BẠN)

* **Phần 1 – SV1 (Nguyễn Minh Hoàng): Từ Slide 1 đến Slide 12**
  * Đặt vấn đề, Hiến chương đạo đức & Khung pháp lý.
  * Kiến trúc tổng thể 3 khối, Phân lập Windows Session 0, Ngăn xếp công nghệ.
  * Giao thức ghép đôi bảo mật, Cơ chế Heartbeat, Bộ đếm giờ đơn điệu `time.monotonic()`.
  * Máy trạng thái khóa máy nhân văn, Kênh truyền WebSocket HMAC-SHA256, Tương tác tiếng nói của trẻ.

* **Phần 2 – SV2 (Lê Văn Hoàng Tấn): Từ Slide 13 đến Slide 23**
  * Kỹ thuật Mạng chuyên sâu: DNS Sinkhole UDP 53, Thuật toán Wildcard & NT6 Whitelist.
  * Ghi đè DNS cưỡng chế SafeSearch/YouTube, Vô hiệu hóa DoH qua Canary Domain.
  * Kiểm soát nhị phân tiến trình qua mã băm SHA-256.
  * An toàn thông tin: Xác thực Argon2id, AES-256-GCM, Chống IDOR, Quyền xóa dữ liệu (NĐ 13/2023).
  * Ma trận 7 lớp phòng thủ chống bypass (M3), Kiến trúc chịu lỗi ngoại tuyến (M5), Đóng góp & Kết luận.

---

# CHI TIẾT KỊCH BẢN TỪNG SLIDE

---

### SLIDE 1: TRANG TIÊU ĐỀ
* **Tiêu đề slide:** CHUYÊN ĐỀ TỐT NGHIỆP MẠNG MÁY TÍNH – ỨNG DỤNG QUẢN LÝ MÁY TÍNH TRẺ EM (OPEN GUARDIAN KIDS)
* **Thời lượng:** 45 giây
* **Người trình bày:** SV1 (Nguyễn Minh Hoàng)
* **Hành động trình chiếu:** Bật slide ở chế độ toàn màn hình, đứng trang nghiêm, mắt bao quát toàn thể Hội đồng.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Kính thưa quý Thầy, Cô trong Hội đồng chấm Chuyên đề Tốt nghiệp!
> 
> Lời đầu tiên, cho phép nhóm chúng em được gửi lời chào trân trọng và lời chúc sức khỏe chân thành nhất đến quý Thầy Cô.
> 
> Hôm nay, nhóm sinh viên gồm em là **Nguyễn Minh Hoàng** và bạn **Lê Văn Hoàng Tấn**, vinh dự được đại diện nhóm báo cáo kết quả nghiên cứu và thực nghiệm đề tài tốt nghiệp chuyên ngành Mạng máy tính với tên gọi: **'Xây dựng ứng dụng hỗ trợ quản lý việc sử dụng máy tính của trẻ em — Open Guardian Kids'**.
> 
> Đề tài được định hướng giải quyết bài toán cân bằng giữa việc bảo vệ an toàn trên không gian số cho trẻ em và tôn trọng tối đa quyền riêng tư cá nhân theo chuẩn quốc tế. Ngay sau đây, em xin phép được bắt đầu phần trình bày."

---

### SLIDE 2: VẤN ĐỀ THỰC TIỄN & GIẢI PHÁP TIẾP CẬN
* **Tiêu đề slide:** VẤN ĐỀ THỰC TIỄN & GIẢI PHÁP TIẾP CẬN
* **Thời lượng:** 50 giây
* **Người trình bày:** SV1
* **Hành động trình chiếu:** Trỏ chuột/laser vào cột "Cách tiếp cận còn hạn chế", sau đó chuyển sang cột "Hướng tiếp cận Open Guardian Kids".

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Thưa Thầy Cô, hiện nay nhu cầu sử dụng máy tính để học tập của trẻ em là vô cùng cấp thiết, tuy nhiên các giải pháp quản lý hiện có trên thị trường đang bộc lộ 3 nhược điểm lớn:
> 
> 1. **Rất dễ bị vô hiệu hóa:** Trẻ em ngày nay rất thông thạo công nghệ, các em có thể dễ dàng chỉnh lùi đồng hồ Windows, tự đổi DNS trên card mạng, hoặc gỡ bỏ các tiện ích mở rộng (extension) trên trình duyệt.
> 2. **Mang tính giám sát xâm lấn tiêu cực:** Nhiều phần mềm dùng cơ chế chụp lén màn hình, ghi phím (Keylogger) — điều này biến máy tính thành công cụ do thám, gây tổn thương tâm lý trẻ và vi phạm nghiêm trọng quyền riêng tư.
> 3. **Chi phí đắt đỏ và phụ thuộc máy chủ nước ngoài.**
> 
> Để khắc phục triệt để, **Open Guardian Kids** lựa chọn một hướng tiếp cận hoàn toàn mới ở tầng mạng và tầng lõi hệ điều hành:
> * Thay vì cài extension, chúng em can thiệp tại **tầng Mạng qua DNS Sinkhole cổng UDP 53** — hoạt động độc lập với mọi trình duyệt.
> * Thay vì đọc giờ hệ thống, chúng em dùng **đồng hồ phần cứng đơn điệu `time.monotonic()`** — chống lại 100% thủ thuật tua giờ.
> * Và đặc biệt, tuân thủ triết lý **Privacy by Design**: Tuyệt đối không chụp màn hình, không keylogger, biến công nghệ thành cầu nối tin tưởng giữa cha mẹ và con cái."

* **💡 Mẹo phản biện:** Nếu Thầy Cô hỏi *"Tại sao lại bỏ tính năng chụp màn hình trong khi phụ huynh rất muốn?"* $\rightarrow$ Trả lời: *"Việc chụp màn hình vi phạm Công ước LHQ về Quyền trẻ em và Nghị định 13/2023/NĐ-CP; đồng thời trẻ sẽ cảm thấy bị theo dõi và tìm mọi cách chống đối. Thay vào đó, việc bảo vệ ở cổng vào Internet (DNS) và khóa thời gian là giải pháp văn minh và an toàn hơn."*

---

### SLIDE 3: HIẾN CHƯƠNG ĐẠO ĐỨC & KHUNG PHÁP LÝ
* **Tiêu đề slide:** HIẾN CHƯƠNG ĐẠO ĐỨC & KHUNG PHÁP LÝ (6 NGUYÊN TẮC NT1 – NT6)
* **Thời lượng:** 50 giây
* **Người trình bày:** SV1
* **Hành động trình chiếu:** Trỏ vào hình lục giác trung tâm "Trẻ em là trọng tâm", nhấn mạnh 2 trụ cột pháp lý và kỹ thuật ở chân slide.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Thưa Hội đồng, xuất phát điểm của Open Guardian Kids là một **Hiến chương Đạo đức gồm 6 nguyên tắc (từ NT1 đến NT6)**, lấy trẻ em làm trung tâm:
> * **NT1 & NT2:** Cam kết '2 Không': Không chụp màn hình và Không ghi phím.
> * **NT3:** Tính minh bạch: Trẻ luôn biết rõ mình còn bao nhiêu phút sử dụng qua giao diện khay hệ thống trực quan.
> * **NT4:** Khóa nhân văn: Khi hết giờ chơi, máy không tắt phụt đột ngột mà luôn có khoảng thời gian ân hạn 60 giây để trẻ kịp lưu bài tập học trực tuyến và đóng ứng dụng.
> * **NT5:** Tôn trọng tiếng nói của trẻ: Trẻ có thể bấm nút xin thêm giờ có lý do, hoặc gửi báo cáo nếu một trang web giáo dục bị chặn nhầm.
> * **NT6:** Vùng an toàn bất khả xâm phạm: Các trang web thiết yếu như Cổng dịch vụ công, Bộ Giáo dục, Đường dây nóng bảo vệ trẻ em 111 luôn được bảo vệ, phụ huynh không thể vô tình chặn nhầm.
> 
> Toàn bộ hiến chương này được bảo chứng bởi **Luật Trẻ em 2016**, **Nghị định 13/2023/NĐ-CP** về bảo vệ dữ liệu cá nhân, cùng các tiêu chuẩn an toàn kỹ thuật hàng đầu như **NIST SP 800-63B** và **OWASP ASVS v4**."

---

### SLIDE 4: KIẾN TRÚC PHÂN TÁN 3 KHỐI TỔNG THỂ
* **Tiêu đề slide:** KIẾN TRÚC PHÂN TÁN 3 KHỐI TỔNG THỂ
* **Thời lượng:** 50 giây
* **Người trình bày:** SV1
* **Hành động trình chiếu:** Lần lượt chỉ từ Khối 1 (Client) $\rightarrow$ Khối 2 (Server) $\rightarrow$ Khối 3 (Dashboard) và các mũi tên giao thức.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Để hiện thực hóa các nguyên tắc trên, hệ thống được thiết kế theo mô hình kiến trúc phân tán 3 khối độc lập:
> 
> 1. **Khối Máy con (Protected Client Tier):** Chạy ngầm trên máy tính Windows của trẻ, gồm Core Service quản trị chính sách, DNS Proxy cổng 53 để lọc web, bộ kiểm soát tiến trình AppController và bộ nhớ đệm SQLite cục bộ.
> 2. **Khối Máy chủ Trung tâm (Central Server Tier):** Được xây dựng trên nền tảng FastAPI hiệu năng cao, tích hợp WebSocket Hub để truyền lệnh điều khiển tức thời, dịch vụ định kỳ dọn dẹp dữ liệu và cơ sở dữ liệu Cloud PostgreSQL.
> 3. **Khối Bảng điều khiển (Parent Dashboard Tier):** Giao diện Web Responsive hiện đại, giúp phụ huynh quản lý con em từ điện thoại hay máy tính mọi lúc mọi nơi thông qua cơ chế xác thực JWT HttpOnly cookie an toàn.
> 
> Mối liên kết giữa 3 khối được đảm bảo bởi kênh **HTTPS** cho các tác vụ đồng bộ cấu hình và kênh **WebSocket song công (WSS)** cho phép phụ huynh đẩy lệnh khóa máy khẩn cấp tới Agent với độ trễ phản hồi dưới 5 giây."

---

### SLIDE 5: KIẾN TRÚC WINDOWS SESSION 0 ISOLATION
* **Tiêu đề slide:** KIẾN TRÚC WINDOWS SESSION 0 ISOLATION
* **Thời lượng:** 55 giây
* **Người trình bày:** SV1
* **Hành động trình chiếu:** Trỏ vào vạch phân cách giữa Session 0 (Môi trường Dịch vụ Hệ thống) và Session 1 (Không gian làm việc của Người dùng).

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Một thách thức kỹ thuật rất lớn trong các phần mềm giám sát trên Windows là: *'Làm thế nào ngăn trẻ em không mở Task Manager để tắt ứng dụng?'*.
> 
> Chúng em giải quyết bằng kiến trúc **Phân lập phiên làm việc (Session 0 Isolation)** kết hợp cơ chế phân quyền hệ điều hành:
> * Toàn bộ nhân xử lý gồm Core Service, DNS Proxy và AppController được đưa vào **Session 0 (Dịch vụ nền SYSTEM phi tương tác)**. Môi trường này chạy hoàn toàn độc lập với màn hình desktop của người dùng.
> * Tại **Session 1 (Màn hình của trẻ)**, chỉ chạy duy nhất giao diện nhẹ Tray UI thông báo thời gian và hộp thoại tương tác. Hai bên giao tiếp qua kênh IPC Loopback nội bộ.
> * Khi trẻ mở Task Manager bấm 'End Task' vào tiến trình dịch vụ, do tài khoản trẻ được thiết lập là **Standard User**, Bộ giám sát an ninh nhân hệ điều hành (Windows SRM) sẽ lập tức kích hoạt lỗi **`0x5: Access is Denied`**.
> * Nhờ vậy, ngay cả khi trẻ tắt được giao diện Tray UI ở Session 1, toàn bộ bức tường bảo vệ ở Session 0 vẫn hoạt động bền bỉ 100%."

---

### SLIDE 6: NGĂN XẾP CÔNG NGHỆ & GIAO THỨC MẠNG
* **Tiêu đề slide:** NGĂN XẾP CÔNG NGHỆ & GIAO THỨC MẠNG
* **Thời lượng:** 45 giây
* **Người trình bày:** SV1
* **Hành động trình chiếu:** Quét qua 4 tầng công nghệ từ trên xuống dưới.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Trên màn hình là bức tranh toàn cảnh về Stack công nghệ được nhóm tuyển chọn kỹ lưỡng:
> * **Tầng Trình bày:** Dashboard phụ huynh được tối ưu chuẩn HTML5/CSS, phía máy con sử dụng thư viện `pystray` và giao diện Tkinter tùy biến thân thiện với trẻ nhỏ.
> * **Tầng Ứng dụng:** Backend sử dụng **FastAPI** bất đồng bộ (ASGI) với Uvicorn, chuẩn hóa dữ liệu bằng Pydantic v2 và quản lý cơ sở dữ liệu qua SQLAlchemy 2.0.
> * **Tầng Giao thức & An ninh mạng:** Giao tiếp hoàn toàn qua **TLS 1.3**, WebSocket bảo mật WSS theo chuẩn **RFC 6455**, và Socket UDP 53 cho DNS. Hệ thống sử dụng thuật toán băm mật khẩu hiện đại nhất **Argon2id**, mã hóa dữ liệu tĩnh **AES-256-GCM AEAD**, và chữ ký số xác thực **HMAC-SHA256**.
> * **Tầng Hệ thống:** Tương tác trực tiếp với Win32 API, thư viện đo tài nguyên `psutil`, kết hợp lưu trữ SQLite 3 tại máy con và PostgreSQL trên máy chủ đám mây."

---

### SLIDE 7: GIAO THỨC GHÉP ĐÔI THIẾT BỊ AN TOÀN (DEVICE ENROLLMENT)
* **Tiêu đề slide:** GIAO THỨC GHÉP ĐÔI THIẾT BỊ AN TOÀN
* **Thời lượng:** 50 giây
* **Người trình bày:** SV1
* **Hành động trình chiếu:** Trỏ theo các bước số 1 $\rightarrow$ 2 $\rightarrow$ 3 $\rightarrow$ 4 trên sơ đồ tuần tự.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Tiếp theo là **Giao thức ghép đôi thiết bị (Enrollment Protocol)**. Một lỗi rất phổ biến ở các phần mềm khác là bắt phụ huynh phải nhập tài khoản mật khẩu trực tiếp trên máy của trẻ — điều này rất dễ bị lộ mật khẩu.
> 
> Open Guardian Kids giải quyết bằng quy trình mã PIN ủy quyền một lần:
> 1. Trên Dashboard, phụ huynh bấm 'Thêm thiết bị', máy chủ sinh một **mã PIN ngẫu nhiên 6 ký tự** với thời gian sống (TTL) đúng **10 phút**.
> 2. Phụ huynh chỉ cần đưa mã PIN này cho trẻ hoặc tự nhập vào giao diện Agent máy con.
> 3. Agent gửi yêu cầu ghép đôi kèm theo mã PIN, Hardware UUID và Hostname qua kênh mã hóa HTTPS.
> 4. Máy chủ xác thực tính hợp lệ của mã PIN, cấp phát một cặp định danh gồm `device_id` và một chuỗi khóa bí mật `device_token` ngẫu nhiên 32 bytes (256-bit entropy).
> 
> Mã PIN lập tức bị hủy sau lần dùng đầu tiên, loại bỏ hoàn toàn nguy cơ tấn công replay hay rò rỉ mật khẩu của cha mẹ."

---

### SLIDE 8: GIÁM SÁT TRẠNG THÁI & HEARTBEAT
* **Tiêu đề slide:** GIÁM SÁT TRẠNG THÁI & HEARTBEAT
* **Thời lượng:** 45 giây
* **Người trình bày:** SV1
* **Hành động trình chiếu:** Trỏ vào công thức phân loại trạng thái $\Delta t \le 120s$.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Để phụ huynh luôn biết con mình có đang bật máy hay không, hệ thống triển khai cơ chế **Nhịp tim định kỳ (Heartbeat)**:
> * Định kỳ mỗi **60 giây**, Agent tại máy con sẽ gửi một gói tin HTTP POST chứa thông số viễn trắc tối thiểu: Tải CPU, dung lượng RAM sử dụng, thời gian máy hoạt động (Uptime) và phiên bản phần mềm.
> * Máy chủ xác thực Token thiết bị và cập nhật trường thời gian `last_seen_at`.
> * Dashboard phân loại trạng thái thiết bị theo công thức: Nếu độ trễ $\Delta t \le 120$ giây, thiết bị được đánh dấu **ONLINE (Màu xanh)**; nếu quá 120 giây không có tín hiệu, thiết bị chuyển sang trạng thái **OFFLINE (Màu xám)**.
> * Đặc biệt, cơ chế Heartbeat chủ động đẩy từ Client ra ngoài giúp hệ thống **vượt qua mọi tường lửa NAT gia đình**, không cần phụ thuộc vào gói tin ICMP Ping vốn thường xuyên bị chặn."

---

### SLIDE 9: BỘ ĐẾM GIỜ ĐƠN ĐIỆU & NHẬN DIỆN IDLE
* **Tiêu đề slide:** BỘ ĐẾM GIỜ ĐƠN ĐIỆU & NHẬN DIỆN IDLE
* **Thời lượng:** 55 giây
* **Người trình bày:** SV1
* **Hành động trình chiếu:** Trỏ vào công thức $\Delta t = \text{monotonic\_now} - \text{monotonic\_prev}$ và hàm `GetLastInputInfo()`.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Slide số 9 thể hiện một cải tiến kỹ thuật quan trọng của đề tài: **Khắc phục triệt để chiêu trò gian lận thời gian của trẻ**.
> 
> * **Chống tua giờ bằng `time.monotonic()`:** Nếu dùng hàm `time.time()`, khi trẻ vào Windows Settings chỉnh lùi ngày giờ về quá khứ, bộ đếm giờ sẽ bị sai lệch hoàn toàn. Nhóm chúng em sử dụng hàm `time.monotonic()` — bộ đếm đo xung nhịp phần cứng vi xử lý (Hardware Clock). Đồng hồ này là một hàm đơn điệu chỉ tăng dần theo thời gian vật lý của máy tính và hoàn toàn miễn nhiễm trước việc sửa giờ Windows hay sửa BIOS.
> * **Nhận diện trạng thái nghỉ (Idle Detection):** Thông qua hàm Win32 API `GetLastInputInfo()`, hệ thống phát hiện chính xác thời điểm trẻ không di chuột hoặc gõ phím. Nếu máy tính ở trạng thái nhàn rỗi quá **300 giây (5 phút)**, bộ đếm sẽ tạm dừng tích lũy giờ chơi để đảm bảo tính công bằng.
> * Toàn bộ thời gian tích lũy được ghi đệm vào SQLite nội bộ định kỳ 30 giây một lần, giúp khôi phục chính xác thời gian đã dùng ngay cả khi trẻ cố tình bấm nút Reset thùng máy."

---

### SLIDE 10: MÁY TRẠNG THÁI KHÓA MÁY NHÂN VĂN
* **Tiêu đề slide:** MÁY TRẠNG THÁI KHÓA MÁY NHÂN VĂN (MÁY TRẠNG THÁI FSM)
* **Thời lượng:** 50 giây
* **Người trình bày:** SV1
* **Hành động trình chiếu:** Trỏ chuột theo chu trình: RUNNING $\rightarrow$ GRACE PERIOD $\rightarrow$ LOCKED và mũi tên Vòng lặp tái khóa.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Cơ chế thực thi giới hạn thời gian được mô hình hóa bằng một **Máy trạng thái hữu hạn (Finite State Machine)** với 3 trạng thái chính:
> 
> 1. **RUNNING (Bình thường):** Trẻ sử dụng máy tính tự do trong khung giờ cho phép. Hệ thống chủ động hiển thị thông báo nhắc nhở khi còn 5 phút và 1 phút.
> 2. **GRACE PERIOD (Thời gian ân hạn nhân văn):** Khi hết sạch thời gian sử dụng, hệ thống không khóa ngay lập tức mà chuyển sang trạng thái ân hạn **60 giây**. Màn hình xuất hiện đồng hồ đếm ngược thông báo để trẻ kịp bấm lưu tài liệu học tập, tránh làm mất bài vở của trẻ.
> 3. **LOCKED (Khóa màn hình an toàn):** Hết 60 giây, Agent gọi hàm API Windows `ctypes.windll.user32.LockWorkStation()` để đưa màn hình về trạng thái khóa bảo vệ của Windows.
> * Đồng thời, Agent duy trì **Vòng lặp tái khóa (Re-lock loop)** quét mỗi 1 đến 2 giây: Nếu trẻ cố tình đăng nhập lại bằng mật khẩu Windows nhưng chưa được cha mẹ cộng thêm giờ, máy tính sẽ lập tức bị khóa lại ngay."

---

### SLIDE 11: LỆNH THỜI GIAN THỰC & HMAC-SHA256
* **Tiêu đề slide:** LỆNH THỜI GIAN THỰC & CHỮ KÝ TOÀN VẸN HMAC-SHA256
* **Thời lượng:** 50 giây
* **Người trình bày:** SV1
* **Hành động trình chiếu:** Trỏ vào chuỗi truyền bản tin WSS và công thức toán học của chữ ký HMAC-SHA256.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Khi phụ huynh muốn can thiệp khẩn cấp — ví dụ bấm nút 'Khóa máy ngay' hoặc 'Tặng thêm 30 phút' từ điện thoại — tín hiệu không thể chờ đợi lâu.
> 
> * Chúng em thiết lập đường truyền **WebSocket bảo mật (WSS)** duy trì kết nối song công liên tục giữa Máy chủ và Agent máy con, cho phép truyền lệnh đến đích trong thời gian chưa đầy **0.5 giây**.
> * Để ngăn chặn triệt để nguy cơ kẻ xấu tấn công giả mạo lệnh điều khiển trên mạng, mỗi bản tin gửi đi bắt buộc phải đi kèm một **Chữ ký xác thực thông điệp HMAC-SHA256**:
>   $$\text{Signature} = \text{HMAC-SHA256}(\text{device\_token}, \text{payload} + \text{timestamp})$$
> * Agent nhận lệnh sẽ kiểm tra tính toàn vẹn của chữ ký dựa trên khóa mật mã chia sẻ `device_token`. Đồng thời kiểm tra tem thời gian: Nếu bản tin bị trễ hoặc bị phát lại sau quá **60 giây** (Replay Attack), Agent sẽ lập tức từ chối thực thi."

---

### SLIDE 12: TIẾNG NÓI CỦA TRẺ & TƯƠNG TÁC HAI CHIỀU
* **Tiêu đề slide:** TIẾNG NÓI CỦA TRẺ & TƯƠNG TÁC HAI CHIỀU
* **Thời lượng:** 45 giây
* **Người trình bày:** SV1
* **Hành động trình chiếu:** Giới thiệu giao diện Tray UI trên slide, sau đó giới thiệu bạn SV2 tiếp nối phần trình bày.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Slide số 12 minh chứng cho nguyên tắc nhân văn cốt lõi của đề tài: **Lắng nghe tiếng nói của trẻ**.
> 
> * Trên giao diện Tray UI ở góc màn hình, trẻ luôn thấy rõ mình đã dùng bao nhiêu phút và còn lại bao nhiêu phút.
> * Khi cần thêm thời gian để làm bài tập, trẻ bấm nút **'Xin thêm giờ'**, chọn các mốc 15, 30 hoặc 60 phút và nhập lý do gửi đến cha mẹ.
> * Nếu một trang web học tập lành mạnh bị bộ lọc chặn nhầm, trẻ có thể bấm nút **'Báo chặn nhầm'**.
> * Yêu cầu này lập tức hiển thị trên Dashboard của cha mẹ. Nếu cha mẹ bấm phê duyệt, lệnh mở khóa sẽ đồng bộ ngược trở lại máy con qua WebSocket ngay tức thì.
> 
> Vừa rồi là phần trình bày về kiến trúc tổng quan, phương thức quản lý thời gian và các tính năng tương tác. Tiếp theo, em xin phép kính mời bạn **Lê Văn Hoàng Tấn** sẽ trình bày chi tiết về các giải pháp kỹ thuật mạng chuyên sâu, bảo mật dữ liệu và cơ chế chống bypass của hệ thống."

---

### SLIDE 13: DNS SINKHOLE PROXY UDP 53 (M1)
* **Tiêu đề slide:** DNS SINKHOLE PROXY UDP 53 (M1)
* **Thời lượng:** 55 giây
* **Người trình bày:** SV2 (Lê Văn Hoàng Tấn)
* **Hành động trình chiếu:** SV2 bước lên cúi chào Hội đồng, trỏ vào sơ đồ phân luồng 2 nhánh: Nhánh Cấm (0.0.0.0) và Nhánh Hợp lệ (Upstream 1.1.1.3).

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Kính thưa quý Thầy Cô! Em là **Lê Văn Hoàng Tấn**, em xin phép được tiếp tục phần báo cáo với trọng tâm là các giải pháp kỹ thuật mạng và an toàn thông tin chuyên sâu của đề tài.
> 
> Trái tim của hệ thống lọc web trong Open Guardian Kids là một **DNS Sinkhole Proxy** tự phát triển chạy ngay tại máy con ở địa chỉ `127.0.0.1:53`:
> * Toàn bộ card mạng Windows được cấu hình ưu tiên trỏ DNS về Localhost. Bất cứ khi nào trình duyệt hay ứng dụng gửi yêu cầu phân giải tên miền (DNS Query), gói tin UDP cổng 53 sẽ bị Agent bắt giữ và đối chiếu với bộ quy tắc:
>   * **Nếu tên miền thuộc Blacklist (Nội dung xấu/Game cấm):** DNS Proxy phản hồi ngay lập tức một bản ghi nhân tạo trỏ về địa chỉ ngõ cụt `0.0.0.0`. Trình duyệt lập tức báo lỗi ngắt kết nối mà không thể tải được trang web. Thời gian xử lý chặn đo được trong thực tế chỉ mất **0.83 mili-giây**!
>   * **Nếu tên miền hợp lệ:** Gói tin được chuyển tiếp an toàn tới máy chủ DNS cấp trên (Upstream DNS) là Cloudflare 1.1.1.3 (Dịch vụ DNS bảo vệ gia đình) để lấy IP thật trả về cho ứng dụng.
> * Nhờ hoạt động ở tầng mạng, cơ chế này lọc được toàn bộ các trình duyệt từ Chrome, Edge đến Firefox mà không cần cài bất kỳ tiện ích mở rộng nào."

---

### SLIDE 14: WILDCARD SUBDOMAIN & WHITELIST NT6
* **Tiêu đề slide:** WILDCARD SUBDOMAIN & WHITELIST NT6
* **Thời lượng:** 50 giây
* **Người trình bày:** SV2
* **Hành động trình chiếu:** Trỏ vào công thức toán học logic khớp tên miền và danh sách bảo vệ NT6 màu xanh lá.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Để việc lọc tên miền đạt độ chính xác cao và tránh hiện tượng chặn nhầm, nhóm đã xây dựng **Thuật toán khớp tên miền con linh hoạt (Wildcard Subdomain Matching)**:
> * Điều kiện logic được định nghĩa chặt chẽ:
>   $$\text{Match}(Q, D) \iff (Q = D) \lor Q.\text{endsWith}("." + D)$$
> * Ví dụ: Khi phụ huynh cấm tên miền `tiktok.com`, thuật toán sẽ chặn chính xác `tiktok.com` và toàn bộ các tên miền con như `vt.tiktok.com`, `api.tiktok.com`. Tuy nhiên, các tên miền an toàn khác chỉ tình cờ chứa cụm từ đó như `nottiktok.com` sẽ **hoàn toàn không bị chặn nhầm**.
> * Đặc biệt, để hiện thực hóa nguyên tắc **NT6 (Vùng an toàn)**, hệ thống thiết lập một **Danh sách Trắng Miễn Nhiễm (Immutable Whitelist)** gồm các tên miền thiết yếu quốc gia: `tongdai111.vn`, `moet.gov.vn`, `chinhphu.vn` và đuôi học tập `.edu.vn`.
> * Danh sách này được ưu tiên thẩm định đầu tiên trong pipeline, phụ huynh không thể thêm vào danh sách cấm, đảm bảo quyền tiếp cận thông tin giáo dục và cứu hộ khẩn cấp của trẻ luôn được bảo toàn."

---

### SLIDE 15: GHI ĐÈ DNS: SAFESEARCH & YOUTUBE
* **Tiêu đề slide:** GHI ĐÈ DNS: SAFESEARCH & YOUTUBE (DNS REWRITE)
* **Thời lượng:** 55 giây
* **Người trình bày:** SV2
* **Hành động trình chiếu:** Trỏ vào cột "Truy vấn đầu vào" $\rightarrow$ "Ghi đè bản ghi A" $\rightarrow$ "Địa chỉ IP an toàn (VIP)".

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Một câu hỏi đặt ra là: *'Nếu trẻ không vào trang web đen trực tiếp, mà lên Google Tìm kiếm hoặc YouTube gõ từ khóa tìm nội dung 18+, hoặc trẻ lén tắt tính năng SafeSearch thì sao?'*.
> 
> Nhóm chúng em đã ứng dụng kỹ thuật **Ghi đè bản ghi DNS (DNS Rewrite)**:
> * Thay vì giải mã nội dung HTTPS (vốn xâm phạm quyền riêng tư và rất phức tạp), khi DNS Proxy nhận truy vấn `A Record` đến `google.com`, `bing.com` hay `youtube.com`, nó sẽ không trả về IP thông thường mà trả về các **Địa chỉ IP ảo chuyên biệt (Virtual IPs - VIP)** do Google và Microsoft quy chuẩn cho môi trường học đường:
>   * `forcesafesearch.google.com` $\rightarrow$ IP `216.239.38.120`
>   * `strict.bing.com` $\rightarrow$ IP `204.79.197.220`
>   * `restrict.youtube.com` $\rightarrow$ IP `216.239.38.119`
> * Khi trình duyệt kết nối đến các IP VIP này, máy chủ của Google và YouTube sẽ **tự động ép cứng cờ tìm kiếm an toàn ở cấp độ nghiêm ngặt nhất (Strict Mode)**. Nút gạt tắt SafeSearch trên giao diện web sẽ bị làm mờ, trẻ hoàn toàn không có cách nào tắt được bộ lọc này kể cả khi mở tab ẩn danh."

---

### SLIDE 16: CANARY DOMAIN & PHẢN HỒI NXDOMAIN
* **Tiêu đề slide:** CANARY DOMAIN & PHẢN HỒI NXDOMAIN (VÔ HIỆU HÓA DoH)
* **Thời lượng:** 50 giây
* **Người trình bày:** SV2
* **Hành động trình chiếu:** Trỏ vào chu trình 4 bước và tên miền Canary `use-application-dns.net`.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Hiện nay, các trình duyệt hiện đại như Google Chrome, Microsoft Edge hay Mozilla Firefox đều hỗ trợ tính năng **DNS over HTTPS (DoH)** — mã hóa truy vấn DNS qua cổng HTTPS 443 trực tiếp tới Cloudflare `1.1.1.1` hoặc Google `8.8.8.8`, qua mặt cổng DNS 53 thông thường.
> 
> Để khắc phục, Open Guardian Kids ứng dụng tiêu chuẩn chính thức của Mozilla và liên minh Chromium thông qua cơ chế **Canary Domain**:
> 1. Trước khi tự động kích hoạt tính năng mã hóa DoH, mọi trình duyệt chuẩn đều bắt buộc phải gửi một gói tin DNS thăm dò tới tên miền đặc biệt là: `use-application-dns.net`.
> 2. DNS Proxy của chúng em phát hiện truy vấn này và lập tức phản hồi mã trạng thái **`RCODE = 3 (NXDOMAIN - Tên miền không tồn tại)`**.
> 3. Nhận được tín hiệu `NXDOMAIN`, trình duyệt hiểu rằng mạng nội bộ này đang có một chính sách quản trị phụ huynh/học đường cần tuân thủ và **tự động vô hiệu hóa tính năng DoH**, quay trở về sử dụng cổng phân giải DNS hệ thống cổng 53 do Agent kiểm soát."

---

### SLIDE 17: KIỂM SOÁT ỨNG DỤNG BẰNG SHA-256
* **Tiêu đề slide:** KIỂM SOÁT ỨNG DỤNG BẰNG BĂM NHỊ PHÂN SHA-256
* **Thời lượng:** 50 giây
* **Người trình bày:** SV2
* **Hành động trình chiếu:** Trỏ vào lưu đồ luồng: Quét tiến trình $\rightarrow$ Bộ đệm Cache $\rightarrow$ Băm SHA-256 $\rightarrow$ Terminate nếu vi phạm.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Bên cạnh kiểm soát web, việc quản lý ứng dụng và trò chơi được đảm trách bởi module **AppController**:
> * Nhiều phần mềm phụ huynh hiện nay chỉ so khớp tên file exe — trẻ em chỉ cần vào thư mục game đổi tên file `roblox.exe` thành `winword.exe` là qua mặt được ngay.
> * Với Open Guardian Kids, chúng em áp dụng giải pháp **Băm nhị phân mật mã học SHA-256**:
>   * Định kỳ mỗi 3 giây, Agent quét các tiến trình đang chạy.
>   * Thay vì chỉ nhìn tên tiến trình, Agent đọc các khối nhị phân của tệp thực thi từ ổ cứng và tính chuỗi mã băm SHA-256 64 ký tự. Mã băm này là đại diện duy nhất cho nội dung của file — dù đổi tên file thành bất cứ thứ gì, mã băm vẫn bất biến và bị chặn đứng trong vòng 3 giây.
> * Để không gây tốn tài nguyên máy tính, chúng em tích hợp **Bộ đệm thông minh LRU Cache `(mtime, sha256)`**: Chỉ khi nào file bị chỉnh sửa thì mới tính toán lại, giúp tiến trình duy trì mức tiêu thụ CPU gần như tuyệt đối là **0.0%**."

---

### SLIDE 18: BẢO MẬT XÁC THỰC & MÃ HÓA AES-256-GCM
* **Tiêu đề slide:** BẢO MẬT XÁC THỰC & MÃ HÓA AES-256-GCM
* **Thời lượng:** 50 giây
* **Người trình bày:** SV2
* **Hành động trình chiếu:** Trỏ vào phễu lọc bảo mật (Rate Limit $\rightarrow$ Lockout $\rightarrow$ Argon2id) và cấu trúc gói tin mã hóa AES-256-GCM.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Về mặt an toàn thông tin, hệ thống tuân thủ nghiêm ngặt chuẩn an ninh mạng **OWASP ASVS v4 cấp độ 1**:
> * **Đường ống xác thực phụ huynh 3 lớp:**
>   1. *Rate Limiting:* Giới hạn tối đa 10 yêu cầu/phút trên mỗi IP để ngăn chặn rà quét tự động.
>   2. *Chống tấn công Brute-force:* Nếu đăng nhập sai quá 5 lần liên tiếp, tài khoản phụ huynh sẽ bị khóa cứng trong 15 phút.
>   3. *Băm mật khẩu Argon2id:* Đạt giải nhất cuộc thi băm mật khẩu thế giới, có khả năng kháng cự vượt trội trước các hệ thống bẻ khóa phần cứng GPU chuyên dụng.
> * **Mã hóa dữ liệu tĩnh chuẩn AES-256-GCM (AEAD):** Toàn bộ dữ liệu cấu hình nhạy cảm được bảo vệ bằng cơ chế Mã hóa có xác thực (Authenticated Encryption), bao gồm: Vector khởi tạo ngẫu nhiên Nonce 12 bytes, phần thân mã hóa Ciphertext, và thẻ xác thực toàn vẹn Auth Tag 16 bytes — giúp phát hiện tức thì nếu cơ sở dữ liệu bị can thiệp trái phép."

---

### SLIDE 19: CHỐNG IDOR & QUYỀN XÓA DỮ LIỆU
* **Tiêu đề slide:** CHỐNG IDOR & QUYỀN XÓA DỮ LIỆU (RIGHT TO ERASURE)
* **Thời lượng:** 50 giây
* **Người trình bày:** SV2
* **Hành động trình chiếu:** Trỏ vào quy trình thẩm quyền sở hữu ở mục 01 và quy trình 4 bước xóa dữ liệu ở mục 02.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Slide số 19 thể hiện hai tính năng an ninh và pháp lý cốt lõi:
> 
> 1. **Triệt tiêu lỗ hổng IDOR (Insecure Direct Object References):**
>    * Trong các hệ thống nhiều người dùng, phụ huynh A có thể sửa mã `device_id` trên đường link để xem lén máy tính của con phụ huynh B.
>    * Trong toàn bộ các API của chúng em, hệ thống luôn thực hiện bước kiểm tra thẩm quyền sở hữu nghiêm ngặt: `device.parent_id == current_user.id`. Bất kỳ yêu cầu truy cập trái thẩm quyền nào đều bị chặn đứng ngay lập tức với mã lỗi **HTTP 403 Forbidden**.
> 2. **Hiện thực hóa quyền xóa dữ liệu (Right to Erasure theo Nghị định 13):**
>    * Khi phụ huynh quyết định ngừng sử dụng dịch vụ và bấm nút 'Xóa vĩnh viễn thiết bị', hệ thống kích hoạt quy trình xóa dữ liệu toàn diện 2 chiều: Xóa sạch bản ghi trên Cloud PostgreSQL, đồng thời phát lệnh WebSocket yêu cầu Agent máy con xóa sạch cơ sở dữ liệu SQLite cục bộ, bảo vệ quyền riêng tư tuyệt đối cho trẻ."

---

### SLIDE 20: MA TRẬN 7 LỚP PHÒNG THỦ CHỐNG VƯỢT RÀO
* **Tiêu đề slide:** MA TRẬN 7 LỚP PHÒNG THỦ CHỐNG VƯỢT RÀO (ANTI-BYPASS GUARD)
* **Thời lượng:** 60 giây
* **Người trình bày:** SV2
* **Hành động trình chiếu:** Trỏ từ Tầng Mạng (Lớp 1-3) $\rightarrow$ Tầng Tiến trình & Thời gian (Lớp 4-5) $\rightarrow$ Tầng Dịch vụ & HĐH (Lớp 6-7).

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Thưa Hội đồng, nguyên lý cốt lõi của an toàn thông tin là không bao giờ tin tưởng vào một chốt chặn duy nhất. Chúng em đã thiết lập **Ma trận 7 lớp phòng thủ chống vượt rào (M3 Defense-in-Depth)**:
> 
> * **Tại tầng Mạng:**
>   * *Lớp 1 (DnsWatchdog):* Cứ 20 giây một lần tự động kiểm tra card mạng; nếu trẻ đổi DNS sang 8.8.8.8, Watchdog tự động cưỡng chế trỏ lại `127.0.0.1`.
>   * *Lớp 2 (Canary NXDOMAIN):* Đón đầu và vô hiệu hóa chế độ mã hóa DNS over HTTPS của trình duyệt.
>   * *Lớp 3 (Kiểm soát DoT / Tường lửa):* Khóa cổng DNS mã hóa TCP 853.
> * **Tại tầng Ứng dụng & Thời gian:**
>   * *Lớp 4 (VPN & App Guard):* Chặn các trình duyệt lạ và ứng dụng VPN thông qua nhận diện mã băm SHA-256.
>   * *Lớp 5 (Monotonic Time):* Khóa cứng bộ đếm thời gian bằng xung nhịp phần cứng, bất biến trước việc tua lùi giờ Windows.
> * **Tại tầng Hệ điều hành Windows:**
>   * *Lớp 6 (Session 0 Isolation):* Tách rời dịch vụ lõi khỏi giao diện người dùng.
>   * *Lớp 7 (Windows Standard User):* Tước quyền Administrator của trẻ, khiến trẻ không thể gỡ phần mềm, không thể End Task tiến trình và không thể sửa card mạng.
> 
> Sự kết hợp nhịp nhàng của 7 lớp bảo vệ này tạo nên một bức tường phòng thủ kiên cố, nâng độ khó vượt rào lên mức tối đa."

---

### SLIDE 21: KIẾN TRÚC CHỊU LỖI NGOẠI TUYẾN & TỰ PHỤC HỒI
* **Tiêu đề slide:** KIẾN TRÚC CHỊU LỖI NGOẠI TUYẾN & TỰ PHỤC HỒI (M5)
* **Thời lượng:** 50 giây
* **Người trình bày:** SV2
* **Hành động trình chiếu:** Trỏ vào 2 trạng thái Online Normal $\leftrightarrow$ Offline Autonomous và hàng đợi đồng bộ SQLite.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Một kịch bản thực tế rất phổ biến: *'Nếu trẻ cố tình rút dây mạng Internet hoặc tắt Wi-Fi để máy chủ không gửi lệnh khóa máy được thì sao?'*.
> 
> Module **M5 Fault Tolerance** giải quyết bài toán này bằng cơ chế **Tự hành ngoại tuyến (Offline Autonomous Mode)**:
> * Khi mất mạng Internet hoặc máy chủ gặp sự cố, Agent máy con không bị vô hiệu hóa mà tự động chuyển sang chế độ độc lập: Tiếp tục lấy chính sách đã được mã hóa trong SQLite cục bộ ra thực thi, tiếp tục đếm giờ bằng `time.monotonic()`, và khi hết giờ vẫn tự động khóa màn hình máy tính bình thường.
> * Mọi sự kiện vi phạm hoặc nhật ký sử dụng trong thời gian mất mạng được xếp vào hàng đợi SQLite bền vững.
> * Khi kết nối Internet được khôi phục, Agent tự động thực hiện tiến trình **Đồng bộ hàng loạt có tính lũy đẳng (Bulk Sync with Idempotency)** lên Cloud mà không làm trùng lặp dữ liệu.
> * Ngay cả trường hợp máy tính bị tắt nguồn đột ngột, trạng thái sử dụng trước đó vẫn được khôi phục chính xác 100% từ đĩa."

---

### SLIDE 22: KẾT LUẬN & HƯỚNG PHÁT TRIỂN
* **Tiêu đề slide:** KẾT LUẬN & HƯỚNG PHÁT TRIỂN
* **Thời lượng:** 45 giây
* **Người trình bày:** SV2 (hoặc cả 2 bạn cùng đứng lên)
* **Hành động trình chiếu:** Điểm qua 4 đóng góp cốt lõi và các hướng mở rộng trong tương lai.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Kính thưa Hội đồng, qua quá trình nghiên cứu và thực nghiệm nghiêm túc, đề tài **Open Guardian Kids** đã đạt được các kết quả nổi bật:
> 1. Xây dựng thành công giải pháp quản lý thời gian chính xác, chống gian lận bằng đồng hồ đơn điệu phần cứng.
> 2. Kiểm soát truy cập mạng và ứng dụng hiệu quả ở tầng mạng (DNS Sinkhole cổng 53) và băm nhị phân SHA-256.
> 3. Thiết lập kênh điều khiển thời gian thực WebSocket có độ trễ dưới 0.5 giây kèm chữ ký số xác thực HMAC-SHA256.
> 4. Đặc biệt là bảo vệ toàn diện quyền riêng tư của trẻ theo đúng chuẩn mực đạo đức và pháp lý.
> 
> Trong giai đoạn tiếp theo, nhóm định hướng mở rộng:
> * Phát triển ứng dụng Native Mobile cho phụ huynh trên iOS và Android.
> * Tích hợp mô hình trí tuệ nhân tạo (Lightweight AI) phân loại tên miền tự động ngay tại máy con.
> * Mở rộng phiên bản Agent cho các hệ điều hành khác như macOS và Linux."

---

### SLIDE 23: LỜI CẢM ƠN & PHIÊN HỎI ĐÁP (Q&A)
* **Tiêu đề slide:** CẢM ƠN MỌI NGƯỜI ĐÃ LẮNG NGHE – Q&A
* **Thời lượng:** 30 giây
* **Người trình bày:** Cả hai bạn cùng cúi chào
* **Hành động trình chiếu:** Giữ nguyên slide Q&A, đứng thẳng, nét mặt tự tin, tươi tắn, sẵn sàng đón nhận câu hỏi.

#### 🎙️ Lời thoại thuyết trình (Speaking Script):
> "Đến đây, nhóm chúng em xin phép được kết thúc bài báo cáo kết quả Chuyên đề Tốt nghiệp đề tài Open Guardian Kids.
> 
> Chúng em xin chân thành cảm ơn quý Thầy Cô trong Hội đồng đã chú ý lắng nghe. Nhóm chúng em rất mong nhận được những nhận xét, góp ý quý báu từ quý Thầy Cô để đồ án được hoàn thiện hơn nữa.
> 
> Chúng em xin trân trọng kính mời quý Thầy Cô đặt câu hỏi cho nhóm ạ!"

---

## BỘ CÂU HỎI PHẢN BIỆN THƯỜNG GẶP TỪ HỘI ĐỒNG & CÁCH TRẢ LỜI ĐIỂM 10

### ❓ Câu hỏi 1: "Nếu trẻ tải trình duyệt lạ như Tor Browser hoặc dùng Opera bật VPN thì DNS Sinkhole có còn tác dụng không?"
* **Trả lời sắc bén:**
  > "Thưa Thầy Cô, đây là lý do hệ thống áp dụng triết lý **Phòng thủ chiều sâu (Defense-in-Depth)** thay vì chỉ dựa vào DNS:
  > 1. Trẻ dùng tài khoản **Standard User**, khi tải và cài đặt Tor/Opera sẽ bị Windows UAC chặn lại do thiếu mật khẩu Administrator.
  > 2. Nếu trẻ mang bản **Tor Browser Portable** cắm USB chạy trực tiếp, module `AppController` của chúng em quét tiến trình mỗi 3 giây, nhận diện mã băm SHA-256 của `tor.exe` trong Blacklist và lập tức kích hoạt lệnh `kill()` hạ gục tiến trình trong vòng chưa đầy 3 giây.
  > 3. Ngoài ra, phụ huynh có thể kích hoạt chế độ **Whitelist (Chỉ cho phép ứng dụng được duyệt)** — bất kỳ trình duyệt lạ nào không có tên trong danh sách đều tự động bị đóng ngay khi vừa khởi động."

### ❓ Câu hỏi 2: "Tại sao lại dùng `time.monotonic()` mà không dùng đồng hồ của Windows hay NTP Server?"
* **Trả lời sắc bén:**
  > "Thưa Thầy Cô, đồng hồ của Windows (`time.time()`) phụ thuộc vào giá trị ngày giờ hệ thống có thể bị thay đổi qua hàm Win32 `SetLocalTime` hoặc chỉnh trong BIOS. Nếu trẻ chỉnh lùi giờ lại 3 tiếng, hệ thống dùng `time.time()` sẽ bị lừa hoàn toàn.
  > 
  > Còn nếu dùng NTP Server từ Internet, khi trẻ rút dây mạng ra thì hệ thống mất mốc tham chiếu thời gian.
  > 
  > Do đó, `time.monotonic()` là lời giải tối ưu nhất vì nó đo trực tiếp xung nhịp đồng hồ phần cứng CPU (Hardware Time Stamp Counter), xung nhịp này chỉ tăng dần theo thời gian vật lý của máy tính và hoàn toàn độc lập với việc có mạng hay chỉnh lùi giờ hệ thống."

### ❓ Câu hỏi 3: "DNS Proxy chạy trên máy con có làm chậm tốc độ lướt web không?"
* **Trả lời sắc bén:**
  > "Thưa Thầy Cô, hoàn toàn không làm chậm mà ngược lại còn tối ưu hơn:
  > * Với các truy vấn bị chặn trong Blacklist: Proxy trả về bản ghi `0.0.0.0` ngay lập tức từ bộ nhớ RAM, thời gian phản hồi thực tế đo được chỉ là **0.83 mili-giây**, tức là nhanh hơn hàng chục lần so với việc gửi gói tin ra Internet.
  > * Với các truy vấn hợp lệ: Proxy chỉ đóng vai trò forwarder không đồng bộ tới Upstream DNS Cloudflare 1.1.1.3 qua Socket UDP thô hiệu năng cao, độ trễ tăng thêm chỉ ở mức dưới 2 mili-giây, người dùng hoàn toàn không cảm nhận được độ trễ này."
