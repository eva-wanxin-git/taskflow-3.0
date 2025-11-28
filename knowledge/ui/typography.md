# 字体系统

**项目**: 任务所·Flow v1.7  
**设计风格**: 工业美学  
**创建时间**: 2025-11-19

---

## 字体家族

### 等宽字体（Monospace）

**用途**: 代码、数据、技术信息

```css
font-family: 'Consolas', 'Monaco', 'SF Mono', 'Courier New', monospace;
```

**使用场景**:
- 任务ID (TASK-001)
- Token使用量 (132,418/1,000,000)
- 时间戳 (2025-11-19 14:30)
- 代码块
- 数据表格

### 无衬线字体（Sans-serif）

**用途**: 标题、正文

```css
font-family: 'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

**使用场景**:
- 页面标题
- 模块标题
- 按钮文字
- 正文内容

---

## 字体大小体系

### 标题级别

```css
/* 特大标题 */
42px  /* 页面主标题，如："📊 事件流 · Event Stream" */
      font-weight: 700
      letter-spacing: -1px

/* 大标题 */
32px  /* 区块标题，如文档标题 */
      font-weight: 700
      
/* 中标题 */
22px  /* 子区块标题 */
      font-weight: 600

/* 小标题 */
18px  /* 卡片标题 */
      font-weight: 600
```

### 正文级别

```css
/* 标准正文 */
14px  /* 主要内容 */
      font-weight: 400
      line-height: 1.6

/* 小文本 */
13px  /* 次要内容 */
      font-weight: 400

/* 辅助文本 */
12px  /* 元数据、说明 */
      font-weight: 400-600

/* 标签文本 */
11px  /* 标签、图例 */
      font-weight: 600
      text-transform: uppercase
      letter-spacing: 1px

/* 极小文本 */
10px  /* Tag标签 */
      font-weight: 600
```

---

## 字重规范

```css
400  /* Normal - 正文 */
500  /* Medium - 强调 */
600  /* Semibold - 小标题 */
700  /* Bold - 大标题 */
```

---

## 特殊效果

### 大写字母

**使用场景**:
- 按钮文字
- 标签文字
- 模块标题副标题

```css
text-transform: uppercase;
letter-spacing: 1-2px;  /* 增加字间距提升可读性 */
```

### 字母间距

```css
/* 标题 */
letter-spacing: -1px    /* 紧凑，现代感 */

/* 大写文字 */
letter-spacing: 1-2px   /* 松散，清晰 */

/* 正文 */
letter-spacing: normal  /* 默认 */
```

---

## 行高规范

```css
/* 标题 */
line-height: 1.2-1.3

/* 正文 */
line-height: 1.6-1.8

/* 代码 */
line-height: 1.5
```

---

## 使用示例

### 页面标题

```html
<h1 style="
    font-size: 42px;
    font-weight: 700;
    color: #000;
    letter-spacing: -1px;
    font-family: 'Consolas', monospace;
">
    📊 事件流 · Event Stream
</h1>
```

### 模块标题

```html
<span style="
    font-size: 14px;
    font-weight: 700;
    color: #000;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
">
    ◆ 全栈开发工程师
</span>
```

### 标签文字

```html
<span style="
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #616161;
">
    ARCHITECTURE
</span>
```

---

**更新时间**: 2025-11-19  
**维护者**: AI 架构师

