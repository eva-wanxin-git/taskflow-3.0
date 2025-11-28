#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
架构师创建任务工具
快速创建并分配任务给全栈工程师
"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

def create_task(
    task_id: str,
    title: str,
    description: str,
    priority: str = "P1",
    estimated_hours: float = 3.0,
    complexity: str = "medium",
    tags: list = None,
    parallel: bool = False,
    assigned_to: str = "fullstack-engineer"
):
    """
    创建新任务
    
    参数:
        task_id: 任务ID，如 TASK-FE-101
        title: 任务标题
        description: 任务详细描述
        priority: 优先级 P0/P1/P2/P3
        estimated_hours: 预估工时（小时）
        complexity: 复杂度 low/medium/high
        tags: 标签列表
        parallel: 是否可并行
        assigned_to: 分配给谁
    """
    
    db_path = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
    
    if not db_path.exists():
        print(f"❌ 数据库不存在: {db_path}")
        return False
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 检查任务ID是否已存在
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    if cursor.fetchone():
        print(f"❌ 任务ID已存在: {task_id}")
        conn.close()
        return False
    
    # 构建metadata
    metadata = {
        "tags": tags or [],
        "parallel": parallel,
        "created_by": "architect",
        "source": "manual"
    }
    
    try:
        cursor.execute("""
            INSERT INTO tasks (
                id, title, description, status, priority,
                estimated_hours, complexity, assigned_to,
                created_at, updated_at, metadata
            ) VALUES (?, ?, ?, 'pending', ?, ?, ?, ?, 
                      datetime('now'), datetime('now'), ?)
        """, (
            task_id, 
            title, 
            description, 
            priority,
            estimated_hours, 
            complexity, 
            assigned_to,
            json.dumps(metadata, ensure_ascii=False)
        ))
        
        conn.commit()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ 任务创建成功！".center(60))
        print("="*60)
        print(f"\n任务ID: {task_id}")
        print(f"标题: {title}")
        print(f"优先级: {priority}")
        print(f"预估工时: {estimated_hours}小时")
        print(f"复杂度: {complexity}")
        print(f"可并行: {'是 ✅' if parallel else '否'}")
        print(f"分配给: {assigned_to}")
        print(f"创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n" + "="*60)
        
        # 生成提示词
        generate_task_prompt(task_id, title, description, priority, estimated_hours, parallel)
        
        return True
        
    except Exception as e:
        print(f"❌ 创建任务失败: {e}")
        conn.close()
        return False


def generate_task_prompt(task_id, title, description, priority, hours, parallel):
    """生成任务提示词"""
    
    prompt = f"""# 📤 派发给全栈工程师 - {task_id}

**派发时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**派发人**: AI架构师 (Expert Level)  
**接收人**: 全栈工程师  
**优先级**: {priority}  
**预估工时**: {hours}小时  
**是否可并行**: {'是 ✅' if parallel else '否'}

---

## 🚀 第一步：接受任务（必做！）

请打开 Dashboard: http://localhost:8831

1. 进入"全栈工程师工作台"
2. 点击"任务看板" Tab
3. 找到任务卡片 `{task_id}`
4. 点击"✅ 接受任务"按钮

---

## 📋 任务详情

### 任务描述
{description}

### 验收标准
- [ ] 功能完整实现
- [ ] 代码质量良好
- [ ] 自测通过
- [ ] 文档完整

---

## 📝 完成后提交

1. 点击"✅ 提交完成"按钮
2. 填写实际工时和完成说明
3. 点击"复制完成报告"
4. 提交给架构师审查

---

**祝开发顺利！** 💪
"""
    
    # 保存提示词到文件
    prompt_file = Path(__file__).parent.parent / f"📤派发给全栈工程师-{task_id}.md"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"\n✅ 任务提示词已生成: {prompt_file.name}")
    print(f"\n📋 复制以下内容发给全栈工程师：\n")
    print(prompt)
    print("\n" + "="*60 + "\n")


# ============================================
# 示例使用
# ============================================

if __name__ == "__main__":
    print("\n🎯 架构师创建任务工具\n")
    
    # 示例1: 创建前端任务（可并行）
    create_task(
        task_id="TASK-FE-999",
        title="实现用户头像上传功能",
        description="""
实现用户个人中心的头像上传功能。

【功能需求】
1. 点击头像打开文件选择器
2. 支持图片预览
3. 上传到服务器
4. 更新显示

【技术要求】
- 使用HTML5 File API
- 图片压缩（≤500KB）
- 支持裁剪
- 调用 POST /api/upload 接口

【验收标准】
- [ ] 可以选择图片
- [ ] 实时预览
- [ ] 上传成功
- [ ] 头像更新
""",
        priority="P2",
        estimated_hours=3.0,
        complexity="medium",
        tags=["frontend", "upload", "ui"],
        parallel=True
    )

