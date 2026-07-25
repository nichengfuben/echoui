"""3D viewport helpers (web: WebGL via escape or bundled three.js)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class Viewport3D:
    width: int = 640
    height: int = 360
    background: str = "#101020"
    objects: List[Dict[str, Any]] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.objects is None:
            self.objects = []

    def add_box(self, *, x: float, y: float, z: float, size: float = 1.0, color: str = "#888") -> None:
        self.objects.append({"kind": "box", "x": x, "y": y, "z": z, "size": size, "color": color})

    def to_ir_props(self) -> Dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "background": self.background,
            "objects": self.objects,
        }


def viewport3d(**props: Any) -> Dict[str, Any]:
    vp = Viewport3D(**props)
    return vp.to_ir_props()
