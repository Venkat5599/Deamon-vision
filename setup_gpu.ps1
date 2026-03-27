Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GPU Setup Script for RTX 4060" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Creating Python 3.11 virtual environment..." -ForegroundColor Yellow
try {
    python3.11 -m venv venv311
    Write-Host "✓ Virtual environment created!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python 3.11 not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.11 from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}
Write-Host ""

Write-Host "Step 2: Activating environment..." -ForegroundColor Yellow
.\venv311\Scripts\Activate.ps1
Write-Host "✓ Environment activated!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 3: Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel | Out-Null
Write-Host "✓ Pip upgraded!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 4: Installing PyTorch with CUDA 11.8..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install PyTorch" -ForegroundColor Red
    exit 1
}
Write-Host "✓ PyTorch with CUDA installed!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 5: Installing other dependencies..." -ForegroundColor Yellow
pip install ultralytics fastapi uvicorn websockets python-multipart opencv-python pillow pyyaml numpy scipy filterpy lap
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ All dependencies installed!" -ForegroundColor Green
Write-Host ""

Write-Host "Step 6: Verifying GPU..." -ForegroundColor Yellow
python check_cuda.py
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run with GPU:" -ForegroundColor Yellow
Write-Host "  python main.py --device cuda" -ForegroundColor White
Write-Host ""
