#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署透视塔模块到8826测试环境
从dashboard-test提取透视塔，部署到dashboard-test-8826
"""

import os
from datetime import datetime

def deploy_insight_module():
    """部署透视塔模块"""
    
    source_file = "dashboard-test/index.html"
    target_file = "dashboard-test-8826/index.html"
    
    print("="*80)
    print("🔧 部署透视塔模块到8826测试环境")
    print("="*80)
    print()
    
    # 读取源文件和目标文件
    with open(source_file, 'r', encoding='utf-8') as f:
        source_content = f.read()
    
    with open(target_file, 'r', encoding='utf-8') as f:
        target_content = f.read()
    
    # 备份
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = f"{target_file}.backup-insight-{timestamp}"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(target_content)
    print(f"📋 已备份8826: {backup_file}\n")
    
    # 步骤1: 从源文件提取透视塔模块
    print("📍 步骤1: 从dashboard-test提取透视塔模块...")
    
    source_start = source_content.find('<!-- ========== 项目透视模块 ========== -->')
    if source_start == -1:
        print("   ❌ 未找到源透视塔标记")
        return False
    
    # 找到透视塔模块的结束（下一个模块开始）
    next_module = source_content.find('<!-- ========== 待开发任务', source_start + 100)
    if next_module == -1:
        print("   ❌ 未找到模块结束标记")
        return False
    
    source_insight = source_content[source_start:next_module]
    print(f"   ✅ 提取了 {len(source_insight):,} 字符")
    print()
    
    # 步骤2: 找到目标文件的透视塔位置
    print("📍 步骤2: 找到8826的透视塔位置...")
    
    target_start = target_content.find('<!-- ========== 项目透视模块 ========== -->')
    if target_start == -1:
        # 如果没有，找page-container
        target_start = target_content.find('<div class="page-container version-content" data-version="1" id="module-project-view">')
        if target_start == -1:
            print("   ❌ 未找到目标位置")
            return False
    
    target_next = target_content.find('<!-- ========== 待开发任务', target_start + 100)
    if target_next == -1:
        # 如果找不到待开发任务，找架构师模块
        target_next = target_content.find('<!-- ========== 架构师', target_start + 100)
        if target_next == -1:
            print("   ❌ 未找到替换结束位置")
            return False
    
    print(f"   ✅ 找到位置: {target_start} - {target_next}")
    print()
    
    # 步骤3: 替换
    print("📍 步骤3: 替换透视塔模块...")
    
    new_content = target_content[:target_start] + source_insight + target_content[target_next:]
    
    old_size = len(target_content)
    new_size = len(new_content)
    print(f"   原大小: {old_size:,} 字符")
    print(f"   新大小: {new_size:,} 字符")
    print(f"   变化: {new_size - old_size:+,} 字符")
    print()
    
    # 保存
    print("📍 步骤4: 保存到8826...")
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("   ✅ 已保存")
    print()
    
    print("="*80)
    print("✅ 透视塔模块部署完成！")
    print("="*80)
    print()
    print("🎯 新透视塔功能:")
    print("   • 5个Tab（最后一个是'架构师扫描'）")
    print("   • 实时API数据")
    print("   • 161个已实现功能（不是132）")
    print("   • 架构师扫描指令一键复制")
    print()
    print("🧪 测试地址: http://localhost:8826/")
    print("   请强制刷新测试！")
    print()
    
    return True

if __name__ == "__main__":
    import sys
    try:
        success = deploy_insight_module()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

