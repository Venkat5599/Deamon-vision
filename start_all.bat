@echo off
echo ========================================
echo Starting Daemon Vision Full Stack
echo ========================================
echo.

REM Start backend in new window
start "Daemon Vision Backend" cmd /k start_backend.bat

REM Wait 5 seconds for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend in new window
start "Daemon Vision Frontend" cmd /k start_frontend.bat

echo.
echo ========================================
echo System Starting...
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Two windows will open:
echo   1. Backend (Python)
echo   2. Frontend (React)
echo.
echo Press any key to exit this window...
pause >nul
