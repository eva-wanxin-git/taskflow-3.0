#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务所·Flow - Blanc Luxury Edition
白色奢华版Dashboard启动脚本

运行在独立端口8878，不影响现有的8877端口
"""
import sys
import os
from pathlib import Path

# ⚠️ 重要：设置工作目录到 apps/dashboard
dashboard_dir = Path(__file__).parent
os.chdir(dashboard_dir)

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from industrial_dashboard import IndustrialDashboard
from industrial_dashboard.adapters import StateManagerAdapter
from automation.state_manager import StateManager


def main():
    """主函数"""
    print()
    print("=" * 80)
    print(" 任务所·Flow - Blanc Luxury Edition ".center(80))
    print(" 白色奢华版 · 光的建筑学 · 呼吸感设计 ".center(80))
    print("=" * 80)
    print()
    
    # 显示工作目录
    print(f"[OK] 工作目录: {os.getcwd()}")
    automation_data = Path(os.getcwd()) / "automation-data"
    print(f"[OK] 数据目录: {automation_data}")
    print(f"[OK] 数据目录存在: {automation_data.exists()}")
    print()
    
    # 使用新端口8878（避免冲突）
    port = 8878
    print(f"[OK] 独立端口: {port} (Blanc Luxury专属)")
    print()
    
    # 初始化StateManager
    db_path = Path(__file__).parent.parent.parent / "database" / "data" / "tasks.db"
    sm = StateManager(db_path=str(db_path))
    print("[OK] StateManager initialized")
    
    # 创建适配器
    provider = StateManagerAdapter(sm)
    print("[OK] Data provider created")
    
    # 创建Dashboard
    dashboard = IndustrialDashboard(
        data_provider=provider,
        title="任务所·FLOW - Blanc Luxury",
        subtitle="白色奢华版 | Ethereal Industrial Elegance",
        port=port,
        host="127.0.0.1"
    )
    print("[OK] Blanc Luxury Dashboard ready")
    print()
    print("🎨 设计风格: Blanc Luxury Edition")
    print("   - 光的建筑学 (Light Architecture)")
    print("   - 呼吸感设计 (Breathing Space)")
    print("   - 触感视觉化 (Tactile Visualization)")
    print("   - 减法美学 (Less is Luxury)")
    print()
    print(f"✨ 访问地址:")
    print(f"   主页: http://127.0.0.1:{port}/blanc")
    print(f"   事件流: http://127.0.0.1:{port}/blanc/events (即将推出)")
    print(f"   对话历史: http://127.0.0.1:{port}/blanc/conversations (即将推出)")
    print(f"   记忆空间: http://127.0.0.1:{port}/blanc/memory (即将推出)")
    print()
    print("=" * 80)
    print()
    
    # 启动
    dashboard.run(open_browser=True)


if __name__ == "__main__":
    main()

