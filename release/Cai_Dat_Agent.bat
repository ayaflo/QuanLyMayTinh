@echo off
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
    powershell -Command "Start-Process cmd -ArgumentList '/c ""%~dpnx0""' -Verb RunAs"
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
    schtasks /create /tn "OpenGuardianKidsAgent" /tr ""%AGENT_EXE%"" /sc onlogon /rl highest /f >nul 2>&1
    :: 2. Registry HKLM Run
    reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "OpenGuardianKidsAgent" /t REG_SZ /d ""%AGENT_EXE%"" /f >nul 2>&1
    :: 3. Registry HKCU Run
    reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "OpenGuardianKidsAgent" /t REG_SZ /d ""%AGENT_EXE%"" /f >nul 2>&1
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
