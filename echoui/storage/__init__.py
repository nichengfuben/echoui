"""Client-side storage APIs."""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, Optional


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


_local = MemoryBackend()
_session = MemoryBackend()
_cookies = MemoryBackend()
_kv = MemoryBackend()
_cache: Dict[str, tuple[Any, float]] = {}


def local() -> MemoryBackend:
    return _local


def session() -> MemoryBackend:
    return _session


def cookies() -> MemoryBackend:
    return _cookies


def kv() -> MemoryBackend:
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


def json_get(store: MemoryBackend, key: str) -> Any:
    raw = store.get(key)
    return json.loads(raw) if raw else None


def json_set(store: MemoryBackend, key: str, value: Any) -> None:
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
]
