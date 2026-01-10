@echo off
REM Frontend Coordinator - Setup Script for Windows
REM This script installs all dependencies for the Frontend

echo.
echo ========================================
echo   FRONTEND COORDINATOR - SETUP
echo ========================================
echo.

echo [1/3] Checking Python installation...
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

echo [2/3] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [3/3] Configuration check...
echo.
echo IMPORTANT: Before running the frontend, you need to configure PC URLs.
echo.
echo Edit coordinator.py and set:
echo   PC1_CHAIRMAN_URL = "http://[PC1_IP]:5002"
echo   PC2_COUNCIL_URL = "http://[PC2_IP]:5001"
echo.
echo Replace [PC1_IP] and [PC2_IP] with actual IP addresses.
echo.
echo To find IP addresses:
echo   - On PC1: Run ipconfig and look for IPv4 Address
echo   - On PC2: Run ipconfig and look for IPv4 Address
echo.

echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Get IP addresses from PC1 and PC2
echo 2. Edit coordinator.py with the correct URLs
echo 3. Run run.bat to start the frontend
echo 4. Open browser to http://localhost:5000
echo.
pause
