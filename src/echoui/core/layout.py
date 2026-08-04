from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Breakpoint(str, Enum):
    """14 级视口断点枚举。"""

    XS3 = "3xs"
    XS2 = "2xs"
    XS = "xs"
    SM = "sm"
    MD = "md"
    LG = "lg"
    XL = "xl"
    XL2 = "2xl"
    XL3 = "3xl"
    XL4 = "4xl"
    XL5 = "5xl"
    XL6 = "6xl"
    XL7 = "7xl"
    XL8 = "8xl"


@dataclass(frozen=True)
class BreakpointConfig:
    """单个断点的完整布局配置。

    Attributes:
        name: 断点名称。
        min_width: 最小视口宽度（px），None 表示无下限。
        max_width: 最大视口宽度（px），None 表示无上限。
        layout_mode: 布局模式（single/double/triple/multi）。
        sidebar_behavior: 侧栏行为描述。
        sidebar_width: 侧栏宽度（px），0 表示隐藏。
        content_density: 内容密度等级（low/medium/high/ultra）。
        bg_shape_max: 背景装饰图形最大数量。
        bg_echo_max: 背景残影最大数量。
    """

    name: Breakpoint
    min_width: Optional[int]
    max_width: Optional[int]
    layout_mode: str
    sidebar_behavior: str
    sidebar_width: int
    content_density: str
    bg_shape_max: int
    bg_echo_max: int


# 断点完整配置表（权威数据源，所有计算引用此处）
BREAKPOINT_CONFIGS: tuple[BreakpointConfig, ...] = (
    BreakpointConfig(
        name=Breakpoint.XS3,
        min_width=None,
        max_width=179,
        layout_mode="single",
        sidebar_behavior="手势触发",
        sidebar_width=0,
        content_density="ultra-low",
        bg_shape_max=0,
        bg_echo_max=0,
    ),
    BreakpointConfig(
        name=Breakpoint.XS2,
        min_width=180,
        max_width=239,
        layout_mode="single",
        sidebar_behavior="底部菜单",
        sidebar_width=0,
        content_density="low",
        bg_shape_max=0,
        bg_echo_max=0,
    ),
    BreakpointConfig(
        name=Breakpoint.XS,
        min_width=240,
        max_width=319,
        layout_mode="single",
        sidebar_behavior="抽屉",
        sidebar_width=0,
        content_density="low",
        bg_shape_max=0,
        bg_echo_max=0,
    ),
    BreakpointConfig(
        name=Breakpoint.SM,
        min_width=320,
        max_width=479,
        layout_mode="single",
        sidebar_behavior="抽屉(85%宽)",
        sidebar_width=0,
        content_density="low",
        bg_shape_max=2,
        bg_echo_max=2,
    ),
    BreakpointConfig(
        name=Breakpoint.MD,
        min_width=480,
        max_width=639,
        layout_mode="single",
        sidebar_behavior="抽屉(70%宽)",
        sidebar_width=0,
        content_density="medium",
        bg_shape_max=2,
        bg_echo_max=2,
    ),
    BreakpointConfig(
        name=Breakpoint.LG,
        min_width=640,
        max_width=767,
        layout_mode="single",
        sidebar_behavior="条件显示",
        sidebar_width=0,
        content_density="medium",
        bg_shape_max=2,
        bg_echo_max=2,
    ),
    BreakpointConfig(
        name=Breakpoint.XL,
        min_width=768,
        max_width=1023,
        layout_mode="double",
        sidebar_behavior="侧边抽屉",
        sidebar_width=220,
        content_density="medium",
        bg_shape_max=2,
        bg_echo_max=4,
    ),
    BreakpointConfig(
        name=Breakpoint.XL2,
        min_width=1024,
        max_width=1279,
        layout_mode="double",
        sidebar_behavior="侧边常驻",
        sidebar_width=240,
        content_density="medium-high",
        bg_shape_max=2,
        bg_echo_max=4,
    ),
    BreakpointConfig(
        name=Breakpoint.XL3,
        min_width=1280,
        max_width=1535,
        layout_mode="triple",
        sidebar_behavior="两侧常驻",
        sidebar_width=256,
        content_density="high",
        bg_shape_max=3,
        bg_echo_max=6,
    ),
    BreakpointConfig(
        name=Breakpoint.XL4,
        min_width=1536,
        max_width=1919,
        layout_mode="triple",
        sidebar_behavior="两侧常驻",
        sidebar_width=280,
        content_density="high",
        bg_shape_max=3,
        bg_echo_max=6,
    ),
    BreakpointConfig(
        name=Breakpoint.XL5,
        min_width=1920,
        max_width=2559,
        layout_mode="triple",
        sidebar_behavior="两侧常驻(居中约束)",
        sidebar_width=300,
        content_density="high",
        bg_shape_max=3,
        bg_echo_max=6,
    ),
    BreakpointConfig(
        name=Breakpoint.XL6,
        min_width=2560,
        max_width=3839,
        layout_mode="triple",
        sidebar_behavior="两侧常驻(边距扩展)",
        sidebar_width=360,
        content_density="ultra",
        bg_shape_max=5,
        bg_echo_max=10,
    ),
    BreakpointConfig(
        name=Breakpoint.XL7,
        min_width=3840,
        max_width=5119,
        layout_mode="multi",
        sidebar_behavior="两侧常驻",
        sidebar_width=480,
        content_density="ultra",
        bg_shape_max=5,
        bg_echo_max=10,
    ),
    BreakpointConfig(
        name=Breakpoint.XL8,
        min_width=5120,
        max_width=None,
        layout_mode="multi",
        sidebar_behavior="两侧常驻",
        sidebar_width=560,
        content_density="ultra",
        bg_shape_max=5,
        bg_echo_max=10,
    ),
)


def resolve_breakpoint(viewport_width: int) -> BreakpointConfig:
    """根据视口宽度解析对应的断点配置。

    Args:
        viewport_width: 当前视口宽度（px），必须为正整数。

    Returns:
        BreakpointConfig: 匹配的断点配置。

    Raises:
        ConfigError: 当 viewport_width 为负数时抛出。

    Examples:
        >>> config = resolve_breakpoint(1024)
        >>> config.name == Breakpoint.XL2
        True
        >>> resolve_breakpoint(320).name == Breakpoint.SM
        True
    """
    from echoui.core.exceptions import ConfigError

    if viewport_width < 0:
        raise ConfigError(f"视口宽度不能为负数: {viewport_width}")

    for config in BREAKPOINT_CONFIGS:
        min_ok = config.min_width is None or viewport_width >= config.min_width
        max_ok = config.max_width is None or viewport_width <= config.max_width
        if min_ok and max_ok:
            return config

    # 回退到最大断点（理论上不会触发）
    return BREAKPOINT_CONFIGS[-1]
