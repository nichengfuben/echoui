"""Awaitable motion chains for sprites."""

from __future__ import annotations

import asyncio
from typing import Any, Callable, List


class MotionChain:
    def __init__(self, sprite: Any) -> None:
        self._sprite = sprite
        self._steps: List[Callable[[], Any]] = []

    def glide_to(self, x: float, y: float, duration: float) -> "MotionChain":
        sprite = self._sprite

        async def step() -> None:
            start_x, start_y = sprite.x, sprite.y
            frames = max(1, int(duration * 60))
            for i in range(1, frames + 1):
                t = i / frames
                sprite.x = start_x + (x - start_x) * t
                sprite.y = start_y + (y - start_y) * t
                await asyncio.sleep(duration / frames)

        self._steps.append(step)
        return self

    def then_(self, other: "MotionChain | Callable[[], Any]") -> "MotionChain":
        if isinstance(other, MotionChain):
            self._steps.extend(other._steps)
        else:
            self._steps.append(other)
        return self

    def __await__(self) -> Any:
        return self._run().__await__()

    async def _run(self) -> None:
        for step in self._steps:
            result = step()
            if asyncio.iscoroutine(result):
                await result
