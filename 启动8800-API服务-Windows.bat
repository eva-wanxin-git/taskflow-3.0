@echo off
REM 启动8800 API服务 - Windows版本
echo ====================================
echo 启动透视塔API服务 - 端口8800
echo ====================================
echo.

cd /d "%~dp0"

echo 检查Python是否安装...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.x
    pause
    exit /b 1
)

echo [OK] Python已安装
echo.

echo 检查依赖包...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [警告] FastAPI未安装，正在安装...
    pip install fastapi uvicorn
)

python -c "import uvicorn" >nul 2>&1
if errorlevel 1 (
    echo [警告] Uvicorn未安装，正在安装...
    pip install uvicorn
)

echo [OK] 依赖包就绪
echo.

echo 启动API服务...
echo 端口: 8800
echo 访问: http://localhost:8800
echo.
echo 按 Ctrl+C 停止服务
echo.

python start_insight_api.py

pause






