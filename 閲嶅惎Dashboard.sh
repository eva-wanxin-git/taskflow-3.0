#!/bin/bash
# Dashboard重启脚本

echo "停止Dashboard..."
kill $(ps aux | grep start_dashboard | grep -v grep | awk '{print $2}') 2>/dev/null

sleep 2

echo "启动Dashboard..."
cd /Users/yalinwang/Desktop/taskflow-v1.7-from-github
python3 apps/dashboard/start_dashboard.py --port 8877 > dashboard_latest.log 2>&1 &

sleep 8

echo "✅ Dashboard已启动"
echo "访问地址: http://localhost:8877"
echo ""
echo "查看日志:"
tail -20 dashboard_latest.log

