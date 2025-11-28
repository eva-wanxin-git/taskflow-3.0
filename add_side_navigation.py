#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加左侧固定导航栏
实现快速定位到各个模块
"""

import os
import re
from datetime import datetime

def add_side_navigation():
    """添加左侧固定导航栏"""
    
    # 文件路径
    html_file = "dashboard-test-8826/index.html"
    
    if not os.path.exists(html_file):
        print(f"❌ 文件不存在: {html_file}")
        return False
    
    print("="*80)
    print("🔧 添加左侧固定导航栏")
    print("="*80)
    print()
    
    # 备份
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = f"{html_file}.backup-side-nav-{timestamp}"
    
    print(f"📋 备份原文件...")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✅ 已备份到: {backup_file}")
    print()
    
    # 定义模块列表（按照页面顺序）
    modules = [
        {"name": "项目透视塔", "id": "module-project-view", "icon": "🏗️"},
        {"name": "待开发任务池", "id": "module-pending-tasks", "icon": "📋"},
        {"name": "架构师工作台", "id": "module-architect", "icon": "🎯"},
        {"name": "全栈工程师", "id": "module-fullstack", "icon": "💻"},
        {"name": "实时脉动", "id": "module-pulse", "icon": "⚡"},
        {"name": "运维工程师", "id": "module-devops", "icon": "🔧"},
        {"name": "Noah代码管家", "id": "module-noah", "icon": "🤖"},
    ]
    
    print("📍 步骤1: 为模块添加ID标识...")
    
    # 为每个模块添加ID
    id_mapping = {
        '项目透视塔': '<div class="page-container version-content" data-version="1">',
        '待开发任务池': '<div class="pending-features-module">',
        '架构师工作台': '<div class="architect-module">',
        '全栈工程师': '<div class="engineer-module">',
        '实时脉动': '<div class="pulse-module">',
        '运维工程师': '<div class="devops-module">',
        'Noah代码管家': '<div class="code-manager-module">',
    }
    
    for module in modules:
        old_pattern = id_mapping[module['name']]
        # 添加id属性
        new_pattern = old_pattern.replace('>', f' id="{module["id"]}">', 1)
        
        # 只替换第一个匹配（避免替换多个相同class的div）
        count = content.count(old_pattern)
        if count > 0:
            content = content.replace(old_pattern, new_pattern, 1)
            print(f"   ✅ {module['name']}: 已添加ID")
        else:
            print(f"   ⚠️  {module['name']}: 未找到匹配")
    
    print()
    print("📍 步骤2: 创建导航栏CSS...")
    
    # CSS样式
    nav_css = """
        /* ========== 左侧固定导航栏 ========== */
        .side-navigation {
            position: fixed;
            left: 24px;
            top: 120px;
            width: 200px;
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            border-radius: 12px;
            padding: 16px 12px;
            box-shadow: var(--shadow-md);
            z-index: 1000;
            max-height: calc(100vh - 180px);
            overflow-y: auto;
        }

        .side-nav-header {
            font-size: 12px;
            font-weight: var(--weight-semibold);
            color: var(--noir-silver);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            padding: 0 8px;
        }

        .side-nav-list {
            list-style: none;
            margin: 0;
            padding: 0;
        }

        .side-nav-item {
            margin-bottom: 4px;
        }

        .side-nav-link {
            display: flex;
            align-items: center;
            padding: 8px 12px;
            border-radius: 8px;
            text-decoration: none;
            color: var(--noir-graphite);
            font-size: 14px;
            font-weight: var(--weight-regular);
            transition: all var(--duration-fast) var(--ease-luxury);
            cursor: pointer;
        }

        .side-nav-link:hover {
            background: var(--blanc-silk);
            color: var(--noir-ink);
            transform: translateX(2px);
        }

        .side-nav-link.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: var(--weight-medium);
        }

        .side-nav-icon {
            margin-right: 8px;
            font-size: 16px;
            opacity: 0.8;
        }

        .side-nav-link.active .side-nav-icon {
            opacity: 1;
        }

        /* 滚动条样式 */
        .side-navigation::-webkit-scrollbar {
            width: 4px;
        }

        .side-navigation::-webkit-scrollbar-track {
            background: var(--blanc-pearl);
            border-radius: 2px;
        }

        .side-navigation::-webkit-scrollbar-thumb {
            background: var(--noir-ash);
            border-radius: 2px;
        }

        .side-navigation::-webkit-scrollbar-thumb:hover {
            background: var(--noir-silver);
        }

        /* 响应式：小屏幕隐藏 */
        @media (max-width: 1400px) {
            .side-navigation {
                display: none;
            }
        }
    """
    
    # 在</style>标签前插入CSS
    style_end = content.find('</style>')
    if style_end != -1:
        content = content[:style_end] + nav_css + content[style_end:]
        print("   ✅ CSS已添加")
    else:
        print("   ❌ 未找到</style>标签")
        return False
    
    print()
    print("📍 步骤3: 创建导航栏HTML...")
    
    # 生成导航栏HTML
    nav_items = []
    for module in modules:
        nav_items.append(f'''            <li class="side-nav-item">
                <a class="side-nav-link" data-module="{module["id"]}" onclick="scrollToModule('{module["id"]}')">
                    <span class="side-nav-icon">{module["icon"]}</span>
                    <span>{module["name"]}</span>
                </a>
            </li>''')
    
    nav_html = f'''
    <!-- 左侧固定导航栏 -->
    <nav class="side-navigation">
        <div class="side-nav-header">快速导航</div>
        <ul class="side-nav-list">
{chr(10).join(nav_items)}
        </ul>
    </nav>
'''
    
    # 在<main class="main-container">之后插入导航栏
    main_start = content.find('<main class="main-container">')
    if main_start != -1:
        # 找到>后的位置
        insert_pos = content.find('>', main_start) + 1
        content = content[:insert_pos] + nav_html + content[insert_pos:]
        print("   ✅ 导航栏HTML已添加")
    else:
        print("   ❌ 未找到<main>标签")
        return False
    
    print()
    print("📍 步骤4: 添加滚动功能JavaScript...")
    
    # JavaScript代码
    nav_js = """
        /* ========== 左侧导航栏滚动功能 ========== */
        function scrollToModule(moduleId) {
            const element = document.getElementById(moduleId);
            if (element) {
                // 平滑滚动到目标模块
                element.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start',
                    inline: 'nearest'
                });
                
                // 更新导航栏激活状态
                updateActiveNav(moduleId);
            }
        }

        function updateActiveNav(moduleId) {
            // 移除所有active类
            document.querySelectorAll('.side-nav-link').forEach(link => {
                link.classList.remove('active');
            });
            
            // 添加active类到当前项
            const activeLink = document.querySelector(`[data-module="${moduleId}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }
        }

        // 监听滚动，自动更新导航栏激活状态
        let scrollTimeout;
        window.addEventListener('scroll', function() {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(function() {
                const modules = [
                    'module-project-view',
                    'module-pending-tasks',
                    'module-architect',
                    'module-fullstack',
                    'module-pulse',
                    'module-devops',
                    'module-noah'
                ];
                
                let activeModule = null;
                let minDistance = Infinity;
                
                // 找到最接近视口顶部的模块
                modules.forEach(moduleId => {
                    const element = document.getElementById(moduleId);
                    if (element) {
                        const rect = element.getBoundingClientRect();
                        const distance = Math.abs(rect.top - 100); // 100px偏移
                        
                        if (distance < minDistance && rect.top < window.innerHeight) {
                            minDistance = distance;
                            activeModule = moduleId;
                        }
                    }
                });
                
                if (activeModule) {
                    updateActiveNav(activeModule);
                }
            }, 100);
        });

        // 页面加载时初始化第一个为active
        window.addEventListener('DOMContentLoaded', function() {
            updateActiveNav('module-project-view');
        });
    """
    
    # 在</script>标签前插入JavaScript
    # 找到最后一个</script>
    script_positions = [m.end() for m in re.finditer('</script>', content)]
    if script_positions:
        last_script_pos = script_positions[-1]
        content = content[:last_script_pos] + nav_js + '\n' + content[last_script_pos:]
        print("   ✅ JavaScript已添加")
    else:
        print("   ❌ 未找到</script>标签")
        return False
    
    print()
    print("📍 步骤5: 保存修改后的文件...")
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ 文件已保存")
    
    print()
    print("="*80)
    print("✅ 左侧导航栏添加完成！")
    print("="*80)
    print()
    print("📊 添加内容:")
    print(f"   • {len(modules)} 个导航项")
    print(f"   • CSS样式（约{len(nav_css)}字符）")
    print(f"   • JavaScript功能（约{len(nav_js)}字符）")
    print()
    print("🌐 功能说明:")
    print("   • 固定在左侧的导航栏")
    print("   • 点击可平滑滚动到对应模块")
    print("   • 滚动时自动高亮当前模块")
    print("   • 小屏幕自动隐藏（<1400px）")
    print()
    print("🚀 测试方法:")
    print("   1. 访问 http://localhost:8826/")
    print("   2. 查看左侧导航栏")
    print("   3. 点击任意模块测试滚动")
    print()
    print(f"📁 备份文件: {backup_file}")
    print()
    
    return True

if __name__ == "__main__":
    import sys
    try:
        success = add_side_navigation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print()
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

