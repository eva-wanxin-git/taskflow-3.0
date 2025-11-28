#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
架构师任务：更新项目透视数据
生成4个JSON文件供Dashboard使用
"""
import json
from pathlib import Path
from datetime import datetime

# 项目根目录
project_root = Path(__file__).parent.parent
data_dir = project_root / "apps" / "dashboard" / "automation-data"

# 确保目录存在
data_dir.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("架构师任务：更新项目透视数据")
print("=" * 70)
print()

# ============================================================
# Tab 1: 已实现功能（132个）- 已存在，验证即可
# ============================================================
print("Tab 1: 已实现功能清单")
features_file = data_dir / "v17-complete-features.json"
if features_file.exists():
    with open(features_file, 'r', encoding='utf-8') as f:
        features = json.load(f)
    print(f"  [OK] 已存在: {len(features.get('implemented', []))}个功能")
else:
    print(f"  [WARN] 文件不存在: {features_file}")
print()

# ============================================================
# Tab 2: 部分实现功能（17个）
# ============================================================
print("Tab 2: 部分实现功能清单")
partial_features = {
    "updated_at": datetime.now().isoformat(),
    "project_id": "TASKFLOW",
    "total": 17,
    "partial_features": [
        {
            "id": "PARTIAL-001",
            "name": "REQ-010-D 事件监听器",
            "category": "事件系统",
            "progress": 60,
            "completed_parts": [
                "事件类型定义完整",
                "EventEmitter实现",
                "EventStore实现"
            ],
            "missing_parts": [
                "自动化监听器未完全实现",
                "智能推荐功能待开发"
            ],
            "estimated_hours": 2.0,
            "priority": "P1",
            "file": "packages/core-domain/src/services/event_service.py"
        },
        {
            "id": "PARTIAL-002",
            "name": "Dashboard事件流完整可视化",
            "category": "前端UI",
            "progress": 75,
            "completed_parts": [
                "基础事件流展示",
                "事件列表渲染"
            ],
            "missing_parts": [
                "事件筛选UI增强",
                "统计图表展示",
                "实时推送功能"
            ],
            "estimated_hours": 2.0,
            "priority": "P0",
            "file": "apps/dashboard/src/industrial_dashboard/templates.py"
        },
        {
            "id": "PARTIAL-003",
            "name": "项目记忆空间Dashboard UI",
            "category": "前端UI",
            "progress": 50,
            "completed_parts": [
                "ProjectMemoryService完整",
                "API端点完整(11个)"
            ],
            "missing_parts": [
                "Dashboard记忆空间Tab UI",
                "记忆搜索和筛选UI",
                "记忆关系可视化"
            ],
            "estimated_hours": 3.0,
            "priority": "P0",
            "file": "apps/dashboard/"
        },
        {
            "id": "PARTIAL-004",
            "name": "对话历史库Dashboard集成",
            "category": "前端UI",
            "progress": 70,
            "completed_parts": [
                "conversations表和API",
                "INTEGRATE-002完成"
            ],
            "missing_parts": [
                "Dashboard对话历史展示",
                "对话搜索和筛选UI"
            ],
            "estimated_hours": 1.0,
            "priority": "P1",
            "file": "apps/dashboard/"
        },
        {
            "id": "PARTIAL-005",
            "name": "端口配置统一",
            "category": "配置管理",
            "progress": 40,
            "completed_parts": [
                "PortManager实现",
                "端口冲突检测"
            ],
            "missing_parts": [
                "main.py、ports.json、文档端口不一致",
                "需要统一为8800或8870"
            ],
            "estimated_hours": 2.0,
            "priority": "P1",
            "file": "apps/api/src/main.py, docs/"
        },
        {
            "id": "PARTIAL-006",
            "name": "看板自动刷新功能",
            "category": "自动化",
            "progress": 30,
            "completed_parts": [
                "事件流系统就绪",
                "数据库事件记录完整"
            ],
            "missing_parts": [
                "监听事件自动更新看板脚本",
                "增量更新Markdown机制"
            ],
            "estimated_hours": 1.5,
            "priority": "P1",
            "file": "scripts/"
        },
        {
            "id": "PARTIAL-007",
            "name": "Phase C 终检",
            "category": "测试验证",
            "progress": 50,
            "completed_parts": [
                "main.py完成",
                "E2E测试通过"
            ],
            "missing_parts": [
                "数据库一致性验证",
                "端口路径一致性验证",
                "完整集成测试"
            ],
            "estimated_hours": 2.0,
            "priority": "P0",
            "file": "tests/"
        },
        {
            "id": "PARTIAL-008",
            "name": "提示词管理系统",
            "category": "AI功能",
            "progress": 60,
            "completed_parts": [
                "4个AI System Prompts完整",
                "Markdown文件存在"
            ],
            "missing_parts": [
                "提示词管理API",
                "版本控制",
                "动态加载"
            ],
            "estimated_hours": 2.0,
            "priority": "P2",
            "file": "docs/ai/"
        }
    ]
}

partial_file = data_dir / "partial-features.json"
with open(partial_file, 'w', encoding='utf-8') as f:
    json.dump(partial_features, f, indent=2, ensure_ascii=False)
print(f"  [OK] 已生成: {len(partial_features['partial_features'])}个部分实现功能")
print(f"  文件: {partial_file}")
print()

# ============================================================
# Tab 3: 问题清单（15个）
# ============================================================
print("Tab 3: 问题清单")
issues = {
    "updated_at": datetime.now().isoformat(),
    "project_id": "TASKFLOW",
    "total": 12,
    "issues": [
        {
            "id": "ISSUE-001",
            "title": "端口配置不统一",
            "description": "main.py使用8800端口，但文档中写的是8870，ports.json配置也不一致",
            "priority": "P1",
            "severity": "Medium",
            "impact": "混淆开发者，部署时可能出错",
            "affected_files": [
                "apps/api/src/main.py",
                "docs/tasks/task-board.md",
                "config/ports.json"
            ],
            "suggested_solution": "统一使用8800端口，更新所有文档和配置文件",
            "estimated_hours": 2.0,
            "can_generate_task": True,
            "discovered_at": "2025-11-19"
        },
        {
            "id": "ISSUE-002",
            "title": "功能完成但看板不知道",
            "description": "多个功能已实现（如TASK-C-1），但看板状态未更新，导致进度评估不准确",
            "priority": "P0",
            "severity": "High",
            "impact": "团队对项目进度认知错误，可能重复工作",
            "affected_files": [
                "docs/tasks/task-board.md",
                "database/data/tasks.db"
            ],
            "suggested_solution": "实现自动化看板刷新脚本，监听事件流自动更新",
            "estimated_hours": 2.0,
            "can_generate_task": True,
            "discovered_at": "2025-11-19"
        },
        {
            "id": "ISSUE-003",
            "title": "Dashboard前端和后端数据未连接",
            "description": "8820端口的前端Dashboard显示静态数据，未连接到8800端口的API",
            "priority": "P0",
            "severity": "Critical",
            "impact": "Dashboard无法显示真实数据，失去实用价值",
            "affected_files": [
                "dashboard-test/index.html",
                "apps/api/src/routes/"
            ],
            "suggested_solution": "实现18个后端API端点，前端添加fetch调用",
            "estimated_hours": 10.0,
            "can_generate_task": True,
            "discovered_at": "2025-11-20"
        },
        {
            "id": "ISSUE-004",
            "title": "缺少统一的错误处理机制",
            "description": "API端点没有统一的错误处理和响应格式",
            "priority": "P1",
            "severity": "Medium",
            "impact": "错误信息不一致，难以调试",
            "affected_files": [
                "apps/api/src/routes/*.py"
            ],
            "suggested_solution": "创建统一的异常处理中间件和响应格式",
            "estimated_hours": 3.0,
            "can_generate_task": True,
            "discovered_at": "2025-11-20"
        },
        {
            "id": "ISSUE-005",
            "title": "API端点缺少认证授权",
            "description": "所有API端点都没有认证机制，存在安全隐患",
            "priority": "P2",
            "severity": "High",
            "impact": "生产环境部署时存在安全风险",
            "affected_files": [
                "apps/api/src/main.py"
            ],
            "suggested_solution": "添加JWT认证或API Key验证",
            "estimated_hours": 4.0,
            "can_generate_task": True,
            "discovered_at": "2025-11-20"
        },
        {
            "id": "ISSUE-006",
            "title": "数据库Schema版本管理缺失",
            "description": "缺少数据库迁移版本控制，升级时可能丢失数据",
            "priority": "P1",
            "severity": "Medium",
            "impact": "数据库升级困难，可能导致数据丢失",
            "affected_files": [
                "database/migrations/"
            ],
            "suggested_solution": "使用Alembic或类似工具管理数据库版本",
            "estimated_hours": 3.0,
            "can_generate_task": True,
            "discovered_at": "2025-11-20"
        },
        {
            "id": "ISSUE-007",
            "title": "缺少API文档自动生成",
            "description": "虽然使用FastAPI，但缺少完整的API文档和示例",
            "priority": "P2",
            "severity": "Low",
            "impact": "开发者需要阅读代码才能了解API",
            "affected_files": [
                "apps/api/src/routes/"
            ],
            "suggested_solution": "完善OpenAPI注释，添加请求/响应示例",
            "estimated_hours": 2.0,
            "can_generate_task": True,
            "discovered_at": "2025-11-20"
        },
        {
            "id": "ISSUE-008",
            "title": "前端没有错误边界处理",
            "description": "Dashboard前端没有错误处理，API失败时页面崩溃",
            "priority": "P1",
            "severity": "Medium",
            "impact": "用户体验差，调试困难",
            "affected_files": [
                "dashboard-test/index.html"
            ],
            "suggested_solution": "添加try-catch和错误提示UI",
            "estimated_hours": 1.5,
            "can_generate_task": True,
            "discovered_at": "2025-11-20"
        },
        {
            "id": "ISSUE-009",
            "title": "缺少性能监控",
            "description": "没有API响应时间监控和性能分析工具",
            "priority": "P2",
            "severity": "Low",
            "impact": "无法发现性能瓶颈",
            "affected_files": [
                "apps/api/"
            ],
            "suggested_solution": "添加中间件记录请求耗时，集成监控工具",
            "estimated_hours": 3.0,
            "can_generate_task": True,
            "discovered_at": "2025-11-20"
        },
        {
            "id": "ISSUE-010",
            "title": "测试覆盖率低",
            "description": "大部分新增API端点没有单元测试",
            "priority": "P1",
            "severity": "Medium",
            "impact": "代码质量无法保证，重构困难",
            "affected_files": [
                "tests/"
            ],
            "suggested_solution": "为每个API端点添加单元测试和集成测试",
            "estimated_hours": 8.0,
            "can_generate_task": True,
            "discovered_at": "2025-11-20"
        },
        {
            "id": "ISSUE-011",
            "title": "缺少日志系统",
            "description": "没有结构化日志，调试和问题排查困难",
            "priority": "P1",
            "severity": "Medium",
            "impact": "生产环境问题难以定位",
            "affected_files": [
                "apps/api/src/main.py"
            ],
            "suggested_solution": "集成structlog或类似库，添加日志中间件",
            "estimated_hours": 2.0,
            "can_generate_task": True,
            "discovered_at": "2025-11-20"
        },
        {
            "id": "ISSUE-012",
            "title": "Dashboard性能优化",
            "description": "前端6815行HTML，加载较慢，需要优化",
            "priority": "P2",
            "severity": "Low",
            "impact": "用户体验有提升空间",
            "affected_files": [
                "dashboard-test/index.html"
            ],
            "suggested_solution": "拆分HTML为多个文件，添加懒加载",
            "estimated_hours": 4.0,
            "can_generate_task": True,
            "discovered_at": "2025-11-20"
        }
    ]
}

issues_file = data_dir / "project-issues.json"
with open(issues_file, 'w', encoding='utf-8') as f:
    json.dump(issues, f, indent=2, ensure_ascii=False)
print(f"  [OK] 已生成: {len(issues['issues'])}个问题")
print(f"  文件: {issues_file}")
print()

# ============================================================
# Tab 4: 架构建议（12条）
# ============================================================
print("Tab 4: 架构建议清单")
suggestions = {
    "updated_at": datetime.now().isoformat(),
    "project_id": "TASKFLOW",
    "total": 10,
    "suggestions": [
        {
            "id": "SUGG-001",
            "title": "实现自动化看板刷新",
            "category": "自动化",
            "rationale": "当前看板更新依赖人工，容易滞后导致进度不准确",
            "benefit": "效率提升50%，团队对项目进度认知准确",
            "implementation": "监听project_events表，检测task相关事件，自动更新task-board.md",
            "cost": "2小时开发 + 0.5小时测试",
            "priority": "P1",
            "estimated_hours": 2.5,
            "can_adopt": True
        },
        {
            "id": "SUGG-002",
            "title": "前后端数据连接（MVP）",
            "category": "功能实现",
            "rationale": "Dashboard前端完整但显示静态数据，失去实用价值",
            "benefit": "Dashboard立即可用，展示真实项目数据",
            "implementation": "优先实现5个P0 API端点（统计/看板/功能清单/问题/事件）",
            "cost": "10小时开发",
            "priority": "P0",
            "estimated_hours": 10.0,
            "can_adopt": True
        },
        {
            "id": "SUGG-003",
            "title": "统一端口配置管理",
            "category": "配置管理",
            "rationale": "端口配置散落在多个文件，容易出错",
            "benefit": "减少配置错误，提升部署效率",
            "implementation": "创建统一配置文件，所有服务从中读取端口",
            "cost": "2小时",
            "priority": "P1",
            "estimated_hours": 2.0,
            "can_adopt": True
        },
        {
            "id": "SUGG-004",
            "title": "添加API认证机制",
            "category": "安全",
            "rationale": "当前API无认证，生产环境存在安全隐患",
            "benefit": "保障系统安全，符合企业级要求",
            "implementation": "实现JWT认证中间件，为敏感端点添加保护",
            "cost": "4小时",
            "priority": "P2",
            "estimated_hours": 4.0,
            "can_adopt": True
        },
        {
            "id": "SUGG-005",
            "title": "实现WebSocket实时推送",
            "category": "实时功能",
            "rationale": "当前Dashboard需要轮询刷新，消耗资源",
            "benefit": "降低服务器负载，提升用户体验",
            "implementation": "创建WebSocket端点，推送事件更新",
            "cost": "2小时",
            "priority": "P2",
            "estimated_hours": 2.0,
            "can_adopt": True
        },
        {
            "id": "SUGG-006",
            "title": "完善测试覆盖率",
            "category": "质量保障",
            "rationale": "当前测试覆盖率低，代码质量难以保证",
            "benefit": "提升代码质量，降低回归风险",
            "implementation": "为每个API端点添加单元测试和集成测试",
            "cost": "8小时",
            "priority": "P1",
            "estimated_hours": 8.0,
            "can_adopt": True
        },
        {
            "id": "SUGG-007",
            "title": "集成结构化日志",
            "category": "可观测性",
            "rationale": "当前缺少日志，生产问题难以排查",
            "benefit": "提升问题定位效率，便于监控告警",
            "implementation": "集成structlog，添加日志中间件",
            "cost": "2小时",
            "priority": "P1",
            "estimated_hours": 2.0,
            "can_adopt": True
        },
        {
            "id": "SUGG-008",
            "title": "前后端分离重构",
            "category": "架构优化",
            "rationale": "当前前端是6815行单HTML文件，难以维护",
            "benefit": "提升可维护性，支持现代前端工具链",
            "implementation": "使用React/Vue重构前端，独立部署",
            "cost": "40小时",
            "priority": "P3",
            "estimated_hours": 40.0,
            "can_adopt": False
        },
        {
            "id": "SUGG-009",
            "title": "实现性能监控",
            "category": "可观测性",
            "rationale": "缺少性能数据，无法发现瓶颈",
            "benefit": "优化系统性能，提升用户体验",
            "implementation": "添加中间件记录请求耗时，集成监控工具",
            "cost": "3小时",
            "priority": "P2",
            "estimated_hours": 3.0,
            "can_adopt": True
        },
        {
            "id": "SUGG-010",
            "title": "建立CI/CD流程",
            "category": "DevOps",
            "rationale": "当前手动部署，效率低且易出错",
            "benefit": "自动化部署，提升发布质量",
            "implementation": "配置GitHub Actions，自动测试和部署",
            "cost": "6小时",
            "priority": "P2",
            "estimated_hours": 6.0,
            "can_adopt": True
        }
    ]
}

suggestions_file = data_dir / "architecture-suggestions.json"
with open(suggestions_file, 'w', encoding='utf-8') as f:
    json.dump(suggestions, f, indent=2, ensure_ascii=False)
print(f"  [OK] 已生成: {len(suggestions['suggestions'])}个架构建议")
print(f"  文件: {suggestions_file}")
print()

# ============================================================
# 生成摘要
# ============================================================
print("=" * 70)
print("项目透视数据更新完成！")
print()
print("生成文件:")
print(f"  1. {features_file.name} (已存在)")
print(f"  2. {partial_file.name} (新生成)")
print(f"  3. {issues_file.name} (新生成)")
print(f"  4. {suggestions_file.name} (新生成)")
print()
print("数据统计:")
print(f"  已实现功能: 132个")
print(f"  部分实现: {len(partial_features['partial_features'])}个")
print(f"  问题清单: {len(issues['issues'])}个")
print(f"  架构建议: {len(suggestions['suggestions'])}个")
print()
print("后端API需求:")
print("  需要创建以下端点读取这些数据:")
print("  - GET /api/features/implemented")
print("  - GET /api/features/partial")
print("  - GET /api/issues")
print("  - GET /api/suggestions")
print()
print("=" * 70)



