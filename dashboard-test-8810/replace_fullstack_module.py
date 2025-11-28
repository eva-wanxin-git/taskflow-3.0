#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
替换全栈工程师模块 - 8810测试环境
将旧版模块替换为完整版
"""

import os
from datetime import datetime

# 文件路径
INDEX_HTML = "index.html"
FULLSTACK_COMPLETE = "../dashboard-test/fullstack-engineer-workbench-optimized.html"
BACKUP_SUFFIX = datetime.now().strftime("-%Y%m%d-%H%M%S")

def main():
    print("=" * 80)
    print("全栈工程师模块替换工具 - v1.0")
    print("=" * 80)
    
    # 1. 备份
    print("\n[Step 1] 备份文件...")
    backup_file = f"index.html.backup-before-module-replace{BACKUP_SUFFIX}"
    with open(INDEX_HTML, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] 已备份: {backup_file}")
    
    # 2. 读取完整版模块
    print("\n[Step 2] 读取完整版模块...")
    with open(FULLSTACK_COMPLETE, 'r', encoding='utf-8') as f:
        complete_module = f.read()
    print(f"[OK] 已读取: {FULLSTACK_COMPLETE} ({len(complete_module)} bytes)")
    
    # 3. 读取当前index.html
    print("\n[Step 3] 读取当前Dashboard...")
    lines = content.split('\n')
    total_lines = len(lines)
    print(f"[OK] 总行数: {total_lines}")
    
    # 4. 定位模块位置
    print("\n[Step 4] 定位模块位置...")
    
    # 找到第一个全栈工程师模块（8887-11062）
    old_module_start = None
    old_module_end = None
    
    # 找到第二个全栈工程师完整版（13285-15690）
    duplicate_start = None
    duplicate_end = None
    
    for i, line in enumerate(lines, 1):
        # 查找旧版模块开始（约8887行）
        if old_module_start is None and '全栈工程师工作台' in line and '====' in line:
            old_module_start = i - 1  # 转为0-based index
            print(f"[OK] 找到旧版模块开始: 第{i}行")
        
        # 查找旧版模块结束（约11062行）- 找</div>加上后面是API状态条
        if old_module_start is not None and old_module_end is None:
            if '</div>' in line and 'engineer-module' in lines[i-2]:
                # 检查下一个非空行是否是API状态条
                next_line_idx = i
                while next_line_idx < len(lines) and lines[next_line_idx].strip() == '':
                    next_line_idx += 1
                if next_line_idx < len(lines) and 'API状态条' in lines[next_line_idx]:
                    old_module_end = i  # 包含这一行
                    print(f"[OK] 找到旧版模块结束: 第{i}行")
                    print(f"   旧版模块: {old_module_start+1}-{old_module_end}行 ({old_module_end-old_module_start}行)")
        
        # 查找完整版模块（约13285行开始）
        if old_module_end is not None and duplicate_start is None:
            if i > 13000 and '全栈工程师' in line and ('完整版' in line or ('====' in line and i > 13200)):
                duplicate_start = i - 1
                print(f"[WARN] 找到重复完整版开始: 第{i}行")
        
        # 查找重复完整版结束（约15690行）
        if duplicate_start is not None and duplicate_end is None:
            if 'TASKFLOW FOOTER' in line or (i > 15600 and 'Footer' in line):
                duplicate_end = i - 1  # 不包含footer
                print(f"[WARN] 找到重复完整版结束: 第{i}行")
                print(f"   重复模块: {duplicate_start+1}-{duplicate_end}行 ({duplicate_end-duplicate_start}行)")
                break
    
    if old_module_start is None or old_module_end is None:
        print("[ERROR] 错误: 无法找到旧版模块位置")
        return
    
    # 5. 执行替换
    print("\n[Step 5] 执行替换...")
    
    # 提取完整版模块的body部分（去掉HTML头尾）
    complete_lines = complete_module.split('\n')
    
    # 找到body内容开始和结束
    body_start = None
    body_end = None
    for i, line in enumerate(complete_lines):
        if '<body>' in line:
            body_start = i + 1
        if '</body>' in line:
            body_end = i
            break
    
    if body_start and body_end:
        complete_body = '\n'.join(complete_lines[body_start:body_end])
        print(f"[OK] 提取完整版body内容: {body_start}-{body_end}行")
    else:
        # 如果没有找到body标签，就用整个文件
        complete_body = complete_module
        print(f"[WARN] 使用完整文件内容")
    
    # 添加注释标记
    complete_with_comments = f"""
        <!-- 全栈工程师工作台 开始 -->
        <!-- 版本: v2.0 完整版 -->
        <!-- 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->
        <!-- 包含: 5个Tab (事件流/任务看板/代码审查/技术文档/对话历史) -->
        
{complete_body}
        
        <!-- 全栈工程师工作台 结束 -->
"""
    
    # 构建新内容
    new_lines = []
    
    # 1. 保留开头到旧模块之前的内容
    new_lines.extend(lines[:old_module_start])
    
    # 2. 插入完整版模块
    new_lines.append(complete_with_comments)
    
    # 3. 跳过旧模块，继续到重复模块之前（或文件末尾）
    if duplicate_start:
        # 保留旧模块后到重复模块前的内容
        new_lines.extend(lines[old_module_end:duplicate_start])
        # 跳过重复模块，继续到文件末尾
        new_lines.extend(lines[duplicate_end:])
    else:
        # 没有重复模块，直接继续到文件末尾
        new_lines.extend(lines[old_module_end:])
    
    print(f"[OK] 新内容构建完成")
    print(f"   原始行数: {total_lines}")
    print(f"   新行数: {len(new_lines)}")
    print(f"   差异: {len(new_lines) - total_lines} 行")
    
    # 6. 写入文件
    print("\n[Step 6] 写入新文件...")
    new_content = '\n'.join(new_lines)
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    file_size = len(new_content)
    print(f"[OK] 已写入: {INDEX_HTML}")
    print(f"   文件大小: {file_size:,} bytes")
    
    print("\n" + "=" * 80)
    print("[SUCCESS] 替换完成!")
    print("=" * 80)
    print(f"\n备份文件: {backup_file}")
    print(f"新文件: {INDEX_HTML}")
    print("\n下一步:")
    print("1. 运行验证脚本: python check_balance.py")
    print("2. 启动服务器: python -m http.server 8810")
    print("3. 浏览器访问: http://localhost:8810/")
    print("=" * 80)

if __name__ == '__main__':
    main()

