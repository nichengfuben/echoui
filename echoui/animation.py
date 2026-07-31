"""Tween, spring, and keyframe animations."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class Tween:
    start: float
    end: float
    duration: float
    elapsed: float = 0
    on_update: Optional[Callable[[float], None]] = None
    easing: Callable[[float], float] = lambda t: t

    def tick(self, dt: float) -> bool:
        self.elapsed = min(self.duration, self.elapsed + dt)
        t = self.elapsed / self.duration if self.duration else 1
        val = self.start + (self.end - self.start) * self.easing(t)
        if self.on_update:
            self.on_update(val)
        return self.elapsed >= self.duration


@dataclass
class Spring:
    target: float
    current: float = 0
    velocity: float = 0
    stiffness: float = 180
    damping: float = 12
    on_update: Optional[Callable[[float], None]] = None

    def tick(self, dt: float) -> bool:
        force = -self.stiffness * (self.current - self.target)
        damp = -self.damping * self.velocity
        accel = force + damp
        self.velocity += accel * dt
        self.current += self.velocity * dt
        if self.on_update:
            self.on_update(self.current)
        return abs(self.current - self.target) < 0.01 and abs(self.velocity) < 0.01


@dataclass
class Keyframe:
    offset: float
    props: Dict[str, Any]


@dataclass
class Keyframes:
    frames: List[Keyframe] = field(default_factory=list)
    duration: float = 1.0
    elapsed: float = 0

    def tick(self, dt: float) -> bool:
        self.elapsed = min(self.duration, self.elapsed + dt)
        return self.elapsed >= self.duration

    def value_at(self, prop: str) -> Any:
        if not self.frames:
            return None
        return self.frames[-1].props.get(prop)


@dataclass
class Timeline:
    tweens: List[Tween] = field(default_factory=list)

    def add(self, tween: Tween) -> "Timeline":
        self.tweens.append(tween)
        return self

    def tick(self, dt: float) -> bool:
        return all(t.tick(dt) for t in self.tweens)


def spring(target: float, **kwargs: Any) -> Spring:
    return Spring(target=target, **kwargs)


def keyframes(*frames: Keyframe, duration: float = 1.0) -> Keyframes:
    return Keyframes(frames=list(frames), duration=duration)


def ease_linear(t: float) -> float:
    return t


def ease_in(t: float) -> float:
    return t * t * t


def ease_out(t: float) -> float:
    return 1 - math.pow(1 - t, 3)


def ease_in_out(t: float) -> float:
    if t < 0.5:
        return 4 * t * t * t
    return 1 - math.pow(-2 * t + 2, 3) / 2


def ease_out_expo(t: float) -> float:
    if t >= 1:
        return 1.0
    return 1 - math.pow(2, -10 * t)


def ease_out_back(t: float) -> float:
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * math.pow(t - 1, 3) + c1 * math.pow(t - 1, 2)


def ease_out_bounce(t: float) -> float:
    n1 = 7.5625
    d1 = 2.75
    if t < 1 / d1:
        return n1 * t * t
    if t < 2 / d1:
        t = t - 1.5 / d1
        return n1 * t * t + 0.75
    if t < 2.5 / d1:
        t = t - 2.25 / d1
        return n1 * t * t + 0.9375
    t = t - 2.625 / d1
    return n1 * t * t + 0.984375


EASINGS: Dict[str, Callable[[float], float]] = {
    "linear": ease_linear,
    "ease_in": ease_in,
    "ease_out": ease_out,
    "ease_in_out": ease_in_out,
    "ease_out_expo": ease_out_expo,
    "ease_out_back": ease_out_back,
    "ease_out_bounce": ease_out_bounce,
}


def resolve_easing(name: str | Callable[[float], float] | None) -> Callable[[float], float]:
    if name is None:
        return ease_linear
    if callable(name):
        return name
    return EASINGS.get(str(name), ease_linear)


def tween(
    start: float,
    end: float,
    duration: float,
    *,
    easing: str | Callable[[float], float] | None = None,
    on_update: Optional[Callable[[float], None]] = None,
    **kwargs: Any,
) -> Tween:
    ease_fn = resolve_easing(easing if easing is not None else kwargs.pop("easing", None))
    return Tween(start=start, end=end, duration=duration, on_update=on_update, easing=ease_fn, **kwargs)


@dataclass
class Rect:
    x: float
    y: float
    width: float = 0.0
    height: float = 0.0


@dataclass
class FlipDelta:
    key: str
    dx: float
    dy: float
    sx: float = 1.0
    sy: float = 1.0


@dataclass
class FlipAnimation:
    """First/Last/Invert/Play — list reorder deltas driven by Tween ticks."""

    deltas: List[FlipDelta]
    duration: float = 0.3
    easing: Callable[[float], float] = field(default_factory=lambda: ease_out)
    on_update: Optional[Callable[[str, float, float], None]] = None
    _elapsed: float = 0.0
    _done: bool = False

    def tick(self, dt: float) -> bool:
        if self._done:
            return True
        self._elapsed = min(self.duration, self._elapsed + dt)
        t = self._elapsed / self.duration if self.duration else 1.0
        p = self.easing(t)
        inv = 1.0 - p
        if self.on_update:
            for d in self.deltas:
                self.on_update(d.key, d.dx * inv, d.dy * inv)
        self._done = self._elapsed >= self.duration
        if self._done and self.on_update:
            for d in self.deltas:
                self.on_update(d.key, 0.0, 0.0)
        return self._done


def capture_rects(items: Dict[str, Rect] | Dict[str, tuple[float, float]]) -> Dict[str, Rect]:
    """Snapshot element rects keyed by stable id (First or Last step)."""
    out: Dict[str, Rect] = {}
    for key, val in items.items():
        if isinstance(val, Rect):
            out[key] = Rect(val.x, val.y, val.width, val.height)
        else:
            x, y = val[0], val[1]
            w = val[2] if len(val) > 2 else 0.0  # type: ignore[index]
            h = val[3] if len(val) > 3 else 0.0  # type: ignore[index]
            out[key] = Rect(float(x), float(y), float(w), float(h))
    return out


def invert_rects(first: Dict[str, Rect], last: Dict[str, Rect]) -> List[FlipDelta]:
    """Compute invert deltas so elements appear to move from first → last."""
    deltas: List[FlipDelta] = []
    for key, a in first.items():
        b = last.get(key)
        if b is None:
            continue
        sx = (a.width / b.width) if b.width else 1.0
        sy = (a.height / b.height) if b.height else 1.0
        deltas.append(FlipDelta(key=key, dx=a.x - b.x, dy=a.y - b.y, sx=sx, sy=sy))
    return deltas


def flip(
    first: Dict[str, Rect] | Dict[str, tuple[float, float]],
    last: Dict[str, Rect] | Dict[str, tuple[float, float]],
    *,
    duration: float = 0.3,
    easing: str | Callable[[float], float] | None = "ease_out",
    on_update: Optional[Callable[[str, float, float], None]] = None,
) -> FlipAnimation:
    """Build a FLIP animation from before/after rect maps (list reorder)."""
    first_map = capture_rects(first)
    last_map = capture_rects(last)
    return FlipAnimation(
        deltas=invert_rects(first_map, last_map),
        duration=duration,
        easing=resolve_easing(easing),
        on_update=on_update,
    )
