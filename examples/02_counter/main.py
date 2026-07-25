from echoui import App, Screen, Store, button, col, text


class CounterStore(Store):
    count: int = 0


store = CounterStore()


def increment_count() -> None:
    s = CounterStore()
    s.count = s.count + 1


class Counter(Screen):
    def build(self):
        return col(
            text(lambda: f"Count: {store.count}"),
            button("+1", on_click=increment_count),
        )


app = App(screens=[Counter], initial="Counter")
