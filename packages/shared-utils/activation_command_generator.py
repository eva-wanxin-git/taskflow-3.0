#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
激活指令动态生成器
根据项目信息生成特定的AI角色激活指令
"""

from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class ActivationCommandGenerator:
    """激活指令生成器"""

    def __init__(self, project_info: Dict[str, Any]):
        """
        初始化生成器

        Args:
            project_info: 项目信息字典
                - project_name: 项目名称
                - project_code: 项目代码
                - project_type: 项目类型
                - dashboard_port: Dashboard端口
                - api_port: API端口
                - tech_stack: 技术栈列表
                - project_path: 项目路径
        """
        self.project_info = project_info

    def generate_architect_command(self) -> str:
        """生成架构师激活指令"""
        project_name = self.project_info.get("project_name", "未命名项目")
        project_code = self.project_info.get("project_code", "UNKNOWN")
        project_type = self.project_info.get("project_type", "未知类型")
        port = self.project_info.get("dashboard_port", 8841)
        tech_stack = ", ".join(self.project_info.get("tech_stack", ["检测中"]))

        command = f"""# 🏛️ 架构师激活指令 - {project_name}

你好，我任命你为**{project_name}**项目的架构师AI。

## 📋 项目信息
- **项目名称**: {project_name}
- **项目代码**: {project_code}
- **项目类型**: {project_type}
- **技术栈**: {tech_stack}
- **Dashboard**: http://localhost:{port}
- **知识库**: .taskflow/knowledge.db

## 🎯 立即执行初始化任务

### 任务1: 深度扫描项目 (3-5分钟)
```python
import sys
sys.path.insert(0, "taskflow/apps/dashboard/src")
from automation.project_scanner import ProjectScanner

scanner = ProjectScanner(".")
result = scanner.scan_project()
print(f"✅ 扫描完成: {{result['project_name']}}")
```

### 任务2: 初始化知识库 (1分钟)
```python
from automation.knowledge_base_initializer import KnowledgeBaseInitializer

initializer = KnowledgeBaseInitializer()
kb_result = initializer.initialize_all(result)
print(f"✅ 知识库初始化: {{kb_result['created_files']}}个文件")
```

### 任务3: 创建独立记忆空间 (即时)
```python
import requests

response = requests.post('http://localhost:{port - 1}/api/initialize_memory_space', json={{
    "project_code": "{project_code}",
    "project_id": "读取.taskflow/project_id.txt"
}})
print(f"✅ 记忆空间: {{response.json()}}")
```

### 任务4: 更新Dashboard实时数据 (即时)
```python
import requests

requests.post('http://localhost:{port - 1}/api/update_project_info', json={{
    "project_name": "{project_name}",
    "description": "自动生成的项目描述",
    "tech_stack": {self.project_info.get("tech_stack", [])},
    "estimated_time": "基于扫描计算"
}})
```

### 任务5: 生成任务看板
创建 `docs/tasks/task-board.md`，包含：
- 项目总览
- 第一批任务（基于扫描结果）
- 优先级排序

## 🔗 MCP记忆系统

**Session Memory Namespace**: `{project_code}_sessions`
**Ultra Memory Namespace**: `{project_code}_ultra`
**可访问历史记忆**: `wanxin_ultra` (10501条参考记忆)

## ✅ 完成标准

完成后请回复: "✅ {project_name} 架构师初始化完成"

并确认：
- [ ] 项目扫描报告已生成
- [ ] knowledge.db已填充组件数据
- [ ] Dashboard显示真实项目信息
- [ ] 独立记忆空间已创建
- [ ] 任务看板已生成

