"""Frame event and motion tests."""

from __future__ import annotations

import asyncio

from echoui import App, Screen, Sprite, Store
from echoui.events import on
from echoui.testing import mount, tick


class GameStore(Store):
    ticks: int = 0


store = GameStore()


class Mover(Sprite):
    @on("frame")
    def update(self, dt: float) -> None:
        gs = GameStore()
        gs.ticks += 1
        self.change_x(10 * dt)


class Game(Screen):
    def build(self):
        return Mover().move_to(0, 0)


app = App(screens=[Game], initial="Game")


def test_frame_tick_updates_store():
    Store.reset_registry()
    gs = GameStore()
    gs.ticks = 0
    m = mount(app)
    tick(m, 5)
    assert gs.ticks >= 5


def test_glide_to_moves_sprite():
    hero = Mover()
    hero.x = 0

    async def run() -> None:
        await hero.glide_to(100, 0, 0.1)

    asyncio.run(run())
    assert abs(hero.x - 100) < 1
