"""Pytest configuration."""

from __future__ import annotations

import pytest

from echoui.state import Store


@pytest.fixture(autouse=True)
def _no_proxy_for_localhost(monkeypatch):
    """Avoid system HTTP proxy breaking urllib tests against 127.0.0.1."""
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("NO_PROXY", "127.0.0.1,localhost")
    monkeypatch.setenv("no_proxy", "127.0.0.1,localhost")
    yield


@pytest.fixture(autouse=True)
def _reset_store_registry():
    Store.reset_registry()
    yield
    Store.reset_registry()
