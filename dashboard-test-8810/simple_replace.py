#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单直接的替换 - 只做3件事：
1. 删除旧版（8887-11062行）
2. 删除重复版（13285-15690行）
3. 在8887位置插入完整版
"""

import sys
from datetime import datetime

def main():
    print("简单替换 - 直接操作")
    
    # 读取8810的index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"原始: {len(lines)} 行")
    
    # 读取完整版
    with open('../dashboard-test/fullstack-engineer-workbench-optimized.html', 'r', encoding='utf-8') as f:
        complete = f.read()
    
    # 提取body内容
    start = complete.find('<body>') + 6
    end = complete.find('</body>')
    body = complete[start:end].strip()
    
    # 备份
    backup = f"index.html.backup-simple-{datetime.now().strftime('%H%M%S')}"
    with open(backup, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"备份: {backup}")
    
    # 构建新内容
    new_lines = []
    
    # 1. 保留开头到8887之前
    new_lines.extend(lines[:8886])
    
    # 2. 插入注释和完整版
    new_lines.append('\n')
    new_lines.append('        <!-- ========== 全栈工程师工作台（完整版 v2.0）========== -->\n')
    new_lines.append(f'        <!-- 更新: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -->\n')
    new_lines.append(body)
    new_lines.append('\n        <!-- ========== /全栈工程师工作台 ========== -->\n')
    new_lines.append('\n')
    
    # 3. 跳过8887-11062，保留11063-13284
    new_lines.extend(lines[11062:13284])
    
    # 4. 跳过13285-15690，保留15691到末尾
    new_lines.extend(lines[15690:])
    
    print(f"新版: {len(new_lines)} 行")
    print(f"差异: {len(new_lines) - len(lines):+d} 行")
    
    # 写入
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("[OK] 完成!")
    print(f"备份: {backup}")

if __name__ == '__main__':
    main()

