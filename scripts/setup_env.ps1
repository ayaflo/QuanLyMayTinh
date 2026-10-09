# scripts/setup_env.ps1
# Kich ban khoi tao moi truong ao .venv va cai dat cac thu vien cho OGK

$ErrorActionPreference = "Stop"

$RootDir = Resolve-Path "$PSScriptRoot\.."
Set-Location $RootDir

Write-Host "=== Khoi tao moi truong ao Python cho OGK ===" -ForegroundColor Cyan

# 1. Kiem tra Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Khong tim thay Python tren he thong. Vui long cai dat Python 3.11+ truoc khi tiep tuc."
    exit 1
}

# 2. Tao virtual environment neu chua ton tai
$VenvDir = Join-Path $RootDir ".venv"
if (-not (Test-Path $VenvDir)) {
    Write-Host "[1/3] Dang tao moi truong ao .venv..." -ForegroundColor Yellow
    python -m venv $VenvDir
} else {
    Write-Host "[1/3] Moi truong ao .venv da ton tai." -ForegroundColor Green
}

$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

# 3. Nang cap pip
Write-Host "[2/3] Dang cap nhat pip..." -ForegroundColor Yellow
& $VenvPython -m pip install --upgrade pip --quiet

# 4. Cai dat cac thu vien cho Server va Agent
Write-Host "[3/3] Dang cai dat cac thu vien can thiet..." -ForegroundColor Yellow

$ServerReq = Join-Path $RootDir "server\requirements.txt"
if (Test-Path $ServerReq) {
    Write-Host "  -> Cai dat server/requirements.txt..." -ForegroundColor Gray
    & $VenvPython -m pip install -r $ServerReq --quiet
}

$AgentReq = Join-Path $RootDir "agent\requirements.txt"
if (Test-Path $AgentReq) {
    Write-Host "  -> Cai dat agent/requirements.txt..." -ForegroundColor Gray
    & $VenvPython -m pip install -r $AgentReq --quiet
}

# 5. Khoi tao bien moi truong tu .env.example neu chua co .env
$EnvFile = Join-Path $RootDir ".env"
$EnvExample = Join-Path $RootDir ".env.example"
if ((-not (Test-Path $EnvFile)) -and (Test-Path $EnvExample)) {
    Write-Host "  -> Khoi tao .env tu .env.example..." -ForegroundColor Gray
    Copy-Item $EnvExample $EnvFile
}

Write-Host "=== Hoan tat khoi tao moi truong thanh cong! ===" -ForegroundColor Green
Write-Host "De kich hoat moi truong ao, chay: .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "(Neu gap loi ExecutionPolicy tren PowerShell, chay truoc: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass)" -ForegroundColor DarkGray
