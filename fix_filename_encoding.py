#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件名编码修复工具
修复乱码的中文文件名
"""

import os
import sys

def fix_filename_encoding(directory="."):
    """修复目录中的乱码文件名"""
    
    fixed_count = 0
    error_count = 0
    
    print(f"🔍 扫描目录: {os.path.abspath(directory)}\n")
    
    # 获取所有文件和目录
    try:
        items = os.listdir(directory)
    except Exception as e:
        print(f"❌ 无法读取目录: {e}")
        return
    
    for item in items:
        # 跳过隐藏文件和特殊目录
        if item.startswith('.'):
            continue
            
        old_path = os.path.join(directory, item)
        
        try:
            # 尝试检测乱码（包含特定乱码字符）
            # 这些是UTF-8中文在Latin-1编码下的常见乱码特征
            has_garbled = any(char in item for char in ['浣', '鐢', '鎸', '鍗', '鏋', '瀹', '鎴', '鎬', '缁', '浠', '鍔', '瑕', '鍙', '鍙', '鎶', '鎻', '璁', '椤', '鐩', '绾', '闆', '淇', '妯', '閮', '鏁', '缁', '鐗', '璐', '涓', '浜', '浠', '鍔', '鎽', '瀹', '鍏', '鍋', '鍙', '鍙', '鍙', '鎻', '璁', '鐪', '鎴', '浠', '瀹', '鎻', '娲', '鍏', '鎵', '閮', '鎺', '缁', '棰', '闆', '淇', '瀹', '鍏', '鎵', '涓', '鍘', '鍐', '浠', '寰', '璇', '璇', '娲', '璇', '璺', '涓', '甯', '鐢', '瀛', '浜', '鑴', '闃', '瀵', '绉', '鍘', '鍔', '鍓', '缁', '姝', '闈', '瑙', '缃', '鍒', '瀵', '鍨', '鏄', '閰', '琛', '鍦', '璺', '妞', '纭', '鏌', '鏌', '缁', '鏍', '椤', '鐩', '鏋', '鏋', '宸', '澶', '鐪', '鏍', '閲', '馃', '鈿'])
            
            if not has_garbled:
                continue
            
            # 尝试修复编码
            # 方法1: latin-1 -> utf-8 (最常见的情况)
            try:
                new_name = item.encode('latin-1').decode('utf-8')
                new_path = os.path.join(directory, new_name)
                
                # 检查新文件名是否已存在
                if os.path.exists(new_path):
                    print(f"⚠️  跳过 (目标已存在): {item}")
                    continue
                
                # 重命名
                os.rename(old_path, new_path)
                print(f"✅ 修复: {item}")
                print(f"   → {new_name}\n")
                fixed_count += 1
                continue
            except (UnicodeDecodeError, UnicodeEncodeError):
                pass
            
            # 方法2: cp1252 -> utf-8
            try:
                new_name = item.encode('cp1252').decode('utf-8')
                new_path = os.path.join(directory, new_name)
                
                if os.path.exists(new_path):
                    print(f"⚠️  跳过 (目标已存在): {item}")
                    continue
                
                os.rename(old_path, new_path)
                print(f"✅ 修复: {item}")
                print(f"   → {new_name}\n")
                fixed_count += 1
                continue
            except (UnicodeDecodeError, UnicodeEncodeError):
                pass
            
            # 无法修复
            print(f"❌ 无法修复: {item}")
            error_count += 1
            
        except Exception as e:
            print(f"❌ 处理出错: {item}")
            print(f"   错误: {e}\n")
            error_count += 1
    
    # 输出统计
    print("\n" + "="*60)
    print(f"📊 修复统计:")
    print(f"   ✅ 成功修复: {fixed_count} 个")
    print(f"   ❌ 失败/跳过: {error_count} 个")
    print("="*60)
    
    if fixed_count > 0:
        print("\n✨ 建议: 重新运行一次以确保所有文件都已修复")
    
    return fixed_count, error_count


if __name__ == "__main__":
    # 获取目标目录
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = "."
    
    print("🔧 文件名编码修复工具")
    print("="*60)
    
    # 执行修复
    fixed, errors = fix_filename_encoding(target_dir)
    
    # 提示是否需要再次运行
    if fixed > 0:
        print("\n💡 提示: 如果还有乱码文件，请再次运行此脚本")


