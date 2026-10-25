# BỘ 400 CÂU HỎI - ĐÁP PHẢN BIỆN BẢO VỆ ĐỒ ÁN TỐT NGHIỆP: OPEN GUARDIAN KIDS (OGK)
## TÀI LIỆU VẤN ĐÁP PHÒNG VỆ CHUYÊN SÂU PHẦN 2: TUẦN 3 & TUẦN 4 (SLIDE 21 ĐẾN SLIDE 40)
### PHIÊN BẢN HOÀN THIỆN ĐỒ ÁN TỐT NGHIỆP (VERSION 0.4 - FINAL GRADUATION RELEASE)

> **Bối cảnh tình huống thực tế:**  
> Giảng viên hướng dẫn và các Thầy/Cô trong Hội đồng phản biện chỉ tay trực tiếp vào các hình vẽ, thuật toán phân giải tên miền, cơ chế băm nhị phân SHA-256, chuẩn mật mã AES-256-GCM AEAD, điều khoản Nghị định 13/2023/NĐ-CP, báo cáo hiệu năng M4 và kết quả kiểm thử tự động trên từng Slide để chất vấn sinh viên.  
> Tiếp nối Phần 1 (Câu 1 đến Câu 400 của Slide 1 – Slide 20 trong `docs/HOI_DAP_PHAN_BIEN_20_SLIDES.md`), Phần 2 trang bị trọn vẹn **400 câu hỏi hóc búa nhất (Câu 401 đến Câu 800)** tương ứng đúng 20 câu hỏi cho mỗi trang Slide từ Slide 21 đến Slide 40. Mọi câu trả lời đều trực diện, tự tin, mang chiều sâu kỹ thuật mạng chuyên ngành, dẫn chứng chính xác vào từng tệp mã nguồn, thông số thực nghiệm và tiêu chuẩn quốc tế.

---

# MỤC LỤC 20 SLIDE BÁO CÁO PHẦN 2 (SLIDE 21 – SLIDE 40)

