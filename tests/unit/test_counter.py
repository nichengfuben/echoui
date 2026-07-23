"""Counter example integration tests."""

from echoui import App, Screen, Store, button, col, text
from echoui.testing import mount


class CounterStore(Store):
    count: int = 0


def test_counter_increments():
    store = CounterStore()

    class Counter(Screen):
        def build(self):
            return col(
                text(lambda: f"Count: {store.count}"),
                button("+1", on_click=lambda: setattr(store, "count", store.count + 1)),
            )

    app = App(screens=[Counter], initial="Counter")
    m = mount(app)
    assert "Count: 0" in m.snapshot()

    btn_id = _find_button(m)
    m.fire(btn_id)
    assert "Count: 1" in m.snapshot()
    m.fire(btn_id)
    assert "Count: 2" in m.snapshot()


def _find_button(m):
    def walk(node):
        if node.tag == "button":
            return node.id
        for child in node.children:
            found = walk(child)
            if found:
                return found
        return None

    btn_id = walk(m.root)
    if btn_id:
        return btn_id
    raise AssertionError("button not found")
