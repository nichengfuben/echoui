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
    }


def _lower_node(node: Any) -> Dict[str, Any]:
    tag = role_tag(node.role)
    return {
        "id": node.id,
        "tag": tag,
        "role": node.role,
        "props": node.props,
        "children": [_lower_node(c) for c in node.children],
        "bindings": node.bindings,
    }
