"""Stage coordinate container."""

from __future__ import annotations

from typing import Any, List, Tuple, Union

from echoui.physics import World
from echoui.sprite import IRNode, Sprite, normalize_children


class Stage(Sprite):
    role = "stage"
    width: float = 1920
    height: float = 1080
    layout: str = "free"
    origin: str = "center"
    y_axis: str = "up"
    background: str = "#101020"
    physics: bool = False
    gravity: Tuple[float, float] = (0, -10)

    def __init__(self) -> None:
        super().__init__()
        self._sprites: List[Sprite] = []
        self._world: World | None = None

    def build(self) -> Union[IRNode, Sprite, List[Any], None]:
        return IRNode("stage")

    def add(self, sprite: Sprite) -> Sprite:
        self._sprites.append(sprite)
        return sprite

    def remove(self, sprite: Sprite) -> Sprite:
        if sprite in self._sprites:
            self._sprites.remove(sprite)
        return sprite

    def set_background(self, value: str) -> None:
        self.background = value

    def clear_pen(self) -> None:
        pass

    def step_physics(self, dt: float) -> None:
        if not self.physics:
            return
        if self._world is None:
            self._world = World(gravity=(self.gravity[0], -self.gravity[1]))
        self._world.step(dt)

    def to_ir(self) -> IRNode:
        return IRNode(
            "stage",
            props={
                "width": self.width,
                "height": self.height,
                "layout": self.layout,
                "origin": self.origin,
                "y_axis": self.y_axis,
                "background": self.background,
                "physics": self.physics,
            },
            children=normalize_children(self.build()),
        )


def stage(*children: Any, **props: Any) -> IRNode:
    return IRNode("stage", props=props, children=normalize_children(list(children)))
