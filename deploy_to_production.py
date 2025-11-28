#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署到8820正式环境
将8826测试版本部署到8820
"""

import os
import shutil
from datetime import datetime

def deploy_to_production():
    """部署测试版本到正式环境"""
    
    print("="*80)
    print("🚀 部署到8820正式环境")
    print("="*80)
    print()
    
    # 源目录和目标目录
    test_dir = "dashboard-test-8826"
    prod_dir = "dashboard-v1.9-20251121"
    
    test_html = os.path.join(test_dir, "index.html")
    prod_html = os.path.join(prod_dir, "index.html")
    
    # 检查文件是否存在
    if not os.path.exists(test_html):
        print(f"❌ 测试文件不存在: {test_html}")
        return False
    
    if not os.path.exists(prod_html):
        print(f"❌ 正式文件不存在: {prod_html}")
        return False
    
    print(f"📁 测试版本: {test_dir}")
    print(f"📁 正式版本: {prod_dir}")
    print()
    
    # 获取文件信息
    test_size = os.path.getsize(test_html)
    prod_size = os.path.getsize(prod_html)
    
    print(f"📊 文件大小:")
    print(f"   测试版: {test_size:,} 字节")
    print(f"   正式版: {prod_size:,} 字节")
    print()
    
    # 确认部署
    print("⚠️  即将部署以下改动到正式环境:")
    print("   ✅ 左侧固定导航栏（7个模块快速定位）")
    print("   ✅ 顶部标题栏满宽设计")
    print("   ✅ 右侧版本切换器已隐藏")
    print("   ✅ 导航栏浅灰色激活态")
    print()
    
    response = input("确认部署到正式环境？(y/N): ")
    if response.lower() != 'y':
        print("❌ 已取消部署")
        return False
    
    print()
    print("🔧 开始部署...")
    print()
    
    # 步骤1: 备份正式版本
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = f"{prod_html}.backup-before-deploy-{timestamp}"
    
    print("📋 步骤1: 备份正式版本...")
    shutil.copy2(prod_html, backup_file)
    print(f"   ✅ 已备份到: {backup_file}")
    print()
    
    # 步骤2: 复制测试版本到正式环境
    print("📋 步骤2: 复制测试版本到正式环境...")
    shutil.copy2(test_html, prod_html)
    print(f"   ✅ 已复制: {test_html} → {prod_html}")
    print()
    
    # 步骤3: 验证部署
    print("📋 步骤3: 验证部署...")
    new_size = os.path.getsize(prod_html)
    print(f"   正式版新大小: {new_size:,} 字节")
    
    if new_size == test_size:
        print(f"   ✅ 文件大小匹配")
    else:
        print(f"   ⚠️  文件大小不匹配")
    print()
    
    # 步骤4: 创建部署日志
    print("📋 步骤4: 创建部署日志...")
    
    deploy_log = f"""
# 🚀 部署日志

**部署时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**源**: {test_dir}
**目标**: {prod_dir}

## 部署内容

### 新增功能
1. ✅ 左侧固定导航栏
   - 7个模块快速定位
   - 平滑滚动效果
   - 自动高亮当前模块

2. ✅ 顶部标题栏满宽
   - 自适应屏幕宽度
   - 完全贴合左右边缘

3. ✅ 右侧切换器隐藏
   - display: none
   - 功能保留

### 文件信息
- 测试版大小: {test_size:,} 字节
- 正式版大小: {new_size:,} 字节
- 备份文件: {backup_file}

## 访问地址
- 正式环境: http://localhost:8820/
- 测试环境: http://localhost:8826/

## 回滚方法
如需回滚，执行:
```bash
cp {backup_file} {prod_html}
```

---
部署状态: ✅ 成功
"""
    
    log_file = f"部署日志-8820-{timestamp}.md"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(deploy_log)
    
    print(f"   ✅ 部署日志已创建: {log_file}")
    print()
    
    # 完成
    print("="*80)
    print("✅ 部署完成！")
    print("="*80)
    print()
    print("🌐 访问地址:")
    print("   正式环境: http://localhost:8820/")
    print("   测试环境: http://localhost:8826/")
    print()
    print("💡 注意:")
    print("   - 8820服务器无需重启（已自动读取新文件）")
    print("   - 请使用 Cmd+Shift+R 强制刷新浏览器")
    print("   - 备份文件已保存，可随时回滚")
    print()
    print(f"📁 备份文件: {backup_file}")
    print(f"📝 部署日志: {log_file}")
    print()
    
    return True

if __name__ == "__main__":
    import sys
    try:
        success = deploy_to_production()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print()
        print("❌ 用户中断")
        sys.exit(1)
    except Exception as e:
        print()
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

