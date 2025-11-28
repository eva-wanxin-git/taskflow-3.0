#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
替换全栈工程师模块 - 修复编码问题
严格使用UTF-8编码处理所有文件
"""

import os
from datetime import datetime

def main():
    print("=" * 80)
    print("替换全栈工程师模块（UTF-8编码）")
    print("=" * 80)
    
    INDEX_HTML = "index.html"
    FULLSTACK_COMPLETE = "../dashboard-test/fullstack-engineer-workbench-optimized.html"
    
    # 行号配置
    OLD_MODULE_START = 8887
    OLD_MODULE_END = 11062
    DUPLICATE_START = 13285
    DUPLICATE_END = 15690
    
    # 1. 备份
    print("\n[Step 1] 备份...")
    backup_file = f"index.html.backup-utf8-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        original_content = f.read()
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(original_content)
    print(f"[OK] 备份: {backup_file}")
    
    # 2. 读取完整版模块（UTF-8）
    print("\n[Step 2] 读取完整版模块...")
    with open(FULLSTACK_COMPLETE, 'r', encoding='utf-8') as f:
        complete_html = f.read()
    
    # 提取body内容（保持UTF-8）
    body_start_tag = '<body>'
    body_end_tag = '</body>'
    
    start_idx = complete_html.find(body_start_tag)
    end_idx = complete_html.find(body_end_tag)
    
    if start_idx != -1 and end_idx != -1:
        # 提取body标签之间的内容
        body_content = complete_html[start_idx + len(body_start_tag):end_idx]
        # 去掉前后空白行
        body_lines = body_content.split('\n')
        # 去掉开头和结尾的空行
        while body_lines and not body_lines[0].strip():
            body_lines.pop(0)
        while body_lines and not body_lines[-1].strip():
            body_lines.pop()
        body_content = '\n'.join(body_lines)
        print(f"[OK] 提取body内容: {len(body_content)} bytes")
    else:
        print("[ERROR] 无法找到body标签")
        return
    
    # 3. 分割原始HTML为行
    print("\n[Step 3] 处理原始HTML...")
    original_lines = original_content.split('\n')
    print(f"[OK] 原始行数: {len(original_lines)}")
    
    # 4. 构建新内容
    print("\n[Step 4] 构建新内容...")
    new_lines = []
    
    # 保留开头到旧模块之前
    new_lines.extend(original_lines[:OLD_MODULE_START-1])
    
    # 添加新模块标记和内容
    new_lines.append("")
    new_lines.append("        <!-- ========== 全栈工程师工作台（完整版 v2.0）========== -->")
    new_lines.append(f"        <!-- 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->")
    
    # 添加body内容（逐行添加，保持缩进）
    for line in body_content.split('\n'):
        new_lines.append(line)
    
    new_lines.append("        <!-- ========== /全栈工程师工作台 ========== -->")
    new_lines.append("")
    
    # 跳过旧模块，保留到重复模块之前的内容
    new_lines.extend(original_lines[OLD_MODULE_END:DUPLICATE_START-1])
    
    # 跳过重复模块，保留到文件末尾
    new_lines.extend(original_lines[DUPLICATE_END:])
    
    print(f"[OK] 新行数: {len(new_lines)}")
    print(f"   差异: {len(new_lines) - len(original_lines):+d} 行")
    
    # 5. 写入文件（UTF-8）
    print("\n[Step 5] 写入文件...")
    new_content = '\n'.join(new_lines)
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[OK] 已写入: {INDEX_HTML}")
    print(f"   文件大小: {len(new_content):,} bytes")
    
    # 6. 验证中文
    print("\n[Step 6] 验证中文内容...")
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        verify_lines = f.readlines()
    
    # 检查全栈工程师模块的标题
    for i in range(OLD_MODULE_START-1, min(OLD_MODULE_START+20, len(verify_lines))):
        if '全栈工程师' in verify_lines[i]:
            print(f"[OK] 第{i+1}行: {verify_lines[i].strip()[:50]}...")
            break
    
    print("\n" + "=" * 80)
    print("[SUCCESS] 替换完成!")
    print("=" * 80)
    print(f"\n备份: {backup_file}")
    print("\n下一步:")
    print("1. 重启服务器（如果需要）")
    print("2. 访问 http://localhost:8810/")
    print("3. Ctrl+Shift+R 强制刷新")
    print("=" * 80)

if __name__ == '__main__':
    main()

