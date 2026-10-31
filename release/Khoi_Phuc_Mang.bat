@echo off
chcp 65001 >nul
title Open Guardian Kids - Khoi Phuc Cai Dat Mang (Restore Network DNS)
color 0A

:: Kiem tra quyen Administrator (UAC)
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ========================================================================
    echo   [!] Dang yeu cau cap quyen Administrator (Windows UAC)...
    echo   [*] Vui long nhan 'Yes' (Co) khi hop thoai xac nhan hien len!
    echo ========================================================================
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs" 2>nul
    exit /b
)

echo.
echo ========================================================================
echo        KHOI PHUC CAI DAT MANG & DNS VE MAC DINH (DHCP)
echo ========================================================================
echo.

echo  [1/4] Dang dat lai DNS tat ca card mang ve Tu dong (DHCP)...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-NetAdapter | ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.ifIndex -ResetServerAddresses }" >nul 2>&1

:: Netsh fallback cho cac interface
for /f "tokens=4*" %%a in ('netsh interface ipv4 show interfaces ^| findstr /i "connected"') do (
    netsh interface ipv4 set dns name="%%b" dhcp >nul 2>&1
    netsh interface ipv6 set dnsservers name="%%b" dhcp >nul 2>&1
)
netsh interface ipv4 set dns name="Wi-Fi" dhcp >nul 2>&1
netsh interface ipv4 set dns name="Wi-Fi 2" dhcp >nul 2>&1
netsh interface ipv4 set dns name="Ethernet" dhcp >nul 2>&1
netsh interface ipv6 set dnsservers name="Wi-Fi" dhcp >nul 2>&1
netsh interface ipv6 set dnsservers name="Wi-Fi 2" dhcp >nul 2>&1
netsh interface ipv6 set dnsservers name="Ethernet" dhcp >nul 2>&1

echo        - Da reset DNS ve DHCP thanh cong.

echo.
echo  [2/4] Dang lam sach tep hosts Windows...
python -c "
import os, re
hosts = r'C:\Windows\System32\drivers\etc\hosts'
if os.path.exists(hosts):
    try:
        with open(hosts, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        pattern = re.compile(r'# === OPEN GUARDIAN KIDS BLOCKED DOMAINS.*?# === END OPEN GUARDIAN KIDS BLOCKED DOMAINS ===\n?', re.DOTALL)
        clean = pattern.sub('', content).strip()
        with open(hosts, 'w', encoding='utf-8') as f:
            f.write(clean + '\n')
    except Exception as e:
        pass
" 2>nul
echo        - Da lam sach tep hosts Windows.

echo.
echo  [3/4] Dang khoi phuc chinh sach DNS tren trinh duyet...
reg delete "HKLM\SOFTWARE\Policies\Google\Chrome" /v DnsOverHttpsMode /f >nul 2>&1
reg delete "HKCU\SOFTWARE\Policies\Google\Chrome" /v DnsOverHttpsMode /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Policies\Google\Chrome" /v QuicAllowed /f >nul 2>&1
reg delete "HKCU\SOFTWARE\Policies\Google\Chrome" /v QuicAllowed /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Edge" /v DnsOverHttpsMode /f >nul 2>&1
reg delete "HKCU\SOFTWARE\Policies\Microsoft\Edge" /v DnsOverHttpsMode /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Policies\BraveSoftware\Brave" /v DnsOverHttpsMode /f >nul 2>&1
reg delete "HKCU\SOFTWARE\Policies\BraveSoftware\Brave" /v DnsOverHttpsMode /f >nul 2>&1
echo        - Da khoi phuc thiet lap DoH trinh duyet.

echo.
echo  [4/4] Lam moi bo nho dem DNS (ipconfig /flushdns)...
ipconfig /flushdns >nul 2>&1
echo        - Da lam moi bo nho dem DNS.

echo.
echo ========================================================================
echo  [THANH CONG] Mang Internet cua ban da duoc khoi phuc ve mac dinh!
echo  Hay thu mo trinh duyet va vao web de kiem tra.
echo ========================================================================
echo.
pause
