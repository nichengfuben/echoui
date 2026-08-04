from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from echoui.core.exceptions import ConfigError
from echoui.utils.validators import validate_hex_color


@dataclass(frozen=True)
class ThemeConfig:
    """主题配置值对象（不可变）。

    包含主题所需的全部颜色令牌，所有颜色均为 #RRGGBB 格式。

    Attributes:
        name: 主题唯一标识符。
        primary_start: 主色渐变起始色。
        primary_end: 主色渐变结束色。
        border_start: 边框渐变起始色。
        border_end: 边框渐变结束色。
        accent_start: 强调色渐变起始色。
        accent_end: 强调色渐变结束色。
        success: 成功状态色。
        warning: 警告状态色。
        error: 错误状态色。
        info: 信息状态色。
        muted: 静音/辅助色。
        bg_dark: 深色背景色。
        bg_light: 浅色背景色。
        text_primary: 主文字色。
        text_secondary: 辅助文字色。
    """

    name: str
    primary_start: str
    primary_end: str
    border_start: str
    border_end: str
    accent_start: str
    accent_end: str
    success: str
    warning: str
    error: str
    info: str
    muted: str
    bg_dark: str
    bg_light: str
    text_primary: str
    text_secondary: str

    def __post_init__(self) -> None:
        """验证所有颜色字段格式。"""
        color_fields = [
            "primary_start",
            "primary_end",
            "border_start",
            "border_end",
            "accent_start",
            "accent_end",
            "success",
            "warning",
            "error",
            "info",
            "muted",
            "bg_dark",
            "bg_light",
            "text_primary",
            "text_secondary",
        ]
        for field_name in color_fields:
            value = getattr(self, field_name)
            try:
                validate_hex_color(value)
            except ConfigError as exc:
                raise ConfigError(
                    f"主题 {self.name!r} 的字段 {field_name!r} 颜色无效: {exc}"
                ) from exc


