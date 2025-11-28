"""
Blanc Luxury Edition - 白色奢华版设计系统
基于原型图实现的极简主义Dashboard

设计哲学：Ethereal Industrial Elegance
- 光影诗学：通过微妙的阴影层次创造空间深度
- 呼吸感设计：大量留白，让界面自由呼吸
- 触感视觉化：模拟高端材质的细腻质感
- 减法美学：Less is Luxury
"""


def get_blanc_luxury_dashboard(
    data_provider,
    event_provider,
    memory_provider,
    conversations_provider=None
) -> str:
    """
    生成Blanc Luxury风格的Dashboard主页（集成真实数据）
    
    Args:
        data_provider: 任务数据提供器（StateManagerAdapter）
        event_provider: 事件流数据提供器（EventStreamProvider）
        memory_provider: 项目记忆数据提供器（ProjectMemoryProvider）
        conversations_provider: 对话历史数据提供器（可选）
    """
    
    # 1. 获取任务统计数据
    stats = data_provider.get_stats()
    tasks_total = stats.total_tasks
    tasks_completed = stats.completed_tasks
    tasks_pending = stats.pending_tasks
    tasks_in_progress = stats.in_progress_tasks
    tasks_today = tasks_pending + tasks_in_progress  # 今日活跃任务
    
    # 2. 获取事件流统计
    event_stats = event_provider.get_event_stats()
    events_total = event_stats.get('total_events', 0)
    events_warnings = event_stats.get('warning_events', 0)
    events_errors = event_stats.get('error_events', 0)
    events_today = events_warnings + events_errors  # 今日需关注
    
    # 3. 获取记忆空间统计
    memory_stats = memory_provider.get_memory_stats()
    memory_total = memory_stats.get('total_memories', 0)
    memory_decisions = memory_stats.get('decision_memories', 0)
    memory_solutions = memory_stats.get('solution_memories', 0)
    
    # 4. Token统计（模拟数据，后续可接入真实API）
    tokens_remaining = '850K'
    tokens_used = '25K'
    tokens_percent = 85
    
    # 5. 对话会话统计（如果有提供器）
    if conversations_provider:
        conversations_total = conversations_provider.get('total', 5)
        conversations_active = conversations_provider.get('active', 2)
    else:
        conversations_total = 5
        conversations_active = 2
    
    # 6. 获取最近事件（转换为前端格式）
    recent_events_raw = event_provider.get_recent_events(hours=24, limit=5)
    recent_events = _format_events_for_display(recent_events_raw)
    
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>任务所·Flow - Blanc Luxury Edition</title>
    <style>
        /* ========================================
           BLANC LUXURY DESIGN SYSTEM V3
           光的建筑学 · 呼吸感设计
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
            
            /* ===== 奢华点缀色 - 极度克制使用 ===== */
            --accent-gold: #D4AF37;         /* 香槟金 */
            --accent-rose: #E8B4B8;         /* 玫瑰金 */
            --accent-platinum: #E5E4E2;     /* 铂金 */
            
            /* ===== 功能色系统 - 柔和雅致 ===== */
            --status-success: #4A7C59;      /* 森林绿 */
            --status-success-bg: #F0F9F4;   /* 成功背景 */
            --status-warning: #D4A574;      /* 驼色 */
            --status-warning-bg: #FFF8F0;   /* 警告背景 */
            --status-error: #C73E1D;        /* 朱砂红 */
            --status-error-bg: #FFF5F5;     /* 错误背景 */
            --status-info: #5B7C99;         /* 钴蓝 */
            --status-info-bg: #F0F5FA;      /* 信息背景 */
            
            /* ===== 微渐变背景 ===== */
            --gradient-subtle: linear-gradient(180deg, #FFFFFF 0%, #FAFBFC 100%);
            --gradient-header: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(255,255,255,0.95) 100%);
            --gradient-card: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
            
            /* ===== 字体系统 ===== */
            --font-primary: 'SF Pro Display', 'Helvetica Neue', -apple-system, system-ui, 'PingFang SC', sans-serif;
            --font-secondary: 'Playfair Display', 'Georgia', 'PingFang SC', serif;
            --font-mono: 'SF Mono', 'Monaco', 'Consolas', monospace;
            
            /* 字号系统 - 优雅比例 */
            --text-2xs: 10px;
            --text-xs: 12px;
            --text-sm: 14px;
            --text-base: 16px;
            --text-lg: 18px;
            --text-xl: 21px;
            --text-2xl: 28px;
            --text-3xl: 36px;
            --text-4xl: 48px;
            
            /* 字重系统 */
            --weight-thin: 200;
            --weight-light: 300;
            --weight-regular: 400;
            --weight-medium: 500;
            --weight-semibold: 600;
            
            /* 行高系统 */
            --leading-tight: 1.2;
            --leading-normal: 1.5;
            --leading-relaxed: 1.75;
            --leading-loose: 2;
            
            /* ===== 空间系统 - 更大的呼吸感 ===== */
            --space-0: 0px;
            --space-1: 6px;
            --space-2: 12px;
            --space-3: 18px;
            --space-4: 24px;
            --space-5: 32px;
            --space-6: 40px;
            --space-7: 48px;
            --space-8: 64px;
            --space-9: 80px;
            --space-10: 96px;
            --space-11: 120px;
            
            /* ===== 超细腻阴影系统 ===== */
            --shadow-xs: 0 1px 3px rgba(0, 0, 0, 0.04);
            --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
            --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.10);
            --shadow-xl: 0 12px 48px rgba(0, 0, 0, 0.12);
            
            /* 内凹阴影 */
            --shadow-inset-sm: inset 0 1px 2px rgba(0, 0, 0, 0.04);
            --shadow-inset-md: inset 0 2px 4px rgba(0, 0, 0, 0.06);
            
            /* 光晕效果 */
            --glow-soft: 0 0 20px rgba(255, 255, 255, 0.5);
            --glow-gold: 0 0 30px rgba(212, 175, 55, 0.3);
            
            /* ===== 特殊尺寸 ===== */
            --header-height: 72px;
            --sidebar-width: 280px;
            --container-max: 1400px;
            --card-padding: 36px;
            
            /* ===== 动画系统 ===== */
            --duration-instant: 100ms;
            --duration-fast: 200ms;
            --duration-normal: 300ms;
            --duration-slow: 400ms;
            --duration-slower: 600ms;
            
            --ease-in-out-soft: cubic-bezier(0.4, 0, 0.2, 1);
            --ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1);
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
            font-size: var(--text-base);
            font-weight: var(--weight-regular);
            line-height: var(--leading-normal);
            color: var(--noir-graphite);
            background: var(--blanc-pure);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        /* ========================================
           LUXURY NAVIGATION
           ======================================== */
        
        .luxury-nav {{
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--blanc-mist);
            height: var(--header-height);
            position: sticky;
            top: 0;
            z-index: 1000;
            transition: all var(--duration-normal) var(--ease-luxury);
        }}
        
        .luxury-nav.scrolled {{
            box-shadow: var(--shadow-sm);
            background: rgba(255, 255, 255, 0.95);
        }}
        
        .nav-content {{
            max-width: var(--container-max);
            margin: 0 auto;
            padding: 0 var(--space-8);
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .nav-logo {{
            display: flex;
            flex-direction: column;
            gap: var(--space-1);
        }}
        
        .nav-logo__title {{
            font-family: var(--font-secondary);
            font-size: var(--text-xl);
            font-weight: var(--weight-light);
            letter-spacing: 0.08em;
            color: var(--noir-ink);
        }}
        
        .nav-logo__subtitle {{
            font-size: var(--text-xs);
            font-weight: var(--weight-light);
            color: var(--noir-silver);
            letter-spacing: 0.05em;
        }}
        
        .nav-actions {{
            display: flex;
            gap: var(--space-3);
            align-items: center;
        }}
        
        .icon-btn {{
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--blanc-snow);
            border: 1px solid var(--blanc-mist);
            border-radius: 10px;
            cursor: pointer;
            transition: all var(--duration-normal) var(--ease-luxury);
            font-size: var(--text-lg);
            position: relative;
            overflow: hidden;
        }}
        
        .icon-btn::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(0, 0, 0, 0.05);
            transform: translate(-50%, -50%);
            transition: width var(--duration-slower), height var(--duration-slower);
        }}
        
        .icon-btn:hover {{
            background: var(--blanc-pure);
            border-color: var(--blanc-cloud);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}
        
        .icon-btn:hover::before {{
            width: 200px;
            height: 200px;
        }}
        
        .icon-btn:active {{
            transform: translateY(0) scale(0.95);
        }}
        
        /* ========================================
           SECONDARY NAVIGATION
           ======================================== */
        
        .secondary-nav {{
            background: var(--blanc-pearl);
            border-bottom: 1px solid var(--blanc-mist);
            padding: var(--space-3) 0;
            position: sticky;
            top: var(--header-height);
            z-index: 999;
        }}
        
        .secondary-nav__content {{
            max-width: var(--container-max);
            margin: 0 auto;
            padding: 0 var(--space-8);
            display: flex;
            gap: var(--space-7);
        }}
        
        .nav-link {{
            color: var(--noir-steel);
            font-weight: var(--weight-regular);
            font-size: var(--text-sm);
            text-decoration: none;
            position: relative;
            padding: var(--space-2) 0;
            transition: color var(--duration-normal);
        }}
        
        .nav-link::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 1px;
            background: var(--noir-ink);
            transition: width var(--duration-normal) var(--ease-luxury);
        }}
        
        .nav-link:hover {{
            color: var(--noir-charcoal);
        }}
        
        .nav-link:hover::after,
        .nav-link.active::after {{
            width: 100%;
        }}
        
        .nav-link.active {{
            color: var(--noir-ink);
            font-weight: var(--weight-medium);
        }}
        
        /* ========================================
           MAIN CONTAINER
           ======================================== */
        
        .luxury-container {{
            max-width: var(--container-max);
            margin: 0 auto;
            padding: var(--space-10) var(--space-8);
            display: flex;
            flex-direction: column;
            gap: var(--space-9);
        }}
        
        /* ========================================
           SECTION HEADER
           ======================================== */
        
        .section-header {{
            display: flex;
            flex-direction: column;
            gap: var(--space-2);
            margin-bottom: var(--space-6);
        }}
        
        .section-title {{
            font-family: var(--font-secondary);
            font-size: var(--text-2xl);
            font-weight: var(--weight-light);
            color: var(--noir-ink);
            letter-spacing: -0.02em;
        }}
        
        .section-subtitle {{
            font-size: var(--text-sm);
            font-weight: var(--weight-light);
            color: var(--noir-silver);
        }}
        
        /* ========================================
           LUXURY CARD
           ======================================== */
        
        .luxury-card {{
            background: var(--blanc-pure);
            border-radius: 16px;
            padding: var(--card-padding);
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--blanc-mist);
            transition: all var(--duration-slow) var(--ease-luxury);
            position: relative;
            overflow: hidden;
        }}
        
        .luxury-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--blanc-cloud), transparent);
            opacity: 0;
            transition: opacity var(--duration-normal);
        }}
        
        .luxury-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: var(--blanc-cloud);
        }}
        
        .luxury-card:hover::before {{
            opacity: 1;
        }}
        
        /* ========================================
           PULSE GRID - 系统脉搏
           ======================================== */
        
        .pulse-section {{
            background: var(--gradient-subtle);
            border-radius: 20px;
            padding: var(--space-8);
            border: 1px solid var(--blanc-mist);
        }}
        
        .pulse-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: var(--space-6);
            margin-top: var(--space-6);
        }}
        
        .pulse-card {{
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            border-radius: 16px;
            padding: var(--space-6);
            position: relative;
            overflow: hidden;
            transition: all var(--duration-slow) var(--ease-luxury);
            cursor: pointer;
        }}
        
        /* 顶部装饰线 - 更细腻 */
        .pulse-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--card-accent, var(--noir-ink));
            opacity: 0.6;
        }}
        
        /* 光泽效果 */
        .pulse-card::after {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent 30%,
                rgba(255, 255, 255, 0.8) 50%,
                transparent 70%
            );
            transform: rotate(45deg);
            opacity: 0;
            transition: opacity var(--duration-slower);
        }}
        
        .pulse-card:hover {{
            transform: translateY(-6px) scale(1.02);
            box-shadow: var(--shadow-lg);
            border-color: var(--blanc-cloud);
        }}
        
        .pulse-card:hover::after {{
            animation: shine var(--duration-slower) ease-in-out;
        }}
        
        @keyframes shine {{
            0% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); opacity: 0; }}
            50% {{ opacity: 1; }}
            100% {{ transform: translateX(100%) translateY(100%) rotate(45deg); opacity: 0; }}
        }}
        
        .pulse-card.breathing {{
            animation: breathe 6s infinite;
        }}
        
        @keyframes breathe {{
            0%, 100% {{ 
                transform: scale(1); 
                opacity: 1; 
            }}
            50% {{ 
                transform: scale(0.98); 
                opacity: 0.95; 
            }}
        }}
        
        .pulse-label {{
            font-size: var(--text-xs);
            font-weight: var(--weight-light);
            color: var(--noir-ash);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: var(--space-3);
        }}
        
        .pulse-value {{
            font-family: var(--font-mono);
            font-size: 64px;
            font-weight: var(--weight-thin);
            color: var(--noir-ink);
            line-height: 1;
            margin-bottom: var(--space-2);
            letter-spacing: -0.03em;
        }}
        
        .pulse-desc {{
            font-size: var(--text-sm);
            font-weight: var(--weight-light);
            color: var(--noir-steel);
            margin-bottom: var(--space-4);
        }}
        
        .pulse-trend {{
            display: flex;
            align-items: center;
            gap: var(--space-1);
            font-size: var(--text-sm);
            font-weight: var(--weight-medium);
            margin-bottom: var(--space-2);
        }}
        
        .trend-up {{ color: var(--status-success); }}
        .trend-down {{ color: var(--status-error); }}
        .trend-neutral {{ color: var(--noir-silver); }}
        
        .pulse-meta {{
            font-size: var(--text-xs);
            color: var(--noir-ash);
            font-weight: var(--weight-light);
        }}
        
        /* ========================================
           LIVE FEED - 实时动态
           ======================================== */
        
        .live-feed {{
            display: flex;
            flex-direction: column;
            gap: var(--space-5);
        }}
        
        .feed-item {{
            background: var(--blanc-snow);
            border: 1px solid var(--blanc-mist);
            border-left: 3px solid var(--event-color, var(--noir-ash));
            border-radius: 12px;
            padding: var(--space-5);
            transition: all var(--duration-normal) var(--ease-luxury);
            cursor: pointer;
            animation: fadeInUp var(--duration-slower) var(--ease-luxury);
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .feed-item:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            background: var(--blanc-pure);
            border-left-width: 4px;
        }}
        
        .feed-header {{
            display: flex;
            align-items: center;
            gap: var(--space-3);
            margin-bottom: var(--space-3);
        }}
        
        .severity-indicator {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--event-color, var(--noir-ash));
            animation: pulse-dot 3s infinite;
        }}
        
        @keyframes pulse-dot {{
            0%, 100% {{
                opacity: 1;
                transform: scale(1);
            }}
            50% {{
                opacity: 0.5;
                transform: scale(1.2);
            }}
        }}
        
        .feed-time {{
            font-size: var(--text-xs);
            font-weight: var(--weight-light);
            color: var(--noir-silver);
            letter-spacing: 0.05em;
        }}
        
        .feed-title {{
            font-size: var(--text-lg);
            font-weight: var(--weight-medium);
            color: var(--noir-charcoal);
            margin-bottom: var(--space-2);
            line-height: var(--leading-tight);
        }}
        
        .feed-desc {{
            font-size: var(--text-sm);
            font-weight: var(--weight-light);
            color: var(--noir-steel);
            line-height: var(--leading-relaxed);
            margin-bottom: var(--space-3);
        }}
        
        .feed-meta {{
            display: flex;
            gap: var(--space-5);
            font-size: var(--text-xs);
            color: var(--noir-ash);
        }}
        
        /* ========================================
           INFO PANEL - 信息面板
           ======================================== */
        
        .two-col-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: var(--space-7);
        }}
        
        .info-panel {{
            background: var(--blanc-pure);
            border: 1px solid var(--blanc-mist);
            border-radius: 16px;
            padding: var(--space-7);
            transition: all var(--duration-normal) var(--ease-luxury);
        }}
        
        .info-panel:hover {{
            box-shadow: var(--shadow-md);
            border-color: var(--blanc-cloud);
        }}
        
        .panel-title {{
            font-family: var(--font-secondary);
            font-size: var(--text-xl);
            font-weight: var(--weight-light);
            color: var(--noir-ink);
            margin-bottom: var(--space-6);
            letter-spacing: -0.01em;
        }}
        
        .panel-stats {{
            display: flex;
            flex-direction: column;
            gap: var(--space-4);
            margin-bottom: var(--space-6);
        }}
        
        .stat-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: var(--space-3);
            border-bottom: 1px solid var(--blanc-silk);
        }}
        
        .stat-label {{
            font-size: var(--text-sm);
            font-weight: var(--weight-light);
            color: var(--noir-steel);
        }}
        
        .stat-value {{
            font-family: var(--font-mono);
            font-size: var(--text-lg);
            font-weight: var(--weight-medium);
            color: var(--noir-ink);
        }}
        
        .panel-list {{
            list-style: none;
            margin-bottom: var(--space-6);
        }}
        
        .panel-list li {{
            padding: var(--space-3) 0;
            border-bottom: 1px solid var(--blanc-silk);
            font-size: var(--text-sm);
            font-weight: var(--weight-light);
            color: var(--noir-graphite);
        }}
        
        .panel-list li:last-child {{
            border-bottom: none;
        }}
        
        /* ========================================
           LUXURY BUTTON
           ======================================== */
        
        .luxury-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: var(--space-2);
            padding: var(--space-3) var(--space-5);
            font-family: var(--font-primary);
            font-size: var(--text-sm);
            font-weight: var(--weight-medium);
            color: var(--noir-charcoal);
            text-decoration: none;
            background: transparent;
            border: 1.5px solid var(--blanc-cloud);
            border-radius: 10px;
            cursor: pointer;
            transition: all var(--duration-normal) var(--ease-luxury);
            position: relative;
            overflow: hidden;
        }}
        
        .luxury-btn::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(0, 0, 0, 0.03);
            transform: translate(-50%, -50%);
            transition: width var(--duration-slower), height var(--duration-slower);
        }}
        
        .luxury-btn:hover {{
            background: var(--noir-ink);
            color: var(--blanc-pure);
            border-color: var(--noir-ink);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}
        
        .luxury-btn:hover::before {{
            width: 300px;
            height: 300px;
        }}
        
        .luxury-btn:active {{
            transform: translateY(0) scale(0.98);
        }}
        
        .luxury-btn.primary {{
            background: var(--noir-ink);
            color: var(--blanc-pure);
            border-color: var(--noir-ink);
        }}
        
        .luxury-btn.primary:hover {{
            background: var(--noir-charcoal);
            border-color: var(--noir-charcoal);
        }}
        
        /* ========================================
           STATUS BANNER - 状态横幅
           ======================================== */
        
        .status-banner {{
            background: var(--status-success-bg);
            border: 1px solid var(--status-success);
            border-radius: 12px;
            padding: var(--space-5);
            display: flex;
            align-items: center;
            gap: var(--space-5);
        }}
        
        .status-icon {{
            width: 48px;
            height: 48px;
            background: var(--status-success);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--blanc-pure);
            font-size: var(--text-2xl);
            flex-shrink: 0;
        }}
        
        .status-content {{
            flex: 1;
        }}
        
        .status-title {{
            font-size: var(--text-lg);
            font-weight: var(--weight-medium);
            color: var(--status-success);
            margin-bottom: var(--space-1);
        }}
        
        .status-desc {{
            font-size: var(--text-sm);
            font-weight: var(--weight-light);
            color: var(--noir-steel);
        }}
        
        /* ========================================
           RESPONSIVE
           ======================================== */
        
        @media (max-width: 1024px) {{
            .pulse-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .two-col-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        @media (max-width: 768px) {{
            .luxury-container {{
                padding: var(--space-7) var(--space-4);
            }}
            
            .nav-content,
            .secondary-nav__content {{
                padding: 0 var(--space-4);
            }}
            
            .pulse-grid {{
                grid-template-columns: 1fr;
            }}
            
            .pulse-value {{
                font-size: 48px;
            }}
            
            .secondary-nav__content {{
                overflow-x: auto;
                white-space: nowrap;
            }}
        }}
    </style>
</head>
<body>
    <!-- LUXURY NAVIGATION -->
    <nav class="luxury-nav">
        <div class="nav-content">
            <div class="nav-logo">
                <div class="nav-logo__title">任务所·Flow</div>
                <div class="nav-logo__subtitle">用对话开工 · 用流程收工</div>
            </div>
            <div class="nav-actions">
                <button class="icon-btn" title="设置">⚙</button>
                <button class="icon-btn" title="通知">🔔</button>
                <button class="icon-btn" title="个人">👤</button>
            </div>
        </div>
    </nav>

    <!-- SECONDARY NAVIGATION -->
    <nav class="secondary-nav">
        <div class="secondary-nav__content">
            <a href="/blanc" class="nav-link active">总览</a>
            <a href="/blanc/events" class="nav-link">事件流</a>
            <a href="/blanc/conversations" class="nav-link">对话历史</a>
            <a href="/blanc/memory" class="nav-link">记忆空间</a>
            <a href="/" class="nav-link">任务看板</a>
        </div>
    </nav>

    <!-- MAIN CONTAINER -->
    <main class="luxury-container">
        <!-- SYSTEM PULSE -->
        <section class="pulse-section">
            <div class="section-header">
                <h2 class="section-title">系统脉搏</h2>
                <p class="section-subtitle">实时运营指标监控</p>
            </div>
            
            <div class="pulse-grid">
                <!-- Tasks -->
                <div class="pulse-card breathing" style="--card-accent: var(--noir-ink);">
                    <div class="pulse-label">任务</div>
                    <div class="pulse-value">{tasks_total}</div>
                    <div class="pulse-desc">活跃项目</div>
                    <div class="pulse-trend trend-up">↑ 今日新增 {tasks_today}</div>
                    <div class="pulse-meta">已完成 {tasks_completed} 项</div>
                </div>

                <!-- Events -->
                <div class="pulse-card breathing" style="--card-accent: var(--status-info); animation-delay: 1.5s;">
                    <div class="pulse-label">事件流</div>
                    <div class="pulse-value">{events_total}</div>
                    <div class="pulse-desc">总事件数</div>
                    <div class="pulse-trend trend-up">↑ 今日新增 {events_today}</div>
                    <div class="pulse-meta">⚠ {events_warnings} 条警告</div>
                </div>

                <!-- Conversations -->
                <div class="pulse-card breathing" style="--card-accent: var(--status-success); animation-delay: 3s;">
                    <div class="pulse-label">对话会话</div>
                    <div class="pulse-value">{conversations_total}</div>
                    <div class="pulse-desc">活跃会话</div>
                    <div class="pulse-trend trend-neutral">→ 今日无变化</div>
                    <div class="pulse-meta">{conversations_active} 个活跃</div>
                </div>

                <!-- Tokens -->
                <div class="pulse-card breathing" style="--card-accent: var(--status-warning); animation-delay: 4.5s;">
                    <div class="pulse-label">Token 余量</div>
                    <div class="pulse-value">{tokens_remaining}</div>
                    <div class="pulse-desc">剩余配额</div>
                    <div class="pulse-trend trend-down">↓ 消耗 {tokens_used}</div>
                    <div class="pulse-meta">剩余 {tokens_percent}%</div>
                </div>
            </div>
        </section>

        <!-- LIVE FEED -->
        <section class="luxury-card">
            <div class="section-header">
                <h2 class="section-title">实时脉动</h2>
                <p class="section-subtitle">最近系统活动</p>
            </div>

            <div class="live-feed">
                {_generate_feed_items(recent_events)}
            </div>
        </section>

        <!-- INFO PANELS -->
        <div class="two-col-grid">
            <!-- Memory Space -->
            <div class="info-panel">
                <h3 class="panel-title">记忆空间</h3>
                <div class="panel-stats">
                    <div class="stat-row">
                        <span class="stat-label">总记录数</span>
                        <span class="stat-value">{memory_total}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">决策记录</span>
                        <span class="stat-value">{memory_decisions}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">解决方案</span>
                        <span class="stat-value">{memory_solutions}</span>
                    </div>
                </div>
                
                <ul class="panel-list">
                    <li>ADR：采用 Monorepo 架构</li>
                    <li>方案：Tab 切换失败解决方案</li>
                    <li>知识：React Hooks 性能优化最佳实践</li>
                </ul>
                
                <a href="/blanc/memory" class="luxury-btn">查看记忆空间 →</a>
            </div>

            <!-- Conversations -->
            <div class="info-panel">
                <h3 class="panel-title">最近对话</h3>
                <div class="panel-stats">
                    <div class="stat-row">
                        <span class="stat-label">活跃会话</span>
                        <span class="stat-value">{conversations_active}</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">总消息数</span>
                        <span class="stat-value">156</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Token 用量</span>
                        <span class="stat-value">125K</span>
                    </div>
                </div>
                
                <ul class="panel-list">
                    <li>Dashboard 重构讨论（6 条消息）</li>
                    <li>API 集成讨论（12 条消息）</li>
                </ul>
                
                <a href="/blanc/conversations" class="luxury-btn">查看所有对话 →</a>
            </div>
        </div>

        <!-- STATUS BANNER -->
        <div class="status-banner">
            <div class="status-icon">✓</div>
            <div class="status-content">
                <h3 class="status-title">系统运行正常</h3>
                <p class="status-desc">API 服务：8800 端口 | 8 个端点可用 | 响应时间 &lt; 100ms</p>
            </div>
            <a href="#" class="luxury-btn primary">查看详情 →</a>
        </div>
    </main>

    <script>
        // 导航栏滚动效果
        const nav = document.querySelector('.luxury-nav');
        let lastScroll = 0;

        window.addEventListener('scroll', () => {{
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > 10) {{
                nav.classList.add('scrolled');
            }} else {{
                nav.classList.remove('scrolled');
            }}
            
            lastScroll = currentScroll;
        }});

        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                }}
            }});
        }});

        // 数字动画
        const animateValue = (element, start, end, duration) => {{
            let startTimestamp = null;
            const step = (timestamp) => {{
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                const easeProgress = 1 - Math.pow(1 - progress, 3); // ease-out
                element.textContent = Math.floor(easeProgress * (end - start) + start);
                if (progress < 1) {{
                    window.requestAnimationFrame(step);
                }}
            }};
            window.requestAnimationFrame(step);
        }};

        // 页面加载时动画数字
        setTimeout(() => {{
            document.querySelectorAll('.pulse-value').forEach(el => {{
                const endValue = parseInt(el.textContent.replace(/[^0-9]/g, '')) || 0;
                if (endValue > 0) {{
                    animateValue(el, 0, endValue, 1500);
                }}
            }});
        }}, 400);

        // 按钮波纹效果
        document.querySelectorAll('.icon-btn').forEach(button => {{
            button.addEventListener('click', function(e) {{
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                this.style.setProperty('--ripple-x', x + 'px');
                this.style.setProperty('--ripple-y', y + 'px');
            }});
        }});
    </script>
