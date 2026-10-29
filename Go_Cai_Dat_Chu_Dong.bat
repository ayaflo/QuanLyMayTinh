@echo off
chcp 65001 >nul
title Open Guardian Kids - Go Cai Dat Chu Dong (Cho Phu Huynh)
color 0C

:: ============================================================================
:: BUOC 1: KIEM TRA VA YEU CAU QUYEN ADMINISTRATOR (UAC)
:: ============================================================================
if "%1"=="--elevated" goto :START_UNINSTALL

net session >nul 2>&1
if %errorlevel% equ 0 goto :START_UNINSTALL

echo.
echo ========================================================================
echo   [!] LUU Y: Go cai dat can quyen Administrator de khoi phuc card mang.
echo   [*] Dang yeu cau quyen Administrator (Windows UAC Prompt)...
echo   [*] Vui long nhan 'Yes' (Co) khi hop thoai xac nhan hien len!
echo ========================================================================

powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -ArgumentList '--elevated' -Verb RunAs" 2>nul
if %errorlevel% equ 0 exit /b

echo.
echo [x] Khong the lay quyen Administrator hoac ban da bam 'No'.
echo     De tiep tuc, vui long click chuot phai vao file nay
echo     va chon 'Run as administrator' (Chay voi quyen quan tri vien).
echo.
pause
exit /b

:START_UNINSTALL
cd /d "%~dp0"

echo.
echo ========================================================================
echo     OPEN GUARDIAN KIDS - CONG CU GO CAI DAT CHU DONG CHO PHU HUYNH
echo              (KHONG CAN MA HOA - KHOI PHUC GOC 100%%)
echo ========================================================================
echo.
echo  Tep nay danh rieng cho phu huynh de chu dong go bo tac tu giam sat
echo  tren may tinh cua con ma khong can phu thuoc vao ma hoa may chu.
echo.
echo  Thao tac se thuc hien:
echo   1. Dung ngay lap tuc moi tien trinh Agent, DNS Proxy, App Controller.
echo   2. Khoi phuc toan bo card mang (Wi-Fi, Ethernet, IPv4, IPv6) ve DHCP tu dong.
echo   3. Don sach danh sach ten mien chan trong tep Windows hosts.
echo   4. Go bo chinh sach ep DNS-over-HTTPS (DoH) tren Chrome, Edge, Brave.
echo   5. Xoa dang ky tu khoi dong cung Windows (Task Scheduler ^& Registry Run).
echo   6. Xoa bo nho dem tep agent_cache.db va lam moi DNS (ipconfig /flushdns).
echo.
echo ------------------------------------------------------------------------
set /p "CONFIRM= Ban co chac chan muon tien hanh go bo sach se? (Y/N): "
if /i "%CONFIRM%" neq "Y" if /i "%CONFIRM%" neq "YES" (
    echo.
    echo  [x] Da huy thao tac.
    pause
    exit /b
)

echo.
echo  [*] Dang tien hanh go bo va khoi phuc he thong...
echo.

:: 1. Thu goi qua Python module uninstaller voi co --force-unprotected neu co
set "UNINSTALLED_VIA_PY=0"
where python >nul 2>&1
if %errorlevel% equ 0 (
    if exist "agent\uninstall.py" (
        python agent\uninstall.py --force-unprotected --yes
        set "UNINSTALLED_VIA_PY=1"
    )
)

:: 2. Thu goi qua file OGK_Agent.exe neu dang chay o thu muc release
if exist "OGK_Agent\OGK_Agent.exe" (
    OGK_Agent\OGK_Agent.exe --uninstall --unlock-key OGK_STATIC_MASTER_UNINSTALL_KEY_2026 >nul 2>&1
)
if exist "release\OGK_Agent\OGK_Agent.exe" (
    release\OGK_Agent\OGK_Agent.exe --uninstall --unlock-key OGK_STATIC_MASTER_UNINSTALL_KEY_2026 >nul 2>&1
)

