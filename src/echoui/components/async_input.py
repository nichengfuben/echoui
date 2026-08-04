from __future__ import annotations

import asyncio
import sys
from typing import TextIO

from echoui.components.base_component import BaseComponent


class AsyncInput(BaseComponent):
    """异步输入组件。

    通过 asyncio 从标准输入异步读取单行文本。
    ``render()`` 方法返回空字符串，因为该组件主要用于输入交互。

    Examples:
        >>> ai = AsyncInput()
        >>> ai.render()
        ''
    """

    def __init__(self, stream: TextIO | None = None) -> None:
        """初始化 AsyncInput 实例。

        Args:
            stream: 可选的输入流，默认为标准输入。
        """
        super().__init__()
        self._stream: TextIO = stream if stream is not None else sys.stdin

    async def readline(self, prompt: str = "") -> str:  # pragma: no cover
        """异步读取一行输入。

        使用 asyncio 的事件循环从 stdin 读取单行文本。

        Args:
            prompt: 可选的提示文本。

        Returns:
            str: 用户输入的文本（不含末尾换行符）。
        """
        loop = asyncio.get_running_loop()
        if prompt:
            sys.stdout.write(prompt)
            sys.stdout.flush()

        def _read() -> str:
            return self._stream.readline().rstrip("\n")

        return await loop.run_in_executor(None, _read)

    def render(self) -> str:
        """渲染方法。

        此组件主要用于输入交互，渲染返回空字符串。

        Returns:
            str: 空字符串。
        """
        return ""
