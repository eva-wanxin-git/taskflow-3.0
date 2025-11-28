#!/bin/bash
# 📦 打包Dashboard项目传输到新电脑
# 执行方式：bash 📦打包传输到新电脑.sh

echo "=========================================="
echo "📦 任务所·Flow Dashboard 打包脚本"
echo "=========================================="
echo ""

# 进入项目根目录
cd "$(dirname "$0")"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

echo "Step 1: 创建打包目录..."
PACKAGE_DIR="dashboard-package-${TIMESTAMP}"
mkdir -p "$PACKAGE_DIR"
echo "✅ 目录已创建: $PACKAGE_DIR"
echo ""

echo "Step 2: 复制dashboard-test目录..."
cp -r dashboard-test "$PACKAGE_DIR/"
echo "✅ dashboard-test已复制"
echo ""

echo "Step 3: 复制关键文档..."
cp 📋给新AI-全栈工程师任务看板标签换行问题.md "$PACKAGE_DIR/" 2>/dev/null
cp ✅今日工作总结-2025-11-21.md "$PACKAGE_DIR/" 2>/dev/null
cp 🚀换电脑部署-第一步提示词.md "$PACKAGE_DIR/" 2>/dev/null
cp 🎯复制给新Cursor-第一句话.txt "$PACKAGE_DIR/" 2>/dev/null
cp ⚠️CURSOR开始任务前必读.md "$PACKAGE_DIR/" 2>/dev/null
cp README.md "$PACKAGE_DIR/" 2>/dev/null
echo "✅ 关键文档已复制"
echo ""

echo "Step 4: 创建README..."
cat > "$PACKAGE_DIR/📖新电脑部署说明.txt" << 'EOF'
# 📖 新电脑部署说明

## 🚀 快速开始（3步）

### Step 1: 解压文件
把这个文件夹放到任意位置，比如桌面。

### Step 2: 进入dashboard-test目录
cd dashboard-test

### Step 3: 启动服务器
python3 -m http.server 8820

### Step 4: 打开浏览器
访问：http://localhost:8820/

---

## 📋 如果需要继续解决问题

打开Cursor，复制文件：
🎯复制给新Cursor-第一句话.txt

粘贴到Cursor对话框，发送。

---

## 📚 关键文档

- 🎯复制给新Cursor-第一句话.txt - 给Cursor的第一句话
- 📋给新AI-全栈工程师任务看板标签换行问题.md - 详细问题分析
- ✅今日工作总结-2025-11-21.md - 完整工作记录
- ⚠️CURSOR开始任务前必读.md - 工作规范

---

## 🌐 访问地址

http://localhost:8820/

如果8820被占用，可以换其他端口：
python3 -m http.server 8821
python3 -m http.server 8822
...

---

准备好了！开始部署！🚀
EOF

echo "✅ README已创建"
echo ""

echo "Step 5: 打包压缩..."
PACKAGE_FILE="Dashboard-传输包-${TIMESTAMP}.tar.gz"
tar -czf "$PACKAGE_FILE" "$PACKAGE_DIR"
PACKAGE_SIZE=$(du -h "$PACKAGE_FILE" | cut -f1)
echo "✅ 压缩包已创建: $PACKAGE_FILE"
echo "   大小: $PACKAGE_SIZE"
echo ""

echo "Step 6: 清理临时目录..."
rm -rf "$PACKAGE_DIR"
echo "✅ 临时目录已清理"
echo ""

echo "=========================================="
echo "✅ 打包完成！"
echo "=========================================="
echo ""
echo "📦 传输包："
echo "   文件: $PACKAGE_FILE"
echo "   大小: $PACKAGE_SIZE"
echo "   位置: $(pwd)/$PACKAGE_FILE"
echo ""
echo "🚀 下一步："
echo "1. 把 $PACKAGE_FILE 复制到新电脑"
echo "2. 在新电脑解压：tar -xzf $PACKAGE_FILE"
echo "3. 按照 📖新电脑部署说明.txt 操作"
echo ""
echo "💡 或者用网盘/U盘/网络传输都可以！"
echo ""

