from __future__ import annotations

from unittest.mock import Mock

from echoui.adapters.base_adapter import BaseAdapter


class _ConcreteAdapter(BaseAdapter):
    """Concrete subclass of BaseAdapter for testing."""

    def run(self) -> None:
        pass

    def run_async(self) -> None:
        pass

    def stop(self) -> None:
        pass


class TestBaseAdapter:
    """Tests for BaseAdapter class."""

    def test_creates_with_defaults(self) -> None:
        adapter = _ConcreteAdapter()
        assert adapter.host == "127.0.0.1"
        assert adapter.port == 8000
        assert adapter.routes == {}

    def test_get_decorator_registers_route(self) -> None:
        adapter = _ConcreteAdapter()

        @adapter.get("/test")
        def handler() -> str:
            return "ok"

        assert "GET /test" in adapter.routes
        assert adapter.routes["GET /test"]["handler"] is handler

    def test_post_decorator(self) -> None:
        adapter = _ConcreteAdapter()

        @adapter.post("/submit")
        def handler() -> str:
            return "created"

        assert "POST /submit" in adapter.routes
        assert adapter.routes["POST /submit"]["method"] == "POST"

    def test_register_route(self) -> None:
        adapter = _ConcreteAdapter()
        handler = Mock()
        adapter.register_route("GET", "/api", handler)
        assert "GET /api" in adapter.routes
        assert adapter.routes["GET /api"]["path"] == "/api"
        assert adapter.routes["GET /api"]["handler"] is handler

    def test_routes_stored_correctly(self) -> None:
        adapter = _ConcreteAdapter()
        h1 = Mock()
        h2 = Mock()
        adapter.register_route("GET", "/one", h1)
        adapter.register_route("POST", "/two", h2)
        assert len(adapter.routes) == 2
        assert adapter.routes["GET /one"]["method"] == "GET"
        assert adapter.routes["POST /two"]["method"] == "POST"
