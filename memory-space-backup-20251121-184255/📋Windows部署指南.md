# 📋 记忆空间模块 - Windows部署指南

**版本**: v1.9 完整版  
**备份时间**: 2025-11-21  
**适用系统**: Windows 10/11

---

## 🎯 快速部署（5步）

### 前置条件
```
✅ Python 3.8+ 已安装
✅ SQLite3 已安装
✅ 项目已克隆到Windows
```

---

### 步骤1: 复制文件 (PowerShell)

```powershell
# 设置你的项目根目录
$PROJECT = "C:\你的项目路径\taskflow-v1-2"
$BACKUP = "memory-space-backup-20251121-184255"

# 复制数据库文件
Copy-Item "$BACKUP\database\schemas\v5_project_memory_schema.sql" "$PROJECT\database\schemas\"
Copy-Item "$BACKUP\database\migrations\005_add_project_memory_tables.sql" "$PROJECT\database\migrations\"

# 复制后端服务
Copy-Item "$BACKUP\packages\core-domain\src\services\project_memory_service.py" "$PROJECT\packages\core-domain\src\services\"
Copy-Item "$BACKUP\apps\api\src\routes\project_memory.py" "$PROJECT\apps\api\src\routes\"
Copy-Item "$BACKUP\apps\api\src\routes\conversation_hook.py" "$PROJECT\apps\api\src\routes\"

# 复制脚本
Copy-Item "$BACKUP\scripts\init_project_memory_mcp.py" "$PROJECT\scripts\"
Copy-Item "$BACKUP\scripts\test_auto_memory.py" "$PROJECT\scripts\"

# 复制前端Dashboard
Copy-Item "$BACKUP\dashboard\index.html" "$PROJECT\dashboard-v1.9-20251121\index.html"

Write-Host "✅ 文件复制完成"
```

---

### 步骤2: 执行数据库迁移

```powershell
cd $PROJECT

# 执行Schema创建
Get-Content database\schemas\v5_project_memory_schema.sql | sqlite3 database\data\tasks.db

# 验证表创建
sqlite3 database\data\tasks.db "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%memor%'"
```

**预期输出**:
```
project_memories
memory_relations
memory_retrieval_history
project_memory_stats
```

---

### 步骤3: 注册API路由

#### 修改 `apps\api\src\main.py`

**第22行附近，添加导入**:
```python
from routes.conversation_hook import router as conversation_hook_router
```

**第66-76行附近，添加注册**:
```python
app.include_router(conversation_hook_router, tags=["conversation-hook"])
```

#### 修改 `apps\api\src\routes\__init__.py`

**添加导出**:
```python
from . import conversation_hook

__all__ = [..., "conversation_hook"]
```

---

### 步骤4: 启动服务

```powershell
# 启动API服务（终端1）
cd $PROJECT\apps\api
uvicorn src.main:app --reload --port 8000

# 启动Dashboard（终端2）
cd $PROJECT\dashboard-v1.9-20251121
python -m http.server 8820
```

---

### 步骤5: 验证部署

```powershell
# 测试API
Invoke-WebRequest http://localhost:8000/api/projects/TASKFLOW/memories/stats

# 运行测试脚本
python scripts\test_auto_memory.py

# 打开Dashboard
start http://localhost:8820/
```

---

## 📊 部署验证清单

### API端点验证
```powershell
# 1. 根端点
curl http://localhost:8000/

# 2. API文档
start http://localhost:8000/api/docs

# 3. 记忆统计
curl http://localhost:8000/api/projects/TASKFLOW/memories/stats

# 4. 记忆列表
curl http://localhost:8000/api/projects/TASKFLOW/memories

# 5. 自动记录Hook
curl -X POST http://localhost:8000/api/conversations/hook/auto-record `
  -H "Content-Type: application/json" `
  -d '{"user_input":"测试","ai_response":"好的","ai_role":"assistant"}' `
  --url-query "project_code=TASKFLOW"
