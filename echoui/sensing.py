"""Sprite sensing helpers."""

from __future__ import annotations

import math
from typing import Any, Tuple


def _rect(sprite: Any) -> Tuple[float, float, float, float]:
    w = getattr(sprite, "width", getattr(sprite, "w", 32))
    h = getattr(sprite, "height", getattr(sprite, "h", 32))
    return sprite.x, sprite.y, float(w), float(h)


def touches(a: Any, b: Any) -> bool:
    ax, ay, aw, ah = _rect(a)
    bx, by, bw, bh = _rect(b)
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


def touches_point(sprite: Any, px: float, py: float) -> bool:
    x, y, w, h = _rect(sprite)
    return x <= px <= x + w and y <= py <= y + h


def touches_edge(sprite: Any, stage_w: float, stage_h: float) -> bool:
    x, y, w, h = _rect(sprite)
    return x <= 0 or y <= 0 or x + w >= stage_w or y + h >= stage_h


def distance_to(a: Any, b: Any) -> float:
    ax, ay, _, _ = _rect(a)
    bx, by, _, _ = _rect(b)
    return math.hypot(bx - ax, by - ay)


def overlapping(a: Any, b: Any) -> bool:
    return touches(a, b)


def touches_color(sprite: Any, color: str, *, tolerance: int = 0) -> bool:
    target = str(color).lower().strip()
    bg = getattr(sprite, "background", None)
    if bg is None and hasattr(sprite, "props"):
        bg = sprite.props.get("background")  # type: ignore[attr-defined]
    if bg is None:
        return False
    current = str(bg).lower().strip()
    if tolerance <= 0:
        return current == target
    return current == target


def touches_team(sprite: Any, team: str, others: list[Any]) -> bool:
    for other in others:
        if getattr(other, "team", None) == team and touches(sprite, other):
            return True
    return False


def raycast(sprite: Any, angle_deg: float, max_dist: float = 500) -> Tuple[float, float]:
    rad = math.radians(angle_deg)
    return sprite.x + math.cos(rad) * max_dist, sprite.y + math.sin(rad) * max_dist
