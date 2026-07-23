"""Unified event decorators."""

from __future__ import annotations

from typing import Any, Callable, Dict, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

_handlers: Dict[str, Dict[str, Callable[..., Any]]] = {}


def on(event: str, **filters: Any) -> Callable[[F], F]:
    def decorator(fn: F) -> F:
        key = _event_key(event, filters)
        cls_name = getattr(fn, "__qualname__", fn.__name__).split(".")[0]
        _handlers.setdefault(cls_name, {})[key] = fn
        if not hasattr(fn, "_echoui_events"):
            fn._echoui_events = []  # type: ignore[attr-defined]
        fn._echoui_events.append((event, filters))  # type: ignore[attr-defined]
        return fn

    return decorator


def _event_key(event: str, filters: Dict[str, Any]) -> str:
    if not filters:
        return event
    parts = [f"{k}={filters[k]}" for k in sorted(filters)]
    return f"{event}?{'&'.join(parts)}"


def get_handlers(cls: type) -> Dict[str, Callable[..., Any]]:
    return _handlers.get(cls.__name__, {})


def collect_click_handlers(ir_nodes: list, registry: Dict[str, Callable[..., Any]]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for node in _walk(ir_nodes):
        handler = node.props.get("_handler_click")
        if handler is not None:
            hid = f"h{id(handler)}"
            registry[hid] = handler
            mapping[node.id] = hid
    return mapping


def _walk(nodes: list) -> Any:
    for n in nodes:
        yield n
        yield from _walk(n.children)
