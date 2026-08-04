"""EchoUI 桌面应用演示程序。

展示如何使用桌面适配器（Tkinter/PyQt）运行 EchoUI。
"""
from __future__ import annotations

import sys

# 确保项目路径可用
sys.path.insert(0, "src")

from echoui import EchoUI


def main() -> None:
    """运行桌面应用演示。"""
    ui = EchoUI(normal_mode=True)

    ui.rule("=").title("EchoUI 桌面应用演示").rule("=").newline()

    ui.box(
        "EchoUI 支持多种桌面后端:\n\n"
        "- TkinterAdapter (标准库，跨平台)\n"
        "- PyQtAdapter (PyQt5/PyQt6，专业桌面)\n\n"
        "适配器层将终端 UI 组件映射到桌面控件。\n"
        "当前需实现对应的适配器模块。",
        title="桌面后端支持",
    ).newline()

    ui.table(
        headers=["适配器", "依赖", "特点"],
        rows=[
            ["TkinterAdapter", "标准库", "跨平台，无需安装"],
            ["PyQtAdapter", "PyQt5/6", "专业桌面，信号槽"],
            ["TerminalAdapter", "无", "终端 UI，纯文本"],
        ],
    ).newline()

    ui.warning("桌面适配器待实现").success("核心组件已全部就绪").print()


if __name__ == "__main__":
    main()
