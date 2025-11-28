#!/usr/bin/env python3
"""精确删除任务Tab系统（不删除全栈工程师）"""

def remove_tasks_precise():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 任务Tab系统：4438-4650行（在全栈工程师之前）
    # 索引：4437-4649
    start_line = 4437  # 第4438行
    end_line = 4649    # 第4650行
    
    print(f"原文件行数: {len(lines)}")
    print(f"删除范围: 第{start_line+1}行到第{end_line+1}行 ({end_line-start_line+1}行)")
    print(f"删除内容预览:")
    print(f"  开始: {lines[start_line][:60].strip()}")
    print(f"  结束: {lines[end_line][:60].strip()}")
    print(f"  下一行（应该是全栈工程师）: {lines[end_line+1][:60].strip()}")
    
    # 构建新文件
    new_lines = lines[:start_line] + ['\n'] + lines[end_line+1:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✅ 删除完成！")
    print(f"新文件行数: {len(new_lines)}")
    print(f"删除行数: {len(lines) - len(new_lines)}")
    
    return True

if __name__ == '__main__':
    remove_tasks_precise()

