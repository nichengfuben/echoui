"""Build IR from App via runtime introspection."""

from __future__ import annotations

from typing import Any, Dict, List

from echoui.events import collect_click_handlers
from echoui.sprite import IRNode


def compile_app(app: Any) -> Dict[str, Any]:
    return parse_app(app)


def parse_app(app: Any) -> Dict[str, Any]:
    ir = app.build_ir()
    handlers: Dict[str, Any] = {}
    screen_dict = ir["screen"]
    root = _dict_to_node(screen_dict)
    clicks = collect_click_handlers([root], handlers)
    return {
        "ir": ir,
        "root": root,
        "handlers": handlers,
        "click_map": clicks,
    }


def _dict_to_node(d: Dict[str, Any]) -> IRNode:
    return IRNode(
        d["role"],
        node_id=d["id"],
        props=d.get("props", {}),
        children=[_dict_to_node(c) for c in d.get("children", [])],
        events=d.get("events", {}),
        bindings=d.get("bindings", {}),
    )


def walk_nodes(node: IRNode) -> List[IRNode]:
    out = [node]
    for c in node.children:
        out.extend(walk_nodes(c))
    return out
