"""Desktop window, tray, and menubar (PySide6 when available)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Tuple


@dataclass
class WindowState:
    title: str = "EchoUI"
    size: Tuple[int, int] = (800, 600)
    always_on_top: bool = False


class Window:
    def __init__(self) -> None:
        self._state = WindowState()

    def set_title(self, title: str) -> None:
        self._state.title = title

    def set_size(self, w: int, h: int) -> None:
        self._state.size = (w, h)

    def center(self) -> None:
        pass

    def minimize(self) -> None:
        pass

    def maximize(self) -> None:
        pass

    def fullscreen(self) -> None:
        pass

    def set_always_on_top(self, value: bool) -> None:
        self._state.always_on_top = value


window = Window()


@dataclass
class TrayMenu:
    icon: str = ""
    items: List[Tuple[str, Callable[[], None]]] = field(default_factory=list)


def tray_create(*, icon: str, menu: List[Tuple[str, Callable[[], None]]]) -> TrayMenu:
    return TrayMenu(icon=icon, items=menu)


def menubar_set(entries: List[Tuple[str, List[Tuple[str, Callable[[], None]]]]]) -> None:
    _menubar = entries


def global_shortcut_register(combo: str, handler: Callable[[], None]) -> None:
    _shortcuts = getattr(global_shortcut_register, "_map", {})
    _shortcuts[combo] = handler
    global_shortcut_register._map = _shortcuts  # type: ignore[attr-defined]


def run_qt_app(main_fn: Callable[[], None]) -> None:
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError as e:
        raise ImportError("pip install echoui[desktop]") from e
    import sys

    app = QApplication(sys.argv)
    main_fn()
    sys.exit(app.exec())
