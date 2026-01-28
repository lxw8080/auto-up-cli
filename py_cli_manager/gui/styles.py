"""
UI 样式定义 - 使用 ttkbootstrap
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# 字体定义
FONTS = {
    "title": ("Microsoft YaHei UI", 16, "bold"),
    "heading": ("Microsoft YaHei UI", 12, "bold"),
    "body": ("Microsoft YaHei UI", 10),
    "small": ("Microsoft YaHei UI", 9),
    "mono": ("Consolas", 9),
}

# 间距
PADDING = {
    "small": 5,
    "medium": 10,
    "large": 15,
    "xlarge": 20,
}

# 主题配置
DEFAULT_THEME = "cosmo"  # 浅色默认
DARK_THEME = "darkly"    # 深色默认

# 状态样式映射 (映射到 bootstyle)
STATUS_STYLES = {
    "installed": SUCCESS,
    "upgradable": WARNING,
    "not_installed": SECONDARY,
    "latest": PRIMARY,
    "error": DANGER,
}

# 辅助函数：虽然 ttkbootstrap 自动处理大部分颜色，
# 但有时我们需要获取具体颜色值用于非 ttk 组件（如 Text 控件）
def get_text_colors(is_dark: bool) -> dict:
    """获取文本控件的颜色配置"""
    if is_dark:
        return {
            "bg": "#2b2b2b",
            "fg": "#ffffff",
            "insert": "#ffffff"
        }
    else:
        return {
            "bg": "#ffffff",
            "fg": "#000000",
            "insert": "#000000"
        }

# 当前主题状态管理（简单包装，实际由 Window 实例管理）
_current_theme_name = DEFAULT_THEME

def get_current_theme_name() -> str:
    return _current_theme_name

def set_current_theme_name(name: str):
    global _current_theme_name
    _current_theme_name = name