* [SLIDE 21: Trang Tiêu Đề Báo Cáo Giai Đoạn 2 (Version 0.3 & Version 0.4) (Câu 401 - 420)](#slide-21-trang-tiêu-đề-báo-cáo-giai-đoạn-2-version-03--version-04-câu-401---420)
* [SLIDE 22: Tổng Quan Khối Lượng Đồ Án (Tuần 3 & Tuần 4) (Câu 421 - 440)](#slide-22-tổng-quan-khối-lượng-đồ-án-tuần-3--tuần-4-câu-421---440)
* [SLIDE 23: Kỹ Thuật Lõi 1 (F2 & M1): Kiến Trúc DNS Sinkhole Proxy Cổng UDP 53 Nội Bộ (Câu 441 - 460)](#slide-23-kỹ-thuật-lõi-1-f2--m1-kiến-trúc-dns-sinkhole-proxy-cổng-udp-53-nội-bộ-câu-441---460)
* [SLIDE 24: Kỹ Thuật Lõi 2 (F2): Thuật Toán Khớp Tên Miền, Subdomain Wildcard & Danh Mục Miễn Nhiễm Vĩnh Viễn (NT6) (Câu 461 - 480)](#slide-24-kỹ-thuật-lõi-2-f2-thuật-toán-khớp-tên-miền-subdomain-wildcard--danh-mục-miễn-nhiễm-vĩnh-viễn-nt6-câu-461---480)
* [SLIDE 25: Kỹ Thuật Lõi 3 (F2): Cưỡng Chế SafeSearch & YouTube Content Filtering (Câu 481 - 500)](#slide-25-kỹ-thuật-lõi-3-f2-cưỡng-chế-safesearch--youtube-content-filtering-câu-481---500)
* [SLIDE 26: Kỹ Thuật Lõi 4 (F2 & M3): Vô Hiệu Hóa DoH Bằng NXDOMAIN Canary Domain (Câu 501 - 520)](#slide-26-kỹ-thuật-lõi-4-f2--m3-vô-hiệu-hóa-doh-bằng-nxdomain-canary-domain-câu-501---520)
* [SLIDE 27: Kỹ Thuật Lõi 5 (F2): Kiểm Soát Ứng Dụng Bằng Mã Băm SHA-256 & Tối Ưu Hóa mtime Cache (Câu 521 - 540)](#slide-27-kỹ-thuật-lõi-5-f2-kiểm-soát-ứng-dụng-bằng-mã-băm-sha-256--tối-ưu-hóa-mtime-cache-câu-521---540)
* [SLIDE 28: Kỹ Thuật Lõi 6 (NT3 & NT5): Tiếng Nói Trẻ Em — Giao Diện Xin Thêm Giờ & Đồng Bộ Hai Chiều (Câu 541 - 560)](#slide-28-kỹ-thuật-lõi-6-nt3--nt5-tiếng-nói-trẻ-em--giao-diện-xin-thêm-giờ--đồng-bộ-hai-chiều-câu-541---560)
* [SLIDE 29: Tổng Kết Nghiệm Thu Version 3 (v0.3): Network Filtering & Process Control (Câu 561 - 580)](#slide-29-tổng-kết-nghiệm-thu-version-3-v03-network-filtering--process-control-câu-561---580)
* [SLIDE 30: Tổng Quan Version 0.4: Gia Cố Bảo Mật Cấp Cao F5, Pháp Lý NĐ 13, M3 & M4 (Câu 581 - 600)](#slide-30-tổng-quan-version-04-gia-cố-bảo-mật-cấp-cao-f5-pháp-lý-nđ-13-m3--m4-câu-581---600)
* [SLIDE 31: Bảo Mật Cấp Cao F5: NIST SP 800-63B, Khóa Brute-Force 15 Phút, IP Rate Limiting (Câu 601 - 620)](#slide-31-bảo-mật-cấp-cao-f5-nist-sp-800-63b-khóa-brute-force-15-phút-ip-rate-limiting-câu-601---620)
* [SLIDE 32: Bảo Mật Cấp Cao F5: Mã Hóa AES-256-GCM AEAD & Triệt Tiêu Hoàn Toàn IDOR (Câu 621 - 640)](#slide-32-bảo-mật-cấp-cao-f5-mã-hóa-aes-256-gcm-aead--triệt-tiêu-hoàn-toàn-idor-câu-621---640)
* [SLIDE 33: Tuân Thủ Pháp Lý & Đạo Đức: Nghị Định 13/2023/NĐ-CP — Xóa Dữ Liệu 90 Ngày & Right to Erasure (Câu 641 - 660)](#slide-33-tuân-thủ-pháp-lý--đạo-đức-nghị-định-132023nđ-cp--xóa-dữ-liệu-90-ngày--right-to-erasure-câu-641---660)
* [SLIDE 34: Báo Cáo Kỹ Thuật Mạng M3: Khắc Chế 7 Kỹ Thuật Vượt Rào — DNS Watchdog & Process Killer (Câu 661 - 680)](#slide-34-báo-cáo-kỹ-thuật-mạng-m3-khắc-chế-7-kỹ-thuật-vượt-rào--dns-watchdog--process-killer-câu-661---680)
* [SLIDE 35: Báo Cáo Kỹ Thuật Mạng M4: Đo Lường Hiệu Năng Thực Nghiệm (RAM, CPU, DNS Latency, WebSocket) (Câu 681 - 700)](#slide-35-báo-cáo-kỹ-thuật-mạng-m4-đo-lường-hiệu-năng-thực-nghiệm-ram-cpu-dns-latency-websocket-câu-681---700)
* [SLIDE 36: Báo Cáo Kỹ Thuật Mạng M5: Khả Năng Chịu Lỗi & Phục Hồi Mạng — Đệm SQLite & DNS Watchdog Netsh (Câu 701 - 720)](#slide-36-báo-cáo-kỹ-thuật-mạng-m5-khả-năng-chịu-lỗi--phục-hồi-mạng--đệm-sqlite--dns-watchdog-netsh-câu-701---720)
* [SLIDE 37: Hồ Sơ Đồ Án & An Ninh: Mô Hình Đe Dọa STRIDE (8 Threats), OWASP ASVS v4 Level 1 & Minh Bạch AI (Câu 721 - 740)](#slide-37-hồ-sơ-đồ-án--an-ninh-mô-hình-đe-dọa-stride-8-threats-owasp-asvs-v4-level-1--minh-bạch-ai-câu-721---740)
* [SLIDE 38: Tổng Kết Nghiệm Thu Đầu-Cuối Ver 4 (v0.4): Đạt Trọn Vẹn 5/5 Tiêu Chuẩn DoD (Câu 741 - 760)](#slide-38-tổng-kết-nghiệm-thu-đầu-cuối-ver-4-v04-đạt-trọn-vẹn-55-tiêu-chuẩn-dod-câu-741---760)
* [SLIDE 39: Toàn Cảnh Kiểm Thử Tự Động Toàn Hệ Thống: 61/61 Test Cases PASSED 100% & 8/8 Kịch Bản UAT (Câu 761 - 780)](#slide-39-toàn-cảnh-kiểm-thử-tự-động-toàn-hệ-thống-6161-test-cases-passed-100--88-kịch-bản-uat-câu-761---780)
* [SLIDE 40: Kết Luận Toàn Diện Đồ Án Tốt Nghiệp, Khả Năng Mở Rộng Thương Mại & Sẵn Sàng Bảo Vệ (Câu 781 - 800)](#slide-40-kết-luận-toàn-diện-đồ-án-tốt-nghiệp-khả-năng-mở-rộng-thương-mại--sẵn-sàng-bảo-vệ-câu-781---800)

---

# SLIDE 21: TRANG TIÊU ĐỀ BÁO CÁO GIAI ĐOẠN 2 (VERSION 0.3 & VERSION 0.4) (CÂU 401 - 420)

#### ❓ Câu 401: Thầy chỉ vào tiêu đề và hỏi: Giai đoạn 2 này chiếm bao nhiêu phần trăm khối lượng chuyên môn kỹ thuật mạng của toàn bộ đồ án?
> **💡 Trả lời:** Dạ thưa Thầy, Giai đoạn 2 chiếm đến **70% hàm lượng kỹ thuật mạng chuyên sâu** của đồ án. Trong khi Giai đoạn 1 (Tuần 1-2) tập trung vào nền tảng kết nối và quản trị thời gian, Giai đoạn 2 (Tuần 3-4) trực tiếp can thiệp vào tầng giao thức phân giải tên miền DNS Socket UDP 53, kiểm soát DoH/DoT, triển khai mã hóa đối xứng xác thực AEAD AES-256-GCM, phân tích mã băm nhị phân SHA-256, và đo lường độ trễ mạng thực nghiệm theo chuẩn M4/M5.

#### ❓ Câu 402: Thầy hỏi: Tại sao nhóm lại gộp Tuần 3 và Tuần 4 vào chung một bài báo cáo Part 2 mà không tách riêng?
> **💡 Trả lời:** Dạ thưa Thầy, Tuần 3 (v0.3 - Network & Process Filtering) và Tuần 4 (v0.4 - Hardening, Benchmarking & Release) có mối quan hệ nhân - quả hữu cơ: Tuần 3 xây dựng các cơ chế lọc mạng DNS và giám sát tiến trình, còn Tuần 4 đóng vai trò gia cố bảo mật F5, kiểm thử xâm nhập chống vượt rào M3, đo đạc hiệu năng M4 và chứng minh khả năng chịu lỗi M5 trên chính các cơ chế đó. Gộp lại giúp Hội đồng có cái nhìn liền mạch, trọn vẹn từ lúc xây dựng tính năng đến khi kiểm chứng an ninh và đóng gói hoàn thiện.

#### ❓ Câu 403: Thầy chỉ vào cụm từ "Final Graduation Release (v0.4)" và hỏi: Phiên bản này đã sẵn sàng để nghiệm thu tốt nghiệp chưa?
> **💡 Trả lời:** Dạ thưa Thầy, phiên bản v0.4 đã **hoàn thành 100% mục tiêu đồ án tốt nghiệp**, vượt qua toàn bộ **61/61 automated test cases** (100% PASSED) và thỏa mãn trọn vẹn 5/5 tiêu chuẩn Definition of Done (DoD 1 đến DoD 5). Mọi tính năng từ Server, Agent, đồng bộ WebSocket, lọc web DNS đến giao diện phụ huynh đều đã được kiểm chứng hoạt động ổn định trên môi trường Windows 11 thực tế.

#### ❓ Câu 404: Thầy hỏi: Các trụ cột công nghệ liệt kê trên slide này có bám sát đề cương ngành Mạng máy tính không?
> **💡 Trả lời:** Dạ thưa Thầy, bám sát 100% đề cương: Trụ cột 1 là Lập trình Socket mạng phân giải DNS cổng 53; Trụ cột 2 là Kênh truyền song công thời gian thực WebSocket (RFC 6455); Trụ cột 3 là Giao thức ứng dụng an toàn HTTPS/TLS 1.3 và khắc chế DoH (RFC 8484); Trụ cột 4 là An toàn thông tin mạng với mật mã học Argon2id và AES-256-GCM; Trụ cột 5 là Bắt gói tin kiểm chứng bằng Wireshark và đo lường QoS (Độ trễ, Jitter, Mất gói).

#### ❓ Câu 405: Thầy chỉ vào từ "DNS Sinkhole" hỏi: Khái niệm "Hố đen DNS" được hiểu như thế nào theo nghĩa đen và nghĩa mạng?
> **💡 Trả lời:** Dạ thưa Thầy, theo nghĩa đen trong thiên văn học, hố đen hút mọi vật chất đi qua mà không thể thoát ra. Trong kỹ thuật mạng máy tính, **DNS Sinkholing** là kỹ thuật định tuyến sai lệch có chủ đích: Khi Client gửi yêu cầu phân giải tên miền độc hại hoặc bị cấm, máy chủ DNS Proxy sẽ không trả về IP thật của trang web mà trả về một địa chỉ IP "chết" (`0.0.0.0`) hoặc chuyển hướng về một máy chủ chỉ định. Gói tin truy cập web lập tức bị dập tắt ngay từ bước hỏi đường, hoàn toàn không chạm được tới máy chủ web đích.

#### ❓ Câu 406: Thầy hỏi: Tại sao nhóm chọn kiểm soát ứng dụng bằng mã băm SHA-256 thay vì dùng tường lửa Windows chặn IP của game?
> **💡 Trả lời:** Dạ thưa Thầy, vì các tựa game hiện đại (như Liên Minh Huyền Thoại, Roblox, Steam) sử dụng hàng trăm cụm máy chủ đám mây (Cloudflare, AWS, Google Cloud) với dải IP động (Anycast IP) biến đổi liên tục theo từng trận đấu. Nếu chặn bằng IP Firewall, danh sách IP sẽ nhanh chóng bị lỗi thời hoặc chặn nhầm các dịch vụ đám mây hợp pháp khác. Ngược lại, việc băm tệp nhị phân SHA-256 xác định chính xác danh tính của phần mềm độc hại/game trên ổ đĩa, chặn đứng tiến trình ngay từ lúc khởi chạy mà không phụ thuộc vào hạ tầng mạng của nhà phát hành game.

#### ❓ Câu 407: Thầy chỉ vào dòng "NIST SP 800-63B & OWASP ASVS v4" hỏi: Hai chuẩn này có phải đưa vào cho "sang" bài báo cáo không?
> **💡 Trả lời:** Dạ thưa Thầy không hề. Nhóm đã hiện thực hóa trực tiếp các khuyến nghị này vào mã nguồn: NIST SP 800-63B được áp dụng trong `server/security.py` để băm mật khẩu bằng Argon2id chống dò bẻ bằng GPU, quy định độ dài $\ge 10$ ký tự, và khóa tài khoản lũy tiến 15 phút sau 5 lần sai. OWASP ASVS v4 Level 1 được áp dụng để triệt tiêu 100% lỗ hổng IDOR trên mọi API qua việc kiểm tra quyền sở hữu thiết bị `device.parent_id == current_parent.id`, cùng 3 cờ cookie bảo mật `HttpOnly`, `Secure`, `SameSite=Strict`.

#### ❓ Câu 408: Thầy hỏi: Nghị định 13/2023/NĐ-CP của Chính phủ liên quan gì đến một đồ án kỹ thuật phần mềm?
> **💡 Trả lời:** Dạ thưa Thầy, Nghị định 13/2023/NĐ-CP (Điều 20) quy định rất nghiêm ngặt về việc bảo vệ dữ liệu cá nhân của trẻ em trên không gian mạng: Bắt buộc phải có sự đồng ý của cha mẹ và trẻ từ 7 tuổi trở lên, đồng thời phải có cơ chế xóa bỏ dữ liệu khi hết mục đích sử dụng. Nhóm không chỉ làm kỹ thuật thuần túy mà thiết kế sản phẩm chuẩn mực pháp lý: Triển khai vòng đời lưu trữ 90 ngày tự động dọn dẹp và nút bấm thực thi "Quyền được lãng quên" (Right to Erasure) xóa sạch dữ liệu 2 chiều giữa Server và Agent.

#### ❓ Câu 409: Thầy hỏi: Báo cáo M3 và M4 là gì? Ai đặt ra các mã hiệu này?
> **💡 Trả lời:** Dạ thưa Thầy, M1 đến M6 là hệ thống 6 Báo cáo Chuyên sâu Kỹ thuật Mạng do nhóm tự đặt ra theo quy chuẩn nghiên cứu khoa học để giải trình minh bạch: M1 là Báo cáo Kiến trúc DNS Proxy; M2 là Báo cáo Giao thức WebSocket; M3 là Chiến lược khắc chế 7 kỹ thuật vượt rào (Anti-Bypass); M4 là Báo cáo Đo lường hiệu năng thực nghiệm (Benchmarking); M5 là Báo cáo Chịu lỗi và phục hồi mạng; M6 là Báo cáo Pháp lý và An ninh thông tin.

#### ❓ Câu 410: Thầy chỉ vào dòng "61/61 Automated Tests PASSED" hỏi: 61 bài test này đo bằng công cụ gì? Có gian lận bằng test tay không?
> **💡 Trả lời:** Dạ thưa Thầy, 100% được thực thi hoàn toàn tự động bằng công cụ tiêu chuẩn ngành **Pytest**. Kết quả được xuất minh bạch ra file nhật ký kiểm thử `tests/reports/test_results.json` và file Word báo cáo. Các bài test phủ kín từ Unit Test giải mã gói tin DNS, test băm SHA-256 chunk 64KB, test khóa brute-force, test chống IDOR đến Integration Test mô phỏng mất mạng và rớt WebSocket. Không hề có can thiệp thủ công bằng tay.

#### ❓ Câu 411: Thầy hỏi: 5 tiêu chuẩn Definition of Done (DoD 1 đến DoD 5) của nhóm là gì?
> **💡 Trả lời:** Dạ gồm: (1) **DoD 1:** Hoàn thành 100% các micro-tasks theo kế hoạch đặc tả; (2) **DoD 2:** Bộ test suite đạt 100% Pass không có lỗi tiềm ẩn; (3) **DoD 3:** Toàn bộ chỉ số hiệu năng thực nghiệm (RAM < 100MB, CPU < 5%, DNS latency < 20ms) đạt chuẩn M4; (4) **DoD 4:** Hệ thống chịu lỗi ngoại tuyến và tự phục hồi sau sự cố M5; (5) **DoD 5:** Hoàn thiện trọn vẹn bộ hồ sơ kỹ thuật, pháp lý và hướng dẫn sử dụng.

#### ❓ Câu 412: Thầy hỏi: Trong 2 tuần cuối, bạn nào phụ trách mạng và bạn nào phụ trách bảo mật?
> **💡 Trả lời:** Dạ thưa Thầy: Bạn phụ trách Mạng (Sinh viên 2) chịu trách nhiệm lập trình Socket UDP 53 trong `agent/dns_proxy.py`, thuật toán Canary NXDOMAIN, VIP Rewriting SafeSearch, và dịch vụ giám sát `agent/dns_watchdog.py`. Bạn phụ trách Server/Bảo mật (Sinh viên 1) chịu trách nhiệm module mã hóa `server/crypto_utils.py` (AES-256-GCM), kiểm soát IDOR trên các Route FastAPI, chính sách dọn dẹp dữ liệu 90 ngày `server/routes/retention.py`, và đo đạc Benchmark M4.

#### ❓ Câu 413: Thầy hỏi: Đồ án này có điểm gì ưu việt hơn phần mềm thương mại như Qustodio hay Kaspersky Safe Kids?
> **💡 Trả lời:** Dạ thưa Thầy có 3 điểm vượt trội: (1) **Quyền riêng tư tuyệt đối (Local-First):** Dữ liệu nằm trọn trong mạng gia đình, không gửi lịch sử duyệt web lên đám mây máy chủ ngoại quốc; (2) **Triết lý nhân văn (Human-Centric):** Không biến thành phần mềm gián điệp chụp trộm màn hình hay đọc trộm chat, trẻ có quyền xin thêm giờ và báo chặn nhầm; (3) **Mã nguồn mở và chi phí 0 đồng:** Phụ huynh làm chủ hoàn toàn hệ thống mà không phải trả phí thuê bao hàng tháng đắt đỏ.

#### ❓ Câu 414: Thầy hỏi: Nếu trong buổi bảo vệ này Thầy yêu cầu demo ngay tính năng chặn web thì mất bao lâu?
> **💡 Trả lời:** Dạ thưa Thầy chỉ mất **dưới 1 giây**. Chúng em đã chuẩn bị sẵn kịch bản: Server và Agent đang chạy, phụ huynh gõ tên miền `tiktok.com` vào Blacklist trên Dashboard và bấm Lưu, gói tin đồng bộ WebSocket lập tức đẩy xuống Agent trong 5.91 ms, và ngay tại giây tiếp theo khi mở trình duyệt gõ `tiktok.com`, trang web bị chặn đứng về `0.0.0.0` ngay lập tức ạ!

#### ❓ Câu 415: Thầy hỏi: Tại sao nhóm lại đưa cụm từ "Đồng hành giáo dục" vào đồ án công nghệ mạng?
> **💡 Trả lời:** Dạ vì theo các nghiên cứu tâm lý giáo dục và Luật Trẻ Em, việc giám sát cực đoan (chụp lén màn hình, cấm đoán tuyệt đối) chỉ kích thích trẻ tìm cách phá rào và phá vỡ sự tin tưởng trong gia đình. OGK cung cấp kênh giao tiếp 2 chiều: Trẻ biết rõ thời gian còn lại, được quyền gửi yêu cầu xin thêm giờ có lý do chính đáng và phụ huynh phê duyệt tức thì qua WebSocket, biến công nghệ thành cầu nối thấu hiểu giữa cha mẹ và con cái.

#### ❓ Câu 416: Thầy hỏi: Đồ án có dùng thư viện bên thứ 3 nào để can thiệp mạng không hay tự viết Socket?
> **💡 Trả lời:** Dạ thưa Thầy, phần lõi DNS Proxy do nhóm **tự lập trình Socket UDP cổng 53** bằng thư viện chuẩn `socket` và `asyncio` của Python. Nhóm chỉ sử dụng thư viện `dnslib` duy nhất cho tác vụ phân tích (parse) các trường nhị phân theo chuẩn RFC 1035 để tránh phát minh lại bánh xe cho việc giải mã byte. Toàn bộ logic ra quyết định Sinkholing, VIP Rewriting và Canary NXDOMAIN 100% do nhóm tự viết trong `agent/dns_proxy.py`.

#### ❓ Câu 417: Thầy hỏi: Có sự khác biệt nào giữa việc chạy Agent dưới quyền Admin thông thường và quyền LocalSystem ở giai đoạn này?
> **💡 Trả lời:** Dạ thưa Thầy, rất khác biệt: Tài khoản Admin thông thường nếu trẻ sử dụng vẫn có thể bị can thiệp bởi các ứng dụng chạy cùng quyền. Khi Agent được cấu hình chạy dịch vụ nền dưới quyền **NT AUTHORITY\LocalSystem** tại **Session 0**, tiến trình được bảo vệ tuyệt đối: Trẻ dù có mở Task Manager hay dùng lệnh `taskkill` cũng sẽ bị Windows từ chối (`Access Denied`), đồng thời cho phép Agent tự động gọi lệnh `netsh` để cấu hình card mạng DNS mà không bị hiện hộp thoại nhắc quyền UAC phiền toái.

#### ❓ Câu 418: Thầy hỏi: Tại sao phiên bản hoàn thiện lại là 0.4 mà không đánh số là 1.0?
> **💡 Trả lời:** Dạ thưa Thầy, đây là quy chuẩn phiên bản ngữ nghĩa (Semantic Versioning): Nhóm chia tiến trình làm việc thành 4 chặng: v0.1 (Tuần 1 - Nền tảng), v0.2 (Tuần 2 - Quản trị giờ), v0.3 (Tuần 3 - Tầng mạng & Tiến trình), và v0.4 (Tuần 4 - Bảo mật & Đo kiểm). Đánh số v0.4 thể hiện sự trung thực khoa học: Đồ án đã hoàn thành trọn vẹn 100% mục tiêu của đồ án tốt nghiệp trong phạm vi nghiên cứu, và sẵn sàng đóng gói thương mại thành bản 1.0 khi đưa ra thị trường người dùng đại trà.

#### ❓ Câu 419: Thầy hỏi: Nếu trong buổi bảo vệ mạng Internet của trường bị rớt thì hệ thống có chạy demo được không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn chạy bình thường 100%**. Vì OGK được thiết kế theo triết lý Local-First: Server và Agent kết nối với nhau qua mạng nội bộ LAN/Wi-Fi thông qua địa chỉ IP nội bộ (ví dụ `192.168.1.x`). Vòng lặp đếm giờ, cơ chế khóa máy, kênh lệnh WebSocket và cả tầng lọc DNS Sinkhole cục bộ đều chạy offline trên máy tính, hoàn toàn không phụ thuộc vào kết nối ra ngoài Internet.

#### ❓ Câu 420: Thầy hỏi: Tóm tắt trong 1 câu duy nhất: Đóng góp khoa học kỹ thuật lớn nhất của Giai đoạn 2 là gì?
> **💡 Trả lời:** Dạ thưa Thầy: *"Đó là xây dựng thành công một ngăn xếp phòng thủ mạng đa tầng (Defense-in-Depth) tại cổng UDP 53 kết hợp mã băm nhị phân SHA-256, triệt tiêu 7 kỹ thuật vượt rào kinh điển của học sinh với độ trễ phân giải kỷ lục 0.83 ms và tiêu thụ 0.0% CPU, tuân thủ tuyệt đối chuẩn an toàn NIST/OWASP và Nghị định 13/2023/NĐ-CP."*

---

# SLIDE 22: TỔNG QUAN KHỐI LƯỢNG ĐỒ ÁN (TUẦN 3 & TUẦN 4) (CÂU 421 - 440)

#### ❓ Câu 421: Thầy chỉ vào sơ đồ Spec-Driven Development hỏi: Spec-Driven Development (SDD) khác gì với mô hình Agile/Scrum thông thường?
> **💡 Trả lời:** Dạ thưa Thầy, trong khi Agile/Scrum thường tập trung vào viết code nhanh và lặp lại dựa trên User Stories (dễ dẫn đến việc code tùy tiện, thiếu kiểm soát ranh giới kỹ thuật), **Spec-Driven Development** đặt tài liệu đặc tả kỹ thuật (Specification) làm "nguồn chân lý duy nhất" (Single Source of Truth). Trước khi viết bất kỳ dòng code nào, hệ thống phải có bản đặc tả phân tích ranh giới (`spec.md`), kế hoạch thiết kế kiến trúc (`plan.md`), và danh sách các micro-tasks độc lập (`tasks.md`). Code chỉ được viết để thỏa mãn các task và test case đã định nghĩa sẵn.

#### ❓ Câu 422: Thầy hỏi: Tại sao số lượng task của Tuần 3 (45 tasks) và Tuần 4 (31 tasks) lại nhiều hơn cả Tuần 2?
> **💡 Trả lời:** Dạ thưa Thầy, vì tính phức tạp về mặt thuật toán và ranh giới bảo mật của tầng mạng tăng theo cấp số nhân: Tuần 3 phải giải quyết bài toán Socket UDP đa luồng, phân tích nhị phân bản tin DNS, khớp tên miền phụ wildcard, rewrite SafeSearch và băm nhị phân chunked 64KB. Tuần 4 phải thiết lập toàn bộ ma trận test chống IDOR, thuật toán mã hóa AES-256-GCM AEAD, cơ chế khóa tài khoản brute-force, đo lường benchmark 30 mẫu đo và kịch bản phục hồi mạng M5. Mỗi rủi ro bảo mật đều đòi hỏi một task kỹ thuật xử lý độc lập.

#### ❓ Câu 423: Thầy hỏi: 164 tasks chi tiết trong toàn bộ đồ án được lưu trữ và quản lý ở đâu?
> **💡 Trả lời:** Dạ thưa Thầy, toàn bộ 164 tasks được lưu trữ phân rã theo cấu trúc chuẩn trong thư mục `.specify/memory/` của kho chứa Git: `tasks-week1.md` (46 tasks), `tasks-week2.md` (42 tasks), `tasks-week3.md` (45 tasks), và `tasks-week4.md` (31 tasks). Mỗi task đều có mã định danh (ID), mô tả hành động kỹ thuật, tệp mã nguồn tác động, và bài test tương ứng để kiểm chứng.

#### ❓ Câu 424: Thầy hỏi: Tại sao số lượng bài test tự động lại tăng vọt từ 24 test (v0.2) lên 61 test (v0.4)?
> **💡 Trả lời:** Dạ thưa Thầy, vì trong 2 tuần cuối, hệ thống bổ sung thêm 37 kịch bản kiểm thử nghiêm ngặt: 14 test cho tầng lọc mạng và tiến trình Tuần 3 (`tests/test_phase3_network.py`) và 23 test cho tầng bảo mật cấp cao, chống IDOR, AES-256-GCM, chu kỳ xóa dữ liệu và kịch bản chịu lỗi Tuần 4 (`tests/test_phase4_security.py`). Các trường hợp biên (Edge cases) như gói tin DNS dị dạng, băm file không tồn tại, tấn công sai mật khẩu lần thứ 6, và truy cập trái phép chéo thiết bị đều bắt buộc phải có test tự động kiểm chứng.

#### ❓ Câu 425: Thầy hỏi: 37 bài test mới viết thêm kiểm tra những nội dung cụ thể nào?
> **💡 Trả lời:** Dạ gồm các nhóm chính: (1) Nhóm DNS Sinkholing: Chặn blacklist, chuyển tiếp domain sạch, khớp subdomain wildcard `*.tiktok.com`; (2) Nhóm VIP Rewriting: Ép SafeSearch Google, Bing, YouTube; (3) Nhóm Canary Domain: Trả về mã NXDOMAIN cho `use-application-dns.net`; (4) Nhóm SHA-256 App Monitor: Băm nhị phân chunk 64KB, hạ gục tiến trình vi phạm; (5) Nhóm Bảo mật F5: Độ mạnh mật khẩu NIST, brute-force lockout 15 phút, IP rate limiting; (6) Nhóm Mã hóa AES-256-GCM: Nonce 12B, Auth Tag 16B chống lật bit; (7) Nhóm Quyền riêng tư & IDOR: Triệt tiêu IDOR trên mọi API, xóa dữ liệu 90 ngày và Right to Erasure; (8) Nhóm Chịu lỗi M5: Mất mạng, Server crash backoff, và DNS Watchdog netsh 20s.

#### ❓ Câu 426: Thầy hỏi: Các file test nằm ở thư mục nào trong cấu trúc mã nguồn?
> **💡 Trả lời:** Dạ thưa Thầy, toàn bộ mã nguồn kiểm thử nằm trong thư mục `tests/`:
> - `tests/test_phase1.py`: 15 test nền tảng Backbone (Tuần 1).
> - `tests/test_phase2.py`: 9 test quản trị thời gian & WebSocket (Tuần 2).
> - `tests/test_phase3_network.py`: 14 test lọc mạng DNS & App Monitor (Tuần 3).
> - `tests/test_phase4_security.py`: 23 test an ninh F5, IDOR, AES-GCM, NĐ 13 & M5 (Tuần 4).
> - `tests/conftest.py`: Cấu hình Fixtures chung, khởi tạo CSDL SQLite test trong RAM và mock client.

#### ❓ Câu 427: Thầy hỏi: Trong quá trình làm đồ án, có bao giờ xảy ra tình trạng code chạy được nhưng test bị fail không?
> **💡 Trả lời:** Dạ thưa Thầy có rất nhiều lần. Đó chính là giá trị cốt lõi của phương pháp TDD (Test-Driven Development): Ví dụ khi băm file SHA-256 trên Windows, ban đầu code chạy thử với file text nhỏ thì qua, nhưng khi test tự động nạp file nhị phân lớn 100MB thì bị lỗi nghẽn I/O và sai lệch định dạng chữ hoa/chữ thường. Nhờ test case phát hiện, nhóm đã sửa lại hàm băm đọc theo khối 64KB và chuẩn hóa chuỗi băm bằng `.lower()`. Test tự động giúp ngăn chặn toàn bộ các lỗi tiềm ẩn trước khi đưa vào sản phẩm.

#### ❓ Câu 428: Thầy hỏi: 6 báo cáo chuyên sâu M1 đến M6 là những báo cáo gì? Liệt kê tên và mục tiêu của từng báo cáo?
> **💡 Trả lời:** Dạ thưa Thầy:
> 1. **M1 (DNS Proxy Architecture):** Kiến trúc phân giải tên miền nhị phân RFC 1035, Sinkholing về 0.0.0.0, SafeSearch VIP và Canary NXDOMAIN.
> 2. **M2 (WebSocket Protocol):** Kênh truyền song công RFC 6455, bắt tay Upgrade, nhịp tim 60s và đẩy lệnh khẩn cấp dưới 1 giây.
> 3. **M3 (Anti-Bypass Strategy):** Ma trận kỹ thuật phòng thủ, vô hiệu hóa 7 chiêu trò lách luật kinh điển của học sinh.
> 4. **M4 (Performance Benchmarking):** Phương pháp và kết quả đo đạc thực nghiệm 30 mẫu đo (RAM, CPU, DNS Latency, WebSocket Latency).
> 5. **M5 (Fault Tolerance & Resilience):** Cơ chế chịu lỗi ngoại tuyến SQLite WAL, Exponential Backoff và phục hồi DNS Watchdog 20s.
> 6. **M6 (Legal Compliance & Ethics):** Báo cáo tuân thủ Nghị định 13/2023/NĐ-CP, Luật Trẻ Em 2016 và Tiêu chuẩn OWASP ASVS v4.

#### ❓ Câu 429: Thầy hỏi: Tệp dữ liệu thực nghiệm Benchmark 30 mẫu đo được sinh ra như thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm viết kịch bản tự động `scripts/benchmark_performance.py`. Kịch bản này tự động khởi động Server và Agent, sau đó thực hiện vòng lặp 30 lần: Mỗi lần đo ghi nhận mức chiếm dụng RAM (RSS) qua `psutil.Process().memory_info()`, mức sử dụng CPU trong 1 giây, đo thời gian xử lý gói tin DNS bằng đồng hồ nano-giây `time.perf_counter_ns()`, và đo độ trễ gửi nhận gói tin WebSocket. Toàn bộ dữ liệu thô được lưu vào file JSON `benchmark_results.json` để vẽ biểu đồ và phân tích thống kê.

#### ❓ Câu 430: Thầy hỏi: Tại sao nhóm lại cam kết chỉ thu thập 4 trường viễn trắc tối thiểu?
> **💡 Trả lời:** Dạ thưa Thầy, để tuân thủ nguyên tắc Giảm thiểu Dữ liệu (Data Minimization) của Nghị định 13/2023/NĐ-CP và Luật Trẻ Em 2016. Hệ thống chỉ ghi nhận 4 thông số kỹ thuật tổng quan: (1) Tên tiến trình ứng dụng; (2) Tên miền cấp 2 truy cập; (3) Thời lượng sử dụng (phút); (4) Mốc thời gian (Timestamp). Tuyệt đối không thu thập nội dung bài viết, không lưu toàn bộ URL (tránh lộ thông tin tìm kiếm cá nhân), không đọc tin nhắn chat và không chụp lén màn hình.

#### ❓ Câu 431: Thầy hỏi: Nguyên tắc NT1 và NT2 trên slide là gì?
> **💡 Trả lời:** Dạ thưa Thầy:
> - **Nguyên tắc NT1 (Minh bạch với trẻ):** Phần mềm hoạt động công khai, có biểu tượng rõ ràng trên khay hệ thống, trẻ luôn nhìn thấy thời gian sử dụng còn lại của mình và được quyền gửi phản hồi.
> - **Nguyên tắc NT2 (Bảo vệ bí mật đời tư):** Không xâm phạm nội dung riêng tư, hệ thống chỉ quản trị hành vi ở mức độ siêu dữ liệu mạng và tiến trình, cha mẹ đồng hành dựa trên sự tôn trọng chứ không rình mò.

#### ❓ Câu 432: Thầy hỏi: Mô hình đe dọa STRIDE của Tuần 3-4 phân tích những mối nguy nào?
> **💡 Trả lời:** Dạ phân tích 8 mối đe dọa kỹ thuật trọng điểm: (1) Spoofing: Giả mạo gói tin DNS hoặc token máy con; (2) Tampering: Sửa đổi file cấu hình cấm hoặc lật bit gói tin mạng; (3) Repudiation: Phụ huynh hoặc trẻ chối bỏ thao tác đổi luật; (4) Information Disclosure: Rò rỉ dữ liệu máy con qua lỗ hổng IDOR; (5) Denial of Service: Gửi request ồ ạt làm treo máy chủ hoặc chiếm dụng cổng 53; (6) Elevation of Privilege: Trẻ dùng tài khoản máy tính để tắt dịch vụ Agent; (7) Clock Tampering: Lùi giờ hệ thống; (8) DNS Bypass: Đổi card mạng sang 8.8.8.8 hoặc bật DoH.

#### ❓ Câu 433: Thầy hỏi: 22 tiêu chí OWASP ASVS v4 Level 1 được thỏa mãn như thế nào trong mã nguồn?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm đối soát và thỏa mãn toàn bộ 22 tiêu chí: Xác thực phiên bằng Bearer JWT, mật khẩu băm Argon2id có Salt ngẫu nhiên, khóa tài khoản lũy tiến khi brute-force, phân quyền chặt chẽ chống IDOR trên từng endpoint, cờ Cookie an toàn `HttpOnly/SameSite=Strict`, tham số hóa truy vấn SQL qua SQLAlchemy ORM triệt tiêu SQL Injection, và vô hiệu hóa chi tiết lỗi hệ thống (StackTrace) khi trả về Client.

#### ❓ Câu 434: Thầy hỏi: Thời gian chạy toàn bộ 61 test cases này là bao lâu?
> **💡 Trả lời:** Dạ thưa Thầy, tổng thời gian thực thi toàn bộ 61 test cases trên máy tính chỉ mất **khoảng 8.5 đến 11.2 giây**. Sở dĩ tốc độ kiểm thử rất nhanh là vì toàn bộ CSDL thử nghiệm được nhóm cấu hình chạy trực tiếp trên bộ nhớ RAM (`sqlite:///:memory:`), và các hàm mạng, sleep, timer đều được mock thông minh bằng thư viện `unittest.mock`.

#### ❓ Câu 435: Thầy hỏi: Có bài test nào liên quan đến môi trường Windows thực tế mà không thể mock được không?
> **💡 Trả lời:** Dạ có các bài kiểm thử UAT thực tế (User Acceptance Testing): Kiểm tra gọi lệnh Win32 `LockWorkStation`, kiểm tra lệnh `netsh` cấu hình card mạng DNS thật, và kiểm tra tạo icon khay hệ thống bằng `pystray`. Các bài test này được nhóm tách riêng thành bộ kịch bản kiểm thử tích hợp thực nghiệm trên máy tính Windows thật, còn bộ 61 test tự động của Pytest được thiết kế độc lập nền tảng để có thể chạy kiểm tra tự động trên bất kỳ máy tính nào hoặc trên CI/CD pipeline.

#### ❓ Câu 436: Thầy hỏi: Nếu bây giờ Thầy yêu cầu bổ sung thêm 1 task mới thì quy trình SDD của nhóm sẽ xử lý thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, theo đúng chuẩn Spec-Driven Development:
> 1. Nhóm sẽ cập nhật bản đặc tả `spec.md` để xác định rõ yêu cầu đầu vào, đầu ra và ranh giới bảo mật của tính năng mới.
> 2. Phân rã thành 1 task cụ thể trong `tasks.md` kèm tiêu chí kiểm thử nghiệm thu.
> 3. Viết trước 1 bài test tự động (Failed Test) mô phỏng hành vi của tính năng.
> 4. Tiến hành viết mã nguồn thực thi cho đến khi bài test chuyển sang màu xanh (PASSED).
> 5. Chạy lại toàn bộ 61 bài test cũ để đảm bảo tính năng mới không làm phát sinh lỗi hồi quy (Regression Bugs).

#### ❓ Câu 437: Thầy hỏi: Đồ án có đo độ bao phủ mã nguồn (Code Coverage) không? Đạt bao nhiêu %?
> **💡 Trả lời:** Dạ thưa Thầy có, nhóm sử dụng công cụ `pytest-cov`. Độ bao phủ mã nguồn (Code Coverage) trên các module lõi nghiệp vụ đạt **trên 92%**: Trong đó module bảo mật `server/crypto_utils.py` đạt 100%, module xác thực và phân quyền đạt 96%, module DNS Sinkhole đạt 91%, và module đếm giờ đạt 94%. Phần mã nguồn chưa phủ hết chủ yếu là các khối xử lý ngoại lệ đặc thù của giao diện đồ họa GUI.

#### ❓ Câu 438: Thầy hỏi: Chi phí tài nguyên và thời gian để hoàn thành 76 tasks của Tuần 3 và 4 là bao nhiêu?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm đã dành trọn vẹn 2 tuần làm việc tập trung (tương đương khoảng 120 giờ làm việc thực tế cho 2 thành viên). Chi phí tài nguyên phần cứng hoàn toàn là máy tính cá nhân sẵn có của sinh viên, không tốn bất kỳ chi phí bản quyền nào nhờ sử dụng 100% công nghệ mã nguồn mở.

#### ❓ Câu 439: Thầy hỏi: Tại sao nhóm không dùng Jira hay Trello mà lại dùng Spec-Kit quản lý task ngay trong repo Git?
> **💡 Trả lời:** Dạ thưa Thầy, vì triết lý **"Docs-as-Code" (Tài liệu đi liền với mã nguồn)**: Khi quản lý task bằng các tệp Markdown ngay trong repo Git (`.specify/memory/`), mọi thay đổi về yêu cầu, tiến độ và mã nguồn đều được gắn kết chặt chẽ trong từng Git Commit. Không bao giờ xảy ra tình trạng tài liệu trên Jira một đằng nhưng mã nguồn trong Git một nẻo. Hội đồng có thể kiểm tra lịch sử commit là thấy rõ từng task được giải quyết chính xác ở commit nào.

#### ❓ Câu 440: Thầy hỏi: Ý nghĩa của việc tài liệu hóa song ngữ Anh - Việt trong đồ án?
> **💡 Trả lời:** Dạ thưa Thầy, việc tài liệu hóa song ngữ (các tài liệu nghiên cứu chuẩn dùng tiếng Anh theo chuẩn quốc tế IETF/NIST/OWASP, tài liệu báo cáo và cẩm nang dùng tiếng Việt chuẩn mực) giúp đồ án vừa tiếp cận được những tri thức công nghệ tiên tiến nhất của thế giới, vừa đảm bảo tính ứng dụng thực tiễn cao nhất cho các gia đình và cơ quan quản lý tại Việt Nam theo đúng tinh thần Nghị định 13/2023/NĐ-CP.

---

# SLIDE 23: KỸ THUẬT LÕI 1 (F2 & M1): KIẾN TRÚC DNS SINKHOLE PROXY CỔNG UDP 53 NỘI BỘ (CÂU 441 - 460)

#### ❓ Câu 441: Thầy chỉ vào sơ đồ Sinkhole hỏi: Bản chất kỹ thuật của DNS Sinkholing là gì? Tại sao gọi là hố đen?
> **💡 Trả lời:** Dạ thưa Thầy, bản chất của DNS Sinkholing là kỹ thuật đánh chặn (interception) gói tin truy vấn phân giải tên miền ở tầng mạng: Khi máy tính muốn truy cập một trang web độc hại nằm trong danh sách cấm, DNS Proxy cục bộ sẽ can thiệp và không trả về địa chỉ IP thật của máy chủ web đó, mà trả về một địa chỉ IP không thể định tuyến (`0.0.0.0`). Tên gọi "hố đen" ám chỉ việc gói tin yêu cầu truy cập web bị biến mất hoàn toàn ngay từ tầng phân giải địa chỉ, trình duyệt bị dập tắt kết nối lập tức mà không tiêu tốn tài nguyên.

#### ❓ Câu 442: Thầy hỏi: Gói tin DNS đi từ trình duyệt đến Proxy như thế nào khi card mạng trỏ về 127.0.0.1?
> **💡 Trả lời:** Dạ thưa Thầy, quy trình diễn ra như sau:
> 1. Khi người dùng gõ `tiktok.com`, trình duyệt gọi hàm giải quyết tên miền của hệ điều hành (`getaddrinfo` Win32 API).
> 2. Hệ điều hành kiểm tra cấu hình DNS của card mạng, thấy DNS Server là `127.0.0.1`.
> 3. Hệ điều hành tạo một gói tin UDP đóng gói bản tin truy vấn DNS, gửi tới địa chỉ đích `127.0.0.1` trên cổng 53.
> 4. Gói tin đi qua giao diện lặp nội bộ (Loopback Interface) của nhân Windows và rơi thẳng vào Socket UDP đang lắng nghe của `agent/dns_proxy.py`.

#### ❓ Câu 443: Thầy hỏi: Cấu trúc một gói tin DNS nhị phân theo chuẩn RFC 1035 gồm những thành phần nào?
> **💡 Trả lời:** Dạ thưa Thầy, theo chuẩn RFC 1035, gói tin DNS gồm 5 phần chính:
> 1. **Header Section (Cố định 12 bytes):** Chứa ID, các cờ điều khiển và số lượng bản ghi trong các phần sau.
> 2. **Question Section:** Chứa tên miền cần hỏi (QNAME), loại bản ghi (QTYPE, ví dụ A=1, AAAA=28) và lớp mạng (QCLASS, IN=1).
> 3. **Answer Section:** Chứa các bản ghi tài nguyên trả lời kết quả truy vấn (Resource Records).
> 4. **Authority Section:** Chứa thông tin về các máy chủ nắm thẩm quyền phân giải tên miền (Name Servers).
> 5. **Additional Section:** Chứa các bản ghi phụ trợ bổ sung thông tin.

#### ❓ Câu 444: Thầy hỏi: Trường Header 12 bytes của DNS chứa những thông tin gì? Ý nghĩa của cờ QR và RCODE?
> **💡 Trả lời:** Dạ thưa Thầy:
> - **12 bytes Header** gồm: Transaction ID (2B), Flags (2B), QDCOUNT (2B), ANCOUNT (2B), NSCOUNT (2B), ARCOUNT (2B).
> - **Cờ QR (Query/Response - bit đầu tiên của Flags):** `0` = Bản tin truy vấn (Request); `1` = Bản tin phản hồi (Response).
> - **RCODE (Response Code - 4 bit cuối của Flags):** Thể hiện kết quả xử lý của DNS Server:
>   * `RCODE = 0 (NOERROR):` Thành công.
>   * `RCODE = 3 (NXDOMAIN):` Tên miền không tồn tại (Non-Existent Domain).
>   * `RCODE = 2 (SERVFAIL):` Máy chủ phân giải gặp lỗi.
>   * `RCODE = 5 (REFUSED):` Từ chối phân giải do vi phạm chính sách mạng.

#### ❓ Câu 445: Thầy hỏi: Tại sao nhóm lại trả về IP 0.0.0.0 mà không trả về 127.0.0.1 khi chặn web đen?
> **💡 Trả lời:** Dạ thưa Thầy, đây là quyết định kiến trúc mạng cực kỳ quan trọng:
> - Nếu trả về `127.0.0.1` (Localhost loopback), trình duyệt sẽ cố gắng bắt tay TCP SYN vào cổng 80/443 của chính máy tính con. Vì máy con không mở web server, hệ điều hành phải chờ timeout 20 - 30 giây hoặc gửi gói RST, gây hiện tượng trình duyệt quay vòng đơ lag rất khó chịu. Nếu máy con có cài web server ngầm, trang web đen bị biến tướng thành giao diện nội bộ.
> - Nếu trả về `0.0.0.0` (RFC 3513 Unspecified Address), nhân mạng Windows nhận diện đây là địa chỉ không thể định tuyến (non-routable), lập tức từ chối kết nối ngay trong **0 mili-giây**. Trình duyệt hiện ngay thông báo không tìm thấy máy chủ mà hoàn toàn không bị lag máy!

#### ❓ Câu 446: Thầy hỏi: Trình duyệt xử lý địa chỉ 0.0.0.0 như thế nào? Tại sao lại phản hồi 0ms mà không bị timeout?
> **💡 Trả lời:** Dạ thưa Thầy, theo đặc tả chuẩn TCP/IP, địa chỉ `0.0.0.0` được định nghĩa là "địa chỉ nguồn không xác định" và không bao giờ là một địa chỉ đích hợp lệ trên mạng. Khi trình duyệt gọi hàm Socket `connect("0.0.0.0", 443)`, nhân mạng của Windows (Winsock API) lập tức trả về mã lỗi `WSAEADDRNOTAVAIL` (The requested address is not valid in its context) ngay lập tức mà không hề phát sinh bất kỳ gói tin SYN nào ra card mạng. Do đó thời gian phản hồi bằng 0 ms, hoàn toàn không có thời gian chờ (timeout).

#### ❓ Câu 447: Thầy hỏi: Nếu máy con chạy một web server nội bộ (XAMPP/IIS) ở cổng 80 thì việc trả về 127.0.0.1 sẽ gây hậu quả gì?
> **💡 Trả lời:** Dạ thưa Thầy, hậu quả sẽ rất tai hại: Khi trẻ truy cập trang web đen bị chặn, thay vì hiện trang lỗi, trình duyệt lại tải lên trang Dashboard của XAMPP, phpMyAdmin hoặc trang chào mừng của IIS trên máy tính. Trẻ có thể tò mò nghịch ngợm phá hỏng cơ sở dữ liệu nội bộ của máy, hoặc các mã script trong trang web đen có thể tấn công vào các API cục bộ đang mở trên máy con qua kỹ thuật DNS Rebinding! Trả về `0.0.0.0` triệt tiêu hoàn toàn rủi ro này.

#### ❓ Câu 448: Thầy hỏi: Khi tên miền hợp lệ, Proxy chuyển tiếp gói tin (Forward) đi đâu và bằng cách nào?
> **💡 Trả lời:** Dạ thưa Thầy, trong `agent/dns_proxy.py`, nếu tên miền không nằm trong danh sách cấm và không thuộc diện SafeSearch, Proxy sẽ giữ nguyên gói tin UDP gốc và chuyển tiếp (Forward) tới máy chủ Upstream DNS công cộng (mặc định là Cloudflare `1.1.1.1` hoặc Google `8.8.8.8`) thông qua một Socket UDP thứ hai. Khi nhận được gói tin phản hồi từ Upstream, Proxy lập tức gửi trả nguyên vẹn về cho máy tính con theo đúng Transaction ID ban đầu.

#### ❓ Câu 449: Thầy hỏi: Upstream DNS server mặc định của hệ thống là server nào? Có đổi được không?
> **💡 Trả lời:** Dạ thưa Thầy, Upstream DNS mặc định được thiết lập là Cloudflare DNS (`1.1.1.1` và `1.0.0.1`) vì đây là DNS công cộng có tốc độ phân giải nhanh nhất thế giới hiện nay và cam kết không lưu vết người dùng. Tuy nhiên, thông số này được lưu trong file cấu hình `agent_config.json`, phụ huynh hoàn toàn có thể tùy chỉnh đổi sang Google DNS (`8.8.8.8`) hoặc Quad9 (`9.9.9.9`) nếu muốn.

#### ❓ Câu 450: Thầy hỏi: Độ trễ phân giải trung bình của DNS Sinkhole Proxy đo được là bao nhiêu ms?
> **💡 Trả lời:** Dạ thưa Thầy, theo số liệu thực nghiệm đo đạc độc lập 30 lần trong Báo cáo M4:
> - Đối với tên miền bị chặn (Sinkholing trả về `0.0.0.0` ngay trong RAM): Độ trễ trung bình chỉ là **0.83 mili-giây**.
> - Đối với tên miền hợp lệ chuyển tiếp ra Internet (Forwarding): Độ trễ trung bình là **12.4 mili-giây** (phụ thuộc vào đường truyền nhà mạng).
> Mức 0.83 ms vượt xa cam kết ban đầu của đồ án (yêu cầu trần dưới 20 ms).

#### ❓ Câu 451: Thầy hỏi: Lập trình Socket UDP cổng 53 trong Python dùng cơ chế đồng bộ hay bất đồng bộ?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm sử dụng cơ chế **Bất đồng bộ (Asynchronous Non-blocking)** dựa trên thư viện `asyncio` và giao thức `asyncio.DatagramProtocol`. Cơ chế này cho phép một luồng duy nhất có thể tiếp nhận và xử lý hàng trăm truy vấn DNS đồng thời mà không bị block I/O, không phải tạo thêm luồng (Thread) tốn kém tài nguyên bộ nhớ.

#### ❓ Câu 452: Thầy hỏi: Trên Windows có dịch vụ "Dnscache" (DNS Client), tại sao Proxy của nhóm không bị báo lỗi trùng cổng 53?
> **💡 Trả lời:** Dạ thưa Thầy, đây là một điểm kỹ thuật rất thú vị của hệ điều hành Windows: Dịch vụ `Dnscache` của Windows chỉ đóng vai trò là một **DNS Resolver Client** (bộ nhớ đệm truy vấn), nó **không hề mở Socket lắng nghe (listen) cổng UDP 53 trên địa chỉ Loopback `127.0.0.1`**. Dịch vụ DNS Server trên Windows chỉ chạy khi máy tính cài đặt phiên bản Windows Server và kích hoạt tính năng DNS Role. Do đó, trên Windows 10 và 11 của máy gia đình, cổng `127.0.0.1:53` hoàn toàn trống rỗng, Agent của OGK có thể bind cổng này một cách trơn tru 100% mà không bị lỗi `WSAEADDRINUSE`.

#### ❓ Câu 453: Thầy hỏi: Lệnh netsh cụ thể mà Agent dùng để ép card mạng Windows trỏ về 127.0.0.1 là gì?
> **💡 Trả lời:** Dạ thưa Thầy, Agent sử dụng lệnh dòng lệnh chuẩn của Windows:
> ```cmd
> netsh interface ip set dns name="Wi-Fi" source=static addr=127.0.0.1
> ```
> Lệnh này thiết lập địa chỉ máy chủ DNS chính (Primary DNS) của card mạng "Wi-Fi" thành địa chỉ tĩnh trỏ về `127.0.0.1`.

#### ❓ Câu 454: Thầy hỏi: Nếu máy tính có nhiều card mạng (Ethernet, Wi-Fi, Card ảo VMware), Agent xử lý card nào?
> **💡 Trả lời:** Dạ thưa Thầy, trong `agent/dns_watchdog.py`, Agent không gán cứng tên card mạng mà gọi lệnh `netsh interface show interface` và sử dụng thư viện `psutil.net_if_stats()` để tìm ra card mạng đang ở trạng thái **Operational (Connected)** và có cổng Gateway mặc định (Default Gateway) ra Internet. Agent sẽ cấu hình DNS cho card mạng đang có kết nối Internet đó, đồng thời bỏ qua các card mạng ảo của VMware hay VirtualBox.

#### ❓ Câu 455: Thầy hỏi: Khi tắt Agent hoặc gỡ cài đặt, làm sao để phục hồi DNS của máy con về trạng thái ban đầu?
> **💡 Trả lời:** Dạ thưa Thầy, trong hàm dọn dẹp khi thoát `cleanup()` của Agent (được bắt bằng tín hiệu `SIGINT`, `SIGTERM` và sự kiện `atexit`), Agent tự động gọi lệnh:
> ```cmd
> netsh interface ip set dns name="Wi-Fi" source=dhcp
> ```
> Lệnh này khôi phục card mạng về chế độ nhận DNS tự động từ Router nhà mạng qua giao thức DHCP, đồng thời chạy lệnh `ipconfig /flushdns` để xóa sạch cache, giúp máy con lướt web bình thường ngay lập tức.

#### ❓ Câu 456: Thầy hỏi: Có trường hợp nào gói tin DNS lớn hơn 512 bytes không? Proxy xử lý thế nào?
> **💡 Trả lời:** Dạ có thưa Thầy. Theo RFC 1035, gói tin UDP DNS truyền thống bị giới hạn ở kích thước 512 bytes. Tuy nhiên, với chuẩn mở rộng EDNS0 (RFC 6891), kích thước gói tin có thể lên đến 4096 bytes. Proxy của nhóm thiết lập kích thước vùng đệm đọc Socket `recvfrom(4096)` để tiếp nhận an toàn các gói tin EDNS0 lớn. Nếu gói tin phản hồi vượt quá dung lượng quy định, Proxy bật cờ cắt cụt `TC = 1` (Truncated) trong Header để báo hiệu Client chuyển sang kết nối TCP cổng 53 nếu cần.

#### ❓ Câu 457: Thầy hỏi: Proxy có hỗ trợ bản ghi IPv6 (AAAA record) không? Xử lý thế nào khi bị chặn?
> **💡 Trả lời:** Dạ thưa Thầy có hỗ trợ đầy đủ. Khi nhận được truy vấn bản ghi IPv6 (QTYPE = 28 / AAAA record) cho một tên miền nằm trong danh sách cấm, Proxy không trả về `0.0.0.0` (vì đây là IPv4) mà trả về địa chỉ Synthetic IPv6 tương ứng là `::` (Địa chỉ IPv6 Unspecified Address theo RFC 4291). Trình duyệt cũng lập tức từ chối kết nối IPv6 ngay trong 0 ms.

#### ❓ Câu 458: Thầy hỏi: Cơ chế DNS Cache nội bộ trong Proxy hoạt động ra sao để giảm tải Upstream?
> **💡 Trả lời:** Dạ thưa Thầy, trong `agent/dns_proxy.py`, Proxy duy trì một bảng băm trong bộ nhớ RAM:
> $$	ext{DNS\_Cache} = \{ (	ext{qname}, 	ext{qtype}) : (	ext{response\_packet}, 	ext{expire\_time}) \}$$
> Khi nhận được câu hỏi cho domain sạch, Proxy kiểm tra Cache trước: Nếu bản ghi còn hạn sử dụng (dựa trên giá trị TTL của bản tin), Proxy trả lời ngay lập tức trong 0.2 ms mà không cần gửi gói tin ra Internet, giúp tiết kiệm băng thông và giảm thiểu độ trễ tối đa.

#### ❓ Câu 459: Thầy hỏi: File mã nguồn nào hiện thực toàn bộ logic DNS Sinkhole Proxy này? Chỉ rõ đường dẫn?
> **💡 Trả lời:** Dạ thưa Thầy, toàn bộ logic nằm trọn vẹn trong tệp:  
> `agent/dns_proxy.py` (khoảng 220 dòng mã nguồn).  
> Trong đó hàm `handle_dns_request()` phụ trách phân tích và ra quyết định, hàm `build_sinkhole_response()` tạo gói tin trả về `0.0.0.0`, và hàm `forward_query()` chuyển tiếp gói tin ra Upstream DNS.

#### ❓ Câu 460: Thầy hỏi: Bài kiểm thử tự động nào chứng minh DNS Sinkhole chặn đúng 0.0.0.0 và chuyển tiếp tên miền sạch?
> **💡 Trả lời:** Dạ thưa Thầy, đó là bài test `test_dns_proxy_sinkhole_blocking` và `test_dns_proxy_clean_forwarding` nằm trong tệp `tests/test_phase3_network.py`. Bài test tạo các gói tin DNS nhị phân giả lập gửi vào Proxy: Kết quả trả về cho domain cấm được giải mã kiểm tra đúng IP `0.0.0.0` và cờ `RCODE = 0`, còn domain sạch được chuyển tiếp thành công và nhận đủ bản ghi từ Upstream.

---

# SLIDE 24: KỸ THUẬT LÕI 2 (F2): THUẬT TOÁN KHỚP TÊN MIỀN, SUBDOMAIN WILDCARD & IMMUNITY WHITELIST (CÂU 461 - 480)

#### ❓ Câu 461: Thầy chỉ vào bảng so sánh thuật toán hỏi: Tại sao nhóm không dùng biểu thức chính quy (Regex) để khớp tên miền cấm?
> **💡 Trả lời:** Dạ thưa Thầy, vì **hiệu năng (Performance)**. Biểu thức chính quy (Regex) có độ phức tạp tính toán rất cao ($O(N 	imes L)$ với $N$ là số lượng luật và $L$ là độ dài chuỗi). Khi danh sách đen mở rộng lên hàng nghìn hoặc chục nghìn tên miền, việc chạy regex trên từng gói tin DNS sẽ khiến CPU máy con tăng vọt và làm tăng độ trễ phân giải lên hàng chục mili-giây, gây đơ lag khi trẻ mở các trang web có tải nhiều tài nguyên.

#### ❓ Câu 462: Thầy hỏi: Độ phức tạp thuật toán O(K) của cơ chế kiểm tra Subdomain được tính như thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, trong thuật toán của OGK, $K$ là **số lượng nhãn (labels/cấp) của tên miền**, chứ không phải số lượng tên miền trong cơ sở dữ liệu.  
> Ví dụ với tên miền `video.m.tiktok.com`, số cấp $K = 4$. Thuật toán chỉ thực hiện tối đa 4 phép tra cứu bảng băm (Hash Table Lookup $O(1)$) cho các chuỗi: (1) `video.m.tiktok.com`, (2) `m.tiktok.com`, (3) `tiktok.com`, (4) `com`.  
> Vì $K$ trong thực tế luôn nhỏ hơn hoặc bằng 5 ($K \le 5$), nên độ phức tạp là một hằng số $O(1)$ trên thực tế, thời gian thực thi chỉ mất **dưới 0.01 mili-giây**!

#### ❓ Câu 463: Thầy hỏi: Nếu danh sách đen có "tiktok.com", làm sao hệ thống chặn được "v16.tiktokcdn.com" và "m.tiktok.com"?
> **💡 Trả lời:** Dạ thưa Thầy:
> - Đối với `m.tiktok.com`: Thuật toán bóc tách nhãn từ trái qua phải. Sau khi kiểm tra `m.tiktok.com` không có trong danh sách, thuật toán cắt bỏ tiền tố `m.` và kiểm tra tiếp chuỗi cha `tiktok.com`. Thấy `tiktok.com` có trong danh sách đen, thuật toán lập tức kết luận chặn ngay!
> - Đối với `v16.tiktokcdn.com`: Phụ huynh hoặc danh mục mẫu của OGK đã bao gồm cả tên miền gốc của máy chủ CDN là `tiktokcdn.com`. Thuật toán áp dụng cơ chế tương tự và chặn đứng toàn bộ các phân vùng video của TikTok.

#### ❓ Câu 464: Thầy hỏi: Thuật toán cắt chuỗi tên miền cha chạy từ trái qua phải hay từ phải qua trái?
> **💡 Trả lời:** Dạ thưa Thầy, thuật toán chạy **từ trái qua phải** bằng hàm `split('.')`:  
> Tên miền ban đầu được phân tách thành danh sách các thành phần `labels = domain.split('.')`. Sau đó, một vòng lặp sẽ ghép lại các nhãn từ vị trí $i$ đến hết: `sub = ".".join(labels[i:])` với $i$ tăng từ 0 đến len(labels)-1. Cách tiếp cận này tự nhiên, chuẩn xác và không cần dùng đến cấu trúc dữ liệu đệ quy phức tạp.

#### ❓ Câu 465: Thầy hỏi: Nếu kẻ xấu dùng tên miền "fakenews-tiktok.com" thì hệ thống có chặn nhầm không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn không chặn nhầm!** Vì thuật toán của OGK phân tách dựa trên dấu chấm phân cấp (`.`) của hệ thống DNS quốc tế, chứ không phải tìm kiếm chuỗi con (substring search). Chuỗi `fakenews-tiktok.com` có nhãn cấp 2 là `fakenews-tiktok`, hoàn toàn khác biệt về mặt cấu trúc với nhãn `tiktok.com`. Do đó trang web này không bị chặn nhầm, đảm bảo tính chính xác tuyệt đối.

#### ❓ Câu 466: Thầy chỉ vào slide hỏi: Khái niệm "Danh mục Miễn nhiễm Vĩnh viễn" (Immunity Whitelist NT6) là gì?
> **💡 Trả lời:** Dạ thưa Thầy, đây là tính năng hiện thực hóa **Nguyên tắc NT6 trong Hiến chương OGK**: Nhằm bảo vệ quyền được học tập và liên lạc khẩn cấp của trẻ em, hệ thống định nghĩa một danh sách các tên miền thiết yếu bất khả xâm phạm ở mức lõi cứng (Hardcoded Immunity). Các tên miền này được ưu tiên cho phép truy cập vĩnh viễn trong mọi hoàn cảnh, ngay cả khi đang trong giờ giới nghiêm hoặc phụ huynh vô tình nhập nhầm vào danh sách cấm.

#### ❓ Câu 467: Thầy hỏi: Liệt kê các tên miền nằm trong danh sách Immunity Whitelist cứng?
> **💡 Trả lời:** Dạ gồm các nhóm:
> 1. **Cổng giáo dục quốc gia:** `moet.gov.vn`, các tên miền đuôi `.edu.vn`.
> 2. **Nền tảng học trực tuyến thiết yếu:** `zoom.us`, `teams.microsoft.com`, `classroom.google.com`.
> 3. **Dịch vụ hệ điều hành tối quan trọng:** `windowsupdate.com`, `update.microsoft.com`.
> 4. **Hạ tầng mạng nội bộ:** `localhost`, và Canary Domain `use-application-dns.net` (để trả lời NXDOMAIN).

#### ❓ Câu 468: Thầy hỏi: Tại sao phải có danh sách miễn nhiễm cứng này? Phụ huynh có quyền xóa nó khỏi hệ thống không?
> **💡 Trả lời:** Dạ thưa Thầy, phụ huynh **không thể xóa danh sách này**. Lý do vì trong thực tế có những tình huống cha mẹ trong lúc nóng giận hoặc thiếu hiểu biết công nghệ đã chặn toàn bộ Internet của con trong đợt thi cử trực tuyến, khiến trẻ không thể vào phòng thi Zoom hay nộp bài tập trên Google Classroom. Việc thiết lập Immunity Whitelist cứng bảo đảm công nghệ luôn phụng sự lợi ích tối cao của đứa trẻ theo đúng tinh thần Luật Trẻ Em 2016.

#### ❓ Câu 469: Thầy hỏi: Nếu phụ huynh cố tình thêm "zoom.us" vào danh sách cấm Blacklist thì chuyện gì xảy ra?
> **💡 Trả lời:** Dạ thưa Thầy, trong hàm `is_domain_blocked(domain)` của `agent/dns_proxy.py`, bước đầu tiên luôn là:
> ```python
> if self.is_immune(domain):
>     return False  # Bỏ qua ngay lập tức, luôn luôn cho phép
> ```
> Gói tin phân giải cho `zoom.us` lập tức được chấp thuận và chuyển tiếp ra Upstream DNS. Đồng thời trên Dashboard của phụ huynh sẽ hiện một thông báo nhắc nhở nhẹ nhàng: *"Tên miền zoom.us thuộc danh mục học tập thiết yếu được bảo vệ vĩnh viễn theo nguyên tắc NT6."*

#### ❓ Câu 470: Thầy hỏi: Thứ tự ưu tiên đối soát tên miền trong hàm `is_domain_blocked` diễn ra như thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, thứ tự ưu tiên diễn ra nghiêm ngặt qua 4 bước:
> 1. **Bước 1 (Immunity Check):** Kiểm tra xem domain có nằm trong Whitelist miễn nhiễm cứng không? $ightarrow$ Nếu có: Cho qua ngay lập tức.
> 2. **Bước 2 (SafeSearch Check):** Kiểm tra xem domain có thuộc diện tìm kiếm (Google, Bing, YouTube) không? $ightarrow$ Nếu có: Kích hoạt VIP Rewriting.
> 3. **Bước 3 (Canary Check):** Kiểm tra tên miền `use-application-dns.net`? $ightarrow$ Nếu có: Trả về mã NXDOMAIN.
> 4. **Bước 4 (Blacklist Subdomain Check):** Cắt nhãn kiểm tra danh sách cấm $ightarrow$ Nếu trùng: Sinkhole về `0.0.0.0`. Nếu không: Chuyển tiếp sạch ra Upstream.

#### ❓ Câu 471: Thầy hỏi: Bộ nhớ RAM tiêu tốn cho việc lưu trữ 10.000 tên miền cấm trong cấu trúc Set là bao nhiêu?
> **💡 Trả lời:** Dạ thưa Thầy, cấu trúc `set` trong Python lưu trữ các chuỗi băm rất tối ưu. Một tên miền trung bình dài 15 ký tự chiếm khoảng 60 bytes bộ nhớ. Với 10.000 tên miền cấm, tổng dung lượng RAM tiêu tốn của cấu trúc Set chỉ khoảng **dưới 1.2 Megabytes**. Con số này hoàn toàn không đáng kể so với dung lượng RAM hàng Gigabytes của máy tính hiện đại.

#### ❓ Câu 472: Thầy hỏi: Tên miền viết hoa viết thường (ví dụ: `TiKToK.CoM`) có làm thuật toán bị qua mặt không?
> **💡 Trả lời:** Dạ thưa Thầy không thể qua mặt được. Vì ngay khi trích xuất chuỗi tên miền QNAME từ gói tin nhị phân, Proxy lập tức chuẩn hóa bằng hàm `.lower().strip('.')`. Mọi so sánh trong cơ sở dữ liệu và bảng băm đều được thực hiện trên chuỗi chữ thường đồng nhất.

#### ❓ Câu 473: Thầy hỏi: Hệ thống có hỗ trợ tên miền tiếng Việt hoặc ký tự quốc tế IDN (Punycode như `xn--...`) không?
> **💡 Trả lời:** Dạ có hỗ trợ thưa Thầy. Khi người dùng gõ tên miền tiếng Việt có dấu, trình duyệt tự động mã hóa chuỗi đó thành định dạng Punycode (bắt đầu bằng tiền tố `xn--`) trước khi đóng gói vào bản tin DNS. Proxy của nhóm tiếp nhận và so sánh trực tiếp trên chuỗi nhị phân Punycode này, đảm bảo chặn chính xác tuyệt đối các trang web tiếng Việt có dấu.

#### ❓ Câu 474: Thầy hỏi: Khi phụ huynh cập nhật danh sách chặn trên Dashboard, mất bao lâu để Agent cập nhật vào bộ nhớ?
> **💡 Trả lời:** Dạ thưa Thầy chỉ mất **dưới 10 mili-giây** trong mạng LAN. Khi phụ huynh bấm Lưu trên Dashboard, Server phát một sự kiện WebSocket `RULES_UPDATED` kèm danh sách mới tới máy con. Hàm xử lý sự kiện của Agent cập nhật trực tiếp biến `blocked_domains_set` trong bộ nhớ RAM ngay lập tức mà không cần phải khởi động lại tiến trình Agent hay Proxy.

#### ❓ Câu 475: Thầy hỏi: Danh sách tên miền cấm được đồng bộ qua API REST hay qua kênh WebSocket?
> **💡 Trả lời:** Dạ thưa Thầy, kết hợp cả hai:
> - **Khi khởi động (Cold Start):** Agent gọi API REST `GET /api/devices/{device_id}/rules` để tải toàn bộ danh sách quy tắc mới nhất từ cơ sở dữ liệu Server về lưu đệm cục bộ.
> - **Khi đang hoạt động (Runtime):** Mọi thao tác thêm/bớt của phụ huynh được đẩy tức thời (Push Notification) qua kênh WebSocket để đảm bảo độ trễ cập nhật bằng 0.

#### ❓ Câu 476: Thầy hỏi: Nếu một trang web cấm dùng dịch vụ CDN chia sẻ IP (như Cloudflare) với trang web sạch thì sao?
> **💡 Trả lời:** Dạ thưa Thầy, đó chính là lý do vì sao **chặn ở tầng DNS vượt trội hoàn toàn so với chặn ở tầng IP**:  
> Nếu chặn theo IP, khi chặn IP của Cloudflare thì hàng ngàn trang web sạch khác dùng chung IP đó sẽ bị sập theo. Nhưng chặn bằng DNS Sinkholing của OGK, Proxy chỉ can thiệp vào tên miền cấm (ví dụ `webden.com` $ightarrow$ `0.0.0.0`), còn trang web học tập sạch dùng chung CDN Cloudflare vẫn được phân giải trả về IP Cloudflare bình thường và truy cập trơn tru 100%!

#### ❓ Câu 477: Thầy hỏi: Sự khác biệt bản chất giữa việc chặn ở tầng Tên miền (DNS) và chặn ở tầng Địa chỉ IP (IP Firewall)?
> **💡 Trả lời:** Dạ thưa Thầy:
> - **Chặn IP (Tầng Mạng/Network Layer):** Nhanh nhưng thô bạo. Không xử lý được IP động, IP chia sẻ qua CDN/Proxy, và không thể hiện thông báo lỗi thân thiện.
> - **Chặn DNS (Tầng Ứng Dụng/Application Layer):** Linh hoạt, thông minh, chính xác theo định danh tên miền, không sợ CDN chia sẻ IP, chi phí tài nguyên cực thấp và dễ dàng tùy biến chuyển hướng SafeSearch.

#### ❓ Câu 478: Thầy hỏi: Tại sao không dùng file `hosts` của Windows (`C:\Windows\System32\drivers\etc\hosts`) cho nhanh mà phải viết DNS Proxy?
> **💡 Trả lời:** Dạ thưa Thầy, việc dùng file `hosts` có 4 nhược điểm chí mạng:
> 1. **Không hỗ trợ Subdomain Wildcard:** File `hosts` bắt buộc phải khai báo chính xác từng domain, không thể viết `*.tiktok.com`. Muốn chặn phải liệt kê hàng ngàn tên miền con rất bất khả thi.
> 2. **Bị phần mềm diệt virus khóa:** Các phần mềm Antivirus (Windows Defender) thường khóa quyền ghi file `hosts` vì đây là mục tiêu hàng đầu của mã độc Trojan.
> 3. **Không hỗ trợ SafeSearch CNAME Rewriting:** File `hosts` không thể biến đổi bản ghi CNAME cho YouTube hay Google.
> 4. **Trễ bộ nhớ đệm:** Hệ điều hành Windows lưu cache file `hosts` rất lâu, khi phụ huynh đổi luật thì máy tính không cập nhật ngay.

#### ❓ Câu 479: Thầy hỏi: Hàm kiểm tra domain trong mã nguồn tên là gì? Nằm ở dòng nào của `agent/dns_proxy.py`?
> **💡 Trả lời:** Dạ thưa Thầy, hàm đó tên là `is_blocked(self, domain: str) -> bool` nằm từ **dòng 85 đến dòng 112** trong tệp `agent/dns_proxy.py`.

#### ❓ Câu 480: Thầy hỏi: Bài test `test_domain_filtering_wildcard` trong `tests/test_phase3_network.py` kiểm tra những ca nào?
> **💡 Trả lời:** Dạ bài test kiểm tra 5 trường hợp biên: (1) Khớp chính xác tên miền gốc `tiktok.com`; (2) Khớp tên miền phụ cấp 1 `m.tiktok.com`; (3) Khớp tên miền phụ cấp 2 `v16.m.tiktok.com`; (4) Không chặn tên miền tương đồng nhưng khác nhãn `not-tiktok.com`; (5) Đảm bảo tên miền trong Immunity Whitelist `moet.gov.vn` luôn trả về False (không chặn). Toàn bộ 5 ca đều PASSED 100%.

---

# SLIDE 25: KỸ THUẬT LÕI 3 (F2): CƯỠNG CHẾ SAFESEARCH & YOUTUBE CONTENT FILTERING (CÂU 481 - 500)

#### ❓ Câu 481: Thầy hỏi: SafeSearch là gì và tại sao phụ huynh cần nó khi đã có DNS Sinkhole chặn web đen?
> **💡 Trả lời:** Dạ thưa Thầy, DNS Sinkhole chỉ chặn được các trang web đen khi biết trước tên miền cụ thể (ví dụ trong danh sách Blacklist). Tuy nhiên, nếu trẻ lên các công cụ tìm kiếm hợp pháp như Google, Bing và gõ các từ khóa nhạy cảm thì Google vẫn có thể hiển thị hàng loạt hình ảnh bạo lực, khiêu dâm ngay trên trang kết quả `google.com` (một trang web sạch). **SafeSearch** là bộ lọc trí tuệ nhân tạo nội tại của chính Google/Microsoft giúp gạn lọc toàn bộ các hình ảnh, video độc hại đó khỏi kết quả tìm kiếm.

#### ❓ Câu 482: Thầy hỏi: Nếu không có SafeSearch, trẻ tìm từ khóa nhạy cảm trên Google Hình ảnh thì DNS Sinkhole có chặn được không?
> **💡 Trả lời:** Dạ thưa Thầy, DNS Sinkhole **hoàn toàn bất lực trong tình huống này**! Bởi vì tên miền mà trẻ đang kết nối là `images.google.com` hoặc `www.google.com` — đây là các tên miền dịch vụ học tập hợp pháp, không thể đưa vào danh sách đen để chặn được. Do đó, bắt buộc phải có kỹ thuật DNS VIP Rewriting để ép Google kích hoạt chế độ SafeSearch từ phía máy chủ.

#### ❓ Câu 483: Thầy hỏi: Bản chất kỹ thuật của DNS VIP Rewriting là gì? Khác gì với Sinkholing trả về 0.0.0.0?
> **💡 Trả lời:** Dạ thưa Thầy:
> - **DNS Sinkholing:** Trả về IP chết `0.0.0.0` để dập tắt hoàn toàn kết nối tới trang web cấm.
> - **DNS VIP Rewriting:** Không dập tắt kết nối, mà **đánh tráo có chủ đích (Spoofing/Rewriting)** địa chỉ IP trả về: Thay vì trả về cụm IP máy chủ tìm kiếm thông thường của Google, Proxy sẽ trả về địa chỉ IP của một cụm máy chủ đặc biệt gọi là **VIP (Virtual IP)** do chính Google cấu hình riêng cho các trường học và tổ chức giáo dục. Cụm máy chủ này cưỡng chế bật 100% bộ lọc nội dung mà người dùng không thể tắt.

#### ❓ Câu 484: Thầy hỏi: Địa chỉ IP VIP của Google SafeSearch là bao nhiêu? Tại sao lại có địa chỉ IP này?
> **💡 Trả lời:** Dạ thưa Thầy, địa chỉ IP VIP của Google SafeSearch là:  
> $$	extbf{216.239.38.120}$$  
> (Tương ứng với tên miền CNAME chính thức: `forcesafesearch.google.com`).  
> Đây là địa chỉ IP được tập đoàn Google công bố chính thức toàn cầu trong tài liệu quản trị mạng giáo dục của họ, dành riêng cho các quản trị viên mạng trường học áp dụng chính sách bảo vệ học sinh.

#### ❓ Câu 485: Thầy hỏi: Google có rất nhiều tên miền tìm kiếm quốc gia, cấu hình rewrite xử lý `google.com` và `google.com.vn` ra sao?
> **💡 Trả lời:** Dạ thưa Thầy, trong `agent/dns_proxy.py`, nhóm sử dụng quy tắc khớp hậu tố: Mọi truy vấn có tên miền kết thúc bằng `.google.com` hoặc các đuôi quốc gia như `.google.com.vn`, `.google.com.sg` đều được bộ lọc nhận diện và tự động ánh xạ trả về địa chỉ IP VIP `216.239.38.120`.

#### ❓ Câu 486: Thầy hỏi: Đối với Microsoft Bing, tên miền VIP là gì và IP trả về là bao nhiêu?
> **💡 Trả lời:** Dạ thưa Thầy:
> - Tên miền VIP chính thức của Microsoft Bing là: `strict.bing.com`.
> - Địa chỉ IP VIP tương ứng là: **`204.79.197.220`**.  
> Mọi truy vấn tới `www.bing.com` đều được Proxy viết lại thành địa chỉ IP này, kích hoạt chế độ tìm kiếm nghiêm ngặt (Strict Search) của Microsoft.

#### ❓ Câu 487: Thầy hỏi: YouTube Restricted Mode hoạt động trên cơ chế nào? Tên miền VIP của YouTube là gì?
> **💡 Trả lời:** Dạ thưa Thầy, YouTube Restricted Mode (Chế độ hạn chế của YouTube) sử dụng CNAME VIP chính thức của Google là:  
> $$	extbf{restrict.youtube.com}$$  
> Khi trẻ truy vấn `www.youtube.com`, `m.youtube.com` hoặc `youtubei.googleapis.com`, DNS Proxy chuyển hướng sang máy chủ hạn chế. Cụm máy chủ này tự động ẩn toàn bộ các video bị gắn cờ nhạy cảm, tắt tính năng bình luận (comments) dưới video để bảo vệ tâm lý trẻ, và loại bỏ các nội dung bạo lực.

#### ❓ Câu 488: Thầy hỏi: Khi truy vấn `www.google.com`, DNS Proxy trả về bản ghi CNAME hay bản ghi A trực tiếp?
> **💡 Trả lời:** Dạ thưa Thầy, Proxy trả về **Bản ghi A (A Record) chứa trực tiếp IP `216.239.38.120`**. Sở dĩ trả về bản ghi A thay vì CNAME là để tối ưu hóa hiệu năng: Trình duyệt nhận được địa chỉ IP ngay lập tức mà không phải tốn thêm một vòng truy vấn đệ quy thứ hai để phân giải tên miền CNAME `forcesafesearch.google.com`, giúp tốc độ tải trang Google của trẻ nhanh hơn.

#### ❓ Câu 489: Thầy hỏi: Trình duyệt có báo lỗi cảnh báo chứng chỉ SSL/TLS khi truy cập IP VIP SafeSearch không? Tại sao?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn KHÔNG báo lỗi chứng chỉ SSL/TLS!**  
> Đây là điểm mấu chốt kỹ thuật: Cụm máy chủ tại IP `216.239.38.120` là do chính Google sở hữu và quản lý. Chứng chỉ số SSL/TLS trên cụm máy chủ này có chứa đầy đủ tên miền Subject Alternative Name (SAN) cho `*.google.com`. Khi trình duyệt bắt tay TLS, máy chủ Google trình chứng chỉ xịn 100%, trình duyệt xác thực hợp lệ màu xanh mà không hề có bất kỳ cảnh báo bảo mật nào!

#### ❓ Câu 490: Thầy hỏi: Nếu trẻ mở tab Ẩn danh (Incognito Mode) của Chrome thì SafeSearch có bị tắt không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn không thể tắt được!**  
> Chế độ ẩn danh chỉ xóa lịch sử duyệt web và cookie cục bộ trên máy, nhưng mọi yêu cầu mạng của tab ẩn danh vẫn bắt buộc phải đi qua card mạng Windows, và gói tin DNS vẫn rơi vào DNS Proxy của OGK. Vì địa chỉ IP kết nối đến là máy chủ VIP của Google nên giao diện Google luôn hiển thị dòng chữ: *"SafeSearch is locked on by your network administrator"* (SafeSearch đã bị khóa bật bởi quản trị mạng của bạn) kèm biểu tượng ổ khóa.

#### ❓ Câu 491: Thầy hỏi: Nếu trẻ đăng nhập tài khoản Google cá nhân đã tắt SafeSearch trong phần Cài đặt thì hệ thống có ép được không?
> **💡 Trả lời:** Dạ thưa Thầy, **vẫn ép buộc thành công 100%!**  
> Cấu hình phần cứng tại máy chủ VIP `216.239.38.120` của Google có độ ưu tiên cao nhất, ghi đè (override) toàn bộ cấu hình cá nhân của tài khoản người dùng. Dù tài khoản Google của trẻ có chọn "Tắt SafeSearch", máy chủ Google vẫn từ chối và thực thi lọc nghiêm ngặt.

#### ❓ Câu 492: Thầy hỏi: YouTube Restricted Mode có chặn được toàn bộ video 18+ không? Giới hạn kỹ thuật của nó là gì?
> **💡 Trả lời:** Dạ thưa Thầy, YouTube Restricted Mode dựa trên thuật toán phân loại tự động của Google và báo cáo cộng đồng, loại bỏ được khoảng 95-98% video nhạy cảm. Giới hạn kỹ thuật là nó không thể kiểm soát các video mới tải lên chưa kịp gắn nhãn. Do đó, OGK kết hợp thêm tầng quản trị thời gian: Cho phép phụ huynh giới hạn thời lượng xem YouTube mỗi ngày không quá 60 phút.

#### ❓ Câu 493: Thầy hỏi: DuckDuckGo có chế độ tìm kiếm an toàn qua DNS không? Tên miền là gì?
> **💡 Trả lời:** Dạ có thưa Thầy. Công cụ tìm kiếm ẩn danh DuckDuckGo cũng hỗ trợ SafeSearch qua DNS: Tên miền CNAME an toàn là `safe.duckduckgo.com` trỏ về IP `52.142.124.215`.

#### ❓ Câu 494: Thầy hỏi: Tại sao không dùng tiện ích mở rộng (Browser Extension) để bật SafeSearch mà phải dùng DNS?
> **💡 Trả lời:** Dạ vì tiện ích mở rộng (Extension) có 3 điểm yếu chí mạng: (1) Trẻ dễ dàng vào mục quản lý Extensions bấm nút Gỡ bỏ (Remove); (2) Không hoạt động trong tab Ẩn danh nếu trẻ không cấp quyền; (3) Hoàn toàn không áp dụng được cho các trình duyệt khác mà trẻ tự tải về (như Cốc Cốc, Brave, Opera). Sử dụng DNS ở tầng mạng giải quyết triệt để cho mọi trình duyệt trên máy tính.

#### ❓ Câu 495: Thầy hỏi: Nếu Google thay đổi địa chỉ IP của SafeSearch trong tương lai thì hệ thống xử lý ra sao?
> **💡 Trả lời:** Dạ thưa Thầy, địa chỉ IP VIP được cấu hình dưới dạng biến linh hoạt trong tệp cấu hình của Agent. Khi Google có sự thay đổi hạ tầng, Server có thể tự động đồng bộ địa chỉ IP mới xuống toàn bộ các Agent qua bản tin WebSocket mà không cần phải biên dịch lại mã nguồn phần mềm.

#### ❓ Câu 496: Thầy hỏi: Cấu hình SafeSearch trong OGK được lưu trong file nào? Phụ huynh có bật/tắt tùy ý được không?
> **💡 Trả lời:** Dạ thưa Thầy, tính năng SafeSearch được quản lý qua cờ `enforce_safesearch: bool` trong bảng `rules` trên cơ sở dữ liệu Server và đồng bộ vào `agent_rules.json` trên máy con. Trên Dashboard phụ huynh có một nút gạt bật/tắt trực quan, cho phép phụ huynh chủ động kích hoạt hoặc tạm dừng tính năng này.

#### ❓ Câu 497: Thầy hỏi: Proxy xử lý như thế nào nếu người dùng gõ trực tiếp địa chỉ IP của Google vào thanh địa chỉ trình duyệt?
> **💡 Trả lời:** Dạ thưa Thầy, trong thực tế hầu như không người dùng nào nhớ được địa chỉ IP để gõ. Hơn nữa, các trang web hiện đại sử dụng giao thức HTTPS và công nghệ chia sẻ máy chủ tên miền ảo (Virtual Hosting qua SNI). Nếu gõ trực tiếp IP lên thanh địa chỉ, chứng chỉ SSL của Google sẽ báo lỗi tên miền không khớp (Certificate Name Mismatch), ngăn chặn việc truy cập thẳng qua IP.

#### ❓ Câu 498: Thầy hỏi: Độ trễ khi thực hiện DNS Rewrite SafeSearch so với truy vấn DNS bình thường có chênh lệch không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn không có chênh lệch!**  
> Vì khi phát hiện tên miền là `google.com`, Proxy trả về ngay địa chỉ IP `216.239.38.120` đã lưu sẵn trong RAM mà không cần phải chuyển tiếp gói tin ra ngoài Internet. Độ trễ của thao tác Rewrite SafeSearch chỉ là **0.85 mili-giây**, tương đương với tốc độ của một truy vấn Sinkhole thông thường.

#### ❓ Câu 499: Thầy hỏi: Mã nguồn hàm ghi đè SafeSearch tên là gì trong `agent/dns_proxy.py`?
> **💡 Trả lời:** Dạ thưa Thầy, hàm đó tên là `handle_safesearch_rewrite(self, domain: str, qtype: int) -> DNSRecord` nằm ở dòng 120 đến 145 trong tệp `agent/dns_proxy.py`.

#### ❓ Câu 500: Thầy hỏi: Bài test nào trong test suite xác nhận việc phân giải Google trả về đúng IP VIP 216.239.38.120?
> **💡 Trả lời:** Dạ thưa Thầy, đó là bài test `test_safesearch_enforcement_google_bing` nằm trong tệp `tests/test_phase3_network.py`. Bài test gửi gói tin truy vấn cho `www.google.com` và `www.bing.com`, sau đó phân tích gói tin nhị phân phản hồi, kiểm tra chính xác giá trị trường RDATA trùng khớp với các chuỗi byte của IP `216.239.38.120` và `204.79.197.220`. Kết quả test đạt PASSED 100%.

# SLIDE 26: KỸ THUẬT LÕI 4 (F2 & M3): VÔ HIỆU HÓA DoH BẰNG NXDOMAIN CANARY DOMAIN (CÂU 501 - 520)

#### ❓ Câu 501: Thầy chỉ vào slide hỏi: DoH là viết tắt của từ gì? Giao thức này được chuẩn hóa trong RFC nào?
> **💡 Trả lời:** Dạ thưa Thầy, **DoH** là viết tắt của **DNS over HTTPS**. Giao thức này được Hiệp hội Kỹ sư Mạng Quốc tế (IETF) chuẩn hóa trong văn bản **RFC 8484** vào tháng 10 năm 2018.

#### ❓ Câu 502: Thầy hỏi: Tại sao DoH lại là "cơn ác mộng" đối với các hệ thống quản trị mạng gia đình và tường lửa truyền thống?
> **💡 Trả lời:** Dạ thưa Thầy, vì truyền thống DNS hoạt động không mã hóa trên cổng UDP 53, tường lửa và Proxy có thể dễ dàng nhìn thấy và lọc được. Tuy nhiên, DoH đóng gói toàn bộ gói tin DNS vào các truy vấn HTTPS tiêu chuẩn trên cổng **TCP 443**, mã hóa bằng TLS 1.3. Lưu lượng DoH trộn lẫn hoàn toàn với lưu lượng duyệt web thông thường, khiến tường lửa truyền thống hoàn toàn bị "mù", không thể phân biệt đâu là truy vấn tìm kiếm đâu là dữ liệu web, từ đó bị qua mặt 100%.

#### ❓ Câu 503: Thầy hỏi: Trình duyệt đóng gói truy vấn DNS vào bản tin HTTPS như thế nào? Cổng dịch vụ là cổng mấy?
> **💡 Trả lời:** Dạ thưa Thầy, theo RFC 8484, trình duyệt tạo một bản tin HTTP POST (hoặc GET) gửi tới máy chủ phân giải DoH (như `https://cloudflare-dns.com/dns-query` hoặc `https://dns.google/dns-query`) trên cổng **TCP 443**. Header của bản tin thiết lập `Content-Type: application/dns-message`, và phần thân (Body) chứa nguyên vẹn chuỗi byte nhị phân của gói tin DNS theo chuẩn RFC 1035.

#### ❓ Câu 504: Thầy hỏi: DoT (DNS over TLS) khác gì với DoH? Cổng chuẩn của DoT là cổng bao nhiêu?
> **💡 Trả lời:** Dạ thưa Thầy:
> - **DoT (RFC 7858):** Mã hóa DNS trực tiếp bằng lớp TLS trên một cổng mạng chuyên dụng riêng biệt là cổng **TCP 853**. DoT không sử dụng giao thức HTTP.
> - **DoH (RFC 8484):** Đóng gói DNS bên trong giao thức HTTP/2 hoặc HTTP/3 trên cổng chung **TCP 443**.
> DoT dễ quản lý hơn vì tường lửa chỉ cần khóa cổng 853 là ngăn chặn được, còn DoH chạy chung cổng 443 với toàn bộ mạng Internet toàn cầu nên không thể chặn bằng cổng được.

#### ❓ Câu 505: Thầy hỏi: Hệ thống OGK chặn DoT bằng phương thức kỹ thuật nào?
> **💡 Trả lời:** Dạ thưa Thầy, trong `agent/dns_watchdog.py`, Agent tự động kiểm tra và thiết lập một luật trên Windows Firewall thông qua lệnh `netsh advfirewall firewall`:  
> Chặn toàn bộ lưu lượng ra ngoài (Outbound Traffic) trên cổng đích **TCP 853**. Mọi ứng dụng cố gắng mở kết nối DoT đều bị tường lửa hệ điều hành ngắt kết nối ngay lập tức.

#### ❓ Câu 506: Thầy hỏi: Khái niệm "Canary Domain" bắt nguồn từ đâu? Ý nghĩa hình tượng "chim hoàng yến" là gì?
> **💡 Trả lời:** Dạ thưa Thầy, thuật ngữ này bắt nguồn từ lịch sử ngành khai mỏ than thế kỷ 19: Các thợ mỏ mang theo một con chim hoàng yến (Canary) xuống hầm lò vì loài chim này rất nhạy cảm với khí độc CO/Methane. Nếu chim chết hoặc ngất đi, thợ mỏ biết ngay hầm có khí độc và lập tức rút lui. Trong mạng máy tính, **Canary Domain** là một tên miền đặc biệt dùng để "báo bão" cho phần mềm biết môi trường mạng có đang áp dụng chính sách kiểm duyệt hay không.

#### ❓ Câu 507: Thầy hỏi: Tên miền Canary tiêu chuẩn quốc tế của Firefox và Chromium là gì?
> **💡 Trả lời:** Dạ thưa Thầy, tên miền Canary tiêu chuẩn quốc tế được Mozilla và Google thống nhất là:  
> $$	extbf{use-application-dns.net}$$

#### ❓ Câu 508: Thầy hỏi: Tại sao lại chọn tên miền `use-application-dns.net`? Ai quy định tên miền này?
> **💡 Trả lời:** Dạ thưa Thầy, tên miền này do **Mozilla Foundation** đăng ký và quản lý, sau đó được dự án mã nguồn mở **Chromium (nền tảng của Chrome, Microsoft Edge, Brave, Cốc Cốc)** chính thức công nhận và tích hợp vào nhân trình duyệt từ năm 2019 theo tiêu chuẩn đồng thuận của các nhà phát triển trình duyệt web toàn cầu.

#### ❓ Câu 509: Thầy hỏi: Mã lỗi `NXDOMAIN` trong chuẩn DNS RFC 1035 có ý nghĩa gì? Giá trị RCODE bằng mấy?
> **💡 Trả lời:** Dạ thưa Thầy:
> - `NXDOMAIN` là viết tắt của **Non-Existent Domain (Tên miền không tồn tại)**.
> - Giá trị trường mã phản hồi là **`RCODE = 3`** (trong 4 bit cuối của trường Flags).  
> Mã này thông báo chính thức cho Client rằng tên miền đang tìm kiếm hoàn toàn không tồn tại trong không gian tên miền Internet.

#### ❓ Câu 510: Thầy hỏi: Khi nhận được phản hồi NXDOMAIN cho Canary domain, trình duyệt hành xử như thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, theo tài liệu kỹ thuật của Mozilla và Chromium: Khi người dùng khởi động trình duyệt, trước khi tự động kích hoạt tính năng DoH ngầm, trình duyệt sẽ gửi một truy vấn DNS chuẩn UDP 53 hỏi `use-application-dns.net`.  
> Nếu nhận được phản hồi là `NXDOMAIN (RCODE=3)`, trình duyệt sẽ suy diễn rằng: *"Mạng gia đình/trường học này đang có một hệ thống giám sát lọc mạng hợp pháp của phụ huynh/quản trị viên"*.  
> Trình duyệt sẽ **ngay lập tức tự vô hiệu hóa (disable) tính năng DoH**, và quay trở lại sử dụng cơ chế phân giải DNS mặc định của hệ điều hành trên cổng 53 — nơi mà OGK Sinkhole Proxy đang kiểm soát 100%!

#### ❓ Câu 511: Thầy hỏi: Tính năng Canary này có áp dụng cho Google Chrome không? Microsoft Edge có tuân thủ không?
> **💡 Trả lời:** Dạ thưa Thầy, **cả Google Chrome và Microsoft Edge đều tuân thủ 100%!**  
> Vì cả hai trình duyệt này đều dùng chung nhân Chromium. Logic kiểm tra Canary Domain `use-application-dns.net` được viết trực tiếp trong mã nguồn C++ của Chromium (tệp `net/dns/dns_transaction.cc`), do đó mọi trình duyệt chạy nhân Chromium trên máy tính trẻ em đều tự động tôn trọng tín hiệu này.

#### ❓ Câu 512: Thầy hỏi: Nếu trẻ chủ động vào Settings của Chrome và chọn "Always use Secure DNS" với Custom DoH Provider thì sao?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm đã dự liệu kịch bản này trong Báo cáo M3:  
> Khi trẻ cố tình cấu hình thủ công (Force Secure DNS) trỏ về Cloudflare hoặc Google DoH, trình duyệt bắt buộc phải phân giải tên miền của DoH Provider đó (như `cloudflare-dns.com` hoặc `dns.google`) trước khi thiết lập TLS.  
> DNS Proxy của OGK lập tức chặn các tên miền này về `0.0.0.0` ngay từ đầu, khiến trình duyệt không thể kết nối tới DoH Resolver và buộc phải fallback (lùi về) cơ chế DNS tiêu chuẩn của hệ điều hành.

#### ❓ Câu 513: Thầy hỏi: OGK làm gì để chặn trẻ kết nối đến các DoH Resolvers công cộng phổ biến qua địa chỉ IP trực tiếp (như 1.1.1.1 hay 8.8.8.8)?
> **💡 Trả lời:** Dạ thưa Thầy, trong `agent/dns_watchdog.py`, hệ thống phối hợp thiết lập các luật tường lửa Windows Firewall chặn gói tin ra cổng 443 đối với các địa chỉ IP DoH công cộng nổi tiếng (`1.1.1.1`, `1.0.0.1`, `8.8.8.8`, `8.8.4.4`, `9.9.9.9`). Trình duyệt không thể mở kết nối HTTPS tới các IP này và buộc phải phân giải qua `127.0.0.1:53` của OGK.

#### ❓ Câu 514: Thầy hỏi: Tại sao nhóm không dùng kỹ thuật tấn công Man-in-the-Middle (MITM) giải mã HTTPS để chặn DoH?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm **kiên quyết từ chối kỹ thuật MITM SSL Bumping** vì 2 lý do:
> 1. **Vi phạm đạo đức và pháp lý nghiêm trọng:** Kỹ thuật MITM yêu cầu cài chứng chỉ số giả mạo Root CA vào máy tính con để giải mã toàn bộ lưu lượng HTTPS. Khi đó, phần mềm có thể nhìn thấy toàn bộ mật khẩu ngân hàng, thông tin thẻ tín dụng của phụ huynh khi dùng chung máy, vi phạm Điều 21 Luật Trẻ Em và Điều 20 Nghị định 13.
> 2. **Phá vỡ tính toàn vẹn của trình duyệt:** Kỹ thuật MITM phá vỡ cơ chế bảo mật HTTP Strict Transport Security (HSTS) và Certificate Transparency, gây ra vô số lỗi cảnh báo màu đỏ làm gián đoạn việc học trực tuyến của trẻ.

#### ❓ Câu 515: Thầy hỏi: Hậu quả pháp lý nếu cài chứng chỉ Root CA giả mạo lên máy tính của trẻ để soi DoH?
> **💡 Trả lời:** Dạ thưa Thầy, theo Điều 289 Bộ luật Hình sự Việt Nam về tội xâm nhập trái phép mạng máy tính và Điều 20 Nghị định 13/2023/NĐ-CP: Việc giải mã dữ liệu cá nhân không có căn cứ hoặc tạo backdoor trung gian đánh chặn thông tin liên lạc được coi là hành vi xâm phạm bí mật đời tư bất hợp pháp. Giải pháp Canary NXDOMAIN của OGK là phương thức phòng vệ chuẩn mực quốc tế, không giải mã, không can thiệp đời tư.

#### ❓ Câu 516: Thầy hỏi: Độ trễ của việc trả về NXDOMAIN cho gói tin Canary là bao nhiêu mili-giây?
> **💡 Trả lời:** Dạ thưa Thầy, độ trễ đo được là **0.78 mili-giây**. Vì khi phát hiện chuỗi QNAME là `use-application-dns.net`, Proxy lập tức sinh gói tin phản hồi với cờ `RCODE = 3` ngay trong bộ nhớ RAM mà không cần thực hiện bất kỳ thao tác I/O nào.

#### ❓ Câu 517: Thầy hỏi: Có khi nào gói tin Canary bị gửi lặp lại nhiều lần làm nghẽn Proxy không?
> **💡 Trả lời:** Dạ không thưa Thầy. Vì gói tin NXDOMAIN trả về của OGK có thiết lập trường thời gian sống TTL (Time-To-Live) là **300 giây (5 phút)**. Trình duyệt lưu kết quả này vào bộ nhớ đệm nội bộ và chỉ gửi lại gói tin thăm dò sau mỗi 5 phút hoặc khi mạng thay đổi trạng thái kết nối.

#### ❓ Câu 518: Thầy hỏi: Đoạn code trả về NXDOMAIN nằm ở hàm nào trong `agent/dns_proxy.py`?
> **💡 Trả lời:** Dạ thưa Thầy, đoạn code đó nằm trong hàm `handle_dns_request()` tại các dòng **150 đến 165** của tệp `agent/dns_proxy.py`. Cụ thể:
> ```python
> if qname.rstrip('.') == "use-application-dns.net":
>     reply = request.reply()
>     reply.header.rcode = getattr(RCODE, 'NXDOMAIN')
>     return reply.pack()
> ```

#### ❓ Câu 519: Thầy hỏi: Làm sao dùng Wireshark để chứng minh trình duyệt đã nhận được mã NXDOMAIN và quay về UDP 53?
> **💡 Trả lời:** Dạ thưa Thầy, chúng em dùng bộ lọc Wireshark: `dns.flags.response == 1 && dns.qry.name == "use-application-dns.net"`.  
> Trên màn hình Wireshark, gói tin phản hồi từ `127.0.0.1` hiển thị rõ trường `Flags: 0x8183 (Standard query response, No error, Non-existent domain)`. Ngay sau gói tin này, Wireshark ghi nhận các gói tin truy vấn tên miền bình thường của trình duyệt bắt đầu xuất hiện dồn dập trên cổng UDP 53 tới `127.0.0.1`, chứng minh DoH đã bị tắt thành công.

#### ❓ Câu 520: Thầy hỏi: Bài kiểm thử tự động nào kiểm tra kịch bản Canary NXDOMAIN trong repo?
> **💡 Trả lời:** Dạ thưa Thầy, đó là bài test `test_doh_canary_domain_nxdomain` trong tệp `tests/test_phase3_network.py`. Bài test tạo gói tin nhị phân hỏi `use-application-dns.net`, gửi vào Proxy và đối soát: Cờ phản hồi bắt buộc phải có `RCODE == 3 (NXDOMAIN)` và phần Answer không có bất kỳ bản ghi A nào. Bài test đạt kết quả PASSED.

---

# SLIDE 27: KỸ THUẬT LÕI 5 (F2): KIỂM SOÁT ỨNG DỤNG BẰNG MÃ BĂM SHA-256 & TỐI ƯU mtime (CÂU 521 - 540)

#### ❓ Câu 521: Thầy hỏi: Tại sao không dùng tên tiến trình (`proc.name()`) để chặn game và phần mềm không mong muốn?
> **💡 Trả lời:** Dạ thưa Thầy, vì cơ chế lọc theo tên tiến trình rất ngây thơ và dễ bị qua mặt. Khi phụ huynh cấu hình cấm `League of Legends.exe` hay `RobloxPlayer.exe`, học sinh chỉ cần vào thư mục cài đặt, bấm đổi tên tệp thành `winword.exe` hoặc `calculator.exe`. Khi chạy, Windows hiển thị tiến trình là `winword.exe` và phần mềm giám sát thông thường sẽ hoàn toàn bị lừa, cho phép game chạy bình thường.

#### ❓ Câu 522: Thầy hỏi: Trẻ em đổi tên file `.exe` như thế nào để qua mặt các phần mềm giám sát thông thường?
> **💡 Trả lời:** Dạ học sinh chỉ cần thao tác đơn giản: Mở File Explorer, tìm đến thư mục cài game (thường nằm ở `AppData\Local` hoặc ổ `D:`), bấm chuột phải chọn Rename (hoặc phím F2), sửa tên file thực thi `.exe` thành tên một ứng dụng học tập bất kỳ, sau đó tạo Shortcut ra ngoài Desktop để chơi.

#### ❓ Câu 523: Thầy hỏi: Mã băm SHA-256 là gì? Tại sao đổi tên file nhưng mã băm SHA-256 lại không thay đổi?
> **💡 Trả lời:** Dạ thưa Thầy, **SHA-256 (Secure Hash Algorithm 256-bit)** là thuật toán băm mật mã học một chiều chuẩn quốc tế (FIPS 180-4). Thuật toán này băm **toàn bộ nội dung dữ liệu nhị phân (mã máy/bytecode)** bên trong tệp tin, chứ không băm chuỗi tên tệp. Tên tệp chỉ là một nhãn siêu dữ liệu trong bảng thư mục hệ điều hành. Dù học sinh có đổi tên file 100 lần, nội dung nhị phân bên trong không đổi thì kết quả chuỗi băm 64 ký tự hex của SHA-256 vẫn là duy nhất tuyệt đối.

#### ❓ Câu 524: Thầy hỏi: Nếu tệp thực thi game dung lượng 2 GB, đọc hết vào RAM để băm thì có bị tràn bộ nhớ không?
> **💡 Trả lời:** Dạ thưa Thầy, **chắc chắn sẽ làm tràn RAM (Out-Of-Memory Crash)** nếu dùng hàm `f.read()` đọc toàn bộ. Máy tính con sẽ lập tức bị đơ cứng, giật lag và hệ điều hành sẽ cưỡng chế tắt tiến trình Agent. Đó là lý do vì sao OGK không bao giờ đọc trọn gói tệp vào RAM.

#### ❓ Câu 525: Thầy hỏi: Thuật toán đọc theo khối (Chunked reading) của nhóm chia kích thước mỗi khối là bao nhiêu KB?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm chia nhỏ kích thước mỗi khối đọc đệm chính xác là:  
> $$	extbf{64 KB (65,536 Bytes)}$$

#### ❓ Câu 526: Thầy hỏi: Tại sao lại chọn kích thước khối đệm 64 KB mà không phải 4 KB hay 1 MB?
> **💡 Trả lời:** Dạ thưa Thầy, đây là kết quả tối ưu hóa kiến trúc phần cứng:
> - Nếu chọn **4 KB:** Kích thước quá nhỏ, số lần gọi hàm đọc hệ thống (System Calls `read()`) quá nhiều, làm tăng độ trễ chuyển ngữ cảnh (Context Switching Overhead) giữa User Mode và Kernel Mode.
> - Nếu chọn **1 MB:** Kích thước quá lớn, chiếm dụng bộ nhớ đệm L3 Cache của CPU không cần thiết.
> - Chọn **64 KB:** Đây là kích thước phân cụm khối tối ưu tương thích hoàn hảo với kích thước phân vùng bộ nhớ đệm (NTFS Cluster Allocation Unit & I/O Buffer Size) của hệ điều hành Windows, giúp thông lượng đọc đĩa đạt tốc độ tối đa của phần cứng.

#### ❓ Câu 527: Thầy hỏi: Chu kỳ quét tiến trình của Agent là bao nhiêu giây một lần? Có tốn tài nguyên không?
> **💡 Trả lời:** Dạ thưa Thầy, chu kỳ quét tiến trình được thiết lập là **5.0 giây một lần**. Chu kỳ này đủ nhanh để ngăn chặn trẻ chơi game (trẻ vừa bật game lên thì trong vòng tối đa 5s game đã bị tắt), đồng thời đủ dài để CPU nghỉ ngơi. Kết hợp với giải thuật mtime Cache, mức tiêu thụ CPU thực tế duy trì ở ngưỡng **0.0%**.

#### ❓ Câu 528: Thầy hỏi: Vấn đề nghẽn cổ chai I/O đĩa cứng (Disk Bottleneck) khi băm liên tục các file `.exe` là gì?
> **💡 Trả lời:** Dạ thưa Thầy, trên máy tính Windows thông thường luôn có khoảng 150 đến 250 tiến trình đang chạy. Nếu mỗi 5 giây Agent lại đọc toàn bộ ổ đĩa cứng để băm mã SHA-256 của 200 tệp tin này, ổ đĩa sẽ luôn trong tình trạng hoạt động 100% (Disk Active Time 100%), gây sụt giảm nghiêm trọng tốc độ máy tính, nhanh chai pin laptop và làm giảm tuổi thọ của ổ SSD.

#### ❓ Câu 529: Thầy hỏi: Thuật toán `mtime` cache là gì? `os.path.getmtime` đọc thông tin từ đâu trong Windows?
> **💡 Trả lời:** Dạ thưa Thầy, **`mtime`** là thuộc tính **Last Modified Time (Thời điểm chỉnh sửa cuối cùng)** của tệp tin.  
> Hàm `os.path.getmtime(path)` ánh xạ trực tiếp xuống Win32 API `GetFileInformationByHandle` của hệ điều hành. Hàm này chỉ đọc siêu dữ liệu tệp tin được lưu sẵn trong bảng **Master File Table (MFT)** của phân vùng NTFS, **hoàn toàn không phải đọc nội dung tệp tin trên ổ đĩa**.

#### ❓ Câu 530: Thầy hỏi: Tại sao đọc `mtime` từ NTFS Master File Table (MFT) chỉ mất 0.02 ms?
> **💡 Trả lời:** Dạ thưa Thầy, vì bảng Master File Table (MFT) của NTFS là chỉ mục hệ thống luôn được hệ điều hành Windows nạp sẵn vào bộ nhớ RAM đệm (File System Cache). Thao tác đọc `mtime` thực chất chỉ là một phép tra cứu con trỏ bộ nhớ RAM nội bộ của kernel, không kích hoạt cơ chế đọc vật lý (Physical I/O) trên bề mặt đĩa từ hay chip nhớ NAND flash, do đó tốc độ đạt mức tức thì **0.02 mili-giây**!

#### ❓ Câu 531: Thầy hỏi: Cấu trúc từ điển bộ nhớ đệm Cache lưu trong RAM của Agent gồm những khóa và giá trị nào?
> **💡 Trả lời:** Dạ thưa Thầy, cấu trúc bộ nhớ đệm trong `agent/app_monitor.py` là một từ điển Python (Dictionary):  
> $$	ext{hash\_cache} = \{ 	extbf{file\_path} : (	extbf{mtime}, 	extbf{sha256\_digest}) \}$$  
> - **Khóa (Key):** Đường dẫn tuyệt đối tới tệp thực thi (ví dụ: `C:\Program Files\Game\game.exe`).  
> - **Giá trị (Value):** Một bộ Tuple gồm mốc thời gian sửa đổi gần nhất và chuỗi mã băm SHA-256 đã tính toán trước đó.

#### ❓ Câu 532: Thầy hỏi: Khi nào thì một tiến trình bị buộc phải băm lại mã SHA-256 trên đĩa cứng?
> **💡 Trả lời:** Dạ thưa Thầy, chỉ xảy ra trong 2 tình huống duy nhất:
> 1. Tệp thực thi đó lần đầu tiên xuất hiện trong danh sách tiến trình của máy tính (chưa từng có trong Cache).
> 2. Mốc thời gian sửa đổi hiện tại $T_{	ext{current}}$ khác với mốc thời gian lưu trong Cache ($T_{	ext{cached}}$), báo hiệu tệp tin đã bị ghi đè, cập nhật bản vá hoặc can thiệp chỉnh sửa.  
> Mọi chu kỳ quét 5s còn lại, Agent chỉ tra cứu Cache trong RAM với thời gian 0.001 ms!

#### ❓ Câu 533: Thầy hỏi: Nếu trẻ dùng công cụ sửa đổi binary (Hex Editor) chèn thêm 1 byte rác vào cuối file `.exe` thì sao?
> **💡 Trả lời:** Dạ thưa Thầy, khi trẻ dùng Hex Editor chèn byte rác và lưu lại:
> - Thuộc tính `mtime` của tệp tin trên NTFS lập tức bị thay đổi.
> - Ở chu kỳ 5 giây tiếp theo, Agent phát hiện $T_{	ext{current}} 
e T_{	ext{cached}}$ và lập tức băm lại file.
> - Hơn nữa, việc tự ý chèn byte rác vào một file thực thi PE (Portable Executable) của Windows sẽ phá vỡ cấu trúc Section Table hoặc làm hỏng Chữ ký số Authenticode của nhà sản xuất, khiến Windows từ chối khởi chạy file đó (`The application was unable to start correctly`).

#### ❓ Câu 534: Thầy hỏi: Các ngoại lệ hệ điều hành `AccessDenied`, `NoSuchProcess`, `ZombieProcess` được xử lý như thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, trong `agent/app_monitor.py`:
> - `psutil.AccessDenied`: Bắt riêng ngoại lệ và bỏ qua (`pass`), đây là các tiến trình nhân hệ thống của Windows chạy ở Session 0 (`System`, `csrss.exe`) được hệ điều hành bảo vệ.
> - `psutil.NoSuchProcess`: Bắt ngoại lệ và bỏ qua, xảy ra khi một tiến trình ngắn hạn vừa thoát trước khi kịp quét.
> - `psutil.ZombieProcess`: Bắt ngoại lệ, giải phóng tài nguyên và loại khỏi danh sách theo dõi.  
> Nhờ đó, Agent không bao giờ bị sập (crash) do các biến động tức thời của hệ điều hành.

#### ❓ Câu 535: Thầy hỏi: Khi phát hiện game cấm, Agent đóng tiến trình bằng `terminate()` hay `kill()`? Sự khác nhau là gì?
> **💡 Trả lời:** Dạ thưa Thầy, Agent áp dụng quy trình 2 pha:
> 1. Đầu tiên gọi `proc.terminate()`: Gửi tín hiệu `SIGTERM` / thông điệp `WM_CLOSE` yêu cầu ứng dụng đóng lịch sự và lưu trạng thái, chờ tối đa 2.0 giây (`proc.wait(timeout=2.0)`).
> 2. Nếu sau 2.0 giây ứng dụng cố tình phớt lờ hoặc treo đơ, Agent lập tức kích hoạt pha 2 gọi `proc.kill()` để cưỡng chế hủy diệt tiến trình ngay lập tức ở mức nhân hệ điều hành.

#### ❓ Câu 536: Thầy hỏi: Win32 API gốc nào được gọi ở tầng C-Runtime để cưỡng chế hủy tiến trình?
> **💡 Trả lời:** Dạ thưa Thầy, đó là hàm Win32 API gốc trong thư viện `kernel32.dll`:  
> $$	extbf{TerminateProcess(HANDLE hProcess, UINT uExitCode)}$$  
> Hàm này ra lệnh trực tiếp cho bộ điều phối nhân Windows thu hồi toàn bộ bộ nhớ và handle của tiến trình với mã thoát chỉ định, không cho phép ứng dụng hoãn lệnh.

#### ❓ Câu 537: Thầy hỏi: Agent có phân biệt được tiến trình hệ thống trọng yếu (như `explorer.exe`, `svchost.exe`) để tránh kill nhầm không?
> **💡 Trả lời:** Dạ thưa Thầy có bảo vệ nghiêm ngặt: Trong `agent/app_monitor.py` có danh sách **Critical System Whitelist** gồm: `explorer.exe`, `svchost.exe`, `lsass.exe`, `winlogon.exe`, `csrss.exe`, `services.exe` và chính tiến trình của OGK. Dù phụ huynh có nhập nhầm mã hash của các ứng dụng này, hàm kiểm tra luôn bỏ qua, đảm bảo máy tính không bao giờ bị lỗi màn hình xanh (BSOD).

#### ❓ Câu 538: Thầy hỏi: Mức tiêu thụ CPU đo đạc thực tế của module App Monitor là bao nhiêu %?
> **💡 Trả lời:** Dạ thưa Thầy, theo số liệu thực nghiệm đo đạc độc lập 30 lần trong Báo cáo M4: Mức tiêu thụ CPU trung bình là **0.0%**. Chỉ trong tích tắc khoảng 0.05 giây khi quét kiểm tra thì CPU có một đỉnh nhọn ngắn đo được là **0.12%**, hoàn toàn vô hình đối với người dùng.

#### ❓ Câu 539: Thầy hỏi: Đường dẫn file mã nguồn và tên class quản lý giám sát ứng dụng là gì?
> **💡 Trả lời:** Dạ thưa Thầy, mã nguồn nằm tại tệp `agent/app_monitor.py`, do lớp **`AppMonitor`** quản lý, trong đó hàm `scan_and_enforce()` thực hiện quét và cưỡng chế, hàm `get_file_sha256()` thực hiện băm khối 64KB kết hợp mtime cache.

#### ❓ Câu 540: Thầy hỏi: Bài test `test_app_monitor_sha256_detection` chứng minh điều gì trong báo cáo kiểm thử?
> **💡 Trả lời:** Dạ thưa Thầy, bài test tạo một tệp nhị phân giả lập game, ghi mã băm của nó vào danh sách cấm, sau đó đổi tên file thành `calc.exe` và khởi chạy một tiến trình con. Bài test kiểm tra: AppMonitor nhận diện chính xác mã SHA-256 bất chấp tên file đã bị đổi, gọi lệnh hủy tiến trình thành công và ghi nhận nhật ký vi phạm. Bài test đạt PASSED 100%.

---

# SLIDE 28: KỸ THUẬT LÕI 6 (NT3 & NT5): TIẾNG NÓI TRẺ EM — GIAO DIỆN XIN THÊM GIỜ & ĐỒNG BỘ HAI CHIỀU (CÂU 541 - 560)

#### ❓ Câu 541: Thầy hỏi: Nguyên tắc NT3 và NT5 trong Hiến chương OGK quy định điều gì?
> **💡 Trả lời:** Dạ thưa Thầy:
> - **Nguyên tắc NT3 (Quyền được lắng nghe & Giải trình):** Trẻ em không phải là đối tượng bị cai trị thụ động; trẻ có quyền được biết lý do mình bị hạn chế và có quyền đề xuất xin thêm thời gian cho các nhu cầu học tập chính đáng.
> - **Nguyên tắc NT5 (Kênh đối thoại hai chiều tức thì):** Phần mềm phải cung cấp cơ chế tương tác thời gian thực giữa hai bên, biến việc quản lý thiết bị thành một thỏa thuận gia đình minh bạch, tôn trọng lẫn nhau.

#### ❓ Câu 542: Thầy hỏi: Giao diện khay hệ thống (System Tray) của máy con được xây dựng bằng thư viện Python nào?
> **💡 Trả lời:** Dạ thưa Thầy, giao diện khay hệ thống được xây dựng bằng thư viện **`pystray`** kết hợp với thư viện đồ họa **`Pillow (PIL)`** để vẽ biểu tượng động thể hiện trạng thái (xanh lá = an toàn, vàng = sắp hết giờ, đỏ = bị khóa), cùng với **`tkinter`** để hiển thị các hộp thoại tương tác khi trẻ bấm vào menu.

#### ❓ Câu 543: Thầy hỏi: Trẻ em có thể xem được những thông tin gì từ giao diện của Agent trên máy tính mình?
> **💡 Trả lời:** Dạ khi bấm đúp vào icon OGK dưới khay hệ thống, trẻ xem được:
> 1. Thời gian sử dụng còn lại trong ngày (đếm lùi chính xác theo phút).
> 2. Khung giờ được phép sử dụng máy tính hôm nay.
> 3. Trạng thái kết nối tới máy chủ phụ huynh (Online / Offline).
> 4. Nút bấm "Xin thêm giờ" và nút "Báo cáo chặn nhầm trang web".

#### ❓ Câu 544: Thầy hỏi: Tính năng "Xin thêm giờ" (Request Extra Time) hoạt động theo luồng dữ liệu mạng như thế nào?
> **💡 Trả lời:** Dạ luồng dữ liệu mạng diễn ra qua 5 bước:
> 1. Trẻ chọn số phút xin thêm và nhập lý do trên hộp thoại máy con.
> 2. Agent đóng gói bản tin JSON gửi lên Server qua API `POST /api/devices/{device_id}/time-requests`.
> 3. Server lưu yêu cầu vào bảng `time_requests` và phát tín hiệu WebSocket `NEW_TIME_REQUEST` tới Dashboard phụ huynh.
> 4. Phụ huynh thấy thông báo pop-up trên Dashboard và bấm nút Phê duyệt (Approve).
> 5. Server gửi lệnh WebSocket `TIME_GRANTED` kèm số phút cộng thêm xuống máy con để cập nhật bộ đếm.

#### ❓ Câu 545: Thầy hỏi: Trẻ có thể chọn xin thêm bao nhiêu phút? Có tự gõ số tùy tiện 1000 phút được không?
> **💡 Trả lời:** Dạ thưa Thầy không thể gõ tùy tiện. Để tránh trẻ xin giờ vô tội vạ, giao diện cung cấp 3 nút chọn nhanh cố định: **15 phút, 30 phút, hoặc 60 phút**. Schema Pydantic trên Server `TimeRequestCreate` kiểm tra chặt chẽ điều kiện: `15 <= requested_minutes <= 120`, nếu gửi số phút sai lệch sẽ bị Server từ chối ngay với mã lỗi `422 Unprocessable Entity`.

#### ❓ Câu 546: Thầy hỏi: Khi trẻ bấm gửi yêu cầu, bản tin gửi lên Server qua REST API hay WebSocket?
> **💡 Trả lời:** Dạ thưa Thầy, gửi qua **REST API có xác thực Bearer Token của thiết bị**. Sở dĩ dùng REST API cho chiều gửi yêu cầu là để đảm bảo tính bền vững (Persistence): Bản tin đi kèm cơ chế Transaction của CSDL, đảm bảo nếu mạng chập chờn thì thư viện HTTP client sẽ có mã phản hồi xác nhận 200 OK rõ ràng. Kênh WebSocket sau đó được dùng cho chiều ngược lại để Server báo tin tức thời cho phụ huynh.

#### ❓ Câu 547: Thầy hỏi: Server lưu yêu cầu xin giờ vào bảng nào trong cơ sở dữ liệu?
> **💡 Trả lời:** Dạ thưa Thầy, Server lưu vào bảng **`time_requests`** trong CSDL SQLite, gồm các trường: `id`, `device_id`, `requested_minutes`, `reason`, `status` (PENDING, APPROVED, REJECTED), `created_at`, và `resolved_at`.

#### ❓ Câu 548: Thầy hỏi: Phụ huynh nhận được thông báo xin giờ trên Dashboard như thế nào (Real-time hay Polling)?
> **💡 Trả lời:** Dạ nhận được **Real-time 100% qua kênh WebSocket**. Dashboard phụ huynh duy trì kết nối WebSocket tới endpoint `/api/ws/parent`. Ngay khi bản tin xin giờ được ghi vào CSDL, Server gọi hàm `manager.broadcast_to_parent(parent_id, message)` đẩy thông báo xuống trình duyệt trong vòng **dưới 6 mili-giây**, phụ huynh nghe tiếng chuông thông báo và thấy hộp thoại phê duyệt nổi lên ngay lập tức mà không cần bấm F5 tải lại trang.

#### ❓ Câu 549: Thầy hỏi: Nếu phụ huynh duyệt đồng ý (Approve), Server đẩy lệnh gì xuống máy con qua WebSocket?
> **💡 Trả lời:** Dạ Server gửi bản tin JSON qua WebSocket tới kết nối của máy con:
> ```json
> {
>   "event": "TIME_GRANTED",
>   "extra_minutes": 30,
>   "timestamp": 1711789200
> }
> ```

#### ❓ Câu 550: Thầy hỏi: Agent nhận được lệnh cộng giờ thì xử lý bộ đếm thời gian `time.monotonic()` ra sao?
> **💡 Trả lời:** Dạ trong `agent/time_tracker.py`, Agent quản lý biến giới hạn thời gian trong ngày `daily_limit_seconds`. Khi nhận được sự kiện `TIME_GRANTED`, Agent cộng trực tiếp số giây được duyệt vào biến này:  
> $$	ext{daily\_limit\_seconds} += 	ext{extra\_minutes} 	imes 60$$  
> Bộ đếm phần cứng `time.monotonic()` vẫn tiếp tục tăng đều đặn, nhưng mốc thời gian hết hạn bị đẩy lùi xa hơn, giúp máy con tiếp tục hoạt động bình thường.

#### ❓ Câu 551: Thầy hỏi: Nếu máy con đang ở trạng thái bị khóa màn hình, khi được duyệt thêm giờ thì máy có tự mở khóa không?
> **💡 Trả lời:** Dạ thưa Thầy, vì lý do an ninh của hệ điều hành Windows, một ứng dụng người dùng không được phép tự ý mở khóa màn hình LockWorkStation mà không cần nhập mật khẩu Windows (để bảo vệ dữ liệu khi trẻ đi vắng). Tuy nhiên, khi được duyệt thêm giờ, Agent lập tức hủy cờ cưỡng chế khóa `is_locked = False`, phát âm thanh thông báo mở khóa, và trẻ chỉ cần đăng nhập mật khẩu Windows vào lại là máy tính sẽ sử dụng được ngay mà không bị Agent khóa lại nữa.

#### ❓ Câu 552: Thầy hỏi: Tính năng "Báo cáo chặn nhầm" (Report False Positive) giải quyết vấn đề gì trong thực tế?
> **💡 Trả lời:** Dạ giải quyết bài toán "Chặn nhầm tài liệu học tập": Trong thực tế, các bộ lọc DNS hoặc từ khóa đôi khi chặn nhầm các trang web phục vụ việc học của trẻ (ví dụ trang nghiên cứu sinh học, giáo dục giới tính hoặc tài liệu lập trình). Thay vì bất lực chịu trận, trẻ có nút bấm "Báo cáo chặn nhầm" để gửi tên miền đó về cho cha mẹ xem xét và mở khóa nhanh.

#### ❓ Câu 553: Thầy hỏi: Khi trẻ học trực tuyến bị chặn nhầm tài liệu, trẻ gửi phản hồi kèm những thông tin gì?
> **💡 Trả lời:** Dạ bản tin báo cáo gửi kèm: Tên miền bị chặn (`blocked_domain`), mốc thời gian bị chặn (`timestamp`), ứng dụng đang sử dụng (`browser_name`), và một đoạn giải thích ngắn của trẻ (ví dụ: *"Con cần tài liệu này để làm bài thuyết trình môn Sinh học"*).

#### ❓ Câu 554: Thầy hỏi: Phụ huynh xem báo cáo chặn nhầm ở đâu và có thể thêm nhanh vào danh sách cho phép (Whitelist) không?
> **💡 Trả lời:** Dạ trên Dashboard phụ huynh có tab **"Kháng nghị & Báo cáo" (Appeals & Reports)**. Tại mỗi dòng báo cáo của con, bên cạnh lý do có một nút bấm màu xanh: **"Cho phép tên miền này" (Add to Whitelist)**. Phụ huynh chỉ cần bấm nút này, tên miền lập tức được thêm vào Whitelist của thiết bị và đồng bộ xuống Agent trong 1 giây.

#### ❓ Câu 555: Thầy hỏi: Cơ chế chống spam: Nếu trẻ bấm nút xin giờ liên tục 100 lần thì hệ thống xử lý sao?
> **💡 Trả lời:** Dạ hệ thống áp dụng cơ chế chống spam 2 tầng:
> - **Tầng Client GUI:** Sau khi bấm nút gửi, nút bấm bị vô hiệu hóa (disabled) và hiển thị dòng chữ: *"Yêu cầu của bạn đang chờ phụ huynh xem xét..."*.
> - **Tầng Server API:** Module kiểm tra CSDL: Nếu thiết bị đang có một yêu cầu ở trạng thái `PENDING` chưa được xử lý, Server từ chối tiếp nhận yêu cầu mới và trả về mã lỗi `400 Bad Request` kèm thông báo: *"Bạn đã có một yêu cầu đang chờ duyệt, vui lòng không gửi lại"*.

#### ❓ Câu 556: Thầy hỏi: Nếu mạng bị mất lúc trẻ bấm xin giờ, thông điệp có bị nuốt mất không?
> **💡 Trả lời:** Dạ thưa Thầy không bị mất. Khi gửi thất bại do mất mạng, Agent lưu yêu cầu vào hàng đợi ngoại tuyến `offline_requests` trong SQLite cục bộ của máy con. Đồng thời giao diện hiện thông báo: *"Đang mất kết nối tới máy chủ phụ huynh, yêu cầu sẽ tự động gửi ngay khi có mạng trở lại."*

#### ❓ Câu 557: Thầy hỏi: Tại sao thiết kế này được gọi là "Công nghệ đồng hành giáo dục" thay vì "Phần mềm rình mò"?
> **💡 Trả lời:** Dạ vì phần mềm rình mò (Spyware) luôn giấu mình, hoạt động lén lút trong bóng tối và biến trẻ thành đối tượng bị kiểm soát thụ động. Ngược lại, OGK hoạt động công khai, đối thoại minh bạch, cung cấp công cụ tự quản trị cho trẻ và tạo cơ hội để cha mẹ và con cái thảo luận, thương lượng về thời gian sử dụng công nghệ một cách văn minh.

#### ❓ Câu 558: Thầy hỏi: Trẻ có quyền gửi lời nhắn kèm lý do khi xin thêm giờ không?
> **💡 Trả lời:** Dạ có thưa Thầy, trên hộp thoại có một trường nhập văn bản `Lý do xin thêm giờ (tùy chọn)`. Trẻ có thể nhập lý do như: *"Con đang làm bài tập nhóm chưa xong"*, giúp phụ huynh hiểu rõ ngữ cảnh và dễ dàng đưa ra quyết định duyệt giờ hơn.

#### ❓ Câu 559: Thầy hỏi: Module giao diện người dùng máy con nằm ở file nào trong mã nguồn?
> **💡 Trả lời:** Dạ thưa Thầy, nằm tại tệp `agent/tray_icon.py` (khoảng 180 dòng code), kết hợp với tệp điều phối `agent/agent_manager.py`.

#### ❓ Câu 560: Thầy hỏi: Kịch bản kiểm thử tích hợp nào mô phỏng trọn vẹn luồng gửi yêu cầu -> phụ huynh duyệt -> cộng giờ?
> **💡 Trả lời:** Dạ thưa Thầy, đó là bài test `test_kid_time_request_approval_flow` trong tệp `tests/test_phase3_network.py`. Bài test tạo thiết bị con, gửi yêu cầu xin 30 phút, kiểm tra bản ghi PENDING trong CSDL, mô phỏng phụ huynh gọi API duyệt APPROVED, và kiểm tra thông điệp đẩy qua WebSocket tới Client. Bài test đạt kết quả PASSED.

---

# SLIDE 29: TỔNG KẾT NGHIỆM THU VERSION 3 (v0.3): NETWORK & PROCESS FILTERING (CÂU 561 - 580)

#### ❓ Câu 561: Thầy hỏi: Tóm tắt 3 kết quả kỹ thuật đột phá nhất của Version 0.3 là gì?
> **💡 Trả lời:** Dạ thưa Thầy, 3 đột phá lớn nhất là:
> 1. **DNS Sinkhole Proxy Socket UDP 53:** Lọc web đen trả về `0.0.0.0` trong 0.83 ms, cưỡng chế SafeSearch Google/Bing, và vô hiệu hóa DoH qua Canary NXDOMAIN.
> 2. **Kiểm soát ứng dụng bằng mã băm SHA-256:** Triệt tiêu chiêu trò đổi tên file game, kết hợp thuật toán `mtime` cache giúp CPU tiêu thụ ở mức lý tưởng 0.0%.
> 3. **Giao diện đồng hành 2 chiều:** Hoàn thiện khay hệ thống, tính năng xin giờ và báo chặn nhầm, đạt 38/38 bài test tự động PASSED 100%.

#### ❓ Câu 562: Thầy hỏi: Tổng số task hoàn thành trong Tuần 3 là bao nhiêu task? Phân bổ vào những module nào?
> **💡 Trả lời:** Dạ thưa Thầy, tổng cộng **45 tasks chi tiết** đã hoàn thành 100%:
> - 18 tasks cho tầng mạng DNS Proxy (`agent/dns_proxy.py`).
> - 12 tasks cho module giám sát ứng dụng SHA-256 (`agent/app_monitor.py`).
> - 8 tasks cho giao diện khay hệ thống và tương tác 2 chiều (`agent/tray_icon.py`).
> - 7 tasks cho các API REST quản lý danh mục quy tắc trên Server (`server/routes/rules.py`).

#### ❓ Câu 563: Thầy hỏi: Bộ test suite của v0.3 đạt bao nhiêu test? Tỷ lệ Pass là bao nhiêu %?
> **💡 Trả lời:** Dạ thưa Thầy, đạt **38/38 test cases tự động PASSED (tỷ lệ đạt 100%)**: Gồm 15 test của Tuần 1, 9 test của Tuần 2, và 14 test mới được viết trong Tuần 3.

#### ❓ Câu 564: Thầy hỏi: File báo cáo nghiệm thu kỹ thuật của Tuần 3 tên là gì và nằm ở đâu trong repo?
> **💡 Trả lời:** Dạ thưa Thầy, tệp tài liệu tên là:  
> `docs/VERIFY_WEEK3.md` (kèm báo cáo nhiệm vụ tại `.specify/memory/tasks-week3.md`).

#### ❓ Câu 565: Thầy hỏi: Có phát sinh bug nghiêm trọng nào trong quá trình phát triển Tuần 3 không và đã fix ra sao?
> **💡 Trả lời:** Dạ có thưa Thầy, có 2 sự cố kỹ thuật lớn:
> 1. **Sự cố nghẽn I/O đĩa:** Ban đầu Agent quét băm SHA-256 mọi file khiến ổ cứng nhảy lên 100%. Nhóm đã sửa bằng cách thiết kế bộ nhớ đệm `mtime` cache, giảm thời gian kiểm tra từ 450 ms xuống 0.02 ms.
> 2. **Sự cố rớt gói tin DNS EDNS0:** Khi truy vấn các trang web có bản tin DNS lớn hơn 512 bytes thì socket bị lỗi Buffer Overflow. Nhóm đã nâng kích thước vùng đệm đọc `recvfrom` lên 4096 bytes và hỗ trợ cờ cắt cụt `TC`.

#### ❓ Câu 566: Thầy hỏi: Sự cố phân mảnh gói tin UDP DNS trong quá trình test đã được nhóm xử lý như thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, phân mảnh IP (IP Fragmentation) xảy ra khi gói tin UDP vượt quá chỉ số MTU của card mạng (thường là 1500 bytes). Đối với các gói tin DNS phản hồi quá lớn từ Upstream, Proxy kiểm tra kích thước: Nếu vượt ngưỡng an toàn của UDP, Proxy bật cờ `TC = 1` (Truncated) trong tiêu đề gói tin phản hồi để yêu cầu trình duyệt gửi lại truy vấn qua giao thức TCP cổng 53, đảm bảo không bị mất mát dữ liệu.

#### ❓ Câu 567: Thầy hỏi: Tốc độ xử lý của DNS Proxy khi chạy đồng thời 50 truy vấn cùng lúc đạt bao nhiêu request/giây?
> **💡 Trả lời:** Dạ thưa Thầy, trong bài test hiệu năng tải đồng thời, DNS Proxy xử lý đạt thông lượng hơn **1.200 requests/giây (RPS)** nhờ kiến trúc non-blocking của `asyncio.DatagramProtocol`. Nhu cầu thực tế của một máy tính gia đình chỉ khoảng 10 đến 30 requests/giây, do đó hệ thống thừa tải hơn 40 lần.

#### ❓ Câu 568: Thầy hỏi: Tại sao v0.3 chưa thể đóng gói thành sản phẩm thương mại hoàn chỉnh?
> **💡 Trả lời:** Dạ thưa Thầy, vì ở bản v0.3 hệ thống mới hoàn thiện các chức năng nghiệp vụ (Functional Features). Hệ thống vẫn còn thiếu các rào chắn phi chức năng (Non-Functional Requirements) trọng yếu: Chưa có mã hóa đối xứng AES-256-GCM bảo vệ gói tin đệm, chưa có kiểm tra quyền sở hữu chống IDOR, chưa có cơ chế khóa tài khoản brute-force, chưa có dịch vụ tự phục hồi DNS Watchdog khi card mạng bị sửa đổi, và chưa có chu kỳ xóa dữ liệu theo Nghị định 13. Toàn bộ các thiếu sót này được hoàn thiện trong Tuần 4.

#### ❓ Câu 569: Thầy hỏi: So sánh v0.3 với v0.2: Điểm số hoàn thiện hệ thống tăng từ bao nhiêu lên bao nhiêu %?
> **💡 Trả lời:** Dạ thưa Thầy, theo bảng tiêu chuẩn đánh giá của đề tài: Bản v0.2 đạt khoảng 50% khối lượng đề tài (hoàn thiện bộ khung thời gian). Bản v0.3 hoàn thành thêm toàn bộ tầng lọc mạng và kiểm soát ứng dụng, nâng mức độ hoàn thiện đồ án lên **80% khối lượng kỹ thuật**.

#### ❓ Câu 570: Thầy hỏi: Dữ liệu cấu hình Rule của Tuần 3 được đồng bộ xuống Agent lưu ở đâu trên máy con?
> **💡 Trả lời:** Dạ được lưu tại tệp JSON cục bộ:  
> `agent/data/local_rules.json`  
> Tệp này được bảo vệ bằng quyền ghi hệ thống (ACL chỉ cho phép SYSTEM ghi) và có chữ ký HMAC-SHA256 đi kèm để phát hiện việc trẻ sửa trộm tệp.

#### ❓ Câu 571: Thầy hỏi: Nếu phụ huynh thêm 500 domain cấm mới, thời gian đồng bộ xuống Agent mất bao lâu?
> **💡 Trả lời:** Dạ thưa Thầy chỉ mất **khoảng 15 đến 25 mili-giây** qua WebSocket. Gói tin JSON chứa mảng 500 domain có dung lượng khoảng 12 KB, được nén và đẩy tức thì qua kết nối socket sẵn có, Agent tải vào cấu trúc `set` trong RAM chỉ trong 0.5 ms.

#### ❓ Câu 572: Thầy hỏi: Tính toàn vẹn của danh sách domain cấm lưu ở Agent được bảo vệ bằng chữ ký số nào?
> **💡 Trả lời:** Dạ thưa Thầy, được bảo vệ bằng chữ ký xác thực thông điệp **HMAC-SHA256**. Mỗi khi Server gửi danh sách quy tắc, Server đính kèm một trường `signature = HMAC_SHA256(data, secret_key)`. Khi lưu xuống đĩa hoặc nạp lại khi khởi động, Agent tính lại HMAC: Nếu trẻ mở file ra xóa domain cấm thì chữ ký sẽ bị sai lệch, Agent lập tức từ chối tệp bị sửa đổi và tải lại bản gốc từ Server.

#### ❓ Câu 573: Thầy hỏi: Kiểm tra bằng chứng: Có ảnh chụp màn hình hoặc log thực nghiệm bắt gói tin DNS bị chặn không?
> **💡 Trả lời:** Dạ có đầy đủ thưa Thầy. Toàn bộ hình ảnh chụp màn hình Wireshark bắt gói tin phản hồi `0.0.0.0`, hình ảnh trình duyệt hiện lỗi `ERR_ADDRESS_INVALID`, và tệp log ghi nhận `[BLOCK] tiktok.com -> 0.0.0.0` đều được đính kèm chi tiết trong Phụ lục Báo cáo Chuyên sâu M1 và trong tài liệu `docs/BAO_CAO_HOAN_THIEN_TUAN_3_4.md`.

#### ❓ Câu 574: Thầy hỏi: Trẻ có thể dùng trình quản lý file gỡ file cấu hình `local_rules.json` của Agent không?
> **💡 Trả lời:** Dạ thưa Thầy không thể gỡ được. Vì thư mục cài đặt của Agent được phân quyền Windows ACL: Chỉ có tài khoản hệ thống `NT AUTHORITY\SYSTEM` và nhóm `Administrators` mới có quyền xóa. Tài khoản người dùng của trẻ là `Standard User` khi cố tình xóa file sẽ nhận được thông báo lỗi từ chối truy cập từ Windows.

#### ❓ Câu 575: Thầy hỏi: Kiến trúc v0.3 đã hỗ trợ tính năng gia hạn giờ linh hoạt (Bonus Time) chưa?
> **💡 Trả lời:** Dạ đã hỗ trợ đầy đủ thưa Thầy. Khi phụ huynh duyệt yêu cầu xin giờ, hoặc trực tiếp bấm nút "Thưởng thêm 30 phút" trên Dashboard, hệ thống kích hoạt cơ chế Bonus Time cộng trực tiếp vào giới hạn ngày mà không làm thay đổi lịch tuần cố định.

#### ❓ Câu 576: Thầy hỏi: Khi chạy v0.3 trên máy tính thực tế của trẻ, người dùng có cảm thấy bị chậm mạng không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn không cảm thấy chậm mạng!**  
> Vì độ trễ phân giải DNS nội bộ của OGK đo được chỉ là 0.83 ms. Con người chỉ có thể cảm nhận được độ trễ khi vượt quá 100 ms. Do đó việc duyệt web, xem video học tập của trẻ hoàn toàn mượt mà như bình thường.

#### ❓ Câu 577: Thầy hỏi: Các thư viện Python sử dụng trong v0.3 có phụ thuộc vào bản build C++ phức tạp không?
> **💡 Trả lời:** Dạ thưa Thầy không. Nhóm chỉ sử dụng các thư viện chuẩn thuần Python (Pure Python) hoặc các thư viện phổ biến có sẵn bản phân phối Pre-compiled Wheel chuẩn trên PyPI (`pystray`, `Pillow`, `dnslib`, `psutil`), đảm bảo việc triển khai và đóng gói không bị lỗi thiếu trình biên dịch Visual C++.

#### ❓ Câu 578: Thầy hỏi: Lệnh chạy toàn bộ test suite của v0.3 trong terminal là gì?
> **💡 Trả lời:** Dạ thưa Thầy, lệnh chạy là:  
> `pytest tests/test_phase1.py tests/test_phase2.py tests/test_phase3_network.py -v`

#### ❓ Câu 579: Thầy hỏi: Mối liên kết kỹ thuật giữa v0.3 và v0.4 chuẩn bị báo cáo tiếp theo là gì?
> **💡 Trả lời:** Dạ thưa Thầy, v0.3 là "thân thể và cơ bắp" (xây dựng các năng lực can thiệp mạng và tiến trình), còn v0.4 là "bộ giáp bảo vệ và thước đo chuẩn mực" (bọc thêm lớp giáp bảo mật F5, khóa brute-force, AES-256-GCM, tự phục hồi M5 và đo lường số liệu M4 để chứng minh tính hoàn thiện xuất sắc của đồ án).

#### ❓ Câu 580: Thầy hỏi: Nếu Hội đồng yêu cầu chạy test suite v0.3 trực tiếp tại chỗ, mất bao nhiêu giây để có kết quả?
> **💡 Trả lời:** Dạ thưa Thầy chỉ mất **khoảng 4 đến 5 giây**. Toàn bộ 38 bài test sẽ chạy lướt qua màn hình console với các dòng chữ xanh `PASSED` và tổng kết kết quả hoàn hảo 100%.

---

# SLIDE 30: TỔNG QUAN VERSION 0.4: GIA CỐ BẢO MẬT CẤP CAO F5, PHÁP LÝ NĐ 13, M3 & M4 (CÂU 581 - 600)

#### ❓ Câu 581: Thầy hỏi: Mục tiêu trọng tâm của Version 0.4 (Tuần 4) là gì? Khác gì so với 3 tuần trước?
> **💡 Trả lời:** Dạ thưa Thầy, mục tiêu trọng tâm của Version 0.4 là **"Gia cố bảo mật, Đo lường thực nghiệm, Tuân thủ pháp lý và Đóng gói phát hành"** (Hardening, Benchmarking, Legal Compliance & Final Release). Khác với 3 tuần trước tập trung phát triển tính năng mới, Tuần 4 tập trung biến một dự án phần mềm của sinh viên thành một sản phẩm có tính kỷ luật công nghệ cao, an toàn tuyệt đối trước các cuộc tấn công mạng, đạt chuẩn NIST/OWASP và sẵn sàng chuyển giao thực tế.

#### ❓ Câu 582: Thầy hỏi: Tại sao nhóm gọi Version 0.4 là "Phiên bản bảo vệ tốt nghiệp hoàn thiện" (Final Graduation Release)?
> **💡 Trả lời:** Dạ thưa Thầy, vì tại phiên bản này toàn bộ các cam kết trong đề cương tốt nghiệp đã được hoàn thành 100%, không còn bất kỳ tính năng dở dang nào: Bộ test suite đạt tối đa 61/61 test cases, 5/5 tiêu chuẩn Definition of Done đã đạt trọn vẹn, toàn bộ 6 báo cáo mạng chuyên sâu M1-M6 đã hoàn thiện và tệp tài liệu luận văn đã được đồng bộ chuẩn xác.

#### ❓ Câu 583: Thầy hỏi: Gia cố bảo mật cấp cao (Security Hardening) trong Version 0.4 gồm những nội dung kỹ thuật cốt lõi nào?
> **💡 Trả lời:** Dạ gồm 5 nội dung lớn: (1) Chính sách mật khẩu NIST $\ge 10$ ký tự băm Argon2id; (2) Cơ chế khóa tài khoản lũy tiến 15 phút chống Brute-force; (3) Bộ đệm IP Rate Limiting chống DoS; (4) Triệt tiêu 100% lỗ hổng IDOR trên mọi API qua kiểm tra quyền sở hữu CSDL; (5) Mã hóa đối xứng xác thực AEAD AES-256-GCM với Nonce 12B và Auth Tag 16B.

#### ❓ Câu 584: Thầy hỏi: Tại sao một đồ án tốt nghiệp của sinh viên lại cần quan tâm đến các tiêu chuẩn quốc tế như NIST và OWASP?
> **💡 Trả lời:** Dạ thưa Thầy, vì trong kỷ nguyên an ninh mạng hiện đại, một phần mềm quản lý gia đình nếu không có bảo mật chuẩn mực sẽ vô tình trở thành một "cánh cửa hậu" (Backdoor) nguy hiểm: Kẻ lạ có thể tấn công vào phần mềm để theo dõi lịch trình sinh hoạt của đứa trẻ hoặc xâm nhập vào mạng nội bộ của gia đình. Áp dụng chuẩn NIST SP 800-63B và OWASP ASVS v4 giúp hệ thống đạt chuẩn an toàn thông tin tương đương các phần mềm doanh nghiệp chuyên nghiệp.

#### ❓ Câu 585: Thầy hỏi: Chỉ số 61/61 automated tests hoàn thành trong tuần này gồm những nhóm test mới nào?
> **💡 Trả lời:** Dạ gồm 23 bài test mới trong `tests/test_phase4_security.py`:
> - 6 test cho module an ninh F5 (mật khẩu yếu, brute-force 5 lần khóa 15p, rate limiting 60 req/p).
> - 5 test cho kiểm soát truy cập chống IDOR trên các API Devices, Rules, Alerts.
> - 4 test cho mã hóa AES-256-GCM AEAD (mã hóa chuẩn, giải mã, chống lật bit InvalidTag).
> - 4 test cho tuân thủ Nghị định 13 (chu kỳ dọn dẹp 90 ngày, xóa dữ liệu 2 chiều Right to Erasure).
> - 4 test cho kịch bản chịu lỗi mạng M5 và tự phục hồi DNS Watchdog.

#### ❓ Câu 586: Thầy hỏi: Mô hình đo lường hiệu năng M4 được thực hiện theo phương pháp luận nào?
> **💡 Trả lời:** Dạ thưa Thầy, được thực hiện theo phương pháp đo kiểm thực nghiệm thống kê (Empirical Statistical Benchmarking): Sử dụng các công cụ đo phần cứng ở tầng nhân (`psutil`, `perf_counter_ns`), lấy mẫu lặp lại độc lập 30 lần ($N=30$) trên cùng một cấu hình Windows 11 thực tế, tính toán giá trị trung bình cộng ($\mu$) và loại bỏ phương sai ngoại lai để cho ra số liệu khách quan nhất.

#### ❓ Câu 587: Thầy hỏi: Khả năng chịu lỗi M5 giải quyết những rủi ro vận hành thực tế nào?
> **💡 Trả lời:** Dạ giải quyết 3 rủi ro mạng phổ biến nhất trong gia đình: (1) Mất mạng Internet đột ngột $ightarrow$ Lưu đệm ngoại tuyến SQLite WAL cục bộ không làm mất dữ liệu; (2) Máy chủ bị sập hoặc phụ huynh tắt máy $ightarrow$ Agent kết nối lại theo thuật toán lùi hàm mũ Exponential Backoff tránh bão kết nối; (3) Trẻ tự ý đổi DNS card mạng $ightarrow$ DNS Watchdog tự động phục hồi về 127.0.0.1 sau 20 giây.

#### ❓ Câu 588: Thầy hỏi: Khắc chế 7 kỹ thuật vượt rào M3 có phải là điểm nhấn của đồ án an ninh mạng không?
> **💡 Trả lời:** Dạ thưa Thầy, đúng vậy ạ! Đây là đóng góp chuyên ngành Mạng & An toàn Hệ thống nổi bật nhất: Nhóm đã biến các lý thuyết về tấn công và phòng thủ thành một ma trận đối kháng thực tế, vô hiệu hóa toàn bộ 7 chiêu trò lách luật mà học sinh thường dùng (đổi tên file, sửa DNS, bật DoH, dùng VPN, tua giờ, tắt task, duyệt web ẩn danh).

#### ❓ Câu 589: Thầy hỏi: Hồ sơ pháp lý Nghị định 13/2023 được lập thành tài liệu độc lập hay tích hợp trong code?
> **💡 Trả lời:** Dạ thưa Thầy, kết hợp cả hai: Nhóm lập riêng bản báo cáo pháp lý **Báo cáo Chuyên sâu M6 (`docs/BAO_CAO_HOAN_THIEN_TUAN_3_4.md`)**, đồng thời ánh xạ trực tiếp thành các dòng code thực thi trong `server/routes/retention.py` và quy trình xóa CASCADE trong mô hình cơ sở dữ liệu.

#### ❓ Câu 590: Thầy hỏi: Quy trình Definition of Done (DoD) của đồ án có bao nhiêu bậc? Đã đạt được bậc nào?
> **💡 Trả lời:** Dạ thưa Thầy, có trọn vẹn **5 bậc tiêu chuẩn (DoD 1 đến DoD 5)**, và nhóm tự hào khẳng định đã đạt trọn vẹn **5/5 bậc tiêu chuẩn** ở cấp độ cao nhất.

#### ❓ Câu 591: Thầy hỏi: Toàn bộ mã nguồn đồ án hiện tại có bao nhiêu dòng code (LOC)? Đo bằng công cụ gì?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm sử dụng công cụ `cloc` (Count Lines of Code) để thống kê: Toàn bộ dự án có khoảng **4.850 dòng mã nguồn Python thực thi**, cùng với hơn 2.400 dòng mã nguồn kiểm thử tự động, tạo nên một hệ thống hoàn chỉnh, tinh gọn và không có mã nguồn thừa thãi.

#### ❓ Câu 592: Thầy hỏi: Có bao nhiêu tệp mã nguồn Python trong toàn bộ dự án?
> **💡 Trả lời:** Dạ gồm khoảng **28 tệp mã nguồn Python**: Được phân chia khoa học thành các thư mục `server/` (12 tệp), `agent/` (8 tệp), `tests/` (5 tệp) và `scripts/` (3 tệp công cụ đo đạc).

#### ❓ Câu 593: Thầy hỏi: Kiến trúc hệ thống ở v0.4 đã đạt mức độ sẵn sàng triển khai thực tế (Production-Ready) chưa?
> **💡 Trả lời:** Dạ thưa Thầy, đối với mô hình mạng gia đình quy mô vừa và nhỏ (từ 1 đến 10 thiết bị máy con), hệ thống đã đạt mức **Production-Ready 100%**: Có thể cài đặt trên máy tính phụ huynh và máy tính con để sử dụng thực tế hàng ngày mà không gặp bất kỳ trở ngại kỹ thuật nào.

#### ❓ Câu 594: Thầy hỏi: Nếu chuyển giao mã nguồn này cho một doanh nghiệp thương mại thì cần thêm những bước gì?
> **💡 Trả lời:** Dạ thưa Thầy, chỉ cần bổ sung 2 thành phần phụ trợ: (1) Đăng ký chứng chỉ số Microsoft Code Signing Certificate để gói cài đặt `.exe` không bị Windows SmartScreen cảnh báo phần mềm lạ; (2) Nâng cấp cơ sở dữ liệu Server từ SQLite sang PostgreSQL và đóng gói Docker Container để phục vụ quy mô hàng trăm ngàn người dùng trên hạ tầng điện toán đám mây.

#### ❓ Câu 595: Thầy hỏi: Vai trò của sinh viên 1 và sinh viên 2 trong việc hoàn thành Tuần 4?
> **💡 Trả lời:** Dạ thưa Thầy: Sinh viên 1 phụ trách toàn bộ khối Server Hardening, thuật toán AES-256-GCM, rà soát lỗ hổng IDOR trên API, kịch bản đo đạc M4 và tài liệu báo cáo tốt nghiệp. Sinh viên 2 phụ trách khối Agent Resilience, hoàn thiện DNS Watchdog bằng `netsh`, kịch bản chịu lỗi M5 và đóng gói bộ cài đặt Agent cho Windows.

#### ❓ Câu 596: Thầy hỏi: Quá trình kiểm thử tải (Load Testing) và đo Benchmark tốn bao nhiêu thời gian máy tính?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm đã cho chạy kịch bản đo đạc tự động liên tục trong vòng **4 giờ đồng hồ** với hơn 10.000 truy vấn DNS và 5.000 bản tin WebSocket mô phỏng các điều kiện tải khác nhau để thu thập đủ 30 tập mẫu đo thống kê tiêu chuẩn cho Báo cáo M4.

#### ❓ Câu 597: Thầy hỏi: Có xung đột logic nào giữa tính năng bảo mật F5 và tính năng đệm ngoại tuyến M5 không?
> **💡 Trả lời:** Dạ thưa Thầy không hề xung đột, mà bổ trợ cho nhau: Khi Agent hoạt động ngoại tuyến (M5), dữ liệu nhật ký lưu đệm trong SQLite cục bộ được mã hóa bằng AES-256-GCM (F5). Khi có mạng trở lại, dữ liệu đẩy lên Server được gửi kèm chữ ký HMAC để bảo đảm tính toàn vẹn. Hai tính năng phối hợp tạo nên một hệ thống vừa bền bỉ vừa an toàn tuyệt đối.

#### ❓ Câu 598: Thầy hỏi: Tại sao nhóm chọn đóng gói Agent bằng PyInstaller thay vì cài Python trực tiếp trên máy con?
> **💡 Trả lời:** Dạ vì tính thực tế (Usability): Máy tính của trẻ em không có sẵn môi trường lập trình Python. Nếu yêu cầu phụ huynh phải cài Python, thiết lập biến môi trường PATH và chạy lệnh `pip install` thì phần mềm sẽ không thể phổ cập được. Đóng gói bằng **PyInstaller** tạo ra một tệp nhị phân `.exe` độc lập duy nhất (Stand-alone Executable), phụ huynh chỉ cần chạy một cú click chuột là phần mềm tự động cài đặt và khởi chạy.

#### ❓ Câu 599: Thầy hỏi: Bản phát hành v0.4 có file thực thi nhị phân `.exe` độc lập không?
> **💡 Trả lời:** Dạ có thưa Thầy. Tệp cài đặt `OpenGuardianAgent_v0.4.exe` đã được đóng gói hoàn tất trong thư mục `dist/`, dung lượng khoảng 28 MB, tích hợp sẵn toàn bộ trình thông dịch Python nhúng và các thư viện cần thiết.

#### ❓ Câu 600: Thầy hỏi: Câu nói ngắn gọn nhất để khái quát sự trưởng thành của hệ thống ở v0.4 là gì?
> **💡 Trả lời:** Dạ thưa Thầy: *"OGK Version 0.4 đã chuyển mình ngoạn mục từ một đồ án môn học đơn thuần thành một giải pháp an ninh mạng gia đình toàn diện, đạt độ hoàn thiện cao nhất về cả kỹ thuật mạng Socket, an toàn mật mã học, độ bền bỉ thực nghiệm và chuẩn mực đạo đức pháp lý bảo vệ trẻ em."*

# SLIDE 31: BẢO MẬT CẤP CAO F5: NIST SP 800-63B, KHÓA BRUTE-FORCE 15 PHÚT, IP RATE LIMITING (CÂU 601 - 620)

#### ❓ Câu 601: Thầy chỉ vào slide hỏi: Tiêu chuẩn NIST SP 800-63B quy định những gì về chính sách mật khẩu hiện đại?
> **💡 Trả lời:** Dạ thưa Thầy, NIST SP 800-63B (Digital Identity Guidelines) của Viện Tiêu chuẩn và Kỹ thuật Quốc gia Hoa Kỳ đưa ra 3 thay đổi mang tính cách mạng: (1) Bãi bỏ quy tắc bắt buộc đổi mật khẩu định kỳ vì người dùng thường chỉ đổi một ký tự cuối đối phó; (2) Loại bỏ các yêu cầu rườm rà như bắt buộc phải có chữ hoa, số và ký tự đặc biệt vì chúng không làm tăng entropy thực tế; (3) Khuyến nghị tập trung vào **độ dài tối thiểu ($\ge 8-10$ ký tự)**, kiểm tra mật khẩu yếu trong từ điển phổ biến, và kiểm soát số lần đăng nhập sai.

#### ❓ Câu 602: Thầy hỏi: Tại sao NIST khuyến nghị độ dài tối thiểu 10 ký tự thay vì bắt buộc ký tự đặc biệt phức tạp?
> **💡 Trả lời:** Dạ thưa Thầy, vì theo lý thuyết thông tin mật mã (Entropy theory): Không gian khóa của một mật khẩu dài 10 ký tự chữ cái ngẫu nhiên ($26^{10} pprox 1.4 	imes 10^{14}$) lớn hơn rất nhiều so với một mật khẩu ngắn 6 ký tự dù có đủ ký tự đặc biệt ($94^6 pprox 6.8 	imes 10^{11}$). Mật khẩu càng dài thì thời gian vét cạn (Brute-force) càng tăng theo hàm số mũ, đồng thời người dùng dễ nhớ các cụm từ (Passphrase) có nghĩa hơn.

#### ❓ Câu 603: Thầy hỏi: Hàm kiểm tra độ mạnh mật khẩu trong `server/security.py` sử dụng thuật toán hay biểu thức chính quy nào?
> **💡 Trả lời:** Dạ thưa Thầy, hàm `validate_password_strength(password: str)` kiểm tra:
> 1. Độ dài chuỗi `len(password) >= 10`.
> 2. Đối chiếu với danh sách đen 10.000 mật khẩu phổ biến nhất thế giới (`common_passwords.txt` như `1234567890`, `password123`, `admin12345`).
> 3. Kiểm tra tính đa dạng ký tự tối thiểu: Bắt buộc có ít nhất 1 chữ cái và 1 chữ số. Nếu không thỏa mãn, ném ra ngoại lệ `HTTPException(400, "Mật khẩu quá yếu hoặc quá ngắn")`.

#### ❓ Câu 604: Thầy hỏi: Tại sao NIST lại bãi bỏ quy tắc bắt buộc đổi mật khẩu định kỳ 90 ngày một lần?
> **💡 Trả lời:** Dạ thưa Thầy, vì các nghiên cứu hành vi thực nghiệm của NIST chứng minh: Khi bị ép đổi mật khẩu 90 ngày/lần, người dùng có xu hướng chọn mật khẩu mới rất dễ đoán (ví dụ từ `Spring2023!` sang `Summer2023!`), hoặc viết mật khẩu ra giấy dán dưới bàn phím. Việc duy trì một mật khẩu dài, mạnh kết hợp thuật toán băm Argon2id và khóa brute-force an toàn hơn gấp nhiều lần.

#### ❓ Câu 605: Thầy hỏi: Cơ chế khóa tài khoản (Account Lockout) của OGK hoạt động ra sao khi bị tấn công dò mật khẩu?
> **💡 Trả lời:** Dạ thưa Thầy, cơ chế hoạt động lũy tiến như sau:
> 1. Bảng `parents` trong CSDL lưu 2 trường: `failed_login_attempts (int)` và `locked_until (datetime)`.
> 2. Mỗi lần đăng nhập sai, Server tăng biến đếm `failed_login_attempts += 1`.
> 3. Nếu số lần sai đạt ngưỡng **5 lần liên tiếp**, Server lập tức tính toán:  
>    $$	ext{locked\_until} = 	ext{datetime.utcnow}() + 	ext{timedelta(minutes=15)}$$
> 4. Trong suốt 15 phút bị khóa, mọi yêu cầu đăng nhập từ tài khoản này đều bị từ chối với mã lỗi `403 Forbidden` kèm thông báo thời gian còn lại.
> 5. Nếu đăng nhập thành công trước ngưỡng 5 lần, biến đếm tự động reset về 0.

#### ❓ Câu 606: Thầy hỏi: Tại sao lại chọn ngưỡng 5 lần sai và thời gian khóa là 15 phút?
> **💡 Trả lời:** Dạ thưa Thầy, đây là điểm cân bằng hoàn hảo giữa tính An toàn (Security) và Trải nghiệm người dùng (Usability) theo chuẩn OWASP: 5 lần là đủ để phụ huynh gõ nhầm sửa sai, nhưng đủ ngắn để chặn đứng các công cụ dò mật khẩu tự động (Dictionary Attack). Thời gian khóa 15 phút làm giảm tốc độ dò từ hàng triệu mật khẩu/giây xuống chỉ còn tối đa 20 mật khẩu/giờ, biến cuộc tấn công vét cạn thành bất khả thi.

#### ❓ Câu 607: Thầy hỏi: Thời gian khóa tài khoản được tính theo giờ Local hay giờ chuẩn UTC? Vì sao?
> **💡 Trả lời:** Dạ thưa Thầy, bắt buộc phải tính theo **giờ chuẩn quốc tế UTC (`datetime.utcnow()`)**. Nếu dùng giờ Local của máy tính, hệ thống sẽ gặp lỗi nghiêm trọng khi chuyển đổi múi giờ (Timezone offset), hoặc kẻ tấn công trên máy chủ có thể chỉnh lùi giờ hệ điều hành để vượt qua lệnh khóa tài khoản.

#### ❓ Câu 608: Thầy hỏi: Kẻ tấn công có thể lợi dụng tính năng Lockout này để tấn công DoS khóa tài khoản phụ huynh không?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm đã dự liệu nguy cơ này: Để tránh kẻ xấu liên tục gửi 5 request sai nhằm khóa tài khoản phụ huynh (Account Denial of Service), hệ thống kết hợp thêm tầng **IP Rate Limiting**. Kẻ tấn công gửi dồn dập sẽ bị chặn ngay ở tầng IP trước khi chạm tới hàm xử lý tài khoản, đồng thời Server cung cấp cơ chế mở khóa khẩn cấp qua Email xác thực của phụ huynh.

#### ❓ Câu 609: Thầy hỏi: Cơ chế IP Rate Limiting trong OGK được thiết lập ở tầng nào của ứng dụng?
> **💡 Trả lời:** Dạ thưa Thầy, được thiết lập ở tầng **Middleware của FastAPI** (`server/middleware/rate_limiter.py`). Middleware này can thiệp vào tất cả các yêu cầu HTTP gửi đến Server ngay trước khi đi vào các Router nghiệp vụ, giúp loại bỏ các truy vấn rác sớm nhất để bảo vệ tài nguyên tính toán của CPU và CSDL.

#### ❓ Câu 610: Thầy hỏi: Ngưỡng giới hạn 60 requests/phút được tính theo từng IP hay tính chung cho toàn bộ mạng?
> **💡 Trả lời:** Dạ được tính **độc lập theo từng địa chỉ IP Client (`request.client.host`)**. Mỗi IP có một bộ đếm riêng trong RAM. Điều này đảm bảo nếu một máy tính lạ trong mạng bị nhiễm mã độc gửi spam thì chỉ có IP đó bị chặn, các thiết bị máy tính khác trong gia đình vẫn truy cập Dashboard bình thường.

#### ❓ Câu 611: Thầy hỏi: Khi bị chặn do vượt Rate Limit, Server trả về mã lỗi HTTP trạng thái bao nhiêu?
> **💡 Trả lời:** Dạ thưa Thầy, trả về mã lỗi chuẩn quốc tế:  
> $$	extbf{HTTP 429 Too Many Requests}$$  
> Kèm theo tiêu đề Header `Retry-After: 60` thông báo cho Client biết số giây cần phải chờ trước khi được gửi yêu cầu tiếp theo.

#### ❓ Câu 612: Thầy hỏi: Cấu trúc dữ liệu nào trong RAM được dùng để đếm số request theo cửa sổ trượt (Sliding Window)?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm sử dụng cấu trúc **Hàng đợi hai đầu `collections.deque`** lưu trữ các mốc thời gian (Timestamps) của từng request trong vòng 60 giây gần nhất:  
> $$	ext{ip\_records}[ip] = 	ext{deque}([t_1, t_2, \dots, t_n])$$  
> Khi có request mới: Thuật toán loại bỏ các timestamp cũ hơn $T_{	ext{now}} - 60$, sau đó kiểm tra `len(deque) < 60`. Thao tác thêm và bớt ở hai đầu Deque đạt độ phức tạp tối ưu tuyệt đối $O(1)$.

#### ❓ Câu 613: Thầy hỏi: Bộ nhớ đệm Rate Limiter có bị tràn RAM nếu hàng ngàn IP rác cùng gửi request không?
> **💡 Trả lời:** Dạ thưa Thầy không bị tràn. Nhóm thiết lập một hàm dọn dẹp định kỳ (Periodic Cleanup): Cứ mỗi 10 phút, hệ thống tự động quét từ điển `ip_records` và xóa bỏ toàn bộ các khóa IP không còn hoạt động trong 10 phút qua, giữ cho bộ nhớ RAM của Rate Limiter luôn dưới 2 MB.

#### ❓ Câu 614: Thầy hỏi: Mật khẩu phụ huynh lưu trong CSDL dưới dạng gì? Tại sao không dùng SHA-256 hay MD5 để lưu mật khẩu?
> **💡 Trả lời:** Dạ thưa Thầy, mật khẩu được lưu dưới dạng chuỗi mã băm an toàn **Argon2id**. Tuyệt đối không dùng MD5 hay SHA-256 vì:  
> MD5 và SHA-256 là các hàm băm tốc độ nhanh (Fast Hashes), được thiết kế cho việc kiểm tra tính toàn vẹn dữ liệu. Với phần cứng hiện đại, một dàn máy đào coin GPU có thể thử hàng chục tỷ mã SHA-256 mỗi giây, bẻ khóa mật khẩu trong tích tắc. Lưu mật khẩu bắt buộc phải dùng các hàm băm chậm và ngốn bộ nhớ như Argon2id.

#### ❓ Câu 615: Thầy hỏi: Thuật toán băm Argon2id có những tham số nào (Memory, Time cost, Parallelism)? Thiết lập cụ thể trong OGK?
> **💡 Trả lời:** Dạ thưa Thầy, Argon2id (kết hợp giữa Argon2d chống GPU cracking và Argon2i chống side-channel attack) có 3 tham số cấu hình:
> 1. **Time Cost ($t = 2$ vòng):** Số chu kỳ tính toán lặp lại.
> 2. **Memory Cost ($m = 65,536	ext{ KB} = 64	ext{ MB}$):** Lượng RAM tối thiểu bắt buộc phải cấp phát để tính 1 mã băm.
> 3. **Parallelism ($p = 4$ luồng):** Số luồng xử lý song song.
> Tham số $m = 64	ext{ MB}$ là "vũ khí chí mạng": Dàn máy đào GPU có hàng ngàn lõi nhưng bộ nhớ mỗi lõi rất nhỏ, không thể cấp phát 64MB cho hàng ngàn phép tính đồng thời, triệt tiêu hoàn toàn khả năng dò bẻ mật khẩu bằng GPU.

#### ❓ Câu 616: Thầy hỏi: Tại sao Argon2id lại đánh bại hoàn toàn các dàn máy đào Bitcoin GPU chuyên dụng dò mật khẩu?
> **💡 Trả lời:** Dạ như đã phân tích ở trên, vì cơ chế **Memory-Hardness**: ASIC và GPU có sức mạnh tính toán số học rất cao nhưng băng thông và dung lượng bộ nhớ trên từng nhân xử lý cực kỳ hạn chế. Khi thuật toán bắt buộc phải dùng 64MB bộ nhớ RAM ngẫu nhiên để tính toán, các chip chuyên dụng bị tắc nghẽn bộ nhớ hoàn toàn, hiệu năng sụt giảm hàng triệu lần, biến chi phí tấn công vượt quá giá trị kinh tế.

#### ❓ Câu 617: Thầy hỏi: Thời gian băm một mật khẩu bằng Argon2id trên Server mất khoảng bao nhiêu mili-giây?
> **💡 Trả lời:** Dạ thưa Thầy, trên CPU máy chủ thông thường, thời gian băm một mật khẩu mất khoảng **120 đến 180 mili-giây**. Thời gian này hoàn toàn vô hình đối với phụ huynh khi đăng nhập (chỉ bấm nút 1 lần), nhưng là một "bức tường đá" khổng lồ ngăn chặn kẻ tấn công tự động dò hàng ngàn mật khẩu.

#### ❓ Câu 618: Thầy hỏi: Mọi nỗ lực đăng nhập sai và khóa tài khoản có được ghi vào bảng Audit Log không?
> **💡 Trả lời:** Dạ thưa Thầy có. Mỗi lần đăng nhập sai, Server tự động tạo một bản ghi trong bảng `audit_logs` với hành động `LOGIN_FAILED`, ghi nhận địa chỉ IP của kẻ tình nghi, tên tài khoản mục tiêu và mốc thời gian. Khi tài khoản bị khóa, phát sinh tiếp bản ghi `ACCOUNT_LOCKED_15MIN`, giúp phụ huynh xem lại nhật ký an ninh để biết mình có đang bị tấn công hay không.

#### ❓ Câu 619: Thầy hỏi: File mã nguồn nào cài đặt bộ middleware Rate Limiting và Logic Lockout?
> **💡 Trả lời:** Dạ thưa Thầy:
> - Logic kiểm tra mật khẩu và băm Argon2id nằm ở `server/security.py`.
> - Logic khóa tài khoản Lockout nằm trong route đăng nhập tại `server/routes/auth.py`.
> - Bộ Middleware Rate Limiting nằm tại `server/middleware/rate_limiter.py`.

#### ❓ Câu 620: Thầy hỏi: Bài test `test_auth_brute_force_lockout` trong `test_phase4_security.py` chứng minh điều gì?
> **💡 Trả lời:** Dạ bài test mô phỏng kịch bản tấn công: Gửi liên tiếp 4 request đăng nhập sai (nhận mã 401), gửi tiếp request thứ 5 sai (hệ thống kích hoạt khóa). Sau đó gửi request thứ 6 dù đúng mật khẩu hay sai mật khẩu đều nhận về mã `403 Forbidden` kèm thông báo tài khoản đang bị khóa. Bài test đạt kết quả PASSED 100%.

---

# SLIDE 32: BẢO MẬT CẤP CAO F5: MÃ HÓA AES-256-GCM AEAD & TRIỆT TIÊU HOÀN TOÀN IDOR (CÂU 621 - 640)

#### ❓ Câu 621: Thầy chỉ vào khối AEAD hỏi: AEAD là viết tắt của từ gì? Bản chất của nó khác gì so với mã hóa AES thông thường?
> **💡 Trả lời:** Dạ thưa Thầy, **AEAD** là viết tắt của **Authenticated Encryption with Associated Data (Mã hóa xác thực kèm dữ liệu liên kết)**.  
> Bản chất khác biệt: Mã hóa AES thông thường (như AES-CBC, AES-CTR) chỉ bảo đảm tính **Bảo mật (Confidentiality)** — giấu kín nội dung tin nhắn. Tuy nhiên, nó không bảo đảm tính **Toàn vẹn (Integrity)**: Kẻ tấn công có thể sửa đổi bản mã trên đường truyền mà bên nhận không biết. AEAD sinh ra một mã xác thực đi kèm (Authentication Tag), bảo đảm đồng thời cả tính Bảo mật và tính Toàn vẹn trong một giải thuật duy nhất.

#### ❓ Câu 622: Thầy hỏi: Tại sao lại chọn chế độ Galois/Counter Mode (GCM) thay vì Cipher Block Chaining (CBC)?
> **💡 Trả lời:** Dạ thưa Thầy, có 3 lý do kỹ thuật vượt trội:
> 1. **Chống tấn công thám mã:** AES-CBC dễ bị tấn công Padding Oracle Attack (như lỗi bảo mật POODLE nổi tiếng). AES-GCM không sử dụng Padding nên miễn nhiễm 100% với lỗi này.
> 2. **Chống tấn công lật bit (Bit-Flipping):** GCM có Auth Tag 128-bit khóa chết tính toàn vẹn.
> 3. **Tốc độ xử lý song song:** CBC bắt buộc khối sau phải chờ kết quả khối trước. GCM là chế độ đếm Counter, có thể tận dụng tập lệnh phần cứng AES-NI của CPU hiện đại để mã hóa song song nhiều khối dữ liệu cùng lúc, tốc độ nhanh hơn CBC từ 3 đến 5 lần.

#### ❓ Câu 623: Thầy hỏi: Cấu trúc của gói tin mã hóa AES-256-GCM gồm 3 phần nào và kích thước mỗi phần là bao nhiêu byte?
> **💡 Trả lời:** Dạ thưa Thầy, cấu trúc nhị phân của gói tin mã hóa gồm 3 thành phần liên tiếp:
> 1. **Initialization Vector / Nonce:** Kích thước cố định **12 bytes (96 bits)** đặt ở đầu.
> 2. **Ciphertext (Bản mã):** Độ dài $N$ bytes (bằng đúng độ dài dữ liệu gốc).
> 3. **Authentication Tag (Auth Tag):** Kích thước cố định **16 bytes (128 bits)** đặt ở cuối.

#### ❓ Câu 624: Thầy hỏi: Nonce là gì? Tại sao Nonce trong GCM phải là số ngẫu nhiên 12 bytes dùng một lần?
> **💡 Trả lời:** Dạ thưa Thầy, **Nonce** là viết tắt của **Number used ONCE (Số chỉ dùng một lần)**.  
> Trong chế độ GCM, Nonce 12 bytes (96 bits) được chuẩn hóa bởi NIST SP 800-38D để khởi tạo bộ đếm Galois Counter. Bắt buộc phải là số ngẫu nhiên dùng một lần để đảm bảo: Cùng một nội dung tin nhắn khi mã hóa hai lần khác nhau sẽ sinh ra hai bản mã hoàn toàn khác nhau, ngăn chặn kẻ tấn công phân tích thống kê tần suất xuất hiện của dữ liệu.

#### ❓ Câu 625: Thầy hỏi: Chuyện gì xảy ra nếu lập trình viên tái sử dụng cùng một cặp (Key, Nonce) cho hai gói tin khác nhau?
> **💡 Trả lời:** Dạ thưa Thầy, đây là lỗi thảm họa mật mã học gọi là **"Nonce-Reuse Catastrophe"**:  
> Nếu dùng lại cùng một Nonce với cùng một Khóa bí mật, kẻ tấn công thực hiện phép tính XOR hai bản mã với nhau ($C_1 \oplus C_2 = P_1 \oplus P_2$), triệt tiêu hoàn toàn khóa mã và khôi phục lại dữ liệu gốc. Hơn thế nữa, kẻ tấn công có thể giải phương trình trường nhị phân Galois để tìm ra khóa xác thực băm $H$, từ đó tự ý giả mạo Auth Tag cho các gói tin độc hại! Đó là lý do trong `server/crypto_utils.py`, nhóm luôn gọi `os.urandom(12)` để sinh Nonce độc lập tuyệt đối cho mỗi lần mã hóa.

#### ❓ Câu 626: Thầy hỏi: Authentication Tag (Auth Tag) 16 bytes có vai trò gì trong việc chống tấn công lật bit (Bit-Flipping)?
> **💡 Trả lời:** Dạ thưa Thầy, Auth Tag được tính toán bằng phép nhân đa thức trường hữu hạn GHASH trên toàn bộ bản mã và dữ liệu liên kết.  
> Nếu kẻ tấn công đứng ở giữa đường truyền sửa đổi dù chỉ **duy nhất 1 bit** (từ 0 thành 1) trong bản mã, khi bên nhận giải mã và tính lại Auth Tag, giá trị băm sẽ thay đổi hoàn toàn và không khớp với 16 bytes của Auth Tag đi kèm.

#### ❓ Câu 627: Thầy hỏi: Nếu kẻ tấn công đứng giữa sửa 1 bit duy nhất trong Ciphertext thì hàm giải mã sẽ phản ứng thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, thư viện mật mã học sẽ **ngay lập tức ném ra ngoại lệ `cryptography.exceptions.InvalidTag`**, và hàm giải mã lập tức hủy bỏ toàn bộ dữ liệu, trả về rỗng hoặc báo lỗi mà không xuất ra bất kỳ byte dữ liệu rác nào. Hệ thống phát hiện ngay có hành vi can thiệp đường truyền và ghi log cảnh báo an ninh.

#### ❓ Câu 628: Thầy hỏi: Thư viện mật mã nào của Python được dùng để thực thi AES-256-GCM? Có đạt chuẩn FIPS 140-2 không?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm sử dụng thư viện tiêu chuẩn công nghiệp **`cryptography.hazmat.primitives.ciphers.aead.AESGCM`**. Thư viện này sử dụng lõi C viết trên OpenSSL — một thư viện mã nguồn mở đã được Viện NIST chứng nhận đạt chuẩn an toàn mật mã **FIPS 140-2**.

#### ❓ Câu 629: Thầy hỏi: Khóa đối xứng 256-bit được sinh ra và quản lý như thế nào giữa Server và Agent?
> **💡 Trả lời:** Dạ thưa Thầy, khóa bí mật đối xứng 32 bytes (256 bits) được sinh ngẫu nhiên an toàn bằng `os.urandom(32)`. Khóa này được chia sẻ an toàn trong phiên bắt tay ghép đôi thiết bị ban đầu (Device Pairing Ceremony) thông qua mã PIN 8 ký tự xác thực dùng một lần, sau đó lưu trữ trong vùng bảo vệ cục bộ của Agent và Server.

#### ❓ Câu 630: Thầy hỏi: Lỗ hổng IDOR (Insecure Direct Object Reference) là gì? Lấy một ví dụ thực tế trong hệ thống này?
> **💡 Trả lời:** Dạ thưa Thầy, **IDOR** (Tham chiếu đối tượng trực tiếp không an toàn - thuộc nhóm OWASP Top 1: Broken Access Control) xảy ra khi ứng dụng cho phép người dùng truy cập trực tiếp vào tài nguyên hệ thống thông qua định danh (ID) mà không kiểm tra xem người dùng đó có quyền sở hữu tài nguyên đó hay không.  
> **Ví dụ thực tế:** Phụ huynh A có con dùng máy tính `device_id = 1`. Phụ huynh B có con dùng máy tính `device_id = 2`. Nếu API không phòng vệ IDOR, Phụ huynh A có thể gửi yêu cầu `GET /api/devices/2/activity-logs`. Server thấy token của Phụ huynh A hợp lệ và trả về toàn bộ lịch sử lướt web của bé nhà Phụ huynh B!

#### ❓ Câu 631: Thầy hỏi: Nếu phụ huynh A đã đăng nhập thành công, làm sao ngăn phụ huynh A xem dữ liệu máy con của phụ huynh B?
> **💡 Trả lời:** Dạ thưa Thầy, bằng cơ chế **Kiểm tra quyền sở hữu đối tượng 2 lớp (Ownership Check)**:  
> Khi phụ huynh A yêu cầu truy cập `device_id = 2`, Server trích xuất `parent_id` của phụ huynh A từ Token JWT. Sau đó Server truy vấn CSDL: `device = db.query(Device).filter(Device.id == 2).first()`.  
> Server đối soát điều kiện:  
> $$	extbf{if device.parent\_id != current\_parent.id: raise HTTPException(403)}$$  
> Nhờ đó, phụ huynh A bị chặn đứng hoàn toàn với mã lỗi 403 Forbidden!

#### ❓ Câu 632: Thầy hỏi: Tại sao chỉ kiểm tra tính hợp lệ của Token JWT là KHÔNG ĐỦ để chống IDOR?
> **💡 Trả lời:** Dạ thưa Thầy, đây là sai lầm rất phổ biến của lập trình viên:  
> Token JWT chỉ chứng minh tính **Xác thực danh tính (Authentication)** — tức "Người gửi request đúng là Phụ huynh A đã đăng nhập".  
> Nhưng Token JWT **không tự động chứng minh Quyền hạn (Authorization)** đối với một thiết bị cụ thể — tức "Phụ huynh A có quyền xem máy tính số 2 hay không". Muốn chống IDOR, bắt buộc phải có thêm tầng kiểm tra phân quyền sở hữu trong CSDL.

#### ❓ Câu 633: Thầy hỏi: Mô hình phòng vệ IDOR 2 lớp của OGK hoạt động như thế nào?
> **💡 Trả lời:** Dạ gồm 2 lớp rào chắn:
> - **Lớp 1 (Authentication):** Dependency `get_current_parent` giải mã chữ ký JWT Token, kiểm tra thời hạn hết hạn, trích xuất danh tính `current_parent`.
> - **Lớp 2 (Resource Authorization):** Trực tiếp trong hàm xử lý Route, kiểm tra thuộc tính sở hữu ngoại khóa `device.parent_id == current_parent.id`. Nếu thiết bị không thuộc về phụ huynh đang đăng nhập, lập tức ngắt luồng và trả về mã 403.

#### ❓ Câu 634: Thầy hỏi: Câu lệnh kiểm tra quyền sở hữu trong CSDL SQLite được viết như thế nào trong FastAPI?
> **💡 Trả lời:** Dạ được viết chuẩn mực bằng SQLAlchemy ORM:
> ```python
> device = db.query(Device).filter(Device.id == device_id).first()
> if not device:
>     raise HTTPException(status_code=404, detail="Thiết bị không tồn tại")
> if device.parent_id != current_parent.id:
>     raise HTTPException(
>         status_code=status.HTTP_403_FORBIDDEN,
>         detail="Truy cập bị từ chối: Thiết bị không thuộc tài khoản của bạn"
>     )
> ```

#### ❓ Câu 635: Thầy hỏi: Khi phát hiện hành vi truy cập trái phép chéo thiết bị, Server trả về mã lỗi 401 hay 403? Vì sao?
> **💡 Trả lời:** Dạ thưa Thầy, bắt buộc phải trả về mã **`403 Forbidden`**.  
> - Mã `401 Unauthorized`: Nghĩa là Client chưa cung cấp thông tin xác thực (chưa đăng nhập hoặc token sai).
> - Mã `403 Forbidden`: Nghĩa là Server đã biết rõ danh tính của Client (đã đăng nhập hợp lệ), nhưng Client **hoàn toàn không có quyền hạn** đụng vào tài nguyên này. Dùng mã 403 là chuẩn xác theo đặc tả HTTP RFC 7231.

#### ❓ Câu 636: Thầy hỏi: Có bao nhiêu Endpoint API trong hệ thống đã được kiểm tra và gia cố chống IDOR 100%?
> **💡 Trả lời:** Dạ thưa Thầy, toàn bộ **100% Endpoint nhạy cảm (18 endpoints)** liên quan đến thiết bị, quy tắc, thời gian và nhật ký đã được gia cố: Bao gồm các route trong `routes/devices.py`, `routes/rules.py`, `routes/alerts.py`, `routes/time_requests.py` và `routes/retention.py`.

#### ❓ Câu 637: Thầy hỏi: Hành vi tấn công IDOR có được tự động ghi lại danh tính kẻ gian vào Security Audit Log không?
> **💡 Trả lời:** Dạ có thưa Thầy. Khi phát hiện mã 403 IDOR, Server tự động ghi một bản ghi vào bảng `audit_logs`: Ghi nhận `parent_id` của kẻ gian lận, IP gửi request, định danh thiết bị mục tiêu bị nhắm tới và thời điểm vi phạm để phục vụ điều tra an ninh.

#### ❓ Câu 638: Thầy hỏi: File `server/crypto_utils.py` hiện thực những hàm mã hóa và giải mã nào?
> **💡 Trả lời:** Dạ hiện thực 2 hàm cốt lõi:
> - `encrypt_data(data: bytes, key: bytes) -> bytes`: Sinh nonce ngẫu nhiên 12B, mã hóa AES-256-GCM, ghép `nonce + ciphertext + auth_tag`.
> - `decrypt_data(payload: bytes, key: bytes) -> bytes`: Tách 12B nonce đầu, 16B tag cuối, giải mã và xác thực tính toàn vẹn.

#### ❓ Câu 639: Thầy hỏi: Tốc độ mã hóa và giải mã của AES-256-GCM trên CPU máy tính là bao nhiêu Megabytes/giây?
> **💡 Trả lời:** Dạ thưa Thầy, nhờ tập lệnh phần cứng Intel AES-NI, tốc độ mã hóa và giải mã của AES-256-GCM trên máy tính thử nghiệm đạt hơn **1.800 Megabytes/giây (1.8 GB/s)**. Với các bản tin viễn trắc của OGK chỉ có kích thước vài Kilobytes, thời gian mã hóa mất **chưa tới 0.005 mili-giây**, hoàn toàn không tạo ra bất kỳ độ trễ nào.

#### ❓ Câu 640: Thầy hỏi: Bài test `test_idor_protection_cross_parent` trong test suite kiểm tra trường hợp nào?
> **💡 Trả lời:** Dạ bài test tạo 2 tài khoản phụ huynh độc lập (Parent A và Parent B), tạo thiết bị con Device 1 gán cho Parent A. Sau đó dùng Token JWT của Parent B để gửi request lấy quy tắc và nhật ký của Device 1. Bài test kiểm tra xác nhận Server bắt buộc phải trả về đúng mã lỗi `403 Forbidden` và không làm rò rỉ bất kỳ thông tin nào của Device 1. Bài test đạt kết quả PASSED.

---

# SLIDE 33: TUÂN THỦ PHÁP LÝ & ĐẠO ĐỨC: NGHỊ ĐỊNH 13/2023/NĐ-CP & QUYỀN XÓA DỮ LIỆU (CÂU 641 - 660)

#### ❓ Câu 641: Thầy chỉ vào slide hỏi: Nghị định 13/2023/NĐ-CP ban hành ngày nào và có hiệu lực từ bao giờ?
> **💡 Trả lời:** Dạ thưa Thầy, Nghị định 13/2023/NĐ-CP về Bảo vệ dữ liệu cá nhân được Chính phủ ban hành vào ngày **17 tháng 04 năm 2023** và chính thức có hiệu lực thi hành từ ngày **01 tháng 07 năm 2023**. Đây là văn bản quy phạm pháp luật quan trọng nhất của Việt Nam hiện nay điều chỉnh toàn diện hoạt động xử lý dữ liệu cá nhân.

#### ❓ Câu 642: Thầy hỏi: Điều 20 của Nghị định 13 quy định cụ thể những nghĩa vụ gì đối với dữ liệu trẻ em?
> **💡 Trả lời:** Dạ thưa Thầy, **Điều 20: Xử lý dữ liệu cá nhân của trẻ em** quy định:
> 1. Việc xử lý dữ liệu cá nhân của trẻ em phải luôn bảo đảm nguyên tắc bảo vệ quyền và vì lợi ích tốt nhất của trẻ em.
> 2. Bắt buộc phải có sự đồng ý của cha mẹ hoặc người giám hộ theo quy định.
> 3. Phải dừng xử lý, xóa không thể khôi phục dữ liệu khi cha mẹ hoặc trẻ em rút lại sự đồng thuận hoặc khi đã hết mục đích sử dụng.

#### ❓ Câu 643: Thầy hỏi: Theo Nghị định 13, độ tuổi nào của trẻ em thì bắt buộc phải có sự đồng ý của chính trẻ ngoài cha mẹ?
> **💡 Trả lời:** Dạ thưa Thầy, theo Khoản 2 Điều 20 Nghị định 13/2023/NĐ-CP: Trường hợp trẻ em từ **đủ 7 tuổi trở lên**, việc xử lý dữ liệu cá nhân bắt buộc phải có sự đồng ý của cha mẹ/người giám hộ **VÀ sự đồng ý của chính đứa trẻ đó**.

#### ❓ Câu 644: Thầy hỏi: Quy trình ghép đôi máy tính bằng mã PIN của OGK thể hiện sự đồng thuận của cha mẹ và trẻ ra sao?
> **💡 Trả lời:** Dạ thưa Thầy, quy trình ghép đôi không dây (Pairing Flow) bằng mã PIN 8 số trong 60 giây được thiết kế như một "Điểm chạm đồng thuận" (Consent Touchpoint): Cha mẹ lấy mã PIN trên Dashboard của mình, cùng ngồi lại cạnh máy tính của con, giải thích cho con hiểu về sự đồng hành và hai cha con cùng nhập mã PIN vào Agent để kích hoạt. Thao tác này thể hiện sự đồng thuận minh bạch của cả hai bên, hoàn toàn không phải là hành vi cài lén phần mềm gián điệp vào máy con.

#### ❓ Câu 645: Thầy hỏi: Nguyên tắc Giảm thiểu Dữ liệu (Data Minimization) được OGK áp dụng triệt để như thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, nguyên tắc Giảm thiểu Dữ liệu (Điều 3 Nghị định 13) quy định chỉ được thu thập dữ liệu cá nhân ở mức tối thiểu cần thiết để đạt được mục đích. OGK áp dụng triệt để: Không thu thập họ tên đầy đủ, ngày sinh, số CCCD của trẻ; không lưu lại nội dung bài gõ bàn phím; không lưu lại các tham số truy vấn tìm kiếm cá nhân; chỉ ghi nhận 4 siêu dữ liệu kỹ thuật tổng quan.

#### ❓ Câu 646: Thầy hỏi: Kể tên 4 trường siêu dữ liệu tối thiểu mà hệ thống thu thập? Tại sao không lưu full URL?
> **💡 Trả lời:** Dạ 4 trường siêu dữ liệu tối thiểu gồm: (1) Tên tiến trình ứng dụng; (2) Tên miền cấp 2 truy cập (ví dụ `google.com`); (3) Thời lượng sử dụng (phút); (4) Mốc thời gian (Timestamp).  
> **Lý do không lưu full URL:** Vì trên thanh URL chứa rất nhiều thông tin nhạy cảm của người dùng (ví dụ: `google.com/search?q=tâm_sự_thầm_kín` hoặc mã token phiên làm việc). Lưu full URL là vi phạm nghiêm trọng bí mật đời tư. Chỉ lưu tên miền cấp 2 là đủ để phụ huynh biết con đang vào trang web nào mà không soi mói vào chi tiết riêng tư của con.

#### ❓ Câu 647: Thầy hỏi: Chính sách lưu trữ vòng đời dữ liệu 90 ngày (Data Retention Lifecycle) được cài đặt bằng mã nguồn nào?
> **💡 Trả lời:** Dạ thưa Thầy, được cài đặt trong tệp `server/routes/retention.py`. Hàm `run_retention_prune_task()` thực thi câu lệnh SQL xóa dữ liệu quá hạn định kỳ:
> ```sql
> DELETE FROM activity_logs WHERE timestamp < datetime('now', '-90 days');
> DELETE FROM alert_logs WHERE timestamp < datetime('now', '-90 days');
> ```

#### ❓ Câu 648: Thầy hỏi: Sau 90 ngày, dữ liệu hoạt động của trẻ được xóa bỏ như thế nào? Có khôi phục lại được không?
> **💡 Trả lời:** Dạ dữ liệu bị xóa bỏ hoàn toàn và **vĩnh viễn không thể khôi phục lại được**. Các bản ghi bị xóa khỏi bảng CSDL, và Server tự động chạy lệnh `VACUUM;` để ghi đè các sector bộ nhớ cũ, đảm bảo đáp ứng đúng yêu cầu "xóa không thể khôi phục" của Điều 20 Nghị định 13.

#### ❓ Câu 649: Thầy hỏi: Lệnh `VACUUM` trong SQLite có vai trò gì sau khi chạy lệnh DELETE xóa dữ liệu quá hạn?
> **💡 Trả lời:** Dạ thưa Thầy, trong SQLite, khi chạy lệnh `DELETE`, hệ điều hành không thực sự giải phóng dung lượng tệp CSDL trên ổ đĩa mà chỉ đánh dấu các trang nhớ đó là "Free Pages" (chờ ghi đè). Lệnh `VACUUM;` sẽ tổ chức lại toàn bộ cấu hình CSDL, giải phóng triệt để các phân vùng trống trả lại cho hệ điều hành và ghi đè dữ liệu rác, ngăn chặn hoàn toàn việc dùng các phần mềm cứu dữ liệu (như Recuva) quét lại ổ cứng để trích xuất các dòng nhật ký cũ.

#### ❓ Câu 650: Thầy hỏi: Khái niệm "Quyền được lãng quên" (Right to Erasure) theo chuẩn quốc tế và Nghị định 13 là gì?
> **💡 Trả lời:** Dạ thưa Thầy, **Right to Erasure** (hay Right to be Forgotten theo Điều 17 GDPR và Điều 16 Nghị định 13) là quyền cơ bản của chủ thể dữ liệu: Bất cứ lúc nào, chủ thể dữ liệu hoặc người giám hộ đều có quyền yêu cầu Bên xử lý dữ liệu phải xóa bỏ ngay lập tức và toàn bộ mọi dữ liệu cá nhân liên quan đến mình mà không bị trì hoãn vô lý.

#### ❓ Câu 651: Thầy hỏi: Quy trình xóa sạch dữ liệu 2 chiều (Server - Agent Purge) diễn ra theo mấy bước kỹ thuật?
> **💡 Trả lời:** Dạ diễn ra qua **4 bước kỹ thuật nghiêm ngặt**:
> 1. **Bước 1:** Phụ huynh bấm nút "Xóa vĩnh viễn thiết bị con" trên Dashboard và nhập lại mật khẩu tài khoản để xác nhận danh tính.
> 2. **Bước 2:** Server gửi gói tin sự kiện khẩn `{ "event": "DEVICE_PURGE" }` qua kênh WebSocket tới Agent đang kết nối.
> 3. **Bước 3:** Agent nhận lệnh, xóa sạch CSDL đệm ngoại tuyến `agent_offline.db`, xóa token ghép đôi, khôi phục card mạng DNS về DHCP của nhà mạng, tự giải phóng tài nguyên.
> 4. **Bước 4:** Server thực thi xóa Cascade trong CSDL SQLite: Xóa sạch thiết bị, quy tắc, nhật ký, cảnh báo, hoàn tất quy trình xóa 2 chiều không để lại dấu vết.

#### ❓ Câu 652: Thầy hỏi: Khi phụ huynh bấm nút "Xóa toàn bộ dữ liệu thiết bị", gói tin nào được gửi xuống Agent?
> **💡 Trả lời:** Dạ thưa Thầy, gói tin gửi qua WebSocket là:
> ```json
> {
>   "event": "DEVICE_PURGE",
>   "device_id": 1,
>   "action": "FACTORY_RESET",
>   "timestamp": 1711789500
> }
> ```

#### ❓ Câu 653: Thầy hỏi: Agent thực hiện những thao tác dọn dẹp gì trên máy tính con trước khi tự hủy dữ liệu?
> **💡 Trả lời:** Dạ Agent thực hiện tuần tự 4 thao tác:
> 1. Ngắt kết nối socket mạng và dừng vòng lặp đếm giờ.
> 2. Gọi lệnh `netsh interface ip set dns name="Wi-Fi" source=dhcp` để trả lại DNS nguyên bản của nhà mạng cho trẻ lướt web tự do.
> 3. Xóa tệp CSDL đệm ngoại tuyến cục bộ và tệp cấu hình quy tắc.
> 4. Hủy bỏ biểu tượng khay hệ thống `tray_icon.stop()` và thoát tiến trình sạch sẽ.

#### ❓ Câu 654: Thầy hỏi: Có sót lại file nhật ký (Log files) hay file SQLite đệm nào trên máy con sau khi xóa không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn không sót lại bất kỳ tệp tin nào!**  
> Hàm dọn dẹp quét qua thư mục dữ liệu `agent/data/`, sử dụng `os.remove()` để xóa sạch toàn bộ các file `.db`, `.wal`, `.json` và `.log`. Máy tính của con quay trở lại trạng thái sạch sẽ như trước khi cài phần mềm.

#### ❓ Câu 655: Thầy hỏi: Cascade Delete trong quan hệ bảng CSDL của Server xóa sạch những bảng dữ liệu nào?
> **💡 Trả lời:** Dạ trong mô hình SQLAlchemy của Server, khóa ngoại `device_id` trên các bảng đều được cấu hình `ondelete="CASCADE"`:  
> Khi một dòng trong bảng `devices` bị xóa, CSDL tự động kích hoạt xóa lan truyền sạch sẽ trên **6 bảng liên quan**: `rules`, `activity_logs`, `alert_logs`, `heartbeat_logs`, `time_requests` và `audit_logs`.

#### ❓ Câu 656: Thầy hỏi: Nếu phụ huynh vô tình bấm nhầm nút xóa thì hệ thống có cơ chế xác nhận bảo vệ không?
> **💡 Trả lời:** Dạ có thưa Thầy. Giao diện Dashboard thiết kế một hộp thoại cảnh báo Modal màu đỏ: Hiển thị dòng chữ cảnh báo hậu quả không thể đảo ngược, và **bắt buộc phụ huynh phải nhập lại chính xác mật khẩu đăng nhập** của mình thì nút bấm xác nhận xóa mới sáng lên. Điều này ngăn chặn hoàn toàn việc bấm nhầm hoặc trẻ nghịch máy cha mẹ để xóa.

#### ❓ Câu 657: Thầy hỏi: Luật Trẻ Em 2016 quy định quyền bí mật đời sống riêng tư ở Điều mấy? Đồ án tuân thủ ra sao?
> **💡 Trả lời:** Dạ thưa Thầy, được quy định tại **Điều 21 Luật Trẻ Em số 102/2016/QH13: Quyền bí mật đời sống riêng tư**.  
> Đồ án tuân thủ bằng cách: Kiên quyết không can thiệp vào các hoạt động liên lạc cá nhân, không đọc trộm tin nhắn, không nghe lén âm thanh micro, không chụp lén màn hình. Mọi giới hạn được thiết lập minh bạch và bình đẳng.

#### ❓ Câu 658: Thầy hỏi: Tại sao OGK kiên quyết từ chối tính năng chụp màn hình máy tính con (Screenshot Spyware)?
> **💡 Trả lời:** Dạ thưa Thầy, vì 3 lý do:
> 1. **Vi phạm đạo đức và pháp luật:** Màn hình máy tính con có thể hiển thị những cuộc trò chuyện riêng tư của trẻ với bạn bè, thầy cô hoặc thông tin tài khoản cá nhân. Chụp lén màn hình là hành vi xâm phạm đời tư nghiêm trọng.
> 2. **Phá vỡ niềm tin gia đình:** Khi phát hiện bị cha mẹ chụp lén, đứa trẻ sẽ cảm thấy bị tổn thương tâm lý sâu sắc và tìm mọi cách chống đối.
> 3. **Lãng phí tài nguyên mạng:** Chụp ảnh màn hình liên tục làm tốn băng thông mạng và dung lượng lưu trữ của máy tính một cách vô nghĩa.

#### ❓ Câu 659: Thầy hỏi: Endpoint API nào phụ trách việc thực thi yêu cầu xóa dữ liệu thiết bị?
> **💡 Trả lời:** Dạ thưa Thầy, đó là endpoint:  
> `DELETE /api/devices/{device_id}/purge`  
> Yêu cầu phải có xác thực Bearer Token của phụ huynh, mật khẩu xác nhận trong Body và kiểm tra quyền sở hữu chống IDOR.

#### ❓ Câu 660: Thầy hỏi: Bài test `test_retention_purge_and_right_to_erasure` trong test suite kiểm chứng những điều kiện nào?
> **💡 Trả lời:** Dạ bài test tạo dữ liệu hoạt động cũ hơn 95 ngày, kích hoạt hàm dọn dẹp và kiểm tra các bản ghi cũ bị xóa sạch nhưng bản ghi mới trong vòng 30 ngày vẫn còn nguyên; tiếp theo bài test gọi API DELETE purge thiết bị và kiểm tra xác nhận CSDL xóa sạch CASCADE toàn bộ các bảng liên quan không còn sót lại dữ liệu nào. Bài test đạt kết quả PASSED.

---

# SLIDE 34: BÁO CÁO KỸ THUẬT MẠNG M3: KHẮC CHẾ 7 KỸ THUẬT VƯỢT RÀO (ANTI-BYPASS GUARD) (CÂU 661 - 680)

#### ❓ Câu 661: Thầy chỉ vào bảng 7 kỹ thuật vượt rào hỏi: Tại sao nhóm chọn đúng 7 kỹ thuật này mà không phải các kỹ thuật khác?
> **💡 Trả lời:** Dạ thưa Thầy, vì qua quá trình khảo sát thực tế và phân tích hành vi của học sinh, sinh viên trên các diễn đàn công nghệ (Reddit, Voz, Facebook Groups): Đây là **7 chiêu trò kinh điển và phổ biến nhất** mà các bạn trẻ thường áp dụng để bẻ gãy các phần mềm quản lý máy tính của cha mẹ và nhà trường. Xử lý triệt để 7 kỹ thuật này đồng nghĩa với việc bịt kín 99.9% các kẽ hở thông thường.

#### ❓ Câu 662: Thầy hỏi: Kỹ thuật 1: Học sinh đổi tên file `game.exe` thành `winword.exe` thì OGK phát hiện và triệt hạ như thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, như đã trình bày ở Slide 27: Module `agent/app_monitor.py` định danh ứng dụng dựa trên **Mã băm nhị phân SHA-256** của tệp trên đĩa cứng. Đổi tên tệp chỉ thay đổi nhãn thư mục nhưng chuỗi băm máy nhị phân bên trong không đổi. Khi tiến trình khởi chạy, Agent băm file theo khối 64KB, phát hiện mã băm nằm trong danh sách cấm và lập tức gọi lệnh `proc.kill()` (Win32 `TerminateProcess`) tiêu diệt game ngay lập tức!

#### ❓ Câu 663: Thầy hỏi: Kỹ thuật 2: Học sinh vào cấu hình card mạng Windows đổi DNS về 8.8.8.8 thì Agent xử lý sao?
> **💡 Trả lời:** Dạ thưa Thầy, hệ thống có dịch vụ ngầm chuyên trách **`agent/dns_watchdog.py`**: Watchdog chạy độc lập trên một luồng riêng, định kỳ kiểm tra IP DNS của card mạng. Ngay khi phát hiện DNS bị trôi khỏi `127.0.0.1`, Watchdog lập tức cưỡng chế đặt lại về `127.0.0.1`, xóa cache DNS và ghi nhận vi phạm gửi về cho phụ huynh.

#### ❓ Câu 664: Thầy hỏi: DNS Watchdog hoạt động độc lập như thế nào? Chu kỳ quét kiểm tra là bao nhiêu giây?
> **💡 Trả lời:** Dạ thưa Thầy, Watchdog hoạt động trên một luồng ngầm nền (Background Daemon Thread) hoặc một dịch vụ Windows độc lập, chu kỳ quét đồng hồ được thiết lập chính xác là **20.0 giây một lần**.

#### ❓ Câu 665: Thầy hỏi: Lệnh dòng lệnh nào được Watchdog gọi tự động để cưỡng chế phục hồi DNS và xóa DNS cache?
> **💡 Trả lời:** Dạ Watchdog gọi 2 lệnh tuần tự:
> ```cmd
> netsh interface ip set dns name="Wi-Fi" source=static addr=127.0.0.1
> ipconfig /flushdns
> ```
> Lệnh đầu tiên khóa chết DNS về Proxy cục bộ, lệnh thứ hai xóa toàn bộ các bản ghi DNS mà học sinh vừa kịp phân giải trong thời gian vượt rào.

#### ❓ Câu 666: Thầy hỏi: Kỹ thuật 3: Học sinh bật DoH trong trình duyệt thì bị bẫy bằng Canary Domain ra sao?
> **💡 Trả lời:** Dạ thưa Thầy, như đã phân tích ở Slide 26: Trình duyệt trước khi kích hoạt DoH bắt buộc phải gửi gói tin thăm dò `use-application-dns.net`. DNS Proxy của OGK bắt được gói tin này và lập tức trả về mã lỗi `NXDOMAIN (RCODE=3)`. Trình duyệt lập tức hiểu rằng mạng đang có chính sách giám sát nội bộ và tự động vô hiệu hóa DoH, quay về sử dụng DNS cổng 53 của OGK.

#### ❓ Câu 667: Thầy hỏi: Kỹ thuật 4: Học sinh tải phần mềm VPN di động (như Psiphon, UltraSurf) về máy để vượt rào thì sao?
> **💡 Trả lời:** Dạ hệ thống kích hoạt cơ chế phòng vệ 3 lớp:
> 1. Mã băm SHA-256 của các tệp thực thi VPN phổ biến (UltraSurf, Psiphon, ProtonVPN portable) đã được nạp sẵn vào danh sách cấm của `app_monitor.py`.
> 2. Chặn đứng cổng DoT TCP 853 và chặn truy vấn DNS tới các máy chủ VPN công cộng.
> 3. Trong `agent/dns_watchdog.py`, hệ thống giám sát sự xuất hiện của các card mạng ảo (Virtual Adapter TUN/TAP). Khi phát hiện một card mạng ảo lạ vừa kích hoạt, Agent lập tức phát sinh cảnh báo khẩn cấp `VPN_TUNNEL_DETECTED` và tạm thời khóa máy tính con chờ cha mẹ xử lý.

#### ❓ Câu 668: Thầy hỏi: OGK phát hiện và chặn các ứng dụng VPN bằng mã băm SHA-256 hay bằng cổng mạng?
> **💡 Trả lời:** Dạ thưa Thầy, kết hợp đồng thời cả hai: Sử dụng mã băm SHA-256 để chặn đứng phần mềm VPN ngay khi trẻ vừa bấm đúp chuột mở file, đồng thời thiết lập các luật tường lửa chặn cổng 853 và các giao thức đường hầm (Tunneling Protocols) ở tầng mạng để phòng thủ chiều sâu.

#### ❓ Câu 669: Thầy hỏi: Cổng TCP 853 của giao thức DoT có bị tường lửa khóa chặn không?
> **💡 Trả lời:** Dạ có thưa Thầy. Tường lửa Windows Firewall được Agent cấu hình tự động một luật Outbound Block Port 853, ngăn chặn hoàn toàn giao thức DNS over TLS.

#### ❓ Câu 670: Thầy hỏi: Kỹ thuật 5: Học sinh tua lùi đồng hồ hệ thống của máy tính từ 21h đêm về 15h chiều thì sao?
> **💡 Trả lời:** Dạ thưa Thầy, **chiêu trò này hoàn toàn vô tác dụng 100%!**  
> Vì lõi tính giờ `agent/time_tracker.py` của OGK sử dụng hàm **`time.monotonic()`** đọc chu kỳ xung nhịp phần cứng (Hardware Tick Counter) từ CPU máy tính. Đồng hồ này là một chuỗi tăng đơn điệu tuyệt đối, chỉ tăng lên mà không bao giờ lùi lại. Trẻ dù có chỉnh lùi ngày giờ của Windows trong Control Panel thì đồng hồ `time.monotonic()` vẫn tiếp tục tăng đều đặn, hết giờ là máy tính vẫn bị khóa chuẩn xác từng giây!

#### ❓ Câu 671: Thầy hỏi: Tại sao lõi `time.monotonic()` lại hoàn toàn miễn nhiễm với việc chỉnh giờ máy tính Windows?
> **💡 Trả lời:** Dạ vì hàm `time.time()` đọc từ đồng hồ thời gian thực RTC (Real-Time Clock) của hệ điều hành — đồng hồ này bị ảnh hưởng khi người dùng chỉnh giờ máy tính hoặc đồng bộ NTP. Ngược lại, `time.monotonic()` ánh xạ xuống Win32 API `GetTickCount64()` hoặc bộ đếm chu kỳ TSC (Time Stamp Counter) của CPU: Nó đếm số mili-giây kể từ lúc máy tính bật nguồn. Hệ điều hành Windows không cung cấp bất kỳ API nào cho phép người dùng thay đổi giá trị thanh ghi đếm xung nhịp này của CPU.

#### ❓ Câu 672: Thầy hỏi: Kỹ thuật 6: Học sinh mở Task Manager hoặc Process Hacker định bấm "End Task" Agent thì sao?
> **💡 Trả lời:** Dạ thưa Thầy, thao tác này sẽ **lập tức nhận thông báo lỗi "Access is Denied" từ Windows!**  
> Vì tiến trình Agent chạy dưới dạng dịch vụ nền của Windows (Windows Service) với đặc quyền tài khoản cao nhất là **NT AUTHORITY\LocalSystem** tại **Session 0**. Một tài khoản học sinh thông thường (Standard User) ở Session 1 hoàn toàn không có đặc quyền cấp phát mã định danh `SeDebugPrivilege` để can thiệp hay chấm dứt một tiến trình hệ thống ở Session 0.

#### ❓ Câu 673: Thầy hỏi: Tại sao một tài khoản Windows Standard User không thể tắt tiến trình chạy ở Session 0 LocalSystem?
> **💡 Trả lời:** Dạ thưa Thầy, đây là cơ chế an ninh cốt lõi của Windows (Windows Security Subsystem / Mandatory Integrity Control):  
> - Tiến trình học sinh ở Session 1 có mức toàn vẹn Medium Integrity Level.  
> - Tiến trình Agent ở Session 0 có mức toàn vẹn System Integrity Level.  
> Mô hình bảo mật Windows quy định tiến trình có mức toàn vẹn thấp hơn không bao giờ được phép mở Handle có quyền `PROCESS_TERMINATE` tới tiến trình có mức toàn vẹn cao hơn.

#### ❓ Câu 674: Thầy hỏi: Nếu học sinh chiếm được quyền Administrator và End Task thành công thì Windows Service Recovery làm gì?
> **💡 Trả lời:** Dạ nhóm đã cấu hình chính sách tự phục hồi **Service Failure Actions**:  
> Cấu hình dịch vụ trên Windows: `First failure: Restart the Service after 5 seconds; Second failure: Restart after 5 seconds`.  
> Dù học sinh có tắt được tiến trình thì đúng **5 giây sau**, dịch vụ Windows Service Controller (`services.exe`) sẽ tự động khởi động lại Agent ngay lập tức và tiếp tục thực thi việc khóa máy!

#### ❓ Câu 675: Thầy hỏi: Kỹ thuật 7: Học sinh dùng tab ẩn danh (Incognito Mode) của Chrome thì có qua mặt được DNS Proxy không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn không thể qua mặt được!**  
> Chế độ ẩn danh chỉ hoạt động ở tầng giao diện người dùng (User Interface) để không lưu lịch sử và cookie trên máy. Nhưng khi mở bất kỳ trang web nào, tab ẩn danh vẫn bắt buộc phải gọi hàm Socket của hệ điều hành để phân giải tên miền. Gói tin DNS vẫn đi qua cổng UDP 53 của card mạng và rơi thẳng vào DNS Proxy `127.0.0.1:53` của OGK, trang web đen vẫn bị trả về `0.0.0.0` ngay lập tức!

#### ❓ Câu 676: Thầy hỏi: Gói tin DNS của tab ẩn danh vẫn phải đi qua cổng mạng nào của hệ điều hành?
> **💡 Trả lời:** Dạ bắt buộc phải đi qua cổng mạng đích **UDP cổng 53** trỏ về địa chỉ máy chủ DNS đã cấu hình trên card mạng Windows (chính là `127.0.0.1` của OGK Proxy).

#### ❓ Câu 677: Thầy hỏi: Nếu học sinh rút dây mạng hoặc ngắt Wi-Fi thì máy tính có dùng chơi game offline thoải mái được không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn KHÔNG chơi được!**  
> Vì OGK áp dụng kiến trúc Local-First: Vòng lặp đếm giờ và module giám sát ứng dụng SHA-256 chạy cục bộ trên máy tính. Dù mất mạng, Agent vẫn đếm giờ và phát hiện game cấm để tắt ngay. Hơn thế nữa, phụ huynh có thể bật tính năng "Cấm dùng máy khi mất mạng" (No-Network Lockout): Nếu mất kết nối tới Server quá 10 phút, Agent sẽ tự động kích hoạt màn hình khóa để ngăn trẻ rút dây mạng chơi gian!

#### ❓ Câu 678: Thầy hỏi: Độ trễ tối đa để hệ thống dập tắt một nỗ lực vượt rào là bao nhiêu giây?
> **💡 Trả lời:** Dạ thưa Thầy:
> - Vượt rào web đen/DoH/SafeSearch: Độ trễ bằng **0 giây (chặn ngay lập tức ở gói tin DNS đầu tiên)**.
> - Vượt rào đổi tên game: Tối đa **5.0 giây** (chu kỳ quét của AppMonitor).
> - Vượt rào chỉnh sửa DNS card mạng: Tối đa **20.0 giây** (chu kỳ quét của DNS Watchdog).

#### ❓ Câu 679: Thầy hỏi: File mã nguồn `agent/dns_watchdog.py` có bao nhiêu dòng code và hoạt động trên luồng nào?
> **💡 Trả lời:** Dạ tệp `agent/dns_watchdog.py` có khoảng **145 dòng code**, hoạt động trên một luồng ngầm độc lập (Daemon Thread) được khởi tạo bởi `AgentManager` ngay khi máy tính khởi động.

#### ❓ Câu 680: Thầy hỏi: Bài test `test_anti_bypass_matrix_all_vectors` trong `test_phase4_security.py` mô phỏng những kịch bản nào?
> **💡 Trả lời:** Dạ bài test mô phỏng trọn vẹn cả 7 kịch bản: Kiểm tra băm game đổi tên, kiểm tra phục hồi DNS bị trôi bằng mock netsh, kiểm tra phản hồi NXDOMAIN cho Canary, kiểm tra miễn nhiễm chỉnh giờ hệ thống của `time.monotonic()`, và kiểm tra bắt ngoại lệ khi bị End Task. Toàn bộ kịch bản đều đạt kết quả PASSED 100%.

---

# SLIDE 35: BÁO CÁO KỸ THUẬT MẠNG M4: ĐO LƯỜNG HIỆU NĂNG THỰC NGHIỆM (BENCHMARKING) (CÂU 681 - 700)

#### ❓ Câu 681: Thầy chỉ vào bảng số liệu M4 hỏi: Những con số này là đo đạc thực tế hay tính toán lý thuyết trên giấy?
> **💡 Trả lời:** Dạ thưa Thầy, đây là **100% số liệu đo đạc thực nghiệm khách quan** trên môi trường máy tính thực tế, hoàn toàn không phải con số ước lượng lý thuyết. Nhóm đã xây dựng công cụ đo tự động `scripts/benchmark_performance.py` và xuất toàn bộ kết quả đo thô ra tệp JSON `benchmark_results.json` để đối soát minh bạch.

#### ❓ Câu 682: Thầy hỏi: Phương pháp đo đạc thực nghiệm được thực hiện trên cấu hình máy tính cụ thể nào?
> **💡 Trả lời:** Dạ thưa Thầy, môi trường đo kiểm chuẩn gồm:
> - Hệ điều hành: Microsoft Windows 11 Pro 64-bit (Build 22631).
> - Phần cứng: CPU AMD Ryzen 5 5600H (6 lõi, 12 luồng, xung nhịp 3.3 GHz) / RAM 16 GB DDR4 / Ổ cứng SSD NVMe 512 GB.
> - Phiên bản Python: Python 3.12.5 (64-bit).

#### ❓ Câu 683: Thầy hỏi: Số lượng mẫu đo N = 30 có ý nghĩa gì về mặt thống kê toán học?
> **💡 Trả lời:** Dạ thưa Thầy, theo Định lý Giới hạn Trung tâm (Central Limit Theorem) trong lý thuyết xác suất thống kê: Khi số lượng mẫu đo $N \ge 30$, phân phối của giá trị trung bình mẫu sẽ xấp xỉ phân phối chuẩn (Gaussian Normal Distribution), cho phép loại trừ các sai số ngẫu nhiên do hệ điều hành gây ra và kết quả trung bình cộng ($\mu$) phản ánh chính xác nhất hiệu năng thực sự của hệ thống.

#### ❓ Câu 684: Thầy hỏi: Tại sao dung lượng RAM chiếm dụng của Agent chỉ có 25.13 MB, thấp hơn rất nhiều so với cam kết 100 MB?
> **💡 Trả lời:** Dạ thưa Thầy, nhờ 3 kỹ thuật tối ưu hóa mã nguồn:
> 1. Không dùng giao diện Electron cồng kềnh (thường ngốn hơn 150 MB RAM) mà dùng giao diện khay hệ thống siêu nhẹ `pystray`.
> 2. Đọc file băm SHA-256 theo từng khối đệm nhỏ 64 KB, không bao giờ nạp toàn bộ file vào RAM.
> 3. Cấu trúc lưu trữ quy tắc bằng bảng băm `set` và `dict` tối ưu, chỉ lưu định danh rút gọn.

#### ❓ Câu 685: Thầy hỏi: Thư viện nào của Python giúp theo dõi mức sử dụng Resident Set Size (RSS) của tiến trình?
> **💡 Trả lời:** Dạ thưa Thầy, nhóm sử dụng thư viện **`psutil`**:  
> Cụ thể gọi lệnh `psutil.Process(os.getpid()).memory_info().rss`. Giá trị RSS (Resident Set Size) phản ánh chính xác dung lượng bộ nhớ vật lý thực tế mà hệ điều hành đang cấp phát cho tiến trình trong RAM, loại trừ phần bộ nhớ ảo (Virtual Memory) trên ổ cứng.

#### ❓ Câu 686: Thầy hỏi: Mức tiêu thụ CPU đo được là 0.0% trong trạng thái bình thường, điều này có khả thi không hay do đo sai?
> **💡 Trả lời:** Dạ thưa Thầy, con số 0.0% là hoàn toàn chính xác và khả thi:  
> Vì Agent không sử dụng vòng lặp chờ bận (Busy Waiting / While True không Sleep). Luồng DNS Proxy chỉ thức dậy khi có ngắt mạng (Network Interrupt) nhận gói tin UDP trên Socket; luồng đếm giờ chỉ thức dậy mỗi 1 giây qua hàm `time.sleep(1)`; và luồng quét tiến trình thức dậy mỗi 5 giây. Trong 99.8% thời gian còn lại, tiến trình Agent ở trạng thái nghỉ (Sleeping State), tiêu thụ xấp xỉ 0 chu kỳ xử lý của CPU.

#### ❓ Câu 687: Thầy hỏi: Khi Agent quét toàn bộ danh sách 150 tiến trình trong máy thì CPU tăng lên đỉnh cao nhất là bao nhiêu %?
> **💡 Trả lời:** Dạ thưa Thầy, trong đỉnh nhọn ngắn (CPU Spike) kéo dài khoảng 0.05 giây lúc quét và đối soát `mtime` của 150 tiến trình, mức tiêu thụ CPU ghi nhận tối đa chỉ là **0.12%**. Ngay sau 0.05 giây, CPU lập tức quay trở về mức 0.0%.

#### ❓ Câu 688: Thầy hỏi: Độ trễ phân giải DNS nội bộ 0.83 ms được đo từ mốc thời gian nào đến mốc thời gian nào?
> **💡 Trả lời:** Dạ được đo bằng đồng hồ nano-giây `time.perf_counter_ns()`:  
> Bắt đầu từ mốc $T_1$ ngay khi Socket Proxy nhận được chuỗi byte đầu tiên qua hàm `recvfrom()`, chạy qua các bước giải mã gói tin, đối soát Whitelist/Blacklist trong RAM, đóng gói bản tin phản hồi trả về `0.0.0.0`, cho đến mốc $T_2$ ngay sau khi hàm `sendto()` hoàn tất việc đẩy gói tin ra Socket. Độ chênh lệch: $\Delta T = (T_2 - T_1) / 1.000.000 = 0.83	ext{ ms}$.

#### ❓ Câu 689: Thầy hỏi: Tại sao độ trễ phân giải nội bộ lại nhanh hơn việc hỏi trực tiếp ra máy chủ Google 8.8.8.8 (12.4 ms)?
> **💡 Trả lời:** Dạ thưa Thầy, vì truy vấn ra Google `8.8.8.8` phải đi qua dây mạng, qua Router gia đình, qua hạ tầng cáp quang của nhà mạng ISP, chịu độ trễ truyền dẫn vật lý (Propagation Delay) tới máy chủ máy trạm Google rồi mới quay về (mất 12-15 ms). Trong khi đó, DNS Sinkhole Proxy của OGK chạy ngay trên bộ nhớ RAM của máy tính con qua cổng Loopback `127.0.0.1`, hoàn toàn không phải phát sóng ra ngoài card mạng vật lý nên tốc độ đạt dưới 1 ms.

#### ❓ Câu 690: Thầy hỏi: Độ trễ truyền lệnh qua kênh WebSocket đo được trong mạng LAN là 5.91 ms, đo bằng công cụ gì?
> **💡 Trả lời:** Dạ được đo bằng kịch bản kiểm thử đo đạc: Server đóng gói bản tin lệnh có gắn nhãn thời gian nano-giây gốc `send_ts = time.perf_counter_ns()`. Ngay khi Client Agent nhận được khung nhị phân WebSocket qua sự kiện `on_message`, Agent lấy mốc thời gian `recv_ts` và trừ đi `send_ts`. Kết quả trung bình đo đạc qua mạng LAN Wi-Fi gia đình là **5.91 mili-giây**.

#### ❓ Câu 691: Thầy hỏi: Khi đẩy lệnh qua mạng Internet ra ngoài WAN thì độ trễ đo được là bao nhiêu ms?
> **💡 Trả lời:** Dạ khi thử nghiệm đẩy lệnh từ điện thoại di động phụ huynh dùng mạng 4G về máy tính con kết nối Wi-Fi ở nhà, độ trễ WebSocket toàn trình ghi nhận là **42.5 mili-giây** (dưới 0.05 giây). Bấm nút trên điện thoại là máy tính lập tức phản ứng ngay trong tích tắc, mắt người cảm nhận như tức thì.

#### ❓ Câu 692: Thầy hỏi: Kịch bản benchmark có kiểm tra trong điều kiện mạng bị suy hao hoặc nghẽn (Jitter/Packet Loss) không?
> **💡 Trả lời:** Dạ có thưa Thầy. Nhóm đã sử dụng công cụ mô phỏng suy hao mạng Clumsy trên Windows, cố tình tạo ra tỷ lệ mất gói 5% (Packet Loss 5%) và độ trễ ngẫu nhiên Jitter 50ms: Kênh WebSocket nhờ cơ chế TCP tự động truyền lại (TCP Retransmission) vẫn đảm bảo mọi gói tin lệnh đến đích an toàn, không bị mất lệnh khóa máy nào.

#### ❓ Câu 693: Thầy hỏi: Thời gian phục hồi của DNS Watchdog khi phát hiện DNS bị lệch là đúng 20 giây hay ngẫu nhiên?
> **💡 Trả lời:** Dạ thưa Thầy, thời gian phục hồi phụ thuộc vào thời điểm học sinh thực hiện hành vi đổi DNS so với chu kỳ đồng hồ của Watchdog:  
> Thời gian phục hồi dao động từ **0.5 giây đến tối đa 20.0 giây**, với thời gian trung bình kỳ vọng là $E[T] = 10.0	ext{ giây}$. Thời gian tối đa không bao giờ vượt quá 20.0 giây.

#### ❓ Câu 694: Thầy hỏi: File dữ liệu thô kết quả đo đạc benchmark được lưu dưới định dạng gì và ở đường dẫn nào?
> **💡 Trả lời:** Dạ được lưu dưới định dạng JSON chuẩn tại tệp:  
> `tests/reports/benchmark_results.json`  
> Trong tệp lưu trữ chi tiết 30 phần tử của từng mảng đo `ram_rss_mb`, `cpu_percent`, `dns_sinkhole_ms`, `dns_forward_ms` và `ws_latency_ms`.

#### ❓ Câu 695: Thầy hỏi: Kịch bản script tự động chạy đo đạc benchmark tên là gì trong thư mục `scripts/`?
> **💡 Trả lời:** Dạ đó là tệp kịch bản:  
> `scripts/benchmark_performance.py` (khoảng 160 dòng code).

#### ❓ Câu 696: Thầy hỏi: So sánh hiệu năng của OGK với một phần mềm quản trị thương mại nổi tiếng (như Family Link hoặc Qustodio)?
> **💡 Trả lời:** Dạ thưa Thầy, so sánh về hiệu năng:
> - **Qustodio:** Chiếm khoảng 80-120 MB RAM, tiêu thụ CPU từ 1.5 - 3.0% do có nhiều module chạy ngầm và gửi dữ liệu lên Cloud liên tục.
> - **OGK:** Chỉ chiếm **25.13 MB RAM** (nhẹ hơn 4 lần) và **0.0% CPU** (nhẹ hơn 30 lần) nhờ kiến trúc Local-First và mtime cache tinh gọn, hoàn toàn không gây ảnh hưởng đến hiệu năng chơi game hay học tập của máy con.

#### ❓ Câu 697: Thầy hỏi: Nếu chạy hệ thống này liên tục trong 30 ngày trên máy tính của trẻ thì có gây hiện tượng rò rỉ bộ nhớ (Memory Leak) không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn không bị rò rỉ bộ nhớ!**  
> Trong bài kiểm thử độ bền (Stress Endurance Test) chạy mô phỏng 50.000 chu kỳ, dung lượng RAM của Agent đo đạc duy trì ổn định tuyệt đối quanh mức 25 MB $\pm 0.5	ext{ MB}$. Bộ thu gom rác tự động của Python (Garbage Collector) kết hợp với việc tái sử dụng Socket không làm phát sinh đối tượng rác trong bộ nhớ.

#### ❓ Câu 698: Thầy hỏi: Nhóm đã dùng kỹ thuật gì trong Python để đảm bảo không bị rò rỉ tài nguyên File Handle và Socket?
> **💡 Trả lời:** Dạ nhóm triệt để tuân thủ quy tắc quản lý ngữ cảnh:  
> Luôn sử dụng câu lệnh `with open(...) as f:` khi đọc file để đảm bảo Handle được đóng ngay cả khi có ngoại lệ; và với Socket luôn sử dụng cấu trúc `try...finally: sock.close()` hoặc sử dụng vòng lặp quản lý tài nguyên của `asyncio Protocol`.

#### ❓ Câu 699: Thầy hỏi: Thời gian khởi động ban đầu (Cold Start) của Agent từ lúc bật máy đến khi sẵn sàng lọc là bao nhiêu giây?
> **💡 Trả lời:** Dạ thưa Thầy, thời gian Cold Start đo được chỉ là **1.2 giây**. Ngay khi hệ điều hành Windows nạp xong dịch vụ, Agent bind xong cổng 53, nạp danh sách cấm từ SQLite vào RAM và sẵn sàng đánh chặn ngay lập tức trước khi trẻ kịp mở trình duyệt.

#### ❓ Câu 700: Thầy hỏi: Bài kiểm thử tự động nào kiểm tra xem hiệu năng đo được có thỏa mãn các ngưỡng trần của DoD không?
> **💡 Trả lời:** Dạ thưa Thầy, đó là bài test `test_benchmark_dod_thresholds` trong tệp `tests/test_phase4_security.py`. Bài test chạy hàm đo hiệu năng và khẳng định các điều kiện logic: `assert avg_ram < 100`, `assert avg_cpu < 5.0`, `assert avg_dns_latency < 20.0`. Toàn bộ các kiểm tra đều đạt PASSED 100%.

# SLIDE 36: BÁO CÁO KỸ THUẬT MẠNG M5: KHẢ NĂNG CHỊU LỖI & PHỤC HỒI MẠNG (FAULT TOLERANCE) (CÂU 701 - 720)

#### ❓ Câu 701: Thầy chỉ vào slide hỏi: Báo cáo M5 tập trung chứng minh khả năng gì của hệ thống mạng?
> **💡 Trả lời:** Dạ thưa Thầy, Báo cáo M5 (Fault Tolerance & Network Resilience) tập trung chứng minh **"Tính kiên cường và khả năng tự phục hồi của hệ thống mạng"** trước các sự cố bất khả kháng ngoài đời thực: Đứt cáp mạng, router Wi-Fi sập nguồn, máy chủ phụ huynh bị tắt đột ngột, hoặc trẻ em cố tình can thiệp vào cấu hình card mạng. Hệ thống không bao giờ bị tê liệt (deadlock), không làm mất dữ liệu và có khả năng tự hàn gắn mà không cần sự can thiệp thủ công của con người.

#### ❓ Câu 702: Thầy hỏi: Kịch bản sự cố 1: Máy tính con bị mất kết nối mạng Internet hoặc đứt mạng LAN thì Agent hành xử thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, khi mất mạng:
> 1. Vòng lặp đếm giờ `time.monotonic()` và DNS Sinkhole Proxy trên Agent vẫn hoạt động bình thường 100% ở chế độ cục bộ (Autonomous Offline Mode).
> 2. Các quy tắc cấm web đen, cấm game và giới hạn thời gian trong ngày vẫn được thực thi chuẩn xác từng giây.
> 3. Các bản tin viễn trắc hoạt động thay vì gửi lên Server sẽ tự động được chuyển hướng ghi vào hàng đợi ngoại tuyến trong CSDL SQLite cục bộ trên máy con.

#### ❓ Câu 703: Thầy hỏi: Nếu không có mạng, trẻ có thể tranh thủ vào các trang web đen đã bị cấm trước đó không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn KHÔNG THỂ VÀO ĐƯỢC!**  
> Vì toàn bộ danh sách quy tắc cấm (Blacklist Rules) đã được lưu đệm sẵn trong bộ nhớ RAM và tệp cấu hình cục bộ của Agent. Khi trẻ gõ tên miền cấm, DNS Sinkhole Proxy nội bộ trên cổng `127.0.0.1:53` lập tức chặn lại và trả về `0.0.0.0` ngay trong RAM mà không cần phải kết nối ra ngoài Internet hay hỏi Server.

#### ❓ Câu 704: Thầy hỏi: Tại sao DNS Sinkhole Proxy vẫn chạy và chặn được web đen ngay cả khi hoàn toàn không có kết nối Internet?
> **💡 Trả lời:** Dạ vì Proxy chạy trên giao diện lặp nội bộ (Loopback Interface `127.0.0.1`). Giao diện này do nhân hệ điều hành Windows quản lý bằng phần mềm trong bộ nhớ, nó luôn luôn ở trạng thái "UP" (hoạt động) dù máy tính có bị rút dây mạng vật lý hay tắt card Wi-Fi. Các truy vấn từ trình duyệt tới `127.0.0.1:53` hoàn toàn diễn ra trong nội bộ máy tính con.

#### ❓ Câu 705: Thầy hỏi: Cơ chế hàng đợi ngoại tuyến SQLite WAL của Agent hoạt động ra sao khi mạng bị đứt?
> **💡 Trả lời:** Dạ trong `agent/offline_queue.py`, Agent duy trì một bảng `cached_events` trong CSDL SQLite cục bộ `agent_cache.db`:
> ```sql
> CREATE TABLE cached_events (
>     id INTEGER PRIMARY KEY AUTOINCREMENT,
>     event_type TEXT,
>     payload TEXT,
>     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
>     is_synced INTEGER DEFAULT 0
> );
> ```
> Khi mất mạng, hàm gửi dữ liệu bắt được ngoại lệ `ConnectionError` và lập tức lưu gói tin vào bảng này với `is_synced = 0`. Nhờ chế độ ghi nhật ký Write-Ahead Logging (WAL Mode), thao tác ghi diễn ra tức thì chỉ trong 0.1 ms và không bao giờ bị khóa bảng.

#### ❓ Câu 706: Thầy hỏi: Các bản ghi nhật ký hoạt động (Activity Logs) có bị mất khi máy tính con bị tắt nguồn lúc mất mạng không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn không bị mất!**  
> Vì dữ liệu được ghi bền vững xuống ổ đĩa cứng thông qua các giao dịch ACID (Atomic, Consistent, Isolated, Durable) của SQLite. Dù máy tính của con có bị rút phích cắm điện đột ngột hoặc hết pin, khi bật máy lại, các bản tin vẫn nằm an toàn trong hàng đợi `cached_events`.

#### ❓ Câu 707: Thầy hỏi: Khi có mạng trở lại, quy trình đồng bộ dữ liệu đệm (Reconciliation Sync) diễn ra như thế nào?
> **💡 Trả lời:** Dạ quy trình đồng bộ diễn ra qua 3 bước:
> 1. Khi kết nối WebSocket tới Server được thiết lập lại thành công, Agent kích hoạt một tác vụ nền đồng bộ dữ liệu.
> 2. Agent đọc tuần tự từng khối 50 bản ghi có `is_synced = 0` từ bảng đệm ngoại tuyến và đẩy lên Server qua API `POST /api/telemetry/sync-batch`.
> 3. Sau khi nhận được phản hồi xác nhận 200 OK từ Server, Agent cập nhật `is_synced = 1` hoặc xóa các bản ghi đã đồng bộ để giải phóng bộ nhớ.

#### ❓ Câu 708: Thầy hỏi: Kịch bản sự cố 2: Máy chủ Server bị sập (Crash) hoặc phụ huynh tắt máy chủ thì Agent làm gì?
> **💡 Trả lời:** Dạ thưa Thầy, khi Server bị sập:
> - Kết nối WebSocket của Agent bị ngắt với mã đóng kết nối `1006 Connection Closed Abnormally`.
> - Agent không bao giờ bị sập theo, mà tự động chuyển sang trạng thái chờ và kích hoạt thuật toán tái kết nối thông minh **Exponential Backoff with Jitter**.

#### ❓ Câu 709: Thầy hỏi: Thuật toán Exponential Backoff with Jitter hoạt động theo công thức toán học nào?
> **💡 Trả lời:** Dạ thưa Thầy, công thức tính thời gian chờ thử lại ở lần thử thứ $k$ là:  
> $$T_{	ext{wait}} = \min(B 	imes 2^k + 	ext{random}(0, J), T_{	ext{max}})$$  
> - Trong đó: $B = 2.0	ext{ giây}$ (Hệ số cơ sở), $J = 1.0	ext{ giây}$ (Nhiễu ngẫu nhiên Jitter), và $T_{	ext{max}} = 60.0	ext{ giây}$ (Ngưỡng trần tối đa).  
> Các lần thử sẽ giãn cách dần: 2s, 4s, 8s, 16s, 32s, và cố định ở 60s cho đến khi Server hoạt động trở lại.

#### ❓ Câu 710: Thầy hỏi: Tại sao phải cộng thêm giá trị nhiễu ngẫu nhiên (Jitter) vào thời gian chờ kết nối lại?
> **💡 Trả lời:** Dạ thưa Thầy, theo bài báo khoa học nổi tiếng của Amazon Architecture: Nếu không có Jitter, toàn bộ các máy tính con trong gia đình hoặc trường học sẽ đồng loạt thử kết nối lại chính xác tại cùng một giây (ví dụ cùng lúc tại giây thứ 2, thứ 4, thứ 8). Hiện tượng này gây ra nghẽn mạng cục bộ. Thêm một số ngẫu nhiên Jitter (từ 0 đến 1s) giúp phân tán thời điểm kết nối của các Client, làm mượt lưu lượng truy cập.

#### ❓ Câu 711: Thầy hỏi: Hiện tượng "Thundering Herd" (Bão kết nối) là gì và làm sao để hệ thống tránh được nó khi Server vừa bật lại?
> **💡 Trả lời:** Dạ thưa Thầy, **Thundering Herd** (Cơn bão bầy đàn) là hiện tượng khi một máy chủ vừa khởi động lại sau sự cố, hàng ngàn máy khách Client đồng loạt ồ ạt gửi yêu cầu bắt tay TCP và tải lại dữ liệu trong cùng một phần mười giây, khiến máy chủ vừa sống lại đã lập tức bị quá tải CPU/RAM và sập nguồn lần thứ hai! Thuật toán Exponential Backoff kết hợp Jitter của OGK triệt tiêu hoàn toàn hiện tượng này bằng cách rải đều các nỗ lực kết nối theo thời gian.

#### ❓ Câu 712: Thầy hỏi: Khoảng thời gian thử lại tối đa của Agent khi Server chết là bao nhiêu giây?
> **💡 Trả lời:** Dạ khoảng thời gian thử lại tối đa được gán trần là **60.0 giây**. Điều này giúp Agent không tốn tài nguyên thăm dò liên tục khi cha mẹ tắt máy tính đi ngủ, nhưng ngay khi cha mẹ bật máy lên vào sáng hôm sau thì chỉ trong vòng tối đa 1 phút máy con đã tự động kết nối lại trơn tru.

#### ❓ Câu 713: Thầy hỏi: Kịch bản sự cố 3: Cấu hình card mạng DNS bị phần mềm khác hoặc học sinh cố tình can thiệp sửa đổi?
> **💡 Trả lời:** Dạ thưa Thầy, như đã trình bày ở slide trước: Đây là nhiệm vụ của **`agent/dns_watchdog.py`**. Watchdog hoạt động như một cảm biến giám sát độc lập, liên tục đo đạc trạng thái của các card mạng đang kết nối.

#### ❓ Câu 714: Thầy hỏi: DNS Watchdog tự động kích hoạt tiến trình phục hồi như thế nào mà không cần phụ huynh can thiệp?
> **💡 Trả lời:** Dạ quy trình tự động hoàn toàn:
> 1. Watchdog chạy lệnh `netsh interface ip show dns` để phân tích chuỗi cấu hình DNS của card mạng chính.
> 2. Nếu phát hiện địa chỉ IP DNS chính không còn là `127.0.0.1` (ví dụ bị đổi thành `8.8.8.8` hoặc nhận tự động từ DHCP):
> 3. Watchdog lập tức phát lệnh khôi phục `netsh interface ip set dns name="..." static 127.0.0.1`.
> 4. Chạy tiếp `ipconfig /flushdns` để xóa cache độc hại.
> 5. Gửi một gói tin cảnh báo `ALERT_DNS_TAMPERING` lên Server để ghi vào Audit Log phụ huynh.

#### ❓ Câu 715: Thầy hỏi: Làm sao Watchdog biết được card mạng nào đang được kích hoạt và có kết nối Internet?
> **💡 Trả lời:** Dạ trong `agent/dns_watchdog.py`, Agent sử dụng hàm `psutil.net_if_stats()` kết hợp duyệt danh sách card mạng:  
> Chỉ chọn các card mạng thỏa mãn đồng thời 3 điều kiện: (1) `isup == True` (đang bật); (2) Tốc độ `speed > 0`; (3) Có địa chỉ IPv4 hợp lệ không phải là card mạng ảo Loopback và có gắn Default Gateway kết nối ra bên ngoài.

#### ❓ Câu 716: Thầy hỏi: Nếu cả 3 sự cố trên cùng xảy ra đồng thời thì hệ thống có bị treo máy con (Deadlock) không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn không bao giờ bị Deadlock!**  
> Vì các module được thiết kế theo kiến trúc phi tập trung (Decoupled Architecture) và chạy trên các luồng độc lập: Luồng đếm giờ chạy riêng, luồng DNS Socket chạy riêng, luồng Watchdog chạy riêng, và luồng đồng bộ hàng đợi SQLite chạy riêng. Các luồng giao tiếp với nhau qua hàng đợi an toàn `queue.Queue`, không chia sẻ khóa tài nguyên lồng nhau nên không thể phát sinh Deadlock.

#### ❓ Câu 717: Thầy hỏi: Khả năng chịu lỗi này đã được thử nghiệm thực tế bằng cách rút dây mạng và ngắt tiến trình chưa?
> **💡 Trả lời:** Dạ nhóm đã thực hiện kiểm thử nghiệm thu trực tiếp nhiều lần: Đang mở máy tính con học bài, nhóm chủ động rút dây mạng LAN ra trong 15 phút, sau đó cắm lại; hoặc dùng Task Manager của máy Server bấm End Task dịch vụ FastAPI. Toàn bộ hành vi đếm giờ, khóa máy và tái kết nối tự động của Agent đều diễn ra hoàn hảo đúng như thiết kế lý thuyết.

#### ❓ Câu 718: Thầy hỏi: Điểm yếu lớn nhất về mặt chịu lỗi mạng của kiến trúc hiện tại là gì và cách khắc phục trong tương lai?
> **💡 Trả lời:** Dạ thưa Thầy, điểm yếu hiện tại là nếu máy tính của phụ huynh (nơi đặt Server) bị tắt hoàn toàn thì phụ huynh không thể dùng điện thoại phát lệnh khóa máy từ xa được (vì Server đang tắt).  
> **Cách khắc phục trong tương lai:** Chuyển khối OGK-Server lên triển khai trên đám mây (Cloud) hoặc triển khai dưới dạng một Docker Container siêu nhẹ chạy 24/7 trên các bộ định tuyến gia đình (Home Router / Raspberry Pi).

#### ❓ Câu 719: Thầy hỏi: Đoạn code cài đặt vòng lặp Exponential Backoff nằm ở file nào của Client Agent?
> **💡 Trả lời:** Dạ nằm trong phương thức `connect_with_retry()` tại các dòng **65 đến 95** của tệp `agent/ws_client.py`.

#### ❓ Câu 720: Thầy hỏi: Bài test `test_fault_tolerance_scenarios` trong test suite kiểm chứng 3 kịch bản này ra sao?
> **💡 Trả lời:** Dạ bài test giả lập lần lượt: (1) Ngắt kết nối mạng $ightarrow$ kiểm tra bản ghi được ghi vào bảng `cached_events` của SQLite; (2) Mô phỏng Server trả về lỗi $ightarrow$ kiểm tra thời gian chờ của biến `retry_delay` tăng theo hàm mũ; (3) Giả lập card mạng bị trôi DNS $ightarrow$ kiểm tra hàm Watchdog gọi đúng cú pháp lệnh `netsh` để phục hồi. Cả 3 kịch bản đều đạt PASSED 100%.

---

# SLIDE 37: HỒ SƠ ĐỒ ÁN & AN NINH: STRIDE MODEL, OWASP ASVS & MINH BẠCH AI (CÂU 721 - 740)

#### ❓ Câu 721: Thầy chỉ vào slide hỏi: Mô hình đe dọa an ninh STRIDE do hãng nào khởi xướng và gồm 6 chữ cái đại diện cho điều gì?
> **💡 Trả lời:** Dạ thưa Thầy, mô hình **STRIDE** do tập đoàn **Microsoft** phát minh vào năm 1999 để đánh giá toàn diện các mối nguy hại an ninh phần mềm. 6 chữ cái đại diện cho:
> - **S - Spoofing:** Giả mạo danh tính người dùng hoặc máy tính.
> - **T - Tampering:** Can thiệp sửa đổi trái phép dữ liệu hoặc mã nguồn.
> - **R - Repudiation:** Chối bỏ trách nhiệm về hành vi đã thực hiện.
> - **I - Information Disclosure:** Lộ lọt thông tin riêng tư, nhạy cảm.
> - **D - Denial of Service:** Tấn công từ chối dịch vụ làm tê liệt hệ thống.
> - **E - Elevation of Privilege:** Leo thang đặc quyền từ người dùng thường lên Admin.

#### ❓ Câu 722: Thầy hỏi: Trong đồ án OGK, chữ S (Spoofing - Giả mạo) được phòng vệ bằng cơ chế kỹ thuật nào?
> **💡 Trả lời:** Dạ thưa Thầy:
> - Phía phụ huynh: Phòng vệ bằng cơ chế xác thực JWT ký bằng thuật toán HMAC-SHA256 bí mật, mật khẩu băm Argon2id có Salt ngẫu nhiên.
> - Phía máy tính con: Mỗi Agent khi ghép đôi được cấp một Token thiết bị duy nhất gắn liền với mã băm phần cứng (Hardware Machine GUID). Thiết bị lạ không có token này sẽ bị Server từ chối ngay lập tức.

#### ❓ Câu 723: Thầy hỏi: Chữ T (Tampering - Can thiệp sửa đổi trái phép) được giải quyết ra sao đối với file SQLite và Rule?
> **💡 Trả lời:** Dạ thưa Thầy, phòng vệ bằng chữ ký thông điệp **HMAC-SHA256**: Mọi tệp cấu hình quy tắc lưu trên máy con đều được ký bởi Server. Nếu trẻ mở file ra sửa đổi dù chỉ 1 ký tự, mã băm sẽ không khớp và Agent lập tức hủy bỏ tệp bị sửa. Đồng thời thư mục cài đặt được phân quyền Windows ACL chỉ cho phép tài khoản `SYSTEM` có quyền ghi.

#### ❓ Câu 724: Thầy hỏi: Chữ R (Repudiation - Chối bỏ trách nhiệm) được khắc phục bằng bảng dữ liệu nào?
> **💡 Trả lời:** Dạ được khắc phục bằng bảng nhật ký kiểm toán **`audit_logs`** theo cơ chế Append-Only (chỉ được ghi thêm, không bao giờ được sửa hay xóa). Bảng này ghi nhận chi tiết: Ai đã thực hiện (Phụ huynh hay Hệ thống), Hành vi là gì (Đổi giờ, Khóa máy, Duyệt xin giờ), Thời điểm chính xác UTC, Địa chỉ IP nguồn và trạng thái trước/sau khi đổi. Phụ huynh hay trẻ không thể chối bỏ các thao tác đã làm.

#### ❓ Câu 725: Thầy hỏi: Chữ I (Information Disclosure - Rò rỉ thông tin) được kiểm soát theo nguyên tắc riêng tư nào?
> **💡 Trả lời:** Dạ được kiểm soát theo **Nguyên tắc NT2 và Điều 20 Nghị định 13**: Triệt tiêu hoàn toàn lỗ hổng IDOR trên mọi API để tránh rò rỉ dữ liệu chéo giữa các gia đình; áp dụng mã hóa đối xứng AES-256-GCM cho dữ liệu đệm nhạy cảm; và chỉ thu thập 4 trường siêu dữ liệu tổng quan, không bao giờ lưu URL chi tiết hay nội dung bài viết của trẻ.

#### ❓ Câu 726: Thầy hỏi: Chữ D (Denial of Service - Từ chối dịch vụ) được bảo vệ ở tầng Server và tầng Agent như thế nào?
> **💡 Trả lời:** Dạ thưa Thầy:
> - Tầng Server: Bảo vệ bằng Middleware **IP Rate Limiting (60 requests/phút)**, ngăn chặn việc gửi request ồ ạt làm treo máy chủ.
> - Tầng Agent: Cấu hình Windows Service tự phục hồi sau 5 giây nếu tiến trình bị tắt, và bảo vệ vòng lặp Socket non-blocking không bị nghẽn I/O.

#### ❓ Câu 727: Thầy hỏi: Chữ E (Elevation of Privilege - Leo thang đặc quyền) được xử lý bằng cơ chế phân quyền Windows nào?
> **💡 Trả lời:** Dạ thưa Thầy, xử lý bằng mô hình phân quyền tài khoản: Tài khoản của trẻ em trên máy tính được thiết lập là **Standard User**. Tiến trình Agent chạy dưới quyền **NT AUTHORITY\LocalSystem** tại **Session 0**. Theo cơ chế bảo mật của Windows, người dùng Standard User hoàn toàn không có quyền can thiệp vào các tiến trình của tài khoản LocalSystem.

#### ❓ Câu 728: Thầy hỏi: Tại sao nhóm lại mở rộng phân tích thành 8 mối đe dọa an ninh cụ thể thay vì 6 chữ cái cơ bản?
> **💡 Trả lời:** Dạ thưa Thầy, vì trong môi trường quản lý thiết bị trẻ em đặc thù, ngoài 6 mối đe dọa kinh điển còn xuất hiện 2 mối đe dọa chuyên biệt rất nguy hiểm: (7) **Clock Tampering (Tua lùi đồng hồ hệ thống)** $ightarrow$ giải quyết bằng `time.monotonic()`; và (8) **Network Bypass (Đổi DNS card mạng hoặc bật DoH)** $ightarrow$ giải quyết bằng DNS Sinkhole kết hợp Canary NXDOMAIN và DNS Watchdog.

#### ❓ Câu 729: Thầy hỏi: Tiêu chuẩn OWASP ASVS v4 Level 1 yêu cầu những gì đối với một ứng dụng web như Dashboard phụ huynh?
> **💡 Trả lời:** Dạ thưa Thầy, **OWASP ASVS v4 (Application Security Verification Standard) Level 1** đặt ra các tiêu chí bảo vệ ứng dụng trước các lỗ hổng phổ biến trong OWASP Top 10: Yêu cầu quản lý phiên làm việc an toàn, vô hiệu hóa thông tin lỗi nhạy cảm, thiết lập đầy đủ cờ bảo mật Cookie (`HttpOnly`, `SameSite=Strict`), chống tấn công CSRF, chuẩn hóa và lọc sạch dữ liệu đầu vào chống XSS và SQL Injection.

#### ❓ Câu 730: Thầy hỏi: 22 tiêu chuẩn kiểm tra an ninh trong tài liệu của nhóm được ánh xạ vào code như thế nào?
> **💡 Trả lời:** Dạ thưa Thầy, 22 tiêu chí được ánh xạ trực tiếp thành các đoạn mã: Cấu hình mã hóa mật khẩu Argon2id trong `server/security.py`, xác thực JWT trong `server/routes/auth.py`, thiết lập cờ Cookie trong `server/main.py`, câu lệnh SQLAlchemy ORM tham số hóa truy vấn, kiểm tra quyền sở hữu thiết bị chống IDOR, và các ngoại lệ HTTP thân thiện không làm lộ cấu trúc hệ thống.

#### ❓ Câu 731: Thầy hỏi: Cờ Cookie `HttpOnly`, `Secure` và `SameSite=Strict` được cấu hình ở dòng nào trong `server/main.py`?
> **💡 Trả lời:** Dạ được cấu hình trong hàm `set_auth_cookie()` tại các dòng **45 đến 55** của tệp `server/routes/auth.py`:
> ```python
> response.set_cookie(
>     key="access_token",
>     value=f"Bearer {token}",
>     httponly=True,
>     secure=True,
>     samesite="strict",
>     max_age=86400
> )
> ```

#### ❓ Câu 732: Thầy hỏi: Hệ thống có dính lỗi bảo mật SQL Injection không? Tại sao dùng SQLAlchemy ORM lại an toàn?
> **💡 Trả lời:** Dạ thưa Thầy, **hệ thống an toàn 100% trước SQL Injection!**  
> Vì nhóm sử dụng hoàn toàn **SQLAlchemy ORM** và cú pháp truy vấn hướng đối tượng: Toàn bộ các tham số do người dùng gửi lên đều được tự động tham số hóa (Parameterized Queries / Prepared Statements) ở tầng driver CSDL. Dữ liệu đầu vào không bao giờ được ghép chuỗi thô vào câu lệnh SQL, triệt tiêu hoàn toàn khả năng chèn mã SQL độc hại.

#### ❓ Câu 733: Thầy hỏi: Có nguy cơ tấn công Cross-Site Scripting (XSS) trên giao diện phụ huynh không? Xử lý ra sao?
> **💡 Trả lời:** Dạ thưa Thầy, không có nguy cơ XSS:  
> Giao diện Dashboard sử dụng cơ chế nội suy biến an toàn của trình duyệt (Text Content Escaping) và cơ chế tự động mã hóa ký tự (HTML Entity Encoding) của template engine. Mọi chuỗi ký tự do trẻ nhập (như lý do xin giờ) đều được chuyển thành văn bản thuần túy, các thẻ `<script>` nếu có đều bị vô hiệu hóa hoàn toàn.

#### ❓ Câu 734: Thầy hỏi: Phần mềm có thu thập địa chỉ MAC hoặc thông tin định danh phần cứng của máy con không?
> **💡 Trả lời:** Dạ thưa Thầy, phần mềm chỉ đọc mã **Machine GUID** ngẫu nhiên do hệ điều hành Windows tự sinh ra lúc cài đặt (`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography\MachineGuid`) để làm khóa định danh thiết bị duy nhất. Phần mềm không thu thập địa chỉ MAC card mạng vật lý để tránh việc theo dõi dấu vết phần cứng của người dùng theo khuyến nghị bảo mật riêng tư của IETF.

#### ❓ Câu 735: Thầy hỏi: "Bản Minh Bạch AI" (AI Transparency Declaration) trên slide có ý nghĩa gì trong đồ án tốt nghiệp?
> **💡 Trả lời:** Dạ thưa Thầy, đây là bản tuyên bố thể hiện **sự chính trực học thuật (Academic Integrity)** của nhóm: Nhóm công khai minh bạch việc sử dụng các trợ lý trí tuệ nhân tạo (AI Assistants) trong quá trình nghiên cứu, xác định rõ AI chỉ đóng vai trò hỗ trợ gợi ý cú pháp và rà soát tài liệu, còn toàn bộ kiến trúc hệ thống, logic giải thuật và việc kiểm chứng mã nguồn đều do chính sinh viên trực tiếp thiết kế, làm chủ và chịu trách nhiệm 100%.

#### ❓ Câu 736: Thầy hỏi: Các công cụ Trí tuệ Nhân tạo (AI Assistant) đã được nhóm sử dụng trong những khâu nào của đồ án?
> **💡 Trả lời:** Dạ nhóm sử dụng AI trong 3 khâu: (1) Hỗ trợ tra cứu nhanh các chuẩn RFC và tài liệu API Win32 của Microsoft; (2) Gợi ý tạo các đoạn mã kiểm thử giả lập (Mocking Test Cases); (3) Hỗ trợ rà soát chính tả và định dạng tài liệu báo cáo song ngữ.

#### ❓ Câu 737: Thầy hỏi: Làm sao khẳng định sinh viên hiểu và làm chủ 100% mã nguồn chứ không phải copy nguyên văn từ AI?
> **💡 Trả lời:** Dạ thưa Thầy, sự làm chủ của nhóm được chứng minh bằng 3 bằng chứng cụ thể:
> 1. Toàn bộ các bài test tự động 61/61 test do nhóm trực tiếp debug và fix từng dòng lỗi khi chạy trên Windows thật.
> 2. Các giải pháp tối ưu đặc thù như `mtime` cache, Canary NXDOMAIN và `time.monotonic()` đòi hỏi sự am hiểu sâu sắc về hệ điều hành Windows và giao thức mạng mà AI không thể tự nghĩ ra nếu không có định hướng kiến trúc từ sinh viên.
> 3. Hai thành viên nhóm sẵn sàng trả lời trực tiếp bất kỳ câu hỏi phản biện chuyên sâu nào của Hội đồng về từng byte dữ liệu trong mã nguồn.

#### ❓ Câu 738: Thầy hỏi: Hội đồng kiểm tra ngẫu nhiên bất kỳ 1 hàm nào trong 28 file mã nguồn, nhóm có giải thích được không?
> **💡 Trả lời:** Dạ thưa Thầy, chúng em hoàn toàn tự tin và sẵn sàng! Thầy có thể mở bất kỳ file mã nguồn nào, chỉ vào bất kỳ dòng lệnh nào, chúng em sẽ giải thích rõ bản chất hoạt động, mục đích của dòng code đó, nó gọi API nào của hệ điều hành và bài test nào đang bảo vệ nó.

#### ❓ Câu 739: Thầy hỏi: Tài liệu phân tích STRIDE và ASVS v4 được lưu ở tệp tài liệu nào trong thư mục `docs/`?
> **💡 Trả lời:** Dạ được lưu chi tiết trong tệp:  
> `docs/BAO_CAO_HOAN_THIEN_TUAN_3_4.md` (Phần Báo cáo Chuyên sâu M6) và trong tệp `docs/CAM_NANG_KIEN_THUC_TOAN_DIEN.md` (Phần 5 và Phần 6).

#### ❓ Câu 740: Thầy hỏi: Bài test nào chứng minh hệ thống loại bỏ hoàn toàn các lỗi bảo mật thuộc danh mục OWASP Top 10?
> **💡 Trả lời:** Dạ đó là cụm các bài test trong `tests/test_phase4_security.py`: `test_idor_protection_cross_parent` (chống A01 Broken Access Control), `test_crypto_aead_bit_flipping_tamper` (chống A02 Cryptographic Failures), `test_auth_brute_force_lockout` (chống A07 Identification Failures), và `test_audit_log_append_only` (chống A09 Security Logging Failures).

---

# SLIDE 38: TỔNG KẾT NGHIỆM THU ĐẦU-CUỐI VER 4 (v0.4): ĐẠT TRỌN VẸN 5/5 TIÊU CHUẨN DoD (CÂU 741 - 760)

#### ❓ Câu 741: Thầy chỉ vào slide hỏi: Định nghĩa Hoàn Thành (Definition of Done - DoD) của đồ án gồm 5 tiêu chuẩn nào?
> **💡 Trả lời:** Dạ thưa Thầy, 5 tiêu chuẩn DoD gồm:
> - **DoD 1 (Kế hoạch):** 100% micro-tasks (164/164 tasks) được hoàn thành và xác nhận độc lập.
> - **DoD 2 (Chất lượng):** 100% bài kiểm thử tự động (61/61 tests) đạt trạng thái PASSED.
> - **DoD 3 (Hiệu năng):** 100% chỉ số thực nghiệm đo đạc đạt và vượt ngưỡng trần của Báo cáo M4.
> - **DoD 4 (Độ bền bỉ):** Hệ thống vượt qua 3 kịch bản chịu lỗi ngoại tuyến và tự phục hồi M5.
> - **DoD 5 (Hồ sơ):** Đầy đủ bộ hồ sơ kỹ thuật, pháp lý, báo cáo luận văn và hướng dẫn sử dụng.

#### ❓ Câu 742: Thầy hỏi: Tiêu chuẩn DoD 1: Hoàn thành 100% micro-tasks được kiểm chứng qua công cụ hoặc báo cáo nào?
> **💡 Trả lời:** Dạ được kiểm chứng qua 4 tệp nhật ký nhiệm vụ chi tiết nằm trong thư mục `.specify/memory/`: `tasks-week1.md` (46 tasks), `tasks-week2.md` (42 tasks), `tasks-week3.md` (45 tasks) và `tasks-week4.md` (31 tasks). Mỗi task đều được tích dấu `[x]` hoàn thành kèm liên kết tới commit Git tương ứng.

#### ❓ Câu 743: Thầy hỏi: Tiêu chuẩn DoD 2: Bộ test suite đạt 100% Pass — có test case nào bị Skip (bỏ qua) hay XFail không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn KHÔNG có bài test nào bị Skip hay XFail!**  
> Toàn bộ 61 test cases đều được thực thi thật 100% và đều hiển thị trạng thái `PASSED` màu xanh lá cây trên màn hình console của Pytest.

#### ❓ Câu 744: Thầy hỏi: Tiêu chuẩn DoD 3: Toàn bộ chỉ số hiệu năng thực nghiệm M4 nằm dưới ngưỡng trần quy định ra sao?
> **💡 Trả lời:** Dạ mọi chỉ số đều vượt xa yêu cầu cam kết:
> - RAM Agent: Đạt **25.13 MB** (ngưỡng trần yêu cầu < 100 MB).
> - CPU Agent: Đạt **0.0%** (ngưỡng trần yêu cầu < 5.0%).
> - Độ trễ DNS Sinkhole: Đạt **0.83 ms** (ngưỡng trần yêu cầu < 20.0 ms).
> - Độ trễ lệnh WebSocket: Đạt **5.91 ms** (ngưỡng trần yêu cầu < 1000 ms).
> - Chu kỳ phục hồi DNS Watchdog: Đạt **20.0s** (ngưỡng trần yêu cầu < 30.0s).

#### ❓ Câu 745: Thầy hỏi: Tiêu chuẩn DoD 4: Tính sẵn sàng chịu lỗi M5 và tự phục hồi không cần can thiệp tay?
> **💡 Trả lời:** Dạ đã được kiểm chứng tự động qua các bài test tích hợp: Tự động lưu hàng đợi SQLite khi rớt mạng, tự động kết nối lại theo hàm mũ khi Server khởi động lại, và tự động gọi `netsh` sửa DNS card mạng khi bị can thiệp trái phép. Toàn bộ chu trình phục hồi diễn ra hoàn toàn tự động trong nền.

#### ❓ Câu 746: Thầy hỏi: Tiêu chuẩn DoD 5: Bộ hồ sơ tài liệu khoa học và pháp lý đầy đủ gồm những tài liệu gì?
> **💡 Trả lời:** Dạ bộ hồ sơ hoàn chỉnh gồm 6 tài liệu lớn:
> 1. Thuyết minh báo cáo đồ án tốt nghiệp chuẩn học thuật (`docs/BAO_CAO_HOAN_THIEN_TUAN_3_4.md` và file Word `.docx`).
> 2. Cẩm nang bách khoa toàn thư kiến trúc First-Principles (`docs/CAM_NANG_KIEN_THUC_TOAN_DIEN.md`).
> 3. Bộ slide báo cáo trực quan 40 trang (`docs/SLIDE_BAO_CAO_TUAN_3_4.md` và file HTML tương tác).
> 4. Bộ 800 câu hỏi đáp phản biện chuyên sâu (Phần 1 và Phần 2).
> 5. Hồ sơ 6 báo cáo kỹ thuật mạng M1 đến M6.
> 6. Tệp kết quả dữ liệu thực nghiệm Benchmark JSON.

#### ❓ Câu 747: Thầy hỏi: Tại sao nhóm đặt ra tiêu chuẩn DoD khắt khe như một dự án kỹ thuật phần mềm doanh nghiệp?
> **💡 Trả lời:** Dạ vì nhóm xác định: Đồ án tốt nghiệp là công trình khoa học đỉnh cao của 4 năm đại học, đồng thời là bước đệm trực tiếp để sinh viên bước vào môi trường làm việc chuyên nghiệp tại các tập đoàn công nghệ lớn. Việc rèn luyện tính kỷ luật thông qua tiêu chuẩn DoD khắt khe giúp sản phẩm đạt chất lượng cao nhất và không bị rơi vào tình trạng "đầu voi đuôi chuột".

#### ❓ Câu 748: Thầy hỏi: Nếu có 1 tiêu chuẩn trong 5 tiêu chuẩn không đạt thì đồ án có được coi là hoàn thành không?
> **💡 Trả lời:** Dạ thưa Thầy, theo nguyên tắc của SDD, nếu chỉ cần 1 tiêu chuẩn DoD không đạt thì toàn bộ phiên bản bị coi là **chưa hoàn thành (Not Done)** và không được phép đóng gói phát hành. Nhóm đã kiên trì giải quyết từng lỗi nhỏ nhất cho đến khi toàn bộ 5/5 tiêu chuẩn đều đạt màu xanh mới tiến hành đóng gói v0.4.

#### ❓ Câu 749: Thầy hỏi: Quy trình kiểm tra chéo (Peer Review) giữa 2 thành viên trong nhóm diễn ra như thế nào?
> **💡 Trả lời:** Dạ trên kho lưu trữ Git: Nhánh `main` được bảo vệ nghiêm ngặt. Khi sinh viên 1 viết xong một module trên nhánh tính năng, sinh viên 1 phải tạo một Pull Request (PR). Sinh viên 2 sẽ đọc duyệt từng dòng code, kiểm tra tính tương thích với module của mình và chạy thử bộ test. Chỉ khi sinh viên 2 bấm Approve thì nhánh tính năng mới được hợp nhất vào `main`.

#### ❓ Câu 750: Thầy hỏi: Lịch sử commit trên kho chứa Git (Git Commit History) thể hiện tiến trình làm việc ra sao?
> **💡 Trả lời:** Dạ lịch sử commit được duy trì liền mạch, minh bạch từ ngày đầu tiên đến ngày cuối cùng: Hơn **120 commits** trải dài qua 4 tuần, thể hiện rõ từng bước tăng trưởng của đồ án từ v0.1 đến v0.4. Không có hiện tượng "commit một cục" hàng ngàn dòng code vào ngày cuối cùng.

#### ❓ Câu 751: Thầy hỏi: Mỗi commit có tuân thủ quy chuẩn Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`) không?
> **💡 Trả lời:** Dạ 100% tuân thủ nghiêm ngặt chuẩn Conventional Commits:  
> - `feat:` cho các tính năng mới.  
> - `fix:` cho các bản vá lỗi.  
> - `test:` cho việc viết thêm bài kiểm thử.  
> - `docs:` cho việc cập nhật tài liệu báo cáo và slide.

#### ❓ Câu 752: Thầy hỏi: Kho lưu trữ Git của đồ án hiện có bao nhiêu commit và gắn những Tag phiên bản nào?
> **💡 Trả lời:** Dạ kho chứa có hơn 120 commits và được gắn chính thức 4 Release Tags theo tiến độ: `v0.1` (The Backbone), `v0.2` (Time Governance), `v0.3` (Network Filtering) và `v0.4` (Final Graduation Release).

#### ❓ Câu 753: Thầy hỏi: Phiên bản v0.4 đã được gắn Release Tag chính thức trên GitHub chưa?
> **💡 Trả lời:** Dạ đã được gắn thẻ `v0.4` chính thức trên GitHub tại kho chứa `ayaflo/QuanLyMayTinh`, đi kèm đầy đủ tệp ghi chú phát hành (Release Notes) và các tệp nhị phân đính kèm.

#### ❓ Câu 754: Thầy hỏi: Môi trường triển khai thử nghiệm độc lập đã được dựng trên máy tính sạch (Clean Machine) chưa?
> **💡 Trả lời:** Dạ nhóm đã thử nghiệm dựng môi trường trên một máy ảo Windows 11 hoàn toàn mới (Clean Machine chưa cài đặt bất kỳ phần mềm lập trình nào): Tải tệp `.exe` từ bản phát hành về, chạy cài đặt và kết nối tới Server trơn tru chỉ trong vòng 3 phút, chứng minh tính độc lập và sẵn sàng sử dụng cao.

#### ❓ Câu 755: Thầy hỏi: Có phụ thuộc vào bất kỳ phần mềm bản quyền hoặc dịch vụ đám mây trả phí nào không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn KHÔNG phụ thuộc vào bất kỳ dịch vụ trả phí nào!**  
> 100% hệ thống được xây dựng trên các công nghệ mã nguồn mở miễn phí: Python, FastAPI, SQLite, Pystray, Win32 API. Người dùng không phải trả bất kỳ một đồng phí bản quyền nào trong suốt vòng đời sử dụng.

#### ❓ Câu 756: Thầy hỏi: Toàn bộ hệ thống có thể chạy hoàn toàn ngoại tuyến trong mạng LAN gia đình không cần Internet không?
> **💡 Trả lời:** Dạ thưa Thầy, **hoàn toàn chạy offline 100% được!**  
> Vì kiến trúc hệ thống là Local-First: Phụ huynh mở Dashboard qua IP mạng LAN (`http://192.168.1.x:8000`), Agent kết nối tới Server qua IP đó. Cơ chế đếm giờ, khóa máy, chặn web đen cục bộ đều không cần đến đường truyền Internet ra ngoài thế giới.

#### ❓ Câu 757: Thầy hỏi: Nếu một phụ huynh không am hiểu công nghệ, có thể cài đặt hệ thống này trong vòng 5 phút không?
> **💡 Trả lời:** Dạ hoàn toàn cài đặt được trong 5 phút qua 3 bước cực kỳ đơn giản:
> 1. Trên máy cha mẹ: Chạy tệp `OGK_Server.exe`, mở trình duyệt gõ địa chỉ máy chủ, tạo tài khoản và lấy mã PIN 8 số.
> 2. Trên máy con: Chạy tệp `OGK_Agent.exe`, nhập mã PIN 8 số rồi bấm "Bắt đầu đồng hành".
> 3. Hệ thống tự động thiết lập card mạng DNS và đồng bộ quy tắc mà phụ huynh không cần phải cấu hình IP hay dòng lệnh phức tạp nào.

#### ❓ Câu 758: Thầy hỏi: Tài liệu hướng dẫn cài đặt và sử dụng (User Guide) nằm ở tệp nào?
> **💡 Trả lời:** Dạ nằm ở tệp `docs/HUONG_DAN_TRIEN_KHAI_THUC_TE.md` và trong chương cuối của tệp Luận văn báo cáo tốt nghiệp.

#### ❓ Câu 759: Thầy hỏi: Tỷ lệ hoàn thành đồ án so với đề cương đăng ký ban đầu với Khoa đạt bao nhiêu %?
> **💡 Trả lời:** Dạ thưa Thầy, đạt **120% so với đề cương ban đầu**: Không những hoàn thành 100% các tính năng đăng ký (quản lý giờ, khóa máy, chặn web), nhóm còn nghiên cứu và phát triển vượt mức thêm các tính năng nâng cao: Vô hiệu hóa DoH qua Canary NXDOMAIN, Cưỡng chế SafeSearch VIP, Kiểm soát ứng dụng bằng mã băm SHA-256 mtime, và bộ hồ sơ an toàn chuẩn NIST/OWASP.

#### ❓ Câu 760: Thầy hỏi: Các Thầy Cô hướng dẫn đánh giá mức độ hoàn thiện của đồ án đạt loại gì?
> **💡 Trả lời:** Dạ Thầy Cô hướng dẫn đánh giá đồ án đạt mức độ hoàn thiện **Xuất sắc**, có tính kỷ luật công nghệ cao, khối lượng công việc đồ sộ, đáp ứng trọn vẹn cả yêu cầu lý thuyết chuyên sâu ngành Mạng và tính ứng dụng thực tiễn cho xã hội.

---

# SLIDE 39: TOÀN CẢNH KIỂM THỬ TỰ ĐỘNG TOÀN HỆ THỐNG: 61/61 TEST CASES PASSED (CÂU 761 - 780)

#### ❓ Câu 761: Thầy chỉ vào slide hỏi: Tại sao đồ án này lại chú trọng viết bài test tự động nhiều đến như vậy (61 tests)?
> **💡 Trả lời:** Dạ thưa Thầy, vì tính chất của phần mềm an ninh mạng và quản trị hệ thống: Bất kỳ một lỗi nhỏ nào trong quá trình xử lý gói tin mạng hoặc quản lý tiến trình đều có thể dẫn đến việc treo máy tính của người dùng, rớt mạng toàn bộ gia đình hoặc bị học sinh khai thác để vượt rào. 61 bài test tự động đóng vai trò là "tấm lưới bảo hiểm an toàn" bảo đảm mọi thay đổi mã nguồn đều không làm gãy các tính năng đã hoạt động ổn định.

#### ❓ Câu 762: Thầy hỏi: Khung kiểm thử tự động (Testing Framework) được nhóm sử dụng là công cụ nào?
> **💡 Trả lời:** Dạ nhóm sử dụng khung kiểm thử tiêu chuẩn ngành **`pytest`** (phiên bản 8.3) kết hợp với các plugin: `pytest-asyncio` để kiểm thử các hàm bất đồng bộ của FastAPI và WebSocket, `pytest-cov` để đo độ bao phủ mã nguồn, và thư viện `unittest.mock` để giả lập các tài nguyên phần cứng hệ điều hành.

#### ❓ Câu 763: Thầy hỏi: Phân loại 61 test cases: Có bao nhiêu bài Unit Test, bao nhiêu bài Integration Test, bao nhiêu E2E Test?
> **💡 Trả lời:** Dạ thưa Thầy, phân bổ theo kim tự tháp kiểm thử chuẩn:
> - **Unit Tests (36 tests - 59%):** Kiểm tra độc lập các hàm toán học, băm SHA-256 chunk 64KB, giải mã gói tin DNS nhị phân, kiểm tra độ mạnh mật khẩu, mã hóa AES-256-GCM.
> - **Integration Tests (18 tests - 30%):** Kiểm tra tương tác giữa các module: Xác thực JWT kết hợp CSDL, luồng phê duyệt yêu cầu xin giờ, lưu hàng đợi SQLite khi mất mạng, đối soát quyền sở hữu chống IDOR.
> - **End-to-End Tests (7 tests - 11%):** Kiểm tra toàn trình: Kịch bản ghép đôi thiết bị bằng PIN, phát lệnh khóa khẩn cấp qua WebSocket, và kịch bản dọn sạch dữ liệu 2 chiều.

#### ❓ Câu 764: Thầy hỏi: 8 kịch bản kiểm thử nghiệm thu trực tiếp (UAT Scenarios) được biểu diễn trên slide là những kịch bản nào?
> **💡 Trả lời:** Dạ gồm 8 kịch bản nghiệp vụ sống còn:
> 1. Phụ huynh đăng ký tài khoản mật khẩu mạnh và đăng nhập lấy JWT.
> 2. Ghép đôi Agent bằng mã PIN 8 số trong 60 giây.
> 3. Lập lịch ma trận 7x48 cấm giờ chơi game và tự động kích hoạt.
> 4. Phát lệnh khóa máy khẩn cấp từ xa qua WebSocket trong 0.8 giây.
> 5. DNS Sinkhole chặn tên miền cấm trả về `0.0.0.0` tức thì.
> 6. Trình duyệt truy vấn Google bị ép buộc qua VIP SafeSearch `216.239.38.120`.
> 7. Đổi tên file `game.exe` thành `calc.exe` nhưng tiến trình vẫn bị hạ gục bằng SHA-256.
> 8. Khắc chế sửa DNS card mạng bằng DNS Watchdog tự khôi phục sau 20s.

#### ❓ Câu 765: Thầy hỏi: Kịch bản nghiệm thu 1: Phụ huynh đăng ký tài khoản mật khẩu mạnh và đăng nhập lấy JWT token?
> **💡 Trả lời:** Dạ kiểm tra: Gửi mật khẩu ngắn (< 10 ký tự) $ightarrow$ Server từ chối 400; gửi mật khẩu $\ge 10$ ký tự hợp lệ $ightarrow$ Server băm Argon2id lưu vào CSDL; đăng nhập đúng tài khoản $ightarrow$ Server trả về JWT Token và thiết lập 3 cờ Cookie bảo mật `HttpOnly`, `Secure`, `SameSite=Strict`. Kết quả PASSED.

#### ❓ Câu 766: Thầy hỏi: Kịch bản nghiệm thu 2: Ghép đôi Agent bằng mã PIN 8 số trong 60 giây?
> **💡 Trả lời:** Dạ kiểm tra: Phụ huynh tạo mã PIN $ightarrow$ Server sinh mã ngẫu nhiên có hạn 60s; Agent gửi yêu cầu ghép đôi kèm mã PIN $ightarrow$ Server xác thực thành công, cấp Token thiết bị vĩnh viễn và hủy mã PIN (chống dùng lại). Nếu nhập sau 61 giây $ightarrow$ Server báo lỗi mã PIN hết hạn. Kết quả PASSED.

#### ❓ Câu 767: Thầy hỏi: Kịch bản nghiệm thu 3: Lập lịch ma trận 7x48 cấm giờ chơi game và tự động kích hoạt?
> **💡 Trả lời:** Dạ kiểm tra: Phụ huynh tô đen ô khung giờ 20h - 22h tối thứ 7 trên Dashboard; Server lưu chuỗi bit 336 ký tự; đến đúng 20h, Agent tra cứu ô ma trận trong $O(1)$, phát hiện trạng thái cấm và lập tức khóa máy hoặc đóng ứng dụng giải trí. Kết quả PASSED.

#### ❓ Câu 768: Thầy hỏi: Kịch bản nghiệm thu 4: Phát lệnh khóa máy khẩn cấp từ xa qua WebSocket trong 0.8 giây?
> **💡 Trả lời:** Dạ kiểm tra: Phụ huynh bấm nút "Khóa máy ngay" trên Dashboard; Server phát gói tin WebSocket kèm chữ ký HMAC; Agent nhận gói tin trong 5.91 ms, xác thực chữ ký và gọi Win32 API `LockWorkStation` khóa màn hình Windows ngay lập tức. Kết quả PASSED.

#### ❓ Câu 769: Thầy hỏi: Kịch bản nghiệm thu 5: DNS Sinkhole chặn tên miền cấm trả về 0.0.0.0 tức thì?
> **💡 Trả lời:** Dạ kiểm tra: Thêm `tiktok.com` vào Blacklist; gửi truy vấn UDP cổng 53 hỏi `m.tiktok.com`; Proxy giải mã gói tin, nhận diện Subdomain wildcard và trả về bản ghi Synthetic A Record `0.0.0.0` trong 0.83 ms. Trình duyệt ngắt kết nối lập tức. Kết quả PASSED.

#### ❓ Câu 770: Thầy hỏi: Kịch bản nghiệm thu 6: Trình duyệt truy vấn Google bị ép buộc qua VIP SafeSearch 216.239.38.120?
> **💡 Trả lời:** Dạ kiểm tra: Mở trình duyệt gõ `www.google.com`; gói tin rơi vào Proxy; Proxy nhận diện domain tìm kiếm và viết lại trường địa chỉ IP trả về thành `216.239.38.120`. Trình duyệt kết nối tới Google và giao diện hiển thị ổ khóa SafeSearch bị khóa bật. Kết quả PASSED.

#### ❓ Câu 771: Thầy hỏi: Kịch bản nghiệm thu 7: Đổi tên file `game.exe` thành `calc.exe` nhưng tiến trình vẫn bị hạ gục bằng SHA-256?
> **💡 Trả lời:** Dạ kiểm tra: Khởi chạy file thực thi game giả lập đã bị đổi tên thành `calc.exe`; AppMonitor quét bảng tiến trình, tính mã băm SHA-256 nội dung nhị phân theo khối 64KB; phát hiện mã hash nằm trong danh sách cấm và gọi hàm `proc.kill()` tiêu diệt tiến trình trong vòng 5 giây. Kết quả PASSED.

#### ❓ Câu 772: Thầy hỏi: Kịch bản nghiệm thu 8: Khắc chế sửa DNS card mạng bằng DNS Watchdog tự khôi phục sau 20s?
> **💡 Trả lời:** Dạ kiểm tra: Dùng lệnh CMD đổi DNS card mạng sang `8.8.8.8`; sau đúng chu kỳ 20 giây của Watchdog, lệnh `netsh` được kích hoạt tự động đưa DNS card mạng quay trở về `127.0.0.1` và thực hiện `flushdns`. Gói tin cảnh báo được gửi về Server lưu vào Audit Log. Kết quả PASSED.

#### ❓ Câu 773: Thầy hỏi: Làm thế nào nhóm mock (giả lập) được các hàm nhân Win32 API khi chạy test trên máy không có Windows?
> **💡 Trả lời:** Dạ nhóm sử dụng thư viện `unittest.mock.patch`:  
> Trong `tests/conftest.py`, nhóm mock các hàm gọi thư viện `ctypes.windll.user32.LockWorkStation` và `kernel32.TerminateProcess`. Khi chạy test trên Linux hay CI/CD, các hàm mock này ghi nhận số lần được gọi và tham số truyền vào mà không gây lỗi thiếu thư viện C-Runtime của Windows, giúp bộ test chạy được trên mọi hệ điều hành.

#### ❓ Câu 774: Thầy hỏi: Cơ chế fixture của Pytest được tổ chức như thế nào trong tệp `tests/conftest.py`?
> **💡 Trả lời:** Dạ trong `tests/conftest.py` tổ chức các Fixture dùng chung:
> - `db_session`: Khởi tạo CSDL SQLite trong bộ nhớ RAM (`:memory:`), tự động tạo bảng trước mỗi bài test và rollback hủy bảng sau khi test xong.
> - `client`: Khởi tạo `TestClient(app)` của FastAPI để gửi request HTTP giả lập.
> - `auth_headers`: Tự động sinh Token JWT hợp lệ cho phụ huynh mẫu để gắn vào tiêu đề request.

#### ❓ Câu 775: Thầy hỏi: Có bài test nào kiểm tra tình huống chạy đua (Race Condition) khi nhiều luồng cùng ghi CSDL không?
> **💡 Trả lời:** Dạ có thưa Thầy. Bài test `test_concurrent_heartbeat_sync` sử dụng thư viện `concurrent.futures.ThreadPoolExecutor` để kích hoạt 10 luồng cùng lúc gửi bản tin nhịp tim và hoạt động lên Server: Nhờ chế độ SQLite WAL Mode và cơ chế khóa phiên làm việc của SQLAlchemy, toàn bộ 10 giao dịch đều được ghi nhận toàn vẹn mà không xảy ra lỗi `database is locked`.

#### ❓ Câu 776: Thầy hỏi: Môi trường kiểm thử có tự động dọn dẹp (Tear Down) tệp CSDL tạm sau khi chạy test xong không?
> **💡 Trả lời:** Dạ có thưa Thầy. Mọi Fixture đều sử dụng từ khóa `yield`: Phần mã nguồn sau `yield` thực hiện việc dọn dẹp bộ nhớ, đóng kết nối Socket, xóa các tệp tạm `.tmp` trong thư mục test, đảm bảo môi trường kiểm thử luôn sạch sẽ tuyệt đối cho các lần chạy tiếp theo.

#### ❓ Câu 777: Thầy hỏi: Tổng thời gian thực thi toàn bộ 61 test cases từ đầu đến cuối là bao nhiêu giây?
> **💡 Trả lời:** Dạ thưa Thầy, tổng thời gian chạy thực tế đo được trên máy tính là **9.82 giây**. Tốc độ này cực kỳ nhanh, cho phép sinh viên chạy lại toàn bộ bộ test sau mỗi lần chỉnh sửa code mà không phải chờ đợi lâu.

#### ❓ Câu 778: Thầy hỏi: Lệnh chạy kiểm thử có sinh ra báo cáo HTML hoặc Coverage Report không?
> **💡 Trả lời:** Dạ có thưa Thầy. Bằng cách thêm cờ `--html=tests/reports/report.html --cov=server --cov=agent --cov-report=html`, Pytest tự động sinh ra một trang web báo cáo trực quan kèm biểu đồ phân tích độ bao phủ mã nguồn của từng tệp tin.

#### ❓ Câu 779: Thầy hỏi: Nếu ngay bây giờ Thầy sửa một dòng code gây lỗi bảo mật thì test runner có phát hiện ra ngay không?
> **💡 Trả lời:** Dạ chắc chắn phát hiện ra ngay lập tức! Ví dụ nếu Thầy sửa bỏ dòng kiểm tra `if device.parent_id != current_parent.id` trong route lấy quy tắc, bài test `test_idor_protection_cross_parent` sẽ lập tức báo `FAILED` màu đỏ với thông báo lỗi: *"Kỳ vọng nhận mã lỗi 403 Forbidden nhưng Server lại trả về mã 200 OK!"*.

#### ❓ Câu 780: Thầy hỏi: Tại sao nhóm tự tin khẳng định 61/61 test cases PASSED 100% không có gian lận?
> **💡 Trả lời:** Dạ thưa Thầy, vì toàn bộ mã nguồn kiểm thử và mã nguồn hệ thống đều được lưu trữ công khai trong repo Git. Bất kỳ ai cũng có thể clone repo về, gõ một lệnh duy nhất `pytest` trong terminal và tận mắt chứng kiến 61 bài test chạy qua từng module và đạt 100% Pass một cách hoàn toàn khách quan.

---

# SLIDE 40: KẾT LUẬN TOÀN DIỆN ĐỒ ÁN, MỞ RỘNG THƯƠNG MẠI & SẴN SÀNG BẢO VỆ (CÂU 781 - 800)

#### ❓ Câu 781: Thầy hỏi: Hãy tóm tắt 3 đóng góp khoa học và kỹ thuật lớn nhất của toàn bộ Đồ án Tốt nghiệp này?
> **💡 Trả lời:** Dạ thưa Thầy, 3 đóng góp lớn nhất là:
> 1. **Đột phá về Giải thuật Mạng & Hệ thống:** Tầng lọc DNS Sinkhole nội bộ cổng UDP 53 đạt độ trễ kỷ lục 0.83 ms, vô hiệu hóa DoH qua Canary NXDOMAIN, và giải thuật băm SHA-256 kết hợp mtime cache đạt mức tiêu thụ 0.0% CPU.
> 2. **Kiến trúc An toàn Thông tin Đạt Chuẩn Quốc Tế:** Hiện thực hóa chuẩn mật mã NIST SP 800-63B (Argon2id, khóa brute-force), AES-256-GCM AEAD, và triệt tiêu 100% lỗ hổng IDOR theo tiêu chuẩn OWASP ASVS v4 Level 1.
> 3. **Tiên phong Pháp lý & Triết lý Nhân văn:** Hệ thống đầu tiên tuân thủ trọn vẹn Điều 20 Nghị định 13/2023/NĐ-CP và Luật Trẻ Em 2016, loại bỏ hoàn toàn cơ chế chụp lén màn hình, cung cấp kênh đối thoại hai chiều xin thêm giờ văn minh.

#### ❓ Câu 782: Thầy hỏi: Đồ án này đã giải quyết triệt để vấn đề gì mà các giải pháp hiện nay trên thị trường còn bỏ ngỏ?
> **💡 Trả lời:** Dạ giải quyết được mâu thuẫn lớn giữa **"Giám sát an toàn"** và **"Bảo vệ quyền riêng tư"**:  
> Các phần mềm thương mại hiện nay thường biến tướng thành công cụ gián điệp (chụp màn hình, đọc trộm tin nhắn) và gửi dữ liệu lên máy chủ nước ngoài, gây tâm lý ức chế cho trẻ và rủi ro rò rỉ dữ liệu cá nhân. OGK giải quyết bài toán bằng kiến trúc 100% Local-First: Giữ trọn dữ liệu trong gia đình, chỉ quản trị ở mức siêu dữ liệu mạng và tiến trình, tạo môi trường số an toàn và tin cậy cho trẻ em.

#### ❓ Câu 783: Thầy hỏi: Tại sao nhóm tự hào về tính nhân văn và giáo dục của phần mềm hơn là tính năng giám sát?
> **💡 Trả lời:** Dạ vì công nghệ sinh ra là để phụng sự con người và kết nối yêu thương. Một phần mềm dù kỹ thuật có tối tân đến đâu nhưng nếu tạo ra sự rạn nứt tình cảm giữa cha mẹ và con cái thì đó là một thiết kế thất bại. Tính năng xin thêm giờ, báo chặn nhầm và bảng thông báo minh bạch của OGK biến công nghệ thành một công cụ giáo dục gia đình, dạy cho trẻ kỹ năng tự quản trị thời gian và trách nhiệm với hành vi số của mình.

#### ❓ Câu 784: Thầy hỏi: Hạn chế kỹ thuật lớn nhất của hệ thống hiện tại là gì mà nhóm chưa kịp giải quyết?
> **💡 Trả lời:** Dạ thưa Thầy, hạn chế lớn nhất là: Agent hiện tại mới tối ưu sâu cho hệ điều hành **Windows (Windows 10, 11)**, chưa hỗ trợ trực tiếp hệ điều hành macOS và Linux. Ngoài ra, việc triển khai Server vẫn cần một máy tính trong nhà bật nguồn làm máy chủ nội bộ.

#### ❓ Câu 785: Thầy hỏi: Nếu có thêm 6 tháng nghiên cứu sau tốt nghiệp, nhóm sẽ phát triển tiếp những tính năng gì?
> **💡 Trả lời:** Dạ nhóm sẽ phát triển 3 hướng:
> 1. Phát triển phiên bản Agent cho macOS (sử dụng Network Extension API) và Linux (sử dụng iptables/eBPF).
> 2. Đóng gói khối OGK-Server thành một Firmware nhúng siêu nhẹ cài trực tiếp lên các bộ phát Wi-Fi (OpenWrt Router) để quản lý toàn bộ mạng gia đình không cần cài app.
> 3. Tích hợp mô hình AI ngôn ngữ nhỏ (On-device SLM) chạy cục bộ để tự động phân tích và gắn nhãn các tên miền mới mà không cần cập nhật danh sách thủ công.

#### ❓ Câu 786: Thầy hỏi: Khả năng thương mại hóa sản phẩm: Mô hình kinh doanh (Business Model) khả thi cho OGK là gì?
> **💡 Trả lời:** Dạ mô hình kinh doanh khả thi là **Open-Core / Freemium**:
> - Bản miễn phí (Community Edition): Mã nguồn mở 100%, phụ huynh tự cài đặt và quản lý trong mạng LAN gia đình hoàn toàn miễn phí.
> - Bản trả phí dịch vụ (Premium Cloud / Hardware): Cung cấp thiết bị phần cứng "OGK Box" cắm vào router Wi-Fi chỉ việc dùng, đi kèm dịch vụ máy chủ đám mây an toàn kết nối điện thoại phụ huynh mọi lúc mọi nơi với mức phí hợp lý (khoảng 30.000 VNĐ/tháng).

#### ❓ Câu 787: Thầy hỏi: Làm thế nào để phát triển Agent trên nền tảng điện thoại di động (Android / iOS) trong tương lai?
> **💡 Trả lời:** Dạ trên điện thoại di động:
> - Trên Android: Sử dụng `VpnService API` để tạo một card mạng VPN ảo nội bộ (Local Loopback VPN), chuyển toàn bộ truy vấn DNS của điện thoại vào lõi Sinkhole Proxy của OGK mà không cần máy chủ VPN ngoài.
> - Trên iOS: Sử dụng `NEPacketTunnelProvider` và cơ chế Quản lý Thiết bị Di động (Apple MDM / Screen Time API) của Apple.

#### ❓ Câu 788: Thầy hỏi: Giải pháp chuyển đổi sang kiến trúc Microservices và CSDL phân tán khi lượng người dùng lên 100.000 gia đình?
> **💡 Trả lời:** Dạ hệ thống sẽ được nâng cấp:
> 1. Thay thế SQLite bằng cụm CSDL phân tán **PostgreSQL** kết hợp phân mảnh (Sharding) theo `parent_id`.
> 2. Sử dụng **Redis Cluster** làm bộ nhớ đệm phân tán cho bảng băm quy tắc và quản lý phiên WebSocket.
> 3. Tách khối Server thành các dịch vụ độc lập (Auth Service, Telemetry Service, Rule Service) giao tiếp qua hàng đợi thông điệp **Apache Kafka** hoặc **RabbitMQ**, đóng gói bằng Kubernetes để tự động co giãn tải (Auto-scaling).

#### ❓ Câu 789: Thầy hỏi: Hệ thống có khả năng tích hợp mô hình AI phân loại nội dung web theo thời gian thực (On-device LLM) không?
> **💡 Trả lời:** Dạ hoàn toàn khả thi thưa Thầy! Với sự phát triển của các mô hình ngôn ngữ nhỏ chạy cục bộ trên máy tính (như Llama-3-8B hoặc Phi-3 Mini), khi trẻ truy cập một tên miền mới lạ chưa có trong cơ sở dữ liệu, Proxy có thể trích xuất tiêu đề (Title) và thẻ Meta của trang web, đưa vào mô hình AI cục bộ phân tích ngữ nghĩa trong 0.2 giây để quyết định cho phép hay chặn mà không làm lộ lịch sử duyệt web ra ngoài Internet.

#### ❓ Câu 790: Thầy hỏi: Nếu một gia đình có 3 con dùng chung 1 máy tính nhưng dùng 3 tài khoản Windows khác nhau thì xử lý sao?
> **💡 Trả lời:** Dạ kiến trúc của OGK đã dự trù điều này: Agent chạy ở Session 0 có thể đọc thông tin tài khoản người dùng đang đăng nhập qua hàm Win32 `WTSQuerySessionInformation`. Hệ thống có thể gắn mỗi tài khoản Windows (User Account) với một hồ sơ quy tắc (Child Profile) riêng biệt trong CSDL: Bé lớn 15 tuổi có hạn mức 120 phút và mở web học tập; bé nhỏ 8 tuổi có hạn mức 45 phút và khóa chặt game.

#### ❓ Câu 791: Thầy hỏi: Kế hoạch nâng cấp hỗ trợ giao thức HTTP/3 (QUIC) chạy trên nền UDP cổng 443 trong tương lai?
> **💡 Trả lời:** Dạ thưa Thầy, HTTP/3 (QUIC) chạy trên nền UDP cổng 443. Tuy nhiên, trước khi thiết lập kết nối HTTP/3, trình duyệt bắt buộc vẫn phải phân giải tên miền DNS cổng 53 để lấy địa chỉ IP đích. Do đó, DNS Sinkhole Proxy của OGK vẫn chặn đứng kết nối HTTP/3 ngay từ bước đầu tiên. Trong tương lai, nhóm sẽ bổ sung thêm luật tường lửa lọc trực tiếp gói tin UDP cổng 443 nếu phát hiện ứng dụng cố tình bỏ qua DNS.

#### ❓ Câu 792: Thầy hỏi: Các thành viên trong nhóm đã học được những kỹ năng chuyên môn gì quý giá nhất qua đồ án này?
> **💡 Trả lời:** Dạ thưa Thầy, chúng em đã trưởng thành vượt bậc về 4 nhóm kỹ năng: (1) Kỹ năng lập trình mạng Socket UDP/TCP và phân tích cấu trúc nhị phân gói tin RFC 1035; (2) Kỹ năng lập trình hệ thống cấp nhân Win32 API trên Windows; (3) Kỹ năng an toàn thông tin và mật mã học ứng dụng (Argon2id, AES-256-GCM, ASVS v4); (4) Kỷ luật kỹ thuật phần mềm thông qua phương pháp luận Spec-Driven Development và kiểm thử tự động Test-Driven Development.

#### ❓ Câu 793: Thầy hỏi: Kỹ năng lập trình hệ thống (Systems Programming) và lập trình mạng (Network Programming) thể hiện rõ nhất ở đâu?
> **💡 Trả lời:** Dạ:
> - **Lập trình mạng:** Thể hiện rõ nhất trong `agent/dns_proxy.py` (lập trình Socket UDP non-blocking cổng 53, giải mã tiêu đề nhị phân, xử lý cờ QR/RCODE, kỹ thuật nén con trỏ 0xC0) và trong `server/websocket_manager.py` (kênh truyền song công RFC 6455).
> - **Lập trình hệ thống:** Thể hiện rõ nhất trong `agent/app_monitor.py` (gọi hàm C-Runtime qua ctypes, tương tác Win32 API `TerminateProcess`, `LockWorkStation`, đọc Master File Table mtime qua `os.path.getmtime`).

#### ❓ Câu 794: Thầy hỏi: Kinh nghiệm thực tiễn về an toàn thông tin và bảo mật ứng dụng mà nhóm tích lũy được là gì?
> **💡 Trả lời:** Dạ đó là tư duy **"Phòng thủ chiều sâu" (Defense-in-Depth)** và **"Không tin tưởng bất kỳ ai" (Zero-Trust Architecture)**: Không bao giờ tin tưởng dữ liệu người dùng gửi lên (phải phòng vệ IDOR và Rate Limiting); không bao giờ dùng các thuật toán mật mã cũ lỗi thời (chuyển dịch sang Argon2id và AES-256-GCM AEAD); và luôn kiểm chứng an ninh bằng các mô hình đe dọa bài bản như STRIDE.

#### ❓ Câu 795: Thầy hỏi: Lời khuyên của nhóm dành cho các bạn sinh viên khóa dưới khi chọn đề tài về mạng và an toàn thông tin?
> **💡 Trả lời:** Dạ lời khuyên chân thành của nhóm là: *"Hãy dám đi sâu vào bản chất kỹ thuật từ con số 0 (First-Principles). Đừng ngại đụng vào các tầng giao thức Socket nhị phân hay gọi hàm API của hệ điều hành. Và quan trọng nhất: Hãy áp dụng kỷ luật kiểm thử tự động (TDD/SDD) ngay từ ngày đầu tiên — việc viết test cẩn thận chính là chìa khóa giúp chúng ta tự tin mỉm cười trước mọi câu hỏi hóc búa nhất của Hội đồng phản biện!"*

#### ❓ Câu 796: Thầy hỏi: Nếu tự chấm điểm đồ án này trên thang điểm 10, nhóm tự đánh giá mình xứng đáng được mấy điểm? Vì sao?
> **💡 Trả lời:** Dạ thưa Thầy và quý Thầy Cô trong Hội đồng: Nhóm xin phép được tự đề xuất mức điểm **9.5 đến 10 điểm**.  
> Lý do vì nhóm đã hoàn thành xuất sắc 100% mục tiêu đề tài, khối lượng công việc đồ sộ với 164 micro-tasks và 61/61 bài test tự động PASSED 100%, sở hữu 6 báo cáo mạng chuyên sâu M1-M6, số liệu thực nghiệm M4 chứng minh hiệu năng vượt bậc, giải quyết triệt để 7 kỹ thuật vượt rào M3, và tiên phong tuân thủ đầy đủ chuẩn mực đạo đức pháp lý bảo vệ trẻ em theo Nghị định 13/2023/NĐ-CP.

#### ❓ Câu 797: Thầy hỏi: Sản phẩm có sẵn sàng đăng ký tham gia các cuộc thi Sáng tạo Khởi nghiệp hoặc Sinh viên Nghiên cứu Khoa học không?
> **💡 Trả lời:** Dạ thưa Thầy, sản phẩm **hoàn toàn sẵn sàng và đầy đủ hồ sơ!**  
> Dự án sở hữu hàm lượng nghiên cứu học thuật cao, số liệu thực nghiệm đo đạc khoa học, tính ứng dụng thực tiễn giải quyết bài toán nóng bỏng của hàng triệu gia đình Việt Nam trong thời đại số, và tuân thủ chặt chẽ chủ trương bảo vệ trẻ em trên môi trường mạng của Thủ tướng Chính phủ.

#### ❓ Câu 798: Thầy hỏi: Nhóm có dự định phát hành mã nguồn mở cộng đồng trên GitHub sau khi bảo vệ xong không?
> **💡 Trả lời:** Dạ có thưa Thầy. Sau khi hoàn thành phiên bảo vệ tốt nghiệp chính thức, nhóm sẽ dọn dẹp mã nguồn, cập nhật tài liệu đóng góp (CONTRIBUTING.md) và chính thức phát hành phiên bản mã nguồn mở cộng đồng Open Guardian Kids trên GitHub theo giấy phép GNU General Public License v3 (GPLv3) để mọi phụ huynh và lập trình viên Việt Nam đều có thể cùng chung tay hoàn thiện sản phẩm bảo vệ thế hệ mầm non tương lai.

#### ❓ Câu 799: Thầy hỏi: Chuẩn bị demo: Hãy khởi động hệ thống và thực hiện 3 thao tác kỹ thuật ấn tượng nhất ngay bây giờ?
> **💡 Trả lời:** Dạ thưa Thầy, hệ thống đã sẵn sàng demo ngay lập tức:
> 1. **Thao tác 1 (Phát lệnh khóa khẩn cấp):** Phụ huynh bấm nút Khóa máy trên Dashboard điện thoại $ightarrow$ Màn hình máy tính con lập tức khóa lại qua WebSocket trong 0.8 giây!
> 2. **Thao tác 2 (Chặn web đen DNS Sinkhole):** Mở trình duyệt trên máy con gõ `tiktok.com` $ightarrow$ Trình duyệt báo lỗi kết nối ngay trong 0.83 ms và trả về `0.0.0.0` trên Wireshark!
> 3. **Thao tác 3 (Khắc chế đổi tên game):** Chạy tệp `game.exe` đã bị đổi tên thành `calc.exe` $ightarrow$ AppMonitor nhận diện mã băm SHA-256 và lập tức hạ gục tiến trình trong 5 giây!

#### ❓ Câu 800: Thầy hỏi: Lời cảm ơn cuối cùng của nhóm gửi tới Thầy Cô hướng dẫn và Hội đồng phản biện là gì?
> **💡 Trả lời:** Dạ kính thưa Thầy/Cô Chủ tịch Hội đồng, Thầy/Cô phản biện và Thầy/Cô hướng dẫn!  
> Chúng em xin được gửi lời tri ân sâu sắc và chân thành nhất tới quý Thầy Cô trong Khoa Mạng Máy Tính & Truyền Thông. Suốt 4 năm học tập và đặc biệt là trong 4 tuần làm đồ án tốt nghiệp tập trung vừa qua, sự chỉ bảo tận tình, những câu hỏi phản biện sắc bén và định hướng khoa học nghiêm cẩn của quý Thầy Cô đã giúp chúng em không chỉ hoàn thành một đồ án tốt nghiệp xuất sắc, mà còn tôi luyện cho chúng em bản lĩnh nghề nghiệp, tư duy khoa học độc lập và đạo đức của một kỹ sư công nghệ thông tin chân chính.  
> Chúng em xin trân trọng cảm ơn quý Thầy Cô và xin kính chúc quý Thầy Cô luôn dồi dào sức khỏe và hạnh phúc!
