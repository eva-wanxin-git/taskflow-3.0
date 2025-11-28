#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复乱码文件名 - 正确版本
这些文件名是UTF-8的中文被错误编码后的结果
"""

import os
import sys

def decode_garbled_name(garbled):
    """尝试解码乱码文件名"""
    
    # 尝试多种解码方式
    decoders = [
        # UTF-8误读为GBK再当UTF-8读
        lambda s: s.encode('utf-8').decode('gbk', errors='ignore'),
        # UTF-8误读为latin-1
        lambda s: s.encode('latin-1', errors='ignore').decode('utf-8', errors='ignore'),
        # GB2312相关
        lambda s: s.encode('utf-8').decode('gb18030', errors='ignore'),
        # 其他常见编码
        lambda s: s.encode('iso-8859-1', errors='ignore').decode('utf-8', errors='ignore'),
    ]
    
    for decoder in decoders:
        try:
            decoded = decoder(garbled)
            # 检查解码后是否包含合法的中文字符
            if any('\u4e00' <= c <= '\u9fff' for c in decoded):
                return decoded
        except:
            continue
    
    return None


def fix_filenames(directory='.', dry_run=False):
    """修复目录中的乱码文件名"""
    
    print(f"{'='*80}")
    print(f"{'🔧 文件名修复工具' if not dry_run else '🔍 文件名检测模式（dry-run）'}")
    print(f"{'='*80}\n")
    print(f"📁 目录: {os.path.abspath(directory)}\n")
    
    fixed_count = 0
    skip_count = 0
    error_count = 0
    
    try:
        items = os.listdir(directory)
    except Exception as e:
        print(f"❌ 无法读取目录: {e}")
        return 0, 0, 0
    
    # 过滤出可能是乱码的文件
    garbled_chars = set('浣鐢鎸鍗鏋瀹鎴鎬缁浠鍔瑕鍙鎸鎻璁椤鐩绾闆淇妯閮鏁鐗璐涓浜鍔鎽瀹鍏鍋鍙鎻璁鐪鎴浠瀹鎻娲鍏鎵閮鎺缁棰闆淇瀹鍏鎵涓鍘鍐浠寰璇璺涓甯鐢瀛浜鑴闃瀵绉鍘鍔鍓缁姝闈瑙缃鍒瀵鍨鏄閰琛鍦璺妞纭鏌缁鏍椤鐩鏋宸澶鐪鏍閲馃鈿')
    
    garbled_files = []
    for item in items:
        if item.startswith('.') or os.path.isdir(os.path.join(directory, item)):
            continue
        if any(c in garbled_chars for c in item):
            garbled_files.append(item)
    
    print(f"找到 {len(garbled_files)} 个疑似乱码文件\n")
    
    if not garbled_files:
        print("✅ 没有发现乱码文件！")
        return 0, 0, 0
    
    for old_name in garbled_files:
        old_path = os.path.join(directory, old_name)
        
        # 尝试解码
        new_name = decode_garbled_name(old_name)
        
        if not new_name or new_name == old_name:
            print(f"⚠️  无法解码: {old_name[:50]}...")
            error_count += 1
            continue
        
        new_path = os.path.join(directory, new_name)
        
        # 检查目标文件是否已存在
        if os.path.exists(new_path):
            print(f"⚠️  目标已存在，跳过: {old_name[:30]}... → {new_name[:30]}...")
            skip_count += 1
            continue
        
        if dry_run:
            print(f"🔍 将修复: {old_name[:40]}...")
            print(f"   →  {new_name}")
            fixed_count += 1
        else:
            try:
                os.rename(old_path, new_path)
                print(f"✅ {old_name[:40]}...")
                print(f"   →  {new_name}\n")
                fixed_count += 1
            except Exception as e:
                print(f"❌ 重命名失败: {old_name[:40]}...")
                print(f"   错误: {e}\n")
                error_count += 1
    
    # 输出统计
    print(f"\n{'='*80}")
    print(f"📊 统计:")
    print(f"   ✅ {'将修复' if dry_run else '已修复'}: {fixed_count} 个")
    print(f"   ⚠️  跳过: {skip_count} 个")
    print(f"   ❌ 失败: {error_count} 个")
    print(f"{'='*80}\n")
    
    if dry_run and fixed_count > 0:
        print("💡 确认无误后，运行以下命令执行修复:")
        print(f"   python3 {__file__}")
    
    return fixed_count, skip_count, error_count


if __name__ == "__main__":
    # 检查参数
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    target_dir = "."
    
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        target_dir = sys.argv[1]
    
    # 先运行dry-run模式看看结果
    if not dry_run and '-y' not in sys.argv:
        print("⚠️  将执行文件重命名操作！")
        print("💡 建议先运行: python3 fix_garbled_filenames.py --dry-run")
        print()
        response = input("确认继续？(y/N): ")
        if response.lower() != 'y':
            print("已取消")
            sys.exit(0)
    
    # 执行修复
    fixed, skipped, errors = fix_filenames(target_dir, dry_run=dry_run)
    
    sys.exit(0 if errors == 0 else 1)


