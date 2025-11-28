#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成所有任务列表HTML（包括NULL project_id的任务）
"""
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "database" / "data" / "tasks.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("查询所有任务（包括project_id为NULL的）")
print("=" * 70)

# 查询所有任务（不限制project_id）
cursor.execute("""
    SELECT id, title, description, status, priority, estimated_hours, assigned_to
    FROM tasks 
    ORDER BY 
        CASE status 
            WHEN 'in_progress' THEN 1
            WHEN 'pending' THEN 2
            WHEN 'completed' THEN 3
            WHEN 'cancelled' THEN 4
            ELSE 5
        END,
        CASE priority 
            WHEN 'P0' THEN 1
            WHEN 'P1' THEN 2
            WHEN 'P2' THEN 3
            ELSE 4
        END,
        created_at DESC
""")

all_tasks = cursor.fetchall()
print(f"总任务数: {len(all_tasks)}")

# 统计
status_count = {}
for task in all_tasks:
    status = task[3]
    status_count[status] = status_count.get(status, 0) + 1

print("\n状态分布:")
for status, count in sorted(status_count.items()):
    print(f"  {status}: {count}个")
print()

# 生成HTML
html_parts = []

for task in all_tasks:
    task_id, title, desc, status, priority, hours, assigned_to = task
    
    # 状态映射
    status_map = {
        'pending': '待处理',
        'in_progress': '进行中',
        'completed': '已完成',
        'cancelled': '已取消'
    }
    status_cn = status_map.get(status, status)
    
    # 优先级
    priority_class = priority.lower() if priority else 'p2'
    
    # 描述
    desc_short = (desc or '')[:120] + '...' if desc and len(desc) > 120 else (desc or '暂无描述')
    
    # 小时数
    hours_str = f"{hours}" if hours else "未估算"
    
    # 分配者
    assigned_str = assigned_to or '未分配'
    
    # 状态标记
    status_attr = f' data-status="{status}"' if status == 'completed' else ''
    
    html = f'''
                        <div class="engineer-list-item" data-task-id="{task_id}"{status_attr}>
                            <div class="engineer-item-header">
                                <div class="engineer-item-title">{task_id} | {title}</div>
                                <div class="engineer-item-time">预估{hours_str}小时 · {priority or 'P2'}</div>
                            </div>
                            <div class="engineer-item-content">
                                {desc_short}
                            </div>
                            <div class="engineer-item-meta">
                                <span class="engineer-tag">{status_cn}</span>
                                <span class="engineer-tag">{assigned_str}</span>
                            </div>
                            <div class="engineer-item-actions">
                                <button class="engineer-action-btn primary" onclick="copyTaskPrompt(this)">复制提示词</button>
                                <button class="engineer-action-btn">查看详情</button>
                            </div>
                        </div>
'''
    html_parts.append(html)

# 输出
output_file = Path(__file__).parent / "all_tasks_list.html"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_parts))

print(f"HTML已生成: {output_file}")
print(f"共 {len(all_tasks)} 个任务")
print("\n替换位置: dashboard-test/index.html 行7664")
print("找到: <div class=\"engineer-list\">")
print("替换里面所有的 engineer-list-item")
print("=" * 70)

conn.close()