```

### Dashboard验证
```
1. 访问 http://localhost:8820/
2. 滚动到"项目记忆空间Dashboard UI"模块
3. 检查点：
   ✅ 模块正常显示
   ✅ 左侧有4个统计卡片
   ✅ 右上角有6个筛选按钮（含"🤖 自动笔记"）
   ✅ 右侧时间线正常显示
   ✅ 打开F12控制台无JS错误
   ✅ 看到fetch请求到8000端口
```

---

## 🔧 MCP配置（可选）

### Ultra Memory Cloud MCP

**服务器**: AWS Tokyo  
**IP**: 13.158.83.99  
**端口**: 7000

**方式1: SSH隧道（推荐）**
```powershell
# 在PowerShell中（需要OpenSSH）
ssh -i C:\path\to\librechat-tokyo-2025.pem `
    -L 3000:localhost:7000 `
    ubuntu@13.158.83.99 `
    -N
```

**方式2: 直接连接（需要开放AWS安全组）**
```python
# 修改 project_memory_service.py 的URL
url = "http://13.158.83.99:7000/api/memory/store"
```

**方式3: 禁用MCP（本地存储模式）**
```python
# 修改初始化参数
session_memory_enabled=False,
ultra_memory_enabled=False
```

---

## 🐛 常见问题

### 问题1: sqlite3命令不存在
```powershell
# 解决：使用Python执行
python -c "import sqlite3; exec(open('database/schemas/v5_project_memory_schema.sql').read())"
```

### 问题2: uvicorn找不到
```powershell
pip install fastapi uvicorn httpx
```

### 问题3: 路径导入错误
```powershell
# 确保项目根目录在PYTHONPATH中
$env:PYTHONPATH = "$PROJECT;$PROJECT\packages\core-domain\src"
```

### 问题4: 端口被占用
```powershell
# 查看占用
netstat -ano | findstr :8000

# 杀死进程
taskkill /PID <进程ID> /F

# 或换端口
uvicorn src.main:app --port 8001
```

---

## 📄 文件内容说明

### v5_project_memory_schema.sql
```sql
-- 4张核心表
CREATE TABLE project_memories (...);     -- 记忆主表
CREATE TABLE memory_relations (...);     -- 关系表
CREATE TABLE memory_retrieval_history (...);  -- 检索历史
CREATE TABLE project_memory_stats (...); -- 统计表

-- 索引优化
CREATE INDEX idx_project_memories_project ON project_memories(project_id);
...

-- 视图
CREATE VIEW v_memory_full_view AS ...

-- 初始化数据
INSERT INTO project_memory_stats VALUES ('TASKFLOW', 0, ...);
```

### project_memory_service.py (核心方法)
```python
class ProjectMemoryService:
    # 基础CRUD
    def create_memory()          # 创建记忆
    def retrieve_memories()      # 检索记忆
    def get_memory_stats()       # 获取统计
    
    # 自动记录（新功能）
    def auto_record_conversation()      # 自动记录对话
    def _analyze_conversation()         # 分析对话
    def _generate_conversation_summary() # 生成摘要
    def _calculate_importance()         # 计算重要度
    
    # MCP集成
    def _store_to_ultra_memory()   # Ultra MCP存储
    def _store_to_session_memory() # Session MCP存储
    def _query_from_ultra_memory() # Ultra MCP检索
    
    # 决策和方案
    def auto_record_architecture_decision()  # 记录决策
    def auto_record_problem_solution()       # 记录方案
    
    # 知识继承
    def inherit_knowledge()        # 跨会话知识继承
```

### conversation_hook.py (API端点)
```python
# 自动记录端点
POST /api/conversations/hook/auto-record
  → 单次对话自动记录
  
POST /api/conversations/hook/batch-auto-record
  → 批量对话记录
  
GET /api/conversations/hook/stats
  → 自动记录统计
```

