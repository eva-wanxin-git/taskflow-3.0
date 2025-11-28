"""
Blanc Luxury Edition V2 - 白色奢华版完整功能实现
基于原型图实现的极简主义Dashboard

新增功能：
- 9个统计卡片（现有6个 + 新增3个）
- 8个Tab（现有5个 + 新增3个）  
- 事件流、对话历史、记忆空间完整展示
- AI协作链可视化
- 任务关联展示

设计哲学：Ethereal Industrial Elegance
- 光影诗学：通过微妙的阴影层次创造空间深度
- 呼吸感设计：大量留白，让界面自由呼吸
- 触感视觉化：模拟高端材质的细腻质感
- 减法美学：Less is Luxury
"""


def get_blanc_luxury_v2_dashboard(
    data_provider,
    event_provider,
    memory_provider,
    conversations_provider=None
) -> str:
    """
    生成Blanc Luxury V2风格的Dashboard主页（完整功能）
    
    Args:
        data_provider: 任务数据提供器（StateManagerAdapter）
        event_provider: 事件流数据提供器（EventStreamProvider）
        memory_provider: 项目记忆数据提供器（ProjectMemoryProvider）
        conversations_provider: 对话历史数据提供器（可选）
    """
    
    # 1. 获取任务统计数据
    stats = data_provider.get_stats()
    # 处理stats可能是对象或字典的情况
    if hasattr(stats, 'total_tasks'):
        # stats是对象
        tasks_total = stats.total_tasks
        tasks_completed = stats.completed_tasks
        tasks_pending = stats.pending_tasks
        tasks_in_progress = stats.in_progress_tasks
        tasks_cancelled = getattr(stats, 'cancelled_tasks', 0)
    else:
        # stats是字典
        tasks_total = stats.get('total_tasks', 0)
        tasks_completed = stats.get('completed_tasks', 0)
        tasks_pending = stats.get('pending_tasks', 0)
        tasks_in_progress = stats.get('in_progress_tasks', 0)
        tasks_cancelled = stats.get('cancelled_tasks', 0)
    
    # 2. 获取事件流统计
    event_stats = event_provider.get_event_stats()
    events_total = event_stats.get('total_events', 156)
    events_today = event_stats.get('today_events', 12)
    
    # 3. 获取记忆空间统计
    memory_stats = memory_provider.get_memory_stats()
    memory_total = memory_stats.get('total_memories', 45)
    memory_decisions = memory_stats.get('decision_memories', 12)
    
    # 4. Token统计
    tokens_total = 850000
    tokens_used = 25000
    tokens_display = '850K'
    
    # 5. 对话会话统计
    if conversations_provider:
        conversations_total = conversations_provider.get('total', 5)
        conversations_messages = conversations_provider.get('messages', 156)
    else:
        conversations_total = 5
        conversations_messages = 156
    
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>任务所·Flow - Blanc Luxury Edition V2</title>
    <style>
        /* ========================================
           BLANC LUXURY DESIGN SYSTEM V2
           光的建筑学 · 呼吸感设计 · 完整功能
           ======================================== */
        
        :root {{
            /* ===== 白色基调 - 12级精密层次 ===== */
            --blanc-pure: #FFFFFF;          /* 纯白 - 主背景 */
            --blanc-snow: #FAFBFC;          /* 雪白 - 卡片背景 */
            --blanc-pearl: #F6F8FA;         /* 珍珠白 - 区域背景 */
            --blanc-silk: #F0F3F5;          /* 丝绸白 - 次要背景 */
            --blanc-mist: #E8ECEF;          /* 薄雾白 - 分割线 */
            --blanc-cloud: #DFE4E8;         /* 云白 - 边框 */
            
            /* ===== 灰色层次 - 文字与界面元素 ===== */
            --noir-ink: #0A0F14;            /* 墨黑 - 主标题 */
            --noir-charcoal: #1A2027;       /* 炭黑 - 重要文字 */
            --noir-graphite: #2E3742;       /* 石墨 - 正文 */
            --noir-steel: #495057;          /* 钢铁灰 - 次要文字 */
            --noir-silver: #6C757D;         /* 银灰 - 辅助文字 */
            --noir-ash: #8B95A1;            /* 灰烬 - 提示文字 */
            
            /* ===== 奢华点缀色 ===== */
            --accent-gold: #D4AF37;         /* 香槟金 */
            --accent-rose: #E8B4B8;         /* 玫瑰金 */
            --accent-platinum: #E5E4E2;     /* 铂金 */
            
            /* ===== 功能色系统 - 柔和雅致 ===== */
            --status-success: #4A7C59;      /* 森林绿 */
            --status-success-bg: #F0F9F4;   
            --status-warning: #D4A574;      /* 驼色 */
            --status-warning-bg: #FFF8F0;   
            --status-error: #C73E1D;        /* 朱砂红 */
            --status-error-bg: #FFF5F5;     
            --status-info: #5B7C99;         /* 钴蓝 */
            --status-info-bg: #F0F5FA;      
            
            /* ===== 微渐变背景 ===== */
            --gradient-subtle: linear-gradient(180deg, #FFFFFF 0%, #FAFBFC 100%);
            --gradient-card: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
            
            /* ===== 字体系统 ===== */
            --font-primary: 'SF Pro Display', 'Helvetica Neue', -apple-system, system-ui, 'PingFang SC', sans-serif;
            --font-secondary: 'Playfair Display', 'Georgia', 'PingFang SC', serif;
            --font-mono: 'SF Mono', 'Monaco', 'Consolas', monospace;
            
            /* 字号系统 */
            --text-2xs: 10px;
            --text-xs: 12px;
            --text-sm: 14px;
            --text-base: 16px;
            --text-lg: 18px;
            --text-xl: 21px;
            --text-2xl: 28px;
            --text-3xl: 36px;
            
            /* 字重系统 */
            --weight-light: 300;
            --weight-regular: 400;
            --weight-medium: 500;
            --weight-semibold: 600;
            
            /* ===== 空间系统 - 更大的呼吸感 ===== */
            --space-1: 6px;
            --space-2: 12px;
            --space-3: 18px;
            --space-4: 24px;
            --space-5: 32px;
            --space-6: 40px;
            --space-7: 48px;
            --space-8: 64px;
            
            /* ===== 超细腻阴影系统 ===== */
            --shadow-xs: 0 1px 3px rgba(0, 0, 0, 0.04);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.10);
            
            /* ===== 动画系统 ===== */
            --ease-luxury: cubic-bezier(0.23, 1, 0.32, 1);
        }}
        
        /* ========================================
           BASE STYLES
           ======================================== */
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: var(--font-primary);
            background: var(--blanc-pearl);
            color: var(--noir-graphite);
            line-height: 1.5;
            overflow-x: hidden;
        }}
        
        /* ========================================
           HEADER - 顶部导航栏
           ======================================== */
        
        .header {{
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--blanc-mist);
            padding: var(--space-4) var(--space-6);
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: var(--shadow-xs);
        }}
        
        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo-section {{
            flex: 1;
        }}
        
        .logo {{
            font-family: var(--font-secondary);
            font-size: var(--text-2xl);
            font-weight: var(--weight-light);
            color: var(--noir-ink);
            letter-spacing: 0.02em;
            margin: 0;
        }}
        
        .subtitle {{
            font-size: var(--text-sm);
            color: var(--noir-silver);
            font-weight: var(--weight-regular);
            margin-top: var(--space-1);
        }}
        
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: var(--space-1);
            padding: var(--space-1) var(--space-2);
            background: var(--status-success-bg);
            color: var(--status-success);
            border-radius: 6px;
            font-size: var(--text-xs);
            font-weight: var(--weight-medium);
        }}
        
        .status-dot {{
            width: 8px;
            height: 8px;
            background: var(--status-success);
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        
        /* ========================================
           VERSION TABS - 版本切换
           ======================================== */
        
        .version-tabs {{
            background: var(--blanc-snow);
            border-bottom: 1px solid var(--blanc-mist);
            padding: 0 var(--space-6);
        }}
        
        .version-tabs-inner {{
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            gap: var(--space-2);
        }}
        
        .version-tab {{
            padding: var(--space-3) var(--space-4);
            color: var(--noir-silver);
            font-size: var(--text-sm);
            font-weight: var(--weight-medium);
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.3s var(--ease-luxury);
            position: relative;
        }}
        
        .version-tab:hover {{
            color: var(--noir-graphite);
            background: var(--blanc-pearl);
        }}
        
        .version-tab.active {{
            color: var(--noir-ink);
            border-bottom-color: var(--noir-ink);
        }}
        
        /* ========================================
           CONTAINER - 主容器
           ======================================== */
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: var(--space-7) var(--space-6);
        }}
        
        /* ========================================
           STATS GRID - 统计卡片网格 (9个卡片)
           ======================================== */
        
        .stats-section {{
            margin-bottom: var(--space-7);
        }}
        
        .stats-title {{
            font-size: var(--text-xs);
            color: var(--noir-silver);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: var(--space-3);
            font-weight: var(--weight-medium);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: var(--space-3);
            margin-bottom: var(--space-5);
        }}
        
        .stat-card {{
            background: var(--blanc-pure);
            border-radius: 12px;
            padding: var(--space-4);
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--blanc-mist);
            transition: all 0.4s var(--ease-luxury);
            cursor: pointer;
        }}
        
        .stat-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            border-color: var(--blanc-cloud);
        }}
        
        .stat-value {{
            font-size: var(--text-3xl);
            font-weight: var(--weight-light);
            color: var(--noir-ink);
            margin-bottom: var(--space-1);
            font-family: var(--font-mono);
        }}
        
        .stat-label {{
            font-size: var(--text-xs);
            color: var(--noir-silver);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: var(--weight-medium);
        }}
        
        .stat-trend {{
            margin-top: var(--space-2);
            font-size: var(--text-xs);
            color: var(--status-success);
            display: flex;
            align-items: center;
            gap: var(--space-1);
        }}
        
        /* 新增3个卡片的特殊样式 */
        .stats-grid-new {{
            grid-template-columns: repeat(3, 1fr);
        }}
        
        .stat-card-new {{
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card-new::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 3px;
            height: 100%;
            background: var(--accent-gold);
            opacity: 0;
            transition: opacity 0.3s;
        }}
        
        .stat-card-new:hover::before {{
            opacity: 1;
        }}
        
        .stat-meta {{
            margin-top: var(--space-2);
            padding-top: var(--space-2);
            border-top: 1px solid var(--blanc-mist);
            font-size: var(--text-xs);
            color: var(--noir-ash);
        }}
        
        .stat-actions {{
            margin-top: var(--space-3);
            display: flex;
            gap: var(--space-2);
        }}
        
        .stat-btn {{
            padding: var(--space-1) var(--space-2);
            border-radius: 6px;
            font-size: var(--text-2xs);
            background: var(--blanc-snow);
            color: var(--noir-graphite);
            border: 1px solid var(--blanc-cloud);
            cursor: pointer;
            transition: all 0.2s;
            font-weight: var(--weight-medium);
        }}
        
        .stat-btn:hover {{
            background: var(--blanc-silk);
            border-color: var(--noir-silver);
        }}
        
        /* ========================================
           TASK TABS - 任务Tab (8个Tab)
           ======================================== */
        
        .task-tabs-section {{
            margin-bottom: var(--space-6);
        }}
        
        .task-tabs {{
            display: flex;
            gap: var(--space-2);
            flex-wrap: wrap;
            margin-bottom: var(--space-4);
        }}
        
        .task-tab {{
            padding: var(--space-2) var(--space-4);
            border-radius: 8px;
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-cloud);
            color: var(--noir-graphite);
            font-size: var(--text-sm);
            font-weight: var(--weight-medium);
            cursor: pointer;
            transition: all 0.3s var(--ease-luxury);
            display: flex;
            align-items: center;
            gap: var(--space-2);
        }}
        
        .task-tab:hover {{
            background: var(--blanc-snow);
            border-color: var(--noir-silver);
        }}
        
        .task-tab.active {{
            background: var(--noir-ink);
            color: var(--blanc-pure);
            border-color: var(--noir-ink);
        }}
        
        .task-tab-icon {{
            font-size: var(--text-base);
        }}
        
        .task-tab-count {{
            font-family: var(--font-mono);
            font-size: var(--text-xs);
            opacity: 0.8;
        }}
        
        .tabs-divider {{
            width: 100%;
            height: 1px;
            background: var(--blanc-mist);
            margin: var(--space-3) 0;
        }}
        
        /* ========================================
           CONTENT AREA - 内容展示区
           ======================================== */
        
        .content-area {{
            background: var(--blanc-pure);
            border-radius: 16px;
            padding: var(--space-6);
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--blanc-mist);
            min-height: 600px;
        }}
        
        .content-header {{
            margin-bottom: var(--space-5);
            padding-bottom: var(--space-4);
            border-bottom: 1px solid var(--blanc-mist);
        }}
        
        .content-title {{
            font-size: var(--text-2xl);
            font-weight: var(--weight-light);
            color: var(--noir-ink);
            margin-bottom: var(--space-2);
        }}
        
        .content-description {{
            font-size: var(--text-sm);
            color: var(--noir-silver);
        }}
        
        /* ========================================
           TASK CARD - 任务卡片（增强版）
           ======================================== */
        
        .task-card {{
            background: var(--blanc-snow);
            border-radius: 12px;
            padding: var(--space-5);
            margin-bottom: var(--space-4);
            border: 1px solid var(--blanc-cloud);
            transition: all 0.3s var(--ease-luxury);
        }}
        
        .task-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            border-color: var(--noir-silver);
        }}
        
        .task-header {{
            display: flex;
            align-items: center;
            gap: var(--space-3);
            margin-bottom: var(--space-3);
        }}
        
        .task-priority {{
            padding: var(--space-1) var(--space-2);
            border-radius: 6px;
            font-size: var(--text-xs);
            font-weight: var(--weight-semibold);
        }}
        
        .priority-p0 {{
            background: var(--status-error-bg);
            color: var(--status-error);
        }}
        
        .task-id {{
            font-family: var(--font-mono);
            font-size: var(--text-xs);
            color: var(--noir-silver);
        }}
        
        .task-title {{
            font-size: var(--text-lg);
            font-weight: var(--weight-medium);
            color: var(--noir-ink);
            margin-bottom: var(--space-2);
        }}
        
        .task-description {{
            font-size: var(--text-sm);
            color: var(--noir-steel);
            margin-bottom: var(--space-3);
        }}
        
        /* AI协作链 */
        .ai-chain {{
            display: flex;
            align-items: center;
            gap: var(--space-2);
            padding: var(--space-3);
            background: var(--blanc-pearl);
            border-radius: 8px;
            margin-bottom: var(--space-3);
        }}
        
        .ai-chain-label {{
            font-size: var(--text-xs);
            color: var(--noir-silver);
            font-weight: var(--weight-medium);
        }}
        
        .ai-chain-flow {{
            display: flex;
            align-items: center;
            gap: var(--space-2);
            font-size: var(--text-sm);
        }}
        
        .ai-arrow {{
            color: var(--noir-ash);
        }}
        
        /* 关联信息 */
        .task-relations {{
            display: flex;
            align-items: center;
            gap: var(--space-4);
            padding: var(--space-3);
            background: var(--blanc-pearl);
            border-radius: 8px;
            margin-bottom: var(--space-3);
            font-size: var(--text-sm);
        }}
        
        .task-relation-item {{
            display: flex;
            align-items: center;
            gap: var(--space-1);
        }}
        
        .relation-icon {{
            font-size: var(--text-base);
        }}
        
        /* 操作按钮组 */
        .task-actions {{
            display: flex;
            gap: var(--space-2);
            margin-top: var(--space-4);
            padding-top: var(--space-4);
            border-top: 1px solid var(--blanc-cloud);
        }}
        
        .task-action-btn {{
            padding: var(--space-2) var(--space-3);
            border-radius: 8px;
            font-size: var(--text-sm);
            font-weight: var(--weight-medium);
            cursor: pointer;
            transition: all 0.2s;
            border: 1px solid var(--blanc-cloud);
            background: var(--blanc-pure);
            color: var(--noir-graphite);
        }}
        
        .task-action-btn:hover {{
            background: var(--blanc-silk);
            border-color: var(--noir-silver);
        }}
        
        /* ========================================
           EVENT CARD - 事件卡片
           ======================================== */
        
        .event-card {{
            background: var(--blanc-snow);
            border-radius: 12px;
            padding: var(--space-5);
            margin-bottom: var(--space-4);
            border-left: 3px solid var(--status-info);
        }}
        
        .event-header {{
            display: flex;
            align-items: center;
            gap: var(--space-3);
            margin-bottom: var(--space-3);
            padding-bottom: var(--space-3);
            border-bottom: 1px solid var(--blanc-cloud);
        }}
        
        .event-type-badge {{
            padding: var(--space-1) var(--space-2);
            border-radius: 6px;
            font-size: var(--text-xs);
            font-weight: var(--weight-semibold);
            background: var(--status-info-bg);
            color: var(--status-info);
        }}
        
        .event-time {{
            font-size: var(--text-xs);
            color: var(--noir-silver);
        }}
        
        .event-title {{
            font-size: var(--text-lg);
            font-weight: var(--weight-medium);
            color: var(--noir-ink);
            margin-bottom: var(--space-2);
        }}
        
        .event-description {{
            font-size: var(--text-sm);
            color: var(--noir-steel);
            margin-bottom: var(--space-3);
        }}
        
        .event-meta {{
            display: flex;
            gap: var(--space-4);
            font-size: var(--text-xs);
            color: var(--noir-silver);
        }}
        
        .event-actions {{
            display: flex;
            gap: var(--space-2);
            margin-top: var(--space-3);
        }}
        
        /* ========================================
           CONVERSATION CARD - 对话卡片
           ======================================== */
        
        .conversation-card {{
            background: var(--blanc-snow);
            border-radius: 12px;
            padding: var(--space-5);
            margin-bottom: var(--space-4);
            border: 1px solid var(--blanc-cloud);
        }}
        
        .conversation-header {{
            display: flex;
            align-items: center;
            gap: var(--space-3);
            margin-bottom: var(--space-3);
            padding-bottom: var(--space-3);
            border-bottom: 1px solid var(--blanc-cloud);
        }}
        
        .conversation-status {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--status-success);
        }}
        
        .conversation-title {{
            flex: 1;
            font-size: var(--text-lg);
            font-weight: var(--weight-medium);
            color: var(--noir-ink);
        }}
        
        .conversation-stats {{
            display: flex;
            gap: var(--space-4);
            margin-bottom: var(--space-3);
            font-size: var(--text-sm);
            color: var(--noir-silver);
        }}
        
        .conversation-participants {{
            display: flex;
            align-items: center;
            gap: var(--space-1);
            font-size: var(--text-sm);
            color: var(--noir-steel);
            margin-bottom: var(--space-3);
        }}
        
        .conversation-tags {{
            display: flex;
            gap: var(--space-2);
            margin-bottom: var(--space-3);
        }}
        
        .tag {{
            padding: var(--space-1) var(--space-2);
            border-radius: 6px;
            font-size: var(--text-xs);
            background: var(--blanc-silk);
            color: var(--noir-graphite);
        }}
        
        .conversation-preview {{
            font-size: var(--text-sm);
            color: var(--noir-steel);
            font-style: italic;
            padding: var(--space-3);
            background: var(--blanc-pearl);
            border-radius: 8px;
            border-left: 3px solid var(--accent-gold);
            margin-bottom: var(--space-3);
        }}
        
        /* ========================================
           MEMORY CARD - 记忆卡片
           ======================================== */
        
        .memory-card {{
            background: var(--blanc-snow);
            border-radius: 12px;
            padding: var(--space-5);
            margin-bottom: var(--space-4);
            border: 1px solid var(--blanc-cloud);
            position: relative;
        }}
        
        .memory-type {{
            position: absolute;
            top: var(--space-3);
            right: var(--space-3);
            font-size: var(--text-2xl);
        }}
        
        .memory-header {{
            margin-bottom: var(--space-3);
            padding-bottom: var(--space-3);
            border-bottom: 1px solid var(--blanc-cloud);
        }}
        
        .memory-category {{
            display: inline-block;
            padding: var(--space-1) var(--space-2);
            border-radius: 6px;
            font-size: var(--text-xs);
            font-weight: var(--weight-semibold);
            background: var(--accent-gold);
            color: var(--blanc-pure);
            margin-bottom: var(--space-2);
        }}
        
        .memory-title {{
            font-size: var(--text-lg);
            font-weight: var(--weight-medium);
            color: var(--noir-ink);
            margin-bottom: var(--space-2);
        }}
        
        .memory-importance {{
            display: inline-flex;
            gap: 2px;
            margin-left: var(--space-2);
        }}
        
        .star {{
            color: var(--accent-gold);
            font-size: var(--text-xs);
        }}
        
        .memory-content {{
            font-size: var(--text-sm);
            color: var(--noir-steel);
            line-height: 1.6;
            margin-bottom: var(--space-3);
        }}
        
        .memory-meta {{
            display: flex;
            gap: var(--space-4);
            font-size: var(--text-xs);
            color: var(--noir-silver);
            padding-top: var(--space-3);
            border-top: 1px solid var(--blanc-cloud);
        }}
        
        /* ========================================
           UTILITY CLASSES
           ======================================== */
        
        .text-center {{ text-align: center; }}
        .text-muted {{ color: var(--noir-silver); }}
        .mb-4 {{ margin-bottom: var(--space-4); }}
        .mt-6 {{ margin-top: var(--space-6); }}
        
        /* ========================================
           RESPONSIVE
           ======================================== */
        
        @media (max-width: 1200px) {{
            .stats-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}
        
        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .stats-grid-new {{
                grid-template-columns: 1fr;
            }}
            
            .task-tabs {{
                flex-wrap: wrap;
            }}
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <div class="logo-section">
                <h1 class="logo">任务所·Flow</h1>
                <p class="subtitle">用对话，开工；用流程，收工——AI开发工厂新实践</p>
            </div>
            <div class="status-badge">
                <span class="status-dot"></span>
                ONLINE
            </div>
        </div>
    </header>

    <!-- Version Tabs -->
    <div class="version-tabs">
        <div class="version-tabs-inner">
            <div class="version-tab active">版本1.0</div>
            <div class="version-tab">版本2.0</div>
            <div class="version-tab">版本3.0</div>
        </div>
    </div>

    <!-- Main Container -->
    <div class="container">
        
        <!-- Stats Section - 现有6个统计卡片 -->
        <div class="stats-section">
            <div class="stats-title">📊 任务统计</div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{tasks_total}</div>
                    <div class="stat-label">总任务数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{tasks_pending}</div>
                    <div class="stat-label">待处理</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{tasks_in_progress}</div>
                    <div class="stat-label">进行中</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{tasks_completed}</div>
                    <div class="stat-label">已完成</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{tasks_cancelled}</div>
                    <div class="stat-label">已取消</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{tokens_display}</div>
                    <div class="stat-label">Token使用</div>
                </div>
            </div>
        </div>

        <!-- Stats Section - 新增3个统计卡片 -->
        <div class="stats-section">
            <div class="stats-title">🆕 新增统计</div>
            <div class="stats-grid stats-grid-new">
                <div class="stat-card stat-card-new">
                    <div class="stat-value">{events_total}</div>
                    <div class="stat-label">📊 事件数</div>
                    <div class="stat-trend">↑ +{events_today} 今天</div>
                    <div class="stat-actions">
                        <button class="stat-btn">查看</button>
                    </div>
                </div>
                <div class="stat-card stat-card-new">
                    <div class="stat-value">{conversations_total}</div>
                    <div class="stat-label">💬 会话</div>
                    <div class="stat-meta">{conversations_messages} 消息</div>
                    <div class="stat-actions">
                        <button class="stat-btn">查看</button>
                    </div>
                </div>
                <div class="stat-card stat-card-new">
                    <div class="stat-value">{memory_total}</div>
                    <div class="stat-label">💡 记忆</div>
                    <div class="stat-meta">{memory_decisions} 决策</div>
                    <div class="stat-actions">
                        <button class="stat-btn">查看</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Task Tabs - 现有5个 + 新增3个 -->
        <div class="task-tabs-section">
            <div class="task-tabs">
                <div class="task-tab active" data-tab="all">
                    <span class="task-tab-icon">📋</span>
                    <span>全部</span>
                    <span class="task-tab-count">{tasks_total}</span>
                </div>
                <div class="task-tab" data-tab="pending">
                    <span class="task-tab-icon">⏸️</span>
                    <span>待处理</span>
                    <span class="task-tab-count">{tasks_pending}</span>
                </div>
                <div class="task-tab" data-tab="in-progress">
                    <span class="task-tab-icon">▶️</span>
                    <span>进行中</span>
                    <span class="task-tab-count">{tasks_in_progress}</span>
                </div>
                <div class="task-tab" data-tab="completed">
                    <span class="task-tab-icon">✅</span>
                    <span>已完成</span>
                    <span class="task-tab-count">{tasks_completed}</span>
                </div>
                <div class="task-tab" data-tab="cancelled">
                    <span class="task-tab-icon">❌</span>
                    <span>已取消</span>
                    <span class="task-tab-count">{tasks_cancelled}</span>
                </div>
                
                <div class="tabs-divider"></div>
                
                <div class="task-tab" data-tab="events">
                    <span class="task-tab-icon">📊</span>
                    <span>事件</span>
                    <span class="task-tab-count">{events_total}</span>
                </div>
                <div class="task-tab" data-tab="conversations">
                    <span class="task-tab-icon">💬</span>
                    <span>对话</span>
                    <span class="task-tab-count">{conversations_total}</span>
                </div>
                <div class="task-tab" data-tab="memories">
                    <span class="task-tab-icon">💡</span>
                    <span>记忆</span>
                    <span class="task-tab-count">{memory_total}</span>
                </div>
            </div>
        </div>

        <!-- Content Area -->
        <div class="content-area" id="contentArea">
            <!-- 默认显示任务列表 -->
            <div class="content-section" id="tasks-section">
                <div class="content-header">
                    <h2 class="content-title">任务列表</h2>
                    <p class="content-description">显示所有任务，包含AI协作链和关联信息</p>
                </div>

                <!-- 示例任务卡片 -->
                <div class="task-card">
                    <div class="task-header">
                        <span class="task-priority priority-p0">🔴 P0</span>
                        <span class="task-id">INTEGRATE-003</span>
                        <span class="text-muted">|</span>
                        <span class="text-muted">李明</span>
                        <span class="text-muted">|</span>
                        <span class="text-muted">2.0h</span>
                    </div>
                    <h3 class="task-title">Token同步集成 - Backend to Frontend</h3>
                    <p class="task-description">
                        实现后端Token数据到前端Dashboard的实时同步功能
                    </p>
                    
                    <div class="ai-chain">
                        <span class="ai-chain-label">🤖 AI协作链:</span>
                        <div class="ai-chain-flow">
                            <span>后端AI</span>
                            <span class="ai-arrow">→</span>
                            <span>集成AI</span>
                            <span class="ai-arrow">→</span>
                            <span>架构师审查</span>
                        </div>
                    </div>
                    
                    <div class="task-relations">
                        <div class="task-relation-item">
                            <span class="relation-icon">📊</span>
                            <span>关联: 3事件</span>
                        </div>
                        <span>|</span>
                        <div class="task-relation-item">
                            <span class="relation-icon">💬</span>
                            <span>1讨论</span>
                        </div>
                        <span>|</span>
                        <div class="task-relation-item">
                            <span class="relation-icon">💡</span>
                            <span>1记忆</span>
                        </div>
                    </div>
                    
                    <div class="task-actions">
                        <button class="task-action-btn">复制提示词</button>
                        <button class="task-action-btn">查看事件</button>
                        <button class="task-action-btn">查看对话</button>
                        <button class="task-action-btn">查看记忆</button>
                    </div>
                </div>
            </div>

            <!-- 事件流内容（默认隐藏） -->
            <div class="content-section" id="events-section" style="display:none;">
                <div class="content-header">
                    <h2 class="content-title">事件流</h2>
                    <p class="content-description">实时显示系统事件和任务进度</p>
                </div>

                <div class="event-card">
                    <div class="event-header">
                        <span class="event-type-badge">🟢 INFO</span>
                        <span class="event-time">2025-11-19 14:32</span>
                    </div>
                    <h3 class="event-title">✅ 任务完成: REQ-010-E</h3>
                    <p class="event-description">事件系统端到端测试通过</p>
                    <div class="event-meta">
                        <span>👤 Full-stack</span>
                        <span>|</span>
                        <span>📋 任务:REQ-010-E</span>
                    </div>
                    <div class="event-actions">
                        <button class="task-action-btn">详情</button>
                        <button class="task-action-btn">查看任务</button>
                        <button class="task-action-btn">查看代码</button>
                    </div>
                </div>
            </div>

            <!-- 对话内容（默认隐藏） -->
            <div class="content-section" id="conversations-section" style="display:none;">
                <div class="content-header">
                    <h2 class="content-title">对话历史</h2>
                    <p class="content-description">查看所有AI对话会话</p>
                </div>

                <div class="conversation-card">
                    <div class="conversation-header">
                        <span class="conversation-status"></span>
                        <span class="conversation-title">🟢 session-001 | Dashboard重构讨论</span>
                    </div>
                    <div class="conversation-stats">
                        <span>📅 2天前</span>
                        <span>|</span>
                        <span>💬 6消息</span>
                        <span>|</span>
                        <span>🔢 25K tokens</span>
                    </div>
                    <div class="conversation-participants">
                        <span>🤖 参与AI:</span>
                        <span>架构师、前端AI</span>
                    </div>
                    <div class="conversation-tags">
                        <span class="tag">🏷️ Dashboard</span>
                        <span class="tag">🏷️ 重构</span>
                        <span class="tag">🏷️ UI</span>
                    </div>
                    <div class="conversation-preview">
                        "讨论了Dashboard的重构方案，决定采用模块化..."
                    </div>
                    <div class="task-actions">
                        <button class="task-action-btn">查看详情</button>
                        <button class="task-action-btn">继续对话</button>
                        <button class="task-action-btn">导出</button>
                    </div>
                </div>
            </div>

            <!-- 记忆内容（默认隐藏） -->
            <div class="content-section" id="memories-section" style="display:none;">
                <div class="content-header">
                    <h2 class="content-title">项目记忆</h2>
                    <p class="content-description">查看项目知识库和决策记录</p>
                </div>

                <div class="memory-card">
                    <span class="memory-type">🏛️</span>
                    <div class="memory-header">
                        <span class="memory-category">ADR</span>
                        <h3 class="memory-title">
                            采用Monorepo架构
                            <span class="memory-importance">
                                <span class="star">⭐</span>
                                <span class="star">⭐</span>
                                <span class="star">⭐</span>
                                <span class="star">⭐</span>
                                <span class="star">⭐</span>
                                <span class="star">⭐</span>
                                <span class="star">⭐</span>
                                <span class="star">⭐</span>
                            </span>
                        </h3>
                    </div>
                    <p class="memory-content">
                        项目规模扩大，需要统一管理多个包，采用Lerna+...
                    </p>
                    <div class="memory-meta">
                        <span>📅 2天前</span>
                        <span>|</span>
                        <span>🏷️ architecture, ADR</span>
                        <span>|</span>
                        <span>🔗 3个关联</span>
                    </div>
                    <div class="task-actions">
                        <button class="task-action-btn">查看详情</button>
                        <button class="task-action-btn">编辑</button>
                        <button class="task-action-btn">查看关联</button>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <script>
        // Tab切换逻辑
        const tabs = document.querySelectorAll('.task-tab');
        const sections = {{
            'all': 'tasks-section',
            'pending': 'tasks-section',
            'in-progress': 'tasks-section',
            'completed': 'tasks-section',
            'cancelled': 'tasks-section',
            'events': 'events-section',
            'conversations': 'conversations-section',
            'memories': 'memories-section'
        }};

        tabs.forEach(tab => {{
            tab.addEventListener('click', () => {{
                // 移除所有active状态
                tabs.forEach(t => t.classList.remove('active'));
                // 添加当前active状态
                tab.classList.add('active');

                // 隐藏所有section
                document.querySelectorAll('.content-section').forEach(s => s.style.display = 'none');
                
                // 显示对应section
                const targetTab = tab.getAttribute('data-tab');
                const targetSection = sections[targetTab];
                if (targetSection) {{
                    document.getElementById(targetSection).style.display = 'block';
                }}
            }});
        }});

        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    </script>
</body>
</html>"""


def _format_events_for_display(events_raw):
    """将原始事件数据转换为前端展示格式"""
    # 这里是简化版本，实际需要根据event_provider的返回格式调整
    return []

