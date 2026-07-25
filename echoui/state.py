"""Singleton reactive Store."""

from __future__ import annotations

from typing import Any, ClassVar, Dict, TypeVar

from echoui.reactive import Signal, batch

T = TypeVar("T", bound="Store")

_instances: Dict[Any, "Store"] = {}
_SIGNAL_REGISTRY: Dict[str, Signal[Any]] = {}
_STORE_NAMES: Dict[Any, str] = {}


def signal_key(class_name: str, field: str) -> str:
    return f"{class_name}.{field}"


def register_signal(key: str, sig: Signal[Any]) -> None:
    _SIGNAL_REGISTRY[key] = sig


def get_signal_key_for_signal(sig: Signal[Any]) -> str | None:
    for key, registered in _SIGNAL_REGISTRY.items():
        if registered is sig:
            return key
    return None


def serialize_signals() -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for inst in _instances.values():
        cls_name = inst.__class__.__name__
        signals = getattr(inst, "_signals", {})
        for name, sig in signals.items():
            key = signal_key(cls_name, name)
            out[key] = sig.value
            register_signal(key, sig)
    for key, sig in _SIGNAL_REGISTRY.items():
        if key not in out:
            out[key] = sig.value
    return out


def reset_signal_registry() -> None:
    _SIGNAL_REGISTRY.clear()
    _STORE_NAMES.clear()


class StoreMeta(type):
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls in _instances:
            return _instances[cls]
        inst = super().__call__(*args, **kwargs)
        _instances[cls] = inst
        _STORE_NAMES[inst] = cls.__name__
        inst._init_signals()
        return inst


class Store(metaclass=StoreMeta):
    """Singleton reactive store; field writes notify subscribers."""

    _signals: Dict[str, Signal[Any]]
    _initialized: ClassVar[bool] = False

    def _init_signals(self) -> None:
        self._signals = {}
        cls_name = self.__class__.__name__
        hints = getattr(self.__class__, "__annotations__", {})
        for name in hints:
            if name.startswith("_"):
                continue
            if hasattr(self, name):
                sig = Signal(getattr(self, name))
                self._signals[name] = sig
                register_signal(signal_key(cls_name, name), sig)

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
            register_signal(signal_key(self.__class__.__name__, name), self._signals[name])

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
        reset_signal_registry()


def batch_update(fn: Any) -> Any:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        with batch():
            return fn(*args, **kwargs)

    return wrapper
