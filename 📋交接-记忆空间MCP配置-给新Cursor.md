# 📋 交接任务 - 记忆空间MCP远程配置与完整部署

**任务目标**: 配置远程MCP服务，完成记忆空间的完整部署和测试  
**当前状态**: 代码已完成，但MCP服务未配置，API未启动  
**工作目录**: `/Users/yalinwang/Desktop/任务所 1.8/taskflow-v1-2/taskflow-v1-2`

---

## 🎯 任务概述

需要完成以下工作：
1. 配置远程Ultra Memory MCP服务（AWS服务器）
2. 配置Session Memory MCP（本地或远程）
3. 启动本地API服务（8000端口）
4. 测试8840环境的完整功能
5. 部署到8820正式环境
6. 完整验证所有功能

---

## 📊 当前完成状态

### ✅ 已完成（100%）

#### 1. 数据库结构
```
✅ project_memories表 - 记忆主表
✅ memory_relations表 - 关系图谱
✅ memory_retrieval_history表 - 检索历史
✅ project_memory_stats表 - 统计数据

位置: database/data/tasks.db
Schema: database/schemas/v5_project_memory_schema.sql
```

#### 2. 后端服务代码
```
✅ ProjectMemoryService完整实现
   - auto_record_conversation() 自动记录对话
   - _store_to_ultra_memory() Ultra MCP集成
   - _store_to_session_memory() Session MCP集成
   - _query_from_ultra_memory() 语义检索
   
✅ conversation_hook API端点
   - POST /api/conversations/hook/auto-record
   - POST /api/conversations/hook/batch-auto-record
   - GET /api/conversations/hook/stats
   
✅ 事件流集成
   - memory.created
   - memory.auto_created
   - memory.decision_recorded
   - memory.problem_solution_recorded

文件位置:
- packages/core-domain/src/services/project_memory_service.py
- apps/api/src/routes/conversation_hook.py
- apps/api/src/routes/project_memory.py
```

#### 3. 前端Dashboard集成（8840测试环境）
```
✅ API集成代码
✅ 事件流监听
✅ 自动笔记筛选
✅ 动态渲染
✅ 实时刷新

位置: dashboard-memory-test-8840/index.html
```

---

### ❌ 未完成（需要你做的）

#### 1. 远程MCP服务配置
```
❌ Ultra Memory MCP (AWS服务器)
❌ Session Memory MCP
❌ 本地API服务 (8000端口)
```

#### 2. 环境部署
```
❌ 8840环境测试验证
❌ 8820正式环境部署
```

---

## 🔧 远程MCP服务器信息

### Ultra Memory Cloud MCP (AWS Tokyo)

**服务器信息**:
```
IP地址: 13.158.83.99
区域: AWS Tokyo (ap-northeast-1)
实例ID: i-047d76083e99d5af2
SSH用户: ubuntu
```

**SSH密钥**:
```
主密钥: ~/Desktop/重要/librechat-claude-key-new
备用密钥: ~/Desktop/重要/librechat-tokyo-2025.pem
```

**SSH连接**:
```bash
# 方式1: 直接连接
ssh -i ~/Desktop/重要/librechat-tokyo-2025.pem ubuntu@13.158.83.99

# 方式2: 使用快速登录脚本（如果存在）
bash ~/Desktop/🚀_快速登录LibreChat服务器.sh
```

**服务器上的MCP位置**:
```
目录: /home/ubuntu/ultra-memory-cloud-mcp/
端口: 7000 (已在文档中说明)
服务: pm2管理
```

**当前问题**:
- ❌ 端口7000从本地无法访问
- 可能原因：防火墙未开放/服务未启动/端口映射问题

---

## 🚀 你需要做的步骤

### 第1步: 检查和启动远程Ultra Memory MCP

```bash
# 1. SSH登录服务器
ssh -i ~/Desktop/重要/librechat-tokyo-2025.pem ubuntu@13.158.83.99

# 2. 检查MCP服务状态
cd /home/ubuntu/ultra-memory-cloud-mcp
pm2 list

# 3. 如果服务未启动
pm2 start src/server.js --name ultra-memory-mcp

# 4. 检查端口监听
netstat -tlnp | grep 7000

# 5. 查看日志
pm2 logs ultra-memory-mcp --lines 50

# 6. 测试服务
curl http://localhost:7000/health
```

