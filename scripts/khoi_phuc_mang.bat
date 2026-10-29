@echo off
chcp 65001 > nul
cd /d "%~dp0\.."
call khoi_phuc_mang.bat %*
