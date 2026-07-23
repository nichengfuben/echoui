"""Pointer gesture helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, Tuple


@dataclass
class DragState:
    active: bool = False
    start: Tuple[float, float] = (0, 0)
    current: Tuple[float, float] = (0, 0)
    on_drag: Optional[Callable[[float, float], None]] = None

    def pointer_down(self, x: float, y: float) -> None:
        self.active = True
        self.start = (x, y)
        self.current = (x, y)

    def pointer_move(self, x: float, y: float) -> None:
        if not self.active:
            return
        dx = x - self.current[0]
        dy = y - self.current[1]
        self.current = (x, y)
        if self.on_drag:
            self.on_drag(dx, dy)

    def pointer_up(self) -> None:
        self.active = False


def draggable(on_drag: Callable[[float, float], None] | None = None) -> DragState:
    return DragState(on_drag=on_drag)


@dataclass
class PanState:
    offset: Tuple[float, float] = (0, 0)
    _drag: DragState = field(default_factory=DragState)

    def __post_init__(self) -> None:
        self._drag.on_drag = self._apply

    def _apply(self, dx: float, dy: float) -> None:
        ox, oy = self.offset
        self.offset = (ox + dx, oy + dy)


def pannable() -> PanState:
    return PanState()


@dataclass
class PinchState:
    scale: float = 1.0
    _dist: float = 0

    def pointer_down(self, d1: Tuple[float, float], d2: Tuple[float, float]) -> None:
        self._dist = _distance(d1, d2)

    def pointer_move(self, d1: Tuple[float, float], d2: Tuple[float, float]) -> None:
        if self._dist <= 0:
            return
        nd = _distance(d1, d2)
        self.scale *= nd / self._dist
        self._dist = nd


def pinchable() -> PinchState:
    return PinchState()


@dataclass
class SwipeState:
    threshold: float = 50
    on_swipe: Optional[Callable[[str], None]] = None
    _start: Tuple[float, float] = (0, 0)

    def pointer_down(self, x: float, y: float) -> None:
        self._start = (x, y)

    def pointer_up(self, x: float, y: float) -> None:
        dx = x - self._start[0]
        dy = y - self._start[1]
        if abs(dx) > self.threshold and abs(dx) > abs(dy):
            direction = "left" if dx < 0 else "right"
            if self.on_swipe:
                self.on_swipe(direction)
        elif abs(dy) > self.threshold:
            direction = "up" if dy < 0 else "down"
            if self.on_swipe:
                self.on_swipe(direction)


def swipeable(on_swipe: Callable[[str], None] | None = None, threshold: float = 50) -> SwipeState:
    return SwipeState(threshold=threshold, on_swipe=on_swipe)


def _distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
