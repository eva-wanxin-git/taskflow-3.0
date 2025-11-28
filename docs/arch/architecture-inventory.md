# 📋 任务所·Flow v1.7 - 项目架构清单

**创建时间**：2025-11-19  
**架构师**：AI Architect (Expert Level)  
**扫描范围**：完整项目（420个文件，173个Python文件）  
**数据库**：3个主数据库表 + 12个知识库表 + 3个事件表

---

## 项目基本信息

- **项目名称**：任务所·Flow v1.7
- **项目类型**：企业级AI任务协作中枢 + Web Dashboard
- **当前版本**：v1.7.0-alpha
- **完成度**：96.4%（108/112功能已实现）
- **代码仓库**：taskflow-v1.7-from-github
- **核心理念**：用对话开工，用流程收工 - 让AI成为项目的常驻团队
- **最后更新**：2025-11-19
- **团队规模**：适合1-10人团队，3个AI角色协作

---

## 🏗️ 技术栈

### 后端
- **语言**：Python 3.9+
- **框架**：FastAPI 0.104+
- **数据库**：SQLite 3.x
- **数据模型**：Pydantic 2.5+ (类型安全)
- **异步框架**：Uvicorn (ASGI server)
- **API风格**：RESTful API

### 前端
- **框架**：原生JavaScript (无框架依赖)
- **样式**：纯CSS（工业美学设计）
- **服务端渲染**：FastAPI + Jinja2风格模板
- **实时更新**：Service Worker + 版本管理
- **UI风格**：黑白红配色，等宽字体，极简主义

### 数据持久化
- **主数据库**：SQLite (`database/data/tasks.db`)
- **Schema管理**：迁移脚本 (`database/migrations/`)
- **表数量**：18个表（3基础 + 12知识库 + 3事件）
- **备份机制**：自动备份脚本

### 部署
- **容器化**：Docker-ready (Dockerfile存在)
- **云服务**：可部署到本地/云端
- **端口管理**：PortManager智能分配（8870-8880）
- **启动脚本**：`启动Dashboard.bat` / `start_dashboard.py`

---

## 📂 目录结构概览（Monorepo）

```
taskflow-v1.7-from-github/
├── apps/                     # 应用层（可独立部署）
│   ├── api/                  # 后端API服务（FastAPI）
│   │   ├── src/              # API源代码
│   │   ├── database/         # API专用数据库
│   │   └── start_api.py      # API启动入口
│   │
│   ├── dashboard/            # Web Dashboard前端
│   │   ├── src/              # Dashboard源代码
│   │   │   ├── automation/   # 任务管理核心逻辑
│   │   │   └── industrial_dashboard/  # UI组件和API路由
│   │   ├── automation-data/  # 数据存储（96个文件）
│   │   └── start_dashboard.py  # Dashboard启动入口
│   │
│   └── README.md
│
├── packages/                 # 共享代码包
│   ├── core-domain/          # 核心领域模型
│   │   ├── enums/            # 枚举定义（事件类型）
│   │   └── src/services/     # 核心服务（事件、记忆）
│   │
│   └── shared-utils/         # 共享工具
│       ├── port_manager.py   # 端口管理器
│       ├── version_cache_manager.py  # 版本缓存管理
│       ├── token_sync.py     # Token同步
│       └── event_helper.py   # 事件辅助工具
│
├── docs/                     # 文档中心
│   ├── ai/                   # AI System Prompts（12个）
│   │   ├── architect-system-prompt-expert.md  # 架构师AI (8000字)
│   │   ├── fullstack-engineer-system-prompt.md  # 全栈工程师AI (7000字)
│   │   ├── code-steward-system-prompt.md  # 代码管家AI (5000字)
│   │   └── sre-system-prompt.md  # SRE AI (4500字)
│   │
│   ├── arch/                 # 架构文档
│   │   ├── architecture-review.md  # 架构审查报告
│   │   ├── monorepo-structure-taskflow.md  # Monorepo结构
│   │   └── ...
│   │
│   ├── adr/                  # 架构决策记录（ADR）
│   ├── features/             # 功能文档
│   ├── reports/              # 完成报告
│   └── tasks/                # 任务看板

│
├── database/                 # 数据库管理
│   ├── data/
│   │   └── tasks.db          # SQLite主数据库
│   ├── schemas/              # Schema定义
│   │   ├── v1_tasks_schema.sql  # 任务表
│   │   ├── v2_knowledge_schema.sql  # 知识库表（12表）
│   │   ├── v3_events_schema.sql  # 事件表（3表）
│   │   └── v4_enterprise_knowledge_schema.sql
│   ├── migrations/           # 迁移脚本
│   └── seeds/                # 初始数据
│
├── scripts/                  # 工具脚本（84个）
│   ├── 李明收到任务.py          # 任务接收自动化
│   ├── 李明提交完成.py          # 任务提交自动化
│   ├── create_v17_tasks.py   # 任务录入
│   ├── update_dashboard_data_v17.py  # Dashboard数据更新
│   └── ...                   # 大量自动化脚本
│
├── services/                 # 后台服务
│   ├── smart_task_detector.py  # 智能任务检测器
│   ├── task_auto_monitor.py    # 任务自动监控
│   └── task_status_poller.py   # 状态轮询器
│
├── tests/                    # 测试目录
│   ├── e2e/                  # 端到端测试
│   ├── integration/          # 集成测试
│   └── ...
│
├── knowledge/                # 知识库
│   ├── issues/               # 问题记录
│   └── solutions/            # 解决方案
│
├── config/                   # 配置文件
│   └── ports.json            # 端口配置
│
├── README.md                 # 项目入口文档
├── CHANGELOG.md              # 变更日志
└── 启动Dashboard.bat         # Windows一键启动
```

