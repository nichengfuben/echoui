"""WebAssembly module loading for web target (PLAN § wasm)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class WasmModule:
    path: Path
    exports: tuple[str, ...] = ()

    def to_spec(self) -> dict[str, str | tuple[str, ...]]:
        return {"path": str(self.path), "exports": self.exports}
