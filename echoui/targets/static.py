"""Static site generation target."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from echoui.compiler.analyzer import analyze
from echoui.compiler.emit_web import _render_nodes, emit_web
from echoui.compiler.lower import lower_web
from echoui.compiler.optimizer import optimize
from echoui.compiler.parser import collect_all_handlers, parse_app


def build_static(app: Any, *, out_dir: str = "dist/static") -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
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
        analyzed["static"] = True
        optimized = optimize(analyzed)
        lowered = lower_web(optimized)
        html_body = _render_nodes(lowered["nodes"], gpu=lowered.get("free_gpu"))
        files = emit_web(lowered, ssr_html=html_body)
        fname = "index.html" if name == app.initial else f"{name.lower()}.html"
        (out / fname).write_text(files["index.html"], encoding="utf-8")
        if not runtime_written:
            (out / "runtime.js").write_text(files["runtime.js"], encoding="utf-8")
            runtime_written = True
    app.switch_screen(saved)
    manifest_src = Path("dist/web")
    for extra in ("manifest.webmanifest", "manifest.json", "sw.js"):
        src = manifest_src / extra
        if src.exists():
            shutil.copy(src, out / extra)
    (out / "screens.json").write_text(json.dumps(screens), encoding="utf-8")
    return str(out.resolve())
