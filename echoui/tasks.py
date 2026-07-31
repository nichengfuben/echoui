"""Deferred task scheduling with optional cron expression parse (minute field)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional


@dataclass
class ScheduledTask:
    fn: Callable[[], None]
    cron: str = ""
    # Simple support: "*/N * * * *" every N minutes from process start ticks
    every_minutes: Optional[int] = None
    ticks: int = 0


@dataclass
class TaskQueue:
    _pending: List[Callable[[], None]] = field(default_factory=list)
    _scheduled: List[ScheduledTask] = field(default_factory=list)

    def defer(self, fn: Callable[[], None]) -> None:
        self._pending.append(fn)

    def schedule(self, fn: Callable[[], None], *, cron: str = "") -> None:
        every = _parse_every_minutes(cron)
        if every is None and not cron:
            self._pending.append(fn)
            return
        self._scheduled.append(ScheduledTask(fn=fn, cron=cron, every_minutes=every or 1))

    def flush(self) -> int:
        count = len(self._pending)
        while self._pending:
            self._pending.pop(0)()
        return count

    def tick_minute(self) -> int:
        """Advance one minute of scheduled tasks (for tests / host loop)."""
        ran = 0
        for task in self._scheduled:
            task.ticks += 1
            interval = task.every_minutes or 1
            if task.ticks % interval == 0:
                task.fn()
                ran += 1
        return ran


def _parse_every_minutes(cron: str) -> Optional[int]:
    if not cron:
        return None
    parts = cron.split()
    if len(parts) < 1:
        return None
    minute = parts[0]
    if minute.startswith("*/"):
        try:
            return max(1, int(minute[2:]))
        except ValueError:
            return 1
    if minute == "*":
        return 1
    return 1


_queue = TaskQueue()


def background(fn: Callable[[], None]) -> None:
    _queue.defer(fn)


def schedule(fn: Callable[[], None], *, cron: str = "") -> None:
    _queue.schedule(fn, cron=cron)


def flush() -> int:
    return _queue.flush()


def tick_minute() -> int:
    return _queue.tick_minute()
