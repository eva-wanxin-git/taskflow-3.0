#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给8826添加完整的API调用逻辑
让透视塔从API动态获取数据（161个功能）
"""

import os
from datetime import datetime

def add_api_logic():
    """添加API调用逻辑"""
    
    html_file = "dashboard-test-8826/index.html"
    
    print("="*80)
    print("🔧 添加透视塔API调用逻辑")
    print("="*80)
    print()
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 备份
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = f"{html_file}.backup-api-{timestamp}"
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📋 已备份: {backup_file}\n")
    
    # 查找loadInsightData函数位置
    load_insight_pos = content.find('async function loadInsightData(tabName)')
    if load_insight_pos == -1:
        print("❌ 未找到loadInsightData函数")
        return False
    
    # 在这个函数后面插入缺失的loadImplementedFeatures函数
    insert_pos = content.find('}', content.find('}', load_insight_pos) + 1) + 1
    
    # 完整的API调用函数
    api_functions = """

        // Tab1: 加载已实现功能（从API）
        async function loadImplementedFeatures() {
            try {
                const response = await fetch('http://localhost:8800/api/features/implemented');
                const data = await response.json();
                
                if (data.success) {
                    console.log('✅ 已实现功能数据:', data);
                    
                    // 更新透视塔头部统计数字
                    const countEl = document.getElementById('insightImplementedCount');
                    if (countEl) {
                        countEl.textContent = data.total;  // 应该是161
                        console.log('更新已实现数量:', data.total);
                    }
                    
                    // 更新Tab标题
                    const tabTitle = document.querySelector('#implemented .section-title');
                    if (tabTitle) {
                        tabTitle.textContent = `已实现功能（${data.total}项）`;
                    }
                    
                    showToast(`✓ 已加载 ${data.total} 个已实现功能`);
                } else {
                    showToast('⚠️ 数据加载失败');
                }
            } catch (error) {
                console.error('加载已实现功能失败:', error);
                showToast('⚠️ API连接失败，请确保8800端口服务运行中');
            }
        }
"""
    
    content = content[:insert_pos] + api_functions + content[insert_pos:]
    print("✅ 添加了loadImplementedFeatures函数")
    print()
    
    # 保存
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 文件已保存")
    print()
    print("="*80)
    print("✅ API调用逻辑添加完成！")
    print("="*80)
    print()
    print("🎯 功能说明:")
    print("   • 从 http://localhost:8800/api/features/implemented 获取数据")
    print("   • 自动更新顶部统计数字（132 → 161）")
    print("   • 自动更新Tab标题")
    print("   • Toast提示加载状态")
    print()
    print("🧪 测试方法:")
    print("   1. 确保8800 API服务运行中")
    print("   2. 访问 http://localhost:8826/")
    print("   3. 打开控制台（F12）")
    print("   4. 刷新页面，等待2秒")
    print("   5. 应该看到顶部数字从132变成161")
    print()
    
    return True

if __name__ == "__main__":
    import sys
    try:
        success = add_api_logic()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

