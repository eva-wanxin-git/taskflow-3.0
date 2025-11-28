# 任务所 2.1 - 即插即用使用指南

**版本**: 2.1  
**类型**: 企业级AI协作系统 + 项目脚手架

---

## 🎯 核心理念

**任务所 = GitHub Copilot + Linear + Notion 的完整整合**

- 📊 **自动项目结构化**: 将任何项目整理为企业级Monorepo
- 🧠 **知识图谱**: 10张表的结构化知识库
- 🤖 **AI协作**: 4个AI角色完整工作台
- 💾 **MCP记忆系统**: 访问10501条历史记忆

---

## 🚀 3步即插即用

### 步骤1: 复制任务所到项目

```bash
# 解压任务所2.1
tar -xzf 任务所2.1-更新版-20251125-132401.tar.gz

# 复制到您的项目目录
cp -r taskflow-v1-2/taskflow-v1-2 /path/to/your-project/taskflow
```

### 步骤2: 在项目目录中初始化

```bash
cd /path/to/your-project
./taskflow/🚀即插即用-初始化项目.sh
```

**自动执行**:
1. ✅ 检测项目类型（Python/Node.js/Go/Rust）
2. ✅ 创建企业级Monorepo结构
3. ✅ 移动现有文件到标准目录
4. ✅ 初始化知识库数据库（10张表）
5. ✅ 扫描项目生成组件清单
6. ✅ 自动分配端口（8841-8899）
7. ✅ 创建启动脚本

### 步骤3: 启动Dashboard

```bash
./.taskflow/启动Dashboard.sh
```

访问: `http://localhost:8841`（端口自动分配）

---

## 📂 初始化后的项目结构

```
your-project/
├── apps/                    # 🎯 应用层（自动创建）
│   ├── api/                # 后端API
│   ├── web/                # 前端Web
│   ├── admin/              # 管理后台
│   └── worker/             # 后台任务
│
├── packages/                # 🧩 共享代码包
│   ├── core-domain/        # 🏛️ 领域模型
│   ├── infra/              # 🔌 基础设施
│   ├── ui-kit/             # 🎨 UI组件库
│   └── shared-utils/       # 🧰 工具函数
│
├── docs/                    # 📖 文档中心
│   ├── product/            # 产品文档
│   ├── arch/               # 架构文档
│   ├── adr/                # 架构决策记录
│   └── api/                # API文档
│
├── ops/                     # 🚀 运维部署
│   ├── infra/              # IaC配置
│   ├── k8s/                # Kubernetes
│   ├── docker/             # Docker配置
│   └── ci-cd/              # CI/CD
│
├── knowledge/               # 💎 知识库
│   ├── issues/             # 问题记录
│   ├── solutions/          # 解决方案
│   ├── patterns/           # 设计模式
│   └── lessons-learned/    # 经验教训
│
├── database/                # 🗄️ 数据库
│   ├── migrations/         # 迁移脚本
│   ├── schemas/            # Schema定义
│   └── knowledge-db/       # 知识库DB
│
├── .taskflow/               # ⚙️ 任务所配置（自动创建）
│   ├── knowledge.db        # 知识图谱数据库
│   ├── dashboard_port      # Dashboard端口
│   ├── project_id.txt      # 项目UUID
│   ├── 启动Dashboard.sh     # 启动脚本
│   └── logs/               # 日志目录
│
└── taskflow/                # 任务所核心代码
    ├── dashboard-test-8831/
    ├── apps/
    └── packages/
```

---

## 🗄️ 知识库数据库（10张核心表）

初始化后自动创建：

### 项目管理
1. **projects** - 项目主表
2. **components** - 组件/模块
3. **environments** - 环境配置

### 知识管理
4. **issues** - 问题库（核心！）
5. **solutions** - 解决方案
6. **decisions** - 架构决策(ADR)
7. **knowledge_articles** - 知识文章

### 记忆系统
8. **memory_layers** - 记忆层级（短期/中期/长期）
9. **interaction_events** - 交互事件
10. **deployments** - 部署记录

