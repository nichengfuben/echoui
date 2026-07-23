"""Test harness: mount, fire, tick, snapshot."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from echoui.compiler.parser import parse_app
from echoui.reactive import batch
from echoui.sprite import IRNode


@dataclass
class TestNode:
    id: str
    role: str
    tag: str
    props: Dict[str, Any]
    children: List["TestNode"] = field(default_factory=list)
    text: str = ""


@dataclass
class MountedApp:
    app: Any
    root: TestNode
    handlers: Dict[str, Callable[..., Any]]
    click_map: Dict[str, str]
    _ticks: int = 0

    def fire(self, node_id: str, event: str = "click") -> None:
        if event != "click":
            raise ValueError(f"Unsupported event: {event}")
        hid = self.click_map.get(node_id)
        if not hid:
            raise KeyError(f"No click handler for {node_id}")
        handler = self.handlers.get(hid)
        if handler:
            handler()
        self._refresh()

    def tick(self, n: int = 1) -> None:
        self._ticks += n

    def snapshot(self) -> str:
        return _serialize(self.root)

    def find_text(self, pattern: str) -> Optional[str]:
        snap = self.snapshot()
        m = re.search(pattern, snap)
        return m.group(0) if m else None

    def _refresh(self) -> None:
        parsed = parse_app(self.app)
        self.root = _to_test_node(parsed["root"])
        self.handlers = parsed["handlers"]
        self.click_map = parsed["click_map"]


def mount(app: Any) -> MountedApp:
    parsed = parse_app(app)
    root = _to_test_node(parsed["root"])
    return MountedApp(
        app=app,
        root=root,
        handlers=parsed["handlers"],
        click_map=parsed["click_map"],
    )


def fire(mounted: MountedApp, node_id: str, event: str = "click") -> None:
    mounted.fire(node_id, event)


def tick(mounted: MountedApp, n: int = 1) -> None:
    with batch():
        mounted.tick(n)


def snapshot(mounted: MountedApp) -> str:
    return mounted.snapshot()


def _to_test_node(node: IRNode) -> TestNode:
    props = dict(node.props)
    text = ""
    if callable(props.get("text")):
        text = str(props["text"]())
    elif "text" in props:
        text = str(props["text"])
    elif "label" in props:
        text = str(props["label"])
    from echoui.roles import role_tag

    return TestNode(
        id=node.id,
        role=node.role,
        tag=role_tag(node.role),
        props=props,
        text=text,
        children=[_to_test_node(c) for c in node.children],
    )


def _serialize(node: TestNode, depth: int = 0) -> str:
    indent = "  " * depth
    line = f"{indent}<{node.tag} id={node.id}"
    if node.text:
        line += f' text="{node.text}"'
    for k, v in node.props.items():
        if k.startswith("_") or k in ("text", "label"):
            continue
        if isinstance(v, (str, int, float, bool)):
            line += f' {k}="{v}"'
    line += ">"
    lines = [line]
    for c in node.children:
        lines.append(_serialize(c, depth + 1))
    lines.append(f"{indent}</{node.tag}>")
    return "\n".join(lines)
