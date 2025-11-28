#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
架构师任务：扩充项目透视数据到完整数量
- 部分实现：8 → 24个
- 问题清单：12 → 15个
- 建议：10 → 12个
"""
import json
from pathlib import Path
from datetime import datetime

# 项目根目录
project_root = Path(__file__).parent.parent
data_dir = project_root / "apps" / "dashboard" / "automation-data"

print("=" * 70)
print("架构师任务：扩充项目透视数据")
print("=" * 70)
print()

# ============================================================
# Tab 2: 部分实现功能（8 → 24个）
# ============================================================
print("Tab 2: 扩充部分实现功能 (8 -> 24个)")

partial_features = {
    "updated_at": datetime.now().isoformat(),
    "project_id": "TASKFLOW",
    "total": 24,
    "partial_features": [
        # 原有8个
        {
            "id": "PARTIAL-001",
            "name": "REQ-010-D 事件监听器",
            "category": "事件系统",
            "progress": 60,
            "completed_parts": ["事件类型定义", "EventEmitter实现", "EventStore实现"],
            "missing_parts": ["自动化监听器", "智能推荐功能"],
            "estimated_hours": 2.0,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-002",
            "name": "Dashboard事件流完整可视化",
            "category": "前端UI",
            "progress": 75,
            "completed_parts": ["基础事件流展示", "事件列表渲染"],
            "missing_parts": ["事件筛选UI增强", "统计图表", "实时推送"],
            "estimated_hours": 2.0,
            "priority": "P0"
        },
        {
            "id": "PARTIAL-003",
            "name": "项目记忆空间Dashboard UI",
            "category": "前端UI",
            "progress": 50,
            "completed_parts": ["ProjectMemoryService完整", "API端点完整(11个)"],
            "missing_parts": ["Dashboard记忆空间Tab UI", "记忆搜索UI", "记忆关系可视化"],
            "estimated_hours": 3.0,
            "priority": "P0"
        },
        {
            "id": "PARTIAL-004",
            "name": "对话历史库Dashboard集成",
            "category": "前端UI",
            "progress": 70,
            "completed_parts": ["conversations表和API", "INTEGRATE-002完成"],
            "missing_parts": ["Dashboard对话历史展示", "对话搜索UI"],
            "estimated_hours": 1.0,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-005",
            "name": "端口配置统一",
            "category": "配置管理",
            "progress": 40,
            "completed_parts": ["PortManager实现", "端口冲突检测"],
            "missing_parts": ["main.py、ports.json、文档端口不一致"],
            "estimated_hours": 2.0,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-006",
            "name": "看板自动刷新功能",
            "category": "自动化",
            "progress": 30,
            "completed_parts": ["事件流系统就绪", "数据库事件记录完整"],
            "missing_parts": ["监听事件自动更新看板脚本", "增量更新Markdown"],
            "estimated_hours": 1.5,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-007",
            "name": "Phase C 终检",
            "category": "测试验证",
            "progress": 50,
            "completed_parts": ["main.py完成", "E2E测试通过"],
            "missing_parts": ["数据库一致性验证", "端口路径验证", "完整集成测试"],
            "estimated_hours": 2.0,
            "priority": "P0"
        },
        {
            "id": "PARTIAL-008",
            "name": "提示词管理系统",
            "category": "AI功能",
            "progress": 60,
            "completed_parts": ["4个AI System Prompts完整", "Markdown文件存在"],
            "missing_parts": ["提示词管理API", "版本控制", "动态加载"],
            "estimated_hours": 2.0,
            "priority": "P2"
        },
        # 新增16个
        {
            "id": "PARTIAL-009",
            "name": "Dashboard统计卡片数据连接",
            "category": "前端集成",
            "progress": 20,
            "completed_parts": ["9个统计卡片UI完整"],
            "missing_parts": ["GET /api/stats/overview端点", "前端fetch调用", "自动刷新"],
            "estimated_hours": 2.0,
            "priority": "P0"
        },
        {
            "id": "PARTIAL-010",
            "name": "任务看板拖拽功能",
            "category": "前端交互",
            "progress": 40,
            "completed_parts": ["看板UI布局完整", "任务卡片渲染"],
            "missing_parts": ["拖拽交互实现", "状态更新API调用"],
            "estimated_hours": 3.0,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-011",
            "name": "代码审查结果展示",
            "category": "前端UI",
            "progress": 30,
            "completed_parts": ["审查清单UI设计"],
            "missing_parts": ["GET /api/code-reviews端点", "数据渲染", "审查提交功能"],
            "estimated_hours": 2.0,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-012",
            "name": "技术文档树形展示",
            "category": "前端UI",
            "progress": 25,
            "completed_parts": ["文档列表UI框架"],
            "missing_parts": ["GET /api/documents端点", "树形结构渲染", "文档内容预览"],
            "estimated_hours": 2.5,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-013",
            "name": "运维日志查询和筛选",
            "category": "运维功能",
            "progress": 35,
            "completed_parts": ["日志时间轴UI", "级别筛选UI"],
            "missing_parts": ["GET /api/logs/operations端点", "实时日志推送"],
            "estimated_hours": 1.5,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-014",
            "name": "Bug看板管理",
            "category": "问题追踪",
            "progress": 40,
            "completed_parts": ["Bug看板UI完整", "issues表结构"],
            "missing_parts": ["GET /api/bugs端点", "Bug创建和更新功能"],
            "estimated_hours": 2.0,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-015",
            "name": "系统监控Dashboard",
            "category": "监控",
            "progress": 45,
            "completed_parts": ["6个服务监控卡片UI", "基础健康检查"],
            "missing_parts": ["详细监控指标", "实时数据更新", "告警功能"],
            "estimated_hours": 3.0,
            "priority": "P0"
        },
        {
            "id": "PARTIAL-016",
            "name": "知识库分类展示",
            "category": "知识管理",
            "progress": 65,
            "completed_parts": ["knowledge_articles表完整", "基础API端点"],
            "missing_parts": ["分类筛选UI", "全文搜索", "知识推荐"],
            "estimated_hours": 2.0,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-017",
            "name": "实时脉动系统",
            "category": "实时监控",
            "progress": 30,
            "completed_parts": ["实时脉动UI框架", "事件流基础"],
            "missing_parts": ["GET /api/pulse/realtime端点", "WebSocket推送"],
            "estimated_hours": 2.5,
            "priority": "P2"
        },
        {
            "id": "PARTIAL-018",
            "name": "AI协作链可视化",
            "category": "可视化",
            "progress": 20,
            "completed_parts": ["协作链UI设计"],
            "missing_parts": ["GET /api/collaboration/chain端点", "D3.js图表集成"],
            "estimated_hours": 2.5,
            "priority": "P2"
        },
        {
            "id": "PARTIAL-019",
            "name": "Noah代码管家任务队列",
            "category": "AI功能",
            "progress": 55,
            "completed_parts": ["任务队列UI", "GET /api/tasks基础端点"],
            "missing_parts": ["assigned_to筛选参数", "任务认领功能"],
            "estimated_hours": 1.0,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-020",
            "name": "代码清单目录树",
            "category": "代码分析",
            "progress": 25,
            "completed_parts": ["目录树UI组件"],
            "missing_parts": ["GET /api/code/inventory端点", "代码扫描功能", "复杂度分析"],
            "estimated_hours": 2.5,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-021",
            "name": "需求管理模块",
            "category": "需求管理",
            "progress": 35,
            "completed_parts": ["待开发任务池UI", "需求卡片设计"],
            "missing_parts": ["GET /api/requirements端点", "需求状态更新", "需求评审功能"],
            "estimated_hours": 2.0,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-022",
            "name": "问题生成任务功能",
            "category": "项目管理",
            "progress": 40,
            "completed_parts": ["问题清单展示", "生成任务按钮UI"],
            "missing_parts": ["POST /api/issues/{id}/generate-task端点", "任务模板生成"],
            "estimated_hours": 1.5,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-023",
            "name": "建议采纳转任务",
            "category": "项目管理",
            "progress": 40,
            "completed_parts": ["架构建议展示", "采纳按钮UI"],
            "missing_parts": ["POST /api/suggestions/{id}/adopt端点", "任务自动创建"],
            "estimated_hours": 1.5,
            "priority": "P1"
        },
        {
            "id": "PARTIAL-024",
            "name": "前端错误处理机制",
            "category": "错误处理",
            "progress": 30,
            "completed_parts": ["基础console.error"],
            "missing_parts": ["统一错误边界", "错误提示Toast", "网络错误重试"],
            "estimated_hours": 2.0,
            "priority": "P1"
        }
    ]
}

partial_file = data_dir / "partial-features.json"
with open(partial_file, 'w', encoding='utf-8') as f:
    json.dump(partial_features, f, indent=2, ensure_ascii=False)
print(f"  [OK] 已更新: {len(partial_features['partial_features'])}个部分实现功能")
print()

# ============================================================
# Tab 3: 问题清单（12 → 15个）
# ============================================================
print("Tab 3: 扩充问题清单 (12 -> 15个)")

issues = {
    "updated_at": datetime.now().isoformat(),
    "project_id": "TASKFLOW",
    "total": 15,
    "issues": [
        {
            "id": "ISSUE-001",
            "title": "端口配置不统一",
            "description": "main.py使用8800端口，但文档中写的是8870，ports.json配置也不一致",
            "priority": "P1",
            "severity": "Medium",
            "impact": "混淆开发者，部署时可能出错",
            "estimated_hours": 2.0
        },
        {
            "id": "ISSUE-002",
            "title": "功能完成但看板不知道",
            "description": "多个功能已实现，但看板状态未更新，导致进度评估不准确",
            "priority": "P0",
            "severity": "High",
            "impact": "团队对项目进度认知错误",
            "estimated_hours": 2.0
        },
        {
            "id": "ISSUE-003",
            "title": "Dashboard前后端数据未连接",
            "description": "8820端口的前端Dashboard显示静态数据，未连接到8800端口的API",
            "priority": "P0",
            "severity": "Critical",
            "impact": "Dashboard无法显示真实数据",
            "estimated_hours": 10.0
        },
        {
            "id": "ISSUE-004",
            "title": "缺少统一的错误处理机制",
            "description": "API端点没有统一的错误处理和响应格式",
            "priority": "P1",
            "severity": "Medium",
            "impact": "错误信息不一致，难以调试",
            "estimated_hours": 3.0
        },
        {
            "id": "ISSUE-005",
            "title": "API端点缺少认证授权",
            "description": "所有API端点都没有认证机制，存在安全隐患",
            "priority": "P2",
            "severity": "High",
            "impact": "生产环境部署时存在安全风险",
            "estimated_hours": 4.0
        },
        {
            "id": "ISSUE-006",
            "title": "数据库Schema版本管理缺失",
            "description": "缺少数据库迁移版本控制，升级时可能丢失数据",
            "priority": "P1",
            "severity": "Medium",
            "impact": "数据库升级困难",
            "estimated_hours": 3.0
        },
        {
            "id": "ISSUE-007",
            "title": "缺少API文档自动生成",
            "description": "虽然使用FastAPI，但缺少完整的API文档和示例",
            "priority": "P2",
            "severity": "Low",
            "impact": "开发者需要阅读代码",
            "estimated_hours": 2.0
        },
        {
            "id": "ISSUE-008",
            "title": "前端没有错误边界处理",
            "description": "Dashboard前端没有错误处理，API失败时页面崩溃",
            "priority": "P1",
            "severity": "Medium",
            "impact": "用户体验差",
            "estimated_hours": 1.5
        },
        {
            "id": "ISSUE-009",
            "title": "缺少性能监控",
            "description": "没有API响应时间监控和性能分析工具",
            "priority": "P2",
            "severity": "Low",
            "impact": "无法发现性能瓶颈",
            "estimated_hours": 3.0
        },
        {
            "id": "ISSUE-010",
            "title": "测试覆盖率低",
            "description": "大部分新增API端点没有单元测试",
            "priority": "P1",
            "severity": "Medium",
            "impact": "代码质量无法保证",
            "estimated_hours": 8.0
        },
        {
            "id": "ISSUE-011",
            "title": "缺少日志系统",
            "description": "没有结构化日志，调试和问题排查困难",
            "priority": "P1",
            "severity": "Medium",
            "impact": "生产环境问题难以定位",
            "estimated_hours": 2.0
        },
        {
            "id": "ISSUE-012",
            "title": "Dashboard性能优化",
            "description": "前端6815行HTML，加载较慢，需要优化",
            "priority": "P2",
            "severity": "Low",
            "impact": "用户体验有提升空间",
            "estimated_hours": 4.0
        },
        {
            "id": "ISSUE-013",
            "title": "缺少数据备份机制",
            "description": "SQLite数据库没有自动备份，存在数据丢失风险",
            "priority": "P1",
            "severity": "High",
            "impact": "数据丢失风险",
            "estimated_hours": 2.0
        },
        {
            "id": "ISSUE-014",
            "title": "缺少环境配置管理",
            "description": "开发、测试、生产环境配置混在一起",
            "priority": "P1",
            "severity": "Medium",
            "impact": "部署配置容易出错",
            "estimated_hours": 2.5
        },
        {
            "id": "ISSUE-015",
            "title": "缺少API速率限制",
            "description": "API没有速率限制，可能被恶意调用",
            "priority": "P2",
            "severity": "Medium",
            "impact": "服务可能被滥用",
            "estimated_hours": 2.0
        }
    ]
}

issues_file = data_dir / "project-issues.json"
with open(issues_file, 'w', encoding='utf-8') as f:
    json.dump(issues, f, indent=2, ensure_ascii=False)
print(f"  [OK] 已更新: {len(issues['issues'])}个问题")
print()

# ============================================================
# Tab 4: 架构建议（10 → 12条）
# ============================================================
print("Tab 4: 扩充架构建议 (10 -> 12条)")

suggestions = {
    "updated_at": datetime.now().isoformat(),
    "project_id": "TASKFLOW",
    "total": 12,
    "suggestions": [
        {
            "id": "SUGG-001",
            "title": "实现自动化看板刷新",
            "category": "自动化",
            "rationale": "当前看板更新依赖人工",
            "benefit": "效率提升50%",
            "cost": "2.5小时",
            "priority": "P1",
            "estimated_hours": 2.5
        },
        {
            "id": "SUGG-002",
            "title": "前后端数据连接MVP",
            "category": "功能实现",
            "rationale": "Dashboard前端完整但显示静态数据",
            "benefit": "Dashboard立即可用",
            "cost": "10小时",
            "priority": "P0",
            "estimated_hours": 10.0
        },
        {
            "id": "SUGG-003",
            "title": "统一端口配置管理",
            "category": "配置管理",
            "rationale": "端口配置散落在多个文件",
            "benefit": "减少配置错误",
            "cost": "2小时",
            "priority": "P1",
            "estimated_hours": 2.0
        },
        {
            "id": "SUGG-004",
            "title": "添加API认证机制",
            "category": "安全",
            "rationale": "当前API无认证",
            "benefit": "保障系统安全",
            "cost": "4小时",
            "priority": "P2",
            "estimated_hours": 4.0
        },
        {
            "id": "SUGG-005",
            "title": "实现WebSocket实时推送",
            "category": "实时功能",
            "rationale": "当前Dashboard需要轮询刷新",
            "benefit": "降低服务器负载",
            "cost": "2小时",
            "priority": "P2",
            "estimated_hours": 2.0
        },
        {
            "id": "SUGG-006",
            "title": "完善测试覆盖率",
            "category": "质量保障",
            "rationale": "当前测试覆盖率低",
            "benefit": "提升代码质量",
            "cost": "8小时",
            "priority": "P1",
            "estimated_hours": 8.0
        },
        {
            "id": "SUGG-007",
            "title": "集成结构化日志",
            "category": "可观测性",
            "rationale": "当前缺少日志",
            "benefit": "提升问题定位效率",
            "cost": "2小时",
            "priority": "P1",
            "estimated_hours": 2.0
        },
        {
            "id": "SUGG-008",
            "title": "前后端分离重构",
            "category": "架构优化",
            "rationale": "当前前端是6815行单HTML文件",
            "benefit": "提升可维护性",
            "cost": "40小时",
            "priority": "P3",
            "estimated_hours": 40.0
        },
        {
            "id": "SUGG-009",
            "title": "实现性能监控",
            "category": "可观测性",
            "rationale": "缺少性能数据",
            "benefit": "优化系统性能",
            "cost": "3小时",
            "priority": "P2",
            "estimated_hours": 3.0
        },
        {
            "id": "SUGG-010",
            "title": "建立CI/CD流程",
            "category": "DevOps",
            "rationale": "当前手动部署",
            "benefit": "自动化部署",
            "cost": "6小时",
            "priority": "P2",
            "estimated_hours": 6.0
        },
        {
            "id": "SUGG-011",
            "title": "实现数据库自动备份",
            "category": "数据安全",
            "rationale": "当前没有备份机制",
            "benefit": "防止数据丢失",
            "cost": "2小时",
            "priority": "P1",
            "estimated_hours": 2.0
        },
        {
            "id": "SUGG-012",
            "title": "添加API限流保护",
            "category": "安全",
            "rationale": "API可能被恶意调用",
            "benefit": "保护服务稳定",
            "cost": "2小时",
            "priority": "P2",
            "estimated_hours": 2.0
        }
    ]
}

suggestions_file = data_dir / "architecture-suggestions.json"
with open(suggestions_file, 'w', encoding='utf-8') as f:
    json.dump(suggestions, f, indent=2, ensure_ascii=False)
print(f"  [OK] 已更新: {len(suggestions['suggestions'])}个架构建议")
print()

print("=" * 70)
print("项目透视数据扩充完成！")
print()
print("最终统计:")
print(f"  已实现功能: 132个 (v17-complete-features.json)")
print(f"  部分实现: {len(partial_features['partial_features'])}个")
print(f"  问题清单: {len(issues['issues'])}个")
print(f"  架构建议: {len(suggestions['suggestions'])}个")
print()
print("=" * 70)



