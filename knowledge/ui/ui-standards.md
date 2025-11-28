# UI设计规范

**创建时间**: 2025-11-19  
**项目**: 任务所·Flow v1.7  
**设计风格**: 工业美学 (Industrial Aesthetics)

---

## 设计语言

### 核心理念

**工业美学三要素**:
1. **简洁** - 去除一切装饰
2. **清晰** - 高对比度，易识别
3. **实用** - 功能至上，避免花哨

---

## 色彩系统

### 主色调

```css
/* 基础色 */
--black: #000000        /* 主色：边框、文字、按钮 */
--white: #FFFFFF        /* 背景、卡片 */
--bg: #FFFDF7          /* 页面背景（浅黄） */

/* 灰度 */
--gray-50: #fafafa
--gray-100: #f5f5f5
--gray-200: #eeeeee
--gray-300: #e0e0e0
--gray-400: #bdbdbd
--gray-500: #9e9e9e
--gray-600: #757575
--gray-700: #616161
--gray-800: #424242
--gray-900: #212121
```

### 功能色

```css
/* 分类色彩（用于标识不同类型） */
--architecture: #5d6d7e    /* 蓝灰 - 架构 */
--problem: #985239         /* 棕红 - 问题 */
--solution: #87a96b        /* 草绿 - 解决方案 */
--decision: #d4a373        /* 土黄 - 决策 */
--knowledge: #537696       /* 天蓝 - 知识 */

/* 状态色 */
--success: #2e7d32         /* 成功 - 深绿 */
--warning: #f57c00         /* 警告 - 橙色 */
--error: #d32f2f           /* 错误 - 红色 */
--info: #1976d2            /* 信息 - 蓝色 */
```

### 使用场景

**主色调**:
- 页面背景: `#FFFDF7`
- 卡片背景: `#FFFFFF`
- 主要文字: `#212121`
- 次要文字: `#616161`

**功能色**:
- 左侧边框标识分类
- 标签背景色
- 统计卡片强调色

---

## 字体系统

### 字体家族

```css
/* 等宽字体（用于代码、数据）*/
--font-mono: 'Consolas', 'Monaco', 'SF Mono', monospace;

/* 中文字体（用于标题、正文）*/
--font-chinese: 'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

### 字体大小

```css
/* 标题 */
--text-4xl: 42px    /* 页面主标题 */
--text-3xl: 32px    /* 区块标题 */
--text-2xl: 22px    /* 子标题 */
--text-xl: 18px     /* 卡片标题 */

/* 正文 */
--text-base: 14px   /* 正文 */
--text-sm: 13px     /* 小文本 */
--text-xs: 12px     /* 辅助文本 */
--text-2xs: 11px    /* 标签、元数据 */
--text-3xs: 10px    /* 极小文本 */
```

### 字重

```css
--font-normal: 400
--font-medium: 500
--font-semibold: 600
--font-bold: 700
```

---

## 布局系统

### 间距

```css
/* 内边距 */
--spacing-xs: 4px
--spacing-sm: 8px
--spacing-md: 12px
--spacing-lg: 16px
--spacing-xl: 20px
--spacing-2xl: 24px
--spacing-3xl: 32px

/* 外边距 */
--gap-sm: 8px
--gap-md: 16px
--gap-lg: 24px
--gap-xl: 32px
```

### 容器宽度

```css
--container-sm: 640px
--container-md: 768px
--container-lg: 1024px
--container-xl: 1280px
--container-2xl: 1600px
```

---

## 组件规范

### 按钮

```css
/* 主要按钮 */
.btn-primary {
    background: #000;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* 次要按钮 */
.btn-secondary {
    background: white;
    color: #000;
    border: 1px solid #000;
    padding: 10px 20px;
}
```

### 卡片

```css
.card {
    background: white;
    border: 1px solid #e0e0e0;
    border-left: 4px solid #9e9e9e;  /* 左侧色条标识分类 */
    padding: 20px;
}
```

### 输入框

```css
.input {
    padding: 10px 12px;
    border: 1px solid #bdbdbd;
    background: #fafafa;
    font-family: 'Consolas', monospace;
}

.input:focus {
    outline: none;
    border-color: #000;
    background: white;
}
```

---

## 交互反馈

### 悬停效果

```css
/* 按钮悬停 */
.btn:hover {
    background: #424242;  /* 变深 */
}

/* 卡片悬停 */
.card:hover {
    border-left-width: 8px;  /* 左侧条加粗 */
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
```

### 点击反馈

```css
/* 按钮点击 */
.btn:active {
    transform: translateY(1px);
}

/* 复制成功 */
.btn.success {
    background: #2e7d32;
    color: white;
}
```

---

## 响应式设计

### 断点

```css
/* 移动端 */
@media (max-width: 768px) {
    /* 单列布局 */
    /* 字体略小 */
    /* 间距减半 */
}

/* 桌面端 */
@media (min-width: 769px) {
    /* 多列布局 */
    /* 正常字体 */
    /* 标准间距 */
}
```

---

## 待完善内容

- [ ] 组件库详细规范
- [ ] 动画效果指南
- [ ] 图标系统
- [ ] 暗色模式

---

**更新时间**: 2025-11-19  
**维护者**: AI 架构师

