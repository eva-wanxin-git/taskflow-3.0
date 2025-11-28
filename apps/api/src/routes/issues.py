# -*- coding: utf-8 -*-
"""
问题清单API路由
提供项目问题的查询和管理接口
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pathlib import Path
import json
from datetime import datetime

router = APIRouter(prefix="/api/issues")

# 数据文件路径
DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "apps" / "dashboard" / "automation-data"
ISSUES_FILE = DATA_DIR / "project-issues.json"


def load_json_file(file_path: Path) -> Dict:
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加载数据文件失败: {str(e)}")


@router.get("")
async def get_issues(priority: str = None, severity: str = None) -> Dict[str, Any]:
    """
    获取问题清单
    
    参数：
    - priority: 过滤优先级 (P0, P1, P2)
    - severity: 过滤严重性 (Critical, High, Medium, Low)
    
    返回：
    - total: 问题总数
    - issues: 问题列表
    - stats: 统计信息（按优先级和严重性）
    """
    data = load_json_file(ISSUES_FILE)
    
    issues = data.get("issues", [])
    
    # 过滤
    if priority:
        issues = [i for i in issues if i.get("priority") == priority]
    if severity:
        issues = [i for i in issues if i.get("severity") == severity]
    
    # 统计
    priority_stats = {}
    severity_stats = {}
    for issue in data.get("issues", []):  # 使用原始数据统计
        p = issue.get("priority", "未知")
        s = issue.get("severity", "未知")
        priority_stats[p] = priority_stats.get(p, 0) + 1
        severity_stats[s] = severity_stats.get(s, 0) + 1
    
    # 计算总工时
    total_hours = sum(i.get("estimated_hours", 0) for i in data.get("issues", []))
    
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


@router.get("/{issue_id}")
async def get_issue_detail(issue_id: str) -> Dict[str, Any]:
    """
    获取单个问题详情
    
    参数：
    - issue_id: 问题ID
    
    返回：问题详细信息
    """
    data = load_json_file(ISSUES_FILE)
    
    issues = data.get("issues", [])
    issue = next((i for i in issues if i.get("id") == issue_id), None)
    
    if not issue:
        raise HTTPException(status_code=404, detail=f"问题 {issue_id} 未找到")
    
    return {
        "success": True,
        "issue": issue
    }


@router.post("/{issue_id}/generate-task")
async def generate_task_from_issue(issue_id: str) -> Dict[str, Any]:
    """
    将问题转换为任务（预留接口）
    
    参数：
    - issue_id: 问题ID
    
    返回：生成的任务信息
    """
    data = load_json_file(ISSUES_FILE)
    
    issues = data.get("issues", [])
    issue = next((i for i in issues if i.get("id") == issue_id), None)
    
    if not issue:
        raise HTTPException(status_code=404, detail=f"问题 {issue_id} 未找到")
    
    # TODO: 实际实现任务生成逻辑
    task_id = f"TASK-FROM-{issue_id}"
    
    return {
        "success": True,
        "message": "任务生成成功（模拟）",
        "task_id": task_id,
        "issue_id": issue_id,
        "title": issue.get("title"),
        "estimated_hours": issue.get("estimated_hours")
    }

