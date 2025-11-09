#!/bin/bash

# AI CLI工具管理器 - 依赖安装脚本 (Mac/Linux)
# 版本: v1.0.0

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo ""
echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║            AI CLI工具管理器 - 依赖安装器 v1.0.0           ║${NC}"
echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 检查Node.js
echo -e "${BLUE}[步骤 1/3]${NC} 检查Node.js环境..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}[错误]${NC} 未检测到Node.js"
    echo ""
    echo "请先安装Node.js:"
    echo "  1. 访问 https://nodejs.org/"
    echo "  2. 下载并安装Node.js (推荐LTS版本)"
    echo "  3. 或使用包管理器安装:"
    echo "     • macOS (Homebrew): brew install node"
    echo "     • Ubuntu/Debian: sudo apt install nodejs npm"
    echo "  4. 安装完成后重新运行此脚本"
    echo ""
    exit 1
fi

NODE_VER=$(node --version)
echo -e "${GREEN}[信息]${NC} Node.js版本: ${NODE_VER} ✓"
echo ""

# 检查npm
echo -e "${BLUE}[步骤 2/3]${NC} 检查npm..."
if ! command -v npm &> /dev/null; then
    echo -e "${RED}[错误]${NC} npm未安装"
    exit 1
fi

NPM_VER=$(npm --version)
echo -e "${GREEN}[信息]${NC} npm版本: ${NPM_VER} ✓"
echo ""

# 安装依赖
echo -e "${BLUE}[步骤 3/3]${NC} 安装项目依赖..."
echo ""
echo -e "${YELLOW}正在安装chalk包（用于美化输出）...${NC}"
npm install chalk

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}[错误]${NC} 依赖安装失败"
    echo ""
    echo "可能的解决方案:"
    echo "  1. 检查网络连接"
    echo "  2. 使用国内镜像源:"
    echo "     npm config set registry https://registry.npmmirror.com"
    echo "     然后重新运行此脚本"
    echo "  3. 使用sudo (Linux/macOS):"
    echo "     sudo npm install chalk"
    echo ""
    exit 1
fi

echo ""
echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}║                    安装完成！${NC}"
echo -e "${CYAN}${BOLD}║${NC}"
echo -e "${CYAN}${BOLD}║  现在你可以使用以下方式运行管理器:${NC}"
echo -e "${CYAN}${BOLD}║${NC}"
echo -e "${CYAN}${BOLD}║  方法1: 命令行运行${NC}"
echo -e "${CYAN}${BOLD}║    → node ai-cli-manager.js${NC}"
echo -e "${CYAN}${BOLD}║${NC}"
echo -e "${CYAN}${BOLD}║  方法2: 安装为全局工具 (可选)${NC}"
echo -e "${CYAN}${BOLD}║    → npm install -g${NC}"
echo -e "${CYAN}${BOLD}║    → ai-cli-manager${NC}"
echo -e "${CYAN}${BOLD}║${NC}"
echo -e "${CYAN}${BOLD}║  方法3: 使用Shell脚本${NC}"
echo -e "${CYAN}${BOLD}║    → ./ai-cli-manager.sh${NC}"
echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 让脚本可执行
chmod +x ai-cli-manager.sh 2>/dev/null || true
