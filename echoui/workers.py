"""Web Worker bridge for off-main-thread tasks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, TypeVar

T = TypeVar("T")

_workers: Dict[str, Callable[..., Any]] = {}


@dataclass
class WorkerBridge:
    """Compile-time worker registration; emitted into web runtime."""

    name: str
    script: str
    handlers: Dict[str, Callable[..., Any]] = field(default_factory=dict)

    def on_message(self, kind: str, handler: Callable[..., Any]) -> "WorkerBridge":
        self.handlers[kind] = handler
        return self


def worker(fn: Callable[..., T]) -> Callable[..., T]:
    _workers[fn.__name__] = fn
    return fn


def shared_worker(fn: Callable[..., T]) -> Callable[..., T]:
    fn.__echoui_shared_worker__ = True  # type: ignore[attr-defined]
    return worker(fn)
