"""2D endless runner — SSS: Screen → Stage → Sprite."""

from __future__ import annotations

from echoui import App, Screen, button, on, text
from echoui.layout import box
from echoui.stage import stage

from game import GROUND_Y, MAX_OBS, PLAYER_X, RunnerStore, jump, reset_game, tick

store = RunnerStore()


class Runner(Screen):
    layout = "free"
    background = "#1a1a2e"

    @on("frame")
    def loop(self, dt: float) -> None:
        tick(dt)

    @on("keydown", key="Space")
    def do_jump(self, event) -> None:
        jump()

    @on("keydown", key="KeyR")
    def do_reset(self, event) -> None:
        reset_game()

    def build(self):
        obstacles = [
            box(
                width=28,
                height=40,
                x=lambda i=i: getattr(store, f"obs{i}_x"),
                y=GROUND_Y,
                background="#c0392b",
            )
            for i in range(MAX_OBS)
        ]
        score_text = lambda: (
            f"Score: {store.score}"
            + (" — GAME OVER (R)" if store.game_over else " — Space jump")
        )
        return stage(
            box(width=640, height=360, x=0, y=0, background="#87ceeb"),
            box(width=640, height=60, x=0, y=GROUND_Y, background="#8B4513"),
            box(
                width=32,
                height=32,
                x=PLAYER_X,
                y=lambda: store.player_y,
                background="#2ecc71",
            ),
            *obstacles,
            box(width=300, height=24, x=8, y=8, background="rgba(0,0,0,0.35)"),
            text(score_text, x=14, y=11),
            button("Jump", x=16, y=320, on_click=lambda: jump()),
            button("Reset", x=96, y=320, on_click=lambda: reset_game()),
            width=640,
            height=360,
            layout="free",
            fill_viewport=True,
            background="#87ceeb",
        )


app = App(screens=[Runner], initial="Runner")
