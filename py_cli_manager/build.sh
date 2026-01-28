#!/bin/bash
# AI CLI 工具管理器打包脚本 (macOS/Linux)
# 使用 PyInstaller 打包为可执行文件

echo "================================"
echo "AI CLI 工具管理器打包脚本"
echo "================================"
echo

# 检查 Python 是否可用
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python，请先安装 Python 3.9+"
    exit 1
fi

# 检查 PyInstaller 是否已安装
if ! pip3 show pyinstaller &> /dev/null; then
    echo "[INFO] 正在安装 PyInstaller..."
    pip3 install pyinstaller
fi

# 切换到脚本目录
cd "$(dirname "$0")"

echo
echo "[INFO] 开始打包..."
echo

# 执行打包
pyinstaller --onefile --windowed --name "AI-CLI-Manager" \
    --add-data "config/tools.json:config" \
    --noconfirm \
    main.py

if [ $? -ne 0 ]; then
    echo
    echo "[错误] 打包失败！"
    exit 1
fi

echo
echo "================================"
echo "[成功] 打包完成！"
echo "================================"
echo
echo "可执行文件位置: dist/AI-CLI-Manager"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS 应用: dist/AI-CLI-Manager.app"
fi
echo
