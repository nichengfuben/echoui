"""Build IR from App via runtime introspection."""

from __future__ import annotations

from typing import Any, Dict, List

from echoui.events import collect_click_handlers, collect_dom_handlers, register_app_handlers
from echoui.sprite import IRNode


def compile_app(app: Any) -> Dict[str, Any]:
    return parse_app(app)


def parse_app(app: Any) -> Dict[str, Any]:
    ir = app.build_ir()
    handlers: Dict[str, Any] = {}
    screen_dict = ir["screen"]
    root = _dict_to_node(screen_dict)
    clicks = collect_click_handlers([root], handlers)
    register_app_handlers(app, handlers)
    dom_handlers = collect_dom_handlers([root], handlers)
    return {
        "ir": ir,
        "root": root,
        "handlers": handlers,
        "click_map": clicks,
        "dom_handlers": dom_handlers,
        "app": app,
    }


def collect_all_handlers(app: Any) -> tuple[Dict[str, Any], Dict[str, str], list[Dict[str, str]]]:
    """Merge click/DOM/@on handlers from every screen (multi-screen build validation)."""
    handlers: Dict[str, Any] = {}
    click_map: Dict[str, str] = {}
    dom_handlers: list[Dict[str, str]] = []
    saved = app._current
    for name in app.screens:
        app.switch_screen(name)
        sub = parse_app(app)
        handlers.update(sub["handlers"])
        click_map.update(sub["click_map"])
        dom_handlers.extend(sub["dom_handlers"])
    app.switch_screen(saved)
    return handlers, click_map, dom_handlers


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
