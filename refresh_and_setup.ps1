Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Refreshing PATH and Running Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Refreshing PATH environment..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
Write-Host "OK PATH refreshed!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 2: Checking for Python 3.11..." -ForegroundColor Yellow

# Try py -3.11 (Windows Python Launcher)
$pythonCmd = $null
$testPy = py -3.11 --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "OK Found: $testPy (using py launcher)" -ForegroundColor Green
    $pythonCmd = "py"
    $pythonArgs = "-3.11"
}

if (-not $pythonCmd) {
    Write-Host "ERROR Python 3.11 not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please close PowerShell and open a NEW window, then run:" -ForegroundColor Yellow
    Write-Host "  .\refresh_and_setup.ps1" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

Write-Host "Step 3: Creating Python 3.11 virtual environment..." -ForegroundColor Yellow
& $pythonCmd $pythonArgs -m venv venv311
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create venv" -ForegroundColor Red
    exit 1
}
Write-Host "OK Virtual environment created!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 4: Activating environment..." -ForegroundColor Yellow
.\venv311\Scripts\Activate.ps1
Write-Host "OK Environment activated!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 5: Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel | Out-Null
Write-Host "OK Pip upgraded!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 6: Installing PyTorch with CUDA 11.8..." -ForegroundColor Yellow
Write-Host "This may take a few minutes (downloading ~2GB)..." -ForegroundColor Gray
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install PyTorch" -ForegroundColor Red
    exit 1
}
Write-Host "OK PyTorch with CUDA installed!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 7: Installing other dependencies..." -ForegroundColor Yellow
pip install ultralytics fastapi uvicorn websockets python-multipart opencv-python pillow pyyaml numpy scipy filterpy lap
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "OK All dependencies installed!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 8: Verifying GPU..." -ForegroundColor Yellow
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
