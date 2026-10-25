@echo off
chcp 65001 >nul
echo =========================================================================
echo    OPEN GUARDIAN KIDS - CÀI ĐẶT TỰ ĐỘNG KHỞI ĐỘNG CÙNG WINDOWS
echo =========================================================================
echo.
echo Đang tiến hành đăng ký tác tử Agent vào hệ thống Windows...

python -c "import sys; sys.stdout.reconfigure(encoding='utf-8'); from agent.autostart import enable_autostart, install_startup_vbs_shortcut; ok1, m1 = enable_autostart(); ok2, m2 = install_startup_vbs_shortcut(); print('[1]', m1); print('[2]', m2)"

echo.
echo -------------------------------------------------------------------------
echo [✓] HOÀN TẤT!
echo Từ bây giờ, mỗi khi máy tính bật lên hoặc trẻ đăng nhập vào Windows,
echo Open Guardian Kids Agent sẽ tự động chạy ngầm dưới khay hệ thống (System Tray)
echo để đảm bảo các quy tắc quản lý, giới hạn thời gian và lọc web luôn hoạt động.
echo -------------------------------------------------------------------------
pause
