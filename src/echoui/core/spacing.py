from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class SpacingScale:
    """流体间距配置（基于 4px 网格，clamp 插值）。

    Attributes:
        variable: CSS 变量名。
        min_px: 最小间距（px）。
        max_px: 最大间距（px）。
    """

    variable: str
    min_px: int
    max_px: int

    def compute_px(self, viewport_width: int) -> float:
        """在给定视口宽度下计算实际间距（px）。

        Args:
            viewport_width: 视口宽度（px）。

        Returns:
            float: 实际间距（px）。

        Examples:
            >>> scale = SPACING_MAP["md"]
            >>> scale.compute_px(320) == scale.min_px
            True
            >>> scale.compute_px(1920) == scale.max_px
            True
        """
        min_vp: Final[int] = 320
        max_vp: Final[int] = 1920
        t = (viewport_width - min_vp) / (max_vp - min_vp)
        t = max(0.0, min(1.0, t))
        return self.min_px + (self.max_px - self.min_px) * t


# 间距阶梯（4px 网格，共 9 级）
SPACING_MAP: dict[str, SpacingScale] = {
    "3xs": SpacingScale("--space-3xs", min_px=2, max_px=4),
    "2xs": SpacingScale("--space-2xs", min_px=4, max_px=8),
    "xs": SpacingScale("--space-xs", min_px=6, max_px=12),
    "sm": SpacingScale("--space-sm", min_px=8, max_px=16),
    "md": SpacingScale("--space-md", min_px=12, max_px=24),
    "lg": SpacingScale("--space-lg", min_px=16, max_px=32),
    "xl": SpacingScale("--space-xl", min_px=24, max_px=48),
    "2xl": SpacingScale("--space-2xl", min_px=32, max_px=64),
    "3xl": SpacingScale("--space-3xl", min_px=48, max_px=96),
}

# 页面边距（特殊处理，4K+ 扩展至 64px）
PAGE_PADDING_MIN: Final[int] = 8  # 320px 视口
PAGE_PADDING_MAX: Final[int] = 32  # 1920px 视口
PAGE_PADDING_4K: Final[int] = 64  # 3840px+ 视口
