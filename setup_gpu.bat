@echo off
echo ========================================
echo GPU Setup Script for RTX 4060
echo ========================================
echo.

echo Step 1: Creating Python 3.11 virtual environment...

REM Try python3.11 first
python3.11 --version >nul 2>&1
if %errorlevel% equ 0 (
    python3.11 -m venv venv311
    goto :venv_created
)

REM Try py -3.11
py -3.11 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using py -3.11 launcher...
    py -3.11 -m venv venv311
    goto :venv_created
)

REM Try python (might be 3.11)
python --version 2>&1 | findstr "3.11" >nul
if %errorlevel% equ 0 (
    echo Using python command...
    python -m venv venv311
    goto :venv_created
)

echo ERROR: Python 3.11 not found in PATH!
echo.
echo Python 3.11 was installed but you need to:
echo 1. Close this PowerShell window
echo 2. Open a NEW PowerShell window
echo 3. Run: .\setup_gpu.bat again
echo.
pause
exit /b 1

:venv_created
echo ✓ Virtual environment created!
echo.

echo Step 2: Activating environment...
call venv311\Scripts\activate.bat
echo ✓ Environment activated!
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip setuptools wheel
echo ✓ Pip upgraded!
echo.

echo Step 4: Installing PyTorch with CUDA 11.8...
echo This may take a few minutes...
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
if errorlevel 1 (
    echo ERROR: Failed to install PyTorch
    pause
    exit /b 1
)
echo ✓ PyTorch with CUDA installed!
echo.

echo Step 5: Installing other dependencies...
pip install ultralytics fastapi uvicorn websockets python-multipart opencv-python pillow pyyaml numpy scipy filterpy lap
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ All dependencies installed!
echo.

echo Step 6: Verifying GPU...
python check_cuda.py
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run with GPU:
echo   python main.py --device cuda
echo.
pause
