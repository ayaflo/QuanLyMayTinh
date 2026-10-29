@echo off
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
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-NetAdapter | ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ResetServerAddresses }" >nul 2>&1
ipconfig /flushdns >nul 2>&1
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
:: BUOC 3: CHUAN BI HE THONG BAO VE MANG & TRINH DUYET
:: ============================================================================
echo.
echo  [3/4] Chuan bi co che loc ten mien va khoa tab An danh (Incognito)...
ipconfig /flushdns >nul 2>&1

:: 1. Khoa che do an danh va ep SafeSearch tren Google Chrome
reg add "HKLM\SOFTWARE\Policies\Google\Chrome" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Google\Chrome" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Google\Chrome" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Google\Chrome" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:32 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Google\Chrome" /v ForceGoogleSafeSearch /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Google\Chrome" /v ForceGoogleSafeSearch /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Google\Chrome" /v ForceYouTubeSafetyMode /t REG_DWORD /d 2 /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Google\Chrome" /v ForceYouTubeSafetyMode /t REG_DWORD /d 2 /f /reg:32 >nul 2>&1

reg add "HKCU\SOFTWARE\Policies\Google\Chrome" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Google\Chrome" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Google\Chrome" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Google\Chrome" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:32 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Google\Chrome" /v ForceGoogleSafeSearch /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Google\Chrome" /v ForceGoogleSafeSearch /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Google\Chrome" /v ForceYouTubeSafetyMode /t REG_DWORD /d 2 /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Google\Chrome" /v ForceYouTubeSafetyMode /t REG_DWORD /d 2 /f /reg:32 >nul 2>&1

:: 2. Khoa che do InPrivate va ep SafeSearch tren Microsoft Edge
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v InPrivateModeAvailability /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v InPrivateModeAvailability /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:32 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v ForceGoogleSafeSearch /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v ForceGoogleSafeSearch /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v ForceBingSafeSearch /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v ForceBingSafeSearch /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v ForceYouTubeSafetyMode /t REG_DWORD /d 2 /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v ForceYouTubeSafetyMode /t REG_DWORD /d 2 /f /reg:32 >nul 2>&1

reg add "HKCU\SOFTWARE\Policies\Microsoft\Edge" /v InPrivateModeAvailability /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Microsoft\Edge" /v InPrivateModeAvailability /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Microsoft\Edge" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Microsoft\Edge" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:32 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Microsoft\Edge" /v ForceGoogleSafeSearch /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Microsoft\Edge" /v ForceGoogleSafeSearch /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Microsoft\Edge" /v ForceBingSafeSearch /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Microsoft\Edge" /v ForceBingSafeSearch /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Microsoft\Edge" /v ForceYouTubeSafetyMode /t REG_DWORD /d 2 /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Microsoft\Edge" /v ForceYouTubeSafetyMode /t REG_DWORD /d 2 /f /reg:32 >nul 2>&1

:: 3. Khoa che do an danh va Tor tren Brave
reg add "HKLM\SOFTWARE\Policies\BraveSoftware\Brave" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\BraveSoftware\Brave" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\BraveSoftware\Brave" /v TorDisabled /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\BraveSoftware\Brave" /v TorDisabled /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\BraveSoftware\Brave" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\BraveSoftware\Brave" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:32 >nul 2>&1

reg add "HKCU\SOFTWARE\Policies\BraveSoftware\Brave" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\BraveSoftware\Brave" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\BraveSoftware\Brave" /v TorDisabled /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\BraveSoftware\Brave" /v TorDisabled /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\BraveSoftware\Brave" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\BraveSoftware\Brave" /v DnsOverHttpsMode /t REG_SZ /d "off" /f /reg:32 >nul 2>&1

:: 4. Khoa che do an danh tren Mozilla Firefox
reg add "HKLM\SOFTWARE\Policies\Mozilla\Firefox" /v DisablePrivateBrowsing /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Mozilla\Firefox" /v DisablePrivateBrowsing /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Mozilla\Firefox" /v DisablePrivateBrowsing /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\Mozilla\Firefox" /v DisablePrivateBrowsing /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1

:: 5. Khoa che do an danh tren CocCoc
reg add "HKLM\SOFTWARE\Policies\CocCoc\Browser" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\CocCoc\Browser" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\CocCoc\Browser" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:64 >nul 2>&1
reg add "HKCU\SOFTWARE\Policies\CocCoc\Browser" /v IncognitoModeAvailability /t REG_DWORD /d 1 /f /reg:32 >nul 2>&1

:: Lam moi cac tien trinh trinh duyet chay ngam de chinh sach khoa An danh duoc Chrome ap dung ngay
taskkill /f /im chrome.exe >nul 2>&1
taskkill /f /im msedge.exe >nul 2>&1
taskkill /f /im brave.exe >nul 2>&1

echo       - Da thiet lap khoa tab An danh va ep SafeSearch tren Chrome, Edge, Brave, CocCoc.
echo       - Da lam moi tien trinh trinh duyet de che do An danh bi vo hieu hoa ngay lap tuc.

:: ============================================================================
:: BUOC 4: KHOI DONG TAC TU VA MO GIAO DIEN NHAP MA GHEP DOI
:: ============================================================================
echo.
echo  [4/4] Dang khoi dong tac tu va mo giao dien nhap ma ghep doi...
echo.
echo ========================================================================
echo  HUONG DAN DANH CHO PHU HUYNH:
echo  1. Mo trang quan tri Web Dashboard tren dien thoai hoac may tinh.
echo  2. Chon '+ Them thiet bi' de lay Ma 8 ky tu.
echo  3. Nhap 8 ky tu vao cua so 'Ghep Doi Cung Ba Me' tren man hinh!
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
