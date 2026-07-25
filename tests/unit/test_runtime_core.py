"""Runtime core.js must register compiled frame handlers in IIFE scope."""

from __future__ import annotations

from echoui.runtime import load_web_runtime


def test_runtime_bundle_includes_extensions() -> None:
    src = load_web_runtime(minify=False)
    assert "frameFn" in src
    assert "loadFrameScript" in src
    assert "__echoui.storage" in src
    assert "__echoui.webgpu" in src
    assert "__echoui.widgets" in src
    assert "eval(c.frame_script)" not in src
