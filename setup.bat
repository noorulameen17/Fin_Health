@echo off
echo ========================================
echo Financial Health Assessment Tool
echo Setup Script
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo Step 1: Setting up Backend...
echo ========================================
cd backend

:: Create virtual environment
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

:: Copy .env.example to .env if .env doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ========================================
    echo IMPORTANT: Edit backend\.env file with your actual API keys!
    echo ========================================
    echo.
)

:: Create uploads directory
if not exist uploads (
    mkdir uploads
)

cd ..

echo.
echo Step 2: Setting up Frontend...
echo ========================================
cd frontend

:: Install npm dependencies
echo Installing Node.js dependencies...
call npm install

:: Copy .env.example to .env if .env doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
)

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo.
echo 1. Install PostgreSQL if not already installed
echo    Download from: https://www.postgresql.org/download/windows/
echo.
echo 2. Create database:
echo    - Open PostgreSQL
echo    - Run: CREATE DATABASE financial_health;
echo.
echo 3. Update backend\.env with your:
echo    - Database credentials
echo    - OpenAI API key (get from https://platform.openai.com/api-keys)
echo    - Other API keys as needed
echo.
echo 4. Initialize database:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    alembic upgrade head
echo.
echo 5. Start the application using run.bat
echo.
pause
