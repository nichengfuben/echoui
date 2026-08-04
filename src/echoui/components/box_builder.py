from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from echoui.components.base_component import BaseComponent
from echoui.utils.text import get_display_width

if TYPE_CHECKING:
    from echoui.core.renderer import GradientRenderer
    from echoui.core.theme import ThemeConfig


class BoxBuilder(BaseComponent):
    """文本框构建组件，用于在内容周围绘制边框。

    支持四种边框样式：rounded（圆角）、square（方角）、
    double（双线）和 ascii（ASCII 兼容）。

    Examples:
        >>> box = BoxBuilder(normal_mode=True)
        >>> _ = box.content("Hello").title("标题").border_style("ascii")
        >>> result = box.build()
        >>> "Hello" in result
        True
    """

    _BORDER_CHARS: dict[str, dict[str, str]] = {
        "ascii": {
            "tl": "+",
            "tr": "+",
            "bl": "+",
            "br": "+",
            "h": "-",
            "v": "|",
        },
        "square": {
            "tl": "\u250c",
            "tr": "\u2510",
            "bl": "\u2514",
            "br": "\u2518",
            "h": "\u2500",
            "v": "\u2502",
        },
        "rounded": {
            "tl": "\u256d",
            "tr": "\u256e",
            "bl": "\u2570",
            "br": "\u256f",
            "h": "\u2500",
            "v": "\u2502",
        },
        "double": {
            "tl": "\u2554",
            "tr": "\u2557",
            "bl": "\u255a",
            "br": "\u255d",
            "h": "\u2550",
            "v": "\u2551",
        },
    }

    def __init__(
        self,
        content: str = "",
        title: str = "",
        border_style: str = "rounded",
        renderer: Optional[GradientRenderer] = None,
        normal_mode: bool = False,
        theme: Optional[ThemeConfig] = None,
    ) -> None:
        """初始化文本框构建组件。

        Args:
            content: 框内文本内容。
            title: 框顶部标题。
            border_style: 边框样式，支持 rounded/square/double/ascii。
            renderer: 渐变渲染器实例。
            normal_mode: 是否启用正常模式。
            theme: 主题配置。
        """
        super().__init__(renderer=renderer, normal_mode=normal_mode, theme=theme)
        self._content = content
        self._title = title
        self._border_style = border_style

    def content(self, text: str) -> BoxBuilder:
        """设置框内文本内容。

        Args:
            text: 框内文本。

        Returns:
            BoxBuilder: 组件自身，支持链式调用。
        """
        self._content = text
        return self

    def title(self, text: str) -> BoxBuilder:
        """设置框顶部标题。

        Args:
            text: 标题文本。

        Returns:
            BoxBuilder: 组件自身，支持链式调用。
        """
        self._title = text
        return self

    def border_style(self, style: str) -> BoxBuilder:
        """设置边框样式。

        Args:
            style: 边框样式，支持 rounded/square/double/ascii。

        Returns:
            BoxBuilder: 组件自身，支持链式调用。
        """
        self._border_style = style
        return self

    def build(self) -> str:
        """构建带边框的文本框。

        正常模式或 ascii 样式时使用 ASCII 字符，
        其他样式使用 Unicode 制表符。

        Returns:
            str: 带边框的完整文本字符串。
        """
        use_ascii = self._normal_mode or self._border_style == "ascii"
        style_key = "ascii" if use_ascii else self._border_style
        chars = self._BORDER_CHARS.get(style_key, self._BORDER_CHARS["ascii"])

        lines = self._content.split("\n") if self._content else [""]
        max_width = max(get_display_width(line) for line in lines)

        if self._title:
            title_width = get_display_width(self._title)
            if title_width > max_width:
                max_width = title_width

        padding = 2
        inner_width = max_width + padding * 2
        h_border = chars["h"] * inner_width
        v = chars["v"]
        pad_str = " " * padding

        top_line = chars["tl"] + h_border + chars["tr"]
        bottom_line = chars["bl"] + h_border + chars["br"]

        if self._title:
            title_pad_right = inner_width - get_display_width(self._title) - 1
            title_line = v + " " + self._title + " " * title_pad_right + v
        else:
            title_line = None

        result_lines = [top_line]
        if title_line is not None:
            result_lines.append(title_line)

        for line in lines:
            line_width = get_display_width(line)
            right_pad = max_width - line_width + padding
            result_lines.append(f"{v}{pad_str}{line}{' ' * right_pad}{v}")

        result_lines.append(bottom_line)
        return "\n".join(result_lines)

    def render(self) -> str:
        """渲染文本框。

        Returns:
            str: 委托给 build() 方法生成的文本框字符串。
        """
        return self.build()
