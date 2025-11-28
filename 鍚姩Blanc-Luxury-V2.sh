#!/bin/bash
# 启动Blanc Luxury Edition V2 - 完整功能版
# 运行在端口8879

cd "$(dirname "$0")/apps/dashboard"

echo "========================================="
echo "  启动 Blanc Luxury Edition V2"
echo "  端口: 8879"
echo "  完整功能: 9个统计卡片 + 8个Tab"
echo "========================================="
echo ""

python3 start_blanc_luxury_v2.py


