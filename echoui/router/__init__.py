"""Application router."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from urllib.parse import parse_qs, urlparse

GuardFn = Callable[[], Optional[str]]
MiddlewareFn = Callable[[Dict[str, Any]], Dict[str, Any]]
# Lazy screen: callable returning screen name/class/module path string
LazyScreen = Callable[[], Any]
ScreenRef = Union[str, LazyScreen]
LayoutRef = Union[str, List[str], None]


def _as_layout_list(layout: LayoutRef) -> List[str]:
    if layout is None:
        return []
    if isinstance(layout, str):
        return [layout] if layout else []
    return [str(x) for x in layout if x]


@dataclass
class Route:
    pattern: str
    screen: ScreenRef
    layout: LayoutRef = None
    guard: Optional[GuardFn] = None
    lazy: bool = False
    parent: Optional[str] = None


@dataclass
class Router:
    routes: List[Route] = field(default_factory=list)
    middleware: List[MiddlewareFn] = field(default_factory=list)
    _current: str = "/"
    _params: Dict[str, str] = field(default_factory=dict)
    _query: Dict[str, List[str]] = field(default_factory=dict)
    _layout: Optional[str] = None
    _layouts: List[str] = field(default_factory=list)
    _resolved_cache: Dict[int, str] = field(default_factory=dict)

    def add(
        self,
        pattern: str,
        screen: ScreenRef,
        *,
        layout: LayoutRef = None,
        guard: GuardFn | None = None,
        lazy: bool = False,
        parent: str | None = None,
    ) -> "Router":
        is_lazy = lazy or callable(screen)
        self.routes.append(
            Route(pattern, screen, layout, guard, lazy=is_lazy, parent=parent)
        )
        return self

    def group(
        self,
        prefix: str,
        *,
        layout: LayoutRef = None,
        guard: GuardFn | None = None,
    ) -> "RouteGroup":
        """Nested route group: children inherit prefix + layout chain."""
        return RouteGroup(self, prefix.rstrip("/") or "", layout, guard)

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
                layouts = self._resolve_layouts(route)
                self._layouts = layouts
                self._layout = layouts[-1] if layouts else None
                screen_name = self._resolve_screen(route)
                ctx = {
                    "path": path,
                    "params": params,
                    "query": self._query,
                    "layout": self._layout,
                    "layouts": list(layouts),
                    "screen": screen_name,
                }
                for mw in self.middleware:
                    ctx = mw(ctx)
                return screen_name, params
        if self.routes:
            fallback = self.routes[-1]
            layouts = self._resolve_layouts(fallback)
            self._layouts = layouts
            self._layout = layouts[-1] if layouts else None
            return self._resolve_screen(fallback), {}
        raise LookupError(f"No route for {path}")

    def _resolve_layouts(self, route: Route) -> List[str]:
        chain: List[str] = []
        seen: set[str] = set()
        parent = route.parent
        while parent:
            if parent in seen:
                break
            seen.add(parent)
            parent_route = self._find_route(parent)
            if parent_route is None:
                break
            chain = _as_layout_list(parent_route.layout) + chain
            parent = parent_route.parent
        chain = chain + _as_layout_list(route.layout)
        # de-dupe consecutive duplicates while preserving order
        out: List[str] = []
        for name in chain:
            if not out or out[-1] != name:
                out.append(name)
        return out

    def _find_route(self, pattern: str) -> Optional[Route]:
        for r in self.routes:
            if r.pattern == pattern:
                return r
        return None

    def _resolve_screen(self, route: Route) -> str:
        if not callable(route.screen):
            return str(route.screen)
        key = id(route)
        cached = self._resolved_cache.get(key)
        if cached is not None:
            return cached
        loaded = route.screen()
        name = loaded if isinstance(loaded, str) else getattr(loaded, "name", None) or getattr(
            loaded, "__name__", str(loaded)
        )
        self._resolved_cache[key] = str(name)
        return str(name)

    def current_layout(self) -> Optional[str]:
        return self._layout

    def current_layouts(self) -> List[str]:
        return list(self._layouts)

    def route_params(self) -> Dict[str, str]:
        return dict(self._params)

    def query_params(self) -> Dict[str, List[str]]:
        return dict(self._query)


@dataclass
class RouteGroup:
    router: Router
    prefix: str
    layout: LayoutRef = None
    guard: Optional[GuardFn] = None
    parent: Optional[str] = None

    def add(
        self,
        pattern: str,
        screen: ScreenRef,
        *,
        layout: LayoutRef = None,
        guard: GuardFn | None = None,
        lazy: bool = False,
    ) -> "RouteGroup":
        full = _join_path(self.prefix, pattern)
        layouts = _as_layout_list(self.layout) + _as_layout_list(layout)
        layout_ref: LayoutRef = layouts if layouts else None
        self.router.add(
            full,
            screen,
            layout=layout_ref,
            guard=guard or self.guard,
            lazy=lazy,
            parent=self.parent,
        )
        return self

    def group(
        self,
        prefix: str,
        *,
        layout: LayoutRef = None,
        guard: GuardFn | None = None,
    ) -> "RouteGroup":
        full_prefix = _join_path(self.prefix, prefix)
        # parent pattern = current group root if registered, else None
        parent_pat = self.prefix if self.prefix else None
        return RouteGroup(
            self.router,
            full_prefix,
            layout=_as_layout_list(self.layout) + _as_layout_list(layout),
            guard=guard or self.guard,
            parent=parent_pat,
        )


def _join_path(prefix: str, pattern: str) -> str:
    if not prefix:
        return pattern if pattern.startswith("/") else f"/{pattern}"
    if pattern in ("", "/"):
        return prefix or "/"
    p = pattern if pattern.startswith("/") else f"/{pattern}"
    return f"{prefix.rstrip('/')}{p}"


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
