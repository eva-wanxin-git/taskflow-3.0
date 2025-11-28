#!/usr/bin/env python3
"""删除项目记忆库模块"""

def remove_memory_lib():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 删除项目记忆库模块：5141-5285行（索引5140-5284）
    start_line = 5140  # 第5141行，索引5140
    end_line = 5284    # 第5285行，索引5284
    
    print(f"原文件行数: {len(lines)}")
    print(f"删除范围: 第{start_line+1}行到第{end_line+1}行 ({end_line-start_line+1}行)")
    print(f"删除内容预览:")
    print(f"  开始: {lines[start_line][:60]}")
    print(f"  结束: {lines[end_line][:60]}")
    
    # 构建新文件
    new_lines = lines[:start_line] + ['\n'] + lines[end_line+1:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✅ 删除完成！")
    print(f"新文件行数: {len(new_lines)}")
    print(f"删除行数: {len(lines) - len(new_lines)}")
    
    return True

if __name__ == '__main__':
    remove_memory_lib()

