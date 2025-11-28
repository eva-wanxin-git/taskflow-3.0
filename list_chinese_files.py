#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
列出所有中文文件名，帮助理解真实情况
"""

import os
import re

def list_chinese_files():
    """列出包含中文字符的文件"""
    
    print("📋 项目中的中文文件列表:\n")
    print("="*80)
    
    files = []
    for item in os.listdir('.'):
        # 跳过隐藏文件和目录
        if item.startswith('.') or os.path.isdir(item):
            continue
        
        # 检查是否包含中文字符
        if re.search(r'[\u4e00-\u9fff]', item) or any(c in item for c in ['✅', '📋', '🎉', '🎨', '📚', '🎯', '⚠️', '🔧', '🚀']):
            files.append(item)
    
    # 按类型分组
    reports = [f for f in files if '报告' in f or '总结' in f or 'REPORT' in f.upper()]
    guides = [f for f in files if '指南' in f or '说明' in f or 'GUIDE' in f.upper()]
    tasks = [f for f in files if 'REQ-' in f or 'TASK-' in f or 'INTEGRATE-' in f or '任务' in f]
    others = [f for f in files if f not in reports and f not in guides and f not in tasks]
    
    # 输出
    def print_category(title, items):
        if items:
            print(f"\n### {title} ({len(items)}个):\n")
            for i, item in enumerate(sorted(items), 1):
                print(f"{i:3}. {item}")
    
    print_category("📊 报告和总结", reports)
    print_category("📖 指南和说明", guides)
    print_category("📋 任务相关", tasks)
    print_category("📁 其他文件", others)
    
    print("\n" + "="*80)
    print(f"✅ 总共找到 {len(files)} 个中文文件")
    print("\n💡 提示: 这些文件名在文件系统中是正确存储的，只是在某些环境中显示为乱码")
    
    return files

if __name__ == "__main__":
    files = list_chinese_files()


