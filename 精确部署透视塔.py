#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确部署透视塔模块到8820
只替换透视塔相关代码，保护其他模块
"""
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent
SOURCE_FILE = PROJECT_ROOT / "dashboard-test" / "index.html"  # 8829源文件
TARGET_FILE = PROJECT_ROOT / "dashboard-v1.9-20251121" / "index.html"  # 8820目标

print("="*70)
print("精确部署透视塔模块到8820")
print("="*70)
print()

# 1. 备份
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_file = TARGET_FILE.parent / f"index.html.backup-precise-{timestamp}"
print(f"📦 备份目标文件...")
with open(TARGET_FILE, 'r', encoding='utf-8') as f:
    target_content = f.read()
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(target_content)
print(f"✅ 备份: {backup_file.name}")
print()

# 2. 读取源文件
print(f"📖 读取源文件: dashboard-test/index.html")
with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
    source_content = f.read()
print(f"✅ 源文件大小: {len(source_content):,} 字符")
print()

# 3. 提取透视塔HTML模块（精确边界）
print("🔍 提取透视塔模块...")
html_pattern = r'(<!-- ========== 项目透视模块 ========== -->.*?</div>\s*</div>\s*\n\s*<!-- ========== 待开发任务模块)'

html_match = re.search(html_pattern, source_content, re.DOTALL)
if not html_match:
    print("❌ 提取失败：未找到透视塔模块")
    exit(1)

insight_html = html_match.group(1)
print(f"✅ 提取HTML: {len(insight_html):,} 字符")

# 4. 提取透视塔JavaScript（5个新函数）
print("\n🔍 提取JavaScript函数...")
js_functions = []

# 精确提取每个函数
func_patterns = [
    (r'// Tab1: 加载已实现功能\s*async function loadImplementedFeatures\(\).*?^\s*}', 'loadImplementedFeatures'),
    (r'// Tab2: 加载部分实现.*?async function loadPartialFeatures\(\).*?^\s*}', 'loadPartialFeatures'),
    (r'// Tab3: 加载问题清单.*?async function loadIssues\(\).*?^\s*}', 'loadIssues'),
    (r'// Tab4: 加载架构建议.*?async function loadRecommendations\(\).*?^\s*}', 'loadRecommendations'),
    (r'// 刷新透视塔.*?async function refreshInsightData\(\).*?^\s*}', 'refreshInsightData'),
    (r'// 复制架构师扫描指令.*?function copyArchitectPrompt\(\).*?^\s*}', 'copyArchitectPrompt'),
]

for pattern, name in func_patterns:
    match = re.search(pattern, source_content, re.MULTILINE | re.DOTALL)
    if match:
        js_functions.append(match.group(0))
        print(f"✅ 提取: {name}")
    else:
        print(f"⚠️ 未找到: {name}")

insight_js = '\n\n        '.join(js_functions)

# 5. 精确替换目标文件的透视塔模块
print("\n🔧 替换目标文件...")

# 替换HTML部分
new_content = re.sub(
    html_pattern,
    insight_html + r'\n\n        <!-- ========== 待开发任务模块',
    target_content,
    flags=re.DOTALL
)

if new_content == target_content:
    print("❌ HTML替换失败：未找到匹配内容")
    exit(1)

print("✅ HTML部分已替换")

# 替换JavaScript（删除旧函数，添加新函数）
# 先删除旧的透视塔函数
old_funcs = [
    r'// ========== 项目透视模块函数 ==========.*?function handleExport\(\).*?^\s*}',
]

for old_pattern in old_funcs:
    new_content = re.sub(old_pattern, '', new_content, flags=re.MULTILINE | re.DOTALL)

# 在</script></body>之前插入新JS
script_end = r'(</script>\s*</body>)'
new_content = re.sub(
    script_end,
    f'\n\n        // ========== 项目透视塔模块JavaScript ==========\n        {insight_js}\n\n    \\1',
    new_content
)

print("✅ JavaScript部分已替换")

# 6. 保存
print("\n💾 保存文件...")
with open(TARGET_FILE, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ 已保存: {TARGET_FILE}")

# 7. 验证
print("\n🔍 验证部署...")
with open(TARGET_FILE, 'r', encoding='utf-8') as f:
    verify_content = f.read()

checks = [
    ("架构师扫描", "Tab5"),
    ("id=\"insightImplementedCount\"", "统计ID"),
    ("loadImplementedFeatures", "加载函数"),
    ("copyArchitectPrompt", "复制函数"),
]

print()
for keyword, desc in checks:
    if keyword in verify_content:
        print(f"✅ {desc}: 存在")
    else:
        print(f"❌ {desc}: 缺失")

print("\n" + "="*70)
print("✅ 部署完成！")
print("="*70)
print("\n刷新8820测试: http://localhost:8820")
print("按 Command+Shift+R 强制刷新")






