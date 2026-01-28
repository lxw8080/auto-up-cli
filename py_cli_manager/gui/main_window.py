"""
主窗口 - 使用 ttkbootstrap 重构
"""
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from typing import Optional
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip

from .styles import (
    FONTS, PADDING, 
    DEFAULT_THEME, DARK_THEME,
    get_text_colors, set_current_theme_name, get_current_theme_name
)
from .tool_list import ToolListView
from .add_tool_dialog import AddToolDialog
from .edit_tool_dialog import EditToolDialog
from .changelog_dialog import ChangelogDialog
from config import (
    load_tools_config,
    save_tools_config,
    APP_NAME,
    APP_VERSION,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)
from core import (
    ToolInfo,
    ToolStatus,
    check_tool_status,
    load_tools_from_config,
    tool_to_dict,
    install_tool,
    find_npm,
    get_changelog,
    get_github_repo_from_npm,
)


class MainWindow(ttk.Window):
    """主窗口"""
    
    def __init__(self):
        super().__init__(themename=DEFAULT_THEME)
        
        self.tools: list[ToolInfo] = []
        self._filtered_tools: list[ToolInfo] = []
        self._current_category = "全部"
        self._is_busy = False
        
        # 初始化主题状态
        set_current_theme_name(DEFAULT_THEME)
        
        self._setup_window()
        self._create_widgets()
        self._load_tools()
        
        # 启动时不自动刷新，只显示提示
        self.after(500, self._show_welcome_message)
    
    def _setup_window(self):
        """设置窗口"""
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(800, 600)
        
        # 设置窗口图标（如果有）
        try:
            self.iconbitmap("icon.ico")
        except:
            pass
            
    def _create_widgets(self):
        """创建控件"""
        # 主框架
        main_frame = ttk.Frame(self, padding=PADDING["medium"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题栏
        self._create_header(main_frame)
        
        # 工具栏
        self._create_toolbar(main_frame)
        
        # 筛选栏
        self._create_filter_bar(main_frame)
        
        # 工具列表
        self._create_tool_list(main_frame)
        
        # 日志区域
        self._create_log_area(main_frame)
        
        # 状态栏
        self._create_statusbar()
    
    def _create_header(self, parent):
        """创建标题栏"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, PADDING["medium"]))
        
        title_label = ttk.Label(
            header_frame,
            text=f"🤖 {APP_NAME}",
            font=FONTS["title"],
            bootstyle=PRIMARY
        )
        title_label.pack(side=tk.LEFT)
        
        version_label = ttk.Label(
            header_frame,
            text=f"v{APP_VERSION}",
            font=FONTS["small"],
            bootstyle=SECONDARY
        )
        version_label.pack(side=tk.LEFT, padx=(10, 0), pady=(8, 0)) # Slight adjustment for alignment
        
        # 主题切换按钮 (放右上角)
        self.theme_btn = ttk.Button(
            header_frame,
            text="🌙",
            command=self._toggle_theme,
            bootstyle="link",
            cursor="hand2"
        )
        self.theme_btn.pack(side=tk.RIGHT)
        ToolTip(self.theme_btn, text="切换深色/浅色模式")

    
    def _create_toolbar(self, parent):
        """创建工具栏"""
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X, pady=(0, PADDING["medium"]))
        
        # 刷新全部按钮
        self.refresh_btn = ttk.Button(
            toolbar_frame,
            text="🔄 刷新全部",
            command=self._refresh_all_status,
            bootstyle=INFO
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, PADDING["small"]))
        
        # 新增工具按钮
        self.add_btn = ttk.Button(
            toolbar_frame,
            text="➕ 新增",
            command=self._show_add_dialog,
            bootstyle=SUCCESS
        )
        self.add_btn.pack(side=tk.LEFT, padx=(0, PADDING["small"]))
        
        # 全部升级按钮
        self.upgrade_all_btn = ttk.Button(
            toolbar_frame,
            text="📦 全部升级",
            command=self._upgrade_all,
            bootstyle=WARNING
        )
        self.upgrade_all_btn.pack(side=tk.LEFT, padx=(0, PADDING["small"]))
        
        # 安装选中按钮
        self.install_btn = ttk.Button(
            toolbar_frame,
            text="⬇️ 安装选中",
            command=self._install_selected,
            bootstyle=PRIMARY
        )
        self.install_btn.pack(side=tk.LEFT, padx=(0, PADDING["medium"]))
        
        # 分隔符
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=PADDING["small"])
        
        # 导出按钮
        self.export_btn = ttk.Button(
            toolbar_frame,
            text="📤 导出",
            command=self._export_config,
            bootstyle="outline-secondary"
        )
        self.export_btn.pack(side=tk.LEFT, padx=(0, PADDING["small"]))
        
        # 导入按钮
        self.import_btn = ttk.Button(
            toolbar_frame,
            text="📥 导入",
            command=self._import_config,
            bootstyle="outline-secondary"
        )
        self.import_btn.pack(side=tk.LEFT, padx=(0, PADDING["small"]))
        
    
    def _create_filter_bar(self, parent):
        """创建筛选栏"""
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=tk.X, pady=(0, PADDING["small"]))
        
        # 分类筛选标签
        ttk.Label(filter_frame, text="分类:", font=FONTS["body"]).pack(side=tk.LEFT)
        
        # 分类下拉框
        self.category_var = tk.StringVar(value="全部")
        self.category_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.category_var,
            values=["全部"],  # 初始值，加载工具后更新
            width=15,
            font=FONTS["body"],
            state="readonly",
            bootstyle=PRIMARY
        )
        self.category_combo.pack(side=tk.LEFT, padx=PADDING["small"])
        self.category_combo.bind("<<ComboboxSelected>>", self._on_category_changed)
        
        # 工具数量统计
        self.count_label = ttk.Label(
            filter_frame,
            text="",
            font=FONTS["small"],
            bootstyle=SECONDARY
        )
        self.count_label.pack(side=tk.LEFT, padx=PADDING["medium"])
    
    def _create_tool_list(self, parent):
        """创建工具列表"""
        # 使用 Labelframe 会有边框，直接用 Frame 也可以，但在 ttkbootstrap 中 Labelframe 也好看
        list_frame = ttk.Labelframe(
            parent, 
            text="工具列表", 
            padding=PADDING["small"],
            bootstyle=PRIMARY
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, PADDING["medium"]))
        
        # 提示标签
        ttk.Label(
            list_frame, 
            text="双击检测/升级 | 右键更多操作", 
            font=FONTS["small"],
            bootstyle=SECONDARY
        ).pack(anchor=tk.E, pady=(0, 5))
        
        self.tool_list = ToolListView(
            list_frame,
            on_install=self._on_install_tool,
            on_upgrade=self._on_install_tool,
            on_refresh_single=self._refresh_single_tool,
            on_edit=self._show_edit_dialog
        )
        self.tool_list.on_changelog = self._show_changelog_dialog
        self.tool_list.pack(fill=tk.BOTH, expand=True)
    
    def _create_log_area(self, parent):
        """创建日志区域"""
        log_frame = ttk.Labelframe(parent, text="系统日志", padding=PADDING["small"], bootstyle=INFO)
        log_frame.pack(fill=tk.X)
        
        # 日志文本框 - Text 不是 ttk 组件，需要单独处理颜色
        self.log_text = tk.Text(
            log_frame,
            height=6,
            font=FONTS["mono"],
            wrap=tk.WORD,
            state=tk.DISABLED,
            bd=0,
            highlightthickness=0
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        log_scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        
        # 初始化颜色
        self._update_log_colors()
        
        # 配置日志标签颜色
        self.log_text.tag_configure("INFO", foreground="#17a2b8")
        self.log_text.tag_configure("SUCCESS", foreground="#28a745")
        self.log_text.tag_configure("ERROR", foreground="#dc3545")
        self.log_text.tag_configure("CMD", foreground="#ffc107")
    
    def _update_log_colors(self):
        """更新日志区域颜色"""
        is_dark = get_current_theme_name() == DARK_THEME
        colors = get_text_colors(is_dark)
        self.log_text.configure(
            bg=colors["bg"],
            fg=colors["fg"],
            insertbackground=colors["insert"]
        )
        
    def _create_statusbar(self):
        """创建状态栏"""
        self.statusbar = ttk.Label(
            self,
            text="就绪 - 点击\"刷新全部\"检测工具版本",
            relief=tk.FLAT, # Flat look for modern UI
            anchor=tk.W,
            padding=(PADDING["medium"], 5),
            bootstyle="inverse-light" 
        )
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _load_tools(self):
        """加载工具配置"""
        config = load_tools_config()
        self.tools = load_tools_from_config(config)
        self._update_category_list()
        self._apply_filter()
    
    def _update_category_list(self):
        """更新分类下拉框"""
        categories = set()
        for tool in self.tools:
            categories.add(tool.category)
        
        category_list = ["全部"] + sorted(list(categories))
        self.category_combo["values"] = category_list
    
    def _apply_filter(self):
        """应用分类筛选"""
        category = self.category_var.get()
        
        if category == "全部":
            self._filtered_tools = self.tools.copy()
        else:
            self._filtered_tools = [t for t in self.tools if t.category == category]
        
        self.tool_list.update_tools(self._filtered_tools)
        
        # 更新计数
        total = len(self.tools)
        shown = len(self._filtered_tools)
        if category == "全部":
            self.count_label.configure(text=f"共 {total} 个工具")
        else:
            self.count_label.configure(text=f"显示 {shown}/{total} 个工具")
    
    def _on_category_changed(self, event=None):
        """分类变更"""
        self._apply_filter()
    
    def _show_welcome_message(self):
        """显示欢迎信息"""
        self._log("[INFO] 欢迎使用 AI CLI 工具管理器！")
        self._log("[INFO] 点击\"刷新全部\"检测所有工具版本")
        self._log("[INFO] 右键工具可编辑或删除")
    
    def _log(self, message: str):
        """输出日志"""
        self.log_text.configure(state=tk.NORMAL)
        
        # 解析日志级别
        tag = None
        if message.startswith("[INFO]"):
            tag = "INFO"
        elif message.startswith("[SUCCESS]"):
            tag = "SUCCESS"
        elif message.startswith("[ERROR]") or message.startswith("[错误]"):
            tag = "ERROR"
        elif message.startswith("[CMD]"):
            tag = "CMD"
        
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.configure(state=tk.DISABLED)
        # self.update_idletasks() # 频繁 update 可能会卡
    
    def _set_status(self, text: str):
        """设置状态栏文本"""
        self.statusbar.configure(text=text)
        # self.update_idletasks()
    
    def _set_busy(self, busy: bool):
        """设置忙碌状态"""
        self._is_busy = busy
        state = tk.DISABLED if busy else tk.NORMAL
        
        self.refresh_btn.configure(state=state)
        self.add_btn.configure(state=state)
        self.upgrade_all_btn.configure(state=state)
        self.install_btn.configure(state=state)
    
    def _refresh_single_tool(self, tool: ToolInfo):
        """刷新单个工具状态"""
        if self._is_busy:
            return
        
        if not find_npm():
            messagebox.showerror(
                "错误",
                "未找到 npm 命令！\n请确保已安装 Node.js 并将其添加到 PATH。"
            )
            return
        
        self._set_status(f"正在检测 {tool.name}...")
        self._log(f"[INFO] 检测 {tool.name}...")
        
        # 设置为检测中状态
        self.tool_list.set_tool_pending(tool)
        
        def do_check():
            check_tool_status(tool)
            self.after(0, lambda: self._on_single_refresh_complete(tool))
        
        thread = threading.Thread(target=do_check, daemon=True)
        thread.start()
    
    def _on_single_refresh_complete(self, tool: ToolInfo):
        """单个工具刷新完成"""
        self.tool_list.refresh_tool(tool)
        self._set_status("就绪")
        
        if tool.installed_version:
            self._log(f"[SUCCESS] {tool.name}: 已安装 v{tool.installed_version}")
            if tool.latest_version and tool.installed_version != tool.latest_version:
                self._log(f"[INFO] 发现新版本: v{tool.latest_version}")
        else:
            self._log(f"[INFO] {tool.name}: 未安装")
    
    def _refresh_all_status(self):
        """刷新全部工具状态（并行）"""
        if self._is_busy:
            return
        
        if not find_npm():
            messagebox.showerror(
                "错误",
                "未找到 npm 命令！\n请确保已安装 Node.js 并将其添加到 PATH。"
            )
            return
        
        self._set_busy(True)
        self._set_status("正在并行检测全部工具状态...")
        self._log("[INFO] 开始检测全部工具状态...")
        
        # 设置所有工具为待检测状态
        for tool in self.tools:
            self.tool_list.set_tool_pending(tool)
        
        def check_all():
            # 使用线程池并行检测
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(check_tool_status, tool): tool for tool in self.tools}
                
                for future in as_completed(futures):
                    tool = futures[future]
                    try:
                        future.result()  # 获取结果（如有异常会抛出）
                        self.after(0, lambda t=tool: self._log(f"[INFO] 检测 {t.name}... 完成"))
                    except Exception as e:
                        self.after(0, lambda t=tool, err=e: self._log(f"[ERROR] 检测 {t.name} 失败: {err}"))
                    
                    self.after(0, lambda t=tool: self.tool_list.refresh_tool(t))
            
            self.after(0, self._on_refresh_all_complete)
        
        thread = threading.Thread(target=check_all, daemon=True)
        thread.start()
    
    def _on_refresh_all_complete(self):
        """全部刷新完成回调"""
        self._set_busy(False)
        self._set_status("就绪")
        self._log("[SUCCESS] 全部工具状态检测完成！")
        
        upgradable = len(self.tool_list.get_upgradable_tools())
        not_installed = len(self.tool_list.get_not_installed_tools())
        
        if upgradable > 0:
            self._log(f"[INFO] 发现 {upgradable} 个工具可升级")
        if not_installed > 0:
            self._log(f"[INFO] 有 {not_installed} 个工具未安装")
    
    def _show_add_dialog(self):
        """显示新增工具对话框"""
        dialog = AddToolDialog(self, on_save=self._on_add_tool)
        self.wait_window(dialog)
    
    def _on_add_tool(self, tool_data: dict):
        """添加工具回调"""
        for tool in self.tools:
            if tool.id == tool_data["id"] or tool.package == tool_data["package"]:
                messagebox.showwarning("提示", f"工具 {tool_data['name']} 已存在！")
                return
        
        new_tool = ToolInfo(
            id=tool_data["id"],
            name=tool_data["name"],
            package=tool_data["package"],
            category=tool_data["category"],
            builtin=False,
            note=tool_data.get("note", ""),
            github_repo=tool_data.get("githubRepo", "")
        )
        
        self.tools.append(new_tool)
        self._save_config()
        self._update_category_list()
        self._apply_filter()
        self._log(f"[SUCCESS] 已添加工具: {new_tool.name}")
    
    def _show_edit_dialog(self, tool: ToolInfo):
        """显示编辑工具对话框"""
        tool_data = tool_to_dict(tool)
        dialog = EditToolDialog(
            self,
            tool_data,
            on_save=self._on_edit_tool,
            on_delete=self._on_delete_tool
        )
        self.wait_window(dialog)
    
    def _on_edit_tool(self, tool_data: dict):
        """编辑工具回调"""
        for tool in self.tools:
            if tool.id == tool_data["id"]:
                tool.name = tool_data["name"]
                tool.package = tool_data["package"]
                tool.category = tool_data["category"]
                tool.note = tool_data.get("note", "")
                tool.github_repo = tool_data.get("githubRepo", "")
                break
        
        self._save_config()
        self._update_category_list()
        self._apply_filter()
        self._log(f"[SUCCESS] 已更新工具: {tool_data['name']}")
    
    def _on_delete_tool(self, tool_id: str):
        """删除工具回调"""
        tool_name = ""
        for tool in self.tools:
            if tool.id == tool_id:
                tool_name = tool.name
                break
        
        self.tools = [t for t in self.tools if t.id != tool_id]
        self._save_config()
        self._update_category_list()
        self._apply_filter()
        self._log(f"[SUCCESS] 已删除工具: {tool_name}")
    
    def _save_config(self):
        """保存配置"""
        config = load_tools_config()
        config["tools"] = [tool_to_dict(t) for t in self.tools]
        save_tools_config(config)
    
    def _on_install_tool(self, tool: ToolInfo):
        """安装/升级工具"""
        if self._is_busy:
            return
        
        self._set_busy(True)
        action = "升级" if tool.installed_version else "安装"
        self._set_status(f"正在{action} {tool.name}...")
        
        def do_install():
            success, msg = install_tool(tool, lambda m: self.after(0, lambda: self._log(m)))
            
            if success:
                check_tool_status(tool)
                self.after(0, lambda: self.tool_list.refresh_tool(tool))
            
            self.after(0, lambda: self._on_install_complete(success, tool.name, action))
        
        thread = threading.Thread(target=do_install, daemon=True)
        thread.start()
    
    def _on_install_complete(self, success: bool, tool_name: str, action: str):
        """安装完成回调"""
        self._set_busy(False)
        self._set_status("就绪")
        
        if success:
            messagebox.showinfo("成功", f"{tool_name} {action}成功！")
        else:
            messagebox.showerror("失败", f"{tool_name} {action}失败，请查看日志。")
    
    def _install_selected(self):
        """安装/升级选中的工具"""
        tool = self.tool_list.get_selected_tool()
        if not tool:
            messagebox.showwarning("提示", "请先选择一个工具！")
            return
        
        if tool.installed_version is None and tool.latest_version is None:
            self._refresh_single_tool(tool)
            return
        
        if tool.status not in (ToolStatus.NOT_INSTALLED, ToolStatus.UPGRADABLE):
            messagebox.showinfo("提示", f"{tool.name} 已是最新版本！")
            return
        
        self._on_install_tool(tool)
    
    def _upgrade_all(self):
        """升级所有可升级的工具"""
        upgradable = self.tool_list.get_upgradable_tools()
        
        if not upgradable:
            messagebox.showinfo("提示", "没有可升级的工具！\n请先点击\"刷新全部\"检测版本。")
            return
        
        if not messagebox.askyesno(
            "确认",
            f"发现 {len(upgradable)} 个工具可升级，是否全部升级？"
        ):
            return
        
        if self._is_busy:
            return
        
        self._set_busy(True)
        self._set_status(f"正在升级 {len(upgradable)} 个工具...")
        
        def do_upgrade_all():
            success_count = 0
            fail_count = 0
            
            for i, tool in enumerate(upgradable):
                self.after(0, lambda t=tool, idx=i: self._set_status(
                    f"正在升级 {t.name} ({idx+1}/{len(upgradable)})..."
                ))
                
                success, msg = install_tool(
                    tool,
                    lambda m: self.after(0, lambda: self._log(m))
                )
                
                if success:
                    success_count += 1
                    check_tool_status(tool)
                    self.after(0, lambda t=tool: self.tool_list.refresh_tool(t))
                else:
                    fail_count += 1
            
            self.after(0, lambda: self._on_upgrade_all_complete(success_count, fail_count))
        
        thread = threading.Thread(target=do_upgrade_all, daemon=True)
        thread.start()
    
    def _on_upgrade_all_complete(self, success: int, fail: int):
        """全部升级完成回调"""
        self._set_busy(False)
        self._set_status("就绪")
        
        message = f"升级完成！\n成功: {success} 个"
        if fail > 0:
            message += f"\n失败: {fail} 个"
        
        messagebox.showinfo("升级完成", message)
    
    def _export_config(self):
        """导出配置到 JSON 文件"""
        file_path = filedialog.asksaveasfilename(
            title="导出工具配置",
            defaultextension=".json",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")],
            initialfile="ai-cli-tools-config.json"
        )
        
        if not file_path:
            return
        
        try:
            config = {
                "tools": [tool_to_dict(t) for t in self.tools],
                "exported_by": f"{APP_NAME} v{APP_VERSION}"
            }
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self._log(f"[SUCCESS] 配置已导出到: {file_path}")
            messagebox.showinfo("导出成功", f"已导出 {len(self.tools)} 个工具配置")
        
        except Exception as e:
            self._log(f"[ERROR] 导出失败: {str(e)}")
            messagebox.showerror("导出失败", str(e))
    
    def _import_config(self):
        """导入配置"""
        file_path = filedialog.askopenfilename(
            title="导入工具配置",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            imported_tools = config.get("tools", [])
            if not imported_tools:
                messagebox.showwarning("导入提示", "配置文件中没有工具数据")
                return
            
            added = 0
            skipped = 0
            existing_ids = {t.id for t in self.tools}
            existing_packages = {t.package for t in self.tools}
            
            for tool_data in imported_tools:
                if tool_data.get("id") in existing_ids or tool_data.get("package") in existing_packages:
                    skipped += 1
                    continue
                
                new_tool = ToolInfo(
                    id=tool_data.get("id", ""),
                    name=tool_data.get("name", ""),
                    package=tool_data.get("package", ""),
                    category=tool_data.get("category", "其他"),
                    builtin=False,
                    note=tool_data.get("note", ""),
                    github_repo=tool_data.get("githubRepo", "")
                )
                self.tools.append(new_tool)
                existing_ids.add(new_tool.id)
                existing_packages.add(new_tool.package)
                added += 1
            
            self._save_config()
            self._update_category_list()
            self._apply_filter()
            
            self._log(f"[SUCCESS] 导入完成: 新增 {added} 个, 跳过 {skipped} 个已存在")
            messagebox.showinfo("导入完成", f"新增: {added} 个工具\n跳过: {skipped} 个已存在")
        
        except Exception as e:
            self._log(f"[ERROR] 导入失败: {str(e)}")
            messagebox.showerror("导入失败", str(e))
    
    def _toggle_theme(self):
        """切换深色/浅色主题"""
        current = get_current_theme_name()
        new_theme = DARK_THEME if current == DEFAULT_THEME else DEFAULT_THEME
        
        self.style.theme_use(new_theme)
        set_current_theme_name(new_theme)
        
        # 更新按钮文本/图标
        if new_theme == DARK_THEME:
            self.theme_btn.configure(text="☀️")
            self.statusbar.configure(bootstyle="inverse-dark")
        else:
            self.theme_btn.configure(text="🌙")
            self.statusbar.configure(bootstyle="inverse-light")
        
        # 更新日志颜色
        self._update_log_colors()
        
        # 通知工具列表更新（如果需要）
        # self.tool_list.update_theme() # ToolList now uses ttk widgets so they should auto update mostly
        
        self._log(f"[INFO] 已切换到{'深色' if new_theme == DARK_THEME else '浅色'}主题")
    
    def _show_changelog_dialog(self, tool: ToolInfo):
        """显示更新日志"""
        repo = tool.github_repo
        if not repo:
            repo = get_github_repo_from_npm(tool.package)
        
        if not repo:
            messagebox.showinfo(
                "提示",
                f"{tool.name} 没有配置 GitHub 仓库，无法获取更新日志。\n"
                f"您可以在编辑工具时添加 GitHub 仓库地址。"
            )
            return
        
        self._set_status(f"正在获取 {tool.name} 的更新日志...")
        self._log(f"[INFO] 获取 {tool.name} 更新日志...")
        
        def fetch_changelog():
            changelog_text = get_changelog(repo)
            self.after(0, lambda: self._display_changelog(tool.name, changelog_text))
        
        threading.Thread(target=fetch_changelog, daemon=True).start()
    
    def _display_changelog(self, tool_name: str, content: str):
        """显示更新日志对话框 - 移到主线程"""
        self._set_status("就绪")
        dialog = ChangelogDialog(self, tool_name, content)
        dialog.show()
