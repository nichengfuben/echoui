"""Screen view surface type."""

from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Union

from echoui.sprite import IRNode, Sprite, normalize_children


class Screen(Sprite):
    name: ClassVar[str] = ""
    layout: ClassVar[str] = "flow"
    background: ClassVar[str] = ""

    async def on_enter(self) -> None:
        pass

    def on_leave(self) -> None:
        pass

    def build(self) -> Union[IRNode, Sprite, List[Any], None]:
        return IRNode("box", props={"class": "screen"})

    def to_ir(self) -> IRNode:
        children = normalize_children(self.build())
        props: Dict[str, Any] = {
            "layout": self.layout,
            "screen": self.name or self.__class__.__name__,
        }
        if self.background:
            props["background"] = self.background
        return IRNode(
            "screen",
            props=props,
            children=children,
        )
