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
    _shake_duration: float = 0
    _zoom_from: float = 1.0
    _zoom_to: float = 1.0
    _zoom_t: float = 0
    _zoom_duration: float = 0

    def follow(self, target: Any, *, lerp: float = 0.1, deadzone: Tuple[float, float] = (0, 0)) -> "Camera":
        name = target if isinstance(target, str) else getattr(target, "id", str(target))
        self.follow_target = name
        self.lerp = lerp
        self.deadzone = deadzone
        return self

    def zoom_to(self, zoom: float, duration: float = 0) -> "Camera":
        if duration <= 0:
            self.zoom = zoom
            self._zoom_duration = 0
            self._zoom_t = 0
        else:
            self._zoom_from = self.zoom
            self._zoom_to = zoom
            self._zoom_duration = duration
            self._zoom_t = duration
        return self

    def shake(self, magnitude: float, duration: float) -> "Camera":
        self._shake_mag = magnitude
        self._shake_duration = max(duration, 0.0)
        self._shake_t = self._shake_duration
        return self

    def tick(self, dt: float, targets: dict[str, tuple[float, float]]) -> None:
        if self.follow_target and self.follow_target in targets:
            tx, ty = targets[self.follow_target]
            dx = tx - self.x
            dy = ty - self.y
            dzx, dzy = self.deadzone
            if abs(dx) > dzx:
                self.x += (dx - (dzx if dx > 0 else -dzx)) * self.lerp
            if abs(dy) > dzy:
                self.y += (dy - (dzy if dy > 0 else -dzy)) * self.lerp
        if self._zoom_t > 0 and self._zoom_duration > 0:
            self._zoom_t = max(0.0, self._zoom_t - dt)
            t = 1.0 - (self._zoom_t / self._zoom_duration)
            self.zoom = self._zoom_from + (self._zoom_to - self._zoom_from) * t
            if self._zoom_t <= 0:
                self.zoom = self._zoom_to
        if self._shake_t > 0:
            self._shake_t = max(0.0, self._shake_t - dt)
        if self.bounds:
            bx0, by0, bx1, by1 = self.bounds
            self.x = max(bx0, min(bx1, self.x))
            self.y = max(by0, min(by1, self.y))

    def shake_offset(self) -> tuple[float, float]:
        if self._shake_t <= 0 or self._shake_duration <= 0:
            return 0.0, 0.0
        import random

        # Linear decay: full magnitude at start, zero at end.
        m = self._shake_mag * (self._shake_t / self._shake_duration)
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
