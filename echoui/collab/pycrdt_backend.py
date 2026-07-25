"""Optional pycrdt-backed document (pip install echoui[collab])."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class PyCRDTSession:
    """Shared document using pycrdt YMap when available."""

    peer_id: str = ""
    on_change: Optional[Callable[[str, Any], None]] = None
    _doc: Any = field(default=None, repr=False)
    _ymap: Any = field(default=None, repr=False)

    def __post_init__(self) -> None:
        try:
            from pycrdt import Doc, Map
        except ImportError as e:
            raise ImportError("pip install echoui[collab] or pip install pycrdt") from e
        self._doc = Doc()
        self._ymap = self._doc.get("state", type=Map)

    def set(self, key: str, value: Any) -> None:
        self._ymap[key] = value
        if self.on_change:
            self.on_change(key, value)

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return self._ymap[key]
        except KeyError:
            return default

    def keys(self) -> List[str]:
        return list(self._ymap.keys())

    def apply_update(self, data: bytes) -> None:
        self._doc.apply_update(data)

    def encode_update(self) -> bytes:
        return self._doc.get_update()

    def snapshot(self) -> Dict[str, Any]:
        return {"peer": self.peer_id, "keys": self.keys(), "ts": time.time()}


def merge_updates(base: bytes, incoming: bytes) -> bytes:
    from pycrdt import Doc

    doc: Any = Doc()
    doc.apply_update(base)
    doc.apply_update(incoming)
    return doc.get_update()
