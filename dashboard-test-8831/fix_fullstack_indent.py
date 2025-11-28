# -*- coding: utf-8 -*-
"""
修复全栈完整版模块的缩进
统一为8个空格，和其他模块保持一致
"""

def fix_indent():
    print("1. 读取文件...")
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 2. 找到新模块范围
    print("2. 查找新模块...")
    start_line = None
    end_line = None
    
    for i, line in enumerate(lines):
        if '全栈工程师工作台（完整版）' in line:
            start_line = i
            print(f"   开始: 第{i+1}行")
            
    # 找结束：往后找到匹配的</div>
    if start_line:
        depth = 0
        found_first_div = False
        for i in range(start_line, len(lines)):
            line = lines[i]
            
            # 开始计数（从第一个<div开始）
            if '<div' in line:
                found_first_div = True
            
            if found_first_div:
                depth += line.count('<div')
                depth -= line.count('</div>')
                
                if depth == 0 and i > start_line + 50:
                    end_line = i
                    print(f"   结束: 第{i+1}行")
                    break
    
    if not start_line or not end_line:
        print("错误：找不到模块范围")
        return False
    
    print(f"   共{end_line-start_line+1}行")
    
    # 3. 修复缩进
    print("\n3. 修复缩进...")
    fixed_count = 0
    
    for i in range(start_line, end_line + 1):
        line = lines[i]
        
        # 跳过空行
        if line.strip() == '':
            continue
        
        # 计算当前缩进
        current_indent = len(line) - len(line.lstrip())
        
        # 期望缩进：8个空格
        expected_indent = 8
        
        # 如果行内有内容且缩进不是8
        if current_indent != expected_indent:
            # 移除当前缩进，添加8个空格
            lines[i] = ' ' * expected_indent + line.lstrip()
            fixed_count += 1
    
    print(f"   修复了 {fixed_count} 行")
    
    # 4. 写入文件
    print("\n4. 写入文件...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("\n✅ 缩进修复完成！")
    return True

if __name__ == '__main__':
    try:
        fix_indent()
        print("\n现在所有模块的缩进都统一为8个空格了")
        print("请重启服务器并强制刷新浏览器")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

