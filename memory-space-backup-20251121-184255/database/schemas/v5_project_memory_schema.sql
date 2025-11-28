-- ============================================================================
-- 任务所·Flow v1.9 - 项目记忆空间Schema
-- ============================================================================
-- 创建时间: 2025-11-21
-- 说明: 项目记忆空间专属表，集成Session Memory MCP和Ultra Memory MCP
-- 功能: 
--   1. 项目记忆存储（决策/方案/重要记忆）
--   2. 记忆关系图谱
--   3. 记忆统计和检索
--   4. MCP双向同步
-- ============================================================================

-- ============================================================================
-- 1. 项目记忆主表
-- ============================================================================
CREATE TABLE IF NOT EXISTS project_memories (
    id TEXT PRIMARY KEY,                           -- MEM-xxxxxxxx
    project_id TEXT NOT NULL,                      -- 项目代码: TASKFLOW
    
    -- 记忆类型和分类
    memory_type TEXT NOT NULL,                     -- session/ultra/decision/solution/knowledge
    category TEXT NOT NULL,                        -- architecture/problem/solution/decision/knowledge
    
    -- 外部MCP记忆ID（用于同步）
    external_memory_id TEXT,                       -- MCP返回的外部记忆ID
    mcp_source TEXT,                               -- session/ultra，标识来自哪个MCP
    
    -- 记忆内容
    title TEXT NOT NULL,                           -- 标题
    content TEXT NOT NULL,                         -- 内容
    
    -- 上下文和元数据
    context TEXT,                                  -- 上下文信息（JSON格式）
    tags TEXT,                                     -- 标签列表（JSON数组）
    
    -- 关联实体
    related_tasks TEXT,                            -- 关联任务ID列表（JSON数组）
    related_issues TEXT,                           -- 关联问题ID列表（JSON数组）
    
    -- 重要性和质量
    importance INTEGER DEFAULT 5,                  -- 重要性 1-10
    confidence_score REAL DEFAULT 1.0,             -- 置信度 0.0-1.0
    
    -- 使用统计
    access_count INTEGER DEFAULT 0,                -- 访问次数
    reference_count INTEGER DEFAULT 0,             -- 被引用次数
    last_accessed_at TEXT,                         -- 最后访问时间
    
    -- 创建和更新信息
    created_by TEXT DEFAULT 'system',              -- 创建者
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    -- 外键约束
    FOREIGN KEY (project_id) REFERENCES projects(code)
);

-- ============================================================================
-- 2. 记忆关系表 - 构建知识图谱
-- ============================================================================
CREATE TABLE IF NOT EXISTS memory_relations (
    id TEXT PRIMARY KEY,                           -- REL-xxxxxxxx
    source_memory_id TEXT NOT NULL,                -- 源记忆ID
    target_memory_id TEXT NOT NULL,                -- 目标记忆ID
    
    -- 关系类型
    relation_type TEXT NOT NULL,                   -- related/caused-by/solved-by/evolved-from/depends-on
    
    -- 关系属性
    strength REAL DEFAULT 1.0,                     -- 关系强度 0.0-1.0
    bidirectional INTEGER DEFAULT 0,               -- 是否双向关系
    
    -- 关系描述
    description TEXT,                              -- 关系描述
    
    -- 元数据
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    created_by TEXT DEFAULT 'system',
    
    -- 外键约束
    FOREIGN KEY (source_memory_id) REFERENCES project_memories(id) ON DELETE CASCADE,
    FOREIGN KEY (target_memory_id) REFERENCES project_memories(id) ON DELETE CASCADE,
    
    -- 唯一约束：同一对记忆间同一类型关系只能有一个
    UNIQUE(source_memory_id, target_memory_id, relation_type)
);

-- ============================================================================
-- 3. 记忆检索历史表 - 优化推荐算法
-- ============================================================================
CREATE TABLE IF NOT EXISTS memory_retrieval_history (
    id TEXT PRIMARY KEY,                           -- RET-xxxxxxxx
    project_id TEXT NOT NULL,                      -- 项目代码
    
    -- 检索信息
    query_text TEXT,                               -- 查询文本
    query_type TEXT,                               -- semantic/keyword/filter
    
    -- 检索参数
    filters TEXT,                                  -- 过滤条件（JSON格式）
    
    -- 检索结果
    memory_ids TEXT,                               -- 返回的记忆ID列表（JSON数组）
    result_count INTEGER DEFAULT 0,                -- 结果数量
    
    -- 用户反馈
    clicked_memory_id TEXT,                        -- 用户点击的记忆ID
    feedback_score INTEGER,                        -- 反馈评分 1-5
    
    -- 时间戳
    retrieved_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    -- 外键约束
    FOREIGN KEY (project_id) REFERENCES projects(code)
);

