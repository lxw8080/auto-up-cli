"""
AI CLI 工具管理器
跨平台 Python GUI 应用，用于检测、安装和升级 AI CLI 工具
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import MainWindow


def main():
    """主函数"""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
