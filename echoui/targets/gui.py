"""PySide6 GUI target — IR → QWidget tree (reuses desktop renderer)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from echoui.compiler.analyzer import analyze
from echoui.compiler.lower import lower_web
from echoui.compiler.optimizer import optimize
from echoui.compiler.parser import parse_app


def build_gui(app: Any, *, out_dir: str = "dist/gui") -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    parsed = parse_app(app)
    lowered = lower_web(optimize(analyze(parsed)))
    (out / "app.json").write_text(json.dumps(parsed["ir"], indent=2, default=str), encoding="utf-8")
    (out / "lowered.json").write_text(json.dumps(lowered["nodes"], indent=2, default=str), encoding="utf-8")
    (out / "run.py").write_text(_GUI_RUNNER, encoding="utf-8")
    return str(out.resolve())


_GUI_RUNNER = '''"""Generated GUI runner — renders lowered IR via desktop Qt tree."""
import json
import sys
from pathlib import Path

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
except ImportError:
    raise SystemExit("pip install echoui[gui]")


def main():
    root = Path(__file__).resolve().parent
    lowered_path = root / "lowered.json"
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("EchoUI GUI")
    if lowered_path.exists():
        from echoui.targets.desktop import render_qt_tree

        data = json.loads(lowered_path.read_text(encoding="utf-8"))
        # Prefer first screen root if nodes is a list
        node = data[0] if isinstance(data, list) and data else data
        if isinstance(node, dict) and "children" in node and node.get("role") in (None, "screen", "stage"):
            # use as-is
            pass
        win.setCentralWidget(render_qt_tree(node if isinstance(node, dict) else {"role": "box", "props": {}, "children": []}))
    else:
        win.setCentralWidget(QLabel("EchoUI GUI — missing lowered.json"))
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
'''
