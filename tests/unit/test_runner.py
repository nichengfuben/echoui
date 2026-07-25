"""Runner example compile and tick tests."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from echoui import Store
from echoui.compiler.analyzer import analyze
from echoui.compiler.client_cfg import build_client_cfg
from echoui.compiler.lower import lower_web
from echoui.compiler.optimizer import optimize
from echoui.compiler.parser import parse_app
from echoui.testing import mount, tick


def _load_runner():
    import sys

    example_dir = Path(__file__).resolve().parents[2] / "examples" / "06_runner"
    root = example_dir / "main.py"
    sys.path.insert(0, str(example_dir))
    spec = importlib.util.spec_from_file_location("runner_main", root)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_runner_keymap_and_frames():
    mod = _load_runner()
    Store.reset_registry()
    mod.RunnerStore()
    parsed = analyze(parse_app(mod.app))
    cfg = build_client_cfg(lower_web(optimize(parsed)))
    assert cfg["frames"] is True
    assert cfg["keymap"].get("Space")
    assert cfg["keymap"].get("KeyR")
    assert "RunnerStore.player_y" in cfg["signals"]


def test_runner_actions_compile_local():
    """PLAN §34: jump/reset compile to local JS — no runtime Python round-trip."""
    mod = _load_runner()
    Store.reset_registry()
    mod.RunnerStore()
    parsed = analyze(parse_app(mod.app))
    cfg = build_client_cfg(lower_web(optimize(parsed)))
    actions = cfg["actions"]
    assert actions, "handlers must compile to local actions"
    space_h = cfg["keymap"]["Space"]
    reset_h = cfg["keymap"]["KeyR"]
    assert actions[space_h]["local"] is True
    assert actions[reset_h]["local"] is True
    assert "script" in actions[space_h]
    assert "RunnerStore.vy" in actions[space_h]["script"]
    assert "RunnerStore.grounded" in actions[space_h]["script"]
    assert "RunnerStore.player_y" in actions[reset_h]["script"]


def test_runner_tick_advances_score():
    mod = _load_runner()
    Store.reset_registry()
    s = mod.RunnerStore()
    s.score = 0
    m = mount(mod.app)
    tick(m, 3)
    assert s.score > 0


def test_runner_viewport_fill(tmp_path):
    mod = _load_runner()
    Store.reset_registry()
    mod.RunnerStore()
    from echoui.compiler.bundler import build_target

    out = tmp_path / "web"
    build_target(mod.app, target="web", out_dir=str(out))
    html = (out / "index.html").read_text(encoding="utf-8")
    assert "e-fill" in html
    assert "e-stage-inner" in html
    assert "fitStage" in (out / "runtime.js").read_text(encoding="utf-8")


def test_runner_sss_tree():
    """PLAN §1: Screen → Stage → Sprite; no flow col wrapping stage."""
    mod = _load_runner()
    Store.reset_registry()
    mod.RunnerStore()
    root = parse_app(mod.app)["root"]
    assert root.role == "screen"
    assert root.props.get("layout") == "free"
    assert len(root.children) == 1
    assert root.children[0].role == "stage"
    for child in root.children:
        assert child.role != "box" or child.props.get("direction") != "col"
