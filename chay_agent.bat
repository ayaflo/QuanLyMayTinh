@echo off
chcp 65001 > nul
title Open Guardian Kids - Client Agent
color 0A

:: Neu da co co --elevated, bo qua buoc nang quyen tranh lap vo tan
if "%1"=="--elevated" goto :START_AGENT

:: Kiem tra quyen Administrator
net session >nul 2>&1
if %errorlevel% equ 0 goto :START_AGENT

echo =================================================================
echo   [!] LUU Y: Agent can quyen Administrator de cau hinh mang.
echo   [*] Dang yeu cau quyen Administrator (UAC Prompt)...
echo =================================================================

powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -ArgumentList '--elevated' -Verb RunAs" 2>nul
if %errorlevel% equ 0 exit /b

echo.
echo [!] Khong the lay quyen Administrator hoac da tu choi UAC.
echo [!] Agent se tiep tuc chay o che do thong thuong...
echo.

:START_AGENT
echo =================================================================
echo   OPEN GUARDIAN KIDS (OGK) - CLIENT AGENT
echo   Trang thai: Dang hoat dong va bao ve may tinh toan dien
echo =================================================================
echo.
cd /d "%~dp0"
python agent/main.py %*
if errorlevel 1 (
    echo.
    echo [!] Agent da dung lai voi ma loi: %errorlevel%
)

:: Luon khoi phuc DNS mang ve DHCP khi Agent ket thuc de tranh mat mang
python -c "from agent.dns_configurator import restore_dns_to_dhcp; restore_dns_to_dhcp()" >nul 2>&1

echo.
pause
