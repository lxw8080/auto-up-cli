"""
安装/升级模块
支持 npm install 和自定义安装命令
"""
from typing import Callable, Optional

from .platform_utils import get_npm_command, run_command_realtime, is_windows, get_shell
from .detector import ToolInfo, InstallType, get_installed_version, get_install_command, get_alt_install_command
import subprocess


def install_package_npm(
    package_name: str,
    callback: Optional[Callable[[str], None]] = None
) -> tuple[bool, str]:
    """
    使用 npm 安装或升级包
    """
    npm_cmd = get_npm_command()
    cmd = [npm_cmd, "install", "-g", package_name]
    
    if callback:
        callback(f"[INFO] 正在安装/升级 {package_name}...")
        callback(f"[CMD] {' '.join(cmd)}")
    
    success, output = run_command_realtime(cmd, callback)
    
    if success:
        msg = "安装成功!"
        if callback:
            callback(f"[SUCCESS] {msg}")
        return True, msg
    else:
        msg = f"安装失败: {output}"
        if callback:
            callback(f"[ERROR] {msg}")
        return False, msg


def _prepare_install_command(install_cmd: str) -> str:
    """
    预处理安装命令，添加必要的参数
    """
    # 对 winget 命令自动添加协议接受参数
    if "winget" in install_cmd.lower():
        if "--accept-source-agreements" not in install_cmd:
            install_cmd += " --accept-source-agreements"
        if "--accept-package-agreements" not in install_cmd:
            install_cmd += " --accept-package-agreements"
    
    # 检测 PowerShell 特有命令，需要用 powershell 执行
    # irm = Invoke-RestMethod, iex = Invoke-Expression
    ps_keywords = ['irm ', 'iex', 'invoke-', '| iex', 'Invoke-WebRequest', 'Invoke-RestMethod']
    is_powershell_cmd = any(kw.lower() in install_cmd.lower() for kw in ps_keywords)
    
    if is_powershell_cmd and not install_cmd.lower().startswith('powershell'):
        # 转义引号并包装为 PowerShell 命令
        escaped_cmd = install_cmd.replace('"', '\\"')
        install_cmd = f'powershell -ExecutionPolicy Bypass -Command "{escaped_cmd}"'
    
    return install_cmd


def _run_install_command(
    install_cmd: str,
    callback: Optional[Callable[[str], None]] = None
) -> tuple[bool, str]:
    """
    执行单个安装命令
    返回 (成功, 消息)
    """
    install_cmd = _prepare_install_command(install_cmd)
    
    if callback:
        callback(f"[CMD] {install_cmd}")
    
    try:
        process = subprocess.Popen(
            install_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
            encoding="utf-8",
            errors="replace"
        )
        
        output_lines = []
        for line in process.stdout:
            line = line.rstrip()
            output_lines.append(line)
            if callback:
                callback(line)
        
        process.wait()
        success = process.returncode == 0
        
        return success, "\n".join(output_lines[-10:])  # 返回最后10行作为消息
            
    except Exception as e:
        return False, str(e)


def install_package_custom(
    tool: ToolInfo,
    callback: Optional[Callable[[str], None]] = None
) -> tuple[bool, str]:
    """
    使用自定义命令安装工具
    支持主命令失败后自动尝试备用命令
    """
    install_cmd = get_install_command(tool)
    alt_install_cmd = get_alt_install_command(tool)
    
    if not install_cmd:
        msg = f"未找到适用于当前系统的安装命令"
        if callback:
            callback(f"[ERROR] {msg}")
        return False, msg
    
    if callback:
        callback(f"[INFO] 正在安装 {tool.name}...")
        if tool.note:
            callback(f"[INFO] 注意: {tool.note}")
    
    # 尝试主安装命令
    success, output = _run_install_command(install_cmd, callback)
    
    if success:
        if callback:
            callback(f"[SUCCESS] 安装成功!")
        return True, "安装成功!"
    
    # 主命令失败，尝试备用命令
    if alt_install_cmd:
        if callback:
            callback(f"[WARN] 主安装方式失败，正在尝试备用安装方式...")
        
        success, output = _run_install_command(alt_install_cmd, callback)
        
        if success:
            if callback:
                callback(f"[SUCCESS] 备用方式安装成功!")
            return True, "备用方式安装成功!"
        else:
            msg = f"主安装和备用安装均失败"
            if callback:
                callback(f"[ERROR] {msg}")
            return False, msg
    else:
        msg = f"安装失败，且没有可用的备用安装方式"
        if callback:
            callback(f"[ERROR] {msg}")
        return False, msg


def install_tool(
    tool: ToolInfo,
    callback: Optional[Callable[[str], None]] = None
) -> tuple[bool, str]:
    """
    安装或升级工具
    根据安装类型选择不同的安装方式
    """
    if callback:
        callback(f"[INFO] 开始处理 {tool.name}...")
        if tool.installed_version:
            callback(f"[INFO] 当前版本: {tool.installed_version}")
        if tool.latest_version:
            callback(f"[INFO] 目标版本: {tool.latest_version}")
    
    if tool.install_type == InstallType.CUSTOM:
        return install_package_custom(tool, callback)
    else:
        success, msg = install_package_npm(tool.package, callback)
        if success:
            return True, msg

        alt_install_cmd = get_alt_install_command(tool)
        if alt_install_cmd:
            if callback:
                callback("[WARN] npm 安装失败，正在尝试备用安装方式...")
            alt_success, alt_output = _run_install_command(alt_install_cmd, callback)
            if alt_success:
                if callback:
                    callback("[SUCCESS] 备用方式安装成功!")
                return True, "备用方式安装成功!"
            else:
                fail_msg = "npm 安装失败，备用安装也失败"
                if callback:
                    callback(f"[ERROR] {fail_msg}")
                return False, fail_msg

        return False, msg


def batch_install_tools(
    tools: list[ToolInfo],
    callback: Optional[Callable[[str], None]] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None
) -> dict[str, tuple[bool, str]]:
    """
    批量安装/升级工具
    """
    results = {}
    total = len(tools)
    
    for i, tool in enumerate(tools):
        if progress_callback:
            progress_callback(i + 1, total)
        
        if callback:
            callback(f"\n{'='*50}")
            callback(f"[{i+1}/{total}] 处理 {tool.name}")
            callback(f"{'='*50}")
        
        success, msg = install_tool(tool, callback)
        results[tool.id] = (success, msg)
    
    return results
