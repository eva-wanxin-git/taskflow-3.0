#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速启动透视塔API服务
只包含透视塔需要的3个新端点
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from datetime import datetime
import uvicorn

app = FastAPI(title="透视塔API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据文件路径
DATA_DIR = Path(__file__).parent / "apps" / "dashboard" / "automation-data"

def load_json_file(file_path: Path):
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.get("/")
async def root():
    return {
        "name": "透视塔API",
        "version": "1.0.0",
        "endpoints": {
            "features_implemented": "/api/features/implemented",
            "features_partial": "/api/features/partial",
            "issues": "/api/issues",
            "suggestions": "/api/suggestions",
            "architect_events": "/api/architect/events",
            "architect_monitor": "/api/architect/monitor",
            "architect_conversations": "/api/architect/conversations",
            "engineer_events": "/api/engineer/events",
            "engineer_conversations": "/api/engineer/conversations",
            "engineer_tasks": "/api/engineer/tasks",
            "engineer_task_accept": "/api/engineer/tasks/{task_id}/accept",
            "engineer_task_complete": "/api/engineer/tasks/{task_id}/complete",
            "engineer_reviews": "/api/engineer/reviews",
            "engineer_review_approve": "/api/engineer/reviews/{review_id}/approve",
            "engineer_review_reject": "/api/engineer/reviews/{review_id}/reject",
            "pulse_events": "/api/pulse/events",
            "memory_stats": "/api/projects/TASKFLOW/memories/stats",
            "memory_list": "/api/projects/TASKFLOW/memories"
        }
    }

@app.get("/api/features/implemented")
async def get_implemented_features():
    """获取已实现功能列表"""
    data = load_json_file(DATA_DIR / "v17-complete-features.json")
    features = data.get("implemented", [])

    # 按类型分组统计
    categories = {}
    for feature in features:
        category = feature.get("type", "其他")
        categories[category] = categories.get(category, 0) + 1

    return {
        "success": True,
        "total": len(features),
        "features": features,
        "categories": categories,
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/features/partial")
async def get_partial_features():
    """获取部分实现功能列表"""
    data = load_json_file(DATA_DIR / "partial-features.json")
    features = data.get("partial_features", [])

    # 计算平均进度
    avg_progress = sum(f.get("progress", 0) for f in features) / len(features) if features else 0

    return {
        "success": True,
        "total": len(features),
        "features": features,
        "avg_progress": round(avg_progress, 1),
        "updated_at": data.get("updated_at", datetime.now().isoformat())
    }

@app.get("/api/issues")
async def get_issues():
    """获取问题清单"""
    data = load_json_file(DATA_DIR / "project-issues.json")
    issues = data.get("issues", [])

    # 统计
    priority_stats = {}
    severity_stats = {}
    total_hours = 0

    for issue in issues:
        p = issue.get("priority", "未知")
        s = issue.get("severity", "未知")
        priority_stats[p] = priority_stats.get(p, 0) + 1
        severity_stats[s] = severity_stats.get(s, 0) + 1
        total_hours += issue.get("estimated_hours", 0)

    return {
        "success": True,
        "total": len(issues),
        "issues": issues,
        "stats": {
            "by_priority": priority_stats,
            "by_severity": severity_stats,
            "total_estimated_hours": round(total_hours, 1)
        },
        "updated_at": data.get("updated_at", datetime.now().isoformat())
    }

@app.get("/api/suggestions")
async def get_suggestions():
    """获取架构建议清单"""
    data = load_json_file(DATA_DIR / "architecture-suggestions.json")
    suggestions = data.get("suggestions", [])

    # 统计
    category_stats = {}
    priority_stats = {}
    total_hours = 0

    for sugg in suggestions:
        cat = sugg.get("category", "其他")
        pri = sugg.get("priority", "未知")
        category_stats[cat] = category_stats.get(cat, 0) + 1
        priority_stats[pri] = priority_stats.get(pri, 0) + 1
        total_hours += sugg.get("estimated_hours", 0)

    # 按优先级排序
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    suggestions.sort(key=lambda x: priority_order.get(x.get("priority", "P3"), 999))

    return {
        "success": True,
        "total": len(suggestions),
        "suggestions": suggestions,
        "stats": {
            "by_category": category_stats,
            "by_priority": priority_stats,
            "total_estimated_hours": round(total_hours, 1)
        },
        "updated_at": data.get("updated_at", datetime.now().isoformat())
    }

@app.get("/api/features/summary")
async def get_features_summary():
    """获取功能实现概况"""
    complete_data = load_json_file(DATA_DIR / "v17-complete-features.json")
    partial_data = load_json_file(DATA_DIR / "partial-features.json")

    implemented_count = len(complete_data.get("implemented", []))
    partial_count = len(partial_data.get("partial_features", []))
    total = implemented_count + partial_count

    completion_rate = (implemented_count / total * 100) if total > 0 else 0

    return {
        "success": True,
        "implemented_count": implemented_count,
        "partial_count": partial_count,
        "total_features": total,
        "completion_rate": round(completion_rate, 1),
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/architect/events")
async def get_architect_events():
    """获取架构师事件流"""
    data = load_json_file(DATA_DIR / "architect_events.json")
    events = data.get("events", [])

    return {
        "success": True,
        "total": len(events),
        "events": events,
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/architect/monitor")
async def get_architect_monitor():
    """获取架构师监控数据"""
    data = load_json_file(DATA_DIR / "architect_monitor.json")

    return {
        "success": True,
        "data": data,
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/architect/conversations")
async def get_architect_conversations():
    """获取架构师对话历史"""
    data = load_json_file(DATA_DIR / "architect-conversations.json")
    sessions = data.get("sessions", [])
    stats = data.get("stats", {})

    return {
        "success": True,
        "total": len(sessions),
        "sessions": sessions,
        "stats": stats,
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/dashboard/overview")
async def get_dashboard_overview():
    """获取Dashboard主页统计数据"""
    # 加载各种数据
    architect_monitor = load_json_file(DATA_DIR / "architect_monitor.json")
    architect_events = load_json_file(DATA_DIR / "architect_events.json")
    architect_conversations = load_json_file(DATA_DIR / "architect-conversations.json")
    pulse_events = load_json_file(DATA_DIR / "realtime_pulse_events.json")

    # 计算任务统计（从architect_monitor中获取）
    project_info = architect_monitor.get("project_info", {})
    total_tasks = project_info.get("total_tasks", 0)
    pending_tasks = project_info.get("pending_tasks", 0)
    completed_tasks = project_info.get("completed_tasks", 0)
    cancelled_tasks = project_info.get("cancelled_tasks", 0)
    in_progress_tasks = max(0, total_tasks - pending_tasks - completed_tasks - cancelled_tasks)  # 确保不为负数

    # Token使用
    token_usage = architect_monitor.get("token_usage", {})
    token_used = token_usage.get("used", 0)

    # 事件数（从architect_events）
    total_architect_events = len(architect_events.get("events", []))

    # 会话数和消息数
    conversations = architect_conversations.get("sessions", [])
    total_conversations = len(conversations)
    total_messages = sum(s.get("messages_count", 0) for s in conversations)

    # 记忆数（暂时使用占位数据，实际应该从记忆系统获取）
    total_memories = 45
    memory_decisions = 12

    # 今日增量
    today = datetime.now().strftime("%Y-%m-%d")
    today_events = [e for e in architect_events.get("events", []) if e.get("timestamp", "").startswith(today)]

    return {
        "success": True,
        "existing_stats": {
            "total_tasks": total_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks,
            "cancelled_tasks": cancelled_tasks,
            "token_used": token_used,
            "today_pending_change": len([e for e in today_events if e.get("type") == "task_create"]),
            "today_completed_change": len([e for e in today_events if e.get("type") == "task_complete"])
        },
        "new_stats": {
            "total_events": total_architect_events,
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "total_memories": total_memories,
            "memory_decisions": memory_decisions,
            "today_events_change": len(today_events)
        },
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/engineer/events")
async def get_engineer_events():
    """获取全栈工程师事件流"""
    data = load_json_file(DATA_DIR / "engineer_events.json")
    events = data.get("events", [])

    return {
        "success": True,
        "total": len(events),
        "events": events,
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/engineer/conversations")
async def get_engineer_conversations():
    """获取全栈工程师对话历史"""
    data = load_json_file(DATA_DIR / "engineer-conversations.json")
    sessions = data.get("sessions", [])
    stats = data.get("stats", {})

    return {
        "success": True,
        "total": len(sessions),
        "sessions": sessions,
        "stats": stats,
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/engineer/tasks")
async def get_engineer_tasks():
    """获取全栈工程师任务列表（实时从数据库读取）"""
    import sqlite3
    db_path = Path(__file__).parent / "database" / "data" / "tasks.db"

    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # 查询所有全栈工程师任务（实时数据）
        cursor.execute("""
            SELECT id, title, description, status, priority,
                   estimated_hours, actual_hours, complexity,
                   assigned_to, created_at, updated_at,
                   completed_at, metadata
            FROM tasks
            WHERE assigned_to IN ('fullstack-engineer', '全栈工程师', '李明')
            ORDER BY
                CASE status
                    WHEN 'in_progress' THEN 1
                    WHEN 'pending' THEN 2
                    WHEN 'completed' THEN 3
                    ELSE 4
                END,
                CASE priority
                    WHEN 'P0' THEN 0
                    WHEN 'P1' THEN 1
                    WHEN 'P2' THEN 2
                    ELSE 3
                END,
                created_at DESC
        """)

        tasks = []
        for row in cursor.fetchall():
            task = dict(row)
            # 从metadata解析tags和parallel
            if task.get('metadata'):
                try:
                    metadata = json.loads(task['metadata'])
                    task['tags'] = metadata.get('tags', [])
                    task['parallel'] = metadata.get('parallel', False)
                except:
                    task['tags'] = []
                    task['parallel'] = False
            else:
                task['tags'] = []
                task['parallel'] = False
            tasks.append(task)

        # 按状态分组
        tasks_by_status = {
            'pending': [t for t in tasks if t['status'] == 'pending'],
            'in_progress': [t for t in tasks if t['status'] == 'in_progress'],
            'completed': [t for t in tasks if t['status'] == 'completed']
        }

        stats = {
            'total': len(tasks),
            'pending': len(tasks_by_status['pending']),
            'in_progress': len(tasks_by_status['in_progress']),
            'completed': len(tasks_by_status['completed'])
        }

        conn.close()

        return {
            "success": True,
            "total": len(tasks),
            "tasks": tasks,
            "tasks_by_status": tasks_by_status,
            "stats": stats,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"获取任务失败: {str(e)}",
            "error": str(e),
            "tasks": [],
            "stats": {"total": 0, "pending": 0, "in_progress": 0, "completed": 0}
        }

# 旧的数据库查询版本（已废弃）
@app.get("/api/engineer/tasks/old")
async def get_engineer_tasks_old():
    """获取全栈工程师任务列表（从数据库读取实时数据）- 已废弃"""
    import sqlite3
    db_path = Path(__file__).parent / "database" / "data" / "tasks.db"

    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row  # 返回字典格式
        cursor = conn.cursor()

        # 查询所有全栈工程师任务（不查询tags和parallel列）
        cursor.execute("""
            SELECT id, title, description, status, priority,
                   estimated_hours, actual_hours, complexity,
                   assigned_to, metadata,
                   created_at, updated_at, completed_at
            FROM tasks
            WHERE assigned_to = 'fullstack-engineer'
            ORDER BY
                CASE priority
                    WHEN 'P0' THEN 0
                    WHEN 'P1' THEN 1
                    WHEN 'P2' THEN 2
                    WHEN 'P3' THEN 3
                    ELSE 4
                END,
                created_at DESC
        """)

        rows = cursor.fetchall()
        tasks = [dict(row) for row in rows]

        # 统计各状态任务数
        stats = {
            "pending": 0,
            "in_progress": 0,
            "completed": 0
        }

        for task in tasks:
            status = task.get("status", "pending")
            if status in stats:
                stats[status] += 1

        conn.close()

        return {
            "success": True,
            "total": len(tasks),
            "tasks": tasks,
            "stats": stats,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"获取任务列表失败: {str(e)}",
            "error": str(e),
            "tasks": [],
            "stats": {"pending": 0, "in_progress": 0, "completed": 0}
        }

@app.post("/api/engineer/tasks/{task_id}/accept")
async def accept_task(task_id: str):
    """接受任务 - 状态从pending变为in_progress"""
    import sqlite3
    db_path = Path(__file__).parent / "database" / "data" / "tasks.db"

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # 更新任务状态
        cursor.execute("""
            UPDATE tasks
            SET status = 'in_progress',
                updated_at = datetime('now'),
                assigned_at = datetime('now')
            WHERE id = ?
        """, (task_id,))

        conn.commit()
        conn.close()

        return {
            "success": True,
            "message": f"任务 {task_id} 已接受，状态更新为进行中",
            "task_id": task_id,
            "new_status": "in_progress",
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"接受任务失败: {str(e)}",
            "error": str(e)
        }

@app.post("/api/engineer/tasks/{task_id}/complete")
async def complete_task(task_id: str, completion_data: dict):
    """提交完成报告 - 状态从in_progress变为completed"""
    import sqlite3
    db_path = Path(__file__).parent / "database" / "data" / "tasks.db"

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # 获取任务的实际工时
        actual_hours = completion_data.get("actual_hours", 0)

        # 更新任务状态
        cursor.execute("""
            UPDATE tasks
            SET status = 'completed',
                actual_hours = ?,
                updated_at = datetime('now'),
                completed_at = datetime('now')
            WHERE id = ?
        """, (actual_hours, task_id))

        # 插入或更新完成详情
        cursor.execute("""
            INSERT OR REPLACE INTO task_completions
            (task_id, features_implemented, files_created, files_modified,
             code_lines, actual_hours, notes, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            task_id,
            json.dumps(completion_data.get("features", []), ensure_ascii=False),
            json.dumps(completion_data.get("files_created", []), ensure_ascii=False),
            json.dumps(completion_data.get("files_modified", []), ensure_ascii=False),
            completion_data.get("code_lines", 0),
            actual_hours,
            completion_data.get("notes", "")
        ))

        conn.commit()
        conn.close()

        return {
            "success": True,
            "message": f"任务 {task_id} 已完成",
            "task_id": task_id,
            "new_status": "completed",
            "actual_hours": actual_hours,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"提交完成失败: {str(e)}",
            "error": str(e)
        }

# ============================================
# 代码审查相关API
# ============================================

@app.get("/api/engineer/reviews")
async def get_code_reviews():
    """获取代码审查列表"""
    data = load_json_file(DATA_DIR / "engineer-code-reviews.json")
    reviews = data.get("reviews", [])
    stats = data.get("stats", {})

    return {
        "success": True,
        "total": len(reviews),
        "reviews": reviews,
        "stats": stats,
        "updated_at": datetime.now().isoformat()
    }

@app.post("/api/engineer/reviews/{review_id}/approve")
async def approve_review(review_id: str):
    """通过代码审查"""
    data_file = DATA_DIR / "engineer-code-reviews.json"
    data = load_json_file(data_file)

    # 查找审查记录
    review = None
    for r in data.get("reviews", []):
        if r["review_id"] == review_id:
            review = r
            break

    if not review:
        return {
            "success": False,
            "message": f"审查记录 {review_id} 不存在"
        }

    # 更新状态
    review["status"] = "approved"
    review["reviewed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 更新统计
    data["stats"]["pending_review"] = data["stats"].get("pending_review", 0) - 1
    data["stats"]["approved"] = data["stats"].get("approved", 0) + 1

    # 保存文件
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "success": True,
        "message": f"审查 {review_id} 已通过",
        "review_id": review_id,
        "task_id": review["task_id"],
        "new_status": "approved",
        "updated_at": datetime.now().isoformat()
    }

@app.post("/api/engineer/reviews/{review_id}/reject")
async def reject_review(review_id: str, reject_data: dict):
    """拒绝代码审查，要求修改"""
    data_file = DATA_DIR / "engineer-code-reviews.json"
    data = load_json_file(data_file)

    # 查找审查记录
    review = None
    for r in data.get("reviews", []):
        if r["review_id"] == review_id:
            review = r
            break

    if not review:
        return {
            "success": False,
            "message": f"审查记录 {review_id} 不存在"
        }

    # 更新状态
    review["status"] = "rejected"
    review["reviewed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    review["review_notes"] = reject_data.get("notes", "需要修改")

    # 更新统计
    data["stats"]["pending_review"] = data["stats"].get("pending_review", 0) - 1
    data["stats"]["rejected"] = data["stats"].get("rejected", 0) + 1

    # 保存文件
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "success": True,
        "message": f"审查 {review_id} 已拒绝，要求修改",
        "review_id": review_id,
        "task_id": review["task_id"],
        "new_status": "rejected",
        "notes": reject_data.get("notes", ""),
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/pending-tasks")
async def get_pending_tasks():
    """获取待开发任务池数据"""
    data = load_json_file(DATA_DIR / "pending_tasks.json")
    user_requirements = data.get("user_requirements", [])
    architect_suggestions = data.get("architect_suggestions", [])
    stats = data.get("stats", {})

    return {
        "success": True,
        "user_requirements": user_requirements,
        "architect_suggestions": architect_suggestions,
        "stats": stats,
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/projects/TASKFLOW/memories/stats")
async def get_memory_stats():
    """获取项目记忆统计"""
    import sqlite3
    db_path = Path(__file__).parent / "database" / "data" / "tasks.db"

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # 查询统计
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN memory_type = 'decision' THEN 1 ELSE 0 END) as decisions,
                SUM(CASE WHEN memory_type = 'solution' THEN 1 ELSE 0 END) as solutions,
                SUM(CASE WHEN category = 'knowledge' THEN 1 ELSE 0 END) as knowledge,
                SUM(CASE WHEN importance >= 8 THEN 1 ELSE 0 END) as important
            FROM project_memories
            WHERE project_id = 'TASKFLOW'
        """)
        row = cursor.fetchone()
        conn.close()

        return {
            "success": True,
            "project_id": "TASKFLOW",
            "stats": {
                "total_memories": row[0] if row else 0,
                "decision_memories": row[1] if row else 0,
                "solution_memories": row[2] if row else 0,
                "by_category": {"knowledge": row[3] if row else 0},
                "by_importance": {"critical (9-10)": row[4] if row else 0},
                "last_updated": datetime.now().isoformat()
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/projects/TASKFLOW/memories")
async def get_memories():
    """获取项目记忆列表"""
    import sqlite3
    db_path = Path(__file__).parent / "database" / "data" / "tasks.db"

    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM project_memories
            WHERE project_id = 'TASKFLOW'
            ORDER BY importance DESC, created_at DESC
            LIMIT 50
        """)
        rows = cursor.fetchall()

        memories = []
        for row in rows:
            memory = dict(row)
            # 解析JSON字段
            for field in ['tags', 'related_tasks', 'related_issues']:
                if memory.get(field):
                    try:
                        memory[field] = json.loads(memory[field])
                    except:
                        memory[field] = []
            memories.append(memory)

        conn.close()

        return {
            "success": True,
            "project_id": "TASKFLOW",
            "memories": memories,
            "count": len(memories),
            "retrieved_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"success": False, "error": str(e), "memories": []}

@app.get("/api/pulse/events")
async def get_pulse_events():
    """获取实时脉动事件流（全角色）"""
    data = load_json_file(DATA_DIR / "realtime_pulse_events.json")
    events = data.get("events", [])
    stats = data.get("stats", {})

    # 按时间倒序排列
    events_sorted = sorted(events, key=lambda x: x.get("timestamp", ""), reverse=True)

    return {
        "success": True,
        "total": len(events_sorted),
        "events": events_sorted,
        "stats": stats,
        "updated_at": datetime.now().isoformat()
    }

@app.post("/api/architect/save-conversation")
async def save_conversation(conversation: dict):
    """保存新的对话记录"""
    try:
        file_path = DATA_DIR / "architect-conversations.json"

        # 读取现有数据
        data = load_json_file(file_path)
        sessions = data.get("sessions", [])

        # 生成新的session_id
        session_id = f"conv-{str(len(sessions) + 1).zfill(3)}"

        # 构建新对话记录
        new_session = {
            "session_id": session_id,
            "title": conversation.get("title", "未命名对话"),
            "project_id": conversation.get("project_id", "TASKFLOW"),
            "model": conversation.get("model", "claude-3-5-sonnet-4"),
            "status": conversation.get("status", "completed"),
            "total_tokens": conversation.get("total_tokens", 0),
            "messages_count": conversation.get("messages_count", 0),
            "created_at": conversation.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "participants": conversation.get("participants", ["用户", "AI架构师"]),
            "summary": conversation.get("summary", ""),
            "messages": [],
            "started_at": conversation.get("started_at", datetime.now().isoformat()),
            "last_active": datetime.now().isoformat(),
            "tags": conversation.get("tags", [])
        }

        # 添加到列表
        sessions.append(new_session)

        # 更新统计
        data["sessions"] = sessions
        data["stats"] = {
            "total_conversations": len(sessions),
            "active_conversations": sum(1 for s in sessions if s.get("status") == "active"),
            "total_tokens": sum(s.get("total_tokens", 0) for s in sessions),
            "total_messages": sum(s.get("messages_count", 0) for s in sessions),
            "last_updated": datetime.now().isoformat()
        }

        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {
            "success": True,
            "message": "对话记录已保存",
            "session_id": session_id,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"保存失败: {str(e)}"
        }

@app.post("/api/rescan")
async def trigger_rescan():
    """触发重新扫描项目 - 返回实时统计"""
    import subprocess
    from pathlib import Path

    project_root = Path(__file__).parent
    script_path = project_root / "scripts" / "auto_update_insight_data.py"

    if not script_path.exists():
        return {
            "success": False,
            "message": "扫描脚本不存在",
            "path": str(script_path)
        }

    try:
        # 运行扫描脚本
        result = subprocess.run(
            ["python3", str(script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            # 重新加载更新后的数据
            complete_data = load_json_file(DATA_DIR / "v17-complete-features.json")

            # 提取统计信息
            scan_stats = complete_data.get("summary", {}).get("scan_stats", {})

            return {
                "success": True,
                "message": "扫描完成，数据已更新",
                "stats": {
                    "features_count": len(complete_data.get("implemented", [])),
                    "files_count": scan_stats.get("total_files", 0),
                    "lines_count": scan_stats.get("total_lines", 0),
                    "py_files": scan_stats.get("py_files", 0),
                    "html_files": scan_stats.get("html_files", 0),
                    "json_files": scan_stats.get("json_files", 0)
                },
                "scan_time": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "message": "扫描失败",
                "error": result.stderr
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "扫描超时（>30秒）"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"扫描异常: {str(e)}"
        }

# ============================================================================
# 记忆空间API端点
# ============================================================================

# 内存存储记忆数据（简单实现）
memories_storage = []

@app.get("/api/memories/stats")
async def get_memory_stats():
    """获取记忆统计数据"""
    # 从内存中统计
    total = len(memories_storage)
    decision_count = sum(1 for m in memories_storage if m.get('type') == 'decision')
    solution_count = sum(1 for m in memories_storage if m.get('type') == 'solution')
    important_count = sum(1 for m in memories_storage if m.get('importance', 5) >= 9)

    return {
        "success": True,
        "stats": {
            "total_memories": total,
            "decision_memories": decision_count,
            "solution_memories": solution_count,
            "by_importance": {
                "critical (9-10)": important_count
            }
        },
        "updated_at": datetime.now().isoformat()
    }

@app.get("/api/memories")
async def get_memories():
    """获取记忆列表"""
    return {
        "success": True,
        "memories": memories_storage,
        "count": len(memories_storage),
        "updated_at": datetime.now().isoformat()
    }

@app.post("/api/memories")
async def create_memory(memory_data: dict):
    """创建新记忆"""
    new_memory = {
        "id": f"mem_{len(memories_storage) + 1}_{datetime.now().strftime('%H%M%S')}",
        "title": memory_data.get("title"),
        "content": memory_data.get("content"),
        "memory_type": memory_data.get("type", "knowledge"),
        "category": memory_data.get("type", "knowledge"),
        "type": memory_data.get("type", "knowledge"),
        "importance": 5,
        "created_by": "用户",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "tags": memory_data.get("tags", [])
    }

    memories_storage.append(new_memory)

    return {
        "success": True,
        "message": "记忆创建成功",
        "memory": new_memory
    }

@app.post("/api/update_project_info")
async def update_project_info(request: Request):
    """更新项目信息（架构师激活后调用）"""
    try:
        data = await request.json()

        # 保存项目信息到配置文件
        config_file = Path(__file__).parent / ".taskflow" / "project_info.json"
        config_file.parent.mkdir(exist_ok=True)

        project_info = {
            "project_name": data.get("project_name"),
            "description": data.get("description"),
            "tech_stack": data.get("tech_stack", []),
            "components": data.get("components", []),
            "estimated_time": data.get("estimated_time"),
            "updated_at": datetime.now().isoformat(),
            "updated_by": "architect_ai"
        }

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(project_info, f, indent=2, ensure_ascii=False)

        return {
            "success": True,
            "message": "项目信息已更新",
            "data": project_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/get_project_info")
async def get_project_info():
    """获取项目信息"""
    config_file = Path(__file__).parent / ".taskflow" / "project_info.json"

    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    # 返回默认信息
    project_name = Path(__file__).parent.name
    return {
        "project_name": project_name,
        "description": "企业级AI任务中板 | 多项目支持 · 智能跟踪管理",
        "tech_stack": "检测中...",
        "estimated_time": "待分析"
    }

@app.post("/api/initialize_memory_space")
async def initialize_memory_space(request: Request):
    """初始化独立项目记忆空间"""
    try:
        data = await request.json()
        project_code = data.get("project_code")
        project_id = data.get("project_id")

        # 创建本地记忆空间
        memory_dir = Path(__file__).parent / ".taskflow" / "memories" / project_id
        memory_dir.mkdir(parents=True, exist_ok=True)

        # 创建子目录
        (memory_dir / "conversations").mkdir(exist_ok=True)
        (memory_dir / "decisions").mkdir(exist_ok=True)
        (memory_dir / "solutions").mkdir(exist_ok=True)
        (memory_dir / "knowledge").mkdir(exist_ok=True)

        # 创建元数据
        metadata = {
            "project_code": project_code,
            "project_id": project_id,
            "created_at": datetime.now().isoformat(),
            "mcp_namespaces": {
                "session": f"{project_code}_sessions",
                "ultra": f"{project_code}_ultra"
            }
        }

        with open(memory_dir / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)

        return {
            "success": True,
            "message": "记忆空间已创建",
            "memory_dir": str(memory_dir),
            "namespaces": metadata["mcp_namespaces"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/activation_commands/{role}")
async def get_activation_command(role: str):
    """获取指定角色的激活指令"""
    try:
        commands_file = Path(__file__).parent / ".taskflow" / "activation_commands.json"

        if commands_file.exists():
            with open(commands_file, 'r', encoding='utf-8') as f:
                commands = json.load(f)

            if role in commands:
                return {
                    "success": True,
                    "role": role,
                    "command": commands[role]
                }
            else:
                raise HTTPException(status_code=404, detail=f"角色 {role} 不存在")
        else:
            raise HTTPException(status_code=404, detail="激活指令未生成，请先初始化项目")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/activation_commands")
async def get_all_activation_commands():
    """获取所有角色的激活指令"""
    try:
        commands_file = Path(__file__).parent / ".taskflow" / "activation_commands.json"

        if commands_file.exists():
            with open(commands_file, 'r', encoding='utf-8') as f:
                commands = json.load(f)

            return {
                "success": True,
                "commands": commands,
                "roles": list(commands.keys())
            }
        else:
            return {
                "success": False,
                "message": "激活指令未生成，请先初始化项目",
                "commands": {},
                "roles": []
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("\n" + "="*60)
    print("透视塔API服务".center(60))
    print("="*60)
    print(f"\n端口: 8800")
    print(f"数据目录: {DATA_DIR}")

    # 启动前自动扫描更新数据
    print(f"\n🔄 自动扫描项目数据...")
    import subprocess

    script_path = Path(__file__).parent / "scripts" / "auto_update_insight_data.py"
    if script_path.exists():
        try:
            result = subprocess.run(
                ["python3", str(script_path)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # 从输出中提取关键信息
                if "功能数量变化:" in result.stdout:
                    for line in result.stdout.split('\n'):
                        if "功能数量变化:" in line or "已完成任务:" in line or "代码行数:" in line:
                            print(f"   {line.strip()}")
                print(f"   ✅ 数据已更新")
            else:
                print(f"   ⚠️ 扫描失败: {result.stderr[:200]}")
        except Exception as e:
            print(f"   ⚠️ 扫描异常: {str(e)}")
    else:
        print(f"   ⚠️ 扫描脚本不存在: {script_path}")

    print(f"\n🚀 启动API服务...")
    print("="*60 + "\n")

    uvicorn.run(app, host="127.0.0.1", port=8800, log_level="info")

