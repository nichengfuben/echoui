"""Sprite motion, sensing, and MotionChain tests."""

from __future__ import annotations

import asyncio

from echoui import Sprite
from echoui.chain import MotionChain
from echoui.costume import costume
from echoui.input import mouse
from echoui.sensing import touches_team
from echoui.state import Store
from echoui.storage import json_get, local, persist_mixin


class Mover(Sprite):
    role = "sprite"
    x: float = 10
    y: float = 10
    width: float = 20
    height: float = 20
    background: str = "#ff0000"
    team: str = "hero"


class Foe(Sprite):
    role = "sprite"
    x: float = 25
    y: float = 10
    width: float = 20
    height: float = 20
    team: str = "enemy"


def test_sprite_motion_helpers():
    s = Mover()
    mouse.move(100, 50)
    s.point_toward("mouse")
    assert s.rotation != 0
    s.bounce_on_edge(640, 360)
    s.flip_horizontal()
    s.flip_vertical()
    assert "flip_h" in s._effects
    s.change_layer(2)
    assert s.layer == 2
    s.orbit((0, 0), 90)
    assert s.x != 10 or s.y != 10


def test_sprite_sensing_wrappers():
    a = Mover()
    b = Foe()
    assert a.touches(b)
    assert a.touches_point(15, 15)
    assert a.touches_edge(640, 360) is False
    assert a.touches_team("enemy", [b])
    assert touches_team(a, "enemy", [b])
    a.background = "#ff0000"
    assert a.touches_color("#ff0000")
    end = a.raycast(0, 100)
    assert end[0] > a.x


def test_sprite_split_and_image():
    hero = Sprite()
    hero.costumes = [costume("a", "a.png")]
    hero.current_costume = "a"
    clones = hero.split_to(2)
    assert len(clones) == 2
    node = hero.image()
    assert node.role == "image"


def test_motion_chain_when_otherwise():
    values: list[str] = []

    class Actor(Sprite):
        flag: bool = False

    actor = Actor()
    actor.flag = False

    async def run():
        chain = MotionChain(actor).when(lambda: actor.flag, lambda s: values.append("yes")).otherwise(
            lambda s: values.append("no")
        )
        await chain
        actor.flag = True
        chain2 = MotionChain(actor).when(lambda: actor.flag, lambda s: values.append("yes")).otherwise(
            lambda s: values.append("no")
        )
        await chain2

    asyncio.run(run())
    assert values == ["no", "yes"]


def test_persist_mixin():
    Store.reset_registry()

    class Prefs(Store, persist_mixin("local")):
        theme: str = "light"

    p = Prefs()
    p._load_persisted()
    p.theme = "dark"
    assert json_get(local(), "Prefs.theme") == "dark"


def test_responsive_layout_emits_media_query():
    from echoui import App, Screen, col, row, text
    from echoui.compiler.bundler import build_target

    class R(Screen):
        def build(self):
            return col(
                row(text("a"), text("b"), responsive={"sm": {"direction": "col"}}),
                responsive={"md": {"gap": 4}},
            )

    import tempfile
    from pathlib import Path

    out = Path(tempfile.mkdtemp()) / "web"
    build_target(App(screens=[R], initial="R"), target="web", out_dir=str(out))
    html = (out / "index.html").read_text(encoding="utf-8")
    assert "@media (max-width:640px)" in html
