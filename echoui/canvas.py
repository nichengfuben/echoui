"""Canvas rendering helpers with fluent context API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from echoui.sprite import IRNode


@dataclass
class CanvasContext:
    """Fluent immediate-mode style command builder for canvas role."""

    layer: "CanvasLayer"
    _fill: str = "#000000"
    _stroke: str = "#ffffff"
    _width: float = 1.0
    _font_size: int = 16
    _font_color: str = "#ffffff"
    _blend: str = "source-over"
    _path: List[Dict[str, Any]] = field(default_factory=list)

    def clear(self, color: str | None = None) -> "CanvasContext":
        self.layer.commands.append({"op": "clear", "color": color or "#000000"})
        return self

    def fill(self, color: str) -> "CanvasContext":
        self._fill = color
        return self

    def pen(self, color: str) -> "CanvasContext":
        self._stroke = color
        return self

    def width(self, w: float) -> "CanvasContext":
        self._width = w
        return self

    def font(self, size: int, color: str = "#ffffff") -> "CanvasContext":
        self._font_size = size
        self._font_color = color
        return self

    def blend(self, mode: str) -> "CanvasContext":
        self._blend = mode
        self.layer.commands.append({"op": "blend", "mode": mode})
        return self

    def circle(self, x: float, y: float, r: float, *, fill: bool = True) -> "CanvasContext":
        self.layer.commands.append(
            {
                "op": "circle",
                "x": x,
                "y": y,
                "r": r,
                "fill": self._fill if fill else None,
                "stroke": self._stroke,
                "width": self._width,
            }
        )
        return self

    def rect(self, x: float, y: float, w: float, h: float, *, fill: bool = True) -> "CanvasContext":
        self.layer.commands.append(
            {
                "op": "fillRect" if fill else "strokeRect",
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "color": self._fill if fill else self._stroke,
                "width": self._width,
            }
        )
        return self

    def text(self, content: str, x: float, y: float) -> "CanvasContext":
        self.layer.commands.append(
            {
                "op": "text",
                "text": content,
                "x": x,
                "y": y,
                "color": self._font_color,
                "size": self._font_size,
            }
        )
        return self

    def path(self, *points: tuple[float, float], close: bool = False) -> "CanvasContext":
        self.layer.commands.append(
            {
                "op": "path",
                "points": list(points),
                "close": close,
                "stroke": self._stroke,
                "fill": self._fill,
                "width": self._width,
            }
        )
        return self

    def gradient(self, x0: float, y0: float, x1: float, y1: float, stops: List[tuple[float, str]]) -> "CanvasContext":
        self.layer.commands.append(
            {"op": "gradient", "x0": x0, "y0": y0, "x1": x1, "y1": y1, "stops": stops}
        )
        return self

    def clip(self, x: float, y: float, w: float, h: float) -> "CanvasContext":
        self.layer.commands.append({"op": "clip", "x": x, "y": y, "w": w, "h": h})
        return self


@dataclass
class CanvasLayer:
    width: int = 800
    height: int = 600
    commands: List[Dict[str, Any]] = field(default_factory=list)
    _ctx: Optional[CanvasContext] = field(default=None, repr=False)

    def clear(self, color: str = "#000000") -> "CanvasLayer":
        self.commands.append({"op": "clear", "color": color})
        return self

    def fill_rect(self, x: float, y: float, w: float, h: float, color: str) -> "CanvasLayer":
        self.commands.append({"op": "fillRect", "x": x, "y": y, "w": w, "h": h, "color": color})
        return self

    def draw_text(self, text: str, x: float, y: float, *, color: str = "#fff", size: int = 16) -> "CanvasLayer":
        self.commands.append({"op": "text", "text": text, "x": x, "y": y, "color": color, "size": size})
        return self

    def ctx(self) -> CanvasContext:
        if self._ctx is None:
            self._ctx = CanvasContext(layer=self)
        return self._ctx

    def to_ir(self) -> IRNode:
        return IRNode("canvas", props={"width": self.width, "height": self.height, "commands": self.commands})


def canvas(width: int = 800, height: int = 600) -> CanvasLayer:
    return CanvasLayer(width=width, height=height)
