#!/bin/bash
# 更新透视塔数据 - 重新扫描项目功能

echo "============================================"
echo "  更新透视塔数据"
echo "============================================"
echo ""

cd "$(dirname "$0")"

echo "📊 步骤1: 重新生成功能清单..."
python3 scripts/鐢熸垚v17瀹屾暣鍔熻兘娓呭崟.py

echo ""
echo "📋 步骤2: 更新项目概况数据..."
python3 scripts/architect_update_project_overview.py

echo ""
echo "✅ 数据更新完成！"
echo ""
echo "下一步："
echo "1. 刷新浏览器: http://localhost:8820"
echo "2. 数字应该已更新"
echo ""

