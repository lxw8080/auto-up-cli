"""
更新日志对话框
显示工具的 GitHub Release Notes
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from .styles import FONTS, PADDING, get_text_colors, get_current_theme_name, DARK_THEME


class ChangelogDialog(ttk.Toplevel):
    """更新日志对话框"""
    
    def __init__(self, parent, tool_name: str, changelog: str):
        super().__init__(parent, title=f"更新日志 - {tool_name}")
        
        self.tool_name = tool_name
        self.changelog = changelog
        
        self._setup_window(parent)
        self._create_widgets()
        
    def _setup_window(self, parent):
        """设置窗口"""
        self.geometry("700x550")
        self.minsize(500, 400)
        
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
        
        # 标题
        title_label = ttk.Label(
            main_frame,
            text=f"📋 {self.tool_name} 更新日志",
            font=FONTS["heading"],
            bootstyle=PRIMARY
        )
        title_label.pack(fill=tk.X, pady=(0, PADDING["medium"]))
        
        # 日志内容区域
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text 控件颜色适配
        is_dark = get_current_theme_name() == DARK_THEME
        colors = get_text_colors(is_dark)
        
        self.text_widget = tk.Text(
            text_frame,
            font=FONTS["body"],
            wrap=tk.WORD,
            padx=10,
            pady=10,
            bg=colors["bg"],
            fg=colors["fg"],
            insertbackground=colors["insert"],
            bd=0,
            highlightthickness=0
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        # 插入内容
        self.text_widget.insert(tk.END, self.changelog)
        self.text_widget.configure(state=tk.DISABLED)
        
        # 配置简单的 Markdown 高亮
        self._configure_tags(is_dark)
        self._apply_highlighting()
        
        # 关闭按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(PADDING["medium"], 0))
        
        ttk.Button(
            button_frame,
            text="关闭",
            command=self.destroy,
            bootstyle=SECONDARY
        ).pack(side=tk.RIGHT)
        
        self.bind("<Escape>", lambda e: self.destroy())
    
    def _configure_tags(self, is_dark: bool):
        """配置文本标签样式"""
        if is_dark:
            h_color = "#569cd6"
            bold_color = "#dcdcaa"
            code_fg = "#ce9178"
            code_bg = "#2d2d2d"
        else:
            h_color = "#007acc"
            bold_color = "#795E26"
            code_fg = "#a31515"
            code_bg = "#f0f0f0"

        self.text_widget.tag_configure("h1", font=("Microsoft YaHei UI", 14, "bold"), foreground=h_color)
        self.text_widget.tag_configure("h2", font=("Microsoft YaHei UI", 12, "bold"), foreground=h_color)
        self.text_widget.tag_configure("bold", font=("Microsoft YaHei UI", 10, "bold"), foreground=bold_color)
        self.text_widget.tag_configure("bullet", foreground="#6a9955" if is_dark else "#008000")
        self.text_widget.tag_configure("code", font=("Consolas", 9), foreground=code_fg, background=code_bg)
    
    def _apply_highlighting(self):
        """应用简单的 Markdown 高亮"""
        content = self.text_widget.get("1.0", tk.END)
        
        # 按行处理
        for i, line in enumerate(content.split('\n'), 1):
            line_start = f"{i}.0"
            line_end = f"{i}.end"
            
            if line.startswith('## '):
                self.text_widget.tag_add("h2", line_start, line_end)
            elif line.startswith('# '):
                self.text_widget.tag_add("h1", line_start, line_end)
            elif line.startswith('**') and '**' in line[2:]:
                self.text_widget.tag_add("bold", line_start, line_end)
            elif line.strip().startswith('- ') or line.strip().startswith('* '):
                self.text_widget.tag_add("bullet", line_start, line_end)
