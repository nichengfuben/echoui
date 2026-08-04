from __future__ import annotations

from unittest.mock import Mock

import pytest

from echoui.adapters.terminal_adapter import TerminalAdapter
from echoui.components.console_ui import ConsoleUI
from echoui.components.key_value_list import KeyValueList


class TestTerminalAdapterIntegration:
    """TerminalAdapter 集成测试。"""

    def test_run_with_console_ui(self, capsys: pytest.CaptureFixture) -> None:
        """TerminalAdapter 应能与 ConsoleUI 配合运行。"""
        ui = ConsoleUI(normal_mode=True)
        adapter = TerminalAdapter(ui)
        # ConsoleUI 没有 write 方法，terminal_adapter 需要 mock
        ui.write = Mock()
        ui.writeln = Mock()
        adapter.run()
        assert adapter._running is False

    def test_run_with_key_value_list(self) -> None:
        """TerminalAdapter 应能与 KeyValueList 配合运行。"""
        kvl = KeyValueList().add("name", "test").add("version", "2.0.0")
        kvl.write = Mock()
        kvl.writeln = Mock()
        adapter = TerminalAdapter(kvl)
        adapter.run()
        kvl.write.assert_called_once()
        kvl.writeln.assert_called_once()
        assert adapter._running is False

    def test_stop_sets_running_false(self) -> None:
        """stop() 应将 _running 设为 False。"""
        ui = Mock()
        ui.render.return_value = "output"
        adapter = TerminalAdapter(ui)
        adapter._running = True
        adapter.stop()
        assert adapter._running is False

    def test_run_async_renders_ui(self) -> None:
        """run_async() 应异步渲染 UI 组件。"""
        import asyncio

        ui = Mock()
        ui.render.return_value = "async output"
        ui._output = Mock()
        adapter = TerminalAdapter(ui)

        async def _run() -> None:
            await adapter.run_async()

        asyncio.run(_run())
        ui.render.assert_called_once()
        ui.write.assert_called()
        ui.writeln.assert_called()
        assert adapter._running is False


class TestBaseAdapterIntegration:
    """BaseAdapter 集成测试。"""

    def test_route_registration(self) -> None:
        """路由注册应正确存储在内部路由表中。"""
        adapter = TerminalAdapter(Mock())
        handler = Mock()
        adapter.register_route("GET", "/api/test", handler)
        assert "GET /api/test" in adapter.routes
        assert adapter.routes["GET /api/test"]["handler"] is handler

    def test_get_decorator(self) -> None:
        """@adapter.get() 装饰器应注册 GET 路由。"""
        adapter = TerminalAdapter(Mock())

        @adapter.get("/users")
        def get_users() -> dict:
            return {"users": []}

        assert "GET /users" in adapter.routes
        assert adapter.routes["GET /users"]["handler"] is get_users

    def test_post_decorator(self) -> None:
        """@adapter.post() 装饰器应注册 POST 路由。"""
        adapter = TerminalAdapter(Mock())

        @adapter.post("/users")
        def create_user() -> dict:
            return {"id": 1}

        assert "POST /users" in adapter.routes

    def test_put_decorator(self) -> None:
        """@adapter.put() 装饰器应注册 PUT 路由。"""
        adapter = TerminalAdapter(Mock())

        @adapter.put("/users/1")
        def update_user() -> dict:
            return {"id": 1, "updated": True}

        assert "PUT /users/1" in adapter.routes

    def test_delete_decorator(self) -> None:
        """@adapter.delete() 装饰器应注册 DELETE 路由。"""
        adapter = TerminalAdapter(Mock())

        @adapter.delete("/users/1")
        def delete_user() -> dict:
            return {"deleted": True}

        assert "DELETE /users/1" in adapter.routes

    def test_multiple_routes(self) -> None:
        """应能注册多个不同方法的路由。"""
        adapter = TerminalAdapter(Mock())
        adapter.register_route("GET", "/resource", Mock())
        adapter.register_route("POST", "/resource", Mock())
        adapter.register_route("PUT", "/resource", Mock())
        adapter.register_route("DELETE", "/resource", Mock())
        assert len(adapter.routes) == 4

    def test_route_method_uppercase(self) -> None:
        """路由方法应自动转换为大写。"""
        adapter = TerminalAdapter(Mock())
        adapter.register_route("get", "/test", Mock())
        assert "GET /test" in adapter.routes
        assert adapter.routes["GET /test"]["method"] == "GET"

    def test_host_port_properties(self) -> None:
        """host 和 port 属性应返回初始化时的值。"""
        adapter = TerminalAdapter(Mock())
        assert adapter.host == "127.0.0.1"
        assert adapter.port == 8000
