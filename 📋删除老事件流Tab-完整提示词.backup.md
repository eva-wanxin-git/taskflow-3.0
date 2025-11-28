# 📋 删除老事件流Tab - 完整提示词

**给下一个Cursor的完整删除指令**

---

## 🎯 任务目标

在架构师工作台中删除**原始的"事件流"Tab**（保留新增的"新事件流"Tab）

## 📍 删除目标位置

### 1. Tab导航按钮位置
- **文件**: `/Users/yalinwang/Desktop/任务所 1.8/taskflow-v1-2/taskflow-v1-2/dashboard-test-8831/index.html`
- **第12897-12900行**：Tab导航中的"事件流"按钮
```html
<button class="architect-tab-item" onclick="switchArchitectTab('events')">
    事件流
    <span class="architect-tab-badge">89</span>
</button>
```

### 2. Tab内容位置
- **第13637-13652行**：Tab内容中的"事件流"面板

```html
<div id="architect-events" class="architect-tab-pane">
    <div class="architect-event-timeline">
        <!-- 内容 -->
    </div>
</div>
```

### 3. CSS样式位置
- **第2930行开始**：`.architect-event-timeline` 及相关CSS
- **第5455行附近**：事件流相关的architect CSS

### 4. JavaScript函数位置
- **第22498行附近**：`architect-event-timeline` 相关JavaScript

---

## 🗑️ 删除步骤（严格顺序）

### 第1步：总备份
```bash
cp index.html index.html.backup-before-delete-events-tab-$(date +%Y%m%d-%H%M%S)
```

### 第2步：删除Tab导航按钮
**查找**：第12897-12900行
```
grep -n "switchArchitectTab('events')" index.html
```

**删除内容**（共4行）：
```html
                <button class="architect-tab-item" onclick="switchArchitectTab('events')">
                    事件流
                    <span class="architect-tab-badge">89</span>
                </button>
```

**使用工具**：`search_replace`
- 找到上面的4行代码
- 替换为空（注意保留前后的换行符）

**备份**：
```bash
cp index.html index.html.backup-step1-button-deleted
```

### 第3步：删除Tab内容面板
**查找**：第13637-13652行
```
grep -n 'id="architect-events"' index.html
```

**删除内容**（共16行）：
```html
                <div id="architect-events" class="architect-tab-pane">
                    <div class="architect-event-timeline">
                        <div class="architect-timeline-filters">
                            <button class="architect-filter-chip active">全部</button>
                            <button class="architect-filter-chip">今天</button>
                            <button class="architect-filter-chip">本周</button>
                            <button class="architect-filter-chip">决策</button>
                            <button class="architect-filter-chip">任务</button>
                            <button class="architect-filter-chip">交接</button>
                        </div>
                        <!-- 事件将通过JavaScript动态加载 -->
                        <div style="padding: 40px; text-align: center; color: var(--noir-silver);">
                            <div style="font-size: 14px;">正在加载事件流...</div>
                        </div>
                    </div>
                </div>
```

**使用工具**：`search_replace`

**备份**：
```bash
cp index.html index.html.backup-step2-content-deleted
```

### 第4步：删除CSS样式
**查找**：第2930行开始
```
grep -n "\.architect-event-timeline" index.html
```

**需要删除的CSS块**（从`.architect-event-timeline`开始，包含所有相关样式）：
- `.architect-event-timeline`
- `.architect-timeline-filters`
- `.architect-filter-chip`（architect版本）
- `.architect-timeline-item`
- `.architect-timeline-marker`
- `.architect-event-card`
- `.architect-event-header`
- `.architect-event-title`
- `.architect-event-meta`
- 其他所有以 `.architect-` 开头的事件流相关样式

**方法**：
1. 找到第一个 `/* ==================== 事件流` 注释（大约第2920-2930行）
2. 找到下一个主要CSS块的开始位置（下一个 `/* ==== ` 注释）
3. 删除这之间的所有代码

**备份**：
```bash
cp index.html index.html.backup-step3-css-deleted
```

### 第5步：删除JavaScript函数
**查找**：第22498行附近
```
grep -n "architect-event-timeline" index.html
```

