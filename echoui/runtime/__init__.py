"""EchoUI per-target runtimes."""

from __future__ import annotations

from pathlib import Path

RUNTIME_WEB_DIR = Path(__file__).parent / "web"
_WEB_PARTS = ("core.js", "storage.js", "webgpu.js", "widgets.js", "audio.js", "platform.js", "ui.js", "gestures.js")


def load_web_runtime(*, minify: bool = True) -> str:
    source = "\n".join((RUNTIME_WEB_DIR / name).read_text(encoding="utf-8") for name in _WEB_PARTS)
    if not minify:
        return source
    try:
        import rjsmin

        return rjsmin.jsmin(source)
    except ImportError:
        return source
