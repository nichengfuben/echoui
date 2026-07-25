"""Unified event decorators and dispatch helpers."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

_handlers: Dict[str, Dict[str, Callable[..., Any]]] = {}

DOM_NODE_EVENTS = frozenset(
    {
        "click",
        "dblclick",
        "hover_enter",
        "hover_leave",
        "focus",
        "blur",
        "wheel",
        "contextmenu",
        "drag",
        "drop",
    }
)

DOM_TO_BROWSER = {
    "hover_enter": "mouseenter",
    "hover_leave": "mouseleave",
    "drag": "mousedown",
}


@dataclass
class Event:
    """Normalized event payload (PLAN §10)."""

    type: str
    x: float = 0
    y: float = 0
    dy: float = 0
    key: str = ""
    data: Any = None
    files: List[Any] = field(default_factory=list)
    dt: float = 0
    timestamp: float = field(default_factory=time.time)
    _prevented: bool = False

    def prevent_default(self) -> None:
        self._prevented = True


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
    for item in collect_dom_handlers(ir_nodes, registry):
        if item["type"] == "click":
            mapping[item["node"]] = item["handler"]
    return mapping


def collect_dom_handlers(
    ir_nodes: list, registry: Dict[str, Callable[..., Any]]
) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for node in _walk(ir_nodes):
        for ev in DOM_NODE_EVENTS:
            handler = node.props.get(f"_handler_{ev}")
            if handler is None:
                continue
            hid = f"h{id(handler)}"
            registry[hid] = handler
            out.append({"node": node.id, "type": ev, "handler": hid})
    return out


def attach_class_handlers(node: Any, cls: type) -> None:
    """Bind @on DOM handlers from a Screen/Sprite class onto an IR node."""
    for event_key, fn in get_handlers(cls).items():
        base = event_key.split("?", 1)[0]
        if base not in DOM_NODE_EVENTS:
            continue
        node.props[f"_handler_{base}"] = fn
        node.events[base] = f"h{id(fn)}"


def collect_frame_handlers(app: Any) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    if app is None:
        return out
    for name, screen_cls in app.screens.items():
        handlers = get_handlers(screen_cls)
        fn = handlers.get("frame")
        if fn:
            out.append({"screen": name, "handler": f"h{id(fn)}", "cls": screen_cls.__name__})
        for sprite_cls in _sprite_classes_from_module(screen_cls):
            sh = get_handlers(sprite_cls)
            sfn = sh.get("frame")
            if sfn:
                out.append(
                    {
                        "screen": name,
                        "handler": f"h{id(sfn)}",
                        "cls": sprite_cls.__name__,
                    }
                )
    return out


def collect_screen_handlers(app: Any) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if app is None:
        return mapping
    for name, screen_cls in app.screens.items():
        handlers = get_handlers(screen_cls)
        for key in ("screen_enter", "screen_leave"):
            fn = handlers.get(key)
            if fn:
                mapping[f"{name}:{key}"] = f"h{id(fn)}"
    return mapping


def register_frame_handlers(app: Any, registry: Dict[str, Callable[..., Any]]) -> None:
    for item in collect_frame_handlers(app):
        hid = item["handler"]
        cls_name = item["cls"]
        screen_name = item["screen"]
        screen_cls = app.screens.get(screen_name)
        if screen_cls and screen_cls.__name__ == cls_name:
            fn = get_handlers(screen_cls).get("frame")
        else:
            fn = _handlers.get(cls_name, {}).get("frame")
        if fn:
            registry[hid] = fn


def register_app_handlers(app: Any, registry: Dict[str, Callable[..., Any]]) -> None:
    """Register @on frame/keydown handlers from screens and sprites."""
    register_frame_handlers(app, registry)
    if app is None:
        return
    for screen_cls in app.screens.values():
        for event_key, fn in get_handlers(screen_cls).items():
            if event_key.startswith("keydown") or event_key.startswith("key"):
                registry[f"h{id(fn)}"] = fn
        for sprite_cls in _sprite_classes_from_module(screen_cls):
            for event_key, fn in get_handlers(sprite_cls).items():
                if event_key.startswith("keydown") or event_key.startswith("key"):
                    registry[f"h{id(fn)}"] = fn


def collect_key_handlers(app: Any) -> Dict[str, str]:
    """Map keyboard code -> handler id for @on('keydown', key=...)."""
    mapping: Dict[str, str] = {}
    if app is None:
        return mapping
    for screen_cls in app.screens.values():
        _add_key_handlers(screen_cls, mapping)
        for sprite_cls in _sprite_classes_from_module(screen_cls):
            _add_key_handlers(sprite_cls, mapping)
    return mapping


def _add_key_handlers(cls: type, mapping: Dict[str, str]) -> None:
    for event_key, fn in get_handlers(cls).items():
        if not event_key.startswith("keydown"):
            continue
        code = _key_filter_code(event_key)
        if code:
            mapping[code] = f"h{id(fn)}"


def _key_filter_code(event_key: str) -> str:
    if "key=" in event_key:
        return event_key.split("key=", 1)[1].split("&", 1)[0]
    return ""


def dispatch_dom(
    registry: Dict[str, Callable[..., Any]],
    dom_handlers: List[Dict[str, str]],
    node_id: str,
    event_type: str,
    *,
    app: Any = None,
    instance: Any = None,
) -> bool:
    """Dispatch a DOM event to a registered @on handler. Returns True if handled."""
    for item in dom_handlers:
        if item["node"] != node_id or item["type"] != event_type:
            continue
        fn = registry.get(item["handler"])
        if not fn:
            continue
        inst = instance if instance is not None else _handler_instance(app, fn)
        _call_handler(fn, inst, Event(type=event_type))
        return True
    return False


def _handler_instance(app: Any, fn: Callable[..., Any]) -> Any:
    if app is None:
        return None
    qual = getattr(fn, "__qualname__", fn.__name__).split(".")[0]
    current = getattr(app, "_current", app.initial)
    screen_cls = app.screens.get(current)
    if screen_cls and screen_cls.__name__ == qual:
        return screen_cls()
    if screen_cls:
        screen = screen_cls()
        built = screen.build()
        by_class = _sprite_instances(built)
        for inst in by_class.get(qual, []):
            return inst
    return None


def dispatch_key(app: Any, registry: Dict[str, Callable[..., Any]], code: str) -> None:
    mapping = collect_key_handlers(app)
    hid = mapping.get(code)
    if hid and hid in registry:
        ev = Event(type="keydown", key=code)
        fn = registry[hid]
        _call_handler(fn, None, ev)


def dispatch_frame(app: Any, registry: Dict[str, Callable[..., Any]], dt: float = 1 / 60) -> None:
    ev = Event(type="frame", dt=dt)
    current = getattr(app, "_current", app.initial)
    screen_cls = app.screens[current]
    screen = screen_cls()
    built = screen.build()
    by_class = _sprite_instances(built)
    for item in collect_frame_handlers(app):
        fn = registry.get(item["handler"])
        if not fn:
            continue
        cls = item["cls"]
        if screen_cls.__name__ == cls:
            _call_handler(fn, screen, ev)
            continue
        for inst in by_class.get(cls, []):
            _call_handler(fn, inst, ev)


def _sprite_instances(obj: Any) -> Dict[str, List[Any]]:
    from echoui.sprite import IRNode, Sprite

    out: Dict[str, List[Any]] = {}

    def walk(item: Any) -> None:
        if isinstance(item, Sprite):
            out.setdefault(item.__class__.__name__, []).append(item)
        if isinstance(item, IRNode):
            for child in item.children:
                walk(child)
        elif isinstance(item, (list, tuple)):
            for child in item:
                walk(child)

    walk(obj)
    return out


def _call_handler(fn: Callable[..., Any], instance: Any, event: Event) -> None:
    import inspect

    try:
        params = list(inspect.signature(fn).parameters.values())
        if instance is not None and len(params) >= 2:
            second = params[1].name
            if second == "dt":
                fn(instance, event.dt)
            else:
                fn(instance, event)
        elif len(params) == 1:
            first = params[0].name
            if first == "dt":
                fn(event.dt)
            elif first in ("event", "e"):
                fn(event)
            else:
                fn(event)
        else:
            fn()
    except TypeError:
        if instance is not None:
            try:
                fn(instance, event.dt)
            except TypeError:
                fn(instance)
        else:
            fn()


def _sprite_classes_from_module(screen_cls: type) -> List[type]:
    import sys

    mod = sys.modules.get(screen_cls.__module__)
    if mod is None:
        return []
    from echoui.sprite import Sprite

    return [obj for obj in vars(mod).values() if isinstance(obj, type) and issubclass(obj, Sprite)]


def _walk(nodes: list) -> Any:
    for n in nodes:
        yield n
        yield from _walk(n.children)
