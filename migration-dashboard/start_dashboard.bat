@echo off
echo ========================================
echo  4G/5G Core Migration Dashboard
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Starting FastAPI Backend (Port 8000)...
start "FastAPI Backend" cmd /k "cd /d %~dp0 && python -m uvicorn api.main:app --reload --port 8000"

echo.
echo [3/3] Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Streamlit Frontend (Port 8501)...
start "Streamlit Frontend" cmd /k "cd /d %~dp0 && streamlit run streamlit_app.py"

echo.
echo ========================================
echo  Dashboard is starting!
echo ========================================
echo.
echo  Frontend: http://localhost:8501
echo  API Docs: http://localhost:8000/docs
echo.
echo  Press any key to exit this window...
pause >nul
