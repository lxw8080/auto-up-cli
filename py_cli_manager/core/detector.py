"""
版本检测模块
检测本地已安装版本和最新版本
支持 npm registry 和 GitHub Releases API
"""
import json
import re
import urllib.request
import urllib.error
from typing import Optional
from dataclasses import dataclass, field
from enum import Enum

from .platform_utils import get_npm_command, run_command, is_windows, is_macos


class ToolStatus(Enum):
    """工具状态枚举"""
    NOT_INSTALLED = "未安装"
    INSTALLED = "已安装"
    UPGRADABLE = "可升级"
    LATEST = "最新"
    ERROR = "错误"


class InstallType(Enum):
    """安装类型枚举"""
    NPM = "npm"
    CUSTOM = "custom"


@dataclass
class ToolInfo:
    """工具信息数据类"""
    id: str
    name: str
    package: str
    category: str
    builtin: bool = True
    note: str = ""
    install_type: InstallType = InstallType.NPM
    install_commands: dict = field(default_factory=dict)
    version_command: str = ""
    github_repo: str = ""  # 新增: GitHub 仓库 (如 "anthropics/claude-code")
    
    # 运行时状态
    installed_version: Optional[str] = None
    latest_version: Optional[str] = None
    status: ToolStatus = ToolStatus.NOT_INSTALLED
    error_message: str = ""


def get_installed_version_npm(package_name: str) -> Optional[str]:
    """
    获取本地已安装的 npm 包版本
    
    通过执行: npm list -g <package> --depth=0 --json
    """
    npm_cmd = get_npm_command()
    cmd = [npm_cmd, "list", "-g", package_name, "--depth=0", "--json"]
    
    success, stdout, stderr = run_command(cmd, timeout=30)
    
    if not success or not stdout:
        return None
    
    try:
        data = json.loads(stdout)
        dependencies = data.get("dependencies", {})
        
        if package_name in dependencies:
            return dependencies[package_name].get("version")
        
        # 有些包名带 scope，尝试只用包名部分匹配
        for pkg_name, pkg_info in dependencies.items():
            if package_name.endswith(pkg_name) or pkg_name.endswith(package_name.split("/")[-1]):
                return pkg_info.get("version")
        
        return None
    except json.JSONDecodeError:
        return None


def get_installed_version_custom(version_command: str) -> Optional[str]:
    """
    通过自定义版本命令获取已安装版本
    
    例如: claude --version
    """
    if not version_command:
        return None
    
    # 分割命令
    parts = version_command.split()
    if not parts:
        return None
    
    success, stdout, stderr = run_command(parts, timeout=10)
    
    if not success:
        return None
    
    # 尝试从输出中提取版本号
    output = stdout.strip() or stderr.strip()
    if not output:
        return None
    
    # 常见版本号格式匹配
    version_patterns = [
        r'(\d+\.\d+\.\d+)',  # 1.2.3
        r'v(\d+\.\d+\.\d+)',  # v1.2.3
        r'version[:\s]+(\d+\.\d+\.\d+)',  # version: 1.2.3
    ]
    
    for pattern in version_patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            return match.group(1)
    
    # 如果没有匹配到，返回第一行作为版本
    first_line = output.split('\n')[0].strip()
    return first_line if first_line else None


def get_installed_version(tool: 'ToolInfo') -> Optional[str]:
    """
    获取工具的已安装版本
    根据安装类型选择不同的检测方式
    """
    if tool.install_type == InstallType.CUSTOM and tool.version_command:
        return get_installed_version_custom(tool.version_command)
    else:
        return get_installed_version_npm(tool.package)


def get_latest_version_npm(package_name: str) -> Optional[str]:
    """
    获取 npm registry 上的最新版本
    
    通过执行: npm view <package> version
    """
    npm_cmd = get_npm_command()
    cmd = [npm_cmd, "view", package_name, "version"]
    
    success, stdout, stderr = run_command(cmd, timeout=30)
    
    if success and stdout:
        return stdout.strip()
    
    return None


def get_latest_version_github(repo: str) -> Optional[str]:
    """
    通过 GitHub Releases API 获取最新版本
    
    Args:
        repo: GitHub 仓库路径，如 "anthropics/claude-code"
    
    Returns:
        最新版本号，如 "2.1.20"
    """
    if not repo:
        return None
    
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    
    try:
        request = urllib.request.Request(
            api_url,
            headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "AI-CLI-Manager"
            }
        )
        
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            tag_name = data.get("tag_name", "")
            
            # 智能提取版本号
            # 支持格式: v1.2.3, 1.2.3, rust-v0.92.0, release-1.2.3 等
            version_match = re.search(r'(\d+\.\d+\.\d+(?:[.-]\w+)?)', tag_name)
            if version_match:
                return version_match.group(1)
            
            # 如果没有匹配到语义化版本，返回原始 tag（去除 v 前缀）
            if tag_name.startswith("v"):
                return tag_name[1:]
            return tag_name
            
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, Exception):
        return None


