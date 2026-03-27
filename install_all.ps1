Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Complete GPU Setup - One Command" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Installing Python 3.11 via winget..." -ForegroundColor Yellow
try {
    winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
    Write-Host "✓ Python 3.11 installed!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to install Python 3.11" -ForegroundColor Red
    Write-Host "Please run manually: winget install Python.Python.3.11" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "Step 2: Refreshing PATH..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
Write-Host "✓ PATH refreshed!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 3: Verifying Python 3.11..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
try {
    $pythonVersion = & python3.11 --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ Python 3.11 installed but not in PATH yet" -ForegroundColor Yellow
    Write-Host "Please close PowerShell and run: .\setup_gpu.bat" -ForegroundColor Yellow
    exit 0
}
Write-Host ""

Write-Host "Step 4: Creating Python 3.11 virtual environment..." -ForegroundColor Yellow
python3.11 -m venv venv311
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create venv" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Virtual environment created!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 5: Activating environment..." -ForegroundColor Yellow
.\venv311\Scripts\Activate.ps1
Write-Host "✓ Environment activated!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 6: Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel | Out-Null
Write-Host "✓ Pip upgraded!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 7: Installing PyTorch with CUDA 11.8..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install PyTorch" -ForegroundColor Red
    exit 1
}
Write-Host "✓ PyTorch with CUDA installed!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 8: Installing other dependencies..." -ForegroundColor Yellow
pip install ultralytics fastapi uvicorn websockets python-multipart opencv-python pillow pyyaml numpy scipy filterpy lap
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ All dependencies installed!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 9: Verifying GPU..." -ForegroundColor Yellow
python check_cuda.py
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run with GPU:" -ForegroundColor Yellow
Write-Host "  .\venv311\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python main.py --device cuda" -ForegroundColor White
Write-Host ""
