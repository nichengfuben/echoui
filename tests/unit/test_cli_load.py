"""CLI entry path loading tests."""

from __future__ import annotations

from echoui.cli import _load_app


def test_load_app_multi_file_example():
    mod = _load_app("examples/06_runner/main.py")
    assert hasattr(mod, "screens")
    assert mod.initial == "Runner"