**结构类型**：**企业级Monorepo**
- ✅ 清晰的应用层（apps/）
- ✅ 可复用的包层（packages/）
- ✅ 完整的文档层（docs/）
- ✅ 规范的数据库管理（database/）

---

## 🎯 已发现的应用/服务

### 1. 📊 Web Dashboard（主应用）
- **位置**：`apps/dashboard/`
- **端口**：8877（固定，使用版本缓存管理）
- **入口**：`start_dashboard.py`
- **核心模块**：`industrial_dashboard/dashboard.py`（1622行）
- **功能**：
  - 实时任务监控
  - 多模块Tab切换（8个模块）
  - 事件流可视化
  - Token余量显示
  - AI提示词加载
  - 任务三态流转UI
  - 缓存版本管理
- **技术亮点**：
  - Service Worker智能缓存
  - 无刷新版本更新
  - 工业美学设计
  - 完全无前端框架依赖

### 2. 🔌 API Server
- **位置**：`apps/api/`
- **端口**：8870（可配置）
- **入口**：`start_api.py`
- **状态**：⚠️ 部分实现（40%）
- **已有端点**：
  - 架构师监控API
  - 项目扫描API
  - 知识库查询API
- **待完善**：
  - 完整的RESTful API
  - 数据库集成
  - 认证授权

### 3. 🤖 自动化服务（后台）
- **位置**：`services/`
- **服务列表**：
  - `smart_task_detector.py` - 智能任务检测
  - `task_auto_monitor.py` - 任务自动监控
  - `task_status_poller.py` - 状态轮询
- **运行方式**：独立进程，后台运行

---

## 🧩 核心模块识别

### 业务核心模块

#### 1. 任务管理系统
- **StateManager** (`state_manager.py`, 439行)
  - 任务CRUD操作
  - 状态流转管理
  - SQLite持久化
  - 审查记录管理
  - Worker管理
  
#### 2. 依赖分析引擎
- **DependencyAnalyzer** (`dependency_analyzer.py`)
  - 循环依赖检测（DFS算法）
  - 拓扑排序（Kahn算法）
  - 关键路径分析（CPM）
  - 并行任务分组

#### 3. 任务调度系统
- **TaskScheduler** (`task_scheduler.py`)
  - Worker注册管理
  - 任务负载均衡
  - 能力匹配分配
  - Worker健康检查

#### 4. 事件流系统
- **EventService** (`packages/core-domain/src/services/event_service.py`)
  - 28种事件类型
  - 事件发射和存储
  - 事件追踪和审计
  - 事件统计
  
- **EventHelper** (`packages/shared-utils/event_helper.py`, 670行)
  - 便捷辅助工具
  - 批量操作
  - 事件筛选

#### 5. 项目记忆空间
- **ProjectMemoryService** (`packages/core-domain/src/services/project_memory_service.py`)
  - 记忆创建和查询
  - 语义搜索
  - 记忆管理

### 基础设施模块

#### 1. 版本缓存管理
- **VersionCacheManager** (`packages/shared-utils/version_cache_manager.py`)
  - 自动版本号生成
  - 缓存控制
  - Service Worker集成

#### 2. 端口管理器
- **PortManager** (`packages/shared-utils/port_manager.py`)
  - 智能端口分配
  - 冲突检测
  - 端口预留

#### 3. Token同步
- **TokenSync** (`packages/shared-utils/token_sync.py`)
  - Claude API Token查询
  - 实时同步
  - 余量显示

#### 4. 数据模型层
- **Models** (`models.py`, 231行)
  - Pydantic模型定义
  - 类型安全验证
  - Task/Review/Worker/SystemStatus

