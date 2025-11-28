#!/bin/bash
# 任务所 2.1 - 即插即用安装脚本
# 自动扫描项目，初始化数据，启动Dashboard

echo "========================================="
echo "🚀 任务所 2.1 - 即插即用安装"
echo "========================================="
echo ""

# 获取当前项目路径
PROJECT_DIR=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_DIR")

echo "📁 检测到项目："
echo "   路径: $PROJECT_DIR"
echo "   名称: $PROJECT_NAME"
echo ""

# 检查是否在项目根目录
if [ ! -d ".git" ] && [ ! -f "package.json" ] && [ ! -f "requirements.txt" ] && [ ! -f "go.mod" ]; then
    echo "⚠️  警告: 未检测到项目标识文件（.git, package.json, requirements.txt等）"
    echo "   当前可能不在项目根目录"
    echo ""
    read -p "是否继续安装？(y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 安装取消"
        exit 1
    fi
fi

# 创建.taskflow配置目录
echo "📂 创建任务所配置目录..."
mkdir -p .taskflow
mkdir -p .taskflow/database
mkdir -p .taskflow/logs
mkdir -p .taskflow/cache

# 自动检测项目类型
echo ""
echo "🔍 自动扫描项目..."
PROJECT_TYPE="Unknown"
LANGUAGE="Unknown"

if [ -f "package.json" ]; then
    PROJECT_TYPE="Node.js/JavaScript"
    LANGUAGE="JavaScript"
    if grep -q "react" package.json 2>/dev/null; then
        PROJECT_TYPE="$PROJECT_TYPE (React)"
    fi
    if grep -q "vue" package.json 2>/dev/null; then
        PROJECT_TYPE="$PROJECT_TYPE (Vue)"
    fi
fi

if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    PROJECT_TYPE="Python"
    LANGUAGE="Python"
    if [ -d "django" ] || grep -q "django" requirements.txt 2>/dev/null; then
        PROJECT_TYPE="$PROJECT_TYPE (Django)"
    fi
    if grep -q "flask" requirements.txt 2>/dev/null || [ -f "app.py" ]; then
        PROJECT_TYPE="$PROJECT_TYPE (Flask)"
    fi
    if grep -q "fastapi" requirements.txt 2>/dev/null; then
        PROJECT_TYPE="$PROJECT_TYPE (FastAPI)"
    fi
fi

if [ -f "go.mod" ]; then
    PROJECT_TYPE="Go"
    LANGUAGE="Go"
fi

if [ -f "Cargo.toml" ]; then
    PROJECT_TYPE="Rust"
    LANGUAGE="Rust"
fi

echo "   项目类型: $PROJECT_TYPE"
echo "   主语言: $LANGUAGE"

