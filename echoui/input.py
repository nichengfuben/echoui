"""Keyboard and mouse polling stubs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Set


@dataclass
class Keyboard:
    _down: Set[str] = field(default_factory=set)
    _pressed: Set[str] = field(default_factory=set)

    def down(self, key: str) -> bool:
        return key in self._down

    def pressed(self, key: str) -> bool:
        return key in self._pressed

    def released(self, key: str) -> bool:
        return key not in self._down and key in self._pressed

    def simulate_down(self, key: str) -> None:
        self._down.add(key)
        self._pressed.add(key)

    def simulate_up(self, key: str) -> None:
        self._down.discard(key)


@dataclass
class Mouse:
    x: float = 0
    y: float = 0
    _down: bool = False

    def down(self) -> bool:
        return self._down


keyboard = Keyboard()
mouse = Mouse()

_shortcuts: Dict[str, Callable[..., Any]] = {}


class Shortcuts:
    def __init__(self, mapping: Dict[str, Callable[..., Any]]) -> None:
        _shortcuts.update(mapping)
