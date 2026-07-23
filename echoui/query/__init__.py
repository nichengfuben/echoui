"""Stale-while-revalidate query layer."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")

FetcherFn = Callable[[], Any]
AsyncFetcherFn = Callable[[], Any]


@dataclass
class QueryResult(Generic[T]):
    data: Optional[T] = None
    error: Optional[str] = None
    is_stale: bool = False
    is_loading: bool = False


@dataclass
class Query:
    key: str
    fetcher: Callable[[], Any]
    stale_time: float = 60.0
    _cached: Any = None
    _fetched_at: float = 0
    _loading: bool = False
    _error: Optional[str] = None
    _subs: List[Callable[[], None]] = field(default_factory=list)

    @property
    def result(self) -> QueryResult[Any]:
        stale = time.time() - self._fetched_at > self.stale_time if self._fetched_at else True
        return QueryResult(
            data=self._cached,
            error=self._error,
            is_stale=stale,
            is_loading=self._loading,
        )

    async def fetch(self) -> Any:
        self._loading = True
        self._notify()
        try:
            result = self.fetcher()
            if asyncio.iscoroutine(result):
                result = await result
            self._cached = result
            self._fetched_at = time.time()
            self._error = None
        except Exception as e:
            self._error = str(e)
        finally:
            self._loading = False
            self._notify()
        return self._cached

    async def refetch(self) -> Any:
        self._fetched_at = 0
        return await self.fetch()

    def _notify(self) -> None:
        for s in self._subs:
            s()


_queries: Dict[str, Query] = {}


def query(key: str, fetcher: Callable[[], Any], *, stale_time: float = 60.0) -> Query:
    q = Query(key=key, fetcher=fetcher, stale_time=stale_time)
    _queries[key] = q
    return q


@dataclass
class Mutation:
    fn: Callable[[Dict[str, Any]], Any]
    on_success: Optional[Callable[[Any], None]] = None
    optimistic: Optional[Callable[[Dict[str, Any]], None]] = None

    async def run(self, variables: Dict[str, Any]) -> Any:
        if self.optimistic:
            self.optimistic(variables)
        result = self.fn(variables)
        if asyncio.iscoroutine(result):
            result = await result
        if self.on_success:
            self.on_success(result)
        return result


def mutation(
    fn: Callable[[Dict[str, Any]], Any],
    *,
    on_success: Callable[[Any], None] | None = None,
    optimistic: Callable[[Dict[str, Any]], None] | None = None,
) -> Mutation:
    return Mutation(fn=fn, on_success=on_success, optimistic=optimistic)


@dataclass
class InfiniteQuery:
    key: str
    fetcher: Callable[[int], Any]
    pages: List[Any] = field(default_factory=list)
    page: int = 0
    has_more: bool = True

    async def fetch_next(self) -> Any:
        data = self.fetcher(self.page)
        if asyncio.iscoroutine(data):
            data = await data
        if not data:
            self.has_more = False
            return None
        self.pages.append(data)
        self.page += 1
        return data


def infinite_query(key: str, fetcher: Callable[[int], Any]) -> InfiniteQuery:
    return InfiniteQuery(key=key, fetcher=fetcher)
