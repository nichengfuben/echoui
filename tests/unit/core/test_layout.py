from __future__ import annotations

import pytest

from echoui.core.exceptions import ConfigError
from echoui.core.layout import (
    BREAKPOINT_CONFIGS,
    Breakpoint,
    resolve_breakpoint,
)


class TestBreakpoint:
    """Tests for Breakpoint enum."""

    def test_breakpoint_enum_has_14(self) -> None:
        assert len(Breakpoint) == 14

    def test_breakpoint_members_exist(self) -> None:
        expected = [
            "XS3",
            "XS2",
            "XS",
            "SM",
            "MD",
            "LG",
            "XL",
            "XL2",
            "XL3",
            "XL4",
            "XL5",
            "XL6",
            "XL7",
            "XL8",
        ]
        for member in expected:
            assert hasattr(Breakpoint, member)


class TestBreakpointConfig:
    """Tests for BreakpointConfig dataclass."""

    def test_breakpoint_config_has_required_fields(self) -> None:
        config = BREAKPOINT_CONFIGS[0]
        required_fields = [
            "name",
            "min_width",
            "max_width",
            "layout_mode",
            "sidebar_behavior",
            "sidebar_width",
            "content_density",
            "bg_shape_max",
            "bg_echo_max",
        ]
        for field in required_fields:
            assert hasattr(config, field)


class TestResolveBreakpoint:
    """Tests for resolve_breakpoint function."""

    def test_resolve_sm_breakpoint(self) -> None:
        config = resolve_breakpoint(320)
        assert config.name == Breakpoint.SM
        assert config.min_width == 320

    def test_resolve_xl_breakpoint(self) -> None:
        config = resolve_breakpoint(768)
        assert config.name == Breakpoint.XL
        assert config.min_width == 768

    def test_resolve_xl2_breakpoint(self) -> None:
        config = resolve_breakpoint(1024)
        assert config.name == Breakpoint.XL2
        assert config.min_width == 1024

    def test_resolve_negative_raises_config_error(self) -> None:
        with pytest.raises(ConfigError, match="视口宽度不能为负数"):
            resolve_breakpoint(-1)

    @pytest.mark.parametrize(
        "width,expected",
        [
            (100, Breakpoint.XS3),
            (200, Breakpoint.XS2),
            (280, Breakpoint.XS),
            (400, Breakpoint.SM),
            (500, Breakpoint.MD),
            (700, Breakpoint.LG),
            (900, Breakpoint.XL),
            (1200, Breakpoint.XL2),
            (1400, Breakpoint.XL3),
            (1700, Breakpoint.XL4),
            (2000, Breakpoint.XL5),
            (3000, Breakpoint.XL6),
            (4000, Breakpoint.XL7),
            (6000, Breakpoint.XL8),
        ],
    )
    def test_resolve_all_breakpoints(self, width: int, expected: Breakpoint) -> None:
        config = resolve_breakpoint(width)
        assert config.name == expected