-- ============================================================================
-- 4. 项目记忆统计表
-- ============================================================================
CREATE TABLE IF NOT EXISTS project_memory_stats (
    project_id TEXT PRIMARY KEY,                   -- 项目代码
    
    -- 总体统计
    total_memories INTEGER DEFAULT 0,              -- 总记忆数
    session_memories INTEGER DEFAULT 0,            -- 会话记忆数
    ultra_memories INTEGER DEFAULT 0,              -- 长期记忆数
    decision_memories INTEGER DEFAULT 0,           -- 决策记忆数
    solution_memories INTEGER DEFAULT 0,           -- 方案记忆数
    
    -- 按分类统计
    architecture_count INTEGER DEFAULT 0,          -- 架构类
    problem_count INTEGER DEFAULT 0,               -- 问题类
    solution_count INTEGER DEFAULT 0,              -- 解决方案类
    decision_count INTEGER DEFAULT 0,              -- 决策类
    knowledge_count INTEGER DEFAULT 0,             -- 知识类
    
    -- 活跃度统计
    total_accesses INTEGER DEFAULT 0,              -- 总访问次数
    avg_importance REAL DEFAULT 5.0,               -- 平均重要性
    
    -- 时间信息
    last_memory_created_at TEXT,                   -- 最后记忆创建时间
    last_updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    
    -- 外键约束
    FOREIGN KEY (project_id) REFERENCES projects(code)
);

-- ============================================================================
-- 索引优化
-- ============================================================================

-- project_memories表索引
CREATE INDEX IF NOT EXISTS idx_project_memories_project ON project_memories(project_id);
CREATE INDEX IF NOT EXISTS idx_project_memories_type ON project_memories(memory_type);
CREATE INDEX IF NOT EXISTS idx_project_memories_category ON project_memories(category);
CREATE INDEX IF NOT EXISTS idx_project_memories_importance ON project_memories(importance DESC);
CREATE INDEX IF NOT EXISTS idx_project_memories_created ON project_memories(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_project_memories_external ON project_memories(external_memory_id);
CREATE INDEX IF NOT EXISTS idx_project_memories_mcp_source ON project_memories(mcp_source);

-- memory_relations表索引
CREATE INDEX IF NOT EXISTS idx_memory_relations_source ON memory_relations(source_memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_relations_target ON memory_relations(target_memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_relations_type ON memory_relations(relation_type);

-- memory_retrieval_history表索引
CREATE INDEX IF NOT EXISTS idx_memory_retrieval_project ON memory_retrieval_history(project_id);
CREATE INDEX IF NOT EXISTS idx_memory_retrieval_time ON memory_retrieval_history(retrieved_at DESC);

-- ============================================================================
-- 初始化TASKFLOW项目统计数据
-- ============================================================================
INSERT OR IGNORE INTO project_memory_stats (project_id, total_memories) VALUES ('TASKFLOW', 0);

-- ============================================================================
-- 视图：记忆全景视图
-- ============================================================================
CREATE VIEW IF NOT EXISTS v_memory_full_view AS
SELECT 
    m.id,
    m.project_id,
    m.memory_type,
    m.category,
    m.title,
    m.content,
    m.importance,
    m.tags,
    m.access_count,
    m.reference_count,
    m.created_at,
    m.updated_at,
    m.created_by,
    -- 统计关联关系数量
    (SELECT COUNT(*) FROM memory_relations WHERE source_memory_id = m.id) as outgoing_relations,
    (SELECT COUNT(*) FROM memory_relations WHERE target_memory_id = m.id) as incoming_relations
FROM project_memories m;

-- ============================================================================
-- 说明
-- ============================================================================
-- 
-- 【新增表】
-- 1. project_memories: 项目记忆主表，存储所有记忆内容
-- 2. memory_relations: 记忆关系表，构建知识图谱
-- 3. memory_retrieval_history: 检索历史，优化推荐
-- 4. project_memory_stats: 统计表，快速获取项目记忆概览
-- 
-- 【MCP集成】
-- - external_memory_id: 存储MCP返回的外部记忆ID
-- - mcp_source: 标识记忆来自session-memory-mcp或ultra-memory-mcp
-- - 支持双向同步：本地→MCP，MCP→本地
-- 
-- 【关系类型】
-- - related: 相关（通用关联）
-- - caused-by: 问题由某个决策/变更引起
-- - solved-by: 问题由某个方案解决
-- - evolved-from: 知识由另一知识演化而来
-- - depends-on: 依赖关系
-- 
-- 【使用场景】
-- 1. 架构师记录架构决策 → decision_memories
-- 2. 自动记录问题解决方案 → solution_memories
-- 3. 跨会话知识继承 → 检索historical memories
-- 4. 知识图谱导航 → memory_relations
-- 
-- ============================================================================

