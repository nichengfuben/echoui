"""Development tools for EchoUI apps."""

from __future__ import annotations

import json
from typing import Any, Dict

from echoui.compiler.parser import parse_app


def inspect_app(app: Any) -> Dict[str, Any]:
    parsed = parse_app(app)
    return {
        "screens": list(app.screens.keys()),
        "initial": app.initial,
        "handlers": list(parsed["handlers"].keys()),
        "click_nodes": list(parsed["click_map"].keys()),
    }


def dump_ir(app: Any) -> str:
    return json.dumps(app.build_ir(), indent=2, default=str)


class DevTools:
    def __init__(self, app: Any) -> None:
        self.app = app
        self._log: list[str] = []

    def log(self, msg: str) -> None:
        self._log.append(msg)

    def snapshot(self) -> Dict[str, Any]:
        return inspect_app(self.app)

    def history(self) -> list[str]:
        return list(self._log)
