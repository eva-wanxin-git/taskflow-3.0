#!/bin/bash
# 透视塔服务一键启动
# 自动扫描更新 + 启动API服务

echo ""
echo "============================================"
echo "  透视塔服务启动"
echo "============================================"
echo ""
echo "🔍 功能:"
echo "  1. 自动扫描项目最新完成情况"
echo "  2. 更新透视塔数据文件"
echo "  3. 启动API服务 (端口8800)"
echo ""
echo "📍 Dashboard地址: http://localhost:8820"
echo "📍 API文档: http://localhost:8800/docs"
echo ""
echo "============================================"
echo ""

cd "$(dirname "$0")"

# 检查8820是否运行
if ! lsof -i :8820 > /dev/null 2>&1; then
    echo "⚠️  Dashboard (8820) 未运行"
    echo "   启动命令: cd dashboard-test && python3 -m http.server 8820"
    echo ""
fi

# 启动API（包含自动扫描）
echo "🚀 启动透视塔API服务..."
python3 start_insight_api.py

echo ""
echo "✅ 服务已启动"
echo ""