---

## 📊 数据库架构

### 主数据库（tasks.db）

#### 核心表（v1 Schema）
1. **tasks** - 任务主表
   - 字段：id, title, description, status, priority, estimated_hours, actual_hours, complexity, assigned_to, metadata
   - 索引：status, priority, assigned_to, created_at
   
2. **task_dependencies** - 任务依赖关系
   - 字段：task_id, dependency_id
   - 外键约束
   
3. **task_completions** - 任务完成详情
   - 字段：task_id, features_implemented, files_created, files_modified, code_lines, actual_hours, notes

#### 知识库表（v2 Schema，12个表）
1. **projects** - 项目管理
2. **components** - 组件管理
3. **issues** - 问题追踪
4. **solutions** - 解决方案库
5. **decisions** - 技术决策（ADR）
6. **knowledge_articles** - 知识文章
7. **tools** - 工具管理
8. **component_tools** - 组件工具关联
9. **deployments** - 部署记录
10. **project_memory** - 项目记忆
11. **conversations** - 对话历史
12. **conversation_messages** - 对话消息

#### 事件系统表（v3 Schema，3个表）
1. **project_events** - 项目事件
   - 28种事件类型
   - 完整事件追踪
   
2. **event_types** - 事件类型定义
   - 预定义18种标准事件
   
3. **event_stats** - 事件统计
   - 实时统计数据

### 数据库统计
- **总表数**：18个
- **总索引数**：15+个
- **外键约束**：完整
- **数据完整性**：✅ 高

---

## 🔧 依赖清单

### Python核心依赖（关键）
```python
fastapi>=0.104.1          # Web框架
uvicorn>=0.24.0           # ASGI服务器
pydantic>=2.5.0           # 数据验证
sqlite3                   # 数据库（内置）
requests>=2.31.0          # HTTP客户端
anthropic                 # Claude API
```

### 开发依赖
```python
pytest                    # 测试框架
pytest-cov                # 覆盖率
black                     # 代码格式化
```

### 无前端依赖
- ✅ 纯JavaScript，无npm/yarn
- ✅ 无构建步骤
- ✅ 无node_modules

---

## ⚙️ 配置概览

### 环境变量
- `ANTHROPIC_API_KEY` - Claude API密钥（Token同步）
- `DATABASE_PATH` - 数据库路径（可选）
- `DASHBOARD_PORT` - Dashboard端口（可选）

### 端口分配
```json
{
  "dashboard": 8877,    # Web Dashboard（固定）
  "api": 8870,          # API Server
  "backup_ports": [8871, 8872, 8873, 8874, 8875, 8876]
}
```

### 配置文件
- `config/ports.json` - 端口配置
- `automation-data/dashboard_version.json` - 版本信息
- `automation-data/versions.json` - 版本历史

---

## 📈 代码规模统计

### 文件统计
- **总文件数**：420个
- **Python文件**：173个
- **Markdown文档**：80+个
- **JSON配置**：16个
- **SQL Schema**：5个

### 代码行数估算
```
后端Python:      ~15,000行
  - automation/: ~5,000行
  - industrial_dashboard/: ~8,000行
  - packages/: ~2,000行

前端JavaScript: ~3,000行（嵌入在templates中）
SQL Schema:      ~800行
文档:            ~50,000字
脚本工具:        ~10,000行
─────────────────────────────
总计:           ~28,000行代码 + 大量文档
```

### 功能模块数
- **已实现功能**：108个（细粒度）
- **部分实现**：4个
- **总功能点**：112个

---

## 🎨 架构特点

### 优势 ✅

1. **清晰的分层架构**
   - 应用层（apps/）
   - 领域层（packages/core-domain/）
   - 基础设施层（packages/shared-utils/）
   - 依赖方向正确：apps → packages

2. **Monorepo最佳实践**
   - 代码复用高效
   - 模块边界清晰
   - 统一的版本管理

3. **强类型系统**
   - Pydantic模型定义完整
   - 枚举类型规范
   - 类型安全保障

4. **完整的知识图谱**
   - 18个数据库表
   - 任务-知识-事件-决策全关联
   - 可追溯性强

5. **自动化程度高**
   - 84个工具脚本
   - 智能检测器
   - 自动监控服务

6. **文档体系完整**
   - 12个AI System Prompts
   - 80+个完成报告
   - 6个架构文档
   - ADR决策记录

### 风险点 ⚠️

1. **SQLite并发限制**
   - 单写锁机制
   - 高并发场景（QPS>100）可能锁表
   - 建议：添加连接池和重试机制

