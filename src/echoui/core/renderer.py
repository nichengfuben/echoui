from __future__ import annotations

from echoui.utils.color import hex_to_rgb
from echoui.utils.text import get_display_width as _get_display_width


class GradientRenderer:
    """渐变文本渲染器。

    支持 ANSI 24 位彩色渐变输出，兼容正常模式（无彩色）和彩色模式。
    """

    def __init__(self, normal_mode: bool = False) -> None:
        """初始化渲染器。

        Args:
            normal_mode: 是否启用正常模式（无彩色输出）。
        """
        self._normal_mode = normal_mode

    @property
    def normal_mode(self) -> bool:
        """返回当前是否处于正常模式。"""
        return self._normal_mode

    def render_text_ansi(self, text: str, start_color: str, end_color: str) -> str:
        """对文本应用逐字符的 ANSI 24 位彩色渐变。

        在 normal_mode 下直接返回原文本。彩色模式下，每个字符根据其
        在文本中的显示宽度位置计算渐变比例，生成对应的 24 位 ANSI 转义色。

        Args:
            text: 要渲染的文本。
            start_color: 起始颜色（#RRGGBB 格式）。
            end_color: 结束颜色（#RRGGBB 格式）。

        Returns:
            str: 带 ANSI 彩色转义码的文本，或正常模式下的原文本。

        Examples:
            >>> renderer = GradientRenderer(normal_mode=True)
            >>> renderer.render_text_ansi("Hello", "#FF0000", "#0000FF")
            'Hello'
        """
        if self._normal_mode:
            return text

        total_width = _get_display_width(text)
        if total_width == 0:
            return text

        sr, sg, sb = hex_to_rgb(start_color)
        er, eg, eb = hex_to_rgb(end_color)
        reset = "\x1b[0m"
        parts: list[str] = []
        gradient_index = 0

        for char in text:
            char_width = _get_display_width(char)
            if char_width <= 0:
                char_width = 1
            t = gradient_index / total_width
            r = int(sr + (er - sr) * t)
            g = int(sg + (eg - sg) * t)
            b = int(sb + (eb - sb) * t)
            parts.append(f"\x1b[38;2;{r};{g};{b}m{char}")
            gradient_index += char_width

        parts.append(reset)
        return "".join(parts)

    def render_progress_bar(self, current: int, total: int, width: int = 20) -> str:
        """渲染进度条字符串。

        根据 current/total 计算百分比，生成固定宽度的进度条。
        正常模式下使用 ASCII 字符，彩色模式下使用方块字符。

        Args:
            current: 当前进度值。
            total: 总进度值。
            width: 进度条显示宽度。

        Returns:
            str: 形如 "[========------] 40%" 的进度条字符串。

        Raises:
            ConfigError: 当 current < 0 或 current > total 时抛出。

        Examples:
            >>> GradientRenderer(True).render_progress_bar(4, 10, 10)
            '[====------] 40%'
        """
        from echoui.core.exceptions import ConfigError

        if current < 0 or current > total:
            raise ConfigError(f"进度值无效: current={current}, total={total}")

        ratio = 0.0 if total == 0 else current / total
        filled = int(round(ratio * width))
        empty = width - filled
        percent = int(round(ratio * 100))

        if self._normal_mode:
            bar = "=" * filled + "-" * empty
        else:
            bar = "\u2588" * filled + "\u2591" * empty

        return f"[{bar}] {percent}%"

    @staticmethod
    def get_display_width(text: str) -> int:
        """计算字符串的显示宽度（委托给 utils.text.get_display_width）。

        Args:
            text: 待计算宽度的字符串。

        Returns:
            int: 字符串的显示宽度。

        Examples:
            >>> GradientRenderer.get_display_width("Hello")
            5
            >>> GradientRenderer.get_display_width("你好")
            4
        """
        return _get_display_width(text)
