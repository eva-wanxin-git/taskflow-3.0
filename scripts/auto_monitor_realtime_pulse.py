#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实时脉动自动监听脚本（全角色）
监听项目文件变化，自动添加所有角色的事件到realtime_pulse_events.json

监听内容：
1. 完成报告（全栈工程师、架构师等）
2. 部署文件（*.bat, 启动*.sh）
3. 测试结果（测试工程师）
4. 架构文档（架构师）
5. 运维日志（运维工程师）
6. 代码扫描（代码管家）
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
PULSE_FILE = PROJECT_ROOT / "apps" / "dashboard" / "automation-data" / "realtime_pulse_events.json"

# 监听的目录
WATCH_DIRS = [
    PROJECT_ROOT / "docs" / "reports",  # 完成报告（全角色）
    PROJECT_ROOT / "docs" / "arch",     # 架构文档（架构师）
    PROJECT_ROOT / "apps" / "dashboard" / "automation-data" / "ops",  # 运维日志
    PROJECT_ROOT / "scripts",            # 脚本更新（代码管家）
    PROJECT_ROOT,                        # 根目录（部署脚本）
]

# 角色识别规则
ROLE_PATTERNS = {
    "全栈工程师": ["李明", "REQ-", "TASK-C", "完成报告"],
    "架构师": ["架构师", "ADR-", "审查报告", "ARCH-"],
    "用户": ["用户需求", "USER-"],
    "代码管家": ["代码扫描", "Noah", "代码审查"],
    "运维": ["运维", "DevOps", "incidents", "故障", "SRE"],
    "测试": ["测试", "test", "QA"],
}

