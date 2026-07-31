"""Desktop window, tray, and menubar (PySide6 when available)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Tuple

from echoui.exceptions import UnsupportedCapability


@dataclass
class WindowState:
    title: str = "EchoUI"
    size: Tuple[int, int] = (800, 600)
    always_on_top: bool = False
    minimized: bool = False
    maximized: bool = False
    fullscreen: bool = False


class Window:
    def __init__(self) -> None:
        self._state = WindowState()
        self._qt_window: object | None = None

    def bind_qt(self, win: object) -> None:
        self._qt_window = win

    def set_title(self, title: str) -> None:
        self._state.title = title
        if self._qt_window is not None and hasattr(self._qt_window, "setWindowTitle"):
            self._qt_window.setWindowTitle(title)  # type: ignore[attr-defined]

    def set_size(self, w: int, h: int) -> None:
        self._state.size = (w, h)
        if self._qt_window is not None and hasattr(self._qt_window, "resize"):
            self._qt_window.resize(w, h)  # type: ignore[attr-defined]

    def center(self) -> None:
        if self._qt_window is not None and hasattr(self._qt_window, "frameGeometry"):
            try:
                from PySide6.QtWidgets import QApplication

                geo = self._qt_window.frameGeometry()  # type: ignore[attr-defined]
                screen = QApplication.primaryScreen()
                if screen is not None:
                    center = screen.availableGeometry().center()
                    geo.moveCenter(center)
                    self._qt_window.move(geo.topLeft())  # type: ignore[attr-defined]
                return
            except Exception:
                pass
        # No bound window: record intent only (tests / headless).
        self._state.minimized = False

    def minimize(self) -> None:
        self._state.minimized = True
        if self._qt_window is not None and hasattr(self._qt_window, "showMinimized"):
            self._qt_window.showMinimized()  # type: ignore[attr-defined]

    def maximize(self) -> None:
        self._state.maximized = True
        if self._qt_window is not None and hasattr(self._qt_window, "showMaximized"):
            self._qt_window.showMaximized()  # type: ignore[attr-defined]

    def fullscreen(self) -> None:
        self._state.fullscreen = True
        if self._qt_window is not None and hasattr(self._qt_window, "showFullScreen"):
            self._qt_window.showFullScreen()  # type: ignore[attr-defined]

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
    menubar_set._entries = entries  # type: ignore[attr-defined]


def global_shortcut_register(combo: str, handler: Callable[[], None]) -> None:
    _shortcuts = getattr(global_shortcut_register, "_map", {})
    _shortcuts[combo] = handler
    global_shortcut_register._map = _shortcuts  # type: ignore[attr-defined]


def run_qt_app(main_fn: Callable[[], None]) -> None:
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError as e:
        raise UnsupportedCapability("pip install echoui[desktop]") from e
    import sys

    app = QApplication(sys.argv)
    main_fn()
    sys.exit(app.exec())
