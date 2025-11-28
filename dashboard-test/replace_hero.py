#!/usr/bin/env python3
"""替换Hero区HTML"""

def replace_hero():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open('new_hero_html.txt', 'r', encoding='utf-8') as f:
        new_hero = f.read()
    
    # 找到<body>标签
    body_line = None
    for i, line in enumerate(lines):
        if '<body>' in line:
            body_line = i
            break
    
    # 找到<!-- 主容器 -->或者<main class="main-container">
    main_line = None
    for i in range(body_line, len(lines)):
        if '<main class="main-container">' in lines[i]:
            main_line = i
            break
    
    if body_line is None or main_line is None:
        print("❌ 未找到<body>或<main>标签")
        return False
    
    print(f"原文件行数: {len(lines)}")
    print(f"找到<body>在第{body_line+1}行")
    print(f"找到<main>在第{main_line+1}行")
    print(f"替换范围: {main_line - body_line}行")
    
    # 构建新文件
    new_lines = lines[:body_line]
    new_lines.append(new_hero)
    if not new_hero.endswith('\n'):
        new_lines.append('\n')
    new_lines.extend(lines[main_line:])
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✅ 替换完成！")
    print(f"新文件行数: {len(new_lines)}")
    print(f"行数变化: {len(new_lines) - len(lines):+d}")
    
    return True

if __name__ == '__main__':
    replace_hero()

