"""Android mobile target template."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol


class MobileBuilder(Protocol):
    def build(self, app: Any, out_dir: str) -> str: ...


def build_android(app: Any, *, out_dir: str = "dist/android") -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    manifest = {
        "package": "com.echoui.app",
        "screens": list(app.screens.keys()),
        "initial": app.initial,
    }
    (out / "AndroidManifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (out / "MainActivity.kt.template").write_text(_KOTLIN_TEMPLATE, encoding="utf-8")
    return str(out.resolve())


_KOTLIN_TEMPLATE = """// EchoUI Android template
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Load EchoUI webview or native bridge
    }
}
"""