---

## 🧠 MCP记忆系统集成

### 自动连接
初始化后自动连接到您的MCP记忆系统：

**Session Memory** (短期记忆)
- API: `http://13.158.83.99:4000`
- 功能: 任务管理、会话跟踪

**Ultra Memory** (长期记忆)
- 方式: 直连AWS DynamoDB
- 记忆数: 10501条
- Namespace: wanxin_ultra

### 自动记忆流程
```
对话 → 交互事件 → 自动分析 → 
  ├─ 重要问题 → issues表
  ├─ 解决方案 → solutions表
  ├─ 架构决策 → decisions表
  └─ 自动提炼 → Ultra Memory长期记忆
```

---

## 🤖 AI协作功能

### Dashboard包含
- 🏛️ 架构师工作台（7个Tab）
- 👨‍💻 全栈工程师工作台（5个Tab）
- 🔧 运维工程师模块
- 🤖 Noah代码管家

### 自动化功能
- 📡 23种自动记忆触发
- 🔄 任务自动派发
- 📊 代码质量实时扫描
- 🎯 智能知识推荐

---

## 📋 多项目管理

### 全局注册表
位置: `~/.taskflow/projects.json`

可管理多个项目，每个独立端口：
```
项目A: http://localhost:8841
项目B: http://localhost:8842
项目C: http://localhost:8843
```

### 查看所有项目
```bash
cat ~/.taskflow/projects.json | python3 -m json.tool
```

---

## 🔧 配置文件

### .taskflow目录
```
.taskflow/
├── knowledge.db          # 知识图谱（SQLite）
├── project_id.txt        # 项目UUID
├── dashboard_port        # Dashboard端口号
├── api_port             # API端口号
├── 启动Dashboard.sh      # 启动脚本
├── logs/                # 日志
│   └── api.log
└── README.md            # 说明文档
```

---

## 💡 使用场景

### 场景1: 全新项目
```bash
mkdir my-awesome-project
cd my-awesome-project
git init
../taskflow/🚀即插即用-初始化项目.sh
```

### 场景2: 现有项目
```bash
cd existing-project
../taskflow/🚀即插即用-初始化项目.sh
# 现有文件自动移动到标准目录
```

### 场景3: 多项目管理
```bash
# 项目A
cd project-a
../taskflow/🚀即插即用-初始化项目.sh  # 端口8841

# 项目B  
cd project-b
../taskflow/🚀即插即用-初始化项目.sh  # 端口8842（自动避开）

# 同时运行多个Dashboard
```

---

## ✅ 验收清单

初始化完成后检查：

- [ ] 标准目录结构已创建（apps/packages/docs/ops/knowledge等）
- [ ] `.taskflow/knowledge.db` 数据库已创建
- [ ] `.taskflow/启动Dashboard.sh` 脚本可执行
- [ ] `~/.taskflow/projects.json` 已注册项目
- [ ] Dashboard可以正常启动
- [ ] 能访问 `http://localhost:8841`（或分配的端口）
- [ ] Dashboard中可以看到项目信息
- [ ] MCP记忆系统连接正常

---

## 🎊 特性亮点

### 即插即用
- ✅ 3步启动，零配置
- ✅ 自动检测项目类型
- ✅ 自动分配端口，避免冲突

### 企业级结构
- ✅ 标准Monorepo布局
- ✅ 10张表知识图谱
- ✅ 完整文档体系

### AI深度集成
- ✅ MCP记忆系统（10501条）
- ✅ 4个AI角色工作台
- ✅ 23种自动记忆触发

### 多项目支持
- ✅ 独立端口和数据库
- ✅ 全局注册表管理
- ✅ 可同时运行多个项目

---

## 📞 技术支持

遇到问题查看：
- `.taskflow/logs/api.log` - API日志
- Dashboard中的错误提示
- 知识库中的问题记录

---

**创建时间**: 2025-11-25  
**版本**: 2.1  
**记忆系统**: 已集成（10501条历史记忆可用）


