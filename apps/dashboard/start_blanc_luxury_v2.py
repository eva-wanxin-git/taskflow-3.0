#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
任务所·Flow - Blanc Luxury Edition V2
白色奢华版Dashboard启动脚本 - 完整功能版

运行在独立端口8879，包含：
- 9个统计卡片（现有6个 + 新增3个）
- 8个Tab（现有5个 + 新增3个）
- 完整的事件、对话、记忆展示
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
from industrial_dashboard.templates_blanc_luxury_v2 import get_blanc_luxury_v2_dashboard
from fastapi.responses import HTMLResponse


def main():
    """主函数"""
    print()
    print("=" * 80)
    print(" 任务所·Flow - Blanc Luxury Edition V2 ".center(80))
    print(" 白色奢华版 · 光的建筑学 · 呼吸感设计 · 完整功能 ".center(80))
    print("=" * 80)
    print()
    
    # 显示工作目录
    print(f"[OK] 工作目录: {os.getcwd()}")
    automation_data = Path(os.getcwd()) / "automation-data"
    print(f"[OK] 数据目录: {automation_data}")
    print(f"[OK] 数据目录存在: {automation_data.exists()}")
    print()
    
    # 使用新端口8879（完整功能版）
    port = 8879
    print(f"[OK] 独立端口: {port} (Blanc Luxury V2 - 完整版)")
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
        title="任务所·FLOW - Blanc Luxury V2",
        subtitle="白色奢华版完整版 | Ethereal Industrial Elegance",
        port=port,
        host="127.0.0.1"
    )
    
    # 添加Blanc Luxury V2专属路由
    @dashboard.app.get("/blanc-v2", response_class=HTMLResponse)
    async def blanc_luxury_v2_page():
        """Blanc Luxury V2主页"""
        html = get_blanc_luxury_v2_dashboard(
            data_provider=provider,
            event_provider=dashboard.event_stream_provider,
            memory_provider=dashboard.project_memory_provider,
            conversations_provider=None
        )
        return html
    
    # 默认路由也指向V2
    @dashboard.app.get("/", response_class=HTMLResponse)
    async def root():
        """默认路由重定向到V2"""
        html = get_blanc_luxury_v2_dashboard(
            data_provider=provider,
            event_provider=dashboard.event_stream_provider,
            memory_provider=dashboard.project_memory_provider,
            conversations_provider=None
        )
        return html
    
    print("[OK] Blanc Luxury V2 Dashboard ready")
    print("[OK] Custom routes registered")
    print()
    print("🎨 设计风格: Blanc Luxury Edition V2")
    print("   - 光的建筑学 (Light Architecture)")
    print("   - 呼吸感设计 (Breathing Space)")
    print("   - 触感视觉化 (Tactile Visualization)")
    print("   - 减法美学 (Less is Luxury)")
    print()
    print("✨ 新增功能:")
    print("   - 📊 3个新统计卡片: 事件数、会话数、记忆数")
    print("   - 🎯 3个新Tab: 事件流、对话历史、记忆空间")
    print("   - 🔗 任务关联展示: 显示关联的事件、对话、记忆")
    print("   - 🤖 AI协作链可视化")
    print()
    print(f"✨ 访问地址:")
    print(f"   主页: http://127.0.0.1:{port}/blanc-v2")
    print()
    print("=" * 80)
    print()
    
    # 启动
    dashboard.run(open_browser=True)


if __name__ == "__main__":
    main()

