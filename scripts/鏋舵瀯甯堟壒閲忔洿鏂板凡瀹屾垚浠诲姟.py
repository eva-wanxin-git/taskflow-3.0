#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
架构师批量更新已完成任务状态
根据完成报告，批量更新数据库中的任务状态为completed
"""
import sqlite3
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "database/data/tasks.db"

# 根据扫描结果，这些任务有完成报告，应该标记为completed
TASKS_TO_UPDATE = [
    # 最新完成的
    'TASK-UI-002',  # Dashboard事件流Tab增强版（用户确认已完成）
    'TASK-UI-001',  # Dashboard记忆空间Tab（完成报告已存在）
    'TASK-AUTO-001', # 自动化看板刷新脚本（完成报告已存在）
    
    # 集成任务（有完成报告）
    'INTEGRATE-005', # 集成事件流系统
    'INTEGRATE-009', # 集成记忆空间
    'INTEGRATE-014', # 集成BUG-001修复
    
    # 架构任务（有完成报告）
    'TASK-004-A2',   # 补充企业级知识库Schema
    'TASK-004-C',    # 真实项目测试封装包
    'TASK-C-2',      # 集成ArchitectOrchestrator数据库
    
    # 验证任务
    'INTEGRATE-010', # 验证REQ-009
    'INTEGRATE-011', # 验证REQ-010
    'INTEGRATE-013', # 验证TASK-C-3
    
    # 其他
    'TASK-INTEGRATE-003', # 集成对话历史库
    'TASK-ARCH-005',  # 深度分析REQ-005
    'TASK-ARCH-008',  # 设计REQ-008
    'TASK-D-1',       # 迁移models
    'TASK-D-2',       # 迁移state_manager
]

def update_task_status(task_id, new_status='completed'):
    """更新单个任务状态"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE tasks 
            SET status = ?, updated_at = ?, actual_hours = estimated_hours
            WHERE id = ?
        """, (new_status, datetime.now().isoformat(), task_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def check_task_exists(task_id):
    """检查任务是否存在"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status FROM tasks WHERE id = ?", (task_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def main():
    """主函数"""
    print("\n" + "="*80)
    print("架构师批量更新已完成任务状态")
    print("="*80)
    print()
    
    print(f"准备更新: {len(TASKS_TO_UPDATE)}个任务")
    print()
    
    updated = []
    skipped = []
    not_found = []
    
    for task_id in TASKS_TO_UPDATE:
        # 检查任务是否存在
        task_info = check_task_exists(task_id)
        
        if not task_info:
            not_found.append(task_id)
            print(f"  ✗ {task_id:25s} - 任务不存在")
            continue
        
        current_status = task_info[2]
        
        if current_status == 'completed':
            skipped.append(task_id)
            print(f"  - {task_id:25s} - 已经是completed，跳过")
        elif current_status == 'cancelled':
            skipped.append(task_id)
            print(f"  - {task_id:25s} - 已取消，跳过")
        else:
            if update_task_status(task_id):
                updated.append(task_id)
                print(f"  ✓ {task_id:25s} - {current_status} → completed")
            else:
                print(f"  ✗ {task_id:25s} - 更新失败")
    
    # 总结
    print()
    print("="*80)
    print("更新总结")
    print("="*80)
    print()
    print(f"  ✓ 成功更新: {len(updated)}个")
    print(f"  - 已是completed: {len([t for t in skipped if check_task_exists(t) and check_task_exists(t)[2]=='completed'])}个")
    print(f"  - 已取消跳过: {len([t for t in skipped if check_task_exists(t) and check_task_exists(t)[2]=='cancelled'])}个")
    print(f"  ✗ 任务不存在: {len(not_found)}个")
    print()
    
    if updated:
        print("已更新的任务:")
        for task_id in updated:
            print(f"  • {task_id}")
        print()
    
    if not_found:
        print("不存在的任务（可能ID错误）:")
        for task_id in not_found:
            print(f"  • {task_id}")
        print()
    
    # 查询最新统计
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status")
    stats = dict(cursor.fetchall())
    conn.close()
    
    print("="*80)
    print("更新后任务统计")
    print("="*80)
    print()
    print(f"  ✅ 已完成: {stats.get('completed', 0)}个")
    print(f"  🔄 进行中: {stats.get('in_progress', 0)}个")
    print(f"  ⏳ 待处理: {stats.get('pending', 0)}个")
    print(f"  ❌ 已取消: {stats.get('cancelled', 0)}个")
    print()
    total = sum(stats.values())
    completed_pct = stats.get('completed', 0) / total * 100 if total > 0 else 0
    print(f"  完成度: {completed_pct:.1f}% ({stats.get('completed', 0)}/{total})")
    print()
    print("="*80)

if __name__ == "__main__":
    main()

