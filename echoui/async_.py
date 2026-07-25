"""Async helpers for non-blocking UI work (PLAN §15)."""

from __future__ import annotations

import asyncio
import time
from typing import Any, Awaitable, Callable, Coroutine, TypeVar, cast

T = TypeVar("T")


async def run_in_executor(fn: Callable[[], T]) -> T:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, fn)


async def defer(coro: Awaitable[T]) -> T:
    return await coro


async def gather(*coros: Awaitable[T]) -> list[T]:
    return list(await asyncio.gather(*coros))


async def race(*coros: Awaitable[T]) -> T:
    tasks: list[asyncio.Task[T]] = [
        asyncio.create_task(cast(Coroutine[Any, Any, T], c)) for c in coros
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    return done.pop().result()


async def timeout(coro: Awaitable[T], seconds: float) -> T:
    return await asyncio.wait_for(coro, timeout=seconds)


def debounce(fn: Callable[..., T], ms: int) -> Callable[..., None]:
    timer: list[float] = [0.0]

    def wrapped(*args: object, **kwargs: object) -> None:
        timer[0] = time.monotonic() + ms / 1000.0
        due = timer[0]

        def fire() -> None:
            if time.monotonic() >= due:
                fn(*args, **kwargs)

        asyncio.get_event_loop().call_later(ms / 1000.0, fire)

    return wrapped


def throttle(fn: Callable[..., T], ms: int) -> Callable[..., T | None]:
    last: list[float] = [0.0]

    def wrapped(*args: object, **kwargs: object) -> T | None:
        now = time.monotonic()
        if now - last[0] >= ms / 1000.0:
            last[0] = now
            return fn(*args, **kwargs)
        return None

    return wrapped


async def retry(fn: Callable[[], Awaitable[T]], *, attempts: int = 3, delay: float = 0.2) -> T:
    err: Exception | None = None
    for _ in range(attempts):
        try:
            return await fn()
        except Exception as exc:
            err = exc
            await asyncio.sleep(delay)
    assert err is not None
    raise err
