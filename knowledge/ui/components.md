# 组件库

**项目**: 任务所·Flow v1.7  
**设计风格**: 工业美学  
**创建时间**: 2025-11-19

---

## 按钮组件

### 主要按钮（Primary Button）

**样式**:
```css
background: #000;
color: white;
border: none;
padding: 10px 20px;
font-size: 12px;
text-transform: uppercase;
letter-spacing: 1px;
cursor: pointer;
transition: all 0.2s;
```

**使用场景**: 主要操作（刷新、确认、提交）

### 次要按钮（Secondary Button）

**样式**:
```css
background: white;
color: #000;
border: 1px solid #000;
padding: 10px 20px;
font-size: 12px;
```

**使用场景**: 辅助操作（取消、返回）

---

## 卡片组件

### 任务卡片

**特点**:
- 白色背景
- 1px浅灰边框
- 4px左侧色条（标识类型）
- 悬停效果：左侧条加粗到8px

```css
.task-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-left: 4px solid #537696;
    padding: 20px;
    cursor: pointer;
}

.task-card:hover {
    border-left-width: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
```

### 统计卡片

**特点**:
- 白色背景
- 顶部黑色粗线（3px）
- 大号数字 + 小号标签

```css
.stat-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-top: 3px solid #000;
    padding: 20px;
}
```

---

## 输入组件

### 文本输入框

**样式**:
```css
.input {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #bdbdbd;
    background: #fafafa;
    font-family: 'Consolas', monospace;
    font-size: 13px;
}

.input:focus {
    outline: none;
    border-color: #000;
    background: white;
}
```

### 下拉选择器

**样式**:
```css
.select {
    padding: 10px 12px;
    border: 1px solid #bdbdbd;
    background: white;
    font-family: 'Consolas', monospace;
    font-size: 13px;
}

.select:focus {
    outline: none;
    border-color: #000;
}
```

---

## 标签组件

### 分类标签

**样式**:
```css
.badge {
    display: inline-block;
    padding: 4px 10px;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-radius: 2px;
}

/* 不同分类颜色 */
.badge-architecture { background: #e8eaf6; color: #3f51b5; }
.badge-problem { background: #ffe0b2; color: #e65100; }
.badge-solution { background: #e8f5e9; color: #2e7d32; }
```

---

## 列表组件

### 文件树（参考Dify）

**特点**:
- 左侧边栏（320px宽）
- 缩进展示层级（20px/层）
- 折叠/展开图标（▶/▼）
- 图标 + 标签 + 计数

```css
.tree-node-header {
    display: flex;
    align-items: center;
    padding: 8px 20px;
    cursor: pointer;
}

.tree-node-header:hover {
    background: #f5f5f5;
}

.tree-node-header.active {
    background: #000;
    color: white;
}
```

---

## 模态框组件

### 弹窗（Modal）

**样式**:
```css
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.5);
    z-index: 1000;
}

.modal-content {
    max-width: 700px;
    margin: 40px auto;
    background: white;
    border-radius: 8px;
    padding: 32px;
}
```

---

## 待完善

- [ ] 表单组件详细规范
- [ ] 表格组件
- [ ] 分页组件
- [ ] 加载动画

---

**更新时间**: 2025-11-19  
**维护者**: AI 架构师

