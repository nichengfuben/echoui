"""iOS mobile target template (macOS CI build)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_ios(app: Any, *, out_dir: str = "dist/ios") -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    app.compile(target="web", out_dir=str(out / "web"))
    manifest = {
        "bundle": "com.echoui.app",
        "screens": list(app.screens.keys()),
        "initial": app.initial,
    }
    (out / "Info.plist.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (out / "README.txt").write_text(
        "EchoUI iOS shell: WKWebView loads dist/ios/web. Build .ipa on macOS CI.",
        encoding="utf-8",
    )
    return str(out.resolve())
