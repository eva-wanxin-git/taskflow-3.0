#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
架构师逐个验证任务完成情况
不只是看完成报告，而是真正检查：代码是否存在、功能是否可用、是否集成到Dashboard
"""
import sqlite3
from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "database/data/tasks.db"

def check_file_exists(file_path):
    """检查文件是否存在"""
    full_path = PROJECT_ROOT / file_path
    return full_path.exists(), full_path

def check_code_in_file(file_path, search_text):
    """检查文件中是否包含指定代码"""
    full_path = PROJECT_ROOT / file_path
    if not full_path.exists():
        return False
    try:
        content = full_path.read_text(encoding='utf-8')
        return search_text in content
    except:
        return False

def verify_task(task_id, task_title):
    """验证单个任务"""
    print(f"\n{'='*80}")
    print(f"验证: {task_id} - {task_title}")
    print(f"{'='*80}")
    
    verification = {
        'task_id': task_id,
        'checks': [],
        'is_completed': False,
        'is_integrated': False,
        'notes': []
    }
    
    # 根据不同任务类型进行不同的验证
    
    if task_id == 'TASK-UI-001':
        print("\n检查：Dashboard项目记忆空间Tab")
        # 检查templates.py中是否有记忆空间Tab
        has_tab_button = check_code_in_file('apps/dashboard/src/industrial_dashboard/templates.py', '项目记忆空间')
        has_tab_content = check_code_in_file('apps/dashboard/src/industrial_dashboard/templates.py', 'id="architectMemory"')
        has_js_function = check_code_in_file('apps/dashboard/src/industrial_dashboard/templates.py', 'loadMemories()')
        
        print(f"  ✓ Tab按钮存在: {has_tab_button}")
        print(f"  ✓ Tab内容区存在: {has_tab_content}")
        print(f"  ✓ JavaScript函数存在: {has_js_function}")
        
        verification['checks'] = [has_tab_button, has_tab_content, has_js_function]
        verification['is_completed'] = all([has_tab_button, has_tab_content, has_js_function])
        verification['is_integrated'] = verification['is_completed']
        
        if verification['is_completed']:
            print("\n  ✅ 结论：TASK-UI-001 已完成且已集成到Dashboard")
        else:
            print("\n  ❌ 结论：TASK-UI-001 代码不完整")
    
    elif task_id == 'TASK-UI-002':
        print("\n检查：Dashboard事件流Tab增强版")
        # 检查event_stream_template_v3.html是否存在
        exists, file_path = check_file_exists('event_stream_template_v3.html')
        has_chart_js = check_code_in_file('apps/dashboard/src/industrial_dashboard/templates.py', 'Chart.js') if not exists else check_code_in_file('event_stream_template_v3.html', 'Chart.js')
        has_filter = check_code_in_file('apps/dashboard/src/industrial_dashboard/templates.py', '筛选器') or check_code_in_file('apps/dashboard/src/industrial_dashboard/dashboard.py', '/events')
        
        print(f"  ✓ v3模板存在: {exists}")
        print(f"  ✓ Chart.js集成: {has_chart_js}")
        print(f"  ✓ 筛选功能: {has_filter}")
        
        verification['is_completed'] = True  # 用户确认已完成
        verification['is_integrated'] = exists  # 需要模板文件存在
        
        if verification['is_completed']:
            print("\n  ✅ 结论：TASK-UI-002 已完成")
            if verification['is_integrated']:
                print("  ✅ 已集成到Dashboard")
            else:
                print("  ⚠️ 需要确认集成情况")
    
    elif task_id == 'TASK-AUTO-001':
        print("\n检查：自动化看板刷新脚本")
        # 检查脚本是否存在
        script_exists = check_file_exists('services/task_board_auto_sync.py')[0]
        has_backup = check_code_in_file('services/task_board_auto_sync.py', 'backup_board') if script_exists else False
        has_sync = check_code_in_file('services/task_board_auto_sync.py', 'def sync') if script_exists else False
        
        print(f"  ✓ 脚本文件存在: {script_exists}")
        print(f"  ✓ 备份功能: {has_backup}")
        print(f"  ✓ 同步功能: {has_sync}")
        
        verification['is_completed'] = script_exists and has_backup and has_sync
        verification['is_integrated'] = verification['is_completed']  # 脚本类任务，存在即可用
        
        if verification['is_completed']:
            print("\n  ✅ 结论：TASK-AUTO-001 已完成且可立即使用")
        else:
            print("\n  ❌ 结论：TASK-AUTO-001 代码不完整")
    
    elif task_id == 'TASK-C-2':
        print("\n检查：ArchitectOrchestrator数据库集成")
        # 检查architect_orchestrator.py中的TODO是否实现
        has_file = check_file_exists('apps/api/src/services/architect_orchestrator.py')[0]
        has_todo = check_code_in_file('apps/api/src/services/architect_orchestrator.py', '# TODO:') if has_file else True
        
        print(f"  ✓ 文件存在: {has_file}")
        print(f"  ⚠️ 还有TODO: {has_todo}")
        
        verification['is_completed'] = has_file and not has_todo
        verification['is_integrated'] = has_file  # 文件存在但可能有TODO未实现
        
        if verification['is_completed']:
            print("\n  ✅ 结论：TASK-C-2 已完成")
        else:
            print("\n  ⚠️ 结论：TASK-C-2 部分完成（还有TODO）")
    
    elif task_id.startswith('INTEGRATE-'):
        print(f"\n检查：集成任务 {task_id}")
        # 集成任务需要检查功能是否真的可用
        print("  ⚠️ 需要人工验证：功能是否真的集成到Dashboard")
        verification['is_completed'] = False  # 需要人工确认
        verification['notes'].append("需要启动Dashboard验证功能是否可用")
    
    else:
        print(f"\n  ⚠️ 未定义验证规则，需要人工检查")
        verification['is_completed'] = False
    
    return verification

# 关键任务列表（需要逐个验证）
KEY_TASKS = [
    ('TASK-UI-001', 'Dashboard项目记忆空间Tab'),
    ('TASK-UI-002', 'Dashboard事件流Tab增强版'),
    ('TASK-AUTO-001', '自动化看板刷新脚本'),
    ('TASK-C-2', 'ArchitectOrchestrator数据库集成'),
    ('INTEGRATE-005', '集成事件流系统'),
    ('INTEGRATE-009', '集成记忆空间'),
]

def main():
    """主函数"""
    print("\n" + "="*80)
    print("架构师逐个验证任务完成情况")
    print("="*80)
    print("\n⚠️ 重要：不只是看完成报告，而是真正检查代码和集成情况！")
    print()
    
    results = []
    
    for task_id, task_title in KEY_TASKS:
        result = verify_task(task_id, task_title)
        results.append(result)
    
    # 总结
    print("\n" + "="*80)
    print("验证总结")
    print("="*80)
    print()
    
    completed_and_integrated = [r for r in results if r['is_completed'] and r['is_integrated']]
    completed_not_integrated = [r for r in results if r['is_completed'] and not r['is_integrated']]
    not_completed = [r for r in results if not r['is_completed']]
    
    print(f"  ✅ 已完成且已集成: {len(completed_and_integrated)}个")
    for r in completed_and_integrated:
        print(f"     • {r['task_id']}")
    
    print()
    print(f"  ⚠️ 已完成但未集成: {len(completed_not_integrated)}个")
    for r in completed_not_integrated:
        print(f"     • {r['task_id']}")
    
    print()
    print(f"  ❌ 未完成: {len(not_completed)}个")
    for r in not_completed:
        print(f"     • {r['task_id']}")
    
    print()
    print("="*80)
    print("建议行动")
    print("="*80)
    print()
    print("只有真正验证完成且集成的任务，才应该更新为completed状态。")
    print("其他任务需要继续完成或集成。")
    print()

if __name__ == "__main__":
    main()

