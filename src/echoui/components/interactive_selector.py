from __future__ import annotations

import asyncio
import sys

from echoui.components.base_component import BaseComponent


class InteractiveSelector(BaseComponent):
    """交互式选择器组件。

    显示选项列表供用户选择，``select()`` 方法异步等待用户输入并返回选中项。

    Examples:
        >>> selector = InteractiveSelector(["apple", "banana", "cherry"])
        >>> print(selector.render())
        1. apple
        2. banana
        3. cherry
    """

    def __init__(self, items: list[str] | None = None) -> None:
        """初始化 InteractiveSelector 实例。

        Args:
            items: 可选的选项列表。
        """
        super().__init__()
        self._items: list[str] = items if items is not None else []

    def render(self) -> str:
        """渲染选项列表。

        每行显示序号和选项内容，格式为 ``N. item``。

        Returns:
            str: 渲染后的选项列表字符串。
        """
        if not self._items:
            return ""
        lines = [f"{i + 1}. {item}" for i, item in enumerate(self._items)]
        return "\n".join(lines)

    async def select(self) -> str:  # pragma: no cover
        """异步等待用户选择并返回选中项。

        渲染选项后从标准输入读取序号，返回对应的选项文本。
        输入无效时返回空字符串。

        Returns:
            str: 选中的选项文本，输入无效时返回空字符串。
        """
        sys.stdout.write(self.render() + "\n")
        sys.stdout.write("Enter choice (1-{}): ".format(len(self._items)))
        sys.stdout.flush()

        loop = asyncio.get_running_loop()

        def _read() -> str:
            try:
                return sys.stdin.readline().rstrip("\n")
            except (OSError, EOFError):
                return ""

        user_input = await loop.run_in_executor(None, _read)

        try:
            index = int(user_input) - 1
            if 0 <= index < len(self._items):
                return self._items[index]
        except (ValueError, TypeError):
            return ""

        return ""
