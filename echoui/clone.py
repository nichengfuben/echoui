"""Deep copy utilities for IR and sprites."""

from __future__ import annotations

from typing import Any, Dict, List

from echoui.sprite import IRNode, Sprite


def clone_ir(node: IRNode) -> IRNode:
    return IRNode(
        node.role,
        node_id=node.id,
        props=dict(node.props),
        children=[clone_ir(c) for c in node.children],
        events=dict(node.events),
        bindings=dict(node.bindings),
    )


def clone_sprite(sprite: Sprite) -> Sprite:
    cls = type(sprite)
    copy = cls.__new__(cls)
    for k, v in sprite.__dict__.items():
        setattr(copy, k, v)
    return copy


def clone_dict(d: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out[k] = clone_dict(v)
        elif isinstance(v, list):
            out[k] = clone_list(v)
        else:
            out[k] = v
    return out


def clone_list(items: List[Any]) -> List[Any]:
    return [clone_dict(i) if isinstance(i, dict) else i for i in items]
