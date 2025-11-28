# 📋 Cursor #2: 待开发任务池数据校验任务

**负责人**: 全栈工程师 #2  
**模块**: 待开发任务池  
**工时**: 1.5小时  
**优先级**: P1 ⭐⭐⭐⭐

---

## 📊 Tab 1: 用户需求（~8个REQ任务）

### 数据源
```python
# 从数据库查询REQ-开头的任务
import sqlite3

conn = sqlite3.connect('../database/data/tasks.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT id, title, description, status, priority, 
           estimated_hours, created_at
    FROM tasks 
    WHERE project_id='TASKFLOW' 
      AND id LIKE 'REQ-%'
    ORDER BY priority, created_at DESC
""")

requirements = cursor.fetchall()
print(f"找到 {len(requirements)} 个用户需求")
```

### 生成HTML卡片

```python
for req in requirements:
    id, title, desc, status, priority, hours, created = req
    
    # 状态映射
    status_map = {
        'completed': '已完成',
        'in_progress': '开发中',
        'pending': '待评估'
    }
    
    html = f'''
    <div class="requirement-card {priority.lower()}">
        <div class="req-header">
            <div class="req-id">{id}</div>
            <div class="req-status {status}">{status_map.get(status, status)}</div>
        </div>
        <div class="req-title">{title}</div>
        <div class="req-description">{desc[:200]}...</div>
        <div class="req-meta">
            <span>⏱️ {hours}小时</span>
            <span>📅 {created[:10]}</span>
            <span class="issue-priority {priority.lower()}">{priority}</span>
        </div>
    </div>
    '''
    print(html)
```

---

## 📊 Tab 2: 架构师建议任务（~15个）

### 数据源
```python
# 查询分配给工程师的待处理任务
cursor.execute("""
    SELECT id, title, description, status, priority, 
           estimated_hours, assigned_to
    FROM tasks 
    WHERE project_id='TASKFLOW' 
      AND assigned_to='fullstack-engineer'
      AND status='pending'
    ORDER BY priority, created_at DESC
""")
```

---

## ✅ 完成标准

- [ ] 从数据库读取真实任务数据
- [ ] 生成所有需求卡片
- [ ] 状态映射正确显示中文
- [ ] 优先级颜色正确
- [ ] Tab切换正常

完成后提交报告！

