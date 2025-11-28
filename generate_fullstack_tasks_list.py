#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成全栈工程师任务列表（列表样式，不是看板）
从数据库读取所有75个任务
"""
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "database" / "data" / "tasks.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("查询数据库中所有任务")
print("=" * 70)

# 查询所有任务
cursor.execute("""
    SELECT id, title, description, status, priority, estimated_hours, assigned_to
    FROM tasks 
    WHERE project_id='TASKFLOW'
    ORDER BY 
        CASE status 
            WHEN 'in_progress' THEN 1
            WHEN 'pending' THEN 2
            WHEN 'completed' THEN 3
            ELSE 4
        END,
        CASE priority 
            WHEN 'P0' THEN 1
            WHEN 'P1' THEN 2
            WHEN 'P2' THEN 3
            ELSE 4
        END
""")

all_tasks = cursor.fetchall()
print(f"总任务数: {len(all_tasks)}")

# 统计
status_count = {}
for task in all_tasks:
    status = task[3]
    status_count[status] = status_count.get(status, 0) + 1

for status, count in status_count.items():
    print(f"  {status}: {count}个")
print()

# 生成HTML（列表样式）
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
    
    # 优先级class
    priority_class = priority.lower() if priority else 'p2'
    
    # 描述截断
    desc_short = (desc or '')[:100] + '...' if desc and len(desc) > 100 else (desc or '暂无描述')
    
    # 生成列表项HTML
    html = f'''
                        <div class="engineer-list-item" data-task-id="{task_id}" data-status="{status}">
                            <div class="engineer-item-header">
                                <div class="engineer-item-title">{task_id} | {title}</div>
                                <div class="engineer-item-time">预估{hours}小时 · {priority}</div>
                            </div>
                            <div class="engineer-item-content">
                                {desc_short}
                            </div>
                            <div class="engineer-item-meta">
                                <span class="engineer-tag">{status_cn}</span>
                                <span class="engineer-tag">{assigned_to or '未分配'}</span>
                            </div>
                            <div class="engineer-item-actions">
                                <button class="engineer-action-btn primary" onclick="copyTaskPrompt(this)">复制提示词</button>
                                <button class="engineer-action-btn">查看详情</button>
                            </div>
                        </div>
'''
    html_parts.append(html)

# 输出
output_file = Path(__file__).parent / "fullstack_tasks_list.html"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_parts))

print(f"HTML已生成: {output_file}")
print(f"共 {len(all_tasks)} 个任务")
print()
print("=" * 70)
print("下一步:")
print("找到 index.html 行7664的 <div class=\"engineer-list\">")
print("替换里面的所有 engineer-list-item")
print("=" * 70)

conn.close()