**修复端口访问问题**:
```bash
# 在服务器上，如果需要从外部访问7000端口

# 方式1: 使用AWS安全组开放端口
# 在AWS控制台 → EC2 → 安全组 → 添加入站规则
# 端口: 7000, 协议: TCP, 来源: 0.0.0.0/0

# 方式2: 使用SSH隧道转发（临时方案）
# 在本地执行：
ssh -i ~/Desktop/重要/librechat-tokyo-2025.pem -L 3000:localhost:7000 ubuntu@13.158.83.99 -N -f
# 然后在代码中使用 http://localhost:3000 访问远程MCP
```

---

### 第2步: 配置Session Memory MCP

**选项A: 使用本地Session Memory**
```bash
# 如果你有本地的session-memory-mcp项目
cd packages/session-memory-mcp  # 或其他位置
npm install
npm start  # 默认端口5173

# 测试
curl http://localhost:5173/health
```

**选项B: 使用Ultra Memory代替（简化方案）**
```python
# 修改代码，暂时禁用Session Memory
# 文件: packages/core-domain/src/services/project_memory_service.py

def __init__(self, ...):
    self.session_memory_enabled = False  # 暂时禁用
    self.ultra_memory_enabled = True
```

---

### 第3步: 更新MCP服务URL配置

**需要修改的文件**:

#### 文件1: `packages/core-domain/src/services/project_memory_service.py`

找到这些方法，修改URL：

```python
def _store_to_ultra_memory(self, ...):
    # 当前代码：
    url = "http://localhost:3000/mcp_ultra-memory-cloud_store_memory"
    
    # 修改为（根据你的选择）：
    # 选项1: 使用SSH隧道
    url = "http://localhost:3000/mcp_ultra-memory-cloud_store_memory"
    
    # 选项2: 直接连接远程（需要开放端口）
    url = "http://13.158.83.99:7000/api/memory/store"
    
    # 选项3: 使用AWS内网（如果有VPN）
    url = "http://172.31.5.19:7000/api/memory/store"
```

```python
def _query_from_ultra_memory(self, ...):
    # 同样修改URL
    url = "http://localhost:3000/mcp_ultra-memory-cloud_retrieve_memories"
    
    # 修改为对应的远程URL
```

#### 文件2: `scripts/init_project_memory_mcp.py`

```python
# 第17-18行
SESSION_MEMORY_URL = "http://localhost:5173"  # 本地或禁用
ULTRA_MEMORY_URL = "http://localhost:3000"     # 修改为实际URL
```

---

### 第4步: 启动本地API服务

```bash
# 进入API目录
cd /Users/yalinwang/Desktop/任务所\ 1.8/taskflow-v1-2/taskflow-v1-2/apps/api

# 启动服务
uvicorn src.main:app --reload --port 8000

# 在另一个终端测试
curl http://localhost:8000/
curl http://localhost:8000/api/projects/TASKFLOW/memories/stats
```

---

### 第5步: 测试8840环境

```bash
# 1. 确保8840服务运行
lsof -i :8840 | grep LISTEN

# 2. 访问测试
open http://localhost:8840/

# 3. 打开浏览器控制台(F12)，查看：
#    - 是否有API请求
#    - 统计数字是否更新
#    - 是否有JavaScript错误

# 4. 运行自动记录测试
python3 scripts/test_auto_memory.py
```

---

### 第6步: 部署到8820正式环境

```bash
# 1. 备份
cp dashboard-v1.9-20251121/index.html \
   dashboard-v1.9-20251121/index.html.backup-before-auto-memory-$(date +%Y%m%d-%H%M%S)

# 2. 部署
cp dashboard-memory-test-8840/index.html \
   dashboard-v1.9-20251121/index.html

# 3. 验证
open http://localhost:8820/
```

---

## 🔍 问题诊断清单

