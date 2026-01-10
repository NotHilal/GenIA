@echo off
REM Frontend Coordinator - Launcher for Windows
REM This script starts the Frontend server

echo.
echo ========================================
echo   FRONTEND COORDINATOR - STARTING
echo ========================================
echo.

REM Check if port is already in use
netstat -ano | findstr :5000 >nul
if not errorlevel 1 (
    echo WARNING: Port 5000 is already in use!
    echo Another instance might be running.
    echo.
)

echo Starting Frontend Coordinator on port 5000...
echo.
echo Once started, open your browser to:
echo   http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python coordinator.py

REM This runs if server stops
echo.
echo Server stopped.
pause
