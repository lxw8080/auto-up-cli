"""
配置模块
"""
from .settings import (
    get_config_dir,
    get_tools_config_path,
    load_tools_config,
    save_tools_config,
    APP_NAME,
    APP_VERSION,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    CHECK_PARALLEL_WORKERS,
)

__all__ = [
    "get_config_dir",
    "get_tools_config_path",
    "load_tools_config",
    "save_tools_config",
    "APP_NAME",
    "APP_VERSION",
    "WINDOW_WIDTH",
    "WINDOW_HEIGHT",
    "CHECK_PARALLEL_WORKERS",
]
