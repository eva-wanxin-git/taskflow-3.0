"""
Dashboard HTML 模板 - 指挥舱风格（Mission Control）
根据顶级设计师原型方案重设计

设计灵感: NASA休斯顿控制中心 + Apple Watch表盘 + 高级轿车仪表盘
"""


def get_mission_control_dashboard(title: str, subtitle: str, cache_version: str = "v1") -> str:
    """
    获取指挥舱风格的Dashboard HTML
    
    核心特性:
    1. 系统脉搏区 - 4秒心跳动画
    2. 实时脉动区 - 最近5条事件实时更新
    3. 记忆+对话双栏
    4. 任务态势
    5. 系统健康监控
    """
    return f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <title>{title} - 指挥舱 - {cache_version}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            /* 敦煌壁画色系 */
            --black: #000000;
            --gray-900: #212121;
            --gray-800: #424242;
            --gray-700: #616161;
            --gray-600: #757575;
            --gray-500: #9E9E9E;
            --gray-400: #BDBDBD;
            --gray-300: #E0E0E0;
            --gray-200: #EEEEEE;
            --gray-100: #F5F5F5;
            --gray-50: #FAFAFA;
            --white: #FFFFFF;
            --red: #985239;        /* 敦煌赭红 */
            --blue: #537696;       /* 敦煌青蓝 */
            
            /* 严重性颜色 */
            --info: #2E7D32;
            --warning: #F57C00;
            --error: #D32F2F;
            --critical: #C62828;
            
            /* 状态颜色 */
            --status-active: #4CAF50;
            --status-pending: #FFA726;
            --status-completed: #9E9E9E;
            --status-blocked: #EF5350;
            
            /* 空间系统 */
            --space-2: 8px;
            --space-4: 16px;
            --space-6: 24px;
            --space-8: 32px;
            --space-12: 48px;
            --space-16: 64px;
            
            /* 阴影 */
            --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.04);
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.08);
            --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.12);
            --shadow-xl: 0 12px 24px rgba(0, 0, 0, 0.16);
            --shadow-focus: 0 0 0 3px rgba(152, 82, 57, 0.2);
            
            /* 字体 */
            --font-primary: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            --font-chinese: "PingFang SC", "Microsoft YaHei", "Hiragino Sans GB", sans-serif;
            --font-mono: "SF Mono", "Consolas", "Monaco", "Courier New", monospace;
            --font-number: "SF Pro Display", "Helvetica Neue", sans-serif;
            
            /* 动画缓动 */
            --ease-standard: cubic-bezier(0.4, 0.0, 0.2, 1);
            --ease-elegant: cubic-bezier(0.25, 0.1, 0.25, 1);
            
            /* 时长 */
            --duration-fast: 200ms;
            --duration-normal: 300ms;
            --duration-slow: 500ms;
        }}
        
        body {{
            font-family: var(--font-primary), var(--font-chinese);
            background: var(--white);
            color: var(--gray-900);
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1920px;
            margin: 0 auto;
            padding: 0;
        }}
        
        /* ===== 顶栏 (60px高) ===== */
        .top-bar {{
            background: var(--white);
            border-bottom: 1px solid var(--gray-300);
            padding: var(--space-4) var(--space-16);
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 60px;
        }}
        
        .brand-area {{
            display: flex;
            flex-direction: column;
        }}
        
        .brand-title {{
            font-size: 24px;
            font-weight: 700;
            color: var(--black);
            font-family: var(--font-chinese);
            line-height: 1.2;
        }}
        
        .brand-slogan {{
            font-size: 11px;
            color: var(--gray-600);
            margin-top: 2px;
        }}
        
        .top-actions {{
            display: flex;
            gap: var(--space-4);
        }}
        
        .icon-button {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: var(--white);
            border: 1px solid var(--gray-300);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all var(--duration-normal) var(--ease-standard);
            font-size: 18px;
        }}
        
        .icon-button:hover {{
            background: var(--gray-100);
            border-color: var(--black);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}
        
        /* ===== Sticky导航 ===== */
        .sticky-nav {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: var(--white);
            border-bottom: 1px solid var(--gray-300);
            padding: 0 var(--space-16);
        }}
        
        .nav-tabs {{
            display: flex;
            gap: var(--space-2);
            overflow-x: auto;
        }}
        
        .nav-tab {{
            padding: var(--space-4) var(--space-6);
            font-size: 14px;
            font-weight: 500;
            color: var(--gray-700);
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            cursor: pointer;
            transition: all var(--duration-fast) var(--ease-standard);
            white-space: nowrap;
        }}
        
        .nav-tab:hover {{
            color: var(--black);
            background: var(--gray-50);
        }}
        
        .nav-tab.active {{
            color: var(--red);
            border-bottom-color: var(--red);
        }}
        
        /* ===== 主内容区 ===== */
        .main-content {{
            padding: var(--space-12) var(--space-16);
        }}
        
        /* ===== 系统脉搏区 ===== */
        .system-pulse {{
            background: linear-gradient(135deg, var(--gray-50) 0%, var(--white) 100%);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--black);
            padding: var(--space-8);
            margin-bottom: var(--space-12);
        }}
        
        .section-title {{
            font-size: 14px;
            font-weight: 600;
            color: var(--gray-900);
            margin-bottom: var(--space-6);
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: var(--space-2);
        }}
        
        .pulse-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: var(--space-6);
        }}
        
        .pulse-card {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            padding: var(--space-6);
            transition: all var(--duration-normal) var(--ease-elegant);
            animation: heartbeat 4s infinite;
        }}
        
        .pulse-card:hover {{
            border-color: var(--black);
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }}
        
        @keyframes heartbeat {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(0.98); }}
        }}
        
        .pulse-icon {{
            font-size: 24px;
            margin-bottom: var(--space-2);
        }}
        
        .pulse-label {{
            font-size: 10px;
            color: var(--gray-600);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: var(--space-2);
        }}
        
        .pulse-value {{
            font-family: var(--font-number);
            font-size: 48px;
            font-weight: 300;
            color: var(--black);
            line-height: 1;
            margin-bottom: var(--space-2);
            font-variant-numeric: tabular-nums;
        }}
        
        .pulse-trend {{
            font-size: 12px;
            color: var(--gray-600);
            margin-bottom: var(--space-2);
        }}
        
        .pulse-trend.up {{
            color: var(--status-active);
        }}
        
        .pulse-trend.down {{
            color: var(--error);
        }}
        
        .pulse-meta {{
            font-size: 11px;
            color: var(--gray-500);
        }}
        
        .pulse-action {{
            margin-top: var(--space-4);
        }}
        
        .link-button {{
            font-size: 11px;
            color: var(--red);
            text-decoration: none;
            font-weight: 500;
            transition: color var(--duration-fast);
        }}
        
        .link-button:hover {{
            color: var(--black);
        }}
        
        /* ===== 实时脉动区 ===== */
        .live-pulse {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--red);
            padding: var(--space-8);
            margin-bottom: var(--space-12);
        }}
        
        .event-list {{
            display: flex;
            flex-direction: column;
            gap: var(--space-4);
        }}
        
        .event-item {{
            display: flex;
            align-items: flex-start;
            gap: var(--space-4);
            padding: var(--space-4);
            background: var(--gray-50);
            border-left: 3px solid var(--info);
            transition: all var(--duration-fast) var(--ease-standard);
            cursor: pointer;
        }}
        
        .event-item:hover {{
            background: var(--white);
            box-shadow: var(--shadow-sm);
            transform: translateX(4px);
        }}
        
        .event-item.warning {{
            border-left-color: var(--warning);
        }}
        
        .event-item.error {{
            border-left-color: var(--error);
        }}
        
        .event-item.critical {{
            border-left-color: var(--critical);
        }}
        
        .event-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--info);
            flex-shrink: 0;
            margin-top: 6px;
            animation: pulse-dot 2s infinite;
        }}
        
        @keyframes pulse-dot {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.6; transform: scale(1.1); }}
        }}
        
        .event-dot.warning {{
            background: var(--warning);
        }}
        
        .event-dot.error {{
            background: var(--error);
        }}
        
        .event-dot.critical {{
            background: var(--critical);
        }}
        
        .event-content {{
            flex: 1;
        }}
        
        .event-header {{
            display: flex;
            align-items: center;
            gap: var(--space-2);
            margin-bottom: 4px;
        }}
        
        .event-time {{
            font-size: 11px;
            color: var(--gray-500);
            font-family: var(--font-mono);
        }}
        
        .event-type {{
            font-size: 11px;
            color: var(--gray-600);
            font-weight: 500;
        }}
        
        .event-title {{
            font-size: 14px;
            color: var(--gray-900);
            font-weight: 500;
            margin-bottom: 2px;
        }}
        
        .event-meta {{
            font-size: 11px;
            color: var(--gray-600);
        }}
        
        /* ===== 双栏布局 ===== */
        .two-column {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: var(--space-6);
            margin-bottom: var(--space-12);
        }}
        
        .column-card {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--blue);
            padding: var(--space-8);
            transition: all var(--duration-normal) var(--ease-standard);
        }}
        
        .column-card:hover {{
            border-color: var(--black);
            box-shadow: var(--shadow-md);
        }}
        
        .card-stats {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: var(--space-4);
            margin-bottom: var(--space-6);
        }}
        
        .stat-item {{
            display: flex;
            flex-direction: column;
        }}
        
        .stat-item-label {{
            font-size: 11px;
            color: var(--gray-600);
            margin-bottom: 4px;
        }}
        
        .stat-item-value {{
            font-size: 24px;
            font-weight: 600;
            color: var(--black);
            font-family: var(--font-number);
        }}
        
        .recent-list {{
            display: flex;
            flex-direction: column;
            gap: var(--space-2);
            margin-bottom: var(--space-6);
        }}
        
        .recent-item {{
            font-size: 13px;
            color: var(--gray-700);
            padding-left: var(--space-4);
            position: relative;
        }}
        
        .recent-item::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: var(--red);
        }}
        
        /* ===== 任务态势 ===== */
        .task-landscape {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--black);
            padding: var(--space-8);
            margin-bottom: var(--space-12);
        }}
        
        .status-flow {{
            display: flex;
            gap: var(--space-6);
            margin-bottom: var(--space-6);
            padding-bottom: var(--space-6);
            border-bottom: 1px solid var(--gray-300);
        }}
        
        .status-node {{
            flex: 1;
            text-align: center;
            padding: var(--space-4);
            background: var(--gray-50);
            border: 1px solid var(--gray-300);
            cursor: pointer;
            transition: all var(--duration-fast);
        }}
        
        .status-node:hover {{
            background: var(--white);
            border-color: var(--black);
            transform: translateY(-2px);
        }}
        
        .status-node-label {{
            font-size: 12px;
            color: var(--gray-600);
            margin-bottom: 4px;
        }}
        
        .status-node-count {{
            font-size: 28px;
            font-weight: 600;
            color: var(--black);
            font-family: var(--font-number);
        }}
        
        .task-card {{
            background: var(--gray-50);
            border-left: 3px solid var(--error);
            padding: var(--space-4);
            margin-bottom: var(--space-4);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .task-info {{
            flex: 1;
        }}
        
        .task-title {{
            font-size: 14px;
            font-weight: 500;
            color: var(--gray-900);
            margin-bottom: 4px;
        }}
        
        .task-meta {{
            font-size: 11px;
            color: var(--gray-600);
        }}
        
        .task-actions {{
            display: flex;
            gap: var(--space-2);
        }}
        
        .action-button {{
            padding: 6px 12px;
            font-size: 11px;
            background: var(--white);
            border: 1px solid var(--gray-300);
            cursor: pointer;
            transition: all var(--duration-fast);
        }}
        
        .action-button:hover {{
            background: var(--black);
            color: var(--white);
            border-color: var(--black);
        }}
        
        /* ===== 系统健康 ===== */
        .system-health {{
            background: var(--white);
            border: 1px solid var(--gray-300);
            border-top: 2px solid var(--status-active);
            padding: var(--space-6);
            display: flex;
            align-items: center;
            gap: var(--space-4);
        }}
        
        .health-indicator {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--status-active);
            animation: pulse-dot 2s infinite;
        }}
        
        .health-text {{
            flex: 1;
            font-size: 13px;
            color: var(--gray-700);
        }}
        
        .health-details {{
            font-size: 12px;
            color: var(--gray-600);
            font-family: var(--font-mono);
        }}
        
        /* ===== 响应式 ===== */
        @media (max-width: 1200px) {{
            .pulse-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .two-column {{
                grid-template-columns: 1fr;
            }}
            
            .status-flow {{
                flex-wrap: wrap;
            }}
        }}
        
        @media (max-width: 768px) {{
            .pulse-grid {{
                grid-template-columns: 1fr;
            }}
            
            .main-content {{
                padding: var(--space-6) var(--space-4);
            }}
            
            .top-bar {{
                padding: var(--space-4) var(--space-4);
            }}
        }}
        
        /* ===== 加载状态 ===== */
        .loading {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border: 2px solid var(--gray-300);
            border-top-color: var(--red);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        /* ===== 提示信息 ===== */
        .toast {{
            position: fixed;
            bottom: var(--space-6);
            right: var(--space-6);
            background: var(--black);
            color: var(--white);
            padding: var(--space-4) var(--space-6);
            border-radius: 4px;
            font-size: 13px;
            box-shadow: var(--shadow-xl);
            z-index: 1000;
            animation: slideInUp 0.3s var(--ease-elegant);
        }}
        
        @keyframes slideInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 顶栏 -->
        <div class="top-bar">
            <div class="brand-area">
                <div class="brand-title">任务所·Flow</div>
                <div class="brand-slogan">用对话，开工；用流程，收工</div>
            </div>
            <div class="top-actions">
                <button class="icon-button" title="设置">⚙️</button>
                <button class="icon-button" title="通知" id="notificationBtn">🔔</button>
                <button class="icon-button" title="用户">👤</button>
            </div>
        </div>
        
        <!-- Sticky导航 -->
        <div class="sticky-nav">
            <div class="nav-tabs">
                <button class="nav-tab active" data-tab="overview">📊 总览</button>
                <button class="nav-tab" data-tab="events">📊 事件流</button>
                <button class="nav-tab" data-tab="conversations">💬 对话</button>
                <button class="nav-tab" data-tab="memories">💡 记忆</button>
                <button class="nav-tab" data-tab="tasks">📋 任务</button>
            </div>
        </div>
        
        <!-- 主内容区 -->
        <div class="main-content">
            <!-- 系统脉搏区 -->
            <div class="system-pulse">
                <div class="section-title">
                    <span>🎯</span>
                    <span>系统脉搏 (System Pulse)</span>
                    <span style="margin-left: auto; font-size: 11px; color: var(--gray-500);">4秒心跳动画</span>
                </div>
                <div class="pulse-grid">
                    <div class="pulse-card">
                        <div class="pulse-icon">💓</div>
                        <div class="pulse-label">总览</div>
                        <div class="pulse-value" id="totalTasks">57</div>
                        <div class="pulse-trend up">↑ +3 今天</div>
                        <div class="pulse-meta">29完成</div>
                        <div class="pulse-action">
                            <a href="#" class="link-button">详情 →</a>
                        </div>
                    </div>
                    
                    <div class="pulse-card">
                        <div class="pulse-icon">📊</div>
                        <div class="pulse-label">事件流</div>
                        <div class="pulse-value" id="totalEvents">156</div>
                        <div class="pulse-trend up">↑ +12 今天</div>
                        <div class="pulse-meta">⚠️ 8警告</div>
                        <div class="pulse-action">
                            <a href="/events" class="link-button">查看 →</a>
                        </div>
                    </div>
                    
                    <div class="pulse-card">
                        <div class="pulse-icon">💬</div>
                        <div class="pulse-label">对话</div>
                        <div class="pulse-value" id="totalSessions">5</div>
                        <div class="pulse-trend">→ 0 今天</div>
                        <div class="pulse-meta">2活跃</div>
                        <div class="pulse-action">
                            <a href="#" class="link-button">查看 →</a>
                        </div>
                    </div>
                    
                    <div class="pulse-card">
                        <div class="pulse-icon">🔢</div>
                        <div class="pulse-label">Token</div>
                        <div class="pulse-value" style="font-size: 36px;" id="tokenRemaining">850K</div>
                        <div class="pulse-trend down">↓ -25K</div>
                        <div class="pulse-meta">85% 剩余</div>
                        <div class="pulse-action">
                            <a href="#" class="link-button">详情 →</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 实时脉动区 -->
            <div class="live-pulse">
                <div class="section-title">
                    <span>⚡</span>
                    <span>实时脉动 (Live Pulse)</span>
                    <span style="margin-left: auto; font-size: 11px; color: var(--gray-500);">每30秒自动刷新</span>
                </div>
                <div class="event-list" id="recentEventsList">
                    <div class="event-item">
                        <div class="event-dot"></div>
                        <div class="event-content">
                            <div class="event-header">
                                <span class="event-time">2分钟前</span>
                                <span>|</span>
                                <span class="event-type">任务完成</span>
                            </div>
                            <div class="event-title">REQ-010-E 事件系统测试</div>
                            <div class="event-meta">👤 李明 | 📋 任务</div>
                        </div>
                        <button class="action-button">详情</button>
                    </div>
                    
                    <div class="event-item warning">
                        <div class="event-dot warning"></div>
                        <div class="event-content">
                            <div class="event-header">
                                <span class="event-time">15分钟前</span>
                                <span>|</span>
                                <span class="event-type">任务阻塞</span>
                            </div>
                            <div class="event-title">INTEGRATE-003 等待依赖</div>
                            <div class="event-meta">👤 System | 📋 任务</div>
                        </div>
                        <button class="action-button">详情</button>
                    </div>
                    
                    <div class="event-item">
                        <div class="event-dot"></div>
                        <div class="event-content">
                            <div class="event-header">
                                <span class="event-time">1小时前</span>
                                <span>|</span>
                                <span class="event-type">决策记录</span>
                            </div>
                            <div class="event-title">采用事件驱动架构</div>
                            <div class="event-meta">👤 架构师 | 🏛️ 决策</div>
                        </div>
                        <button class="action-button">详情</button>
                    </div>
                </div>
                <div style="text-align: center; margin-top: var(--space-6);">
                    <a href="/events" class="link-button">查看完整事件流 →</a>
                </div>
            </div>
            
            <!-- 双栏: 记忆空间 + 对话历史 -->
            <div class="two-column">
                <div class="column-card">
                    <div class="section-title">
                        <span>💡</span>
                        <span>记忆空间</span>
                    </div>
                    <div class="card-stats">
                        <div class="stat-item">
                            <div class="stat-item-label">📚 总记忆</div>
                            <div class="stat-item-value" id="totalMemories">45</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-item-label">🏛️ 决策</div>
                            <div class="stat-item-value">12</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-item-label">🔧 方案</div>
                            <div class="stat-item-value">23</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-item-label">⭐ 重要</div>
                            <div class="stat-item-value">8</div>
                        </div>
                    </div>
                    <div class="section-title" style="margin-top: var(--space-6); margin-bottom: var(--space-4); font-size: 12px;">
                        最新记忆
                    </div>
                    <div class="recent-list">
                        <div class="recent-item">ADR: 采用Monorepo</div>
                        <div class="recent-item">方案: 解决Tab切换bug</div>
                        <div class="recent-item">知识: React Hooks最佳实践</div>
                    </div>
                    <div style="text-align: center;">
                        <a href="/memories" class="link-button">进入记忆空间 →</a>
                    </div>
                </div>
                
                <div class="column-card">
                    <div class="section-title">
                        <span>💬</span>
                        <span>最近对话</span>
                    </div>
                    <div class="card-stats">
                        <div class="stat-item">
                            <div class="stat-item-label">📝 活跃会话</div>
                            <div class="stat-item-value" id="activeSessions">2</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-item-label">💬 总消息</div>
                            <div class="stat-item-value">156</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-item-label">🔢 Token</div>
                            <div class="stat-item-value">125K</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-item-label">⏱️ 最后</div>
                            <div class="stat-item-value" style="font-size: 16px;">2h前</div>
                        </div>
                    </div>
                    <div class="section-title" style="margin-top: var(--space-6); margin-bottom: var(--space-4); font-size: 12px;">
                        最新会话
                    </div>
                    <div class="recent-list">
                        <div class="recent-item">Dashboard重构讨论</div>
                        <div class="recent-item">API集成讨论</div>
                    </div>
                    <div style="text-align: center;">
                        <a href="#" class="link-button">查看所有对话 →</a>
                    </div>
                </div>
            </div>
            
            <!-- 任务态势 -->
            <div class="task-landscape">
                <div class="section-title">
                    <span>📋</span>
                    <span>任务态势 (Task Landscape)</span>
                </div>
                <div class="status-flow">
                    <div class="status-node">
                        <div class="status-node-label">待处理</div>
                        <div class="status-node-count" id="pendingCount">24</div>
                    </div>
                    <div class="status-node">
                        <div class="status-node-label">进行中</div>
                        <div class="status-node-count" id="inProgressCount">1</div>
                    </div>
                    <div class="status-node">
                        <div class="status-node-label">已完成</div>
                        <div class="status-node-count" id="completedCount">29</div>
                    </div>
                    <div class="status-node">
                        <div class="status-node-label">已取消</div>
                        <div class="status-node-count" id="cancelledCount">4</div>
                    </div>
                </div>
                <div id="taskListPreview">
                    <div class="task-card">
                        <div class="task-info">
                            <div class="task-title">🔴 P0 | INTEGRATE-003 | Token同步集成</div>
                            <div class="task-meta">👤 李明 | ⏱️ 2.0h</div>
                        </div>
                        <div class="task-actions">
                            <button class="action-button">复制提示词</button>
                            <button class="action-button">查看事件</button>
                            <button class="action-button">查看对话</button>
                        </div>
                    </div>
                    
                    <div class="task-card" style="border-left-color: var(--warning);">
                        <div class="task-info">
                            <div class="task-title">🟡 P1 | REQ-005 | Dashboard重构升级</div>
                            <div class="task-meta">👤 待分配 | ⏱️ 16.0h</div>
                        </div>
                        <div class="task-actions">
                            <button class="action-button">复制提示词</button>
                            <button class="action-button">查看事件</button>
                            <button class="action-button">分配任务</button>
                        </div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: var(--space-6);">
                    <a href="#" class="link-button">查看完整任务看板 →</a>
                </div>
            </div>
            
            <!-- 系统健康 -->
            <div class="system-health">
                <div class="health-indicator"></div>
                <div class="health-text">🔌 API服务运行正常</div>
                <div class="health-details">端口: 8800 | 8个端点可用</div>
                <a href="http://localhost:8800/api/docs" class="link-button" target="_blank">查看详情 →</a>
            </div>
        </div>
    </div>
    
    <script>
        // ===== 初始化 =====
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('🎯 指挥舱Dashboard已加载');
            
            // 加载统计数据
            loadStats();
            
            // 加载事件流
            loadRecentEvents();
            
            // 加载任务列表
            loadTasks();
            
            // 启动自动刷新（每30秒）
            setInterval(loadRecentEvents, 30000);
            
            // 设置Tab切换
            setupTabNavigation();
        }});
        
        // ===== Tab导航 =====
        function setupTabNavigation() {{
            const tabs = document.querySelectorAll('.nav-tab');
            tabs.forEach(tab => {{
                tab.addEventListener('click', function() {{
                    // 移除所有active
                    tabs.forEach(t => t.classList.remove('active'));
                    // 添加当前active
                    this.classList.add('active');
                    
                    const tabName = this.dataset.tab;
                    console.log('切换到Tab:', tabName);
                    
                    // 根据tab跳转
                    switch(tabName) {{
                        case 'overview':
                            // 当前页面
                            break;
                        case 'events':
                            window.location.href = '/events';
                            break;
                        case 'conversations':
                            window.location.href = '/conversations';
                            break;
                        case 'memories':
                            window.location.href = '/memories';
                            break;
                        case 'tasks':
                            showToast('任务看板功能开发中...');
                            break;
                    }}
                }});
            }});
        }}
        
        // ===== 加载统计数据 =====
        async function loadStats() {{
            try {{
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                // 更新任务统计
                document.getElementById('totalTasks').textContent = data.total || 0;
                document.getElementById('pendingCount').textContent = data.pending || 0;
                document.getElementById('inProgressCount').textContent = data.in_progress || 0;
                document.getElementById('completedCount').textContent = data.completed || 0;
                document.getElementById('cancelledCount').textContent = data.cancelled || 0;
                
                console.log('✅ 统计数据已加载', data);
            }} catch (error) {{
                console.error('❌ 加载统计数据失败:', error);
            }}
        }}
        
        // ===== 加载最近事件 =====
        async function loadRecentEvents() {{
            try {{
                const response = await fetch('/api/events/recent?hours=24&limit=5');
                const data = await response.json();
                
                if (data.success && data.events && data.events.length > 0) {{
                    const eventList = document.getElementById('recentEventsList');
                    eventList.innerHTML = '';
                    
                    data.events.slice(0, 5).forEach(event => {{
                        const severityClass = event.severity || 'info';
                        const eventItem = document.createElement('div');
                        eventItem.className = `event-item ${{severityClass}}`;
                        eventItem.innerHTML = `
                            <div class="event-dot ${{severityClass}}"></div>
                            <div class="event-content">
                                <div class="event-header">
                                    <span class="event-time">${{formatTime(event.occurred_at || event.timestamp)}}</span>
                                    <span>|</span>
                                    <span class="event-type">${{event.event_type || event.type}}</span>
                                </div>
                                <div class="event-title">${{event.title}}</div>
                                <div class="event-meta">👤 ${{event.actor || 'System'}} | 📋 ${{event.event_category || event.category}}</div>
                            </div>
                            <button class="action-button" onclick="viewEventDetail('${{event.id}}')">详情</button>
                        `;
                        eventList.appendChild(eventItem);
                    }});
                    
                    // 更新事件统计
                    document.getElementById('totalEvents').textContent = data.count || 0;
                    
                    console.log('✅ 最近事件已加载', data.events.length);
                }} else {{
                    console.log('暂无最近事件');
                }}
            }} catch (error) {{
                console.error('❌ 加载事件失败:', error);
            }}
        }}
        
        // ===== 加载任务列表 =====
        async function loadTasks() {{
            try {{
                const response = await fetch('/api/tasks');
                const tasks = await response.json();
                
                if (tasks && tasks.length > 0) {{
                    // 筛选待处理和进行中的任务
                    const activeTasks = tasks.filter(t => t.status === 'pending' || t.status === 'in_progress');
                    
                    const taskList = document.getElementById('taskListPreview');
                    taskList.innerHTML = '';
                    
                    activeTasks.slice(0, 2).forEach(task => {{
                        const priorityEmoji = task.priority === 'P0' ? '🔴' : task.priority === 'P1' ? '🟡' : '⚪';
                        const taskCard = document.createElement('div');
                        taskCard.className = 'task-card';
                        taskCard.style.borderLeftColor = task.priority === 'P0' ? 'var(--error)' : 'var(--warning)';
                        taskCard.innerHTML = `
                            <div class="task-info">
                                <div class="task-title">${{priorityEmoji}} ${{task.priority}} | ${{task.id}} | ${{task.title}}</div>
                                <div class="task-meta">👤 ${{task.assigned_to || '待分配'}} | ⏱️ ${{task.estimated_hours || 0}}h</div>
                            </div>
                            <div class="task-actions">
                                <button class="action-button">复制提示词</button>
                                <button class="action-button">查看事件</button>
                                <button class="action-button">${{task.assigned_to ? '查看对话' : '分配任务'}}</button>
                            </div>
                        `;
                        taskList.appendChild(taskCard);
                    }});
                    
                    console.log('✅ 任务列表已加载', tasks.length);
                }}
            }} catch (error) {{
                console.error('❌ 加载任务失败:', error);
            }}
        }}
        
        // ===== 工具函数 =====
        function formatTime(timestamp) {{
            if (!timestamp) return '刚刚';
            
            const now = new Date();
            const time = new Date(timestamp);
            const diffMs = now - time;
            const diffMins = Math.floor(diffMs / 60000);
            
            if (diffMins < 1) return '刚刚';
            if (diffMins < 60) return `${{diffMins}}分钟前`;
            if (diffMins < 1440) return `${{Math.floor(diffMins/60)}}小时前`;
            return time.toLocaleString('zh-CN');
        }}
        
        function showToast(message) {{
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.textContent = message;
            document.body.appendChild(toast);
            
            setTimeout(() => {{
                toast.remove();
            }}, 3000);
        }}
        
        function viewEventDetail(eventId) {{
            showToast('事件详情功能开发中...');
            console.log('查看事件:', eventId);
        }}
        
        // ===== 通知按钮 =====
        document.getElementById('notificationBtn').addEventListener('click', function() {{
            showToast('暂无新通知');
        }});
    </script>
</body>
</html>
"""

