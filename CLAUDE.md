# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ai-cli-manager** is a cross-platform Node.js tool that manages installation and upgrades for 15+ AI programming CLI tools. It provides an interactive menu system and command-line interface for managing tools like Gemini CLI, Claude Code, GitHub Copilot CLI, Continue, Aider, and more.

- **Version**: 1.2.1
- **Main Language**: JavaScript (Node.js)
- **Platforms**: Windows, macOS (Intel & Apple Silicon), Linux (x64 & ARM64)
- **Node.js Version**: >=14.0.0
- **Single Dependency**: `chalk` (for colored terminal output)
- **Key Feature**: Quick Mode for fast tool list display (no verification) with optional Verification Mode toggle

## Architecture

### Core Files
- **`ai-cli-manager.js`** (613 lines) - Main Node.js application containing all logic
- **`ai-cli-manager.sh`** - Shell wrapper for macOS/Linux with dependency checking
- **`install-dependencies.sh`** - Automated dependency installer for macOS/Linux
- **Windows Scripts**: `.bat` and `.ps1` equivalents for Windows users

### Code Structure
The application follows a single-file architecture with these key sections:

1. **Tool Configuration** (lines 13-113) - `CLI_TOOLS` object defining all managed tools with:
   - Package names (npm registry)
   - Display names
   - Categories (AI助手, AI编程助手, 代码安全, Git工具)
   - Special notes (e.g., "需要GitHub Copilot订阅")

2. **Version Management Functions**:
   - `getInstalledVersion()` - Checks installed version via `npm list -g`
   - `getLatestVersion()` - Gets latest version via `npm view`
   - `installPackage()` - Performs npm install/upgrade with version comparison

3. **Interactive Mode** (lines ~200-450) - Full terminal UI with:
   - `interactiveMode()` - Main menu system
   - `displayMainMenu()` - Operation selection (upgrade selected, all, status, exit)
   - `displayToolSelectionMenu()` - Multi-select tool picker with keyboard controls
   - **Verification Modes**:
     - Quick Mode (default) - Fast display without version verification
     - Verification Mode - Shows installation status and versions (slower)
   - Readline-based input handling

4. **Execution Modes**:
   - Interactive menu (default when no args)
   - Command-line mode (--all, --status, specific tool)
   - Batch mode via platform-specific scripts

### Tool Categories
The `CLI_TOOLS` object in `ai-cli-manager.js:13-113` organizes 15+ tools:
- **AI助手**: gemini-cli, claude-code, codex, auggie, copilot-cli
- **AI编程助手**: continue, codegpt, tabnine, opencommit, aider, qwen-code, kilo-code
- **代码安全**: gitleaks
- **Git工具**: gitmoji-cli

## Common Commands

### Running the Tool
```bash
# Interactive mode (recommended)
node ai-cli-manager.js
./ai-cli-manager.sh  # macOS/Linux

# Upgrade all tools
node ai-cli-manager.js --all

# View all tools status
node ai-cli-manager.js --status

# Upgrade specific tool
node ai-cli-manager.js gemini-cli
node ai-cli-manager.js claude-code

# Show help
node ai-cli-manager.js --help
```

### Development & Testing
```bash
# Install dependencies (only chalk is required)
npm install

# Run directly
node ai-cli-manager.js

# Install globally (optional)
npm install -g

# Test on different platforms
./ai-cli-manager.sh                    # macOS/Linux
一键升级AI-CLI工具.bat                  # Windows (double-click)
```

### Platform-Specific Setup
```bash
# macOS/Linux - make scripts executable
chmod +x ai-cli-manager.sh
chmod +x install-dependencies.sh

# Windows - run as administrator if needed
# Just double-click the .bat file
```

## Key Functions

