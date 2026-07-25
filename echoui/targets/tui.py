"""Textual TUI target."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from echoui.compiler.parser import parse_app


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items() if not str(k).startswith("_handler")}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if callable(value):
        return {"type": "fn", "name": getattr(value, "__name__", "lambda")}
    return value


def build_tui(app: Any, *, out_dir: str = "dist/tui") -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    parse_app(app)
    screens = {n: _json_safe(sc().to_ir().to_dict()) for n, sc in app.screens.items()}
    payload = _json_safe({"screens": screens, "initial": app.initial})
    (out / "app.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tui_main = _TUI_RUNNER
    (out / "main.py").write_text(tui_main, encoding="utf-8")
    return str(out.resolve())


_TUI_RUNNER = '''"""Generated TUI runner."""
try:
    from textual.app import App as TextualApp
    from textual.widgets import Static, Button
    from textual.containers import Vertical
except ImportError:
    raise SystemExit("pip install echoui[tui]")

class EchoTuiApp(TextualApp):
    def compose(self):
        yield Vertical(Static("EchoUI TUI"), Button("Quit", id="quit"))

    def on_button_pressed(self, event):
        if event.button.id == "quit":
            self.exit()

if __name__ == "__main__":
    EchoTuiApp().run()
'''
