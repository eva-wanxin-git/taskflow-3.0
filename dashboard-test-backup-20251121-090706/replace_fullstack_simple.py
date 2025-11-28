#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全栈工程师模块简单替换脚本
删除第9089-11277行的简版模块
"""

import shutil
from datetime import datetime

CURRENT_FILE = "index.html"
COMPLETE_VERSION = "../dashboard-test-v1.8-20251120-final/模块的演示页面和代码/fullstack-engineer-workbench-optimized.txt"

# 简版模块的HTML范围（手动指定）
HTML_START = 9089  # <!-- ========== 全栈工程师工作台 ========== -->
HTML_END = 11278   # 到记忆空间模块之前

print("=" * 70)
print("全栈工程师模块简单替换脚本")
print("=" * 70)
print()

# 备份
print(f"Step 1: 创建备份...")
backup_file = f"{CURRENT_FILE}.backup-simple-replace-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
shutil.copy2(CURRENT_FILE, backup_file)
print(f"✅ 备份: {backup_file}")
print()

# 读取当前文件
print(f"Step 2: 读取当前文件...")
with open(CURRENT_FILE, 'r', encoding='utf-8') as f:
    current_lines = f.readlines()
print(f"✅ 当前文件: {len(current_lines)} 行")
print()

# 读取完整版
print(f"Step 3: 读取完整版代码...")
with open(COMPLETE_VERSION, 'r', encoding='utf-8') as f:
    complete_content = f.read()

complete_lines = complete_content.split('\n')

# 提取CSS
css_start = None
css_end = None
for i, line in enumerate(complete_lines):
    if '<style>' in line:
        css_start = i + 1
    elif '</style>' in line and css_start:
        css_end = i
        break

# 提取HTML (body内容)
html_start = None
html_end = None
for i, line in enumerate(complete_lines):
    if '<body>' in line:
        html_start = i + 1
    elif '</body>' in line and html_start:
        html_end = i
        break

complete_css = complete_lines[css_start:css_end]
complete_html = complete_lines[html_start:html_end]

print(f"✅ 完整版CSS: {len(complete_css)} 行")
print(f"✅ 完整版HTML: {len(complete_html)} 行")
print()

# Step 4: 删除简版HTML
print(f"Step 4: 删除简版模块（第{HTML_START}-{HTML_END}行）...")
new_lines = []
new_lines.extend(current_lines[:HTML_START-1])
new_lines.extend(current_lines[HTML_END-1:])

print(f"✅ 已删除 {HTML_END - HTML_START} 行")
print(f"   新文件: {len(new_lines)} 行")
print()

# Step 5: 在架构师模块后插入完整版
print(f"Step 5: 查找插入位置...")

# 找到架构师模块结束的位置
insert_pos = None
for i, line in enumerate(new_lines):
    if '<!-- ========== 记忆空间模块 ========== -->' in line:
        insert_pos = i
        break

if not insert_pos:
    print("❌ 未找到插入位置")
    exit(1)

print(f"✅ 插入位置: 第{insert_pos+1}行（记忆空间模块之前）")
print()

# Step 6: 插入完整版HTML
print(f"Step 6: 插入完整版HTML...")
final_lines = []
final_lines.extend(new_lines[:insert_pos])
final_lines.append('\n')
final_lines.append('        <!-- ========== 全栈工程师工作台（完整版） ========== -->\n')
final_lines.extend([line + '\n' for line in complete_html])
final_lines.append('\n')
final_lines.extend(new_lines[insert_pos:])

print(f"✅ 已插入完整版HTML: {len(complete_html)} 行")
print()

# Step 7: 现在处理CSS - 需要找到简版CSS并删除，插入完整版CSS
print(f"Step 7: 处理CSS部分...")

# 简单方法：查找 .engineer-module { 开始的CSS块
css_insert_pos = None
css_block_start = None
css_block_end = None

for i, line in enumerate(final_lines):
    # 找到待开发任务模块CSS结束的位置（作为插入点）
    if '.pending-features-module.version-content[data-version=' in line:
        css_insert_pos = i + 1
    # 找到简版engineer-module的CSS块
    if '.engineer-module {' in line and not css_block_start:
        css_block_start = i
    # 找到engineer-module CSS块的结束（到下一个大模块CSS）
    if css_block_start and ('.api-status-' in line or '.memory-space-module' in line):
        css_block_end = i
        break

if css_block_start and css_block_end:
    print(f"✅ 找到简版CSS: 第{css_block_start+1}-{css_block_end}行")
    # 删除简版CSS
    final_lines_no_old_css = final_lines[:css_block_start] + final_lines[css_block_end:]
    
    # 重新计算插入位置
    if css_insert_pos:
        css_diff = css_block_end - css_block_start
        new_css_insert_pos = css_insert_pos if css_insert_pos < css_block_start else css_insert_pos - css_diff
    else:
        new_css_insert_pos = css_block_start
    
    # 插入完整版CSS
    final_lines = []
    final_lines.extend(final_lines_no_old_css[:new_css_insert_pos])
    final_lines.append('\n')
    final_lines.append('        /* ==================== 全栈工程师工作台（完整版） ==================== */\n')
    final_lines.extend([line + '\n' for line in complete_css])
    final_lines.append('\n')
    final_lines.extend(final_lines_no_old_css[new_css_insert_pos:])
    
    print(f"✅ 已插入完整版CSS: {len(complete_css)} 行")
else:
    print(f"⚠️ 未找到简版CSS，跳过CSS替换")

print()

# Step 8: 写入文件
print(f"Step 8: 写入文件...")
with open(CURRENT_FILE, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print(f"✅ 文件已更新")
print(f"   最终行数: {len(final_lines)} 行")
print(f"   变化: {len(final_lines) - len(current_lines)} 行")
print()

print("=" * 70)
print("✅ 全栈工程师完整版替换成功！")
print("=" * 70)
print()
print("📍 下一步:")
print("1. 重启服务器: lsof -ti:8823 | xargs kill -9 && python3 -m http.server 8823")
print("2. 访问: http://localhost:8823/")
print("3. 查找全栈工程师模块，应该有5个Tab")
print()

