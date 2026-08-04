from __future__ import annotations

from echoui.components.base_component import BaseComponent


class PanelBuilder(BaseComponent):
    """面板构建器组件。

    支持链式设置标题和内容，渲染时生成带标题栏和内容区域的边框面板。

    Examples:
        >>> panel = PanelBuilder()
        >>> result = panel.title("Info").content("Hello World").render()
        >>> "Info" in result and "Hello World" in result
        True
    """

    def __init__(
        self,
        title: str = "",
        content: str = "",
        border_style: str = "default",
    ) -> None:
        """初始化 PanelBuilder 实例。

        Args:
            title: 面板标题。
            content: 面板内容。
            border_style: 边框样式标识。
        """
        super().__init__()
        self._title: str = title
        self._content: str = content
        self._border_style: str = border_style

    def title(self, text: str) -> PanelBuilder:
        """设置面板标题。

        Args:
            text: 标题文本。

        Returns:
            PanelBuilder: 自身引用，支持链式调用。
        """
        self._title = text
        return self

    def content(self, text: str) -> PanelBuilder:
        """设置面板内容。

        Args:
            text: 内容文本。

        Returns:
            PanelBuilder: 自身引用，支持链式调用。
        """
        self._content = text
        return self

    def render(self) -> str:
        """渲染带标题栏和内容区域的面板。

        根据标题和内容中最宽的行计算面板宽度，
        使用 ``+``, ``-``, ``|`` 字符绘制边框。

        Returns:
            str: 渲染后的面板字符串。
        """
        content_lines = self._content.split("\n") if self._content else [""]
        border_chars = self._get_border_chars()

        all_display_lines = [self._title] + content_lines
        max_width = (
            max(len(line) for line in all_display_lines) if all_display_lines else 0
        )
        panel_width = max_width + 2

        border_line = (
            border_chars["corner"]
            + border_chars["h"] * panel_width
            + border_chars["corner"]
        )
        lines: list[str] = [border_line]

        if self._title:
            title_line = self._format_inner(self._title, panel_width)
            lines.append(border_chars["v"] + title_line + border_chars["v"])
            lines.append(border_line)

        for content_line in content_lines:
            inner = self._format_inner(content_line, panel_width)
            lines.append(border_chars["v"] + inner + border_chars["v"])

        lines.append(border_line)
        return "\n".join(lines)

    def _get_border_chars(self) -> dict[str, str]:
        """根据模式和边框样式获取边框字符。

        Returns:
            dict[str, str]: 包含 corner, h, v 键的边框字符字典。
        """
        if self._normal_mode:
            return {"corner": "+", "h": "-", "v": "|"}
        return {"corner": "\u250c", "h": "\u2500", "v": "\u2502"}

    def _format_inner(self, text: str, panel_width: int) -> str:
        """格式化面板内部行文本。

        Args:
            text: 原始文本。
            panel_width: 面板内部宽度。

        Returns:
            str: 填充空格后的格式化文本。
        """
        padding = panel_width - len(text)
        return " " + text + " " * padding
