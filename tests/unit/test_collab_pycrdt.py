"""Optional pycrdt backend tests."""

from __future__ import annotations

import pytest

pycrdt = pytest.importorskip("pycrdt")

from echoui.collab import PyCRDTSession, merge_updates  # noqa: E402


def test_pycrdt_session_set_get():
    s = PyCRDTSession(peer_id="a")
    s.set("score", 10)
    assert s.get("score") == 10
    assert "score" in s.keys()


def test_pycrdt_merge_updates():
    a = PyCRDTSession(peer_id="a")
    a.set("x", 1)
    u1 = a.encode_update()
    b = PyCRDTSession(peer_id="b")
    b.set("y", 2)
    u2 = b.encode_update()
    merged = merge_updates(u1, u2)
    c = PyCRDTSession(peer_id="c")
    c.apply_update(merged)
    assert c.get("x") == 1
    assert c.get("y") == 2
