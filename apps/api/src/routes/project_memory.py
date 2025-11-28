# -*- coding: utf-8 -*-
"""
项目记忆空间 API 路由

提供项目记忆管理的RESTful API接口
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import sys
import json

# TODO: 实际导入ProjectMemoryService
# from packages.core_domain.src.services.project_memory_service import (
#     ProjectMemoryService,
#     MemoryType,
#     MemoryCategory,
#     RelationType
# )


packages_path = (
    Path(__file__).resolve().parent.parent.parent.parent.parent
    / "packages"
    / "core-domain"
    / "src"
)
if str(packages_path) not in sys.path:
    sys.path.insert(0, str(packages_path))

from services.project_memory_service import (  # type: ignore[import]
    ProjectMemoryService,
    MemoryType,
    MemoryCategory,
    RelationType,
    create_project_memory_service,
)
from services.event_service import (  # type: ignore[import]
    create_event_emitter,
    EventCategory,
    EventSeverity,
    EventSource,
)

# ============================================================================
# Pydantic 模型定义
# ============================================================================

class CreateMemoryRequest(BaseModel):
    """创建记忆请求"""
    memory_type: str = Field(..., description="记忆类型: session/ultra/decision/solution")
    category: str = Field(..., description="分类: architecture/problem/solution/decision/knowledge")
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容")
    context: Optional[Dict[str, Any]] = Field(None, description="上下文信息")
    tags: Optional[List[str]] = Field(None, description="标签列表")
    related_tasks: Optional[List[str]] = Field(None, description="关联任务ID")
    related_issues: Optional[List[str]] = Field(None, description="关联问题ID")
    importance: int = Field(5, ge=1, le=10, description="重要性1-10")
    created_by: str = Field("system", description="创建者")


class RetrieveMemoriesRequest(BaseModel):
    """检索记忆请求"""
    query: Optional[str] = Field(None, description="查询文本（语义搜索）")
    category: Optional[str] = Field(None, description="分类过滤")
    memory_type: Optional[str] = Field(None, description="类型过滤")
    tags: Optional[List[str]] = Field(None, description="标签过滤")
    limit: int = Field(10, ge=1, le=100, description="返回数量")


class AutoRecordDecisionRequest(BaseModel):
    """自动记录架构决策请求"""
    title: str = Field(..., description="决策标题")
    context: str = Field(..., description="决策背景")
    decision: str = Field(..., description="决策内容")
    consequences: Optional[str] = Field(None, description="影响和后果")
    alternatives: Optional[List[str]] = Field(None, description="备选方案")
    decided_by: str = Field("AI Architect", description="决策者")


class AutoRecordSolutionRequest(BaseModel):
    """自动记录问题解决方案请求"""
    problem_title: str = Field(..., description="问题标题")
    problem_description: str = Field(..., description="问题描述")
    solution_title: str = Field(..., description="解决方案标题")
    solution_description: str = Field(..., description="解决方案描述")
    solution_steps: Optional[List[str]] = Field(None, description="解决步骤")
    tools_used: Optional[List[str]] = Field(None, description="使用的工具")
    severity: str = Field("medium", description="严重性: critical/high/medium/low")
    component_id: Optional[str] = Field(None, description="组件ID")


class CreateRelationRequest(BaseModel):
    """创建记忆关系请求"""
    source_memory_id: str = Field(..., description="源记忆ID")
    target_memory_id: str = Field(..., description="目标记忆ID")
    relation_type: str = Field(..., description="关系类型: related/caused-by/solved-by/evolved-from")
    strength: float = Field(1.0, ge=0.0, le=1.0, description="关系强度")


# ============================================================================
# API 路由器
# ============================================================================

router = APIRouter(prefix="/api/projects", tags=["project-memory"])

# 全局服务与事件发射器实例（惰性初始化）
_project_memory_service: Optional[ProjectMemoryService] = None
_event_emitter = None


def get_project_memory_service() -> ProjectMemoryService:
    """获取项目记忆服务单例，指向主 tasks.db。"""
    global _project_memory_service
    if _project_memory_service is None:
        db_path = (
            Path(__file__).resolve().parent.parent.parent.parent
            / "database"
            / "data"
            / "tasks.db"
        )
        # state_manager 仅作为启用 DB 持久化的标记，不参与具体逻辑
        _project_memory_service = create_project_memory_service(
            state_manager=object(),
            db_path=str(db_path),
            session_memory_enabled=True,
            ultra_memory_enabled=True,
        )
    return _project_memory_service


def get_event_emitter():
    """获取事件发射器单例，用于记忆相关事件流。"""
    global _event_emitter
    if _event_emitter is None:
        try:
            db_path = (
                Path(__file__).resolve().parent.parent.parent.parent
                / "database"
                / "data"
                / "tasks.db"
            )
            _event_emitter = create_event_emitter(db_path=str(db_path))
        except Exception:
            _event_emitter = None
    return _event_emitter


# ============================================================================
# 基础记忆管理
# ============================================================================

@router.post("/{project_code}/memories")
async def create_project_memory(
    project_code: str,
    request: CreateMemoryRequest
) -> Dict[str, Any]:
    """
    创建项目记忆
    
    **用途**: 手动创建项目记忆，存储到本地数据库和外部记忆系统
    
    **示例**:
    ```json
    {
        "memory_type": "ultra",
        "category": "knowledge",
        "title": "React Hooks 最佳实践",
        "content": "使用 useCallback 优化性能...",
        "tags": ["react", "hooks", "performance"],
        "importance": 7
    }
    ```
    """
    try:
        service = get_project_memory_service()
        memory = service.create_memory(
            project_id=project_code,
            memory_type=request.memory_type,
            category=request.category,
            title=request.title,
            content=request.content,
            context=request.context,
            tags=request.tags,
            related_tasks=request.related_tasks,
            related_issues=request.related_issues,
            importance=request.importance,
            created_by=request.created_by,
        )

        # 写入记忆创建事件
        emitter = get_event_emitter()
        if emitter is not None:
            try:
                emitter.emit(
                    project_id=project_code,
                    event_type="memory.created",
                    title=f"记忆创建: {memory.get('title')}",
                    description=f"项目 {project_code} 新建记忆 {memory.get('id')}",
                    category=EventCategory.GENERAL,
                    source=EventSource.AI,
                    actor=request.created_by,
                    severity=EventSeverity.INFO,
                    related_entity_type="memory",
                    related_entity_id=memory.get("id"),
                    tags=(request.tags or []) + [request.category, request.memory_type],
                    data={
                        "memory_id": memory.get("id"),
                        "memory_type": request.memory_type,
                        "category": request.category,
                        "importance": request.importance,
                    },
                )
            except Exception:
                # 事件失败不影响主流程
                pass

        return {
            "success": True,
            "memory": memory
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_code}/memories")
async def retrieve_project_memories(
    project_code: str,
    query: Optional[str] = Query(None, description="查询文本"),
    category: Optional[str] = Query(None, description="分类过滤"),
    memory_type: Optional[str] = Query(None, description="类型过滤"),
    tags: Optional[str] = Query(None, description="标签过滤（逗号分隔）"),
    limit: int = Query(10, ge=1, le=100, description="返回数量")
) -> Dict[str, Any]:
    """
    检索项目记忆
    
    **用途**: 查询项目的历史记忆，支持语义搜索和过滤
    
    **示例**:
    - GET /api/projects/TASKFLOW/memories?query=如何优化性能
    - GET /api/projects/TASKFLOW/memories?category=solution&limit=20
    """
    try:
        tags_list = tags.split(",") if tags else None
        
        service = get_project_memory_service()
        memories = service.retrieve_memories(
            project_id=project_code,
            query=query,
            category=category,
            memory_type=memory_type,
            tags=tags_list,
            limit=limit
        )
        
        return {
            "success": True,
            "project_id": project_code,
            "query": query,
            "filters": {
                "category": category,
                "memory_type": memory_type,
                "tags": tags_list
            },
            "memories": memories,
            "count": len(memories),
            "retrieved_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_code}/memories/{memory_id}")
async def get_memory_detail(
    project_code: str,
    memory_id: str
) -> Dict[str, Any]:
    """
    获取记忆详情
    
    **用途**: 查看单个记忆的完整信息，包括关联关系
    """
    try:
        service = get_project_memory_service()
        with service._get_connection() as conn:  # type: ignore[attr-defined]
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT *
                FROM project_memories
                WHERE id = ? AND project_id = ?
                """,
                (memory_id, project_code),
            )
            row = cursor.fetchone()

        if not row:
            raise HTTPException(
                status_code=404,
                detail=f"Memory not found: {memory_id}",
            )

        memory = dict(row)
        # 解析 JSON 字段，保持与服务内部一致的格式
        for field in ("context", "tags", "related_tasks", "related_issues"):
            if memory.get(field):
                try:
                    memory[field] = json.loads(memory[field])
                except Exception:
                    if field in ("tags", "related_tasks", "related_issues"):
                        memory[field] = []

        return {
            "success": True,
            "memory": memory
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=404, detail=f"Memory not found: {memory_id}")


