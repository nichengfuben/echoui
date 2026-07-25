"""Collaborative document: Doc, presence, and awareness."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from echoui.collab._core import Session, SyncRelay


@dataclass
class Presence:
    peer_id: str
    name: str = ""
    cursor: Tuple[float, float] = (0.0, 0.0)
    color: str = "#6200EE"
    updated_at: float = field(default_factory=time.time)


@dataclass
class Awareness:
    """Who is connected and where their cursor is."""

    peers: Dict[str, Presence] = field(default_factory=dict)

    def update(self, peer_id: str, *, name: str = "", cursor: Tuple[float, float] = (0, 0)) -> None:
        p = self.peers.get(peer_id) or Presence(peer_id=peer_id)
        if name:
            p.name = name
        p.cursor = cursor
        p.updated_at = time.time()
        self.peers[peer_id] = p

    def remove(self, peer_id: str) -> None:
        self.peers.pop(peer_id, None)

    def list_peers(self) -> List[Presence]:
        return list(self.peers.values())


class Doc:
    """Shared CRDT document with optional presence."""

    def __init__(
        self,
        *,
        peer_id: str = "",
        session: Optional[Session] = None,
        relay: Optional[SyncRelay] = None,
        on_change: Optional[Callable[[str, Any], None]] = None,
    ) -> None:
        self.session = session or Session(peer_id=peer_id, on_change=on_change)
        self.session.peer_id = peer_id or self.session.peer_id
        self.awareness = Awareness()
        self.relay = relay
        if relay:
            relay.join(self.session)
        if peer_id:
            self.awareness.update(peer_id, name=peer_id)

    def set(self, key: str, value: Any) -> None:
        self.session.apply_op(key, value)
        if self.relay:
            self.relay.broadcast(self.session, key, value)

    def get(self, key: str, default: Any = None) -> Any:
        val = self.session.doc.get(key)
        return default if val is None else val

    def set_cursor(self, x: float, y: float) -> None:
        pid = self.session.peer_id or "local"
        self.awareness.update(pid, cursor=(x, y))

    def merge_remote(self, other: "Doc") -> None:
        self.session.sync(other.session)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "doc": self.session.snapshot(),
            "awareness": {p.peer_id: {"name": p.name, "cursor": p.cursor} for p in self.awareness.list_peers()},
        }
