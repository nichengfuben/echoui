from __future__ import annotations

import logging
import threading
from typing import Any, Optional

from echoui.adapters.base_adapter import BaseAdapter
from echoui.components.console_ui import ConsoleUI

logger = logging.getLogger(__name__)


class TkinterAdapter(BaseAdapter):
    """Tkinter 桌面适配器。

    将 EchoUI 组件渲染为 Tkinter 窗口控件。
    使用标准库，无需额外依赖。

    Examples:
        >>> from echoui.components.console_ui import ConsoleUI
        >>> ui = ConsoleUI(normal_mode=True)
        >>> adapter = TkinterAdapter(ui=ui)
        >>> adapter.title
        'EchoUI'
    """

    def __init__(
        self,
        ui: ConsoleUI,
        title: str = "EchoUI",
        width: int = 800,
        height: int = 600,
    ) -> None:
        """初始化 Tkinter 适配器。

        Args:
            ui: ConsoleUI 主控制器实例。
            title: 窗口标题。
            width: 窗口宽度。
            height: 窗口高度。
        """
        super().__init__(host="localhost", port=0)
        self._ui = ui
        self._title = title
        self._width = width
        self._height = height
        self._root: Optional[Any] = None

    @property
    def title(self) -> str:
        """窗口标题。"""
        return self._title

    @property
    def ui(self) -> ConsoleUI:
        """返回绑定的 ConsoleUI 实例。"""
        return self._ui

    def run(self) -> None:
        """同步阻塞启动 Tkinter 窗口。"""
        import tkinter as tk

        self._root = tk.Tk()
        self._root.title(self._title)
        self._root.geometry(f"{self._width}x{self._height}")

        text_frame = tk.Frame(self._root)
        text_frame.pack(fill=tk.BOTH, expand=True)
        text_widget = tk.Text(text_frame, wrap=tk.WORD)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)

        text_widget.insert(tk.END, "EchoUI 桌面应用已启动\n")
        logger.info("Tkinter 窗口已启动: %s", self._title)

        self._root.protocol("WM_DELETE_WINDOW", self.stop)
        self._root.mainloop()

    async def run_async(self) -> None:
        """异步启动 Tkinter 窗口（通过后台线程）。"""
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def stop(self) -> None:
        """关闭 Tkinter 窗口。"""
        if self._root is not None:
            self._root.quit()
            self._root.destroy()
            self._root = None
            logger.info("Tkinter 窗口已关闭")
