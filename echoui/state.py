"""Singleton reactive Store."""

from __future__ import annotations

from typing import Any, ClassVar, Dict, Type, TypeVar

from echoui.reactive import Signal, batch

T = TypeVar("T", bound="Store")

_instances: Dict[Any, "Store"] = {}


class StoreMeta(type):
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls in _instances:
            return _instances[cls]
        inst = super().__call__(*args, **kwargs)
        _instances[cls] = inst
        inst._init_signals()
        return inst


class Store(metaclass=StoreMeta):
    """Singleton reactive store; field writes notify subscribers."""

    _signals: Dict[str, Signal[Any]]
    _initialized: ClassVar[bool] = False

    def _init_signals(self) -> None:
        self._signals = {}
        hints = getattr(self, "__annotations__", {})
        for name in hints:
            if name.startswith("_"):
                continue
            if hasattr(self, name):
                self._signals[name] = Signal(getattr(self, name))

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_") or name == "_signals":
            super().__setattr__(name, value)
            return
        sig = getattr(self, "_signals", {}).get(name)
        if sig is not None:
            sig.set(value)
            super().__setattr__(name, value)
            return
        super().__setattr__(name, value)
        if hasattr(self, "_signals") and name in self.__class__.__annotations__:
            self._signals[name] = Signal(value)

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("_"):
            return super().__getattribute__(name)
        signals = super().__getattribute__("_signals") if "_signals" in self.__dict__ else {}
        if name in signals:
            return signals[name].value
        return super().__getattribute__(name)

    @classmethod
    def reset_registry(cls) -> None:
        _instances.clear()


def batch_update(fn: Any) -> Any:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with batch():
            return fn(*args, **kwargs)

    return wrapper
