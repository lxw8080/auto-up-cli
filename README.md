# AI CLI工具一键升级管理器 v1.2.1

一个跨平台（Windows/macOS/Linux）的AI CLI工具管理器，支持统一管理和升级多个AI CLI工具。

## 支持的工具

### 🤖 AI助手
- **Gemini CLI** (`@google/gemini-cli`) - Google的Gemini AI命令行工具
- **Claude Code** (`@anthropic-ai/claude-code`) - Anthropic的Claude代码助手
- **Codex CLI** (`@openai/codex`) - OpenAI的Codex命令行工具
- **Auggie CLI** (`@augmentcode/auggie`) - Augment的AI编程助手
- **iFlow CLI** (`@iflow-ai/iflow-cli`) - iFlow AI命令行工具
- **Grok CLI** (`@vibe-kit/grok-cli`) - Grok AI命令行工具
- **GitHub Copilot CLI** (`@github/copilot-cli`) - GitHub官方AI编程助手 ⭐

### 👨‍💻 AI编程助手
- **Continue CLI** (`@continue.dev/cli`) - 专业的AI结对编程助手
- **CodeGPT CLI** (`codegpt-cli`) - CodeGPT命令行工具
- **Tabnine CLI** (`@tabnine/cli`) - Tabnine AI代码补全CLI
- **OpenCommit** (`opencommit-cli`) - AI驱动的Git提交信息生成
- **Aider** (`aider-chat`) - 终端中的AI编程助手
- **OpenCode** (`opencode-ai`) - OpenCode AI编程工具
- **Qwen2.5 Coder** (`qwen2.5-coder`) - 阿里通义千问2.5 Coder模型
- **Kilo Code CLI** (`kilo-code-cli`) - Kilo Code AI编程工具
- **Qoder** (`@qoder-ai/qodercli`) - Qoder AI编程助手

### 🔐 代码安全
- **GitLeaks** (`gitleaks`) - Git提交中的敏感信息检测

### 📝 Git工具
- **Gitmoji CLI** (`gitmoji-cli`) - Gitmoji命令行工具

*注：部分工具的包名可能需要确认，请注意状态提示*

## 功能特性

✅ **自动检测已安装的版本** - 智能检测当前版本和npm最新版本
✅ **升级前显示当前版本** - 升级前后版本对比清晰
✅ **升级后显示新版本** - 确认升级结果
✅ **交互式菜单模式** - 图形化界面选择要升级的工具
✅ **多选支持** - 可同时选择多个工具进行升级
✅ **全选/全不选功能** - 快速选择所有或取消所有工具
✅ **查看工具状态** - 一键查看所有工具的安装和版本状态
✅ **多种运行模式** - 交互式、命令行、批处理三种模式
✅ **美观的终端输出** - 彩色界面，升级统计报告
✅ **灵活的命令行参数** - 支持多种参数组合
✅ **跨平台支持** - Windows、macOS (Intel & Apple Silicon)、Linux
✅ **自动依赖检查** - 自动检查并安装所需依赖

## 平台支持

| 平台 | 架构 | 状态 | 脚本 |
|------|------|------|------|
| Windows 10/11 | x64/AMD64 | ✅ 完全支持 | `.bat` / `.ps1` |
| macOS | Intel (x64) | ✅ 完全支持 | `.sh` |
| macOS | Apple Silicon (ARM64) | ✅ 完全支持 | `.sh` |
| Linux | x64 | ✅ 完全支持 | `.sh` |
| Linux | ARM64 | ✅ 完全支持 | `.sh` |

## 首次使用（新设备）

### 在新设备上使用前的准备工作

#### Windows用户

**方法一：自动检查依赖（推荐）**
```bash
# 直接双击运行，脚本会自动检查并安装依赖
一键升级AI-CLI工具.bat
```

**方法二：手动安装依赖**
```bash
# 1. 安装Node.js (如果未安装)
#    访问: https://nodejs.org/

# 2. 运行依赖安装脚本
install-dependencies.bat
```

#### macOS/Linux用户

