@echo off
echo ===================================================================
echo  Starting Agentic AI - Student Success & Career Platform (4-Page)
echo ===================================================================

echo [1/2] Starting Python FastAPI Backend on http://127.0.0.1:8000 ...
start "Agentic AI - Backend" cmd /k "cd /d %~dp0 && .\backend\venv\Scripts\python.exe -m uvicorn main:app --app-dir backend --port 8000 --reload"

echo [2/2] Starting React + Vite Frontend on http://localhost:5173 ...
start "Agentic AI - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers have been launched in separate windows!
echo Open your browser at: http://localhost:5173
echo ===================================================================
pause
