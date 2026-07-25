"""IR nodes and Sprite base type."""

from __future__ import annotations

import itertools
import random
from typing import Any, Dict, List, Union

from echoui import sensing
from echoui.chain import MotionChain
from echoui.reactive import Computed, Signal
from echoui.state import get_signal_key_for_signal

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
        key = get_signal_key_for_signal(v)
        return {"type": "signal", "key": key or id(v)}
    if isinstance(v, Computed):
        return {"type": "computed", "id": id(v)}
    if callable(v) and not isinstance(v, type):
        return {"type": "fn", "name": getattr(v, "__name__", "lambda"), "_fn": v}
    return v


class Sprite:
    role: str = "box"
    x: float = 0
    y: float = 0
    rotation: float = 0
    scale: float = 1
    opacity: float = 1.0
    hidden: bool = False
    layer: int = 0
    width: float = 32
    height: float = 32

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

    def __init__(self) -> None:
        self._children: List["Sprite"] = []
        self._effects: Dict[str, float] = {}
        self._destroyed = False
        self._costumes: Dict[str, str] = {}
        self.current_costume = ""
        cls_costumes = getattr(self.__class__, "costumes", None)
        if cls_costumes:
            for item in cls_costumes:
                if hasattr(item, "name") and hasattr(item, "src"):
                    self._costumes[item.name] = item.src
                elif isinstance(item, tuple) and len(item) == 2:
                    self._costumes[str(item[0])] = str(item[1])
            if self._costumes and not self.current_costume:
                default = getattr(self.__class__, "current_costume", "")
                self.current_costume = default if default in self._costumes else next(iter(self._costumes))

    def build(self) -> Union["IRNode", "Sprite", List[Any], None]:
        return IRNode(self.role)

    def on_mount(self) -> None:
        pass

    def on_unmount(self) -> None:
        pass

    def on_update(self, prev: Dict[str, Any]) -> None:
        pass

    def on_clone(self) -> None:
        pass

    def on_error(self, err: Exception) -> None:
        return None

    def move_to(self, x: float | str, y: float | str | None = None) -> "Sprite":
        if y is None and isinstance(x, str):
            y = x
            x = 0
        if x == "random":
            x = random.uniform(0, 640)
        if y == "random":
            y = random.uniform(0, 360)
        if isinstance(x, (int, float)):
            self.x = float(x)
        if isinstance(y, (int, float)):
            self.y = float(y)
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

    def move_steps(self, steps: float) -> "Sprite":
        import math

        rad = math.radians(self.rotation)
        self.x += math.cos(rad) * steps
        self.y += math.sin(rad) * steps
        return self

    def show(self) -> "Sprite":
        self.hidden = False
        return self

    def hide(self) -> "Sprite":
        self.hidden = True
        return self

    def set_opacity(self, value: float) -> "Sprite":
        self.opacity = value
        return self

    def set_size(self, w: float, h: float | None = None) -> "Sprite":
        self.width = w
        if h is not None:
            self.height = h
        return self

    def change_size(self, delta: float) -> "Sprite":
        self.width += delta
        self.height += delta
        return self

    def set_scale(self, value: float) -> "Sprite":
        self.scale = value
        return self

    def set_effect(self, name: str, value: float) -> "Sprite":
        self._effects[name] = value
        return self

    def clear_effects(self) -> "Sprite":
        self._effects.clear()
        return self

    @property
    def costume_src(self) -> str:
        if self.current_costume and self.current_costume in self._costumes:
            return self._costumes[self.current_costume]
        if self._costumes:
            return next(iter(self._costumes.values()))
        return ""

    def switch_costume(self, name_or_idx: str | int) -> "Sprite":
        if isinstance(name_or_idx, int):
            keys = list(self._costumes.keys())
            if 0 <= name_or_idx < len(keys):
                self.current_costume = keys[name_or_idx]
        elif name_or_idx in self._costumes:
            self.current_costume = str(name_or_idx)
        return self

    def next_costume(self) -> "Sprite":
        if not self._costumes:
            return self
        keys = list(self._costumes.keys())
        if self.current_costume not in keys:
            self.current_costume = keys[0]
            return self
        idx = (keys.index(self.current_costume) + 1) % len(keys)
        self.current_costume = keys[idx]
        return self

    def point_toward(self, target: Any = "mouse") -> "Sprite":
        import math

        if hasattr(target, "x") and hasattr(target, "y"):
            dx = float(target.x) - self.x
            dy = float(target.y) - self.y
        elif isinstance(target, (int, float)):
            self.rotation = float(target)
            return self
        elif target == "mouse":
            from echoui.input import mouse

            dx = mouse.x - self.x
            dy = mouse.y - self.y
        else:
            return self
        self.rotation = math.degrees(math.atan2(dy, dx))
        return self

    def bounce_on_edge(self, stage_w: float = 640, stage_h: float = 360) -> "Sprite":
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x + self.width > stage_w:
            self.x = stage_w - self.width
        if self.y + self.height > stage_h:
            self.y = stage_h - self.height
        return self

    def flip_horizontal(self) -> "Sprite":
        self._effects["flip_h"] = 1.0
        return self

    def flip_vertical(self) -> "Sprite":
        self._effects["flip_v"] = 1.0
        return self

    def change_layer(self, delta: int) -> "Sprite":
        self.layer += delta
        return self

    def say(self, message: str, *, seconds: float = 2.0) -> "Sprite":
        self._speech = message  # type: ignore[attr-defined]
        self._speech_seconds = seconds  # type: ignore[attr-defined]
        return self

    def orbit(self, center: Any, degrees: float) -> "Sprite":
        import math

        if hasattr(center, "x") and hasattr(center, "y"):
            cx, cy = float(center.x), float(center.y)
        elif isinstance(center, (tuple, list)) and len(center) >= 2:
            cx, cy = float(center[0]), float(center[1])
        else:
            return self
        dx = self.x - cx
        dy = self.y - cy
        dist = math.hypot(dx, dy) or 1.0
        base = math.atan2(dy, dx)
        new_a = base + math.radians(degrees)
        self.x = cx + math.cos(new_a) * dist
        self.y = cy + math.sin(new_a) * dist
        return self

    def touches_team(self, team: str, others: List["Sprite"]) -> bool:
        return sensing.touches_team(self, team, others)

    def touches_color(self, color: str, *, tolerance: int = 0) -> bool:
        return sensing.touches_color(self, color, tolerance=tolerance)

    def touches_edge(self, stage_w: float = 640, stage_h: float = 360) -> bool:
        return sensing.touches_edge(self, stage_w, stage_h)

    def touches_point(self, px: float, py: float) -> bool:
        return sensing.touches_point(self, px, py)

    def raycast(self, angle_deg: float, max_dist: float = 500) -> tuple[float, float]:
        return sensing.raycast(self, angle_deg, max_dist)

    def split_to(self, n: int) -> List["Sprite"]:
        return [self.clone() for _ in range(max(0, n))]

    def image(self, src: Any = None, **props: Any) -> IRNode:
        from echoui.layout import image as image_fn

        resolved = src if src is not None else self.costume_src
        return image_fn(
            resolved,
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            **props,
        )

    def move_to_front(self) -> "Sprite":
        self.layer += 1
        return self

    def move_to_back(self) -> "Sprite":
        self.layer -= 1
        return self

    def touches(self, other: "Sprite") -> bool:
        return sensing.touches(self, other)

    def distance_to(self, other: "Sprite") -> float:
        return sensing.distance_to(self, other)

    def overlapping(self, other: "Sprite") -> bool:
        return sensing.overlapping(self, other)

    def glide_to(self, x: float, y: float, duration: float) -> MotionChain:
        return MotionChain(self).glide_to(x, y, duration)

    def fade_in(self, duration: float = 0.3) -> MotionChain:
        return MotionChain(self).fade_in(duration)

    def fade_out(self, duration: float = 0.3) -> MotionChain:
        return MotionChain(self).fade_out(duration)

    def spin(self, degrees: float, duration: float) -> MotionChain:
        return MotionChain(self).spin(degrees, duration)

    def add(self, child: "Sprite") -> "Sprite":
        self._children.append(child)
        return self

    def remove(self, child: "Sprite") -> "Sprite":
        if child in self._children:
            self._children.remove(child)
        return self

    def clear_children(self) -> "Sprite":
        self._children.clear()
        return self

    def destroy(self) -> None:
        self._destroyed = True
        self.on_unmount()

    def clone(self) -> "Sprite":
        import copy

        dup = copy.copy(self)
        dup.on_clone()
        return dup

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
        node.props.setdefault("opacity", self.opacity)
        if self.hidden:
            node.props["hidden"] = True
        if self._effects:
            node.props["effects"] = dict(self._effects)
        from echoui.events import attach_class_handlers

        attach_class_handlers(node, self.__class__)
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
