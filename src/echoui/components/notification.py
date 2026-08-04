from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from echoui.components.base_component import BaseComponent

if TYPE_CHECKING:
    from echoui.core.renderer import GradientRenderer
    from echoui.core.theme import ThemeConfig


class Notification(BaseComponent):
    """通知组件，用于显示不同级别的通知消息。

    支持成功、警告、错误和信息四种通知类型，
    在正常模式下使用前缀文本，彩色模式下使用主题色渲染。

    Examples:
        >>> n = Notification(normal_mode=True)
        >>> n.success("操作成功")
        Notification(theme='default', normal_mode=True)
        >>> n.render()
        '[OK] 操作成功'
    """

    def __init__(
        self,
        message: str = "",
        renderer: Optional[GradientRenderer] = None,
        normal_mode: bool = False,
        theme: Optional[ThemeConfig] = None,
    ) -> None:
        """初始化通知组件。

        Args:
            message: 通知消息内容。
            renderer: 渐变渲染器实例。
            normal_mode: 是否启用正常模式。
            theme: 主题配置。
        """
        super().__init__(renderer=renderer, normal_mode=normal_mode, theme=theme)
        self._message = message
        self._prefix = ""

    def success(self, message: str) -> Notification:
        """设置成功级别通知。

        Args:
            message: 通知消息内容。

        Returns:
            Notification: 组件自身，支持链式调用。
        """
        self._prefix = "[OK]"
        self._message = message
        return self

    def warning(self, message: str) -> Notification:
        """设置警告级别通知。

        Args:
            message: 通知消息内容。

        Returns:
            Notification: 组件自身，支持链式调用。
        """
        self._prefix = "[!]"
        self._message = message
        return self

    def error(self, message: str) -> Notification:
        """设置错误级别通知。

        Args:
            message: 通知消息内容。

        Returns:
            Notification: 组件自身，支持链式调用。
        """
        self._prefix = "[X]"
        self._message = message
        return self

    def info(self, message: str) -> Notification:
        """设置信息级别通知。

        Args:
            message: 通知消息内容。

        Returns:
            Notification: 组件自身，支持链式调用。
        """
        self._prefix = "[i]"
        self._message = message
        return self

    def render(self) -> str:
        """渲染通知消息。

        正常模式下返回 "{prefix} {message}" 格式文本。
        彩色模式下使用主题色对前缀进行渐变渲染。

        Returns:
            str: 渲染后的通知字符串。
        """
        if self._normal_mode:
            return f"{self._prefix} {self._message}"

        color_map = {
            "[OK]": self._theme.success,
            "[!]": self._theme.warning,
            "[X]": self._theme.error,
            "[i]": self._theme.info,
        }
        color = color_map.get(self._prefix, self._theme.muted)

        rendered_prefix = self._renderer.render_text_ansi(self._prefix, color, color)
        return f"{rendered_prefix} {self._message}"
