#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运维工程师工作台数据校验 - 更新脚本
将硬编码的示例数据替换为友好的占位符
"""

# Tab 1: 运维日志占位符
TAB1_PLACEHOLDER = '''            <div id="logs" class="devops-tab-pane active">
                <div class="empty-state" style="margin-top: 60px;">
                    <div class="empty-state-icon" style="font-size: 48px;">📋</div>
                    <div class="empty-state-title">运维日志功能待实现</div>
                    <div class="empty-state-description">
                        此功能需要后端API支持<br><br>
                        
                        <strong style="color: var(--noir-ink);">需要API</strong>: <code style="background: var(--blanc-mist); padding: 2px 8px; border-radius: 4px;">GET /api/logs/operations</code><br>
                        <strong style="color: var(--noir-ink);">预估工时</strong>: 1小时<br>
                        <strong style="color: var(--noir-ink);">优先级</strong>: P1<br><br>
                        
                        <strong style="color: var(--noir-ink);">功能规划</strong>:<br>
                        <div style="text-align: left; display: inline-block; margin-top: 12px;">
                            • 实时日志流展示（847条+）<br>
                            • 按级别筛选（INFO/WARN/ERROR/CRITICAL）<br>
                            • 时间轴可视化<br>
                            • 日志搜索和导出<br>
                            • 故障告警、版本更新、日常巡检分类<br>
                        </div>
                        <br><br>
                        
                        <button class="primary-button" onclick="alert('已加入开发计划：TASK-API-010\\n\\n将在Phase D实现：\\n1. 运维日志API\\n2. 日志级别筛选\\n3. 实时日志流\\n4. 日志导出功能')" style="margin-top: 16px;">
                            加入开发计划
                        </button>
                    </div>
                </div>
            </div>'''

# Tab 2: Bug看板占位符
TAB2_PLACEHOLDER = '''            <div id="bugs" class="devops-tab-pane">
                <div class="empty-state" style="margin-top: 60px;">
                    <div class="empty-state-icon" style="font-size: 48px;">🐛</div>
                    <div class="empty-state-title">Bug管理功能完整，暂无数据</div>
                    <div class="empty-state-description">
                        数据库 <code style="background: var(--blanc-mist); padding: 2px 8px; border-radius: 4px;">issues</code> 表已就绪<br>
                        可以开始创建Bug记录<br><br>
                        
                        <strong style="color: var(--noir-ink);">功能说明</strong>:<br>
                        <div style="text-align: left; display: inline-block; margin-top: 12px;">
                            • 三栏看板布局（待修复/修复中/已验证）<br>
                            • Bug卡片包含：ID、标题、描述、优先级<br>
                            • 支持按优先级筛选（P0/P1/P2）<br>
                            • 关联运维日志和解决方案<br>
                        </div>
                        <br><br>
                        
                        <strong style="color: var(--noir-ink);">如何添加Bug</strong>:<br>
                        <div style="text-align: left; display: inline-block; margin-top: 12px;">
                            1. 通过API: <code>POST /api/issues</code><br>
                            2. 数据库插入: 向 <code>issues</code> 表添加记录<br>
                            3. 自动检测: 运维AI巡检自动发现<br>
                        </div>
                        <br><br>
                        
                        <button class="primary-button" onclick="alert('Bug管理功能说明：\\n\\n1. 数据库表已创建\\n2. API端点已就绪\\n3. 前端展示已完成\\n4. 只需添加数据即可展示\\n\\n建议：先完成几个真实Bug的录入')" style="margin-top: 16px;">
                            查看使用指南
                        </button>
                    </div>
                </div>
            </div>'''

# Tab 3: 系统状态占位符
TAB3_PLACEHOLDER = '''            <div id="status" class="devops-tab-pane">
                <div class="empty-state" style="margin-top: 60px;">
                    <div class="empty-state-icon" style="font-size: 48px;">📊</div>
                    <div class="empty-state-title">系统监控功能待增强</div>
                    <div class="empty-state-description">
                        此功能需要后端API增强<br><br>
                        
                        <strong style="color: var(--noir-ink);">需要API</strong>: <code style="background: var(--blanc-mist); padding: 2px 8px; border-radius: 4px;">GET /api/system/health</code> (增强版)<br>
                        <strong style="color: var(--noir-ink);">预估工时</strong>: 3小时<br>
                        <strong style="color: var(--noir-ink);">优先级</strong>: P0<br><br>
                        
                        <strong style="color: var(--noir-ink);">功能规划</strong>:<br>
                        <div style="text-align: left; display: inline-block; margin-top: 12px;">
                            • <strong>系统总览</strong>: 在线率、响应时间、错误率、在线用户数<br>
                            • <strong>服务监控</strong>: 6个服务实时状态<br>
                            &nbsp;&nbsp;- API服务 (FastAPI)<br>
                            &nbsp;&nbsp;- Dashboard服务<br>
                            &nbsp;&nbsp;- Worker服务<br>
                            &nbsp;&nbsp;- 数据库服务 (SQLite)<br>
                            &nbsp;&nbsp;- 静态资源 (CDN)<br>
                            &nbsp;&nbsp;- WebSocket服务<br>
                            • <strong>每个服务显示</strong>: 状态、端口、响应时间、CPU、内存<br>
                            • <strong>告警功能</strong>: 服务异常自动告警<br>
                        </div>
                        <br><br>
                        
                        <button class="primary-button" onclick="alert('已加入开发计划：TASK-API-011\\n\\n将在Phase D实现：\\n1. 系统健康检查API\\n2. 服务状态监控\\n3. 资源使用统计\\n4. 实时告警推送')" style="margin-top: 16px;">
                            加入开发计划
                        </button>
                    </div>
                </div>
            </div>'''

# Tab 4: 知识库占位符
TAB4_PLACEHOLDER = '''            <div id="knowledge" class="devops-tab-pane">
                <div class="empty-state" style="margin-top: 60px;">
                    <div class="empty-state-icon" style="font-size: 48px;">📚</div>
                    <div class="empty-state-title">知识库功能完整，暂无数据</div>
                    <div class="empty-state-description">
                        数据库 <code style="background: var(--blanc-mist); padding: 2px 8px; border-radius: 4px;">knowledge_articles</code> 表已就绪<br>
                        可以开始添加知识条目<br><br>
                        
                        <strong style="color: var(--noir-ink);">功能说明</strong>:<br>
                        <div style="text-align: left; display: inline-block; margin-top: 12px;">
                            • <strong>知识分类</strong>: 6大类别<br>
                            &nbsp;&nbsp;- 环境配置（开发/测试/生产环境）<br>
                            &nbsp;&nbsp;- 依赖库文档（版本记录、升级日志）<br>
                            &nbsp;&nbsp;- 问题解决方案（Bug修复、FAQ）<br>
                            &nbsp;&nbsp;- 部署流程（CI/CD、Docker、K8s）<br>
                            &nbsp;&nbsp;- 监控告警（指标定义、告警规则）<br>
                            &nbsp;&nbsp;- 安全认证（API密钥、OAuth、SSL）<br>
                            • <strong>文章展示</strong>: 标题、分类、重要度、标签、更新时间<br>
                            • <strong>筛选功能</strong>: 按分类、按重要度、按更新时间<br>
                        </div>
                        <br><br>
                        
                        <strong style="color: var(--noir-ink);">如何添加知识</strong>:<br>
                        <div style="text-align: left; display: inline-block; margin-top: 12px;">
                            1. 通过API: <code>POST /api/knowledge/articles</code><br>
                            2. 数据库插入: 向 <code>knowledge_articles</code> 表添加记录<br>
                            3. 自动生成: 运维AI自动提取文档生成知识条目<br>
                        </div>
                        <br><br>
                        
                        <button class="primary-button" onclick="alert('知识库功能说明：\\n\\n1. 数据库表已创建（12个字段）\\n2. API端点已就绪\\n3. 前端展示已完成\\n4. 支持分类筛选\\n\\n建议：先完成几篇核心知识文档的录入')" style="margin-top: 16px;">
                            查看使用指南
                        </button>
                    </div>
                </div>
            </div>'''

print("=== 运维工程师工作台占位符生成完成 ===")
print("\n现在需要在 dashboard-test/index.html 中替换以下4个Tab的内容：")
print("\n1. Tab 1: 运维日志 (lines 9216-9428)")
print("2. Tab 2: Bug看板 (lines 9431-9574)")
print("3. Tab 3: 系统状态 (lines 9577-9733)")
print("4. Tab 4: 知识库 (lines 9736-9848)")
print("\n占位符已生成，准备替换...")

