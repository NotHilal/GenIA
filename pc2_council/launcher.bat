@echo off
REM PC2 Council - Launcher for Windows
REM This script starts the Council server

echo.
echo ========================================
echo   PC2 COUNCIL - STARTING SERVER
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

echo Available models:
ollama list
echo.

REM Display IP address
echo Your PC2 IP addresses:
ipconfig | findstr /i "IPv4"
echo.
echo Share this IP with your teammate for the frontend configuration.
echo.

REM Check if port is already in use
netstat -ano | findstr :5001 >nul
if not errorlevel 1 (
    echo WARNING: Port 5001 is already in use!
    echo Another instance might be running.
    echo.
)

echo Starting Council server on port 5001...
echo This server hosts 3+ LLMs for the council.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python council_server.py

REM This runs if server stops
echo.
echo Server stopped.
pause