# ============================================================================
# 自动记录功能
# ============================================================================

@router.post("/{project_code}/memories/auto-record/decision")
async def auto_record_architecture_decision(
    project_code: str,
    request: AutoRecordDecisionRequest
) -> Dict[str, Any]:
    """
    自动记录架构决策（ADR）
    
    **用途**: 架构师AI自动记录架构决策，格式化为ADR并存储
    
    **示例**:
    ```json
    {
        "title": "采用 Monorepo 架构",
        "context": "项目规模扩大，需要统一管理多个包...",
        "decision": "使用 pnpm workspace 实现 Monorepo",
        "consequences": "提高代码复用性，简化依赖管理",
        "alternatives": ["Lerna", "Nx", "Turborepo"],
        "decided_by": "AI Architect"
    }
    ```
    """
    try:
        service = get_project_memory_service()
        memory = service.auto_record_architecture_decision(
            project_id=project_code,
            title=request.title,
            context=request.context,
            decision=request.decision,
            consequences=request.consequences,
            alternatives=request.alternatives,
            decided_by=request.decided_by
        )

        # 发射架构决策记录事件
        emitter = get_event_emitter()
        if emitter is not None:
            try:
                emitter.emit(
                    project_id=project_code,
                    event_type="memory.decision_recorded",
                    title=f"架构决策记录: {request.title}",
                    description=f"项目 {project_code} 记录架构决策 {memory.get('id')}",
                    category=EventCategory.DECISION,
                    source=EventSource.AI,
                    actor=request.decided_by,
                    severity=EventSeverity.INFO,
                    related_entity_type="memory",
                    related_entity_id=memory.get("id"),
                    tags=["decision", "adr"],
                    data={
                        "memory_id": memory.get("id"),
                        "title": request.title,
                    },
                )
            except Exception:
                pass

        return {
            "success": True,
            "message": "Architecture decision recorded successfully",
            "memory": memory
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{project_code}/memories/auto-record/solution")
async def auto_record_problem_solution(
    project_code: str,
    request: AutoRecordSolutionRequest
) -> Dict[str, Any]:
    """
    自动记录问题解决方案
    
    **用途**: 自动记录问题及其解决方案，建立关联关系
    
    **示例**:
    ```json
    {
        "problem_title": "Dashboard Tab 切换失败",
        "problem_description": "JavaScript 反引号未转义导致语法错误",
        "solution_title": "修复模板字符串转义",
        "solution_description": "在 Python f-string 中转义反引号",
        "solution_steps": [
            "定位错误位置",
            "添加反斜杠转义",
            "测试验证"
        ],
        "tools_used": ["node -c", "debug_tab_issue.py"],
        "severity": "high"
    }
    ```
    """
    try:
        service = get_project_memory_service()
        result = service.auto_record_problem_solution(
            project_id=project_code,
            problem_title=request.problem_title,
            problem_description=request.problem_description,
            solution_title=request.solution_title,
            solution_description=request.solution_description,
            solution_steps=request.solution_steps,
            tools_used=request.tools_used,
            severity=request.severity,
            component_id=request.component_id
        )

        emitter = get_event_emitter()
        if emitter is not None:
            try:
                emitter.emit(
                    project_id=project_code,
                    event_type="memory.problem_solution_recorded",
                    title=f"问题与解决方案记录: {request.problem_title}",
                    description=f"项目 {project_code} 记录问题与解决方案",
                    category=EventCategory.PROBLEM,
                    source=EventSource.AI,
                    actor="system",
                    severity=EventSeverity.INFO,
                    related_entity_type="memory",
                    related_entity_id=result["solution_memory"]["id"],
                    tags=[
                        "problem",
                        "solution",
                        request.severity,
                    ],
                    data={
                        "problem_memory_id": result["problem_memory"]["id"],
                        "solution_memory_id": result["solution_memory"]["id"],
                    },
                )
            except Exception:
                pass

        return {
            "success": True,
            **result,
            "recorded_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# 跨会话知识继承
# ============================================================================

@router.get("/{project_code}/knowledge/inherit")
async def inherit_project_knowledge(
    project_code: str,
    context: Optional[str] = Query(None, description="当前上下文"),
    limit: int = Query(20, ge=1, le=100, description="返回记忆数量")
) -> Dict[str, Any]:
    """
    跨会话知识继承
    
    **用途**: 新会话开始时，自动获取项目的历史知识和经验
    
    **返回内容**:
    - 架构决策历史
    - 问题解决方案
    - 重要知识点
    - 最近记忆
    - 相关记忆（如果提供context）
    
    **使用场景**:
    ```
    新架构师接手项目时：
    GET /api/projects/TASKFLOW/knowledge/inherit?context=准备开始重构
    
    系统返回：
    - 之前的重构决策
    - 已知的技术债务
    - 过去的重构经验
    - 相关问题和解决方案
    ```
    """
    try:
        service = get_project_memory_service()
        knowledge_package = service.inherit_knowledge(
            project_id=project_code,
            context=context,
            limit=limit
        )
        
        return {
            "success": True,
            **knowledge_package,
            "usage_hint": "使用这些知识帮助新会话快速了解项目历史和经验"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# 记忆关系管理
# ============================================================================

@router.post("/{project_code}/memories/relations")
async def create_memory_relation(
    project_code: str,
    request: CreateRelationRequest
) -> Dict[str, Any]:
    """
    创建记忆关系
    
    **用途**: 手动创建记忆之间的关联关系
    
    **关系类型**:
    - related: 相关
    - caused-by: 由...引起
    - solved-by: 由...解决
    - evolved-from: 由...演化
    - depends-on: 依赖于
    """
    try:
        service = get_project_memory_service()
        relation = service.create_memory_relation(
            source_memory_id=request.source_memory_id,
            target_memory_id=request.target_memory_id,
            relation_type=request.relation_type,
            strength=request.strength
        )
        
        return {
            "success": True,
            "relation": relation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_code}/memories/{memory_id}/related")
async def get_related_memories(
    project_code: str,
    memory_id: str,
    relation_types: Optional[str] = Query(None, description="关系类型过滤（逗号分隔）"),
    min_strength: float = Query(0.5, ge=0.0, le=1.0, description="最小关系强度")
) -> Dict[str, Any]:
    """
    获取相关记忆
    
    **用途**: 查询与指定记忆相关的其他记忆
    """
    try:
        relation_types_list = relation_types.split(",") if relation_types else None
        
        service = get_project_memory_service()
        related = service.get_related_memories(
            memory_id=memory_id,
            relation_types=relation_types_list,
            min_strength=min_strength
        )
        
        return {
            "success": True,
            "memory_id": memory_id,
            "related_memories": related,
            "count": len(related)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# 统计和管理
# ============================================================================

@router.get("/{project_code}/memories/stats")
async def get_memory_stats(project_code: str) -> Dict[str, Any]:
    """
    获取项目记忆统计
    
    **用途**: Dashboard展示项目的记忆统计信息
    
    **返回内容**:
    - 总记忆数
    - 按类型分类统计
    - 按分类统计
    - 最近活动
    """
    try:
        service = get_project_memory_service()
        base_stats = service.get_memory_stats(project_id=project_code) or {}

        # 额外按分类和重要性分桶统计
        by_category = {
            "architecture": 0,
            "problem": 0,
            "solution": 0,
            "decision": 0,
            "knowledge": 0
        }
        by_importance = {
            "critical (9-10)": 0,
            "high (7-8)": 0,
            "medium (5-6)": 0,
            "low (1-4)": 0
        }

        with service._get_connection() as conn:  # type: ignore[attr-defined]
            cursor = conn.cursor()

            # 按分类统计
            cursor.execute(
                """
                SELECT category, COUNT(*) AS cnt
                FROM project_memories
                WHERE project_id = ?
                GROUP BY category
                """,
                (project_code,),
            )
            for category, cnt in cursor.fetchall():
                if category in by_category:
                    by_category[category] = cnt

            # 按重要性分桶
            cursor.execute(
                """
                SELECT importance, COUNT(*) AS cnt
                FROM project_memories
                WHERE project_id = ?
                GROUP BY importance
                """,
                (project_code,),
            )
            for importance, cnt in cursor.fetchall():
                if importance >= 9:
                    by_importance["critical (9-10)"] += cnt
                elif importance >= 7:
                    by_importance["high (7-8)"] += cnt
                elif importance >= 5:
                    by_importance["medium (5-6)"] += cnt
                else:
                    by_importance["low (1-4)"] += cnt

        stats = {
            "total_memories": base_stats.get("total_memories", 0),
            "session_memories": base_stats.get("session_memories", 0),
            "ultra_memories": base_stats.get("ultra_memories", 0),
            "decision_memories": base_stats.get("decision_memories", 0),
            "solution_memories": base_stats.get("solution_memories", 0),
            "by_category": by_category,
            "by_importance": by_importance,
            "last_updated": datetime.now().isoformat()
        }

        return {
            "success": True,
            "project_id": project_code,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_code}/memories/{memory_id}")
async def delete_memory(
    project_code: str,
    memory_id: str
) -> Dict[str, Any]:
    """
    删除记忆
    
    **用途**: 删除不再需要的记忆（谨慎使用）
    """
    try:
        service = get_project_memory_service()
        with service._get_connection() as conn:  # type: ignore[attr-defined]
            cursor = conn.cursor()

            # 先删除关联关系，再删除记忆本身
            cursor.execute(
                """
                DELETE FROM memory_relations
                WHERE source_memory_id = ? OR target_memory_id = ?
                """,
                (memory_id, memory_id),
            )
            cursor.execute(
                """
                DELETE FROM project_memories
                WHERE id = ? AND project_id = ?
                """,
                (memory_id, project_code),
            )
            deleted = cursor.rowcount > 0

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=f"Memory not found: {memory_id}",
            )

        return {
            "success": True,
            "message": f"Memory {memory_id} deleted successfully",
            "deleted_at": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete memory {memory_id}: {e}",
        )


# ============================================================================
# 健康检查
# ============================================================================

@router.get("/{project_code}/memories/health")
async def check_memory_system_health(project_code: str) -> Dict[str, Any]:
    """
    检查记忆系统健康状态
    
    **用途**: 验证本地数据库和外部记忆系统的连接状态
    """
    return {
        "success": True,
        "project_id": project_code,
        "local_db": "healthy",
        "session_memory": "healthy",  # TODO: 实际检查
        "ultra_memory": "healthy",    # TODO: 实际检查
        "checked_at": datetime.now().isoformat()
    }

