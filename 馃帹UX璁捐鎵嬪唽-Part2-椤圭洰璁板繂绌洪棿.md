# 🎨 UX设计手册 Part 2：项目记忆空间详细解析

**目标**: 详细解析项目记忆空间的实现逻辑和UX设计方案  
**读者**: UX/UI设计师  
**生成时间**: 2025-11-19

---

## 💡 功能概述

**项目记忆空间是什么？**

项目记忆空间是一个**跨会话的知识管理系统**，可以：
- 📝 记录重要知识和经验
- 🏛️ 自动记录架构决策（ADR格式）
- 🐛 自动记录问题和解决方案
- 🔗 管理记忆之间的关联关系
- 🔍 语义搜索历史记忆
- 📚 跨会话知识继承（新会话自动获取历史知识）

**核心价值**：
- ✅ 知识沉淀：重要知识不会丢失
- ✅ 经验复用：避免重复犯错
- ✅ 团队协作：知识在团队间共享
- ✅ AI增强：新会话可以继承历史经验

---

## 🏗️ 实现架构

### 三层存储架构

```
┌─────────────────────────────────────────────┐
│  ProjectMemoryService（服务层）              │
│  ↓                                           │
│  ├─ 本地SQLite（project_memories表）         │
│  │    → 快速查询、关系管理                   │
│  │                                           │
│  ├─ Session Memory MCP（会话记忆）           │
│  │    → 当前会话的临时记忆                   │
│  │                                           │
│  └─ Ultra Memory Cloud MCP（长期记忆）       │
│       → 语义搜索、跨项目共享                  │
└─────────────────────────────────────────────┘
```

### 4种记忆类型

```javascript
// 1. session记忆 - 会话级别（当前对话有效）
{
  memory_type: "session",
  lifetime: "当前会话",
  storage: "Session Memory MCP",
  use_case: "临时上下文、当前任务状态"
}

// 2. ultra记忆 - 长期记忆（永久保存，可搜索）
{
  memory_type: "ultra",
  lifetime: "永久",
  storage: "Ultra Memory Cloud + SQLite",
  use_case: "重要知识、核心经验、最佳实践"
}

// 3. decision记忆 - 架构决策（ADR格式）
{
  memory_type: "decision",
  lifetime: "永久",
  storage: "decisions表 + Ultra Memory",
  use_case: "技术决策、架构选择"
}

// 4. solution记忆 - 解决方案（问题-方案配对）
{
  memory_type: "solution",
  lifetime: "永久",
  storage: "solutions表 + Ultra Memory",
  use_case: "问题解决经验"
}
```

### 5种记忆分类

```javascript
// 1. architecture - 架构相关
// 2. problem - 问题相关
// 3. solution - 解决方案相关
// 4. decision - 决策相关
// 5. knowledge - 一般知识
```

---

## 📊 数据模型

### 记忆对象（Memory）

```json
{
  "id": "MEM-a1b2c3d4",
  "project_id": "TASKFLOW",
  "memory_type": "ultra",
  "external_memory_id": "ultra-xxxxxxxxxxxx",
  "category": "solution",
  "title": "解决Dashboard Tab切换失败问题",
  "content": "问题是JavaScript模板字符串反引号未转义...",
  "context": {
    "issue_id": "ISS-001",
    "severity": "high",
    "component_id": "dashboard-ui"
  },
  "tags": ["dashboard", "javascript", "tab", "bug-fix"],
  "related_tasks": ["REQ-009-A"],
  "related_issues": ["ISS-001"],
  "importance": 8,
  "created_by": "AI Architect",
  "created_at": "2025-11-18T22:30:00Z",
  "updated_at": "2025-11-18T22:30:00Z"
}
```

### ADR（架构决策记录）对象

```json
{
  "id": "DEC-a1b2c3d4",
  "project_id": "TASKFLOW",
  "title": "采用Monorepo架构",
  "context": "项目规模扩大，需要管理多个包...",
  "decision": "使用pnpm workspace实现Monorepo",
  "consequences": "提高代码复用性，简化依赖管理",
  "alternatives": ["Lerna", "Nx", "Turborepo"],
  "status": "accepted",
  "decided_by": "AI Architect",
  "decided_at": "2025-11-18T20:00:00Z"
}
```

### 问题-解决方案配对

