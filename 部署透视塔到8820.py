#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署透视塔模块到8820生产环境
只替换透视塔相关的代码，不影响其他模块
"""
import re
from pathlib import Path
from datetime import datetime

# 路径配置
PROJECT_ROOT = Path(__file__).parent
SOURCE_FILE = PROJECT_ROOT / "dashboard-test" / "index.html"  # 8829测试版本
TARGET_DIRS = [
    PROJECT_ROOT / "dashboard-test",
    PROJECT_ROOT / "dashboard-test-8826",
    PROJECT_ROOT / "dashboard-v1.9-20251121",
]

def backup_file(file_path):
    """备份文件"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = file_path.parent / f"{file_path.name}.backup-insight-deploy-{timestamp}"
    
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 备份: {backup_path.name}")
        return True
    return False

def extract_insight_module(source_html):
    """从源文件提取透视塔模块的完整代码"""
    
    # 1. 提取CSS（透视塔专属的CSS）
    css_pattern = r'(/\* === 透视塔模块样式.*?/\* === 下一个模块)'
    
    # 2. 提取HTML（从<!-- 项目透视模块 -->到下一个模块）
    html_start = r'<!-- ========== 项目透视模块 ========== -->'
    html_end = r'<!-- ========== 待开发任务模块'
    
    # 3. 提取JavaScript（透视塔相关函数）
    js_funcs = [
        'function switchTab',
        'async function loadImplementedFeatures',
        'async function loadPartialFeatures',  
        'async function loadIssues',
        'async function loadRecommendations',
        'async function refreshInsightData',
        'function copyArchitectPrompt'  # 新版本
    ]
    
    print("\n提取透视塔模块代码...")
    
    # 提取HTML部分
    html_match = re.search(
        f'{html_start}(.*?){html_end}',
        source_html,
        re.DOTALL
    )
    
    if html_match:
        insight_html = html_start + html_match.group(1)
        print(f"✅ HTML: 已提取 ({len(insight_html)} 字符)")
    else:
        print("❌ HTML: 提取失败")
        return None
    
    # 提取JavaScript
    insight_js = ""
    for func_name in js_funcs:
        # 查找函数定义
        pattern = rf'({func_name}.*?^\s*}})'
        match = re.search(pattern, source_html, re.MULTILINE | re.DOTALL)
        if match:
            insight_js += "\n        // " + func_name + "\n"
            insight_js += "        " + match.group(1) + "\n"
            print(f"✅ JS: {func_name}")
    
    return {
        'html': insight_html,
        'js': insight_js
    }

def deploy_to_target(target_file, insight_code):
    """部署到目标文件"""
    
    if not target_file.exists():
        print(f"❌ 文件不存在: {target_file}")
        return False
    
    print(f"\n部署到: {target_file.parent.name}/index.html")
    
    # 备份
    backup_file(target_file)
    
    # 读取目标文件
    with open(target_file, 'r', encoding='utf-8') as f:
        target_html = f.read()
    
    # 替换HTML部分
    html_start = r'<!-- ========== 项目透视模块 ========== -->'
    html_end = r'<!-- ========== 待开发任务模块'
    
    new_html = re.sub(
        f'{html_start}.*?{html_end}',
        insight_code['html'] + '\n\n        ' + html_end,
        target_html,
        flags=re.DOTALL
    )
    
    if new_html == target_html:
        print("⚠️ HTML替换失败，未找到匹配的模块标记")
        return False
    
    print("✅ HTML部分已替换")
    
    # 替换JavaScript部分（透视塔相关函数）
    # 找到旧的switchTab等函数并替换
    for old_func in ['function switchTab', 'async function loadImplementedFeatures']:
        if old_func in new_html:
            # 删除旧函数
            pattern = rf'{old_func}.*?^\s*}}'
            new_html = re.sub(pattern, '', new_html, count=1, flags=re.MULTILINE | re.DOTALL)
    
    # 在</script>之前插入新的JS
    new_html = new_html.replace(
        '    </script>\n</body>',
        insight_code['js'] + '\n    </script>\n</body>'
    )
    
    print("✅ JavaScript部分已替换")
    
    # 保存
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"✅ 部署完成: {target_file}")
    return True

def main():
    print("="*70)
    print("部署透视塔模块到8820生产环境")
    print("="*70)
    
    # 读取源文件（8829测试版本）
    print(f"\n读取源文件: {SOURCE_FILE}")
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        source_html = f.read()
    print(f"✅ 源文件大小: {len(source_html)} 字符")
    
    # 提取透视塔模块
    insight_code = extract_insight_module(source_html)
    
    if not insight_code:
        print("\n❌ 提取失败，终止部署")
        return
    
    # 询问部署到哪个目录
    print("\n" + "="*70)
    print("可用的目标目录:")
    for i, target_dir in enumerate(TARGET_DIRS, 1):
        exists = "✅" if (target_dir / "index.html").exists() else "❌"
        print(f"{i}. {exists} {target_dir.name}")
    
    print("\n自动部署到第1个目录（dashboard-test，应该是8820生产环境）")
    
    target_file = TARGET_DIRS[0] / "index.html"
    
    # 执行部署
    success = deploy_to_target(target_file, insight_code)
    
    if success:
        print("\n" + "="*70)
        print("✅ 部署成功！")
        print("="*70)
        print("\n下一步:")
        print("1. 刷新浏览器: http://localhost:8820")
        print("2. 按 Command+Shift+R 强制刷新")
        print("3. 测试透视塔5个Tab")
        print("4. 测试复制指令功能")
    else:
        print("\n❌ 部署失败")

if __name__ == "__main__":
    main()






