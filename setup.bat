@echo off
echo 🚀 Publication Assistant Quick Setup
echo ===================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Run setup
python setup.py

echo.
echo 🎯 Setup completed! 
echo.
echo To get started:
echo 1. Edit .env file with your API keys
echo 2. Run: venv\Scripts\activate
echo 3. Run: python main.py --repo-url "https://github.com/owner/repo"
echo.
pause
