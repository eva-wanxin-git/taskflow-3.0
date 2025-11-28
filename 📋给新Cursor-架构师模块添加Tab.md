# 📋 给新Cursor - 架构师模块添加Tab任务

**任务时间**: 2025-11-22 19:50  
**环境**: 8831测试环境  
**模块**: 架构师工作台  
**要求**: 手动添加（禁止使用Python脚本）

---

## ✅ 当前状态

### 已完成的工作
- ✅ **全栈工程师模块**已添加3个新Tab（单元测试、代码审查、集成部署）
- ✅ 所有Tab滚动条正常工作（应用了血泪教训）
- ✅ 筛选功能全部正常
- ✅ 8820生产环境已同步更新

### 当前架构师模块Tab
- ✅ Tab 1: 事件流（89个事件）
- ✅ Tab 2: 认命指令
- ✅ Tab 3: 对话历史（12条对话）
- ⏳ 缺少：代码审查、扫描任务等Tab

---

## 🎯 本次任务目标

在**架构师模块**添加以下Tab（参考全栈工程师模块的成功实现）：

1. **代码审查Tab**（在认命指令之后）
2. **扫描任务Tab**（可选，如果有UI演示文件）
3. **其他Tab**（根据UI演示文件中的可用内容）

---

## 📂 工作目录和参考文件

### 工作目录
```
/Users/yalinwang/Desktop/任务所 1.8/taskflow-v1-2/taskflow-v1-2/dashboard-test-8831
```

### 目标文件
```
index.html
```

### UI演示文件目录
```
/Users/yalinwang/Dropbox/UI演示文稿/
```

**可用的演示文件**：
- `fullstack-code-review-tab.html` - 代码审查Tab参考
- `fullstack-integration-tab-v2.html` - 集成部署Tab参考
- `fullstack-unit-test-module.html` - 单元测试Tab参考
- 其他架构师相关的HTML文件（需要先list_dir查看）

---

## 🩸 血泪教训 - 滚动条修复3要素（必须遵守！）

参考文件：`✅滚动条完全修复-左右双滚动-8831.md`

### 要素1️⃣: Tab面板固定高度
```css
.architect-module #architect-[tab-name].active {
    height: 1200px;  /* ✅ 固定高度 */
    min-height: 0;   /* ✅ 关键：允许收缩 */
    overflow: hidden; /* ✅ 隐藏外层溢出 */
}
```

### 要素2️⃣: Tab面板是flex容器
```css
.architect-module #architect-[tab-name].active {
    display: flex;           /* ✅ flex布局 */
    flex-direction: column;  /* ✅ 垂直方向 */
}
```

### 要素3️⃣: 内容区域flex滚动
```css
.architect-module .[content-container] {
    flex: 1;              /* ✅ 占满剩余空间（关键！） */
    overflow-y: auto;     /* ✅ 允许滚动 */
    min-height: 0;        /* ✅ 关键：允许flex子元素收缩 */
    max-height: 100%;     /* ✅ 限制最大高度 */
}
```

**⚠️ 三要素缺一不可，否则滚动条不会出现！**

---

## 📋 详细操作步骤

### 第一步：准备工作

1. **查看UI演示文件目录**，了解有哪些可用的Tab演示：
```
使用list_dir工具查看：/Users/yalinwang/Dropbox/UI演示文稿/
```

2. **确定要添加的Tab**（建议从代码审查开始）

3. **创建总备份**：
```bash
cp index.html index.html.backup-before-architect-tabs-$(date +%Y%m%d-%H%M%S)
```

---

### 第二步：添加代码审查Tab（示例）

#### 2.1 读取UI演示文件
```
read_file: /Users/yalinwang/Dropbox/UI演示文稿/[对应文件].html
分段读取：
- 第1-500行：查看CSS部分
- 第500-1000行：查看HTML部分
- 最后部分：查看JavaScript函数
```

#### 2.2 添加CSS（步骤A）

**备份**：
```bash
cp index.html index.html.backup-step-A-before-css
```

**查找插入位置**：
```
在architect-module的CSS区域，找到合适位置
建议：在现有Tab CSS之后添加
```

**添加CSS**：
- 提取UI演示文件中的CSS
- **为所有选择器添加 `.architect-module` 前缀**
- 使用`search_replace`工具手动替换插入

