@echo off
chcp 65001 >nul
echo =========================================================================
echo    OPEN GUARDIAN KIDS - HỦY TỰ ĐỘNG KHỞI ĐỘNG CÙNG WINDOWS
echo =========================================================================
echo.
echo Đang gỡ bỏ tác tử Agent khỏi danh sách khởi động Windows...

python -c "import sys; sys.stdout.reconfigure(encoding='utf-8'); from agent.autostart import disable_autostart, remove_startup_vbs_shortcut; ok1, m1 = disable_autostart(); ok2, m2 = remove_startup_vbs_shortcut(); print('[1]', m1); print('[2]', m2)"

echo.
echo -------------------------------------------------------------------------
echo [✓] Đã hủy đăng ký tự khởi động cùng Windows thành công!
echo -------------------------------------------------------------------------
pause
