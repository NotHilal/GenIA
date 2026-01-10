@echo off
REM PC1 Chairman - Setup Script for Windows
REM This script installs all dependencies for the Chairman server

echo.
echo ========================================
echo   PC1 CHAIRMAN - SETUP
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

echo [4/4] Pulling Chairman model (llama3.2:3b)...
echo This may take several minutes (large download)...
ollama pull llama3.2:3b
if errorlevel 1 (
    echo ERROR: Failed to pull model!
    echo Make sure you have internet connection and enough disk space.
    pause
    exit /b 1
)
echo Model pulled successfully!
echo.

echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Configure firewall to allow port 5002
echo 2. Run run.bat to start the Chairman server
echo 3. Share your PC IP address with your teammate
echo.
pause
