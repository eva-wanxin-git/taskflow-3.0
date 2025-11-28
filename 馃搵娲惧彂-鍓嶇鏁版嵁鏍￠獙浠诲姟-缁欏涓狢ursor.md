# 📋 前端数据校验任务派发 - 给多个Cursor

**生成时间**: 2025-11-20  
**派发者**: 架构师AI  
**任务目标**: 将前端硬编码数据替换为真实数据

---

## 🎯 总体策略

### 原则
1. **有真实数据的** → 立即从JSON文件或数据库读取并填充
2. **没有数据的** → 先留空或显示"待实现"占位符
3. **硬编码逻辑** → 全部改为动态数据加载

### 数据源
```
✅ 有真实数据:
  - v17-complete-features.json (132个已实现功能)
  - partial-features.json (24个部分实现)
  - project-issues.json (15个问题)
  - architecture-suggestions.json (12个建议)
  - database/data/tasks.db (任务数据)
  - project_events表 (事件数据)
  - conversations表 (对话数据)
  - project_memory表 (记忆数据)

❌ 暂无数据:
  - 代码审查结果
  - 技术文档索引
  - 运维日志
  - Bug看板
  - 代码清单
  - 系统监控数据
```

---

## 📋 任务分配（7个模块，分配给7个Cursor窗口）

### Cursor #1: 项目透视塔（4个Tab）⭐⭐⭐⭐⭐

**文件**: `dashboard-test/index.html` (行6058-6383)  
**工时**: 2小时  
**优先级**: P0 Critical

**任务清单**:
- [ ] Tab 1: 已实现功能（132个）
  - 当前：硬编码少量示例
  - 目标：从 `v17-complete-features.json` 读取全部132个
  - 动作：循环生成132个功能卡片HTML

- [ ] Tab 2: 部分实现（24个）
  - 当前：空占位
  - 目标：从 `partial-features.json` 读取全部24个
  - 动作：生成24个部分实现卡片（带进度条）

- [ ] Tab 3: 问题清单（15个）
  - 当前：硬编码少量示例
  - 目标：从 `project-issues.json` 读取全部15个
  - 动作：生成15个问题卡片（按优先级排序）

- [ ] Tab 4: 架构建议（12条）
  - 当前：硬编码少量示例
  - 目标：从 `architecture-suggestions.json` 读取全部12条
  - 动作：生成12个建议卡片（含采纳按钮）

**数据源**:
```
apps/dashboard/automation-data/
├── v17-complete-features.json     ✅ 132个
├── partial-features.json          ✅ 24个
├── project-issues.json            ✅ 15个
└── architecture-suggestions.json  ✅ 12个
```

**输出**: 更新后的 `index.html` 项目透视塔部分

---

### Cursor #2: 待开发任务池（2个Tab）⭐⭐⭐⭐

**文件**: `dashboard-test/index.html` (待开发任务池模块)  
**工时**: 1.5小时  
**优先级**: P1

**任务清单**:
- [ ] Tab 1: 用户需求（~8个REQ任务）
  - 数据源：`database/data/tasks.db` → `SELECT * FROM tasks WHERE id LIKE 'REQ-%' AND status IN ('pending', 'in_progress')`
  - 动作：查询数据库，生成需求卡片

- [ ] Tab 2: 架构师建议任务（~15个）
  - 数据源：`database/data/tasks.db` → `SELECT * FROM tasks WHERE assigned_to='fullstack-engineer' AND status='pending'`
  - 动作：查询数据库，生成任务卡片

**数据源**: `database/data/tasks.db` ✅ (真实数据库)

**输出**: 更新后的待开发任务池HTML

---

### Cursor #3: 架构师工作台（3个Tab）⭐⭐⭐⭐

**文件**: `dashboard-test/index.html` (架构师模块)  
**工时**: 1.5小时  
**优先级**: P1

**任务清单**:
- [ ] Tab 1: 事件流（架构决策事件）
  - 数据源：`database/data/tasks.db` → `SELECT * FROM project_events WHERE category='architecture' OR category='decision' ORDER BY occurred_at DESC LIMIT 100`
  - 动作：查询数据库，生成事件时间轴

- [ ] Tab 2: 认命指令（静态内容）
  - 当前：可能已有
  - 动作：验证内容是否完整

- [ ] Tab 3: 对话历史
  - 数据源：`database/data/tasks.db` → `SELECT * FROM conversations WHERE project_id='TASKFLOW' AND metadata LIKE '%architect%' ORDER BY created_at DESC`
  - 动作：查询数据库，生成对话卡片

