"""
核心功能模块
"""
from .platform_utils import (
    is_windows,
    is_macos,
    is_linux,
    get_npm_command,
    find_npm,
    run_command,
    run_command_realtime,
)

from .detector import (
    ToolStatus,
    InstallType,
    ToolInfo,
    get_installed_version,
    get_latest_version,
    get_install_command,
    check_tool_status,
    load_tools_from_config,
    tool_to_dict,
    get_changelog,
    get_github_repo_from_npm,
)

from .installer import (
    install_package_npm,
    install_package_custom,
    install_tool,
    batch_install_tools,
)

__all__ = [
    # platform_utils
    "is_windows",
    "is_macos",
    "is_linux",
    "get_npm_command",
    "find_npm",
    "run_command",
    "run_command_realtime",
    # detector
    "ToolStatus",
    "InstallType",
    "ToolInfo",
    "get_installed_version",
    "get_latest_version",
    "get_install_command",
    "check_tool_status",
    "load_tools_from_config",
    "tool_to_dict",
    "get_changelog",
    # installer
    "install_package_npm",
    "install_package_custom",
    "install_tool",
    "batch_install_tools",
]
