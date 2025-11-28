#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复待开发任务模块CSS前缀
给所有通用class添加.pending-features-module前缀
"""

import re
from datetime import datetime

FILE = "index.html"
BACKUP_SUFFIX = datetime.now().strftime("backup-before-css-prefix-%Y%m%d-%H%M%S")

# 需要添加前缀的class（不包括已经有前缀的）
CLASSES_TO_PREFIX = [
    '.task-card',
    '.task-header',
    '.task-id',
    '.task-title',
    '.task-source',
    '.task-description',
    '.task-requirements',
    '.task-requirements-title',
    '.task-requirements-list',
    '.task-meta',
    '.task-meta-item',
    '.task-meta-label',
    '.task-meta-value',
    '.task-priority',
    '.task-tags',
    '.task-tag',
    '.review-info',
    '.review-info-title',
    '.review-info-content',
    '.user-decision-area',
    '.decision-title',
    '.decision-buttons',
    '.decision-button',
    '.architect-status',
    '.status-icon',
]

print("=" * 60)
print("待开发任务模块CSS前缀修复脚本")
print("=" * 60)
print()

# Step 1: 备份
print(f"Step 1: 创建备份...")
import shutil
backup_file = f"{FILE}.{BACKUP_SUFFIX}"
shutil.copy2(FILE, backup_file)
print(f"✅ 备份已创建: {backup_file}")
print()

# Step 2: 读取文件
print(f"Step 2: 读取文件...")
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')
print(f"✅ 文件共 {len(lines)} 行")
print()

# Step 3: 在CSS部分添加前缀（第1863-2350行区间）
print(f"Step 3: 批量添加.pending-features-module前缀...")

# 只处理CSS部分（大约1863-2400行之间）
new_lines = []
in_pending_css = False
pending_css_start = 1863
pending_css_end = 2400
fixes_count = 0

for i, line in enumerate(lines):
    line_num = i + 1
    
    # 判断是否在待开发任务模块的CSS范围内
    if line_num == pending_css_start:
        in_pending_css = True
    elif line_num == pending_css_end:
        in_pending_css = False
    
    # 如果在范围内，处理CSS
    if in_pending_css and '.pending-features-module' in line:
        # 已经有前缀的行，直接跳过
        new_lines.append(line)
    elif in_pending_css:
        # 需要添加前缀的行
        original_line = line
        for class_name in CLASSES_TO_PREFIX:
            # 匹配独立的class选择器（后面跟空格、{、:、.等）
            pattern = re.escape(class_name) + r'(?=\s|\{|:|\.)'
            if re.search(pattern, line):
                # 添加前缀
                line = re.sub(pattern, '.pending-features-module ' + class_name, line)
                if line != original_line:
                    fixes_count += 1
                break
        new_lines.append(line)
    else:
        new_lines.append(line)

print(f"✅ 已处理 {fixes_count} 个CSS选择器")
print()

# Step 4: 写入文件
print(f"Step 4: 写入文件...")
content = '\n'.join(new_lines)
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ 文件已更新")
print()

print("=" * 60)
print("✅ CSS前缀修复完成！")
print("=" * 60)
print()
print("下一步:")
print("1. 重启服务器")
print("2. 强制刷新浏览器: Cmd+Shift+R")
print("3. 检查待开发任务模块")
print()

