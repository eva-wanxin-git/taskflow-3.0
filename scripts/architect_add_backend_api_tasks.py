#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
架构师任务：录入18个后端API开发任务到看板
基于：📊前端反向工程-后端API需求分析.md
"""
import sqlite3
from pathlib import Path
from datetime import datetime

# 数据库路径
db_path = Path(__file__).parent.parent / "database" / "data" / "tasks.db"

# 18个后端API任务清单
BACKEND_API_TASKS = [
    # Phase 1: 核心Dashboard数据（P0，8小时）
    {
        "id": "TASK-API-001",
        "title": "创建统一统计API",
        "description": """创建 GET /api/stats/overview 端点
        
功能：提供Dashboard顶部9个统计卡片的数据
- 总任务数
- 进行中/待处理/已完成
- 完成率
- P0任务数
- 事件总数
- 记忆数量
- 会话数

输出格式：JSON
位置：apps/api/src/routes/stats.py
预期结果：前端9个统计卡片显示真实数据""",
        "priority": "P0",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,dashboard,statistics,p0,mvp"
    },
    {
        "id": "TASK-API-002",
        "title": "创建功能清单API",
        "description": """创建功能清单查询端点

端点1: GET /api/features/implemented
- 返回已实现功能列表（~132个）
- 数据源：automation-data/v17-complete-features.json

端点2: GET /api/features/partial
- 返回部分实现功能列表（~17个）
- 包含进度百分比和缺失部分

位置：apps/api/src/routes/features.py
预期结果：项目透视塔Tab1和Tab2可显示真实数据""",
        "priority": "P0",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,features,project-overview,p0,mvp"
    },
    {
        "id": "TASK-API-003",
        "title": "创建问题和建议管理API",
        "description": """创建问题和建议管理端点

端点1: GET /api/issues
- 返回问题清单（~15个）
- 包含：标题、描述、优先级、影响、建议方案

端点2: POST /api/issues/{id}/generate-task
- 将问题转换为任务

端点3: GET /api/suggestions
- 返回架构建议清单（~12条）

端点4: POST /api/suggestions/{id}/adopt
- 采纳建议，生成任务

位置：apps/api/src/routes/issues.py, suggestions.py
预期结果：项目透视塔Tab3和Tab4可用""",
        "priority": "P0",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,issues,suggestions,project-management,p0,mvp"
    },
    {
        "id": "TASK-API-004",
        "title": "任务看板格式化API",
        "description": """扩展任务查询API，支持看板格式输出

端点: GET /api/tasks/kanban
- 参数：project_id, assigned_to
- 返回格式：
  {
    pending: [...],
    in_progress: [...],
    completed: [...]
  }
- 任务卡片包含：ID、标题、优先级、预估工时、标签

位置：apps/api/src/routes/task_board.py（扩展）
预期结果：全栈工程师看板Tab可拖拽显示""",
        "priority": "P0",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,kanban,task-management,p0,mvp"
    },
    
    # Phase 2: 工作台核心功能（P1，10小时）
    {
        "id": "TASK-API-005",
        "title": "事件流参数扩展",
        "description": """为现有事件流API添加筛选参数

扩展端点: GET /api/events
- 新增参数：category（architecture/development/operations）
- 新增参数：role（architect/fullstack-engineer/sre）
- 新增参数：real_time（实时模式）

位置：apps/api/src/routes/events.py（扩展）
预期结果：各角色工作台可按类别筛选事件流""",
        "priority": "P1",
        "estimated_hours": 1.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,events,filtering,p1,mvp"
    },
    {
        "id": "TASK-API-006",
        "title": "需求管理API",
        "description": """创建需求管理端点

端点1: GET /api/requirements
- 参数：project_id, source（user/architect）
- 返回用户需求或架构师建议任务

端点2: PUT /api/requirements/{id}/status
- 更新需求状态（待评估/已规划/开发中/已完成）

