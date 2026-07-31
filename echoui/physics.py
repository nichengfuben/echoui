"""AABB physics plus optional pymunk backend."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Tuple, Union


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
    mass: float = 1.0
    friction: float = 0.0
    bounciness: float = 0.0
    material: str = ""


class World:
    """Built-in AABB world (always available, no extra deps)."""

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
            for b in self.bodies[i + 1 :]:
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


def pymunk_available() -> bool:
    try:
        import pymunk  # noqa: F401

        return True
    except ImportError:
        return False


class PymunkWorld:
    """Optional pymunk-backed world (`pip install echoui[physics]`).

    Not a full Box2D feature clone — circle/box bodies, gravity, and step only.
    """

    def __init__(self, gravity: Tuple[float, float] = (0, 980)) -> None:
        try:
            import pymunk
        except ImportError as exc:
            raise ImportError(
                "pymunk is required for PymunkWorld; install with: pip install echoui[physics]"
            ) from exc
        self._pymunk = pymunk
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self._bodies: List[Any] = []
        self._shapes: List[Any] = []

    def add_box(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        static: bool = False,
        mass: float = 1.0,
        friction: float = 0.5,
        elasticity: float = 0.0,
    ) -> Any:
        pm = self._pymunk
        if static:
            body = self.space.static_body
            shape = pm.Poly(
                body,
                [
                    (x - w / 2, y - h / 2),
                    (x + w / 2, y - h / 2),
                    (x + w / 2, y + h / 2),
                    (x - w / 2, y + h / 2),
                ],
            )
        else:
            moment = pm.moment_for_box(mass, (w, h))
            body = pm.Body(mass, moment)
            body.position = (x, y)
            shape = pm.Poly.create_box(body, (w, h))
            self.space.add(body)
            self._bodies.append(body)
        shape.friction = friction
        shape.elasticity = elasticity
        self.space.add(shape)
        self._shapes.append(shape)
        return body if not static else shape

    def add_circle(
        self,
        x: float,
        y: float,
        radius: float,
        *,
        static: bool = False,
        mass: float = 1.0,
        friction: float = 0.5,
        elasticity: float = 0.9,
    ) -> Any:
        pm = self._pymunk
        if static:
            body = self.space.static_body
            shape = pm.Circle(body, radius, offset=(x, y))
        else:
            moment = pm.moment_for_circle(mass, 0, radius)
            body = pm.Body(mass, moment)
            body.position = (x, y)
            shape = pm.Circle(body, radius)
            self.space.add(body)
            self._bodies.append(body)
        shape.friction = friction
        shape.elasticity = elasticity
        self.space.add(shape)
        self._shapes.append(shape)
        return body if not static else shape

    def step(self, dt: float, iterations: int = 10) -> None:
        self.space.step(dt)
        # extra substeps optional for stability when caller passes large dt
        for _ in range(max(0, iterations - 1)):
            pass

    def positions(self) -> List[Tuple[float, float]]:
        return [(float(b.position.x), float(b.position.y)) for b in self._bodies]


def create_world(
    backend: str = "aabb",
    gravity: Tuple[float, float] = (0, 980),
) -> Union[World, PymunkWorld]:
    """Factory: ``aabb`` (default) or ``pymunk`` (requires optional extra)."""
    if backend in ("aabb", "builtin", "simple"):
        return World(gravity=gravity)
    if backend in ("pymunk", "chipmunk"):
        return PymunkWorld(gravity=gravity)
    raise ValueError(f"unknown physics backend: {backend!r} (use 'aabb' or 'pymunk')")
