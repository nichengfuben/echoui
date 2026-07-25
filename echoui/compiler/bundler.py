"""Build orchestration for all compile targets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from echoui.compiler.analyzer import analyze
from echoui.compiler.emit_web import emit_web
from echoui.compiler.lower import lower_web
from echoui.compiler.optimizer import optimize
from echoui.compiler.parser import parse_app
from echoui.compiler.ssr import render_ssr


def build_target(app: Any, *, target: str = "web", out_dir: str = "dist/web", **kwargs: Any) -> str:
    parsed = parse_app(app)
    analyzed = analyze(parsed)
    optimized = optimize(analyzed)
    lowered = lower_web(optimized)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    if target == "web":
        ssr = render_ssr(lowered)
        files = emit_web(lowered, ssr_html=ssr)
        for name, content in files.items():
            (out / name).write_text(content, encoding="utf-8")
        manifest = {"target": "web", "screens": list(app.screens.keys())}
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        _write_pwa(out)
        return str(out.resolve())

    if target == "static":
        from echoui.targets.static import build_static

        return build_static(app, out_dir=out_dir)

    if target == "tui":
        from echoui.targets.tui import build_tui

        return build_tui(app, out_dir=out_dir)

    if target == "desktop":
        from echoui.targets.desktop import build_desktop

        return build_desktop(app, out_dir=out_dir)

    if target == "gui":
        from echoui.targets.gui import build_gui

        return build_gui(app, out_dir=out_dir)

    if target == "android":
        from echoui.targets.mobile_android import build_android

        return build_android(app, out_dir=out_dir)

    if target == "ios":
        from echoui.targets.mobile_ios import build_ios

        return build_ios(app, out_dir=out_dir)

    raise ValueError(f"Unknown target: {target}")


def _write_pwa(out: Path) -> None:
    manifest = {
        "name": "EchoUI App",
        "short_name": "EchoUI",
        "start_url": ".",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#6200EE",
    }
    (out / "manifest.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    sw = "self.addEventListener('install',function(e){self.skipWaiting();});"
    (out / "sw.js").write_text(sw, encoding="utf-8")
