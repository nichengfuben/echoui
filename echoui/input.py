"""Keyboard and mouse input (PLAN §10)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Set


@dataclass
class Keyboard:
    _down: Set[str] = field(default_factory=set)
    _pressed: Set[str] = field(default_factory=set)
    _released: Set[str] = field(default_factory=set)

    def down(self, key: str) -> bool:
        return key in self._down

    def pressed(self, key: str) -> bool:
        return key in self._pressed

    def released(self, key: str) -> bool:
        return key in self._released

    def simulate_down(self, key: str) -> None:
        self._down.add(key)
        self._pressed.add(key)

    def simulate_up(self, key: str) -> None:
        self._down.discard(key)
        self._released.add(key)

    def end_frame(self) -> None:
        self._pressed.clear()
        self._released.clear()


@dataclass
class Mouse:
    x: float = 0
    y: float = 0
    _down: bool = False

    def down(self) -> bool:
        return self._down

    def move(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


keyboard = Keyboard()
mouse = Mouse()


@dataclass
class TouchPoint:
    x: float = 0
    y: float = 0


@dataclass
class Touch:
    points: list[TouchPoint] = field(default_factory=list)


@dataclass
class Gamepad:
    index: int = 0
    _buttons: Dict[str, bool] = field(default_factory=dict)

    def button(self, name: str) -> bool:
        return self._buttons.get(name, False)

    def press(self, name: str) -> None:
        self._buttons[name] = True

    def release(self, name: str) -> None:
        self._buttons[name] = False


@dataclass
class Gyroscope:
    x: float = 0
    y: float = 0
    z: float = 0


@dataclass
class Pen:
    pressure: float = 0
    tilt: float = 0


touch = Touch()
gyroscope = Gyroscope()
pen = Pen()


def gamepad(index: int = 0) -> Gamepad:
    return Gamepad(index=index)


_shortcuts: Dict[str, Callable[..., Any]] = {}


class Shortcuts:
    def __init__(self, mapping: Dict[str, Callable[..., Any]]) -> None:
        _shortcuts.update(mapping)

    @staticmethod
    def handlers() -> Dict[str, Callable[..., Any]]:
        return dict(_shortcuts)


def end_input_frame() -> None:
    keyboard.end_frame()
