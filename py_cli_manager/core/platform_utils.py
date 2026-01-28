"""
跨平台工具模块
提供跨平台命令执行支持
"""
import platform
import subprocess
import shutil
from typing import Optional


def is_windows() -> bool:
    """判断是否为 Windows 系统"""
    return platform.system() == "Windows"


def is_macos() -> bool:
    """判断是否为 macOS 系统"""
    return platform.system() == "Darwin"


def is_linux() -> bool:
    """判断是否为 Linux 系统"""
    return platform.system() == "Linux"


def get_npm_command() -> str:
    """
    获取 npm 命令
    Windows: npm.cmd
    macOS/Linux: npm
    """
    if is_windows():
        # Windows 需要使用 npm.cmd
        return "npm.cmd"
    return "npm"


def get_shell() -> bool:
    """
    获取是否需要使用 shell
    Windows: True (需要通过 cmd)
    macOS/Linux: False
    """
    return is_windows()


def find_npm() -> Optional[str]:
    """
    查找 npm 可执行文件路径
    返回 None 如果未找到
    """
    npm_cmd = get_npm_command()
    return shutil.which(npm_cmd)


def run_command(cmd: list, timeout: int = 30) -> tuple[bool, str, str]:
    """
    执行命令并返回结果
    
    Args:
        cmd: 命令列表
        timeout: 超时时间（秒）
    
    Returns:
        (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=get_shell(),
            encoding="utf-8",
            errors="replace"
        )
        return (
            result.returncode == 0,
            result.stdout.strip(),
            result.stderr.strip()
        )
    except subprocess.TimeoutExpired:
        return False, "", "命令执行超时"
    except FileNotFoundError:
        return False, "", f"未找到命令: {cmd[0]}"
    except Exception as e:
        return False, "", str(e)


def run_command_realtime(cmd: list, callback=None) -> tuple[bool, str]:
    """
    实时执行命令，通过 callback 输出日志
    
    Args:
        cmd: 命令列表
        callback: 回调函数，接收 (line: str) 参数
    
    Returns:
        (success, output)
    """
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=get_shell(),
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
        return process.returncode == 0, "\n".join(output_lines)
        
    except FileNotFoundError:
        error_msg = f"未找到命令: {cmd[0]}"
        if callback:
            callback(f"[错误] {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = str(e)
        if callback:
            callback(f"[错误] {error_msg}")
        return False, error_msg
