"""Canvas rendering helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from echoui.sprite import IRNode


@dataclass
class CanvasLayer:
    width: int = 800
    height: int = 600
    commands: List[Dict[str, Any]] = field(default_factory=list)

    def clear(self, color: str = "#000000") -> None:
        self.commands.append({"op": "clear", "color": color})

    def fill_rect(self, x: float, y: float, w: float, h: float, color: str) -> None:
        self.commands.append({"op": "fillRect", "x": x, "y": y, "w": w, "h": h, "color": color})

    def draw_text(self, text: str, x: float, y: float, *, color: str = "#fff", size: int = 16) -> None:
        self.commands.append({"op": "text", "text": text, "x": x, "y": y, "color": color, "size": size})

    def to_ir(self) -> IRNode:
        return IRNode("canvas", props={"width": self.width, "height": self.height, "commands": self.commands})


def canvas(width: int = 800, height: int = 600) -> CanvasLayer:
    return CanvasLayer(width=width, height=height)
