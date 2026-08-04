from __future__ import annotations

import sys
from typing import TYPE_CHECKING, TextIO

from echoui.components.base_component import BaseComponent
from echoui.components.box_builder import BoxBuilder
from echoui.components.notification import Notification
from echoui.components.table_builder import TableBuilder

if TYPE_CHECKING:
    from echoui.core.renderer import GradientRenderer
    from echoui.core.theme import ThemeConfig


class ConsoleUI(BaseComponent):
    """控制台 UI 主控制器，支持链式调用。

    提供打印、表格、框体、通知等快捷方法。

    Attributes:
        _output_stream: 输出流，默认为 sys.stdout。
    """

    def __init__(
        self,
        renderer: GradientRenderer | None = None,
        normal_mode: bool = False,
        theme: ThemeConfig | None = None,
    ) -> None:
        """初始化控制台。

        Args:
            renderer: 渐变渲染引擎。
            normal_mode: 降级模式开关。
            theme: 主题配置。
        """
        super().__init__(renderer=renderer, normal_mode=normal_mode, theme=theme)
        self._output_stream: TextIO = sys.stdout

    def print(self, text: str) -> "ConsoleUI":
        """打印文本（链式）。

        Args:
            text: 要打印的文本。

        Returns:
            ConsoleUI: 返回 self。
        """
        self._output_stream.write(text + "\n")
        self._output_stream.flush()
        return self

    def newline(self) -> "ConsoleUI":
        """打印空行（链式）。

        Returns:
            ConsoleUI: 返回 self。
        """
        self._output_stream.write("\n")
        self._output_stream.flush()
        return self

    def box(self, content: str, title: str = "") -> "ConsoleUI":
        """打印带框的内容（链式）。

        Args:
            content: 框内文字。
            title: 框标题。

        Returns:
            ConsoleUI: 返回 self。
        """
        builder = BoxBuilder(
            normal_mode=self._normal_mode,
            renderer=self._renderer,
            theme=self._theme,
        )
        result = builder.content(content).title(title).build()
        self._output_stream.write(result + "\n")
        self._output_stream.flush()
        return self

    def table(
        self,
        headers: list[str],
        rows: list[list[str]],
    ) -> "ConsoleUI":
        """打印表格（链式）。

        Args:
            headers: 表头列表。
            rows: 数据行列表。

        Returns:
            ConsoleUI: 返回 self。
        """
        builder = TableBuilder(
            normal_mode=self._normal_mode,
            renderer=self._renderer,
            theme=self._theme,
        )
        builder.set_headers(headers)
        for row in rows:
            builder.add_row(row)
        result = builder.render()
        self._output_stream.write(result + "\n")
        self._output_stream.flush()
        return self

    def rule(self, char: str = "=", width: int = 40) -> "ConsoleUI":
        """打印分隔线（链式）。

        Args:
            char: 分隔字符。
            width: 分隔线宽度。

        Returns:
            ConsoleUI: 返回 self。
        """
        self._output_stream.write(char * width + "\n")
        self._output_stream.flush()
        return self

    def success(self, message: str) -> "ConsoleUI":
        """打印成功消息（链式）。"""
        notif = Notification(
            normal_mode=self._normal_mode,
            renderer=self._renderer,
            theme=self._theme,
        )
        self._output_stream.write(notif.success(message).render() + "\n")
        self._output_stream.flush()
        return self

    def warning(self, message: str) -> "ConsoleUI":
        """打印警告消息（链式）。"""
        notif = Notification(
            normal_mode=self._normal_mode,
            renderer=self._renderer,
            theme=self._theme,
        )
        self._output_stream.write(notif.warning(message).render() + "\n")
        self._output_stream.flush()
        return self

    def error(self, message: str) -> "ConsoleUI":
        """打印错误消息（链式）。"""
        notif = Notification(
            normal_mode=self._normal_mode,
            renderer=self._renderer,
            theme=self._theme,
        )
        self._output_stream.write(notif.error(message).render() + "\n")
        self._output_stream.flush()
        return self

    def info(self, message: str) -> "ConsoleUI":
        """打印信息消息（链式）。"""
        notif = Notification(
            normal_mode=self._normal_mode,
            renderer=self._renderer,
            theme=self._theme,
        )
        self._output_stream.write(notif.info(message).render() + "\n")
        self._output_stream.flush()
        return self

    def render(self) -> str:
        """ConsoleUI 为控制器，不直接渲染。"""
        return ""
