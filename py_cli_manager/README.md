# AI CLI 工具管理器

一个跨平台的 Python GUI 应用，用于检测、安装和升级 AI CLI 工具。

## 功能特性

- 🔍 **检测已安装工具**：自动检测本地已安装的 AI CLI 工具版本
- 📦 **版本检查**：从 npm registry 获取最新版本信息
- ⬆️ **一键升级**：快速升级到最新版本
- ➕ **新增工具**：支持添加自定义 AI CLI 工具
- 🖥️ **跨平台**：支持 Windows 和 macOS

## 预置工具

| 工具 | NPM 包名 |
|------|----------|
| Claude Code | @anthropic-ai/claude-code |
| Codex CLI | @openai/codex |
| Auggie CLI | @augmentcode/auggie |
| Gemini CLI | @google/gemini-cli |

## 系统要求

- Python 3.9+
- Node.js & npm（用于安装/升级工具）
- tkinter（Python 内置 GUI 库）

## 运行方式

### 方式一：直接运行

```bash
cd py_cli_manager
python main.py
```

### 方式二：打包后运行

**Windows:**

```bash
cd py_cli_manager
build.bat
# 运行 dist/AI-CLI-Manager.exe
```

**macOS/Linux:**

```bash
cd py_cli_manager
chmod +x build.sh
./build.sh
# 运行 dist/AI-CLI-Manager
```

## 项目结构

```
py_cli_manager/
├── main.py                 # 程序入口
├── config/
│   ├── __init__.py
│   ├── tools.json          # 工具配置文件
│   └── settings.py         # 应用设置
├── core/
│   ├── __init__.py
│   ├── detector.py         # 版本检测模块
│   ├── installer.py        # 安装/升级模块
│   └── platform_utils.py   # 跨平台工具
├── gui/
│   ├── __init__.py
│   ├── main_window.py      # 主窗口
│   ├── tool_list.py        # 工具列表组件
│   ├── add_tool_dialog.py  # 新增工具对话框
│   └── styles.py           # UI 样式定义
├── requirements.txt        # Python 依赖
├── build.spec              # PyInstaller 配置
├── build.bat               # Windows 打包脚本
└── build.sh                # macOS/Linux 打包脚本
```

## 使用说明

1. **刷新状态**：点击"刷新状态"按钮检测所有工具的安装情况
2. **安装/升级**：双击工具列表中的项目，或选中后点击"安装/升级选中"
3. **全部升级**：点击"全部升级"一键升级所有可升级的工具
4. **新增工具**：点击"新增工具"添加自定义 AI CLI 工具

## 许可证

MIT License
