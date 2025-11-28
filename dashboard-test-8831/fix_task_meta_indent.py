#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复任务卡片的task-meta HTML结构和缩进
"""

import re
import shutil
from datetime import datetime

FILE = "index.html"

print("=" * 70)
print("修复任务卡片task-meta结构和缩进")
print("=" * 70)
print()

# 备份
print(f"Step 1: 创建备份...")
backup = f"{FILE}.backup-fix-indent-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
shutil.copy2(FILE, backup)
print(f"✅ 备份: {backup}")
print()

# 读取文件
print(f"Step 2: 读取文件...")
with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()
print(f"✅ 文件读取完成")
print()

# 修复task-meta结构（使用正则表达式）
print(f"Step 3: 批量修复task-meta结构...")

# 模式1: 修复错误的缩进（task-meta-left的闭合标签缩进错误）
pattern1 = r'(                                    </span>\n)                            </div>\n(                                <div class="task-meta-right">)'
replacement1 = r'\1                                </div>\n\2'
content, count1 = re.subn(pattern1, replacement1, content)
print(f"✅ 修复task-meta-left闭合: {count1} 处")

# 模式2: 修复task-meta-right的闭合标签
pattern2 = r'(                                    <span class="priority-badge [^"]+">P[0-3]</span>\n)                        </div>\n(                                    </div>)'
replacement2 = r'\1                                </div>\n                            </div>'
content, count2 = re.subn(pattern2, replacement2, content)
print(f"✅ 修复task-meta-right闭合: {count2} 处")

# 模式3: 修复没有可并行标签的情况
pattern3 = r'(                                    <span class="priority-badge [^"]+">P[0-3]</span>\n                        </div>\n                                    </div>)'
replacement3 = r'                                    <span class="priority-badge p1">P1</span>\n                                </div>\n                            </div>'
content, count3 = re.subn(pattern3, replacement3, content)
print(f"✅ 修复其他情况: {count3} 处")

print()

# 写入
print(f"Step 4: 写入文件...")
with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ 文件已更新")
print()

total = count1 + count2 + count3
print("=" * 70)
print(f"✅ 修复完成！共处理 {total} 处")
print("=" * 70)
print()
print("下一步: 重启8825服务器并测试")
print()

