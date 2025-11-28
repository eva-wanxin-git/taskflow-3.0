# 📋 Cursor #6: Noah代码管家工作台数据校验任务

**负责人**: 全栈工程师 #6  
**模块**: Noah AI代码管家  
**工时**: 1.0小时  
**优先级**: P1 ⭐⭐⭐

---

## 🎯 任务概述

**你负责的4个Tab**:
1. Tab 1: 任务队列（12个任务） - ✅ 有数据（tasks表）
2. Tab 2: 代码清单（45个文件） - ❌ 暂无数据
3. Tab 3: 代码审查清单 - ❌ 暂无数据
4. Tab 4: 提示词模板 - ✅ 静态文件

---

## 📊 Tab 1: 任务队列（✅ 有数据）

### 数据源
```python
import sqlite3

conn = sqlite3.connect('../database/data/tasks.db')
cursor = conn.cursor()

# 查询分配给Noah的任务
cursor.execute("""
    SELECT id, title, description, status, priority, 
           estimated_hours, created_at
    FROM tasks 
    WHERE assigned_to='noah' 
      OR assigned_to='code-steward'
    ORDER BY 
        CASE status 
            WHEN 'in_progress' THEN 1
            WHEN 'pending' THEN 2
            WHEN 'completed' THEN 3
            ELSE 4
        END,
        priority,
        created_at DESC
""")

noah_tasks = cursor.fetchall()
print(f"Noah的任务: {len(noah_tasks)}个")
```

### 生成HTML

```python
for task in noah_tasks:
    id, title, desc, status, priority, hours, created = task
    
    # 状态样式映射
    status_class = {
        'pending': 'task-pending',
        'in_progress': 'task-active',
        'completed': 'task-done'
    }
    
    html = f'''
    <div class="task-card {status_class.get(status, 'task-pending')}">
        <div class="task-header">
            <div class="task-id">{id}</div>
            <span class="issue-priority {priority.lower()}">{priority}</span>
        </div>
        <div class="task-title">{title}</div>
        <div class="task-description">{desc[:120]}...</div>
        <div class="task-meta">
            <span>⏱️ {hours}h</span>
            <span>📅 {created[:10]}</span>
            <span class="task-status {status}">{status}</span>
        </div>
        <div class="task-actions">
            <button class="action-button">查看详情</button>
            <button class="action-button primary">开始执行</button>
        </div>
    </div>
    '''
```

---

## 📊 Tab 2: 代码清单（❌ 暂无数据）

### 处理方式

```html
<div id="noah-code-list" class="tab-pane">
    <div class="empty-state">
        <div class="empty-state-icon">📁</div>
        <div class="empty-state-title">代码清单功能待实现</div>
        <div class="empty-state-description">
            <strong>需要API</strong>: GET /api/code/inventory<br>
            <strong>预估工时</strong>: 2小时<br>
            <strong>优先级</strong>: P1<br><br>
            
            <strong>功能规划</strong>:<br>
            • 目录树结构展示（45个文件）<br>
            • 代码行数统计<br>
            • 复杂度分析<br>
            • 最后修改时间<br><br>
            
            <button class="primary-button" onclick="alert('已加入开发计划：TASK-API-012')">
                加入开发计划
            </button>
        </div>
    </div>
</div>
```

---

## 📊 Tab 3: 代码审查清单（❌ 暂无数据）

同Tab 2，显示占位符

---

## 📊 Tab 4: 提示词模板（✅ 静态文件）

### 当前状态
可能已经有静态内容

### 验证方式
检查是否显示了完整的Noah System Prompt内容

如果缺失，可以：
```python
# 读取提示词文件
with open('../docs/ai/code-steward-system-prompt.md', 'r', encoding='utf-8') as f:
    prompt_content = f.read()

# 转换为HTML显示
html = f'''
<div class="prompt-content">
    <pre style="white-space: pre-wrap; font-family: var(--font-primary);">
{prompt_content}
    </pre>
</div>
'''
```

---

## ✅ 完成检查清单

- [ ] Tab 1显示Noah的任务队列（真实数据）
- [ ] Tab 2显示友好占位（说明需要API）
- [ ] Tab 3显示友好占位
- [ ] Tab 4显示完整提示词（或验证已有）
- [ ] 所有Tab切换正常

完成后提交报告！