**数据源**: `project_events表` ✅, `conversations表` ✅

**输出**: 更新后的架构师工作台HTML

---

### Cursor #4: 全栈工程师工作台（5个Tab）⭐⭐⭐⭐⭐

**文件**: `dashboard-test/index.html` (全栈工程师模块)  
**工时**: 2.5小时  
**优先级**: P0

**任务清单**:
- [ ] Tab 1: 事件流（开发事件）
  - 数据源：`project_events表` WHERE `category='development'`
  - 动作：查询并生成事件列表

- [ ] Tab 2: 任务看板（43个任务，3列）
  - 数据源：`tasks表` WHERE `project_id='TASKFLOW'` 按status分组
  - 动作：生成看板布局（pending / in_progress / completed）

- [ ] Tab 3: 代码审查（15个审查项）
  - 数据源：❌ 暂无
  - 动作：显示占位文本"待实现 - 需要 GET /api/code-reviews"

- [ ] Tab 4: 技术文档（68篇）
  - 数据源：❌ 暂无
  - 动作：显示占位文本"待实现 - 需要 GET /api/documents"

- [ ] Tab 5: 对话历史
  - 数据源：`conversations表` WHERE `role='fullstack-engineer'`
  - 动作：查询并生成对话列表

**数据源**: 
- ✅ project_events表
- ✅ tasks表  
- ✅ conversations表
- ❌ 代码审查（待API）
- ❌ 文档索引（待API）

**输出**: 更新后的全栈工程师工作台HTML

---

### Cursor #5: 运维工程师工作台（4个Tab）⭐⭐⭐

**文件**: `dashboard-test/index.html` (运维工程师模块)  
**工时**: 2小时  
**优先级**: P1

**任务清单**:
- [ ] Tab 1: 运维日志（847条）
  - 数据源：❌ 暂无（需要系统日志或日志表）
  - 动作：显示占位文本"待实现 - 需要 GET /api/logs/operations"

- [ ] Tab 2: Bug看板（3个Bug）
  - 数据源：`issues表` WHERE `type='bug'`（如果表有type字段）
  - 动作：查询数据库或显示占位

- [ ] Tab 3: 系统状态（6个服务）
  - 数据源：❌ 暂无（需要监控数据）
  - 动作：显示占位文本"待实现 - 需要 GET /api/system/health"

- [ ] Tab 4: 知识库（128篇）
  - 数据源：`knowledge_articles表`
  - 动作：`SELECT * FROM knowledge_articles WHERE project_id='TASKFLOW'`

**数据源**: 
- ✅ knowledge_articles表
- ⚠️ issues表（可能有）
- ❌ 运维日志（待API）
- ❌ 系统监控（待API）

**输出**: 更新后的运维工程师工作台HTML

---

### Cursor #6: Noah代码管家（4个Tab）⭐⭐⭐

**文件**: `dashboard-test/index.html` (Noah代码管家模块)  
**工时**: 1.5小时  
**优先级**: P1

**任务清单**:
- [ ] Tab 1: 任务队列（12个任务）
  - 数据源：`tasks表` WHERE `assigned_to='noah'`
  - 动作：查询并生成任务列表

- [ ] Tab 2: 代码清单（45个文件）
  - 数据源：❌ 暂无
  - 动作：显示占位文本"待实现 - 需要 GET /api/code/inventory"

- [ ] Tab 3: 代码审查清单
  - 数据源：❌ 暂无
  - 动作：显示占位文本

- [ ] Tab 4: 提示词模板（静态）
  - 数据源：`docs/ai/code-steward-system-prompt.md`
  - 动作：验证内容或读取文件

**数据源**: 
- ✅ tasks表
- ❌ 代码清单（待API）
- ❌ 代码审查（待API）

**输出**: 更新后的Noah代码管家HTML

---

### Cursor #7: 实时脉动系统（3个Tab）⭐⭐

**文件**: `dashboard-test/index.html` (实时脉动模块)  
**工时**: 1小时  
**优先级**: P2

**任务清单**:
- [ ] Tab 1: 系统事件（实时事件流）
  - 数据源：`project_events表` 最新100条
  - 动作：`SELECT * FROM project_events WHERE project_id='TASKFLOW' ORDER BY occurred_at DESC LIMIT 100`

