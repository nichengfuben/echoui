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


def tween(start: float, end: float, duration: float, **kwargs: Any) -> Tween:
    return Tween(start=start, end=end, duration=duration, **kwargs)


def spring(target: float, **kwargs: Any) -> Spring:
    return Spring(target=target, **kwargs)


def keyframes(*frames: Keyframe, duration: float = 1.0) -> Keyframes:
    return Keyframes(frames=list(frames), duration=duration)


def ease_out(t: float) -> float:
    return 1 - math.pow(1 - t, 3)