class RealtimePulseHandler(FileSystemEventHandler):
    """实时脉动事件处理器（全角色）"""
    
    def __init__(self):
        self.last_events = {}
        self.cooldown = 5  # 冷却时间5秒
    
    def should_process(self, file_path):
        """判断是否应该处理这个文件"""
        now = time.time()
        
        # 忽略备份文件
        if 'backup' in file_path.lower() or file_path.endswith('.pyc'):
            return False
        
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
    
    def identify_role(self, file_name, file_content):
        """识别事件所属角色"""
        for role, patterns in ROLE_PATTERNS.items():
            if any(pattern in file_name for pattern in patterns):
                return role
            if file_content and any(pattern in file_content for pattern in patterns):
                return role
        return "系统"
    
    def process_file_event(self, file_path, action):
        """处理文件事件"""
        file_name = os.path.basename(file_path)
        
        # 读取文件内容（用于角色识别）
        file_content = ""
        try:
            if file_path.endswith('.md') or file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read(500)  # 只读前500字符
        except:
            pass
        
        # 识别角色
        role = self.identify_role(file_name, file_content)
        
        # 判断事件类型
        event_type = None
        category = None
        title = None
        description = None
        tags = []
        actor = role
        task_id = None
        
        # 完成报告
        if "完成报告" in file_name:
            event_type = "task_complete"
            category = "任务"
            title = f"任务完成报告: {file_name.replace('.md', '')}"
            description = f"{role}提交了任务完成报告，等待架构师审查。"
            tags = ["任务完成", "待审查", role]
            
            # 提取任务ID
            if "REQ-" in file_name:
                task_id = file_name.split("REQ-")[1].split("-")[0]
                task_id = f"REQ-{task_id}"
        
        # 审查报告
        elif "审查报告" in file_name:
            event_type = "code_review"
            category = "审查"
            title = f"代码审查: {file_name.replace('.md', '')}"
            description = f"架构师完成了代码审查，生成审查报告。"
            tags = ["代码审查", "架构师", "质量把控"]
        
        # 交接文档
        elif "交接" in file_name:
            event_type = "handoff"
            category = "交接"
            title = f"项目交接: {file_name.replace('.md', '')}"
            description = f"生成项目交接文档，包含完整的知识传承内容。"
            tags = ["交接", "知识传承"]
        
        # 部署脚本
        elif any(p in file_name for p in ["启动", ".bat", ".sh"]) and "部署" in file_name:
            event_type = "deployment"
            category = "部署"
            title = f"部署脚本更新: {file_name}"
            description = f"创建或更新了部署脚本，准备部署到生产环境。"
            tags = ["部署", "脚本"]
        
        # 测试文件
        elif "测试" in file_name or "test" in file_name.lower():
            event_type = "test"
            category = "测试"
            title = f"测试更新: {file_name}"
            description = f"测试文件更新，可能包含新的测试用例或测试结果。"
            tags = ["测试", role]
        
        # 运维日志
        elif "incidents" in file_path or "故障" in file_name:
            event_type = "incident"
            category = "事故"
            role = "运维"
            actor = "SRE"
            title = f"运维事件记录: {file_name}"
            description = f"运维工程师记录了系统事件或故障处理过程。"
            tags = ["运维", "事故处理"]
        
        # 代码扫描
        elif "scan" in file_name.lower() or "扫描" in file_name:
            event_type = "code_scan"
            category = "扫描"
            role = "代码管家"
            actor = "Noah"
            title = f"代码扫描: {file_name}"
            description = f"代码管家执行了项目代码扫描，识别功能和问题。"
            tags = ["代码扫描", "功能识别"]
        
        # 如果识别到了事件，添加到JSON
        if event_type and title:
            self.add_pulse_event(
                role=role,
                actor=actor,
                event_type=event_type,
                category=category,
                title=title,
                description=description,
                tags=tags,
                task_id=task_id,
                metadata={
                    "file": file_name,
                    "action": action,
                    "path": file_path
                }
            )
    
    def add_pulse_event(self, role, actor, event_type, category, title, description, tags, task_id, metadata):
        """添加事件到realtime_pulse_events.json"""
        try:
            # 读取现有数据
            with open(PULSE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            events = data.get("events", [])
            
            # 生成新事件ID
            event_id = f"pulse-{str(len(events) + 1).zfill(3)}"
            
            # 构建新事件
            new_event = {
                "id": event_id,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "role": role,
                "actor": actor,
                "type": event_type,
                "category": category,
                "title": title,
                "description": description,
                "tags": tags,
                "task_id": task_id
            }
            
            # 添加到列表
            events.append(new_event)
            
            # 更新统计
            stats = self.calculate_stats(events)
            data["events"] = events
            data["stats"] = stats
            
            # 写入文件
            with open(PULSE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ [{role}] 事件已记录: {title}")
            
        except Exception as e:
            print(f"❌ 添加事件失败: {e}")
    
    def calculate_stats(self, events):
        """计算统计数据"""
        today = datetime.now().strftime("%Y-%m-%d")
        today_events = [e for e in events if e["timestamp"].startswith(today)]
        
        # 按角色统计
        roles = {}
        for event in events:
            role = event.get("role", "未知")
            roles[role] = roles.get(role, 0) + 1
        
        # 按分类统计
        categories = {}
        for event in events:
            category = event.get("category", "其他")
            categories[category] = categories.get(category, 0) + 1
        
        return {
            "total_events": len(events),
            "today_events": len(today_events),
            "roles": roles,
            "categories": categories
        }

def main():
    """主函数"""
    print("="*60)
    print("实时脉动自动监听器（全角色）".center(60))
    print("="*60)
    print()
    print("📁 监听目录:")
    for watch_dir in WATCH_DIRS:
        if watch_dir.exists():
            print(f"   ✅ {watch_dir}")
        else:
            print(f"   ⚠️  {watch_dir} (不存在，跳过)")
    print()
    print(f"💾 脉动文件: {PULSE_FILE}")
    print()
    print("🔍 监听所有角色活动:")
    print("   - 全栈工程师：完成报告、任务ID（REQ-/TASK-）")
    print("   - 架构师：审查报告、架构文档、ADR")
    print("   - 用户：用户需求文档")
    print("   - 代码管家：代码扫描、功能识别")
    print("   - 运维：故障日志、incidents文件")
    print("   - 测试：测试报告、测试用例")
    print()
    print("⏰ 冷却时间: 5秒（防止重复触发）")
    print()
    print("="*60)
    print("🚀 实时脉动监听器已启动，按Ctrl+C停止")
    print("="*60)
    print()
    
    # 创建事件处理器
    event_handler = RealtimePulseHandler()
    
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
        print("⏹️  实时脉动监听器已停止")
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

