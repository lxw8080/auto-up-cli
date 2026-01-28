@echo off
REM AI CLI 工具管理器打包脚本 (Windows)
REM 使用 PyInstaller 打包为可执行文件

echo ================================
echo AI CLI 工具管理器打包脚本
echo ================================
echo.

REM 检查 Python 是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

REM 检查 PyInstaller 是否已安装
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [INFO] 正在安装 PyInstaller...
    pip install pyinstaller
)

REM 切换到脚本目录
cd /d "%~dp0"

echo.
echo [INFO] 开始打包...
echo.

REM 执行打包
pyinstaller --onefile --windowed --name "AI-CLI-Manager" ^
    --add-data "config/tools.json;config" ^
    --noconfirm ^
    main.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    pause
    exit /b 1
)

echo.
echo ================================
echo [成功] 打包完成！
echo ================================
echo.
echo 可执行文件位置: dist\AI-CLI-Manager.exe
echo.
pause
