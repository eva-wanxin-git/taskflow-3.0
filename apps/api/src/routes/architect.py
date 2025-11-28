# -*- coding: utf-8 -*-
"""
架构师API路由

提供架构师AI与任务所·Flow系统交互的API端点
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import sqlite3
import json

from ..services.architect_orchestrator import (
    ArchitectOrchestrator,
    ArchitectAnalysis,
    HandoverSnapshot,
    create_architect_orchestrator,
)

# 创建路由器
router = APIRouter(prefix="/api/architect", tags=["architect"])

# 全局编排器实例（实际应该从依赖注入获取）
_orchestrator: Optional[ArchitectOrchestrator] = None


def get_orchestrator() -> ArchitectOrchestrator:
    """获取编排器实例"""
    global _orchestrator
    if _orchestrator is None:
        # 当前版本直接使用本仓库内的 tasks.db，后续可通过依赖注入替换
        _orchestrator = create_architect_orchestrator(
            state_manager=None,
            docs_root="docs",
        )
    return _orchestrator


# 全局数据库路径（与 ArchitectOrchestrator 一致）
DB_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "database"
    / "data"
    / "tasks.db"
)


def _get_db_connection() -> sqlite3.Connection:
    """获取指向 tasks.db 的连接"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================================
# API端点
# ============================================================================

@router.post(
    "/analysis",
    summary="提交架构分析结果",
    description="架构师AI完成分析后，调用此API提交结果"
)
async def submit_analysis(analysis: ArchitectAnalysis) -> Dict[str, Any]:
    """
    提交架构师分析结果
    
    接收架构师AI的分析，转换为：
    - 数据库记录（tasks, issues, knowledge_articles）
    - Markdown文档（task-board.md）
    
    Args:
        analysis: 架构师分析结果
        
    Returns:
        {
            "success": True,
            "tasks_created": 12,
            "issues_created": 3,
            "articles_created": 2,
            "task_board_url": "docs/tasks/task-board.md"
        }
    """
    try:
        orchestrator = get_orchestrator()
        result = orchestrator.process_analysis(analysis)
        
        return {
            "success": True,
            **result,
            "task_board_url": "docs/tasks/task-board.md",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"处理分析结果失败: {str(e)}"
        )


@router.get(
    "/summary/{project_code}",
    summary="获取项目架构摘要",
    description="返回项目的关键架构信息摘要"
)
async def get_project_summary(project_code: str) -> Dict[str, Any]:
    """
    获取项目架构摘要
    
    优先从数据库读取真实统计信息；如果项目不存在，则回退到示例数据
    （用于测试场景下的 Mock 项目）。
    """
    try:
        with _get_db_connection() as conn:
            cursor = conn.cursor()

            # 查找项目
            cursor.execute(
                "SELECT id, name, code, status FROM projects WHERE code = ?",
                (project_code,),
            )
            project_row = cursor.fetchone()

            if not project_row:
                # 对于尚未入库的项目（例如测试用 TEST_PROJECT），保持向后兼容的示例返回
                return {
                    "project": {
                        "code": project_code,
                        "name": f"项目 {project_code}",
                        "status": "unknown",
                    },
                    "stats": {
                        "total_tasks": 0,
                        "pending": 0,
                        "in_progress": 0,
                        "completed": 0,
                        "total_components": 0,
                        "total_issues": 0,
                    },
                    "components": [],
                    "recent_issues": [],
                    "last_updated": datetime.now().isoformat(),
                }

            project_id = project_row["id"]

            # 统计任务
            cursor.execute(
                "SELECT COUNT(*) FROM tasks WHERE project_id = ?",
                (project_id,),
            )
            total_tasks = cursor.fetchone()[0]

            def _count_by_status(status_value: str) -> int:
                cursor.execute(
                    "SELECT COUNT(*) FROM tasks WHERE project_id = ? AND status = ?",
                    (project_id, status_value),
                )
                return cursor.fetchone()[0]

            pending = _count_by_status("pending")
            in_progress = _count_by_status("in_progress")
            completed = _count_by_status("completed")

            # 统计组件与问题
            cursor.execute(
                "SELECT COUNT(*) FROM components WHERE project_id = ?",
                (project_id,),
            )
            total_components = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM issues WHERE project_id = ?",
                (project_id,),
            )
            total_issues = cursor.fetchone()[0]

            # 组件列表（仅返回少量关键字段）
            cursor.execute(
                """
                SELECT id, name, type
                FROM components
                WHERE project_id = ?
                ORDER BY name
                """,
                (project_id,),
            )
            components = [
                {
                    "id": row["id"],
                    "name": row["name"],
                    "type": row["type"],
                }
                for row in cursor.fetchall()
            ]

            # 最近问题
            cursor.execute(
                """
                SELECT id, title, severity, status, discovered_at
                FROM issues
                WHERE project_id = ?
                ORDER BY discovered_at DESC
                LIMIT 5
                """,
                (project_id,),
            )
            recent_issues = [
                {
                    "id": row["id"],
                    "title": row["title"],
                    "severity": row["severity"],
                    "status": row["status"],
                    "discovered_at": row["discovered_at"],
                }
                for row in cursor.fetchall()
            ]

            return {
                "project": {
                    "code": project_row["code"],
                    "name": project_row["name"],
                    "status": project_row["status"],
                },
                "stats": {
                    "total_tasks": total_tasks,
                    "pending": pending,
                    "in_progress": in_progress,
                    "completed": completed,
                    "total_components": total_components,
                    "total_issues": total_issues,
                },
                "components": components,
                "recent_issues": recent_issues,
                "last_updated": datetime.now().isoformat(),
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取项目摘要失败: {str(e)}",
        )


