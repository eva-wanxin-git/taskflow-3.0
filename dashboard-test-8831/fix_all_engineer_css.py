#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量给全栈工程师模块的所有CSS添加.engineer-module前缀
"""

import re
import shutil
from datetime import datetime

FILE = "index.html"

# 全栈工程师模块CSS范围
CSS_START = 3100
CSS_END = 4300

print("=" * 70)
print("全栈工程师模块CSS前缀批量修复（完整版）")
print("=" * 70)
print()

# 备份
print(f"Step 1: 创建备份...")
backup = f"{FILE}.backup-engineer-all-css-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
shutil.copy2(FILE, backup)
print(f"✅ 备份: {backup}")
print()

# 读取文件
print(f"Step 2: 读取文件...")
with open(FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"✅ 文件: {len(lines)} 行")
print()

# 处理CSS
print(f"Step 3: 批量添加前缀（第{CSS_START}-{CSS_END}行）...")
fixed_count = 0
new_lines = []

for i, line in enumerate(lines):
    line_num = i + 1
    
    # 只处理CSS范围内
    if CSS_START <= line_num <= CSS_END:
        # 跳过已经有前缀、注释、@规则
        if ('.engineer-module' in line or 
            '@keyframes' in line or 
            '@media' in line or
            line.strip().startswith('/*') or
            line.strip().startswith('*/')):
            new_lines.append(line)
            continue
        
        # 匹配CSS选择器行（以8个空格开始，后面跟.或#）
        if re.match(r'^        [\.#][a-zA-Z]', line):
            # 不是伪类、伪元素
            if not re.search(r'::(before|after|webkit-scrollbar)', line):
                # 添加前缀
                line = line.replace('        .', '        .engineer-module .')
                fixed_count += 1
        
        new_lines.append(line)
    else:
        new_lines.append(line)

print(f"✅ 已处理 {fixed_count} 行CSS")
print()

# 写入
print(f"Step 4: 写入文件...")
with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print(f"✅ 文件已更新")
print()

print("=" * 70)
print("✅ 批量前缀添加完成！")
print("=" * 70)
print()
print("下一步: 重启服务器并测试所有Tab的滚动条位置")
print()

