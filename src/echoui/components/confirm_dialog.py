from __future__ import annotations

import asyncio
import sys

from echoui.components.base_component import BaseComponent


class ConfirmDialog(BaseComponent):
    """确认对话框组件。

    向用户显示确认提示，``confirm()`` 方法异步等待 y/n 输入并返回布尔结果。

    Examples:
        >>> dialog = ConfirmDialog("Delete all files?")
        >>> print(dialog.render())
        Delete all files? [y/n]:
    """

    def __init__(self, message: str = "") -> None:
        """初始化 ConfirmDialog 实例。

        Args:
            message: 确认提示消息。
        """
        super().__init__()
        self._message: str = message

    def render(self) -> str:
        """渲染确认提示。

        Returns:
            str: 带 [y/n] 后缀的提示字符串。
        """
        if self._message:
            return f"{self._message} [y/n]:"
        return "[y/n]:"

    async def confirm(self) -> bool:  # pragma: no cover
        """异步等待用户确认输入。

        渲染提示后从标准输入读取响应，``y`` 或 ``Y`` 返回 ``True``，
        其他输入返回 ``False``。

        Returns:
            bool: 用户是否确认。
        """
        sys.stdout.write(self.render() + " ")
        sys.stdout.flush()

        loop = asyncio.get_running_loop()

        def _read() -> str:
            try:
                return sys.stdin.readline().rstrip("\n").strip().lower()
            except (OSError, EOFError):
                return "n"

        response = await loop.run_in_executor(None, _read)
        return response in ("y", "yes")
