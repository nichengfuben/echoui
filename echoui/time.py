"""Time and frame clock helpers (PLAN § time)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FrameClock:
    fps: float = 60.0
    _elapsed: float = 0.0

    @property
    def dt(self) -> float:
        return 1.0 / self.fps if self.fps else 0.0

    def tick(self, dt: float | None = None) -> float:
        step = self.dt if dt is None else dt
        self._elapsed += step
        return step
