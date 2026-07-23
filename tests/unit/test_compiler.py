"""Compiler pipeline tests."""

from pathlib import Path

from echoui import App, Screen, button, col, text
from echoui.compiler.bundler import build_target
from echoui.compiler.parser import compile_app, parse_app
from echoui.state import Store


class CounterStore(Store):
    count: int = 0


store = CounterStore()


class Counter(Screen):
    def build(self):
        return col(
            text(lambda: f"Count: {store.count}"),
            button("+1", on_click=lambda: setattr(store, "count", store.count + 1)),
        )


def test_parse_app_returns_handlers():
    app = App(screens=[Counter], initial="Counter")
    parsed = parse_app(app)
    assert "root" in parsed
    assert "handlers" in parsed
    assert parsed["root"].role == "screen"


def test_compile_app_alias():
    app = App(screens=[Counter], initial="Counter")
    result = compile_app(app)
    assert "ir" in result


def test_build_web_creates_index(tmp_path):
    app = App(screens=[Counter], initial="Counter", title="Test")
    out = tmp_path / "web"
    path = build_target(app, target="web", out_dir=str(out))
    index = Path(path) / "index.html"
    assert index.exists()
    html = index.read_text(encoding="utf-8")
    assert "Count: 0" in html
    assert "EchoUI" in html or "Test" in html


def test_build_static_creates_files(tmp_path):
    app = App(screens=[Counter], initial="Counter")
    out = tmp_path / "static"
    build_target(app, target="static", out_dir=str(out))
    assert (out / "index.html").exists()
    assert (out / "screens.json").exists()
