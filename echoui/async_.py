"""Async helpers for non-blocking UI work (PLAN § async)."""

from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


async def run_in_executor(fn: Callable[[], T]) -> T:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, fn)


async def defer(coro: Awaitable[T]) -> T:
    return await coro
