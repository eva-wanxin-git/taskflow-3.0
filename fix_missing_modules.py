#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复未匹配的模块ID
"""

import os
from datetime import datetime

def fix_missing_modules():
    """修复未匹配的模块"""
    
    html_file = "dashboard-test-8826/index.html"
    
    print("="*80)
    print("🔧 修复未匹配的模块ID")
    print("="*80)
    print()
    
    # 读取文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = f"{html_file}.backup-fix-{timestamp}"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📋 已备份到: {backup_file}\n")
    
    # 定义需要修复的模块
    fixes = [
        {
            'name': '架构师工作台',
            'old': '<div class="architect-module version-content" data-version="1">',
            'new': '<div class="architect-module version-content" data-version="1" id="module-architect">',
        },
        {
            'name': '实时脉动',
            'old': '<div class="pulse-module version-content" data-version="1">',
            'new': '<div class="pulse-module version-content" data-version="1" id="module-pulse">',
        },
        {
            'name': '运维工程师',
            'old': '<div class="devops-module version-content" data-version="1">',
            'new': '<div class="devops-module version-content" data-version="1" id="module-devops">',
        },
        {
            'name': 'Noah代码管家',
            'old': '<div class="code-manager-module version-content" data-version="1">',
            'new': '<div class="code-manager-module version-content" data-version="1" id="module-noah">',
        },
    ]
    
    print("📍 添加模块ID...")
    
    for fix in fixes:
        if fix['old'] in content:
            content = content.replace(fix['old'], fix['new'], 1)
            print(f"   ✅ {fix['name']}: 已添加ID")
        else:
            print(f"   ⚠️  {fix['name']}: 未找到匹配")
            print(f"      查找: {fix['old'][:60]}...")
    
    # 保存
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print()
    print("✅ 修复完成！")
    print()
    print("🌐 现在可以访问 http://localhost:8826/ 测试导航栏")
    print()
    
    return True

if __name__ == "__main__":
    import sys
    try:
        success = fix_missing_modules()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

