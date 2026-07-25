"""Router navigation compile tests."""

from __future__ import annotations

from echoui import App, Screen, button, col, text
from echoui.compiler.analyzer import analyze
from echoui.compiler.parser import collect_all_handlers, parse_app
from echoui.router import Router

router = Router()
router.add("/", "Home")
router.add("/game", "Game")


class Home(Screen):
    def build(self):
        return col(
            text("Home"),
            button("Go", on_click=lambda: router.navigate("/game")),
        )


class Game(Screen):
    def build(self):
        return col(
            text("Game"),
            button("Back", on_click=lambda: router.navigate("/")),
        )


app = App(screens=[Home, Game], initial="Home")


def test_router_nav_compiles():
    handlers, _, _ = collect_all_handlers(app)
    from echoui.compiler.emit_actions import compile_actions

    actions = compile_actions(handlers, app_initial="Home")
    nav = [a for a in actions.values() if a.get("k") == "nav"]
    assert len(nav) >= 2
    assert any(a["href"] == "game.html" for a in nav)
    assert any(a["href"] == "index.html" for a in nav)


def test_multi_screen_analyze_passes():
    app.switch_screen("Home")
    parsed = parse_app(app)
    handlers, click_map, dom = collect_all_handlers(app)
    parsed["handlers"] = handlers
    parsed["click_map"] = click_map
    parsed["dom_handlers"] = dom
    analyzed = analyze(parsed)
    assert analyzed["actions"]
