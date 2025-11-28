# -*- coding: utf-8 -*-
"""
新增完整版全栈工程师模块到Dashboard
安全插入，不影响现有模块
"""

import re
from datetime import datetime

def read_source_html():
    """读取源文件（完整的全栈工程师模块）"""
    with open('../dashboard-test/全栈工程师模块完整代码.txt', 'r', encoding='utf-8') as f:
        return f.read()

def extract_sections(html_content):
    """提取CSS、HTML body和JavaScript三个部分"""
    
    # 提取CSS
    css_match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
    css = css_match.group(1) if css_match else ''
    
    # 提取body内容
    body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
    body = body_match.group(1) if body_match else ''
    
    # 提取JavaScript
    js_match = re.search(r'<script>(.*?)</script>', html_content, re.DOTALL)
    js = js_match.group(1) if js_match else ''
    
    return css, body, js

def modify_css(css):
    """修改CSS，添加唯一前缀避免冲突"""
    
    # 添加模块前缀注释
    modified_css = "\n        /* ==================== 全栈工程师模块（完整版） ==================== */\n"
    
    # 不修改:root变量（已经存在）
    # 移除body样式（已经存在）
    css = re.sub(r'body\s*\{[^}]*\}', '', css)
    
    # 移除:root定义（已存在）
    css = re.sub(r':root\s*\{[^}]*\}', '', css)
    
    # 移除全局重置（已存在）
    css = re.sub(r'\*\s*\{[^}]*\}', '', css)
    
    # 将.engineer-module改为.fullstack-complete-module
    css = css.replace('.engineer-module', '.fullstack-complete-module')
    
    # 将其他通用类名添加父级选择器
    generic_classes = [
        '.module-header', '.header-row', '.module-title', '.status-badge', 
        '.status-dot', '.engineer-info', '.info-section', '.engineer-avatar',
        '.engineer-details', '.engineer-name', '.engineer-meta', '.quick-stats',
        '.stat-item', '.stat-value', '.stat-label', '.tab-navigation', 
        '.tab-item', '.tab-badge', '.tab-content-wrapper', '.tab-pane',
        '.event-timeline', '.timeline-filters', '.filter-chip', '.timeline-item',
        '.timeline-marker', '.event-card', '.event-header', '.event-title',
        '.event-meta', '.event-time', '.event-description', '.event-tags',
        '.event-tag', '.task-board-container', '.task-board-header', 
        '.filter-bar', '.filter-chips', '.sort-select', '.kanban-board',
        '.kanban-column', '.column-header', '.column-title', '.column-count',
        '.column-cards', '.task-card', '.task-card-header', '.task-id',
        '.task-title', '.task-status-badge', '.task-description', '.task-meta',
        '.task-estimate', '.priority-badge', '.task-assignee', '.assignee-avatar',
        '.task-actions', '.task-action-button', '.code-review-container',
        '.code-review-timeline', '.review-filters', '.review-item', 
        '.review-marker', '.review-card', '.review-card-header', '.review-title',
        '.review-meta', '.review-status', '.review-content', '.content-label',
        '.content-list', '.content-item', '.review-comment', '.review-actions',
        '.review-action-button', '.docs-container', '.docs-sidebar', 
        '.docs-search', '.docs-categories', '.category-group', '.category-header',
        '.category-items', '.doc-item', '.docs-content', '.doc-header',
        '.doc-title', '.doc-meta', '.doc-body', '.doc-section', 
        '.doc-section-title', '.doc-section-content', '.doc-code-block',
        '.conversation-layout', '.conversation-list', '.conversation-search',
        '.search-input', '.conversation-items', '.conversation-item',
        '.conversation-item-header', '.conversation-item-title', 
        '.conversation-item-time', '.conversation-item-preview', 
        '.conversation-item-meta', '.conversation-detail', '.detail-header',
        '.detail-title', '.detail-meta', '.messages-container', '.message',
        '.message-avatar', '.message-content', '.message-header', 
        '.message-sender', '.message-time', '.message-text'
    ]
    
    for class_name in generic_classes:
        # 添加父级选择器
        css = re.sub(
            r'(' + re.escape(class_name) + r')(\s*[,{])',
            r'.fullstack-complete-module \1\2',
            css
        )
    
    modified_css += css
    
    return modified_css

def modify_html(html_body):
    """修改HTML，添加唯一ID和class前缀"""
    
    # 找到engineer-module div，改为fullstack-complete-module
    html_body = html_body.replace('class="engineer-module"', 
                                   'class="fullstack-complete-module version-content" data-version="1"')
    
    # 修改所有ID，添加fc-前缀（fullstack-complete）
    id_mappings = {
        'events': 'fc-events',
        'taskboard': 'fc-taskboard',
        'reviews': 'fc-reviews',
        'docs': 'fc-docs',
        'conversations': 'fc-conversations'
    }
    
    for old_id, new_id in id_mappings.items():
        html_body = re.sub(
            rf'id="{old_id}"',
            f'id="{new_id}"',
            html_body
        )
    
    # 修改onclick函数调用
    function_mappings = {
        'switchTab': 'switchFullstackCompleteTab',
        'copyPrompt': 'copyFullstackPrompt',
        'selectConversation': 'selectFullstackConversation',
        'toggleCategory': 'toggleFullstackCategory',
        'selectDoc': 'selectFullstackDoc'
    }
    
    for old_func, new_func in function_mappings.items():
        html_body = html_body.replace(
            f'onclick="{old_func}(',
            f'onclick="{new_func}('
        )
    
    # 在onclick中的Tab名称添加fc-前缀
    for old_id in ['events', 'taskboard', 'reviews', 'docs', 'conversations']:
        html_body = html_body.replace(
            f"'{old_id}'",
            f"'fc-{old_id}'"
        )
    
    # 添加模块注释
    modified_html = f"\n    <!-- ========== 全栈工程师工作台（完整版） ========== -->\n{html_body}"
    
    return modified_html

