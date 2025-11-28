# 📋 Cursor #3: 架构师工作台数据校验任务

**负责人**: 全栈工程师 #3  
**模块**: 架构师工作台  
**工时**: 1.5小时  
**优先级**: P1 ⭐⭐⭐

---

## 📊 Tab 1: 事件流（架构决策事件）

### 数据源
```python
import sqlite3
import json

conn = sqlite3.connect('../database/data/tasks.db')
cursor = conn.cursor()

# 查询架构相关事件
cursor.execute("""
    SELECT event_type, title, description, occurred_at, 
           severity, actor, data
    FROM project_events 
    WHERE project_id='TASKFLOW' 
      AND (category='architecture' OR category='decision')
    ORDER BY occurred_at DESC 
    LIMIT 100
""")

events = cursor.fetchall()
print(f"找到 {len(events)} 条架构事件")
```

### 生成HTML

```python
for event in events:
    event_type, title, desc, time, severity, actor, data_json = event
    
    # 事件类型图标映射
    icon_map = {
        'architecture': '🏛️',
        'decision': '📋',
        'task': '✅'
    }
    
    html = f'''
    <div class="event-item" data-category="{event_type}" data-date="{time[:10]}">
        <div class="event-checkbox"></div>
        <div class="event-time">{time[11:16]}</div>
        <div class="event-icon">{icon_map.get(event_type.split('.')[0], '📌')}</div>
        <div class="event-content">
            <div class="event-title">{title}</div>
            <div class="event-meta">
                <span class="event-actor">{actor}</span>
                <span class="event-type">{event_type}</span>
            </div>
        </div>
    </div>
    '''
```

---

## 📊 Tab 3: 对话历史

### 数据源
```python
# 查询架构师角色的对话
cursor.execute("""
    SELECT id, title, created_at, metadata
    FROM conversations 
    WHERE project_id='TASKFLOW' 
    ORDER BY created_at DESC
""")
```

---

## ✅ 完成标准

- [ ] 事件流显示真实数据
- [ ] 对话历史显示真实数据
- [ ] 筛选功能正常（全部/今天/本周）
- [ ] Tab切换正常

