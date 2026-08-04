from __future__ import annotations

import pytest

from echoui.core.exceptions import ConfigError
from echoui.interfaces.router import Router


class TestRouter:
    def test_add_route(self) -> None:
        router = Router()

        async def handler() -> dict[str, str]:
            return {"status": "ok"}

        router.add_route("GET", "/api", handler)
        assert router.match("GET", "/api") is handler

    def test_add_route_uppercases_method(self) -> None:
        router = Router()

        async def handler() -> None:
            pass

        router.add_route("get", "/test", handler)
        assert router.match("GET", "/test") is handler

    def test_add_route_empty_method_raises(self) -> None:
        router = Router()

        async def handler() -> None:
            pass

        with pytest.raises(ConfigError, match="路由方法和路径不能为空"):
            router.add_route("", "/test", handler)

    def test_add_route_empty_path_raises(self) -> None:
        router = Router()

        async def handler() -> None:
            pass

        with pytest.raises(ConfigError, match="路由方法和路径不能为空"):
            router.add_route("GET", "", handler)

    def test_match_not_found(self) -> None:
        router = Router()
        result = router.match("GET", "/nonexistent")
        assert result is None

    def test_match_wrong_method(self) -> None:
        router = Router()

        async def handler() -> None:
            pass

        router.add_route("GET", "/api", handler)
        result = router.match("POST", "/api")
        assert result is None

    def test_get_routes(self) -> None:
        router = Router()

        async def h1() -> None:
            pass

        async def h2() -> None:
            pass

        router.add_route("GET", "/a", h1)
        router.add_route("POST", "/b", h2)
        routes = router.get_routes()
        assert "GET" in routes
        assert "POST" in routes
        assert routes["GET"]["/a"] is h1
        assert routes["POST"]["/b"] is h2

    def test_get_routes_returns_copy(self) -> None:
        router = Router()

        async def handler() -> None:
            pass

        router.add_route("GET", "/x", handler)
        first = router.get_routes()
        second = router.get_routes()
        assert first == second
        assert first is not second

    def test_remove_route(self) -> None:
        router = Router()

        async def handler() -> None:
            pass

        router.add_route("DELETE", "/item", handler)
        result = router.remove_route("DELETE", "/item")
        assert result is True
        assert router.match("DELETE", "/item") is None

    def test_remove_route_not_found(self) -> None:
        router = Router()
        result = router.remove_route("GET", "/nonexistent")
        assert result is False

    def test_overwrite_route(self) -> None:
        router = Router()

        async def old() -> None:
            pass

        async def new() -> None:
            pass

        router.add_route("PUT", "/update", old)
        router.add_route("PUT", "/update", new)
        assert router.match("PUT", "/update") is new
