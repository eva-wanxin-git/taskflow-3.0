#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化看板刷新脚本 (TASK-AUTO-001)

功能:
1. 从事件流读取最新事件（task.created/completed/status_changed）
2. 从数据库查询任务最新状态
3. 对比看板内容和实际状态
4. 自动更新看板markdown
5. 保存看板并记录更新日志

运行方式:
- 方式1: 定时任务（cron/scheduler）每10分钟运行一次
- 方式2: 手动触发：python services/task_board_auto_sync.py
- 方式3: API触发：POST /api/task-board/sync
"""

import sqlite3
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys
import shutil

# 添加core-domain到路径
core_domain_path = Path(__file__).resolve().parent.parent / "packages" / "core-domain" / "src"
if str(core_domain_path) not in sys.path:
    sys.path.insert(0, str(core_domain_path))

from services.event_service import EventStore


class TaskBoardAutoSync:
    """任务看板自动同步器"""
    
    def __init__(self, project_root: Path = None):
        """
        初始化同步器
        
        Args:
            project_root: 项目根目录路径
        """
        if project_root is None:
            project_root = Path(__file__).resolve().parent.parent
        
        self.project_root = project_root
        self.db_path = project_root / "database/data/tasks.db"
        self.board_path = project_root / "docs/tasks/task-board.md"
        self.backup_dir = project_root / "docs/tasks/backups"
        self.log_file = project_root / "docs/tasks/sync_log.json"
        
        # 确保备份目录存在
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化事件存储
        self.event_store = EventStore(db_path=str(self.db_path))
        
        # 状态映射
        self.status_emoji = {
            "pending": "⏳",
            "in_progress": "🔄",
            "completed": "✅",
            "cancelled": "❌",
            "blocked": "🚫"
        }
    
    def backup_board(self) -> Path:
        """
        备份当前看板
        
        Returns:
            备份文件路径
        """
        if not self.board_path.exists():
            print(f"⚠️  看板文件不存在: {self.board_path}")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"task-board_{timestamp}.md"
        
        shutil.copy2(self.board_path, backup_path)
        print(f"✅ 已备份看板: {backup_path.name}")
        
        return backup_path
    
    def check_file_lock(self) -> bool:
        """
        检查文件是否被锁定（正在编辑中）
        
        Returns:
            True表示文件可以修改，False表示被锁定
        """
        # 简单实现：检查是否存在.lock文件
        lock_file = self.board_path.with_suffix(".md.lock")
        
        if lock_file.exists():
            # 检查锁文件是否过期（超过5分钟）
            lock_time = datetime.fromtimestamp(lock_file.stat().st_mtime)
            if (datetime.now() - lock_time).total_seconds() > 300:
                # 锁文件过期，删除它
                lock_file.unlink()
                print("🔓 已清除过期的锁文件")
                return True
            else:
                print("⚠️  看板文件正在被编辑，跳过本次同步")
                return False
        
        return True
    
    def get_tasks_from_db(self) -> List[Dict]:
        """
        从数据库获取所有任务
        
        Returns:
            任务列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, title, description, status, priority,
                estimated_hours, actual_hours, complexity,
                assigned_to, created_at, updated_at, metadata
            FROM tasks
            ORDER BY 
                CASE priority
                    WHEN 'P0' THEN 0
                    WHEN 'P1' THEN 1
                    WHEN 'P2' THEN 2
                    WHEN 'P3' THEN 3
                    ELSE 4
                END,
                created_at DESC
        """)
        
        tasks = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return tasks
    
    def get_recent_events(self, limit: int = 100) -> List[Dict]:
        """
        获取最近的任务相关事件
        
        Args:
            limit: 获取事件数量
            
        Returns:
            事件列表
        """
        events = self.event_store.query(
            event_type=None,  # 获取所有类型
            category="task",   # 只要任务相关的
            limit=limit,
            order_by="occurred_at",
            order_direction="DESC"
        )
        
        return events
    
    def parse_board_tasks(self) -> Dict[str, Dict]:
        """
        解析看板中的任务信息
        
        Returns:
            任务字典 {task_id: {status, section, line_number}}
        """
        if not self.board_path.exists():
            return {}
        
        with open(self.board_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tasks = {}
        current_section = None
        
        # 定义各个区域的标记
        sections = {
            "completed": ["### ✅ 已完成任务", "#### 核心需求（REQ系列）", "#### 集成任务（INTEGRATE系列）"],
            "in_progress": ["### 🔴 高优先级待处理任务", "#### 🔄 进行中"],
            "pending": ["#### ⏳ P0任务清单", "### 🟡 普通优先级任务", "### 🟢 低优先级任务"],
            "cancelled": ["### ❌ 已取消任务"]
        }
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            # 检测当前所在区域
            for status, markers in sections.items():
                for marker in markers:
                    if marker in line:
                        current_section = status
                        break
            
            # 匹配任务行（支持多种格式）
            # 格式1: **TASK-ID** ✅ 任务标题
            # 格式2: 1. **REQ-001** ✅ 任务标题
            # 格式3: - **TASK-ID** ⏳ 任务标题
            task_match = re.search(r'\*\*([A-Z]+-[A-Z0-9-]+)\*\*\s*([✅⏳🔄❌🚫])', line)
            
            if task_match and current_section:
                task_id = task_match.group(1)
                emoji = task_match.group(2)
                
                # 根据emoji判断状态
                status_from_emoji = None
                for status, status_emoji in self.status_emoji.items():
                    if emoji == status_emoji:
                        status_from_emoji = status
                        break
                
                tasks[task_id] = {
                    "status": status_from_emoji or current_section,
                    "section": current_section,
                    "line_number": i,
                    "original_line": line
                }
        
        return tasks
    
    def detect_inconsistencies(self) -> List[Dict]:
        """
        检测看板与数据库的不一致
        
        Returns:
            不一致列表 [{task_id, db_status, board_status, action}]
        """
        db_tasks = {task['id']: task for task in self.get_tasks_from_db()}
        board_tasks = self.parse_board_tasks()
        
        inconsistencies = []
        
        # 检查数据库中的任务在看板中的状态
        for task_id, db_task in db_tasks.items():
            db_status = db_task['status']
            
            if task_id in board_tasks:
                board_status = board_tasks[task_id]['status']
                
                if db_status != board_status:
                    inconsistencies.append({
                        "task_id": task_id,
                        "title": db_task['title'],
                        "db_status": db_status,
                        "board_status": board_status,
                        "action": "update_status",
                        "line_number": board_tasks[task_id]['line_number']
                    })
            else:
                # 任务在数据库中但不在看板中
                inconsistencies.append({
                    "task_id": task_id,
                    "title": db_task['title'],
                    "db_status": db_status,
                    "board_status": None,
                    "action": "add_to_board",
                    "priority": db_task['priority'],
                    "estimated_hours": db_task['estimated_hours']
                })
        
        return inconsistencies
    
    def update_task_status_in_board(self, task_id: str, new_status: str) -> bool:
        """
        更新看板中某个任务的状态
        
        Args:
            task_id: 任务ID
            new_status: 新状态
            
        Returns:
            是否成功更新
        """
        if not self.board_path.exists():
            return False
        
        with open(self.board_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找任务行并更新emoji
        old_emoji_pattern = r'(\*\*' + re.escape(task_id) + r'\*\*\s*)([✅⏳🔄❌🚫])'
        new_emoji = self.status_emoji.get(new_status, "⏳")
        
        # 替换emoji
        updated_content = re.sub(
            old_emoji_pattern,
            r'\1' + new_emoji,
            content
        )
        
        if updated_content != content:
            with open(self.board_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            return True
        
        return False
    
    def add_task_to_board(self, task: Dict) -> bool:
        """
        将新任务添加到看板
        
        Args:
            task: 任务信息
            
        Returns:
            是否成功添加
        """
        if not self.board_path.exists():
            return False
        
        with open(self.board_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 根据状态和优先级确定插入位置
        status = task['status']
        priority = task.get('priority', 'P2')
        
        # 查找合适的区域标题
        section_markers = {
            "completed": "### ✅ 已完成任务",
            "in_progress": "#### 🔄 进行中",
            "pending": "#### ⏳ P0任务清单" if priority == "P0" else "### 🟡 普通优先级任务"
        }
        
        marker = section_markers.get(status, "### 🟡 普通优先级任务")
        
        # 查找插入位置
        insert_index = None
        for i, line in enumerate(lines):
            if marker in line:
                # 找到区域标题，在下一个空行后插入
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() == "":
                        insert_index = j + 1
                        break
                break
        
        if insert_index is None:
            print(f"⚠️  未找到合适的插入位置: {marker}")
            return False
        
        # 构建任务行
        emoji = self.status_emoji.get(status, "⏳")
        estimated = task.get('estimated_hours', 0)
        assigned = task.get('assigned_to', 'unassigned')
        
        task_line = f"\n**{task['id']}** {emoji} {task['title']} ({estimated}h)\n"
        task_line += f"   - 执行者: {assigned}\n"
        
        # 插入任务
        lines.insert(insert_index, task_line)
        
        # 写回文件
        with open(self.board_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return True
    
    def update_statistics(self) -> bool:
        """
        更新看板中的统计数据
        
        Returns:
            是否成功更新
        """
        if not self.board_path.exists():
            return False
        
        # 获取统计数据
        tasks = self.get_tasks_from_db()
        total = len(tasks)
        completed = len([t for t in tasks if t['status'] == 'completed'])
        in_progress = len([t for t in tasks if t['status'] == 'in_progress'])
        pending = len([t for t in tasks if t['status'] == 'pending'])
        cancelled = len([t for t in tasks if t['status'] == 'cancelled'])
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        # 读取看板内容
        with open(self.board_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新统计数据（使用正则表达式替换）
        # 更新总任务数
        content = re.sub(
            r'- \*\*总任务\*\*: \d+个',
            f'- **总任务**: {total}个',
            content
        )
        
        # 更新已完成数
        content = re.sub(
            r'- \*\*已完成\*\*: \d+个 \(\d+\.?\d*%\) ✅',
            f'- **已完成**: {completed}个 ({completion_rate:.1f}%) ✅',
            content
        )
        
        # 更新进行中数
        content = re.sub(
            r'- \*\*进行中\*\*: \d+个',
            f'- **进行中**: {in_progress}个',
            content
        )
        
        # 更新待处理数
        content = re.sub(
            r'- \*\*待处理\*\*: \d+个',
            f'- **待处理**: {pending}个',
            content
        )
        
        # 更新已取消数
        content = re.sub(
            r'- \*\*已取消\*\*: \d+个',
            f'- **已取消**: {cancelled}个',
            content
        )
        
        # 更新进度条
        progress_bar_length = 30
        filled = int(progress_bar_length * completion_rate / 100)
        empty = progress_bar_length - filled
        progress_bar = "█" * filled + "░" * empty
        
        content = re.sub(
            r'\[█*░*\] \d+\.?\d*% 完成',
            f'[{progress_bar}] {completion_rate:.1f}% 完成',
            content
        )
        
        # 更新时间戳
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        content = re.sub(
            r'\*\*更新时间\*\*: \d{4}-\d{2}-\d{2} \d{2}:\d{2}',
            f'**更新时间**: {now}',
            content
        )
        
        # 写回文件
        with open(self.board_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    def log_sync_result(self, inconsistencies: List[Dict], success: bool):
        """
        记录同步结果
        
        Args:
            inconsistencies: 不一致列表
            success: 是否成功
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "inconsistencies_found": len(inconsistencies),
            "inconsistencies": inconsistencies,
            "tasks_updated": len([i for i in inconsistencies if i['action'] == 'update_status']),
            "tasks_added": len([i for i in inconsistencies if i['action'] == 'add_to_board'])
        }
        
        # 读取现有日志
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        
        # 添加新日志
        logs.append(log_entry)
        
        # 只保留最近100条日志
        logs = logs[-100:]
        
        # 写回日志文件
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    
    def sync(self) -> Dict:
        """
        执行同步
        
        Returns:
            同步结果 {success, message, details}
        """
        print("\n" + "=" * 70)
        print("🔄 任务看板自动同步")
        print("=" * 70)
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"看板: {self.board_path}")
        print(f"数据库: {self.db_path}")
        print()
        
        # 1. 检查文件锁
        if not self.check_file_lock():
            result = {
                "success": False,
                "message": "看板文件正在被编辑，跳过同步",
                "details": {}
            }
            self.log_sync_result([], False)
            return result
        
        # 2. 备份看板
        backup_path = self.backup_board()
        
        # 3. 检测不一致
        print("🔍 检测看板与数据库的不一致...")
        inconsistencies = self.detect_inconsistencies()
        
        if not inconsistencies:
            print("✅ 看板与数据库完全一致，无需更新")
            result = {
                "success": True,
                "message": "看板已是最新状态",
                "details": {
                    "inconsistencies": 0,
                    "updated": 0,
                    "added": 0
                }
            }
            self.log_sync_result([], True)
            return result
        
        print(f"⚠️  发现 {len(inconsistencies)} 处不一致")
        print()
        
        # 4. 应用更新
        updated_count = 0
        added_count = 0
        
        for item in inconsistencies:
            if item['action'] == 'update_status':
                print(f"  📝 更新 {item['task_id']}: {item['board_status']} → {item['db_status']}")
                if self.update_task_status_in_board(item['task_id'], item['db_status']):
                    updated_count += 1
            
            elif item['action'] == 'add_to_board':
                print(f"  ➕ 添加 {item['task_id']}: {item['title']}")
                # 获取完整任务信息
                tasks = self.get_tasks_from_db()
                task = next((t for t in tasks if t['id'] == item['task_id']), None)
                if task and self.add_task_to_board(task):
                    added_count += 1
        
        print()
        
        # 5. 更新统计数据
        print("📊 更新统计数据...")
        self.update_statistics()
        
        # 6. 记录日志
        self.log_sync_result(inconsistencies, True)
        
        print()
        print("=" * 70)
        print("✅ 同步完成")
        print("=" * 70)
        print(f"更新任务: {updated_count} 个")
        print(f"添加任务: {added_count} 个")
        print(f"备份文件: {backup_path.name if backup_path else 'N/A'}")
        print()
        
        result = {
            "success": True,
            "message": f"成功同步 {updated_count + added_count} 个任务",
            "details": {
                "inconsistencies": len(inconsistencies),
                "updated": updated_count,
                "added": added_count,
                "backup": str(backup_path) if backup_path else None
            }
        }
        
        return result


def main():
    """主函数"""
    syncer = TaskBoardAutoSync()
    result = syncer.sync()
    
    # 返回退出码
    sys.exit(0 if result['success'] else 1)


if __name__ == "__main__":
    main()

