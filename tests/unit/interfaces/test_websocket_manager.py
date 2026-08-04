from __future__ import annotations

import asyncio
from typing import Any
from uuid import UUID

import pytest

from echoui.core.exceptions import ConfigError
from echoui.interfaces.websocket_manager import WebSocketConnection, WebSocketManager


class MockWebSocket:
    """模拟 WebSocket 对象。"""

    def __init__(self) -> None:
        self.messages: list[Any] = []

    async def send_json(self, data: Any) -> None:
        self.messages.append(data)


class TestWebSocketConnection:
    def test_connection_created_active(self) -> None:
        ws = MockWebSocket()
        conn_id = UUID("00000000-0000-0000-0000-000000000001")
        conn = WebSocketConnection(conn_id, ws)
        assert conn.is_active is True
        assert conn.connection_id == conn_id
        assert conn.ws_object is ws

    def test_deactivate(self) -> None:
        ws = MockWebSocket()
        conn_id = UUID("00000000-0000-0000-0000-000000000001")
        conn = WebSocketConnection(conn_id, ws)
        conn.deactivate()
        assert conn.is_active is False


class TestWebSocketManager:
    def _run_async(self, coro: Any) -> Any:
        return asyncio.run(coro)

    def test_init(self) -> None:
        manager = WebSocketManager()
        assert manager.get_connection_count() == 0

    def test_connect(self) -> None:
        async def _test() -> None:
            manager = WebSocketManager()
            ws = MockWebSocket()
            conn_id = await manager.connect(ws)
            assert isinstance(conn_id, UUID)
            assert manager.get_connection_count() == 1
            await manager.disconnect_all()

        self._run_async(_test())

    def test_connect_none_raises(self) -> None:
        async def _test() -> None:
            manager = WebSocketManager()
            with pytest.raises(ConfigError, match="WebSocket 对象不能为空"):
                await manager.connect(None)

        self._run_async(_test())

    def test_disconnect(self) -> None:
        async def _test() -> None:
            manager = WebSocketManager()
            ws = MockWebSocket()
            conn_id = await manager.connect(ws)
            result = await manager.disconnect(conn_id)
            assert result is True
            assert manager.get_connection_count() == 0

        self._run_async(_test())

    def test_disconnect_nonexistent(self) -> None:
        async def _test() -> None:
            manager = WebSocketManager()
            fake_id = UUID("00000000-0000-0000-0000-000000000099")
            result = await manager.disconnect(fake_id)
            assert result is False

        self._run_async(_test())

    def test_get_connection(self) -> None:
        async def _test() -> None:
            manager = WebSocketManager()
            ws = MockWebSocket()
            conn_id = await manager.connect(ws)
            conn = manager.get_connection(conn_id)
            assert conn is not None
            assert conn.connection_id == conn_id
            await manager.disconnect_all()

        self._run_async(_test())

    def test_get_connection_not_found(self) -> None:
        manager = WebSocketManager()
        fake_id = UUID("00000000-0000-0000-0000-000000000099")
        conn = manager.get_connection(fake_id)
        assert conn is None

    def test_get_active_connections(self) -> None:
        async def _test() -> None:
            manager = WebSocketManager()
            ws1 = MockWebSocket()
            ws2 = MockWebSocket()
            id1 = await manager.connect(ws1)
            id2 = await manager.connect(ws2)
            await manager.disconnect(id1)
            active = manager.get_active_connections()
            assert len(active) == 1
            assert active[0].connection_id == id2
            await manager.disconnect_all()

        self._run_async(_test())

    def test_broadcast(self) -> None:
        async def _test() -> None:
            manager = WebSocketManager()
            ws1 = MockWebSocket()
            ws2 = MockWebSocket()
            await manager.connect(ws1)
            await manager.connect(ws2)
            results = await manager.broadcast({"type": "ping"})
            assert len(results) == 2
            assert all(results.values())
            assert ws1.messages == [{"type": "ping"}]
            assert ws2.messages == [{"type": "ping"}]
            await manager.disconnect_all()

        self._run_async(_test())

    def test_send_to(self) -> None:
        async def _test() -> None:
            manager = WebSocketManager()
            ws = MockWebSocket()
            conn_id = await manager.connect(ws)
            result = await manager.send_to(conn_id, {"msg": "hello"})
            assert result is True
            assert ws.messages == [{"msg": "hello"}]
            await manager.disconnect_all()

        self._run_async(_test())

    def test_send_to_nonexistent_raises(self) -> None:
        async def _test() -> None:
            manager = WebSocketManager()
            fake_id = UUID("00000000-0000-0000-0000-000000000099")
            with pytest.raises(ConfigError, match="连接不存在"):
                await manager.send_to(fake_id, {"msg": "x"})

        self._run_async(_test())

    def test_send_to_inactive(self) -> None:
        async def _test() -> None:
            manager = WebSocketManager()
            ws = MockWebSocket()
            conn_id = await manager.connect(ws)
            conn = manager.get_connection(conn_id)
            assert conn is not None
            conn.deactivate()
            result = await manager.send_to(conn_id, {"msg": "x"})
            assert result is False

        self._run_async(_test())

    def test_disconnect_all(self) -> None:
        async def _test() -> None:
            manager = WebSocketManager()
            await manager.connect(MockWebSocket())
            await manager.connect(MockWebSocket())
            await manager.connect(MockWebSocket())
            count = await manager.disconnect_all()
            assert count == 3
            assert manager.get_connection_count() == 0

        self._run_async(_test())
