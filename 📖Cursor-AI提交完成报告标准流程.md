# 📖 Cursor中AI提交完成报告标准流程

**适用场景**: 工程师在Cursor对话中完成任务  
**执行者**: Cursor中的AI助手  
**目标**: 自动调用API更新任务状态为已完成

---

## 🎯 标准流程

### 工程师说：
```
任务已完成，请帮我提交完成报告。

实际工时：2小时
完成说明：功能已实现并测试通过
```

### AI执行：

```python
import requests
import json

# 提取任务ID（从之前的对话上下文）
task_id = "TEST-2025-001"  # 或其他任务ID

# 提取完成信息
completion_data = {
    "actual_hours": 2.0,
    "notes": "功能已实现并测试通过",
    "features": [
        "实现了XXX功能",
        "添加了YYY组件"
    ],
    "files_created": [
        "apps/xxx/new_file.py"
    ],
    "files_modified": [
        "apps/xxx/existing.py"
    ],
    "code_lines": 150
}

# 调用API
response = requests.post(
    f'http://localhost:8800/api/engineer/tasks/{task_id}/complete',
    headers={'Content-Type': 'application/json'},
    json=completion_data
)

result = response.json()

if result['success']:
    print(f"""
✅ 任务已提交完成！

任务ID: {task_id}
状态: 进行中 → 已完成
实际工时: {completion_data['actual_hours']}小时

---

现在请前往Dashboard查看完成报告：

1. 打开 http://localhost:8831
2. 进入"全栈工程师工作台" → "任务看板"
3. 点击"已完成"筛选
4. 找到任务 {task_id}
5. 点击"查看详情"按钮查看完整报告
6. 或点击"复制完成报告"复制给架构师审查

---

完成报告已保存到数据库。
""")
else:
    print(f"❌ 提交失败: {result.get('message')}")
```

---

## 📋 API接口说明

### 端点
```
POST http://localhost:8800/api/engineer/tasks/{task_id}/complete
```

### 请求体
```json
{
  "actual_hours": 2.0,
  "notes": "功能已实现并测试通过",
  "features": ["功能1", "功能2"],
  "files_created": ["file1.py", "file2.py"],
  "files_modified": ["file3.py"],
  "code_lines": 150
}
```

### 响应
```json
{
  "success": true,
  "message": "任务 TEST-2025-001 已完成",
  "task_id": "TEST-2025-001",
  "new_status": "completed",
  "actual_hours": 2.0,
  "updated_at": "2025-11-22T15:50:00"
}
```

---

## 🎯 Cursor AI提示词模板

将以下内容添加到Cursor的AI配置中：

```markdown
## 任务完成提交

当工程师说"任务完成"或"提交完成报告"时，我会：

1. 提取任务ID（从对话上下文）
2. 提取完成信息（工时、说明、功能、文件等）
3. 调用API提交完成：

```python
import requests

task_id = "{从上下文提取}"
response = requests.post(
    f'http://localhost:8800/api/engineer/tasks/{task_id}/complete',
    json={
        'actual_hours': 提取的工时,
        'notes': '提取的说明',
        'features': ['提取的功能列表'],
        'files_created': ['提取的新建文件'],
        'files_modified': ['提取的修改文件'],
        'code_lines': 估算的代码行数
    }
)

if response.json()['success']:
    print("✅ 任务已提交完成！请到Dashboard查看。")
```

4. 告诉工程师去Dashboard查看完成报告
```

---

## 📖 工程师标准话术

### 开始任务
```
（粘贴从Dashboard复制的提示词）

请帮我完成这个任务。
```

### 完成任务
```
任务已完成，请帮我提交完成报告。

实际工时：2小时
完成说明：功能已实现并测试通过

实现的功能：
- XXX
- YYY

创建的文件：
- file1.py
- file2.py

修改的文件：
- file3.py
```

---

## 🔄 完整示例对话

**工程师**: 
```
任务TEST-2025-001已完成，请帮我提交完成报告。

实际工时：0.5小时
完成说明：测试任务，验证功能正常
```

**AI响应**:
```python
import requests

response = requests.post(
    'http://localhost:8800/api/engineer/tasks/TEST-2025-001/complete',
    json={
        'actual_hours': 0.5,
        'notes': '测试任务，验证功能正常',
        'features': ['验证任务看板加载', '验证状态流转', '验证详情弹窗'],
        'files_created': [],
        'files_modified': [],
        'code_lines': 0
    }
)

print(response.json())
```

**AI说**:
```
✅ 任务已提交完成！

任务ID: TEST-2025-001
状态: 进行中 → 已完成
实际工时: 0.5小时

现在请：
1. 打开 http://localhost:8831
2. 全栈工程师工作台 → 任务看板 → 已完成
3. 找到TEST-2025-001
4. 点击"查看详情"查看完成报告
5. 点击"复制完成报告"提交给架构师
```

---

## 🎯 Dashboard按钮说明

### 待处理任务
- **[复制提示词]** - 复制提示词 + 自动接受任务（状态→进行中）
- **[查看详情]** - 查看任务提示词

### 进行中任务
- **[查看详情]** - 查看任务进度（任务在Cursor中执行，Dashboard只能查看）

### 已完成任务
- **[复制完成报告]** - 复制markdown格式报告
- **[查看详情]** - 查看完整的完成报告

---

## ✅ 核心设计

**Dashboard的作用**:
- 接受任务（点击"复制提示词"）
- 查看任务详情和进度
- 查看和复制完成报告

**Cursor的作用**:
- 执行任务开发
- 提交完成报告（AI调用API）

**分工明确，各司其职！** 🎯

---

**文档版本**: v1.0  
**创建时间**: 2025-11-22

