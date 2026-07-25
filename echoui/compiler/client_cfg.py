"""Build unified client configuration payload."""

from __future__ import annotations

import json
from typing import Any, Dict


def build_client_cfg(lowered: Dict[str, Any]) -> Dict[str, Any]:
    clicks = []
    actions = dict(lowered.get("actions", {}))
    click_map = lowered.get("click_map", {})
    for node_id, hid in click_map.items():
        entry: Dict[str, Any] = {"node": node_id, "action": hid}
        if hid in actions:
            entry["handler"] = hid
        clicks.append(entry)

    keymap: Dict[str, str] = dict(lowered.get("key_handlers", {}))
    for hid, action in actions.items():
        combo = action.get("key")
        if combo:
            keymap[combo] = hid

    frame_script = lowered.get("frame_script")
    gpu = lowered.get("free_gpu")
    if gpu:
        gpu = _normalize_gpu(gpu)

    return {
        "app": lowered.get("app", {}),
        "signals": lowered.get("signals", {}),
        "bindings": lowered.get("reactive_bindings", []),
        "actions": actions,
        "clicks": clicks,
        "dom": lowered.get("dom_handlers", []),
        "frames": bool(lowered.get("frame_handlers")),
        "frame_local": bool(frame_script),
        "frame_script": frame_script,
        "gpu": gpu,
        "static": lowered.get("static", False),
        "local_exec": lowered.get("local_exec", False),
        "keymap": keymap,
        "click_map": click_map,
        "hydrate": True,
        "file_inputs": lowered.get("file_inputs", []),
        "overlays": lowered.get("overlays", []),
    }


def _normalize_gpu(gpu: Dict[str, Any]) -> Dict[str, Any]:
    nodes = []
    for n in gpu.get("nodes", []):
        nodes.append(
            {
                "x": n.get("sig_x") or n.get("x"),
                "y": n.get("sig_y") or n.get("y"),
                "w": n.get("w"),
                "h": n.get("h"),
                "c": n.get("c", "#888"),
            }
        )
    return {
        "canvas": gpu.get("canvas"),
        "width": gpu.get("width", 640),
        "height": gpu.get("height", 360),
        "backend": gpu.get("backend", "canvas2d"),
        "nodes": nodes,
    }


def cfg_json(lowered: Dict[str, Any]) -> str:
    return json.dumps(build_client_cfg(lowered), ensure_ascii=False)
