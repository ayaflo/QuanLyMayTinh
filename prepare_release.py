"""Script to assemble and bundle the full production release package for Open Guardian Kids Agent."""

import os
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
RELEASE_DIR = os.path.join(PROJECT_ROOT, "release")
DIST_AGENT_DIR = os.path.join(PROJECT_ROOT, "dist", "OGK_Agent")
AGENT_DIR = os.path.join(PROJECT_ROOT, "agent")

def prepare_release():
    print("[*] Đang chuẩn bị thư mục release/ ...")
    os.makedirs(RELEASE_DIR, exist_ok=True)

    # 1. Copy compiled OGK_Agent bundle
    target_ogk_agent = os.path.join(RELEASE_DIR, "OGK_Agent")
    if os.path.exists(DIST_AGENT_DIR):
        print(f"[*] Sao chép gói thực thi từ {DIST_AGENT_DIR} sang {target_ogk_agent} ...")
        if os.path.exists(target_ogk_agent):
            shutil.rmtree(target_ogk_agent)
        shutil.copytree(DIST_AGENT_DIR, target_ogk_agent)

    # 2. Copy encrypted vault file into OGK_Agent
    enc_vault_src = os.path.join(AGENT_DIR, "uninstall_core.enc")
    if os.path.exists(enc_vault_src):
        shutil.copy2(enc_vault_src, os.path.join(target_ogk_agent, "uninstall_core.enc"))
        print("[✓] Đã đính kèm vault mã hóa uninstall_core.enc vào gói cài đặt.")

    # 3. Create Cai_Dat_Agent.bat
    cai_dat_bat = """@echo off
chcp 65001 >nul
title Cài Đặt Open Guardian Kids Agent (Tác Tử Máy Trẻ)

:: ============================================================================
:: BƯỚC 1: TỰ ĐỘNG YÊU CẦU QUYỀN ADMINISTRATOR QUA WINDOWS UAC
:: ============================================================================
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ========================================================================
    echo  [!] YÊU CẦU QUYỀN HỆ THỐNG: Đang yêu cầu quyền Administrator...
    echo      Vui lòng chọn 'Yes' khi cửa sổ Windows User Account Control hiện lên.
    echo ========================================================================
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~dpnx0\"\"' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"

echo.
echo ========================================================================
echo         OPEN GUARDIAN KIDS — BỘ CÀI ĐẶT TÁC TỬ MÁY TÍNH TRẺ EM
echo ========================================================================
echo.
echo  [1/4] Đang thiết lập quyền Administrator hệ thống... [OK]
echo.

:: ============================================================================
:: BƯỚC 2: CẤU HÌNH TỰ ĐỘNG KHỞI ĐỘNG CÙNG WINDOWS (KHÔNG THỂ GỠ TẮT)
:: ============================================================================
echo  [2/4] Đang cấu hình Khởi động cùng Windows (Task Scheduler ^& Registry Run)...
set "AGENT_EXE=%~dp0OGK_Agent\OGK_Agent.exe"

if exist "%AGENT_EXE%" (
    :: 1. Task Scheduler chạy quyền cao nhất khi đăng nhập (Bảo vệ cấp Session 0/1)
    schtasks /create /tn "OpenGuardianKidsAgent" /tr "\"%AGENT_EXE%\"" /sc onlogon /rl highest /f >nul 2>&1
    :: 2. Registry HKLM Run
    reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "OpenGuardianKidsAgent" /t REG_SZ /d "\"%AGENT_EXE%\"" /f >nul 2>&1
    :: 3. Registry HKCU Run
    reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "OpenGuardianKidsAgent" /t REG_SZ /d "\"%AGENT_EXE%\"" /f >nul 2>&1
    echo       -> Đã đăng ký Task Scheduler & Registry Autostart thành công.
) else (
    echo       [!] Cảnh báo: Chưa tìm thấy OGK_Agent.exe, vui lòng kiểm tra thư mục OGK_Agent.
)

:: ============================================================================
:: BƯỚC 3: CẤU HÌNH BẢO VỆ MẠNG DNS LOOPBACK 127.0.0.1
:: ============================================================================
echo.
echo  [3/4] Đang kích hoạt lọc tên miền an toàn qua DNS Proxy...
powershell -Command "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ServerAddresses ('127.0.0.1') }" >nul 2>&1
ipconfig /flushdns >nul 2>&1
echo       -> Đã kích hoạt bảo vệ mạng DNS thành công.

:: ============================================================================
:: BƯỚC 4: HIỂN THỊ CỬA SỔ NHẬP MÃ GHÉP ĐÔI VÀ KHỞI ĐỘNG TÁC TỬ
:: ============================================================================
echo.
echo  [4/4] Đang khởi động tác tử và mở giao diện nhập mã ghép đôi...
echo.
echo ========================================================================
echo  HƯỚNG DẪN DÀNH CHO PHỤ HUYNH:
echo  1. Mở trang quản trị Web Dashboard trên điện thoại hoặc máy tính phụ huynh.
echo  2. Chọn "Ghép đôi máy tính mới" để lấy Mã 8 ký tự (Ví dụ: ABCD-1234).
echo  3. Nhập mã này vào cửa sổ hiện lên để hoàn tất kết nối!
echo ========================================================================
echo.

if exist "%AGENT_EXE%" (
    start "" "%AGENT_EXE%"
) else (
    echo [x] Không tìm thấy file chạy OGK_Agent.exe!
    pause
    exit /b
)

echo  [✓] Hoàn tất cài đặt! Tác tử đang chạy nền và bảo vệ máy tính của con.
echo      Biểu tượng chiếc khiên bảo vệ đã xuất hiện tại khay hệ thống (System Tray).
echo.
timeout /t 5 >nul
exit /b
"""

    with open(os.path.join(RELEASE_DIR, "Cai_Dat_Agent.bat"), "w", encoding="utf-8") as f:
        f.write(cai_dat_bat)

    # 4. Create Chay_Agent_Nen.vbs (silent launcher)
    chay_nen_vbs = """' Open Guardian Kids - Silent Background Runner
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)
agentExe = currentDir & "\\OGK_Agent\\OGK_Agent.exe"

If fso.FileExists(agentExe) Then
    WshShell.Run Chr(34) & agentExe & Chr(34), 0, False
Else
    MsgBox "Khong tim thay tap tin OGK_Agent.exe tai " & agentExe, 16, "Open Guardian Kids"
End If
"""
    with open(os.path.join(RELEASE_DIR, "Chay_Agent_Nen.vbs"), "w", encoding="utf-8") as f:
        f.write(chay_nen_vbs)

    # 5. Create Kiem_Tra_Trang_Thai.bat
    kiem_tra_bat = """@echo off
chcp 65001 >nul
title Kiểm Tra Trạng Thái Open Guardian Kids Agent

echo.
echo ========================================================================
echo       KIỂM TRA TRẠNG THÁI HOẠT ĐỘNG TÁC TỬ (OPEN GUARDIAN KIDS)
echo ========================================================================
echo.

echo 1. Kiểm tra tiến trình ngầm:
tasklist /fi "imagename eq OGK_Agent.exe" | findstr /i "OGK_Agent.exe" >nul
if %errorlevel% equ 0 (
    echo    [✓] OGK_Agent.exe: ĐANG CHẠY NỀN BẢO VỆ
) else (
    echo    [!] OGK_Agent.exe: Chưa chạy (Vui lòng chạy Cai_Dat_Agent.bat)
)

echo.
echo 2. Kiểm tra tự khởi động cùng Windows:
schtasks /query /tn "OpenGuardianKidsAgent" >nul 2>&1
if %errorlevel% equ 0 (
    echo    [✓] Task Scheduler: Đã đăng ký tự khởi động quyền cao nhất
) else (
    echo    [!] Task Scheduler: Chưa đăng ký
)

echo.
echo 3. Kiểm tra cổng DNS Proxy 53:
netstat -ano | findstr ":53" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo    [✓] Cổng DNS 53: ĐANG LẮNG NGHE (Lọc tên miền hoạt động)
) else (
    echo    [!] Cổng DNS 53: Chưa mở
)

echo.
echo ========================================================================
pause
"""
    with open(os.path.join(RELEASE_DIR, "Kiem_Tra_Trang_Thai.bat"), "w", encoding="utf-8") as f:
        f.write(kiem_tra_bat)

    # 6. Create Huong_Dan_Cai_Dat.txt
    huong_dan_txt = """================================================================================
          HƯỚNG DẪN CÀI ĐẶT & SỬ DỤNG OPEN GUARDIAN KIDS AGENT (BẢN RELEASE)
================================================================================

I. YÊU CẦU HỆ THỐNG
   • Hệ điều hành: Windows 10, Windows 11 (64-bit).
   • Quyền tài khoản: Yêu cầu cấp quyền Administrator khi cài đặt.

II. HƯỚNG DẪN CÀI ĐẶT TRÊN MÁY TÍNH CỦA TRẺ
   1. Giải nén thư mục "release" ra máy tính của con (ví dụ: C:\\OpenGuardianKids hoặc Desktop).
   2. Nhấp đúp chuột vào tệp: "Cai_Dat_Agent.bat".
   3. Khi cửa sổ Windows User Account Control (UAC) hiện lên hỏi quyền Administrator,
      chọn "Yes" (Đồng ý).
   4. Cửa sổ "Ghép Đôi Máy Tính Mới" với giao diện hiện đại sẽ hiện lên.
   5. Mở trang Web Dashboard của phụ huynh -> bấm "Ghép Đôi Thiết Bị Mới" -> lấy Mã 8 ký tự
      (Ví dụ: 9K7X-2M4P) và nhập vào ô trên màn hình máy con.
   6. Bấm "Xác Nhận Ghép Đôi". Tác tử sẽ tự động kết nối với máy chủ phụ huynh!

III. CƠ CHẾ BẢO VỆ & CHỐNG CAN THIỆP (ANTI-TAMPER PROTECTION)
   • Tự khởi động cùng Windows:
     - Tác tử tự động tạo Task Scheduler với quyền cao nhất (Highest Available) và đăng ký
       vào Registry Run.
     - Khi trẻ nhấp vào biểu tượng khay hệ thống, mục "Khởi động cùng Windows" luôn được khóa
       ở trạng thái Bắt buộc (không thể tắt).
   • Chống tự ý thoát phần mềm:
     - Khi trẻ bấm "Thoát" trên biểu tượng khay hệ thống, tác tử vẫn tiếp tục chạy ngầm trong
       hệ thống để đảm bảo hạn ngạch giờ và lọc trang web độc hại không bị gián đoạn.
   • Mã hóa file gỡ cài đặt (Encrypted Uninstall):
     - Tệp gỡ cài đặt đã được mã hóa bảo vệ (uninstall_core.enc). Trẻ không thể tự ý kích hoạt
       gỡ cài đặt từ máy tính con.

IV. CÁCH GỠ CÀI ĐẶT & HOÀN NGUYÊN MÁY TÍNH VỀ THIẾT LẬP GỐC
   • CHỈ CÓ PHỤ HUYNH MỚI CÓ THỂ GỠ BỎ:
     1. Phụ huynh đăng nhập vào trang Web Dashboard trên điện thoại/máy tính của mình.
     2. Vào mục "Cài đặt & Gỡ bỏ thiết bị" của máy con.
     3. Nhấn nút "✕ Gỡ Bỏ Thiết Bị".
     4. Máy chủ sẽ lập tức gửi lệnh gỡ cài đặt kèm khóa giải mã ủy quyền từ xa (< 5 giây).
     5. Tác tử trên máy con nhận tín hiệu, tự động giải mã và tiến hành:
        - Khôi phục toàn bộ DNS card mạng (Wi-Fi, LAN) về DHCP tự động ban đầu.
        - Xóa sạch danh sách chặn trong tệp hosts Windows.
        - Gỡ bỏ chính sách DoH trên trình duyệt.
        - Xóa đăng ký tự khởi động cùng Windows.
        - Xóa bộ nhớ đệm và dừng toàn bộ tiến trình tác tử.
        - Máy tính con trở về 100% nguyên trạng ban đầu!

================================================================================
"""
    with open(os.path.join(RELEASE_DIR, "Huong_Dan_Cai_Dat.txt"), "w", encoding="utf-8") as f:
        f.write(huong_dan_txt)

    print("[✓] Đã tạo thành công toàn bộ thư mục release sẵn sàng cài đặt thực tế!")

if __name__ == "__main__":
    prepare_release()
