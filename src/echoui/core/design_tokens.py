from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class RadiusToken:
    """圆角令牌（流体，随视口缩放）。

    Attributes:
        variable: CSS 变量名。
        min_px: 最小圆角半径（px）。
        max_px: 最大圆角半径（px）。
    """

    variable: str
    min_px: int
    max_px: int

    def compute_px(self, viewport_width: int) -> int:
        """计算当前视口下的圆角像素值。

        Args:
            viewport_width: 视口宽度（px）。

        Returns:
            int: 圆角半径（px），已在 320-1920px 范围内线性插值并取整。

        Examples:
            >>> token = RADIUS_MAP["md"]
            >>> token.compute_px(320) == token.min_px
            True
            >>> token.compute_px(1920) == token.max_px
            True
        """
        min_vp: Final[int] = 320
        max_vp: Final[int] = 1920
        t = max(0.0, min(1.0, (viewport_width - min_vp) / (max_vp - min_vp)))
        return round(self.min_px + (self.max_px - self.min_px) * t)


@dataclass(frozen=True)
class ShadowToken:
    """阴影令牌（流体，随视口缩放）。

    Attributes:
        variable: CSS 变量名。
        blur_min_px: 最小模糊半径（px）。
        blur_max_px: 最大模糊半径（px）。
        spread_min_px: 最小扩展半径（px）。
        spread_max_px: 最大扩展半径（px）。
        use_cases: 适用场景描述。
    """

    variable: str
    blur_min_px: int
    blur_max_px: int
    spread_min_px: int
    spread_max_px: int
    use_cases: str


RADIUS_MAP: dict[str, RadiusToken] = {
    "xs": RadiusToken("--radius-xs", min_px=2, max_px=4),
    "sm": RadiusToken("--radius-sm", min_px=4, max_px=8),
    "md": RadiusToken("--radius-md", min_px=6, max_px=12),
    "lg": RadiusToken("--radius-lg", min_px=8, max_px=16),
    "xl": RadiusToken("--radius-xl", min_px=10, max_px=20),
    "2xl": RadiusToken("--radius-2xl", min_px=12, max_px=24),
    "full": RadiusToken("--radius-full", min_px=9999, max_px=9999),
}

SHADOW_MAP: dict[str, ShadowToken] = {
    "sm": ShadowToken("--shadow-sm", 1, 2, 4, 10, "列表项/图标"),
    "md": ShadowToken("--shadow-md", 2, 4, 8, 20, "卡片/下拉菜单"),
    "lg": ShadowToken("--shadow-lg", 4, 8, 16, 32, "模态框/面板"),
    "xl": ShadowToken("--shadow-xl", 6, 12, 20, 40, "悬浮元素"),
    "glow": ShadowToken("--shadow-glow", 8, 16, 0, 0, "辉光标题"),
}

# 背景装饰图形类型（枚举安全集合）
BG_SHAPE_TYPES: Final[frozenset[str]] = frozenset(
    {"circle", "square", "triangle", "hexagon", "diamond"}
)
