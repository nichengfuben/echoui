from __future__ import annotations

import re

from echoui.core.exceptions import ConfigError

_HEX_COLOR_PATTERN: re.Pattern[str] = re.compile(r"^#[0-9A-Fa-f]{6}$")


def validate_hex_color(color: str) -> str:
    """验证十六进制颜色格式。

    Args:
        color: 待验证的颜色字符串。

    Returns:
        str: 验证通过的颜色字符串。

    Raises:
        ConfigError: 当颜色格式不合法时抛出。

    Examples:
        >>> validate_hex_color("#FF6B6B")
        '#FF6B6B'
        >>> try:
        ...     validate_hex_color("red")
        ... except ConfigError as e:
        ...     "无效" in str(e)
        True
    """
    if not _HEX_COLOR_PATTERN.match(color):
        raise ConfigError(f"颜色格式无效，期望 #RRGGBB 格式: {color!r}")
    return color


def hex_to_rgb(color: str) -> tuple[int, int, int]:
    """将 #RRGGBB 颜色转换为 RGB 三元组。

    Args:
        color: 十六进制颜色字符串。

    Returns:
        tuple[int, int, int]: (R, G, B) 三元组，每个值范围 0-255。

    Examples:
        >>> hex_to_rgb("#FF0000")
        (255, 0, 0)
        >>> hex_to_rgb("#00FF00")
        (0, 255, 0)
    """
    validate_hex_color(color)
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    return (r, g, b)


def interpolate_color(
    start: str,
    end: str,
    t: float,
) -> str:
    """在两个颜色之间线性插值。

    Args:
        start: 起始颜色（#RRGGBB）。
        end: 结束颜色（#RRGGBB）。
        t: 插值系数，范围 [0.0, 1.0]。

    Returns:
        str: 插值后的颜色（#RRGGBB）。

    Examples:
        >>> interpolate_color("#000000", "#FFFFFF", 0.5)
        '#7F7F7F'
    """
    validate_hex_color(start)
    validate_hex_color(end)
    if t < 0.0 or t > 1.0:
        raise ConfigError(f"插值系数必须在 [0.0, 1.0] 范围内: {t}")

    sr, sg, sb = hex_to_rgb(start)
    er, eg, eb = hex_to_rgb(end)

    r = int(sr + (er - sr) * t)
    g = int(sg + (eg - sg) * t)
    b = int(sb + (eb - sb) * t)

    return f"#{r:02X}{g:02X}{b:02X}"
