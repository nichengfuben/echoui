"""Web Worker bridge and local thread-pool execution."""

from __future__ import annotations

import concurrent.futures
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Dict, TypeVar

T = TypeVar("T")

_workers: Dict[str, Callable[..., Any]] = {}
_pool: concurrent.futures.ThreadPoolExecutor | None = None


def _get_pool() -> concurrent.futures.ThreadPoolExecutor:
    global _pool
    if _pool is None:
        _pool = concurrent.futures.ThreadPoolExecutor(max_workers=4, thread_name_prefix="echoui-worker")
    return _pool


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
    """Register ``fn`` and run it on a thread pool when called as async-friendly submit."""

    _workers[fn.__name__] = fn

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        return fn(*args, **kwargs)

    def submit(*args: Any, **kwargs: Any) -> concurrent.futures.Future[T]:
        return _get_pool().submit(fn, *args, **kwargs)

    wrapper.submit = submit  # type: ignore[attr-defined]
    wrapper.__echoui_worker__ = True  # type: ignore[attr-defined]
    return wrapper  # type: ignore[return-value]


def shared_worker(fn: Callable[..., T]) -> Callable[..., T]:
    fn.__echoui_shared_worker__ = True  # type: ignore[attr-defined]
    return worker(fn)


def run_in_worker(fn: Callable[..., T], *args: Any, **kwargs: Any) -> concurrent.futures.Future[T]:
    return _get_pool().submit(fn, *args, **kwargs)


def registered_workers() -> Dict[str, Callable[..., Any]]:
    return dict(_workers)
