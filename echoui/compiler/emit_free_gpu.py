"""Analyze free-mode stage nodes for GPU batched canvas rendering."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def collect_free_gpu(root: Any, bindings: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    stage = _find_free_stage(root)
    if stage is None:
        return None
    props = stage.props
    width = int(props.get("width", 640))
    height = int(props.get("height", 360))
    bound_xy = _binding_map(bindings)
    nodes: List[Dict[str, Any]] = []
    for child in stage.children:
        entry = _gpu_node(child, bound_xy)
        if entry:
            nodes.append(entry)
    if not nodes:
        return None
    backend = props.get("gpu_backend", "canvas2d")
    return {
        "canvas": f"gpu-{stage.id}",
        "stage": stage.id,
        "width": width,
        "height": height,
        "backend": backend,
        "nodes": nodes,
    }


def _find_free_stage(node: Any) -> Any:
    if node.role == "stage" and node.props.get("layout") == "free":
        return node
    for child in node.children:
        found = _find_free_stage(child)
        if found:
            return found
    return None


def _binding_map(bindings: List[Dict[str, Any]]) -> Dict[str, Dict[str, str]]:
    out: Dict[str, Dict[str, str]] = {}
    for b in bindings:
        if b.get("t") != "style":
            continue
        nid = b.get("n", "")
        prop = b.get("p", "")
        sig = b.get("v", "")
        if isinstance(sig, str) and sig.startswith("{") and sig.endswith("}"):
            out.setdefault(nid, {})[prop] = sig[1:-1]
    return out


def _gpu_node(node: Any, bound_xy: Dict[str, Dict[str, str]]) -> Optional[Dict[str, Any]]:
    props = node.props
    if props.get("layout") == "free" and node.role == "stage":
        return None
    w = props.get("width")
    h = props.get("height")
    if not w or not h:
        return None
    xy = bound_xy.get(node.id, {})
    x = xy.get("left")
    y = xy.get("top")
    if not x and isinstance(props.get("x"), (int, float)):
        x = str(props["x"])
    if not y and isinstance(props.get("y"), (int, float)):
        y = str(props["y"])
    if x is None or y is None:
        return None
    return {
        "id": node.id,
        "x": x if x.startswith("Runner") or "." in x else x,
        "y": y if y.startswith("Runner") or "." in y else y,
        "w": w,
        "h": h,
        "c": props.get("background", "#888"),
        "sig_x": x if "." in str(x) else None,
        "sig_y": y if "." in str(y) else None,
    }
