#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动记忆空间模块到Noah代码管家后面
"""

import os
import re

def move_memory_module():
    """移动记忆空间模块"""
    
    html_file = "dashboard-v1.9-20251121/index.html"
    
    print("="*80)
    print("🔧 移动记忆空间模块到Noah代码管家后面")
    print("="*80)
    print()
    
    # 读取文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 步骤1: 提取记忆空间模块
    print("📍 步骤1: 提取记忆空间模块...")
    
    memory_start = content.find('<div class="memory-space-module version-content" data-version="1" id="module-memory">')
    if memory_start == -1:
        print("   ❌ 未找到记忆空间模块")
        return False
    
    # 找到对应的结束标签
    pos = memory_start
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
                memory_end = pos
                break
    
    memory_module = content[memory_start:memory_end]
    print(f"   ✅ 提取了记忆空间模块（{len(memory_module):,} 字符）")
    print()
    
    # 步骤2: 删除原位置的记忆空间模块
    print("📍 步骤2: 从原位置删除记忆空间模块...")
    content_without_memory = content[:memory_start] + content[memory_end:]
    print("   ✅ 已删除")
    print()
    
    # 步骤3: 找到Noah代码管家的结束位置
    print("📍 步骤3: 找到Noah代码管家模块...")
    
    noah_start = content_without_memory.find('<div class="code-manager-module version-content" data-version="1" id="module-noah">')
    if noah_start == -1:
        print("   ❌ 未找到Noah模块")
        return False
    
    # 找到Noah的结束标签
    pos = noah_start
    div_count = 1
    pos = content_without_memory.find('>', pos) + 1
    
    while div_count > 0 and pos < len(content_without_memory):
        next_open = content_without_memory.find('<div', pos)
        next_close = content_without_memory.find('</div>', pos)
        
        if next_close == -1:
            break
            
        if next_open != -1 and next_open < next_close:
            div_count += 1
            pos = next_open + 4
        else:
            div_count -= 1
            pos = next_close + 6
            if div_count == 0:
                noah_end = pos
                break
    
    print(f"   ✅ 找到Noah模块结束位置")
    print()
    
    # 步骤4: 在Noah后面插入记忆空间模块
    print("📍 步骤4: 在Noah后面插入记忆空间模块...")
    new_content = content_without_memory[:noah_end] + '\n\n        ' + memory_module + content_without_memory[noah_end:]
    print("   ✅ 已插入")
    print()
    
    # 保存
    print("📍 步骤5: 保存文件...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("   ✅ 文件已保存")
    print()
    
    print("="*80)
    print("✅ 移动完成！")
    print("="*80)
    print()
    print("📊 新的模块顺序:")
    print("   1. 项目透视塔")
    print("   2. 架构师工作台")
    print("   3. 待开发任务池")
    print("   4. 全栈工程师")
    print("   5. 实时脉动")
    print("   6. 运维工程师")
    print("   7. Noah代码管家")
    print("   8. 记忆空间  ← 移到这里了")
    print()
    print("🌐 访问: http://localhost:8820/")
    print("   刷新后查看效果")
    print()
    
    return True

if __name__ == "__main__":
    import sys
    try:
        success = move_memory_module()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

