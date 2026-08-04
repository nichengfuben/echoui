"""EchoUI 终端演示程序。

展示所有核心组件在终端中的使用方式。
"""
from __future__ import annotations

import sys
import time

# 确保项目路径可用
sys.path.insert(0, "src")

from echoui import EchoUI


def main() -> None:
    """运行终端演示。"""
    ui = EchoUI(normal_mode=True)

    # 标题
    ui.block("EchoUI").rule("=").title("终端 UI 框架演示").newline()

    # 基本信息
    ui.kv(name="EchoUI", version="2.0.0", python="3.8-3.14").newline()

    # 框体
    ui.box("这是一个框体内容", title="欢迎").newline()

    # 表格
    ui.table(
        headers=["组件", "描述", "状态"],
        rows=[
            ["BoxBuilder", "框体容器", "完成"],
            ["TableBuilder", "表格渲染", "完成"],
            ["ProgressBar", "进度条", "完成"],
            ["Spinner", "加载动画", "完成"],
            ["Notification", "通知组件", "完成"],
        ],
    ).newline()

    # 进度条
    ui.progress(75, 100, "加载进度").newline()

    # 通知
    ui.success("所有组件加载成功").warning("部分功能待完善").info(
        "更多信息请查看文档"
    )

    ui.rule("=").print()


if __name__ == "__main__":
    main()
