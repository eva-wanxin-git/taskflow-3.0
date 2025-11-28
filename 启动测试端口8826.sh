#!/bin/bash
# 启动测试端口8826

cd "/Users/yalinwang/Desktop/任务所 1.8/taskflow-v1-2/taskflow-v1-2/dashboard-test-8826"
echo "🚀 启动测试端口 8826..."
echo "📁 目录: $(pwd)"
echo "🌐 访问: http://localhost:8826/"
echo ""
python3 -m http.server 8826
