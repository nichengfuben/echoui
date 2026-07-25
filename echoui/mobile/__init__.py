"""Mobile push, permissions, haptics (native bridges)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class PushRegistration:
    token: str = ""
    handlers: List[Callable[[Dict[str, Any]], None]] = field(default_factory=list)


_push = PushRegistration()


async def push_register() -> str:
    return _push.token


def push_on_message(handler: Callable[[Dict[str, Any]], None]) -> None:
    _push.handlers.append(handler)


async def permissions_request(name: str) -> bool:
    return name in ("camera", "microphone", "notifications", "geolocation")


def haptics_impact(style: str = "medium") -> None:
    pass


def orientation_lock(mode: str = "portrait") -> None:
    pass


class AppLifecycle:
    def __init__(self) -> None:
        self._handlers: Dict[str, List[Callable[[], None]]] = {}

    def on(self, event: str, fn: Callable[[], None]) -> None:
        self._handlers.setdefault(event, []).append(fn)

    def emit(self, event: str) -> None:
        for fn in self._handlers.get(event, []):
            fn()


app_lifecycle = AppLifecycle()