**方法一：自动检查依赖（推荐）**
```bash
# 1. 先给脚本执行权限
chmod +x ai-cli-manager.sh
chmod +x install-dependencies.sh

# 2. 运行脚本（会自动检查依赖）
./ai-cli-manager.sh
```

**方法二：手动安装依赖**
```bash
# 1. 安装Node.js (如果未安装)
#    macOS: brew install node
#    Ubuntu/Debian: sudo apt install nodejs npm

# 2. 给脚本执行权限
chmod +x install-dependencies.sh

# 3. 运行依赖安装脚本
./install-dependencies.sh
```

**方法三：直接使用Node.js**
```bash
# 1. 安装Node.js
# 2. 直接运行
node ai-cli-manager.js
```

## 快速开始

### Windows用户

#### 方式一：双击运行（推荐⭐）

1. 直接双击 `一键升级AI-CLI工具.bat` 文件
2. 或在PowerShell中运行：`一键升级AI-CLI工具.ps1`

#### 方式二：命令行运行

```bash
# 直接运行（会自动检查依赖）
node ai-cli-manager.js

# 安装为全局工具（可选）
npm install -g
ai-cli-manager
```

### macOS/Linux用户

#### 方式一：Shell脚本（推荐⭐）

```bash
# 给脚本执行权限（首次使用）
chmod +x ai-cli-manager.sh

# 运行脚本
./ai-cli-manager.sh
```

#### 方式二：命令行运行

```bash
# 直接运行Node.js脚本
node ai-cli-manager.js

# 安装为全局工具（可选）
npm install -g
ai-cli-manager
```

## 使用方法

### 方式一：交互式菜单（推荐 ⭐）

```bash
# 启动交互式菜单（最简单的方式）
node ai-cli-manager.js

# 或强制使用交互模式
node ai-cli-manager.js --interactive
node ai-cli-manager.js -i
```

交互式菜单功能：
- 📋 **主菜单** - 选择操作模式
  - `[1]` 交互式选择工具
  - `[2]` 全部升级
  - `[3]` 查看所有工具状态
  - `[0]` 退出

- 🔧 **工具选择菜单** - 选择要升级的工具
  - `[空格]` 选择/取消工具
  - `[回车]` 确认选择
  - `[A]` 全选所有工具
  - `[N]` 全不选
  - `[C]` 切换验证模式（显示/隐藏安装状态和版本）
  - `[Q]` 返回主菜单

- ⚡ **快速模式 vs 验证模式**：
  - **快速模式**（默认）- 快速显示工具列表，无需等待验证
  - **验证模式** - 显示每个工具的安装状态和版本信息（较慢）

### 方式二：命令行参数

```bash
# 升级所有工具（非交互模式）
node ai-cli-manager.js --all

# 查看所有工具状态
node ai-cli-manager.js --status

# 升级指定工具
node ai-cli-manager.js gemini-cli
node ai-cli-manager.js claude-code
node ai-cli-manager.js codex
node ai-cli-manager.js auggie

# 查看帮助
node ai-cli-manager.js --help
node ai-cli-manager.js -h
```

### 方式三：双击运行

```bash
# 批处理文件方式（推荐）
双击 一键升级AI-CLI工具.bat

# PowerShell方式
.\一键升级AI-CLI工具.ps1
```

## 输出示例

### 交互式菜单示例

