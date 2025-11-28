#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
架构师同步部分实现功能和冲突建议到Dashboard
从v17-complete-features.json提取partial和conflicts数据，更新到project_scan.json
"""
import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
COMPLETE_FEATURES_FILE = PROJECT_ROOT / "apps/dashboard/automation-data/v17-complete-features.json"
PROJECT_SCAN_FILE = PROJECT_ROOT / "apps/dashboard/automation-data/project_scan.json"

def load_complete_features():
    """加载完整功能清单"""
    with open(COMPLETE_FEATURES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_project_scan():
    """加载project_scan数据"""
    with open(PROJECT_SCAN_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def transform_partial_features(partial_list):
    """转换部分实现功能格式"""
    transformed = []
    for item in partial_list:
        transformed.append({
            "name": item['name'],
            "file": item.get('file', ''),
            "type": item.get('type', '待完善'),
            "status": "部分实现",
            "completion": item.get('completion', 0),
            "missing": item.get('missing', []),
            "priority": item.get('priority', 'P2'),
            "estimated_hours": item.get('estimated_fix_hours', 0)
        })
    return transformed

def transform_conflicts(conflicts_list):
    """转换冲突建议格式"""
    transformed = []
    for item in conflicts_list:
        # 根据ID类型判断
        if item['id'].startswith('CONF-'):
            # 真正的冲突
            transformed.append({
                "name": item['name'],
                "severity": item.get('severity', 'Medium'),
                "impact": item.get('impact', ''),
                "affected_features": item.get('affected_features', []),
                "suggestion": item.get('suggestion', ''),
                "estimated_fix_hours": item.get('estimated_fix_hours', 0),
                "type": "冲突"
            })
        elif item['id'].startswith('ARCH-ADVICE-'):
            # 架构建议
            transformed.append({
                "name": item['name'],
                "severity": item.get('severity', 'Strategic'),
                "impact": item.get('impact', ''),
                "suggestion": item.get('suggestion', ''),
                "rationale": item.get('rationale', []),
                "type": "建议"
            })
    return transformed

def main():
    """主函数"""
    print("\n" + "="*70)
    print("架构师同步部分实现和冲突到Dashboard")
    print("="*70)
    print()
    
    # 1. 加载数据
    print("[1/3] 加载完整功能清单...")
    complete_features = load_complete_features()
    partial_count = len(complete_features.get('partial', []))
    conflicts_count = len(complete_features.get('conflicts', []))
    print(f"  部分实现: {partial_count}个")
    print(f"  冲突/建议: {conflicts_count}个")
    
    # 2. 加载project_scan
    print("\n[2/3] 加载project_scan.json...")
    project_scan = load_project_scan()
    old_partial = len(project_scan['features'].get('partial', []))
    old_conflicts = len(project_scan['features'].get('conflicts', []))
    print(f"  当前部分实现: {old_partial}个（旧数据）")
    print(f"  当前冲突: {old_conflicts}个（旧数据）")
    
    # 3. 转换并更新
    print("\n[3/3] 转换并更新数据...")
    project_scan['features']['partial'] = transform_partial_features(
        complete_features.get('partial', [])
    )
    project_scan['features']['conflicts'] = transform_conflicts(
        complete_features.get('conflicts', [])
    )
    
    # 更新扫描时间
    project_scan['scan_time'] = datetime.now().isoformat()
    project_scan['last_updated_by'] = 'architect'
    
    # 保存
    with open(PROJECT_SCAN_FILE, 'w', encoding='utf-8') as f:
        json.dump(project_scan, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ 更新部分实现: {old_partial} → {partial_count}个")
    print(f"  ✓ 更新冲突/建议: {old_conflicts} → {conflicts_count}个")
    
    # 总结
    print("\n" + "="*70)
    print("✅ Dashboard数据已同步")
    print("="*70)
    print()
    print(f"  部分实现功能: {partial_count}个")
    print()
    print("  主要包括:")
    for item in complete_features.get('partial', [])[:5]:
        print(f"    - {item['name']} ({item.get('completion', 0)*100:.0f}%)")
    print()
    print(f"  冲突/建议: {conflicts_count}个")
    print()
    print("  主要包括:")
    for item in complete_features.get('conflicts', [])[:5]:
        severity = item.get('severity', 'Medium')
        emoji = {'Critical': '🔴', 'High': '🟡', 'Medium': '🟠', 'Strategic': '💡'}.get(severity, '⚪')
        print(f"    {emoji} {item['name']}")
    print()
    print("下一步:")
    print("  1. Dashboard会在10秒内自动刷新")
    print("  2. 或手动刷新浏览器: http://localhost:8877")
    print("  3. 查看'部分实现功能'和'冲突/建议取舍'Tab")
    print()
    print("="*70)

if __name__ == "__main__":
    main()

