#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动更新透视塔数据
从数据库实时统计，而不是硬编码
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime

# 路径配置
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "database" / "data" / "tasks.db"
DATA_DIR = PROJECT_ROOT / "apps" / "dashboard" / "automation-data"
OUTPUT_FILE = DATA_DIR / "v17-complete-features.json"

def get_db_connection():
    """获取数据库连接"""
    return sqlite3.connect(str(DB_PATH))

def scan_completed_tasks():
    """扫描已完成的任务"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 查询已完成的任务（不包含tags列）
    cursor.execute("""
        SELECT 
            id, title, description, status, priority,
            estimated_hours, created_at, completed_at,
            assigned_to, metadata
        FROM tasks
        WHERE status = 'completed'
        ORDER BY completed_at DESC
    """)
    
    completed_tasks = []
    for row in cursor.fetchall():
        completed_tasks.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "status": row[3],
            "priority": row[4],
            "estimated_hours": row[5],
            "created_at": row[6],
            "completed_at": row[7],
            "assigned_to": row[8],
            "metadata": row[9]
        })
    
    conn.close()
    return completed_tasks

def scan_project_files():
    """扫描项目文件统计"""
    # 统计Python文件
    py_files = list(PROJECT_ROOT.rglob("*.py"))
    # 统计HTML文件
    html_files = list(PROJECT_ROOT.rglob("*.html"))
    # 统计JSON文件
    json_files = list(PROJECT_ROOT.rglob("*.json"))
    
    total_lines = 0
    for py_file in py_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                total_lines += len(f.readlines())
        except:
            pass
    
    return {
        "total_files": len(py_files) + len(html_files) + len(json_files),
        "py_files": len(py_files),
        "html_files": len(html_files),
        "json_files": len(json_files),
        "total_lines": total_lines
    }

def load_existing_features():
    """加载现有功能清单作为基础"""
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"implemented": []}

def update_features_data():
    """更新功能数据"""
    print("\n" + "="*70)
    print("自动更新透视塔数据")
    print("="*70)
    print()
    
    # 1. 加载现有功能清单
    print("📊 步骤1: 加载现有功能清单...")
    existing_data = load_existing_features()
    existing_count = len(existing_data.get("implemented", []))
    print(f"   现有记录: {existing_count}个功能")
    
    # 2. 扫描已完成任务
    print("\n📋 步骤2: 扫描数据库已完成任务...")
    completed_tasks = scan_completed_tasks()
    print(f"   已完成任务: {len(completed_tasks)}个")
    
    # 3. 扫描项目文件
    print("\n📁 步骤3: 扫描项目文件...")
    file_stats = scan_project_files()
    print(f"   总文件数: {file_stats['total_files']}")
    print(f"   Python文件: {file_stats['py_files']}")
    print(f"   HTML文件: {file_stats['html_files']}")
    print(f"   代码行数: {file_stats['total_lines']}")
    
    # 4. 合并新完成的任务到功能清单
    print("\n🔄 步骤4: 更新功能清单...")
    implemented = existing_data.get("implemented", [])
    
    # 将新完成的任务添加为新功能
    existing_ids = {f.get("id") for f in implemented}
    new_features = 0
    
    for task in completed_tasks:
        task_id = task["id"]
        if task_id not in existing_ids:
            # 根据任务ID判断类型
            task_type = "任务完成"
            if "REQ-" in task_id:
                task_type = "需求实现"
            elif "INTEGRATE-" in task_id:
                task_type = "集成功能"
            elif "TASK-" in task_id:
                task_type = "任务功能"
            
            implemented.append({
                "id": task_id,
                "name": task["title"],
                "type": task_type,
                "file": task.get("assigned_to", "unknown"),
                "version": "v1.9",
                "completion": 1.0,
                "completed_at": task.get("completed_at", ""),
                "priority": task.get("priority", "P2")
            })
            new_features += 1
    
    print(f"   新增功能: {new_features}个")
    print(f"   总计功能: {len(implemented)}个")
    
    # 5. 保存更新
    print("\n💾 步骤5: 保存数据...")
    output_data = {
        "implemented": implemented,
        "summary": {
            "total": len(implemented),
            "last_scan": datetime.now().isoformat(),
            "scan_stats": file_stats
        }
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"   ✅ 已保存到: {OUTPUT_FILE}")
    
    # 6. 总结
    print("\n" + "="*70)
    print("扫描完成")
    print("="*70)
    print(f"\n功能数量变化: {existing_count} → {len(implemented)} (+{new_features})")
    print(f"已完成任务: {len(completed_tasks)}个")
    print(f"项目文件: {file_stats['total_files']}个")
    print(f"代码行数: {file_stats['total_lines']}行")
    print()
    
    return {
        "old_count": existing_count,
        "new_count": len(implemented),
        "added": new_features,
        "completed_tasks": len(completed_tasks)
    }

if __name__ == "__main__":
    result = update_features_data()
    
    print("\n🎯 建议:")
    print("1. 刷新Dashboard: http://localhost:8820")
    print("2. 或点击透视塔的'重新扫描'按钮")
    print()

