"""File pick/save — web uses File System Access / download; native uses pathlib."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Optional, Union


class Files:
    """Cross-target file helpers; web runtime handles pick/save in browser."""

    async def pick(self, *, accept: str = "*/*", multiple: bool = False) -> Union[str, list[str], None]:
        """Return data URL(s) on web after user picks file(s)."""
        return None

    async def save(self, name: str, data: Union[str, bytes], *, mime: str = "application/octet-stream") -> None:
        if isinstance(data, str):
            data = data.encode("utf-8")
        path = Path(name)
        path.write_bytes(data)

    async def open_dir(self) -> Optional[str]:
        return None

    def read_bytes(self, path: Union[str, Path]) -> bytes:
        return Path(path).read_bytes()

    def read_data_url(self, path: Union[str, Path]) -> str:
        raw = self.read_bytes(path)
        ext = Path(path).suffix.lower()
        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
        }.get(ext, "application/octet-stream")
        b64 = base64.b64encode(raw).decode("ascii")
        return f"data:{mime};base64,{b64}"


files = Files()
