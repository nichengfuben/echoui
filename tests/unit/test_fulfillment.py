"""PLAN fulfillment — runtime bundle, production widgets, storage, WebGPU."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from echoui import App, Screen, Store, on, stage
from echoui.bridge import gpu_api, web_api
from echoui.compiler.analyzer import analyze
from echoui.compiler.bundler import build_target
from echoui.compiler.client_cfg import build_client_cfg
from echoui.compiler.emit_web import _render_chart, _render_map
from echoui.compiler.lower import lower_web
from echoui.compiler.optimizer import optimize
from echoui.compiler.parser import parse_app
from echoui.layout import box
from echoui.runtime import load_web_runtime
from echoui.storage import web_sqlite


def test_runtime_bundle_includes_extensions():
    src = load_web_runtime(minify=False)
    assert "loadFrameScript" in src
    assert "__echoui.storage" in src
    assert "__echoui.webgpu" in src
    assert "__echoui.widgets" in src


def test_production_chart_emits_chartjs():
    html = _render_chart(
        {"id": "c1", "props": {"data": [1, 2, 3], "width": 200, "height": 100, "production": True}}
    )
    assert "e-chartjs" in html
    assert "data-values" in html


def test_production_map_emits_maplibre():
    html = _render_map({"id": "m1", "props": {"lat": 1, "lng": 2, "width": 100, "height": 80}})
    assert "e-maplibre" in html
    assert "data-lat" in html


def test_web_sqlite_memory_backend():
    db = web_sqlite()
    db.set("k", "v")
    assert db.get("k") == "v"
    db.delete("k")
    assert db.get("k") is None


def test_gpu_api_web():
    api = gpu_api()
    assert api.backend() == "webgpu"
    assert api.supports() is True


def test_os_api_raises():
    from echoui.bridge import os_api
    from echoui.exceptions import UnsupportedCapability

    with pytest.raises(UnsupportedCapability):
        os_api()


def test_web_api_storage_roundtrip():
    api = web_api()
    api.local_storage_set("x", "1")
    assert api.local_storage_get("x") == "1"


def test_ssr_resume_in_web_build(tmp_path):
    root = Path(__file__).resolve().parents[2] / "examples" / "02_counter"
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("ctr", root / "main.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = tmp_path / "web"
    build_target(mod.app, target="web", out_dir=str(out))
    html = (out / "index.html").read_text(encoding="utf-8")
    assert "__echoui_resume" in html
    assert "resumeCfg" in (out / "runtime.js").read_text(encoding="utf-8")


def test_webgpu_backend_in_client_cfg():
    class GameStore(Store):
        x: float = 0

    gs = GameStore()

    class Game(Screen):
        layout = "free"

        @on("frame")
        def loop(self, dt: float) -> None:
            gs.x += dt

        def build(self):
            return stage(
                box(width=32, height=32, x=0, y=0, background="#0f0"),
                width=320,
                height=240,
                layout="free",
                gpu_backend="webgpu",
            )

    Store.reset_registry()
    GameStore()
    cfg = build_client_cfg(lower_web(optimize(analyze(parse_app(App(screens=[Game], initial="Game"))))))
    assert cfg.get("gpu", {}).get("backend") == "webgpu"


def test_full_web_example_builds(tmp_path):
    root = Path(__file__).resolve().parents[2] / "examples" / "07_full_web"
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("full", root / "main.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = tmp_path / "web"
    build_target(mod.app, target="web", out_dir=str(out))
    html = (out / "index.html").read_text(encoding="utf-8")
    assert "e-chartjs" in html
    assert "e-maplibre" in html
    assert "e-save-dash" in html
