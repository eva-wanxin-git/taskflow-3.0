# 📋 Cursor #4: 全栈工程师工作台数据校验任务

**负责人**: 全栈工程师 #4  
**模块**: 全栈工程师工作台  
**工时**: 2.5小时  
**优先级**: P0 ⭐⭐⭐⭐⭐

---

## 📊 Tab 2: 任务看板（43个任务，3列）⭐⭐⭐⭐⭐

### 数据源
```python
import sqlite3

conn = sqlite3.connect('../database/data/tasks.db')
cursor = conn.cursor()

# 按状态分组查询
statuses = ['pending', 'in_progress', 'completed']
kanban_data = {}

for status in statuses:
    cursor.execute("""
        SELECT id, title, priority, estimated_hours, description
        FROM tasks 
        WHERE project_id='TASKFLOW' 
          AND status=?
        ORDER BY priority, created_at DESC
    """, (status,))
    
    kanban_data[status] = cursor.fetchall()
    print(f"{status}: {len(kanban_data[status])}个任务")
```

### 生成HTML（3列看板）

```python
html = '''
<div class="kanban-board">
    <div class="kanban-column">
        <div class="column-header">
            <h3>待处理</h3>
            <span class="task-count">{}</span>
        </div>
        <div class="column-tasks">
            {}
        </div>
    </div>
    <div class="kanban-column">
        <div class="column-header">
            <h3>进行中</h3>
            <span class="task-count">{}</span>
        </div>
        <div class="column-tasks">
            {}
        </div>
    </div>
    <div class="kanban-column">
        <div class="column-header">
            <h3>已完成</h3>
            <span class="task-count">{}</span>
        </div>
        <div class="column-tasks">
            {}
        </div>
    </div>
</div>
'''.format(
    len(kanban_data['pending']),
    generate_task_cards(kanban_data['pending']),
    len(kanban_data['in_progress']),
    generate_task_cards(kanban_data['in_progress']),
    len(kanban_data['completed']),
    generate_task_cards(kanban_data['completed'])
)
```

---

## 📊 Tab 3: 代码审查（暂无数据）

### 当前处理
```html
<div class="empty-state">
    <div class="empty-state-title">代码审查功能待实现</div>
    <div class="empty-state-description">
        需要实现 GET /api/code-reviews 端点<br>
        预估工时：2小时
    </div>
</div>
```

---

## 📊 Tab 4: 技术文档（暂无数据）

### 当前处理
```html
<div class="empty-state">
    <div class="empty-state-title">技术文档索引待实现</div>
    <div class="empty-state-description">
        需要实现 GET /api/documents 端点<br>
        预估工时：2小时
    </div>
</div>
```

---

## ✅ 完成标准

- [ ] 任务看板显示真实数据（3列）
- [ ] 事件流显示开发相关事件
- [ ] 暂无数据的Tab显示友好占位
- [ ] Tab切换正常

