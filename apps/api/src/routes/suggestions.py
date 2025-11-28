# -*- coding: utf-8 -*-
"""
架构建议API路由
提供架构师建议的查询和采纳接口
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pathlib import Path
import json
from datetime import datetime

router = APIRouter(prefix="/api/suggestions")

# 数据文件路径
DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "apps" / "dashboard" / "automation-data"
SUGGESTIONS_FILE = DATA_DIR / "architecture-suggestions.json"


def load_json_file(file_path: Path) -> Dict:
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加载数据文件失败: {str(e)}")


@router.get("")
async def get_suggestions(
    category: str = None, 
    priority: str = None,
    sort_by: str = "priority"
) -> Dict[str, Any]:
    """
    获取架构建议清单
    
    参数：
    - category: 过滤类别（自动化、功能实现、配置管理等）
    - priority: 过滤优先级 (P0, P1, P2, P3)
    - sort_by: 排序方式 (priority, cost, benefit)
    
    返回：
    - total: 建议总数
    - suggestions: 建议列表
    - stats: 统计信息
    """
    data = load_json_file(SUGGESTIONS_FILE)
    
    suggestions = data.get("suggestions", [])
    
    # 过滤
    if category:
        suggestions = [s for s in suggestions if s.get("category") == category]
    if priority:
        suggestions = [s for s in suggestions if s.get("priority") == priority]
    
    # 排序
    if sort_by == "cost":
        suggestions.sort(key=lambda x: x.get("estimated_hours", 999))
    elif sort_by == "priority":
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        suggestions.sort(key=lambda x: priority_order.get(x.get("priority", "P3"), 999))
    
    # 统计
    category_stats = {}
    priority_stats = {}
    total_hours = 0
    
    for sugg in data.get("suggestions", []):  # 使用原始数据统计
        cat = sugg.get("category", "其他")
        pri = sugg.get("priority", "未知")
        category_stats[cat] = category_stats.get(cat, 0) + 1
        priority_stats[pri] = priority_stats.get(pri, 0) + 1
        total_hours += sugg.get("estimated_hours", 0)
    
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


@router.get("/{suggestion_id}")
async def get_suggestion_detail(suggestion_id: str) -> Dict[str, Any]:
    """
    获取单个建议详情
    
    参数：
    - suggestion_id: 建议ID
    
    返回：建议详细信息
    """
    data = load_json_file(SUGGESTIONS_FILE)
    
    suggestions = data.get("suggestions", [])
    suggestion = next((s for s in suggestions if s.get("id") == suggestion_id), None)
    
    if not suggestion:
        raise HTTPException(status_code=404, detail=f"建议 {suggestion_id} 未找到")
    
    return {
        "success": True,
        "suggestion": suggestion
    }


@router.post("/{suggestion_id}/adopt")
async def adopt_suggestion(suggestion_id: str) -> Dict[str, Any]:
    """
    采纳建议，生成任务（预留接口）
    
    参数：
    - suggestion_id: 建议ID
    
    返回：生成的任务信息
    """
    data = load_json_file(SUGGESTIONS_FILE)
    
    suggestions = data.get("suggestions", [])
    suggestion = next((s for s in suggestions if s.get("id") == suggestion_id), None)
    
    if not suggestion:
        raise HTTPException(status_code=404, detail=f"建议 {suggestion_id} 未找到")
    
    # TODO: 实际实现任务生成逻辑
    task_id = f"TASK-FROM-{suggestion_id}"
    
    return {
        "success": True,
        "message": "建议已采纳，任务已生成（模拟）",
        "task_id": task_id,
        "suggestion_id": suggestion_id,
        "title": suggestion.get("title"),
        "estimated_hours": suggestion.get("estimated_hours")
    }


@router.get("/quick-wins/list")
async def get_quick_wins() -> Dict[str, Any]:
    """
    获取快速收益建议（工时 <= 3小时）
    
    返回：低成本高收益的建议列表
    """
    data = load_json_file(SUGGESTIONS_FILE)
    
    suggestions = data.get("suggestions", [])
    
    # 筛选快速收益建议
    quick_wins = [
        s for s in suggestions 
        if s.get("estimated_hours", 999) <= 3.0
    ]
    
    # 按工时排序
    quick_wins.sort(key=lambda x: x.get("estimated_hours", 999))
    
    return {
        "success": True,
        "total": len(quick_wins),
        "suggestions": quick_wins,
        "total_hours": sum(s.get("estimated_hours", 0) for s in quick_wins)
    }

