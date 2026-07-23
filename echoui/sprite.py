"""IR nodes and Sprite base type."""

from __future__ import annotations

import itertools
from typing import Any, Dict, List, Union

from echoui.chain import MotionChain
from echoui.reactive import Computed, Signal

_id_gen = itertools.count(1)


def reset_id_gen(start: int = 1) -> None:
    global _id_gen
    _id_gen = itertools.count(start)


def _new_id() -> str:
    return f"n{next(_id_gen)}"


class IRNode:
    """Compiler intermediate representation node."""

    def __init__(
        self,
        role: str,
        *,
        node_id: str | None = None,
        props: Dict[str, Any] | None = None,
        children: List["IRNode"] | None = None,
        events: Dict[str, str] | None = None,
        bindings: Dict[str, Any] | None = None,
    ) -> None:
        self.id = node_id or _new_id()
        self.role = role
        self.props = props or {}
        self.children = children or []
        self.events = events or {}
        self.bindings = bindings or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "props": self.props,
            "children": [c.to_dict() for c in self.children],
            "events": self.events,
            "bindings": {k: _binding_ref(v) for k, v in self.bindings.items()},
        }


def _binding_ref(v: Any) -> Any:
    if isinstance(v, Signal):
        return {"type": "signal", "id": id(v)}
    if isinstance(v, Computed):
        return {"type": "computed", "id": id(v)}
    if callable(v) and not isinstance(v, type):
        return {"type": "fn", "name": getattr(v, "__name__", "lambda")}
    return v


class Sprite:
    role: str = "box"
    x: float = 0
    y: float = 0
    rotation: float = 0
    scale: float = 1

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

    def build(self) -> Union["IRNode", "Sprite", List[Any], None]:
        return IRNode(self.role)

    def on_mount(self) -> None:
        pass

    def on_unmount(self) -> None:
        pass

    def on_update(self, prev: Dict[str, Any]) -> None:
        pass

    def move_to(self, x: float, y: float) -> "Sprite":
        self.x, self.y = x, y
        return self

    def set_x(self, x: float) -> "Sprite":
        self.x = x
        return self

    def set_y(self, y: float) -> "Sprite":
        self.y = y
        return self

    def change_x(self, dx: float) -> "Sprite":
        self.x += dx
        return self

    def change_y(self, dy: float) -> "Sprite":
        self.y += dy
        return self

    def rotate(self, deg: float) -> "Sprite":
        self.rotation += deg
        return self

    def glide_to(self, x: float, y: float, duration: float) -> MotionChain:
        return MotionChain(self).glide_to(x, y, duration)

    def to_ir(self) -> IRNode:
        built = self.build()
        if isinstance(built, IRNode):
            node = built
        else:
            node = IRNode(self.role)
        node.props.setdefault("x", self.x)
        node.props.setdefault("y", self.y)
        node.props.setdefault("rotation", self.rotation)
        node.props.setdefault("scale", self.scale)
        return node


def normalize_children(obj: Any) -> List[IRNode]:
    if obj is None:
        return []
    if isinstance(obj, IRNode):
        return [obj]
    if isinstance(obj, Sprite):
        return [obj.to_ir()]
    if isinstance(obj, (list, tuple)):
        out: List[IRNode] = []
        for item in obj:
            out.extend(normalize_children(item))
        return out
    if callable(obj):
        return normalize_children(obj())
    return [IRNode("text", props={"text": str(obj)})]
