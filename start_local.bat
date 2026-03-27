@echo off
echo ========================================
echo DAEMON VISION - Local Development Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

echo [1/5] Creating Python virtual environment...
if not exist venv (
    python -m venv venv
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing Python dependencies...
pip install -r requirements.txt

echo [4/5] Installing frontend dependencies...
cd frontend
if not exist node_modules (
    call npm install
)
cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the system:
echo   1. Backend:  start_backend.bat
echo   2. Frontend: start_frontend.bat
echo.
echo Or run both with: start_all.bat
echo.
pause
