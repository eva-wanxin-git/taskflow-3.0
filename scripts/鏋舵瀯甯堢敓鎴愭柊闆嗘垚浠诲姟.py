#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
架构师生成新集成任务
根据代码检查结果，生成缺失功能的任务并录入数据库
"""
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "database/data/tasks.db"

def create_task(task_id, title, description, priority, estimated_hours, assigned_to="fullstack-engineer"):
    """创建新任务"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO tasks (
                id, title, description, status, priority,
                estimated_hours, assigned_to, created_at, updated_at, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            task_id,
            title,
            description,
            'pending',
            priority,
            estimated_hours,
            assigned_to,
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            '{}'
        ))
        conn.commit()
        print(f"  ✓ 创建任务: {task_id} - {title}")
        return True
    except sqlite3.IntegrityError:
        print(f"  - 跳过: {task_id} - {title} (已存在)")
        return False
    except Exception as e:
        print(f"  ✗ 错误: {task_id} - {e}")
        return False
    finally:
        conn.close()

def main():
    """主函数"""
    print("\n" + "="*70)
    print("架构师生成新集成任务")
    print("="*70)
    print()
    
    print("[检查结果]")
    print("  1. Dashboard事件流Tab: ✅ 已存在（基础版）")
    print("  2. Dashboard记忆空间Tab: ❌ 未实现")
    print("  3. 自动化看板刷新脚本: ❌ 未实现")
    print()
    
    print("[生成任务]")
    print()
    
    # 任务1: Dashboard记忆空间Tab
    created = create_task(
        task_id="TASK-UI-001",
        title="实现Dashboard项目记忆空间Tab",
        description="""
## 任务描述
在Dashboard中新增"项目记忆空间"Tab，展示和管理项目记忆。

## 背景
- REQ-002项目记忆空间已完成 ✅
- API已完整实现（project_memory.py，11个端点）✅
- 缺少Dashboard UI展示 ❌

## 技术要点
在templates.py中新增Tab，包含：
1. 记忆列表展示（按类型/分类筛选）
2. 创建记忆表单（标题/内容/标签/重要性）
3. 记忆详情展开
4. 相关记忆展示
5. 语义搜索功能

## API端点
- GET /api/projects/TASKFLOW/memories
- POST /api/projects/TASKFLOW/memories
- GET /api/projects/TASKFLOW/knowledge/inherit

## 验收标准
- [ ] Tab切换正常
- [ ] 记忆列表显示
- [ ] 可以创建新记忆
- [ ] 可以搜索记忆
- [ ] UI风格符合工业美学

## 参考
- 其他Tab的实现方式
- project_memory.py的API定义
        """,
        priority="P1",
        estimated_hours=3.0,
        assigned_to="fullstack-engineer"
    )
    
    # 任务2: 自动化看板刷新脚本
    created = create_task(
        task_id="TASK-AUTO-001",
        title="实现自动化看板刷新脚本",
        description="""
## 任务描述
创建自动化脚本，定期从事件流和数据库拉取最新状态，自动更新docs/tasks/task-board.md。

## 背景
- 手动更新看板效率低，容易遗漏
- 事件流已记录所有状态变更
- 需要自动化机制同步看板

## 技术要点
新建：services/task_board_auto_sync.py

功能包括：
1. 从事件流读取最新事件（task.created/completed/status_changed）
2. 从数据库查询任务最新状态
3. 对比看板内容和实际状态
4. 自动更新看板markdown：
   - 任务完成 → 标记✅并移动到已完成区
   - 任务开始 → 标记🔄并移动到进行中区
   - 新任务创建 → 添加到待处理区
5. 保存看板并记录更新日志

## 运行方式
- 方式1: 定时任务（cron/scheduler）每10分钟运行一次
- 方式2: 手动触发：python services/task_board_auto_sync.py
- 方式3: API触发：POST /api/task-board/sync

## 验收标准
- [ ] 脚本可以正常运行
- [ ] 能检测出看板和数据库的不一致
- [ ] 能自动更新看板markdown
- [ ] 更新日志清晰
- [ ] 不会破坏看板格式

## 注意事项
- 看板markdown格式要保持
- 只更新任务状态，不改其他内容
- 添加备份机制（更新前备份）
- 添加冲突检测（如果手动编辑中）
        """,
        priority="P1",
        estimated_hours=2.0,
        assigned_to="fullstack-engineer"
    )
    
    # 任务3: 完善Dashboard事件流Tab
    created = create_task(
        task_id="TASK-UI-002",
        title="完善Dashboard事件流Tab（增强版）",
        description="""
## 任务描述
完善现有的Dashboard事件流Tab，添加筛选、搜索和详情展开功能。

## 背景
- 事件流Tab已存在 ✅ (基础版)
- 事件流API已完整 ✅（7个端点）
- 需要增强功能 ⏳

## 当前功能（已有）
- ✅ 基础事件流展示
- ✅ 事件列表显示

## 需要新增功能
1. **筛选器**
   - 按类型筛选（task/issue/decision/deployment/system）
   - 按严重性筛选（info/warning/error/critical）
   - 按时间范围筛选（今日/本周/本月/自定义）
   - 按操作者筛选（AI Architect/fullstack-engineer/system）

2. **搜索功能**
   - 关键词搜索（标题/描述）
   - 按实体ID搜索（查找某任务的所有事件）

3. **事件详情**
   - 点击事件展开详情
   - 显示完整data字段（JSON格式化）
   - 显示关联实体链接

4. **统计图表**
   - 事件数量趋势图
   - 按类型分布饼图
   - 按严重性分布

5. **实时更新**
   - 自动刷新（每30秒）
   - 或WebSocket实时推送

## API端点（已有）
- GET /api/events/stream
- GET /api/events/stats
- GET /api/events/categories
- GET /api/events/severities
- GET /api/events/actors
- GET /api/events/search
- GET /api/events/recent

## 验收标准
- [ ] 筛选器正常工作
- [ ] 搜索功能正常
- [ ] 事件详情可展开
- [ ] 统计图表显示
- [ ] 实时更新正常
- [ ] UI符合工业美学

## 参考
- Dashboard现有的筛选器实现（任务清单Tab）
- 事件流API的完整能力
        """,
        priority="P2",
        estimated_hours=3.0,
        assigned_to="fullstack-engineer"
    )
    
    # 总结
    print()
    print("="*70)
    print("✅ 新任务生成完成")
    print("="*70)
    print()
    print("已创建任务:")
    print("  1. TASK-UI-001: Dashboard项目记忆空间Tab（3h, P1）")
    print("  2. TASK-AUTO-001: 自动化看板刷新脚本（2h, P1）")
    print("  3. TASK-UI-002: 完善Dashboard事件流Tab（3h, P2）")
    print()
    print("总工时: 8小时")
    print()
    print("下一步:")
    print("  1. 看板会在Dashboard刷新后显示新任务")
    print("  2. 派发给其他Cursor窗口执行")
    print("  3. 执行前运行: python scripts/李明收到任务.py TASK-UI-001")
    print()
    print("="*70)

if __name__ == "__main__":
    main()

