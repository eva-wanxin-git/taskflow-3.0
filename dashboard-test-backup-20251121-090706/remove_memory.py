#!/usr/bin/env python3
"""删除记忆空间模块"""

def remove_memory_module():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 删除记忆空间模块：5030-5168行（索引5029-5167）
    # 还要删除前面的空行5169
    start_line = 5029  # 第5030行，索引5029
    end_line = 5168    # 第5169行（空行），索引5168
    
    print(f"原文件行数: {len(lines)}")
    print(f"删除范围: 第{start_line+1}行到第{end_line+1}行 ({end_line-start_line+1}行)")
    print(f"删除内容预览:")
    print(f"  开始: {lines[start_line][:60]}")
    print(f"  结束: {lines[end_line][:60]}")
    
    # 构建新文件
    new_lines = lines[:start_line] + lines[end_line+1:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✅ 删除完成！")
    print(f"新文件行数: {len(new_lines)}")
    print(f"删除行数: {len(lines) - len(new_lines)}")
    
    return True

if __name__ == '__main__':
    remove_memory_module()

