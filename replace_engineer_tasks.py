#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
替换全栈工程师任务看板Tab的内容
将硬编码任务替换为数据库中的真实75个任务
"""
from pathlib import Path
import re

# 读取生成的任务列表HTML
tasks_html_file = Path(__file__).parent / "all_tasks_list.html"
with open(tasks_html_file, 'r', encoding='utf-8') as f:
    tasks_html = f.read()

print("=" * 70)
print("替换全栈工程师任务看板")
print("=" * 70)
print(f"读取任务HTML: {len(tasks_html)} 字符")
print()

# 读取原始HTML
index_file = Path(__file__).parent / "dashboard-test" / "index.html"
with open(index_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

print(f"读取index.html: {len(html_content)} 字符")
print()

# 备份
backup_file = index_file.parent / f"index.html.backup-before-engineer-tasks-fix-{Path(__file__).stem}"
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"已备份: {backup_file.name}")
print()

# 查找替换位置
# 找到：<div id="engineer-tasks" class="engineer-tab-pane active">
#      <div class="engineer-list">
#      ...所有的engineer-list-item...
#      </div>
#      </div>
# 替换为新的engineer-list-item列表

# 使用正则查找
pattern = r'(<div id="engineer-tasks" class="engineer-tab-pane active">\s*<div class="engineer-list">)(.*?)(</div>\s*</div>\s*<!-- Tab 3:)'

match = re.search(pattern, html_content, re.DOTALL)

if match:
    print("找到任务看板Tab位置")
    old_content = match.group(2)
    print(f"  旧内容长度: {len(old_content)} 字符")
    
    # 替换
    new_html = html_content[:match.start(2)] + '\n' + tasks_html + '\n' + html_content[match.end(2):]
    
    # 写回
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"  新内容长度: {len(tasks_html)} 字符")
    print()
    print("✅ 替换完成！")
    print()
    print("验证:")
    print(f"  原文件: {len(html_content)} 字符")
    print(f"  新文件: {len(new_html)} 字符")
    print(f"  差异: {len(new_html) - len(html_content):+d} 字符")
else:
    print("❌ 未找到匹配位置")
    print("尝试另一种方式...")
    
    # 方式2: 简单查找
    start_marker = '<div id="engineer-tasks" class="engineer-tab-pane active">'
    start_pos = html_content.find(start_marker)
    
    if start_pos > 0:
        print(f"找到起始位置: 行 {html_content[:start_pos].count(chr(10))}")
        # 找engineer-list的开始和结束
        list_start = html_content.find('<div class="engineer-list">', start_pos)
        # 找下一个Tab或这个div的结束
        next_tab_start = html_content.find('<!-- Tab 3:', list_start)
        
        if list_start > 0 and next_tab_start > list_start:
            # 找到engineer-list结束位置（在next_tab_start之前的</div></div>）
            list_end = html_content.rfind('</div>', list_start, next_tab_start)
            list_end = html_content.rfind('</div>', list_start, list_end)  # 再往前找一个
            
            print(f"engineer-list 范围: {list_start} - {list_end}")
            
            # 构造新内容
            new_section = f'''<div class="engineer-list">
{tasks_html}
                    </div>'''
            
            # 替换
            new_html = html_content[:list_start] + new_section + html_content[list_end + 6:]
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            print("✅ 替换完成（方式2）")
    else:
        print("❌ 完全找不到位置")

print()
print("=" * 70)
print("刷新浏览器: Ctrl+Shift+R")
print("访问: http://localhost:8820")
print("=" * 70)

