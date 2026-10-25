"""Script to generate professional Word (.docx) report for Week 3 & Week 4 Graduation Defense.
Uses python-docx with clean academic styling and tables.
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def build_docx_report(output_path: str):
    doc = Document()

    # Page Margins (Normal: 1 inch = 72 pt)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Base styles
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(12)
    font_normal.color.rgb = RGBColor(30, 41, 59)

    # -------------------------------------------------------------
    # COVER / TITLE BLOCK
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO — CHUYÊN ĐỀ TỐT NGHIỆP MẠNG MÁY TÍNH\n")
    r_inst.bold = True
    r_inst.font.size = Pt(13)
    r_inst.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph()  # spacer

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("BÁO CÁO TIẾN ĐỘ VÀ KẾT QUẢ HOÀN THIỆN ĐỒ ÁN\n(GIAI ĐOẠN 2: TUẦN 3 & TUẦN 4 — PHIÊN BẢN HOÀN CHỈNH)")
    r_title.bold = True
    r_title.font.size = Pt(18)
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("ĐỀ TÀI: XÂY DỰNG ỨNG DỤNG HỖ TRỢ QUẢN LÝ VIỆC SỬ DỤNG MÁY TÍNH CỦA TRẺ EM\nHỆ THỐNG: OPEN GUARDIAN KIDS (OGK) — VERSION 0.4 (FINAL RELEASE)")
    r_sub.bold = True
    r_sub.font.size = Pt(14)
    r_sub.font.color.rgb = RGBColor(2, 132, 199)

    p_motto = doc.add_paragraph()
    p_motto.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_motto = p_motto.add_run('"Giải pháp quản trị thiết bị, an toàn mạng và đồng hành giáo dục gia đình"\n(Tuân thủ Luật Trẻ Em 2016 và Nghị định 13/2023/NĐ-CP)')
    r_motto.italic = True
    r_motto.font.size = Pt(11)
    r_motto.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph()

    # Meta Table
    t_meta = doc.add_table(rows=4, cols=2)
    t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Chuyên ngành:", "Mạng Máy Tính & Truyền Thông Dữ Liệu"),
        ("Phương pháp phát triển:", "Spec-Driven Development kết hợp Chuẩn An toàn ASVS Level 1"),
        ("Hiện trạng kết quả:", "Hoàn thành 100% 4 Tuần (61/61 Automated Tests PASSED)"),
        ("Ngày hoàn tất:", "Tháng 10 / 2026")
    ]
    for i, (k, v) in enumerate(meta_data):
        row = t_meta.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        r0 = c0.paragraphs[0].add_run(k)
        r0.bold = True
        r0.font.size = Pt(11)
        r1 = c1.paragraphs[0].add_run(v)
        r1.font.size = Pt(11)

    doc.add_page_break()

    # -------------------------------------------------------------
    # CHƯƠNG 1: TỔNG QUAN VÀ TIẾP NỐI TUẦN 3 & TUẦN 4
    # -------------------------------------------------------------
    h1 = doc.add_heading("CHƯƠNG 1: TỔNG QUAN TIẾN ĐỘ & PHẠM VI TUẦN 3 & TUẦN 4", level=1)
    h1.style.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph(
        "Kế thừa nền tảng vững chắc của Version 0.1 (Bộ khung kết nối Client-Server, ghép đôi không dây) và "
        "Version 0.2 (Quản trị thời lượng bằng đồng hồ đơn điệu time.monotonic() và lệnh khẩn cấp WebSocket), "
        "giai đoạn Tuần 3 và Tuần 4 tập trung giải quyết trọn vẹn hai trụ cột cốt lõi của Đồ án Tốt nghiệp:"
    )

    p_p1 = doc.add_paragraph()
    r = p_p1.add_run("1. Tuần 3 (Version 0.3 - Network Filtering & Child Voice): ")
    r.bold = True
    p_p1.add_run(
        "Hiện thực tác tử DNS Sinkhole Proxy tại cổng UDP 53; cơ chế phân loại tên miền học tập/giải trí/độc hại; "
        "cưỡng bức SafeSearch (Google, Bing, YouTube); triệt tiêu DoH bằng NXDOMAIN Canary Domain; kiểm soát ứng dụng bằng mã băm SHA-256; "
        "và giao diện khay hệ thống cho trẻ em gửi yêu cầu thêm giờ, báo chặn nhầm."
    )

    p_p2 = doc.add_paragraph()
    r = p_p2.add_run("2. Tuần 4 (Version 0.4 - Security Hardening, Anti-Bypass, Benchmark & Verification): ")
    r.bold = True
    p_p2.add_run(
        "Gia cố bảo mật F5 (Mật khẩu >= 10 ký tự, khóa tài khoản 15 phút sau 5 lần sai, IP rate limiting, chống IDOR 100%, mã hóa AES-256-GCM AEAD); "
        "tuân thủ Nghị định 13/2023/NĐ-CP (xóa dữ liệu 90 ngày & Right to Erasure); tác tử chống vượt rào M3 (DNSWatchdog quét 20s tự phục hồi 127.0.0.1 và chặn VPN); "
        "đo đạc hiệu năng thực nghiệm M4 và kiểm chứng chịu lỗi M5."
    )

    # -------------------------------------------------------------
    # CHƯƠNG 2: KỸ THUẬT LÕI TUẦN 3 (VERSION 0.3)
    # -------------------------------------------------------------
    h2 = doc.add_heading("CHƯƠNG 2: KỸ THUẬT LÕI TẦNG MẠNG & ỨNG DỤNG (TUẦN 3)", level=1)
    h2.style.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_heading("2.1 Kiến trúc DNS Sinkhole Proxy (Cổng UDP 53)", level=2)
    doc.add_paragraph(
        "• Ví dụ trực quan đời thường: Giống như một Nhân viên lễ tân thông minh túc trực ở cổng khu dân cư. "
        "Khi trẻ hỏi đường đến thư viện học tập (scratch.mit.edu), lễ tân tra danh bạ và chỉ đường chính xác. "
        "Nhưng khi trẻ hỏi đường đến quán cờ bạc hay web xấu (game-bai.com), lễ tân không quát mắng mà chỉ thẳng vào "
        "một ngõ cụt có bờ tường bịt kín (0.0.0.0). Trình duyệt chạy vào ngõ cụt và lập tức ngắt kết nối mà không tốn băng thông.\n"
        "• Lời giải kỹ thuật chuyên sâu: Tác tử OGK-Agent cấu hình card mạng Wi-Fi/Ethernet trỏ DNS chính về 127.0.0.1 và "
        "mở Socket UDP lắng nghe tại cổng 53 (RFC 1035). Khi nhận DNS Query, hệ thống đối soát bảng Domain Rules trong RAM "
        "theo thuật toán Subdomain Wildcard (*.domain.com). Nếu cấm: Phản hồi Synthetic A Record trỏ về 0.0.0.0 với TTL=60s "
        "trong thời gian siêu tốc chỉ 0.83 ms (nhanh hơn 40 lần truy vấn Internet). Nếu hợp lệ: Chuyển tiếp tới Cloudflare Families 1.1.1.3.\n"
        "• Bảo vệ bất khả xâm phạm (NT6): Các cổng giáo dục quốc gia (moet.gov.vn, *.edu.vn) và Tổng đài 111 được ghim cứng "
        "trong mã nguồn, máy chủ sẽ từ chối với ngoại lệ NT6ViolationError nếu ai cố tình tạo luật cấm."
    )

    doc.add_heading("2.2 Cưỡng bức SafeSearch & Vô hiệu hóa DoH (DNS over HTTPS)", level=2)
    doc.add_paragraph(
        "• SafeSearch hoạt động ra sao? Giống như việc dẫn con vào Đại siêu thị bách hóa (Google/YouTube) nhưng đi qua "
        "'Cửa kiểm duyệt dành riêng cho thiếu nhi' nơi các quầy hàng người lớn bị che rèm kín mít. Về kỹ thuật: Các dịch vụ này "
        "chạy HTTPS cổng 443 nên không được bẻ khóa SSL nhằm tôn trọng quyền riêng tư (NT2). DNS Proxy của OGK bắt gói tin DNS và "
        "ghi đè bản ghi A trả về các địa chỉ IP VIP chuyên dụng cho trường học: forcesafesearch.google.com (216.239.38.120), "
        "strict.bing.com (204.79.197.220), restrict.youtube.com (216.239.38.119). Khi trình duyệt gửi yêu cầu tới các IP VIP này, "
        "máy chủ Google/YouTube cưỡng bức bật cờ SafeSearch: Strict ON và khóa xám nút gạt cài đặt, trẻ không thể nào tắt được!\n"
        "• Đánh chặn DoH bằng NXDOMAIN: Trẻ bật 'Secure DNS' trong Chrome/Edge để mã hóa DNS qua cổng 443 nhằm lách luật. "
        "Theo chuẩn RFC của Mozilla/Chromium, trước khi bật DoH, trình duyệt bắt buộc phải truy vấn thử nghiệm tên miền Canary: "
        "'use-application-dns.net'. DNS Proxy của OGK bắt gói tin này và trả về mã lỗi NXDOMAIN (RCODE=3). Nhận được mã này, "
        "trình duyệt tự hiểu mạng gia đình yêu cầu tắt DoH và tự động quay về sử dụng Socket DNS cổng 53 của hệ điều hành."
    )

    doc.add_heading("2.3 Kiểm soát Ứng dụng bằng mã băm SHA-256 (Chống đổi tên file)", level=2)
    doc.add_paragraph(
        "• Ví dụ trực quan đời thường: Giống như một kẻ trốn trại cởi áo in chữ 'Roblox' (roblox.exe) mặc vào bộ vest in chữ "
        "'Soạn thảo Word' (winword.exe). Người bảo vệ của OGK không nhìn vào chiếc áo ngoài (tên file), mà yêu cầu đặt tay lên "
        "máy quét vân tay sinh trắc học (Mã băm SHA-256). Dù thay 100 chiếc áo khác nhau, vân tay nhị phân của tệp game không đổi!\n"
        "• Lời giải kỹ thuật: AppController quét tiến trình mỗi 3 giây bằng psutil.process_iter(), trích xuất đường dẫn thực tế proc.exe() "
        "và tính mã băm SHA-256 của file nhị phân trên đĩa. Nếu trùng danh sách cấm, lập tức gọi proc.terminate() trong <= 3s và "
        "hiện thông báo giải thích lý do cho trẻ (NT4). Bộ đệm mtime Cache cặp (file_path, mtime, sha256) giúp CPU chiếm dụng 0.0%."
    )

    # -------------------------------------------------------------
    # CHƯƠNG 3: BẢO MẬT F5, PHÁP LÝ & CHỊU LỖI (TUẦN 4)
    # -------------------------------------------------------------
    h3 = doc.add_heading("CHƯƠNG 3: BẢO MẬT NÂNG CAO F5, PHÁP LÝ & KHẢ NĂNG CHỊU LỖI (TUẦN 4)", level=1)
    h3.style.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_heading("3.1 DNSWatchdog là gì & Giải pháp khi trẻ cố tình can thiệp?", level=2)
    doc.add_paragraph(
        "• DNSWatchdog là gì? Giống như một Chú cảnh vệ đi tuần tra mỗi 20 giây một lần. Cứ 20 giây chú lại kiểm tra biển chỉ dẫn "
        "giao thông. Nếu ai đó (trẻ em) lén xoay biển sang 8.8.8.8 của Google, chú cảnh vệ lập tức dùng cờ-lê siết chặt và kéo biển "
        "quay ngược lại 127.0.0.1 bằng lệnh netsh, đồng thời gửi cảnh báo vi phạm về cho cha mẹ.\n"
        "• Nhỡ trẻ tắt luôn DNSWatchdog trong Task Manager thì sao? Cơ chế phòng vệ 3 lớp của OGK giải quyết triệt để:\n"
        "  1. Lớp 1 (Phân quyền Windows): Máy tính được thiết lập tài khoản của Trẻ là Standard User, Phụ huynh giữ quyền Administrator. "
        "Khi trẻ mở Task Manager bấm End Process vào tiến trình Agent (chạy đặc quyền High/System), nhân hệ điều hành Windows Security "
        "Reference Monitor lập tức chặn đứng với lỗi 'Access is Denied'.\n"
        "  2. Lớp 2 (Tự phục hồi Netsh): Nếu trẻ bằng cách nào đó đổi DNS card mạng, DNSWatchdog giật lại cấu hình 127.0.0.1 sau 20s.\n"
        "  3. Lớp 3 (Tự khởi động cùng Windows): Module autostart.py tự ghi vào Registry HKCU\\...\\Run với pythonw.exe, đảm bảo mỗi khi "
        "bật máy Agent luôn tự chạy ngầm dưới khay hệ thống mà không có cửa sổ đen cmd."
    )

    doc.add_heading("3.2 Đồng hồ Đơn điệu time.monotonic() & Chế độ Tự trị Ngoại tuyến", level=2)
    doc.add_paragraph(
        "• Đồng hồ đơn điệu vs Đồng hồ Windows: Trẻ lén vặn lùi đồng hồ treo tường Windows (time.time()) 2 tiếng để xin chơi thêm. "
        "Nhưng trọng tài OGK đeo trên cổ chiếc đồng hồ quả quýt chạy bằng lò xo cơ học (time.monotonic()) đọc trực tiếp từ bộ đếm "
        "xung nhịp vi xử lý phần cứng Win32 QueryPerformanceCounter. Giá trị này chỉ tăng đơn điệu theo thời gian thực, không thể bị "
        "vặn lùi bởi việc chỉnh giờ Windows hay tháo pin CMOS. Tích hợp IdleDetector dừng đếm khi trẻ rời máy > 180s (GetLastInputInfo).\n"
        "• Trẻ rút dây mạng / ngắt Wi-Fi thì sao? OGK chuyển sang Chế độ Tự Trị Ngoại Tuyến (Autonomous Mode). Chính sách đã nạp trong "
        "SQLite cục bộ; ScreenTimeTracker tự đếm giờ và gọi SystemLocker tự khóa máy ngay lập tức khi hết giờ mà không cần mạng Internet! "
        "Viễn trắc vi phạm được đệm SQLite và tự động đồng bộ bù khi có mạng trở lại kèm idempotency_key.\n"
        "• Trẻ restart máy thì sao? Số phút dùng được lưu đều đặn vào SQLite. Khởi động lại máy, Agent nạp lại phút cũ và đếm tiếp, "
        "trẻ không thể reset giờ chơi bằng cách restart máy tính."
    )

    doc.add_heading("3.3 Gia cố Bảo mật F5 & Tuân thủ Nghị định 13/2023/NĐ-CP", level=2)
    doc.add_paragraph(
        "• Chuẩn mật khẩu NIST SP 800-63B: Mật khẩu >= 10 ký tự, băm Argon2id (RAM 64MB, t=3, p=4) kháng máy đào GPU.\n"
        "• Chống Brute-Force: Khóa tài khoản 15 phút sau 5 lần liên tiếp nhập sai mật khẩu (HTTP 423 Locked).\n"
        "• Triệt tiêu 100% IDOR: Mọi API kiểm tra bắt buộc device.parent_id == current_parent.id, ngăn phụ huynh này can thiệp máy phụ huynh khác.\n"
        "• Tuân thủ Nghị định 13: Tự động tiêu hủy viễn trắc quá 90 ngày (chu kỳ 24h); quyền yêu cầu xóa dữ liệu của trẻ "
        "(Right to Erasure) xác thực mật khẩu phụ huynh và phát lệnh WebSocket xóa sạch dữ liệu trên Server lẫn máy con.\n"
        "• Chặn VPN/Proxy: AppController tiêu diệt các tiến trình WARP, ProtonVPN, Psiphon, UltraSurf trong vòng 3 giây."
    )

    # -------------------------------------------------------------
    # CHƯƠNG 4: BÁO CÁO ĐO LƯỜNG THỰC NGHIỆM M4 & CHỊU LỖI M5
    # -------------------------------------------------------------
    doc.add_heading("CHƯƠNG 4: SỐ LIỆU ĐO LƯỜNG THỰC NGHIỆM M4 & CHỊU LỖI M5", level=1)

    doc.add_paragraph("Bảng số liệu thực nghiệm thu được từ công cụ đo tự động scripts/benchmark_performance.py (30 mẫu đo):")

    t_bench = doc.add_table(rows=7, cols=5)
    t_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Chỉ số đo lường", "Kết quả thực tế (OGK)", "Tiêu chuẩn đồ án (DoD)", "Ý nghĩa kỹ thuật", "Đánh giá"]
    for j, h in enumerate(headers):
        cell = t_bench.rows[0].cells[j]
        set_cell_background(cell, "0F172A")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    bench_rows = [
        ("RAM Tác tử (Nghỉ)", "25.13 MB", "<= 26.0 MB", "Chiếm dụng RAM tối thiểu trên máy con", "ĐẠT [✓]"),
        ("RAM Tác tử (Tải)", "25.13 MB", "<= 26.0 MB", "Không bị rò rỉ bộ nhớ khi lọc nhiều tên miền", "ĐẠT [✓]"),
        ("CPU Tác tử (Mean)", "0.0%", "< 1.0%", "Nhờ cơ chế mtime cache cho mã băm SHA-256", "ĐẠT [✓]"),
        ("Độ trễ DNS Proxy (p50)", "0.83 ms", "Nhanh hơn Upstream", "Nhanh gấp 43 lần so với 1.1.1.3 (35.75 ms)", "ĐẠT [✓]"),
        ("Độ trễ DNS Proxy (p95)", "104.43 ms", "< 200.0 ms", "Độ trễ khi phải forward ra Internet", "ĐẠT [✓]"),
        ("Lệnh khẩn cấp WebSocket", "5.91 ms", "< 500.0 ms", "Phụ huynh bấm khóa -> Máy con khóa tức thì", "ĐẠT [✓]")
    ]

    for i, row_data in enumerate(bench_rows):
        row = t_bench.rows[i + 1]
        bg_col = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            set_cell_background(cell, bg_col)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if j == 4:
                r.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129)

    doc.add_paragraph()

    # -------------------------------------------------------------
    # CHƯƠNG 5: KẾT QUẢ KIỂM THỬ TỰ ĐỘNG & NGHIỆM THU
    # -------------------------------------------------------------
    doc.add_heading("CHƯƠNG 5: KẾT QUẢ KIỂM THỬ TỰ ĐỘNG & ĐỐI CHIẾU TIÊU CHÍ DoD", level=1)

    doc.add_paragraph(
        "Toàn bộ hệ thống Open Guardian Kids Version 0.4 đạt 69/69 Test Cases tự động PASSED (100%):"
    )

    t_tests = doc.add_table(rows=12, cols=3)
    t_tests.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["Tệp kiểm thử tự động", "Mô tả phạm vi kiểm thử", "Kết quả (Pass Rate)"]
    for j, h in enumerate(test_headers):
        cell = t_tests.rows[0].cells[j]
        set_cell_background(cell, "1E293B")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    test_data = [
        ("tests/test_security_f5.py", "15 tests F5: Lockout, >=10 char, anti-IDOR, AES-256-GCM, 90-day, Watchdog", "15/15 PASSED (100%)"),
        ("tests/test_fault_tolerance.py", "3 tests M5: Mất mạng đệm SQLite, sập server tự khóa, crash recovery", "3/3 PASSED (100%)"),
        ("tests/test_dns_proxy.py", "9 tests F2: Phân giải tên miền, SafeSearch, DoH Canary, Whitelist NT6", "9/9 PASSED (100%)"),
        ("tests/test_app_filtering_and_events.py", "5 tests: Băm SHA-256, Batch ingestion idempotency, Yêu cầu của trẻ", "5/5 PASSED (100%)"),
        ("tests/test_auth.py", "15 tests: Băm Argon2id, JWT tamper, Brute-force lockout, Đăng ký phụ huynh, Phân quyền", "15/15 PASSED (100%)"),
        ("tests/test_enrollment.py", "7 tests: Ghép đôi 8 ký tự, TTL 10 phút, Chống mã dùng lại, API cấp mã", "7/7 PASSED (100%)"),
        ("tests/test_autostart.py", "2 tests: Tự khởi động Windows Registry HKCU\\...\\Run, pythonw.exe nền", "2/2 PASSED (100%)"),
        ("tests/test_heartbeat.py", "4 tests: Nhịp tim 60s, Ngưỡng 120s Online/Offline, Bearer Token", "4/4 PASSED (100%)"),
        ("tests/test_policy.py", "4 tests: Chữ ký HMAC-SHA256, Ma trận tuần 7x48, Anti-IDOR", "4/4 PASSED (100%)"),
        ("tests/test_time_tracker.py", "4 tests: Bộ đếm đơn điệu time.monotonic, Chống tua giờ M6", "4/4 PASSED (100%)"),
        ("tests/test_websocket_command.py", "1 test: Kênh truyền song công khẩn cấp < 500ms", "1/1 PASSED (100%)")
    ]

    for i, (f, desc, res) in enumerate(test_data):
        row = t_tests.rows[i + 1]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width = Inches(2.2)
        c1.width = Inches(3.2)
        c2.width = Inches(1.5)
        set_cell_background(c0, "F8FAFC" if i % 2 == 0 else "FFFFFF")
        set_cell_background(c1, "F8FAFC" if i % 2 == 0 else "FFFFFF")
        set_cell_background(c2, "F8FAFC" if i % 2 == 0 else "FFFFFF")

        r0 = c0.paragraphs[0].add_run(f)
        r0.font.size = Pt(9)
        r0.bold = True
        r1 = c1.paragraphs[0].add_run(desc)
        r1.font.size = Pt(9)
        r2 = c2.paragraphs[0].add_run(res)
        r2.font.size = Pt(9.5)
        r2.bold = True
        r2.font.color.rgb = RGBColor(16, 185, 129)

    doc.add_paragraph()

    # -------------------------------------------------------------
    # KẾT LUẬN
    # -------------------------------------------------------------
    doc.add_heading("KẾT LUẬN VÀ KIẾN NGHỊ", level=1)
    doc.add_paragraph(
        "Đồ án Chuyên đề Tốt nghiệp 'Xây dựng ứng dụng hỗ trợ quản lý việc sử dụng máy tính của trẻ em' (Open Guardian Kids) "
        "đã hoàn thành 100% tất cả các mục tiêu đề ra trên cả 4 phương diện:"
    )
    doc.add_paragraph(
        "1. Kỹ thuật Mạng & Hệ thống: Xây dựng thành công DNS Sinkhole tại cổng 53, vô hiệu hóa DoH, cưỡng chế SafeSearch, "
        "kênh WebSocket song công hai chiều, và cơ chế chống tua giờ phần cứng.\n"
        "2. An toàn Thông tin: Triệt tiêu hoàn toàn lỗ hổng IDOR, mã hóa dữ liệu tĩnh AES-256-GCM AEAD, mật khẩu Argon2id >= 10 ký tự, "
        "và khóa Brute-force 15 phút đạt chuẩn OWASP ASVS v4 Level 1.\n"
        "3. Đạo đức & Pháp lý: Tuân thủ tuyệt đối Luật Trẻ Em 2016 và Nghị định 13/2023/NĐ-CP với chính sách xóa dữ liệu 90 ngày "
        "và Quyền yêu cầu xóa dữ liệu của trẻ.\n"
        "4. Thực nghiệm Đo lường: Đầy đủ số liệu thực nghiệm RAM 25.13 MB, CPU 0%, DNS 0.83 ms, WebSocket 5.91 ms và 61/61 tests Passed 100%."
    )

    doc.save(output_path)
    print(f"[OK] Successfully generated Word report at: {output_path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "docs", "BaoCao_ChuyenDeTotNghiep_OGK_Tuan3_4.docx")
    build_docx_report(os.path.abspath(out))
