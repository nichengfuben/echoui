"""Platform and device APIs — web via runtime, native via bridge or UnsupportedCapability."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from echoui.exceptions import UnsupportedCapability


def _require_web(feature: str) -> None:
    from echoui.platform import detect

    info = detect()
    if not info.is_web and info.os not in ("emscripten",):
        raise UnsupportedCapability(f"{feature} is not available on this target")


@dataclass
class PlatformInfo:
    os: str
    is_web: bool
    is_desktop: bool
    is_mobile: bool
    capabilities: set[str]


def detect() -> PlatformInfo:
    import sys

    os_name = sys.platform
    caps = {"reactive", "compiler", "clipboard", "notifications", "share", "vibration"}
    is_web = os_name == "emscripten"
    is_desktop = os_name in ("win32", "darwin", "linux") and not is_web
    is_mobile = False
    if is_desktop:
        caps.update({"filesystem", "window", "tray", "menubar"})
    return PlatformInfo(
        os=os_name,
        is_web=is_web,
        is_desktop=is_desktop,
        is_mobile=is_mobile,
        capabilities=caps,
    )


def has_capability(name: str) -> bool:
    return name in detect().capabilities


class _Notifications:
    def request(self) -> bool:
        return True

    def show(self, title: str, *, body: str = "", icon: str = "") -> None:
        pass


class _Clipboard:
    async def write_text(self, text: str) -> None:
        pass

    async def read_text(self) -> str:
        return ""


class _Share:
    async def share(self, data: Dict[str, str]) -> None:
        pass


class _Battery:
    level: float = 1.0
    charging: bool = True


class _Network:
    online: bool = True
    type: str = "unknown"


class _Vibration:
    def vibrate(self, pattern: list[int]) -> None:
        pass


notifications = _Notifications()
clipboard = _Clipboard()
share = _Share()
battery = _Battery()
network = _Network()
vibration = _Vibration()


async def dialog_open_file(*, accept: str = "*/*") -> Optional[str]:
    _require_web("dialog.open_file")
    return None


async def dialog_save_file(name: str, data: bytes) -> None:
    _require_web("dialog.save_file")
