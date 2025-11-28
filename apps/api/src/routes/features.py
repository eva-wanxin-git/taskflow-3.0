# -*- coding: utf-8 -*-
"""
功能清单API路由
提供已实现功能和部分实现功能的查询接口
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pathlib import Path
import json
from datetime import datetime

router = APIRouter(prefix="/api/features")

# 数据文件路径
DATA_DIR = Path(__file__).parent.parent.parent.parent.parent / "apps" / "dashboard" / "automation-data"
COMPLETE_FEATURES_FILE = DATA_DIR / "v17-complete-features.json"
PARTIAL_FEATURES_FILE = DATA_DIR / "partial-features.json"


def load_json_file(file_path: Path) -> Dict:
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加载数据文件失败: {str(e)}")


@router.get("/implemented")
async def get_implemented_features() -> Dict[str, Any]:
    """
    获取已实现功能列表
    
    返回：
    - total: 功能总数
    - features: 功能列表
    - categories: 按类型分组的统计
    """
    data = load_json_file(COMPLETE_FEATURES_FILE)
    
    features = data.get("implemented", [])
    
    # 按类型分组统计
    categories = {}
    for feature in features:
        category = feature.get("type", "其他")
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    return {
        "success": True,
        "total": len(features),
        "features": features,
        "categories": categories,
        "updated_at": datetime.now().isoformat()
    }


@router.get("/partial")
async def get_partial_features() -> Dict[str, Any]:
    """
    获取部分实现功能列表
    
    返回：
    - total: 功能总数
    - features: 功能列表（包含进度、已完成部分、缺失部分）
    - avg_progress: 平均进度
    """
    data = load_json_file(PARTIAL_FEATURES_FILE)
    
    features = data.get("partial_features", [])
    
    # 计算平均进度
    if features:
        avg_progress = sum(f.get("progress", 0) for f in features) / len(features)
    else:
        avg_progress = 0
    
    return {
        "success": True,
        "total": len(features),
        "features": features,
        "avg_progress": round(avg_progress, 1),
        "updated_at": data.get("updated_at", datetime.now().isoformat())
    }


@router.get("/summary")
async def get_features_summary() -> Dict[str, Any]:
    """
    获取功能实现概况
    
    返回：
    - implemented_count: 已实现功能数
    - partial_count: 部分实现功能数
    - completion_rate: 完成率
    """
    complete_data = load_json_file(COMPLETE_FEATURES_FILE)
    partial_data = load_json_file(PARTIAL_FEATURES_FILE)
    
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

