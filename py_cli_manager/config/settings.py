"""
应用配置设置
"""
import os
import json
from pathlib import Path

# 获取配置目录
def get_config_dir() -> Path:
    """获取配置文件目录"""
    return Path(__file__).parent


def get_tools_config_path() -> Path:
    """获取工具配置文件路径"""
    return get_config_dir() / "tools.json"


def load_tools_config() -> dict:
    """加载工具配置"""
    config_path = get_tools_config_path()
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tools": [], "settings": {}}


def save_tools_config(config: dict) -> None:
    """保存工具配置"""
    config_path = get_tools_config_path()
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


# 应用设置
APP_NAME = "AI CLI 工具管理器"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
