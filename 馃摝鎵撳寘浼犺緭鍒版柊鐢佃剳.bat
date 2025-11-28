@echo off
REM 📦 打包Dashboard项目传输到新电脑（Windows版）
REM 双击执行此文件

echo ==========================================
echo 📦 任务所·Flow Dashboard 打包脚本
echo ==========================================
echo.

cd /d "%~dp0"

REM 生成时间戳
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%-%datetime:~8,6%

echo Step 1: 创建打包目录...
set PACKAGE_DIR=dashboard-package-%TIMESTAMP%
mkdir "%PACKAGE_DIR%"
echo ✅ 目录已创建: %PACKAGE_DIR%
echo.

echo Step 2: 复制dashboard-test目录...
xcopy dashboard-test "%PACKAGE_DIR%\dashboard-test\" /E /I /Y > nul
echo ✅ dashboard-test已复制
echo.

echo Step 3: 复制关键文档...
copy "📋给新AI-全栈工程师任务看板标签换行问题.md" "%PACKAGE_DIR%\" > nul 2>&1
copy "✅今日工作总结-2025-11-21.md" "%PACKAGE_DIR%\" > nul 2>&1
copy "🚀换电脑部署-第一步提示词.md" "%PACKAGE_DIR%\" > nul 2>&1
copy "🎯复制给新Cursor-第一句话.txt" "%PACKAGE_DIR%\" > nul 2>&1
copy "⚠️CURSOR开始任务前必读.md" "%PACKAGE_DIR%\" > nul 2>&1
copy "README.md" "%PACKAGE_DIR%\" > nul 2>&1
echo ✅ 关键文档已复制
echo.

echo Step 4: 创建README...
(
echo # 📖 新电脑部署说明
echo.
echo ## 🚀 快速开始（3步）
echo.
echo ### Step 1: 进入dashboard-test目录
echo cd dashboard-test
echo.
echo ### Step 2: 启动服务器
echo python -m http.server 8820
echo.
echo ### Step 3: 打开浏览器
echo 访问：http://localhost:8820/
echo.
echo ---
echo.
echo ## 📋 如果需要继续解决问题
echo.
echo 打开Cursor，复制文件：
echo 🎯复制给新Cursor-第一句话.txt
echo.
echo 粘贴到Cursor对话框，发送。
echo.
echo ---
echo.
echo 准备好了！开始部署！🚀
) > "%PACKAGE_DIR%\📖新电脑部署说明.txt"

echo ✅ README已创建
echo.

echo Step 5: 创建压缩包...
set PACKAGE_FILE=Dashboard-传输包-%TIMESTAMP%.zip
powershell -command "Compress-Archive -Path '%PACKAGE_DIR%' -DestinationPath '%PACKAGE_FILE%' -Force"
echo ✅ 压缩包已创建: %PACKAGE_FILE%
echo.

echo Step 6: 清理临时目录...
rmdir /S /Q "%PACKAGE_DIR%"
echo ✅ 临时目录已清理
echo.

echo ==========================================
echo ✅ 打包完成！
echo ==========================================
echo.
echo 📦 传输包：%PACKAGE_FILE%
echo    位置：%CD%\%PACKAGE_FILE%
echo.
echo 🚀 下一步：
echo 1. 把 %PACKAGE_FILE% 复制到新电脑
echo 2. 在新电脑解压
echo 3. 按照 📖新电脑部署说明.txt 操作
echo.
echo 💡 可以用U盘/网盘/网络传输！
echo.

pause

