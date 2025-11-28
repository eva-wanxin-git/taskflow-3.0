#!/bin/bash

cd "$(dirname "$0")/dashboard-test-8831"

echo "======================================"
echo "🚀 启动8831测试环境"
echo "======================================"
echo ""
echo "Dashboard端口: 8831"
echo "访问地址: http://localhost:8831"
echo ""
echo "⚠️  注意: 确保8800 API服务已启动"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python3 -m http.server 8831

