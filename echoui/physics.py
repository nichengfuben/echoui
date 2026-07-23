"""Simple AABB physics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class AABB:
    x: float
    y: float
    w: float
    h: float

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h

    def overlaps(self, other: "AABB") -> bool:
        return not (
            self.right <= other.x
            or other.right <= self.x
            or self.bottom <= other.y
            or other.bottom <= self.y
        )

    def resolve(self, other: "AABB") -> Tuple[float, float]:
        if not self.overlaps(other):
            return 0.0, 0.0
        dx = min(self.right - other.x, other.right - self.x)
        dy = min(self.bottom - other.y, other.bottom - self.y)
        if dx < dy:
            return (-dx if self.x < other.x else dx), 0.0
        return 0.0, (-dy if self.y < other.y else dy)


@dataclass
class Body:
    aabb: AABB
    vx: float = 0
    vy: float = 0
    static: bool = False


class World:
    def __init__(self, gravity: Tuple[float, float] = (0, 980)) -> None:
        self.gravity = gravity
        self.bodies: List[Body] = []

    def add(self, body: Body) -> None:
        self.bodies.append(body)

    def step(self, dt: float) -> None:
        for b in self.bodies:
            if b.static:
                continue
            b.vy += self.gravity[1] * dt
            b.aabb.x += b.vx * dt
            b.aabb.y += b.vy * dt
        self._resolve_collisions()

    def _resolve_collisions(self) -> None:
        for i, a in enumerate(self.bodies):
            for b in self.bodies[i + 1:]:
                if a.static and b.static:
                    continue
                if a.aabb.overlaps(b.aabb):
                    dx, dy = a.aabb.resolve(b.aabb)
                    if not a.static:
                        a.aabb.x += dx
                        a.aabb.y += dy
                    if not b.static:
                        b.aabb.x -= dx
                        b.aabb.y -= dy