```json
{
  "problem": {
    "id": "ISS-001",
    "title": "Dashboard Tab切换失败",
    "description": "点击Tab按钮无反应",
    "severity": "high"
  },
  "solution": {
    "id": "SOL-001",
    "title": "修复JavaScript模板字符串转义",
    "description": "在Python f-string中添加反斜杠转义",
    "steps": [
      "定位错误位置（templates.py第1523行）",
      "添加反斜杠转义反引号",
      "重启Dashboard测试"
    ],
    "tools_used": ["node -c", "debug_tab_issue.py"]
  }
}
```

### 记忆关系对象

```json
{
  "id": "REL-a1b2c3d4",
  "source_memory_id": "MEM-solution-001",
  "target_memory_id": "MEM-problem-001",
  "relation_type": "solved-by",
  "strength": 1.0,
  "created_at": "2025-11-18T22:30:00Z"
}
```

---

## 🔌 API接口详解

### API 1: 创建记忆

```http
POST /api/projects/TASKFLOW/memories
Content-Type: application/json

{
  "memory_type": "ultra",
  "category": "knowledge",
  "title": "React Hooks 最佳实践",
  "content": "使用useCallback优化性能，避免不必要的重渲染...",
  "tags": ["react", "hooks", "performance"],
  "importance": 7,
  "created_by": "Full-stack Engineer"
}
```

**返回**：
```json
{
  "success": true,
  "memory": { /* 完整记忆对象 */ }
}
```

### API 2: 检索记忆（语义搜索）

```http
GET /api/projects/TASKFLOW/memories?query=如何优化性能&limit=10
```

**功能**：
- 支持自然语言查询
- 自动语义匹配
- 返回相关度排序的结果

### API 3: ADR自动记录

```http
POST /api/projects/TASKFLOW/memories/auto-record/decision
Content-Type: application/json

{
  "title": "采用Monorepo架构",
  "context": "项目规模扩大，需要统一管理多个包...",
  "decision": "使用pnpm workspace实现Monorepo",
  "consequences": "提高代码复用性，简化依赖管理",
  "alternatives": ["Lerna", "Nx", "Turborepo"],
  "decided_by": "AI Architect"
}
```

**后端自动操作**：
1. 格式化为标准ADR格式（Markdown）
2. 保存到`decisions`表
3. 创建decision类型的记忆
4. 存储到Ultra Memory Cloud
5. 发射`decision.made`事件到事件流

### API 4: 问题解决方案自动记录

```http
POST /api/projects/TASKFLOW/memories/auto-record/solution
Content-Type: application/json

{
  "problem_title": "Dashboard Tab切换失败",
  "problem_description": "点击Tab按钮无反应，JavaScript错误",
  "solution_title": "修复模板字符串转义",
  "solution_description": "在Python f-string中转义反引号",
  "solution_steps": [
    "定位错误位置",
    "添加反斜杠转义",
    "测试验证"
  ],
  "tools_used": ["node -c", "debug_tab_issue.py"],
  "severity": "high",
  "component_id": "dashboard-ui"
}
```

**后端自动操作**：
1. 保存问题到`issues`表
2. 保存解决方案到`solutions`表
3. 创建problem类型的记忆
4. 创建solution类型的记忆
5. 建立"solved-by"关系
6. 发射`issue.solved`事件

### API 5: 跨会话知识继承

```http
GET /api/projects/TASKFLOW/knowledge/inherit?context=准备重构Dashboard&limit=20
```

**返回**：
```json
{
  "success": true,
  "project_id": "TASKFLOW",
  "decisions": [
    { /* ADR 1 */ },
    { /* ADR 2 */ }
  ],
  "solutions": [
    { /* 解决方案 1 */ },
    { /* 解决方案 2 */ }
  ],
  "important_knowledge": [
    { /* 重要知识 1 */ }
  ],
  "recent_memories": [
    { /* 最近记忆 1 */ }
  ],
  "related_memories": [
    { /* 相关记忆 1 */ }
  ],
  "total_inherited": 15,
  "usage_hint": "使用这些知识帮助新会话快速了解项目历史"
}
```

**用途**：
- 新架构师接手项目时调用
- 获取项目的所有重要历史知识
- 避免重复决策和犯错

---

## 🎨 UX设计建议

### 主页面布局