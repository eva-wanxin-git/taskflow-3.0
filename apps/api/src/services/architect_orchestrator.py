# -*- coding: utf-8 -*-
"""
架构师编排器（Architect Orchestrator）

负责接收架构师AI的分析结果，将其转换为：
- 数据库记录（tasks, issues, decisions, knowledge_articles）
- Markdown文档（task-board.md等）
- API响应

这是架构师AI与任务所·Flow系统的桥梁
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import sqlite3
from contextlib import contextmanager

from pydantic import BaseModel, Field

# 导入事件服务，用于记录架构师分析与任务/问题/知识创建事件
import sys
from pathlib import Path as _PathForEvents

packages_path = _PathForEvents(__file__).parent.parent.parent.parent.parent / "packages" / "core-domain" / "src"
if str(packages_path) not in sys.path:
    sys.path.insert(0, str(packages_path))

from services.event_service import (
    create_event_emitter,
    EventCategory,
    EventSource,
    EventSeverity,
)


# ============================================================================
# Pydantic模型定义
# ============================================================================

class FeatureSummary(BaseModel):
    """功能摘要"""
    title: str = Field(..., description="功能标题")
    description: str = Field(..., description="功能描述")
    related_paths: List[str] = Field(default_factory=list, description="相关文件路径")
    completion: float = Field(default=1.0, ge=0, le=1, description="完成度0-1")
    notes: Optional[str] = Field(None, description="备注")


class PartialFeatureSummary(FeatureSummary):
    """部分实现功能摘要"""
    missing: List[str] = Field(..., description="缺少的部分")
    risk: Optional[str] = Field(None, description="风险描述")
    priority: str = Field(default="medium", description="优先级")


class ProblemSummary(BaseModel):
    """问题摘要"""
    title: str
    description: str
    severity: str = Field(..., description="严重程度: critical/high/medium/low")
    related_paths: List[str] = Field(default_factory=list)
    impact: str = Field(..., description="影响描述")
    suggested_solution: Optional[str] = None


class ArchitectTaskSuggestion(BaseModel):
    """架构师建议的任务"""
    id: str = Field(..., description="任务ID，如ARCH-001")
    title: str
    type: str = Field(..., description="类型: backend/frontend/refactor/bugfix/test/docs")
    priority: str = Field(..., description="优先级: critical/high/medium/low")
    component: str = Field(..., description="所属组件")
    description: str
    related_paths: List[str] = Field(default_factory=list)
    acceptance_criteria: List[str] = Field(default_factory=list, description="验收标准")
    estimated_hours: float = Field(default=0, description="预估工时")
    executor_type: str = Field(default="code-steward", description="建议执行者")
    dependencies: List[str] = Field(default_factory=list, description="依赖的任务ID")


class ArchitectAnalysis(BaseModel):
    """架构师完整分析结果"""
    project_code: str = Field(..., description="项目代码，如MY_PROJECT")
    repo_root: Optional[str] = Field(None, description="仓库根目录路径")
    completed_features: List[FeatureSummary] = Field(default_factory=list)
    partial_features: List[PartialFeatureSummary] = Field(default_factory=list)
    problems: List[ProblemSummary] = Field(default_factory=list)
    suggested_tasks: List[ArchitectTaskSuggestion] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="元数据")


class HandoverSnapshot(BaseModel):
    """交接快照"""
    snapshot_id: str
    project_code: str
    architect: str = Field(default="AI Architect v2")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    completed_phases: List[Dict[str, Any]] = Field(default_factory=list)
    current_focus: Dict[str, Any] = Field(default_factory=dict)
    key_files_analyzed: List[Dict[str, str]] = Field(default_factory=list)
    unanalyzed_areas: List[str] = Field(default_factory=list)
    recommendations_for_next: List[str] = Field(default_factory=list)
    token_usage: Optional[Dict[str, Any]] = None


# ============================================================================
# 架构师编排器
# ============================================================================

class ArchitectOrchestrator:
    """架构师编排器
    
    负责将架构师AI的分析结果转换为系统可用的格式：
    - 写入数据库（通过Repository）
    - 生成Markdown文档
    - 记录到知识库
    """
    
    def __init__(
        self,
        state_manager=None,
        docs_root: str = "docs",
        db_path: Optional[str] = None,
    ):
        """
        初始化
        
        Args:
            state_manager: 状态管理器（访问数据库，当前未直接使用，保留以便未来迁移）
            docs_root: 文档根目录路径
            db_path: 可选的数据库路径（默认指向 monorepo 下的 database/data/tasks.db）
        """
        self.state_manager = state_manager
        self.docs_root = Path(docs_root)

        # 默认数据库路径：基于当前文件定位到仓库根目录下的 tasks.db
        if db_path is not None:
            self.db_path = Path(db_path)
        else:
            self.db_path = (
                Path(__file__).resolve().parent.parent.parent.parent
                / "database"
                / "data"
                / "tasks.db"
            )

        # 事件发射器：用于记录架构师分析提交、任务/问题/知识创建等事件
        try:
            self._event_emitter = create_event_emitter(db_path=str(self.db_path))
        except Exception:
            # 如果事件系统初始化失败，不阻塞主流程，只在发射事件时静默忽略
            self._event_emitter = None

    # -------------------------------------------------------------------------
    # 数据库连接辅助方法
    # -------------------------------------------------------------------------

    @contextmanager
    def _get_db_connection(self) -> sqlite3.Connection:
        """获取到 tasks.db 的连接（上下文管理器）"""
        conn = sqlite3.connect(str(self.db_path))
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
        
    def process_analysis(
        self,
        analysis: ArchitectAnalysis
    ) -> Dict[str, Any]:
        """
        处理架构师分析结果
        
        Args:
            analysis: 架构师分析结果
            
        Returns:
            处理结果统计：{
                "tasks_created": 12,
                "issues_created": 3,
                "components_created": 2,
                "task_board_updated": True
            }
        """
        result = {
            "tasks_created": 0,
            "issues_created": 0,
            "decisions_created": 0,
            "articles_created": 0,
            "components_created": 0,
            "task_board_updated": False
        }
        
        # 1. 确保项目和组件存在
        project_id = self._ensure_project_exists(analysis.project_code)
        result["components_created"] = self._ensure_components_exist(
            project_id,
            analysis.suggested_tasks
        )
        
        # 2. 创建任务
        result["tasks_created"] = self._create_tasks_from_suggestions(
            project_id,
            analysis.suggested_tasks
        )
        
        # 3. 记录问题
        result["issues_created"] = self._create_issues_from_problems(
            project_id,
            analysis.problems
        )
        
        # 4. 记录功能清单（作为知识文章）
        result["articles_created"] = self._create_feature_articles(
            project_id,
            analysis.completed_features,
            analysis.partial_features
        )
        
        # 5. 更新任务看板文档
        result["task_board_updated"] = self._update_task_board_md(analysis)

        # 6. 记录一次汇总事件，方便事件流与Dashboard展示
        self._emit_architect_analysis_event(analysis.project_code, result)
        
        return result
    
    def _ensure_project_exists(self, project_code: str) -> str:
        """确保项目存在，不存在则创建，并返回项目ID"""
        project_code = project_code.strip()
        if not project_code:
            raise ValueError("project_code 不能为空")

        with self._get_db_connection() as conn:
            cursor = conn.cursor()

            # 1. 按项目代码查找已有项目
            cursor.execute(
                "SELECT id FROM projects WHERE code = ?",
                (project_code,),
            )
            row = cursor.fetchone()
            if row:
                return row[0]

            # 2. 不存在则创建一个新的项目记录
            project_id = f"{project_code.lower()}-main"
            now = datetime.now().isoformat()
            cursor.execute(
                """
                INSERT INTO projects (id, name, code, description, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    project_id,
                    project_code,
                    project_code,
                    f"Auto-created project for {project_code}",
                    "active",
                    now,
                    now,
                ),
            )

        return project_id
    
    def _ensure_components_exist(
        self,
        project_id: str,
        tasks: List[ArchitectTaskSuggestion]
    ) -> int:
        """根据任务中的component字段，确保组件存在"""
        components = set(task.component for task in tasks)
        created = 0

        if not components:
            return 0

        with self._get_db_connection() as conn:
            cursor = conn.cursor()

            for component_name in components:
                if not component_name:
                    continue

                component_id = f"{project_id}-{component_name}"

                # 检查组件是否已存在
                cursor.execute(
                    "SELECT 1 FROM components WHERE id = ?",
                    (component_id,),
                )
                if cursor.fetchone():
                    continue

                # 创建组件记录（类型/描述等先使用保守默认值）
                cursor.execute(
                    """
                    INSERT INTO components (
                        id, project_id, name, type, description, repo_path, tech_stack, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        component_id,
                        project_id,
                        component_name,
                        "backend",
                        None,
                        None,
                        None,
                        datetime.now().isoformat(),
                    ),
                )
                created += 1
        
        return created
    
    def _create_tasks_from_suggestions(
        self,
        project_id: str,
        suggestions: List[ArchitectTaskSuggestion]
    ) -> int:
        """将建议任务转换为实际任务记录"""
        created = 0

        if not suggestions:
            return 0

        with self._get_db_connection() as conn:
            cursor = conn.cursor()

            for suggestion in suggestions:
                component_id = f"{project_id}-{suggestion.component}"
                metadata = {
                    "type": suggestion.type,
                    "executor_type": suggestion.executor_type,
                    "related_paths": suggestion.related_paths,
                    "acceptance_criteria": suggestion.acceptance_criteria,
                    "source": "architect_analysis",
                }

                # 使用 INSERT OR REPLACE，避免重复ID导致失败
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO tasks (
                        id, title, description, status, priority,
                        estimated_hours, actual_hours, complexity,
                        assigned_to, created_at, updated_at,
                        metadata, project_id, component_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        suggestion.id,
                        suggestion.title,
                        suggestion.description,
                        "pending",
                        self._map_priority(suggestion.priority),
                        suggestion.estimated_hours or 0,
                        0,
                        self._infer_complexity(suggestion.estimated_hours or 0),
                        None,
                        datetime.now().isoformat(),
                        datetime.now().isoformat(),
                        json.dumps(metadata, ensure_ascii=False),
                        project_id,
                        component_id,
                    ),
                )
                created += 1

                # 为新建任务发射事件，供全局事件流与自动看板更新使用
                self._emit_task_created_event(
                    project_id=project_id,
                    task_id=suggestion.id,
                    task_title=suggestion.title,
                )
        
        return created
    
    def _create_issues_from_problems(
        self,
        project_id: str,
        problems: List[ProblemSummary]
    ) -> int:
        """将问题转换为issue记录"""
        created = 0

        if not problems:
            return 0

        with self._get_db_connection() as conn:
            cursor = conn.cursor()

            for index, problem in enumerate(problems, start=1):
                issue_id = f"ISS-{datetime.now().strftime('%Y%m%d')}-{index:03d}"

                cursor.execute(
                    """
                    INSERT OR REPLACE INTO issues (
                        id, project_id, component_id, task_id,
                        title, description, severity, status,
                        discovered_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        issue_id,
                        project_id,
                        None,  # TODO: 可从 related_paths 推断 component_id
                        None,
                        problem.title,
                        problem.description,
                        problem.severity,
                        "open",
                        datetime.now().isoformat(),
                    ),
                )
                created += 1

                # 为新发现的问题发射事件
                self._emit_issue_created_event(
                    project_id=project_id,
                    issue_id=issue_id,
                    issue_title=problem.title,
                    severity=problem.severity,
                )
        
        return created
    
    def _create_feature_articles(
        self,
        project_id: str,
        completed: List[FeatureSummary],
        partial: List[PartialFeatureSummary]
    ) -> int:
        """将功能清单记录为知识文章"""
        created = 0

        if not completed and not partial:
            return 0

        with self._get_db_connection() as conn:
            cursor = conn.cursor()

            # 1. 已完成功能文章
            if completed:
                article_id = f"ART-{project_id}-completed-features"
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO knowledge_articles (
                        id, project_id, component_id,
                        title, content, category, tags,
                        created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        article_id,
                        project_id,
                        None,
                        f"{project_id} - 已实现功能清单",
                        self._format_features_as_markdown(completed),
                        "feature-list",
                        json.dumps(["completed", "features"], ensure_ascii=False),
                        datetime.now().isoformat(),
                        datetime.now().isoformat(),
                    ),
                )
                created += 1

            # 2. 部分实现功能文章
            if partial:
                article_id = f"ART-{project_id}-partial-features"
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO knowledge_articles (
                        id, project_id, component_id,
                        title, content, category, tags,
                        created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        article_id,
                        project_id,
                        None,
                        f"{project_id} - 部分实现功能清单",
                        self._format_partial_features_as_markdown(partial),
                        "feature-list",
                        json.dumps(["partial", "features", "wip"], ensure_ascii=False),
                        datetime.now().isoformat(),
                        datetime.now().isoformat(),
                    ),
                )
                created += 1
        
        return created
    
    def _update_task_board_md(self, analysis: ArchitectAnalysis) -> bool:
        """更新任务看板Markdown文档"""
        task_board_path = self.docs_root / "tasks" / "task-board.md"
        task_board_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 生成Markdown内容
        content = self._generate_task_board_markdown(analysis)
        
        # 写入文件
        task_board_path.write_text(content, encoding='utf-8')
        
        return True
    
    def _generate_task_board_markdown(self, analysis: ArchitectAnalysis) -> str:
        """生成任务看板Markdown"""
        lines = []
        
        # 标题
        lines.append(f"# 任务看板\n")
        lines.append(f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        lines.append(f"**项目**: {analysis.project_code}\n")
        lines.append(f"**架构师**: AI Architect\n\n")
        
        # 统计
        total = len(analysis.suggested_tasks)
        by_priority = self._group_by_priority(analysis.suggested_tasks)
        
        lines.append("## 📊 统计\n")
        lines.append(f"- 总任务: {total}\n")
        lines.append(f"- P0: {len(by_priority.get('critical', []))}\n")
        lines.append(f"- P1: {len(by_priority.get('high', []))}\n")
        lines.append(f"- P2: {len(by_priority.get('medium', []))}\n")
        lines.append(f"- P3: {len(by_priority.get('low', []))}\n\n")
        
        lines.append("---\n\n")
        
        # 任务列表（按优先级分组）
        lines.append("## 📋 任务列表\n\n")
        
        for priority_label, priority_key in [
            ("🔴 高优先级（P0/P1）", ["critical", "high"]),
            ("🟡 普通优先级（P2）", ["medium"]),
            ("🟢 低优先级（P3）", ["low"])
        ]:
            tasks_in_group = []
            for key in priority_key:
                tasks_in_group.extend(by_priority.get(key, []))
            
            if not tasks_in_group:
                continue
            
            lines.append(f"### {priority_label}\n\n")
            
            for task in tasks_in_group:
                lines.append(f"#### {task.id}: {task.title}\n")
                lines.append(f"- **类型**: {task.type}\n")
                lines.append(f"- **范围**: {task.component}\n")
                lines.append(f"- **状态**: 待处理\n")
                lines.append(f"- **优先级**: {task.priority}\n")
                lines.append(f"- **预估工时**: {task.estimated_hours}小时\n")
                lines.append(f"- **建议执行者**: {task.executor_type}\n\n")
                
                lines.append(f"**任务描述**:\n{task.description}\n\n")
                
                if task.acceptance_criteria:
                    lines.append("**验收标准**:\n")
                    for criterion in task.acceptance_criteria:
                        lines.append(f"- [ ] {criterion}\n")
                    lines.append("\n")
                
                if task.related_paths:
                    lines.append("**相关文件**:\n")
                    for path in task.related_paths:
                        lines.append(f"- `{path}`\n")
                    lines.append("\n")
                
                lines.append("---\n\n")
        
        # 问题清单
        if analysis.problems:
            lines.append("## 🔴 发现的问题\n\n")
            for i, problem in enumerate(analysis.problems, 1):
                severity_emoji = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🟢"
                }.get(problem.severity, "⚪")
                
                lines.append(f"### {i}. {problem.title} {severity_emoji} {problem.severity}\n")
                lines.append(f"{problem.description}\n\n")
                lines.append(f"**影响**: {problem.impact}\n\n")
                if problem.suggested_solution:
                    lines.append(f"**建议解决方案**: {problem.suggested_solution}\n\n")
                if problem.related_paths:
                    lines.append(f"**相关文件**: {', '.join(f'`{p}`' for p in problem.related_paths)}\n\n")
                lines.append("---\n\n")
        
        # 功能清单摘要
        if analysis.completed_features or analysis.partial_features:
            lines.append("## 📊 功能清单摘要\n\n")
            lines.append(f"- ✅ 已完成: {len(analysis.completed_features)}个功能\n")
            lines.append(f"- 🟡 部分完成: {len(analysis.partial_features)}个功能\n")
            lines.append(f"\n详见: `docs/arch/architecture-review.md`\n\n")
        
        # 关联链接
        lines.append("---\n\n")
        lines.append("## 🔗 相关文档\n\n")
        lines.append("- [架构清单](../arch/architecture-inventory.md)\n")
        lines.append("- [架构审查](../arch/architecture-review.md)\n")
        lines.append("- [重构计划](../arch/refactor-plan.md)\n")
        
        if analysis.metadata and analysis.metadata.get("taskflow_api"):
            api_url = analysis.metadata["taskflow_api"]
            lines.append(f"\n**任务所·Flow Dashboard**: {api_url}\n")
        
        return "".join(lines)

    # ------------------------------------------------------------------
    # 事件发射封装：用于与全局事件流对接
    # ------------------------------------------------------------------

    def _emit_task_created_event(self, project_id: str, task_id: str, task_title: str) -> None:
        """为新建任务发射 task.created 事件。"""
        if not self._event_emitter:
            return
        try:
            self._event_emitter.emit_task_created(
                project_id=project_id,
                task_id=task_id,
                task_title=task_title,
                actor="AI Architect",
            )
        except Exception:
            # 事件失败不阻塞主流程
            return

    def _emit_issue_created_event(self, project_id: str, issue_id: str, issue_title: str, severity: str) -> None:
        """为新建问题发射 issue.discovered 事件。"""
        if not self._event_emitter:
            return
        try:
            self._event_emitter.emit_issue_discovered(
                project_id=project_id,
                issue_id=issue_id,
                issue_title=issue_title,
                severity=severity,
            )
        except Exception:
            return

    def _emit_architect_analysis_event(self, project_code: str, stats: Dict[str, Any]) -> None:
        """发射一次架构师分析提交的汇总事件。"""
        if not self._event_emitter:
            return
        try:
            self._event_emitter.emit(
                project_id=project_code,
                event_type="architect.analysis_submitted",
                title="架构师分析提交并写入系统",
                description=(
                    f"tasks={stats.get('tasks_created', 0)}, "
                    f"issues={stats.get('issues_created', 0)}, "
                    f"articles={stats.get('articles_created', 0)}"
                ),
                category=EventCategory.SYSTEM,
                source=EventSource.AI,
                actor="AI Architect",
                severity=EventSeverity.INFO,
                related_entity_type="architect_analysis",
                related_entity_id=datetime.now().strftime("ANL-%Y%m%d%H%M%S"),
                tags=["architect", "analysis", "ingest"],
                data=stats,
            )
        except Exception:
            return
    
    def process_handover(self, snapshot: HandoverSnapshot) -> Dict[str, Any]:
        """处理交接快照"""
        # 1. 保存快照到文件
        handover_dir = self.docs_root / "arch" / "handovers"
        handover_dir.mkdir(parents=True, exist_ok=True)
        
        snapshot_path = handover_dir / f"{snapshot.snapshot_id}.json"
        snapshot_path.write_text(
            snapshot.json(indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        # 2. 更新HANDOVER.md
        self._update_handover_md(snapshot)
        
        # 3. TODO: 保存到数据库 handover_snapshots表
        
        return {
            "snapshot_saved": True,
            "snapshot_path": str(snapshot_path),
            "handover_md_updated": True
        }
    
    def _update_handover_md(self, snapshot: HandoverSnapshot) -> None:
        """更新HANDOVER.md交接说明"""
        handover_md_path = self.docs_root / "arch" / "HANDOVER.md"
        
        content = f"""# 最新交接说明

**交接时间**: {snapshot.timestamp}  
**快照ID**: {snapshot.snapshot_id}  
**架构师**: {snapshot.architect}

## 📍 下一任架构师请从这里开始

### 快速上手
1. 阅读快照: `handovers/{snapshot.snapshot_id}.json`
2. 阅读四份核心文档（已更新到最新）:
   - architecture-inventory.md
   - architecture-review.md
   - refactor-plan.md
   - task-board.md

### 当前状态
"""
        
        # 添加完成阶段
        if snapshot.completed_phases:
            content += "\n**已完成阶段**:\n"
            for phase in snapshot.completed_phases:
                content += f"- {phase['phase']}: {phase['progress']}%\n"
        
        # 添加当前焦点
        if snapshot.current_focus:
            focus = snapshot.current_focus
            content += f"\n**当前焦点**: {focus.get('area', 'N/A')}\n"
            content += f"**状态**: {focus.get('status', 'N/A')}\n"
            if focus.get('blockers'):
                content += f"**阻塞**: {', '.join(focus['blockers'])}\n"
        
        # 添加建议
        if snapshot.recommendations_for_next:
            content += "\n### 下一步建议\n"
            for i, rec in enumerate(snapshot.recommendations_for_next, 1):
                content += f"{i}. {rec}\n"
        
        content += f"""
---

**快照文件**: `handovers/{snapshot.snapshot_id}.json`  
**查看完整快照**: 打开上述JSON文件
"""
        
        handover_md_path.write_text(content, encoding='utf-8')
    
    # ========================================================================
    # 辅助方法
    # ========================================================================
    
    def _map_priority(self, priority: str) -> str:
        """映射优先级"""
        mapping = {
            "critical": "P0",
            "high": "P1",
            "medium": "P2",
            "low": "P3"
        }
        return mapping.get(priority.lower(), "P2")
    
    def _infer_complexity(self, hours: float) -> str:
        """根据工时推断复杂度"""
        if hours <= 4:
            return "low"
        elif hours <= 16:
            return "medium"
        else:
            return "high"
    
    def _group_by_priority(
        self,
        tasks: List[ArchitectTaskSuggestion]
    ) -> Dict[str, List[ArchitectTaskSuggestion]]:
        """按优先级分组任务"""
        groups = {}
        for task in tasks:
            priority = task.priority.lower()
            if priority not in groups:
                groups[priority] = []
            groups[priority].append(task)
        return groups
    
    def _format_features_as_markdown(self, features: List[FeatureSummary]) -> str:
        """将功能列表格式化为Markdown"""
        lines = ["# 已实现功能清单\n\n"]
        
        for i, feature in enumerate(features, 1):
            lines.append(f"## {i}. {feature.title}\n\n")
            lines.append(f"{feature.description}\n\n")
            lines.append(f"**完成度**: {feature.completion*100:.0f}%\n\n")
            if feature.related_paths:
                lines.append("**相关文件**:\n")
                for path in feature.related_paths:
                    lines.append(f"- `{path}`\n")
                lines.append("\n")
            if feature.notes:
                lines.append(f"**备注**: {feature.notes}\n\n")
            lines.append("---\n\n")
        
        return "".join(lines)
    
    def _format_partial_features_as_markdown(
        self,
        features: List[PartialFeatureSummary]
    ) -> str:
        """将部分实现功能格式化为Markdown"""
        lines = ["# 部分实现功能清单\n\n"]
        
        for i, feature in enumerate(features, 1):
            lines.append(f"## {i}. {feature.title} ⚠️ {feature.completion*100:.0f}%\n\n")
            lines.append(f"{feature.description}\n\n")
            
            lines.append(f"**已完成**: {feature.completion*100:.0f}%\n\n")
            
            lines.append("**缺少部分**:\n")
            for missing in feature.missing:
                lines.append(f"- ❌ {missing}\n")
            lines.append("\n")
            
            if feature.risk:
                lines.append(f"**风险**: {feature.risk}\n\n")
            
            lines.append(f"**优先级**: {feature.priority}\n\n")
            lines.append("---\n\n")
        
        return "".join(lines)


# ============================================================================
# 辅助函数
# ============================================================================

def create_architect_orchestrator(state_manager=None, docs_root="docs"):
    """创建架构师编排器实例（工厂函数）"""
    return ArchitectOrchestrator(
        state_manager=state_manager,
        docs_root=docs_root
    )

