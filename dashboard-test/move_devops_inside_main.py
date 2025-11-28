#!/usr/bin/env python3
"""将运维工程师模块移到main容器内"""

def move_devops_inside():
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # </main>在4929行（索引4928）
    # 运维工程师模块在4932行开始（索引4931）
    
    # 找到运维工程师模块的结束
    devops_start = 4931  # 索引
    devops_end = None
    
    # 找到运维工程师模块的结束（下一个大模块或script）
    for i in range(devops_start + 1, len(lines)):
        if '<script>' in lines[i] or '</body>' in lines[i]:
            devops_end = i - 1
            break
    
    if devops_end is None:
        print("❌ 未找到运维工程师模块结束位置")
        return False
    
    print(f"原文件行数: {len(lines)}")
    print(f"</main>位置: 第4929行")
    print(f"运维工程师模块: 第{devops_start+1}行到第{devops_end+1}行 ({devops_end-devops_start+1}行)")
    
    # 1. 提取运维工程师模块
    devops_module = lines[devops_start:devops_end+1]
    
    # 2. 删除原位置的运维工程师模块
    temp_lines = lines[:devops_start] + lines[devops_end+1:]
    
    # 3. 在</main>之前插入（</main>索引是4928）
    main_close_index = 4928
    final_lines = temp_lines[:main_close_index] + ['\n'] + devops_module + ['\n'] + temp_lines[main_close_index:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
    
    print(f"\n✅ 移动完成！")
    print(f"新文件行数: {len(final_lines)}")
    print(f"运维工程师模块已移到</main>之前")
    
    return True

if __name__ == '__main__':
    move_devops_inside()

