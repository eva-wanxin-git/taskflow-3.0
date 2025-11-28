@echo off
chcp 65001 >nul
REM 一键启动所有服务 - Windows版本
echo ====================================
echo 🚀 TaskFlow Dashboard 一键启动
echo ====================================
echo.

cd /d "%~dp0"

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python！
    echo 请先安装Python: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python已就绪
echo.

echo [2/3] 启动API服务（端口8800）...
start "API服务-8800" cmd /k "title API服务-8800 && python start_insight_api.py"
echo ✅ API服务已启动
timeout /t 3 /nobreak >nul
echo.

echo [3/3] 启动Dashboard（端口8820）...
start "Dashboard-8820" cmd /k "title Dashboard-8820 && cd dashboard-v1.9-20251121 && python -m http.server 8820"
echo ✅ Dashboard已启动
timeout /t 2 /nobreak >nul
echo.

echo ====================================
echo ✅ 所有服务已启动！
echo ====================================
echo.
echo 📊 服务状态:
echo    🔧 API服务:   http://localhost:8800
echo    🌐 Dashboard: http://localhost:8820
echo.
echo 💡 说明:
echo    • 会打开2个命令行窗口
echo    • 不要关闭这些窗口！
echo    • 按 Ctrl+C 可停止对应服务
echo.
echo 🌐 正在打开浏览器...
timeout /t 2 /nobreak >nul

start http://localhost:8820

echo.
echo ✨ 完成！请查看浏览器
echo.
pause