</body>
</html>"""

def _format_events_for_display(events_raw):
    """
    将原始事件数据转换为前端显示格式
    
    Args:
        events_raw: 从EventStreamProvider获取的原始事件列表
    
    Returns:
        格式化后的事件列表
    """
    from datetime import datetime
    
    formatted_events = []
    
    for event in events_raw:
        # 计算相对时间
        occurred_at = event.get('occurred_at', '')
        time_ago = _calculate_time_ago(occurred_at)
        
        # 映射严重性到颜色
        severity = event.get('severity', 'info')
        color_map = {
            'info': 'var(--status-info)',
            'warning': 'var(--status-warning)',
            'error': 'var(--status-error)',
            'critical': 'var(--status-error)'
        }
        color = color_map.get(severity, 'var(--status-info)')
        
        # 映射分类到图标
        category = event.get('category', 'general')
        type_map = {
            'task': '任务',
            'issue': '问题',
            'decision': '决策',
            'deployment': '部署',
            'system': '系统'
        }
        event_type = type_map.get(category, '通用')
        
        formatted_events.append({
            'time': time_ago,
            'title': event.get('title', '未知事件'),
            'desc': event.get('description', ''),
            'actor': event.get('actor', 'System'),
            'type': event_type,
            'link': event.get('task_id', event.get('event_id', '')),
            'color': color
        })
    
    return formatted_events


def _calculate_time_ago(timestamp_str):
    """
    计算相对时间（如：2分钟前、1小时前）
    
    Args:
        timestamp_str: ISO格式时间戳字符串
    
    Returns:
        相对时间描述字符串
    """
    from datetime import datetime
    
    if not timestamp_str:
        return '未知时间'
    
    try:
        # 解析时间戳
        event_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now(event_time.tzinfo) if event_time.tzinfo else datetime.now()
        
        # 计算时间差
        delta = now - event_time
        seconds = delta.total_seconds()
        
        if seconds < 60:
            return f'{int(seconds)} 秒前'
        elif seconds < 3600:
            return f'{int(seconds // 60)} 分钟前'
        elif seconds < 86400:
            return f'{int(seconds // 3600)} 小时前'
        elif seconds < 2592000:
            return f'{int(seconds // 86400)} 天前'
        else:
            return f'{int(seconds // 2592000)} 个月前'
    except Exception as e:
        print(f"[时间计算] 解析失败: {e}")
        return '未知时间'


def _generate_feed_items(events):
    """
    生成事件列表HTML
    
    Args:
        events: 格式化后的事件列表
    
    Returns:
        HTML字符串
    """
    items_html = []
    for event in events:
        items_html.append(f"""
                <div class="feed-item" style="--event-color: {event['color']};">
                    <div class="feed-header">
                        <div class="severity-indicator"></div>
                        <span class="feed-time">{event['time']}</span>
                    </div>
                    <h3 class="feed-title">{event['title']}</h3>
                    <p class="feed-desc">{event['desc']}</p>
                    <div class="feed-meta">
                        <span>👤 {event['actor']}</span>
                        <span>📋 {event['type']}</span>
                        <span>🔗 {event['link']}</span>
                    </div>
                </div>
            """)
    return '\n'.join(items_html)

