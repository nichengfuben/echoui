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


class ClonePool:
    """Object pool for high-frequency sprites (PLAN §17)."""

    def __init__(self, cls: type, *, max_size: int = 100) -> None:
        self.cls = cls
        self.max_size = max_size
        self._free: list[Any] = []
        self._active: list[Any] = []

    def acquire(self, **kwargs: Any) -> Any:
        obj = self._free.pop() if self._free else self.cls()
        for k, v in kwargs.items():
            setattr(obj, k, v)
        if hasattr(obj, "on_clone"):
            obj.on_clone()
        self._active.append(obj)
        return obj

    def release(self, obj: Any) -> None:
        if obj in self._active:
            self._active.remove(obj)
        if len(self._free) < self.max_size:
            self._free.append(obj)


def clone_pool(cls: type, *, max: int = 100) -> ClonePool:
    return ClonePool(cls, max_size=max)