**示例**：
```css
/* ==================== 代码审查监控模块 ==================== */

/* 审查统计栏 */
.architect-module .review-stats-bar {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    ...
}

.architect-module .review-stat-box {
    ...
}

/* 其他CSS... */
```

#### 2.3 添加HTML（步骤B）

**备份**：
```bash
cp index.html index.html.backup-step-B-after-css
```

**查找插入位置**：
```
在架构师模块的Tab内容区
建议：在认命指令Tab之后，对话历史Tab之前
查找：<!-- Tab 3: 对话历史 -->
在此之前插入新Tab
```

**修改要点**：
- 将UI演示文件的 `id="code-review"` 改为 `id="architect-reviews"`
- 将 `class="tab-pane active"` 改为 `class="architect-tab-pane"`（去掉active）
- 确保使用architect的class命名

**示例结构**：
```html
<!-- Tab 2.5: 代码审查 -->
<div id="architect-reviews" class="architect-tab-pane">
    <!-- 统计栏 -->
    <div class="review-stats-bar">
        ...
    </div>
    
    <!-- 筛选器 -->
    <div class="review-filters">
        ...
    </div>
    
    <!-- 内容列表（应用血泪教训） -->
    <div class="review-list-container">
        <div class="review-list">
            <!-- 卡片内容，至少8-10个才能触发滚动 -->
        </div>
    </div>
</div>
```

#### 2.4 添加Tab导航按钮（步骤C）

**查找位置**：
```
搜索：architect-tab-item.*认命指令
在认命指令和对话历史按钮之间插入
```

**添加按钮**：
```html
<button class="architect-tab-item" onclick="switchArchitectTab('reviews')">
    代码审查
    <span class="architect-tab-badge">10</span>
</button>
```

#### 2.5 添加JavaScript函数（步骤D）

**备份**：
```bash
cp index.html index.html.backup-step-C-after-html
```

**查找位置**：
```
搜索：function switchArchitectTab
在这个函数附近添加筛选函数
```

**添加函数**：
```javascript
// 筛选架构师代码审查
function filterArchitectReviews(status) {
    const architectModule = document.querySelector('.architect-module');
    if (!architectModule) return;
    
    architectModule.querySelectorAll('.review-filters .filter-chip').forEach(chip => {
        chip.classList.remove('active');
    });
    event.target.classList.add('active');

    const cards = architectModule.querySelectorAll('.review-card');
    cards.forEach(card => {
        if (status === 'all') {
            card.style.display = 'block';
        } else {
            const cardStatus = card.classList.contains('pending') ? 'pending' :
                              card.classList.contains('reviewing') ? 'reviewing' :
                              card.classList.contains('approved') ? 'approved' :
                              card.classList.contains('rejected') ? 'rejected' : '';
            
            if (cardStatus === status) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });
}
```

#### 2.6 应用血泪教训CSS（步骤E）

**查找位置**：
```
搜索：.architect-module.*tab-pane
在这个区域添加特殊CSS
```

**添加CSS**：
```css
/* 代码审查Tab特殊处理 - 应用血泪教训 */
.architect-module #architect-reviews {
    display: none;
    flex-direction: column;
}

.architect-module #architect-reviews.active {
    display: flex;
    flex-direction: column;
    height: 1200px;  /* ✅ 固定高度（血泪教训） */
    min-height: 0;   /* ✅ 关键属性 */
    overflow: hidden; /* ✅ 隐藏外层溢出 */
}
```

**备份**：
```bash
cp index.html index.html.backup-architect-[tab-name]-complete
```

---

## 🎯 每步之后立即测试

**测试流程**：
1. 每完成一步，刷新浏览器 http://localhost:8831
2. 进入架构师工作台
3. 检查新Tab是否显示
4. 检查滚动条是否出现
5. **有问题立即停止**，不要继续

---

## ⚠️ 关键注意事项

### 1. 命名规范
| 类型 | 全栈工程师 | 架构师 |
|------|-----------|--------|
| 模块class | `.engineer-module` | `.architect-module` |
| Tab ID | `#engineer-reviews` | `#architect-reviews` |
| Tab class | `.tab-pane` | `.architect-tab-pane` |
| 导航按钮 | `.tab-item` | `.architect-tab-item` |
| 徽章 | `.tab-badge` | `.architect-tab-badge` |

