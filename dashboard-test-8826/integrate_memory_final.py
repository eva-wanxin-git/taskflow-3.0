#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正确集成记忆空间模块 - 类名完全匹配原版
"""

# 读取index.html
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到插入位置
insert_line = None
for i, line in enumerate(lines):
    if '<!-- ========== 运维工程师工作台 ========== -->' in line:
        insert_line = i
        break

css_insert_line = None
for i, line in enumerate(lines):
    if '.devops-module {' in line:
        css_insert_line = i
        break

js_insert_line = None
for i, line in enumerate(lines):
    if '// ========== 运维工程师模块函数 ==========' in line:
        js_insert_line = i
        break

print(f"HTML插入位置: 第{insert_line+1}行")
print(f"CSS插入位置: 第{css_insert_line+1}行")
print(f"JS插入位置: 第{js_insert_line+1}行")

# CSS - 使用父级选择器限定作用域，保持原版类名
memory_css = '''
        /* ==================== 记忆空间模块 ==================== */
        .memory-space-module {
            max-width: 1600px;
            margin: 0 auto 48px auto;
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            height: calc(100vh - 80px);
            display: flex;
        }

        .memory-space-module .memory-overview {
            width: 380px;
            border-right: 1px solid var(--blanc-mist);
            background: var(--blanc-snow);
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }

        .memory-space-module .overview-header {
            padding: 32px 24px 24px 24px;
            border-bottom: 1px solid var(--blanc-mist);
        }

        .memory-space-module .overview-title {
            font-family: var(--font-secondary);
            font-size: var(--text-xl);
            font-weight: var(--weight-light);
            color: var(--noir-ink);
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }

        .memory-space-module .overview-subtitle {
            font-size: var(--text-xs);
            color: var(--noir-silver);
        }

        .memory-space-module .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            padding: 24px;
            border-bottom: 1px solid var(--blanc-mist);
        }

        .memory-space-module .stat-card {
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .memory-space-module .stat-card:hover {
            box-shadow: var(--shadow-sm);
            transform: translateY(-2px);
        }

        .memory-space-module .stat-label {
            font-size: var(--text-xs);
            color: var(--noir-silver);
            margin-bottom: 8px;
        }

        .memory-space-module .stat-value {
            font-size: var(--text-2xl);
            font-weight: var(--weight-light);
            color: var(--noir-ink);
            font-family: var(--font-mono);
        }

        .memory-space-module .recent-memories {
            padding: 24px;
        }

        .memory-space-module .recent-header {
            font-size: var(--text-sm);
            font-weight: var(--weight-semibold);
            color: var(--noir-charcoal);
            margin-bottom: 16px;
        }

        .memory-space-module .recent-item {
            padding: 12px 0;
            border-bottom: 1px solid var(--blanc-mist);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .memory-space-module .recent-item:last-child {
            border-bottom: none;
        }

        .memory-space-module .recent-item:hover {
            padding-left: 8px;
        }

        .memory-space-module .recent-item-type {
            font-size: 11px;
            color: var(--noir-silver);
            margin-bottom: 4px;
        }

        .memory-space-module .recent-item-title {
            font-size: var(--text-sm);
            color: var(--noir-graphite);
            line-height: var(--leading-tight);
        }

        .memory-space-module .memory-stream {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--blanc-pure);
            min-height: 0;
        }

        .memory-space-module .stream-filters {
            display: flex;
            gap: 12px;
            padding: 24px 32px;
            border-bottom: 1px solid var(--blanc-mist);
            background: var(--blanc-snow);
        }

        .memory-space-module .filter-chip {
            padding: 8px 16px;
            font-size: var(--text-sm);
            border: 1px solid var(--blanc-cloud);
            background: var(--blanc-pure);
            color: var(--noir-graphite);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .memory-space-module .filter-chip:hover {
            border-color: var(--noir-steel);
        }

        .memory-space-module .filter-chip.active {
            background: var(--noir-ink);
            color: var(--blanc-pure);
            border-color: var(--noir-ink);
        }

        .memory-space-module .memory-timeline {
            flex: 1;
            overflow-y: auto;
            padding: 40px 32px 40px 72px;
            position: relative;
            min-height: 0;
        }

        .memory-space-module .memory-timeline::before {
            content: '';
            position: absolute;
            left: 32px;
            top: 0;
            bottom: 0;
            width: 1px;
            background: var(--blanc-mist);
        }

        .memory-space-module .memory-item {
            position: relative;
            margin-bottom: 32px;
            transition: all 0.3s ease;
        }

        .memory-space-module .memory-marker {
            position: absolute;
            left: -48px;
            top: 0;
            width: 16px;
            height: 16px;
            border: 2px solid var(--noir-ink);
            background: var(--blanc-pure);
        }

        .memory-space-module .memory-marker.decision {
            background: var(--noir-ink);
        }

        .memory-space-module .memory-marker.solution {
            border-color: var(--noir-graphite);
        }

        .memory-space-module .memory-marker.knowledge {
            border-color: var(--noir-silver);
            background: var(--blanc-snow);
        }

        .memory-space-module .memory-card {
            background: var(--blanc-snow);
            border: 1px solid var(--blanc-mist);
            padding: 24px;
            transition: all 0.3s ease;
        }

        .memory-space-module .memory-card:hover {
            box-shadow: var(--shadow-sm);
            transform: translateX(4px);
        }

        .memory-space-module .memory-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 12px;
        }

        .memory-space-module .memory-type-badge {
            display: inline-block;
            padding: 4px 12px;
            font-size: 11px;
            border: 1px solid var(--blanc-cloud);
            color: var(--noir-graphite);
            margin-bottom: 8px;
        }

        .memory-space-module .memory-type-badge.decision {
            background: var(--noir-ink);
            color: var(--blanc-pure);
            border-color: var(--noir-ink);
        }

        .memory-space-module .memory-type-badge.solution {
            border-color: var(--noir-graphite);
        }

        .memory-space-module .memory-type-badge.knowledge {
            border-color: var(--noir-silver);
        }

        .memory-space-module .memory-title {
            font-size: var(--text-base);
            font-weight: var(--weight-semibold);
            color: var(--noir-charcoal);
            margin-bottom: 6px;
        }

        .memory-space-module .memory-meta {
            display: flex;
            gap: 16px;
            font-size: var(--text-xs);
            color: var(--noir-silver);
        }

        .memory-space-module .memory-content {
            font-size: var(--text-sm);
            color: var(--noir-steel);
            line-height: var(--leading-relaxed);
            margin-top: 12px;
        }

        .memory-space-module .memory-tags {
            display: flex;
            gap: 8px;
            margin-top: 16px;
            flex-wrap: wrap;
        }

        .memory-space-module .memory-tag {
            padding: 4px 12px;
            font-size: 11px;
            border: 1px solid var(--blanc-cloud);
            color: var(--noir-graphite);
        }

'''

# HTML - 使用原版类名
memory_html = '''        <!-- ========== 记忆空间模块 ========== -->
        <div class="memory-space-module version-content" data-version="1">
            <!-- 左侧：概览面板 -->
            <div class="memory-overview">
                <div class="overview-header">
                    <h2 class="overview-title">记忆空间</h2>
                    <p class="overview-subtitle">基于MCP自动生成的项目知识库</p>
                </div>

                <!-- 统计卡片 -->
                <div class="stats-grid">
                    <div class="stat-card" data-filter="all">
                        <div class="stat-label">总记忆</div>
                        <div class="stat-value">45</div>
                    </div>

                    <div class="stat-card" data-filter="decision">
                        <div class="stat-label">决策</div>
                        <div class="stat-value">12</div>
                    </div>

                    <div class="stat-card" data-filter="solution">
                        <div class="stat-label">方案</div>
                        <div class="stat-value">23</div>
                    </div>

                    <div class="stat-card" data-filter="important">
                        <div class="stat-label">重要</div>
                        <div class="stat-value">8</div>
                    </div>
                </div>

                <!-- 最新记忆 -->
                <div class="recent-memories">
                    <div class="recent-header">最新记忆</div>

                    <div class="recent-item" onclick="jumpToMemory('memory-1')">
                        <div class="recent-item-type">决策 · 2天前</div>
                        <div class="recent-item-title">ADR: 采用Monorepo架构</div>
                    </div>

                    <div class="recent-item" onclick="jumpToMemory('memory-2')">
                        <div class="recent-item-type">方案 · 3天前</div>
                        <div class="recent-item-title">解决Tab切换bug的方案</div>
                    </div>

                    <div class="recent-item" onclick="jumpToMemory('memory-3')">
                        <div class="recent-item-type">知识 · 5天前</div>
                        <div class="recent-item-title">React Hooks最佳实践</div>
                    </div>
                </div>
            </div>

            <!-- 右侧：记忆流 -->
            <div class="memory-stream">
                <!-- 筛选栏 -->
                <div class="stream-filters">
                    <button class="filter-chip active" onclick="filterMemories('all')">全部</button>
                    <button class="filter-chip" onclick="filterMemories('decision')">决策</button>
                    <button class="filter-chip" onclick="filterMemories('solution')">方案</button>
                    <button class="filter-chip" onclick="filterMemories('knowledge')">知识</button>
                    <button class="filter-chip" onclick="filterMemories('important')">重要</button>
                </div>

                <!-- 记忆时间线 -->
                <div class="memory-timeline">
                    <!-- 记忆项1: 决策 -->
                    <div class="memory-item" id="memory-1" data-type="decision important">
                        <div class="memory-marker decision"></div>
                        <div class="memory-card">
                            <div class="memory-header">
                                <div>
                                    <span class="memory-type-badge decision">决策</span>
                                    <h3 class="memory-title">ADR: 采用Monorepo架构</h3>
                                    <div class="memory-meta">
                                        <span>2025-11-17 10:00</span>
                                        <span>AI Architect</span>
                                        <span>重要度: ⭐⭐⭐⭐⭐⭐⭐⭐</span>
                                    </div>
                                </div>
                            </div>
                            <div class="memory-content">
                                <strong>背景：</strong> 项目规模扩大，需要统一管理多个子项目，包括前端、后端、文档、工具库等。<br><br>
                                <strong>决策：</strong> 采用pnpm workspace实现Monorepo架构，统一依赖管理和构建流程。<br><br>
                                <strong>备选方案：</strong> Lerna、Nx、Turborepo<br><br>
                                <strong>影响范围：</strong> 影响5个核心组件的开发流程
                            </div>
                            <div class="memory-tags">
                                <span class="memory-tag">架构决策</span>
                                <span class="memory-tag">Monorepo</span>
                                <span class="memory-tag">已采纳</span>
                            </div>
                        </div>
                    </div>

                    <!-- 记忆项2: 方案 -->
                    <div class="memory-item" id="memory-2" data-type="solution">
                        <div class="memory-marker solution"></div>
                        <div class="memory-card">
                            <div class="memory-header">
                                <div>
                                    <span class="memory-type-badge solution">方案</span>
                                    <h3 class="memory-title">解决Tab切换bug的方案</h3>
                                    <div class="memory-meta">
                                        <span>2025-11-16 14:30</span>
                                        <span>AI Architect</span>
                                    </div>
                                </div>
                            </div>
                            <div class="memory-content">
                                <strong>问题：</strong> Tab切换时出现闪烁，用户体验不佳。<br><br>
                                <strong>原因分析：</strong> display: none切换导致重绘，且没有过渡动画。<br><br>
                                <strong>解决方案：</strong> 
                                1. 使用opacity + visibility替代display切换<br>
                                2. 添加0.3s过渡动画<br>
                                3. 预加载所有Tab内容，避免懒加载闪烁<br><br>
                                <strong>效果：</strong> 切换流畅度提升，用户反馈良好
                            </div>
                            <div class="memory-tags">
                                <span class="memory-tag">Bug修复</span>
                                <span class="memory-tag">交互优化</span>
                                <span class="memory-tag">已实施</span>
                            </div>
                        </div>
                    </div>

                    <!-- 记忆项3: 知识 -->
                    <div class="memory-item" id="memory-3" data-type="knowledge">
                        <div class="memory-marker knowledge"></div>
                        <div class="memory-card">
                            <div class="memory-header">
                                <div>
                                    <span class="memory-type-badge knowledge">知识</span>
                                    <h3 class="memory-title">React Hooks最佳实践</h3>
                                    <div class="memory-meta">
                                        <span>2025-11-15 09:20</span>
                                        <span>学习笔记</span>
                                    </div>
                                </div>
                            </div>
                            <div class="memory-content">
                                <strong>核心原则：</strong><br>
                                1. 只在顶层调用Hooks，不在循环/条件/嵌套中使用<br>
                                2. 只在React函数组件或自定义Hook中调用<br>
                                3. 使用ESLint规则确保正确使用<br><br>
                                <strong>常见陷阱：</strong><br>
                                - useEffect依赖项遗漏导致闭包陷阱<br>
                                - 过度使用useState导致重渲染<br>
                                - 忘记清理副作用导致内存泄漏
                            </div>
                            <div class="memory-tags">
                                <span class="memory-tag">React</span>
                                <span class="memory-tag">Hooks</span>
                                <span class="memory-tag">最佳实践</span>
                            </div>
                        </div>
                    </div>

                    <!-- 记忆项4: 决策 -->
                    <div class="memory-item" data-type="decision important">
                        <div class="memory-marker decision"></div>
                        <div class="memory-card">
                            <div class="memory-header">
                                <div>
                                    <span class="memory-type-badge decision">决策</span>
                                    <h3 class="memory-title">ADR: 使用FastAPI构建后端</h3>
                                    <div class="memory-meta">
                                        <span>2025-11-14 16:00</span>
                                        <span>AI Architect</span>
                                        <span>重要度: ⭐⭐⭐⭐⭐⭐⭐</span>
                                    </div>
                                </div>
                            </div>
                            <div class="memory-content">
                                <strong>背景：</strong> 需要构建高性能的API服务，支持异步处理和自动文档生成。<br><br>
                                <strong>决策：</strong> 选择FastAPI作为后端框架，基于Python 3.10+和Pydantic。<br><br>
                                <strong>备选方案：</strong> Django REST Framework、Flask、Express.js<br><br>
                                <strong>优势：</strong> 
                                - 原生异步支持，性能接近Node.js<br>
                                - 自动生成OpenAPI文档<br>
                                - 类型提示和数据验证<br>
                                - 与Claude API集成友好
                            </div>
                            <div class="memory-tags">
                                <span class="memory-tag">架构决策</span>
                                <span class="memory-tag">FastAPI</span>
                                <span class="memory-tag">后端</span>
                                <span class="memory-tag">已采纳</span>
                            </div>
                        </div>
                    </div>

                    <!-- 记忆项5: 方案 -->
                    <div class="memory-item" data-type="solution">
                        <div class="memory-marker solution"></div>
                        <div class="memory-card">
                            <div class="memory-header">
                                <div>
                                    <span class="memory-type-badge solution">方案</span>
                                    <h3 class="memory-title">知识库数据库设计方案</h3>
                                    <div class="memory-meta">
                                        <span>2025-11-13 11:30</span>
                                        <span>全栈工程师AI</span>
                                    </div>
                                </div>
                            </div>
                            <div class="memory-content">
                                <strong>技术选型：</strong> Neo4j图数据库<br><br>
                                <strong>核心实体：</strong><br>
                                - 知识节点（Knowledge）<br>
                                - 任务节点（Task）<br>
                                - 文档节点（Document）<br>
                                - ADR节点（Decision）<br><br>
                                <strong>关系设计：</strong><br>
                                - DEPENDS_ON: 依赖关系<br>
                                - REFERENCES: 引用关系<br>
                                - DERIVED_FROM: 衍生关系<br>
                                - IMPLEMENTS: 实现关系
                            </div>
                            <div class="memory-tags">
                                <span class="memory-tag">数据库设计</span>
                                <span class="memory-tag">Neo4j</span>
                                <span class="memory-tag">已实现</span>
                            </div>
                        </div>
                    </div>

                    <!-- 记忆项6: 知识 -->
                    <div class="memory-item" data-type="knowledge">
                        <div class="memory-marker knowledge"></div>
                        <div class="memory-card">
                            <div class="memory-header">
                                <div>
                                    <span class="memory-type-badge knowledge">知识</span>
                                    <h3 class="memory-title">CSS Grid vs Flexbox选择指南</h3>
                                    <div class="memory-meta">
                                        <span>2025-11-12 15:45</span>
                                        <span>学习笔记</span>
                                    </div>
                                </div>
                            </div>
                            <div class="memory-content">
                                <strong>何时使用Grid：</strong><br>
                                - 二维布局（行+列同时控制）<br>
                                - 固定网格结构（如卡片列表）<br>
                                - 需要对齐到网格线<br><br>
                                <strong>何时使用Flexbox：</strong><br>
                                - 一维布局（单行或单列）<br>
                                - 内容驱动的布局<br>
                                - 需要灵活的空间分配<br><br>
                                <strong>最佳实践：</strong> 两者结合使用，Grid定义整体框架，Flexbox处理内部对齐
                            </div>
                            <div class="memory-tags">
                                <span class="memory-tag">CSS</span>
                                <span class="memory-tag">布局</span>
                                <span class="memory-tag">最佳实践</span>
                            </div>
                        </div>
                    </div>

                    <!-- 记忆项7: 决策 -->
                    <div class="memory-item" data-type="decision">
                        <div class="memory-marker decision"></div>
                        <div class="memory-card">
                            <div class="memory-header">
                                <div>
                                    <span class="memory-type-badge decision">决策</span>
                                    <h3 class="memory-title">ADR: 采用事件驱动架构</h3>
                                    <div class="memory-meta">
                                        <span>2025-11-11 14:20</span>
                                        <span>AI Architect</span>
                                        <span>重要度: ⭐⭐⭐⭐⭐⭐</span>
                                    </div>
                                </div>
                            </div>
                            <div class="memory-content">
                                <strong>背景：</strong> 系统模块间需要松耦合的通信方式，支持异步处理和扩展性。<br><br>
                                <strong>决策：</strong> 采用事件驱动架构，使用消息队列（RabbitMQ/Redis）作为事件总线。<br><br>
                                <strong>优势：</strong><br>
                                - 解耦模块间依赖<br>
                                - 支持异步处理<br>
                                - 易于水平扩展<br>
                                - 便于审计和重放
                            </div>
                            <div class="memory-tags">
                                <span class="memory-tag">架构决策</span>
                                <span class="memory-tag">事件驱动</span>
                                <span class="memory-tag">已采纳</span>
                            </div>
                        </div>
                    </div>

                    <!-- 记忆项8: 方案 -->
                    <div class="memory-item" data-type="solution important">
                        <div class="memory-marker solution"></div>
                        <div class="memory-card">
                            <div class="memory-header">
                                <div>
                                    <span class="memory-type-badge solution">方案</span>
                                    <h3 class="memory-title">Dashboard架构重构方案</h3>
                                    <div class="memory-meta">
                                        <span>2025-11-10 16:30</span>
                                        <span>AI Architect</span>
                                    </div>
                                </div>
                            </div>
                            <div class="memory-content">
                                <strong>问题诊断：</strong><br>
                                - 组件耦合度过高（3000+行代码）<br>
                                - 缺乏模块化设计<br>
                                - 性能问题（重渲染频繁）<br><br>
                                <strong>重构方案：</strong><br>
                                采用模块化架构，拆分为7个独立模块：<br>
                                - TaskBoard 任务看板<br>
                                - EventStream 事件流<br>
                                - ConversationHub 对话中心<br>
                                - ArchitectConsole 架构师控制台<br>
                                - KnowledgeGraph 知识图谱<br>
                                - Analytics 分析面板<br><br>
                                <strong>预期效果：</strong> 代码量减少60%，首屏性能提升60%
                            </div>
                            <div class="memory-tags">
                                <span class="memory-tag">架构重构</span>
                                <span class="memory-tag">Dashboard</span>
                                <span class="memory-tag">已实施</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

'''

# JavaScript
memory_js = '''
        // ========== 记忆空间模块函数 ==========
        function filterMemories(type) {
            document.querySelectorAll('.memory-space-module .filter-chip').forEach(chip => {
                chip.classList.remove('active');
            });
            event.target.classList.add('active');

            const items = document.querySelectorAll('.memory-space-module .memory-item');
            items.forEach(item => {
                if (type === 'all') {
                    item.style.display = 'block';
                } else {
                    const itemTypes = item.dataset.type.split(' ');
                    if (itemTypes.includes(type)) {
                        item.style.display = 'block';
                    } else {
                        item.style.display = 'none';
                    }
                }
            });
        }

        function jumpToMemory(memoryId) {
            const element = document.getElementById(memoryId);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                element.style.transform = 'translateX(8px)';
                const card = element.querySelector('.memory-card');
                if (card) {
                    card.style.boxShadow = 'var(--shadow-md)';
                }
                
                setTimeout(() => {
                    element.style.transform = '';
                    if (card) {
                        card.style.boxShadow = '';
                    }
                }, 2000);
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.memory-space-module .stat-card').forEach((card) => {
                card.addEventListener('click', () => {
                    const filterType = card.dataset.filter;
                    const buttons = document.querySelectorAll('.memory-space-module .filter-chip');
                    
                    buttons.forEach(btn => {
                        if (btn.textContent.includes('全部') && filterType === 'all') btn.click();
                        if (btn.textContent.includes('决策') && filterType === 'decision') btn.click();
                        if (btn.textContent.includes('方案') && filterType === 'solution') btn.click();
                        if (btn.textContent.includes('重要') && filterType === 'important') btn.click();
                    });
                });
            });
        });

'''

# 构建新文件
new_lines = (
    lines[:css_insert_line] +
    [memory_css] +
    lines[css_insert_line:insert_line] +
    [memory_html] +
    lines[insert_line:js_insert_line] +
    [memory_js] +
    lines[js_insert_line:]
)

# 写入
with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("集成完成!")
print(f"原来: {len(lines)} 行")
print(f"现在: {len(new_lines)} 行")
print(f"增加: {len(new_lines) - len(lines)} 行")

