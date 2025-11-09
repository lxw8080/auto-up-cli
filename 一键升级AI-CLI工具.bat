@echo off
chcp 65001 >nul
title AI CLI工具一键升级管理器 v1.1.0

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║            AI CLI工具一键升级管理器 v1.1.0                ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: 检查Node.js是否安装
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Node.js，请先安装Node.js
    echo 下载地址: https://nodejs.org/
    echo.
    echo 或者运行依赖安装脚本:
    echo   install-dependencies.bat
    echo.
    pause
    exit /b 1
)

:: 显示Node.js版本
for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
echo [信息] Node.js版本: %NODE_VER%
echo.

:: 检查并安装chalk依赖
echo [步骤 1/2] 检查并安装依赖...
if not exist "node_modules\chalk" (
    echo [提示] 正在安装chalk依赖包...
    npm install chalk
    if %errorlevel% neq 0 (
        echo.
        echo [错误] 安装chalk依赖失败
        echo.
        echo 可能的解决方案:
        echo   1. 检查网络连接
        echo   2. 以管理员身份运行此脚本
        echo   3. 手动运行依赖安装脚本:
        echo      install-dependencies.bat
        echo   4. 使用国内镜像源:
        echo      npm config set registry https://registry.npmmirror.com
        echo      然后重新运行此脚本
        echo.
        pause
        exit /b 1
    )
) else (
    echo [信息] 依赖检查完成 ✓
)

:: 运行主脚本
echo [步骤 2/2] 启动AI CLI工具升级管理器...
echo.
node ai-cli-manager.js

:: 等待用户按键
echo.
pause
