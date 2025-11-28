#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
替换全栈工程师模块 - 部署到8820端口
按照8820端口部署提示词的标准流程
"""

import os
import datetime

# 配置
INDEX_FILE = 'index.html'
BACKUP_DIR = '.'

def backup_file():
    """Step 1: 备份文件"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_name = f'{INDEX_FILE}.backup-fullstack-engineer-{timestamp}'
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(backup_name, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] 备份完成: {backup_name}")
    return backup_name

def read_file():
    """读取index.html"""
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_file(lines):
    """写入index.html"""
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def get_new_engineer_html():
    """Step 2: 获取新的全栈工程师模块HTML"""
    return '''        <!-- ========== 全栈工程师工作台 ========== -->
        <div class="engineer-module version-content" data-version="1">
            <!-- 模块头部 -->
            <div class="engineer-module-header">
                <div class="engineer-header-row">
                    <h2 class="engineer-module-title">全栈工程师工作台</h2>
                    <span class="engineer-status-badge">
                        <span class="engineer-status-dot"></span>
                        在线 · 3人并行
                    </span>
                </div>

                <div class="engineer-info-bar">
                    <div class="engineer-info-section">
                        <div class="engineer-avatar">FS</div>
                        <div class="engineer-details">
                            <div class="engineer-name">Fullstack Engineer AI</div>
                            <div class="engineer-meta">Expert Level · 接手: 2025-11-18 14:00 · 工作时长: 2天6小时</div>
                        </div>
                    </div>
                    <div class="engineer-quick-stats">
                        <div class="engineer-stat-item">
                            <div class="engineer-stat-value">156K</div>
                            <div class="engineer-stat-label">Token已用</div>
                        </div>
                        <div class="engineer-stat-item">
                            <div class="engineer-stat-value">v3.1</div>
                            <div class="engineer-stat-label">提示词</div>
                        </div>
                        <div class="engineer-stat-item">
                            <div class="engineer-stat-value">67</div>
                            <div class="engineer-stat-label">事件</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tab导航（精简到5个） -->
            <div class="engineer-tab-navigation">
                <button class="engineer-tab-item active" onclick="switchEngineerTab('engineer-events')">
                    事件流
                    <span class="engineer-tab-badge">67</span>
                </button>
                <button class="engineer-tab-item" onclick="switchEngineerTab('engineer-taskboard')">
                    任务看板
                    <span class="engineer-tab-badge">43</span>
                </button>
                <button class="engineer-tab-item" onclick="switchEngineerTab('engineer-reviews')">
                    代码审查
                    <span class="engineer-tab-badge">15</span>
                </button>
                <button class="engineer-tab-item" onclick="switchEngineerTab('engineer-docs')">
                    技术文档
                    <span class="engineer-tab-badge">68</span>
                </button>
                <button class="engineer-tab-item" onclick="switchEngineerTab('engineer-conversations')">
                    对话历史
                    <span class="engineer-tab-badge">12</span>
                </button>
            </div>

            <!-- Tab内容 -->
            <div class="engineer-tab-content-wrapper">
                <!-- Tab 1: 事件流 -->
                <div id="engineer-events" class="engineer-tab-pane active">
                    <div class="engineer-event-timeline">
                        <div class="engineer-timeline-filters">
                            <button class="engineer-filter-chip active">全部</button>
                            <button class="engineer-filter-chip">今天</button>
                            <button class="engineer-filter-chip">本周</button>
                            <button class="engineer-filter-chip">任务</button>
                            <button class="engineer-filter-chip">代码</button>
                            <button class="engineer-filter-chip">部署</button>
                        </div>

                        <div class="engineer-event-list">
                            <div class="engineer-event-item">
                                <div class="engineer-event-marker"></div>
                                <div class="engineer-event-card">
                                    <div class="engineer-event-header">
                                        <div>
                                            <div class="engineer-event-title">任务完成: Dashboard响应式优化</div>
                                            <div class="engineer-event-meta">Fullstack Engineer AI · TASK-FE-045</div>
                                        </div>
                                        <div class="engineer-event-time">2025-11-19 16:30</div>
                                    </div>
                                    <div class="engineer-event-description">
                                        完成了Dashboard的完整响应式优化，支持1920/1440/1280/768/375五个断点。
                                        实现了Flexbox+Grid混合布局，移动端优先策略，触摸手势优化。
                                    </div>
                                    <div class="engineer-event-tags">
                                        <span class="engineer-event-tag">前端开发</span>
                                        <span class="engineer-event-tag">响应式</span>
                                        <span class="engineer-event-tag">已完成</span>
                                    </div>
                                </div>
                            </div>

                            <div class="engineer-event-item">
                                <div class="engineer-event-marker"></div>
                                <div class="engineer-event-card">
                                    <div class="engineer-event-header">
                                        <div>
                                            <div class="engineer-event-title">代码审查通过: API集成模块</div>
                                            <div class="engineer-event-meta">架构师审查 · REVIEW-014</div>
                                        </div>
                                        <div class="engineer-event-time">2025-11-19 14:20</div>
                                    </div>
                                    <div class="engineer-event-description">
                                        架构师审查通过，代码质量优秀。成功集成了Claude API和Notion API，
                                        包含完整的错误处理、重试机制和日志记录。已合并到主分支。
                                    </div>
                                    <div class="engineer-event-tags">
                                        <span class="engineer-event-tag">代码审查</span>
                                        <span class="engineer-event-tag">API集成</span>
                                        <span class="engineer-event-tag">已通过</span>
                                    </div>
                                </div>
                            </div>

                            <div class="engineer-event-item">
                                <div class="engineer-event-marker"></div>
                                <div class="engineer-event-card">
                                    <div class="engineer-event-header">
                                        <div>
                                            <div class="engineer-event-title">接收任务: 实现记忆管理Tab</div>
                                            <div class="engineer-event-meta">架构师分配 → Fullstack Engineer AI</div>
                                        </div>
                                        <div class="engineer-event-time">2025-11-19 10:00</div>
                                    </div>
                                    <div class="engineer-event-description">
                                        架构师分配了新任务：实现Dashboard项目记忆Tab。包括记忆增删改查、
                                        分类管理、搜索功能。预估3小时，可并行开发。
                                    </div>
                                    <div class="engineer-event-tags">
                                        <span class="engineer-event-tag">任务分配</span>
                                        <span class="engineer-event-tag">可并行</span>
                                    </div>
                                </div>
                            </div>

                            <div class="engineer-event-item">
                                <div class="engineer-event-marker"></div>
                                <div class="engineer-event-card">
                                    <div class="engineer-event-header">
                                        <div>
                                            <div class="engineer-event-title">部署成功: Dashboard v2.1.0</div>
                                            <div class="engineer-event-meta">CI/CD Pipeline · DEPLOY-028</div>
                                        </div>
                                        <div class="engineer-event-time">2025-11-18 18:45</div>
                                    </div>
                                    <div class="engineer-event-description">
                                        成功部署到生产环境。通过了所有自动化测试（单元测试92%覆盖率，
                                        E2E测试18个场景全通过）。Lighthouse性能评分: 98/100。
                                    </div>
                                    <div class="engineer-event-tags">
                                        <span class="engineer-event-tag">部署</span>
                                        <span class="engineer-event-tag">生产环境</span>
                                        <span class="engineer-event-tag">成功</span>
                                    </div>
                                </div>
                            </div>

                            <div class="engineer-event-item">
                                <div class="engineer-event-marker"></div>
                                <div class="engineer-event-card">
                                    <div class="engineer-event-header">
                                        <div>
                                            <div class="engineer-event-title">Bug修复: 知识图谱渲染问题</div>
                                            <div class="engineer-event-meta">Fullstack Engineer AI · BUG-012</div>
                                        </div>
                                        <div class="engineer-event-time">2025-11-18 14:30</div>
                                    </div>
                                    <div class="engineer-event-description">
                                        修复了知识图谱在大数据量下的渲染卡顿问题。采用虚拟滚动+WebWorker
                                        方案，渲染性能提升80%，支持10000+节点流畅显示。
                                    </div>
                                    <div class="engineer-event-tags">
                                        <span class="engineer-event-tag">Bug修复</span>
                                        <span class="engineer-event-tag">性能优化</span>
                                        <span class="engineer-event-tag">已完成</span>
                                    </div>
                                </div>
                            </div>

                            <div class="engineer-event-item">
                                <div class="engineer-event-marker"></div>
                                <div class="engineer-event-card">
                                    <div class="engineer-event-header">
                                        <div>
                                            <div class="engineer-event-title">数据库优化: Neo4j查询性能提升</div>
                                            <div class="engineer-event-meta">Fullstack Engineer AI · OPT-008</div>
                                        </div>
                                        <div class="engineer-event-time">2025-11-17 16:20</div>
                                    </div>
                                    <div class="engineer-event-description">
                                        优化了Neo4j的Cypher查询语句，添加了合适的索引。复杂关系查询
                                        从2.5s优化到0.3s，提升8倍性能。同时优化了连接池配置。
                                    </div>
                                    <div class="engineer-event-tags">
                                        <span class="engineer-event-tag">数据库</span>
                                        <span class="engineer-event-tag">性能优化</span>
                                        <span class="engineer-event-tag">Neo4j</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tab 2: 任务看板 -->
                <div id="engineer-taskboard" class="engineer-tab-pane">
                    <div class="engineer-taskboard-header">
                        <div class="engineer-filter-bar">
                            <div class="engineer-filter-chips">
                                <button class="engineer-filter-chip active">全部</button>
                                <button class="engineer-filter-chip">P0</button>
                                <button class="engineer-filter-chip">P1</button>
                                <button class="engineer-filter-chip">可并行</button>
                                <button class="engineer-filter-chip">前端</button>
                                <button class="engineer-filter-chip">后端</button>
                            </div>
                            <select class="engineer-sort-select">
                                <option>按优先级排序</option>
                                <option>按时间排序</option>
                                <option>按复杂度排序</option>
                            </select>
                        </div>
                    </div>

                    <div class="engineer-kanban-board">
                        <!-- 待处理列 -->
                        <div class="engineer-kanban-column">
                            <div class="engineer-column-header">
                                <div class="engineer-column-title">
                                    <span>待处理</span>
                                    <span class="engineer-column-count">18</span>
                                </div>
                            </div>
                            <div class="engineer-column-cards">
                                <div class="engineer-task-card">
                                    <div class="engineer-task-header">
                                        <span class="engineer-task-id">TASK-UI-028</span>
                                        <h3 class="engineer-task-title">实现记忆管理Tab</h3>
                                        <span class="engineer-task-badge parallel">可并行</span>
                                    </div>
                                    <div class="engineer-task-description">
                                        实现Dashboard项目记忆Tab，包括记忆增删改查、分类管理、搜索功能。
                                        需要前后端联调，使用Neo4j存储。
                                    </div>
                                    <div class="engineer-task-meta">
                                        <span>预估: <span class="engineer-task-estimate">3小时</span></span>
                                        <span class="engineer-priority-badge p1">P1</span>
                                    </div>
                                    <div class="engineer-task-assignee">
                                        <div class="engineer-assignee-avatar">FS</div>
                                        <span>待领取</span>
                                    </div>
                                    <div class="engineer-task-actions">
                                        <button class="engineer-task-btn primary" onclick="copyEngineerPrompt(event)">复制提示词</button>
                                        <button class="engineer-task-btn">查看详情</button>
                                    </div>
                                </div>

                                <div class="engineer-task-card">
                                    <div class="engineer-task-header">
                                        <span class="engineer-task-id">TASK-BE-015</span>
                                        <h3 class="engineer-task-title">实现API限流中间件</h3>
                                    </div>
                                    <div class="engineer-task-description">
                                        基于Redis实现API限流中间件，支持IP级别和用户级别限流。
                                        采用令牌桶算法，配置化限流规则。
                                    </div>
                                    <div class="engineer-task-meta">
                                        <span>预估: <span class="engineer-task-estimate">4小时</span></span>
                                        <span class="engineer-priority-badge p2">P2</span>
                                    </div>
                                    <div class="engineer-task-assignee">
                                        <div class="engineer-assignee-avatar">FS</div>
                                        <span>待领取</span>
                                    </div>
                                    <div class="engineer-task-actions">
                                        <button class="engineer-task-btn primary" onclick="copyEngineerPrompt(event)">复制提示词</button>
                                        <button class="engineer-task-btn">查看详情</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 进行中列 -->
                        <div class="engineer-kanban-column">
                            <div class="engineer-column-header">
                                <div class="engineer-column-title">
                                    <span>进行中</span>
                                    <span class="engineer-column-count">5</span>
                                </div>
                            </div>
                            <div class="engineer-column-cards">
                                <div class="engineer-task-card">
                                    <div class="engineer-task-header">
                                        <span class="engineer-task-id">TASK-BE-012</span>
                                        <h3 class="engineer-task-title">Claude API集成</h3>
                                    </div>
                                    <div class="engineer-task-description">
                                        集成Claude API实现对话功能。包括流式响应、错误处理、
                                        Token统计、会话管理。已完成60%。
                                    </div>
                                    <div class="engineer-task-meta">
                                        <span>已用: <span class="engineer-task-estimate">1.5天</span></span>
                                        <span class="engineer-priority-badge p0">P0</span>
                                    </div>
                                    <div class="engineer-task-assignee">
                                        <div class="engineer-assignee-avatar">FS</div>
                                        <span>进行中</span>
                                    </div>
                                    <div class="engineer-task-actions">
                                        <button class="engineer-task-btn primary">提交审查</button>
                                        <button class="engineer-task-btn">查看详情</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 已完成列 -->
                        <div class="engineer-kanban-column">
                            <div class="engineer-column-header">
                                <div class="engineer-column-title">
                                    <span>已完成</span>
                                    <span class="engineer-column-count">20</span>
                                </div>
                            </div>
                            <div class="engineer-column-cards">
                                <div class="engineer-task-card">
                                    <div class="engineer-task-header">
                                        <span class="engineer-task-id">TASK-UI-024</span>
                                        <h3 class="engineer-task-title">Dashboard响应式优化</h3>
                                        <span class="engineer-task-badge">✓ 已完成</span>
                                    </div>
                                    <div class="engineer-task-description">
                                        完成了Dashboard的完整响应式优化，支持5个断点。
                                        已通过所有浏览器兼容性测试。
                                    </div>
                                    <div class="engineer-task-meta">
                                        <span>用时: <span class="engineer-task-estimate">6小时</span></span>
                                        <span class="engineer-priority-badge p1">P1</span>
                                    </div>
                                    <div class="engineer-task-assignee">
                                        <div class="engineer-assignee-avatar">FS</div>
                                        <span>2025-11-19</span>
                                    </div>
                                    <div class="engineer-task-actions">
                                        <button class="engineer-task-btn primary">查看完成报告</button>
                                        <button class="engineer-task-btn">查看详情</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tab 3-5 省略，保持简洁 -->
            </div>
        </div>


'''

