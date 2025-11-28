#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全局端口管理器
管理8841-8899端口范围，避免冲突
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime
import socket


class PortManager:
    """全局端口管理器"""

    PORT_RANGE_START = 8841
    PORT_RANGE_END = 8899
    REGISTRY_PATH = Path.home() / ".taskflow" / "port_registry.json"

    def __init__(self):
        """初始化端口管理器"""
        self._ensure_registry()

    def _ensure_registry(self):
        """确保注册表文件存在"""
        self.REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not self.REGISTRY_PATH.exists():
            self._save_registry({"projects": {}, "last_updated": datetime.now().isoformat()})

    def _load_registry(self) -> Dict:
        """加载注册表"""
        try:
            with open(self.REGISTRY_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"projects": {}, "last_updated": datetime.now().isoformat()}

    def _save_registry(self, data: Dict):
        """保存注册表"""
        data["last_updated"] = datetime.now().isoformat()
        with open(self.REGISTRY_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def is_port_available(self, port: int) -> bool:
        """检查端口是否可用"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex(('127.0.0.1', port))
                return result != 0  # 0表示端口被占用
        except:
            return False

    def allocate_port(self, project_code: str, project_path: str) -> Optional[int]:
        """为项目分配端口"""
        registry = self._load_registry()
        projects = registry.get("projects", {})

        # 检查项目是否已有端口
        if project_code in projects:
            existing_port = projects[project_code]["dashboard_port"]
            if self.is_port_available(existing_port):
                print(f"✅ 项目 {project_code} 已分配端口: {existing_port}")
                return existing_port
            else:
                print(f"⚠️  端口 {existing_port} 被占用，重新分配...")

        # 分配新端口
        for port in range(self.PORT_RANGE_START, self.PORT_RANGE_END + 1):
            # 跳过已分配给其他项目的端口
            if any(p["dashboard_port"] == port for p in projects.values()):
                continue

            # 检查端口是否实际可用
            if self.is_port_available(port):
                # 分配端口
                projects[project_code] = {
                    "project_code": project_code,
                    "project_path": project_path,
                    "dashboard_port": port,
                    "api_port": port - 1,
                    "allocated_at": datetime.now().isoformat()
                }

                registry["projects"] = projects
                self._save_registry(registry)

                print(f"✅ 为项目 {project_code} 分配端口: {port}")
                return port

        print(f"❌ 错误: 端口范围 {self.PORT_RANGE_START}-{self.PORT_RANGE_END} 全部被占用")
        return None

    def release_port(self, project_code: str) -> bool:
        """释放项目端口"""
        registry = self._load_registry()
        projects = registry.get("projects", {})

        if project_code in projects:
            port = projects[project_code]["dashboard_port"]
            del projects[project_code]
            registry["projects"] = projects
            self._save_registry(registry)
            print(f"✅ 已释放项目 {project_code} 的端口: {port}")
            return True

        return False

    def list_all_projects(self) -> List[Dict]:
        """列出所有项目"""
        registry = self._load_registry()
        return list(registry.get("projects", {}).values())

    def get_project_port(self, project_code: str) -> Optional[int]:
        """获取项目端口"""
        registry = self._load_registry()
        projects = registry.get("projects", {})

        if project_code in projects:
            return projects[project_code]["dashboard_port"]

        return None


# 命令行使用
if __name__ == "__main__":
    import sys

    manager = PortManager()

    if len(sys.argv) < 2:
        print("用法:")
        print("  python port_manager.py allocate PROJECT_CODE /path/to/project")
        print("  python port_manager.py release PROJECT_CODE")
        print("  python port_manager.py list")
        print("  python port_manager.py get PROJECT_CODE")
        sys.exit(1)

    command = sys.argv[1]

    if command == "allocate":
        if len(sys.argv) < 4:
            print("错误: 需要项目代码和路径")
            sys.exit(1)
        project_code = sys.argv[2]
        project_path = sys.argv[3]
        port = manager.allocate_port(project_code, project_path)
        if port:
            print(f"端口: {port}")

    elif command == "release":
        if len(sys.argv) < 3:
            print("错误: 需要项目代码")
            sys.exit(1)
        project_code = sys.argv[2]
        manager.release_port(project_code)

    elif command == "list":
        projects = manager.list_all_projects()
        print(f"\n已注册项目: {len(projects)}个\n")
        for p in projects:
            print(f"  {p['project_code']}:")
            print(f"    端口: {p['dashboard_port']}")
            print(f"    路径: {p['project_path']}")
            print(f"    分配时间: {p['allocated_at']}")
            print()

    elif command == "get":
        if len(sys.argv) < 3:
            print("错误: 需要项目代码")
            sys.exit(1)
        project_code = sys.argv[2]
        port = manager.get_project_port(project_code)
        if port:
            print(f"端口: {port}")
        else:
            print(f"项目 {project_code} 未找到")
