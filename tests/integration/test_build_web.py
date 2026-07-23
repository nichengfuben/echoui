"""Web build integration tests."""


from echoui import App, Screen, Store, button, col, text
from echoui.compiler.bundler import build_target


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


def test_build_web_manifest(tmp_path):
    out = tmp_path / "dist"
    build_target(app, target="web", out_dir=str(out))
    assert (out / "index.html").exists()
    assert (out / "manifest.json").exists()
    assert (out / "manifest.webmanifest").exists()
    assert (out / "sw.js").exists()


def test_build_web_runtime_size(tmp_path):
    out = tmp_path / "dist"
    build_target(app, target="web", out_dir=str(out))
    runtime = (out / "runtime.js").read_text(encoding="utf-8")
    assert len(runtime) < 4096
