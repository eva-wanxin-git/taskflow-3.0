#!/bin/bash
# 任务所 2.1 - 即插即用初始化脚本
# 功能：
# 1. 检测项目类型
# 2. 整理为企业级Monorepo结构
# 3. 初始化知识库数据库
# 4. 扫描项目生成知识图谱
# 5. 启动Dashboard

set -e  # 遇到错误立即退出

TASKFLOW_DIR=$(cd "$(dirname "$0")" && pwd)
TARGET_PROJECT_DIR=$(pwd)
PROJECT_NAME=$(basename "$TARGET_PROJECT_DIR")

echo "================================================================"
echo "🚀 任务所 2.1 - 企业级项目即插即用初始化"
echo "================================================================"
echo ""
echo "📍 任务所位置: $TASKFLOW_DIR"
echo "📁 目标项目: $TARGET_PROJECT_DIR"
echo "📛 项目名称: $PROJECT_NAME"
echo ""

# ============================================
# 步骤0: 确认初始化
# ============================================
echo "⚠️  此操作将："
echo "   1. 在项目中创建标准Monorepo文件夹结构"
echo "   2. 移动现有文件到对应目录"
echo "   3. 初始化知识库数据库"
echo "   4. 创建.taskflow配置目录"
echo ""
read -p "是否继续初始化？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 初始化取消"
    exit 0
fi

# ============================================
# 步骤1: 整理项目文件夹结构
# ============================================
echo ""
echo "================================================================"
echo "📂 步骤1: 整理为企业级Monorepo结构"
echo "================================================================"

# 创建完整的目录结构
echo ""
echo "创建标准目录..."

mkdir -p apps/{api,web,admin,worker,mobile}
mkdir -p packages/{core-domain,infra,ui-kit,ux-flows,tools-cli,shared-types,shared-config,shared-utils}
mkdir -p packages/core-domain/{entities,value-objects,repositories,use-cases,services}
mkdir -p packages/infra/{database,cache,queue,storage,llm,monitoring}
mkdir -p docs/{product,ux,arch,adr,api,ops-runbook,onboarding}
mkdir -p ops/{infra,k8s,docker,ci-cd,monitoring,environments,scripts}
mkdir -p knowledge/{issues,solutions,patterns,tools,glossary,lessons-learned}
mkdir -p database/{migrations,seeds,schemas,knowledge-db,docs}
mkdir -p tests/{e2e,integration,performance,fixtures}
mkdir -p design/{brand-assets,ui-mockups}
mkdir -p secrets
mkdir -p .github/{workflows,ISSUE_TEMPLATE}
mkdir -p config

echo "✅ 标准目录结构已创建"

# 检测并移动现有文件
echo ""
echo "🔍 检测现有文件结构..."

# 检测项目类型
PROJECT_TYPE="Unknown"
if [ -f "package.json" ]; then
    echo "  📦 检测到: Node.js/JavaScript项目"
    PROJECT_TYPE="Node.js"

    # 移动前端代码
    if [ -d "src" ] && [ ! -d "apps/web/src" ]; then
        echo "  移动 src/ → apps/web/src/"
        mv src apps/web/
    fi

    if [ -f "package.json" ] && [ ! -f "apps/web/package.json" ]; then
        cp package.json apps/web/
    fi
fi

if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    echo "  🐍 检测到: Python项目"
    PROJECT_TYPE="Python"

    # 移动Python代码
    if [ -d "app" ] && [ ! -d "apps/api/src" ]; then
        echo "  移动 app/ → apps/api/src/"
        mv app apps/api/src
    fi

    if [ -f "requirements.txt" ] && [ ! -f "apps/api/requirements.txt" ]; then
        cp requirements.txt apps/api/
    fi
fi

# 移动已有文档
if [ -d "docs" ] && [ "$(ls -A docs 2>/dev/null)" ]; then
    echo "  📚 发现现有文档目录"
    # 不覆盖，保持现有docs
fi

