#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化项目记忆空间 - 在两套MCP中创建TASKFLOW项目记忆空间

功能：
1. 在 session-memory-mcp 中创建项目记忆空间
2. 在 ultra-memory-mcp 中创建项目记忆空间
3. 初始化项目记忆统计数据
4. 测试MCP连接状态
"""

import httpx
import json
from datetime import datetime
from pathlib import Path
import sys

# MCP服务配置
SESSION_MEMORY_URL = "http://13.158.83.99:4000"  # Session Memory API端口
ULTRA_MEMORY_URL = "http://13.158.83.99:7000"     # Ultra Memory HTTP API端口（暂时保留，主要用DynamoDB直连）
PROJECT_CODE = "TASKFLOW"

def test_session_memory_mcp():
    """测试 Session Memory MCP 连接"""
    print("\n" + "="*70)
    print("测试 Session Memory MCP 连接...")
    print("="*70)
    
    try:
        # 测试健康检查端点
        response = httpx.get(f"{SESSION_MEMORY_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Session Memory MCP 连接成功")
            print(f"响应: {response.json()}")
            return True
        else:
            print(f"⚠️ Session Memory MCP 响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Session Memory MCP 连接失败: {e}")
        print("提示: 请确保 session-memory-mcp 服务已启动")
        return False

def test_ultra_memory_mcp():
    """测试 Ultra Memory MCP 连接"""
    print("\n" + "="*70)
    print("测试 Ultra Memory MCP 连接...")
    print("="*70)
    
    try:
        # 测试统计端点
        response = httpx.post(
            f"{ULTRA_MEMORY_URL}/mcp_ultra-memory-cloud_get_memory_stats",
            json={"userId": PROJECT_CODE},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Ultra Memory MCP 连接成功")
            result = response.json()
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"⚠️ Ultra Memory MCP 响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ultra Memory MCP 连接失败: {e}")
        print("提示: 请确保 ultra-memory-mcp 服务已启动")
        return False

def create_session_memory_space():
    """在 Session Memory MCP 中创建项目记忆空间"""
    print("\n" + "="*70)
    print(f"在 Session Memory MCP 中创建项目 {PROJECT_CODE} 记忆空间...")
    print("="*70)
    
    try:
        # 创建初始会话记录
        response = httpx.post(
            f"{SESSION_MEMORY_URL}/api/sessions",
            json={
                "project_id": PROJECT_CODE,
                "session_name": f"{PROJECT_CODE} Main Session",
                "description": f"任务所·Flow v1.9 项目主会话",
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "created_by": "init_script",
                    "purpose": "project_memory_space"
                }
            },
            timeout=10
        )
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print("✅ Session Memory 空间创建成功")
            print(f"会话ID: {result.get('session_id')}")
            return result.get('session_id')
        else:
            print(f"⚠️ 创建失败: {response.status_code}")
            print(f"响应: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Session Memory 空间创建失败: {e}")
        return None

def create_ultra_memory_space():
    """在 Ultra Memory MCP 中创建项目记忆空间"""
    print("\n" + "="*70)
    print(f"在 Ultra Memory MCP 中创建项目 {PROJECT_CODE} 记忆空间...")
    print("="*70)
    
    try:
        # 存储初始记忆（项目概览）
        response = httpx.post(
            f"{ULTRA_MEMORY_URL}/mcp_ultra-memory-cloud_store_memory",
            json={
                "userId": PROJECT_CODE,
                "content": f"任务所·Flow v1.9 - 项目记忆空间已初始化。这是一个AI协作的任务管理系统，支持多角色工作流、记忆空间、实时事件流等功能。",
                "metadata": {
                    "type": "project_init",
                    "created_at": datetime.now().isoformat(),
                    "created_by": "init_script",
                    "importance": 10,
                    "category": "knowledge"
                }
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ultra Memory 空间创建成功")
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"⚠️ 创建失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Ultra Memory 空间创建失败: {e}")
        return False

def init_local_stats():
    """初始化本地数据库统计"""
    print("\n" + "="*70)
    print("初始化本地数据库统计...")
    print("="*70)
    
    try:
        import sqlite3
        db_path = Path(__file__).parent.parent / "database" / "data" / "tasks.db"
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 检查统计记录是否存在
        cursor.execute(
            "SELECT * FROM project_memory_stats WHERE project_id = ?",
            (PROJECT_CODE,)
        )
        existing = cursor.fetchone()
        
        if existing:
            print(f"✅ 项目 {PROJECT_CODE} 统计记录已存在")
            print(f"总记忆数: {existing[1] if len(existing) > 1 else 0}")
        else:
            # 插入初始统计
            cursor.execute(
                """
                INSERT OR IGNORE INTO project_memory_stats (project_id, total_memories)
                VALUES (?, 0)
                """,
                (PROJECT_CODE,)
            )
            conn.commit()
            print(f"✅ 项目 {PROJECT_CODE} 统计记录创建成功")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 本地统计初始化失败: {e}")
        return False

def main():
    """主函数"""
    print("\n" + "="*70)
    print("🚀 任务所·Flow v1.9 - 项目记忆空间初始化")
    print("="*70)
    print(f"项目代码: {PROJECT_CODE}")
    print(f"Session Memory MCP: {SESSION_MEMORY_URL}")
    print(f"Ultra Memory MCP: {ULTRA_MEMORY_URL}")
    print(f"初始化时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "session_mcp_connected": False,
        "ultra_mcp_connected": False,
        "session_space_created": False,
        "ultra_space_created": False,
        "local_stats_initialized": False
    }
    
    # 1. 测试连接
    results["session_mcp_connected"] = test_session_memory_mcp()
    results["ultra_mcp_connected"] = test_ultra_memory_mcp()
    
    # 2. 创建记忆空间（如果MCP可用）
    if results["session_mcp_connected"]:
        session_id = create_session_memory_space()
        results["session_space_created"] = session_id is not None
    
    if results["ultra_mcp_connected"]:
        results["ultra_space_created"] = create_ultra_memory_space()
    
    # 3. 初始化本地统计
    results["local_stats_initialized"] = init_local_stats()
    
    # 4. 生成报告
    print("\n" + "="*70)
    print("📊 初始化结果汇总")
    print("="*70)
    for key, value in results.items():
        status = "✅ 成功" if value else "❌ 失败"
        print(f"{key}: {status}")
    
    # 5. 总结
    all_success = all(results.values())
    if all_success:
        print("\n🎉 所有初始化步骤完成！项目记忆空间已就绪。")
        return 0
    else:
        print("\n⚠️ 部分初始化步骤失败，请检查MCP服务状态。")
        print("\n提示：")
        if not results["session_mcp_connected"]:
            print("  - 启动 session-memory-mcp: cd packages/session-memory-mcp && npm start")
        if not results["ultra_mcp_connected"]:
            print("  - 启动 ultra-memory-mcp: cd packages/ultra-memory-mcp && npm start")
        return 1

if __name__ == "__main__":
    sys.exit(main())

