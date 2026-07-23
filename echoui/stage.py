"""Stage coordinate container."""

from __future__ import annotations

from typing import Any, List, Union

from echoui.sprite import IRNode, Sprite, normalize_children


class Stage(Sprite):
    role = "stage"
    width: float = 1920
    height: float = 1080
    layout: str = "free"
    origin: str = "center"
    y_axis: str = "up"
    background: str = "#101020"

    def build(self) -> Union[IRNode, Sprite, List[Any], None]:
        return IRNode("stage")

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
            },
            children=normalize_children(self.build()),
        )


def stage(*children: Any, **props: Any) -> IRNode:
    return IRNode("stage", props=props, children=normalize_children(list(children)))
