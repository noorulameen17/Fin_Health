@echo off
echo ========================================
echo Financial Health Assessment Tool
echo Starting Application...
echo ========================================
echo.

:: Start Backend
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate.bat && python main.py"

:: Wait a moment for backend to start
timeout /t 3 /nobreak >nul

:: Start Frontend
echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo Application Started!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
echo Press any key to stop all servers...
pause >nul

:: Kill the servers (this is basic, you may need to close windows manually)
echo Shutting down...
taskkill /FI "WindowTitle eq Backend Server*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Frontend Server*" /T /F >nul 2>&1
