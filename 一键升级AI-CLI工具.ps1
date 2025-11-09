# AI CLI工具一键升级管理器 PowerShell版本 v1.1.0

# 设置控制台编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║            AI CLI工具一键升级管理器 v1.1.0                ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 检查Node.js
try {
    $nodeVersion = node --version
    Write-Host "[信息] Node.js版本: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[错误] 未检测到Node.js，请先安装Node.js" -ForegroundColor Red
    Write-Host "下载地址: https://nodejs.org/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "或者运行依赖安装脚本:" -ForegroundColor Yellow
    Write-Host "  install-dependencies.bat" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "按任意键退出"
    exit 1
}

Write-Host ""

# 检查并安装chalk依赖
Write-Host "[步骤 1/2] 检查并安装依赖..." -ForegroundColor Blue
if (-not (Test-Path "node_modules\chalk")) {
    Write-Host "[提示] 正在安装chalk依赖包..." -ForegroundColor Yellow
    try {
        npm install chalk
        if ($LASTEXITCODE -ne 0) {
            throw "npm install failed"
        }
    } catch {
        Write-Host ""
        Write-Host "[错误] 安装chalk依赖失败" -ForegroundColor Red
        Write-Host ""
        Write-Host "可能的解决方案:" -ForegroundColor Yellow
        Write-Host "  1. 检查网络连接" -ForegroundColor White
        Write-Host "  2. 以管理员身份运行此脚本" -ForegroundColor White
        Write-Host "  3. 手动运行依赖安装脚本:" -ForegroundColor White
        Write-Host "     install-dependencies.bat" -ForegroundColor Cyan
        Write-Host "  4. 使用国内镜像源:" -ForegroundColor White
        Write-Host "     npm config set registry https://registry.npmmirror.com" -ForegroundColor Cyan
        Write-Host "     然后重新运行此脚本" -ForegroundColor White
        Write-Host ""
        Read-Host "按任意键退出"
        exit 1
    }
} else {
    Write-Host "[信息] 依赖检查完成 ✓" -ForegroundColor Green
}

# 运行主脚本
Write-Host "[步骤 2/2] 启动AI CLI工具升级管理器..." -ForegroundColor Blue
Write-Host ""
node ai-cli-manager.js

Write-Host ""
Read-Host "按任意键退出"
