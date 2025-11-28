#!/usr/bin/env python3
"""删除全栈工程师模块后面的旧模块"""

def cleanup_modules():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 删除范围：4988行到5990行（索引4987-5989）
    start_line = 4987  # 第4988行（"<!-- ========== 事件模块 =========="）
    end_line = 5989    # 第5990行之前（运维工程师模块开始前的空行）
    
    print(f"原文件行数: {len(lines)}")
    print(f"删除范围: 第{start_line+1}行到第{end_line+1}行 ({end_line-start_line+1}行)")
    print(f"删除内容预览:")
    print(f"  开始: {lines[start_line][:60]}")
    print(f"  结束: {lines[end_line][:60]}")
    
    # 构建新文件
    new_lines = lines[:start_line]
    new_lines.append('\n')
    new_lines.extend(lines[end_line+1:])
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✅ 删除完成！")
    print(f"新文件行数: {len(new_lines)}")
    print(f"删除行数: {len(lines) - len(new_lines)}")
    
    return True

if __name__ == '__main__':
    cleanup_modules()