### 2. CSS前缀
- ✅ **所有CSS选择器必须添加 `.architect-module` 前缀**
- ✅ 例如：`.review-card` → `.architect-module .review-card`

### 3. 内容数量
- ✅ 每个Tab至少8-10个卡片/事件
- ✅ 确保每个筛选状态有足够内容触发滚动
- ✅ 内容不够就复制更多示例

### 4. 备份策略
每个步骤前都要备份：
- `index.html.backup-step-A-before-css`
- `index.html.backup-step-B-after-css`
- `index.html.backup-step-C-after-html`
- `index.html.backup-final-[tab-name]-complete`

### 5. 工具使用
- ✅ 使用 `search_replace` 工具手动替换
- ✅ 使用 `read_file` 读取参考文件
- ✅ 使用 `grep` 查找插入位置
- ❌ **禁止使用Python脚本**
- ❌ **禁止一次性替换大段内容**

---

## 📝 完整提示词（复制给新Cursor）

```markdown
你好！我需要在架构师模块手动添加Tab（和全栈工程师模块一样的方式）。

## 当前状态

### 工作环境
- **测试环境**: 8831
- **工作目录**: /Users/yalinwang/Desktop/任务所 1.8/taskflow-v1-2/taskflow-v1-2/dashboard-test-8831
- **目标文件**: index.html
- **当前文件大小**: 844K

### 架构师模块当前Tab
1. ✅ 事件流（89个事件）
2. ✅ 认命指令
3. ✅ 对话历史（12条对话）

### 全栈工程师模块已完成Tab（可参考）
1. ✅ 任务看板（59个任务）
2. ✅ 事件流
3. ✅ 单元测试（5个事件，滚动正常）
4. ✅ 代码审查（10个卡片，滚动正常）
5. ✅ 集成部署（8个事件，滚动正常）
6. ✅ 技术文档
7. ✅ 对话历史（18条对话）

## 任务要求

### 需要添加到架构师模块的Tab

请先查看UI演示文件目录，了解有哪些可用的架构师Tab演示：

```bash
list_dir: /Users/yalinwang/Dropbox/UI演示文稿/
```

然后添加以下Tab（按优先级）：

1. **代码审查Tab** - 最高优先级
   - 位置：认命指令Tab之后，对话历史Tab之前
   - ID：`id="architect-reviews"`
   - Class：`class="architect-tab-pane"`
   - 内容：参考全栈工程师的代码审查Tab结构

2. **扫描任务Tab**（如果有UI演示文件）
   - 位置：代码审查Tab之后
   - ID：`id="architect-scan"`
   - Class：`class="architect-tab-pane"`

3. **其他Tab**（根据UI演示文件决定）

## 操作步骤（严格遵守）

### 步骤0：总备份
```bash
cp index.html index.html.backup-before-architect-tabs-$(date +%Y%m%d-%H%M%S)
```

### 步骤1：读取UI演示文件

**先查看有哪些文件**：
```
list_dir: /Users/yalinwang/Dropbox/UI演示文稿/
```

**读取对应的演示文件**（以代码审查为例）：
```
read_file: /Users/yalinwang/Dropbox/UI演示文稿/[文件名].html
分段读取：
- 第1-500行：CSS部分
- 第500-1000行：HTML开始
- 第1000-1500行：HTML继续
- 最后部分：JavaScript函数
```

### 步骤2：添加CSS

**2.1 创建步骤备份**：
```bash
cp index.html index.html.backup-step-A-before-css
```

**2.2 查找CSS插入位置**：
```
grep 查找：/* ==================== 对话历史
或其他合适的位置
建议：在architect-module现有CSS之后添加
```

**2.3 提取和修改CSS**：
- 从UI演示文件提取CSS
- **为所有CSS选择器添加 `.architect-module` 前缀**
- 例如：`.review-card` → `.architect-module .review-card`

**2.4 使用search_replace插入CSS**：
```
使用search_replace工具，在找到的位置之前插入CSS
每次插入一个完整的CSS块
```

### 步骤3：添加HTML

**3.1 创建步骤备份**：
```bash
cp index.html index.html.backup-step-B-after-css
```

**3.2 查找HTML插入位置**：
```
grep 查找：<!-- Tab 3: 对话历史 -->
或：architect-conversations.*architect-tab-pane
```

**3.3 修改Tab ID和class**：
- 将 `id="code-review"` 改为 `id="architect-reviews"`
- 将 `class="tab-pane active"` 改为 `class="architect-tab-pane"`（去掉active）
- 将onclick函数名改为architect版本

**3.4 确保内容足够**：
- **至少8-10个卡片/事件**才能触发滚动
- 每个筛选状态至少2-3个示例
- 如果演示文件内容不够，复制更多示例卡片

**3.5 使用search_replace插入HTML**：
```
在找到的位置之前插入完整的Tab HTML
```

### 步骤4：添加Tab导航按钮

**4.1 查找导航栏位置**：
```
grep 查找：architect-tab-item.*认命指令
```

**4.2 在认命指令和对话历史之间插入**：
```html
<button class="architect-tab-item" onclick="switchArchitectTab('reviews')">
    代码审查
    <span class="architect-tab-badge">10</span>
</button>
```

### 步骤5：添加JavaScript函数

**5.1 创建步骤备份**：
```bash
cp index.html index.html.backup-step-C-after-html
```

**5.2 查找JS插入位置**：
```
grep 查找：function switchArchitectTab
在这个函数附近添加新函数
```

**5.3 添加筛选函数**（以代码审查为例）：
```javascript
// 筛选架构师代码审查
function filterArchitectReviews(status) {
    const architectModule = document.querySelector('.architect-module');
    if (!architectModule) return;
    
    architectModule.querySelectorAll('.review-filters .filter-chip').forEach(chip => {
        chip.classList.remove('active');
    });
    event.target.classList.add('active');

    const cards = architectModule.querySelectorAll('.review-card');
    cards.forEach(card => {
        if (status === 'all') {
            card.style.display = 'block';
        } else {
            const cardStatus = card.classList.contains('pending') ? 'pending' :
                              card.classList.contains('reviewing') ? 'reviewing' :
                              card.classList.contains('approved') ? 'approved' :
                              card.classList.contains('rejected') ? 'rejected' : '';
            
            if (cardStatus === status) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });
}
```

### 步骤6：应用血泪教训CSS

**6.1 查找Tab CSS位置**：
```
grep 查找：.architect-module.*tab-pane
```

**6.2 添加特殊滚动CSS**：
```css
/* 代码审查Tab特殊处理 - 应用血泪教训 */
.architect-module #architect-reviews {
    display: none;
    flex-direction: column;
}

