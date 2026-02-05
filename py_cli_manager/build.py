#!/usr/bin/env python3
"""
AI CLI 工具管理器 - 统一构建脚本
支持 Windows、macOS 和 Linux 平台

使用方法:
    python build.py               # 构建当前平台
    python build.py --clean       # 清理后重新构建
    python build.py --installer   # 同时创建安装程序
    python build.py --help        # 显示帮助
"""

import argparse
import os
import shutil
import subprocess
import sys
import platform
from pathlib import Path


class Colors:
    """终端颜色代码"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_info(msg: str):
    print(f"{Colors.BLUE}[INFO]{Colors.END} {msg}")


def print_success(msg: str):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.END} {msg}")


def print_warning(msg: str):
    print(f"{Colors.YELLOW}[WARNING]{Colors.END} {msg}")


def print_error(msg: str):
    print(f"{Colors.RED}[ERROR]{Colors.END} {msg}")


def print_header(msg: str):
    print()
    print("=" * 40)
    print(msg)
    print("=" * 40)
    print()


class BuildConfig:
    """构建配置"""
    APP_NAME = "AI-CLI-Manager"
    VERSION = "1.0.0"
    SPEC_FILE = "build.spec"

    # 平台特定配置
    IS_WINDOWS = platform.system() == 'Windows'
    IS_MACOS = platform.system() == 'Darwin'
    IS_LINUX = platform.system() == 'Linux'

    # 输出文件
    if IS_WINDOWS:
        EXE_NAME = "AI-CLI-Manager.exe"
        INSTALLER_NAME = f"AI-CLI-Manager-Setup-{VERSION}.exe"
        INSTALLER_SCRIPT = "installer.nsi"
        BUILD_SCRIPT = "build_windows.bat"
    elif IS_MACOS:
        EXE_NAME = "AI-CLI-Manager"
        APP_BUNDLE_NAME = "AI CLI Manager.app"
        DMG_NAME = f"AI-CLI-Manager-macOS-{VERSION}.dmg"
        BUILD_SCRIPT = "./build_macos.sh"
    else:
        EXE_NAME = "AI-CLI-Manager"
        BUILD_SCRIPT = "./build.sh"


class Builder:
    """构建器"""

    def __init__(self, args):
        self.args = args
        self.script_dir = Path(__file__).parent.absolute()
        self.dist_dir = self.script_dir / "dist"
        self.release_dir = self.script_dir / "release"
        self.build_dir = self.script_dir / "build"

    def run(self):
        """执行构建"""
        print_header("AI CLI 工具管理器 - 构建")

        # 检查依赖
        self.check_dependencies()

        # 清理
        if self.args.clean:
            self.clean()

        # 构建
        self.build_pyinstaller()

        # 创建安装程序
        if self.args.installer:
            self.create_installer()

        # 显示摘要
        self.show_summary()

    def check_dependencies(self):
        """检查依赖"""
        print_header("检查依赖")

        # 检查 Python
        py_version = sys.version.split()[0]
        print_info(f"Python 版本: {py_version}")
        if sys.version_info < (3, 9):
            print_warning("建议使用 Python 3.9+")

        # 检查 PyInstaller
        try:
            result = subprocess.run(
                [sys.executable, "-m", "PyInstaller", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print_info(f"PyInstaller 版本: {result.stdout.strip()}")
            else:
                raise FileNotFoundError
        except (FileNotFoundError, subprocess.SubprocessError):
            print_warning("PyInstaller 未安装，正在安装...")
            self.install_pyinstaller()

        # 检查平台特定工具
        if BuildConfig.IS_WINDOWS and self.args.installer:
            if self.check_command("makensis"):
                print_info("NSIS 已安装，将创建安装程序")
            else:
                print_warning("NSIS 未安装，跳过安装程序创建")
                self.args.installer = False

        if BuildConfig.IS_MACOS and self.args.installer:
            if self.check_command("create-dmg"):
                print_info("create-dmg 已安装")
            else:
                print_info("create-dmg 未安装，将使用 hdiutil")

    def install_pyinstaller(self):
        """安装 PyInstaller"""
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pyinstaller"]
        )
        print_success("PyInstaller 安装完成")

    def check_command(self, cmd: str) -> bool:
        """检查命令是否可用"""
        try:
            subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                shell=BuildConfig.IS_WINDOWS
            )
            return True
        except (FileNotFoundError, subprocess.SubprocessError):
            return False

    def clean(self):
        """清理构建文件"""
        print_info("清理旧的构建文件...")

        for dir_name in [self.build_dir, self.dist_dir, self.release_dir]:
            if dir_name.exists():
                shutil.rmtree(dir_name)
                print_info(f"  删除: {dir_name}")

        print_success("清理完成")

    def build_pyinstaller(self):
        """使用 PyInstaller 构建"""
        print_header("使用 PyInstaller 构建")

        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--noconfirm",
            BuildConfig.SPEC_FILE
        ]

        if self.args.clean:
            cmd.append("--clean")

        print_info(f"执行: {' '.join(cmd)}")

        result = subprocess.run(cmd, cwd=self.script_dir)

        if result.returncode != 0:
            print_error("PyInstaller 构建失败！")
            sys.exit(1)

        # 检查输出
        exe_path = self.dist_dir / BuildConfig.EXE_NAME
        if exe_path.exists():
            size = exe_path.stat().st_size
            size_mb = size / (1024 * 1024)
            print_success(f"可执行文件: {exe_path.name} ({size_mb:.1f} MB)")
        else:
            print_error("未找到可执行文件！")
            sys.exit(1)

        # 检查 .app bundle (macOS)
        if BuildConfig.IS_MACOS:
            app_path = self.dist_dir / BuildConfig.APP_BUNDLE_NAME
            if app_path.exists():
                print_success(f"应用包: {app_path.name}")

    def create_installer(self):
        """创建安装程序"""
        print_header("创建安装程序")

        self.release_dir.mkdir(exist_ok=True)

        if BuildConfig.IS_WINDOWS:
            self.create_windows_installer()
        elif BuildConfig.IS_MACOS:
            self.create_macos_dmg()
        else:
            print_info("Linux 平台: 可创建 .deb 或 .AppImage (未实现)")

    def create_windows_installer(self):
        """创建 Windows 安装程序"""
        installer_script = self.script_dir / BuildConfig.INSTALLER_SCRIPT
        if not installer_script.exists():
            print_error(f"未找到安装程序脚本: {installer_script}")
            return

        print_info("使用 NSIS 创建安装程序...")

        result = subprocess.run(
            ["makensis", str(installer_script)],
            cwd=self.script_dir
        )

        if result.returncode == 0:
            installer_path = self.release_dir / BuildConfig.INSTALLER_NAME
            if installer_path.exists():
                size = installer_path.stat().st_size
                size_mb = size / (1024 * 1024)
                print_success(f"安装程序: {installer_path.name} ({size_mb:.1f} MB)")
        else:
            print_warning("NSIS 安装程序创建失败")

    def create_macos_dmg(self):
        """创建 macOS DMG"""
        print_info("创建 DMG 磁盘映像...")

        dmg_path = self.release_dir / BuildConfig.DMG_NAME

        # 使用 build_macos.sh 脚本
        if (self.script_dir / "build_macos.sh").exists():
            subprocess.run(["bash", "build_macos.sh"], cwd=self.script_dir)
        else:
            # 直接使用 hdiutil 创建
            self.create_dmg_with_hdiutil(dmg_path)

        if dmg_path.exists():
            size = dmg_path.stat().st_size
            size_mb = size / (1024 * 1024)
            print_success(f"DMG: {dmg_path.name} ({size_mb:.1f} MB)")

    def create_dmg_with_hdiutil(self, dmg_path: Path):
        """使用 hdiutil 创建 DMG"""
        # 实现简化版 DMG 创建
        temp_dmg = self.script_dir / "temp.dmg"
        source = self.dist_dir / BuildConfig.APP_BUNDLE_NAME

        if not source.exists():
            source = self.dist_dir / BuildConfig.EXE_NAME

        if not source.exists():
            print_warning("未找到可分发的文件")
            return

        # 创建临时 DMG
        subprocess.run([
            "hdiutil", "create",
            "-volname", BuildConfig.APP_NAME,
            "-srcfolder", str(self.dist_dir),
            "-ov", "-format", "UDZO",
            str(dmg_path)
        ])

    def show_summary(self):
        """显示构建摘要"""
        print_header("构建完成")

        print("输出文件:")

        # 可执行文件
        exe_path = self.dist_dir / BuildConfig.EXE_NAME
        if exe_path.exists():
            print(f"  可执行: dist/{BuildConfig.EXE_NAME}")

        # macOS .app
        if BuildConfig.IS_MACOS:
            app_path = self.dist_dir / BuildConfig.APP_BUNDLE_NAME
            if app_path.exists():
                print(f"  应用包: dist/{BuildConfig.APP_BUNDLE_NAME}")

        # 安装程序
        if self.args.installer:
            if BuildConfig.IS_WINDOWS:
                installer = self.release_dir / BuildConfig.INSTALLER_NAME
                if installer.exists():
                    print(f"  安装程序: release/{BuildConfig.INSTALLER_NAME}")
            elif BuildConfig.IS_MACOS:
                dmg = self.release_dir / BuildConfig.DMG_NAME
                if dmg.exists():
                    print(f"  DMG: release/{BuildConfig.DMG_NAME}")

        print()
        print_info(f"平台: {platform.system()} {platform.machine()}")
        print_info(f"版本: {BuildConfig.VERSION}")


def main():
    parser = argparse.ArgumentParser(
        description="AI CLI 工具管理器 - 统一构建脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python build.py               # 构建当前平台
  python build.py --clean       # 清理后重新构建
  python build.py --installer   # 同时创建安装程序
  python build.py --all         # 清理构建并创建安装程序
        """
    )

    parser.add_argument(
        "--clean",
        action="store_true",
        help="清理旧的构建文件"
    )
    parser.add_argument(
        "--installer",
        action="store_true",
        help="创建安装程序 (需要 NSIS 或 create-dmg)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="等同于 --clean --installer"
    )

    args = parser.parse_args()

    if args.all:
        args.clean = True
        args.installer = True

    builder = Builder(args)
    builder.run()


if __name__ == "__main__":
    main()
