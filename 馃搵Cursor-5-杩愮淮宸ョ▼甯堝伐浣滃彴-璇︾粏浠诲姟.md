# 📋 Cursor #5: 运维工程师工作台数据校验任务

**负责人**: 全栈工程师 #5  
**模块**: 运维工程师工作台  
**工时**: 2.0小时  
**优先级**: P1 ⭐⭐⭐

---

## 🎯 任务概述

**你负责的4个Tab**:
1. Tab 1: 运维日志（847条） - ❌ 暂无数据，显示占位
2. Tab 2: Bug看板（3个Bug） - ⚠️ 可能有数据
3. Tab 3: 系统状态（6个服务） - ❌ 暂无数据，显示占位
4. Tab 4: 知识库（128篇） - ⚠️ 可能有数据

---

## 📊 Tab 1: 运维日志（❌ 暂无数据）

### 当前状态
可能已有一些硬编码的示例日志

### 处理方式
**显示友好占位符**，因为需要 `GET /api/logs/operations` API

```html
<div id="devops-logs" class="devops-tab-pane active">
    <div class="section-header">
        <h2 class="section-title">运维日志</h2>
    </div>
    
    <div class="empty-state" style="margin-top: 60px;">
        <div class="empty-state-icon" style="font-size: 48px;">📋</div>
        <div class="empty-state-title">运维日志功能待实现</div>
        <div class="empty-state-description">
            此功能需要后端API支持<br><br>
            
            <strong>需要API</strong>: GET /api/logs/operations<br>
            <strong>预估工时</strong>: 1小时<br>
            <strong>优先级</strong>: P1<br><br>
            
            <strong>功能规划</strong>:<br>
            • 实时日志流展示（847条+）<br>
            • 按级别筛选（INFO/WARN/ERROR）<br>
            • 时间轴可视化<br>
            • 日志搜索和导出<br><br>
            
            <button class="primary-button" onclick="alert('已加入开发计划：TASK-API-010')">
                加入开发计划
            </button>
        </div>
    </div>
</div>
```

---

## 📊 Tab 2: Bug看板（⚠️ 可能有数据）

### 第1步：检查数据库

```python
import sqlite3

conn = sqlite3.connect('../database/data/tasks.db')
cursor = conn.cursor()

# 检查issues表是否存在
cursor.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name='issues'
""")
has_issues_table = cursor.fetchone() is not None

if has_issues_table:
    # 查询Bug数据
    cursor.execute("""
        SELECT id, title, description, severity, status, created_at
        FROM issues 
        WHERE project_id='TASKFLOW' 
          AND (title LIKE '%Bug%' OR title LIKE '%bug%' OR severity='high')
        ORDER BY severity DESC, created_at DESC
    """)
    bugs = cursor.fetchall()
    print(f"找到 {len(bugs)} 个Bug")
else:
    print("issues表不存在，使用占位符")
```

### 第2步：生成HTML

**如果有数据**（按状态分3列）:

```python
# 按状态分组
bug_groups = {
    'pending': [],      # 待修复
    'in_progress': [],  # 修复中
    'resolved': []      # 已验证
}

for bug in bugs:
    status = bug[4] if len(bug) > 4 else 'pending'
    if status not in bug_groups:
        status = 'pending'
    bug_groups[status].append(bug)

# 生成3列看板
html = f'''
<div class="bug-kanban">
    <div class="kanban-column">
        <div class="column-header">
            <h3>待修复</h3>
            <span class="task-count">{len(bug_groups['pending'])}</span>
        </div>
        <div class="column-tasks">
            {generate_bug_cards(bug_groups['pending'])}
        </div>
    </div>
    <div class="kanban-column">
        <div class="column-header">
            <h3>修复中</h3>
            <span class="task-count">{len(bug_groups['in_progress'])}</span>
        </div>
        <div class="column-tasks">
            {generate_bug_cards(bug_groups['in_progress'])}
        </div>
    </div>
    <div class="kanban-column">
        <div class="column-header">
            <h3>已验证</h3>
            <span class="task-count">{len(bug_groups['resolved'])}</span>
        </div>
        <div class="column-tasks">
            {generate_bug_cards(bug_groups['resolved'])}
        </div>
    </div>
</div>
'''
```

**如果无数据**（显示占位）:

```html
<div class="empty-state">
    <div class="empty-state-icon">🐛</div>
    <div class="empty-state-title">Bug管理功能待实现</div>
    <div class="empty-state-description">
        需要后端API: GET /api/bugs<br>
        预估工时: 2h | 优先级: P1<br><br>
        <button class="primary-button">加入开发计划</button>
    </div>
</div>
```

---

