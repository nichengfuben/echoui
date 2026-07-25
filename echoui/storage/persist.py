"""Persist Store fields to local/session backends."""

from __future__ import annotations

from typing import Any, Type, cast

from echoui.reactive import Signal
from echoui.state import Store, register_signal, signal_key
from echoui.storage import json_get, json_set, local, session


def persist_mixin(backend: str = "local") -> Type[Any]:
    """Return a mixin that loads/saves annotated Store fields."""

    store_backend = local() if backend == "local" else session()

    class PersistMixin:
        def _persist_key(self, field: str) -> str:
            return f"{self.__class__.__name__}.{field}"

        def _load_persisted(self) -> None:
            hints = getattr(self.__class__, "__annotations__", {})
            for name in hints:
                if name.startswith("_"):
                    continue
                val = json_get(store_backend, self._persist_key(name))
                if val is not None:
                    setattr(self, name, val)

        def __setattr__(self, name: str, value: Any) -> None:
            if name.startswith("_") or name == "_signals":
                object.__setattr__(self, name, value)
                return
            inst = cast(Store, self)
            sig = getattr(inst, "_signals", {}).get(name)
            if sig is not None:
                sig.set(value)
                object.__setattr__(self, name, value)
            else:
                object.__setattr__(self, name, value)
                if hasattr(inst, "_signals") and name in inst.__class__.__annotations__:
                    inst._signals[name] = Signal(value)
                    register_signal(signal_key(inst.__class__.__name__, name), inst._signals[name])
            if name in getattr(self.__class__, "__annotations__", {}):
                json_set(store_backend, self._persist_key(name), value)

    return PersistMixin