.architect-module #architect-reviews.active {
    display: flex;
    flex-direction: column;
    height: 1200px;  /* ✅ 固定高度（血泪教训） */
    min-height: 0;   /* ✅ 关键属性 */
    overflow: hidden; /* ✅ 隐藏外层溢出 */
}
```

**6.3 确保内容容器有滚动CSS**：
```css
.architect-module .review-list-container {
    flex: 1;              /* ✅ 占满剩余空间（血泪教训） */
    overflow-y: auto;     /* ✅ 允许滚动 */
    min-height: 0;        /* ✅ 关键：允许flex子元素收缩 */
    max-height: 100%;     /* ✅ 限制最大高度 */
    padding: 40px 0 160px 40px;
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
}
```

**6.4 最终备份**：
```bash
cp index.html index.html.backup-architect-reviews-complete
```

### 步骤7：测试验证

**刷新浏览器**：http://localhost:8831

**验证清单**：
1. ✅ 架构师工作台Tab导航显示"代码审查"
2. ✅ 点击代码审查Tab可以切换
3. ✅ 显示统计栏（5个统计块）
4. ✅ 显示筛选按钮
5. ✅ **有滚动条可以滚动**
6. ✅ 筛选功能正常工作
7. ✅ 每个筛选状态都有滚动条

---

## 🔥 关键成功要素

### 1. 分步进行（最重要！）
- ✅ CSS → 测试 → HTML → 测试 → JS → 测试
- ✅ 每步之后刷新浏览器验证
- ✅ 有问题立即停止修复，不要继续

### 2. 使用正确的工具
- ✅ `search_replace` - 手动精确替换
- ✅ `read_file` - 分段读取大文件
- ✅ `grep` - 查找插入位置
- ❌ **禁止Python脚本**（会出现乱码）

### 3. 备份策略
- ✅ 总备份（开始前）
- ✅ 步骤备份（每步完成后）
- ✅ 最终备份（全部完成后）
- ✅ 命名清晰：`backup-step-A-before-css`

### 4. 内容要足够
- ✅ 至少8-10个卡片/事件
- ✅ 每个筛选状态2-3个示例
- ✅ 内容高度要超过1200px才能滚动

### 5. 血泪教训3要素
- ✅ Tab固定高度1200px
- ✅ Tab是flex容器
- ✅ 内容区flex:1 + overflow-y:auto + min-height:0

---

## 📚 参考成功案例

### 全栈工程师代码审查Tab（参考）
- **位置**: 8831 index.html 第11623行开始
- **CSS**: 第4085行开始的代码审查CSS
- **函数**: `filterReviews(status)` 第14443行
- **滚动设置**: 第3320行 `#engineer-reviews.active`