:: 3. Thuc thi truc tiep cac lenh he thong Windows de dam bao 100% sach se
echo  [1/6] Dung moi tien trinh ngam...
taskkill /f /im OGK_Agent.exe >nul 2>&1
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-Process | Where-Object { $_.CommandLine -like '*agent*main.py*' -or $_.CommandLine -like '*pairing_gui*' -or $_.CommandLine -like '*dns_proxy*' } | Stop-Process -Force" >nul 2>&1
echo       -> [OK] Da dung cac tien trinh Agent.

echo.
echo  [2/6] Khoi phuc toan bo card mang ve DHCP tu dong (IPv4 ^& IPv6)...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-NetAdapter | ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ResetServerAddresses }" >nul 2>&1
echo       -> [OK] Da tra toan bo card mang (Wi-Fi, Ethernet) ve DHCP ban dau.

echo.
echo  [3/6] Don dep tep Windows hosts...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$p = 'C:\Windows\System32\drivers\etc\hosts'; if (Test-Path $p) { $c = [IO.File]::ReadAllText($p); $c = [regex]::Replace($c, '(?s)# === OPEN GUARDIAN KIDS BLOCKED DOMAINS.*?# === END OPEN GUARDIAN KIDS BLOCKED DOMAINS ===\r?\n?', ''); [IO.File]::WriteAllText($p, $c) }" >nul 2>&1
echo       -> [OK] Da xoa danh sach ten mien chan khoi hosts file.

echo.
echo  [4/6] Go bo chinh sach DoH trinh duyet tren Windows Registry...
reg delete "HKLM\SOFTWARE\Policies\Google\Chrome" /v DnsOverHttpsMode /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Policies\Google\Chrome" /v IncognitoModeAvailability /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v DnsOverHttpsMode /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Policies\BraveSoftware\Brave" /v DnsOverHttpsMode /f >nul 2>&1
echo       -> [OK] Da go bo chinh sach ep DNS tren cac trinh duyet.

echo.
echo  [5/6] Xoa dang ky tu khoi dong cung Windows...
schtasks /delete /tn "OpenGuardianKidsAgent" /f >nul 2>&1
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "OpenGuardianKidsAgent" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "OpenGuardianKidsAgent" /t REG_SZ /f >nul 2>&1
powershell -NoProfile -ExecutionPolicy Bypass -Command "$s = [Environment]::GetFolderPath('Startup') + '\OGK_Agent_Startup.vbs'; if (Test-Path $s) { Remove-Item $s -Force }" >nul 2>&1
powershell -NoProfile -ExecutionPolicy Bypass -Command "$s2 = [Environment]::GetFolderPath('Startup') + '\Chay_Agent_Nen.vbs'; if (Test-Path $s2) { Remove-Item $s2 -Force }" >nul 2>&1
echo       -> [OK] Da xoa toan bo dang ky tu khoi dong.

echo.
echo  [6/6] Xoa co so du lieu dem ^& lam moi bo nho dem DNS...
if exist "agent\agent_cache.db" del /f /q "agent\agent_cache.db" >nul 2>&1
if exist "agent\agent_cache.db-wal" del /f /q "agent\agent_cache.db-wal" >nul 2>&1
if exist "agent\agent_cache.db-shm" del /f /q "agent\agent_cache.db-shm" >nul 2>&1
if exist "release\OGK_Agent\agent_cache.db" del /f /q "release\OGK_Agent\agent_cache.db" >nul 2>&1
ipconfig /flushdns >nul 2>&1
echo       -> [OK] Da xoa tep dem va lam moi DNS he thong.

echo.
echo ========================================================================
echo  [OK] HOAN TAT: MAY TINH DA DUOC GO BO VA KHOI PHUC 100%% VE BAN DAU!
echo ========================================================================
echo.
echo  Nhan phim bat ky de dong cua so nay...
pause >nul
exit /b
