#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诊断HTML DOM结构 - 检查模块嵌套关系"""
from html.parser import HTMLParser
import sys

class ModuleStructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []  # 标签栈
        self.devops_found = False
        self.noah_found = False
        self.devops_level = -1
        self.noah_level = -1
        self.devops_closed = False
        self.line_number = 0
        self.devops_start_line = 0
        self.devops_end_line = 0
        self.noah_start_line = 0
        
    def handle_starttag(self, tag, attrs):
        self.line_number += 1
        attrs_dict = dict(attrs)
        
        # 进栈
        self.stack.append(tag)
        current_level = len(self.stack)
        
        # 检测运维模块
        if tag == 'div' and 'class' in attrs_dict:
            classes = attrs_dict['class']
            if 'devops-module' in classes:
                self.devops_found = True
                self.devops_level = current_level
                self.devops_start_line = self.line_number
                print(f"✅ 找到运维模块开始标签 (行{self.line_number}, 层级{current_level})")
                print(f"   栈内容: {' > '.join(self.stack[-5:])}")
            
            # 检测Noah模块
            if 'code-manager-module' in classes:
                self.noah_found = True
                self.noah_level = current_level
                self.noah_start_line = self.line_number
                print(f"✅ 找到Noah模块开始标签 (行{self.line_number}, 层级{current_level})")
                print(f"   栈内容: {' > '.join(self.stack[-5:])}")
                
                # 关键检查：Noah在运维闭合之前出现
                if self.devops_found and not self.devops_closed:
                    if current_level > self.devops_level:
                        print(f"❌ 错误：Noah模块在运维模块内部！")
                        print(f"   运维层级: {self.devops_level}")
                        print(f"   Noah层级: {self.noah_level}")
                        print(f"   运维已闭合: {self.devops_closed}")
                    else:
                        print(f"✅ 正确：Noah模块和运维模块是兄弟关系")
                        
    def handle_endtag(self, tag):
        if not self.stack:
            return
            
        # 出栈
        if self.stack and self.stack[-1] == tag:
            current_level = len(self.stack)
            
            # 检查运维模块闭合
            if self.devops_found and not self.devops_closed and current_level == self.devops_level:
                self.devops_closed = True
                self.devops_end_line = self.line_number
                print(f"✅ 找到运维模块结束标签 (行{self.line_number}, 层级{current_level})")
                
            self.stack.pop()

print("=" * 80)
print("HTML DOM 结构诊断")
print("=" * 80)
print()

# 读取HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 只分析运维到Noah之间的部分
lines = html_content.split('\n')
devops_line = 0
noah_line = 0

for i, line in enumerate(lines):
    if '<!-- ========== 运维工程师工作台 ========== -->' in line:
        devops_line = i + 1
    if '<!-- ========== Noah AI代码管家模块 ========== -->' in line:
        noah_line = i + 1
        break

print(f"📍 运维模块注释在第 {devops_line} 行")
print(f"📍 Noah模块注释在第 {noah_line} 行")
print(f"📍 两者之间相隔 {noah_line - devops_line} 行")
print()
print("=" * 80)
print("开始解析...")
print("=" * 80)
print()

# 解析这部分HTML
parser = ModuleStructureParser()
section_to_parse = '\n'.join(lines[devops_line-1:noah_line+50])
try:
    parser.handle_data(section_to_parse)
except:
    pass

print()
print("=" * 80)
print("诊断结果")
print("=" * 80)

if parser.devops_found and parser.noah_found:
    if not parser.devops_closed:
        print("❌ 问题：运维模块在Noah之前没有正确闭合！")
        print(f"   运维开始：第 {parser.devops_start_line} 行")
        print(f"   Noah开始：第 {parser.noah_start_line} 行")
        print(f"   运维结束：未找到或在Noah之后")
        print()
        print("💡 这导致Noah模块被包含在运维模块的白色背景内")
    else:
        print("✅ HTML结构正常：运维模块已正确闭合")
        print(f"   运维：第 {parser.devops_start_line} - {parser.devops_end_line} 行")
        print(f"   Noah：第 {parser.noah_start_line} 行开始")
        print()
        print("💡 问题可能在CSS，不是HTML结构")

