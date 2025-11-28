#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建只有全栈工程师模块的版本
方便调试容器高度
"""

import os
import re

def create_fullstack_only():
    """创建精简版本"""
    
    html_file = "dashboard-test-8830/index.html"
    
    print("="*80)
    print("🔧 创建只有全栈工程师模块的精简版")
    print("="*80)
    print()
    
    # 读取文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("📍 步骤1: 提取全栈工程师模块...")
    
    # 找到全栈工程师模块
    engineer_start = content.find('<div class="engineer-module" id="module-fullstack">')
    if engineer_start == -1:
        print("   ❌ 未找到engineer-module")
        return False
    
    # 找到对应的结束标签
    pos = engineer_start
    div_count = 1
    pos = content.find('>', pos) + 1
    
    while div_count > 0 and pos < len(content):
        next_open = content.find('<div', pos)
        next_close = content.find('</div>', pos)
        
        if next_close == -1:
            break
            
        if next_open != -1 and next_open < next_close:
            div_count += 1
            pos = next_open + 4
        else:
            div_count -= 1
            pos = next_close + 6
            if div_count == 0:
                engineer_end = pos
                break
    
    engineer_module = content[engineer_start:engineer_end]
    print(f"   ✅ 提取了全栈工程师模块（{len(engineer_module):,} 字符）")
    print()
    
    # 步骤2: 创建精简HTML
    print("📍 步骤2: 创建精简HTML结构...")
    
    # 提取head部分（包含所有CSS）
    head_start = content.find('<head>')
    head_end = content.find('</head>') + 7
    head_section = content[head_start:head_end]
    
    # 提取顶部标题栏
    header_start = content.find('<header class="brand-header">')
    header_end = content.find('</header>', header_start) + 9
    header_section = content[header_start:header_end]
    
    # 创建新HTML
    simple_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
{head_section}
<body>
    {header_section}

    <!-- 主容器 -->
    <main class="main-container">
        
        <!-- 统计卡片 -->
        <div class="stats-section version-content" data-version="1">
            <div class="stats-label">全栈工程师专用调试版</div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">8830</div>
                    <div class="stat-label">调试端口</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">1</div>
                    <div class="stat-label">模块数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">容器高度</div>
                    <div class="stat-label">调试中</div>
                </div>
            </div>
        </div>

        <!-- 只保留全栈工程师模块 -->
        {engineer_module}
        
    </main>

    <script>
        // 简化的版本切换（全部返回版本1）
        function switchVersion(version) {{
            console.log('Version:', version);
        }}
        
        // 保留切换项目功能
        function switchProject(projectId) {{
            console.log('Switch to:', projectId);
        }}
        
        // 清除缓存
        function clearCache() {{
            localStorage.clear();
            location.reload(true);
        }}
    </script>
</body>
</html>
'''
    
    # 保存精简版本
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(simple_html)
    
    print("   ✅ 精简HTML已创建")
    print()
    
    print("="*80)
    print("✅ 精简版本创建完成！")
    print("="*80)
    print()
    print("📊 内容:")
    print("   • 顶部标题栏")
    print("   • 统计卡片（显示调试信息）")
    print("   • 全栈工程师模块（完整保留）")
    print("   • 删除了其他6个模块")
    print()
    print("🌐 访问地址: http://localhost:8830/")
    print("   全新端口，无缓存，可以清晰看到容器高度效果")
    print()
    
    return True

if __name__ == "__main__":
    import sys
    try:
        success = create_fullstack_only()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