def get_changelog(repo: str) -> Optional[str]:
    """
    从 GitHub Releases API 获取最新版本的更新日志
    
    Args:
        repo: GitHub 仓库路径，如 "anthropics/claude-code"
    
    Returns:
        更新日志文本（markdown 格式）
    """
    if not repo:
        return None
    
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    
    try:
        request = urllib.request.Request(
            api_url,
            headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "AI-CLI-Manager"
            }
        )
        
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            
            tag_name = data.get("tag_name", "Unknown")
            name = data.get("name", tag_name)
            body = data.get("body", "暂无更新说明")
            published_at = data.get("published_at", "")[:10]  # 只取日期部分
            
            changelog = f"## {name}\n\n"
            changelog += f"**版本:** {tag_name}\n"
            if published_at:
                changelog += f"**发布日期:** {published_at}\n"
            changelog += f"\n---\n\n{body}"
            
            return changelog
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "未找到该工具的发布信息，可能没有 GitHub Releases。"
        return f"获取更新日志失败: HTTP {e.code}"
    except urllib.error.URLError:
        return "网络连接失败，请检查网络设置。"
    except Exception as e:
        return f"获取更新日志失败: {str(e)}"


def get_github_repo_from_npm(package_name: str) -> Optional[str]:
    """
    从 npm registry 自动获取包的 GitHub 仓库地址
    
    通过执行: npm view <package> repository.url
    
    Args:
        package_name: npm 包名
    
    Returns:
        GitHub 仓库路径，如 "anthropics/claude-code"，获取失败返回 None
    """
    npm_cmd = get_npm_command()
    cmd = [npm_cmd, "view", package_name, "repository.url"]
    
    success, stdout, stderr = run_command(cmd, timeout=15)
    
    if not success or not stdout:
        return None
    
    repo_url = stdout.strip()
    
    # 解析 GitHub 仓库路径
    # 支持格式:
    # - git+https://github.com/owner/repo.git
    # - https://github.com/owner/repo.git
    # - git://github.com/owner/repo.git
    # - github:owner/repo
    patterns = [
        r'github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$',  # github.com/owner/repo.git
        r'^github:([^/]+/[^/]+)$',  # github:owner/repo
    ]
    
    for pattern in patterns:
        match = re.search(pattern, repo_url)
        if match:
            return match.group(1)
    
    return None


def get_latest_version(tool: 'ToolInfo') -> Optional[str]:
    """
    获取工具的最新版本 (智能检测)
    
    检测顺序:
    1. 如果配置了 githubRepo，直接使用 GitHub API
    2. 尝试 npm registry
    3. 如果 npm 失败，尝试自动从 npm 获取 GitHub 仓库并查询
    """
    # 1. 优先使用配置的 GitHub 仓库
    if tool.github_repo:
        version = get_latest_version_github(tool.github_repo)
        if version:
            return version
    
    # 2. 尝试 npm registry
    if tool.package:
        version = get_latest_version_npm(tool.package)
        if version:
            return version
        
        # 3. npm 失败时，尝试自动获取 GitHub 仓库
        auto_repo = get_github_repo_from_npm(tool.package)
        if auto_repo:
            version = get_latest_version_github(auto_repo)
            if version:
                return version
    
    return None


def get_install_command(tool: 'ToolInfo') -> str:
    """
    获取工具的安装命令
    根据操作系统和安装类型返回适当的命令
    """
    if tool.install_type == InstallType.NPM:
        npm_cmd = get_npm_command()
        return f"{npm_cmd} install -g {tool.package}"
    
    # 自定义安装命令
    commands = tool.install_commands
    if not commands:
        return ""
    
    if is_windows():
        return commands.get("windows", commands.get("windows_alt", ""))
    elif is_macos():
        return commands.get("macos", commands.get("macos_alt", ""))
    else:
        return commands.get("linux", "")


