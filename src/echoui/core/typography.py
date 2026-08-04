from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class FluidTypeScale:
    """流体字号配置（clamp 三值插值）。

    Attributes:
        variable: CSS 变量名（也用作标识符）。
        min_rem: 最小字号（rem），在 320px 视口时生效。
        preferred_intercept: 插值基础值（rem）。
        preferred_vw_coefficient: 视口宽度系数（vw 乘数）。
        max_rem: 最大字号（rem），在 1920px 视口时生效。
        line_height: 对应的行高比例。
    """

    variable: str
    min_rem: float
    preferred_intercept: float
    preferred_vw_coefficient: float
    max_rem: float
    line_height: float

    def to_css_clamp(self) -> str:
        """生成对应的 CSS clamp() 函数字符串。

        Returns:
            str: 形如 "clamp(Xrem, Yrem + Zvw, Wrem)" 的字符串。

        Examples:
            >>> scale = TYPE_SCALE_MAP["body"]
            >>> "clamp(" in scale.to_css_clamp()
            True
        """
        return (
            f"clamp("
            f"{self.min_rem}rem, "
            f"{self.preferred_intercept}rem + {self.preferred_vw_coefficient}vw, "
            f"{self.max_rem}rem)"
        )

    def compute_px(self, viewport_width: int) -> float:
        """在给定视口宽度下计算实际字号（px）。

        用于终端和桌面端的字号近似计算（1rem = 16px 基准）。

        Args:
            viewport_width: 视口宽度（px）。

        Returns:
            float: 实际字号（px），已被 clamp 约束在 min/max 范围内。

        Examples:
            >>> scale = TYPE_SCALE_MAP["body"]
            >>> px = scale.compute_px(1024)
            >>> scale.min_rem * 16 <= px <= scale.max_rem * 16
            True
        """
        base_px: Final[int] = 16
        min_px = self.min_rem * base_px
        max_px = self.max_rem * base_px
        preferred_px = (
            self.preferred_intercept * base_px
            + self.preferred_vw_coefficient * viewport_width / 100
        )
        return max(min_px, min(preferred_px, max_px))


# 权威字号阶梯表
TYPE_SCALE_MAP: dict[str, FluidTypeScale] = {
    "display": FluidTypeScale(
        variable="--fs-display",
        min_rem=1.5,
        preferred_intercept=1.0,
        preferred_vw_coefficient=2.5,
        max_rem=3.5,
        line_height=1.25,
    ),
    "h1": FluidTypeScale(
        variable="--fs-h1",
        min_rem=1.25,
        preferred_intercept=0.9,
        preferred_vw_coefficient=1.75,
        max_rem=2.5,
        line_height=1.25,
    ),
    "h2": FluidTypeScale(
        variable="--fs-h2",
        min_rem=1.125,
        preferred_intercept=0.95,
        preferred_vw_coefficient=0.875,
        max_rem=1.75,
        line_height=1.25,
    ),
    "h3": FluidTypeScale(
        variable="--fs-h3",
        min_rem=1.0,
        preferred_intercept=0.9,
        preferred_vw_coefficient=0.5,
        max_rem=1.375,
        line_height=1.25,
    ),
    "body": FluidTypeScale(
        variable="--fs-body",
        min_rem=0.875,
        preferred_intercept=0.825,
        preferred_vw_coefficient=0.25,
        max_rem=1.125,
        line_height=1.6,
    ),
    "small": FluidTypeScale(
        variable="--fs-small",
        min_rem=0.75,
        preferred_intercept=0.72,
        preferred_vw_coefficient=0.15,
        max_rem=0.9375,
        line_height=1.5,
    ),
    "caption": FluidTypeScale(
        variable="--fs-caption",
        min_rem=0.6875,
        preferred_intercept=0.66,
        preferred_vw_coefficient=0.14,
        max_rem=0.8125,
        line_height=1.5,
    ),
    "micro": FluidTypeScale(
        variable="--fs-micro",
        min_rem=0.5625,
        preferred_intercept=0.55,
        preferred_vw_coefficient=0.0625,
        max_rem=0.6875,
        line_height=1.5,
    ),
}

# 正文段落最大宽度约束
BODY_MAX_CHARS: str = "clamp(28ch, 50vw, 72ch)"

# 消息气泡最大宽度约束
BUBBLE_MAX_CHARS: str = "clamp(20ch, 70vw, 60ch)"
