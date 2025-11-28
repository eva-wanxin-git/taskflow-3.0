#!/bin/bash
# 启动实时脉动自动监听器（全角色）

cd "$(dirname "$0")"

echo "========================================"
echo "  启动实时脉动监听器（全角色）"
echo "========================================"
echo ""

# 检查watchdog是否安装
python3 -c "import watchdog" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少watchdog库，正在安装..."
    pip3 install watchdog
    echo ""
fi

echo "🚀 启动实时脉动监听器..."
echo "   监听全角色活动："
echo "   - 全栈工程师（完成报告、任务）"
echo "   - 架构师（审查报告、架构文档）"
echo "   - 用户（需求文档）"
echo "   - 代码管家（代码扫描）"
echo "   - 运维（故障日志）"
echo "   - 测试（测试报告）"
echo ""
echo "📂 监听目录: docs/reports, docs/arch, scripts, ops/"
echo "💾 数据文件: realtime_pulse_events.json"
echo ""
echo "按 Ctrl+C 停止监听"
echo "========================================"
echo ""

python3 scripts/auto_monitor_realtime_pulse.py

