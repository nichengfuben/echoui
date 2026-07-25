"""Screen view surface type (page / window / route)."""

from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Union

from echoui.compiler.sss import free_screen_must_return_stage
from echoui.sprite import IRNode, Sprite, normalize_children


class Screen(Sprite):
    """Full view surface. flow → Sprite tree; free → single Stage root."""

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
        if self.layout == "free":
            children = free_screen_must_return_stage(children)
            stage = children[0]
            if self.background:
                stage.props.setdefault("background", self.background)
            stage.props.setdefault("fill_viewport", True)
            stage.props.setdefault("layout", "free")
        props: Dict[str, Any] = {
            "layout": self.layout,
            "screen": self.name or self.__class__.__name__,
        }
        if self.background and self.layout != "free":
            props["background"] = self.background
        node = IRNode(
            "screen",
            props=props,
            children=children,
        )
        from echoui.events import attach_class_handlers

        attach_class_handlers(node, self.__class__)
        return node
