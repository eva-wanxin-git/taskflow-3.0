#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务看板定时同步调度器

功能:
- 每10分钟自动运行一次看板同步
- 可以作为后台服务运行
- 支持手动触发同步

使用方法:
    python services/task_board_scheduler.py
"""

import time
import schedule
from datetime import datetime
from pathlib import Path
import sys

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from task_board_auto_sync import TaskBoardAutoSync


class TaskBoardScheduler:
    """任务看板调度器"""
    
    def __init__(self):
        self.syncer = TaskBoardAutoSync()
        self.last_sync_time = None
        self.sync_count = 0
    
    def run_sync(self):
        """运行同步任务"""
        print(f"\n{'='*70}")
        print(f"⏰ 定时同步触发 (第 {self.sync_count + 1} 次)")
        print(f"{'='*70}\n")
        
        try:
            result = self.syncer.sync()
            self.last_sync_time = datetime.now()
            self.sync_count += 1
            
            if result['success']:
                print(f"✅ 同步成功")
            else:
                print(f"⚠️  同步跳过: {result['message']}")
        
        except Exception as e:
            print(f"❌ 同步失败: {e}")
            import traceback
            traceback.print_exc()
    
    def start(self):
        """启动调度器"""
        print("\n" + "="*70)
        print("🚀 任务看板自动同步调度器")
        print("="*70)
        print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"同步间隔: 每 10 分钟")
        print(f"看板路径: {self.syncer.board_path}")
        print("="*70)
        print()
        print("💡 提示:")
        print("  - 按 Ctrl+C 停止服务")
        print("  - 脚本会自动备份看板")
        print("  - 同步日志保存在 docs/tasks/sync_log.json")
        print()
        
        # 立即执行一次同步
        print("🔄 执行首次同步...")
        self.run_sync()
        
        # 设置定时任务
        schedule.every(10).minutes.do(self.run_sync)
        
        print(f"\n⏰ 下次同步时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🟢 调度器运行中...\n")
        
        # 主循环
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("🛑 收到停止信号")
            print("="*70)
            print(f"总同步次数: {self.sync_count}")
            print(f"最后同步: {self.last_sync_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_sync_time else 'N/A'}")
            print("="*70)
            print("👋 调度器已停止\n")


def main():
    """主函数"""
    scheduler = TaskBoardScheduler()
    scheduler.start()


if __name__ == "__main__":
    main()

