#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""简单检查HTML结构"""

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到关键位置
devops_start = 0
noah_start = 0

for i, line in enumerate(lines):
    if 'devops-module version-content' in line and '<div' in line:
        devops_start = i + 1
    if 'code-manager-module version-content' in line and '<div' in line:
        noah_start = i + 1

print("=" * 80)
print("模块位置")
print("=" * 80)
print(f"运维模块开始: 第 {devops_start} 行")
print(f"Noah模块开始: 第 {noah_start} 行")
print(f"间隔: {noah_start - devops_start} 行")
print()

# 统计两者之间的div标签
if devops_start and noah_start:
    div_open = 0
    div_close = 0
    
    print("=" * 80)
    print(f"运维模块区域 (第{devops_start}行 到 第{noah_start}行)")
    print("=" * 80)
    
    for i in range(devops_start - 1, noah_start - 1):
        line = lines[i]
        div_open += line.count('<div')
        div_close += line.count('</div>')
    
    print(f"<div 标签: {div_open}")
    print(f"</div> 标签: {div_close}")
    print(f"差值: {div_open - div_close}")
    print()
    
    if div_open > div_close:
        print(f"❌ 问题：有 {div_open - div_close} 个未闭合的 <div> 标签！")
        print("   Noah模块被错误地包含在运维模块内")
        print()
        print("🔍 查找缺失的闭合标签...")
        print()
        
        # 显示Noah之前的最后几个div
        print("Noah模块开始前的最后10行:")
        for i in range(noah_start - 11, noah_start - 1):
            if '</div>' in lines[i] or '<div' in lines[i]:
                print(f"  {i+1}: {lines[i].rstrip()[:100]}")
                
    elif div_open == div_close:
        print("✅ 标签配对正常")
        print("   问题不在HTML结构，应该检查CSS")
    else:
        print(f"❌ 异常：闭合标签比开始标签多 {div_close - div_open} 个")

print()
print("=" * 80)
print("验证：检查Noah是否在运维的闭合标签之后")  
print("=" * 80)

# 从运维开始往后找，看哪个先出现：运维的闭合还是Noah的开始
devops_depth = 0
found_devops_end = False

for i in range(devops_start - 1, noah_start + 100):
    if i >= len(lines):
        break
    line = lines[i]
    
    # 遇到开标签，深度+1
    devops_depth += line.count('<div')
    # 遇到闭标签，深度-1  
    devops_depth -= line.count('</div>')
    
    # 如果深度回到0，说明运维模块完整闭合了
    if devops_depth == 0 and i > devops_start:
        found_devops_end = True
        print(f"✅ 运维模块在第 {i+1} 行完整闭合")
        break
        
    # 如果还没闭合就遇到Noah
    if 'code-manager-module' in line:
        if devops_depth > 0:
            print(f"❌ 第 {i+1} 行遇到Noah，但运维模块还有 {devops_depth} 层未闭合")
            print(f"   这意味着Noah被包含在运维模块里了")
        break

if found_devops_end and noah_start > i:
    print(f"✅ Noah模块在运维闭合之后(第{noah_start}行)，结构正确")

