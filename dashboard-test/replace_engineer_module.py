#!/usr/bin/env python3
"""
替换全栈工程师工作台模块
"""

import sys

def replace_engineer_module():
    # 读取原文件
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 读取新模块内容
    with open('engineer-module-fixed.html', 'r', encoding='utf-8') as f:
        new_module = f.read()
    
    # 找到模块开始和结束位置
    # 开始: 2860行 (索引2859)，包含 "<!-- ========== 全栈工程师工作台 ========== -->"
    # 结束: 3195行 (索引3194)，包含闭合的 </div>
    
    start_line = 2859  # 行号2860，索引2859
    end_line = 3194    # 行号3195，索引3194
    
    print(f"原文件行数: {len(lines)}")
    print(f"删除范围: 第{start_line+1}行到第{end_line+1}行 ({end_line-start_line+1}行)")
    
    # 确认开始和结束标记
    if '全栈工程师工作台' not in lines[start_line]:
        print(f"⚠️ 警告: 第{start_line+1}行不包含'全栈工程师工作台'")
        print(f"实际内容: {lines[start_line][:100]}")
        return False
    
    # 构建新文件
    new_lines = lines[:start_line]  # 保留之前的内容
    new_lines.append(new_module)     # 插入新模块
    if not new_module.endswith('\n'):
        new_lines.append('\n')
    new_lines.extend(lines[end_line+1:])  # 保留之后的内容
    
    # 写入新文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✅ 替换完成！")
    print(f"新文件行数: {len(new_lines)}")
    print(f"行数变化: {len(new_lines) - len(lines):+d}")
    
    return True

if __name__ == '__main__':
    try:
        success = replace_engineer_module()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

