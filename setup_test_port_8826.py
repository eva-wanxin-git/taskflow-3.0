#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置测试端口8826
将8820正式版本复制到8826作为测试环境
"""

import os
import shutil
import subprocess
import sys
from datetime import datetime

def find_dashboard_directory(port):
    """查找指定端口对应的dashboard目录"""
    base_dir = os.getcwd()
    
    # 可能的目录列表
    candidates = [
        f"dashboard-test-{port}",
        "dashboard-test",
        "dashboard-v1.9-20251121",
        "dashboard-test-v1.8-20251120-final",
    ]
    
    for candidate in candidates:
        path = os.path.join(base_dir, candidate)
        if os.path.exists(path) and os.path.isdir(path):
            # 检查是否有index.html
            index_file = os.path.join(path, "index.html")
            if os.path.exists(index_file):
                return path
    
    return None

def check_port_process(port):
    """检查端口是否有进程运行"""
    try:
        result = subprocess.run(
            ['lsof', '-ti', f':{port}'],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            return result.stdout.strip()
        return None
    except:
        return None

def setup_test_port():
    """设置测试端口"""
    
    print("="*80)
    print("🔧 设置测试端口 8826")
    print("="*80)
    print()
    
    base_dir = os.getcwd()
    
    # 1. 查找8820正式版本目录
    print("📍 步骤1: 查找8820正式版本目录...")
    
    # 检查8820端口
    port_8820_pid = check_port_process(8820)
    if port_8820_pid:
        print(f"   ✅ 8820端口正在运行 (PID: {port_8820_pid})")
    else:
        print(f"   ⚠️  8820端口未运行")
    
    # 查找dashboard目录
    possible_source_dirs = [
        "dashboard-v1.9-20251121",  # v1.9正式版
        "dashboard-test",           # 当前测试版
        "dashboard-test-v1.8-20251120-final",  # v1.8版本
    ]
    
    source_dir = None
    for dir_name in possible_source_dirs:
        path = os.path.join(base_dir, dir_name)
        if os.path.exists(path):
            index_path = os.path.join(path, "index.html")
            if os.path.exists(index_path):
                source_dir = path
                print(f"   ✅ 找到源目录: {dir_name}")
                break
    
    if not source_dir:
        print("   ❌ 未找到dashboard目录！")
        return False
    
    print()
    
    # 2. 创建8826测试目录
    print("📍 步骤2: 创建8826测试目录...")
    
    test_dir_name = "dashboard-test-8826"
    test_dir_path = os.path.join(base_dir, test_dir_name)
    
    # 如果已存在，先备份
    if os.path.exists(test_dir_path):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f"{test_dir_name}-backup-{timestamp}"
        backup_path = os.path.join(base_dir, backup_name)
        
        print(f"   ⚠️  目录已存在，备份为: {backup_name}")
        shutil.move(test_dir_path, backup_path)
    
    # 复制目录
    print(f"   📋 正在复制 {os.path.basename(source_dir)} → {test_dir_name}...")
    
    try:
        shutil.copytree(source_dir, test_dir_path)
        print(f"   ✅ 复制完成")
    except Exception as e:
        print(f"   ❌ 复制失败: {e}")
        return False
    
    print()
    
    # 3. 验证复制结果
    print("📍 步骤3: 验证复制结果...")
    
    index_file = os.path.join(test_dir_path, "index.html")
    if os.path.exists(index_file):
        file_size = os.path.getsize(index_file)
        print(f"   ✅ index.html 存在 ({file_size:,} 字节)")
    else:
        print(f"   ❌ index.html 不存在！")
        return False
    
    print()
    
    # 4. 创建启动脚本
    print("📍 步骤4: 创建启动脚本...")
    
    startup_script = os.path.join(base_dir, "启动测试端口8826.sh")
    with open(startup_script, 'w', encoding='utf-8') as f:
        f.write("#!/bin/bash\n")
        f.write("# 启动测试端口8826\n\n")
        f.write(f"cd \"{test_dir_path}\"\n")
        f.write("echo \"🚀 启动测试端口 8826...\"\n")
        f.write("echo \"📁 目录: $(pwd)\"\n")
        f.write("echo \"🌐 访问: http://localhost:8826/\"\n")
        f.write("echo \"\"\n")
        f.write("python3 -m http.server 8826\n")
    
    os.chmod(startup_script, 0o755)
    print(f"   ✅ 启动脚本已创建: 启动测试端口8826.sh")
    
    print()
    
    # 5. 检查8826端口
    print("📍 步骤5: 检查8826端口...")
    
    port_8826_pid = check_port_process(8826)
    if port_8826_pid:
        print(f"   ⚠️  8826端口已被占用 (PID: {port_8826_pid})")
        print(f"   💡 运行以下命令停止: kill {port_8826_pid}")
    else:
        print(f"   ✅ 8826端口可用")
    
    print()
    
    # 6. 总结
    print("="*80)
    print("✅ 测试端口设置完成！")
    print("="*80)
    print()
    print("📊 配置信息:")
    print(f"   🟢 正式端口: 8820 (不要动)")
    print(f"   🔵 测试端口: 8826 (用于开发测试)")
    print()
    print(f"📁 目录信息:")
    print(f"   正式版: {os.path.basename(source_dir)}")
    print(f"   测试版: {test_dir_name}")
    print()
    print("🚀 启动方法:")
    print("   方法1: ./启动测试端口8826.sh")
    print(f"   方法2: cd {test_dir_name} && python3 -m http.server 8826")
    print()
    print("🌐 访问地址:")
    print("   正式版: http://localhost:8820/")
    print("   测试版: http://localhost:8826/")
    print()
    print("💡 工作流程:")
    print("   1. 在8826测试新功能")
    print("   2. 测试通过后")
    print("   3. 复制到8820正式版")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = setup_test_port()
        if success:
            print("🎉 现在可以启动测试端口了！")
            print()
            response = input("是否立即启动8826测试端口？(y/N): ")
            if response.lower() == 'y':
                print()
                print("🚀 正在启动测试端口8826...")
                print("   按 Ctrl+C 停止服务器")
                print()
                
                test_dir = os.path.join(os.getcwd(), "dashboard-test-8826")
                os.chdir(test_dir)
                subprocess.run(['python3', '-m', 'http.server', '8826'])
        
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print()
        print()
        print("❌ 用户中断")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ 发生错误: {e}")
        sys.exit(1)