位置：apps/api/src/routes/requirements.py
预期结果：待开发任务池Tab可用""",
        "priority": "P1",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,requirements,task-pool,p1"
    },
    {
        "id": "TASK-API-007",
        "title": "代码审查结果API",
        "description": """创建代码审查管理端点

端点1: GET /api/code-reviews
- 返回审查清单（~15个审查项）
- 包含：文件路径、审查结果、问题数、建议

端点2: POST /api/code-reviews
- 提交新的审查结果

位置：apps/api/src/routes/code_reviews.py
预期结果：全栈工程师Tab3代码审查可用""",
        "priority": "P1",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,code-review,quality,p1"
    },
    {
        "id": "TASK-API-008",
        "title": "技术文档索引API",
        "description": """创建文档索引端点

端点1: GET /api/documents
- 参数：project_id, category（technical/api/architecture）
- 返回文档列表（~68篇）
- 扫描docs/目录生成

端点2: GET /api/documents/{id}/content
- 返回文档完整内容（Markdown格式）

位置：apps/api/src/routes/documents.py
预期结果：技术文档Tab可树形展示""",
        "priority": "P1",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,documentation,knowledge,p1"
    },
    {
        "id": "TASK-API-009",
        "title": "Bug管理API",
        "description": """创建Bug管理端点

端点1: GET /api/bugs
- 返回看板格式（待修复/修复中/已验证）
- 基于issues表，type='bug'

端点2: POST /api/bugs
- 创建新Bug

端点3: PUT /api/bugs/{id}/status
- 更新Bug状态

位置：apps/api/src/routes/bugs.py
预期结果：运维工程师Bug看板可用""",
        "priority": "P1",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,bugs,issue-tracking,p1"
    },
    {
        "id": "TASK-API-010",
        "title": "运维日志查询API",
        "description": """创建运维日志查询端点

端点: GET /api/logs/operations
- 参数：project_id, level（INFO/WARN/ERROR）, limit, page
- 返回日志列表（~847条）
- 数据源：系统日志文件或日志表

位置：apps/api/src/routes/logs.py
预期结果：运维日志Tab时间轴显示""",
        "priority": "P1",
        "estimated_hours": 1.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,logs,operations,p1"
    },
    
    # Phase 3: 运维和监控（P0，5小时）
    {
        "id": "TASK-API-011",
        "title": "系统监控增强API",
        "description": """扩展系统健康检查端点

扩展端点: GET /api/system/health
- 当前仅简单检查，需要增强为完整监控
- 返回6个服务状态：
  * API Server (端口8800)
  * Dashboard (端口8820)
  * 其他服务
- 每个服务包含：状态、端口、响应时间、CPU、内存
- 系统总览：总CPU、总内存、磁盘空间

位置：apps/api/src/routes/health.py（扩展）
预期结果：运维工程师系统状态Tab显示6个服务""",
        "priority": "P0",
        "estimated_hours": 3.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,monitoring,system-health,p0"
    },
    {
        "id": "TASK-API-012",
        "title": "代码清单统计API",
        "description": """创建代码清单端点

端点: GET /api/code/inventory
- 扫描项目代码目录
- 返回文件列表（~45个文件）
- 包含：路径、代码行数、复杂度、最后修改时间、语言

位置：apps/api/src/routes/code_inventory.py
预期结果：Noah代码管家Tab2可显示目录树""",
        "priority": "P1",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,code-analysis,inventory,p1"
    },
    
    # Phase 4: 实时和高级功能（P2，6小时）
    {
        "id": "TASK-API-013",
        "title": "实时脉搏统计API",
        "description": """创建实时脉搏数据端点

端点: GET /api/pulse/realtime
- 更新间隔：30秒
- 返回：活跃任务数、最近事件数、平均响应时间、最后活动时间

位置：apps/api/src/routes/pulse.py
预期结果：实时脉动系统Tab2可用""",
        "priority": "P2",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,realtime,pulse,p2"
    },
    {
        "id": "TASK-API-014",
        "title": "AI协作链可视化API",
        "description": """创建协作链数据端点

