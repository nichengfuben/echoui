"""SyncRelay broadcast tests."""

from echoui.collab import Session, SyncRelay


def test_sync_relay_broadcast():
    relay = SyncRelay()
    a = Session(peer_id="a")
    b = Session(peer_id="b")
    relay.join(a)
    relay.join(b)
    relay.broadcast(a, "score", 42)
    assert b.doc.get("score") == 42


def test_sync_relay_initial_merge():
    relay = SyncRelay()
    a = Session(peer_id="a")
    a.apply_op("x", 1, 1.0)
    b = Session(peer_id="b")
    relay.join(a)
    relay.join(b)
    assert b.doc.get("x") == 1