**需要删除的JavaScript代码**：
- 所有与 `architect-event-timeline` 相关的代码
- 所有与 `architect-filter-chip` 事件监听相关的architect事件流代码

**方法**：
1. 搜索 `architect-event-timeline` 出现的位置
2. 删除相关的JavaScript初始化代码和事件监听器

**备份**：
```bash
cp index.html index.html.backup-step4-js-deleted
```

### 第6步：最终备份和验证
```bash
cp index.html index.html.backup-architect-old-events-deleted-complete
```

**验证清单**：
- [ ] Tab导航栏中"事件流"按钮已删除
- [ ] 只剩下以下Tab：指挥中心、认命指令、对话历史、代码审查、异常中心、需求池、新事件流
- [ ] 新事件流Tab仍然存在并正常工作
- [ ] 刷新浏览器，点击"新事件流"Tab能正常显示

---

## ⚠️ 关键注意事项

### 1. 不要删除"新事件流"
- ✅ 保留：`id="architect-new-events"` 的Tab
- ✅ 保留：`class="architect-tab-pane"` 中的新事件流Tab
- ❌ 不删除：新增加的所有新事件流CSS和JS

### 2. 区分老旧CSS
- ❌ 删除：`.architect-event-timeline`（老的）
- ✅ 保留：`.event-stream`（新的）
- ❌ 删除：`.architect-timeline-filters`（老的）
- ✅ 保留：`.stream-filters`（新的）

### 3. 文件大小变化
- **删除前**：约844K
- **删除后**：约800-810K（减少约30-40K）

### 4. 使用正确的工具
- ✅ 使用 `search_replace` 工具手动删除
- ❌ 不要使用Python脚本
- ✅ 每步前备份
- ✅ 每步后刷新浏览器测试

### 5. 验证命名规范
老的（要删除）：
```
id="architect-events"
class="architect-event-timeline"
.architect-timeline-*
.architect-filter-chip (architect版本的事件流筛选)
```

新的（要保留）：
```
id="architect-new-events"
class="event-stream"
class="stream-filters"
class="event-item"
function filterArchitectNewEvents()
```

---

## 📋 检查清单

完成后检查以下项目：

- [ ] 第12897-12900行的"事件流"按钮已删除
- [ ] 第13637-13652行的"architect-events"Tab内容已删除
- [ ] `.architect-event-timeline` CSS块已完全删除
- [ ] 所有architect事件流相关的CSS已删除
- [ ] 所有architect事件流相关的JavaScript已删除
- [ ] 新事件流Tab仍然存在
- [ ] 新事件流CSS仍然存在（`.event-stream`等）
- [ ] 新事件流JavaScript函数仍然存在（`filterArchitectNewEvents`）
- [ ] 刷新浏览器后，点击"新事件流"能正常显示
- [ ] 筛选功能正常工作

---

## 🎯 完成标志

✅ **任务完成的标志**：
1. Tab导航栏中只显示7个Tab：指挥中心、认命指令、对话历史、代码审查、异常中心、需求池、新事件流
2. 文件大小减少约30-40K
3. 没有JavaScript错误
4. 新事件流Tab完全正常工作

---

## 📝 复制给下一个Cursor的开始词

```
你好！我需要删除架构师工作台中的老"事件流"Tab及其所有相关代码。

【当前状态】
- 测试环境：8831
- 工作目录：/Users/yalinwang/Desktop/任务所 1.8/taskflow-v1-2/taskflow-v1-2/dashboard-test-8831
- 目标文件：index.html
- 已有的新Tab：新事件流（id="architect-new-events"）

【需要删除的内容】
1. Tab导航按钮（第12897-12900行）："事件流"按钮
2. Tab内容面板（第13637-13652行）：id="architect-events"
3. CSS样式：.architect-event-timeline 及所有相关architect事件流样式
4. JavaScript：所有architect-event-timeline相关代码

【关键提醒】
- ✅ 保留新事件流Tab（id="architect-new-events"）
- ✅ 保留新事件流的所有CSS和JS
- ❌ 不要删除 .event-stream 相关的样式
- ✅ 每步前备份
- ❌ 不要使用Python脚本

请先做总备份，然后按步骤删除。
```

---

**准备好了吗？复制上面的提示词给下一个Cursor开始删除老事件流Tab！** 🚀


