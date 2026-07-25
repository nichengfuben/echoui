"""Full web compile tests — DOM, frame local, GPU, advanced roles."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from echoui import App, Screen, Store, chart, col, gantt, map, on
from echoui.compiler.analyzer import analyze
from echoui.compiler.bundler import build_target
from echoui.compiler.client_cfg import build_client_cfg
from echoui.compiler.lower import lower_web
from echoui.compiler.optimizer import optimize
from echoui.compiler.parser import parse_app
from echoui.layout import box as layout_box
from echoui.testing import mount


class DashStore(Store):
    value: int = 1


store = DashStore()


class HoverBox(Screen):
    @on("hover_enter")
    def hi(self, event) -> None:
        DashStore().value += 1

    def build(self):
        return layout_box(text="hover me", width=120, height=40, background="#eee")


class Dashboard(Screen):
    def build(self):
        return col(
            chart(data=[5, 9, 4, 12], width=200, height=120),
            map(lat=31.2, lng=121.5, width=180, height=100),
            gantt(tasks=[{"name": "A", "start": 0, "end": 2}], width=220, height=80),
        )


hover_app = App(screens=[HoverBox], initial="HoverBox")
dash_app = App(screens=[Dashboard], initial="Dashboard")


def _load_runner():
    example_dir = Path(__file__).resolve().parents[2] / "examples" / "06_runner"
    sys.path.insert(0, str(example_dir))
    spec = importlib.util.spec_from_file_location("runner_main", example_dir / "main.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_dom_handlers_collected():
    Store.reset_registry()
    DashStore()
    parsed = analyze(parse_app(hover_app))
    assert any(d["type"] == "hover_enter" for d in parsed["dom_handlers"])


def test_dom_handlers_compile_local():
    Store.reset_registry()
    DashStore()
    parsed = analyze(parse_app(hover_app))
    hid = parsed["dom_handlers"][0]["handler"]
    action = parsed["actions"][hid]
    assert action["local"] is True
    assert "DashStore.value" in action.get("script", "")


def test_dom_hover_fire_updates_store():
    Store.reset_registry()
    s = DashStore()
    s.value = 1
    m = mount(hover_app)
    screen_id = m.root.id
    m.fire(screen_id, "hover_enter")
    assert s.value == 2


def test_runner_frame_script_compiles():
    mod = _load_runner()
    Store.reset_registry()
    mod.RunnerStore()
    parsed = analyze(parse_app(mod.app))
    js = parsed.get("frame_script")
    assert js and "__echoui_frame" in js
    assert "obs" in js


def test_runner_free_gpu_cfg():
    mod = _load_runner()
    Store.reset_registry()
    mod.RunnerStore()
    cfg = build_client_cfg(lower_web(optimize(analyze(parse_app(mod.app)))))
    assert cfg.get("gpu")
    assert cfg["gpu"]["nodes"]


def test_runner_web_has_gpu_canvas(tmp_path):
    mod = _load_runner()
    Store.reset_registry()
    mod.RunnerStore()
    out = tmp_path / "web"
    build_target(mod.app, target="web", out_dir=str(out))
    html = (out / "index.html").read_text(encoding="utf-8")
    assert 'id="gpu-' in html
    assert "width:640px" in html
    assert "height:60px" in html or "height:32px" in html


def test_runner_frame_script_spawns_obstacles():
    mod = _load_runner()
    Store.reset_registry()
    mod.RunnerStore()
    parsed = analyze(parse_app(mod.app))
    js = parsed.get("frame_script") or ""
    assert "660" in js


def test_static_build_has_frame_local(tmp_path):
    mod = _load_runner()
    Store.reset_registry()
    mod.RunnerStore()
    out = tmp_path / "static"
    build_target(mod.app, target="static", out_dir=str(out))
    html = (out / "index.html").read_text(encoding="utf-8")
    runtime = (out / "runtime.js").read_text(encoding="utf-8")
    assert "frame_local" in html or "frame_script" in html
    assert (out / "runtime.js").exists()
    assert "wireD" in runtime
    assert "gpu" in runtime


def test_advanced_roles_emit(tmp_path):
    out = tmp_path / "web"
    build_target(dash_app, target="web", out_dir=str(out))
    html = (out / "index.html").read_text(encoding="utf-8")
    assert "e-chartjs" in html
    assert "e-maplibre" in html
    assert "e-gantt" in html


def test_desktop_build_writes_lowered(tmp_path):
    from echoui import App, Screen, col
    from echoui import text as ui_text

    class Hello(Screen):
        def build(self):
            return col(ui_text("Hello desktop"))

    app = App(screens=[Hello], initial="Hello")
    build_target(app, target="desktop", out_dir=str(tmp_path / "desk"))
    assert (tmp_path / "desk" / "lowered.json").exists()
