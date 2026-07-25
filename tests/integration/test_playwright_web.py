"""Playwright: built static page loads and compile-local counter works."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

pytest.importorskip("playwright")
from playwright.sync_api import sync_playwright  # noqa: E402

from echoui.compiler.bundler import build_target


def _build_counter(tmp_path: Path) -> Path:
    root = Path(__file__).resolve().parents[2] / "examples" / "02_counter"
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("ctr", root / "main.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = tmp_path / "web"
    build_target(mod.app, target="web", out_dir=str(out))
    return out


def test_playwright_counter_click(tmp_path):
    out = _build_counter(tmp_path)
    index = out / "index.html"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(index.as_uri())
        page.wait_for_function("window.__ECHoui_CFG && window.__echoui")
        before = page.locator(".e-text").first.inner_text()
        page.locator("button").first.click()
        page.wait_for_timeout(100)
        after = page.locator(".e-text").first.inner_text()
        browser.close()
    assert before != after or "1" in after


def test_playwright_escape_layer_signal(tmp_path):
    root = Path(__file__).resolve().parents[2] / "examples" / "05_escape_layer"
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location("esc", root / "main.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out = tmp_path / "web"
    build_target(mod.app, target="web", out_dir=str(out))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto((out / "index.html").as_uri())
        page.wait_for_function("window.__ECHoui_CFG")
        assert page.locator("body").inner_text()
        browser.close()
