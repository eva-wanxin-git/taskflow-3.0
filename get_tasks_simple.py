import sqlite3
import json

conn = sqlite3.connect('database/data/tasks.db')
c = conn.cursor()

# Query REQ tasks
c.execute('''SELECT id, title, description, status, priority, estimated_hours, created_at 
             FROM tasks 
             WHERE id LIKE "REQ-%" AND status IN ("pending", "in_progress")
             ORDER BY priority, created_at DESC''')
req_tasks = c.fetchall()

# Query architect tasks
c.execute('''SELECT id, title, description, status, priority, estimated_hours, created_at 
             FROM tasks 
             WHERE assigned_to="fullstack-engineer" AND status="pending"
             ORDER BY priority, created_at DESC''')
arch_tasks = c.fetchall()

data = {
    'req_tasks': [
        {
            'id': t[0],
            'title': t[1],
            'description': t[2],
            'status': t[3],
            'priority': t[4],
            'estimated_hours': t[5],
            'created_at': t[6]
        }
        for t in req_tasks
    ],
    'arch_tasks': [
        {
            'id': t[0],
            'title': t[1],
            'description': t[2],
            'status': t[3],
            'priority': t[4],
            'estimated_hours': t[5],
            'created_at': t[6]
        }
        for t in arch_tasks
    ]
}

with open('pending_tasks_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Success! REQ: {len(req_tasks)}, ARCH: {len(arch_tasks)}")
conn.close()

