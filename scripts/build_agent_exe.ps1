# PowerShell script to build standalone Agent executable using PyInstaller
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  DỰ ÁN OPEN GUARDIAN KIDS — ĐÓNG GÓI AGENT EXE  " -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Install pyinstaller if not present
python -m pip install pyinstaller

Write-Host "[*] Đang đóng gói agent/main.py thành dist/ogk-agent.exe..." -ForegroundColor Yellow

python -m PyInstaller --noconfirm --onedir --windowed `
    --name "ogk-agent" `
    --add-data "agent;agent" `
    --hidden-import "dns" `
    --hidden-import "dns.resolver" `
    --hidden-import "psutil" `
    --hidden-import "websockets" `
    --hidden-import "cryptography" `
    agent/main.py

Write-Host "[✓] Hoàn tất đóng gói! Tệp thực thi tại: dist/ogk-agent/ogk-agent.exe" -ForegroundColor Green
