"""Application router."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

GuardFn = Callable[[], Optional[str]]
MiddlewareFn = Callable[[Dict[str, Any]], Dict[str, Any]]


@dataclass
class Route:
    pattern: str
    screen: str
    layout: Optional[str] = None
    guard: Optional[GuardFn] = None


@dataclass
class Router:
    routes: List[Route] = field(default_factory=list)
    middleware: List[MiddlewareFn] = field(default_factory=list)
    _current: str = "/"
    _params: Dict[str, str] = field(default_factory=dict)
    _query: Dict[str, List[str]] = field(default_factory=dict)

    def add(self, pattern: str, screen: str, *, layout: str | None = None, guard: GuardFn | None = None) -> "Router":
        self.routes.append(Route(pattern, screen, layout, guard))
        return self

    def navigate(self, path: str) -> Tuple[str, Dict[str, str]]:
        self._current = path
        parsed = urlparse(path)
        self._query = parse_qs(parsed.query)
        for route in self.routes:
            params = _match(route.pattern, parsed.path)
            if params is not None:
                if route.guard:
                    redirect = route.guard()
                    if redirect:
                        return self.navigate(redirect)
                self._params = params
                ctx = {"path": path, "params": params, "query": self._query}
                for mw in self.middleware:
                    ctx = mw(ctx)
                return route.screen, params
        if self.routes:
            return self.routes[-1].screen, {}
        raise LookupError(f"No route for {path}")

    def route_params(self) -> Dict[str, str]:
        return dict(self._params)

    def query_params(self) -> Dict[str, List[str]]:
        return dict(self._query)


def navigate(router: Router, path: str) -> Tuple[str, Dict[str, str]]:
    return router.navigate(path)


def _match(pattern: str, path: str) -> Optional[Dict[str, str]]:
    if pattern.endswith("*"):
        prefix = pattern[:-1]
        if path.startswith(prefix):
            return {"rest": path[len(prefix):]}
        return None
    if pattern == "/":
        return {} if path == "/" else None
    parts_p = pattern.strip("/").split("/")
    parts_u = path.strip("/").split("/")
    if len(parts_p) != len(parts_u):
        return None
    params: Dict[str, str] = {}
    for pp, pu in zip(parts_p, parts_u):
        if pp.startswith(":"):
            params[pp[1:]] = pu
        elif pp != pu:
            return None
    return params
