from echoui import App, Screen, Sprite, Stage, Store, button, col, row, text
from echoui.router import Router


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
        return col(text(lambda: f"Score: {store.score}"))

class Game(Screen):
    name = "Game"

    def build(self):
        return col(
            Stage(
                Player().move_to(100, 200),
                width=800,
                height=600,
                layout="free",
            ),
            row(
                button("+10", on_click=lambda: setattr(store, "score", store.score + 10)),
                button("Home", on_click=lambda: router.navigate("/")),
            ),
        )

app = App(screens=[Home, Game], initial="Home")
