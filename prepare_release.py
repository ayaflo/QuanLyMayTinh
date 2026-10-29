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

    # Copy .env configuration
    env_src = os.path.join(PROJECT_ROOT, ".env")
    if os.path.exists(env_src):
        shutil.copy2(env_src, os.path.join(RELEASE_DIR, ".env"))
        shutil.copy2(env_src, os.path.join(target_ogk_agent, ".env"))
        print("[✓] Đã đính kèm tệp cấu hình .env vào gói cài đặt release.")

    # 3. Create Cai_Dat_Agent.bat
    cai_dat_bat = r"""@echo off
chcp 65001 >nul
title Open Guardian Kids - Cai Dat Tac Tu May Con (Agent)
color 0B

:: ============================================================================
:: BUOC 1: KIEM TRA VA YEU CAU QUYEN ADMINISTRATOR (UAC)
:: ============================================================================
if "%1"=="--elevated" goto :START_INSTALL

net session >nul 2>&1
if %errorlevel% equ 0 goto :START_INSTALL

echo.
echo ========================================================================
echo   [!] LUU Y: Cai dat can cap quyen Administrator de cau hinh bao ve mang.
echo   [*] Dang yeu cau cap quyen Administrator (Windows UAC Prompt)...
echo   [*] Vui long nhan 'Yes' (Co) khi hop thoai xac nhan hien len!
echo ========================================================================

powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -ArgumentList '--elevated' -Verb RunAs" 2>nul
if %errorlevel% equ 0 exit /b

echo.
echo [x] Khong the lay quyen Administrator hoac ban da bam 'No'.
echo     De tiep tuc, vui long click chuot phai vao file 'Cai_Dat_Agent.bat'
echo     va chon 'Run as administrator' (Chay voi quyen quan tri vien).
echo.
pause
exit /b

:START_INSTALL
cd /d "%~dp0"

echo.
echo ========================================================================
echo         OPEN GUARDIAN KIDS - CAI DAT TAC TU MAY CON (AGENT)
echo ========================================================================
echo.
echo  [1/4] Thiet lap quyen Administrator he thong... [OK]
echo.

:: ============================================================================
:: BUOC 2: CAU HINH TU DONG KHOI DONG CUNG WINDOWS
:: ============================================================================
echo  [2/4] Dang cau hinh Tu dong khoi dong cung Windows...
set "AGENT_EXE="
if exist "%~dp0OGK_Agent\OGK_Agent.exe" set "AGENT_EXE=%~dp0OGK_Agent\OGK_Agent.exe"
if exist "%~dp0release\OGK_Agent\OGK_Agent.exe" set "AGENT_EXE=%~dp0release\OGK_Agent\OGK_Agent.exe"
if exist "%~dp0dist\OGK_Agent\OGK_Agent.exe" set "AGENT_EXE=%~dp0dist\OGK_Agent\OGK_Agent.exe"

if defined AGENT_EXE (
    schtasks /create /tn "OpenGuardianKidsAgent" /tr "\"%AGENT_EXE%\"" /sc onlogon /rl highest /f >nul 2>&1
    reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "OpenGuardianKidsAgent" /t REG_SZ /d "\"%AGENT_EXE%\"" /f >nul 2>&1
    reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "OpenGuardianKidsAgent" /t REG_SZ /d "\"%AGENT_EXE%\"" /f >nul 2>&1
    echo       - Da dang ky Task Scheduler va Registry Autostart thanh cong.
) else (
    echo       [!] Chua tim thay OGK_Agent.exe, se khoi dong qua moi truong Python.
)

:: ============================================================================
:: BUOC 3: CHUAN BI HE THONG BAO VE MANG
:: ============================================================================
echo.
echo  [3/4] Chuan bi co che loc ten mien an toan...
ipconfig /flushdns >nul 2>&1
echo       - He thong DNS san sang. Co che loc se tu dong kich hoat khi tac tu khoi chay.

:: ============================================================================
:: BUOC 4: KHOI DONG TAC TU VA MO GIAO DIEN NHAP MA GHEP DOI
:: ============================================================================
echo.
echo  [4/4] Dang khoi dong tac tu va mo giao dien nhap ma ghep doi...
echo.
echo ========================================================================
echo  HUONG DAN DANH CHO PHU HUYNH:
echo  1. Mo trang quan tri Web Dashboard tren dien thoai hoac may tinh:
echo     - Dang nhap Dashboard quan ly tren Render hoac Localhost.
echo  2. Chon 'Ghep doi may tinh moi' de lay Ma 8 ky tu (Vi du: ABCD-1234).
echo  3. Nhap ma nay vao cua so 'Ghep Doi Cung Ba Me' dang mo tren man hinh!
echo ========================================================================
echo.

if defined AGENT_EXE (
    echo       - Dang khoi dong OGK_Agent.exe...
    start "" "%AGENT_EXE%"
) else (
    echo       - OGK_Agent.exe khong co san, khoi dong qua Python...
    where pythonw >nul 2>&1
    if %errorlevel% equ 0 (
        start "" pythonw agent\main.py
    ) else (
        start "" python agent\main.py
    )
)

echo.
echo  [OK] Hoan tat cai dat! Cua so ghep doi dang duoc hien thi tren man hinh.
echo       Sau khi ghep doi, bieu tuong chiec khien se xuat hien o khay he thong.
echo.
echo  Nhan phim bat ky de dong cua so cai dat nay...
pause >nul
exit /b
"""

    with open(os.path.join(RELEASE_DIR, "Cai_Dat_Agent.bat"), "w", encoding="utf-8") as f:
        f.write(cai_dat_bat)
    with open(os.path.join(PROJECT_ROOT, "Cai_Dat_Agent.bat"), "w", encoding="utf-8") as f:
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
title Open Guardian Kids - Kiem Tra Trang Thai Agent
color 0E

