#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除重复的Noah模块片段
第10018-13086行之间是重复/错误的内容，需要全部删除
"""

import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def remove_duplicate_noah():
    """删除重复的Noah模块内容"""
    
    print("=" * 60)
    print("删除重复Noah模块片段")
    print("=" * 60)
    
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    print(f"\n📖 原文件: {total_lines} 行")
    
    # 要删除的范围（行号从1开始，但索引从0开始）
    delete_start = 10017  # 第10018行的索引
    delete_end = 13085    # 第13086行的索引
    
    print(f"🗑️  删除范围: 第{delete_start+1}-{delete_end+1}行")
    print(f"📊 删除行数: {delete_end - delete_start + 1} 行")
    
    # 构建新文件
    new_lines = lines[:delete_start] + lines[delete_end+1:]
    
    # 保存
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    new_total = len(new_lines)
    deleted = total_lines - new_total
    
    print(f"\n✅ 删除完成！")
    print(f"  原文件: {total_lines} 行")
    print(f"  新文件: {new_total} 行")
    print(f"  删除了: {deleted} 行")
    
    return True

if __name__ == '__main__':
    success = remove_duplicate_noah()
    
    if success:
        print("\n🎉 成功！")
        print("\n下一步:")
        print("  1. 重启服务器: python -m http.server 8822")
        print("  2. 强制刷新浏览器: Ctrl + Shift + R")
        print("  3. 验证Noah模块显示是否正常")

