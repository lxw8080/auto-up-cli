"""
新增工具对话框
支持从完整安装命令自动提取包名
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import re

from .styles import FONTS, PADDING

def extract_package_name(input_text: str) -> str:
    """
    从用户输入中提取 npm 包名
    """
    text = input_text.strip()
    
    prefixes_to_remove = [
        r'^npm\s+install\s+(-g\s+)?',
        r'^npm\s+i\s+(-g\s+)?',
        r'^npx\s+',
        r'^pnpm\s+add\s+(-g\s+)?',
        r'^yarn\s+global\s+add\s+',
    ]
    
    for pattern in prefixes_to_remove:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    text = re.sub(r'@(latest|next|beta|alpha|\d+\.\d+\.\d+.*)$', '', text)
    
    return text.strip()


def make_tool_id(package: str) -> str:
    """
    生成工具 ID，避免 scoped 包冲突
    """
    package = package.strip()
    if package.startswith("@") and "/" in package:
        return package
    if "/" in package:
        return package.split("/")[-1]
    return package


class AddToolDialog(ttk.Toplevel):
    """新增工具对话框"""
    
    def __init__(self, parent, on_save=None):
        super().__init__(parent)
        self.title("新增 AI CLI 工具")
        
        self.on_save = on_save
        self.result = None
        
        self._setup_window(parent)
        self._create_widgets()
        
    def _setup_window(self, parent):
        """设置窗口"""
        self.resizable(False, False)
        
        # 模态设置
        self.transient(parent)
        self.grab_set()
        
        # 居中显示
        self.update_idletasks()
        try:
            x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
            y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
            self.geometry(f"+{x}+{y}")
        except:
            # Fallback if parent not ready
            self.place_window_center()
        
    def _create_widgets(self):
        """创建控件"""
        # 主框架
        main_frame = ttk.Frame(self, padding=PADDING["large"])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 工具显示名称
        ttk.Label(main_frame, text="工具显示名称:", font=FONTS["body"]).grid(
            row=0, column=0, sticky=tk.W, pady=PADDING["small"]
        )
        self.name_entry = ttk.Entry(main_frame, width=40, font=FONTS["body"])
        self.name_entry.grid(row=0, column=1, pady=PADDING["small"])
        
        # NPM 包名/安装命令
        ttk.Label(main_frame, text="NPM 包名或安装命令:", font=FONTS["body"]).grid(
            row=1, column=0, sticky=tk.W, pady=PADDING["small"]
        )
        self.package_entry = ttk.Entry(main_frame, width=40, font=FONTS["body"])
        self.package_entry.grid(row=1, column=1, pady=PADDING["small"])
        
        # 绑定输入事件，实时预览提取结果
        self.package_entry.bind("<KeyRelease>", self._on_package_input)
        self.package_entry.bind("<FocusOut>", self._on_package_focus_out)
        
        # 包名提示
        hint_label = ttk.Label(
            main_frame,
            text="💡 支持粘贴完整命令，如: npm install -g @google/gemini-cli",
            font=FONTS["small"],
            bootstyle=INFO
        )
        hint_label.grid(row=2, column=1, sticky=tk.W)
        
        # 提取结果预览
        self.preview_var = tk.StringVar(value="")
        self.preview_label = ttk.Label(
            main_frame,
            textvariable=self.preview_var,
            font=FONTS["small"],
            bootstyle=SUCCESS
        )
        self.preview_label.grid(row=3, column=1, sticky=tk.W)
        
        # 分类
        ttk.Label(main_frame, text="分类:", font=FONTS["body"]).grid(
            row=4, column=0, sticky=tk.W, pady=PADDING["small"]
        )
        self.category_var = tk.StringVar(value="AI助手")
        categories = ["AI助手", "AI编程助手", "开发工具", "其他"]
        self.category_combo = ttk.Combobox(
            main_frame,
            textvariable=self.category_var,
            values=categories,
            width=38, # slight adjust for ttk styling differenc
            font=FONTS["body"],
            state="readonly",
            bootstyle=PRIMARY
        )
        self.category_combo.grid(row=4, column=1, pady=PADDING["small"])
        
        # GitHub 仓库 (可选)
        ttk.Label(main_frame, text="GitHub 仓库 (可选):", font=FONTS["body"]).grid(
            row=5, column=0, sticky=tk.W, pady=PADDING["small"]
        )
        self.github_entry = ttk.Entry(main_frame, width=40, font=FONTS["body"])
        self.github_entry.grid(row=5, column=1, pady=PADDING["small"])
        
        # GitHub 仓库提示
        github_hint = ttk.Label(
            main_frame,
            text="💡 如: anthropics/claude-code (用于获取最新版本)",
            font=FONTS["small"],
            bootstyle=SECONDARY
        )
        github_hint.grid(row=6, column=1, sticky=tk.W)
        
        # 备注
        ttk.Label(main_frame, text="备注 (可选):", font=FONTS["body"]).grid(
            row=7, column=0, sticky=tk.W, pady=PADDING["small"]
        )
        self.note_entry = ttk.Entry(main_frame, width=40, font=FONTS["body"])
        self.note_entry.grid(row=7, column=1, pady=PADDING["small"])
        
        # 按钮框
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=(PADDING["large"], 0))
        
        ttk.Button(
            button_frame,
            text="取消",
            command=self._on_cancel,
            bootstyle=SECONDARY
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        ttk.Button(
            button_frame,
            text="确认添加",
            command=self._on_save,
            bootstyle=SUCCESS
        ).pack(side=tk.LEFT, padx=PADDING["small"])
        
        self.name_entry.focus_set()
        
        self.bind("<Return>", lambda e: self._on_save())
        self.bind("<Escape>", lambda e: self._on_cancel())
    
    def _on_package_input(self, event=None):
        """包名输入时实时预览"""
        raw_input = self.package_entry.get().strip()
        if not raw_input:
            self.preview_var.set("")
            return
        
        extracted = extract_package_name(raw_input)
        if extracted != raw_input:
            self.preview_var.set(f"✅ 将提取为: {extracted}")
        else:
            self.preview_var.set("")
    
    def _on_package_focus_out(self, event=None):
        """失去焦点时自动替换为提取后的包名"""
        raw_input = self.package_entry.get().strip()
        if not raw_input:
            return
        
        extracted = extract_package_name(raw_input)
        if extracted != raw_input:
            self.package_entry.delete(0, tk.END)
            self.package_entry.insert(0, extracted)
            self.preview_var.set(f"✅ 已自动提取: {extracted}")
    
    def _validate(self) -> bool:
        """验证输入"""
        name = self.name_entry.get().strip()
        package = self.package_entry.get().strip()
        
        if not name:
            messagebox.showwarning("提示", "请输入工具显示名称", parent=self)
            self.name_entry.focus_set()
            return False
        
        if not package:
            messagebox.showwarning("提示", "请输入 NPM 包名或安装命令", parent=self)
            self.package_entry.focus_set()
            return False
        
        extracted = extract_package_name(package)
        if not extracted:
            messagebox.showwarning("提示", "无法解析包名，请检查输入", parent=self)
            self.package_entry.focus_set()
            return False
        
        self.package_entry.delete(0, tk.END)
        self.package_entry.insert(0, extracted)
        
        return True
    
    def _on_save(self):
        """保存工具"""
        if not self._validate():
            return
        
        package = self.package_entry.get().strip()
        tool_id = make_tool_id(package)
        
        self.result = {
            "id": tool_id,
            "name": self.name_entry.get().strip(),
            "package": package,
            "category": self.category_var.get(),
            "note": self.note_entry.get().strip(),
            "githubRepo": self.github_entry.get().strip(),
            "builtin": False
        }
        
        if self.on_save:
            self.on_save(self.result)
        
        self.destroy()
    
    def _on_cancel(self):
        """取消"""
        self.result = None
        self.destroy()
