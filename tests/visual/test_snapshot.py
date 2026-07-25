"""Visual snapshot tests."""

from echoui import App, Screen, Store, button, col, text
from echoui.testing import mount, snapshot


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


def test_counter_snapshot_stable():
    mounted = mount(app)
    snap = snapshot(mounted)
    assert "Count: 0" in snap
    assert "<button" in snap or 'role="button"' in snap or "button" in snap
