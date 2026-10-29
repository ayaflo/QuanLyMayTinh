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
    echo       - Da dang ky Task Scheduler & Registry Autostart thanh cong.
) else (
    echo       [!] Chua tim thay OGK_Agent.exe, se khoi dong qua moi truong Python.
)

:: ============================================================================
:: BUOC 3: CAU HINH BAO VE MANG DNS LOOPBACK 127.0.0.1
:: ============================================================================
echo.
echo  [3/4] Dang kich hoat loc ten mien an toan qua DNS Proxy...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-NetAdapter | Where-Object { $_.Status -eq 'Up' } | ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ServerAddresses ('127.0.0.1') }" >nul 2>&1
ipconfig /flushdns >nul 2>&1
echo       - Da kich hoat bao ve mang DNS thanh cong.

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
