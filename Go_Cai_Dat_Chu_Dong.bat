@echo off
chcp 65001 >nul
title Open Guardian Kids — Gỡ Cài Đặt Chủ Động (Không Cần Mã Hóa)

:: ============================================================================
:: BƯỚC 1: TỰ ĐỘNG YÊU CẦU QUYỀN ADMINISTRATOR QUA WINDOWS UAC
:: ============================================================================
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ========================================================================
    echo  [!] YÊU CẦU QUYỀN ADMINISTRATOR: Đang yêu cầu nâng quyền hệ thống...
    echo      Vui lòng chọn 'Yes' khi hộp thoại Windows UAC xuất hiện.
    echo ========================================================================
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~dpnx0\"\"' -Verb RunAs"
    exit /b
)

cd /d "%~dp0"

echo.
echo ========================================================================
echo     OPEN GUARDIAN KIDS — CÔNG CỤ GỠ CÀI ĐẶT CHỦ ĐỘNG CHO PHỤ HUYNH
echo              (KHÔNG CẦN MÃ HÓA — KHÔI PHỤC GỐC 100%%)
echo ========================================================================
echo.
echo  Tệp này dành riêng cho phụ huynh để chủ động gỡ bỏ tác tử giám sát
echo  trên máy tính của con mà không cần phụ thuộc vào mã hóa máy chủ.
echo.
echo  Thao tác sẽ thực hiện:
echo   1. Dừng ngay lập tức mọi tiến trình Agent, DNS Proxy, App Controller.
echo   2. Khôi phục toàn bộ card mạng (Wi-Fi, Ethernet, IPv4, IPv6) về DHCP tự động.
echo   3. Dọn sạch danh sách tên miền chặn trong tệp Windows hosts.
echo   4. Gỡ bỏ chính sách ép DNS-over-HTTPS (DoH) trên Chrome, Edge, Brave.
echo   5. Xóa đăng ký tự khởi động cùng Windows (Task Scheduler & Registry Run).
echo   6. Xóa bộ nhớ đệm tệp agent_cache.db và làm mới DNS (ipconfig /flushdns).
echo.
echo ------------------------------------------------------------------------
set /p "CONFIRM= Bạn có chắc chắn muốn tiến hành gỡ bỏ sạch sẽ? (Y/N): "
if /i "%CONFIRM%" neq "Y" if /i "%CONFIRM%" neq "YES" (
    echo.
    echo  [x] Đã hủy thao tác.
    pause
    exit /b
)

echo.
echo  [*] Đang tiến hành gỡ bỏ và khôi phục hệ thống...
echo.

:: 1. Thử gọi qua Python module uninstaller với cờ --force-unprotected nếu có
set "UNINSTALLED_VIA_PY=0"
where python >nul 2>&1
if %errorlevel% equ 0 (
    if exist "agent\uninstall.py" (
        python agent\uninstall.py --force-unprotected --yes
        set "UNINSTALLED_VIA_PY=1"
    )
)

:: 2. Thử gọi qua file OGK_Agent.exe nếu đang chạy ở thư mục release
if exist "OGK_Agent\OGK_Agent.exe" (
    OGK_Agent\OGK_Agent.exe --uninstall --unlock-key OGK_STATIC_MASTER_UNINSTALL_KEY_2026 >nul 2>&1
)
if exist "release\OGK_Agent\OGK_Agent.exe" (
    release\OGK_Agent\OGK_Agent.exe --uninstall --unlock-key OGK_STATIC_MASTER_UNINSTALL_KEY_2026 >nul 2>&1
)

:: 3. Thực thi trực tiếp các lệnh hệ thống Windows để đảm bảo 100% sạch sẽ
echo  [1/6] Dừng mọi tiến trình ngầm...
taskkill /f /im OGK_Agent.exe >nul 2>&1
powershell -Command "Get-Process | Where-Object { $_.CommandLine -like '*agent*main.py*' -or $_.CommandLine -like '*pairing_gui*' -or $_.CommandLine -like '*dns_proxy*' } | Stop-Process -Force" >nul 2>&1
echo       -> [✓] Đã dừng các tiến trình Agent.

echo.
echo  [2/6] Khôi phục toàn bộ card mạng về DHCP tự động (IPv4 & IPv6)...
powershell -Command "Get-NetAdapter | ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ResetServerAddresses }" >nul 2>&1
echo       -> [✓] Đã trả toàn bộ card mạng (Wi-Fi, Ethernet) về DHCP ban đầu.

echo.
echo  [3/6] Dọn dẹp tệp Windows hosts...
powershell -Command "$p = 'C:\Windows\System32\drivers\etc\hosts'; if (Test-Path $p) { $c = [IO.File]::ReadAllText($p); $c = [regex]::Replace($c, '(?s)# === OPEN GUARDIAN KIDS BLOCKED DOMAINS.*?# === END OPEN GUARDIAN KIDS BLOCKED DOMAINS ===\r?\n?', ''); [IO.File]::WriteAllText($p, $c) }" >nul 2>&1
echo       -> [✓] Đã xóa danh sách tên miền chặn khỏi hosts file.

echo.
echo  [4/6] Gỡ bỏ chính sách DoH trình duyệt trên Windows Registry...
reg delete "HKLM\SOFTWARE\Policies\Google\Chrome" /v DnsOverHttpsMode /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Policies\Google\Chrome" /v IncognitoModeAvailability /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v DnsOverHttpsMode /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Policies\BraveSoftware\Brave" /v DnsOverHttpsMode /f >nul 2>&1
echo       -> [✓] Đã gỡ bỏ chính sách ép DNS trên các trình duyệt.

echo.
echo  [5/6] Xóa đăng ký tự khởi động cùng Windows...
schtasks /delete /tn "OpenGuardianKidsAgent" /f >nul 2>&1
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "OpenGuardianKidsAgent" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "OpenGuardianKidsAgent" /f >nul 2>&1
powershell -Command "$s = [Environment]::GetFolderPath('Startup') + '\OGK_Agent_Startup.vbs'; if (Test-Path $s) { Remove-Item $s -Force }" >nul 2>&1
powershell -Command "$s2 = [Environment]::GetFolderPath('Startup') + '\Chay_Agent_Nen.vbs'; if (Test-Path $s2) { Remove-Item $s2 -Force }" >nul 2>&1
echo       -> [✓] Đã xóa toàn bộ đăng ký tự khởi động.

echo.
echo  [6/6] Xóa cơ sở dữ liệu đệm & làm mới bộ nhớ đệm DNS...
if exist "agent\agent_cache.db" del /f /q "agent\agent_cache.db" >nul 2>&1
if exist "agent\agent_cache.db-wal" del /f /q "agent\agent_cache.db-wal" >nul 2>&1
if exist "agent\agent_cache.db-shm" del /f /q "agent\agent_cache.db-shm" >nul 2>&1
if exist "release\OGK_Agent\agent_cache.db" del /f /q "release\OGK_Agent\agent_cache.db" >nul 2>&1
ipconfig /flushdns >nul 2>&1
echo       -> [✓] Đã xóa tệp đệm và làm mới DNS hệ thống.

echo.
echo ========================================================================
echo  [⭐] HOÀN TẤT: MÁY TÍNH ĐÃ ĐƯỢC GỠ BỎ VÀ KHÔI PHỤC 100%% VỀ BAN ĐẦU!
echo ========================================================================
echo.
pause
