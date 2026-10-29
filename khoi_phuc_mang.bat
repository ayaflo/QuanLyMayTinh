@echo off
chcp 65001 > nul
title Open Guardian Kids - Khoi Phuc Mang & DNS
color 0B

:: Neu da co co --elevated, bo qua buoc kiem tra
if "%1"=="--elevated" goto :START_RESTORE

:: Kiem tra quyen Administrator
net session >nul 2>&1
if %errorlevel% equ 0 goto :START_RESTORE

echo =================================================================
echo   [*] Dang yeu cau quyen Administrator de khoi phuc DNS mang...
echo =================================================================

powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -ArgumentList '--elevated' -Verb RunAs" 2>nul
if %errorlevel% equ 0 exit /b

echo [!] Vui long chay voi quyen Administrator de khoi phuc mang.
echo.
pause
exit /b 1

:START_RESTORE
echo =================================================================
echo   OPEN GUARDIAN KIDS - CONG CU CUU HO VA KHOI PHUC MANG
echo =================================================================
echo.
echo [*] Dang khôi phuc DNS tat ca card mang ve tu dong (DHCP)...

cd /d "%~dp0"
python -c "from agent.dns_configurator import restore_dns_to_dhcp; restore_dns_to_dhcp()" 2>nul

:: Dam bao netsh truc tiep
for /f "tokens=4* delims= " %%a in ('netsh interface show interface ^| findstr /c:"Connected"') do (
    netsh interface ipv4 set dns name="%%b" dhcp >nul 2>&1
    netsh interface ipv6 set dnsservers name="%%b" dhcp >nul 2>&1
)

ipconfig /flushdns >nul 2>&1

echo.
echo =================================================================
echo   [✓] DA KHOI PHUC KET NOI MANG VA DNS VE DHCP THANH CONG!
echo   [*] May tinh da tro ve trang thai mang goc binh thuong.
echo =================================================================
echo.
pause
