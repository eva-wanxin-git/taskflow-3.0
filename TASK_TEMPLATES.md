# 📋 任务模板库 - 标准化工作流程

> **用途**: AI快速执行常见任务，无需重新思考流程  
> **效率**: 减少50-70%的思考时间和上下文消耗

---

## 🎯 使用方法

**AI直接说**:
```
"按照模板1执行添加新Tab任务"
"使用格式修复模板处理start_insight_api.py"
```

---

## 📁 模板索引

| ID | 任务类型 | 预估时间 | 上下文消耗 |
|----|---------|---------|-----------|
| T01 | 添加新Tab | 5分钟 | 10K tokens |
| T02 | 修复代码格式 | 2分钟 | 2K tokens |
| T03 | 添加API端点 | 10分钟 | 15K tokens |
| T04 | 数据库查询 | 3分钟 | 3K tokens |
| T05 | 调试错误 | 10-30分钟 | 20K tokens |
| T06 | 代码审查 | 15分钟 | 25K tokens |
| T07 | 部署检查 | 5分钟 | 8K tokens |
| T08 | 文档更新 | 5分钟 | 5K tokens |

---

## 📌 模板T01: 添加新Tab

### **适用场景**
为任何工作台模块（架构师/全栈/运维）添加新Tab

### **标准流程**

#### **步骤1: 定位HTML模板**
```bash
# 使用Everything查找
"找到 architect_workspace.html"

# 或使用grep
grep "architect_workspace.html"
```

#### **步骤2: 复制Tab结构**
在HTML中找到现有Tab的结构：
```html
<!-- Tab按钮 -->
<div class="tab-button" data-tab="existing-tab">
  现有Tab名称
</div>

<!-- Tab内容 -->
<div id="existing-tab" class="tab-panel">
  <!-- 内容 -->
</div>
```

#### **步骤3: 修改并添加**
```html
<!-- 新Tab按钮 -->
<div class="tab-button" data-tab="new-tab">
  新Tab名称
</div>

<!-- 新Tab内容 -->
<div id="new-tab" class="tab-panel" style="display: none;">
  <h3>新Tab标题</h3>
  <!-- 添加具体内容 -->
</div>
```

#### **步骤4: 测试**
```bash
# 重启服务
python start_insight_api.py

# 访问并测试
http://localhost:8820/architect
```

### **涉及文件**
- `templates/architect_workspace.html` (或其他模块)
- 可能需要: `routes.py` (如果需要新API)

### **常见问题**
- Tab不显示 → 检查`style="display: none;"`
- 点击无反应 → 检查`data-tab="xxx"`和`id="xxx"`是否匹配

### **预估消耗**
- 时间: 5分钟
- 上下文: 10K tokens

---

## 📌 模板T02: 修复代码格式

### **适用场景**
代码格式混乱、缩进不准、样式不统一

### **标准流程**

#### **Python文件格式修复**
```bash
# 步骤1: 检查问题
"用Ruff检查 start_insight_api.py"

# 步骤2: 自动修复
"用Ruff自动修复 start_insight_api.py"

# 步骤3: 验证
"再次检查确认修复完成"
```

#### **HTML/CSS文件格式修复**
```bash
# 步骤1: 格式化HTML
"用Prettier格式化 templates/architect_workspace.html"

# 步骤2: 格式化CSS
"用Prettier格式化 static/css/*.css"
```

#### **批量格式化**
```bash
# 所有Python文件
"用Ruff格式化所有Python文件"

# 所有前端文件
"用Prettier格式化所有HTML和CSS文件"
```

### **预估消耗**
- 时间: 2分钟
- 上下文: 2K tokens

---

## 📌 模板T03: 添加API端点

### **适用场景**
为模块添加新的API接口

### **标准流程**

#### **步骤1: 定位routes文件**
```bash
# 找到对应模块的routes
grep "Blueprint" apps/architect/routes.py
```

#### **步骤2: 添加路由**
```python
@architect_bp.route('/api/new-endpoint', methods=['GET', 'POST'])
def new_endpoint():
    """新端点说明"""
    try:
        # 处理逻辑
        data = request.get_json()
        result = process_data(data)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
```

#### **步骤3: 测试**
```bash
# 使用Fetch MCP测试
"用Fetch测试 http://localhost:8820/architect/api/new-endpoint"

# 或使用curl
curl -X POST http://localhost:8820/architect/api/new-endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

### **涉及文件**
- `apps/模块名/routes.py`
- 可能需要: 数据库操作、业务逻辑文件

### **预估消耗**
- 时间: 10分钟
- 上下文: 15K tokens

---

## 📌 模板T04: 数据库查询

### **适用场景**
查看数据库结构、查询数据、验证数据

### **标准流程**

#### **查看表结构**
```bash
"用SQLite查看tasks表的结构"
"显示所有表的列表"
```

#### **查询数据**
```sql
-- 查看所有待处理任务
"用SQLite查询: SELECT * FROM tasks WHERE status='pending'"

-- 统计任务数量
"用SQLite查询: SELECT status, COUNT(*) FROM tasks GROUP BY status"