### 问题1: MCP服务无法连接

**症状**: 
- `curl http://13.158.83.99:7000` 超时
- API调用MCP时失败

**可能原因**:
1. AWS安全组未开放7000端口
2. 服务未启动
3. 防火墙阻止

**解决方案**:

```bash
# 登录服务器检查
ssh -i ~/Desktop/重要/librechat-tokyo-2025.pem ubuntu@13.158.83.99

# 检查服务状态
pm2 list
pm2 logs ultra-memory-mcp

# 检查端口
netstat -tlnp | grep 7000

# 如果服务未启动
cd /home/ubuntu/ultra-memory-cloud-mcp
pm2 start ecosystem.config.js
# 或
node src/server.js

# 测试本地连接
curl http://localhost:7000/health
```

**临时方案 - SSH隧道**:
```bash
# 在本地执行（保持运行）
ssh -i ~/Desktop/重要/librechat-tokyo-2025.pem \
    -L 3000:localhost:7000 \
    ubuntu@13.158.83.99 \
    -N -f

# 这样就可以通过 http://localhost:3000 访问远程的7000端口
# 代码中的URL不需要修改
```

---

### 问题2: API服务启动失败

**检查**:
```bash
cd apps/api
cat api.log  # 查看错误日志

# 常见错误：
# - 端口被占用 → 换端口或kill进程
# - 依赖缺失 → pip install -r requirements.txt
# - 路径错误 → 检查sys.path设置
```

---

### 问题3: 数据库权限问题

**症状**: 无法写入数据库

**解决**:
```bash
chmod 666 database/data/tasks.db
```

---

## 📝 完整部署脚本（给新Cursor用）

```bash
#!/bin/bash
# 记忆空间完整部署脚本

echo "🚀 任务所·Flow v1.9 - 记忆空间完整部署"
echo "================================================"

# 工作目录
cd /Users/yalinwang/Desktop/任务所\ 1.8/taskflow-v1-2/taskflow-v1-2

# ============================================================================
# 第1步: 配置SSH隧道（连接远程MCP）
# ============================================================================
echo ""
echo "第1步: 配置远程MCP连接..."

# 检查是否已有隧道
if lsof -i :3000 | grep ssh > /dev/null; then
    echo "✅ SSH隧道已存在"
else
    echo "🔧 创建SSH隧道..."
    ssh -i ~/Desktop/重要/librechat-tokyo-2025.pem \
        -L 3000:localhost:7000 \
        ubuntu@13.158.83.99 \
        -N -f
    sleep 2
    echo "✅ SSH隧道已创建 (localhost:3000 → remote:7000)"
fi

# 测试连接
if curl -s --connect-timeout 3 http://localhost:3000/health > /dev/null 2>&1; then
    echo "✅ Ultra Memory MCP连接成功"
else
    echo "⚠️ Ultra Memory MCP连接失败，将在降级模式运行"
fi

# ============================================================================
# 第2步: 启动本地API服务
# ============================================================================
echo ""
echo "第2步: 启动API服务..."

# 检查是否已运行
if lsof -i :8000 | grep LISTEN > /dev/null; then
    echo "✅ API服务已在运行"
else
    echo "🔧 启动API服务..."
    cd apps/api
    nohup uvicorn src.main:app --reload --port 8000 > api.log 2>&1 &
    sleep 3
    cd ../..
    
    if lsof -i :8000 | grep LISTEN > /dev/null; then
        echo "✅ API服务启动成功 (端口8000)"
    else
        echo "❌ API服务启动失败，查看 apps/api/api.log"
        exit 1
    fi
fi

# ============================================================================
# 第3步: 初始化MCP记忆空间
# ============================================================================
echo ""
echo "第3步: 初始化项目记忆空间..."
python3 scripts/init_project_memory_mcp.py

# ============================================================================
# 第4步: 测试8840环境
# ============================================================================
echo ""
echo "第4步: 测试8840环境..."

# 检查8840服务
if lsof -i :8840 | grep LISTEN > /dev/null; then
    echo "✅ 8840服务运行中"
else
    echo "🔧 启动8840服务..."
    cd dashboard-memory-test-8840
    nohup python3 -m http.server 8840 > server.log 2>&1 &
    sleep 2
    cd ..
    echo "✅ 8840服务已启动"
fi

# 测试API端点
echo ""
echo "测试API端点..."
curl -s http://localhost:8000/api/projects/TASKFLOW/memories/stats | python3 -m json.tool | head -20

# ============================================================================
# 第5步: 运行自动记录测试
# ============================================================================
echo ""
echo "第5步: 测试自动记录功能..."
python3 scripts/test_auto_memory.py

# ============================================================================
# 第6步: 部署到8820正式环境
# ============================================================================
echo ""
read -p "测试通过，是否部署到8820正式环境？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔧 部署到8820..."
    
    # 备份
    cp dashboard-v1.9-20251121/index.html \
       dashboard-v1.9-20251121/index.html.backup-auto-$(date +%H%M%S)
    
    # 部署
    cp dashboard-memory-test-8840/index.html \
       dashboard-v1.9-20251121/index.html
    
    echo "✅ 部署完成！"
    open http://localhost:8820/
fi

echo ""
echo "================================================"
echo "🎉 部署流程完成！"
echo "================================================"
echo ""
echo "服务状态："
echo "  - API服务: http://localhost:8000"
echo "  - 测试环境: http://localhost:8840"
echo "  - 正式环境: http://localhost:8820"
echo "  - Ultra Memory: http://localhost:3000 (SSH隧道)"
echo ""
```

