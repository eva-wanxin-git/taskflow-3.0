# -*- coding: utf-8 -*-
"""
将全栈完整版模块移到main-container内部
确保和其他模块的宽度对齐一致
"""

def move_module():
    print("1. 读取文件...")
    with open('index.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"   总行数: {len(lines)}")
    
    # 2. 找到新模块的开始和结束位置
    print("\n2. 查找新模块位置...")
    module_start = None
    module_end = None
    
    for i, line in enumerate(lines):
        if '<!-- ========== 全栈工程师工作台（完整版） ========== -->' in line:
            module_start = i
            print(f"   找到模块开始: 第{i+1}行")
        
        # 找到模块结束（下一个<script>标签）
        if module_start is not None and module_end is None:
            if i > module_start and '<script>' in line and '</div>' in lines[i-1]:
                module_end = i - 1  # 在<script>前一行结束
                print(f"   找到模块结束: 第{i}行")
                break
    
    if module_start is None or module_end is None:
        print("❌ 错误：找不到模块位置")
        return False
    
    # 3. 提取模块内容
    print("\n3. 提取模块内容...")
    module_content = lines[module_start:module_end+1]
    print(f"   提取了 {len(module_content)} 行")
    
    # 4. 找到</main>的位置
    print("\n4. 查找</main>位置...")
    main_end = None
    for i, line in enumerate(lines):
        if '</main>' in line and i < module_start:
            main_end = i
            print(f"   找到</main>: 第{i+1}行")
    
    if main_end is None:
        print("❌ 错误：找不到</main>")
        return False
    
    # 5. 删除原位置的模块
    print("\n5. 删除原位置的模块...")
    del lines[module_start:module_end+1]
    print(f"   删除了 {len(module_content)} 行")
    
    # 6. 在</main>之前插入（注意行号已变化）
    print("\n6. 在</main>之前插入模块...")
    # 因为删除了后面的内容，main_end位置不变
    lines[main_end:main_end] = module_content
    print(f"   在第{main_end+1}行插入")
    
    # 7. 写入文件
    print("\n7. 写入文件...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\n✅ 完成！模块已移动到main-container内部")
    print(f"   新位置: 第{main_end+1}行（</main>之前）")
    return True

if __name__ == '__main__':
    try:
        success = move_module()
        if success:
            print("\n" + "="*60)
            print("✅ 全栈完整版模块已成功移到main-container内部")
            print("="*60)
            print("\n现在模块将自动继承main-container的宽度约束")
            print("实际显示宽度: 1400px - 40px(左) - 40px(右) = 1320px")
            print("\n请重启服务器并强制刷新浏览器验证")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

