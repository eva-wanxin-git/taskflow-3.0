#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成记忆空间模块到Dashboard
"""

# 读取index.html
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到插入位置（运维工程师模块之前）
insert_line = None
for i, line in enumerate(lines):
    if '<!-- ========== 运维工程师工作台 ========== -->' in line:
        insert_line = i
        break

print(f"找到插入位置: 第{insert_line+1}行")

# 记忆空间模块的CSS（需要插入到<style>标签内，在运维工程师CSS之前）
memory_css = '''
        /* ==================== 记忆空间模块 ==================== */
        .memory-space-module {
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            margin-bottom: var(--space-7);
            display: flex;
            height: 800px;
        }

        /* 左侧：概览面板 */
        .memory-overview {
            width: 380px;
            border-right: 1px solid var(--blanc-mist);
            background: var(--blanc-snow);
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }

        .memory-overview-header {
            padding: 32px 24px 24px 24px;
            border-bottom: 1px solid var(--blanc-mist);
        }

        .memory-overview-title {
            font-family: var(--font-secondary);
            font-size: var(--text-xl);
            font-weight: var(--weight-light);
            color: var(--noir-ink);
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }

        .memory-overview-subtitle {
            font-size: var(--text-xs);
            color: var(--noir-silver);
        }

        /* 统计卡片网格 */
        .memory-stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            padding: 24px;
            border-bottom: 1px solid var(--blanc-mist);
        }

        .memory-stat-card {
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .memory-stat-card:hover {
            box-shadow: var(--shadow-sm);
            transform: translateY(-2px);
        }

        .memory-stat-label {
            font-size: var(--text-xs);
            color: var(--noir-silver);
            margin-bottom: 8px;
        }

        .memory-stat-value {
            font-size: var(--text-2xl);
            font-weight: var(--weight-light);
            color: var(--noir-ink);
            font-family: var(--font-mono);
        }

        /* 最新记忆列表 */
        .memory-recent-memories {
            padding: 24px;
        }

        .memory-recent-header {
            font-size: var(--text-sm);
            font-weight: var(--weight-semibold);
            color: var(--noir-charcoal);
            margin-bottom: 16px;
        }

        .memory-recent-item {
            padding: 12px 0;
            border-bottom: 1px solid var(--blanc-mist);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .memory-recent-item:last-child {
            border-bottom: none;
        }

        .memory-recent-item:hover {
            padding-left: 8px;
        }

        .memory-recent-item-type {
            font-size: 11px;
            color: var(--noir-silver);
            margin-bottom: 4px;
        }

        .memory-recent-item-title {
            font-size: var(--text-sm);
            color: var(--noir-graphite);
            line-height: var(--leading-tight);
        }

        /* 右侧：记忆流 */
        .memory-stream {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--blanc-pure);
            min-height: 0;  /* 关键：允许flex子元素收缩 */
        }

        /* 筛选栏 */
        .memory-stream-filters {
            display: flex;
            gap: 12px;
            padding: 24px 32px;
            border-bottom: 1px solid var(--blanc-mist);
            background: var(--blanc-snow);
        }

        .memory-filter-chip {
            padding: 8px 16px;
            font-size: var(--text-sm);
            border: 1px solid var(--blanc-cloud);
            background: var(--blanc-pure);
            color: var(--noir-graphite);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .memory-filter-chip:hover {
            border-color: var(--noir-steel);
        }

        .memory-filter-chip.active {
            background: var(--noir-ink);
            color: var(--blanc-pure);
            border-color: var(--noir-ink);
        }

        /* 记忆时间线 */
        .memory-timeline {
            flex: 1;
            overflow-y: auto;
            padding: 40px 32px 40px 72px;
            position: relative;
            min-height: 0;  /* 关键：Flexbox中overflow生效 */
        }
        
        .memory-stream-filters {
            flex-shrink: 0;  /* 防止筛选栏被压缩 */
        }

        .memory-timeline::before {
            content: '';
            position: absolute;
            left: 32px;
            top: 0;
            bottom: 0;
            width: 1px;
            background: var(--blanc-mist);
        }

        .memory-item {
            position: relative;
            margin-bottom: 32px;
            transition: all 0.3s ease;
        }

        .memory-marker {
            position: absolute;
            left: -48px;
            top: 0;
            width: 16px;
            height: 16px;
            border: 2px solid var(--noir-ink);
            background: var(--blanc-pure);
        }

        .memory-marker.decision {
            background: var(--noir-ink);
        }

        .memory-marker.solution {
            border-color: var(--noir-graphite);
        }

        .memory-marker.knowledge {
            border-color: var(--noir-silver);
            background: var(--blanc-snow);
        }

        .memory-card {
            background: var(--blanc-snow);
            border: 1px solid var(--blanc-mist);
            padding: 24px;
            transition: all 0.3s ease;
        }

        .memory-card:hover {
            box-shadow: var(--shadow-sm);
            transform: translateX(4px);
        }

        .memory-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 12px;
        }

        .memory-type-badge {
            display: inline-block;
            padding: 4px 12px;
            font-size: 11px;
            border: 1px solid var(--blanc-cloud);
            color: var(--noir-graphite);
            margin-bottom: 8px;
        }

        .memory-type-badge.decision {
            background: var(--noir-ink);
            color: var(--blanc-pure);
            border-color: var(--noir-ink);
        }

        .memory-type-badge.solution {
            border-color: var(--noir-graphite);
        }

        .memory-type-badge.knowledge {
            border-color: var(--noir-silver);
        }

        .memory-title {
            font-size: var(--text-base);
            font-weight: var(--weight-semibold);
            color: var(--noir-charcoal);
            margin-bottom: 6px;
        }

        .memory-meta {
            display: flex;
            gap: 16px;
            font-size: var(--text-xs);
            color: var(--noir-silver);
        }

        .memory-content {
            font-size: var(--text-sm);
            color: var(--noir-steel);
            line-height: var(--leading-relaxed);
            margin-top: 12px;
        }

        .memory-tags {
            display: flex;
            gap: 8px;
            margin-top: 16px;
            flex-wrap: wrap;
        }

        .memory-tag {
            padding: 4px 12px;
            font-size: 11px;
            border: 1px solid var(--blanc-cloud);
            color: var(--noir-graphite);
        }

'''

# 找到运维工程师CSS的位置，在它之前插入
css_insert_line = None
for i, line in enumerate(lines):
    if '.devops-module {' in line:
        css_insert_line = i
        break

print(f"找到CSS插入位置: 第{css_insert_line+1}行")

# 记忆空间模块的HTML
memory_html = '''        <!-- ========== 记忆空间模块 ========== -->
        <div class="memory-space-module version-content" data-version="1">
            <!-- 左侧：概览面板 -->
            <div class="memory-overview">
                <div class="memory-overview-header">
                    <h2 class="memory-overview-title">记忆空间</h2>
                    <p class="memory-overview-subtitle">基于MCP自动生成的项目知识库</p>
                </div>

                <!-- 统计卡片 -->
                <div class="memory-stats-grid">
                    <div class="memory-stat-card" data-filter="all">
                        <div class="memory-stat-label">总记忆</div>
                        <div class="memory-stat-value">45</div>
                    </div>

                    <div class="memory-stat-card" data-filter="decision">
                        <div class="memory-stat-label">决策</div>
                        <div class="memory-stat-value">12</div>
                    </div>

                    <div class="memory-stat-card" data-filter="solution">
                        <div class="memory-stat-label">方案</div>
                        <div class="memory-stat-value">23</div>
                    </div>

                    <div class="memory-stat-card" data-filter="important">
                        <div class="memory-stat-label">重要</div>
                        <div class="memory-stat-value">8</div>
                    </div>
                </div>

                <!-- 最新记忆 -->
                <div class="memory-recent-memories">
                    <div class="memory-recent-header">最新记忆</div>

                    <div class="memory-recent-item" onclick="jumpToMemory('memory-1')">
                        <div class="memory-recent-item-type">决策 · 2天前</div>
                        <div class="memory-recent-item-title">ADR: 采用Monorepo架构</div>
                    </div>

                    <div class="memory-recent-item" onclick="jumpToMemory('memory-2')">
                        <div class="memory-recent-item-type">方案 · 3天前</div>
                        <div class="memory-recent-item-title">解决Tab切换bug的方案</div>
                    </div>

                    <div class="memory-recent-item" onclick="jumpToMemory('memory-3')">
                        <div class="memory-recent-item-type">知识 · 5天前</div>
                        <div class="memory-recent-item-title">React Hooks最佳实践</div>
                    </div>
                </div>
            </div>

            <!-- 右侧：记忆流 -->
            <div class="memory-stream">
                <!-- 筛选栏 -->
                <div class="memory-stream-filters">
                    <button class="memory-filter-chip active" onclick="filterMemories('all')">全部</button>
                    <button class="memory-filter-chip" onclick="filterMemories('decision')">决策</button>
                    <button class="memory-filter-chip" onclick="filterMemories('solution')">方案</button>
                    <button class="memory-filter-chip" onclick="filterMemories('knowledge')">知识</button>
                    <button class="memory-filter-chip" onclick="filterMemories('important')">重要</button>
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

                    <!-- 更多记忆项... -->
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
                </div>
            </div>
        </div>

'''

# 记忆空间的JavaScript函数
memory_js = '''
        // ========== 记忆空间模块函数 ==========
        function filterMemories(type) {
            // 更新筛选按钮状态
            document.querySelectorAll('.memory-filter-chip').forEach(chip => {
                chip.classList.remove('active');
            });
            event.target.classList.add('active');

            // 筛选记忆项
            const items = document.querySelectorAll('.memory-item');
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
                
                // 高亮动画
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

        // 统计卡片点击筛选
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('.memory-stat-card').forEach((card) => {
                card.addEventListener('click', () => {
                    const filterType = card.dataset.filter;
                    const buttons = document.querySelectorAll('.memory-filter-chip');
                    
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

# 找到JavaScript插入位置（在运维工程师函数之前）
js_insert_line = None
for i, line in enumerate(lines):
    if '// ========== 运维工程师模块函数 ==========' in line:
        js_insert_line = i
        break

print(f"找到JS插入位置: 第{js_insert_line+1}行")

# 构建新文件
new_lines = (
    lines[:css_insert_line] +  # CSS之前的部分
    [memory_css] +              # 记忆空间CSS
    lines[css_insert_line:insert_line] +  # CSS之后到HTML插入位置
    [memory_html] +             # 记忆空间HTML
    lines[insert_line:js_insert_line] +   # HTML之后到JS插入位置
    [memory_js] +               # 记忆空间JS
    lines[js_insert_line:]      # JS之后的部分
)

# 写入文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("集成完成!")
print(f"原来: {len(lines)} 行")
print(f"现在: {len(new_lines)} 行")
print(f"增加: {len(new_lines) - len(lines)} 行")

