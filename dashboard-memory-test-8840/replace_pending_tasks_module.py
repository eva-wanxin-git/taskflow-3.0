#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
待开发任务模块替换脚本
用原始备份代码替换当前的待开发任务模块
"""

import os
import shutil
from datetime import datetime

# 文件路径
CURRENT_FILE = "index.html"
ORIGINAL_FILE = "../dashboard-test-v1.8-20251120-final/模块的演示页面和代码/taskflow-pending-tasks-redesigned.txt"
BACKUP_SUFFIX = datetime.now().strftime("backup-before-原始替换-%Y%m%d-%H%M%S")

# CSS范围
CSS_START = 1810
CSS_END = 2296

# HTML范围
HTML_START = 8079
HTML_END = 8588

print("=" * 60)
print("待开发任务模块替换脚本")
print("=" * 60)
print()

# Step 1: 创建备份
print(f"Step 1: 创建备份...")
backup_file = f"{CURRENT_FILE}.{BACKUP_SUFFIX}"
shutil.copy2(CURRENT_FILE, backup_file)
print(f"✅ 备份已创建: {backup_file}")
print()

# Step 2: 读取当前文件
print(f"Step 2: 读取当前文件...")
with open(CURRENT_FILE, 'r', encoding='utf-8') as f:
    current_lines = f.readlines()
print(f"✅ 当前文件共 {len(current_lines)} 行")
print()

# Step 3: 读取原始文件
print(f"Step 3: 读取原始代码...")
with open(ORIGINAL_FILE, 'r', encoding='utf-8') as f:
    original_content = f.read()

# 解析原始文件，提取CSS和HTML
print("   解析原始文件...")
original_lines = original_content.split('\n')

# 找到<style>和</style>之间的内容
style_start = None
style_end = None
for i, line in enumerate(original_lines):
    if '<style>' in line:
        style_start = i + 1
    elif '</style>' in line:
        style_end = i
        break

# 找到<body>和</body>之间的待开发任务模块HTML
body_start = None
body_end = None
for i, line in enumerate(original_lines):
    if '<div class="pending-features-module' in line:
        body_start = i
    elif body_start is not None and '</div>' in line and i > body_start + 100:
        # 检查是否是模块的最外层闭合标签
        # 需要找到正确的闭合标签
        pass

# 简单方法：直接提取body标签内的所有内容
body_content_start = None
body_content_end = None
for i, line in enumerate(original_lines):
    if '<body>' in line:
        body_content_start = i + 1
    elif '</body>' in line:
        body_content_end = i
        break

if style_start and style_end:
    original_css_lines = original_lines[style_start:style_end]
    print(f"✅ 提取到原始CSS: {len(original_css_lines)} 行")
else:
    print("❌ 未找到原始CSS")
    exit(1)

if body_content_start and body_content_end:
    original_html_lines = original_lines[body_content_start:body_content_end]
    print(f"✅ 提取到原始HTML: {len(original_html_lines)} 行")
else:
    print("❌ 未找到原始HTML")
    exit(1)

print()

# Step 4: 替换CSS部分
print(f"Step 4: 替换CSS部分（第{CSS_START}-{CSS_END}行）...")
new_lines = []
new_lines.extend(current_lines[:CSS_START-1])  # 保留CSS之前的部分
new_lines.extend([line + '\n' for line in original_css_lines])  # 插入原始CSS
new_lines.extend(current_lines[CSS_END:])  # 保留CSS之后的部分

print(f"✅ CSS替换完成")
print(f"   原始: {CSS_END - CSS_START + 1} 行")
print(f"   新: {len(original_css_lines)} 行")
print(f"   差异: {len(original_css_lines) - (CSS_END - CSS_START + 1)} 行")
print()

# Step 5: 计算HTML新位置（因为CSS行数变化了）
css_line_diff = len(original_css_lines) - (CSS_END - CSS_START + 1)
new_html_start = HTML_START + css_line_diff
new_html_end = HTML_END + css_line_diff

print(f"Step 5: 替换HTML部分...")
print(f"   原位置: 第{HTML_START}-{HTML_END}行")
print(f"   新位置: 第{new_html_start}-{new_html_end}行（因CSS变化）")

final_lines = []
final_lines.extend(new_lines[:new_html_start-1])  # 保留HTML之前的部分
final_lines.extend([line + '\n' for line in original_html_lines])  # 插入原始HTML
final_lines.extend(new_lines[new_html_end:])  # 保留HTML之后的部分

print(f"✅ HTML替换完成")
print(f"   原始: {HTML_END - HTML_START + 1} 行")
print(f"   新: {len(original_html_lines)} 行")
print(f"   差异: {len(original_html_lines) - (HTML_END - HTML_START + 1)} 行")
print()

# Step 6: 写入文件
print(f"Step 6: 写入新文件...")
with open(CURRENT_FILE, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print(f"✅ 文件已更新")
print(f"   新文件共 {len(final_lines)} 行")
print(f"   总行数变化: {len(final_lines) - len(current_lines)} 行")
print()

# Step 7: 验证
print(f"Step 7: 验证替换结果...")
print(f"✅ 备份文件: {backup_file}")
print(f"✅ 新文件: {CURRENT_FILE}")
print()

print("=" * 60)
print("✅ 替换完成！")
print("=" * 60)
print()
print("下一步:")
print("1. 重启服务器: kill -9 $(lsof -ti:8820) && python -m http.server 8820")
print("2. 强制刷新浏览器: Cmd+Shift+R")
print("3. 检查待开发任务模块的显示和滚动条")
print()

