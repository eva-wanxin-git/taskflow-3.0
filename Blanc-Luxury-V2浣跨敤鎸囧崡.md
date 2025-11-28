# Blanc Luxury Edition V2 使用指南

## 🎨 设计特色

这是任务所·Flow的白色奢华版完整实现，基于您提供的设计原型和Blanc Luxury设计系统。

### 设计哲学
- **光的建筑学** (Light Architecture): 通过微妙的阴影层次创造空间深度
- **呼吸感设计** (Breathing Space): 大量留白，让界面自由呼吸  
- **触感视觉化** (Tactile Visualization): 模拟高端材质的细腻质感
- **减法美学** (Less is Luxury): 少即是奢华

---

## 🚀 快速启动

### 方式1: 使用启动脚本（推荐）

```bash
# 在项目根目录执行
./启动Blanc-Luxury-V2.sh
```

### 方式2: 直接运行Python

```bash
cd apps/dashboard
python3 start_blanc_luxury_v2.py
```

### 方式3: 指定端口（如果8879被占用）

```bash
cd apps/dashboard
python3 start_blanc_luxury_v2.py --port 8880
```

---

## 📊 功能特性

### ✅ 9个统计卡片

#### 现有6个（任务统计）
1. **总任务数** - 显示所有任务数量
2. **待处理** - 等待开始的任务
3. **进行中** - 正在执行的任务
4. **已完成** - 完成的任务
5. **已取消** - 取消的任务
6. **Token使用** - Token使用统计

#### 🆕 新增3个
7. **📊 事件数** - 系统事件总数，显示今日新增
8. **💬 会话** - 对话会话数量，显示消息总数
9. **💡 记忆** - 项目记忆数量，显示决策数

### 🎯 8个Tab切换

#### 现有5个（任务管理）
- 📋 **全部任务** - 显示所有任务
- ⏸️ **待处理** - 待开始的任务
- ▶️ **进行中** - 正在执行的任务
- ✅ **已完成** - 完成的任务
- ❌ **已取消** - 取消的任务

#### 🆕 新增3个
- 📊 **事件流** - 实时系统事件
- 💬 **对话历史** - AI对话会话
- 💡 **记忆空间** - 项目知识库

### 🔗 任务增强显示

每个任务卡片现在包含：

1. **AI协作链可视化**
   ```
   🤖 AI协作链: 后端AI → 集成AI → 架构师审查
   ```

2. **关联信息展示**
   ```
   📊 关联: 3事件 | 💬 1讨论 | 💡 1记忆
   ```

3. **操作按钮**
   - [复制提示词]
   - [查看事件]
   - [查看对话]
   - [查看记忆]

---

## 🌐 访问地址

启动成功后，访问以下地址：

- **主页**: http://127.0.0.1:8879/
- **Blanc V2页面**: http://127.0.0.1:8879/blanc-v2

---

## 🎨 UI设计细节

### 色彩系统

**白色基调 - 12级精密层次**
- `--blanc-pure: #FFFFFF` - 纯白（主背景）
- `--blanc-snow: #FAFBFC` - 雪白（卡片背景）
- `--blanc-pearl: #F6F8FA` - 珍珠白（区域背景）
- `--blanc-silk: #F0F3F5` - 丝绸白（次要背景）
- `--blanc-mist: #E8ECEF` - 薄雾白（分割线）
- `--blanc-cloud: #DFE4E8` - 云白（边框）

**灰色层次 - 文字与界面元素**
- `--noir-ink: #0A0F14` - 墨黑（主标题）
- `--noir-charcoal: #1A2027` - 炭黑（重要文字）
- `--noir-graphite: #2E3742` - 石墨（正文）
- `--noir-steel: #495057` - 钢铁灰（次要文字）
- `--noir-silver: #6C757D` - 银灰（辅助文字）
- `--noir-ash: #8B95A1` - 灰烬（提示文字）

**奢华点缀色**
- `--accent-gold: #D4AF37` - 香槟金
- `--accent-rose: #E8B4B8` - 玫瑰金
- `--accent-platinum: #E5E4E2` - 铂金

