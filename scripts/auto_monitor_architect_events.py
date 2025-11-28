#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
架构师事件流自动监听脚本
监听项目文件变化，自动添加事件到architect_events.json

监听内容：
1. 完成报告（*.md）
2. 部署文件（*.bat, 启动*.sh）
3. 测试结果
4. 架构文档变化
"""
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
EVENTS_FILE = PROJECT_ROOT / "apps" / "dashboard" / "automation-data" / "architect_events.json"

# 监听的目录
WATCH_DIRS = [
    PROJECT_ROOT / "docs" / "reports",  # 完成报告
    PROJECT_ROOT / "docs" / "arch",     # 架构文档
    PROJECT_ROOT,                        # 根目录（部署脚本）
]

# 关键文件模式
REPORT_PATTERNS = ["完成报告", "审查报告", "总结", "交接"]
DEPLOY_PATTERNS = ["启动", "部署", ".bat", ".sh"]
TEST_PATTERNS = ["测试", "验证", "test"]

class ArchitectEventHandler(FileSystemEventHandler):
    """架构师事件处理器"""
    
    def __init__(self):
        self.last_events = {}  # 防止重复触发
        self.cooldown = 5  # 冷却时间5秒
    
    def should_process(self, file_path):
        """判断是否应该处理这个文件"""
        now = time.time()
        
        # 检查冷却时间
        if file_path in self.last_events:
            if now - self.last_events[file_path] < self.cooldown:
                return False
        
        self.last_events[file_path] = now
        return True
    
    def on_created(self, event):
        """文件创建事件"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        if not self.should_process(file_path):
            return
        
        self.process_file_event(file_path, "created")
    
    def on_modified(self, event):
        """文件修改事件"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        if not self.should_process(file_path):
            return
        
        self.process_file_event(file_path, "modified")
    
    def process_file_event(self, file_path, action):
        """处理文件事件"""
        file_name = os.path.basename(file_path)
        
        # 判断事件类型
        event_type = None
        event_icon = "📄"
        event_content = None
        
        # 完成报告
        if any(pattern in file_name for pattern in REPORT_PATTERNS):
            if "完成报告" in file_name:
                event_type = "task_complete"
                event_icon = "✅"
                event_content = f"任务完成报告: {file_name}"
            elif "审查报告" in file_name:
                event_type = "code_review"
                event_icon = "🔍"
                event_content = f"代码审查完成: {file_name}"
            elif "交接" in file_name:
                event_type = "handoff"
                event_icon = "🤝"
                event_content = f"项目交接: {file_name}"
        
        # 部署文件
        elif any(pattern in file_name for pattern in DEPLOY_PATTERNS):
            event_type = "deployment"
            event_icon = "🚀"
            event_content = f"部署脚本更新: {file_name}"
        
        # 测试文件
        elif any(pattern in file_name for pattern in TEST_PATTERNS):
            event_type = "test"
            event_icon = "🧪"
            event_content = f"测试更新: {file_name}"
        
        # 如果是关注的事件，添加到JSON
        if event_type and event_content:
            self.add_event(event_type, event_icon, event_content, {
                "file": file_name,
                "action": action,
                "path": file_path
            })
    
    def add_event(self, event_type, icon, content, metadata):
        """添加事件到JSON文件"""
        try:
            # 读取现有数据
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            events = data.get("events", [])
            
            # 生成新事件
            event_id = f"auto-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            new_event = {
                "id": event_id,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": event_type,
                "content": content,
                "metadata": metadata
            }
            
            # 添加到列表
            events.append(new_event)
            data["events"] = events
            
            # 写入文件
            with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 事件已记录: {content}")
            
        except Exception as e:
            print(f"❌ 添加事件失败: {e}")

def main():
    """主函数"""
    print("="*60)
    print("架构师事件流自动监听器".center(60))
    print("="*60)
    print()
    print("📁 监听目录:")
    for watch_dir in WATCH_DIRS:
        if watch_dir.exists():
            print(f"   ✅ {watch_dir}")
        else:
            print(f"   ❌ {watch_dir} (不存在)")
    print()
    print(f"💾 事件文件: {EVENTS_FILE}")
    print()
    print("🔍 监听事件类型:")
    print("   - 完成报告（*.md 包含'完成报告'）")
    print("   - 审查报告（*.md 包含'审查报告'）")
    print("   - 部署脚本（*.bat, *.sh, 包含'启动'/'部署'）")
    print("   - 测试文件（包含'测试'/'验证'）")
    print()
    print("⏰ 冷却时间: 5秒（防止重复触发）")
    print()
    print("="*60)
    print("🚀 监听器已启动，按Ctrl+C停止")
    print("="*60)
    print()
    
    # 创建事件处理器
    event_handler = ArchitectEventHandler()
    
    # 创建观察者
    observer = Observer()
    
    # 为每个监听目录添加观察者
    for watch_dir in WATCH_DIRS:
        if watch_dir.exists():
            observer.schedule(event_handler, str(watch_dir), recursive=True)
            print(f"👁️  正在监听: {watch_dir}")
    
    # 启动观察者
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n")
        print("="*60)
        print("⏹️  监听器已停止")
        print("="*60)
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    # 检查watchdog是否安装
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("❌ 缺少watchdog库，请安装:")
        print("   pip3 install watchdog")
        sys.exit(1)
    
    main()

