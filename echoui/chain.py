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

    def fade_in(self, duration: float = 0.3) -> "MotionChain":
        sprite = self._sprite

        async def step() -> None:
            frames = max(1, int(duration * 60))
            for i in range(1, frames + 1):
                sprite.opacity = i / frames
                await asyncio.sleep(duration / frames)
            sprite.hidden = False

        self._steps.append(step)
        return self

    def fade_out(self, duration: float = 0.3) -> "MotionChain":
        sprite = self._sprite

        async def step() -> None:
            frames = max(1, int(duration * 60))
            for i in range(frames, -1, -1):
                sprite.opacity = i / frames if frames else 0
                await asyncio.sleep(duration / frames if frames else 0)
            sprite.hidden = True

        self._steps.append(step)
        return self

    def spin(self, degrees: float, duration: float) -> "MotionChain":
        sprite = self._sprite

        async def step() -> None:
            start = sprite.rotation
            frames = max(1, int(duration * 60))
            for i in range(1, frames + 1):
                sprite.rotation = start + degrees * (i / frames)
                await asyncio.sleep(duration / frames)

        self._steps.append(step)
        return self

    def parallel(self, other: "MotionChain") -> "MotionChain":
        async def step() -> None:
            await asyncio.gather(*[self._run_one(s) for s in self._steps], *[
                self._run_one(s) for s in other._steps
            ])

        self._steps = [step]
        return self

    def repeat(self, times: int) -> "MotionChain":
        steps = list(self._steps)

        async def step() -> None:
            for _ in range(times):
                for s in steps:
                    await self._run_one(s)

        self._steps = [step]
        return self

    def forever(self) -> "MotionChain":
        steps = list(self._steps)

        async def step() -> None:
            while True:
                for s in steps:
                    await self._run_one(s)

        self._steps = [step]
        return self

    def when(self, condition: Callable[[], bool], then: Callable[[Any], None]) -> Any:
        sprite = self._sprite
        else_fn: list[Callable[[Any], None] | None] = [None]

        async def step() -> None:
            if condition():
                then(sprite)
            elif else_fn[0] is not None:
                else_fn[0](sprite)

        self._steps.append(step)

        class Branch:
            _owner: "MotionChain"

            def otherwise(self, fn: Callable[[Any], None]) -> "MotionChain":
                else_fn[0] = fn
                return self._owner

        branch = Branch()
        branch._owner = self  # type: ignore[attr-defined]
        return branch

    def otherwise(self, fn: Callable[[Any], None]) -> "MotionChain":
        sprite = self._sprite

        async def step() -> None:
            fn(sprite)

        self._steps.append(step)
        return self

    def then_(self, other: "MotionChain | Callable[[], Any]") -> "MotionChain":
        if isinstance(other, MotionChain):
            self._steps.extend(other._steps)
        else:
            self._steps.append(other)
        return self

    async def _run_one(self, step: Callable[[], Any]) -> None:
        result = step()
        if asyncio.iscoroutine(result):
            await result

    def __await__(self) -> Any:
        return self._run().__await__()

    async def _run(self) -> None:
        for step in self._steps:
            await self._run_one(step)
