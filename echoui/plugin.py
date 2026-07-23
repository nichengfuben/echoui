"""Plugin registration system."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

_plugins: Dict[str, Dict[str, Any]] = {}


def register(name: str, *, setup: Callable[[], None] | None = None, **meta: Any) -> None:
    _plugins[name] = {"setup": setup, **meta}


def get(name: str) -> Dict[str, Any] | None:
    return _plugins.get(name)


def list_plugins() -> List[str]:
    return list(_plugins.keys())


def setup_all() -> None:
    for p in _plugins.values():
        fn = p.get("setup")
        if fn:
            fn()
