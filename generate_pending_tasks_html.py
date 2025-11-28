"""
生成待开发任务池的HTML内容
"""
import json
from datetime import datetime

# 读取数据
with open('pending_tasks_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

req_tasks = data['req_tasks']
arch_tasks = data['arch_tasks']

# 优先级映射
priority_map = {
    'P0': ('high', 'P0 - 紧急'),
    'P1': ('medium', 'P1 - 重要'),
    'P2': ('low', 'P2 - 正常')
}

# 状态映射
status_map = {
    'pending': ('pending', '待处理'),
    'in_progress': ('processing', '进行中'),
    'completed': ('completed', '已完成')
}

def format_date(date_str):
    """格式化日期"""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return date_str

def generate_req_task_html(task):
    """生成用户需求任务HTML"""
    priority_class, priority_text = priority_map.get(task['priority'], ('low', task['priority']))
    status_class, status_text = status_map.get(task['status'], ('pending', task['status']))
    
    # 提取描述的前100字
    desc = task['description']
    if len(desc) > 200:
        desc = desc[:200] + '...'
    
    # 标签（从描述中提取关键词）
    tags = []
    if 'API' in task['title']:
        tags.append('API开发')
    if '集成' in task['title']:
        tags.append('系统集成')
    if '优化' in task['title']:
        tags.append('性能优化')
    if '架构' in task['title']:
        tags.append('架构设计')
    if '测试' in task['title']:
        tags.append('测试')
    
    if not tags:
        tags = ['功能开发']
    
    tags_html = ''.join([f'<span class="task-tag">{tag}</span>' for tag in tags[:3]])
    
    html = f'''                        <div class="task-card {priority_class}-priority">
                            <div class="task-header">
                                <div>
                                    <div class="task-id">{task['id']}</div>
                                    <h3 class="task-title">{task['title']}</h3>
                                </div>
                                <span class="task-source user">用户需求</span>
                            </div>
                            <div class="task-description">
                                {desc}
                            </div>
                            <div class="task-tags">
                                {tags_html}
                            </div>
                            <div class="task-meta">
                                <div class="task-meta-item">
                                    <span class="task-meta-label">优先级:</span>
                                    <span class="task-priority {priority_class}">{priority_text}</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">预计工时:</span>
                                    <span class="task-meta-value">{task['estimated_hours']}小时</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">提交时间:</span>
                                    <span class="task-meta-value">{format_date(task['created_at'])}</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">当前状态:</span>
                                    <span class="task-meta-value">{status_text}</span>
                                </div>
                            </div>
                            <div class="architect-status {status_class}">
                                <span class="status-icon">{'✓' if status_class == 'completed' else '⟳' if status_class == 'processing' else '○'}</span>
                                <span>{'已完成' if status_class == 'completed' else '架构师正在处理' if status_class == 'processing' else '等待架构师处理'}</span>
                            </div>
                        </div>
'''
    return html

def generate_arch_task_html(task):
    """生成架构师建议任务HTML"""
    priority_class, priority_text = priority_map.get(task['priority'], ('low', task['priority']))
    
    # 提取描述的前150字
    desc = task['description']
    if len(desc) > 200:
        desc = desc[:200] + '...'
    
    # 标签
    tags = []
    if 'API' in task['title']:
        tags.append('API开发')
    if '集成' in task['title']:
        tags.append('系统集成')
    if '优化' in task['title']:
        tags.append('性能优化')
    if '架构' in task['title']:
        tags.append('架构设计')
    if '扩展' in task['title']:
        tags.append('功能扩展')
    if '迁移' in task['title']:
        tags.append('代码重构')
    
    if not tags:
        tags = ['架构建议']
    
    tags_html = ''.join([f'<span class="task-tag">{tag}</span>' for tag in tags[:3]])
    
    html = f'''                        <div class="task-card {priority_class}-priority">
                            <div class="task-header">
                                <div>
                                    <div class="task-id">{task['id']}</div>
                                    <h3 class="task-title">{task['title']}</h3>
                                </div>
                                <span class="task-source architect">架构师建议</span>
                            </div>
                            <div class="task-description">
                                {desc}
                            </div>
                            <div class="review-info">
                                <div class="review-info-title">架构师诊断:</div>
                                <div class="review-info-content">
                                    预估工时: {task['estimated_hours']}小时 | 
                                    优先级: {priority_text} | 
                                    创建时间: {format_date(task['created_at'])}
                                </div>
                            </div>
                            <div class="task-tags">
                                {tags_html}
                            </div>
                            <div class="task-meta">
                                <div class="task-meta-item">
                                    <span class="task-meta-label">优先级:</span>
                                    <span class="task-priority {priority_class}">{priority_text}</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">预计工时:</span>
                                    <span class="task-meta-value">{task['estimated_hours']}小时</span>
                                </div>
                                <div class="task-meta-item">
                                    <span class="task-meta-label">创建时间:</span>
                                    <span class="task-meta-value">{format_date(task['created_at'])}</span>
                                </div>
                            </div>
                            
                            <div class="user-decision-area">
                                <div class="decision-title">请决策:</div>
                                <div class="decision-buttons">
                                    <button class="decision-button accept" onclick="acceptSuggestion('{task['id']}')">
                                        采纳建议 - 立即执行
                                    </button>
                                    <button class="decision-button reject" onclick="rejectSuggestion('{task['id']}')">
                                        拒绝建议
                                    </button>
                                </div>
                            </div>
                        </div>
'''
    return html

# 生成Tab 1: 用户需求
print("=" * 60)
print("生成Tab 1: 用户需求")
print("=" * 60)
tab1_html = '<div id="user-requests" class="tab-pane active">\n                    <div class="task-grid">\n'
for task in req_tasks:
    tab1_html += generate_req_task_html(task)
tab1_html += '                    </div>\n                </div>\n'

# 生成Tab 2: 架构师建议
print("生成Tab 2: 架构师建议")
print("=" * 60)
tab2_html = '<div id="architect-suggestions" class="tab-pane">\n                    <div class="task-grid">\n'
for task in arch_tasks[:15]:  # 只显示前15个，避免太长
    tab2_html += generate_arch_task_html(task)
tab2_html += '                    </div>\n                </div>\n'

# 保存HTML片段
with open('pending_tasks_tab1.html', 'w', encoding='utf-8') as f:
    f.write(tab1_html)

with open('pending_tasks_tab2.html', 'w', encoding='utf-8') as f:
    f.write(tab2_html)

print(f"✅ Tab 1生成完成: {len(req_tasks)} 个用户需求任务")
print(f"✅ Tab 2生成完成: 15 个架构师建议任务 (共{len(arch_tasks)}个)")
print("\n已生成文件:")
print("  - pending_tasks_tab1.html")
print("  - pending_tasks_tab2.html")
print("\n下一步: 将这些内容替换到 dashboard-test/index.html 中")
print(f"\n统计卡片数字更新:")
print(f"  - 总任务: {len(req_tasks) + len(arch_tasks)}")
print(f"  - 用户需求: {len(req_tasks)}")
print(f"  - 架构师建议: {len(arch_tasks)}")

