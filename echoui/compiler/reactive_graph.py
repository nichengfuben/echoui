"""Reactive binding analysis for web emit."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Tuple

from echoui.reactive import Computed
from echoui.state import get_signal_key_for_signal, serialize_signals


def trace_binding_deps(fn: Callable[[], Any]) -> Tuple[Any, List[str]]:
    comp = Computed(fn)
    value = comp.value
    deps: List[str] = []
    for sig in comp._deps:
        key = get_signal_key_for_signal(sig)
        if key:
            deps.append(key)
    return value, deps


def template_from_value(value: Any, deps: List[str], signals: Dict[str, Any]) -> str:
    text = str(value)
    template = text
    for i, key in enumerate(deps):
        part = str(signals.get(key, ""))
        if part and part in template:
            template = template.replace(part, "{" + str(i) + "}", 1)
    return template


def analyze_bindings(root: Any) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    signals = serialize_signals()
    bindings: List[Dict[str, Any]] = []
    for node in _walk(root):
        fn = node.props.get("_text_fn")
        if callable(fn):
            try:
                value, deps = trace_binding_deps(fn)
            except Exception:
                value, deps = fn(), []
            if not deps:
                bindings.append({"t": "text", "n": node.id, "tpl": str(value), "d": []})
            else:
                tpl = template_from_value(value, deps, signals)
                bindings.append({"t": "text", "n": node.id, "tpl": tpl, "d": deps})
        src_fn = node.props.get("_src_fn")
        if callable(src_fn):
            try:
                value, deps = trace_binding_deps(src_fn)
            except Exception:
                value, deps = str(src_fn()), []
            if deps:
                bindings.append(
                    {"t": "attr", "n": node.id, "a": "src", "v": "{" + deps[0] + "}", "d": deps}
                )
            else:
                bindings.append(
                    {"t": "attr", "n": node.id, "a": "src", "v": str(value), "d": []}
                )
        bg_fn = node.props.get("_bg_fn")
        if callable(bg_fn):
            try:
                _, deps = trace_binding_deps(bg_fn)
            except Exception:
                deps = []
            if deps:
                bindings.append(
                    {"t": "bg", "n": node.id, "v": "{" + deps[0] + "}", "d": deps}
                )
        for prop, binding in node.bindings.items():
            if not isinstance(binding, dict):
                continue
            btype = binding.get("type")
            if btype == "signal":
                key = binding.get("key")
                if key:
                    if prop in ("src", "href"):
                        bindings.append(
                            {"t": "attr", "n": node.id, "a": prop, "v": "{" + key + "}", "d": [key]}
                        )
                    elif prop == "background":
                        bindings.append(
                            {"t": "bg", "n": node.id, "v": "{" + key + "}", "d": [key]}
                        )
                    else:
                        bindings.append(
                            {"t": "text", "n": node.id, "tpl": "{" + key + "}", "d": [key]}
                        )
            elif btype == "fn":
                fn = binding.get("_fn")
                if fn is None:
                    continue
                try:
                    value, deps = trace_binding_deps(fn)
                except Exception:
                    continue
                if not deps:
                    bindings.append(
                        {"t": "text", "n": node.id, "tpl": str(value), "d": []}
                    )
                else:
                    tpl = template_from_value(value, deps, signals)
                    bindings.append({"t": "text", "n": node.id, "tpl": tpl, "d": deps})
        props = node.props
        for axis in ("x", "y"):
            val = props.get(axis)
            if isinstance(val, (int, float)):
                continue
            if callable(val):
                try:
                    _, deps = trace_binding_deps(val)
                except Exception:
                    continue
                if deps:
                    bindings.append(
                        {
                            "t": "style",
                            "n": node.id,
                            "p": "left" if axis == "x" else "top",
                            "v": "{" + deps[0] + "}",
                            "d": deps,
                        }
                    )
    return bindings, signals


def _walk(node: Any) -> Any:
    yield node
    for c in node.children:
        yield from _walk(c)