class Theme:
    """主题注册表（类方法工厂，无需实例化）。

    内置 9 种主题，支持自定义主题注册。

    Examples:
        >>> config = Theme.get("ocean")
        >>> config.name
        'ocean'
        >>> try:
        ...     Theme.get("nonexistent")
        ... except ConfigError as e:
        ...     "不存在" in str(e)
        True
    """

    _registry: ClassVar[dict[str, ThemeConfig]] = {}
    _initialized: ClassVar[bool] = False

    @classmethod
    def _ensure_initialized(cls) -> None:
        """懒加载内置主题，避免模块导入时的副作用。"""
        if not cls._initialized:
            cls._register_builtin_themes()
            cls._initialized = True

    @classmethod
    def get(cls, name: str) -> ThemeConfig:
        """获取指定名称的主题配置。

        Args:
            name: 主题名称。

        Returns:
            ThemeConfig: 主题配置对象。

        Raises:
            ConfigError: 当主题名称不存在时抛出。
        """
        cls._ensure_initialized()
        if name not in cls._registry:
            available = sorted(cls._registry.keys())
            raise ConfigError(f"主题不存在: {name!r}，可用主题: {available}")
        return cls._registry[name]

    @classmethod
    def register(cls, config: ThemeConfig) -> None:
        """注册自定义主题。

        Args:
            config: 完整的主题配置对象。

        Raises:
            ConfigError: 当主题名称已存在（内置主题）时抛出。
        """
        cls._ensure_initialized()
        cls._registry[config.name] = config

    @classmethod
    def list_names(cls) -> list[str]:
        """返回所有可用主题名称（已排序）。"""
        cls._ensure_initialized()
        return sorted(cls._registry.keys())

    @classmethod
    def _register_builtin_themes(cls) -> None:
        """注册 9 种内置主题。"""
        builtin_themes: list[ThemeConfig] = [
            ThemeConfig(
                name="default",
                primary_start="#6366F1",
                primary_end="#8B5CF6",
                border_start="#6366F1",
                border_end="#8B5CF6",
                accent_start="#F59E0B",
                accent_end="#EF4444",
                success="#10B981",
                warning="#F59E0B",
                error="#EF4444",
                info="#3B82F6",
                muted="#6B7280",
                bg_dark="#0F0F1A",
                bg_light="#1A1A2E",
                text_primary="#F9FAFB",
                text_secondary="#D1D5DB",
            ),
            ThemeConfig(
                name="ocean",
                primary_start="#0EA5E9",
                primary_end="#06B6D4",
                border_start="#0EA5E9",
                border_end="#06B6D4",
                accent_start="#F0ABFC",
                accent_end="#C084FC",
                success="#34D399",
                warning="#FBBF24",
                error="#F87171",
                info="#60A5FA",
                muted="#64748B",
                bg_dark="#0C1A2E",
                bg_light="#0F2744",
                text_primary="#F0F9FF",
                text_secondary="#BAE6FD",
            ),
            ThemeConfig(
                name="sunset",
                primary_start="#F97316",
                primary_end="#EF4444",
                border_start="#F97316",
                border_end="#EF4444",
                accent_start="#FBBF24",
                accent_end="#F97316",
                success="#4ADE80",
                warning="#FCD34D",
                error="#F87171",
                info="#38BDF8",
                muted="#78716C",
                bg_dark="#1A0A00",
                bg_light="#2D1500",
                text_primary="#FFF7ED",
                text_secondary="#FED7AA",
            ),
            ThemeConfig(
                name="forest",
                primary_start="#22C55E",
                primary_end="#16A34A",
                border_start="#22C55E",
                border_end="#16A34A",
                accent_start="#84CC16",
                accent_end="#22C55E",
                success="#4ADE80",
                warning="#FDE047",
                error="#F87171",
                info="#38BDF8",
                muted="#6B7280",
                bg_dark="#031A0A",
                bg_light="#052E16",
                text_primary="#F0FDF4",
                text_secondary="#BBF7D0",
            ),
            ThemeConfig(
                name="purple",
                primary_start="#A855F7",
                primary_end="#7C3AED",
                border_start="#A855F7",
                border_end="#7C3AED",
                accent_start="#EC4899",
                accent_end="#A855F7",
                success="#4ADE80",
                warning="#FBBF24",
                error="#F87171",
                info="#60A5FA",
                muted="#7C3AED",
                bg_dark="#0E0520",
                bg_light="#1A0933",
                text_primary="#FAF5FF",
                text_secondary="#E9D5FF",
            ),
            ThemeConfig(
                name="neon",
                primary_start="#00FF41",
                primary_end="#00D4FF",
                border_start="#00FF41",
                border_end="#00D4FF",
                accent_start="#FF0080",
                accent_end="#FF6600",
                success="#00FF41",
                warning="#FFD700",
                error="#FF0040",
                info="#00D4FF",
                muted="#404040",
                bg_dark="#000000",
                bg_light="#0A0A0A",
                text_primary="#00FF41",
                text_secondary="#00D4FF",
            ),
            ThemeConfig(
                name="monochrome",
                primary_start="#FFFFFF",
                primary_end="#AAAAAA",
                border_start="#FFFFFF",
                border_end="#888888",
                accent_start="#FFFFFF",
                accent_end="#CCCCCC",
                success="#FFFFFF",
                warning="#AAAAAA",
                error="#888888",
                info="#CCCCCC",
                muted="#555555",
                bg_dark="#000000",
                bg_light="#111111",
                text_primary="#FFFFFF",
                text_secondary="#AAAAAA",
            ),
            ThemeConfig(
                name="ruby",
                primary_start="#E11D48",
                primary_end="#BE123C",
                border_start="#FB7185",
                border_end="#E11D48",
                accent_start="#F43F5E",
                accent_end="#E11D48",
                success="#4ADE80",
                warning="#FBBF24",
                error="#F87171",
                info="#38BDF8",
                muted="#9F1239",
                bg_dark="#1A0008",
                bg_light="#2D0012",
                text_primary="#FFF1F2",
                text_secondary="#FECDD3",
            ),
            ThemeConfig(
                name="aurora",
                primary_start="#34D399",
                primary_end="#60A5FA",
                border_start="#34D399",
                border_end="#A78BFA",
                accent_start="#F472B6",
                accent_end="#60A5FA",
                success="#34D399",
                warning="#FCD34D",
                error="#F87171",
                info="#60A5FA",
                muted="#475569",
                bg_dark="#020617",
                bg_light="#0F172A",
                text_primary="#F8FAFC",
                text_secondary="#CBD5E1",
            ),
        ]
        for theme in builtin_themes:
            cls._registry[theme.name] = theme
