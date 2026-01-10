@echo off
REM PC1 Chairman - Launcher for Windows
REM This script starts the Chairman server

echo.
echo ========================================
echo   PC1 CHAIRMAN - STARTING SERVER
echo ========================================
echo.

REM Check if Ollama is running
echo Checking Ollama status...
ollama list >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama is not running!
    echo Please start Ollama first.
    pause
    exit /b 1
)
echo Ollama is running!
echo.

REM Display IP address
echo Your PC1 IP addresses:
ipconfig | findstr /i "IPv4"
echo.
echo Share this IP with your teammate for the frontend configuration.
echo.

REM Check if port is already in use
netstat -ano | findstr :5002 >nul
if not errorlevel 1 (
    echo WARNING: Port 5002 is already in use!
    echo Another instance might be running.
    echo.
)

echo Starting Chairman server on port 5002...
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python chairman_server.py

REM This runs if server stops
echo.
echo Server stopped.
pause
