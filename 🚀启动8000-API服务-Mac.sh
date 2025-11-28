#!/bin/bash
# 启动8000端口API服务

cd "/Users/yalinwang/Desktop/任务所 1.8/taskflow-v1-2/taskflow-v1-2/apps/api"

echo "====================================="
echo "  启动8000端口API服务"
echo "====================================="
echo ""

# 检查端口
if lsof -ti :8000 > /dev/null 2>&1; then
    echo "⚠️  8000端口已被占用，正在清理..."
    lsof -ti :8000 | xargs kill -9 2>/dev/null
    sleep 2
fi

echo "🚀 启动API服务..."
echo "📍 端口: 8000"
echo "📁 目录: $(pwd)"
echo ""

# 启动服务
python3 -m uvicorn src.main:app --reload --port 8000

# 注意：这个脚本会在前台运行
# 按 Ctrl+C 停止服务

