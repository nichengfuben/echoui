"""Mobile push, permissions, haptics — honest host stubs with UnsupportedCapability."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

from echoui.exceptions import UnsupportedCapability
from echoui.platform import enable_capability_sim, has_capability

_SIM_MOBILE = "mobile_host_sim"


@dataclass
class PushRegistration:
    token: str = ""
    handlers: List[Callable[[Dict[str, Any]], None]] = field(default_factory=list)


_push = PushRegistration()
_haptics_log: List[str] = []
_orientation: str = "portrait"
_permission_log: List[str] = []


def enable_mobile_sim() -> None:
    """Tests/dev: allow mobile APIs as in-process logs without native shell."""
    enable_capability_sim(_SIM_MOBILE, "notifications", "camera", "microphone", "geolocation")


async def push_register() -> str:
    if not (has_capability(_SIM_MOBILE) or has_capability("push")):
        raise UnsupportedCapability(
            "push.register requires a mobile shell or enable_mobile_sim()"
        )
    if not _push.token:
        _push.token = "sim-push-token"
    return _push.token


def push_on_message(handler: Callable[[Dict[str, Any]], None]) -> None:
    _push.handlers.append(handler)


async def permissions_request(name: str) -> bool:
    _permission_log.append(name)
    known = {"camera", "microphone", "notifications", "geolocation"}
    if name not in known:
        return False
    if has_capability(name) or has_capability(_SIM_MOBILE):
        return True
    # Host Python without sim: honest deny (not silent True for all names).
    return False


def haptics_impact(style: str = "medium") -> None:
    if not (has_capability(_SIM_MOBILE) or has_capability("haptics")):
        raise UnsupportedCapability(
            "haptics.impact requires a mobile target or enable_mobile_sim()"
        )
    _haptics_log.append(style)


def orientation_lock(mode: str = "portrait") -> None:
    global _orientation
    if not (has_capability(_SIM_MOBILE) or has_capability("orientation")):
        raise UnsupportedCapability(
            "orientation.lock requires a mobile target or enable_mobile_sim()"
        )
    _orientation = mode


def haptics_history() -> List[str]:
    return list(_haptics_log)


def permission_history() -> List[str]:
    return list(_permission_log)


def current_orientation() -> str:
    return _orientation


class AppLifecycle:
    def __init__(self) -> None:
        self._handlers: Dict[str, List[Callable[[], None]]] = {}

    def on(self, event: str, fn: Callable[[], None]) -> None:
        self._handlers.setdefault(event, []).append(fn)

    def emit(self, event: str) -> None:
        for fn in self._handlers.get(event, []):
            fn()


app_lifecycle = AppLifecycle()