### 字体系统

- **主字体**: SF Pro Display, Helvetica Neue, PingFang SC
- **装饰字体**: Playfair Display, Georgia
- **等宽字体**: SF Mono, Monaco, Consolas

### 阴影系统

超细腻阴影，几乎不可见但能感知：
- `--shadow-xs`: 最轻微的阴影
- `--shadow-sm`: 卡片阴影
- `--shadow-md`: 悬停阴影
- `--shadow-lg`: 强调阴影

---

## 🔧 技术栈

- **后端**: FastAPI
- **前端**: 纯HTML + CSS + JavaScript
- **数据源**: StateManager + EventStreamProvider + ProjectMemoryProvider
- **端口**: 8879（独立端口，不影响其他版本）

---

## 📝 开发说明

### 文件结构

```
apps/dashboard/
├── start_blanc_luxury_v2.py          # 启动脚本
└── src/industrial_dashboard/
    └── templates_blanc_luxury_v2.py  # 模板文件
```

### 自定义路由

启动脚本在运行时动态注册了两个路由：
1. `/` - 默认路由（指向V2）
2. `/blanc-v2` - V2专属路由

### 数据提供器

模板需要3个数据提供器：
- `data_provider` - 任务数据（StateManagerAdapter）
- `event_provider` - 事件流数据（EventStreamProvider）
- `memory_provider` - 记忆数据（ProjectMemoryProvider）
- `conversations_provider` - 对话数据（可选）

---

## 🐛 故障排查

### 端口被占用

如果看到 "Address already in use" 错误：

```bash
# 检查端口占用
lsof -i :8879

# 或使用不同端口
python3 start_blanc_luxury_v2.py --port 8880
```

### 数据不显示

确保以下服务正在运行：
- StateManager（任务数据库）
- EventStreamProvider（事件流）
- ProjectMemoryProvider（记忆空间）

### 样式问题

清除浏览器缓存：
- Chrome: Cmd + Shift + R
- Firefox: Cmd + Shift + R
- Safari: Cmd + Option + R

---

## 📊 与其他版本对比

| 特性 | 标准版 (8877) | Blanc V1 (8878) | Blanc V2 (8879) |
|------|--------------|-----------------|-----------------|
| 统计卡片 | 6个 | 6个 | **9个** ✨ |
| Tab数量 | 5个 | 5个 | **8个** ✨ |
| 事件流 | ✅ | ✅ | ✅ |
| 对话历史 | ❌ | ❌ | **✅ ✨** |
| 记忆空间 | ❌ | ❌ | **✅ ✨** |
| AI协作链 | ❌ | ❌ | **✅ ✨** |
| 任务关联 | ❌ | ❌ | **✅ ✨** |
| 设计风格 | 工业美学 | Blanc Luxury | Blanc Luxury |

---

## 💡 使用建议

1. **浏览器选择**: 推荐使用最新版Chrome或Safari获得最佳体验
2. **屏幕分辨率**: 最佳体验分辨率为1400px及以上
3. **主题**: 当前仅支持浅色模式（深色模式计划中）
4. **性能**: 建议定期清理浏览器缓存

---

## 🎯 快捷键（计划中）

- `Cmd + K` - 快速搜索
- `Cmd + 1-8` - 切换Tab
- `Cmd + N` - 新建任务
- `Cmd + E` - 查看事件流
- `Cmd + M` - 查看记忆空间

---

## 📮 反馈与建议

如有任何问题或建议，请：
1. 查看日志文件（console输出）
2. 检查浏览器控制台
3. 提交Issue到项目仓库

---

## 🎉 享受使用！

Blanc Luxury Edition V2 是任务所·Flow的旗舰版本，融合了最先进的UI设计和最完整的功能。

**设计理念**: Less is Luxury - 少即是奢华

通过大量留白、微妙阴影和精致细节，创造出既现代又永恒的视觉体验。

---

*最后更新: 2025-11-19*
*版本: Blanc Luxury Edition V2*
*端口: 8879*

