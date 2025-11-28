#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全按照截图样式修复导航栏
- 完全直角（border-radius: 0）
- 每个导航项都是独立的白色框（有边框）
- 对齐"切换项目/模块"的卡片样式
"""

import os
from datetime import datetime

def fix_exact_style():
    html_file = "dashboard-test-8826/index.html"
    
    print("🔧 修复导航栏为完全直角卡片样式\n")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = f"{html_file}.backup-exact-{timestamp}"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已备份: {backup_file}\n")
    
    # 找到并替换CSS
    nav_css_start = content.find('/* ========== 左侧固定导航栏 ========== */')
    
    if nav_css_start == -1:
        print("❌ 未找到CSS")
        return False
    
    # 完全按照截图的样式
    new_css = """
        /* ========== 左侧固定导航栏 ========== */
        .side-navigation {
            position: fixed;
            left: 24px;
            top: 120px;
            width: 200px;
            z-index: 1000;
            max-height: calc(100vh - 180px);
            overflow-y: auto;
        }

        .side-nav-header {
            font-size: 14px;
            font-weight: var(--weight-regular);
            color: var(--noir-graphite);
            margin-bottom: 12px;
            padding: 0;
        }

        .side-nav-list {
            list-style: none;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .side-nav-item {
            margin: 0;
        }

        .side-nav-link {
            display: block;
            padding: 12px 16px;
            border: 1px solid var(--blanc-cloud);
            background: var(--blanc-pure);
            text-decoration: none;
            color: var(--noir-graphite);
            font-size: 14px;
            font-weight: var(--weight-regular);
            transition: all 200ms ease;
            cursor: pointer;
            border-radius: 0;
            box-sizing: border-box;
        }

        .side-nav-link:hover {
            background: var(--blanc-silk);
            border-color: var(--noir-silver);
        }

        .side-nav-link.active {
            background: var(--noir-ink);
            color: var(--blanc-pure);
            border-color: var(--noir-ink);
        }

        .side-navigation::-webkit-scrollbar {
            width: 4px;
        }

        .side-navigation::-webkit-scrollbar-track {
            background: transparent;
        }

        .side-navigation::-webkit-scrollbar-thumb {
            background: var(--noir-ash);
            border-radius: 0;
        }

        @media (max-width: 1400px) {
            .side-navigation {
                display: none;
            }
        }
    """
    
    # 找到CSS结束位置
    css_end = content.find('@media (max-width: 1400px)', nav_css_start)
    if css_end != -1:
        css_end = content.find('}', content.find('}', css_end) + 1) + 1
        content = content[:nav_css_start] + new_css + content[css_end:]
        print("✅ CSS已更新为完全直角卡片样式")
    
    # 保存
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 完成！刷新 http://localhost:8826/ 查看\n")
    return True

if __name__ == "__main__":
    fix_exact_style()

