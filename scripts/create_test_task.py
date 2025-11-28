#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
创建一个简单的测试任务
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

# 连接数据库
db_path = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# 创建测试任务
task_id = "TEST-2025-001"
title = "测试任务：验证任务看板功能"
description = """这是一个测试任务，用于验证任务看板的完整功能。

【测试目标】
1. 验证任务卡片动态加载
2. 验证复制提示词功能
3. 验证状态流转（待处理 → 进行中 → 已完成）
4. 验证详情弹窗显示

【执行步骤】
1. 在Dashboard任务看板找到此任务
2. 点击"复制提示词"按钮
3. 验证提示词复制成功
4. 验证任务状态自动变为"进行中"
5. 点击"提交完成"
6. 填写实际工时：0.5小时
7. 验证任务移到"已完成"栏
8. 点击"复制完成报告"

【验收标准】
- [ ] 所有功能正常
- [ ] 状态流转正确
- [ ] UI显示正确
"""

metadata = json.dumps({
    "tags": ["test", "frontend", "验证"],
    "parallel": True,
    "created_by": "architect",
    "test": True
}, ensure_ascii=False)

cursor.execute("""
    INSERT INTO tasks (
        id, title, description, status, priority,
        estimated_hours, complexity, assigned_to,
        created_at, updated_at, metadata
    ) VALUES (?, ?, ?, 'pending', ?, ?, ?, 'fullstack-engineer',
              datetime('now'), datetime('now'), ?)
""", (task_id, title, description, 'P0', 1.0, 'low', metadata))

conn.commit()
conn.close()

print("="*70)
print("✅ 测试任务创建成功！".center(70))
print("="*70)
print(f"\n任务ID: {task_id}")
print(f"标题: {title}")
print(f"优先级: P0（最高优先级，排在最前面）")
print(f"预估: 1小时")
print(f"可并行: 是 ✅")
print(f"状态: 待处理\n")
print("="*70)
print("\n📋 任务提示词：\n")

prompt = f"""# 📤 派发给全栈工程师 - {task_id}

**派发时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**派发人**: AI架构师 (Expert Level)  
**优先级**: P0（测试任务）  
**预估工时**: 1小时  
**是否可并行**: 是

---

## 📋 任务描述

{description}

---

## 🚀 测试步骤

1. 在Dashboard找到此任务（应该在最前面，P0优先级）
2. 点击"复制提示词" → 验证提示词复制成功
3. 验证任务自动变为"进行中"
4. 点击"提交完成" → 填写0.5小时
5. 验证任务移到"已完成"
6. 点击"复制完成报告"

---

**这是测试任务，验证完成后即可！** ✅
"""

print(prompt)
print("\n" + "="*70)

# 保存提示词
prompt_file = Path(__file__).parent.parent / f"📤派发给全栈工程师-{task_id}.md"
with open(prompt_file, 'w', encoding='utf-8') as f:
    f.write(prompt)

print(f"✅ 提示词已保存: {prompt_file.name}\n")