---

## 🔑 关键配置信息

### MCP服务URL配置

#### 当前代码中的URL（需要确认/修改）

**文件**: `packages/core-domain/src/services/project_memory_service.py`

**第582-590行左右**:
```python
def _store_to_ultra_memory(self, ...):
    url = "http://localhost:3000/mcp_ultra-memory-cloud_store_memory"
    # 这个URL假设通过SSH隧道访问远程服务
```

**第604-612行左右**:
```python
def _query_from_ultra_memory(self, ...):
    url = "http://localhost:3000/mcp_ultra-memory-cloud_retrieve_memories"
```

**第592-602行左右**:
```python
def _store_to_session_memory(self, ...):
    url = "http://localhost:5173/api/memories"
    # Session Memory - 本地服务或禁用
```

---

### 远程MCP API端点格式

根据文档，Ultra Memory Cloud的API端点可能是：

```
存储记忆:
POST http://13.158.83.99:7000/api/memory/store
或
POST http://13.158.83.99:7000/mcp_ultra-memory-cloud_store_memory

检索记忆:
POST http://13.158.83.99:7000/api/memory/retrieve
或  
POST http://13.158.83.99:7000/mcp_ultra-memory-cloud_retrieve_memories

统计信息:
POST http://13.158.83.99:7000/api/memory/stats
或
POST http://13.158.83.99:7000/mcp_ultra-memory-cloud_get_memory_stats
```

**请登录服务器确认实际端点格式！**

---

## 📋 验证清单

### 连接验证
```bash
# 1. SSH连接
ssh -i ~/Desktop/重要/librechat-tokyo-2025.pem ubuntu@13.158.83.99 "echo '✅ SSH连接成功'"

# 2. Ultra Memory MCP服务
ssh -i ~/Desktop/重要/librechat-tokyo-2025.pem ubuntu@13.158.83.99 "curl -s http://localhost:7000/health"

# 3. SSH隧道
curl -s http://localhost:3000/health

# 4. 本地API
curl http://localhost:8000/
```

### 功能验证
```bash
# 1. 记忆统计
curl http://localhost:8000/api/projects/TASKFLOW/memories/stats

# 2. 记忆列表
curl http://localhost:8000/api/projects/TASKFLOW/memories?limit=5

# 3. 自动记录
curl -X POST http://localhost:8000/api/conversations/hook/auto-record \
  -H "Content-Type: application/json" \
  -d '{"user_input":"测试记忆","ai_response":"已记录","ai_role":"assistant"}' \
  --url-query "project_code=TASKFLOW"

# 4. Hook统计
curl http://localhost:8000/api/conversations/hook/stats?project_code=TASKFLOW
```

