"""Costume API tests."""

from __future__ import annotations

from echoui import Sprite, Store
from echoui.compiler.emit_actions import compile_action_script
from echoui.costume import CostumeFieldsMixin, bind_costumes, costume, make_costume_handlers


class DemoStore(Store, CostumeFieldsMixin):
    sprite_url: str = ""


class Hero(Sprite):
    role = "sprite"
    costumes = [costume("idle", "idle.png"), costume("run", "run.png")]
    current_costume: str = "idle"


def test_sprite_costume_api():
    h = Hero()
    assert h.costume_src == "idle.png"
    h.switch_costume("run")
    assert h.costume_src == "run.png"
    h.next_costume()
    assert h.costume_src == "idle.png"
    h.switch_costume(1)
    assert h.current_costume == "run"


def test_bind_costumes_compile():
    controls = bind_costumes(
        DemoStore,
        [costume("a", "a.png"), costume("b", "b.png")],
        url="sprite_url",
    )
    assert compile_action_script(controls.next_costume)
    assert compile_action_script(controls.save_costume)
    assert compile_action_script(controls.switch["a"])
    assert compile_action_script(controls.switch["b"])


def test_bind_costumes_switch_by_name():
    controls = bind_costumes(
        DemoStore,
        [costume("idle", "i.png"), costume("run", "r.png")],
        url="sprite_url",
    )
    s = DemoStore()
    controls.switch["run"]()
    assert s.sprite_url == "r.png"
    assert s.current_costume == "run"


def test_costume_upload_save_and_cycle():
    save, nxt = make_costume_handlers(DemoStore, url="sprite_url")
    s = DemoStore()
    s.sprite_url = "a.png"
    save()
    s.sprite_url = "b.png"
    save()
    assert s.costume_count == 2
    nxt()
    assert s.sprite_url in ("a.png", "b.png")
