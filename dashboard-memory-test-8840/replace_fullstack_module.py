#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全栈工程师完整版模块替换脚本
自动替换简化版并删除旧完整版
"""

import re
import sys
from pathlib import Path

# 设置Windows命令行编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_module_from_complete_html(html_content):
    """从完整的HTML中提取模块部分（body中的内容，不包括html/head/body标签）"""
    # 提取 body 标签内的所有内容
    body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
    if body_match:
        body_content = body_match.group(1).strip()
        # 返回 body 中的内容
        return body_content
    return None

def replace_fullstack_module():
    """执行模块替换"""
    
    # 文件路径
    index_file = Path('index.html')
    
    if not index_file.exists():
        print("❌ 错误：index.html 文件不存在")
        return False
    
    print("📖 读取 index.html...")
    with open(index_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    print(f"✅ 文件读取成功，共 {total_lines} 行")
    
    # 定位简化版（行号从1开始，但列表索引从0开始）
    simple_start = 8886  # 第8887行的索引
    simple_end = 11060   # 第11061行的索引
    
    # 定位完整版
    complete_start = 13284  # 第13285行的索引
    complete_end = 15688    # 第15689行的索引
    
    print(f"\n📍 定位模块位置:")
    print(f"  简化版: 第{simple_start+1}-{simple_end+1}行")
    print(f"  完整版: 第{complete_start+1}-{complete_end+1}行")
    
    # 验证标记
    simple_marker = lines[simple_start].strip()
    complete_marker = lines[complete_start].strip()
    
    print(f"\n🔍 验证标记:")
    print(f"  简化版标记: {simple_marker[:60]}...")
    print(f"  完整版标记: {complete_marker[:60]}...")
    
    # 使用已有的完整版模块（从第13285-15689行）
    print(f"📦 提取完整版模块...")
    complete_module_lines = lines[complete_start:complete_end+1]
    new_module_content = ''.join(complete_module_lines)
    
    print(f"\n🔄 执行替换...")
    
    # 构建新的文件内容
    # 1. 保留简化版之前的内容
    new_lines = lines[:simple_start]
    
    # 2. 添加新的完整版模块
    new_lines.append(new_module_content)
    
    # 3. 跳过简化版，保留到完整版之前的内容
    new_lines.extend(lines[simple_end+1:complete_start])
    
    # 4. 跳过旧的完整版，添加之后的内容
    new_lines.extend(lines[complete_end+1:])
    
    # 保存新文件
    print(f"💾 保存文件...")
    with open(index_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    new_total = len(new_lines)
    removed_lines = total_lines - new_total
    
    print(f"\n✅ 替换完成！")
    print(f"  原文件: {total_lines} 行")
    print(f"  新文件: {new_total} 行")
    print(f"  删除了: {removed_lines} 行")
    print(f"\n📋 变更摘要:")
    print(f"  ✓ 删除简化版 (第{simple_start+1}-{simple_end+1}行)")
    print(f"  ✓ 删除旧完整版 (第{complete_start+1}-{complete_end+1}行)")
    print(f"  ✓ 插入新完整版 (在第{simple_start+1}行位置)")
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("全栈工程师完整版模块替换脚本")
    print("=" * 60)
    
    success = replace_fullstack_module()
    
    if success:
        print("\n🎉 部署成功！")
        print("\n下一步:")
        print("  1. 运行: python check_balance.py")
        print("  2. 重启: python -m http.server 8822")
        print("  3. 访问: http://localhost:8822/")
    else:
        print("\n❌ 部署失败，请检查错误信息")

