#!/usr/bin/env python3
"""修复运维工程师模块位置：移到script之前"""

def fix_devops_position():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # </main>在4930行（索引4929）
    # <script>在4932行（索引4931）
    # 运维工程师模块开始在5356行（索引5355）
    
    # 找到运维工程师模块的结束位置
    devops_start = 5355  # 索引
    
    # 找到</body>前的位置
    devops_end = None
    for i in range(devops_start, len(lines)):
        if '</body>' in lines[i]:
            devops_end = i - 1
            break
    
    if devops_end is None:
        print("❌ 未找到</body>标签")
        return False
    
    print(f"原文件行数: {len(lines)}")
    print(f"运维工程师模块: 第{devops_start+1}行到第{devops_end+1}行")
    print(f"<script>位置: 第4932行")
    
    # 提取运维工程师模块内容
    devops_module = lines[devops_start:devops_end+1]
    
    # 删除原位置的运维工程师模块
    temp_lines = lines[:devops_start] + lines[devops_end+1:]
    
    # 在<script>之前插入（<script>现在在索引4931）
    script_index = 4931
    new_lines = temp_lines[:script_index] + ['\n'] + devops_module + ['\n'] + temp_lines[script_index:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✅ 修复完成！")
    print(f"新文件行数: {len(new_lines)}")
    print(f"运维工程师模块已移到<script>之前")
    
    return True

if __name__ == '__main__':
    fix_devops_position()

