#!/bin/bash

# AI CLI工具管理器 (Mac/Linux版本)
# 版本: v1.2.1

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# 检查依赖
check_dependencies() {
    if [ ! -d "node_modules" ] || [ ! -d "node_modules/chalk" ]; then
        echo -e "${YELLOW}检测到缺少依赖，正在自动安装...${NC}"
        echo ""
        bash install-dependencies.sh
        if [ $? -ne 0 ]; then
            echo ""
            echo -e "${RED}依赖安装失败，请手动运行: bash install-dependencies.sh${NC}"
            exit 1
        fi
    fi
}

# 运行主程序
run_manager() {
    node ai-cli-manager.js "$@"
}

# 主函数
main() {
    # 检查是否在新设备上
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}首次运行，正在检查环境...${NC}"
        check_dependencies
    else
        # 检查chalk是否已安装
        if [ ! -d "node_modules/chalk" ]; then
            echo -e "${YELLOW}检测到缺少依赖，正在自动安装...${NC}"
            check_dependencies
        fi
    fi

    # 运行管理器
    run_manager "$@"
}

# 显示帮助
show_help() {
    echo -e "${BOLD}AI CLI工具管理器 v1.2.1${NC}"
    echo ""
    echo "用法:"
    echo -e "  ${CYAN}./ai-cli-manager.sh${NC}                # 启动交互式菜单（推荐）"
    echo -e "  ${CYAN}./ai-cli-manager.sh --interactive${NC}  # 强制使用交互式菜单"
    echo -e "  ${CYAN}./ai-cli-manager.sh --all${NC}          # 升级所有工具（非交互）"
    echo -e "  ${CYAN}./ai-cli-manager.sh --status${NC}       # 查看所有工具状态"
    echo -e "  ${CYAN}./ai-cli-manager.sh <tool-name>${NC}    # 升级指定工具"
    echo ""
    echo "工具名称:"
    echo "  gemini-cli, claude-code, codex, auggie"
    echo ""
    echo "示例:"
    echo -e "  ${YELLOW}./ai-cli-manager.sh${NC}                     # 交互式菜单"
    echo -e "  ${YELLOW}./ai-cli-manager.sh --all${NC}              # 升级所有工具"
    echo -e "  ${YELLOW}./ai-cli-manager.sh gemini-cli${NC}         # 只升级 gemini-cli"
    echo -e "  ${YELLOW}./ai-cli-manager.sh --status${NC}           # 查看状态"
    echo ""
    echo "交互模式快捷键:"
    echo "  [空格] 选择/取消工具 | [A] 全选 | [N] 全不选 | [C] 切换验证模式 | [Q] 返回 | [回车] 确认"
    echo ""
    echo "平台支持:"
    echo "  ✓ macOS (Intel & Apple Silicon)"
    echo "  ✓ Linux (x64 & ARM64)"
    echo "  ✓ Windows (通过WSL或Git Bash)"
    echo ""
}

# 处理参数
case "$1" in
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
