"""WebRTC peer connections (web runtime)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class DataChannel:
    label: str
    on_message: Optional[Callable[[str], None]] = None

    def send(self, data: str) -> None:
        pass


@dataclass
class RTCPeer:
    ice_servers: List[Dict[str, str]] = field(default_factory=list)
    channels: List[DataChannel] = field(default_factory=list)

    async def create_offer(self) -> Dict[str, Any]:
        return {"type": "offer", "sdp": ""}

    async def apply_answer(self, answer: Dict[str, Any]) -> None:
        pass

    def create_data_channel(self, label: str) -> DataChannel:
        ch = DataChannel(label=label)
        self.channels.append(ch)
        return ch
