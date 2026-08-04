from __future__ import annotations

import sys
import time
from typing import Any, Optional, TextIO

from echoui.components.base_component import BaseComponent


class Timer(BaseComponent):
    """计时器组件，用于测量代码执行时间。

    记录开始和结束时间，渲染为可读的耗时字符串。
    支持异步上下文管理器协议，可与 async with 语句配合使用。
    """

    def __init__(
        self,
        message: str = "Elapsed",
        theme_name: str = "default",
        normal_mode: bool = False,
        _output_stream: Optional[TextIO] = None,
    ) -> None:
        """初始化计时器组件。

        Args:
            message: 计时结果的前缀消息。
            theme_name: 主题名称。
            normal_mode: 是否启用正常模式（无彩色输出）。
            _output_stream: 输出流，默认为 sys.stdout。
        """
        from echoui.core.theme import Theme

        theme = Theme.get(theme_name)
        super().__init__(theme=theme, normal_mode=normal_mode)
        self._theme_name = theme_name
        self._message = message
        self._output_stream = _output_stream if _output_stream else sys.stdout
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None

    @property
    def elapsed(self) -> float:
        """返回已计时时间（秒）。

        Returns:
            float: 经过的秒数。如果未开始计时则返回 0.0。
        """
        if self._start_time is None:
            return 0.0
        end = self._end_time if self._end_time is not None else time.monotonic()
        return end - self._start_time

    def start(self) -> "Timer":
        """记录开始时间。

        Returns:
            self: 支持方法链调用。
        """
        self._start_time = time.monotonic()
        self._end_time = None
        return self

    def stop(self) -> "Timer":
        """记录结束时间。

        Returns:
            self: 支持方法链调用。
        """
        self._end_time = time.monotonic()
        return self

    def render(self) -> str:
        """渲染计时结果为字符串。

        Returns:
            str: 格式化的计时结果，如 "Elapsed: 1.23s"。
        """
        elapsed = self.elapsed
        return f"{self._message}: {elapsed:.2f}s"

    def print_elapsed(self) -> "Timer":
        """渲染并输出当前计时结果。

        Returns:
            self: 支持方法链调用。
        """
        output = self.render()
        self._output_stream.write(output)
        self._output_stream.write("\n")
        return self

    async def __aenter__(self) -> "Timer":
        """异步上下文管理器入口，自动开始计时。

        Returns:
            self: Timer 实例。
        """
        self.start()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """异步上下文管理器出口，自动停止计时。

        Args:
            exc_type: 异常类型。
            exc_val: 异常值。
            exc_tb: 回溯对象。
        """
        self.stop()
