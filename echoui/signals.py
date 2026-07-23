"""Global named signal bus."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List


@dataclass
class _BusEntry:
    handlers: List[Callable[..., None]] = field(default_factory=list)


_buses: Dict[str, _BusEntry] = {}


class SignalBus:
    def __init__(self, name: str) -> None:
        self.name = name
        self._last_payload: Dict[str, Any] = {}
        _buses.setdefault(name, _BusEntry())

    def emit(self, **payload: Any) -> None:
        self._last_payload = payload
        for h in list(_buses[self.name].handlers):
            h(**payload)

    def on(self, handler: Callable[..., None]) -> Callable[..., None]:
        _buses[self.name].handlers.append(handler)
        return handler

    def clear(self) -> None:
        _buses[self.name].handlers.clear()


def signal(name: str) -> SignalBus:
    return SignalBus(name)
