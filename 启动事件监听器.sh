#!/bin/bash
# 启动架构师事件流自动监听器

cd "$(dirname "$0")"

echo "========================================"
echo "  启动架构师事件流监听器"
echo "========================================"
echo ""

# 检查watchdog是否安装
python3 -c "import watchdog" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少watchdog库，正在安装..."
    pip3 install watchdog
    echo ""
fi

echo "🚀 启动监听器..."
echo ""

python3 scripts/auto_monitor_architect_events.py

