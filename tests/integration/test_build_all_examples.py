"""Build all shipped examples (web + static)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from echoui.compiler.bundler import build_target

EXAMPLES = [
    "01_hello_web",
    "02_counter",
    "03_game_free_mode",
    "04_multi_screen_game",
    "05_escape_layer",
    "06_runner",
    "07_full_web",
    "08_media",
]


def _load_app(example_dir: Path):
    main = example_dir / "main.py"
    sys.path.insert(0, str(example_dir))
    spec = importlib.util.spec_from_file_location(f"ex_{example_dir.name}", main)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.app


def test_all_examples_build_web_and_static(tmp_path):
    root = Path(__file__).resolve().parents[2] / "examples"
    for name in EXAMPLES:
        app = _load_app(root / name)
        web_out = tmp_path / name / "web"
        static_out = tmp_path / name / "static"
        build_target(app, target="web", out_dir=str(web_out))
        build_target(app, target="static", out_dir=str(static_out))
        assert (web_out / "index.html").exists()
        assert (web_out / "runtime.js").exists()
        assert (static_out / "index.html").exists()
        if name == "04_multi_screen_game":
            assert (web_out / "game.html").exists()
