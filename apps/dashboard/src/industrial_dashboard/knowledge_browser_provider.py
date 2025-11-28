# -*- coding: utf-8 -*-
"""
项目知识库浏览器数据提供器

为Dashboard提供知识库文件树和文档内容
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import json


class KnowledgeBrowserProvider:
    """项目知识库浏览器数据提供器"""
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        初始化知识库提供器
        
        Args:
            project_root: 项目根目录路径
        """
        if project_root is None:
            # 默认使用当前文件向上6级目录
            self.project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.docs_dir = self.project_root / "docs"
        self.knowledge_dir = self.project_root / "knowledge"
        self.database_dir = self.project_root / "database"
    
    def get_file_tree(self) -> Dict[str, Any]:
        """
        获取完整的文件树结构
        
        Returns:
            文件树字典
        """
        tree = {
            "name": "TASKFLOW知识库",
            "type": "root",
            "children": []
        }
        
        # 1. docs目录
        if self.docs_dir.exists():
            docs_node = self._build_tree_node(self.docs_dir, "📋 项目文档")
            tree["children"].append(docs_node)
        
        # 2. knowledge目录
        if self.knowledge_dir.exists():
            knowledge_node = self._build_tree_node(self.knowledge_dir, "🔧 知识库")
            # 确保UX和UI文件夹存在
            self._ensure_ux_ui_folders()
            tree["children"].append(knowledge_node)
        
        # 3. database/schemas目录
        schemas_dir = self.database_dir / "schemas"
        if schemas_dir.exists():
            db_node = {
                "type": "folder",
                "name": "database",
                "label": "🗄️ 数据库",
                "children": [self._build_tree_node(schemas_dir, "Schema文档")]
            }
            tree["children"].append(db_node)
        
        return tree
    
    def _build_tree_node(self, path: Path, label: Optional[str] = None) -> Dict[str, Any]:
        """
        递归构建树节点
        
        Args:
            path: 文件或目录路径
            label: 显示标签
        
        Returns:
            树节点字典
        """
        if not path.exists():
            return None
        
        node = {
            "name": path.name,
            "label": label or path.name,
            "path": str(path.relative_to(self.project_root))
        }
        
        if path.is_dir():
            node["type"] = "folder"
            node["children"] = []
            
            # 特殊图标
            if path.name == "ux":
                node["icon"] = "🎨"
            elif path.name == "ui":
                node["icon"] = "🎭"
            
            try:
                # 遍历子项
                for child in sorted(path.iterdir()):
                    # 跳过隐藏文件和特殊目录
                    if child.name.startswith('.') or child.name == '__pycache__':
                        continue
                    
                    child_node = self._build_tree_node(child)
                    if child_node:
                        node["children"].append(child_node)
            except PermissionError:
                pass
        else:
            node["type"] = "file"
            node["size"] = self._format_size(path.stat().st_size)
            node["category"] = self._get_category(path)
            
        return node
    
    def _ensure_ux_ui_folders(self):
        """确保UX和UI文件夹存在"""
        ux_dir = self.knowledge_dir / "ux"
        ui_dir = self.knowledge_dir / "ui"
        
        if not ux_dir.exists():
            ux_dir.mkdir(parents=True, exist_ok=True)
            # 创建默认UX文档
            (ux_dir / "ux-principles.md").write_text(
                "# UX设计原则\n\n待完善...",
                encoding='utf-8'
            )
        
        if not ui_dir.exists():
            ui_dir.mkdir(parents=True, exist_ok=True)
            # 创建默认UI文档
            (ui_dir / "ui-standards.md").write_text(
                "# UI设计规范\n\n## 工业美学风格\n\n待完善...",
                encoding='utf-8'
            )
    
    def get_document(self, category: str, filename: str) -> Optional[Dict[str, Any]]:
        """
        获取文档内容
        
        Args:
            category: 文档分类 (ai/arch/features/ux/ui/issues/solutions等)
            filename: 文件名
        
        Returns:
            文档字典或None
        """
        # 查找文件路径
        possible_paths = [
            self.docs_dir / category / filename,
            self.knowledge_dir / category / filename,
            self.database_dir / "schemas" / filename,
        ]
        
        for file_path in possible_paths:
            if file_path.exists() and file_path.is_file():
                return self._read_document(file_path, category)
        
        return None
    
    def _read_document(self, file_path: Path, category: str) -> Dict[str, Any]:
        """读取文档内容"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            return {
                "filename": file_path.name,
                "title": self._extract_title(content) or file_path.stem,
                "content": content,
                "category": category,
                "size": self._format_size(file_path.stat().st_size),
                "updated_at": file_path.stat().st_mtime,
                "path": str(file_path.relative_to(self.project_root))
            }
        except Exception as e:
            print(f"[知识库] 读取文档失败: {e}")
            return None
    
    def _extract_title(self, content: str) -> Optional[str]:
        """从Markdown内容中提取标题"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return None
    
    def _get_category(self, file_path: Path) -> str:
        """获取文件分类"""
        # 根据父目录判断
        parent = file_path.parent.name
        
        category_map = {
            'ai': 'ai',
            'arch': 'arch',
            'features': 'features',
            'adr': 'adr',
            'tasks': 'tasks',
            'ux': 'ux',
            'ui': 'ui',
            'issues': 'issues',
            'solutions': 'solutions',
            'schemas': 'database',
        }
        
        return category_map.get(parent, 'general')
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes}B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f}KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f}MB"
    
    def search_documents(self, keyword: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        搜索文档
        
        Args:
            keyword: 搜索关键词
            limit: 返回数量限制
        
        Returns:
            匹配的文档列表
        """
        results = []
        keyword_lower = keyword.lower()
        
        # 搜索所有目录
        search_dirs = [
            self.docs_dir,
            self.knowledge_dir,
            self.database_dir / "schemas"
        ]
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
            
            for file_path in search_dir.rglob('*.md'):
                try:
                    content = file_path.read_text(encoding='utf-8')
                    title = self._extract_title(content) or file_path.stem
                    
                    if keyword_lower in title.lower() or keyword_lower in content.lower():
                        results.append({
                            "filename": file_path.name,
                            "title": title,
                            "path": str(file_path.relative_to(self.project_root)),
                            "category": self._get_category(file_path),
                            "snippet": self._extract_snippet(content, keyword)
                        })
                        
                        if len(results) >= limit:
                            return results
                except Exception:
                    continue
        
        return results
    
    def _extract_snippet(self, content: str, keyword: str, context_chars: int = 100) -> str:
        """提取包含关键词的片段"""
        keyword_lower = keyword.lower()
        content_lower = content.lower()
        
        pos = content_lower.find(keyword_lower)
        if pos == -1:
            return content[:200] + "..."
        
        start = max(0, pos - context_chars)
        end = min(len(content), pos + len(keyword) + context_chars)
        
        snippet = content[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        
        return snippet


if __name__ == "__main__":
    # 测试代码
    print("===== KnowledgeBrowserProvider Test =====\n")
    
    provider = KnowledgeBrowserProvider()
    
    # 测试获取文件树
    tree = provider.get_file_tree()
    print(f"文件树根节点: {tree['name']}")
    print(f"一级目录数: {len(tree['children'])}")
    
    # 测试搜索
    results = provider.search_documents("架构")
    print(f"\n搜索'架构': {len(results)} 个结果")
    
    if results:
        print(f"第一个结果: {results[0]['title']}")
    
    print("\n✅ Test completed!")

