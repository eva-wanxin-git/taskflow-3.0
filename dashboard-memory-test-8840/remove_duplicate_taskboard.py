#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除重复的任务看板Tab（第10303-10550行）
"""

import shutil
from datetime import datetime

FILE = "index.html"

# 重复的Tab范围
DUPLICATE_START = 10303  # <!-- Tab 2: 任务看板 -->
DUPLICATE_END = 10551     # 到 <!-- Tab 3: 代码审查 --> 之前

print("=" * 60)
print("删除重复任务看板Tab脚本")
print("=" * 60)
print()

# 备份
print(f"Step 1: 创建备份...")
backup_file = f"{FILE}.backup-remove-duplicate-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
shutil.copy2(FILE, backup_file)
print(f"✅ 备份: {backup_file}")
print()

# 读取文件
print(f"Step 2: 读取文件...")
with open(FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"✅ 当前: {len(lines)} 行")
print()

# 删除重复内容
print(f"Step 3: 删除第{DUPLICATE_START}-{DUPLICATE_END}行...")
new_lines = []
new_lines.extend(lines[:DUPLICATE_START-1])  # 保留之前的
new_lines.extend(lines[DUPLICATE_END-1:])     # 保留之后的（从Tab 3开始）

deleted_lines = DUPLICATE_END - DUPLICATE_START
print(f"✅ 已删除 {deleted_lines} 行")
print(f"   新文件: {len(new_lines)} 行")
print()

# 写入
print(f"Step 4: 写入文件...")
with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print(f"✅ 文件已更新")
print()

print("=" * 60)
print("✅ 重复Tab删除完成！")
print("=" * 60)
print()
print("下一步: 重启服务器并测试Tab切换")
print()

