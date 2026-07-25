"""Deferred task scheduling."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class TaskQueue:
    _pending: List[Callable[[], None]] = field(default_factory=list)

    def defer(self, fn: Callable[[], None]) -> None:
        self._pending.append(fn)

    def flush(self) -> int:
        count = len(self._pending)
        while self._pending:
            self._pending.pop(0)()
        return count


_queue = TaskQueue()


def background(fn: Callable[[], None]) -> None:
    _queue.defer(fn)


def schedule(fn: Callable[[], None], *, cron: str = "") -> None:
    _queue.defer(fn)


def flush() -> int:
    return _queue.flush()
