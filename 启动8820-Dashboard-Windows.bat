@echo off
REM 启动8820 Dashboard服务 - Windows版本
echo ====================================
echo 启动Dashboard - 端口8820
echo ====================================
echo.

cd /d "%~dp0\dashboard-v1.9-20251121"

echo 检查Python是否安装...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.x
    pause
    exit /b 1
)

echo [OK] Python已安装
echo.

echo 启动Dashboard服务...
echo 目录: dashboard-v1.9-20251121
echo 端口: 8820
echo 访问: http://localhost:8820
echo.
echo 按 Ctrl+C 停止服务
echo.

python -m http.server 8820

pause






