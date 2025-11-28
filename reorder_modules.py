#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调整模块顺序
将架构师模块移动到待开发任务池上面
"""

import os
import re
from datetime import datetime

def reorder_modules():
    """调整模块顺序"""
    
    html_file = "dashboard-test-8826/index.html"
    
    print("="*80)
    print("🔧 调整模块顺序：架构师 → 待开发任务池上方")
    print("="*80)
    print()
    
    # 读取文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("📍 步骤1: 提取架构师模块...")
    
    # 找到架构师模块的开始和结束
    architect_start = content.find('<div class="architect-module version-content" data-version="1" id="module-architect">')
    if architect_start == -1:
        print("   ❌ 未找到架构师模块")
        return False
    
    # 找到对应的结束标签（找到匹配的</div>）
    # 需要计数div标签来找到正确的结束位置
    pos = architect_start
    div_count = 1
    pos = content.find('>', pos) + 1
    
    while div_count > 0 and pos < len(content):
        next_open = content.find('<div', pos)
        next_close = content.find('</div>', pos)
        
        if next_close == -1:
            break
            
        if next_open != -1 and next_open < next_close:
            div_count += 1
            pos = next_open + 4
        else:
            div_count -= 1
            pos = next_close + 6
            if div_count == 0:
                architect_end = pos
                break
    
    if div_count != 0:
        print("   ❌ 未找到架构师模块的结束标签")
        return False
    
    # 提取架构师模块
    architect_module = content[architect_start:architect_end]
    print(f"   ✅ 提取了架构师模块（{len(architect_module):,} 字符）")
    print()
    
    # 步骤2: 删除原位置的架构师模块
    print("📍 步骤2: 从原位置删除架构师模块...")
    content_without_architect = content[:architect_start] + content[architect_end:]
    print("   ✅ 已删除")
    print()
    
    # 步骤3: 找到待开发任务池的位置
    print("📍 步骤3: 找到待开发任务池位置...")
    pending_start = content_without_architect.find('<div class="pending-features-module" id="module-pending-tasks">')
    
    if pending_start == -1:
        print("   ❌ 未找到待开发任务池")
        return False
    
    print(f"   ✅ 找到待开发任务池（位置: {pending_start}）")
    print()
    
    # 步骤4: 在待开发任务池前插入架构师模块
    print("📍 步骤4: 在待开发任务池前插入架构师模块...")
    new_content = content_without_architect[:pending_start] + architect_module + '\n\n        ' + content_without_architect[pending_start:]
    print("   ✅ 已插入")
    print()
    
    # 步骤5: 更新左侧导航顺序
    print("📍 步骤5: 更新左侧导航顺序...")
    
    old_nav = """        <ul class="side-nav-list">
            <li class="side-nav-item">
                <a class="side-nav-link" data-module="module-project-view" onclick="scrollToModule('module-project-view'); return false;">
                    项目透视塔
                </a>
            </li>
            <li class="side-nav-item">
                <a class="side-nav-link" data-module="module-pending-tasks" onclick="scrollToModule('module-pending-tasks'); return false;">
                    待开发任务池
                </a>
            </li>
            <li class="side-nav-item">
                <a class="side-nav-link" data-module="module-architect" onclick="scrollToModule('module-architect'); return false;">
                    架构师工作台
                </a>
            </li>"""
    
    new_nav = """        <ul class="side-nav-list">
            <li class="side-nav-item">
                <a class="side-nav-link" data-module="module-project-view" onclick="scrollToModule('module-project-view'); return false;">
                    项目透视塔
                </a>
            </li>
            <li class="side-nav-item">
                <a class="side-nav-link" data-module="module-architect" onclick="scrollToModule('module-architect'); return false;">
                    架构师工作台
                </a>
            </li>
            <li class="side-nav-item">
                <a class="side-nav-link" data-module="module-pending-tasks" onclick="scrollToModule('module-pending-tasks'); return false;">
                    待开发任务池
                </a>
            </li>"""
    
    if old_nav in new_content:
        new_content = new_content.replace(old_nav, new_nav)
        print("   ✅ 导航顺序已更新")
    else:
        print("   ⚠️  导航未找到，可能需要手动调整")
    print()
    
    # 步骤6: 更新JavaScript中的模块顺序
    print("📍 步骤6: 更新JavaScript中的模块顺序...")
    
    old_js_order = """                const modules = [
                    'module-project-view',
                    'module-pending-tasks',
                    'module-architect',"""
    
    new_js_order = """                const modules = [
                    'module-project-view',
                    'module-architect',
                    'module-pending-tasks',"""
    
    if old_js_order in new_content:
        new_content = new_content.replace(old_js_order, new_js_order)
        print("   ✅ JavaScript顺序已更新")
    else:
        print("   ⚠️  JavaScript未更新")
    print()
    
    # 保存
    print("📍 步骤7: 保存修改...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("   ✅ 文件已保存")
    print()
    
    print("="*80)
    print("✅ 模块顺序调整完成！")
    print("="*80)
    print()
    print("📊 新顺序:")
    print("   1. 项目透视塔")
    print("   2. 架构师工作台  ← 移到这里了")
    print("   3. 待开发任务池")
    print("   4. 全栈工程师")
    print("   5. 实时脉动")
    print("   6. 运维工程师")
    print("   7. Noah代码管家")
    print()
    print("🧪 测试地址: http://localhost:8826/")
    print("   强制刷新后查看效果")
    print()
    
    return True

if __name__ == "__main__":
    import sys
    try:
        success = reorder_modules()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

