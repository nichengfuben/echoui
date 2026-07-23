"""CRDT collaboration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


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


@dataclass
class Session:
    doc: CRDTMap = field(default_factory=CRDTMap)
    peers: List[str] = field(default_factory=list)

    def apply_op(self, key: str, value: Any, ts: float) -> None:
        self.doc.set(key, value, ts)

    def sync(self, remote: "Session") -> None:
        self.doc.merge(remote.doc)
