# 构建指南 / Build Guide

AI CLI 工具管理器支持 Windows 和 macOS 平台的封装打包。

## 快速开始

### 方式 1: 使用统一构建脚本 (推荐)

```bash
# Python 脚本 (所有平台)
python build.py               # 构建可执行文件
python build.py --installer   # 同时创建安装程序
python build.py --all         # 清理 + 构建 + 安装程序
```

### 方式 2: 使用平台特定脚本

**Windows:**
```cmd
build_windows.bat
```

**macOS / Linux:**
```bash
./build_macos.sh    # macOS (创建 DMG)
./build.sh          # Linux (仅可执行文件)
```

---

## Windows 平台构建

### 系统要求
- Python 3.9+
- Node.js (运行时需要)
- NSIS (可选，用于创建安装程序)

### 构建步骤

1. **安装 NSIS** (可选，用于创建安装程序)
   - 下载: https://nsis.sourceforge.io/
   - 安装后确保 `makensis` 命令可用

2. **运行构建脚本**
   ```cmd
   build_windows.bat
   ```

3. **输出文件**
   - `dist/AI-CLI-Manager.exe` - 单文件可执行程序
   - `release/AI-CLI-Manager-Setup-1.0.0.exe` - NSIS 安装程序

### NSIS 安装程序特性
- 向导式安装界面
- 开始菜单快捷方式
- 桌面快捷方式
- 注册到"添加/删除程序"
- 完整的卸载支持
- 中文/英文双语支持

---

## macOS 平台构建

### 系统要求
- Python 3.9+
- Node.js (运行时需要)
- Xcode Command Line Tools
- create-dmg (可选，用于美化 DMG)

### 构建步骤

1. **安装 create-dmg** (可选)
   ```bash
   brew install create-dmg
   ```

2. **赋予执行权限**
   ```bash
   chmod +x build_macos.sh
   ```

3. **运行构建脚本**
   ```bash
   ./build_macos.sh
   ```

4. **输出文件**
   - `dist/AI-CLI-Manager` - 单文件可执行程序
   - `dist/AI CLI Manager.app` - macOS 应用包
   - `release/AI-CLI-Manager-macOS-1.0.0.dmg` - 磁盘映像安装包

### macOS 应用包特性
- 原生 .app bundle 格式
- 支持双击启动
- 可拖拽安装到 Applications
- 支持高分辨率显示
- 最低系统版本: macOS 10.13+

---

## Linux 平台构建

### 系统要求
- Python 3.9+
- Node.js (运行时需要)

### 构建步骤

1. **赋予执行权限**
   ```bash
   chmod +x build.sh
   ```

2. **运行构建脚本**
   ```bash
   ./build.sh
   ```

3. **输出文件**
   - `dist/AI-CLI-Manager` - 单文件可执行程序

### 创建桌面快捷方式 (可选)
创建 `~/.local/share/applications/ai-cli-manager.desktop`:
```ini
[Desktop Entry]
Name=AI CLI Manager
Comment=AI CLI 工具管理器
Exec=/path/to/dist/AI-CLI-Manager
Icon=ai-cli-manager
Terminal=false
Type=Application
Categories=Development;Utility;
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| [build.spec](build.spec) | PyInstaller 打包配置文件 |
| [build.py](build.py) | 统一构建脚本 (Python) |
| [build_windows.bat](build_windows.bat) | Windows 构建脚本 |
| [build_macos.sh](build_macos.sh) | macOS 构建脚本 |
| [build.sh](build.sh) | Linux 构建脚本 |
| [installer.nsi](installer.nsi) | NSIS 安装程序脚本 |

---

## 图标设置

图标文件位于 `resources/` 目录:

- `icon.ico` - Windows 图标
- `icon.icns` - macOS 图标
- `icon.png` - Linux/通用图标

详见 [resources/README.md](resources/README.md)

---

## 故障排除

### Windows

**问题**: PowerShell 执行策略错误
```cmd
# 解决方案: 以管理员身份运行
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**问题**: 找不到 Python
```
# 解决方案: 确保 Python 已添加到 PATH
# 或使用完整路径: C:\Python39\python.exe build.py
```

### macOS

**问题**: 无法验证开发者
```
# 解决方案: 右键点击应用 -> 打开
# 或在终端运行: xattr -cr dist/AI\ CLI\ Manager.app
```

**问题**: 打开 DMG 显示"损坏"
```bash
# 解决方案: 移除隔离属性
xattr -d com.apple.quarantine AI-CLI-Manager-macOS-*.dmg
```

### 通用

**问题**: PyInstaller 打包失败
```bash
# 清理并重试
python build.py --all

# 或手动清理
rm -rf build dist release
```

**问题**: ttkbootstrap 主题丢失
```
# 检查 build.spec 中的 hiddenimports
hiddenimports=['ttkbootstrap', 'ttkbootstrap.constants', ...]
```

---

## 发布检查清单

在发布新版本前，请确保:

- [ ] 更新 [config/settings.py](config/settings.py) 中的版本号
- [ ] 更新 [build.spec](build.spec) 中的版本号
- [ ] 更新 [installer.nsi](installer.nsi) 中的版本号
- [ ] 在目标平台上测试构建
- [ ] 测试安装/卸载流程
- [ ] 测试核心功能 (检测、安装、升级)
- [ ] 准备发布说明
