from __future__ import annotations

import sys
from typing import Any, TextIO

# Adapters
from echoui.adapters.aiohttp_adapter import AiohttpAdapter
from echoui.adapters.terminal_adapter import TerminalAdapter

# Common components
from echoui.components.block_art import BlockArt
from echoui.components.box_builder import BoxBuilder

# Main controller
from echoui.components.console_ui import ConsoleUI
from echoui.components.notification import Notification
from echoui.components.progress_bar import ProgressBar
from echoui.components.spinner import Spinner
from echoui.components.table_builder import TableBuilder
from echoui.core.event_bus import EventBus

# Exceptions
from echoui.core.exceptions import (
    AdapterError,
    ConfigError,
    EchoError,
    InputError,
    RenderError,
)

# Core engine
from echoui.core.renderer import GradientRenderer
from echoui.core.state import State
from echoui.core.theme import Theme, ThemeConfig


def echoui(
    *,
    normal_mode: bool = False,
    theme: str = "default",
    stream: TextIO | None = None,
) -> "EchoUI":
    """创建 EchoUI 统一入口。

    这是使用 EchoUI 的最简单方式。
    返回的 EchoUI 实例提供所有组件的快捷方法。

    Args:
        normal_mode: 是否启用降级模式（无 ANSI 颜色）。
        theme: 主题名称，默认 "default"。
        stream: 输出流，默认 sys.stdout。

    Returns:
        EchoUI: 统一入口实例。

    Examples:
        >>> ui = echoui(normal_mode=True)  # doctest: +SKIP
        >>> ui.title("Hello").block("OK").info("Ready").print()  # doctest: +SKIP
    """
    return EchoUI(
        normal_mode=normal_mode,
        theme=theme,
        stream=stream,
    )


