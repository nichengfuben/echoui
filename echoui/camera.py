"""Camera for free-layout scenes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Tuple


@dataclass
class Camera:
    x: float = 0
    y: float = 0
    zoom: float = 1.0
    rotation: float = 0
    follow_target: Optional[str] = None
    lerp: float = 0.1
    deadzone: Tuple[float, float] = (0, 0)
    bounds: Optional[Tuple[float, float, float, float]] = None
    _shake_t: float = 0
    _shake_mag: float = 0

    def follow(self, target: Any, *, lerp: float = 0.1, deadzone: Tuple[float, float] = (0, 0)) -> "Camera":
        name = target if isinstance(target, str) else getattr(target, "id", str(target))
        self.follow_target = name
        self.lerp = lerp
        self.deadzone = deadzone
        return self

    def zoom_to(self, zoom: float, duration: float = 0) -> "Camera":
        self.zoom = zoom
        return self

    def shake(self, magnitude: float, duration: float) -> "Camera":
        self._shake_mag = magnitude
        self._shake_t = duration
        return self

    def tick(self, dt: float, targets: dict[str, tuple[float, float]]) -> None:
        if self.follow_target and self.follow_target in targets:
            tx, ty = targets[self.follow_target]
            self.x += (tx - self.x) * self.lerp
            self.y += (ty - self.y) * self.lerp
        if self._shake_t > 0:
            self._shake_t = max(0, self._shake_t - dt)
        if self.bounds:
            bx0, by0, bx1, by1 = self.bounds
            self.x = max(bx0, min(bx1, self.x))
            self.y = max(by0, min(by1, self.y))

    def shake_offset(self) -> tuple[float, float]:
        if self._shake_t <= 0:
            return 0.0, 0.0
        import random

        m = self._shake_mag * (self._shake_t / max(self._shake_t, 0.001))
        return random.uniform(-m, m), random.uniform(-m, m)

    def to_dict(self) -> dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "zoom": self.zoom,
            "rotation": self.rotation,
            "follow": self.follow_target,
            "lerp": self.lerp,
            "deadzone": self.deadzone,
            "bounds": self.bounds,
        }
