#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard模块索引生成器
快速生成所有模块的行号范围，方便定位和修复
"""

import re
from datetime import datetime

def generate_module_index(html_file='index.html'):
    """生成模块索引"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找所有模块
    modules = []
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # 匹配模块注释
        if '<!-- ========' in line and '==========' in line:
            # 提取模块名称
            module_name = line.strip()
            module_name = module_name.replace('<!-- ', '').replace(' -->', '')
            module_name = module_name.replace('=', '').strip()
            
            if module_name and not module_name.startswith('版本') and module_name not in ['旧的对话模块（已删除，用上面的卡片替代）']:
                modules.append({
                    'name': module_name,
                    'start': line_num,
                    'comment_line': line.strip()
                })
        
        # 查找version-content的div（更精确）
        if 'version-content' in line and '<div' in line and 'data-version' in line:
            # 提取class名称
            class_match = re.search(r'class="([^"]+)"', line)
            if class_match:
                classes = class_match.group(1)
                # 找到主要的模块class
                for cls in classes.split():
                    if 'module' in cls and cls != 'version-content':
                        # 查找对应的注释
                        for j in range(max(0, i-5), i):
                            if '==========' in lines[j]:
                                module_name = lines[j].strip().replace('<!-- ', '').replace(' -->', '').replace('=', '').strip()
                                modules.append({
                                    'name': module_name,
                                    'start': line_num,
                                    'class': cls,
                                    'div_line': line.strip()[:80]
                                })
                                break
    
    # 去重并排序
    unique_modules = []
    seen_lines = set()
    
    for module in modules:
        if module['start'] not in seen_lines:
            seen_lines.add(module['start'])
            unique_modules.append(module)
    
    unique_modules.sort(key=lambda x: x['start'])
    
    # 计算每个模块的结束行（下一个模块的开始行-1）
    for i in range(len(unique_modules) - 1):
        unique_modules[i]['end'] = unique_modules[i + 1]['start'] - 1
        unique_modules[i]['lines'] = unique_modules[i]['end'] - unique_modules[i]['start'] + 1
    
    # 最后一个模块到文件结束
    if unique_modules:
        unique_modules[-1]['end'] = len(lines)
        unique_modules[-1]['lines'] = unique_modules[-1]['end'] - unique_modules[-1]['start'] + 1
    
    return unique_modules, len(lines)

def print_module_index(modules, total_lines):
    """打印模块索引"""
    
    print("=" * 100)
    print(" " * 30 + "Dashboard 模块索引地图")
    print(" " * 30 + f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 100)
    print()
    
    print(f"{'序号':<4} {'模块名称':<30} {'起始行':<8} {'结束行':<8} {'行数':<8} {'快速跳转'}")
    print("-" * 100)
    
    for i, module in enumerate(modules, 1):
        name = module['name'][:28]
        start = module['start']
        end = module.get('end', '?')
        lines = module.get('lines', '?')
        jump_cmd = f"Ctrl+G → {start}"
        
        print(f"{i:<4} {name:<30} {start:<8} {end:<8} {lines:<8} {jump_cmd}")
    
    print("-" * 100)
    print(f"{'总计':<4} {len(modules)} 个模块{' '*17} {'文件总行数':<8} {total_lines}")
    print()

def generate_bookmark_file(modules):
    """生成VSCode书签文件"""
    
    output = "# VSCode Bookmarks for Dashboard Modules\n\n"
    output += "## 使用方法\n"
    output += "1. 安装VSCode插件: Bookmarks (alefragnani.Bookmarks)\n"
    output += "2. 打开 index.html\n"
    output += "3. 按下面的行号，在每个位置按 Ctrl+Alt+K 添加书签\n"
    output += "4. 按 Ctrl+Alt+L 查看所有书签\n\n"
    output += "## 模块书签位置\n\n"
    
    for module in modules:
        output += f"- 第 {module['start']} 行: {module['name']}\n"
    
    with open('模块书签.md', 'w', encoding='utf-8') as f:
        f.write(output)
    
    print("[OK] Generated: 模块书签.md")

def generate_quick_jump_html(modules):
    """生成快速跳转HTML页面"""
    
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dashboard模块快速导航</title>
    <style>
        body { font-family: Consolas, monospace; padding: 40px; background: #f5f5f5; }
        h1 { color: #333; }
        .module-list { background: white; padding: 20px; border: 1px solid #ddd; }
        .module-item { padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }
        .module-item:hover { background: #f9f9f9; }
        .module-name { font-weight: bold; color: #0066cc; }
        .module-range { color: #666; font-size: 14px; }
        .module-cmd { color: #999; font-size: 12px; font-family: monospace; }
    </style>
</head>
<body>
    <h1>📍 Dashboard 模块快速导航</h1>
    <div class="module-list">
"""
    
    for i, module in enumerate(modules, 1):
        html += f"""
        <div class="module-item">
            <div>
                <span style="color: #999;">{i:02d}.</span>
                <span class="module-name">{module['name']}</span>
            </div>
            <div>
                <span class="module-range">第 {module['start']} - {module.get('end', '?')} 行 ({module.get('lines', '?')} 行)</span>
                <span class="module-cmd" style="margin-left: 20px;">VSCode: Ctrl+G → {module['start']}</span>
            </div>
        </div>
"""
    
    html += """
    </div>
    <p style="margin-top: 20px; color: #666;">
        💡 提示：点击复制行号，在VSCode中按 Ctrl+G 粘贴即可快速跳转
    </p>
</body>
</html>
"""
    
    with open('模块导航.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("[OK] Generated: 模块导航.html (Open in browser)")

if __name__ == '__main__':
    print()
    print(">>> Analyzing index.html...")
    print()
    
    modules, total_lines = generate_module_index()
    
    # 打印到控制台
    print_module_index(modules, total_lines)
    
    # 生成辅助文件
    generate_bookmark_file(modules)
    generate_quick_jump_html(modules)
    
    print()
    print("=" * 100)
    print("Usage:")
    print("   1. Check console output - Quick overview")
    print("   2. Open module-nav.html - Visual navigation in browser")
    print("   3. Refer to module-bookmarks.md - Add bookmarks in VSCode")
    print("=" * 100)
    print()

