"""Build orchestration for all compile targets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from echoui.compiler.analyzer import analyze
from echoui.compiler.emit_web import emit_web
from echoui.compiler.lower import lower_web
from echoui.compiler.optimizer import optimize
from echoui.compiler.parser import collect_all_handlers, parse_app
from echoui.compiler.ssr import render_ssr


def build_target(app: Any, *, target: str = "web", out_dir: str = "dist/web", **kwargs: Any) -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    if target == "web":
        return _build_web(app, out)

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


def _build_web(app: Any, out: Path) -> str:
    screens = list(app.screens.keys())
    saved = app._current
    handlers, click_map, dom_handlers = collect_all_handlers(app)
    runtime_written = False
    for name in screens:
        app.switch_screen(name)
        parsed = parse_app(app)
        parsed["handlers"] = handlers
        parsed["click_map"] = click_map
        parsed["dom_handlers"] = dom_handlers
        analyzed = analyze(parsed)
        optimized = optimize(analyzed)
        lowered = lower_web(optimized)
        ssr = render_ssr(lowered)
        files = emit_web(lowered, ssr_html=ssr)
        fname = "index.html" if name == app.initial else f"{name.lower()}.html"
        (out / fname).write_text(files["index.html"], encoding="utf-8")
        if not runtime_written:
            (out / "runtime.js").write_text(files["runtime.js"], encoding="utf-8")
            runtime_written = True
    app.switch_screen(saved)
    manifest = {"target": "web", "screens": screens}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (out / "screens.json").write_text(json.dumps(screens), encoding="utf-8")
    _write_pwa(out, title=app.title)
    return str(out.resolve())


def _write_pwa(out: Path, *, title: str = "EchoUI App") -> None:
    short = title if len(title) <= 12 else title[:12].rstrip()
    manifest = {
        "name": title,
        "short_name": short,
        "start_url": ".",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#6200EE",
    }
    (out / "manifest.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    sw = "self.addEventListener('install',function(e){self.skipWaiting();});"
    (out / "sw.js").write_text(sw, encoding="utf-8")