def replace_engineer_module():
    """Step 3: 替换全栈工程师模块"""
    lines = read_file()
    
    # 找到全栈工程师模块的开始和结束
    start_line = None
    end_line = None
    
    for i, line in enumerate(lines):
        if '<!-- ========== 全栈工程师工作台 ========== -->' in line:
            start_line = i
        if start_line is not None and '<!-- ========== API状态条 ========== -->' in line:
            end_line = i
            break
    
    if start_line is None:
        print("[ERROR] 找不到全栈工程师模块")
        return False
    
    print(f"[FIND] 找到全栈工程师模块: 行 {start_line+1} - {end_line}")
    
    # 验证下一个模块
    if end_line:
        print(f"[OK] 验证: 下一个模块是 API状态条 (行 {end_line+1})")
    
    # 替换模块
    new_html = get_new_engineer_html()
    new_lines = lines[:start_line] + [new_html] + lines[end_line:]
    
    # 写入文件
    write_file(new_lines)
    
    print(f"[OK] 替换完成! 删除了 {end_line - start_line} 行，添加了新模块")
    print(f"[INFO] 新文件行数: {len(new_lines)}")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("全栈工程师模块替换 - 部署到8820端口")
    print("=" * 60)
    
    # Step 1: 备份
    backup_name = backup_file()
    
    # Step 3: 替换模块
    if replace_engineer_module():
        print("\n" + "=" * 60)
        print("[SUCCESS] 替换完成!")
        print("=" * 60)
        print(f"\n[NEXT] 后续步骤:")
        print(f"1. 重启8820服务器:")
        print(f"   ps aux | grep \"http.server 8820\" | grep -v grep | awk '{{print $2}}' | xargs kill -9 2>/dev/null")
        print(f"   python -m http.server 8820")
        print(f"\n2. 浏览器强制刷新: Ctrl + Shift + R")
        print(f"\n3. 访问: http://localhost:8820/")
        print(f"\n4. 如有问题，恢复备份:")
        print(f"   copy {backup_name} {INDEX_FILE}")
    else:
        print("\n[FAILED] 替换失败!")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()

