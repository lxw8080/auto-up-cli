@echo off
chcp 65001 >nul
title 安装AI CLI工具管理器依赖

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║            AI CLI工具管理器 - 依赖安装器 v1.0.0           ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: 检查Node.js是否安装
echo [步骤 1/3] 检查Node.js环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Node.js
    echo.
    echo 请先安装Node.js:
    echo   1. 访问 https://nodejs.org/
    echo   2. 下载并安装Node.js (推荐LTS版本)
    echo   3. 安装完成后重新运行此脚本
    echo.
    pause
    exit /b 1
)

:: 显示Node.js版本
for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
echo [信息] Node.js版本: %NODE_VER% ✓
echo.

:: 检查npm是否安装
echo [步骤 2/3] 检查npm...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] npm未安装
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm --version') do set NPM_VER=%%i
echo [信息] npm版本: %NPM_VER% ✓
echo.

:: 安装依赖
echo [步骤 3/3] 安装项目依赖...
echo.
echo 正在安装chalk包（用于美化输出）...
npm install chalk

if %errorlevel% neq 0 (
    echo.
    echo [错误] 依赖安装失败
    echo.
    echo 可能的解决方案:
    echo   1. 检查网络连接
    echo   2. 使用国内镜像源:
    echo      npm config set registry https://registry.npmmirror.com
    echo      然后重新运行此脚本
    echo   3. 以管理员身份运行此脚本
    echo.
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                    安装完成！                              ║
echo ║                                                          ║
echo ║  现在你可以使用以下方式运行管理器:                        ║
echo ║                                                          ║
echo ║  方法1: 双击运行                                          ║
echo ║    → 一键升级AI-CLI工具.bat                               ║
echo ║                                                          ║
echo ║  方法2: 命令行运行                                        ║
echo ║    → node ai-cli-manager.js                              ║
echo ║                                                          ║
echo ║  方法3: 安装为全局工具 (可选)                             ║
echo ║    → npm install -g                                      ║
echo ║    → ai-cli-manager                                      ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

pause
