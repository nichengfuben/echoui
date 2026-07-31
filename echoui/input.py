"""Keyboard, mouse, touch, gamepad, and IME composition input."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set


@dataclass
class CompositionState:
    """IME / composition session state (host or browser composition*)."""

    active: bool = False
    data: str = ""
    start: int = 0
    end: int = 0

    def begin(self, data: str = "", start: int = 0, end: int = 0) -> None:
        self.active = True
        self.data = data
        self.start = start
        self.end = end if end else len(data)

    def update(self, data: str, start: int = 0, end: int = 0) -> None:
        self.active = True
        self.data = data
        self.start = start
        self.end = end if end else len(data)

    def end_session(self, data: str = "", *, commit: bool = True) -> str:
        """Finish composition; returns committed text when ``commit`` else ''."""
        final = data if data else self.data
        self.active = False
        self.data = ""
        self.start = 0
        self.end = 0
        return final if commit else ""

    def clear(self) -> None:
        self.active = False
        self.data = ""
        self.start = 0
        self.end = 0


@dataclass
class Keyboard:
    _down: Set[str] = field(default_factory=set)
    _pressed: Set[str] = field(default_factory=set)
    _released: Set[str] = field(default_factory=set)
    composition: CompositionState = field(default_factory=CompositionState)
    _committed: List[str] = field(default_factory=list)

    def down(self, key: str) -> bool:
        return key in self._down

    def pressed(self, key: str) -> bool:
        return key in self._pressed

    def released(self, key: str) -> bool:
        return key in self._released

    def composing(self) -> bool:
        return self.composition.active

    def composition_text(self) -> str:
        return self.composition.data

    def simulate_down(self, key: str) -> None:
        self._down.add(key)
        self._pressed.add(key)

    def simulate_up(self, key: str) -> None:
        self._down.discard(key)
        self._released.add(key)

    def composition_start(self, data: str = "") -> None:
        self.composition.begin(data)

    def composition_update(self, data: str) -> None:
        self.composition.update(data)

    def composition_end(self, data: str = "", *, commit: bool = True) -> str:
        text = self.composition.end_session(data, commit=commit)
        if text:
            self._committed.append(text)
        return text

    def take_committed(self) -> List[str]:
        out = list(self._committed)
        self._committed.clear()
        return out

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


def apply_composition_event(
    event_type: str,
    data: str = "",
    *,
    start: int = 0,
    end: int = 0,
    commit: bool = True,
) -> Optional[str]:
    """Apply a browser-style composition event to the global keyboard.

    Returns committed text for ``compositionend``, else None.
    """
    et = event_type.replace("-", "").lower()
    if et in ("compositionstart", "composition_start"):
        keyboard.composition_start(data)
        return None
    if et in ("compositionupdate", "composition_update"):
        keyboard.composition_update(data)
        return None
    if et in ("compositionend", "composition_end"):
        return keyboard.composition_end(data, commit=commit)
    raise ValueError(f"unknown composition event: {event_type!r}")
