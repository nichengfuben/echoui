from __future__ import annotations

import asyncio
import logging
from typing import Any, Optional
from uuid import UUID, uuid4

from echoui.core.exceptions import ConfigError

logger = logging.getLogger(__name__)


class WebSocketConnection:
    """WebSocket 连接描述符。

    封装单个客户端连接的状态信息。
    """

    def __init__(self, connection_id: UUID, ws_object: Any) -> None:
        """初始化连接对象。

        Args:
            connection_id: 连接唯一标识。
            ws_object: 底层 WebSocket 对象（由各适配器提供）。
        """
        self.connection_id = connection_id
        self.ws_object = ws_object
        self.is_active: bool = True

    def deactivate(self) -> None:
        """标记连接为断开状态。"""
        self.is_active = False
        logger.debug("WebSocket 连接已断开: %s", self.connection_id)


class WebSocketManager:
    """WebSocket 连接管理器。

    管理所有活跃的 WebSocket 连接，支持广播消息、
    按 ID 查找连接、以及生命周期回调。

    Examples:
        >>> manager = WebSocketManager()
        >>> manager.get_connection_count()
        0
    """

    def __init__(self) -> None:
        """初始化 WebSocket 管理器。"""
        self._connections: dict[UUID, WebSocketConnection] = {}
        logger.debug("WebSocketManager 已初始化")

    async def connect(self, ws_object: Any) -> UUID:
        """注册新的 WebSocket 连接。

        Args:
            ws_object: 底层 WebSocket 对象。

        Returns:
            新连接的唯一标识。

        Raises:
            ConfigError: 当 ws_object 为 None 时抛出。
        """
        if ws_object is None:
            raise ConfigError("WebSocket 对象不能为空")
        connection_id = uuid4()
        connection = WebSocketConnection(connection_id, ws_object)
        self._connections[connection_id] = connection
        logger.info("WebSocket 连接已建立: %s", connection_id)
        return connection_id

    async def disconnect(self, connection_id: UUID) -> bool:
        """断开并移除指定连接。

        Args:
            connection_id: 连接唯一标识。

        Returns:
            是否成功移除（False 表示连接不存在）。
        """
        connection = self._connections.pop(connection_id, None)
        if connection is not None:
            connection.deactivate()
            logger.info("WebSocket 连接已移除: %s", connection_id)
            return True
        logger.warning("尝试移除不存在的连接: %s", connection_id)
        return False

    async def broadcast(self, message: Any) -> dict[UUID, bool]:
        """向所有活跃连接广播消息。

        Args:
            message: 要发送的消息内容（由各适配器序列化）。

        Returns:
            每个连接的发送结果映射（True 表示成功）。
        """
        if not self._connections:
            return {}

        results: dict[UUID, bool] = {}

        async def _send(conn_id: UUID, connection: WebSocketConnection) -> None:
            if not connection.is_active:
                results[conn_id] = False
                return
            try:
                await connection.ws_object.send_json(message)
                results[conn_id] = True
            except Exception as exc:  # noqa: BLE001
                logger.error("广播失败 %s: %s", conn_id, exc)
                results[conn_id] = False

        tasks = [_send(conn_id, conn) for conn_id, conn in self._connections.items()]
        await asyncio.gather(*tasks)
        return results

    async def send_to(self, connection_id: UUID, message: Any) -> bool:
        """向指定连接发送消息。

        Args:
            connection_id: 目标连接标识。
            message: 要发送的消息内容。

        Returns:
            是否发送成功。

        Raises:
            ConfigError: 当连接不存在时抛出。
        """
        connection = self._connections.get(connection_id)
        if connection is None:
            raise ConfigError(f"连接不存在: {connection_id}")
        if not connection.is_active:
            logger.warning("尝试向非活跃连接发送消息: %s", connection_id)
            return False
        try:
            await connection.ws_object.send_json(message)
            return True
        except Exception as exc:  # noqa: BLE001
            logger.error("发送消息失败 %s: %s", connection_id, exc)
            return False

    def get_connection(self, connection_id: UUID) -> Optional[WebSocketConnection]:
        """获取连接对象。

        Args:
            connection_id: 连接唯一标识。

        Returns:
            连接对象，不存在时返回 None。
        """
        return self._connections.get(connection_id)

    def get_active_connections(self) -> list[WebSocketConnection]:
        """获取所有活跃连接。

        Returns:
            活跃连接列表。
        """
        return [c for c in self._connections.values() if c.is_active]

    def get_connection_count(self) -> int:
        """获取活跃连接数。

        Returns:
            活跃连接数量。
        """
        return sum(1 for c in self._connections.values() if c.is_active)

    async def disconnect_all(self) -> int:
        """断开所有连接。

        Returns:
            断开的连接数量。
        """
        count = len(self._connections)
        for conn_id in list(self._connections.keys()):
            await self.disconnect(conn_id)
        logger.info("已断开所有连接，共 %d 个", count)
        return count
