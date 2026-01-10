@echo off
REM PC2 Council - Setup Script for Windows
REM This script installs all dependencies for the Council server

echo.
echo ========================================
echo   PC2 COUNCIL - SETUP
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo Python is installed!
echo.

echo [2/4] Checking Ollama installation...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama is not installed!
    echo Please install Ollama from https://ollama.ai
    pause
    exit /b 1
)
ollama --version
echo Ollama is installed!
echo.

echo [3/4] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [4/4] Pulling Council models (3 models)...
echo This may take 10-20 minutes (large downloads)...
echo.

echo Pulling llama3.2:3b...
ollama pull llama3.2:3b
if errorlevel 1 (
    echo ERROR: Failed to pull llama3.2:3b!
    pause
    exit /b 1
)
echo.

echo Pulling mistral:7b...
ollama pull mistral:7b
if errorlevel 1 (
    echo ERROR: Failed to pull mistral:7b!
    pause
    exit /b 1
)
echo.

echo Pulling phi3:mini...
ollama pull phi3:mini
if errorlevel 1 (
    echo ERROR: Failed to pull phi3:mini!
    pause
    exit /b 1
)
echo.

echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo Installed models:
ollama list
echo.
echo Next steps:
echo 1. Configure firewall to allow port 5001
echo 2. Run run.bat to start the Council server
echo 3. Share your PC IP address with your teammate
echo.
pause