```bash
$ node ai-cli-manager.js

╔══════════════════════════════════════════════════════════╗
║              AI CLI 工具管理器 v1.1.0                     ║
║                                                          ║
║  请选择操作模式:                                         ║
║                                                          ║
║  [1] 交互式选择工具（推荐）                               ║
║  [2] 全部升级（自动检测并升级所有工具）                   ║
║  [3] 查看所有工具状态                                     ║
║  [0] 退出                                                ║
╚══════════════════════════════════════════════════════════╝

请选择 [0-3]: 1

═══════════════════════════════════════════
选择要安装/升级的工具
═══════════════════════════════════════════

  [1] Gemini CLI v0.13.0 已是最新
  [2] Claude Code v2.0.36 已是最新
  [3] Codex CLI v0.56.0 已是最新
  [4] Auggie CLI v0.7.0 已是最新

操作:
  [空格] 选择/取消 | [回车] 确认选择 | [A] 全选 | [N] 全不选 | [Q] 返回

请操作: 2 4
 ✓ [2] Claude Code v2.0.36 已是最新
   [3] Codex CLI v0.56.0 已是最新
 ✓ [4] Auggie CLI v0.7.0 已是最新

请操作: [回车]

════════════════════════════════════════
开始升级选定的工具
════════════════════════════════════════

检查 Claude Code...
✓ Claude Code: 已是最新版本 (2.0.36)

检查 Auggie CLI...
✓ Auggie CLI: 已是最新版本 (0.7.0)

═══════════════════════════════════════
升级总结
═══════════════════════════════════════

✓ Claude Code: 已是最新版本 (2.0.36)
✓ Auggie CLI: 已是最新版本 (0.7.0)

统计:
  新安装: 0
  已升级: 0
  已是最新: 2
  选中的工具总数: 2
```

### 命令行模式示例

```
╔════════════════════════════════════════╗
║        AI CLI 工具管理器 v1.0.0         ║
║                                        ║
║  管理: gemini-cli, claude-code,        ║
║        codex, auggie                   ║
╚════════════════════════════════════════╝

检查 Gemini CLI...
已安装 - 当前版本: 1.0.0
已是最新版本

检查 Claude Code...
已安装 - 当前版本: 0.5.2
发现新版本: 0.5.3
正在安装/升级 Claude Code...
✓ Claude Code 安装完成
✓ 新版本: 0.5.3

检查 Codex CLI...
未安装
正在安装/升级 Codex CLI...
✓ Codex CLI 安装完成
✓ 新版本: 1.2.0

检查 Auggie CLI...
已安装 - 当前版本: 2.1.0
已是最新版本

═══════════════════════════════════════
升级总结
═══════════════════════════════════════

✓ Gemini CLI: 已是最新版本 (1.0.0)
↑ Claude Code: 已升级到 0.5.3
↓ Codex CLI: 已安装 1.2.0
✓ Auggie CLI: 已是最新版本 (2.1.0)

统计:
  新安装: 1
  已升级: 1
  已是最新: 2
  总计: 4
```

## 系统要求

### 通用要求
- **Node.js**: 14.0.0 或更高版本
- **npm**: 6.0.0 或更高版本

### Windows
- **操作系统**: Windows 10/11 (x64/AMD64)
- **额外软件**: 无需额外软件

### macOS
- **操作系统**: macOS 10.15 (Catalina) 或更高版本
- **支持架构**:
  - Intel (x64)
  - Apple Silicon (ARM64/M1/M2/M3)
