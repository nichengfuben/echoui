from __future__ import annotations

from echoui.components.base_component import BaseComponent


class AsciiArtBuilder(BaseComponent):
    """ASCII 艺术构建器组件。

    支持逐行添加文本或通过 ``add_text()`` 自动按换行符拆分。
    最终通过 ``build()`` 或 ``render()`` 输出完整结果。

    Examples:
        >>> builder = AsciiArtBuilder()
        >>> _ = builder.add_line("  ___")
        >>> _ = builder.add_text(" / _ \\\\")
        >>> _ = builder.add_line("| | | |")
        >>> result = builder.build()
        >>> "___" in result
        True
    """

    def __init__(self) -> None:
        """初始化 AsciiArtBuilder 实例。"""
        super().__init__()
        self._lines: list[str] = []

    def add_line(self, line: str) -> AsciiArtBuilder:
        """添加一行文本。

        Args:
            line: 要添加的单行文本。

        Returns:
            AsciiArtBuilder: 自身引用，支持链式调用。
        """
        self._lines.append(line)
        return self

    def add_text(self, text: str) -> AsciiArtBuilder:
        """添加文本，按换行符自动拆分为多行。

        Args:
            text: 要添加的文本，可包含换行符。

        Returns:
            AsciiArtBuilder: 自身引用，支持链式调用。
        """
        for line in text.split("\n"):
            self._lines.append(line)
        return self

    def build(self) -> str:
        """将所有行拼接为完整字符串。

        Returns:
            str: 用换行符连接的所有行。
        """
        return "\n".join(self._lines)

    def render(self) -> str:
        """渲染 ASCII 艺术内容。

        委托给 ``build()`` 方法。

        Returns:
            str: 渲染后的完整字符串。
        """
        return self.build()
