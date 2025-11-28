#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接用行号替换全栈工程师模块
"""

import os
from datetime import datetime

# 配置
INDEX_HTML = "index.html"
FULLSTACK_COMPLETE = "../dashboard-test/fullstack-engineer-workbench-optimized.html"

# 行号配置（基于生成模块索引.py的输出）
OLD_MODULE_START = 8887  # 旧版开始（1-based）
OLD_MODULE_END = 11062   # 旧版结束（1-based）
DUPLICATE_START = 13285  # 重复完整版开始（1-based）
DUPLICATE_END = 15690    # 重复完整版结束（1-based）

def main():
    print("=" * 80)
    print("直接按行号替换全栈工程师模块")
    print("=" * 80)
    
    # 1. 备份
    print("\n[Step 1] 备份...")
    backup_file = f"index.html.backup-replace-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] 备份完成: {backup_file}")
    
    # 2. 读取完整版模块
    print("\n[Step 2] 读取完整版模块...")
    with open(FULLSTACK_COMPLETE, 'r', encoding='utf-8') as f:
        complete_content = f.read()
    
    # 提取body内容
    body_start = complete_content.find('<body>')
    body_end = complete_content.find('</body>')
    if body_start != -1 and body_end != -1:
        body_content = complete_content[body_start + 6:body_end].strip()
        print(f"[OK] 提取body内容: {len(body_content)} bytes")
    else:
        print("[WARN] 未找到body标签，使用全部内容")
        body_content = complete_content
    
    # 3. 读取当前HTML并分割成行
    print("\n[Step 3] 读取当前Dashboard...")
    lines = content.split('\n')
    total_lines = len(lines)
    print(f"[OK] 总行数: {total_lines}")
    
    # 4. 构建新内容
    print("\n[Step 4] 构建新内容...")
    print(f"   删除旧版: {OLD_MODULE_START}-{OLD_MODULE_END}行 ({OLD_MODULE_END - OLD_MODULE_START + 1}行)")
    print(f"   删除重复: {DUPLICATE_START}-{DUPLICATE_END}行 ({DUPLICATE_END - DUPLICATE_START + 1}行)")
    
    new_lines = []
    
    # 保留开头到旧模块之前
    new_lines.extend(lines[:OLD_MODULE_START-1])
    
    # 添加新模块注释和内容
    new_lines.append("")
    new_lines.append("        <!-- ========== 全栈工程师工作台（完整版 v2.0）========== -->")
    new_lines.append(f"        <!-- 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->")
    new_lines.append("        <!-- 包含: 5个Tab (事件流/任务看板/代码审查/技术文档/对话历史) -->")
    
    # 插入完整版body内容
    for line in body_content.split('\n'):
        new_lines.append(line)
    
    new_lines.append("        <!-- ========== /全栈工程师工作台 ========== -->")
    new_lines.append("")
    
    # 跳过旧模块，继续到重复模块之前
    new_lines.extend(lines[OLD_MODULE_END:DUPLICATE_START-1])
    
    # 跳过重复模块，继续到文件末尾
    new_lines.extend(lines[DUPLICATE_END:])
    
    new_line_count = len(new_lines)
    diff = new_line_count - total_lines
    
    print(f"[OK] 新内容构建完成")
    print(f"   原始行数: {total_lines}")
    print(f"   新行数: {new_line_count}")
    print(f"   差异: {diff:+d} 行")
    
    # 5. 写入文件
    print("\n[Step 5] 写入文件...")
    new_content = '\n'.join(new_lines)
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[OK] 已写入: {INDEX_HTML}")
    print(f"   文件大小: {len(new_content):,} bytes")
    
    print("\n" + "=" * 80)
    print("[SUCCESS] 替换完成!")
    print("=" * 80)
    print(f"\n备份文件: {backup_file}")
    print("\n下一步:")
    print("1. 启动服务器: python -m http.server 8810")
    print("2. 浏览器访问: http://localhost:8810/")
    print("3. Ctrl+Shift+R 强制刷新")
    print("=" * 80)

if __name__ == '__main__':
    main()