- [ ] Tab 2: 项目脉搏（实时统计）
  - 数据源：❌ 暂无
  - 动作：显示占位文本"待实现 - 需要 GET /api/pulse/realtime"

- [ ] Tab 3: 协作链（AI协作可视化）
  - 数据源：❌ 暂无
  - 动作：显示占位文本"待实现 - 需要 GET /api/collaboration/chain"

**数据源**: 
- ✅ project_events表
- ❌ 实时脉搏（待API）
- ❌ 协作链（待API）

**输出**: 更新后的实时脉动系统HTML

---

## 🛠️ 统一提示词模板

给每个Cursor的标准提示词格式：

```markdown
你好！我是架构师AI，派发给你一个前端数据校验任务。

## 🎯 你的任务

**负责模块**: [模块名称]
**文件位置**: dashboard-test/index.html (行[开始]-[结束])
**工时预估**: [X]小时
**优先级**: [P0/P1/P2]

## 📊 你需要做什么

### 第1步：检查当前状态（20分钟）

1. 打开 `dashboard-test/index.html`
2. 找到你负责的模块（搜索关键词：[模块关键词]）
3. 检查每个Tab的数据：
   - 是硬编码的HTML？ → 需要替换
   - 是空占位？ → 需要填充
   - 已经动态加载？ → 验证数据源

### 第2步：准备数据源（30分钟）

**你的数据源清单**:

✅ 有真实数据：
[列出可用的JSON文件或数据库表]

❌ 暂无数据：
[列出需要API但还没有的]

对于有真实数据的：
- Python读取JSON: `json.load(open('apps/dashboard/automation-data/xxx.json'))`
- SQLite查询: `SELECT * FROM xxx WHERE ...`

### 第3步：更新HTML（1-1.5小时）

**方式A**: 直接生成完整HTML（推荐用于少量数据）
- 读取JSON文件
- 用Python生成HTML字符串
- 替换到index.html对应位置

**方式B**: 添加JavaScript动态加载（推荐用于大量数据）
- 在HTML中添加 `<script>` 标签
- 用fetch或XMLHttpRequest读取JSON
- 用JavaScript渲染DOM

### 第4步：验证效果（10分钟）

1. 刷新浏览器: `Ctrl+Shift+R` (Windows)
2. 检查数据是否正确显示
3. 检查数字是否匹配
4. 检查Tab切换是否正常

### 第5步：提交报告（10分钟）

生成完成报告：`✅[模块名]-数据校验完成-2025-11-20.md`

包含：
- 修改了哪些地方
- 数据来自哪里
- 遇到的问题
- 验证结果截图

## 📝 你的详细任务

[每个Cursor的具体任务详情见下方对应章节]

## ⚠️ 注意事项

1. **保持样式一致**: 使用现有的CSS类，不要自己创建新样式
2. **数据格式统一**: 参考已有的HTML结构
3. **错误处理**: 数据读取失败时显示友好提示
4. **备份文件**: 修改前先备份: `cp index.html index.html.backup-[你的名字]-[时间]`

## 🚀 开始工作

当你准备好了，说"我接受任务 - [模块名]"，然后开始执行！

如有问题，随时在文件顶部添加注释告诉架构师。

加油！💪
```

---

## 📋 详细任务清单（给7个Cursor）

### 🔍 Cursor #1: 项目透视塔

**提示词文件**: `📋Cursor-1-项目透视塔.md`

