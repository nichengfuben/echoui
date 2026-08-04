from __future__ import annotations

import sys

from echoui.components.base_component import BaseComponent


class Pager(BaseComponent):
    """分页显示组件。

    将内容按页分割显示，``display()`` 方法逐页输出内容，
    ``render()`` 方法直接返回完整内容。

    Examples:
        >>> pager = Pager("line1\\nline2\\nline3")
        >>> pager.render()
        'line1\\nline2\\nline3'
    """

    DEFAULT_PAGE_SIZE = 20

    def __init__(self, content: str = "", page_size: int = DEFAULT_PAGE_SIZE) -> None:
        """初始化 Pager 实例。

        Args:
            content: 要分页显示的完整内容。
            page_size: 每页显示的行数。
        """
        super().__init__()
        self._content: str = content
        self._page_size: int = page_size

    def display(self) -> None:  # pragma: no cover
        """分页显示内容。

        将内容按行数分页，每页显示后暂停等待用户输入。
        """
        lines = self._content.split("\n")
        total_pages = (len(lines) + self._page_size - 1) // self._page_size

        for page_num in range(total_pages):
            start = page_num * self._page_size
            end = start + self._page_size
            page_lines = lines[start:end]

            for line in page_lines:
                sys.stdout.write(line + "\n")

            if page_num < total_pages - 1:
                prompt = (
                    f"-- Page {page_num + 1}/{total_pages} "
                    "(Press Enter to continue) -- "
                )
                sys.stdout.write(prompt)
                sys.stdout.flush()
                try:
                    sys.stdin.readline()
                except (OSError, EOFError):
                    break

    def render(self) -> str:
        """返回完整内容字符串。

        Returns:
            str: 完整的分页内容。
        """
        return self._content
