# PHỤ LỤC M5: BÁO CÁO KỸ THUẬT MẠNG — KIỂM CHỨNG KHẢ NĂNG CHỊU LỖI, BẢO TOÀN DỮ LIỆU NGOẠI TUYẾN VÀ ĐỒNG BỘ PHỤC HỒI
## ĐỀ TÀI: OPEN GUARDIAN KIDS (OGK) — PHIÊN BẢN 0.4 (FINAL RELEASE)
> **Chuyên ngành:** Mạng máy tính & Truyền thông dữ liệu  
> **Mã phân mục:** `M5` / Tính năng lõi `F1` (Screen Time), `F3` (Telemetry) & `F4` (Policy Sync)  
> **Tệp kiểm thử tự động xác minh:** [`tests/test_fault_tolerance.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/tests/test_fault_tolerance.py)  

---

## 1. ĐẶT VẤN ĐỀ VÀ THIẾT KẾ CHỊU LỖI TRONG MÔI TRƯỜNG MẠNG GIA ĐÌNH

Trong hệ thống phân tán Client-Server triển khai tại mạng gia đình, sự cố gián đoạn đường truyền là điều tất yếu:
- Router Wi-Fi gia đình bị mất kết nối Internet hoặc khởi động lại.
- Trẻ em cố tình rút dây mạng Ethernet hoặc tắt Wi-Fi để vô hiệu hóa sự giám sát của máy chủ.
- Máy chủ quản lý trung tâm bị sập nguồn, quá tải hoặc bảo trì cập nhật.
- Máy tính của trẻ bị sập nguồn đột ngột do hết pin hoặc trẻ tắt nóng bằng nút nguồn.

Một hệ thống quản lý lỏng lẻo sẽ gặp các lỗi nghiêm trọng:
1. **Mất mát dữ liệu kiểm toán (Data Loss):** Các sự kiện mở ứng dụng cấm, truy cập web độc hại diễn ra lúc mất mạng bị biến mất.
2. **Tạo lỗ hổng lách luật (Offline Bypass):** Khi mất kết nối với máy chủ, bộ đếm giờ không thể cập nhật khiến trẻ có thể dùng máy tính vô tội vạ mà không bị khóa.
3. **Mất trạng thái (State Inconsistency):** Khởi động lại máy làm bộ đếm giờ reset về 0, cho phép trẻ "chơi lại từ đầu".

Hệ thống **Open Guardian Kids (OGK)** được thiết kế theo nguyên lý **Chịu lỗi chủ động (Resilience-by-Design)** với 3 trụ cột kỹ thuật:

```mermaid
flowchart TD
    subgraph Client Agent [Tác tử Máy Con (Offline-First)]
        A[Sự kiện Mới / Đếm giờ / Quét App] --> B[Lưu tức thì vào SQLite WAL Mode]
        B --> C[(CSDL Cục bộ agent_cache.db)]
        C --> D{Kiểm tra Kết nối Server}
    end

    subgraph Central Server [Máy Chủ Trung Tâm]
        E[API Ingest Batch / Policy / Command]
        F[(CSDL PostgreSQL / SQLite WAL)]
    end

    D -->|Mạng Offline / Lỗi 503| G[Giữ nguyên bộ đệm pending_events]
    D -->|Mạng Bình thường| H[Đẩy lô Batch Sync qua HTTP POST]
    H --> E
    E -->|Khử trùng lặp Idempotency| F
    E -->|Phản hồi HTTP 200| I[Xóa bản ghi đã gửi khỏi pending_events]
```

---

## 2. PHÂN TÍCH VÀ KIỂM CHỨNG 3 KỊCH BẢN CHỊU LỖI CỐT LÕI (M5)

---

### KỊCH BẢN 1: MẤT KẾT NỐI MẠNG & BỘ ĐỆM BẢO TOÀN DỮ LIỆU (NETWORK LOSS & RESILIENT BUFFERING)

#### 1. Cơ chế kỹ thuật:
- **Bộ đệm ngoại tuyến SQLite ([`agent/event_collector.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/event_collector.py)):**
  - Mọi sự kiện đo đạc (sử dụng ứng dụng `app_usage`, truy cập web `web_access`, vi phạm app cấm `blocked_app`, hoặc cảnh báo can thiệp DNS `tamper_attempt`) trước tiên được gắn một khóa định danh duy nhất **UUID v4 (`idempotency_key`)** và lưu trực tiếp vào bảng `pending_events` trong CSDL SQLite cục bộ.
