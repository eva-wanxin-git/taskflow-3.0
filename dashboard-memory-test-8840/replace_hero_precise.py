#!/usr/bin/env python3
"""精确替换Hero区HTML（保留JavaScript）"""

def replace_hero_precise():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open('new_hero_html.txt', 'r', encoding='utf-8') as f:
        new_hero = f.read()
    
    # 精确位置：3474行（顶部品牌栏注释）到3521行（</main>之前）
    # 索引：3473到3520
    start_line = 3473  # 第3474行，索引3473
    end_line = 3520    # 第3521行，索引3520
    
    print(f"原文件行数: {len(lines)}")
    print(f"替换范围: 第{start_line+1}行到第{end_line+1}行 ({end_line-start_line+1}行)")
    print(f"开始行内容: {lines[start_line][:60]}")
    print(f"结束行内容: {lines[end_line][:60]}")
    
    # 构建新文件
    new_lines = lines[:start_line]
    new_lines.append(new_hero)
    if not new_hero.endswith('\n'):
        new_lines.append('\n')
    new_lines.extend(lines[end_line+1:])
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✅ 替换完成！")
    print(f"新文件行数: {len(new_lines)}")
    print(f"行数变化: {len(new_lines) - len(lines):+d}")
    
    return True

if __name__ == '__main__':
    replace_hero_precise()

