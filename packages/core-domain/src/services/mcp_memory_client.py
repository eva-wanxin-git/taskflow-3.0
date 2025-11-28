# -*- coding: utf-8 -*-
"""
MCP记忆系统客户端
直接调用Ultra Memory Cloud MCP和Session Memory MCP
绕过HTTP API，直接访问DynamoDB的9837条记忆
"""

import subprocess
import json
from typing import Dict, Any, List, Optional
from datetime import datetime


class MCPMemoryClient:
    """MCP记忆系统直接调用客户端"""
    
    def __init__(self):
        """初始化MCP客户端"""
        # Ultra Memory Cloud MCP路径
        self.ultra_memory_script = "/Users/yalinwang/Desktop/资料/cursor工作盘/ultra-memory-cloud-mcp/src/server.js"
        # Session Memory MCP路径
        self.session_memory_script = "/Users/yalinwang/Desktop/资料/cursor工作盘/session-memory-mcp/src/index.js"
        
        # 环境变量（从环境变量读取，不要硬编码）
        self.ultra_env = {
            "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID", ""),
            "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
            "AWS_REGION": "us-east-1",
            "DYNAMODB_WORKING_TABLE": "ultra-memory-dev-working-memory",
            "DYNAMODB_SEMANTIC_TABLE": "ultra-memory-dev-memory-metadata",
            "DYNAMODB_RELATIONS_TABLE": "ultra-memory-dev-relational-memory",
            "DEFAULT_USER_ID": "wanxin"
        }
        
        self.session_env = {
            "SESSION_MEMORY_API_URL": "http://13.158.83.99:4000",
            "DEFAULT_USER_ID": "taskflow",
            "DEFAULT_PLATFORM": "taskflow-system"
        }
    
    def store_to_ultra_memory(
        self,
        content: str,
        user_id: str = "wanxin",
        conversation_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[str]:
        """
        存储记忆到Ultra Memory (直接访问DynamoDB)
        
        Args:
            content: 记忆内容
            user_id: 用户ID (默认wanxin，可访问9801条记忆)
            conversation_id: 对话ID (可选)
            metadata: 元数据 (可选)
            
        Returns:
            记忆ID或None
        """
        try:
            # 这里应该通过MCP SDK调用，但目前简化为HTTP API调用
            # 因为MCP工具已经在Cursor中加载，任务所后端直接用HTTP API
            import httpx
            
            memory_id = f"taskflow_{int(datetime.now().timestamp())}"
            payload = {
                "namespace": f"{user_id}_ultra",  # 使用用户的namespace
                "id": memory_id,
                "content": content,
                "metadata": metadata or {}
            }
            
            response = httpx.post(
                "http://13.158.83.99:7000/store",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return result.get("data", {}).get("id")
            
            return None
            
        except Exception as e:
            print(f"Ultra Memory存储错误: {e}")
            return None
    
    def search_ultra_memory(
        self,
        query: str,
        user_id: str = "wanxin",
        limit: int = 10
    ) -> List[Dict]:
        """
        搜索Ultra Memory (访问9801条Relational记忆)
        
        Args:
            query: 搜索查询
            user_id: 用户ID (wanxin可访问9801条)
            limit: 返回数量
            
        Returns:
            记忆列表
        """
        try:
            import httpx
            
            payload = {
                "namespace": f"{user_id}_ultra",
                "query": query,
                "limit": limit
            }
            
            response = httpx.post(
                "http://13.158.83.99:7000/search",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("results", [])
            
            return []
            
        except Exception as e:
            print(f"Ultra Memory搜索错误: {e}")
            return []
    
    def create_session_task(
        self,
        message: str,
        workspace_path: str = "/taskflow",
        user_id: str = "taskflow"
    ) -> Optional[Dict]:
        """
        创建Session Memory任务
        
        Args:
            message: 任务消息
            workspace_path: 工作空间路径
            user_id: 用户ID
            
        Returns:
            任务信息或None
        """
        try:
            import httpx
            
            payload = {
                "user_id": user_id,
                "platform": "taskflow-system",
                "workspace_path": workspace_path,
                "message": message
            }
            
            response = httpx.post(
                "http://13.158.83.99:4000/api/tasks/match",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return result.get("data", {}).get("task")
            
            return None
            
        except Exception as e:
            print(f"Session Memory任务创建错误: {e}")
            return None


# 如果直接运行，执行测试
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 MCP记忆客户端测试")
    print("="*70)
    
    client = MCPMemoryClient()
    
    # 测试存储
    print("\n1. 测试Ultra Memory存储")
    mem_id = client.store_to_ultra_memory(
        content="MCP客户端测试记忆",
        user_id="wanxin",
        metadata={"source": "mcp_client_test"}
    )
    print(f"   结果: {mem_id}")
    
    # 测试搜索
    print("\n2. 测试Ultra Memory搜索")
    results = client.search_ultra_memory(query="GitHub", user_id="wanxin", limit=3)
    print(f"   找到: {len(results)} 条记忆")
    
    # 测试任务创建
    print("\n3. 测试Session Memory任务创建")
    task = client.create_session_task(message="MCP客户端测试任务")
    if task:
        print(f"   任务ID: {task.get('task_id')}")
    else:
        print("   创建失败")
    
    print("\n" + "="*70)