def modify_javascript(js):
    """修改JavaScript，重命名所有函数"""
    
    # 添加注释
    modified_js = "\n        // ========== 全栈工程师模块（完整版）函数 ==========\n"
    
    # 重命名函数定义
    js = js.replace('function switchTab(', 'function switchFullstackCompleteTab(')
    js = js.replace('function copyPrompt(', 'function copyFullstackPrompt(')
    js = js.replace('function selectConversation(', 'function selectFullstackConversation(')
    js = js.replace('function toggleCategory(', 'function toggleFullstackCategory(')
    js = js.replace('function selectDoc(', 'function selectFullstackDoc(')
    
    # 修改选择器，添加作用域
    js = js.replace("querySelectorAll('.tab-item')", 
                    "querySelectorAll('.fullstack-complete-module .tab-item')")
    js = js.replace("querySelectorAll('.tab-pane')", 
                    "querySelectorAll('.fullstack-complete-module .tab-pane')")
    js = js.replace("querySelectorAll('.conversation-item')", 
                    "querySelectorAll('.fullstack-complete-module .conversation-item')")
    js = js.replace("querySelectorAll('.doc-item')", 
                    "querySelectorAll('.fullstack-complete-module .doc-item')")
    
    # 修改querySelector
    js = js.replace("querySelector('.code-manager-module", 
                    "querySelector('.fullstack-complete-module")
    
    modified_js += js
    
    return modified_js

def insert_into_dashboard():
    """将修改后的内容插入到Dashboard主文件"""
    
    print("1. 读取源文件...")
    source_html = read_source_html()
    
    print("2. 提取三个部分...")
    css, html_body, js = extract_sections(source_html)
    
    print("3. 修改CSS...")
    modified_css = modify_css(css)
    
    print("4. 修改HTML...")
    modified_html = modify_html(html_body)
    
    print("5. 修改JavaScript...")
    modified_js = modify_javascript(js)
    
    print("6. 读取Dashboard主文件...")
    with open('index.html', 'r', encoding='utf-8') as f:
        dashboard_content = f.read()
    
    print("7. 查找插入位置...")
    
    # 在CSS中，找到Noah模块后面插入
    css_insert_marker = "/* ==================== Noah AI代码管家模块 ==================== */"
    css_insert_pos = dashboard_content.find(css_insert_marker)
    
    if css_insert_pos == -1:
        print("❌ 错误：找不到CSS插入位置")
        return False
    
    # 找到Noah模块CSS的结束位置（下一个模块或</style>）
    css_end_pos = dashboard_content.find("</style>", css_insert_pos)
    
    # 在Noah CSS结束前插入新CSS
    dashboard_content = (
        dashboard_content[:css_end_pos] + 
        modified_css + 
        "\n" +
        dashboard_content[css_end_pos:]
    )
    
    # 在HTML中，找到Noah模块后面、<script>标签前插入
    html_insert_marker = "<!-- ========== Noah AI代码管家模块 ========== -->"
    html_insert_pos = dashboard_content.find(html_insert_marker)
    
    if html_insert_pos == -1:
        print("❌ 错误：找不到HTML插入位置")
        return False
    
    # 找到Noah模块HTML的结束位置（找到</div>后再找<script>）
    script_pos = dashboard_content.find("<script>", html_insert_pos)
    
    # 在<script>前插入新HTML
    dashboard_content = (
        dashboard_content[:script_pos] + 
        modified_html + 
        "\n\n" +
        dashboard_content[script_pos:]
    )
    
    # 在JavaScript中，找到Noah函数后面、</script>前插入
    js_insert_marker = "// ========== Noah AI代码管家模块函数 =========="
    js_insert_pos = dashboard_content.find(js_insert_marker)
    
    if js_insert_pos == -1:
        print("❌ 错误：找不到JavaScript插入位置")
        return False
    
    # 找到</script>
    script_end_pos = dashboard_content.find("</script>", js_insert_pos)
    
    # 在</script>前插入新JavaScript
    dashboard_content = (
        dashboard_content[:script_end_pos] + 
        modified_js + 
        "\n" +
        dashboard_content[script_end_pos:]
    )
    
    print("8. 写入文件...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_content)
    
    print("✅ 完成！新模块已成功插入")
    return True

if __name__ == '__main__':
    try:
        success = insert_into_dashboard()
        if success:
            print("\n" + "="*60)
            print("✅ 全栈工程师完整版模块已成功添加到Dashboard")
            print("="*60)
            print("\n访问地址: http://localhost:8820/")
            print("模块名称: 全栈工程师工作台（完整版）")
            print("位置: Noah模块之后")
            print("\n请重启服务器并强制刷新浏览器（Ctrl+Shift+R）")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

