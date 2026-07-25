"""Smoke test for iOS web bundle build (used by CI)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "examples" / "06_runner"
sys.path.insert(0, str(root.resolve()))
spec = importlib.util.spec_from_file_location("runner", root / "main.py")
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
out = Path("dist/ios/runner")
mod.app.compile(target="ios", out_dir=str(out))
assert (out / "web" / "index.html").exists()
print("iOS web bundle ready for WKWebView shell")
