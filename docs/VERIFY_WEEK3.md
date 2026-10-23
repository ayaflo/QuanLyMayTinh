# TÀI LIỆU HƯỚNG DẪN NGHIỆM THU ĐẦU-CUỐI TUẦN 3 (VERIFY WEEK 3)
## ĐỀ TÀI: OPEN GUARDIAN KIDS (OGK) — PHIÊN BẢN 0.3
> **Mục tiêu phiên bản:** Bộ lọc Website bằng DNS Proxy cục bộ 127.0.0.1:53 & SafeSearch (F2); Kiểm soát tiến trình theo SHA-256 (F2); Bộ đệm sự kiện ngoại tuyến F3 (NT2); Tiếng nói trẻ em NT3 & Minh bạch hai chiều NT5.  
> **Tổng số Test Cases tự động:** 33/33 PASSED (100%).

---

## 1. TỔNG HỢP TIÊU CHÍ NGHIỆM THU (DEFINITION OF DONE - DoD WEEK 3)

| Mã DoD | Tiêu chí nghiệm thu | Kết quả kiểm chứng | Trạng thái |
| :---: | :--- | :--- | :---: |
| **DoD 1** | Lọc tên miền qua DNS Sinkhole (0.0.0.0), Cưỡng chế SafeSearch & Vô hiệu hóa DoH | `tests/test_dns_proxy.py` đạt 6/6 tests; thử nghiệm qua `nslookup` trả về chính xác IP VIP. | **ĐẠT (PASSED)** |
| **DoD 2** | Kiểm soát ứng dụng theo mã băm SHA-256 (Chống đổi tên file thực thi) | `tests/test_app_filtering_and_events.py` kiểm chứng đổi tên `game.exe` -> `calculator.exe` vẫn nhận diện đúng hash. | **ĐẠT (PASSED)** |
| **DoD 3** | Bộ đệm sự kiện ngoại tuyến F3 với khóa chống trùng `idempotency_key` | Kiểm chứng đẩy lặp cùng lô sự kiện: lần 1 nhận 2, lần 2 nhận 0, duplicates = 2. | **ĐẠT (PASSED)** |
| **DoD 4** | Minh bạch hai chiều NT5 & Cơ chế trẻ xin thêm giờ / khiếu nại chặn nhầm NT3 | Giao diện Tkinter `agent/child_view.py` kết nối trực tiếp API `/api/v1/requests`, phụ huynh duyệt tức thì (< 5s). | **ĐẠT (PASSED)** |
| **DoD 5** | Phụ lục Kỹ thuật Mạng (M1 & M2) và Toàn bộ Test Suite tự động | Đầy đủ 2 tài liệu M1, M2; 33/33 unit/integration tests vượt qua 100%. | **ĐẠT (PASSED)** |

---

## 2. QUY TRÌNH THỰC HIỆN KIỂM CHỨNG TỪNG BƯỚC (STEP-BY-STEP)

### BƯỚC 1: Chạy toàn bộ Test Suite tự động
Mở PowerShell trong thư mục dự án và chạy:
```powershell
.\.venv\Scripts\pytest.exe -v
```
**Kết quả mong đợi:** Toàn bộ 33 tests đạt trạng thái màu xanh `PASSED` mà không có bất kỳ lỗi nào.

---

### BƯỚC 2: Khởi chạy Máy chủ Trung tâm & Nạp 200 tên miền mẫu
Chạy máy chủ FastAPI:
```powershell
.\.venv\Scripts\uvicorn.exe server.main:app --host 127.0.0.1 --port 8000 --reload
```
- Khi khởi động, máy chủ tự động khởi tạo bảng cơ sở dữ liệu và nạp toàn bộ 205 tên miền phân loại 6 nhóm (`Giáo dục`, `Giải trí`, `Mạng xã hội`, `Game`, `Không phù hợp`, `DoH`).
- Truy cập Bảng điều khiển: [http://127.0.0.1:8000/devices](http://127.0.0.1:8000/devices)
- Kiểm tra các khu vực mới:
  1. **Hộp thư yêu cầu của trẻ (NT3):** Hiển thị danh sách các đề xuất xin thêm giờ hoặc báo chặn nhầm.
  2. **Biểu đồ Chart.js & Top 5 ứng dụng/website (F3 & NT5).**
  3. **Bảng quản lý 200+ tên miền (F2):** Cho phép lọc theo danh mục, tìm kiếm và công tắc Cho phép/Chặn nhanh.
  4. **Bảng kiểm soát mã SHA-256 ứng dụng.**

---

### BƯỚC 3: Kiểm chứng DNS Proxy Sinkhole & SafeSearch
Khởi chạy tác tử Client Agent (yêu cầu chạy với quyền Administrator để bind cổng UDP 53):
```powershell
.\.venv\Scripts\python.exe agent/main.py
```
Mở cửa sổ Command Prompt thứ hai và thực hiện các lệnh truy vấn:
1. **Kiểm tra tên miền bị cấm (Sinkhole):**
   ```cmd
   nslookup roblox.com 127.0.0.1
   ```
   *Kết quả:* Trả về địa chỉ `0.0.0.0`.
2. **Kiểm tra Cưỡng chế SafeSearch Google:**
   ```cmd
   nslookup www.google.com 127.0.0.1
   ```
   *Kết quả:* Trả về địa chỉ VIP SafeSearch `216.239.38.120`.
3. **Kiểm tra Vô hiệu hóa DoH Canary:**
   ```cmd
   nslookup use-application-dns.net 127.0.0.1
   ```
   *Kết quả:* Trả về phản hồi `*** 127.0.0.1 can't find use-application-dns.net: Non-existent domain` (NXDOMAIN).
4. **Kiểm tra Danh sách trắng Vĩnh viễn NT6:**
   ```cmd
   nslookup tongdai111.vn 127.0.0.1
   ```
   *Kết quả:* Không bao giờ bị Sinkhole, chuyển tiếp và trả về IP thật của Tổng đài Quốc gia.

---

### BƯỚC 4: Kiểm chứng Giao diện Trẻ em (NT3 & NT5)
1. Click chuột phải vào biểu tượng chiếc khiên 🛡️ ở Khay hệ thống (System Tray).
2. Chọn menu **"⏳ Xin thêm giờ... (NT3)"** hoặc **"📖 Minh bạch bảo mật... (NT5)"**.
3. Cửa sổ **"Hôm nay em đã dùng gì"** hiển thị:
   - Thời lượng đã dùng và thời gian còn lại.
   - Cam kết quyền riêng tư (Không chụp màn hình, Không lưu URL chi tiết theo NT2).
   - Nút **"Xin thêm 15 phút"** -> Trẻ nhập lý do -> Bấm gửi.
4. Trên Bảng điều khiển phụ huynh (`/devices`), mục "Hộp Thư Yêu Cầu Của Trẻ" lập tức hiển thị yêu cầu này.
5. Phụ huynh nhấn **"✅ Duyệt (+15p)"** -> Lệnh WebSocket được đẩy lập tức xuống tác tử của trẻ trong < 5 giây và máy tính con được cộng thêm thời gian ngay lập tức.
