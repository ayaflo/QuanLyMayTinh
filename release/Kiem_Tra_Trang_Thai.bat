@echo off
chcp 65001 >nul
title Kiểm Tra Trạng Thái Open Guardian Kids Agent

echo.
echo ========================================================================
echo       KIỂM TRA TRẠNG THÁI HOẠT ĐỘNG TÁC TỬ (OPEN GUARDIAN KIDS)
echo ========================================================================
echo.

echo 1. Kiểm tra tiến trình ngầm:
tasklist /fi "imagename eq OGK_Agent.exe" | findstr /i "OGK_Agent.exe" >nul
if %errorlevel% equ 0 (
    echo    [✓] OGK_Agent.exe: ĐANG CHẠY NỀN BẢO VỆ
) else (
    echo    [!] OGK_Agent.exe: Chưa chạy (Vui lòng chạy Cai_Dat_Agent.bat)
)

echo.
echo 2. Kiểm tra tự khởi động cùng Windows:
schtasks /query /tn "OpenGuardianKidsAgent" >nul 2>&1
if %errorlevel% equ 0 (
    echo    [✓] Task Scheduler: Đã đăng ký tự khởi động quyền cao nhất
) else (
    echo    [!] Task Scheduler: Chưa đăng ký
)

echo.
echo 3. Kiểm tra cổng DNS Proxy 53:
netstat -ano | findstr ":53" | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo    [✓] Cổng DNS 53: ĐANG LẮNG NGHE (Lọc tên miền hoạt động)
) else (
    echo    [!] Cổng DNS 53: Chưa mở
)

echo.
echo ========================================================================
pause
