#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新待开发任务模块到原版完整代码
"""

# 读取现有的index.html
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到待开发任务模块的开始和结束位置
start_line = None
end_line = None

for i, line in enumerate(lines):
    if '<!-- ========== 待开发任务模块 ========== -->' in line:
        start_line = i
    if start_line is not None and '<!-- ========== 架构师模块 ========== -->' in line:
        end_line = i
        break

print(f"找到待开发任务模块位置: 第{start_line+1}行 到 第{end_line}行")
print(f"将要替换 {end_line - start_line} 行代码")

# 原版待开发任务模块的完整HTML
pending_tasks_html = '''        <!-- ========== 待开发任务模块 ========== -->
        <div class="pending-features-module version-content" data-version="1">
            <!-- 模块头部 -->
            <div class="module-header">
                <div class="header-row">
                    <h1 class="module-title">待开发任务</h1>
                    <div class="last-update">
                        <span class="sync-indicator"></span>
                        <span>最后更新:</span>
                        <span class="update-time">2025-11-19 14:35</span>
                    </div>
                </div>
            </div>

            <!-- Tab导航 -->
            <div class="tab-navigation">
                <button class="tab-item active" onclick="switchPendingTab('user-requests')">
                    用户需求
                    <span class="tab-badge">4</span>
                </button>
                <button class="tab-item" onclick="switchPendingTab('architect-suggestions')">
                    架构师建议
                    <span class="tab-badge">4</span>
                </button>
            </div>

            <!-- Tab内容 -->
            <div class="tab-content-wrapper">
                <!-- Tab 1: 用户需求 -->
                <div id="user-requests" class="tab-pane active">
                    <div class="task-grid">
                        <!-- 用户需求示例1 - 已转交开发 -->
                        <div class="task-card high-priority">
                            <div class="task-header">
                                <div>
                                    <div class="task-id">REQ-USER-001</div>
                                    <h3 class="task-title">实现实时协作编辑功能</h3>
                                </div>
                                <span class="task-source user">用户需求</span>
                            </div>
                            <div class="task-description">
                                用户希望能够像Google Docs一样，多人同时编辑任务描述和文档，实时看到其他人的修改。
                            </div>
                            <div class="task-requirements">
                                <div class="task-requirements-title">架构师优化后的需求:</div>
                                <ul class="task-requirements-list">
                                    <li>支持多人同时编辑，实时同步内容（WebSocket）</li>
                                    <li>显示其他用户的光标位置和选区</li>
                                    <li>自动解决内容冲突（CRDT算法）</li>
                                    <li>完整的版本历史和回滚功能</li>
                                    <li>离线编辑支持，上线后自动同步</li>
                                </ul>
                            </div>
                            <div class="task-tags">
                                <span class="task-tag">实时协作</span>
                                <span class="task-tag">WebSocket</span>
                                <span class="task-tag">CRDT</span>
                            </div>
                            <div class="task-meta">
                                <div class="task-meta-item">
                                    <span class="task-meta-label">优先级:</span>
                                    <span class="task-priority high">P0 - 紧急</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">预计工时:</span>
                                    <span class="task-meta-value">20-24小时</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">提交时间:</span>
                                    <span class="task-meta-value">2025-11-18 10:30</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">当前状态:</span>
                                    <span class="task-meta-value">架构师已转交开发</span>
                                </div>
                            </div>
                            <div class="architect-status completed">
                                <span class="status-icon">✓</span>
                                <span>架构师已优化并分配给全栈工程师</span>
                            </div>
                        </div>

                        <!-- 用户需求示例2 - 架构师正在处理 -->
                        <div class="task-card medium-priority">
                            <div class="task-header">
                                <div>
                                    <div class="task-id">REQ-USER-002</div>
                                    <h3 class="task-title">移动端App开发</h3>
                                </div>
                                <span class="task-source user">用户需求</span>
                            </div>
                            <div class="task-description">
                                用户希望能在手机上随时随地管理任务，查看进度，接收通知。
                            </div>
                            <div class="task-requirements">
                                <div class="task-requirements-title">架构师优化后的需求:</div>
                                <ul class="task-requirements-list">
                                    <li>采用React Native实现跨平台（降低成本）</li>
                                    <li>完整的任务管理功能（CRUD）</li>
                                    <li>推送通知集成（Firebase Cloud Messaging）</li>
                                    <li>离线模式支持（本地SQLite缓存）</li>
                                    <li>与Web端数据同步（增量同步策略）</li>
                                </ul>
                            </div>
                            <div class="task-tags">
                                <span class="task-tag">移动端</span>
                                <span class="task-tag">React Native</span>
                            </div>
                            <div class="task-meta">
                                <div class="task-meta-item">
                                    <span class="task-meta-label">优先级:</span>
                                    <span class="task-priority medium">P1 - 重要</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">预计工时:</span>
                                    <span class="task-meta-value">80-100小时</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">提交时间:</span>
                                    <span class="task-meta-value">2025-11-17 14:20</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">当前状态:</span>
                                    <span class="task-meta-value">架构师正在评估方案</span>
                                </div>
                            </div>
                            <div class="architect-status processing">
                                <span class="status-icon">⟳</span>
                                <span>架构师正在制定技术方案</span>
                            </div>
                        </div>

                        <!-- 用户需求示例3 - 等待处理 -->
                        <div class="task-card medium-priority">
                            <div class="task-header">
                                <div>
                                    <div class="task-id">REQ-USER-003</div>
                                    <h3 class="task-title">集成第三方日历（Google Calendar）</h3>
                                </div>
                                <span class="task-source user">用户需求</span>
                            </div>
                            <div class="task-description">
                                用户希望将任务截止日期自动同步到Google Calendar，并支持双向同步。
                            </div>
                            <div class="task-tags">
                                <span class="task-tag">第三方集成</span>
                                <span class="task-tag">Google API</span>
                            </div>
                            <div class="task-meta">
                                <div class="task-meta-item">
                                    <span class="task-meta-label">优先级:</span>
                                    <span class="task-priority medium">P1 - 重要</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">预计工时:</span>
                                    <span class="task-meta-value">12-16小时</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">提交时间:</span>
                                    <span class="task-meta-value">2025-11-16 09:15</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">当前状态:</span>
                                    <span class="task-meta-value">待架构师审查</span>
                                </div>
                            </div>
                            <div class="architect-status pending">
                                <span class="status-icon">○</span>
                                <span>排队等待架构师处理</span>
                            </div>
                        </div>

                        <!-- 用户需求示例4 -->
                        <div class="task-card low-priority">
                            <div class="task-header">
                                <div>
                                    <div class="task-id">REQ-USER-004</div>
                                    <h3 class="task-title">支持自定义任务模板</h3>
                                </div>
                                <span class="task-source user">用户需求</span>
                            </div>
                            <div class="task-description">
                                用户希望能够创建任务模板，快速生成重复性任务。例如：每周例会模板、项目启动模板等。
                            </div>
                            <div class="task-tags">
                                <span class="task-tag">模板系统</span>
                                <span class="task-tag">效率工具</span>
                            </div>
                            <div class="task-meta">
                                <div class="task-meta-item">
                                    <span class="task-meta-label">优先级:</span>
                                    <span class="task-priority low">P2 - 正常</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">预计工时:</span>
                                    <span class="task-meta-value">8-10小时</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">提交时间:</span>
                                    <span class="task-meta-value">2025-11-15 16:50</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">当前状态:</span>
                                    <span class="task-meta-value">待架构师审查</span>
                                </div>
                            </div>
                            <div class="architect-status pending">
                                <span class="status-icon">○</span>
                                <span>低优先级，等待架构师排期</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Tab 2: 架构师建议 -->
                <div id="architect-suggestions" class="tab-pane">
                    <div class="task-grid">
                        <!-- 架构师建议示例1 -->
                        <div class="task-card high-priority">
                            <div class="task-header">
                                <div>
                                    <div class="task-id">SUGGEST-ARCH-001</div>
                                    <h3 class="task-title">修复任务状态流转权限漏洞</h3>
                                </div>
                                <span class="task-source architect">架构师建议</span>
                            </div>
                            <div class="task-description">
                                在安全扫描中发现，任务状态流转逻辑与权限系统不一致。普通用户可以绕过"审查中"状态直接将任务标记为"已完成"，违反了权限控制规则。
                            </div>
                            <div class="review-info">
                                <div class="review-info-title">架构师诊断:</div>
                                <div class="review-info-content">
                                    发现时间: 2025-11-19 09:30 | 
                                    扫描来源: 自动化安全审计 | 
                                    风险等级: 高危 | 
                                    影响范围: 已有3个非管理员用户利用此漏洞
                                </div>
                            </div>
                            <div class="task-requirements">
                                <div class="task-requirements-title">修复方案:</div>
                                <ul class="task-requirements-list">
                                    <li>更新任务状态机，强制经过审查状态</li>
                                    <li>添加权限验证中间件</li>
                                    <li>更新前端状态按钮逻辑</li>
                                    <li>补充单元测试和集成测试</li>
                                    <li>更新文档说明状态流转规则</li>
                                </ul>
                            </div>
                            <div class="task-tags">
                                <span class="task-tag">Bug修复</span>
                                <span class="task-tag">权限系统</span>
                                <span class="task-tag">安全漏洞</span>
                            </div>
                            <div class="task-meta">
                                <div class="task-meta-item">
                                    <span class="task-meta-label">优先级:</span>
                                    <span class="task-priority high">P0 - 紧急</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">预计工时:</span>
                                    <span class="task-meta-value">4-6小时</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">发现时间:</span>
                                    <span class="task-meta-value">2025-11-19 09:30</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">来源:</span>
                                    <span class="task-meta-value">安全扫描</span>
                                </div>
                            </div>
                            
                            <div class="user-decision-area">
                                <div class="decision-title">请决策:</div>
                                <div class="decision-buttons">
                                    <button class="decision-button accept" onclick="acceptSuggestion('SUGGEST-ARCH-001')">
                                        采纳建议 - 立即修复
                                    </button>
                                    <button class="decision-button reject" onclick="rejectSuggestion('SUGGEST-ARCH-001')">
                                        拒绝建议
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- 架构师建议示例2 -->
                        <div class="task-card medium-priority">
                            <div class="task-header">
                                <div>
                                    <div class="task-id">SUGGEST-ARCH-002</div>
                                    <h3 class="task-title">实现Redis缓存层优化查询性能</h3>
                                </div>
                                <span class="task-source architect">架构师建议</span>
                            </div>
                            <div class="task-description">
                                Dashboard页面的聚合查询性能较差（平均响应800ms），建议引入Redis缓存层，预计可将响应时间降至50ms以内。
                            </div>
                            <div class="review-info">
                                <div class="review-info-title">架构师分析:</div>
                                <div class="review-info-content">
                                    性能监控发现: 当前查询涉及5个表的JOIN操作，高峰期数据库CPU占用率达90%。
                                    引入缓存后预计: 降低60%数据库负载，响应时间从800ms降至50ms。
                                </div>
                            </div>
                            <div class="task-requirements">
                                <div class="task-requirements-title">实施方案:</div>
                                <ul class="task-requirements-list">
                                    <li>搭建Redis服务器并配置（Docker部署）</li>
                                    <li>实现缓存中间件和工具类</li>
                                    <li>为Dashboard聚合查询添加缓存逻辑</li>
                                    <li>实现缓存更新和失效策略（TTL: 5分钟）</li>
                                    <li>监控缓存命中率和性能指标</li>
                                </ul>
                            </div>
                            <div class="task-tags">
                                <span class="task-tag">性能优化</span>
                                <span class="task-tag">Redis</span>
                                <span class="task-tag">缓存</span>
                            </div>
                            <div class="task-meta">
                                <div class="task-meta-item">
                                    <span class="task-meta-label">优先级:</span>
                                    <span class="task-priority medium">P1 - 重要</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">预计工时:</span>
                                    <span class="task-meta-value">8-10小时</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">发现时间:</span>
                                    <span class="task-meta-value">2025-11-18 15:45</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">来源:</span>
                                    <span class="task-meta-value">性能监控</span>
                                </div>
                            </div>
                            
                            <div class="user-decision-area">
                                <div class="decision-title">请决策:</div>
                                <div class="decision-buttons">
                                    <button class="decision-button accept" onclick="acceptSuggestion('SUGGEST-ARCH-002')">
                                        采纳建议 - 安排实施
                                    </button>
                                    <button class="decision-button reject" onclick="rejectSuggestion('SUGGEST-ARCH-002')">
                                        暂不采纳
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- 架构师建议示例3 -->
                        <div class="task-card medium-priority">
                            <div class="task-header">
                                <div>
                                    <div class="task-id">SUGGEST-ARCH-003</div>
                                    <h3 class="task-title">启用API速率限制保护</h3>
                                </div>
                                <span class="task-source architect">架构师建议</span>
                            </div>
                            <div class="task-description">
                                当前API端点未实施速率限制，存在被滥用或DDoS攻击的风险。建议使用Redis + Token Bucket算法实现频率限制。
                            </div>
                            <div class="review-info">
                                <div class="review-info-title">架构师评估:</div>
                                <div class="review-info-content">
                                    在安全审计中发现，公开API端点可被无限制调用。建议限制为: 
                                    匿名用户 100次/分钟/IP | 认证用户 1000次/分钟 | 管理员无限制
                                </div>
                            </div>
                            <div class="task-requirements">
                                <div class="task-requirements-title">实施方案:</div>
                                <ul class="task-requirements-list">
                                    <li>实现Token Bucket速率限制算法</li>
                                    <li>为不同用户角色配置不同限额</li>
                                    <li>添加速率限制中间件</li>
                                    <li>返回标准的429 Too Many Requests响应</li>
                                    <li>监控和告警系统（异常流量检测）</li>
                                </ul>
                            </div>
                            <div class="task-tags">
                                <span class="task-tag">安全</span>
                                <span class="task-tag">速率限制</span>
                            </div>
                            <div class="task-meta">
                                <div class="task-meta-item">
                                    <span class="task-meta-label">优先级:</span>
                                    <span class="task-priority medium">P1 - 重要</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">预计工时:</span>
                                    <span class="task-meta-value">3-4小时</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">发现时间:</span>
                                    <span class="task-meta-value">2025-11-18 11:20</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">来源:</span>
                                    <span class="task-meta-value">安全审计</span>
                                </div>
                            </div>
                            
                            <div class="user-decision-area">
                                <div class="decision-title">请决策:</div>
                                <div class="decision-buttons">
                                    <button class="decision-button accept" onclick="acceptSuggestion('SUGGEST-ARCH-003')">
                                        采纳建议 - 启用防护
                                    </button>
                                    <button class="decision-button reject" onclick="rejectSuggestion('SUGGEST-ARCH-003')">
                                        暂不采纳
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- 架构师建议示例4 -->
                        <div class="task-card low-priority">
                            <div class="task-header">
                                <div>
                                    <div class="task-id">SUGGEST-ARCH-004</div>
                                    <h3 class="task-title">重构任务模块提高可维护性</h3>
                                </div>
                                <span class="task-source architect">架构师建议</span>
                            </div>
                            <div class="task-description">
                                任务管理模块核心文件（task_service.py）已达1200行，违反单一职责原则。建议拆分为多个独立服务，提升代码可维护性。
                            </div>
                            <div class="review-info">
                                <div class="review-info-title">架构师分析:</div>
                                <div class="review-info-content">
                                    代码质量扫描发现: 单文件包含过多职责（CRUD、状态管理、依赖关系、通知等）。
                                    建议拆分为4个独立服务类，降低耦合度。
                                </div>
                            </div>
                            <div class="task-requirements">
                                <div class="task-requirements-title">重构方案:</div>
                                <ul class="task-requirements-list">
                                    <li>拆分为TaskCRUDService（基础CRUD）</li>
                                    <li>拆分为TaskStatusService（状态流转）</li>
                                    <li>拆分为TaskDependencyService（依赖管理）</li>
                                    <li>拆分为TaskNotificationService（通知）</li>
                                    <li>为每个服务编写单元测试</li>
                                </ul>
                            </div>
                            <div class="task-tags">
                                <span class="task-tag">代码重构</span>
                                <span class="task-tag">技术债务</span>
                            </div>
                            <div class="task-meta">
                                <div class="task-meta-item">
                                    <span class="task-meta-label">优先级:</span>
                                    <span class="task-priority low">P2 - 正常</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">预计工时:</span>
                                    <span class="task-meta-value">6-8小时</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">发现时间:</span>
                                    <span class="task-meta-value">2025-11-17 17:10</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">来源:</span>
                                    <span class="task-meta-value">代码质量审查</span>
                                </div>
                            </div>
                            
                            <div class="user-decision-area">
                                <div class="decision-title">请决策:</div>
                                <div class="decision-buttons">
                                    <button class="decision-button accept" onclick="acceptSuggestion('SUGGEST-ARCH-004')">
                                        采纳建议 - 排入技术债清理
                                    </button>
                                    <button class="decision-button reject" onclick="rejectSuggestion('SUGGEST-ARCH-004')">
                                        暂不处理
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

'''

# 构建新的文件内容
new_lines = lines[:start_line] + [pending_tasks_html] + lines[end_line:]

# 写入新文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("替换完成!")
print(f"原来: {len(lines)} 行")
print(f"现在: {len(new_lines)} 行")
print(f"增加: {len(new_lines) - len(lines)} 行")

