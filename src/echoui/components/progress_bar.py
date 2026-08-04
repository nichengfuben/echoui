from __future__ import annotations

from echoui.components.base_component import BaseComponent
from echoui.core.renderer import GradientRenderer


class ProgressBar(BaseComponent):
    """进度条组件，支持 ASCII 和渐变色两种渲染模式。

    显示当前进度占总进度的百分比，支持链式 API 修改进度值。
    """

    def __init__(
        self,
        current: int = 0,
        total: int = 100,
        width: int = 20,
        message: str = "",
        theme_name: str = "default",
        normal_mode: bool = False,
    ) -> None:
        """初始化进度条组件。

        Args:
            current: 当前进度值。
            total: 总进度值。
            width: 进度条显示宽度（字符数）。
            message: 进度条前方的提示消息。
            theme_name: 主题名称。
            normal_mode: 是否启用正常模式（无彩色输出）。
        """
        from echoui.core.theme import Theme

        theme = Theme.get(theme_name)
        super().__init__(theme=theme, normal_mode=normal_mode)
        self._theme_name = theme_name
        self._current = current
        self._total = total
        self._width = width
        self._message = message

    @property
    def current(self) -> int:
        """返回当前进度值。"""
        return self._current

    @property
    def total(self) -> int:
        """返回总进度值。"""
        return self._total

    @property
    def percentage(self) -> float:
        """返回当前进度百分比（0.0-1.0）。"""
        if self._total == 0:
            return 0.0
        return self._current / self._total

    def advance(self, amount: int = 1) -> "ProgressBar":
        """推进指定数量的进度。

        Args:
            amount: 推进量，默认为 1。

        Returns:
            self: 支持方法链调用。
        """
        self._current = min(self._current + amount, self._total)
        return self

    def set_progress(self, current: int) -> "ProgressBar":
        """直接设置当前进度值。

        Args:
            current: 新的进度值。

        Returns:
            self: 支持方法链调用。
        """
        self._current = max(0, min(current, self._total))
        return self

    def finish(self) -> "ProgressBar":
        """将进度设置为完成状态（current = total）。

        Returns:
            self: 支持方法链调用。
        """
        self._current = self._total
        return self

    def render(self) -> str:
        """渲染进度条为字符串。

        在正常模式下使用 ASCII 字符渲染进度条。
        在彩色模式下使用 GradientRenderer 渲染。

        Returns:
            str: 格式化的进度条字符串。
        """
        if self._normal_mode:
            return self._render_normal()
        return self._render_gradient()

    def _render_normal(self) -> str:
        """使用 ASCII 字符渲染进度条。

        Returns:
            str: ASCII 进度条，形如 "[======------] 60%"。
        """
        renderer = GradientRenderer(normal_mode=True)
        bar = renderer.render_progress_bar(
            current=self._current,
            total=self._total,
            width=self._width,
        )
        if self._message:
            return f"{self._message} {bar}"
        return bar

    def _render_gradient(self) -> str:
        """使用主题颜色渲染渐变进度条。

        Returns:
            str: 带 ANSI 彩色转义的进度条字符串。
        """
        renderer = GradientRenderer(normal_mode=False)
        bar = renderer.render_progress_bar(
            current=self._current,
            total=self._total,
            width=self._width,
        )
        prefix = self._message + " " if self._message else ""
        return prefix + bar
