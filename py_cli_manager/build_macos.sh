#!/bin/bash
# ==============================================================================
# AI CLI 工具管理器 - macOS 打包脚本
# 功能:
#   1. 使用 PyInstaller 创建单文件可执行程序
#   2. 创建 .app 应用包
#   3. 创建 DMG 磁盘映像安装包
# ==============================================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
APP_NAME="AI-CLI-Manager"
APP_BUNDLE_NAME="AI CLI Manager.app"
DMG_NAME="AI-CLI-Manager-macOS"
VERSION="1.0.0"

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "================================"
    echo "$1"
    echo "================================"
    echo ""
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查 Python 和 pip
check_dependencies() {
    print_header "检查依赖"

    if ! command_exists python3; then
        print_error "未找到 Python3，请先安装 Python 3.9+"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_info "Python 版本: $PYTHON_VERSION"

    # 检查 PyInstaller
    if ! python3 -m PyInstaller --version >/dev/null 2>&1; then
        print_warning "PyInstaller 未安装，正在安装..."
        pip3 install pyinstaller
    fi

    PYINSTALLER_VERSION=$(python3 -m PyInstaller --version)
    print_info "PyInstaller 版本: $PYINSTALLER_VERSION"

    # 检查 create-dmg (可选)
    if command_exists create-dmg; then
        print_info "create-dmg 已安装，将用于创建 DMG"
        HAS_CREATE_DMG=true
    else
        print_warning "create-dmg 未安装，将使用 hdiutil 创建 DMG"
        print_info "  安装: brew install create-dmg"
        HAS_CREATE_DMG=false
    fi
}

# 清理旧的构建文件
clean_build() {
    print_info "清理旧的构建文件..."
    rm -rf build dist
    print_success "清理完成"
}

# 使用 PyInstaller 构建
build_executable() {
    print_header "使用 PyInstaller 构建"

    # 构建选项
    PYINSTALLER_ARGS=(
        --clean
        --noconfirm
        build.spec
    )

    print_info "执行: pyinstaller ${PYINSTALLER_ARGS[*]}"
    python3 -m PyInstaller "${PYINSTALLER_ARGS[@]}"

    if [ -f "dist/$APP_NAME" ]; then
        print_success "可执行文件已创建: dist/$APP_NAME"
    elif [ -d "dist/$APP_BUNDLE_NAME" ]; then
        print_success "应用包已创建: dist/$APP_BUNDLE_NAME"
    else
        print_error "构建失败，未找到输出文件"
        exit 1
    fi
}

# 创建 DMG 磁盘映像
create_dmg() {
    print_header "创建 DMG 磁盘映像"

    local dmg_source="dist/$APP_BUNDLE_NAME"
    local dmg_output="release/$DMG_NAME-$VERSION.dmg"

    # 如果 .app 不存在，尝试使用可执行文件
    if [ ! -d "$dmg_source" ]; then
        if [ -f "dist/$APP_NAME" ]; then
            print_warning "未找到 .app bundle，将创建包含可执行文件的 DMG"
            dmg_source="dist/$APP_NAME"
        else
            print_error "未找到可分发的文件"
            exit 1
        fi
    fi

    # 创建 release 目录
    mkdir -p release

    # 删除旧的 DMG
    if [ -f "$dmg_output" ]; then
        rm -f "$dmg_output"
    fi

    # 使用 create-dmg (如果可用) 或 hdiutil
    if [ "$HAS_CREATE_DMG" = true ] && [ -d "dist/$APP_BUNDLE_NAME" ]; then
        # 使用 create-dmg
        create-dmg \
            --volname "$APP_NAME" \
            --window-pos 200 120 \
            --window-size 600 400 \
            --icon-size 100 \
            --app-drop-link 450 185 \
            --icon "$APP_BUNDLE_NAME" 150 185 \
            "$dmg_output" \
            "dist/" || {
            print_warning "create-dmg 失败，回退到 hdiutil"
            create_dmg_hdiutil
        }
    else
        create_dmg_hdiutil
    fi

    if [ -f "$dmg_output" ]; then
        local size=$(du -h "$dmg_output" | cut -f1)
        print_success "DMG 已创建: $dmg_output ($size)"
    fi
}

# 使用 hdiutil 创建 DMG
create_dmg_hdiutil() {
    print_info "使用 hdiutil 创建 DMG..."

    local dmg_output="release/$DMG_NAME-$VERSION.dmg"
    local temp_dmg="temp_$DMG_NAME.dmg"
    local mount_point="/tmp/$APP_NAME-mount"

    # 创建临时 DMG
    hdiutil create -volname "$APP_NAME" -size 100m -fs HFS+ -fsargs "-c c=64,a=16,e=16" -layout SPUD "$temp_dmg"

    # 挂载
    hdiutil attach "$temp_dmg" -readwrite -mountpoint "$mount_point"

    # 复制文件
    if [ -d "dist/$APP_BUNDLE_NAME" ]; then
        cp -R "dist/$APP_BUNDLE_NAME" "$mount_point/"
    elif [ -f "dist/$APP_NAME" ]; then
        cp "dist/$APP_NAME" "$mount_point/"
    fi

    # 创建 Applications 链接
    ln -s /Applications "$mount_point/Applications"

    # 卸载
    hdiutil detach "$mount_point"

    # 转换为压缩的 DMG
    hdiutil convert "$temp_dmg" -format UDZO -o "$dmg_output"

    # 清理
    rm -f "$temp_dmg"
}

# 显示构建摘要
show_summary() {
    print_header "构建完成"

    echo "输出文件:"
    echo "  可执行程序: dist/$APP_NAME"
    if [ -d "dist/$APP_BUNDLE_NAME" ]; then
        echo "  应用包: dist/$APP_BUNDLE_NAME"
    fi
    if [ -f "release/$DMG_NAME-$VERSION.dmg" ]; then
        local size=$(du -h "release/$DMG_NAME-$VERSION.dmg" | cut -f1)
        echo "  安装包: release/$DMG_NAME-$VERSION.dmg ($size)"
    fi
    echo ""
    print_info "安装方法: 双击 DMG 文件，拖拽应用到 Applications 文件夹"
}

# 主流程
main() {
    print_header "AI CLI 工具管理器 - macOS 打包"

    check_dependencies
    clean_build
    build_executable
    create_dmg
    show_summary
}

# 运行
main "$@"
