from echoui import App, Screen, Sprite, Store, button, text
from echoui.layout import box
from echoui.stage import stage


class GameStore(Store):
    x: float = 120.0
    y: float = 80.0


store = GameStore()


class Hero(Sprite):
    role = "box"

    def build(self):
        return box(width=32, height=32, background="#6200EE")


class Arena(Screen):
    layout = "free"

    def build(self):
        hero = Hero().move_to(store.x, store.y)
        return stage(
            box(width=640, height=360, x=0, y=0, background="#101020"),
            hero,
            text(lambda: f"Hero @ ({store.x:.0f}, {store.y:.0f})", x=12, y=12),
            button("Move right", x=12, y=320, on_click=lambda: setattr(store, "x", store.x + 24)),
            width=640,
            height=360,
            layout="free",
        )


app = App(screens=[Arena], initial="Arena")
