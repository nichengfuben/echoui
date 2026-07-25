"""CRDT collaboration with in-memory and WebSocket sync."""

from __future__ import annotations

import asyncio
import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

try:
    import aiohttp
except ImportError:
    aiohttp = None  # type: ignore[assignment]


@dataclass
class LWWRegister:
    value: Any = None
    timestamp: float = 0

    def set(self, value: Any, ts: float) -> None:
        if ts >= self.timestamp:
            self.value = value
            self.timestamp = ts


@dataclass
class CRDTMap:
    entries: Dict[str, LWWRegister] = field(default_factory=dict)

    def set(self, key: str, value: Any, ts: float) -> None:
        reg = self.entries.setdefault(key, LWWRegister())
        reg.set(value, ts)

    def get(self, key: str) -> Any:
        reg = self.entries.get(key)
        return reg.value if reg else None

    def merge(self, other: "CRDTMap") -> None:
        for k, reg in other.entries.items():
            mine = self.entries.setdefault(k, LWWRegister())
            mine.set(reg.value, reg.timestamp)

    def to_dict(self) -> Dict[str, Any]:
        return {k: {"value": v.value, "ts": v.timestamp} for k, v in self.entries.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CRDTMap":
        m = cls()
        for k, entry in data.items():
            m.set(k, entry.get("value"), float(entry.get("ts", 0)))
        return m


@dataclass
class Session:
    doc: CRDTMap = field(default_factory=CRDTMap)
    peers: List[str] = field(default_factory=list)
    peer_id: str = ""
    on_change: Optional[Callable[[str, Any], None]] = None

    def apply_op(self, key: str, value: Any, ts: float | None = None) -> None:
        ts = ts if ts is not None else time.time()
        self.doc.set(key, value, ts)
        if self.on_change:
            self.on_change(key, value)

    def sync(self, remote: "Session") -> None:
        self.doc.merge(remote.doc)

    def snapshot(self) -> Dict[str, Any]:
        return {"peer": self.peer_id, "doc": self.doc.to_dict()}


@dataclass
class SyncRelay:
    """In-memory hub — broadcasts CRDT ops to all joined sessions."""

    sessions: List[Session] = field(default_factory=list)

    def join(self, session: Session) -> None:
        if session not in self.sessions:
            self.sessions.append(session)
        for other in self.sessions:
            if other is not session:
                session.sync(other)

    def leave(self, session: Session) -> None:
        if session in self.sessions:
            self.sessions.remove(session)

    def broadcast(self, source: Session, key: str, value: Any, ts: float | None = None) -> None:
        ts = ts if ts is not None else time.time()
        for s in self.sessions:
            if s is not source:
                s.apply_op(key, value, ts)


class SyncClient:
    """WebSocket client for remote CRDT sync."""

    def __init__(self, url: str, session: Session) -> None:
        self.url = url
        self.session = session
        self._ws: Any = None
        self._task: Optional[asyncio.Task[Any]] = None

    async def connect(self) -> None:
        if aiohttp is None:
            raise ImportError("aiohttp required; pip install echoui[web]")
        session = aiohttp.ClientSession()
        self._ws = await session.ws_connect(self.url)
        await self._ws.send_json(self.session.snapshot())
        self._task = asyncio.create_task(self._listen())

    async def _listen(self) -> None:
        assert self._ws is not None
        async for msg in self._ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                if "key" in data:
                    self.session.apply_op(data["key"], data["value"], float(data.get("ts", 0)))
                elif "doc" in data:
                    self.session.sync(Session(doc=CRDTMap.from_dict(data["doc"])))

    async def push(self, key: str, value: Any) -> None:
        ts = time.time()
        self.session.apply_op(key, value, ts)
        if self._ws:
            await self._ws.send_json({"key": key, "value": value, "ts": ts})

    async def close(self) -> None:
        if self._task:
            self._task.cancel()
        if self._ws:
            await self._ws.close()