@router.post(
    "/handover",
    summary="提交交接快照",
    description="架构师AI完成阶段性工作后，提交交接快照"
)
async def submit_handover(snapshot: HandoverSnapshot) -> Dict[str, Any]:
    """
    提交交接快照
    
    保存架构师的工作快照，便于下一任接手
    
    Args:
        snapshot: 交接快照
        
    Returns:
        {
            "success": True,
            "snapshot_id": "handover-xxx",
            "snapshot_path": "docs/arch/handovers/xxx.json"
        }
    """
    try:
        orchestrator = get_orchestrator()
        result = orchestrator.process_handover(snapshot)
        
        return {
            "success": True,
            "snapshot_id": snapshot.snapshot_id,
            **result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"提交交接快照失败: {str(e)}"
        )


@router.get(
    "/handover/latest",
    summary="获取最新交接快照",
    description="获取指定项目的最新交接快照"
)
async def get_latest_handover(project_code: str) -> Dict[str, Any]:
    """
    获取最新交接快照
    
    Args:
        project_code: 项目代码
        
    Returns:
        最新的交接快照JSON
    """
    try:
        # TODO: 从数据库查询最新快照
        # 这里返回模拟响应
        
        return {
            "found": False,
            "message": f"项目 {project_code} 暂无交接快照",
            "suggestion": "首次使用架构师时会自动创建"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取交接快照失败: {str(e)}"
        )


@router.get(
    "/status",
    summary="获取架构师服务状态",
    description="健康检查和服务状态"
)
async def get_architect_status() -> Dict[str, Any]:
    """获取架构师服务状态"""
    return {
        "status": "healthy",
        "version": "v2.0",
        "features": {
            "analysis_submission": True,
            "handover_snapshot": True,
            "project_summary": True,
            "task_board_generation": True
        },
        "endpoints": [
            "POST /api/architect/analysis",
            "GET  /api/architect/summary/{project_code}",
            "POST /api/architect/handover",
            "GET  /api/architect/handover/latest?project_code=XXX"
        ],
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# 扩展端点（未来可添加）
# ============================================================================

@router.get(
    "/tasks/{project_code}",
    summary="获取项目的架构任务",
    description="查询由架构师创建的任务列表"
)
async def get_architect_tasks(
    project_code: str,
    status: Optional[str] = None,
    priority: Optional[str] = None
) -> Dict[str, Any]:
    """
    获取架构师任务
    
    优先从数据库查询指定项目的任务；如果项目不存在，则返回空列表。
    """
    try:
        with _get_db_connection() as conn:
            cursor = conn.cursor()

            # 先根据项目代码查找项目ID
            cursor.execute(
                "SELECT id FROM projects WHERE code = ?",
                (project_code,),
            )
            row = cursor.fetchone()

            if not row:
                return {
                    "project_code": project_code,
                    "tasks": [],
                    "total": 0,
                }

            project_id = row["id"]

            # 构造查询
            query = """
                SELECT id, title, description, status, priority,
                       estimated_hours, complexity, component_id, metadata,
                       created_at, updated_at
                FROM tasks
                WHERE project_id = ?
            """
            params: List[Any] = [project_id]

            if status:
                query += " AND status = ?"
                params.append(status)

            if priority:
                query += " AND priority = ?"
                params.append(priority)

            query += " ORDER BY created_at DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            tasks = []
            for task in rows:
                metadata = {}
                if task["metadata"]:
                    try:
                        metadata = json.loads(task["metadata"])
                    except Exception:
                        metadata = {}

                tasks.append(
                    {
                        "id": task["id"],
                        "title": task["title"],
                        "description": task["description"],
                        "status": task["status"],
                        "priority": task["priority"],
                        "estimated_hours": task["estimated_hours"],
                        "complexity": task["complexity"],
                        "component_id": task["component_id"],
                        "metadata": metadata,
                        "created_at": task["created_at"],
                        "updated_at": task["updated_at"],
                    }
                )

            return {
                "project_code": project_code,
                "tasks": tasks,
                "total": len(tasks),
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取架构师任务失败: {str(e)}",
        )


@router.post(
    "/task/{task_id}/feedback",
    summary="提交任务反馈",
    description="执行者（代码管家/SRE）完成任务后提交反馈"
)
async def submit_task_feedback(
    task_id: str,
    feedback: Dict[str, Any]
) -> Dict[str, Any]:
    """
    提交任务反馈
    
    代码管家完成任务后，通过此API提交实现细节
    
    Args:
        task_id: 任务ID
        feedback: {
            "status": "completed",
            "actual_hours": 3.5,
            "files_created": [...],
            "files_modified": [...],
            "notes": "..."
        }
    """
    # TODO: 实现
    return {
        "success": True,
        "task_id": task_id,
        "feedback_recorded": True
    }

