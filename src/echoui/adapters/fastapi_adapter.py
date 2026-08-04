from __future__ import annotations

import logging
from typing import Any, Callable

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from echoui.adapters.base_adapter import BaseAdapter
from echoui.components.console_ui import ConsoleUI

logger = logging.getLogger(__name__)


class FastAPIAdapter(BaseAdapter):
    """FastAPI Web 适配器。

    将 EchoUI 组件渲染为 Web 页面，支持自动文档和类型安全。

    Examples:
        >>> from echoui.components.console_ui import ConsoleUI
        >>> ui = ConsoleUI(normal_mode=True)
        >>> adapter = FastAPIAdapter(ui=ui)
        >>> adapter.app is not None
        True
    """

    def __init__(
        self,
        ui: ConsoleUI,
        host: str = "127.0.0.1",
        port: int = 8000,
    ) -> None:
        """初始化 FastAPI 适配器。

        Args:
            ui: ConsoleUI 主控制器实例。
            host: 监听地址。
            port: 监听端口。
        """
        super().__init__(host=host, port=port)
        self._ui = ui
        self._app: FastAPI = FastAPI(title="EchoUI")
        self._router: APIRouter = APIRouter()
        self._setup_routes()
        self._app.include_router(self._router)

    @property
    def app(self) -> FastAPI:
        """返回 FastAPI Application 实例。"""
        return self._app

    @property
    def ui(self) -> ConsoleUI:
        """返回绑定的 ConsoleUI 实例。"""
        return self._ui

    def _setup_routes(self) -> None:
        """注册默认路由。"""

        @self._router.get("/")
        async def index() -> dict[str, str]:
            return {"status": "ok", "framework": "echoui"}

    def register_route(
        self, method: str, path: str, handler: Callable[[Any], Any]
    ) -> None:
        """注册路由到 FastAPI Application。

        Args:
            method: HTTP 方法。
            path: URL 路径。
            handler: 处理函数。
        """
        super().register_route(method, path, handler)
        method_lower = method.lower()
        self._router.add_api_route(path, handler, methods=[method_lower.upper()])

    def run(self) -> None:
        """同步阻塞启动 FastAPI 服务。"""
        import uvicorn
        logger.info("FastAPI 服务启动于 %s:%d", self._host, self._port)
        uvicorn.run(self._app, host=self._host, port=self._port)

    async def run_async(self) -> None:
        """异步启动 FastAPI 服务。"""
        import uvicorn
        import asyncio
        config = uvicorn.Config(self._app, host=self._host, port=self._port)
        server = uvicorn.Server(config)
        await server.serve()

    def stop(self) -> None:
        """停止 FastAPI 服务。

        Raises:
            NotImplementedError: 需在异步上下文中通过 server.shutdown() 停止。
        """
        raise NotImplementedError(
            "FastAPI 停止需在异步上下文中调用 uvicorn.Server.shutdown()"
        )
