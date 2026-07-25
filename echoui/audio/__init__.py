"""Web Audio and HTML5 audio playback (compile-local on web targets)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Sound:
    src: str
    volume: float = 1.0
    loop: bool = False


class AudioEngine:
    """Client-side audio engine; web runtime executes via ``window.__echoui.audio``."""

    def __init__(self) -> None:
        self._volume: float = 1.0
        self._speed: float = 1.0
        self._tempo: int = 120
        self._bgm: Optional[str] = None
        self._queue: List[Sound] = []

    @property
    def volume(self) -> float:
        return self._volume

    def play(self, src: str, *, volume: float | None = None, loop: bool = False) -> None:
        """Play a one-shot sound (web: ``Audio`` element or Web Audio buffer)."""
        self._queue.append(Sound(src=src, volume=volume or self._volume, loop=loop))

    async def play_until_done(self, src: str) -> None:
        self.play(src)

    def play_bgm(self, src: str, *, loop: bool = True) -> None:
        self._bgm = src
        self.play(src, loop=loop)

    def stop_bgm(self) -> None:
        self._bgm = None

    def set_volume(self, pct: int) -> None:
        self._volume = max(0.0, min(1.0, pct / 100.0))

    def set_speed(self, pct: int) -> None:
        self._speed = max(0.25, min(4.0, pct / 100.0))

    def play_note(self, note: str, *, beats: float = 1.0) -> None:
        freq = _NOTE_FREQ.get(note.upper())
        if freq:
            self._queue.append(Sound(src=f"__note:{freq}:{beats}", volume=self._volume))

    def set_tempo(self, bpm: int) -> None:
        self._tempo = max(30, min(300, bpm))

    def compile_ops(self) -> List[Dict[str, Any]]:
        """Serialize pending ops for client cfg (consumed once per build step)."""
        ops = []
        for s in self._queue:
            ops.append({"op": "play", "src": s.src, "volume": s.volume, "loop": s.loop})
        self._queue.clear()
        if self._bgm:
            ops.append({"op": "bgm", "src": self._bgm})
        return ops


_NOTE_FREQ = {
    "C4": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.0,
    "A4": 440.0,
    "B4": 493.88,
}


audio = AudioEngine()


class TTS:
    """Text-to-speech (web: SpeechSynthesisUtterance via runtime)."""

    def __init__(self, language: str = "en") -> None:
        self.language = language

    async def speak_until_done(self, text: str) -> None:
        self._last = text

    async def speak(self, text: str) -> None:
        await self.speak_until_done(text)


async def listen(*, language: str = "en", seconds: float = 5.0) -> str:
    """Speech recognition placeholder — web runtime uses SpeechRecognition when available."""
    return ""


async def record(*, seconds: float = 5.0) -> Sound:
    return Sound(src="__recorded__")


def enable_mic() -> None:
    pass


def translate(text: str, *, to: str = "en") -> str:
    return text