class EchoUI:
    """EchoUI 统一入口类。

    整合所有组件，提供链式调用的简洁 API。
    所有方法均返回 self，支持任意链式组合。

    Examples:
        >>> ui = echoui(normal_mode=True)  # doctest: +SKIP
        >>> (  # doctest: +SKIP
        ...     ui.title("Dashboard")
        ...     .block("OK")
        ...     .table(["Name", "Status"], [["App", "Running"]])
        ...     .success("All systems operational")
        ...     .print()
        ... )
    """

    def __init__(
        self,
        *,
        normal_mode: bool = False,
        theme: str = "default",
        stream: TextIO | None = None,
    ) -> None:
        """初始化 EchoUI 实例。

        Args:
            normal_mode: 降级模式开关。
            theme: 主题名称。
            stream: 输出流。
        """
        self._theme_cfg = Theme.get(theme)
        self._normal_mode = normal_mode
        self._stream = stream or sys.stdout
        self._buffer: list[str] = []
        self._ui = ConsoleUI(
            normal_mode=normal_mode,
            theme=self._theme_cfg,
        )
        self._ui._output_stream = self._stream

    # ---- 输出控制 ----

    def print(self) -> "EchoUI":
        """刷新缓冲区到输出流。

        Returns:
            EchoUI: 自身引用。
        """
        for line in self._buffer:
            self._stream.write(line + "\n")
        self._stream.flush()
        self._buffer.clear()
        return self

    def clear(self) -> "EchoUI":
        """清空缓冲区。

        Returns:
            EchoUI: 自身引用。
        """
        self._buffer.clear()
        return self

    # ---- 块艺术 ----

    def block(self, text: str) -> "EchoUI":
        """添加块字符艺术。

        Args:
            text: 要渲染的文本（建议短文本，1-8 字符）。

        Returns:
            EchoUI: 自身引用。
        """
        art = BlockArt(text=text, normal_mode=self._normal_mode).render()
        self._buffer.extend(art.split("\n"))
        return self

    # ---- 通知 ----

    def success(self, message: str) -> "EchoUI":
        """添加成功通知。

        Args:
            message: 通知消息。

        Returns:
            EchoUI: 自身引用。
        """
        n = Notification(
            normal_mode=self._normal_mode,
            theme=self._theme_cfg,
        )
        self._buffer.append(n.success(message).render())
        return self

    def warning(self, message: str) -> "EchoUI":
        """添加警告通知。"""
        n = Notification(
            normal_mode=self._normal_mode,
            theme=self._theme_cfg,
        )
        self._buffer.append(n.warning(message).render())
        return self

    def error(self, message: str) -> "EchoUI":
        """添加错误通知。"""
        n = Notification(
            normal_mode=self._normal_mode,
            theme=self._theme_cfg,
        )
        self._buffer.append(n.error(message).render())
        return self

    def info(self, message: str) -> "EchoUI":
        """添加信息通知。"""
        n = Notification(
            normal_mode=self._normal_mode,
            theme=self._theme_cfg,
        )
        self._buffer.append(n.info(message).render())
        return self

    # ---- 框体 ----

    def box(self, content: str, title: str = "") -> "EchoUI":
        """添加框体。

        Args:
            content: 框内内容。
            title: 框标题。

        Returns:
            EchoUI: 自身引用。
        """
        b = BoxBuilder(
            normal_mode=self._normal_mode,
            theme=self._theme_cfg,
        )
        self._buffer.extend(b.content(content).title(title).build().split("\n"))
        return self

    # ---- 表格 ----

    def table(
        self,
        headers: list[str],
        rows: list[list[str]],
    ) -> "EchoUI":
        """添加表格。

        Args:
            headers: 表头列表。
            rows: 数据行列表。

        Returns:
            EchoUI: 自身引用。
        """
        t = TableBuilder(
            normal_mode=self._normal_mode,
            theme=self._theme_cfg,
        )
        t.set_headers(headers)
        for row in rows:
            t.add_row(row)
        self._buffer.extend(t.render().split("\n"))
        return self

    # ---- 标题/分隔线 ----

    def title(self, text: str) -> "EchoUI":
        """添加标题行。

        Args:
            text: 标题文本。

        Returns:
            EchoUI: 自身引用。
        """
        self._buffer.append(text)
        return self

    def rule(self, char: str = "=", width: int = 40) -> "EchoUI":
        """添加分隔线。

        Args:
            char: 分隔字符。
            width: 分隔线宽度。

        Returns:
            EchoUI: 自身引用。
        """
        self._buffer.append(char * width)
        return self

    def newline(self) -> "EchoUI":
        """添加空行。

        Returns:
            EchoUI: 自身引用。
        """
        self._buffer.append("")
        return self

    # ---- 进度条 ----

    def progress(self, current: int, total: int, message: str = "") -> "EchoUI":
        """添加进度条。

        Args:
            current: 当前进度。
            total: 总进度。
            message: 前方提示消息。

        Returns:
            EchoUI: 自身引用。
        """
        p = ProgressBar(
            current=current,
            total=total,
            normal_mode=self._normal_mode,
            theme_name=self._theme_cfg.name,
            message=message,
        )
        self._buffer.append(p.render())
        return self

    # ---- 键值列表 ----

    def kv(self, **pairs: str) -> "EchoUI":
        """添加键值对列表。

        Args:
            **pairs: 键值对关键字参数。

        Returns:
            EchoUI: 自身引用。

        Examples:
            >>> ui = echoui(normal_mode=True)  # doctest: +SKIP
            >>> ui.kv(name="EchoUI", version="2.0.0").print()  # doctest: +SKIP
        """
        from echoui.components.key_value_list import KeyValueList

        kvl = KeyValueList()
        for k, v in pairs.items():
            kvl.add(k, v)
        self._buffer.extend(kvl.render().split("\n"))
        return self

    # ---- 树形结构 ----

    def tree(self, data: dict[str, Any]) -> "EchoUI":
        """添加树形结构。

        Args:
            data: 嵌套字典数据。

        Returns:
            EchoUI: 自身引用。
        """
        from echoui.components.tree_view import TreeView

        t = TreeView(data=data, normal_mode=self._normal_mode)
        self._buffer.extend(t.render().split("\n"))
        return self


__version__: str = "2.0.0"
__all__: list[str] = [
    "echoui",
    "EchoUI",
    "GradientRenderer",
    "Theme",
    "ThemeConfig",
    "State",
    "EventBus",
    "ConsoleUI",
    "BoxBuilder",
    "BlockArt",
    "TableBuilder",
    "ProgressBar",
    "Spinner",
    "Notification",
    "TerminalAdapter",
    "AiohttpAdapter",
    "EchoError",
    "ConfigError",
    "RenderError",
    "AdapterError",
    "InputError",
]
