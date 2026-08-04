from __future__ import annotations

import asyncio
import sys

from echoui.components.base_component import BaseComponent


class MultiLineInput(BaseComponent):
    """多行输入组件。

    ``read()`` 方法异步读取多行输入，直到遇到空行为止。
    ``render()`` 方法返回空字符串，因为该组件主要用于输入交互。

    Examples:
        >>> mli = MultiLineInput()
        >>> mli.render()
        ''
    """

    def __init__(self) -> None:
        """初始化 MultiLineInput 实例。"""
        super().__init__()

    async def read(self, prompt: str = "") -> str:  # pragma: no cover
        """异步读取多行输入，直到遇到空行为止。

        Args:
            prompt: 可选的初始提示文本。

        Returns:
            str: 用户输入的多行文本（不含末尾空行）。
        """
        if prompt:
            sys.stdout.write(prompt + "\n")
            sys.stdout.flush()

        loop = asyncio.get_running_loop()
        lines: list[str] = []

        while True:

            def _read() -> str:
                try:
                    return sys.stdin.readline().rstrip("\n")
                except (OSError, EOFError):
                    return ""

            line = await loop.run_in_executor(None, _read)
            if line == "":
                break
            lines.append(line)

        return "\n".join(lines)

    def render(self) -> str:
        """渲染方法。

        此组件主要用于输入交互，渲染返回空字符串。

        Returns:
            str: 空字符串。
        """
        return ""
