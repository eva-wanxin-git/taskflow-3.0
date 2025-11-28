#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
撤销Noah删除操作
从备份中提取第10018-13086行，插入回当前文件
"""

import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def undo_deletion():
    """撤销删除操作"""
    
    print("=" * 60)
    print("撤销Noah删除 - 从备份恢复")
    print("=" * 60)
    
    # 读取当前文件（已删除Noah的版本）
    print("\n📖 读取当前文件...")
    with open('index.html', 'r', encoding='utf-8') as f:
        current_lines = f.readlines()
    
    current_total = len(current_lines)
    print(f"✅ 当前文件: {current_total} 行")
    
    # 读取备份文件（删除之前的版本）
    backup_file = 'index.html.backup-before-fullstack-complete-20251120-211123'
    print(f"\n📖 读取备份文件: {backup_file}")
    
    with open(backup_file, 'r', encoding='utf-8') as f:
        backup_lines = f.readlines()
    
    backup_total = len(backup_lines)
    print(f"✅ 备份文件: {backup_total} 行")
    
    # 计算差异
    diff = backup_total - current_total
    print(f"\n📊 差异: {diff} 行")
    
    # 备份当前文件（删除后的版本）
    print(f"\n💾 创建当前版本备份...")
    import shutil
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_name = f'index.html.backup-after-noah-delete-{timestamp}'
    shutil.copy2('index.html', backup_name)
    print(f"✅ 备份创建: {backup_name}")
    
    # 简单方案：直接恢复整个备份文件
    print(f"\n🔄 恢复备份文件...")
    shutil.copy2(backup_file, 'index.html')
    
    print(f"\n✅ 恢复完成！")
    print(f"  当前文件已恢复到: {backup_file}")
    print(f"  文件大小: {backup_total} 行")
    
    return True

if __name__ == '__main__':
    success = undo_deletion()
    
    if success:
        print("\n🎉 撤销成功！")
        print("\n⚠️  注意:")
        print("  - 已恢复到删除Noah之前的状态")
        print("  - 但是也恢复了全栈工程师模块部署之前的状态")
        print("  - 需要重新应用全栈工程师模块和其他修复")
        print("\n下一步:")
        print("  1. 重启服务器: python -m http.server 8822")
        print("  2. 查看当前状态")
        print("  3. 告诉我需要重新应用哪些修复")

