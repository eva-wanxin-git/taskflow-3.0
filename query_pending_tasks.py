import sqlite3
import json

conn = sqlite3.connect('database/data/tasks.db')
cursor = conn.cursor()

# 查询用户需求任务（REQ-开头的）
print("=" * 60)
print("Tab 1: 用户需求任务 (REQ-开头)")
print("=" * 60)
cursor.execute("""
    SELECT id, title, description, status, priority, estimated_hours, created_at
    FROM tasks 
    WHERE id LIKE 'REQ-%' AND status IN ('pending', 'in_progress')
    ORDER BY priority, created_at DESC
""")
req_tasks = cursor.fetchall()
print(f"找到 {len(req_tasks)} 个REQ任务\n")
for i, task in enumerate(req_tasks, 1):
    print(f"{i}. {task[0]}")
    print(f"   标题: {task[1]}")
    print(f"   状态: {task[3]} | 优先级: {task[4]} | 工时: {task[5]}h")
    print(f"   描述: {task[2][:100]}...")
    print()

# 查询架构师建议任务（分配给全栈工程师的pending任务）
print("=" * 60)
print("Tab 2: 架构师建议任务 (分配给全栈工程师)")
print("=" * 60)
cursor.execute("""
    SELECT id, title, description, status, priority, estimated_hours, created_at
    FROM tasks 
    WHERE assigned_to='fullstack-engineer' AND status='pending'
    ORDER BY priority, created_at DESC
""")
arch_tasks = cursor.fetchall()
print(f"找到 {len(arch_tasks)} 个架构师建议任务\n")
for i, task in enumerate(arch_tasks, 1):
    print(f"{i}. {task[0]}")
    print(f"   标题: {task[1]}")
    print(f"   状态: {task[3]} | 优先级: {task[4]} | 工时: {task[5]}h")
    print(f"   描述: {task[2][:100]}...")
    print()

# 保存为JSON供后续使用
data = {
    "req_tasks": [
        {
            "id": t[0],
            "title": t[1],
            "description": t[2],
            "status": t[3],
            "priority": t[4],
            "estimated_hours": t[5],
            "created_at": t[6]
        }
        for t in req_tasks
    ],
    "arch_tasks": [
        {
            "id": t[0],
            "title": t[1],
            "description": t[2],
            "status": t[3],
            "priority": t[4],
            "estimated_hours": t[5],
            "created_at": t[6]
        }
        for t in arch_tasks
    ]
}

with open('pending_tasks_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("=" * 60)
print(f"总计: REQ任务 {len(req_tasks)} 个 | 架构师建议 {len(arch_tasks)} 个")
print("数据已保存到 pending_tasks_data.json")
print("=" * 60)

conn.close()

