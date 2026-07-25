"""Collect file inputs, overlays, and extended reactive bindings."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from echoui.compiler.reactive_graph import analyze_bindings, trace_binding_deps


def analyze_ui(root: Any) -> Tuple[List[Dict[str, Any]], Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
    bindings, signals = analyze_bindings(root)
    file_inputs: List[Dict[str, Any]] = []
    overlays: List[Dict[str, Any]] = []
    for node in _walk(root):
        props = node.props
        if node.role == "file_input":
            sig = props.get("_file_signal") or props.get("signal")
            if sig:
                file_inputs.append(
                    {
                        "node": node.id,
                        "signal": sig,
                        "previewNode": props.get("preview_id"),
                        "accept": props.get("accept", "*/*"),
                    }
                )
        overlay_kind = props.get("role")
        if overlay_kind in ("modal", "drawer", "sheet"):
            open_sig = props.get("_open_signal")
            if open_sig:
                overlays.append({"node": node.id, "openSignal": open_sig})
        fn = props.get("_src_fn")
        if callable(fn) and node.role == "image":
            try:
                _, deps = trace_binding_deps(fn)
            except Exception:
                deps = []
            if deps:
                bindings.append({"t": "attr", "n": node.id, "a": "src", "v": "{" + deps[0] + "}", "d": deps})
        fn_bg = props.get("_bg_fn")
        if callable(fn_bg):
            try:
                _, deps = trace_binding_deps(fn_bg)
            except Exception:
                deps = []
            if deps:
                bindings.append({"t": "bg", "n": node.id, "v": "{" + deps[0] + "}", "d": deps})
    return bindings, signals, file_inputs, overlays


def _walk(node: Any):
    yield node
    for c in node.children:
        yield from _walk(c)
