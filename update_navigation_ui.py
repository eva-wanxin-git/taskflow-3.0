#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新导航栏UI - 按照用户截图样式
1. 移除图标，只保留文字
2. 修复点击定位功能
"""

import os
import re
from datetime import datetime

def update_navigation_ui():
    """更新导航栏UI和功能"""
    
    html_file = "dashboard-test-8826/index.html"
    
    print("="*80)
    print("🔧 更新导航栏UI和功能")
    print("="*80)
    print()
    
    # 读取文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = f"{html_file}.backup-update-nav-{timestamp}"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📋 已备份到: {backup_file}\n")
    
    # ===== 步骤1: 更新CSS样式 =====
    print("📍 步骤1: 更新CSS样式（按截图设计）...")
    
    # 找到导航栏CSS部分
    nav_css_start = content.find('/* ========== 左侧固定导航栏 ========== */')
    nav_css_end = content.find('/* 响应式：小屏幕隐藏 */', nav_css_start)
    
    if nav_css_start == -1 or nav_css_end == -1:
        print("   ❌ 未找到导航栏CSS")
        return False
    
    # 新的CSS样式（按照截图的简洁设计）
    new_css = """
        /* ========== 左侧固定导航栏 ========== */
        .side-navigation {
            position: fixed;
            left: 24px;
            top: 120px;
            width: 200px;
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-cloud);
            border-radius: 8px;
            padding: 20px 16px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
            z-index: 1000;
            max-height: calc(100vh - 180px);
            overflow-y: auto;
        }

        .side-nav-header {
            font-size: 14px;
            font-weight: var(--weight-medium);
            color: var(--noir-graphite);
            margin-bottom: 16px;
            padding: 0 4px;
            letter-spacing: 0.3px;
        }

        .side-nav-list {
            list-style: none;
            margin: 0;
            padding: 0;
        }

        .side-nav-item {
            margin-bottom: 2px;
        }

        .side-nav-link {
            display: block;
            padding: 10px 12px;
            border-radius: 6px;
            text-decoration: none;
            color: var(--noir-steel);
            font-size: 14px;
            font-weight: var(--weight-regular);
            transition: all 200ms ease;
            cursor: pointer;
        }

        .side-nav-link:hover {
            background: var(--blanc-silk);
            color: var(--noir-ink);
        }

        .side-nav-link.active {
            background: var(--noir-ink);
            color: var(--blanc-pure);
            font-weight: var(--weight-medium);
        }

        /* 移除图标相关样式 */
        .side-nav-icon {
            display: none;
        }

        /* 滚动条样式 */
        .side-navigation::-webkit-scrollbar {
            width: 4px;
        }

        .side-navigation::-webkit-scrollbar-track {
            background: transparent;
        }

        .side-navigation::-webkit-scrollbar-thumb {
            background: var(--noir-ash);
            border-radius: 2px;
        }

        .side-navigation::-webkit-scrollbar-thumb:hover {
            background: var(--noir-silver);
        }

        """
    
    # 替换CSS
    # 找到整个CSS块的结束位置（包括响应式部分）
    responsive_end = content.find('}', content.find('@media (max-width: 1400px)', nav_css_start))
    if responsive_end != -1:
        responsive_end = content.find('}', responsive_end) + 1
        
        # 替换整个CSS块
        content = content[:nav_css_start] + new_css + content[responsive_end:]
        print("   ✅ CSS样式已更新（移除图标，简洁设计）")
    else:
        print("   ⚠️  CSS替换位置不确定")
    
    print()
    
    # ===== 步骤2: 更新HTML（移除图标） =====
    print("📍 步骤2: 更新HTML（移除图标）...")
    
    # 找到导航栏HTML
    nav_html_start = content.find('<!-- 左侧固定导航栏 -->')
    nav_html_end = content.find('</nav>', nav_html_start)
    
    if nav_html_start != -1 and nav_html_end != -1:
        # 生成新的HTML（无图标版本）
        modules = [
            {"name": "项目透视塔", "id": "module-project-view"},
            {"name": "待开发任务池", "id": "module-pending-tasks"},
            {"name": "架构师工作台", "id": "module-architect"},
            {"name": "全栈工程师", "id": "module-fullstack"},
            {"name": "实时脉动", "id": "module-pulse"},
            {"name": "运维工程师", "id": "module-devops"},
            {"name": "Noah代码管家", "id": "module-noah"},
        ]
        
        nav_items = []
        for module in modules:
            nav_items.append(f'''            <li class="side-nav-item">
                <a class="side-nav-link" data-module="{module["id"]}" onclick="scrollToModule('{module["id"]}'); return false;">
                    {module["name"]}
                </a>
            </li>''')
        
        new_nav_html = f'''
    <!-- 左侧固定导航栏 -->
    <nav class="side-navigation">
        <div class="side-nav-header">快速导航</div>
        <ul class="side-nav-list">
{chr(10).join(nav_items)}
        </ul>
    </nav>
'''
        
        # 替换HTML
        content = content[:nav_html_start] + new_nav_html + content[nav_html_end + 6:]
        print("   ✅ HTML已更新（移除图标）")
    else:
        print("   ❌ 未找到导航栏HTML")
    
    print()
    
    # ===== 步骤3: 修复JavaScript滚动功能 =====
    print("📍 步骤3: 修复JavaScript滚动定位功能...")
    
    # 找到JavaScript部分
    js_marker = '/* ========== 左侧导航栏滚动功能 ========== */'
    js_start = content.find(js_marker)
    
    if js_start != -1:
        # 找到这个JavaScript块的结束位置（下一个大的注释或script结束）
        js_end = content.find('</script>', js_start)
        
        # 新的JavaScript（修复滚动功能）
        new_js = """
        /* ========== 左侧导航栏滚动功能 ========== */
        function scrollToModule(moduleId) {
            console.log('Scrolling to:', moduleId);
            const element = document.getElementById(moduleId);
            
            if (element) {
                console.log('Element found:', element);
                
                // 获取元素位置
                const elementPosition = element.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - 100; // 100px偏移
                
                // 滚动到目标位置
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // 更新导航栏激活状态
                updateActiveNav(moduleId);
            } else {
                console.error('Module not found:', moduleId);
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
                        const distance = Math.abs(rect.top - 150);
                        
                        if (distance < minDistance && rect.top < window.innerHeight / 2) {
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

        // 页面加载时初始化
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Page loaded, initializing navigation');
            updateActiveNav('module-project-view');
            
            // 检查所有模块是否有ID
            const modules = [
                'module-project-view',
                'module-pending-tasks',
                'module-architect',
                'module-fullstack',
                'module-pulse',
                'module-devops',
                'module-noah'
            ];
            
            console.log('Checking module IDs:');
            modules.forEach(moduleId => {
                const element = document.getElementById(moduleId);
                if (element) {
                    console.log('✓', moduleId, 'found');
                } else {
                    console.error('✗', moduleId, 'NOT found');
                }
            });
        });
    """
        
        # 找到旧的JavaScript块结束位置
        old_js_end = js_start
        for i in range(100):  # 最多找100个}
            next_brace = content.find('});', old_js_end + 1)
            if next_brace == -1:
                break
            old_js_end = next_brace + 3
            # 检查是否到达了下一个大注释或script结束
            next_section = content[old_js_end:old_js_end + 100]
            if '/*' in next_section or '</script>' in next_section:
                break
        
        # 替换JavaScript
        content = content[:js_start] + new_js + '\n' + content[old_js_end:]
        print("   ✅ JavaScript已更新（修复滚动定位）")
    else:
        print("   ❌ 未找到JavaScript部分")
    
    print()
    
    # 保存文件
    print("📍 步骤4: 保存修改...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("   ✅ 文件已保存")
    
    print()
    print("="*80)
    print("✅ 更新完成！")
    print("="*80)
    print()
    print("🎨 UI变更:")
    print("   • 移除了所有图标")
    print("   • 简洁的文字列表")
    print("   • 黑色激活态背景")
    print("   • 灰色悬停态背景")
    print()
    print("🔧 功能修复:")
    print("   • 修复了点击滚动定位")
    print("   • 添加了console.log调试信息")
    print("   • 优化了滚动偏移量")
    print("   • 添加了模块ID检查")
    print()
    print("🧪 测试方法:")
    print("   1. 访问 http://localhost:8826/")
    print("   2. 打开浏览器控制台（F12）")
    print("   3. 点击导航栏任意模块")
    print("   4. 查看控制台日志和页面滚动效果")
    print()
    print(f"📁 备份: {backup_file}")
    print()
    
    return True

if __name__ == "__main__":
    import sys
    try:
        success = update_navigation_ui()
        sys.exit(0 if success else 1)
    except Exception as e:
        print()
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

