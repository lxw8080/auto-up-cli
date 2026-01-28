"""
安装/升级模块
支持 npm install 和自定义安装命令
"""
from typing import Callable, Optional

from .platform_utils import get_npm_command, run_command_realtime, is_windows, get_shell
from .detector import ToolInfo, InstallType, get_installed_version, get_install_command
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


def install_package_custom(
    tool: ToolInfo,
    callback: Optional[Callable[[str], None]] = None
) -> tuple[bool, str]:
    """
    使用自定义命令安装工具
    """
    install_cmd = get_install_command(tool)
    
    if not install_cmd:
        msg = f"未找到适用于当前系统的安装命令"
        if callback:
            callback(f"[ERROR] {msg}")
        return False, msg
    
    if callback:
        callback(f"[INFO] 正在安装 {tool.name}...")
        callback(f"[CMD] {install_cmd}")
        if tool.note:
            callback(f"[INFO] 注意: {tool.note}")
    
    try:
        # 对于自定义命令，需要使用 shell 执行
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
        
        if success:
            msg = "安装成功!"
            if callback:
                callback(f"[SUCCESS] {msg}")
            return True, msg
        else:
            msg = f"安装失败 (退出码: {process.returncode})"
            if callback:
                callback(f"[ERROR] {msg}")
            return False, msg
            
    except Exception as e:
        msg = f"安装失败: {str(e)}"
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
        return install_package_npm(tool.package, callback)


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
