@echo off
echo ========================================
echo Starting Daemon Vision Frontend
echo ========================================
echo.

cd frontend

REM Check if node_modules exists
if not exist node_modules (
    echo Installing dependencies...
    call npm install
)

REM Create .env if it doesn't exist
if not exist .env (
    echo Creating .env file...
    echo VITE_API_URL=http://localhost:8000 > .env
)

echo Starting frontend on http://localhost:3000
echo.
call npm run dev

pause