def get_alt_install_command(tool: 'ToolInfo') -> str:
    """
    获取工具的备用安装命令
    当主安装命令失败时使用
    """
    if tool.install_type == InstallType.NPM:
        # npm 类型没有备用命令
        return ""
    
    commands = tool.install_commands
    if not commands:
        return ""
    
    if is_windows():
        # 只有当有主命令时才返回备用命令
        if commands.get("windows") and commands.get("windows_alt"):
            return commands.get("windows_alt", "")
    elif is_macos():
        if commands.get("macos") and commands.get("macos_alt"):
            return commands.get("macos_alt", "")
    
    return ""


def normalize_version(version: str) -> str:
    """
    规范化版本号
    
    移除常见前缀如 'v', 并清理空白
    """
    if not version:
        return ""
    
    version = version.strip()
    
    # 移除 v 前缀
    if version.lower().startswith("v"):
        version = version[1:]
    
    return version


def compare_versions(installed: str, latest: str) -> int:
    """
    比较两个版本号
    
    Returns:
        -1: installed < latest (可升级)
         0: installed == latest (最新)
         1: installed > latest (已安装更新版本)
    """
    installed = normalize_version(installed)
    latest = normalize_version(latest)
    
    if not installed or not latest:
        return 0
    
    # 直接字符串比较作为快速路径
    if installed == latest:
        return 0
    
    # 尝试语义化版本比较
    try:
        # 提取主版本号部分 (去除预发布后缀如 -beta, -rc.1)
        def parse_version(v: str) -> tuple:
            # 分离预发布后缀
            main_part = re.split(r'[-+]', v)[0]
            parts = main_part.split('.')
            
            # 转换为整数列表，处理非数字部分
            result = []
            for p in parts:
                try:
                    result.append(int(p))
                except ValueError:
                    # 非数字部分，保留原值用于字符串比较
                    result.append(p)
            
            # 补齐到至少3位
            while len(result) < 3:
                result.append(0)
            
            return tuple(result)
        
        installed_parts = parse_version(installed)
        latest_parts = parse_version(latest)
        
        if installed_parts < latest_parts:
            return -1
        elif installed_parts > latest_parts:
            return 1
        else:
            return 0
            
    except Exception:
        # 解析失败，回退到字符串比较
        if installed < latest:
            return -1
        elif installed > latest:
            return 1
        return 0


def check_tool_status(tool: ToolInfo) -> ToolInfo:
    """
    检查工具状态
    """
    try:
        # 获取已安装版本
        tool.installed_version = get_installed_version(tool)
        
        # 获取最新版本
        tool.latest_version = get_latest_version(tool)
        
        # 判断状态
        if tool.installed_version is None:
            tool.status = ToolStatus.NOT_INSTALLED
        elif tool.latest_version is None:
            tool.status = ToolStatus.INSTALLED
        else:
            # 使用语义化版本比较
            cmp_result = compare_versions(tool.installed_version, tool.latest_version)
            if cmp_result < 0:
                tool.status = ToolStatus.UPGRADABLE
            else:
                tool.status = ToolStatus.LATEST
        
        tool.error_message = ""
        
    except Exception as e:
        tool.status = ToolStatus.ERROR
        tool.error_message = str(e)
    
    return tool



def load_tools_from_config(config: dict) -> list[ToolInfo]:
    """
    从配置加载工具列表
    """
    tools = []
    for tool_data in config.get("tools", []):
        # 解析安装类型
        install_type_str = tool_data.get("installType", "npm")
        install_type = InstallType.CUSTOM if install_type_str == "custom" else InstallType.NPM
        
        tool = ToolInfo(
            id=tool_data.get("id", ""),
            name=tool_data.get("name", ""),
            package=tool_data.get("package", ""),
            category=tool_data.get("category", "其他"),
            builtin=tool_data.get("builtin", False),
            note=tool_data.get("note", ""),
            install_type=install_type,
            install_commands=tool_data.get("installCommands", {}),
            version_command=tool_data.get("versionCommand", ""),
            github_repo=tool_data.get("githubRepo", "")
        )
        tools.append(tool)
    return tools


def tool_to_dict(tool: ToolInfo) -> dict:
    """
    将工具信息转换为字典（用于保存配置）
    """
    result = {
        "id": tool.id,
        "name": tool.name,
        "package": tool.package,
        "category": tool.category,
        "builtin": tool.builtin,
        "note": tool.note
    }
    
    # GitHub 仓库字段（所有类型都可以有）
    if tool.github_repo:
        result["githubRepo"] = tool.github_repo
    
    # 自定义安装类型的额外字段
    if tool.install_type == InstallType.CUSTOM:
        result["installType"] = "custom"
        if tool.install_commands:
            result["installCommands"] = tool.install_commands
        if tool.version_command:
            result["versionCommand"] = tool.version_command
    
    return result