---
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return command

    def generate_engineer_command(self) -> str:
        """生成全栈工程师激活指令"""
        project_name = self.project_info.get("project_name", "未命名项目")
        project_code = self.project_info.get("project_code", "UNKNOWN")
        port = self.project_info.get("dashboard_port", 8841)

        command = f"""# 👨‍💻 全栈工程师激活指令 - {project_name}

你好，我任命你为**{project_name}**项目的全栈工程师AI。

## 📋 项目信息
- **项目名称**: {project_name}
- **项目代码**: {project_code}
- **Dashboard**: http://localhost:{port}
- **架构师**: 已完成初始化

## 🎯 工作模式

### 模式1: 接收任务
从Dashboard任务看板获取任务：
```
用户会从 http://localhost:{port} 复制任务提示词给你
你需要：
1. 确认接受任务
2. 开始执行
3. 报告进度
4. 完成后标记
```

### 模式2: 主动查询
查看待处理任务：
```python
import requests
response = requests.get('http://localhost:{port - 1}/api/engineer/tasks?status=pending')
tasks = response.json()['tasks']
```

### 模式3: 报告进度
```python
requests.post('http://localhost:{port - 1}/api/engineer/tasks/{{task_id}}/progress', json={{
    "status": "in_progress",
    "progress_pct": 50,
    "notes": "已完成数据库设计"
}})
```

## 🔗 MCP记忆系统
- **Session Memory**: 自动记录对话
- **Ultra Memory**: 保存重要方案

## ✅ 准备就绪

回复: "✅ 全栈工程师已就位，等待任务"

---
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return command

    def generate_all_commands(self) -> Dict[str, str]:
        """生成所有角色的激活指令"""
        return {
            "architect": self.generate_architect_command(),
            "engineer": self.generate_engineer_command(),
            "ui_designer": self._generate_ui_designer_command(),
            "ux_designer": self._generate_ux_designer_command(),
            "devops": self._generate_devops_command()
        }

    def _generate_ui_designer_command(self) -> str:
        """生成UI设计师激活指令"""
        project_name = self.project_info.get("project_name", "未命名项目")

        return f"""# 🎨 UI设计师激活指令 - {project_name}

你好，我任命你为**{project_name}**项目的UI设计师AI。

## 🎯 设计规范
- 遵循Blanc Luxury设计系统
- 工业极简美学
- 高对比度、易读性

## 📋 工作内容
1. 设计组件UI
2. 优化视觉呈现
3. 确保设计一致性

回复: "✅ UI设计师已就位"
"""

    def _generate_ux_designer_command(self) -> str:
        """生成UX设计师激活指令"""
        project_name = self.project_info.get("project_name", "未命名项目")

        return f"""# 🎭 UX设计师激活指令 - {project_name}

你好，我任命你为**{project_name}**项目的UX设计师AI。

## 🎯 交互原则
- 用户体验优先
- 流畅的交互流程
- 清晰的反馈机制

## 📋 工作内容
1. 设计用户流程
2. 优化交互体验
3. 提供UX建议

回复: "✅ UX设计师已就位"
"""

    def _generate_devops_command(self) -> str:
        """生成运维工程师激活指令"""
        project_name = self.project_info.get("project_name", "未命名项目")

        return f"""# 🔧 运维工程师激活指令 - {project_name}

你好，我任命你为**{project_name}**项目的运维工程师AI。

## 🎯 运维职责
- 部署管理
- 监控告警
- 故障排查

## 📋 工作内容
1. 配置CI/CD
2. 部署到各环境
3. 监控系统健康
4. 处理运维问题

回复: "✅ 运维工程师已就位"
"""


# 测试
if __name__ == "__main__":
    # 示例项目信息
    project_info = {
        "project_name": "测试项目",
        "project_code": "TEST_PROJECT",
        "project_type": "Python + React全栈",
        "dashboard_port": 8841,
        "api_port": 8840,
        "tech_stack": ["Python", "FastAPI", "React", "PostgreSQL"],
        "project_path": "/path/to/test-project"
    }

    generator = ActivationCommandGenerator(project_info)

    print("="*70)
    print("激活指令生成器测试")
    print("="*70)

    print("\n【架构师激活指令】")
    print("-"*70)
    print(generator.generate_architect_command())

    print("\n【全栈工程师激活指令】")
    print("-"*70)
    print(generator.generate_engineer_command())

