# -*- coding: utf-8 -*-
"""
任务看板API路由

提供任务看板同步的API接口
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from pathlib import Path
import sys

# 添加services路径
services_path = Path(__file__).parent.parent.parent.parent.parent / "services"
sys.path.insert(0, str(services_path))

from task_board_auto_sync import TaskBoardAutoSync

router = APIRouter(prefix="/api/task-board", tags=["task-board"])


class SyncResponse(BaseModel):
    """同步响应模型"""
    success: bool
    message: str
    details: Dict[str, Any]


@router.post("/sync", response_model=SyncResponse)
async def trigger_sync():
    """
    手动触发看板同步
    
    Returns:
        同步结果
    """
    try:
        syncer = TaskBoardAutoSync()
        result = syncer.sync()
        
        return SyncResponse(
            success=result['success'],
            message=result['message'],
            details=result['details']
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"同步失败: {str(e)}"
        )


@router.get("/status")
async def get_sync_status():
    """
    获取同步状态
    
    Returns:
        同步状态信息
    """
    try:
        syncer = TaskBoardAutoSync()
        
        # 读取最后一次同步日志
        if syncer.log_file.exists():
            import json
            with open(syncer.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            last_sync = logs[-1] if logs else None
        else:
            last_sync = None
        
        return {
            "success": True,
            "board_path": str(syncer.board_path),
            "board_exists": syncer.board_path.exists(),
            "last_sync": last_sync,
            "backup_dir": str(syncer.backup_dir)
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取状态失败: {str(e)}"
        )


@router.get("/inconsistencies")
async def check_inconsistencies():
    """
    检查看板与数据库的不一致
    
    Returns:
        不一致列表
    """
    try:
        syncer = TaskBoardAutoSync()
        inconsistencies = syncer.detect_inconsistencies()
        
        return {
            "success": True,
            "count": len(inconsistencies),
            "inconsistencies": inconsistencies
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"检查失败: {str(e)}"
        )

