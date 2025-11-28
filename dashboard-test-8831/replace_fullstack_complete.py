#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全栈工程师完整版替换脚本
删除简版，用1.8备份中的完整版替换
"""

import os
import shutil
from datetime import datetime

# 文件路径
CURRENT_FILE = "index.html"
COMPLETE_VERSION = "../dashboard-test-v1.8-20251120-final/模块的演示页面和代码/fullstack-engineer-workbench-optimized.txt"
BACKUP_SUFFIX = datetime.now().strftime("backup-before-fullstack-complete-%Y%m%d-%H%M%S")

print("=" * 70)
print("全栈工程师完整版替换脚本")
print("=" * 70)
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

# Step 3: 读取完整版代码
print(f"Step 3: 读取完整版代码...")
with open(COMPLETE_VERSION, 'r', encoding='utf-8') as f:
    complete_content = f.read()

complete_lines = complete_content.split('\n')

# 找到<style>和</style>之间的CSS
style_start = None
style_end = None
for i, line in enumerate(complete_lines):
    if '<style>' in line:
        style_start = i + 1
    elif '</style>' in line and style_start:
        style_end = i
        break

# 找到body内的HTML
body_start = None
body_end = None
for i, line in enumerate(complete_lines):
    if '<body>' in line:
        body_start = i + 1
    elif '</body>' in line and body_start:
        body_end = i
        break

if not (style_start and style_end and body_start and body_end):
    print("❌ 无法解析完整版代码")
    exit(1)

complete_css = complete_lines[style_start:style_end]
complete_html = complete_lines[body_start:body_end]

print(f"✅ 提取到完整版CSS: {len(complete_css)} 行")
print(f"✅ 提取到完整版HTML: {len(complete_html)} 行")
print()

# Step 4: 定位并删除第一个简版模块
print(f"Step 4: 查找简版模块位置...")

# 找CSS位置（搜索 .engineer-module {）
engineer_css_start = None
engineer_css_end = None
for i, line in enumerate(current_lines):
    if '.engineer-module {' in line and not engineer_css_start:
        engineer_css_start = i
    # 找到下一个模块的CSS作为结束标记
    if engineer_css_start and '.api-status-' in line:
        engineer_css_end = i
        break

# 找HTML位置（搜索 <!-- ========== 全栈工程师工作台 ========== -->）
engineer_html_start = None
engineer_html_end = None
for i, line in enumerate(current_lines):
    if '<!-- ========== 全栈工程师工作台 ========== -->' in line and not engineer_html_start:
        engineer_html_start = i
    # 找到 <!-- ========== 记忆空间模块 ========== --> 作为结束
    if engineer_html_start and '<!-- ========== 记忆空间模块 ========== -->' in line:
        engineer_html_end = i
        break

if not (engineer_css_start and engineer_html_start):
    print("❌ 无法定位简版模块")
    exit(1)

print(f"✅ 简版CSS位置: 第{engineer_css_start+1}-{engineer_css_end+1}行")
print(f"✅ 简版HTML位置: 第{engineer_html_start+1}-{engineer_html_end}行")
print()

# Step 5: 删除简版并插入完整版
print(f"Step 5: 删除简版，插入完整版...")

# 先删除CSS
new_lines = []
new_lines.extend(current_lines[:engineer_css_start])
new_lines.extend([line + '\n' for line in complete_css])
new_lines.append('\n')
new_lines.extend(current_lines[engineer_css_end:])

# 重新计算HTML位置（因为CSS行数变化）
css_diff = len(complete_css) + 1 - (engineer_css_end - engineer_css_start)
new_html_start = engineer_html_start + css_diff
new_html_end = engineer_html_end + css_diff

print(f"   CSS行数变化: {css_diff}")
print(f"   HTML新位置: 第{new_html_start+1}-{new_html_end}行")

# 删除简版HTML，插入完整版HTML
final_lines = []
final_lines.extend(new_lines[:new_html_start])
final_lines.extend([line + '\n' for line in complete_html])
final_lines.append('\n')
final_lines.extend(new_lines[new_html_end:])

print(f"✅ 替换完成")
print()

# Step 6: 查找并删除第二个重复的完整版（如果存在）
print(f"Step 6: 检查是否有重复的完整版模块...")

content_str = ''.join(final_lines)
if '<!-- ========== 全栈工程师工作台（完整版） ========== -->' in content_str:
    print(f"⚠️ 发现重复的完整版模块")
    
    # 找到重复模块的位置
    duplicate_start = None
    duplicate_end = None
    for i, line in enumerate(final_lines):
        if '<!-- ========== 全栈工程师工作台（完整版） ========== -->' in line:
            duplicate_start = i
        if duplicate_start and ('<!-- ========== Noah' in line or '<!-- ========== API' in line):
            duplicate_end = i
            break
    
    if duplicate_start and duplicate_end:
        print(f"   重复模块位置: 第{duplicate_start+1}-{duplicate_end}行")
        # 删除重复模块
        final_lines = final_lines[:duplicate_start] + final_lines[duplicate_end:]
        print(f"✅ 已删除重复模块")
    else:
        print(f"⚠️ 未找到重复模块结束位置，保留原样")
else:
    print(f"✅ 无重复模块")

print()

# Step 7: 写入文件
print(f"Step 7: 写入新文件...")
with open(CURRENT_FILE, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print(f"✅ 文件已更新")
print(f"   新文件共 {len(final_lines)} 行")
print(f"   总行数变化: {len(final_lines) - len(current_lines)}")
print()

print("=" * 70)
print("✅ 全栈工程师完整版替换完成！")
print("=" * 70)
print()
print("下一步:")
print("1. 重启服务器: kill -9 $(lsof -ti:8823) && python3 -m http.server 8823")
print("2. 访问新端口: http://localhost:8823/")
print("3. 检查全栈工程师模块是否显示完整版（5个Tab）")
print()

