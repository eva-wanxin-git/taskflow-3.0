#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整备份脚本 - TaskFlow v1.9
创建项目的完整备份副本
"""

import os
import shutil
import sys
from datetime import datetime
import subprocess

def get_directory_size(path):
    """计算目录大小"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                total_size += os.path.getsize(filepath)
            except:
                pass
    return total_size

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def count_files(path):
    """统计文件数量"""
    count = 0
    for dirpath, dirnames, filenames in os.walk(path):
        count += len(filenames)
    return count

def create_backup():
    """创建完整备份"""
    
    print("="*80)
    print("🔧 TaskFlow v1.9 完整备份工具")
    print("="*80)
    print()
    
    # 当前目录
    source_dir = os.getcwd()
    project_name = os.path.basename(source_dir)
    
    # 父目录
    parent_dir = os.path.dirname(source_dir)
    
    # 生成备份名称
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"taskflow-v1.9-backup-{timestamp}"
    backup_path = os.path.join(parent_dir, backup_name)
    
    print(f"📁 源目录: {source_dir}")
    print(f"📦 备份目录: {backup_path}")
    print()
    
    # 计算源目录信息
    print("📊 正在分析源目录...")
    file_count = count_files(source_dir)
    dir_size = get_directory_size(source_dir)
    
    print(f"   文件数量: {file_count:,} 个")
    print(f"   目录大小: {format_size(dir_size)}")
    print()
    
    # 确认
    print("⚠️  即将创建完整备份，请确认：")
    print(f"   1. 备份名称: {backup_name}")
    print(f"   2. 备份位置: {parent_dir}")
    print(f"   3. 预计大小: {format_size(dir_size)}")
    print()
    
    response = input("确认继续？(y/N): ")
    if response.lower() != 'y':
        print("❌ 已取消备份")
        return False
    
    print()
    print("🚀 开始备份...")
    print()
    
    # 要排除的目录/文件
    exclude_patterns = [
        '__pycache__',
        '*.pyc',
        '.git',
        '.DS_Store',
        'node_modules',
        '.venv',
        'venv',
        '.pytest_cache',
    ]
    
    # 创建备份
    try:
        def ignore_patterns(directory, files):
            """定义要忽略的文件"""
            ignored = []
            for pattern in exclude_patterns:
                if pattern.startswith('*.'):
                    # 文件扩展名模式
                    ext = pattern[1:]
                    ignored.extend([f for f in files if f.endswith(ext)])
                else:
                    # 目录名模式
                    if pattern in files:
                        ignored.append(pattern)
            return ignored
        
        # 复制目录
        print(f"📋 正在复制文件...")
        shutil.copytree(
            source_dir, 
            backup_path,
            ignore=ignore_patterns,
            dirs_exist_ok=False
        )
        
        print(f"✅ 备份完成！")
        print()
        
        # 验证备份
        print("🔍 正在验证备份...")
        backup_file_count = count_files(backup_path)
        backup_size = get_directory_size(backup_path)
        
        print(f"   备份文件数: {backup_file_count:,} 个")
        print(f"   备份大小: {format_size(backup_size)}")
        print()
        
        # 创建备份信息文件
        info_file = os.path.join(backup_path, "BACKUP_INFO.txt")
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("TaskFlow v1.9 备份信息\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"备份时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"备份名称: {backup_name}\n")
            f.write(f"源目录: {source_dir}\n")
            f.write(f"备份路径: {backup_path}\n\n")
            f.write(f"文件数量: {backup_file_count:,} 个\n")
            f.write(f"备份大小: {format_size(backup_size)}\n\n")
            f.write("=" * 80 + "\n")
            f.write("恢复方法:\n")
            f.write("=" * 80 + "\n")
            f.write("1. 直接使用此备份目录开发\n")
            f.write("2. 或复制回原位置\n")
            f.write(f"   cp -r {backup_path} {source_dir}-restored\n\n")
            f.write("=" * 80 + "\n")
            f.write("版本信息:\n")
            f.write("=" * 80 + "\n")
            f.write("版本: v1.9.0\n")
            f.write("状态: 生产就绪\n")
            f.write("模块数: 9个\n")
            f.write("Tab数: 22个\n")
            f.write("功能数: 132个已实现\n")
            f.write("代码行数: 15,938行\n")
        
        print(f"✅ 备份信息已保存: {info_file}")
        print()
        
        # 创建压缩包（可选）
        print("📦 是否创建压缩包？(便于传输)")
        response = input("创建tar.gz压缩包？(y/N): ")
        
        if response.lower() == 'y':
            print()
            print("🗜️  正在压缩...")
            tar_file = f"{backup_path}.tar.gz"
            
            try:
                # 使用tar命令压缩
                subprocess.run([
                    'tar', '-czf', tar_file,
                    '-C', parent_dir,
                    backup_name
                ], check=True)
                
                tar_size = os.path.getsize(tar_file)
                print(f"✅ 压缩完成: {tar_file}")
                print(f"   压缩包大小: {format_size(tar_size)}")
                print(f"   压缩率: {(1 - tar_size/backup_size)*100:.1f}%")
            except Exception as e:
                print(f"⚠️  压缩失败: {e}")
        
        print()
        print("="*80)
        print("🎉 备份完成！")
        print("="*80)
        print()
        print(f"📁 备份目录: {backup_path}")
        print(f"📊 文件数量: {backup_file_count:,} 个")
        print(f"💾 总大小: {format_size(backup_size)}")
        print()
        print("📝 后续操作:")
        print("   1. 验证备份内容")
        print("   2. 如需要，可以在备份中继续开发")
        print("   3. 如需要，可以传输到其他电脑")
        print()
        
        return True
        
    except Exception as e:
        print()
        print(f"❌ 备份失败: {e}")
        print()
        
        # 清理不完整的备份
        if os.path.exists(backup_path):
            print("🧹 正在清理不完整的备份...")
            try:
                shutil.rmtree(backup_path)
                print("✅ 清理完成")
            except:
                print(f"⚠️  请手动删除: {backup_path}")
        
        return False

if __name__ == "__main__":
    try:
        success = create_backup()
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

