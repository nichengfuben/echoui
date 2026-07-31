"""Collect file inputs, drop targets, overlays, and extended reactive bindings."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from echoui.compiler.reactive_graph import analyze_bindings, trace_binding_deps

# bindings, signals, file_inputs, overlays, drop_targets
AnalyzeUIResult = Tuple[
    List[Dict[str, Any]],
    Dict[str, Any],
    List[Dict[str, Any]],
    List[Dict[str, Any]],
    List[Dict[str, Any]],
]


def analyze_ui(root: Any) -> AnalyzeUIResult:
    bindings, signals = analyze_bindings(root)
    file_inputs: List[Dict[str, Any]] = []
    overlays: List[Dict[str, Any]] = []
    drop_targets: List[Dict[str, Any]] = []
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
        drop_entry = _collect_drop_target(node)
        if drop_entry is not None:
            drop_targets.append(drop_entry)
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
    return bindings, signals, file_inputs, overlays, drop_targets


def _collect_drop_target(node: Any) -> Dict[str, Any] | None:
    """Build client_cfg drop_targets entry for wireDropTargets (ui.js)."""
    props = node.props
    drop_handler = props.get("_handler_drop")
    drop_signal = props.get("_drop_signal") or props.get("drop_signal")
    file_signal = props.get("_drop_file_signal") or props.get("drop_file_signal")
    is_drop_role = node.role == "drop_target" or props.get("drop_target") is True
    if not (drop_handler or drop_signal or file_signal or is_drop_role):
        return None
    entry: Dict[str, Any] = {"node": node.id}
    if drop_signal:
        entry["signal"] = drop_signal
    if file_signal:
        entry["fileSignal"] = file_signal
    if drop_handler is not None:
        entry["handler"] = f"h{id(drop_handler)}"
    effect = props.get("drop_effect") or props.get("effect")
    if effect:
        entry["effect"] = effect
    upload = props.get("upload_url") or props.get("uploadUrl")
    if upload:
        entry["uploadUrl"] = upload
    field = props.get("field") or props.get("name")
    if field:
        entry["field"] = field
    preview_id = props.get("preview_id") or props.get("previewNode")
    if preview_id:
        entry["preview"] = True
        entry["previewNode"] = preview_id
    return entry


def _walk(node: Any):
    yield node
    for c in node.children:
        yield from _walk(c)