## 📊 Tab 3: 系统状态（❌ 暂无数据）

### 处理方式
显示占位符，说明需要监控API

```html
<div id="devops-system" class="devops-tab-pane">
    <div class="section-header">
        <h2 class="section-title">系统状态监控</h2>
    </div>
    
    <div class="empty-state" style="margin-top: 60px;">
        <div class="empty-state-icon" style="font-size: 48px;">📊</div>
        <div class="empty-state-title">系统监控功能待增强</div>
        <div class="empty-state-description">
            此功能需要后端API增强<br><br>
            
            <strong>需要API</strong>: GET /api/system/health (增强版)<br>
            <strong>预估工时</strong>: 3小时<br>
            <strong>优先级</strong>: P0<br><br>
            
            <strong>功能规划</strong>:<br>
            • 6个服务实时监控（API/Dashboard/Worker等）<br>
            • 每个服务显示：状态/端口/响应时间/CPU/内存<br>
            • 系统资源总览<br>
            • 服务健康告警<br><br>
            
            <button class="primary-button" onclick="alert('已加入开发计划：TASK-API-011')">
                加入开发计划
            </button>
        </div>
    </div>
</div>
```

---

## 📊 Tab 4: 知识库（⚠️ 可能有数据）

### 第1步：检查数据库

```python
# 检查knowledge_articles表
cursor.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name='knowledge_articles'
""")
has_kb_table = cursor.fetchone() is not None

if has_kb_table:
    cursor.execute("""
        SELECT id, title, category, content, importance, 
               tags, created_at, updated_at
        FROM knowledge_articles 
        WHERE project_id='TASKFLOW' 
        ORDER BY importance DESC, updated_at DESC
    """)
    articles = cursor.fetchall()
    print(f"找到 {len(articles)} 篇知识文章")
else:
    print("表不存在，使用占位符")
```

### 第2步：生成HTML

**如果有数据**（按分类展示）:

```python
# 按分类分组
categories = {
    'architecture': [],
    'problem': [],
    'solution': [],
    'decision': [],
    'tools': [],
    'other': []
}

for article in articles:
    cat = article[2] if article[2] in categories else 'other'
    categories[cat].append(article)

# 生成分类标签
html = '''
<div class="knowledge-filters">
    <button class="filter-chip active" onclick="filterKnowledge('all')">
        全部 <span>{}</span>
    </button>
    <button class="filter-chip" onclick="filterKnowledge('architecture')">
        架构 <span>{}</span>
    </button>
    <button class="filter-chip" onclick="filterKnowledge('problem')">
        问题 <span>{}</span>
    </button>
    <button class="filter-chip" onclick="filterKnowledge('solution')">
        解决方案 <span>{}</span>
    </button>
    <button class="filter-chip" onclick="filterKnowledge('decision')">
        决策 <span>{}</span>
    </button>
    <button class="filter-chip" onclick="filterKnowledge('tools')">
        工具 <span>{}</span>
    </button>
</div>

<div class="knowledge-list">
    {}
</div>
'''.format(
    len(articles),
    len(categories['architecture']),
    len(categories['problem']),
    len(categories['solution']),
    len(categories['decision']),
    len(categories['tools']),
    generate_knowledge_cards(articles)
)
```

**知识卡片格式**:

```html
<div class="knowledge-card" data-category="{category}">
    <div class="knowledge-header">
        <div class="knowledge-category">{category}</div>
        <div class="knowledge-importance">
            {'⭐' * importance}
        </div>
    </div>
    <div class="knowledge-title">{title}</div>
    <div class="knowledge-preview">{content[:150]}...</div>
    <div class="knowledge-meta">
        <span>📅 {updated_at}</span>
        <span>🏷️ {tags}</span>
    </div>
</div>
```

**如果无数据**:

```html
<div class="empty-state">
    <div class="empty-state-icon">📚</div>
    <div class="empty-state-title">知识库功能完整，暂无数据</div>
    <div class="empty-state-description">
        knowledge_articles 表已就绪<br>
        可以开始添加知识条目<br><br>
        <button class="primary-button">添加第一篇知识</button>
    </div>
</div>
```

---

## ✅ 完成检查清单

- [ ] Tab 1: 运维日志 - 显示友好占位
- [ ] Tab 2: Bug看板 - 有数据则显示，无数据则占位
- [ ] Tab 3: 系统状态 - 显示友好占位
- [ ] Tab 4: 知识库 - 有数据则显示，无数据则占位
- [ ] 所有Tab切换正常
- [ ] 占位符样式统一、信息清晰

---

## 📝 完成报告

完成后创建：`✅运维工程师工作台-数据校验完成-2025-11-20.md`

**架构师期待你的成果！** 💪

