#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量给全栈工程师模块CSS添加.engineer-module前缀
避免和其他模块的通用class冲突
"""

import re
import shutil
from datetime import datetime

FILE = "index.html"

# 全栈工程师模块CSS范围（大约3100-4300行）
CSS_START = 3100
CSS_END = 4400

# 需要添加前缀的通用class（不包括已经有.engineer-module前缀的）
CLASSES_TO_PREFIX = [
    '.status-badge',
    '.status-dot',
    '.engineer-info',
    '.info-section',
    '.engineer-avatar',
    '.engineer-details',
    '.engineer-name',
    '.engineer-meta',
    '.quick-stats',
    '.stat-item',
    '.stat-value',
    '.stat-label',
    '.tab-navigation',
    '.tab-item',
    '.tab-badge',
    '.tab-content-wrapper',
    '.tab-pane',
]

print("=" * 70)
print("全栈工程师模块CSS前缀批量修复")
print("=" * 70)
print()

# 备份
print(f"Step 1: 创建备份...")
backup = f"{FILE}.backup-engineer-css-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
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
print(f"Step 3: 处理CSS（第{CSS_START}-{CSS_END}行）...")
fixed_count = 0
new_lines = []

for i, line in enumerate(lines):
    line_num = i + 1
    
    # 只处理CSS范围内的行
    if CSS_START <= line_num <= CSS_END:
        # 跳过已经有前缀的
        if '.engineer-module' in line or '@keyframes' in line or '@media' in line:
            new_lines.append(line)
            continue
        
        # 检查是否需要添加前缀
        original_line = line
        for class_name in CLASSES_TO_PREFIX:
            # 匹配独立的class选择器
            pattern = re.escape(class_name) + r'(?=\s|\{|:|\.)'
            if re.search(pattern, line):
                line = re.sub(pattern, '.engineer-module ' + class_name, line)
                if line != original_line:
                    fixed_count += 1
                    break
        
        new_lines.append(line)
    else:
        new_lines.append(line)

print(f"✅ 已处理 {fixed_count} 个CSS选择器")
print()

# 写入
print(f"Step 4: 写入文件...")
with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print(f"✅ 文件已更新")
print()

print("=" * 70)
print("✅ CSS前缀批量修复完成！")
print("=" * 70)
print()
print("下一步: 重启8823服务器并测试")
print()