-- 查看最近的任务
"用SQLite查询: SELECT * FROM tasks ORDER BY created_at DESC LIMIT 10"
```

#### **验证数据**
```bash
"查询架构师模块的所有任务"
"检查是否有重复的任务ID"
```

### **预估消耗**
- 时间: 3分钟
- 上下文: 3K tokens

---

## 📌 模板T05: 调试错误

### **适用场景**
发现bug、报错、功能异常

### **标准流程**

#### **步骤1: 定位错误**
```bash
# 1. 查看错误信息
Error Lens会自动显示

# 2. 搜索错误关键词
grep "错误信息关键词"

# 3. 语义搜索
codebase_search "这个功能是怎么实现的"
```

#### **步骤2: 理解逻辑**
```bash
# 读取相关文件（精确定位，不要全读）
"读取 routes.py 的第100-150行"

# 查看函数调用关系
"这个函数被哪些地方调用？"
```

#### **步骤3: 修复问题**
```bash
# 1. 修改代码
search_replace修复问题

# 2. 检查格式
"用Ruff检查修改的文件"

# 3. 测试
重启服务并测试
```

#### **步骤4: 验证修复**
```bash
# 1. 功能测试
手动测试修复的功能

# 2. 数据验证
"用SQLite验证数据正确"

# 3. 日志检查
查看是否还有错误
```

### **预估消耗**
- 时间: 10-30分钟（取决于复杂度）
- 上下文: 20K tokens

---

## 📌 模板T06: 代码审查

### **适用场景**
审查新代码、检查质量、发现潜在问题

### **标准流程**

#### **步骤1: 代码质量检查**
```bash
# Python代码
"用Ruff检查 apps/architect/routes.py"

# 查看报告
分析发现的问题（格式、逻辑错误、潜在bug）
```

#### **步骤2: 结构检查**
```bash
# 检查函数复杂度
是否有过长的函数（>50行）

# 检查命名规范
是否符合Python命名规范

# 检查导入
是否有未使用的导入
```

#### **步骤3: 逻辑审查**
```bash
# 检查异常处理
是否有适当的try-except

# 检查边界条件
是否处理了空值、边界情况

# 检查性能
是否有明显的性能问题
```

#### **步骤4: 输出报告**
```markdown
# 代码审查报告

## 文件: apps/architect/routes.py

### ✅ 优点
- 代码结构清晰
- 异常处理完善

### ⚠️ 问题
1. 第45行: 未使用的导入
2. 第120-180行: 函数过长，建议拆分
3. 第200行: 缺少类型提示

### 💡 建议
1. 使用Ruff自动修复格式问题
2. 拆分长函数
3. 添加文档字符串
```

### **预估消耗**
- 时间: 15分钟
- 上下文: 25K tokens

---

## 📌 模板T07: 部署检查

### **适用场景**
部署前检查、环境验证

### **标准流程**

#### **步骤1: 代码检查**
```bash
# 格式检查
"用Ruff检查所有Python文件"
"用Prettier检查所有HTML文件"

# 自动修复
"自动修复所有格式问题"
```

#### **步骤2: 依赖检查**
```bash
# 检查requirements.txt
cat requirements.txt

# 检查是否有缺失的依赖
pip list | grep flask
```

#### **步骤3: 配置检查**
```bash
# 检查端口配置
grep "8820" start_insight_api.py

# 检查数据库路径
grep "database" start_insight_api.py
```

#### **步骤4: 功能测试**
```bash
# 启动服务
python start_insight_api.py

# 测试关键API
"用Fetch测试主要API端点"

# 数据库验证
"用SQLite验证数据库状态"
```

### **预估消耗**
- 时间: 5分钟
- 上下文: 8K tokens

---

## 📌 模板T08: 文档更新

### **适用场景**
更新README、添加说明、记录变更

### **标准流程**

#### **步骤1: 确定更新内容**
```markdown
更新内容：
- 新功能说明
- API变更
- 配置说明
- 使用指南
```

#### **步骤2: 更新文档**
```bash
# 找到相关文档
"找到README.md"

# 更新内容
使用search_replace更新特定部分

# 或创建新文档
创建 docs/新功能说明.md
```

#### **步骤3: 格式化**
```bash
"用Prettier格式化 README.md"
```

#### **步骤4: 验证**
```bash
# 检查Markdown语法
阅读更新后的文档确认格式正确

# 检查链接
验证文档中的链接是否正确
```

### **预估消耗**
- 时间: 5分钟
- 上下文: 5K tokens

---

## 💡 使用技巧

### **组合使用模板**

**场景: 添加新功能**
```
1. 使用T01添加新Tab
2. 使用T03添加API端点
3. 使用T02修复格式
4. 使用T07部署检查
5. 使用T08更新文档
```

### **自定义模板**

您可以根据项目需要添加自己的模板：
```markdown
## 📌 模板T09: 您的自定义任务

### 适用场景
...

### 标准流程
...
```

---

**创建时间**: 2025-11-22  
**维护者**: AI助手  
**用途**: 标准化常见任务，减少50-70%上下文消耗

**记住**: 标准任务用模板，不要重新发明轮子！ ⚡

