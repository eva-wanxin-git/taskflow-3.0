#!/usr/bin/env python3
"""删除项目切换器和任务Tab系统"""

def remove_modules():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"原文件行数: {len(lines)}")
    
    # 第一段：删除项目切换器（3473-3479行，索引3472-3478）
    switcher_start = 3472  # 第3473行
    switcher_end = 3479    # 第3480行
    
    # 第二段：删除任务Tab系统（4439-4987行，但要考虑第一段删除后的偏移）
    # 第一段删除了7行，所以第二段的索引需要减7
    tasks_start = 4438 - 7  # 第4439行，但已经删除7行
    tasks_end = 4986 - 7    # 第4987行之前
    
    # 先删除项目切换器
    temp_lines = lines[:switcher_start] + lines[switcher_end:]
    
    print(f"第一段删除: 第{switcher_start+1}行到第{switcher_end}行 ({switcher_end-switcher_start}行)")
    print(f"临时行数: {len(temp_lines)}")
    
    # 再删除任务Tab系统
    new_lines = temp_lines[:tasks_start] + ['\n'] + temp_lines[tasks_end+1:]
    
    print(f"第二段删除: 第{tasks_start+1}行到第{tasks_end+1}行（调整后索引）")
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✅ 删除完成！")
    print(f"新文件行数: {len(new_lines)}")
    print(f"总删除行数: {len(lines) - len(new_lines)}")
    
    return True

if __name__ == '__main__':
    remove_modules()

