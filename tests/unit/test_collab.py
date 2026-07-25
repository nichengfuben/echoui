"""CRDT collaboration tests."""

from __future__ import annotations

from echoui.collab import CRDTMap, LWWRegister, Session


def test_lww_register_takes_latest():
    reg = LWWRegister(value="a", timestamp=1)
    reg.set("b", 2)
    assert reg.value == "b"
    reg.set("c", 1)
    assert reg.value == "b"


def test_crdt_map_merge():
    left = CRDTMap()
    left.set("x", 1, 1.0)
    right = CRDTMap()
    right.set("x", 2, 2.0)
    left.merge(right)
    assert left.get("x") == 2


def test_session_sync():
    a = Session()
    b = Session()
    a.apply_op("score", 10, 1.0)
    b.sync(a)
    assert b.doc.get("score") == 10