echo.
echo ========================================================================
echo       KIEM TRA TRANG THAI HOAT DONG TAC TU (OPEN GUARDIAN KIDS)
echo ========================================================================
echo.

echo 1. Kiem tra tien trinh ngam:
tasklist /fi "imagename eq OGK_Agent.exe" | findstr /i "OGK_Agent.exe" >nul
if %errorlevel% equ 0 (
    echo    [OK] OGK_Agent.exe: DANG CHAY NEN BAO VE
) else (
    echo    [!] OGK_Agent.exe: Chua chay (Vui long chay Cai_Dat_Agent.bat)
)

echo.
echo 2. Kiem tra tu khoi dong cung Windows:
schtasks /query /tn "OpenGuardianKidsAgent" >nul 2>&1
if %errorlevel% equ 0 (
    echo    [OK] Task Scheduler: Da dang ky tu khoi dong quyen cao nhat
) else (
    echo    [!] Task Scheduler: Chua dang ky
)

echo.
echo 3. Kiem tra cong DNS Proxy 53:
netstat -ano | findstr ":53" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo    [OK] Cong DNS 53: DANG LANG NGHE (Loc ten mien hoat dong)
) else (
    echo    [!] Cong DNS 53: Chua mo
)

echo.
echo ========================================================================
echo  Nhan phim bat ky de thoat...
pause >nul
"""
    with open(os.path.join(RELEASE_DIR, "Kiem_Tra_Trang_Thai.bat"), "w", encoding="utf-8") as f:
        f.write(kiem_tra_bat)

    # Copy Go_Cai_Dat_Chu_Dong.bat into release
    chu_dong_src = os.path.join(PROJECT_ROOT, "Go_Cai_Dat_Chu_Dong.bat")
    if os.path.exists(chu_dong_src):
        shutil.copy2(chu_dong_src, os.path.join(RELEASE_DIR, "Go_Cai_Dat_Chu_Dong.bat"))
        print("[✓] Đã đính kèm Go_Cai_Dat_Chu_Dong.bat vào gói cài đặt.")

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