### 前端验证
```
1. 访问 http://localhost:8840/
2. 滚动到"项目记忆空间Dashboard UI"
3. 检查统计数字是否从API加载（不再是45/12/23/8）
4. 点击"🤖 自动笔记"筛选
5. 打开控制台查看fetch请求
```

---

## 🛠️ 推荐方案：SSH隧道（最简单）

**原理**: 通过SSH隧道将远程7000端口映射到本地3000端口

**优势**:
- ✅ 不需要修改代码
- ✅ 不需要修改AWS安全组
- ✅ 安全性高（通过SSH加密）
- ✅ 即开即用

**操作**:
```bash
# 1. 创建隧道（后台运行）
ssh -i ~/Desktop/重要/librechat-tokyo-2025.pem \
    -L 3000:localhost:7000 \
    ubuntu@13.158.83.99 \
    -N -f

# 2. 验证隧道
curl http://localhost:3000/health

# 3. 隧道会一直运行，直到关闭：
# 查找进程: ps aux | grep "ssh.*3000"
# 关闭隧道: kill <PID>
```

**这样代码中的 `http://localhost:3000` 就能访问到远程MCP了！**

---

## 📊 当前配置状态总结

| 组件 | 状态 | 说明 |
|------|------|------|
| 数据库 | ✅ 100% | 已创建所有表 |
| 后端代码 | ✅ 100% | 完整实现 |
| 前端代码(8840) | ✅ 100% | 已集成API |
| 前端代码(8820) | ❌ 0% | 未部署 |
| API服务 | ❌ 0% | 未启动 |
| Ultra Memory MCP | ❌ 未知 | 需要SSH验证 |
| Session Memory | ❌ 未知 | 可禁用 |
| SSH隧道 | ❌ 0% | 未建立 |

---

## 🎯 最快完成路径（3个命令）

```bash
# 命令1: 建立SSH隧道（连接远程MCP）
ssh -i ~/Desktop/重要/librechat-tokyo-2025.pem -L 3000:localhost:7000 ubuntu@13.158.83.99 -N -f

# 命令2: 启动API服务
cd apps/api && uvicorn src.main:app --reload --port 8000 &

# 命令3: 测试
sleep 3 && python3 scripts/test_auto_memory.py
```

**如果测试通过，再执行部署命令。**

---

## 💡 简化方案（如果MCP不可用）

如果远程MCP服务配置太复杂，可以暂时使用**本地存储模式**：

```python
# 修改: packages/core-domain/src/services/project_memory_service.py

def __init__(self, ...):
    self.session_memory_enabled = False  # 禁用
    self.ultra_memory_enabled = False    # 禁用

# 这样所有记忆只存储在本地SQLite，仍然完全可用！
```

**优势**:
- ✅ 立即可用，无需配置
- ✅ 核心功能不受影响
- ✅ 后续可随时启用MCP

---

## 📞 如果遇到问题

### SSH连不上
1. 检查密钥权限: `chmod 400 ~/Desktop/重要/librechat-tokyo-2025.pem`
2. 尝试备用密钥: `librechat-claude-key`
3. 检查AWS实例是否运行

### MCP端点不对
1. 登录服务器查看: `cat /home/ubuntu/ultra-memory-cloud-mcp/src/server.js`
2. 查看API文档: `cat /home/ubuntu/ultra-memory-cloud-mcp/README.md`
3. 测试端点: `curl -X POST http://localhost:7000/各种路径`

### API启动失败
1. 查看日志: `cat apps/api/api.log`
2. 手动运行测试: `cd apps/api && python3 -m uvicorn src.main:app`
3. 检查依赖: `pip3 list | grep fastapi`

---

## 🎉 成功标志

完成后应该能看到：
- ✅ http://localhost:8000/api/docs 打开API文档
- ✅ http://localhost:8840/ 统计数字动态加载
- ✅ 运行test_auto_memory.py全部测试通过
- ✅ http://localhost:8820/ 部署后功能正常

---

**祝部署顺利！** 🚀

