"""In-process RTC peer + DataChannel (test/collab bridge; not browser WebRTC)."""

from __future__ import annotations

import weakref
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

_peers: List[weakref.ref["RTCPeer"]] = []
_session_seq = 0


def _next_session() -> str:
    global _session_seq
    _session_seq += 1
    return f"sess-{_session_seq}"


def _live_peers() -> List["RTCPeer"]:
    out: List[RTCPeer] = []
    dead: List[int] = []
    for i, ref in enumerate(_peers):
        p = ref()
        if p is None:
            dead.append(i)
        else:
            out.append(p)
    for i in reversed(dead):
        del _peers[i]
    return out


@dataclass
class DataChannel:
    label: str
    on_message: Optional[Callable[[str], None]] = None
    peer: Optional["RTCPeer"] = field(default=None, repr=False)
    _remote: Optional["DataChannel"] = field(default=None, repr=False)

    def send(self, data: str) -> None:
        remote = self._remote
        if remote is None and self.peer is not None:
            remote = self.peer._find_remote_channel(self.label)
            self._remote = remote
        if remote is not None and remote.on_message is not None:
            remote.on_message(data)

    def pair(self, other: "DataChannel") -> None:
        self._remote = other
        other._remote = self


@dataclass
class RTCPeer:
    ice_servers: List[Dict[str, str]] = field(default_factory=list)
    channels: List[DataChannel] = field(default_factory=list)
    session_id: str = field(default_factory=_next_session)
    remote: Optional["RTCPeer"] = field(default=None, repr=False)
    _local_sdp: str = field(default="", repr=False)
    _remote_sdp: str = field(default="", repr=False)
    _role: str = field(default="", repr=False)

    def __post_init__(self) -> None:
        _peers.append(weakref.ref(self))

    async def create_offer(self) -> Dict[str, Any]:
        self._role = "offerer"
        self._local_sdp = f"v=0\no=- {self.session_id} 0 IN IP4 127.0.0.1\ns=echoui-inproc\n"
        return {"type": "offer", "sdp": self._local_sdp, "session": self.session_id}

    async def create_answer(self, offer: Dict[str, Any]) -> Dict[str, Any]:
        self._role = "answerer"
        self._remote_sdp = str(offer.get("sdp") or "")
        self._local_sdp = f"v=0\no=- {self.session_id} 0 IN IP4 127.0.0.1\ns=echoui-inproc-answer\n"
        return {
            "type": "answer",
            "sdp": self._local_sdp,
            "session": self.session_id,
            "offer_session": offer.get("session"),
        }

    async def apply_answer(self, answer: Dict[str, Any]) -> None:
        self._remote_sdp = str(answer.get("sdp") or "")
        for peer in _live_peers():
            if peer is self:
                continue
            if answer.get("session") and peer.session_id == answer.get("session"):
                self.connect(peer)
                return
        others = [p for p in _live_peers() if p is not self]
        if len(others) == 1:
            self.connect(others[0])

    def connect(self, other: "RTCPeer") -> None:
        """Explicitly pair two in-process peers and matching data channels."""
        self.remote = other
        other.remote = self
        by_label = {c.label: c for c in other.channels}
        for ch in self.channels:
            peer_ch = by_label.get(ch.label)
            if peer_ch is not None:
                ch.pair(peer_ch)

    def create_data_channel(self, label: str) -> DataChannel:
        ch = DataChannel(label=label, peer=self)
        self.channels.append(ch)
        if self.remote is not None:
            peer_ch = self.remote._ensure_channel(label)
            ch.pair(peer_ch)
        return ch

    def _ensure_channel(self, label: str) -> DataChannel:
        for ch in self.channels:
            if ch.label == label:
                return ch
        return self.create_data_channel(label)

    def _find_remote_channel(self, label: str) -> Optional[DataChannel]:
        if self.remote is None:
            return None
        for ch in self.remote.channels:
            if ch.label == label:
                return ch
        return None
