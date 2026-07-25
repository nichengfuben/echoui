"""Local compile validation tests."""

from __future__ import annotations

import pytest

from echoui import App, Screen, Store, button, col, on, text
from echoui.compiler.analyzer import analyze
from echoui.compiler.parser import parse_app
from echoui.exceptions import CompileError


class BadStore(Store):
    count: int = 0


store = BadStore()


class Bad(Screen):
    @on("keydown", key="Space")
    def noop(self, event) -> None:
        print("cannot compile this")

    def build(self):
        return col(text("bad"), button("x", on_click=lambda: None))


bad_app = App(screens=[Bad], initial="Bad")


def test_uncompiled_handler_fails_build():
    Store.reset_registry()
    BadStore()
    with pytest.raises(CompileError, match="not compiled"):
        analyze(parse_app(bad_app))