端点: GET /api/collaboration/chain
- 返回节点：各角色（架构师/工程师/SRE）的任务数和活跃数
- 返回边：角色间任务流转数量

位置：apps/api/src/routes/collaboration.py
预期结果：实时脉动系统Tab3可视化图表""",
        "priority": "P2",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,visualization,collaboration,p2"
    },
    {
        "id": "TASK-API-015",
        "title": "WebSocket实时推送",
        "description": """创建WebSocket连接端点

端点: WS /ws/events
- 实时推送新事件到前端
- 避免轮询，降低服务器负载

位置：apps/api/src/websockets/events.py
预期结果：Dashboard可实时显示新事件（可选功能）""",
        "priority": "P2",
        "estimated_hours": 2.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,websocket,realtime,p2"
    },
    
    # 扩展任务（现有API参数扩展）
    {
        "id": "TASK-API-EXT-001",
        "title": "对话API增加角色筛选",
        "description": """扩展对话查询API

扩展端点: GET /api/conversations
- 新增参数：role（architect/fullstack-engineer/sre）
- 按角色筛选对话历史

位置：apps/api/src/routes/conversations.py（扩展）
预期结果：各工作台对话历史Tab显示对应角色的对话""",
        "priority": "P1",
        "estimated_hours": 0.5,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,conversations,extension,p1"
    },
    {
        "id": "TASK-API-EXT-002",
        "title": "任务API增加分配者筛选",
        "description": """扩展任务查询API

扩展端点: GET /api/tasks
- 新增参数：assigned_to（筛选指定执行者的任务）

位置：apps/api/src/routes/task_board.py（扩展）
预期结果：Noah任务队列Tab可用""",
        "priority": "P1",
        "estimated_hours": 0.5,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,tasks,extension,p1"
    },
    {
        "id": "TASK-API-EXT-003",
        "title": "知识库API完善",
        "description": """完善知识库查询API

验证端点: GET /api/knowledge-base
- 表结构已存在（knowledge_articles）
- 验证API端点是否完整
- 如缺失则补充

位置：apps/api/src/routes/knowledge_base.py
预期结果：运维工程师知识库Tab显示128篇文档""",
        "priority": "P1",
        "estimated_hours": 1.0,
        "status": "pending",
        "assigned_to": "fullstack-engineer",
        "tags": "api,knowledge-base,verification,p1"
    },
]

def create_tasks():
    """创建任务到数据库"""
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    print("=" * 70)
    print("架构师任务：录入后端API开发任务到看板")
    print("=" * 70)
    print()
    
    # 检查是否已存在
    existing_count = 0
    new_count = 0
    
    for task in BACKEND_API_TASKS:
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE id = ?", (task["id"],))
        exists = cursor.fetchone()[0] > 0
        
        if exists:
            print(f"[SKIP] {task['id']} - already exists")
            existing_count += 1
            continue
        
        # 插入任务
        import json
        metadata = json.dumps({"tags": task["tags"].split(",")})
        
        cursor.execute("""
            INSERT INTO tasks (
                id, title, description, status, priority, 
                estimated_hours, assigned_to, metadata, 
                project_id, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task["id"],
            task["title"],
            task["description"],
            task["status"],
            task["priority"],
            task["estimated_hours"],
            task["assigned_to"],
            metadata,
            "TASKFLOW",
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        print(f"[OK] {task['id']:20s} - {task['title'][:40]:40s} [{task['priority']}] {task['estimated_hours']}h")
        new_count += 1
    
    conn.commit()
    conn.close()
    
    print()
    print("=" * 70)
    print(f"Summary:")
    print(f"  New tasks: {new_count}")
    print(f"  Already exists: {existing_count}")
    print(f"  Total: {len(BACKEND_API_TASKS)}")
    print()
    print("Dashboard updated! Visit:")
    print("   http://localhost:8877")
    print("   http://localhost:8820")
    print("=" * 70)

if __name__ == "__main__":
    create_tasks()