- **Cơ chế truyền tin bảo đảm (At-Least-Once Delivery):**
  - Luồng `EventCollector` định kỳ 15 giây gom tối đa 100 sự kiện từ `pending_events` gửi lên `POST /api/v1/events/batch`.
  - **Nếu mất mạng (`ConnectionError`, DNS failure, hoặc timeout):** Hàm `flush_batch()` bắt ngoại lệ an toàn, trả về 0 và **tuyệt đối không xóa bất kỳ bản ghi nào** trong `pending_events`.
  - **Khi kết nối mạng được tái lập:** Toàn bộ dữ liệu tích lũy được đẩy lên máy chủ thành công trong một đợt đồng bộ duy nhất.
- **Bảo đảm tính lũy kết ở máy chủ (Idempotency Enforced on Server):**
  - Máy chủ kiểm tra trường `idempotency_key` (có chỉ mục Unique). Nếu tác tử gửi lại cùng một gói tin do mất mạng chập chờn, máy chủ tự động bỏ qua các bản ghi đã nhận trước đó mà không ném lỗi (trả về `duplicates > 0, status="success"`), ngăn chặn hoàn toàn việc nhân bản số liệu thống kê.

#### 2. Kết quả kiểm chứng tự động:
- Đã kiểm chứng tại test case `test_network_loss_event_buffering_and_idempotent_recovery` trong [`tests/test_fault_tolerance.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/tests/test_fault_tolerance.py):
  - Tạo 5 sự kiện khi mạng bị ngắt: CSDL cục bộ lưu đủ 5 bản ghi.
  - Thử đẩy batch: Thất bại, bộ đệm vẫn bảo toàn nguyên vẹn 5 bản ghi.
  - Khôi phục mạng: Đồng bộ thành công 5 bản ghi, bộ đệm cục bộ tự động dọn sạch về 0.
  - Thử truyền lại batch cũ: Máy chủ phát hiện 5/5 bản ghi trùng lặp và loại trừ chính xác.

---

### KỊCH BẢN 2: MÁY CHỦ SẬP / NGỪNG HOẠT ĐỘNG & THỰC THI HẠN MỨC ĐỘC LẬP (SERVER OUTAGE & AUTONOMOUS ENFORCEMENT)

#### 1. Cơ chế kỹ thuật:
- **Bộ nhớ đệm chính sách có chữ ký số ([`agent/storage.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/agent/storage.py)):**
  - Tác tử lưu trữ bản sao chính sách hạn mức mới nhất trong bảng `policy_cache`. Bản sao này bao gồm hạn mức ngày trong tuần (`weekday_quota_minutes`), ngày cuối tuần (`weekend_quota_minutes`), ma trận lịch học tập (`schedule_matrix`), và chữ ký xác thực toàn vẹn `hmac_signature`.
- **Cưỡng chế ngoại tuyến độc lập (Autonomous Offline Enforcement):**
  - Bộ đếm giờ `ScreenTimeTracker` hoạt động độc lập bằng đồng hồ đơn điệu phần cứng `time.monotonic()`.
  - Khi máy chủ bị sập hoặc trẻ cố tình rút cáp mạng Internet để cô lập máy tính:
    1. Tác tử vẫn tiếp tục đọc hạn mức từ `policy_cache` nội bộ.
    2. Thời gian sử dụng màn hình tiếp tục được cộng dồn chính xác.
    3. Ngay khi tổng thời gian sử dụng vượt quá hạn mức ngày ($T_{used} \ge \text{Quota}$), tác tử tự động phát cờ cảnh báo và gọi API Win32 `LockWorkStation` để **khóa chặt màn hình máy tính ngay lập tức**.
  - **Ý nghĩa thực tiễn:** Trẻ hoàn toàn không thể lách luật bằng chiêu trò "ngắt mạng để phần mềm không khóa được máy".

