from __future__ import annotations

import pytest

from echoui.core.exceptions import ConfigError
from echoui.utils.color import hex_to_rgb, interpolate_color, validate_hex_color


class TestValidateHexColor:
    """validate_hex_color 测试。"""

    def test_valid_uppercase(self) -> None:
        """大写颜色应通过验证。"""
        assert validate_hex_color("#FF0000") == "#FF0000"

    def test_valid_lowercase(self) -> None:
        """小写颜色应通过验证。"""
        assert validate_hex_color("#ff0000") == "#ff0000"

    def test_valid_mixed(self) -> None:
        """混合大小写应通过验证。"""
        assert validate_hex_color("#Ff0000") == "#Ff0000"

    @pytest.mark.parametrize(
        "invalid",
        [
            "red",
            "#FFF",
            "#GGGGGG",
            "rgb(255,0,0)",
            "",
            "#FF6B6B6B",
            "FFFFFF",
            "#",
        ],
    )
    def test_invalid_colors_raise(self, invalid: str) -> None:
        """各种非法颜色格式应抛出 ConfigError。"""
        with pytest.raises(ConfigError, match="颜色格式无效"):
            validate_hex_color(invalid)


class TestHexToRgb:
    """hex_to_rgb 测试。"""

    def test_red(self) -> None:
        """红色转换应正确。"""
        assert hex_to_rgb("#FF0000") == (255, 0, 0)

    def test_green(self) -> None:
        """绿色转换应正确。"""
        assert hex_to_rgb("#00FF00") == (0, 255, 0)

    def test_blue(self) -> None:
        """蓝色转换应正确。"""
        assert hex_to_rgb("#0000FF") == (0, 0, 255)

    def test_white(self) -> None:
        """白色转换应正确。"""
        assert hex_to_rgb("#FFFFFF") == (255, 255, 255)

    def test_black(self) -> None:
        """黑色转换应正确。"""
        assert hex_to_rgb("#000000") == (0, 0, 0)

    def test_invalid_color_raises(self) -> None:
        """非法颜色应抛出 ConfigError。"""
        with pytest.raises(ConfigError):
            hex_to_rgb("invalid")


class TestInterpolateColor:
    """interpolate_color 测试。"""

    def test_t_zero_returns_start(self) -> None:
        """t=0 应返回起始颜色。"""
        assert interpolate_color("#000000", "#FFFFFF", 0.0) == "#000000"

    def test_t_one_returns_end(self) -> None:
        """t=1 应返回结束颜色。"""
        assert interpolate_color("#000000", "#FFFFFF", 1.0) == "#FFFFFF"

    def test_t_half_returns_midpoint(self) -> None:
        """t=0.5 应返回中间颜色。"""
        result = interpolate_color("#000000", "#FFFFFF", 0.5)
        assert result == "#7F7F7F"

    def test_invalid_t_raises(self) -> None:
        """t 超出范围应抛出 ConfigError。"""
        with pytest.raises(ConfigError, match="插值系数"):
            interpolate_color("#000000", "#FFFFFF", 1.5)

    def test_invalid_start_color_raises(self) -> None:
        """非法起始颜色应抛出 ConfigError。"""
        with pytest.raises(ConfigError):
            interpolate_color("red", "#FFFFFF", 0.5)

    def test_invalid_end_color_raises(self) -> None:
        """非法结束颜色应抛出 ConfigError。"""
        with pytest.raises(ConfigError):
            interpolate_color("#000000", "blue", 0.5)
