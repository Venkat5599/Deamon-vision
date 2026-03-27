@echo off
echo ========================================
echo Complete GPU Setup - One Command
echo ========================================
echo.

echo Step 1: Installing Python 3.11 via winget...
winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
if errorlevel 1 (
    echo ERROR: Failed to install Python 3.11
    echo Please run manually: winget install Python.Python.3.11
    pause
    exit /b 1
)
echo ✓ Python 3.11 installed!
echo.

echo Step 2: Refreshing environment...
echo Please close this window and run: setup_gpu.bat
echo.
pause
