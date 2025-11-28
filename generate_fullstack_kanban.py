#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成全栈工程师任务看板的真实数据HTML
从数据库读取所有任务，按状态分3列
"""
import sqlite3
from pathlib import Path
import json

# 数据库路径
db_path = Path(__file__).parent / "database" / "data" / "tasks.db"

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

print("=" * 70)
print("读取全栈工程师任务看板数据")
print("=" * 70)
print()

# 查询所有任务（按状态分组）
cursor.execute("""
    SELECT id, title, description, status, priority, estimated_hours
    FROM tasks 
    WHERE project_id='TASKFLOW'
    ORDER BY 
        CASE priority 
            WHEN 'P0' THEN 1
            WHEN 'P1' THEN 2
            WHEN 'P2' THEN 3
            ELSE 4
        END,
        created_at DESC
""")

all_tasks = cursor.fetchall()

# 按状态分组
kanban = {
    'pending': [],
    'in_progress': [],
    'completed': []
}

for task in all_tasks:
    task_id, title, desc, status, priority, hours = task
    if status in kanban:
        kanban[status].append({
            'id': task_id,
            'title': title,
            'description': desc or '',
            'priority': priority,
            'hours': hours or 0
        })

print(f"待处理: {len(kanban['pending'])}个")
print(f"进行中: {len(kanban['in_progress'])}个")
print(f"已完成: {len(kanban['completed'])}个")
print()

# 生成HTML
def generate_task_card(task):
    """生成单个任务卡片"""
    priority_class = task['priority'].lower() if task['priority'] else 'p2'
    desc_short = task['description'][:80] + '...' if len(task['description']) > 80 else task['description']
    
    return f'''
                                <div class="task-card">
                                    <div class="task-card-header">
                                        <div class="task-id">{task['id']}</div>
                                        <span class="priority-badge {priority_class}">{task['priority']}</span>
                                    </div>
                                    <div class="task-card-title">{task['title']}</div>
                                    <div class="task-card-desc">{desc_short}</div>
                                    <div class="task-card-meta">
                                        <span>⏱️ {task['hours']}h</span>
                                    </div>
                                </div>'''

html = f'''
                        <div class="kanban-board">
                            <!-- 待处理列 -->
                            <div class="kanban-column">
                                <div class="kanban-column-header">
                                    <h3 class="kanban-column-title">待处理</h3>
                                    <span class="kanban-count">{len(kanban['pending'])}</span>
                                </div>
                                <div class="kanban-tasks">
{''.join([generate_task_card(t) for t in kanban['pending']])}
                                </div>
                            </div>

                            <!-- 进行中列 -->
                            <div class="kanban-column">
                                <div class="kanban-column-header">
                                    <h3 class="kanban-column-title">进行中</h3>
                                    <span class="kanban-count">{len(kanban['in_progress'])}</span>
                                </div>
                                <div class="kanban-tasks">
{''.join([generate_task_card(t) for t in kanban['in_progress']])}
                                </div>
                            </div>

                            <!-- 已完成列 -->
                            <div class="kanban-column">
                                <div class="kanban-column-header">
                                    <h3 class="kanban-column-title">已完成</h3>
                                    <span class="kanban-count">{len(kanban['completed'])}</span>
                                </div>
                                <div class="kanban-tasks">
{''.join([generate_task_card(t) for t in kanban['completed']])}
                                </div>
                            </div>
                        </div>'''

# 输出到文件
output_file = Path(__file__).parent / "fullstack_kanban_content.html"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"HTML已生成: {output_file}")
print()
print("=" * 70)
print("下一步:")
print("1. 在 dashboard-test/index.html 中找到全栈工程师任务看板Tab")
print("2. 替换为生成的HTML内容")
print("=" * 70)

conn.close()