### Core Logic Functions
- **`checkTool(toolKey, tool)`** (line ~190) - Checks single tool, installs if needed
- **`checkAllTools()`** (lines ~350-420) - Iterates through all tools non-interactively
- **`checkSingleTool(toolName)`** (lines ~420-450) - Command-line mode for specific tool
- **`upgradeSelectedTools(toolKeys)`** (lines 498-543) - Upgrades user-selected tools
- **`showAllToolsStatus()`** (lines 457-495) - Displays formatted status of all tools

### Interactive UI Functions
- **`interactiveMode()`** - Returns promise with user's menu selection
- **`displayMainMenu()`** - Shows main operation menu
- **`displayToolSelectionMenu()`** - Multi-select interface with keyboard shortcuts:
  - `[空格]` - Select/deselect tool
  - `[A]` - Select all
  - `[N]` - Select none
  - `[C]` - Toggle verification mode (show/hide installation status and versions)
  - `[Q]` - Back to main menu
  - `[Enter]` - Confirm selection

### Verification Modes
- **Quick Mode** (default) - Displays tool list without verification for fast response
- **Verification Mode** - Shows installation status and version information (slower due to npm queries)

## Platform Support

The tool uses platform-specific wrapper scripts:

| File | Windows | macOS | Linux | Purpose |
|------|---------|-------|-------|---------|
| ai-cli-manager.js | ✅ | ✅ | ✅ | Main logic (Node.js) |
| *.bat | ✅ | ❌ | ❌ | Windows batch wrapper |
| *.ps1 | ✅ | ❌ | ❌ | Windows PowerShell wrapper |
| *.sh | ❌ | ✅ | ✅ | Unix shell wrapper |

## Claude Code Settings

Located in `.claude/settings.local.json`:
- **Allowed**: `Bash(npm install:*)`, `Bash(node:*)`, `Bash(bash install-dependencies.sh --help:*)`, `Bash(bash:*)`, `WebSearch`
- **Permissions**: Full access to npm and bash commands for dependency management

## Development Notes

### No Build System
This is a **pure Node.js script** - no compilation, bundling, or transpilation required. Just edit `ai-cli-manager.js` and run.

### Adding New Tools
To add a new tool, edit the `CLI_TOOLS` object in `ai-cli-manager.js:13-113`:
```javascript
'new-tool': {
  name: 'new-tool',
  package: 'npm-package-name',
  displayName: 'Display Name',
  category: 'Category Name'
}
```

### Dependencies
Only one external dependency: **chalk** (for colored output). No test framework, linter, or build tools configured.

### Version Detection
Uses two npm commands:
- `npm list -g <package> --depth=0 --json` - Get installed version
- `npm view <package> version` - Get latest version

**Note**: Version detection is slow (requires multiple npm calls). The interactive tool selection menu now defaults to **Quick Mode** without verification, and allows users to toggle verification mode with the `[C]` key.

### Error Handling
- Graceful fallback to null for version detection failures
- Colored error messages using chalk
- Platform-specific error guidance (e.g., PowerShell execution policy on Windows)

## Important README Sections

The comprehensive README.md covers:
- **Supported Tools** (15+ AI CLI tools with npm package names)
- **Installation Methods** (direct Node.js, shell scripts, Windows batch files)
- **Platform Requirements** (Node.js 14+, npm 6+)
- **Troubleshooting** (Node.js detection, npm failures, script execution policies)
- **Usage Examples** (interactive menus, command-line usage, batch operations)
- **Chinese Documentation** - Fully localized for Chinese users

## Script Wrapper Logic

### Unix Wrapper (ai-cli-manager.sh)
```bash
# Checks for node_modules/chalk before running
# Auto-runs install-dependencies.sh if missing
# Delegates to: node ai-cli-manager.js "$@"
```

### Windows Wrappers
- **.bat** - Simple batch file calling Node.js
- **.ps1** - PowerShell version with better error handling
- Auto-check and install dependencies

## Summary Statistics Tracked
The tool tracks and displays:
- New installations (not previously installed)
- Upgrades (installed but outdated)
- Already latest (no upgrade needed)
- Total tools processed

All results shown with color-coded output and version comparisons.
