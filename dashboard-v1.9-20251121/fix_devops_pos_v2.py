#!/usr/bin/env python3
"""修复运维工程师模块位置v2"""

def fix_devops():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 运维工程师模块：5356-6053行（索引5355-6052）
    devops_start = 5355
    devops_end = 6052
    
    # <script>在4932行（索引4931）
    script_index = 4931
    
    print(f"原文件行数: {len(lines)}")
    print(f"运维工程师模块: 第{devops_start+1}行到第{devops_end+1}行 ({devops_end-devops_start+1}行)")
    print(f"<script>位置: 第{script_index+1}行")
    
    # 1. 提取运维工程师模块
    devops_module = lines[devops_start:devops_end+1]
    
    # 2. 删除原位置（从后往前删，避免索引变化）
    temp_lines = lines[:devops_start] + lines[devops_end+1:]
    
    # 3. 在<script>之前插入（script索引不变，因为删除的在后面）
    final_lines = temp_lines[:script_index] + ['\n'] + devops_module + ['\n'] + temp_lines[script_index:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
    
    print(f"\n✅ 修复完成！")
    print(f"新文件行数: {len(final_lines)}")
    print(f"运维工程师模块已移到<script>之前")
    
    return True

if __name__ == '__main__':
    fix_devops()