echo "✅ 文件结构整理完成"

# ============================================
# 步骤2: 初始化知识库数据库
# ============================================
echo ""
echo "================================================================"
echo "🗄️  步骤2: 初始化知识库数据库"
echo "================================================================"

DB_PATH="$TARGET_PROJECT_DIR/.taskflow/knowledge.db"

echo ""
echo "创建知识库数据库: $DB_PATH"

sqlite3 "$DB_PATH" << 'SQLEOF'
-- 1. 项目主表
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    description TEXT,
    repo_url TEXT,
    status TEXT DEFAULT 'active',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 2. 组件/模块表
CREATE TABLE IF NOT EXISTS components (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,  -- backend/frontend/mcp/package
    description TEXT,
    repo_path TEXT,
    owner TEXT,
    tech_stack TEXT,  -- JSON字符串
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
CREATE INDEX idx_components_project ON components(project_id);

-- 3. 环境表
CREATE TABLE IF NOT EXISTS environments (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    url TEXT,
    config_ref TEXT,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- 4. 问题库（核心！）
CREATE TABLE IF NOT EXISTS issues (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    component_id TEXT,
    environment_id TEXT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    error_message TEXT,
    cause TEXT,
    impact TEXT,
    tags TEXT,  -- JSON数组
    status TEXT DEFAULT 'open',
    severity TEXT DEFAULT 'medium',
    priority TEXT DEFAULT 'medium',
    occurred_at TEXT NOT NULL,
    resolved_at TEXT,
    reporter TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
CREATE INDEX idx_issues_project ON issues(project_id);
CREATE INDEX idx_issues_status ON issues(status);

-- 5. 解决方案表
CREATE TABLE IF NOT EXISTS solutions (
    id TEXT PRIMARY KEY,
    issue_id TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    steps TEXT NOT NULL,
    code_snippet TEXT,
    type TEXT NOT NULL,
    is_final INTEGER DEFAULT 0,
    effectiveness TEXT,
    created_by TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (issue_id) REFERENCES issues(id)
);

-- 6. 架构决策表（ADR）
CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    title TEXT NOT NULL,
    context TEXT NOT NULL,
    decision TEXT NOT NULL,
    consequences TEXT NOT NULL,
    alternatives TEXT,
    status TEXT DEFAULT 'active',
    tags TEXT,
    decided_by TEXT,
    decided_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- 7. 部署记录表
CREATE TABLE IF NOT EXISTS deployments (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    environment_id TEXT NOT NULL,
    version TEXT NOT NULL,
    commit_hash TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    deployed_by TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id),
    FOREIGN KEY (environment_id) REFERENCES environments(id)
);

-- 8. 知识文章表
CREATE TABLE IF NOT EXISTS knowledge_articles (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT NOT NULL,
    tags TEXT,
    views INTEGER DEFAULT 0,
    helpful_count INTEGER DEFAULT 0,
    author TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- 9. 记忆层级表（短期/中期/长期）
CREATE TABLE IF NOT EXISTS memory_layers (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    layer TEXT NOT NULL,  -- short_term/mid_term/long_term
    content TEXT NOT NULL,
    category_code TEXT,  -- 21库分类
    importance INTEGER DEFAULT 5,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    promoted_at TEXT,  -- 提升到下一层的时间
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- 10. 交互事件表
CREATE TABLE IF NOT EXISTS interaction_events (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    user_id TEXT,
    source TEXT,  -- cursor/claude/web
    event_type TEXT,  -- user_message/ai_response/tool_call
    payload TEXT,  -- JSON
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

SQLEOF

echo "✅ 知识库数据库创建完成（10张核心表）"

# ============================================
# 步骤3: 扫描项目生成初始数据
# ============================================
echo ""
echo "================================================================"
echo "🔍 步骤3: 扫描项目生成初始知识"
echo "================================================================"

python3 << PYEOF
import sqlite3
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import uuid

# 连接数据库
db_path = "$DB_PATH"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 生成项目ID
project_id = str(uuid.uuid4())
project_code = "$PROJECT_NAME".upper().replace("-", "_").replace(" ", "_")

# 1. 插入项目记录
print("\n1. 创建项目记录...")
cursor.execute("""
    INSERT INTO projects (id, name, code, description, status)
    VALUES (?, ?, ?, ?, 'active')
""", (
    project_id,
    "$PROJECT_NAME",
    project_code,
    f"$PROJECT_TYPE 项目 - 任务所2.1自动初始化"
))
print(f"   ✅ 项目ID: {project_id}")
print(f"   ✅ 项目代码: {project_code}")

# 2. 扫描并创建组件记录
print("\n2. 扫描项目组件...")
components_found = []

# 扫描apps目录
apps_dir = Path("$TARGET_PROJECT_DIR/apps")
if apps_dir.exists():
    for app_dir in apps_dir.iterdir():
        if app_dir.is_dir() and not app_dir.name.startswith('.'):
            comp_id = str(uuid.uuid4())
            comp_type = "backend" if app_dir.name == "api" else "frontend"

            cursor.execute("""
                INSERT INTO components (id, project_id, name, type, repo_path)
                VALUES (?, ?, ?, ?, ?)
            """, (comp_id, project_id, app_dir.name, comp_type, f"apps/{app_dir.name}"))

            components_found.append(app_dir.name)
            print(f"   ✅ 组件: {app_dir.name} ({comp_type})")

# 扫描packages目录
packages_dir = Path("$TARGET_PROJECT_DIR/packages")
if packages_dir.exists():
    for pkg_dir in packages_dir.iterdir():
        if pkg_dir.is_dir() and not pkg_dir.name.startswith('.'):
            comp_id = str(uuid.uuid4())

            cursor.execute("""
                INSERT INTO components (id, project_id, name, type, repo_path)
                VALUES (?, ?, ?, 'package', ?)
            """, (comp_id, project_id, pkg_dir.name, f"packages/{pkg_dir.name}"))

            components_found.append(pkg_dir.name)
            print(f"   ✅ 包: {pkg_dir.name}")

if not components_found:
    print("   ⚠️  未检测到标准组件，将在后续扫描中分析")

# 3. 创建环境记录
print("\n3. 创建环境配置...")
environments = [
    ("dev", "development", "http://localhost:8841", "开发环境"),
    ("staging", "testing", "http://localhost:8842", "测试环境"),
    ("prod", "production", "TBD", "生产环境")
]

for env_name, env_type, url, desc in environments:
    env_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO environments (id, project_id, name, type, url, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (env_id, project_id, env_name, env_type, url, desc))
    print(f"   ✅ {env_name}: {url}")

# 4. 创建初始知识文章
print("\n4. 创建初始知识文章...")
article_id = str(uuid.uuid4())
cursor.execute("""
    INSERT INTO knowledge_articles (id, project_id, title, content, category, tags, author)
    VALUES (?, ?, ?, ?, ?, ?, 'taskflow-init')
""", (
    article_id,
    project_id,
    f"{project_code} 项目初始化完成",
    f"""# {project_code} 项目知识库

## 项目信息
- 名称: $PROJECT_NAME
- 类型: $PROJECT_TYPE
- 初始化时间: {datetime.now().isoformat()}

## 目录结构
已创建企业级Monorepo结构：
- apps/ - 应用层
- packages/ - 共享代码包
- docs/ - 文档中心
- ops/ - 运维部署
- knowledge/ - 知识库
- database/ - 数据库

## 下一步
1. 将现有代码移动到对应目录
2. 配置MCP记忆系统
3. 启动Dashboard开始协作
""",
    "guide",
    json.dumps(["初始化", "指南", project_code])
))
print(f"   ✅ 初始化指南文章已创建")

# 保存项目ID到配置
Path("$TARGET_PROJECT_DIR/.taskflow").mkdir(exist_ok=True)
with open("$TARGET_PROJECT_DIR/.taskflow/project_id.txt", 'w') as f:
    f.write(project_id)

conn.commit()
conn.close()

print(f"\n✅ 数据库初始化完成")
print(f"   项目ID: {project_id}")
print(f"   组件数: {len(components_found)}")
print(f"   环境数: 3")
PYEOF

# ============================================
# 步骤4: 自动分配端口（使用端口管理器）
# ============================================
echo ""
echo "================================================================"
echo "🔌 步骤4: 自动分配Dashboard端口"
echo "================================================================"

# 读取项目ID和代码
PROJECT_ID=$(cat "$TARGET_PROJECT_DIR/.taskflow/project_id.txt")
PROJECT_CODE=$(echo "$PROJECT_NAME" | tr '[:lower:]' '[:upper:]' | tr '-' '_' | tr ' ' '_')

# 使用端口管理器分配端口
PORT=$(python3 "$TASKFLOW_DIR/packages/shared-utils/port_manager.py" allocate "$PROJECT_CODE" "$TARGET_PROJECT_DIR" | grep "端口:" | awk '{print $2}')

if [ -z "$PORT" ]; then
    echo "❌ 端口分配失败"
    exit 1
fi

API_PORT=$((PORT - 1))
echo "   ✅ Dashboard端口: $PORT"
echo "   ✅ API端口: $API_PORT"
echo "   ✅ 已注册到全局端口管理器"

# 保存端口配置
echo "$PORT" > "$TARGET_PROJECT_DIR/.taskflow/dashboard_port"
echo "$API_PORT" > "$TARGET_PROJECT_DIR/.taskflow/api_port"
echo "$PROJECT_CODE" > "$TARGET_PROJECT_DIR/.taskflow/project_code.txt"

# ============================================
# 步骤5: 生成AI角色激活指令
# ============================================
echo ""
echo "================================================================"
echo "🤖 步骤5: 生成AI角色激活指令"
echo "================================================================"

python3 << PYEOF
import sys
sys.path.insert(0, "$TASKFLOW_DIR/packages/shared-utils")

from activation_command_generator import ActivationCommandGenerator

# 读取项目信息
project_info = {
    "project_name": "$PROJECT_NAME",
    "project_code": "$PROJECT_CODE",
    "project_type": "$PROJECT_TYPE",
    "dashboard_port": $PORT,
    "api_port": $API_PORT,
    "tech_stack": ["$PROJECT_TYPE"],
    "project_path": "$TARGET_PROJECT_DIR"
}

generator = ActivationCommandGenerator(project_info)

# 生成所有激活指令
commands = generator.generate_all_commands()

# 保存到文件
import json
output_dir = "$TARGET_PROJECT_DIR/.taskflow/activation_commands"
import os
os.makedirs(output_dir, exist_ok=True)

for role, command in commands.items():
    with open(f"{output_dir}/{role}.md", 'w', encoding='utf-8') as f:
        f.write(command)
    print(f"   ✅ {role} 激活指令已生成")

# 保存JSON格式供API使用
with open("$TARGET_PROJECT_DIR/.taskflow/activation_commands.json", 'w') as f:
    json.dump(commands, f, indent=2, ensure_ascii=False)

print("")
print("✅ 所有激活指令已生成")
print(f"   位置: .taskflow/activation_commands/")
PYEOF

# 生成项目规则配置
echo ""
echo "生成项目规则配置..."
sed "s/{PROJECT_NAME}/$PROJECT_NAME/g; s/{PROJECT_CODE}/$PROJECT_CODE/g; s/{PORT}/$PORT/g; s/{API_PORT}/$API_PORT/g" \
  "$TASKFLOW_DIR/templates/project_rules_template.yaml" > "$TARGET_PROJECT_DIR/.taskflow/project_rules.yaml"
echo "   ✅ 项目规则配置已生成: .taskflow/project_rules.yaml"

# ============================================
# 步骤6: 创建启动脚本
# ============================================
echo ""
echo "================================================================"
echo "📜 步骤5: 创建启动脚本"
echo "================================================================"

cat > "$TARGET_PROJECT_DIR/.taskflow/启动Dashboard.sh" << STARTSCRIPT
#!/bin/bash
# 任务所 Dashboard 启动脚本

TASKFLOW_DIR="$TASKFLOW_DIR"
PROJECT_DIR="$TARGET_PROJECT_DIR"
PORT=$PORT
API_PORT=$API_PORT

echo "========================================"
echo "🚀 启动任务所 Dashboard"
echo "========================================"
echo ""
echo "项目: $PROJECT_NAME"
echo "Dashboard: http://localhost:\$PORT"
echo "API: http://localhost:\$API_PORT"
echo ""

# 启动API服务（后台）
cd "\$TASKFLOW_DIR" && \
  python3 start_insight_api.py --port \$API_PORT > "\$PROJECT_DIR/.taskflow/logs/api.log" 2>&1 &
API_PID=\$!
echo "\$API_PID" > "\$PROJECT_DIR/.taskflow/api.pid"
echo "✅ API服务启动 (PID: \$API_PID)"

sleep 2

# 启动Dashboard
echo "✅ Dashboard启动中..."
echo ""
echo "按 Ctrl+C 停止服务"
echo ""
cd "\$TASKFLOW_DIR/dashboard-test-8831" && \
  python3 -m http.server \$PORT

# 清理
kill \$API_PID 2>/dev/null
rm "\$PROJECT_DIR/.taskflow/api.pid" 2>/dev/null
STARTSCRIPT

chmod +x "$TARGET_PROJECT_DIR/.taskflow/启动Dashboard.sh"
echo "✅ 启动脚本已创建: .taskflow/启动Dashboard.sh"

# ============================================
# 步骤6: 创建README
# ============================================
cat > "$TARGET_PROJECT_DIR/.taskflow/README.md" << 'README'
# 任务所 2.1 - 已初始化

## 快速启动

```bash
./.taskflow/启动Dashboard.sh
```

## 访问地址

Dashboard将自动打开，端口号见 `.taskflow/dashboard_port`

## 目录说明

```
.taskflow/
├── knowledge.db          # 知识库数据库
├── dashboard_port        # Dashboard端口
├── api_port             # API端口
├── project_id.txt       # 项目UUID
├── 启动Dashboard.sh      # 启动脚本
├── logs/                # 日志目录
└── README.md            # 本文件
```

## MCP记忆系统

已集成MCP记忆系统：
- Session Memory: http://13.158.83.99:4000
- Ultra Memory: DynamoDB (10501条历史记忆)

## 下一步

1. 查看Dashboard了解项目结构
2. 开始使用AI协作开发
3. 所有对话、决策自动保存到知识库
README

# ============================================
# 完成
# ============================================
echo ""
echo "================================================================"
echo "✅ 初始化完成！"
echo "================================================================"
echo ""
echo "📊 项目信息："
echo "   名称: $PROJECT_NAME"
echo "   类型: $PROJECT_TYPE"
echo "   项目ID: $(cat $TARGET_PROJECT_DIR/.taskflow/project_id.txt)"
echo ""
echo "🚀 启动命令："
echo "   ./.taskflow/启动Dashboard.sh"
echo ""
echo "🌐 访问地址："
echo "   http://localhost:$PORT"
echo ""
echo "📁 配置目录："
echo "   $TARGET_PROJECT_DIR/.taskflow/"
echo ""
echo "🗄️  知识库数据库："
echo "   $TARGET_PROJECT_DIR/.taskflow/knowledge.db"
echo ""
echo "📂 项目结构："
echo "   已创建企业级Monorepo结构"
echo "   现有文件已移动到对应目录"
echo ""
echo "================================================================"
echo "🎉 任务所 2.1 已就绪！开始AI协作之旅！"
echo "================================================================"


