"""Reactive dependency analysis."""

from __future__ import annotations

from typing import Any, Dict, List, Set

from echoui.compiler.emit_actions import compile_actions
from echoui.compiler.emit_frame import compile_frame_script
from echoui.compiler.emit_free_gpu import collect_free_gpu
from echoui.compiler.ui_collect import analyze_ui
from echoui.compiler.sss import normalize_screen_tree
from echoui.compiler.validate_local import validate_local_compile
from echoui.events import collect_frame_handlers, collect_key_handlers, collect_screen_handlers


def analyze(parsed: Dict[str, Any]) -> Dict[str, Any]:
    root = parsed["root"]
    normalize_screen_tree(root)
    reactive_bindings, signals, file_inputs, overlays = analyze_ui(root)
    parsed["signals"] = signals
    parsed["reactive_bindings"] = reactive_bindings
    parsed["file_inputs"] = file_inputs
    parsed["overlays"] = overlays
    parsed["actions"] = compile_actions(
        parsed.get("handlers", {}),
        app_initial=getattr(parsed.get("app"), "initial", "Home"),
    )
    parsed["frame_handlers"] = collect_frame_handlers(parsed.get("app"))
    parsed["screen_handlers"] = collect_screen_handlers(parsed.get("app"))
    parsed["key_handlers"] = collect_key_handlers(parsed.get("app"))
    parsed["dom_handlers"] = parsed.get("dom_handlers", [])
    parsed["free_gpu"] = collect_free_gpu(root, reactive_bindings)
    parsed["frame_script"] = compile_frame_script(
        parsed["frame_handlers"], parsed.get("handlers", {})
    )
    parsed["local_exec"] = True
    validate_local_compile(parsed)
    parsed["static_nodes"] = _mark_static(root, reactive_bindings)
    return parsed


def _mark_static(root: Any, bindings: List[Dict[str, Any]]) -> Set[str]:
    bound = {b["n"] for b in bindings}
    static: Set[str] = set()

    def walk(node: Any) -> None:
        if node.id not in bound and not node.bindings:
            static.add(node.id)
        for c in node.children:
            walk(c)

    walk(root)
    return static
