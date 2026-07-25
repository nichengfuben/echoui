"""SSS contract tests."""

from __future__ import annotations

import pytest

from echoui import App, Screen, button, col, text
from echoui.compiler.analyzer import analyze
from echoui.compiler.parser import parse_app
from echoui.exceptions import SSSError
from echoui.layout import box
from echoui.stage import stage as stage_fn


class FlowScreen(Screen):
    def build(self):
        return col(text("hello"))


class GoodFree(Screen):
    layout = "free"

    def build(self):
        return stage_fn(
            box(width=100, height=100, x=0, y=0, background="#000"),
            width=640,
            height=360,
            layout="free",
        )


class BadFree(Screen):
    layout = "free"

    def build(self):
        return col(
            stage_fn(box(width=10, height=10), width=640, height=360, layout="free"),
            button("x"),
        )


def test_flow_screen_sprite_root():
    app = App(screens=[FlowScreen], initial="FlowScreen")
    root = parse_app(app)["root"]
    assert root.role == "screen"
    assert root.props.get("layout", "flow") == "flow"
    assert root.children[0].role == "box"


def test_free_screen_stage_root():
    app = App(screens=[GoodFree], initial="GoodFree")
    root = parse_app(app)["root"]
    assert root.props["layout"] == "free"
    assert len(root.children) == 1
    assert root.children[0].role == "stage"
    assert root.children[0].props.get("fill_viewport") is True


def test_free_screen_col_wrap_raises():
    app = App(screens=[BadFree], initial="BadFree")
    with pytest.raises(SSSError, match="stage"):
        parse_app(app)


def test_analyzer_normalizes_free_stage():
    app = App(screens=[GoodFree], initial="GoodFree")
    parsed = analyze(parse_app(app))
    stage_node = parsed["root"].children[0]
    assert stage_node.props.get("fill_viewport") is True


def test_flow_may_embed_free_stage():
    class Mixed(Screen):
        def build(self):
            return col(
                text("title"),
                stage_fn(box(width=32, height=32), width=200, height=100, layout="free"),
            )

    root = parse_app(App(screens=[Mixed], initial="Mixed"))["root"]
    assert root.children[0].role == "box"
    inner = root.children[0].children
    assert any(c.role == "stage" for c in inner)