#### 2. Kết quả kiểm chứng tự động:
- Đã kiểm chứng tại test case `test_server_outage_offline_quota_enforcement` trong [`tests/test_fault_tolerance.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/tests/test_fault_tolerance.py):
  - Máy chủ hoàn toàn không hoạt động.
  - Tác tử nạp chính sách 60 phút từ bộ đệm cục bộ. Trẻ dùng đạt 3605 giây (> 3600 giây).
  - Tác tử lập tức kích hoạt sự kiện `on_lock_trigger` khóa màn hình và cập nhật trường `is_locked = 1` xuống SQLite.

---

### KỊCH BẢN 3: TẮT MÁY ĐỘT NGỘT / KHỞI ĐỘNG LẠI MÁY (SUDDEN REBOOT & CRASH RECOVERY)

#### 1. Cơ chế kỹ thuật:
- **Cơ chế ghi bền vững SQLite WAL (Write-Ahead Logging):**
  - Tác tử cập nhật bảng `daily_usage` định kỳ mỗi phút hoặc ngay khi có thay đổi hạn mức/thời gian thưởng/khóa máy.
  - Chế độ ghi nhật ký trước `PRAGMA journal_mode=WAL` bảo đảm dữ liệu ghi xuống đĩa có tính nguyên tử (**ACID Compliance**), không bị hỏng file CSDL (Corrupted Database) kể cả khi máy tính bị rút phích cắm điện đột ngột.
- **Quy trình phục hồi khi khởi động (Startup State Recovery):**
  - Khi máy tính khởi động lại và tác tử được nạp lên:
    1. Hàm `_load_today_usage()` được gọi ngay trong constructor của `ScreenTimeTracker`.
    2. Tác tử truy vấn bảng `daily_usage` theo ngày hiện tại (`YYYY-MM-DD`).
    3. Đọc lại nguyên vẹn số giây đã sử dụng `used_seconds`, số phút thưởng `bonus_minutes`, và cờ trạng thái `is_locked`.
    4. **Nếu trước khi tắt máy thiết bị đã bị khóa (`is_locked = 1`):** Bộ đếm giờ khởi tạo ngay lập tức với cờ `is_locked = True` và phát lệnh khóa màn hình ngay khi Windows vừa vào Desktop, ngăn trẻ khởi động lại máy để được chơi tiếp.

#### 2. Kết quả kiểm chứng tự động:
- Đã kiểm chứng tại test case `test_crash_reboot_recovery_preserves_daily_usage` trong [`tests/test_fault_tolerance.py`](file:///d:/CD%20TN%20MMT/QuanLyMayTinh/tests/test_fault_tolerance.py):
  - Thiết lập trạng thái trước sập: Dùng 2700 giây (45 phút), thưởng 15 phút, trạng thái `is_locked = 1`.
  - Giả lập tắt tiến trình và khởi tạo một đối tượng `ScreenTimeTracker` hoàn toàn mới sau khởi động.
  - Kết quả: `used_seconds` phục hồi chính xác 2700 giây (không bị reset về 0), `is_locked` giữ nguyên giá trị `True`.

---

## 3. BẢNG TỔNG HỢP NĂNG LỰC CHỊU LỖI VÀ BẢO TOÀN DỮ LIỆU CỦA OGK

| Kịch bản sự cố | Tác động tiềm ẩn | Cơ chế tự bảo vệ & Phục hồi của OGK | Kết quả kiểm chứng |
| :--- | :--- | :--- | :---: |
| **Mất kết nối Internet** | Sự kiện bị rơi rớt, không gửi được về Server | Đệm tức thì vào bảng `pending_events` (SQLite WAL). Tự động đồng bộ hàng loạt khi có mạng lại. | **100% Không mất dữ liệu [✓]** |
| **Gửi lại gói tin trùng lặp** | Sai lệch báo cáo, số phút sử dụng bị nhân đôi | Khóa định danh `idempotency_key` (UUID v4) độc nhất cho từng sự kiện. Server lọc trùng lặp tự động. | **Bảo toàn tính lũy kết [✓]** |
| **Máy chủ trung tâm sập** | Tác tử không biết chính sách, không khóa được máy | Tác tử vận hành tự quản (Autonomous) dựa trên `policy_cache` cục bộ có chữ ký HMAC. Khóa máy đúng giờ. | **Khóa máy chính xác [✓]** |
| **Trẻ rút dây mạng để lách giờ** | Cố tình tạo lỗi mạng để chơi game quá giờ | Cơ chế đếm giờ đơn điệu `time.monotonic()` độc lập với mạng. Hết giờ vẫn khóa bình thường. | **Không thể vượt rào [✓]** |
| **Khởi động lại / Sập nguồn** | Bộ đếm giờ bị xóa sạch về 0 giây | CSDL `daily_usage` lưu trạng thái tức thì. Khởi động lại nạp đúng số phút đã dùng và duy trì khóa. | **Khôi phục nguyên vẹn [✓]** |

---

## 4. KẾT LUẬN CHUYÊN NGÀNH MẠNG MÁY TÍNH

Khả năng chịu lỗi của Open Guardian Kids chứng minh sự kết hợp hoàn hảo giữa triết lý **Kiến trúc hướng ngoại tuyến (Offline-First Architecture)** và **Đồng bộ lũy kết phân tán (Idempotent Distributed Synchronization)**:
- Hệ thống không phụ thuộc mù quáng vào kết nối mạng liên tục (Zero SPOF - Single Point of Failure).
- Dữ liệu lịch sử máy tính được bảo toàn 100% trong mọi tình huống đứt gãy truyền thông.
- Việc cưỡng chế chính sách phụ huynh diễn ra nghiêm ngặt, công bằng và không thể bị thao túng bởi các sự cố mạng nhân tạo.
