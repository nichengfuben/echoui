from __future__ import annotations

import logging
import sys
import threading
from typing import Any, Optional

from echoui.adapters.base_adapter import BaseAdapter
from echoui.components.console_ui import ConsoleUI

logger = logging.getLogger(__name__)


class PyQtAdapter(BaseAdapter):
    """PyQt5/PyQt6 桌面适配器。

    将 EchoUI 组件渲染为 PyQt 窗口控件。
    支持信号槽机制和专业桌面界面。

    Examples:
        >>> from echoui.components.console_ui import ConsoleUI
        >>> ui = ConsoleUI(normal_mode=True)
        >>> adapter = PyQtAdapter(ui=ui)
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
        """初始化 PyQt 适配器。

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
        self._app: Optional[Any] = None
        self._window: Optional[Any] = None

    @property
    def title(self) -> str:
        """窗口标题。"""
        return self._title

    @property
    def ui(self) -> ConsoleUI:
        """返回绑定的 ConsoleUI 实例。"""
        return self._ui

    def _get_qt_module(self) -> Any:
        """获取可用的 Qt 模块（PyQt6 > PyQt5）。"""
        try:
            from PyQt6 import QtWidgets
            return QtWidgets
        except ImportError:
            from PyQt5 import QtWidgets
            return QtWidgets

    def run(self) -> None:
        """同步阻塞启动 PyQt 窗口。"""
        QtWidgets = self._get_qt_module()

        self._app = QtWidgets.QApplication(sys.argv)
        self._window = QtWidgets.QMainWindow()
        self._window.setWindowTitle(self._title)
        self._window.resize(self._width, self._height)

        text_edit = QtWidgets.QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText("EchoUI 桌面应用已启动\n")
        self._window.setCentralWidget(text_edit)

        self._window.show()
        logger.info("PyQt 窗口已启动: %s", self._title)

        self._app.exec() if hasattr(self._app, "exec") else self._app.exec_()

    async def run_async(self) -> None:
        """异步启动 PyQt 窗口（通过后台线程）。"""
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def stop(self) -> None:
        """关闭 PyQt 窗口。"""
        if self._window is not None:
            self._window.close()
        if self._app is not None:
            self._app.quit()
        logger.info("PyQt 窗口已关闭")
