"""Pytest configuration."""

from __future__ import annotations

import pytest

from echoui.state import Store


@pytest.fixture(autouse=True)
def _reset_store_registry():
    Store.reset_registry()
    yield
    Store.reset_registry()
