@echo off
chcp 65001 > nul
echo =========================================================================
echo    OPEN GUARDIAN KIDS - CAI DAT TU DONG KHOI DONG CUNG WINDOWS
echo =========================================================================
echo.
echo Dang tien hanh dang ky tac tu Agent vao he thong Windows...
echo.
cd /d "%~dp0\.."
python -c "import sys; sys.stdout.reconfigure(encoding='utf-8'); from agent.autostart import enable_autostart, install_startup_vbs_shortcut; ok1, m1 = enable_autostart(); ok2, m2 = install_startup_vbs_shortcut(); print('[1]', m1); print('[2]', m2)"
echo.
echo -------------------------------------------------------------------------
echo [v] HOAN TAT!
echo Tu bay gio, moi khi may tinh bat len hoac tre dang nhap vao Windows,
echo Open Guardian Kids Agent se tu dong chay ngam duoi khay he thong.
echo -------------------------------------------------------------------------
echo.
pause
