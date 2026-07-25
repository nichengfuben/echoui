"""WebAssembly module loading for web target (PLAN §15)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


@dataclass
class WasmModule:
    path: Path
    exports: tuple[str, ...] = ()
    _fns: dict[str, Callable[..., Any]] = field(default_factory=dict)

    def to_spec(self) -> dict[str, str | tuple[str, ...]]:
        return {"path": str(self.path), "exports": self.exports}

    def bind(self, name: str, fn: Callable[..., Any]) -> None:
        self._fns[name] = fn

    def __getattr__(self, name: str) -> Callable[..., Any]:
        if name in self._fns:
            return self._fns[name]
        raise AttributeError(name)


async def load_wasm(path: str | Path) -> WasmModule:
    return WasmModule(Path(path))
