from __future__ import annotations

import asyncio
from typing import Callable, Optional

from echoui.components.base_component import BaseComponent


class Countdown(BaseComponent):
    """倒计时组件，在指定秒数内每秒递减计数。

    支持自定义 tick 回调函数，每秒触发一次。
    渲染为可读的倒计时字符串。
    """

    def __init__(
        self,
        seconds: int,
        message: str = "",
        on_tick: Optional[Callable[[int], None]] = None,
        theme_name: str = "default",
        normal_mode: bool = False,
    ) -> None:
        """初始化倒计时组件。

        Args:
            seconds: 倒计时总秒数。
            message: 倒计时消息前缀。
            on_tick: 每秒触发的回调函数，参数为剩余秒数。
            theme_name: 主题名称。
            normal_mode: 是否启用正常模式（无彩色输出）。
        """
        from echoui.core.theme import Theme

        theme = Theme.get(theme_name)
        super().__init__(theme=theme, normal_mode=normal_mode)
        self._theme_name = theme_name
        self._seconds = seconds
        self._message = message
        self._on_tick = on_tick
        self._remaining = seconds

    @property
    def remaining(self) -> int:
        """返回剩余秒数。"""
        return self._remaining

    @property
    def total_seconds(self) -> int:
        """返回倒计时总秒数。"""
        return self._seconds

    def render(self) -> str:
        """渲染倒计时为字符串。

        Returns:
            str: 格式化的倒计时字符串，如 "Countdown: 5s"。
        """
        if self._message:
            return f"{self._message}: {self._remaining}s"
        return f"{self._remaining}s"

    async def run(self) -> None:  # pragma: no cover
        """执行倒计时循环。

        从设定的秒数开始，每秒递减一次，直到归零。
        每次递减时调用 on_tick 回调（如果提供）。
        """
        self._remaining = self._seconds

        while self._remaining >= 0:
            if self._on_tick is not None:
                self._on_tick(self._remaining)
            if self._remaining > 0:
                await asyncio.sleep(1)
            self._remaining -= 1
