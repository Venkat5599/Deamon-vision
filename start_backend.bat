@echo off
echo ========================================
echo Starting Daemon Vision Backend
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if sample video exists
if not exist data\sample.mp4 (
    echo WARNING: No video file found at data\sample.mp4
    echo.
    echo Please add a video file or the system will use simulated data.
    echo.
    pause
)

REM Start backend
echo Starting backend on http://localhost:8000
echo API docs at http://localhost:8000/docs
echo.
python main.py --video data/sample.mp4 --device cpu

pause
