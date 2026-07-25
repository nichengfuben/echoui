from echoui import App, Screen, Sprite, Store, button, col, text
from echoui.layout import box
from echoui.router import Router
from echoui.stage import stage


class GameStore(Store):
    score: int = 0


store = GameStore()
router = Router()
router.add("/", "Home")
router.add("/game", "Game")


class Home(Screen):
    name = "Home"

    def build(self):
        return col(
            text("EchoUI Multi-Screen Demo"),
            button("Play Game", on_click=lambda: router.navigate("/game")),
        )


class Player(Sprite):
    role = "box"

    def build(self):
        return box(width=48, height=48, background="#2ecc71")


class Game(Screen):
    name = "Game"
    layout = "free"

    def build(self):
        return stage(
            box(width=800, height=600, x=0, y=0, background="#222"),
            Player().move_to(100, 200),
            text(lambda: f"Score: {store.score}", x=16, y=16),
            button("+10", x=16, y=560, on_click=lambda: setattr(store, "score", store.score + 10)),
            button("Home", x=96, y=560, on_click=lambda: router.navigate("/")),
            width=800,
            height=600,
            layout="free",
        )


app = App(screens=[Home, Game], initial="Home")
