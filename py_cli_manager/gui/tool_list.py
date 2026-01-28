"""
工具列表组件
支持单个工具刷新和右键菜单
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from typing import Callable, Optional

from .styles import FONTS, PADDING, STATUS_STYLES
from core import ToolInfo, ToolStatus

class ToolListView(ttk.Frame):
    """工具列表视图"""
    
    def __init__(
        self,
        parent,
        on_install: Optional[Callable[[ToolInfo], None]] = None,
        on_upgrade: Optional[Callable[[ToolInfo], None]] = None,
        on_refresh_single: Optional[Callable[[ToolInfo], None]] = None,
        on_edit: Optional[Callable[[ToolInfo], None]] = None,
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        
        self.on_install = on_install
        self.on_upgrade = on_upgrade
        self.on_refresh_single = on_refresh_single
        self.on_edit = on_edit
        self.on_changelog = None
        self.tools: list[ToolInfo] = []
        self._item_map: dict[str, ToolInfo] = {}
        
        self._create_widgets()
        self._create_context_menu()
    
    def _create_widgets(self):
        """创建控件"""
        # 创建 Treeview
        columns = ("name", "package", "installed", "latest", "status", "action")
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            selectmode="browse",
            bootstyle=PRIMARY
        )
        
        # 设置列
        self.tree.heading("name", text="工具名称")
        self.tree.heading("package", text="NPM 包名")
        self.tree.heading("installed", text="当前版本")
        self.tree.heading("latest", text="最新版本")
        self.tree.heading("status", text="状态")
        self.tree.heading("action", text="操作")
        
        # 设置列宽
        self.tree.column("name", width=120, minwidth=100)
        self.tree.column("package", width=200, minwidth=150)
        self.tree.column("installed", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("latest", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("status", width=80, minwidth=60, anchor=tk.CENTER)
        self.tree.column("action", width=100, minwidth=80, anchor=tk.CENTER)
        
        # 滚动条 - ttkbootstrap 自动样式的滚动条
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", self._on_double_click)
        # 绑定右键菜单
        self.tree.bind("<Button-3>", self._on_right_click)
        
        # 这里的 tag 样式由 ttkbootstrap 主题控制，
        # 但我们仍然可以为特定行设置 tag 来微调（如颜色），
        # 不过 ttkbootstrap treeview 的 tag 支持有限，主要依赖 theme。
        # 这里保留 tag 设置，但在 ttkbootstrap 中可能效果不同，需要测试。
        # 简单的 workaround 是不做 tag_configure 颜色，而是依赖 bootstyle
        # 但是 bootstyle 是作用于整个 treeview 的。
        # 如果需要行变色，还是得用 tag_configure，但颜色值不能写死，要适配主题。
        # 暂时先不做 tag_configure 颜色，保持由于 Treeview 行颜色在 ttkbootstrap 中较难完美自动适配所有行。
        # 或者我们可以在 styles 中定义 adaptive 颜色
        
        # 设置标签样式 (不做具体颜色定义，保持默认清晰度，或者后续添加)
        pass

    def _create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="🔄 刷新此工具", command=self._refresh_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="✏️ 编辑工具", command=self._edit_selected)
        self.context_menu.add_command(label="⬇️ 安装/升级", command=self._install_selected)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 查看更新日志", command=self._show_changelog)
    
    def _on_right_click(self, event):
        """右键点击事件"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _refresh_selected(self):
        """刷新选中的工具"""
        tool = self.get_selected_tool()
        if tool and self.on_refresh_single:
            self.on_refresh_single(tool)
    
    def _edit_selected(self):
        """编辑选中的工具"""
        tool = self.get_selected_tool()
        if tool and self.on_edit:
            self.on_edit(tool)
    
    def _install_selected(self):
        """安装/升级选中的工具"""
        tool = self.get_selected_tool()
        if not tool:
            return
        
        if tool.status == ToolStatus.NOT_INSTALLED:
            if self.on_install:
                self.on_install(tool)
        elif tool.status == ToolStatus.UPGRADABLE:
            if self.on_upgrade:
                self.on_upgrade(tool)
    
    def _show_changelog(self):
        """查看选中工具的更新日志"""
        tool = self.get_selected_tool()
        if tool and self.on_changelog:
            self.on_changelog(tool)
    
    def update_tools(self, tools: list[ToolInfo]):
        """更新工具列表"""
        self.tools = tools
        self._item_map.clear()
        
        # 清空现有项
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 添加工具
        for tool in tools:
            self._add_tool_item(tool)
    
    def _add_tool_item(self, tool: ToolInfo):
        """添加工具项"""
        installed = tool.installed_version or "-"
        latest = tool.latest_version or "-"
        
        status_text, tag = self._get_status_info(tool.status)
        action_text = self._get_action_text(tool)
        
        item_id = self.tree.insert(
            "",
            tk.END,
            values=(
                tool.name,
                tool.package,
                installed,
                latest,
                status_text,
                action_text
            ),
            tags=(tag,)
        )
        
        self._item_map[item_id] = tool
    
    def _get_status_info(self, status: ToolStatus) -> tuple[str, str]:
        """获取状态信息和 tag"""
        status_map = {
            ToolStatus.NOT_INSTALLED: ("未安装", "not_installed"),
            ToolStatus.INSTALLED: ("已安装", "installed"),
            ToolStatus.UPGRADABLE: ("可升级", "upgradable"),
            ToolStatus.LATEST: ("最新", "latest"),
            ToolStatus.ERROR: ("错误", "error"),
        }
        return status_map.get(status, ("待检测", "pending"))
    
    def _get_action_text(self, tool: ToolInfo) -> str:
        """获取操作文本"""
        if tool.installed_version is None and tool.latest_version is None:
            return "[点击刷新]"
        
        if tool.status == ToolStatus.NOT_INSTALLED:
            return "🔧 安装"
        elif tool.status == ToolStatus.UPGRADABLE:
            return "⬆️ 升级"
        else:
            return "-"
    
    def _on_double_click(self, event):
        """双击事件"""
        item = self.tree.identify_row(event.y)
        if not item:
            return
        
        tool = self._item_map.get(item)
        if not tool:
            return
        
        if tool.installed_version is None and tool.latest_version is None:
            if self.on_refresh_single:
                self.on_refresh_single(tool)
            return
        
        if tool.status == ToolStatus.NOT_INSTALLED:
            if self.on_install:
                self.on_install(tool)
        elif tool.status == ToolStatus.UPGRADABLE:
            if self.on_upgrade:
                self.on_upgrade(tool)
    
    def get_selected_tool(self) -> Optional[ToolInfo]:
        """获取选中的工具"""
        selection = self.tree.selection()
        if not selection:
            return None
        return self._item_map.get(selection[0])
    
    def get_upgradable_tools(self) -> list[ToolInfo]:
        """获取所有可升级的工具"""
        return [t for t in self.tools if t.status == ToolStatus.UPGRADABLE]
    
    def get_not_installed_tools(self) -> list[ToolInfo]:
        """获取所有未安装的工具"""
        return [t for t in self.tools if t.status == ToolStatus.NOT_INSTALLED]
    
    def refresh_tool(self, tool: ToolInfo):
        """刷新单个工具显示"""
        for item_id, item_tool in self._item_map.items():
            if item_tool.id == tool.id:
                installed = tool.installed_version or "-"
                latest = tool.latest_version or "-"
                status_text, tag = self._get_status_info(tool.status)
                action_text = self._get_action_text(tool)
                
                self.tree.item(
                    item_id,
                    values=(
                        tool.name,
                        tool.package,
                        installed,
                        latest,
                        status_text,
                        action_text
                    ),
                    tags=(tag,)
                )
                # 更新 map 中的 tool 对象，保持最新状态
                self._item_map[item_id] = tool
                break
    
    def set_tool_pending(self, tool: ToolInfo):
        """设置工具为待检测状态"""
        for item_id, item_tool in self._item_map.items():
            if item_tool.id == tool.id:
                self.tree.item(
                    item_id,
                    values=(
                        tool.name,
                        tool.package,
                        "检测中...",
                        "检测中...",
                        "检测中",
                        "-"
                    ),
                    tags=("pending",)
                )
                break
    def update_theme(self, colors: dict):
        # 兼容性方法，实际不需要做什么，因为 ttkbootstrap 自动处理
        pass
