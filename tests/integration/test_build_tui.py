"""TUI build integration test."""

from echoui import App, Screen, Store, button, col, text
from echoui.targets.tui import build_tui


class CounterStore(Store):
    count: int = 0


store = CounterStore()


class Counter(Screen):
    def build(self):
        return col(
            text(lambda: f"Count: {store.count}"),
            button("+1", on_click=lambda: setattr(store, "count", store.count + 1)),
        )


app = App(screens=[Counter], initial="Counter")


def test_build_tui_writes_json(tmp_path):
    build_tui(app, out_dir=str(tmp_path / "tui"))
    assert (tmp_path / "tui" / "app.json").exists()
    assert (tmp_path / "tui" / "main.py").exists()