2. **测试覆盖不足**
   - 单元测试 <10%
   - 核心业务逻辑缺少测试
   - 风险：重构困难

3. **API服务未完整实现**
   - apps/api/ 仅40%完成
   - 缺少完整的RESTful端点
   - 影响：无法独立部署API

4. **代码重复**
   - 多个脚本有相似逻辑
   - 可提取共用函数

5. **文档过载**
   - 根目录50+个markdown文件
   - 建议：整理到docs/目录

---

## 💡 技术债务初步印象

### 🔴 Critical（需立即处理）
1. ✅ 测试覆盖率提升（当前<10%，目标80%+）
2. ✅ SQLite并发优化（添加连接池）
3. ✅ API服务完整实现（apps/api/补全）

### 🟡 High（建议2周内处理）
1. ✅ 代码重复消除（提取共用函数）
2. ✅ 文档整理（根目录→docs/）
3. ✅ 错误处理标准化

### 🟢 Medium（可延后）
1. ✅ 性能优化（数据库查询）
2. ✅ 日志系统完善
3. ✅ 配置管理集中化

---

## 🎯 下一步行动建议

### 优先深入审查（Phase 2）
1. **核心业务逻辑**：
   - `apps/dashboard/src/automation/state_manager.py`
   - `apps/dashboard/src/automation/dependency_analyzer.py`
   - `apps/dashboard/src/automation/task_scheduler.py`

2. **数据库层**：
   - `database/schemas/` - 所有Schema
   - `database/migrations/` - 迁移脚本

3. **前端核心**：
   - `apps/dashboard/src/industrial_dashboard/dashboard.py`
   - `apps/dashboard/src/industrial_dashboard/templates.py`

### 建议重点关注
- ✅ 性能瓶颈识别（SQLite并发）
- ✅ 安全漏洞扫描（无认证/授权）
- ✅ 架构债务评估（API服务补全）
- ✅ 测试策略设计（提升覆盖率）

### 预计Token消耗
- **Phase 2深度审查**：50k-70k tokens
- **Phase 3文档生成**：20k tokens
- **Phase 4任务拆解**：15k tokens
- **总计**：85k-105k tokens

---

## 📊 当前项目状态快照

### 数据库实际数据（2025-11-19）
```sql
SELECT status, COUNT(*) FROM tasks GROUP BY status;

结果：
cancelled      4个  (7.4%)
completed     25个  (46.3%)
in_progress    1个  (1.9%)
pending       24个  (44.4%)
──────────────────
总计：        54个任务
```

### 完成度分析
- **整体功能完成度**：96.4% (108/112)
- **任务完成度**：46.3% (25/54)
- **核心功能**：100%可用
- **Dashboard**：100%运行正常

### 最近完成的重大功能
1. ✅ REQ-001 - 缓存彻底解决方案
2. ✅ REQ-009 - 任务三态流转系统
3. ✅ REQ-010 - 项目全局事件流系统（92%）
4. ✅ REQ-011 - Dashboard动态进度计算
5. ✅ REQ-002 - 项目记忆空间
6. ✅ REQ-003 - 对话历史库
7. ✅ REQ-006 - Token实时同步

---

## 🔗 相关文档

### 已生成文档
- [项目入口](../../README.md)
- [变更日志](../../CHANGELOG.md)
- [Monorepo结构](monorepo-structure-taskflow.md)
- [架构审查报告](architecture-review.md)（待生成）
- [重构计划](refactor-plan.md)（待生成）
- [任务看板](../tasks/task-board.md)

### AI文档索引
- [架构师AI Prompt](../ai/architect-system-prompt-expert.md) - 8000字
- [全栈工程师AI](../ai/fullstack-engineer-system-prompt.md) - 7000字
- [代码管家AI](../ai/code-steward-system-prompt.md) - 5000字
- [SRE AI](../ai/sre-system-prompt.md) - 4500字

---

**扫描完成时间**：2025-11-19  
**扫描深度**：完整项目扫描（420文件）  
**建议Review周期**：每2周一次  
**下次审查重点**：性能优化 + 测试覆盖率 + API服务补全

---

## 📝 架构师笔记

### 项目整体评价：⭐⭐⭐⭐ (8/10)

**一句话总结**：这是一个结构清晰、文档完善、自动化程度高的企业级任务管理系统，核心功能已完整实现，但测试覆盖不足且API服务需补全。

**最大优势**：完整的AI协作体系 + 清晰的Monorepo架构 + 强大的事件流系统

**最大风险**：SQLite并发限制 + 测试覆盖率低 + API服务未完整

**最大机会**：完善API服务后可独立部署，形成完整的微服务架构

---

🎉 **架构清单创建完成！接下来将进行深度代码审查...**
