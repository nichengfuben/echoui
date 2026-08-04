from __future__ import annotations

import asyncio
import sys
from typing import TYPE_CHECKING

from echoui.adapters.base_adapter import BaseAdapter

if TYPE_CHECKING:
    from echoui.components.base_component import BaseComponent


class _WritableComponent:
    """Internal protocol for components with write/writeln methods."""

    def write(self, text: str) -> None: ...
    def writeln(self, text: str) -> None: ...


class TerminalAdapter(BaseAdapter):
    """终端适配器。

    负责将 EchoUI 组件与终端环境进行桥接，管理组件的生命周期
    和事件循环。支持同步和异步两种运行模式。

    Examples:
        >>> from echoui.components.key_value_list import KeyValueList
        >>> kvl = KeyValueList().add("key", "value")
        >>> adapter = TerminalAdapter(kvl)
    """

    def __init__(self, ui: BaseComponent) -> None:
        """初始化 TerminalAdapter 实例。

        Args:
            ui: 要适配的 UI 组件实例。
        """
        super().__init__()
        self._ui: BaseComponent = ui

    def _write(self, text: str) -> None:
        """Write text to output, handling components with or without write method."""
        if hasattr(self._ui, "write"):
            getattr(self._ui, "write")(text)
        else:
            sys.stdout.write(text)

    def _writeln(self, text: str) -> None:
        """Write line to output, handling components with or without writeln method."""
        if hasattr(self._ui, "writeln"):
            getattr(self._ui, "writeln")(text)
        else:
            sys.stdout.write(text + "\n")

    def run(self) -> None:
        """启动终端适配器的同步主循环。

        渲染 UI 组件内容并输出到终端，设置运行标志为 ``True``。
        """
        self._running = True
        rendered = self._ui.render()
        self._write(rendered)
        self._writeln("")
        self._running = False

    def stop(self) -> None:
        """停止终端适配器的运行。

        将运行标志设置为 ``False``。
        """
        self._running = False

    async def run_async(self) -> None:
        """异步启动终端适配器的主循环。

        在 asyncio 事件循环中渲染 UI 组件并输出内容。
        """
        self._running = True
        rendered = self._ui.render()

        def _write(text: str) -> None:
            self._write(text)
            self._writeln("")
            sys.stdout.flush()

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
        await loop.run_in_executor(None, _write, rendered)
        self._running = False
