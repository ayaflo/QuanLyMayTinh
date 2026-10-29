@echo off
chcp 65001 > nul
title Open Guardian Kids - Go Cai Dat va Lam Sach Agent (Demo Reset)
color 0C

:: Neu da co co --elevated, bo qua buoc nang quyen tranh lap vo tan
if "%1"=="--elevated" goto :START_UNINSTALL

:: Kiem tra quyen Administrator
net session >nul 2>&1
if %errorlevel% equ 0 goto :START_UNINSTALL

echo =================================================================
echo   [!] LUU Y: Can quyen Administrator de khoi phuc card mang.
echo   [*] Dang yeu cau cap quyen Administrator (UAC Prompt)...
echo =================================================================

powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -ArgumentList '--elevated' -Verb RunAs" 2>nul
if %errorlevel% equ 0 exit /b

echo.
echo [!] Khong the cap quyen Administrator. Tiep tuc o che do thong thuong...
echo.

:START_UNINSTALL
echo =================================================================
echo   OPEN GUARDIAN KIDS (OGK) - GO CAI DAT VA LAM SACH DE DEMO
echo =================================================================
echo.
cd /d "%~dp0"
python agent/uninstall.py %*
if errorlevel 1 (
    echo.
    echo [!] Qua trinh go cai dat bao loi: %errorlevel%
)
echo.
pause
