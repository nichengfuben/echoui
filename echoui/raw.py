"""Escape layer: raw HTML, JS, CSS, and DOM hooks."""

from __future__ import annotations

from typing import Any, Callable, Dict

from echoui.sprite import IRNode


def js(code: str, *, on_mount: Callable[[], None] | None = None) -> IRNode:
    return IRNode("raw", props={"kind": "js", "code": code, "_on_mount": on_mount})


def html(content: str) -> IRNode:
    return IRNode("raw", props={"kind": "html", "content": content})


def css(rules: str) -> IRNode:
    return IRNode("raw", props={"kind": "css", "rules": rules})


def dom(selector: str, *, bind: Dict[str, Callable[[], Any]] | None = None) -> IRNode:
    return IRNode("raw", props={"kind": "dom", "selector": selector, "bind": bind or {}})


def native(code: str) -> IRNode:
    from echoui.exceptions import UnsupportedCapability

    raise UnsupportedCapability("raw.native requires native backend")


def ffi(library: str, symbol: str, *args: Any) -> Any:
    from echoui.exceptions import UnsupportedCapability

    raise UnsupportedCapability("raw.ffi requires native backend")


def native_component(name: str, **props: Any) -> IRNode:
    return IRNode("native", props={"component": name, **props})


class RawBridge:
    """Runtime bridge for raw escape nodes."""

    def __init__(self) -> None:
        self._callbacks: Dict[str, Callable[[], None]] = {}
        self._values: Dict[str, Any] = {}

    def register(self, node_id: str, fn: Callable[[], None]) -> None:
        self._callbacks[node_id] = fn

    def mount(self, node_id: str) -> None:
        fn = self._callbacks.get(node_id)
        if fn:
            fn()

    def update(self, key: str, value: Any) -> None:
        self._values[key] = value

    def get(self, key: str) -> Any:
        return self._values.get(key)
