"""CLI entry path loading tests."""

from __future__ import annotations

from watchfiles import Change

from echoui.cli import _dev_watch_filter, _load_app


def test_dev_watch_filter_ignores_dist():
    filt = _dev_watch_filter()
    assert filt(Change.modified, r"game\dist\web\index.html") is False
    assert filt(Change.modified, r"game\main.py") is True


def test_load_app_multi_file_example():
    mod = _load_app("examples/06_runner/main.py")
    assert hasattr(mod, "screens")
    assert mod.initial == "Runner"
