@echo off
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
