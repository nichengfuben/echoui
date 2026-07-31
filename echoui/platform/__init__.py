"""Platform and device APIs — host memory bridge for common APIs; UnsupportedCapability for hardware-only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set

from echoui.exceptions import UnsupportedCapability

_clipboard_text: str = ""
_notification_log: List[Dict[str, str]] = []
_share_log: List[Dict[str, str]] = []
_sim_capabilities: Set[str] = set()

# Host-safe APIs always available in the Python process (memory / logging bridges).
_HOST_CAPS: frozenset[str] = frozenset(
    {
        "reactive",
        "compiler",
        "clipboard",
        "notifications",
        "share",
        "vibration",
        "files",
        "battery",
        "network",
    }
)

# Require real OS / device / browser bridges — never silent success.
_HARDWARE_CAPS: frozenset[str] = frozenset(
    {
        "biometrics",
        "bluetooth",
        "usb",
        "serial",
        "midi",
        "nfc",
        "contacts",
        "calendar",
        "printer",
        "geolocation",
        "camera",
        "microphone",
    }
)


def enable_capability_sim(*names: str) -> None:
    """Test/dev only: allow selected hardware capabilities to use memory stubs."""
    _sim_capabilities.update(names)


def clear_capability_sim() -> None:
    _sim_capabilities.clear()


def _require(feature: str, capability: str) -> None:
    if has_capability(capability) or capability in _sim_capabilities:
        return
    raise UnsupportedCapability(
        f"{feature} is not available on this host "
        f"(capability={capability!r}; use a native/web bridge or enable_capability_sim)"
    )


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
    caps: set[str] = set(_HOST_CAPS)
    is_web = os_name == "emscripten"
    is_desktop = os_name in ("win32", "darwin", "linux") and not is_web
    is_mobile = False
    if is_desktop:
        caps.update({"filesystem", "window", "tray", "menubar", "dialog"})
    if is_web:
        caps.update({"geolocation", "camera", "microphone", "share_native"})
    caps.update(_sim_capabilities)
    return PlatformInfo(
        os=os_name,
        is_web=is_web,
        is_desktop=is_desktop,
        is_mobile=is_mobile,
        capabilities=caps,
    )


def has_capability(name: str) -> bool:
    return name in detect().capabilities


class Notifications:
    def request(self) -> bool:
        return True

    def show(self, title: str, *, body: str = "", icon: str = "") -> None:
        _notification_log.append({"title": title, "body": body, "icon": icon})

    @staticmethod
    def history() -> List[Dict[str, str]]:
        return list(_notification_log)


class Clipboard:
    async def write_text(self, text: str) -> None:
        global _clipboard_text
        _clipboard_text = text

    async def read_text(self) -> str:
        return _clipboard_text


class Share:
    async def share(self, data: Dict[str, str]) -> None:
        _share_log.append(dict(data))

    @staticmethod
    def history() -> List[Dict[str, str]]:
        return list(_share_log)


@dataclass
class Battery:
    level: float = 1.0
    charging: bool = True


@dataclass
class Network:
    online: bool = True
    type: str = "wifi"


class Vibration:
    def __init__(self) -> None:
        self.patterns: List[List[int]] = []

    def vibrate(self, pattern: list[int]) -> None:
        self.patterns.append(list(pattern))


class Biometrics:
    async def authenticate(self, reason: str = "Unlock") -> bool:
        _require("biometrics.authenticate", "biometrics")
        return True


class Bluetooth:
    async def request(self, *, services: Optional[List[str]] = None) -> Dict[str, Any]:
        _require("bluetooth.request", "bluetooth")
        return {"services": list(services or [])}


class Nfc:
    async def read(self) -> str:
        _require("nfc.read", "nfc")
        return ""


class Usb:
    async def request(self) -> Dict[str, Any]:
        _require("usb.request", "usb")
        return {}


class Serial:
    async def request(self) -> Dict[str, Any]:
        _require("serial.request", "serial")
        return {}


class Midi:
    @property
    def inputs(self) -> List[str]:
        _require("midi.inputs", "midi")
        return []


class Contacts:
    async def list(self) -> List[Dict[str, str]]:
        _require("contacts.list", "contacts")
        return []


class Calendar:
    async def list_events(self) -> List[Dict[str, Any]]:
        _require("calendar.list_events", "calendar")
        return []


class Printer:
    async def print(self, node: Any = None) -> None:
        _require("printer.print", "printer")


class Geolocation:
    async def get(self) -> Dict[str, float]:
        _require("geolocation.get", "geolocation")
        return {"lat": 0.0, "lng": 0.0}

    def watch(self, on_move: Callable[[Dict[str, float]], None]) -> None:
        _require("geolocation.watch", "geolocation")


notifications = Notifications()
clipboard = Clipboard()
share = Share()
battery = Battery()
network = Network()
vibration = Vibration()
biometrics = Biometrics()
bluetooth = Bluetooth()
nfc = Nfc()
usb = Usb()
serial = Serial()
midi = Midi()
contacts = Contacts()
calendar = Calendar()
printer = Printer()
geolocation = Geolocation()


async def dialog_open_file(*, accept: str = "*/*") -> Optional[str]:
    from echoui.storage.files import files

    if detect().is_desktop or has_capability("dialog"):
        return await files.pick(accept=accept)  # type: ignore[return-value]
    raise UnsupportedCapability("dialog.open_file is not available on this target")


async def dialog_save_file(name: str, data: bytes) -> None:
    if detect().is_desktop or has_capability("dialog"):
        from echoui.storage.files import files

        await files.save(name, data)
        return
    raise UnsupportedCapability("dialog.save_file is not available on this target")
