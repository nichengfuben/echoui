from __future__ import annotations

import asyncio
from typing import Any, Optional

from echoui.components.base_component import BaseComponent


class Spinner(BaseComponent):
    """旋转加载指示器组件。

    通过循环显示不同的帧（frame）来模拟旋转动画效果。
    支持异步上下文管理器协议，可与 async with 语句配合使用。
    """

    DEFAULT_FRAMES: list[str] = ["|", "/", "-", "\\"]

    def __init__(
        self,
        message: str = "Loading",
        frames: Optional[list[str]] = None,
        interval: float = 0.1,
        theme_name: str = "default",
        normal_mode: bool = False,
    ) -> None:
        """初始化旋转加载指示器。

        Args:
            message: 加载提示消息。
            frames: 自定义动画帧列表，默认为 ["|", "/", "-", "\\"]。
            interval: 帧间隔时间（秒）。
            theme_name: 主题名称。
            normal_mode: 是否启用正常模式（无彩色输出）。
        """
        from echoui.core.theme import Theme

        theme = Theme.get(theme_name)
        super().__init__(theme=theme, normal_mode=normal_mode)
        self._theme_name = theme_name
        self._message = message
        self._frames = frames if frames is not None else self.DEFAULT_FRAMES
        self._interval = interval
        self._running = False
        self._current_frame = 0
        self._task: Optional[asyncio.Task[None]] = None

    @property
    def message(self) -> str:
        """返回当前消息文本。"""
        return self._message

    @property
    def is_running(self) -> bool:
        """返回是否正在运行。"""
        return self._running

    def start(self) -> "Spinner":
        """启动旋转动画。

        Returns:
            self: 支持方法链调用。
        """
        self._running = True
        self._current_frame = 0
        return self

    def stop(self) -> "Spinner":
        """停止旋转动画。

        Returns:
            self: 支持方法链调用。
        """
        self._running = False
        return self

    def update_message(self, message: str) -> "Spinner":
        """更新加载提示消息。

        Args:
            message: 新的消息文本。

        Returns:
            self: 支持方法链调用。
        """
        self._message = message
        return self

    def _next_frame(self) -> None:
        """切换到下一帧。"""
        if self._frames:
            self._current_frame = (self._current_frame + 1) % len(self._frames)

    def render(self) -> str:
        """渲染当前帧和消息。

        Returns:
            str: 当前帧字符 + 消息文本，如 "| Loading"。
        """
        if not self._frames:
            return self._message
        frame = self._frames[self._current_frame]
        return f"{frame} {self._message}"

    async def __aenter__(self) -> "Spinner":
        """异步上下文管理器入口。

        Returns:
            self: Spinner 实例。
        """
        self.start()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any],
    ) -> None:
        """异步上下文管理器出口。

        Args:
            exc_type: 异常类型。
            exc_val: 异常值。
            exc_tb: 回溯对象。
        """
        self.stop()
