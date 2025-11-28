# 🎯 Windows部署指南

**目标**：在Windows电脑上运行TaskFlow Dashboard  
**时间**：5-10分钟

---

## 📋 前置要求

### 1. 安装Python 3.x
```
下载地址：https://www.python.org/downloads/
版本要求：Python 3.8+
```

**安装时注意**：
- ✅ 勾选"Add Python to PATH"
- ✅ 选择"Install for all users"

**验证安装**：
```cmd
python --version
```
应该显示：Python 3.x.x

---

## 🚀 快速启动（2步）

### 第一步：启动API服务（8800端口）⭐⭐⭐⭐⭐

**方法1：双击批处理文件（推荐）**
```
双击：启动8800-API服务-Windows.bat
```

**方法2：手动命令行**
```cmd
cd 项目目录
python start_insight_api.py
```

**成功提示**：
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8800
```

**不要关闭这个窗口！** 让它保持运行。

---

### 第二步：启动Dashboard（8820端口）

**打开新的命令行窗口**

**方法1：双击批处理文件（推荐）**
```
双击：启动8820-Dashboard-Windows.bat
```

**方法2：手动命令行**
```cmd
cd 项目目录\dashboard-v1.9-20251121
python -m http.server 8820
```

**成功提示**：
```
Serving HTTP on :: port 8820 (http://[::]:8820/) ...
```

---

### 第三步：访问Dashboard

**在浏览器打开：**
```
http://localhost:8820/
```

或
```
http://127.0.0.1:8820/
```

---

## ⚠️ 常见问题

### Q1: 端口被占用
**错误信息**：`Address already in use` 或 `OSError: [WinError 10048]`

**解决方法**：
```cmd
# 查看端口占用
netstat -ano | findstr :8820
netstat -ano | findstr :8800

# 结束进程（替换PID为实际进程号）
taskkill /PID 进程号 /F
```

---

### Q2: ModuleNotFoundError: No module named 'fastapi'
**解决方法**：
```cmd
pip install fastapi uvicorn
```

---

### Q3: 页面显示但数据不对（132不是161）
**原因**：8800 API服务未启动

**解决方法**：
1. 检查8800窗口是否还在运行
2. 如果关闭了，重新运行：`启动8800-API服务-Windows.bat`
3. 刷新浏览器：Ctrl + Shift + R

---

### Q4: Python未找到
**错误信息**：`'python' 不是内部或外部命令`

**解决方法**：
1. 重新安装Python，勾选"Add to PATH"
2. 或使用完整路径：`C:\Python3x\python.exe`
3. 或在系统环境变量中添加Python路径

---

## 📊 正常运行的样子

### 命令行窗口1（8800 API）
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8800 (Press CTRL+C to quit)
```

### 命令行窗口2（8820 Dashboard）
```
Serving HTTP on :: port 8820 (http://[::]:8820/) ...
::1 - - [21/Nov/2025 16:50:23] "GET / HTTP/1.1" 200 -
::1 - - [21/Nov/2025 16:50:24] "GET /style.css HTTP/1.1" 200 -
```

### 浏览器效果
- ✅ 看到顶部黑色标题栏"任务所·Flow"
- ✅ 左侧看到"快速导航到模块 ↓"
- ✅ 看到8个导航项
- ✅ 顶部统计数字显示161（等待2秒后从132变成161）

---

## 🔧 一键启动脚本（全自动）

**创建：启动全部服务.bat**
```batch
@echo off
echo 正在启动所有服务...

start "API服务-8800" cmd /k "cd /d %~dp0 && python start_insight_api.py"
timeout /t 3 /nobreak >nul

start "Dashboard-8820" cmd /k "cd /d %~dp0\dashboard-v1.9-20251121 && python -m http.server 8820"
timeout /t 2 /nobreak >nul

echo.
echo ====================================
echo ✅ 所有服务已启动！
echo ====================================
echo.
echo 📊 服务状态:
echo    API服务: http://localhost:8800
echo    Dashboard: http://localhost:8820
echo.
echo 💡 提示: 会打开2个命令行窗口，不要关闭！
echo.

start http://localhost:8820

pause
```

---

## 📦 传输到Windows的文件清单

### 必须文件
```
✅ start_insight_api.py                 (API服务启动脚本)
✅ dashboard-v1.9-20251121/             (Dashboard目录)
   └── index.html                       (主文件)
✅ apps/dashboard/automation-data/      (数据文件目录)
   ├── v17-complete-features.json       (161个功能)
   ├── partial-features.json
   ├── project-issues.json
   └── architecture-suggestions.json
```

### 可选文件
```
⏳ dashboard-test-8826/                 (测试环境)
⏳ 其他Python脚本
⏳ 文档文件
```

---

## 🎯 最小化部署（只要核心功能）

如果您只想要基本功能，最小文件集：

```
项目根目录/
├── start_insight_api.py                     (必须)
├── dashboard-v1.9-20251121/
│   └── index.html                           (必须)
├── apps/dashboard/automation-data/          (必须)
│   ├── v17-complete-features.json
│   ├── partial-features.json
│   ├── project-issues.json
│   └── architecture-suggestions.json
└── 启动全部服务.bat                         (Windows启动脚本)
```

总大小：约30-40 MB

---

## 💡 快速诊断

**执行诊断命令**：
```cmd
# 1. 检查端口
netstat -ano | findstr :8800
netstat -ano | findstr :8820

# 2. 检查文件
dir dashboard-v1.9-20251121\index.html
dir start_insight_api.py
dir apps\dashboard\automation-data\*.json

# 3. 测试API
curl http://localhost:8800
```

---

**现在您在Windows上遇到的是8800没启动的问题，请先运行 `启动8800-API服务-Windows.bat`！**






