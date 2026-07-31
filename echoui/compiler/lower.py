"""Lower IR to target-specific representation."""

from __future__ import annotations

from typing import Any, Dict

from echoui.roles import role_tag


def lower_web(ir_bundle: Dict[str, Any]) -> Dict[str, Any]:
    root = ir_bundle["root"]
    return {
        "nodes": [_lower_node(root)],
        "app": ir_bundle["ir"]["app"],
        "click_map": ir_bundle.get("click_map", {}),
        "signals": ir_bundle.get("signals", {}),
        "reactive_bindings": ir_bundle.get("reactive_bindings", []),
        "actions": ir_bundle.get("actions", {}),
        "frame_handlers": ir_bundle.get("frame_handlers", []),
        "screen_handlers": ir_bundle.get("screen_handlers", {}),
        "key_handlers": ir_bundle.get("key_handlers", {}),
        "dom_handlers": ir_bundle.get("dom_handlers", []),
        "free_gpu": ir_bundle.get("free_gpu"),
        "frame_script": ir_bundle.get("frame_script"),
        "handlers": ir_bundle.get("handlers", {}),
        "static_nodes": list(ir_bundle.get("static_nodes", [])),
        "static": ir_bundle.get("static", False),
        "local_exec": ir_bundle.get("local_exec", False),
        "file_inputs": ir_bundle.get("file_inputs", []),
        "drop_targets": ir_bundle.get("drop_targets", []),
        "overlays": ir_bundle.get("overlays", []),
    }


def _lower_node(node: Any) -> Dict[str, Any]:
    props = dict(node.props)
    props.pop("_text_fn", None)
    props.pop("_handler_click", None)
    tag = role_tag(node.role)
    lowered: Dict[str, Any] = {
        "id": node.id,
        "tag": tag,
        "role": node.role,
        "props": props,
        "children": [_lower_node(c) for c in node.children],
        "bindings": node.bindings,
        "events": node.events,
    }
    if node.role == "canvas" and "commands" in props:
        lowered["canvas_commands"] = props["commands"]
    return lowered
