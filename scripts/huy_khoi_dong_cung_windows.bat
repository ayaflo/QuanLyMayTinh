@echo off
chcp 65001 > nul
echo =========================================================================
echo    OPEN GUARDIAN KIDS - HUY TU DONG KHOI DONG CUNG WINDOWS
echo =========================================================================
echo.
echo Dang go bo tac tu Agent khoi danh sach khoi dong Windows...
echo.
cd /d "%~dp0\.."
python -c "import sys; sys.stdout.reconfigure(encoding='utf-8'); from agent.autostart import disable_autostart, remove_startup_vbs_shortcut; ok1, m1 = disable_autostart(); ok2, m2 = remove_startup_vbs_shortcut(); print('[1]', m1); print('[2]', m2)"
echo.
echo -------------------------------------------------------------------------
echo [v] Da huy dang ky tu khoi dong cung Windows thanh cong!
echo -------------------------------------------------------------------------
echo.
pause
