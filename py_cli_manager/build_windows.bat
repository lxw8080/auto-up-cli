@echo off
REM ==============================================================================
REM AI CLI 工具管理器 - Windows 打包脚本
REM 功能:
REM   1. 使用 PyInstaller 创建单文件可执行程序
REM   2. 使用 NSIS 创建安装程序
REM ==============================================================================

setlocal enabledelayedexpansion

REM 配置
set APP_NAME=AI-CLI-Manager
set VERSION=1.0.0
set INSTALLER_NAME=AI-CLI-Manager-Setup-%VERSION%.exe

REM 获取脚本目录
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo ================================
echo AI CLI 工具管理器 - Windows 打包
echo ================================
echo.

REM ============================
REM 检查依赖
REM ============================
echo [INFO] 检查依赖...

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python 版本: %PYTHON_VERSION%

REM 检查 PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INFO] 正在安装 PyInstaller...
    pip install pyinstaller
)

for /f "tokens=2" %%i in ('pip show pyinstaller ^| findstr /i "Version"') do set PY_VER=%%i
echo [INFO] PyInstaller: !PY_VER!

REM 检查 NSIS (可选)
set HAS_NSIS=0
where makensis >nul 2>&1
if not errorlevel 1 (
    echo [INFO] NSIS 已安装，将创建安装程序
    set HAS_NSIS=1
) else (
    echo [WARNING] NSIS 未安装，跳过安装程序创建
    echo [INFO]   安装 NSIS: https://nsis.sourceforge.io/
)

echo.

REM ============================
REM 清理旧构建
REM ============================
echo [INFO] 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist release rmdir /s /q release
echo [INFO] 清理完成
echo.

REM ============================
REM 使用 PyInstaller 构建
REM ============================
echo ================================
echo [INFO] 使用 PyInstaller 构建...
echo ================================
echo.

pyinstaller --clean --noconfirm build.spec

if errorlevel 1 (
    echo.
    echo [错误] PyInstaller 构建失败！
    pause
    exit /b 1
)

if exist "dist\%APP_NAME%.exe" (
    echo.
    echo [成功] 可执行文件已创建: dist\%APP_NAME%.exe
) else (
    echo.
    echo [错误] 未找到可执行文件！
    pause
    exit /b 1
)

echo.

REM ============================
REM 创建 NSIS 安装程序
REM ============================
if %HAS_NSIS%==1 (
    echo ================================
    echo [INFO] 创建 NSIS 安装程序...
    echo ================================
    echo.

    REM 创建 release 目录
    if not exist release mkdir release

    REM 编译 NSIS 脚本
    makensis installer.nsi

    if errorlevel 1 (
        echo [警告] NSIS 安装程序创建失败
    ) else (
        echo [成功] 安装程序已创建: release\%INSTALLER_NAME%
    )
    echo.
)

REM ============================
REM 显示构建摘要
REM ============================
echo ================================
echo 构建完成
echo ================================
echo.
echo 输出文件:
if exist "dist\%APP_NAME%.exe" (
    for %%F in ("dist\%APP_NAME%.exe") do echo   可执行程序: dist\%APP_NAME%.exe (%%~zF 字节)
)
if exist "release\%INSTALLER_NAME%" (
    for %%F in ("release\%INSTALLER_NAME%") do echo   安装程序: release\%INSTALLER_NAME% (%%~zF 字节)
)
echo.

REM 询问是否运行
set /p RUN_APP="是否运行程序? (Y/N): "
if /i "%RUN_APP%"=="Y" (
    start "" "dist\%APP_NAME%.exe"
)

echo.
pause
