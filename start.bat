@echo off
chcp 65001 >nul
echo ========================================
echo   网上商城系统启动脚本
echo ========================================
echo.

:: 启动后端
echo [1/2] 正在启动后端服务...
start "Django Backend" cmd /k "cd /d %~dp0backend && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"

:: 启动前端
echo [2/2] 正在启动前端服务...
start "Vue Frontend" cmd /k "cd /d %~dp0frontend && npm install && npm run dev"

echo.
echo ========================================
echo   服务已启动!
echo   后端: http://localhost:8000
echo   前端: http://localhost:3000
echo   API文档: http://localhost:8000/api/docs/
echo ========================================
echo.
pause
