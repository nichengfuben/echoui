"""Client-side storage APIs."""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, Optional, Protocol


class StorageBackend(Protocol):
    def get(self, key: str) -> Optional[str]: ...
    def set(self, key: str, value: str) -> None: ...
    def delete(self, key: str) -> None: ...


class MemoryBackend:
    def __init__(self) -> None:
        self._data: Dict[str, str] = {}

    def get(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def set(self, key: str, value: str) -> None:
        self._data[key] = value

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def clear(self) -> None:
        self._data.clear()


class FileBackend:
    """JSON file-backed KV for desktop/native runs."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, str] = {}
        if self.path.exists():
            try:
                raw = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    self._data = {str(k): str(v) if not isinstance(v, str) else v for k, v in raw.items()}
            except (json.JSONDecodeError, OSError):
                self._data = {}

    def get(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def set(self, key: str, value: str) -> None:
        self._data[key] = value
        self._flush()

    def delete(self, key: str) -> None:
        self._data.pop(key, None)
        self._flush()

    def clear(self) -> None:
        self._data.clear()
        self._flush()

    def _flush(self) -> None:
        self.path.write_text(json.dumps(self._data, ensure_ascii=False), encoding="utf-8")


class CookieBackend(MemoryBackend):
    """In-process cookies with optional attributes (max_age/secure/same_site)."""

    def __init__(self) -> None:
        super().__init__()
        self._meta: Dict[str, Dict[str, Any]] = {}

    def set_cookie(
        self,
        key: str,
        value: str,
        *,
        max_age: int | None = None,
        secure: bool = False,
        same_site: str = "lax",
    ) -> None:
        self.set(key, value)
        self._meta[key] = {
            "max_age": max_age,
            "secure": secure,
            "same_site": same_site,
            "set_at": time.time(),
        }

    def get(self, key: str) -> Optional[str]:
        meta = self._meta.get(key)
        if meta and meta.get("max_age") is not None:
            if time.time() - float(meta["set_at"]) > float(meta["max_age"]):
                self.delete(key)
                return None
        return super().get(key)

    def delete(self, key: str) -> None:
        self._meta.pop(key, None)
        super().delete(key)


_local: MemoryBackend | FileBackend = MemoryBackend()
_session: MemoryBackend = MemoryBackend()
_cookies: CookieBackend = CookieBackend()
_kv: MemoryBackend | FileBackend = MemoryBackend()
_cache: Dict[str, tuple[Any, float]] = {}


def configure_storage(*, local_path: str | Path | None = None, kv_path: str | Path | None = None) -> None:
    """Switch local/kv to file backends (desktop). Default remains in-memory for tests."""
    global _local, _kv
    if local_path is not None:
        _local = FileBackend(local_path)
    if kv_path is not None:
        _kv = FileBackend(kv_path)


def local() -> MemoryBackend | FileBackend:
    return _local


def session() -> MemoryBackend:
    return _session


def cookies() -> CookieBackend:
    return _cookies


def kv() -> MemoryBackend | FileBackend:
    return _kv


def cache_get(key: str, *, max_age: float = 300) -> Optional[Any]:
    entry = _cache.get(key)
    if entry is None:
        return None
    val, ts = entry
    if time.time() - ts > max_age:
        del _cache[key]
        return None
    return val


def cache_set(key: str, value: Any) -> None:
    _cache[key] = (value, time.time())


def cache_clear() -> None:
    _cache.clear()


class SqliteStore:
    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        self._conn = sqlite3.connect(self.path)
        self._conn.execute("CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT)")
        self._conn.commit()

    def get(self, key: str) -> Optional[str]:
        row = self._conn.execute("SELECT v FROM kv WHERE k=?", (key,)).fetchone()
        return row[0] if row else None

    def set(self, key: str, value: str) -> None:
        self._conn.execute("INSERT OR REPLACE INTO kv (k,v) VALUES (?,?)", (key, value))
        self._conn.commit()

    def delete(self, key: str) -> None:
        self._conn.execute("DELETE FROM kv WHERE k=?", (key,))
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()


def sqlite(path: str | Path) -> SqliteStore:
    return SqliteStore(path)


class WebSqliteStore:
    """Browser KV (OPFS + localStorage) with in-memory fallback for tests."""

    def __init__(self) -> None:
        self._mem = MemoryBackend()

    def get(self, key: str) -> Optional[str]:
        return self._mem.get(key)

    def set(self, key: str, value: str) -> None:
        self._mem.set(key, value)

    def delete(self, key: str) -> None:
        self._mem.delete(key)


def web_sqlite() -> WebSqliteStore:
    return WebSqliteStore()


def json_get(store: Any, key: str) -> Any:
    raw = store.get(key)
    return json.loads(raw) if raw else None


def json_set(store: Any, key: str, value: Any) -> None:
    store.set(key, json.dumps(value))


from echoui.storage.files import Files, files  # noqa: E402
from echoui.storage.persist import persist_mixin  # noqa: E402

__all__ = [
    "local",
    "session",
    "cookies",
    "kv",
    "cache_get",
    "cache_set",
    "cache_clear",
    "sqlite",
    "web_sqlite",
    "json_get",
    "json_set",
    "Files",
    "files",
    "persist_mixin",
    "FileBackend",
    "MemoryBackend",
    "CookieBackend",
    "configure_storage",
]