### Dashboard index.html (关键部分)

**API集成** (第15639行附近):
```javascript
const MEMORY_API_BASE = 'http://localhost:8000/api/projects/TASKFLOW/memories';

async function loadMemoryStats() {
    const response = await fetch(`${MEMORY_API_BASE}/stats`);
    // 更新统计卡片
}

async function loadMemoriesList() {
    const response = await fetch(`${MEMORY_API_BASE}?limit=50`);
    // 动态渲染记忆列表
}

function setupMemoryEventListener() {
    const eventSource = new EventSource('http://localhost:8000/api/events/stream?project_id=TASKFLOW');
    // 监听记忆事件，自动刷新
}
```

**自动笔记筛选** (第11409行附近):
```html
<button class="filter-chip" onclick="filterMemories('auto-note')">🤖 自动笔记</button>
```

---

## 🎨 UI风格说明

记忆空间模块保持**Blanc Luxury**风格：
- 左侧面板：灰白背景，统计卡片
- 右侧时间线：白色背景，记忆卡片
- 标记点：黑色实心（决策）、灰色空心（方案）、浅灰（知识）
- 筛选按钮：直角边框，黑白色系
- 过渡动画：0.3s ease

**不要修改任何样式，只确保API集成正常！**

---

## 🔍 测试用例

### 测试1: 基础功能
```bash
# 访问Dashboard
http://localhost:8820/

# 检查：
✅ 记忆空间模块显示
✅ 统计卡片：总记忆/决策/方案/重要
✅ 筛选按钮：全部/决策/方案/知识/🤖自动笔记/重要
✅ 记忆时间线
```

### 测试2: API集成
```bash
# 打开浏览器控制台(F12)
# 应该看到：
✅ fetch请求到 http://localhost:8000/api/projects/TASKFLOW/memories/stats
✅ 统计数字从API加载（不是固定的45/12/23/8）
✅ 记忆列表从API加载
```

### 测试3: 自动记录
```bash
# 运行测试脚本
python scripts\test_auto_memory.py

# 预期结果：
✅ 测试1-架构决策：PASS (应该记录)
✅ 测试2-问题解决：PASS (应该记录)
✅ 测试3-普通对话：PASS (不应记录)
✅ 测试4-强制记录：PASS (应该记录)
```

---

## 📂 备份包结构

```
memory-space-backup-20251121-184255/
├── README.md                          # 本文件
├── 📋Windows部署指南.md               # 部署指南
├── database/
│   ├── schemas/
│   │   └── v5_project_memory_schema.sql
│   └── migrations/
│       └── 005_add_project_memory_tables.sql
├── packages/
│   └── core-domain/
│       └── src/
│           └── services/
│               └── project_memory_service.py
├── apps/
│   └── api/
│       └── src/
│           └── routes/
│               ├── project_memory.py
│               └── conversation_hook.py
├── scripts/
│   ├── init_project_memory_mcp.py
│   └── test_auto_memory.py
└── dashboard/
    └── index.html                     # Dashboard完整版
```

---

## 🚀 一键部署脚本（Windows批处理）

将以下内容保存为 `部署记忆空间.bat`:

