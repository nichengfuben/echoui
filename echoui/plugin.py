"""Plugin registration system."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, TypeVar

T = TypeVar("T")

_plugins: Dict[str, Dict[str, Any]] = {}
_compiler_passes: Dict[str, List[Callable[..., Any]]] = {}
_role_plugins: Dict[str, Callable[..., Any]] = {}
_target_plugins: Dict[str, Callable[..., Any]] = {}
_api_bindings: Dict[str, Callable[..., Any]] = {}


class Plugin:
    """Base plugin type; subclass and use decorators to register hooks."""

    name: str = ""


def register(name: str, *, setup: Callable[[], None] | None = None, **meta: Any) -> None:
    _plugins[name] = {"setup": setup, **meta}


def compiler_pass(stage: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def deco(fn: Callable[..., Any]) -> Callable[..., Any]:
        _compiler_passes.setdefault(stage, []).append(fn)
        register(f"pass:{stage}:{fn.__name__}", setup=fn, kind="compiler_pass", stage=stage)
        return fn

    return deco


def role(name: str) -> Callable[[T], T]:
    def deco(target: T) -> T:
        _role_plugins[name] = target  # type: ignore[assignment]
        from echoui.roles import register_role

        register_role(name, "div")
        register(f"role:{name}", setup=None, kind="role", role=name, handler=target)
        return target

    return deco


def target(name: str) -> Callable[[T], T]:
    def deco(target_fn: T) -> T:
        _target_plugins[name] = target_fn  # type: ignore[assignment]
        register(f"target:{name}", setup=None, kind="target", target=name, handler=target_fn)
        return target_fn

    return deco


def api_binding(namespace: str) -> Callable[[T], T]:
    def deco(fn: T) -> T:
        _api_bindings[namespace] = fn  # type: ignore[assignment]
        register(f"binding:{namespace}", kind="api_binding", namespace=namespace)
        return fn

    return deco


def get(name: str) -> Dict[str, Any] | None:
    return _plugins.get(name)


def list_plugins() -> List[str]:
    return list(_plugins.keys())


def list_compiler_passes(stage: str | None = None) -> List[str]:
    if stage is None:
        return [k for k in _compiler_passes]
    return [fn.__name__ for fn in _compiler_passes.get(stage, [])]


def setup_all() -> None:
    for p in _plugins.values():
        fn = p.get("setup")
        if callable(fn):
            fn()
