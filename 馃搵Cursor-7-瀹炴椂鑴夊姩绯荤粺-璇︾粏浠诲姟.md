# 📋 Cursor #7: 实时脉动系统数据校验任务

**负责人**: 全栈工程师 #7  
**模块**: 实时脉动系统  
**工时**: 1.0小时  
**优先级**: P2 ⭐⭐

---

## 🎯 任务概述

**你负责的3个Tab**:
1. Tab 1: 系统事件（实时事件流） - ✅ 有数据（project_events表）
2. Tab 2: 项目脉搏（实时统计） - ❌ 暂无数据
3. Tab 3: 协作链（AI协作可视化） - ❌ 暂无数据

---

## 📊 Tab 1: 系统事件（✅ 有数据）

### 数据源
```python
import sqlite3
import json
from datetime import datetime, timedelta

conn = sqlite3.connect('../database/data/tasks.db')
cursor = conn.cursor()

# 查询最新100条事件
cursor.execute("""
    SELECT event_type, title, description, occurred_at, 
           category, severity, actor, tags
    FROM project_events 
    WHERE project_id='TASKFLOW' 
    ORDER BY occurred_at DESC 
    LIMIT 100
""")

events = cursor.fetchall()
print(f"找到 {len(events)} 条事件")

# 统计今日事件
today = datetime.now().date().isoformat()
cursor.execute("""
    SELECT COUNT(*) 
    FROM project_events 
    WHERE project_id='TASKFLOW' 
      AND DATE(occurred_at) = ?
""", (today,))
today_count = cursor.fetchone()[0]
print(f"今日事件: {today_count} 条")
```

### 生成HTML

```python
html_parts = []

# 筛选器
html_parts.append('''
<div class="pulse-filters">
    <button class="filter-chip active" onclick="filterPulseEvents('all')">
        全部 <span>{}</span>
    </button>
    <button class="filter-chip" onclick="filterPulseEvents('today')">
        今天 <span>{}</span>
    </button>
    <button class="filter-chip" onclick="filterPulseEvents('week')">
        本周
    </button>
    <button class="filter-chip" onclick="filterPulseEvents('decision')">
        决策
    </button>
    <button class="filter-chip" onclick="filterPulseEvents('task')">
        任务
    </button>
</div>
'''.format(len(events), today_count))

# 搜索框
html_parts.append('''
<div class="search-box">
    <input type="text" class="search-input" placeholder="搜索事件...">
</div>
''')

# 事件列表
html_parts.append('<div class="pulse-events-list">')

for event in events:
    event_type, title, desc, time, category, severity, actor, tags = event
    
    # 图标映射
    icon_map = {
        'task': '✅',
        'architecture': '🏛️',
        'decision': '📋',
        'problem': '⚠️',
        'collaboration': '🤝'
    }
    
    icon = icon_map.get(category, '📌')
    
    html_parts.append(f'''
    <div class="event-item" data-category="{category}" data-date="{time[:10]}">
        <div class="event-checkbox"></div>
        <div class="event-time">{time[11:16]}</div>
        <div class="event-icon">{icon}</div>
        <div class="event-content">
            <div class="event-title">{title}</div>
            <div class="event-description">{desc}</div>
            <div class="event-meta">
                <span class="event-actor">{actor}</span>
                <span class="event-type">{event_type}</span>
                <span class="event-severity {severity}">{severity}</span>
            </div>
        </div>
    </div>
    ''')

html_parts.append('</div>')
```

---

## 📊 Tab 2: 项目脉搏（❌ 暂无数据）

### 处理方式

```html
<div id="pulse-heartbeat" class="tab-pane">
    <div class="empty-state">
        <div class="empty-state-icon" style="font-size: 48px;">💓</div>
        <div class="empty-state-title">项目脉搏功能待实现</div>
        <div class="empty-state-description">
            <strong>需要API</strong>: GET /api/pulse/realtime<br>
            <strong>预估工时</strong>: 2小时<br>
            <strong>优先级</strong>: P2<br><br>
            
            <strong>功能规划</strong>:<br>
            • 实时活跃任务数<br>
            • 最近1小时事件数<br>
            • 平均响应时间<br>
            • 最后活动时间<br>
            • 实时更新（30秒刷新）<br><br>
            
            <button class="primary-button" onclick="alert('已加入开发计划：TASK-API-013')">
                加入开发计划
            </button>
        </div>
    </div>
</div>
```

---

## 📊 Tab 3: 协作链（❌ 暂无数据）

### 处理方式

```html
<div id="pulse-collaboration" class="tab-pane">
    <div class="empty-state">
        <div class="empty-state-icon" style="font-size: 48px;">🔗</div>
        <div class="empty-state-title">AI协作链可视化待实现</div>
        <div class="empty-state-description">
            <strong>需要API</strong>: GET /api/collaboration/chain<br>
            <strong>预估工时</strong>: 2小时<br>
            <strong>优先级</strong>: P2<br><br>
            
            <strong>功能规划</strong>:<br>
            • 架构师 → 工程师 → SRE 流转路径<br>
            • 各角色任务统计<br>
            • 流转数量可视化<br>
            • D3.js图表展示<br><br>
            
            <button class="primary-button" onclick="alert('已加入开发计划：TASK-API-014')">
                加入开发计划
            </button>
        </div>
    </div>
</div>
```

---

## 🎨 占位符样式要求

使用统一的空状态样式：

```css
.empty-state {
    text-align: center;
    padding: 60px 40px;
}

.empty-state-icon {
    font-size: 48px;
    margin-bottom: 20px;
    opacity: 0.6;
}

.empty-state-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--noir-ink);
    margin-bottom: 12px;
}

.empty-state-description {
    font-size: 14px;
    color: var(--noir-steel);
    line-height: 1.8;
}

.primary-button {
    margin-top: 24px;
    padding: 12px 32px;
    background: var(--noir-ink);
    color: white;
    border: none;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
}

.primary-button:hover {
    background: var(--noir-charcoal);
    transform: translateY(-2px);
}
```

---

## ✅ 完成检查清单

- [ ] Tab 1显示真实事件流（最新100条）
- [ ] Tab 2显示友好占位
- [ ] Tab 3显示友好占位
- [ ] 筛选器功能正常（全部/今天/本周/决策/任务）
- [ ] 搜索功能正常
- [ ] 所有Tab切换正常

完成后提交报告！

