#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最终验证 - 检查所有模块的闭合情况"""

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到所有模块
modules = []
for i, line in enumerate(lines):
    if 'engineer-module version-content' in line and '<div' in line:
        modules.append(('全栈工程师', i + 1))
    elif 'devops-module version-content' in line and '<div' in line:
        modules.append(('运维工程师', i + 1))
    elif 'code-manager-module version-content' in line and '<div' in line:
        modules.append(('Noah代码管家', i + 1))
    elif 'memory-space-module version-content' in line and '<div' in line:
        modules.append(('记忆空间', i + 1))
    elif 'pulse-module version-content' in line and '<div' in line:
        modules.append(('实时脉动', i + 1))

print("=" * 80)
print("所有模块位置")
print("=" * 80)

for name, line_num in modules:
    print(f"{name:12s}: 第 {line_num} 行")

print()
print("=" * 80)
print("模块闭合验证")
print("=" * 80)
print()

# 检查每个模块之间的div平衡
for i in range(len(modules) - 1):
    name1, start1 = modules[i]
    name2, start2 = modules[i + 1]
    
    # 统计两个模块之间的div
    div_open = 0
    div_close = 0
    
    for line_idx in range(start1 - 1, start2 - 1):
        div_open += lines[line_idx].count('<div')
        div_close += lines[line_idx].count('</div>')
    
    balance = div_open - div_close
    
    if balance == 0:
        status = "OK"
        icon = "✅"
    else:
        status = f"ERROR ({balance} 未闭合)"
        icon = "❌"
    
    print(f"{icon} {name1} → {name2}")
    print(f"   行范围: {start1} - {start2}")
    print(f"   <div>: {div_open}, </div>: {div_close}, 平衡: {balance} - {status}")
    print()

# 检查是否有结束注释
print("=" * 80)
print("结束注释检查")
print("=" * 80)

end_comments = []
for i, line in enumerate(lines):
    if '模块结束' in line or 'module end' in line.lower():
        end_comments.append((i + 1, line.strip()[:80]))

if end_comments:
    print("找到以下结束注释：")
    for line_num, comment in end_comments:
        print(f"  {line_num}: {comment}")
else:
    print("⚠️  建议：添加明确的结束注释，方便维护")

