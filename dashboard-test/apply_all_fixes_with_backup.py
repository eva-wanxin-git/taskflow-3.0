#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新应用所有修复 - 每一步都备份
"""

import sys
import shutil
from datetime import datetime

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def create_backup(step_name):
    """创建备份"""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_name = f'index.html.backup-{step_name}-{timestamp}'
    shutil.copy2('index.html', backup_name)
    print(f"  💾 备份创建: {backup_name}")
    return backup_name

def apply_fixes():
    """应用所有修复"""
    
    print("=" * 70)
    print("重新应用所有修复 - 每一步都备份")
    print("=" * 70)
    
    # 读取文件
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n📖 原文件大小: {len(content)} 字符")
    
    # ========== 修复1: 删除待开发任务池的固定高度 ==========
    print("\n" + "=" * 70)
    print("🔧 修复1: 删除待开发任务池固定高度")
    print("=" * 70)
    
    old_pending_css = """        .pending-features-module {
            max-width: 1600px;
            margin: 64px auto 48px auto;
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            height: calc(100vh - 80px);
            display: flex;
            flex-direction: column;
        }"""
    
    new_pending_css = """        .pending-features-module {
            max-width: 1600px;
            margin: 64px auto 48px auto;
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            /* ✅ 删除固定高度，让内容自适应 */
            display: flex;
            flex-direction: column;
        }"""
    
    if old_pending_css in content:
        content = content.replace(old_pending_css, new_pending_css)
        print("  ✅ 修复成功: 删除了 height: calc(100vh - 80px)")
    else:
        print("  ⚠️  未找到目标CSS，可能已修改")
    
    # 保存并备份
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    create_backup('step1-pending-height')
    
    # ========== 修复2: 修复架构师模块上边距 ==========
    print("\n" + "=" * 70)
    print("🔧 修复2: 修复架构师模块上边距")
    print("=" * 70)
    
    old_architect_css = """        .architect-module {
            max-width: 1600px;
            margin: 64px auto 48px auto;
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            display: flex;
            flex-direction: column;
        }"""
    
    new_architect_css = """        .architect-module {
            max-width: 1600px;
            margin: 0 auto 48px auto;  /* ✅ 上边距改为0，避免与待开发任务池叠加 */
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            display: flex;
            flex-direction: column;
        }"""
    
    if old_architect_css in content:
        content = content.replace(old_architect_css, new_architect_css)
        print("  ✅ 修复成功: 上边距从64px改为0")
    else:
        print("  ⚠️  未找到目标CSS，可能已修改")
    
    # 保存并备份
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    create_backup('step2-architect-margin')
    
    # ========== 修复3: 添加全栈工程师模块间距 ==========
    print("\n" + "=" * 70)
    print("🔧 修复3: 全栈工程师模块添加上下间距")
    print("=" * 70)
    
    old_fullstack_css = """        .fullstack-complete-module {
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            margin-bottom: var(--space-7);  /* ✅ 和架构师模块一致 */
            display: flex;
            flex-direction: column;
        }"""
    
    new_fullstack_css = """        .fullstack-complete-module {
            max-width: 1600px;              /* ✅ 添加最大宽度 */
            margin: 48px auto 48px auto;    /* ✅ 上下48px，左右auto居中 */
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            display: flex;
            flex-direction: column;
        }"""
    
    if old_fullstack_css in content:
        content = content.replace(old_fullstack_css, new_fullstack_css)
        print("  ✅ 修复成功: 添加max-width和上边距")
    else:
        print("  ⚠️  未找到目标CSS，可能已修改")
    
    # 保存并备份
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    create_backup('step3-fullstack-margin')
    
    # ========== 完成 ==========
    print("\n" + "=" * 70)
    print("✅ 所有修复完成！")
    print("=" * 70)
    
    print("\n📋 修复总结:")
    print("  1. ✅ 待开发任务池：删除固定高度")
    print("  2. ✅ 架构师模块：上边距改为0")
    print("  3. ✅ 全栈工程师模块：添加宽度和间距")
    
    print("\n💾 创建了3个备份:")
    print("  - step1-pending-height")
    print("  - step2-architect-margin")
    print("  - step3-fullstack-margin")
    
    return True

if __name__ == '__main__':
    success = apply_fixes()
    
    if success:
        print("\n🎉 修复完成！")
        print("\n下一步:")
        print("  1. 重启服务器: python -m http.server 8822")
        print("  2. 强制刷新: Ctrl + Shift + R")
        print("  3. 检查所有模块显示")