# 统计项目规模
echo ""
echo "📊 统计项目规模..."
FILE_COUNT=$(find . -type f ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/__pycache__/*" 2>/dev/null | wc -l | tr -d ' ')
CODE_FILES=$(find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.go" -o -name "*.rs" 2>/dev/null | wc -l | tr -d ' ')
echo "   总文件数: $FILE_COUNT"
echo "   代码文件: $CODE_FILES"

# 自动分配端口（8841-8899）
echo ""
echo "🔌 自动分配Dashboard端口..."
PORT=8841
while lsof -i :$PORT >/dev/null 2>&1; do
    echo "   端口 $PORT 已占用，尝试下一个..."
    PORT=$((PORT + 1))
    if [ $PORT -gt 8899 ]; then
        echo "❌ 错误: 端口8841-8899全部被占用"
        exit 1
    fi
done
echo "   ✅ 分配端口: $PORT"

# 创建项目元数据
echo ""
echo "📝 创建项目元数据..."
cat > .taskflow/project.json << EOF
{
  "project_name": "$PROJECT_NAME",
  "project_path": "$PROJECT_DIR",
  "project_type": "$PROJECT_TYPE",
  "language": "$LANGUAGE",
  "dashboard_port": $PORT,
  "api_port": $((PORT - 1)),
  "initialized_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "file_count": $FILE_COUNT,
  "code_files": $CODE_FILES,
  "taskflow_version": "2.1"
}
EOF
echo "   ✅ 项目元数据已创建"

# 初始化数据库
echo ""
echo "🗄️  初始化项目数据库..."
TASKFLOW_DIR=$(dirname "$0")
cp "$TASKFLOW_DIR/database/schema/tasks_schema.sql" .taskflow/database/ 2>/dev/null || echo "   跳过schema复制"

# 创建SQLite数据库
sqlite3 .taskflow/database/project.db << EOF
-- 项目任务表
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',
    priority INTEGER DEFAULT 5,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 项目记忆表
CREATE TABLE IF NOT EXISTS memories (
    id TEXT PRIMARY KEY,
    memory_type TEXT,
    category TEXT,
    title TEXT,
    content TEXT,
    importance INTEGER DEFAULT 5,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 对话历史表
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    role TEXT,
    content TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 初始化完成标记
CREATE TABLE IF NOT EXISTS initialization (
    key TEXT PRIMARY KEY,
    value TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO initialization (key, value) VALUES 
    ('status', 'initialized'),
    ('version', '2.1'),
    ('project_name', '$PROJECT_NAME'),
    ('dashboard_port', '$PORT');
EOF

echo "   ✅ 数据库初始化完成"

# 创建启动脚本
echo ""
echo "📜 创建启动脚本..."
cat > .taskflow/start.sh << EOF
#!/bin/bash
cd "\$(dirname "\$0")/.."

echo "========================================"
echo "🚀 启动任务所 Dashboard"
echo "========================================"
echo ""
echo "项目: $PROJECT_NAME"
echo "Dashboard: http://localhost:$PORT"
echo "API: http://localhost:$((PORT - 1))"
echo ""
echo "按 Ctrl+C 停止"
echo ""

# 启动API服务（后台）
cd "$TASKFLOW_DIR" && python3 start_insight_api.py --port $((PORT - 1)) &
API_PID=\$!
echo "API服务 PID: \$API_PID"

# 等待API启动
sleep 2

# 启动Dashboard
cd "$TASKFLOW_DIR/dashboard-test-8831"
python3 -m http.server $PORT

# 清理
kill \$API_PID 2>/dev/null
EOF

chmod +x .taskflow/start.sh
echo "   ✅ 启动脚本已创建"

# 注册到全局注册表
echo ""
echo "📋 注册到全局任务所注册表..."
mkdir -p ~/.taskflow
REGISTRY=~/.taskflow/projects.json

if [ ! -f "$REGISTRY" ]; then
    echo "[]" > "$REGISTRY"
fi

# 添加项目到注册表
python3 << PYEOF
import json
import os

registry_file = os.path.expanduser('~/.taskflow/projects.json')
with open(registry_file, 'r') as f:
    projects = json.load(f)

# 移除旧的同名项目
projects = [p for p in projects if p.get('name') != '$PROJECT_NAME']

# 添加新项目
projects.append({
    'name': '$PROJECT_NAME',
    'path': '$PROJECT_DIR',
    'port': $PORT,
    'api_port': $((PORT - 1)),
    'type': '$PROJECT_TYPE',
    'initialized_at': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
})

with open(registry_file, 'w') as f:
    json.dump(projects, f, indent=2)

print(f'   ✅ 已注册到全局注册表（端口: $PORT）')
PYEOF

# 完成
echo ""
echo "========================================="
echo "✅ 安装完成！"
echo "========================================="
echo ""
echo "📋 项目信息："
echo "   名称: $PROJECT_NAME"
echo "   类型: $PROJECT_TYPE"
echo "   Dashboard端口: $PORT"
echo "   API端口: $((PORT - 1))"
echo ""
echo "🚀 启动方法："
echo "   cd $PROJECT_DIR"
echo "   ./.taskflow/start.sh"
echo ""
echo "或者："
echo "   cd $PROJECT_DIR"
echo "   cd $TASKFLOW_DIR/dashboard-test-8831"
echo "   python3 -m http.server $PORT"
echo ""
echo "🌐 访问地址："
echo "   http://localhost:$PORT"
echo ""
echo "📁 配置文件："
echo "   $PROJECT_DIR/.taskflow/"
echo ""
echo "========================================="


