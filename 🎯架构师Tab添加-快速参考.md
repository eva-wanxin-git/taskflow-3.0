# 🎯 架构师Tab添加 - 快速参考卡片

## 📋 完整提示词位置
- **详细版**: `📋给新Cursor-架构师模块添加Tab.md`
- **快速版**: `🔥给新Cursor-架构师Tab第一句话.txt`

---

## 🔑 关键成功因素

### 1. 命名规范对比

| 项目 | 全栈工程师 | 架构师 |
|------|-----------|--------|
| 模块前缀 | `.engineer-module` | `.architect-module` |
| Tab ID | `#engineer-reviews` | `#architect-reviews` |
| Tab class | `.tab-pane` | `.architect-tab-pane` |
| 导航按钮 | `.tab-item` | `.architect-tab-item` |
| 徽章 | `.tab-badge` | `.architect-tab-badge` |
| 切换函数 | `switchEngineerTab()` | `switchArchitectTab()` |

### 2. 血泪教训3要素

```css
/* 1. Tab固定高度 */
.architect-module #architect-reviews.active {
    height: 1200px;
    min-height: 0;
    overflow: hidden;
}

/* 2. Tab是flex容器 */
.architect-module #architect-reviews.active {
    display: flex;
    flex-direction: column;
}

/* 3. 内容区flex滚动 */
.architect-module .review-list-container {
    flex: 1;
    overflow-y: auto;
    min-height: 0;
    max-height: 100%;
}
```

### 3. 操作步骤

```
1. 总备份 → 
2. 添加CSS（加前缀）→ 
3. 添加HTML（改ID）→ 
4. 添加导航按钮 → 
5. 添加JS函数 → 
6. 应用血泪教训 → 
7. 测试验证
```

每步之间都要：
- ✅ 备份
- ✅ 刷新测试
- ✅ 确认无误再继续

---

## 📂 文件位置

### 工作目录
```
/Users/yalinwang/Desktop/任务所 1.8/taskflow-v1-2/taskflow-v1-2/dashboard-test-8831
```

### UI演示文件
```
/Users/yalinwang/Dropbox/UI演示文稿/
```

### 参考文档
- `✅滚动条完全修复-左右双滚动-8831.md`
- `📖手动添加代码审查Tab-详细步骤.md`

---

## 🎯 成功案例参考

**全栈工程师代码审查Tab**（第11623行）：
- ✅ 10个审查卡片
- ✅ 滚动条正常
- ✅ 筛选功能正常
- ✅ 所有状态都有内容

**完全可以复制这个结构到架构师模块！**

---

## ⚠️ 禁止事项

❌ 不要使用Python脚本（会乱码）  
❌ 不要一次性替换大段内容（容易出错）  
❌ 不要跳过备份步骤  
❌ 不要跳过测试验证  
❌ 不要忘记添加CSS前缀  
❌ 不要忘记应用血泪教训3要素  

---

## ✅ 必做事项

✅ 每步前都备份  
✅ 使用 `search_replace` 手动替换  
✅ CSS选择器全部加 `.architect-module` 前缀  
✅ 内容足够（8-10个卡片）  
✅ 应用血泪教训3要素  
✅ 每步后刷新浏览器测试  

---

## 🚀 开始命令

**复制这段话给新Cursor**：

```
请读取：
1. 📋给新Cursor-架构师模块添加Tab.md（完整步骤）
2. 🔥给新Cursor-架构师Tab第一句话.txt（快速启动）

然后开始在架构师模块添加Tab。
```

---

**准备就绪！复制提示词给新Cursor开始工作！** 🎯

