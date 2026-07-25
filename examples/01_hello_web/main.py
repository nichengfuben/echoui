from echoui import App, Screen, col, text


class Hello(Screen):
    def build(self):
        return col(
            text("Hello, EchoUI!"),
            text("Build with: echoui build --target web"),
        )


app = App(screens=[Hello], initial="Hello")
