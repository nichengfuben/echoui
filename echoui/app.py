"""Application root: screens, compile, and dev entry."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Type

from echoui.screen import Screen
from echoui.sprite import reset_id_gen


class App:
    def __init__(
        self,
        screens: List[Type[Screen]],
        initial: Optional[str] = None,
        theme: str = "light",
        color_scheme: str = "auto",
        title: str = "EchoUI App",
    ) -> None:
        self.screens = {s.name or s.__name__: s for s in screens}
        self.initial = initial or (screens[0].name or screens[0].__name__)
        self.theme = theme
        self.color_scheme = color_scheme
        self.title = title
        self._current = self.initial

    def switch_screen(self, name: str, effect: str = "none", duration: float = 0.3) -> None:
        if name not in self.screens:
            raise KeyError(name)
        self._current = name

    def build_ir(self) -> Dict[str, Any]:
        reset_id_gen()
        screen_cls = self.screens[self._current]
        screen = screen_cls()
        return {
            "app": {"title": self.title, "theme": self.theme, "initial": self.initial},
            "screen": screen.to_ir().to_dict(),
            "screens": {n: sc().to_ir().to_dict() for n, sc in self.screens.items()},
        }

    def compile(self, target: str = "web", out_dir: str = "dist/web", **kwargs: Any) -> str:
        from echoui.compiler.bundler import build_target

        return build_target(self, target=target, out_dir=out_dir, **kwargs)

    def run(self, host: str = "127.0.0.1", port: int = 7999) -> None:
        from echoui.cli import dev_server

        dev_server(self, host=host, port=port)