```markdown
# Cursor #1: 项目透视塔数据校验任务

## 🎯 你的任务

**负责模块**: 项目透视塔  
**文件位置**: dashboard-test/index.html (行6058-6383)  
**Tab数量**: 4个  
**工时预估**: 2小时  
**优先级**: P0 Critical ⭐⭐⭐⭐⭐

---

## 📊 Tab 1: 已实现功能（132个）

### 当前状态
- 硬编码了少量示例功能卡片
- 显示"已实现功能（132项）"但实际只有几个示例

### 数据源
```
文件: apps/dashboard/automation-data/v17-complete-features.json
内容: 132个已实现功能
格式: {
  "implemented": [
    {
      "id": "INFRA-001",
      "name": "SQLite数据库持久化",
      "type": "基础设施",
      "file": "database/data/tasks.db",
      "version": "v1.0",
      "completion": 1.0
    },
    ...
  ]
}
```

### 你需要做什么

1. **读取JSON文件**:
```python
import json
with open('apps/dashboard/automation-data/v17-complete-features.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
features = data['implemented']  # 132个
```

2. **按类别分组**:
```python
categories = {}
for feat in features:
    cat = feat['type']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(feat)
```

3. **生成HTML**（每个类别一个大卡片）:
```html
<div class="feature-module">
    <div class="module-header-content">
        <div>
            <div class="module-title-text">{类别名称}</div>
            <div class="completeness-bar">
                <span>完整度</span>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 95%"></div>
                </div>
                <span>95%</span>
            </div>
        </div>
    </div>
    <div class="module-meta">
        <span>📂 {主要目录}</span>
        <span>📄 {文件数}个文件</span>
    </div>
    <div class="module-features">
        {循环生成feature-item}
        <div class="feature-item">
            <div class="feature-check"></div>
            <span>{功能名称}</span>
            <span class="feature-percentage">100%</span>
        </div>
    </div>
</div>
```

4. **替换到HTML**:
找到 `<!-- Tab 1: 已实现功能 -->` 部分，替换内容

---

## 📊 Tab 2: 部分实现（24个）

### 当前状态
- 空占位："24个部分实现的功能"

### 数据源
```
文件: apps/dashboard/automation-data/partial-features.json
内容: 24个部分实现功能
格式: {
  "partial_features": [
    {
      "id": "PARTIAL-001",
      "name": "REQ-010-D 事件监听器",
      "category": "事件系统",
      "progress": 60,
      "completed_parts": ["事件类型定义", ...],
      "missing_parts": ["自动化监听器", ...],
      "estimated_hours": 2.0,
      "priority": "P1"
    },
    ...
  ]
}
```

### 你需要做什么

生成24个功能卡片，格式：

```html
<div class="feature-module">
    <div class="module-header-content">
        <div>
            <div class="module-title-text">{功能名称}</div>
            <div class="completeness-bar">
                <span>完整度</span>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%"></div>
                </div>
                <span>{progress}%</span>
            </div>
        </div>
    </div>
    <div class="module-meta">
        <span>📂 {路径}</span>
        <span>⏱️ 预估: {estimated_hours}h</span>
        <span class="issue-priority {priority}">{priority}</span>
    </div>
    <div class="module-features">
        <div style="margin-bottom: 12px; color: var(--noir-steel); font-size: 13px; font-weight: 600;">✅ 已完成:</div>
        {循环 completed_parts}
        
        <div style="margin: 16px 0 12px 0; color: var(--status-warning); font-size: 13px; font-weight: 600;">❌ 缺失:</div>
        {循环 missing_parts，样式半透明}
    </div>
</div>
```

---

## 📊 Tab 3: 问题清单（15个）

### 数据源
```
文件: apps/dashboard/automation-data/project-issues.json
```

生成15个问题卡片（当前可能有示例，需要替换为真实数据）

---

## 📊 Tab 4: 架构建议（12条）

### 数据源
```
文件: apps/dashboard/automation-data/architecture-suggestions.json
```

生成12个建议卡片（当前可能有示例，需要替换为真实数据）

---

## ✅ 完成标准

- [ ] 4个Tab全部填充真实数据
- [ ] 数字全部匹配（132/24/15/12）
- [ ] Tab切换正常
- [ ] 刷新浏览器后显示正确
- [ ] 已生成完成报告

---

完成后说"项目透视塔更新完成"，并提交报告！
```

---

## 📝 其他6个Cursor的提示词

我已经在上面的派发清单中列出了所有7个模块的详细任务。

**现在需要你做的**：

1. 打开7个Cursor窗口
2. 每个窗口分配一个模块任务
3. 所有窗口并行工作
4. 完成后汇总结果

---

## 🎯 优先级建议

### 第一批（P0，立即开始）- 3个Cursor
- Cursor #1: 项目透视塔 ⭐⭐⭐⭐⭐
- Cursor #4: 全栈工程师工作台 ⭐⭐⭐⭐⭐
- Cursor #2: 待开发任务池 ⭐⭐⭐⭐

### 第二批（P1，随后开始）- 3个Cursor
- Cursor #3: 架构师工作台 ⭐⭐⭐
- Cursor #5: 运维工程师工作台 ⭐⭐⭐
- Cursor #6: Noah代码管家 ⭐⭐⭐

### 第三批（P2，可选）- 1个Cursor
- Cursor #7: 实时脉动系统 ⭐⭐

---

**总预估工时**: 11.5小时  
**并行执行**: 可缩短到 4-5小时

**完成后**: Dashboard所有模块显示真实数据！🚀

