from __future__ import annotations

from typing import TextIO

from echoui.components.base_component import BaseComponent


class StreamWriter(BaseComponent):
    """流式文本写入组件。

    维护一个内部文本缓冲区，支持链式写入文本和单个字符。
    通过 ``reset()`` 可清空缓冲区。

    Examples:
        >>> sw = StreamWriter()
        >>> _ = sw.write_text("Hello").write_char("!")
        >>> sw.render()
        'Hello!'
    """

    def __init__(self, stream: TextIO | None = None) -> None:
        """初始化 StreamWriter 实例。

        Args:
            stream: 可选的输出流，用于写入操作。
        """
        super().__init__()
        self._buffer: list[str] = []
        if stream is not None:
            self._output = stream

    def write_text(self, text: str) -> StreamWriter:
        """将文本追加到缓冲区。

        Args:
            text: 要写入的文本。

        Returns:
            StreamWriter: 自身引用，支持链式调用。
        """
        self._buffer.append(text)
        return self

    def write_char(self, char: str) -> StreamWriter:
        """将单个字符追加到缓冲区。

        Args:
            char: 要写入的字符。

        Returns:
            StreamWriter: 自身引用，支持链式调用。
        """
        self._buffer.append(char)
        return self

    def reset(self) -> StreamWriter:
        """清空内部缓冲区。

        Returns:
            StreamWriter: 自身引用，支持链式调用。
        """
        self._buffer.clear()
        return self

    def render(self) -> str:
        """返回缓冲区的全部内容。

        Returns:
            str: 缓冲区中累积的文本。
        """
        return "".join(self._buffer)
