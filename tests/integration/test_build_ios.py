"""iOS web bundle target (macOS CI packages WKWebView assets)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from echoui.compiler.bundler import build_target


def _load_runner():
    root = Path(__file__).resolve().parents[2] / "examples" / "06_runner"
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("runner", root / "main.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.app


def test_build_ios_bundle(tmp_path):
    app = _load_runner()
    out = tmp_path / "ios"
    path = build_target(app, target="ios", out_dir=str(out))
    root = Path(path)
    assert (root / "web" / "index.html").is_file()
    assert (root / "Info.plist.json").is_file()
    assert (root / "README.txt").is_file()
