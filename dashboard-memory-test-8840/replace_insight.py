#!/usr/bin/env python3
"""替换项目透视模块"""

def replace_insight_module():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open('new_insight_module.html', 'r', encoding='utf-8') as f:
        new_module = f.read()
    
    # 从2918行到3450行（索引2917-3449）
    start_line = 2918  # 第2919行，索引2918
    end_line = 3449    # 第3450行，索引3449
    
    print(f"原文件行数: {len(lines)}")
    print(f"删除范围: 第{start_line+1}行到第{end_line+1}行 ({end_line-start_line+1}行)")
    
    # 构建新文件
    new_lines = lines[:start_line]
    new_lines.append(new_module)
    if not new_module.endswith('\n'):
        new_lines.append('\n')
    new_lines.extend(lines[end_line+1:])
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✅ 替换完成！")
    print(f"新文件行数: {len(new_lines)}")
    print(f"行数变化: {len(new_lines) - len(lines):+d}")
    
    return True

if __name__ == '__main__':
    replace_insight_module()

