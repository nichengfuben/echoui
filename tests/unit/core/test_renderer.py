from __future__ import annotations

import pytest

from echoui.core.exceptions import ConfigError
from echoui.core.renderer import GradientRenderer


class TestGradientRenderer:
    """Tests for GradientRenderer class."""

    def test_default_normal_mode_is_false(self) -> None:
        renderer = GradientRenderer()
        assert renderer.normal_mode is False

    def test_normal_mode_true_sets_correctly(self) -> None:
        renderer = GradientRenderer(normal_mode=True)
        assert renderer.normal_mode is True

    def test_normal_mode_returns_plain_text(self) -> None:
        renderer = GradientRenderer(normal_mode=True)
        result = renderer.render_text_ansi("Hello World", "#FF0000", "#0000FF")
        assert "\x1b[" not in result
        assert result == "Hello World"

    def test_gradient_mode_contains_ansi_sequences(self) -> None:
        renderer = GradientRenderer(normal_mode=False)
        result = renderer.render_text_ansi("Hello", "#FF0000", "#0000FF")
        assert "\x1b[" in result

    def test_empty_text_returns_empty_string(self) -> None:
        renderer = GradientRenderer()
        result = renderer.render_text_ansi("", "#FF0000", "#0000FF")
        assert result == ""

    @pytest.mark.parametrize("invalid_color", ["red", "FF0000", "#GGG", "", "#FF00"])
    def test_invalid_start_color_raises_config_error(self, invalid_color: str) -> None:
        renderer = GradientRenderer(normal_mode=False)
        with pytest.raises(ConfigError, match="颜色格式无效"):
            renderer.render_text_ansi("test", invalid_color, "#0000FF")

    @pytest.mark.parametrize("invalid_color", ["blue", "00FF00", "#XYZ", None])
    def test_invalid_end_color_raises_config_error(self, invalid_color: str) -> None:
        renderer = GradientRenderer(normal_mode=False)
        with pytest.raises((ConfigError, TypeError)):
            renderer.render_text_ansi("test", "#FF0000", invalid_color)

    def test_progress_bar_zero(self) -> None:
        renderer = GradientRenderer(normal_mode=True)
        result = renderer.render_progress_bar(0, 10, width=10)
        assert result == "[----------] 0%"

    def test_progress_bar_full(self) -> None:
        renderer = GradientRenderer(normal_mode=True)
        result = renderer.render_progress_bar(10, 10, width=10)
        assert result == "[==========] 100%"

    def test_progress_exceeds_total_raises_error(self) -> None:
        renderer = GradientRenderer()
        with pytest.raises(ConfigError, match="进度值无效"):
            renderer.render_progress_bar(11, 10)

    def test_negative_progress_raises_error(self) -> None:
        renderer = GradientRenderer()
        with pytest.raises(ConfigError, match="进度值无效"):
            renderer.render_progress_bar(-1, 10)

    def test_get_display_width_cjk(self) -> None:
        assert GradientRenderer.get_display_width("你好") == 4
        assert GradientRenderer.get_display_width("Hello") == 5
        assert GradientRenderer.get_display_width("Hi你") == 4