### 成功的血泪教训应用
- **文档**: `✅滚动条完全修复-左右双滚动-8831.md`
- **核心**: 3要素必须全部满足

---

## 🚀 开始第一句话

你好！我需要在架构师模块手动添加Tab（和全栈工程师一样的方式）。

**当前状态**：
- 测试环境：8831
- 工作目录：/Users/yalinwang/Desktop/任务所 1.8/taskflow-v1-2/taskflow-v1-2/dashboard-test-8831
- 目标文件：index.html
- 架构师模块当前Tab：事件流、认命指令、对话历史

**参考文件**：
- UI演示目录：/Users/yalinwang/Dropbox/UI演示文稿/
- 血泪教训文档：✅滚动条完全修复-左右双滚动-8831.md
- 成功案例：全栈工程师模块的代码审查Tab（第11623行）

**任务**：
1. 先查看UI演示文稿目录，了解有哪些架构师Tab演示文件
2. 从代码审查Tab开始添加
3. 在认命指令Tab之后，对话历史Tab之前插入
4. 应用血泪教训确保滚动条正常

**要求**：
- ✅ 每步之前先备份
- ✅ 使用search_replace工具手动替换（不用Python脚本）
- ✅ 所有CSS选择器添加 `.architect-module` 前缀
- ✅ Tab ID使用 `#architect-reviews`格式
- ✅ 应用血泪教训3要素（固定高度、flex容器、内容滚动）
- ✅ 确保内容足够（8-10个卡片）
- ✅ 每步后刷新浏览器验证

**步骤**：
1. 先查看UI演示文稿目录，列出可用文件
2. 读取对应的演示文件（分段读取）
3. 提取CSS并添加 `.architect-module` 前缀
4. 在index.html中找到正确位置插入CSS
5. 提取HTML并修改ID/class为architect版本
6. 在对话历史Tab之前插入HTML
7. 在Tab导航添加按钮
8. 添加筛选函数（architect版本）
9. 应用血泪教训CSS确保滚动
10. 测试验证

请先查看UI演示文稿目录，然后告诉我有哪些可用的架构师Tab演示文件。
```

---

## 📋 检查清单（给AI使用）

每完成一个Tab后，检查：

- [ ] CSS已添加且有 `.architect-module` 前缀
- [ ] HTML已添加且ID/class正确
- [ ] Tab导航按钮已添加
- [ ] JavaScript函数已添加
- [ ] 血泪教训3要素已应用
- [ ] 内容数量足够（8-10个）
- [ ] 刷新浏览器测试通过
- [ ] 滚动条出现且可以滚动
- [ ] 筛选功能正常工作
- [ ] 所有备份已创建

---

## 🎯 预期结果

完成后，架构师模块应该有：

1. ✅ 事件流
2. ✅ 认命指令
3. ✅ **代码审查**（新增，10个卡片）
4. ✅ **扫描任务**（新增，如果有）
5. ✅ 对话历史

每个新Tab都有：
- ✅ 统计栏/筛选器
- ✅ 滚动条正常
- ✅ 筛选功能正常
- ✅ 内容完整展示

---

## 🔗 相关文档

1. `✅滚动条完全修复-左右双滚动-8831.md` - 血泪教训
2. `📖手动添加代码审查Tab-详细步骤.md` - 添加步骤参考
3. 全栈工程师模块代码审查Tab - 成功实现参考

---

**准备好了吗？复制上面的提示词给新Cursor，开始添加架构师Tab！** 🚀

