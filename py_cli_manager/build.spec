# -*- mode: python ; coding: utf-8 -*-
"""
AI CLI 工具管理器 - PyInstaller 打包配置
支持 Windows 和 macOS 平台
使用方法:
  pyinstaller build.spec           # 当前平台
  pyinstaller build.spec --clean   # 清理后重新打包
"""

import sys
import os
import platform

block_cipher = None

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(SPEC))

# 平台检测
is_windows = platform.system() == 'Windows'
is_macos = platform.system() == 'Darwin'
is_linux = platform.system() == 'Linux'

# 图标文件路径
icon_path = None
if is_windows:
    icon_path = os.path.join(project_root, 'resources', 'icon.ico')
elif is_macos:
    icon_path = os.path.join(project_root, 'resources', 'icon.icns')
else:
    icon_path = os.path.join(project_root, 'resources', 'icon.png')

# 如果图标不存在，使用 None
if not os.path.exists(icon_path):
    icon_path = None

a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        ('config/tools.json', 'config'),
    ],
    hiddenimports=[
        'ttkbootstrap',
        'ttkbootstrap.constants',
        'ttkbootstrap.tooltip',
        'ttkbootstrap.style',
        'PIL',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'pytest',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AI-CLI-Manager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

# macOS 特定配置：创建 .app bundle
if is_macos:
    app = BUNDLE(
        exe,
        name='AI CLI Manager.app',
        icon=icon_path,
        bundle_identifier='com.aiclimanager.app',
        info_plist={
            'CFBundleName': 'AI CLI Manager',
            'CFBundleDisplayName': 'AI CLI 工具管理器',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13.0',
            'NSPrincipalClass': 'NSApplication',
        },
    )
