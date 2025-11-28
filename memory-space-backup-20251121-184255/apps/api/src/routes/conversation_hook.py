# -*- coding: utf-8 -*-
"""
对话Hook - 自动记录到记忆空间

功能：
1. 拦截每轮对话（用户提问 + AI回答）
2. 自动判断是否需要记录
3. 提取关键信息并存储到记忆空间
4. 触发事件流通知
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import sys

# 导入ProjectMemoryService
packages_path = (
    Path(__file__).resolve().parent.parent.parent.parent.parent
    / "packages"
    / "core-domain"
    / "src"
)
if str(packages_path) not in sys.path:
    sys.path.insert(0, str(packages_path))

from services.project_memory_service import (
    create_project_memory_service,
)
from services.event_service import (
    create_event_emitter,
    EventCategory,
    EventSeverity,
    EventSource,
)


router = APIRouter(prefix="/api/conversations", tags=["conversation-hook"])

# 全局服务实例
_memory_service = None
_event_emitter = None


def get_memory_service():
    """获取记忆服务单例"""
    global _memory_service
    if _memory_service is None:
        db_path = (
            Path(__file__).resolve().parent.parent.parent.parent
            / "database"
            / "data"
            / "tasks.db"
        )
        _memory_service = create_project_memory_service(
            state_manager=object(),
            db_path=str(db_path),
            session_memory_enabled=True,
            ultra_memory_enabled=True,
        )
    return _memory_service


def get_event_emitter():
    """获取事件发射器单例"""
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
# 请求模型
# ============================================================================

class ConversationTurn(BaseModel):
    """对话轮次"""
    user_input: str = Field(..., description="用户输入")
    ai_response: str = Field(..., description="AI回复")
    conversation_id: Optional[str] = Field(None, description="会话ID")
    actor: str = Field("user", description="用户标识")
    ai_role: str = Field("assistant", description="AI角色: architect/fullstack/devops/assistant")


# ============================================================================
# API端点
# ============================================================================

@router.post("/hook/auto-record")
async def auto_record_conversation_hook(
    project_code: str,
    turn: ConversationTurn
) -> Dict[str, Any]:
    """
    对话Hook - 自动记录到记忆空间
    
    **用途**: 在每轮对话完成后调用，自动判断并记录重要内容
    
    **工作流程**:
    1. 分析对话内容
    2. 提取关键词
    3. 判断是否需要记录
    4. 创建记忆条目
    5. 触发事件流
    
    **示例**:
    ```json
    {
        "user_input": "如何优化Dashboard的性能？",
        "ai_response": "建议采用以下方案：1. 使用虚拟滚动...",
        "conversation_id": "conv-001",
        "ai_role": "fullstack"
    }
    ```
    
    **返回**:
    ```json
    {
        "success": true,
        "should_record": true,
        "memories_created": [
            {
                "id": "MEM-xxx",
                "title": "[自动记录] 如何优化Dashboard的性能？",
                "importance": 7
            }
        ],
        "event_emitted": true
    }
    ```
    """
    try:
        service = get_memory_service()
        
        # 调用自动记录方法
        result = service.auto_record_conversation(
            project_id=project_code,
            user_input=turn.user_input,
            ai_response=turn.ai_response,
            conversation_id=turn.conversation_id,
            actor=turn.actor,
            ai_role=turn.ai_role
        )
        
        # 如果记录成功，触发事件
        event_emitted = False
        if result.get("should_record") and result.get("memories_created"):
            emitter = get_event_emitter()
            if emitter is not None:
                try:
                    for memory in result["memories_created"]:
                        emitter.emit(
                            project_id=project_code,
                            event_type="memory.auto_created",
                            title=f"自动记录: {memory.get('title', '')[:30]}",
                            description=f"对话中自动提取并记录了{result.get('memory_type')}",
                            category=EventCategory.GENERAL,
                            source=EventSource.AI,
                            actor=turn.ai_role,
                            severity=EventSeverity.INFO,
                            related_entity_type="memory",
                            related_entity_id=memory.get("id"),
                            tags=result.get("keywords", []) + ["auto-note"],
                            data={
                                "conversation_id": turn.conversation_id,
                                "importance": memory.get("importance"),
                                "memory_type": result.get("memory_type")
                            }
                        )
                    event_emitted = True
                except Exception as e:
                    print(f"事件发射失败: {e}")
        
        return {
            "success": True,
            "project_id": project_code,
            **result,
            "event_emitted": event_emitted,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"自动记录失败: {str(e)}"
        )


@router.post("/hook/batch-auto-record")
async def batch_auto_record(
    project_code: str,
    turns: list[ConversationTurn]
) -> Dict[str, Any]:
    """
    批量自动记录多轮对话
    
    **用途**: 会话结束时批量处理多轮对话
    """
    try:
        results = []
        total_recorded = 0
        
        service = get_memory_service()
        
        for turn in turns:
            result = service.auto_record_conversation(
                project_id=project_code,
                user_input=turn.user_input,
                ai_response=turn.ai_response,
                conversation_id=turn.conversation_id,
                actor=turn.actor,
                ai_role=turn.ai_role
            )
            
            if result.get("should_record"):
                total_recorded += 1
            
            results.append({
                "turn": turn.conversation_id,
                "recorded": result.get("should_record", False),
                "memories_count": len(result.get("memories_created", []))
            })
        
        return {
            "success": True,
            "project_id": project_code,
            "total_turns": len(turns),
            "total_recorded": total_recorded,
            "results": results,
            "processed_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"批量记录失败: {str(e)}"
        )


@router.get("/hook/stats")
async def get_auto_record_stats(project_code: str) -> Dict[str, Any]:
    """
    获取自动记录统计
    
    **返回**:
    - 自动记录总数
    - 按类型统计
    - 最近自动记录
    """
    try:
        service = get_memory_service()
        
        with service._get_connection() as conn:
            cursor = conn.cursor()
            
            # 查询自动记录的记忆
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN category = 'decision' THEN 1 ELSE 0 END) as decisions,
                    SUM(CASE WHEN category = 'solution' THEN 1 ELSE 0 END) as solutions,
                    SUM(CASE WHEN category = 'knowledge' THEN 1 ELSE 0 END) as knowledge
                FROM project_memories
                WHERE project_id = ? 
                AND created_by LIKE 'auto:%'
            """, (project_code,))
            
            row = cursor.fetchone()
            stats = dict(row) if row else {}
            
            # 最近自动记录
            cursor.execute("""
                SELECT id, title, category, importance, created_at
                FROM project_memories
                WHERE project_id = ? 
                AND created_by LIKE 'auto:%'
                ORDER BY created_at DESC
                LIMIT 10
            """, (project_code,))
            
            recent = [dict(r) for r in cursor.fetchall()]
        
        return {
            "success": True,
            "project_id": project_code,
            "auto_record_stats": stats,
            "recent_auto_records": recent,
            "retrieved_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取统计失败: {str(e)}"
        )

