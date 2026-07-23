"""Vector pen drawing helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Pen:
    color: str = "#000000"
    width: float = 2.0
    _paths: List[List[Tuple[float, float]]] = field(default_factory=list)
    _current: List[Tuple[float, float]] = field(default_factory=list)

    def move_to(self, x: float, y: float) -> "Pen":
        if self._current:
            self._paths.append(self._current)
        self._current = [(x, y)]
        return self

    def line_to(self, x: float, y: float) -> "Pen":
        self._current.append((x, y))
        return self

    def close(self) -> "Pen":
        if self._current:
            self._paths.append(self._current)
            self._current = []
        return self

    def to_svg_path(self) -> str:
        parts: List[str] = []
        for path in self._paths:
            if not path:
                continue
            parts.append(f"M {path[0][0]} {path[0][1]}")
            for x, y in path[1:]:
                parts.append(f"L {x} {y}")
        return " ".join(parts)
