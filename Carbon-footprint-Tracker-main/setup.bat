@echo off
REM Carbon Footprint Platform — Quick Start Script for Windows
REM This script sets up the entire project for development

setlocal enabledelayedexpansion

echo.
echo 🌍 Carbon Footprint Platform — Setup Script
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Check Python version
echo ✓ Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH. Please install Python 3.13 or higher.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo   Found Python %PYTHON_VERSION%

REM Check Node version
echo ✓ Checking Node.js version...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH. Please install Node.js 18 or higher.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo   Found Node.js %NODE_VERSION%

REM Setup Backend
echo.
echo 📦 Setting up Backend...
cd backend

if not exist "venv" (
    echo   Creating Python virtual environment...
    python -m venv venv
)

echo   Activating virtual environment...
call venv\Scripts\activate.bat

echo   Installing Python dependencies...
pip install -q -r requirements.txt

if not exist ".env" (
    echo   Creating .env file...
    copy .env.example .env
    echo   ℹ️  .env file created. Review and update if needed.
)

cd ..

REM Setup Frontend
echo.
echo 📦 Setting up Frontend...
cd frontend

echo   Installing Node dependencies...
npm install --quiet

if not exist ".env.local" (
    echo   Creating .env.local file...
    copy .env.local.example .env.local
    echo   ℹ️  .env.local file created.
)

cd ..

echo.
echo ✅ Setup Complete!
echo.
echo 🚀 Next Steps:
echo.
echo Terminal 1 - Start Backend:
echo   cd backend
echo   venv\Scripts\activate.bat
echo   uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo.
echo Terminal 2 - Start Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo 🌐 Then open:
echo   Frontend:     http://localhost:3000
echo   Backend API:  http://localhost:8000/docs
echo.
pause
