from __future__ import annotations

import asyncio
import logging
from typing import Awaitable, Callable, Optional

logger = logging.getLogger(__name__)


class Animator:
    """动画帧调度器。

    管理逐帧渲染的动画序列，支持异步帧循环、
    帧率控制和完成回调。

    Examples:
        >>> animator = Animator()
        >>> animator.frame_count
        0
    """

    def __init__(self, fps: int = 30) -> None:
        """初始化动画调度器。

        Args:
            fps: 每秒帧数，默认 30。
        """
        self._fps: int = fps
        self._frames: list[Callable[[], str]] = []
        self._running: bool = False
        self._on_complete: Optional[Callable[[], None]] = None

    @property
    def fps(self) -> int:
        """每秒帧数。"""
        return self._fps

    @property
    def frame_count(self) -> int:
        """已注册帧数量。"""
        return len(self._frames)

    @property
    def is_running(self) -> bool:
        """动画是否正在运行。"""
        return self._running

    def add_frame(self, renderer: Callable[[], str]) -> int:
        """添加动画帧。

        Args:
            renderer: 无参函数，返回当前帧的字符串表示。

        Returns:
            帧的索引位置。
        """
        index = len(self._frames)
        self._frames.append(renderer)
        return index

    def remove_frame(self, index: int) -> None:
        """移除指定索引的帧。

        Args:
            index: 帧的索引。

        Raises:
            IndexError: 当索引越界时抛出。
        """
        if index < 0 or index >= len(self._frames):
            raise IndexError(f"帧索引 {index} 越界")
        self._frames.pop(index)

    def set_on_complete(self, callback: Callable[[], None]) -> None:
        """设置动画完成回调。

        Args:
            callback: 动画完成时调用的无参函数。
        """
        self._on_complete = callback

    async def run(
        self,
        cycles: int = 1,
        render_fn: Optional[Callable[[str], Awaitable[None]]] = None,
    ) -> None:
        """运行动画循环。

        Args:
            cycles: 循环次数，0 表示无限循环。
            render_fn: 可选的异步渲染函数，接收帧字符串并输出。

        Raises:
            ValueError: 当没有注册帧时抛出。
        """
        if not self._frames:
            raise ValueError("没有注册的帧")

        self._running = True
        frame_interval = 1.0 / self._fps
        cycle_count = 0

        try:
            while self._running:
                if 0 < cycles <= cycle_count:
                    break

                for frame_fn in self._frames:
                    if self._running:
                        frame_output = frame_fn()
                        if render_fn is not None:
                            await render_fn(frame_output)
                        await asyncio.sleep(frame_interval)

                cycle_count += 1
        finally:
            self._running = False
            if self._on_complete is not None:
                self._on_complete()
            logger.debug("动画完成，共运行 %d 个循环", cycle_count)

    def stop(self) -> None:
        """停止动画循环。"""
        self._running = False

    def clear(self) -> None:
        """清空所有帧。"""
        self._frames.clear()
        self._running = False