```batch
@echo off
chcp 65001 >nul
echo 🚀 记忆空间模块 - Windows部署脚本
echo ================================================

REM 设置项目路径
set PROJECT=C:\你的项目路径\taskflow-v1-2
set BACKUP=%~dp0

echo.
echo 第1步: 复制文件...
xcopy /Y "%BACKUP%database\schemas\*.sql" "%PROJECT%\database\schemas\"
xcopy /Y "%BACKUP%database\migrations\*.sql" "%PROJECT%\database\migrations\"
xcopy /Y "%BACKUP%packages\core-domain\src\services\*.py" "%PROJECT%\packages\core-domain\src\services\"
xcopy /Y "%BACKUP%apps\api\src\routes\project_memory.py" "%PROJECT%\apps\api\src\routes\"
xcopy /Y "%BACKUP%apps\api\src\routes\conversation_hook.py" "%PROJECT%\apps\api\src\routes\"
xcopy /Y "%BACKUP%scripts\*.py" "%PROJECT%\scripts\"
xcopy /Y "%BACKUP%dashboard\index.html" "%PROJECT%\dashboard-v1.9-20251121\"

echo ✅ 文件复制完成
echo.

echo 第2步: 执行数据库迁移...
cd %PROJECT%
type database\schemas\v5_project_memory_schema.sql | sqlite3 database\data\tasks.db

echo ✅ 数据库迁移完成
echo.

echo 第3步: 验证表创建...
sqlite3 database\data\tasks.db "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%%memor%%'"

echo.
echo ================================================
echo ✅ 部署完成！
echo ================================================
echo.
echo 下一步：
echo   1. 修改 apps\api\src\main.py 注册conversation_hook路由
echo   2. 启动API服务: cd apps\api ^&^& uvicorn src.main:app --port 8000
echo   3. 启动Dashboard: cd dashboard-v1.9-20251121 ^&^& python -m http.server 8820
echo   4. 测试功能: python scripts\test_auto_memory.py
echo.
pause
```

---

## 📝 手动修改清单

### 文件1: apps\api\src\main.py

**添加导入（约第22行）**:
```python
from routes.conversation_hook import router as conversation_hook_router
```

**注册路由（约第71行，在其他router之后）**:
```python
app.include_router(conversation_hook_router, tags=["conversation-hook"])
```

### 文件2: apps\api\src\routes\__init__.py

**修改导入部分**:
```python
from . import events
from . import project_memory
from . import architect
from . import conversation_hook  # 新增

__all__ = ["events", "project_memory", "architect", "conversation_hook"]  # 新增
```

---

## 🔗 MCP连接配置（Windows版）

### 使用SSH隧道连接AWS MCP

```powershell
# 确保OpenSSH已安装（Windows 10 1809+自带）

# 建立隧道
ssh -i C:\path\to\librechat-tokyo-2025.pem `
    -L 3000:localhost:7000 `
    ubuntu@13.158.83.99 `
    -N

# 测试连接
curl http://localhost:3000/health
```

### 或者暂时禁用MCP

**修改**: `packages\core-domain\src\services\project_memory_service.py`

**第64-65行**:
```python
self.session_memory_enabled = False  # 暂时禁用
self.ultra_memory_enabled = False    # 暂时禁用
```

**效果**: 所有记忆只存储在本地SQLite，功能完全正常！

---

## 🎯 成功标志

部署成功后应该看到：

### API服务
```
✅ http://localhost:8000/ 返回API信息
✅ http://localhost:8000/api/docs 显示API文档
✅ /api/projects/TASKFLOW/memories/stats 返回统计JSON
```

### Dashboard
```
✅ http://localhost:8820/ 打开Dashboard
✅ 记忆空间模块正常显示
✅ 统计数字可能为0（初始状态）
✅ 有6个筛选按钮（含🤖自动笔记）
✅ 控制台无JS错误
```

### 测试脚本
```
✅ python scripts\test_auto_memory.py 
✅ 4个测试用例全部PASS
```

---

## 💾 如果需要导出数据

```powershell
# 导出记忆数据
sqlite3 database\data\tasks.db ".mode insert" "SELECT * FROM project_memories" > memories_export.sql

# 在Windows导入
type memories_export.sql | sqlite3 database\data\tasks.db
```

---

## 📞 技术支持

如果遇到问题，检查：
1. `apps\api\api.log` - API错误日志
2. `dashboard-v1.9-20251121\server.log` - Dashboard日志
3. 浏览器控制台(F12) - 前端错误

---

**部署完成后，Windows环境的记忆空间模块将与Mac环境完全一致！** ✅