- **包管理器 (可选)**: [Homebrew](https://brew.sh/)

### Linux
- **发行版**: Ubuntu 18.04+, Debian 10+, CentOS 7+, Fedora 30+
- **支持架构**: x64, ARM64
- **包管理器**: apt, yum, dnf (取决于发行版)

## 安装Node.js

### Windows/macOS
访问 [nodejs.org](https://nodejs.org/) 下载并安装Node.js (推荐LTS版本)

### macOS (使用Homebrew)
```bash
brew install node
```

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install nodejs npm
```

### Fedora/CentOS/RHEL
```bash
# Fedora
sudo dnf install nodejs npm

# CentOS/RHEL
sudo yum install nodejs npm
```

### 验证安装
```bash
node --version
npm --version
```

## 注意事项

### 通用注意事项
1. **依赖检查**: 工具会自动检查并安装chalk依赖（用于美化输出）
2. **网络问题**: 如果npm安装速度慢，可以使用国内镜像源：
   ```bash
   npm config set registry https://registry.npmmirror.com
   ```
3. **API密钥**: 升级完成后，需要配置相应的API密钥才能使用这些AI工具

### Windows用户
1. **权限问题**: 如果遇到权限错误，需要以管理员身份运行批处理文件
2. **PowerShell策略**: 如果PowerShell脚本无法运行，检查执行策略：
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. **脚本文件**: 推荐使用 `.bat` 文件，比 `.ps1` 更简单

### macOS/Linux用户
1. **脚本权限**: 首次使用需要给脚本添加执行权限：
   ```bash
   chmod +x ai-cli-manager.sh
   chmod +x install-dependencies.sh
   ```
2. **权限问题**: 如果遇到权限错误，使用 `sudo`:
   ```bash
   sudo npm install -g <package-name>
   ```
3. **终端支持**: 确保终端支持UTF-8编码（现代终端默认支持）

## 故障排除

### 问题1: 提示"未检测到Node.js"

**解决方案**:
- 确保已安装Node.js
- 重新打开命令提示符/PowerShell
- 检查环境变量PATH是否包含Node.js路径

### 问题2: npm安装失败

**解决方案**:
- 检查网络连接
- 使用国内镜像源：
  ```bash
  npm config set registry https://registry.npmmirror.com
  ```
- 以管理员身份运行

### 问题3: 脚本无法执行

**解决方案**:
- 检查PowerShell执行策略：
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- 或直接使用批处理文件(.bat)

## 文件说明

### 核心文件
- `ai-cli-manager.js` - 主程序文件（Node.js脚本，跨平台）
- `package.json` - npm包配置文件

### Windows脚本
- `一键升级AI-CLI工具.bat` - Windows批处理脚本（推荐Windows用户使用）
- `一键升级AI-CLI工具.ps1` - PowerShell脚本（Windows用户备选）
- `install-dependencies.bat` - Windows依赖安装脚本

### macOS/Linux脚本
- `ai-cli-manager.sh` - Shell脚本（推荐macOS/Linux用户使用）
- `install-dependencies.sh` - Shell依赖安装脚本

### 依赖和文档
- `node_modules/` - 依赖包目录（首次运行后自动生成）
- `README.md` - 本说明文档

### 平台兼容性
| 文件 | Windows | macOS | Linux |
|------|---------|-------|-------|
| ai-cli-manager.js | ✅ | ✅ | ✅ |
| *.bat / *.ps1 | ✅ | ❌ | ❌ |
| *.sh | ❌* | ✅ | ✅ |
| install-dependencies.* | ✅ | ✅ | ✅ |

*注：Windows 10/11的WSL或Git Bash可以运行.sh脚本

## 许可证

MIT

## 更新日志

### v1.2.0 (当前版本)
#### ✨ 新增功能
- **新增快速模式** - 工具选择界面默认不验证状态，响应速度更快
- **新增验证模式切换** - 按 [C] 键可切换显示/隐藏工具安装状态和版本信息
- **优化用户体验** - 解决工具选择时长时间等待的问题

#### ⚡ 性能优化
- **延迟验证** - 工具列表展示不再自动验证版本，按需验证
- **用户选择** - 用户可自主选择是否需要查看详细的版本信息

### v1.1.0
#### ✨ 新增功能
- **新增交互式菜单模式** - 图形化选择要升级的工具
- **新增多选功能** - 可同时选择多个工具进行升级
- **新增全选/全不选** - 快捷键 [A] 全选，[N] 全不选
- **新增查看状态功能** - 一键查看所有工具的安装和版本状态
- **新增命令行参数** - 支持 `--interactive`, `--all`, `--status` 等参数
- **新增跨平台支持** - 支持macOS (Intel & Apple Silicon) 和 Linux
- **新增依赖安装脚本** - Windows和macOS/Linux独立的依赖安装脚本

#### 🎨 界面优化
- **优化菜单界面** - 彩色状态显示，升级前后版本对比
- **增强统计报告** - 显示选中的工具数量等更多信息
- **改进错误处理** - 更详细的错误提示和解决方案

#### 🔧 脚本增强
- **自动依赖检查** - 脚本自动检测并安装chalk依赖
- **更好的权限检查** - 针对不同平台的权限问题提供解决方案
- **Shell脚本支持** - 为macOS/Linux用户提供原生Shell脚本

### v1.0.0
- 初始版本
- 支持4个AI CLI工具的统一管理
- 支持版本检测和自动升级
- 美观的终端输出界面
- 支持单独升级指定工具
