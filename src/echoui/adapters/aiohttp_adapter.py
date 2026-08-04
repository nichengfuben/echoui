from __future__ import annotations

import logging
from typing import Any, Callable, Optional

from aiohttp import web

from echoui.adapters.base_adapter import BaseAdapter
from echoui.components.console_ui import ConsoleUI

logger = logging.getLogger(__name__)


class AiohttpAdapter(BaseAdapter):
    """aiohttp Web 适配器。

    将 EchoUI 组件渲染为 Web 页面，支持原生异步和 WebSocket。

    Examples:
        >>> from echoui.components.console_ui import ConsoleUI
        >>> ui = ConsoleUI(normal_mode=True)
        >>> adapter = AiohttpAdapter(ui=ui)
        >>> adapter.app is not None
        True
    """

    def __init__(
        self,
        ui: ConsoleUI,
        host: str = "127.0.0.1",
        port: int = 8000,
    ) -> None:
        """初始化 aiohttp 适配器。

        Args:
            ui: ConsoleUI 主控制器实例。
            host: 监听地址。
            port: 监听端口。
        """
        super().__init__(host=host, port=port)
        self._ui = ui
        self._app: web.Application = web.Application()
        self._runner: Optional[web.AppRunner] = None
        self._setup_routes()

    @property
    def app(self) -> web.Application:
        """返回 aiohttp Application 实例。"""
        return self._app

    @property
    def ui(self) -> ConsoleUI:
        """返回绑定的 ConsoleUI 实例。"""
        return self._ui

    def _setup_routes(self) -> None:
        """注册默认路由。"""
        self._app.router.add_get("/", self._handle_index)

    async def _handle_index(self, request: web.Request) -> web.Response:
        """处理根路径请求。"""
        return web.json_response({"status": "ok", "framework": "echoui"})

    def register_route(
        self, method: str, path: str, handler: Callable[[Any], Any]
    ) -> None:
        """注册路由到 aiohttp Application。

        Args:
            method: HTTP 方法。
            path: URL 路径。
            handler: 处理函数。
        """
        super().register_route(method, path, handler)
        handler_name = method.upper()
        if hasattr(self._app.router, f"add_{handler_name.lower()}"):
            add_method = getattr(self._app.router, f"add_{handler_name.lower()}")
            add_method(path, handler)

    def run(self) -> None:
        """同步阻塞启动 aiohttp 服务。"""
        import asyncio

        from echoui.utils.compat import configure_platform

        configure_platform()
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(self.run_async())
        finally:
            loop.close()

    async def run_async(self) -> None:
        """异步启动 aiohttp 服务。"""
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, self._host, self._port)
        await site.start()
        logger.info("aiohttp 服务启动于 %s:%d", self._host, self._port)

    def stop(self) -> None:
        """停止 aiohttp 服务。"""
        if self._runner is not None:
            import asyncio

            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(self._runner.cleanup())
            finally:
                loop.close()
            self._runner = None
            logger.info("aiohttp 服务已停止")
