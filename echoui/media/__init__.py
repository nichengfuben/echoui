"""Device capture and sensors — honest host stubs with UnsupportedCapability."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

from echoui.exceptions import UnsupportedCapability
from echoui.platform import clear_capability_sim, enable_capability_sim, has_capability

_MEDIA_CAPS = ("geolocation", "camera", "microphone", "screen_capture", "sensors")


def enable_media_sim() -> None:
    """Tests/dev: allow media APIs as in-process memory stubs."""
    enable_capability_sim(*_MEDIA_CAPS)


def clear_media_sim() -> None:
    clear_capability_sim()


def _require(feature: str, capability: str) -> None:
    if has_capability(capability):
        return
    raise UnsupportedCapability(
        f"{feature} is not available on this host "
        f"(capability={capability!r}; use a native/web bridge or enable_media_sim)"
    )


@dataclass
class GeoPosition:
    latitude: float
    longitude: float
    accuracy: float = 0.0


class Geolocation:
    def __init__(self) -> None:
        self._watchers: List[Callable[[GeoPosition], None]] = []
        self._sim_pos = GeoPosition(0.0, 0.0, accuracy=0.0)

    async def get(self) -> GeoPosition:
        _require("geolocation.get", "geolocation")
        return GeoPosition(
            self._sim_pos.latitude,
            self._sim_pos.longitude,
            self._sim_pos.accuracy,
        )

    def watch(self, on_move: Callable[[GeoPosition], None]) -> int:
        _require("geolocation.watch", "geolocation")
        self._watchers.append(on_move)
        return len(self._watchers)

    def clear_watch(self, watch_id: int) -> None:
        idx = watch_id - 1
        if 0 <= idx < len(self._watchers):
            self._watchers[idx] = lambda _p: None

    def set_sim_position(self, lat: float, lng: float, accuracy: float = 1.0) -> None:
        self._sim_pos = GeoPosition(lat, lng, accuracy)
        for w in self._watchers:
            w(self._sim_pos)


class Camera:
    def __init__(self) -> None:
        self._last_facing: str = "environment"
        self._sim_frame: bytes = b"\x00sim-frame"

    async def capture(self) -> bytes:
        _require("camera.capture", "camera")
        return self._sim_frame

    def stream(self, *, facing: str = "environment") -> Any:
        _require("camera.stream", "camera")
        self._last_facing = facing
        return {"facing": facing, "active": True}


class ScreenCapture:
    def __init__(self) -> None:
        self._sim_blob: bytes = b"\x00sim-screen"

    async def record(self, *, seconds: float = 10.0) -> bytes:
        _require("screen.record", "screen_capture")
        # seconds kept for API parity; sim returns fixed blob
        _ = seconds
        return self._sim_blob


@dataclass
class Sensors:
    _accel: Dict[str, float] = field(default_factory=lambda: {"x": 0.0, "y": 0.0, "z": 0.0})
    _compass: float = 0.0
    _light: float = 1.0
    _proximity: float = 0.0

    @property
    def accelerometer(self) -> Dict[str, float]:
        _require("sensors.accelerometer", "sensors")
        return dict(self._accel)

    @property
    def compass(self) -> float:
        _require("sensors.compass", "sensors")
        return self._compass

    @property
    def ambient_light(self) -> float:
        _require("sensors.ambient_light", "sensors")
        return self._light

    @property
    def proximity(self) -> float:
        _require("sensors.proximity", "sensors")
        return self._proximity

    def set_sim(
        self,
        *,
        accel: Dict[str, float] | None = None,
        compass: float | None = None,
        light: float | None = None,
        proximity: float | None = None,
    ) -> None:
        if accel is not None:
            self._accel = dict(accel)
        if compass is not None:
            self._compass = compass
        if light is not None:
            self._light = light
        if proximity is not None:
            self._proximity = proximity


geolocation = Geolocation()
camera = Camera()
screen = ScreenCapture()
sensors = Sensors()
