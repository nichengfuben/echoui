from __future__ import annotations

import pytest

from echoui.core.exceptions import ConfigError
from echoui.core.theme import Theme, ThemeConfig


class TestThemeConfig:
    """Tests for ThemeConfig dataclass."""

    def test_theme_config_creation(self) -> None:
        config = ThemeConfig(
            name="test",
            primary_start="#FF0000",
            primary_end="#00FF00",
            border_start="#0000FF",
            border_end="#FFFF00",
            accent_start="#FF00FF",
            accent_end="#00FFFF",
            success="#10B981",
            warning="#F59E0B",
            error="#EF4444",
            info="#3B82F6",
            muted="#6B7280",
            bg_dark="#0F0F1A",
            bg_light="#1A1A2E",
            text_primary="#F9FAFB",
            text_secondary="#D1D5DB",
        )
        assert config.name == "test"
        assert config.primary_start == "#FF0000"

    def test_theme_config_invalid_color_raises(self) -> None:
        with pytest.raises(ConfigError, match="颜色无效"):
            ThemeConfig(
                name="bad",
                primary_start="not-a-color",
                primary_end="#00FF00",
                border_start="#0000FF",
                border_end="#FFFF00",
                accent_start="#FF00FF",
                accent_end="#00FFFF",
                success="#10B981",
                warning="#F59E0B",
                error="#EF4444",
                info="#3B82F6",
                muted="#6B7280",
                bg_dark="#0F0F1A",
                bg_light="#1A1A2E",
                text_primary="#F9FAFB",
                text_secondary="#D1D5DB",
            )

    def test_theme_config_is_frozen(self) -> None:
        config = ThemeConfig(
            name="frozen_test",
            primary_start="#FF0000",
            primary_end="#00FF00",
            border_start="#0000FF",
            border_end="#FFFF00",
            accent_start="#FF00FF",
            accent_end="#00FFFF",
            success="#10B981",
            warning="#F59E0B",
            error="#EF4444",
            info="#3B82F6",
            muted="#6B7280",
            bg_dark="#0F0F1A",
            bg_light="#1A1A2E",
            text_primary="#F9FAFB",
            text_secondary="#D1D5DB",
        )
        with pytest.raises(AttributeError):
            config.name = "modified"


class TestTheme:
    """Tests for Theme registry."""

    def test_theme_get_default_theme(self) -> None:
        config = Theme.get("default")
        assert config.name == "default"
        assert config.primary_start == "#6366F1"
        assert config.primary_end == "#8B5CF6"

    def test_theme_get_ocean_theme(self) -> None:
        config = Theme.get("ocean")
        assert config.name == "ocean"
        assert config.primary_start == "#0EA5E9"
        assert config.primary_end == "#06B6D4"

    def test_theme_get_nonexistent_raises(self) -> None:
        with pytest.raises(ConfigError, match="主题不存在"):
            Theme.get("nonexistent_theme_xyz")

    def test_theme_list_names_has_9(self) -> None:
        names = Theme.list_names()
        assert len(names) == 9

    def test_theme_register_custom(self) -> None:
        custom = ThemeConfig(
            name="custom_test_theme",
            primary_start="#AABBCC",
            primary_end="#DDEEFF",
            border_start="#112233",
            border_end="#445566",
            accent_start="#778899",
            accent_end="#AABBCC",
            success="#10B981",
            warning="#F59E0B",
            error="#EF4444",
            info="#3B82F6",
            muted="#6B7280",
            bg_dark="#0F0F1A",
            bg_light="#1A1A2E",
            text_primary="#F9FAFB",
            text_secondary="#D1D5DB",
        )
        Theme.register(custom)
        retrieved = Theme.get("custom_test_theme")
        assert retrieved.name == "custom_test_theme"
        assert retrieved.primary_start == "#AABBCC"
