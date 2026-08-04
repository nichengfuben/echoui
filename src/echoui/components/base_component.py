from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from echoui.core.renderer import GradientRenderer
    from echoui.core.theme import ThemeConfig


class BaseComponent(ABC):
    """组件基类，所有 EchoUI 组件必须继承此类。

    提供渲染器、正常模式、主题和可见性的统一管理。

    Examples:
        >>> class Dummy(BaseComponent):
        ...     def render(self) -> str:
        ...         return "dummy"
        >>> comp = Dummy(normal_mode=True)
        >>> comp.normal_mode
        True
    """

    def __init__(
        self,
        renderer: Optional[GradientRenderer] = None,
        normal_mode: bool = False,
        theme: Optional[ThemeConfig] = None,
    ) -> None:
        """初始化组件基类。

        Args:
            renderer: 渐变渲染器实例，未提供时自动创建默认实例。
            normal_mode: 是否启用正常模式（无彩色输出），
                可通过 ECHOUI_NORMAL_MODE 环境变量覆盖。
            theme: 主题配置，未提供时使用默认主题。
        """
        from echoui.core.renderer import GradientRenderer
        from echoui.core.theme import Theme

        env_value = os.environ.get("ECHOUI_NORMAL_MODE", "").lower()
        if env_value in ("1", "true", "yes"):
            normal_mode = True

        if renderer is None:
            renderer = GradientRenderer(normal_mode=normal_mode)

        if theme is None:
            theme = Theme.get("default")

        self._normal_mode = normal_mode
        self._renderer = renderer
        self._theme = theme
        self._visible = True

    @property
    def normal_mode(self) -> bool:
        """返回当前是否处于正常模式（只读）。"""
        return self._normal_mode

    @property
    def theme(self) -> ThemeConfig:
        """返回当前主题配置（只读）。"""
        return self._theme

    @property
    def is_visible(self) -> bool:
        """返回组件是否可见（只读）。"""
        return self._visible

    def show(self) -> BaseComponent:
        """将组件设为可见。

        Returns:
            BaseComponent: 组件自身，支持链式调用。
        """
        self._visible = True
        return self

    def hide(self) -> BaseComponent:
        """将组件设为不可见。

        Returns:
            BaseComponent: 组件自身，支持链式调用。
        """
        self._visible = False
        return self

    @abstractmethod
    def render(self) -> str:
        """渲染组件内容。

        Returns:
            str: 渲染后的字符串。
        """
        ...

    def __repr__(self) -> str:
        """返回组件的字符串表示。"""
        cls_name = type(self).__name__
        return (
            f"{cls_name}(theme={self._theme.name!r}, "
            f"normal_mode={self._normal_mode})"
        )
