"""
编辑工具对话框
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import re

from .styles import FONTS, PADDING
from .add_tool_dialog import extract_package_name


class EditToolDialog(ttk.Toplevel):
    """编辑工具对话框"""
    
    def __init__(self, parent, tool_data: dict, on_save=None, on_delete=None):
        super().__init__(parent)
        self.title("编辑工具")
        
        self.tool_data = tool_data
        self.on_save = on_save
        self.on_delete = on_delete
        self.result = None
        
        self._setup_window(parent)
        self._create_widgets()
        self._load_data()
        
    def _setup_window(self, parent):
        """设置窗口"""
        self.resizable(False, False)
        
        # 模态
        self.transient(parent)
        self.grab_set()
        
        # 居中
        self.update_idletasks()
        try:
            x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
            y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
            self.geometry(f"+{x}+{y}")
        except:
            self.place_window_center()
        
    def _create_widgets(self):
        """创建控件"""
        # 主框架
        main_frame = ttk.Frame(self, padding=PADDING["large"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 内置工具提示
        self.builtin_label = ttk.Label(
            main_frame,
            text="⚠️ 这是内置工具，部分字段不可修改",
            font=FONTS["small"],
            bootstyle=WARNING
        )
        
        # 工具显示名称
        ttk.Label(main_frame, text="工具显示名称:", font=FONTS["body"]).grid(
            row=1, column=0, sticky=tk.W, pady=PADDING["small"]
        )
        self.name_entry = ttk.Entry(main_frame, width=40, font=FONTS["body"])
        self.name_entry.grid(row=1, column=1, pady=PADDING["small"])
        
        # NPM 包名
        ttk.Label(main_frame, text="NPM 包名:", font=FONTS["body"]).grid(
            row=2, column=0, sticky=tk.W, pady=PADDING["small"]
        )
        self.package_entry = ttk.Entry(main_frame, width=40, font=FONTS["body"])
        self.package_entry.grid(row=2, column=1, pady=PADDING["small"])
        
        # 分类
        ttk.Label(main_frame, text="分类:", font=FONTS["body"]).grid(
            row=3, column=0, sticky=tk.W, pady=PADDING["small"]
        )
        self.category_var = tk.StringVar(value="AI助手")
        categories = ["AI助手", "AI编程助手", "开发工具", "其他"]
        self.category_combo = ttk.Combobox(
            main_frame,
            textvariable=self.category_var,
            values=categories,
            width=38,
            font=FONTS["body"],
            state="readonly",
            bootstyle=PRIMARY
        )
        self.category_combo.grid(row=3, column=1, pady=PADDING["small"])
        
        # GitHub 仓库
        ttk.Label(main_frame, text="GitHub 仓库:", font=FONTS["body"]).grid(
            row=4, column=0, sticky=tk.W, pady=PADDING["small"]
        )
        self.github_entry = ttk.Entry(main_frame, width=40, font=FONTS["body"])
        self.github_entry.grid(row=4, column=1, pady=PADDING["small"])
        
        # GitHub 仓库提示
        github_hint = ttk.Label(
            main_frame,
            text="💡 如: anthropics/claude-code (用于获取最新版本)",
            font=FONTS["small"],
            bootstyle=SECONDARY
        )
        github_hint.grid(row=5, column=1, sticky=tk.W)
        
        # 备注
        ttk.Label(main_frame, text="备注:", font=FONTS["body"]).grid(
            row=6, column=0, sticky=tk.W, pady=PADDING["small"]
        )
        self.note_entry = ttk.Entry(main_frame, width=40, font=FONTS["body"])
        self.note_entry.grid(row=6, column=1, pady=PADDING["small"])
        
        # 按钮框
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(PADDING["large"], 0))
        
        # 删除按钮（红色）
        self.delete_btn = ttk.Button(
            button_frame,
            text="🗑️ 删除工具",
            command=self._on_delete,
            bootstyle=DANGER
        )
        self.delete_btn.pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Button(
            button_frame,
            text="取消",
            command=self._on_cancel,
            bootstyle=SECONDARY
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Button(
            button_frame,
            text="保存修改",
            command=self._on_save,
            bootstyle=SUCCESS
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        self.bind("<Return>", lambda e: self._on_save())
        self.bind("<Escape>", lambda e: self._on_cancel())
    
    def _load_data(self):
        """加载工具数据"""
        self.name_entry.insert(0, self.tool_data.get("name", ""))
        self.package_entry.insert(0, self.tool_data.get("package", ""))
        self.category_var.set(self.tool_data.get("category", "AI助手"))
        self.github_entry.insert(0, self.tool_data.get("githubRepo", ""))
        self.note_entry.insert(0, self.tool_data.get("note", ""))
        
        # 内置工具限制编辑
        if self.tool_data.get("builtin", False):
            self.builtin_label.grid(row=0, column=0, columnspan=2, pady=PADDING["small"])
            self.package_entry.configure(state="disabled")
            self.delete_btn.configure(state="disabled")
    
    def _validate(self) -> bool:
        """验证输入"""
        name = self.name_entry.get().strip()
        package = self.package_entry.get().strip()
        
        if not name:
            messagebox.showwarning("提示", "请输入工具显示名称", parent=self)
            self.name_entry.focus_set()
            return False
        
        if not package:
            messagebox.showwarning("提示", "请输入 NPM 包名", parent=self)
            self.package_entry.focus_set()
            return False
        
        return True
    
    def _on_save(self):
        """保存修改"""
        if not self._validate():
            return
        
        package = self.package_entry.get().strip()
        package = extract_package_name(package)
        
        self.result = {
            "id": self.tool_data.get("id"),
            "name": self.name_entry.get().strip(),
            "package": package,
            "category": self.category_var.get(),
            "note": self.note_entry.get().strip(),
            "builtin": self.tool_data.get("builtin", False),
            "githubRepo": self.github_entry.get().strip()
        }
        
        if self.tool_data.get("installType"):
            self.result["installType"] = self.tool_data["installType"]
        if self.tool_data.get("installCommands"):
            self.result["installCommands"] = self.tool_data["installCommands"]
        if self.tool_data.get("versionCommand"):
            self.result["versionCommand"] = self.tool_data["versionCommand"]
        
        if self.on_save:
            self.on_save(self.result)
        
        self.destroy()
    
    def _on_delete(self):
        """删除工具"""
        if self.tool_data.get("builtin", False):
            messagebox.showwarning("提示", "内置工具不可删除", parent=self)
            return
        
        if not messagebox.askyesno(
            "确认删除",
            f"确定要删除工具 \"{self.tool_data.get('name')}\" 吗？\n此操作不可撤销。",
            parent=self
        ):
            return
        
        if self.on_delete:
            self.on_delete(self.tool_data.get("id"))
        
        self.destroy()
    
    def _on_cancel(self):
        """取消"""
        self.result = None
        self.destroy()
