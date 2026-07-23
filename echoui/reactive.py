"""Fine-grained reactive primitives; no virtual DOM."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Callable, Generator, Generic, Set, TypeVar

T = TypeVar("T")

_batch_depth: ContextVar[int] = ContextVar("batch_depth", default=0)
_pending: ContextVar[Set[Callable[[], None]] | None] = ContextVar("pending", default=None)
_current_computed: ContextVar[Any] = ContextVar("current_computed", default=None)
_current_effect: ContextVar[Any] = ContextVar("current_effect", default=None)


def untrack(fn: Callable[[], T]) -> T:
    token_c = _current_computed.set(None)
    token_e = _current_effect.set(None)
    try:
        return fn()
    finally:
        _current_computed.reset(token_c)
        _current_effect.reset(token_e)


class Signal(Generic[T]):
    def __init__(self, value: T) -> None:
        self._value = value
        self._subs: set[Computed[Any] | Effect] = set()

    @property
    def value(self) -> T:
        cc = _current_computed.get()
        ce = _current_effect.get()
        if cc is not None:
            cc._deps.add(self)
            self._subs.add(cc)
        if ce is not None:
            ce._deps.add(self)
            self._subs.add(ce)
        return self._value

    def set(self, value: T) -> None:
        if value == self._value:
            return
        self._value = value
        self._notify()

    def update(self, fn: Callable[[T], T]) -> None:
        self.set(fn(self._value))

    def _notify(self) -> None:
        subs = list(self._subs)
        if _batch_depth.get() > 0:
            pending = _pending.get()
            if pending is None:
                pending = set()
                _pending.set(pending)
            for s in subs:
                pending.add(s._run)
            return
        for s in subs:
            s._run()


class Computed(Generic[T]):
    def __init__(self, fn: Callable[[], T]) -> None:
        self._fn = fn
        self._value: T | None = None
        self._deps: set[Signal[Any]] = set()
        self._dirty = True

    def _run(self) -> None:
        self._dirty = True
        for eff in list(_effects):
            if self in eff._deps or any(d in eff._deps for d in self._deps):
                eff._schedule()

    @property
    def value(self) -> T:
        if self._dirty:
            for d in list(self._deps):
                d._subs.discard(self)
            self._deps.clear()
            token = _current_computed.set(self)
            try:
                self._value = self._fn()
            finally:
                _current_computed.reset(token)
            self._dirty = False
        return self._value  # type: ignore[return-value]


class Effect:
    def __init__(self, fn: Callable[[], None]) -> None:
        self._fn = fn
        self._deps: set[Signal[Any] | Computed[Any]] = set()
        self._disposed = False
        _effects.add(self)
        self._execute()

    def _run(self) -> None:
        self._schedule()

    def _schedule(self) -> None:
        if _batch_depth.get() > 0:
            pending = _pending.get()
            if pending is None:
                pending = set()
                _pending.set(pending)
            pending.add(self._execute)
            return
        self._execute()

    def _execute(self) -> None:
        if self._disposed:
            return
        for d in list(self._deps):
            if isinstance(d, Signal):
                d._subs.discard(self)
        self._deps.clear()
        token = _current_effect.set(self)
        try:
            self._fn()
        finally:
            _current_effect.reset(token)

    def dispose(self) -> None:
        self._disposed = True
        _effects.discard(self)


_effects: set[Effect] = set()


def effect(fn: Callable[[], None]) -> Effect:
    return Effect(fn)


def watch(source: Callable[[], T], on_change: Callable[[T, T], None]) -> Effect:
    prev: dict[str, T] = {}

    def runner() -> None:
        val = source()
        old = prev.get("v")
        if old is not None and old != val:
            on_change(old, val)
        prev["v"] = val

    return effect(runner)


@contextmanager
def batch() -> Generator[None, None, None]:
    token = _batch_depth.set(_batch_depth.get() + 1)
    _pending.set(set())
    try:
        yield
    finally:
        _batch_depth.reset(token)
        pending = _pending.get() or set()
        _pending.set(None)
        for fn in pending:
            fn()


def computed(fn: Callable[[], T]) -> Computed[T]:
    return Computed(fn)


def computed_method(fn: Callable[..., T]) -> property:
    def getter(self: Any) -> T:
        cache_attr = f"_computed_{fn.__name__}"
        comp = getattr(self, cache_attr, None)
        if comp is None:
            comp = Computed(lambda: fn(self))
            setattr(self, cache_attr, comp)
        return comp.value

    return property(getter)
