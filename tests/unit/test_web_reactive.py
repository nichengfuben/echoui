"""Web reactive compile tests."""

from __future__ import annotations

from echoui import App, Screen, Store, button, col, text
from echoui.compiler.bundler import build_target
from echoui.compiler.client_cfg import build_client_cfg
from echoui.compiler.emit_actions import compile_handler
from echoui.compiler.parser import parse_app
from echoui.testing import mount


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


def _inc_count() -> None:
    setattr(store, "count", store.count + 1)


def test_compile_actions_inc():
    action = compile_handler(_inc_count)
    assert action == {"k": "inc", "s": "CounterStore.count", "by": 1, "local": True}


def test_client_cfg_has_signals_and_bindings(tmp_path):
    Store.reset_registry()
    CounterStore()
    build_target(app, target="web", out_dir=str(tmp_path / "dist"))
    parsed = parse_app(app)
    from echoui.compiler.analyzer import analyze
    from echoui.compiler.lower import lower_web
    from echoui.compiler.optimizer import optimize

    lowered = lower_web(optimize(analyze(parsed)))
    cfg = build_client_cfg(lowered)
    assert "CounterStore.count" in cfg["signals"]
    assert cfg["bindings"]
    assert cfg["actions"]


def test_build_emits_runtime_and_cfg(tmp_path):
    out = tmp_path / "dist"
    build_target(app, target="web", out_dir=str(out))
    html = (out / "index.html").read_text(encoding="utf-8")
    runtime = (out / "runtime.js").read_text(encoding="utf-8")
    assert "runtime.js" in html
    assert "__ECHoui_CFG" in html
    assert "local_exec" in html
    assert "/api/action" not in runtime
    assert "/api/frame" not in runtime
    assert "fetch(" not in runtime
    assert len(runtime) < 16384  # core + storage + webgpu + widgets + audio + platform + ui


def test_mount_counter_click_updates_snapshot():
    Store.reset_registry()
    store2 = CounterStore()
    store2.count = 0
    m = mount(app)
    before = m.snapshot()
    btn = next(n.id for n in _walk(m.root) if n.tag == "button")
    m.fire(btn, "click")
    after = m.snapshot()
    assert before != after or "Count: 1" in after


def _walk(node):
    yield node
    for c in node.children:
        yield from _walk(c)
