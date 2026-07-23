"""Modal, drawer, and overlay primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

from echoui.sprite import IRNode, normalize_children


@dataclass
class OverlayState:
    open: bool = False
    content: Any = None

    def show(self, content: Any = None) -> None:
        self.open = True
        if content is not None:
            self.content = content

    def hide(self) -> None:
        self.open = False


def modal(content: Any, *, open: bool = False) -> IRNode:
    return IRNode("box", props={"role": "modal", "open": open}, children=normalize_children([content]))


def drawer(content: Any, *, side: str = "right", open: bool = False) -> IRNode:
    return IRNode("box", props={"role": "drawer", "side": side, "open": open},
                  children=normalize_children([content]))


def sheet(content: Any, *, open: bool = False) -> IRNode:
    return IRNode("box", props={"role": "sheet", "open": open}, children=normalize_children([content]))


_toasts: List[Dict[str, Any]] = []


def toast(message: str, *, duration: float = 3.0) -> None:
    _toasts.append({"message": message, "duration": duration})


def get_toasts() -> List[Dict[str, Any]]:
    return list(_toasts)


def confirm(message: str, on_ok: Callable[[], None], on_cancel: Callable[[], None] | None = None) -> IRNode:
    return IRNode("box", props={"role": "confirm", "message": message})


def alert(message: str) -> IRNode:
    return IRNode("box", props={"role": "alert", "message": message})


def popover(content: Any, *, anchor: str = "") -> IRNode:
    return IRNode("box", props={"role": "popover", "anchor": anchor},
                  children=normalize_children([content]))


def portal(content: Any, *, target: str = "body") -> IRNode:
    return IRNode("box", props={"role": "portal", "target": target},
                  children=normalize_children([content]))


@dataclass
class CommandPalette:
    open: bool = False
    commands: List[Dict[str, Any]] = field(default_factory=list)

    def toggle(self) -> None:
        self.open = not self.open

    def register(self, label: str, action: Callable[[], None]) -> None:
        self.commands.append({"label": label, "action": action})


def command_palette() -> CommandPalette:
    return CommandPalette()
