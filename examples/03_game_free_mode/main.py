from echoui import App, Screen, Sprite, Store, button, col, text
from echoui.layout import box
from echoui.stage import stage


class GameStore(Store):
    x: float = 120.0
    y: float = 80.0


store = GameStore()


class Hero(Sprite):
    role = "box"

    def build(self):
        return box(width=32, height=32)


class Arena(Screen):
    def build(self):
        return col(
            stage(
                Hero().move_to(store.x, store.y),
                width=640,
                height=360,
                layout="free",
            ),
            button("Move right", on_click=lambda: setattr(store, "x", store.x + 24)),
            text(lambda: f"Free mode hero @ ({store.x:.0f}, {store.y:.0f})"),
        )


app = App(screens=[Arena], initial="Arena")
