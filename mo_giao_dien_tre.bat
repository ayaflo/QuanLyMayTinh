@echo off
chcp 65001 > nul
title Open Guardian Kids - Giao Dien Minh Bach Cho Tre
color 0B
echo =================================================================
echo   OPEN GUARDIAN KIDS - GIAO DIEN MINH BACH CHO TRE (NT3 VA NT5)
echo =================================================================
echo.
echo Dang khoi dong giao dien xem thoi gian va quy tac danh cho tre...
echo.
cd /d "%~dp0"
python -c "from agent.child_view import ChildViewWindow; w = ChildViewWindow(); w.show()"
if errorlevel 1 (
    echo.
    echo [!] Gap loi khi mo giao dien cho tre [Ma loi: %errorlevel%]
)
echo.
pause
