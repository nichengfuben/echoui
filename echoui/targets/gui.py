"""PySide6 GUI target."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from echoui.compiler.parser import parse_app


def build_gui(app: Any, *, out_dir: str = "dist/gui") -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    parsed = parse_app(app)
    (out / "app.json").write_text(json.dumps(parsed["ir"], indent=2, default=str), encoding="utf-8")
    (out / "run.py").write_text(_GUI_RUNNER, encoding="utf-8")
    return str(out.resolve())


_GUI_RUNNER = '''"""Generated GUI runner."""
import sys
try:
    from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
except ImportError:
    raise SystemExit("pip install echoui[gui]")

def main():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("EchoUI GUI")
    layout = QVBoxLayout(w)
    layout.addWidget(QLabel("EchoUI GUI"))
    layout.addWidget(QPushButton("OK"))
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
'''
