# -*- coding: utf-8 -*-
"""
项目记忆空间数据提供器

为Dashboard提供项目记忆数据
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import requests

# API基础URL
API_BASE_URL = "http://localhost:8800/api"


class ProjectMemoryProvider:
    """项目记忆空间数据提供器"""
    
    def __init__(self, project_code: str = "TASKFLOW", api_base_url: str = API_BASE_URL):
        """
        初始化记忆空间提供器
        
        Args:
            project_code: 项目代码
            api_base_url: API基础URL
        """
        self.project_code = project_code
        self.api_base_url = api_base_url
        self.timeout = 5  # 请求超时时间（秒）
    
    def get_memories(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        memory_type: Optional[str] = None,
        tags: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        获取记忆列表
        
        Args:
            query: 查询文本（语义搜索）
            category: 分类过滤 (architecture/problem/solution/decision/knowledge)
            memory_type: 类型过滤 (session/ultra/decision/solution)
            tags: 标签过滤（逗号分隔）
            limit: 返回数量限制
        
        Returns:
            记忆列表
        """
        try:
            url = f"{self.api_base_url}/projects/{self.project_code}/memories"
            params = {}
            
            if query:
                params['query'] = query
            if category:
                params['category'] = category
            if memory_type:
                params['memory_type'] = memory_type
            if tags:
                params['tags'] = tags
            params['limit'] = limit
            
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('memories', [])
            else:
                print(f"[记忆空间] API错误: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"[记忆空间] 请求失败: {e}")
            return []
        except Exception as e:
            print(f"[记忆空间] 未知错误: {e}")
            return []
    
    def get_memory_detail(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        获取记忆详情
        
        Args:
            memory_id: 记忆ID
        
        Returns:
            记忆详情字典或None
        """
        try:
            url = f"{self.api_base_url}/projects/{self.project_code}/memories/{memory_id}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('memory')
            else:
                return None
        except Exception as e:
            print(f"[记忆空间] 获取详情失败: {e}")
            return None
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        获取记忆统计
        
        Returns:
            统计数据字典
        """
        try:
            url = f"{self.api_base_url}/projects/{self.project_code}/memories/stats"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('stats', {})
            else:
                return self._get_default_stats()
        except Exception as e:
            print(f"[记忆空间] 获取统计失败: {e}")
            return self._get_default_stats()
    
    def _get_default_stats(self) -> Dict[str, Any]:
        """返回默认统计数据"""
        return {
            "total_memories": 0,
            "session_memories": 0,
            "ultra_memories": 0,
            "decision_memories": 0,
            "solution_memories": 0,
            "by_category": {
                "architecture": 0,
                "problem": 0,
                "solution": 0,
                "decision": 0,
                "knowledge": 0
            },
            "by_importance": {
                "critical (9-10)": 0,
                "high (7-8)": 0,
                "medium (5-6)": 0,
                "low (1-4)": 0
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def get_related_memories(
        self,
        memory_id: str,
        relation_types: Optional[str] = None,
        min_strength: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        获取相关记忆
        
        Args:
            memory_id: 记忆ID
            relation_types: 关系类型过滤（逗号分隔）
            min_strength: 最小关系强度
        
        Returns:
            相关记忆列表
        """
        try:
            url = f"{self.api_base_url}/projects/{self.project_code}/memories/{memory_id}/related"
            params = {
                'min_strength': min_strength
            }
            if relation_types:
                params['relation_types'] = relation_types
            
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('related_memories', [])
            else:
                return []
        except Exception as e:
            print(f"[记忆空间] 获取相关记忆失败: {e}")
            return []
    
    def inherit_knowledge(
        self,
        context: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        跨会话知识继承
        
        Args:
            context: 当前上下文
            limit: 返回记忆数量
        
        Returns:
            知识包字典
        """
        try:
            url = f"{self.api_base_url}/projects/{self.project_code}/knowledge/inherit"
            params = {'limit': limit}
            if context:
                params['context'] = context
            
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "architecture_decisions": [],
                    "problem_solutions": [],
                    "important_knowledge": [],
                    "recent_memories": []
                }
        except Exception as e:
            print(f"[记忆空间] 知识继承失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_categories_summary(self) -> Dict[str, int]:
        """
        获取各分类记忆数量汇总
        
        Returns:
            {category: count}字典
        """
        stats = self.get_memory_stats()
        return stats.get("by_category", {})
    
    def get_importance_summary(self) -> Dict[str, int]:
        """
        获取各重要性级别记忆数量汇总
        
        Returns:
            {importance_level: count}字典
        """
        stats = self.get_memory_stats()
        return stats.get("by_importance", {})
    
    def search_memories(
        self,
        keyword: str,
        limit: int = 30
    ) -> List[Dict[str, Any]]:
        """
        搜索记忆（语义搜索）
        
        Args:
            keyword: 搜索关键词
            limit: 返回数量限制
        
        Returns:
            匹配的记忆列表
        """
        return self.get_memories(query=keyword, limit=limit)


if __name__ == "__main__":
    # 测试代码
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("===== ProjectMemoryProvider Test =====\n")
    
    provider = ProjectMemoryProvider()
    
    # 测试获取记忆
    memories = provider.get_memories(limit=5)
    print(f"Recent memories: {len(memories)}")
    
    if memories:
        print("\nFirst memory:")
        first = memories[0]
        print(f"  - ID: {first.get('id')}")
        print(f"  - Title: {first.get('title')}")
        print(f"  - Category: {first.get('category')}")
        print(f"  - Type: {first.get('memory_type')}")
    
    # 测试统计
    stats = provider.get_memory_stats()
    print(f"\nTotal memories: {stats.get('total_memories', 0)}")
    
    # 测试分类汇总
    categories = provider.get_categories_summary()
    print(f"\nCategories:")
    for cat, count in categories.items():
        print(f"  - {cat}: {count}")
    
    print("\n✅ Test completed!")

