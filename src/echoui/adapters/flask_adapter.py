from __future__ import annotations

import logging
from typing import Any, Callable

from flask import Flask, jsonify

from echoui.adapters.base_adapter import BaseAdapter
from echoui.components.console_ui import ConsoleUI

logger = logging.getLogger(__name__)


class FlaskAdapter(BaseAdapter):
    """Flask Web 适配器。

    将 EchoUI 组件渲染为 Web 页面，适合轻量原型开发。

    Examples:
        >>> from echoui.components.console_ui import ConsoleUI
        >>> ui = ConsoleUI(normal_mode=True)
        >>> adapter = FlaskAdapter(ui=ui)
        >>> adapter.app is not None
        True
    """

    def __init__(
        self,
        ui: ConsoleUI,
        host: str = "127.0.0.1",
        port: int = 8000,
    ) -> None:
        """初始化 Flask 适配器。

        Args:
            ui: ConsoleUI 主控制器实例。
            host: 监听地址。
            port: 监听端口。
        """
        super().__init__(host=host, port=port)
        self._ui = ui
        self._app: Flask = Flask(__name__)
        self._setup_routes()

    @property
    def app(self) -> Flask:
        """返回 Flask Application 实例。"""
        return self._app

    @property
    def ui(self) -> ConsoleUI:
        """返回绑定的 ConsoleUI 实例。"""
        return self._ui

    def _setup_routes(self) -> None:
        """注册默认路由。"""

        @self._app.route("/")
        def index() -> Any:
            return jsonify({"status": "ok", "framework": "echoui"})

    def register_route(
        self, method: str, path: str, handler: Callable[[Any], Any]
    ) -> None:
        """注册路由到 Flask Application。

        Args:
            method: HTTP 方法。
            path: URL 路径。
            handler: 处理函数。
        """
        super().register_route(method, path, handler)
        self._app.add_url_rule(
            path,
            endpoint=f"{method}_{path}",
            view_func=handler,
            methods=[method.upper()],
        )

    def run(self) -> None:
        """同步阻塞启动 Flask 服务。"""
        logger.info("Flask 服务启动于 %s:%d", self._host, self._port)
        self._app.run(host=self._host, port=self._port)

    async def run_async(self) -> None:
        """异步启动 Flask 服务（通过线程包装）。"""
        import threading

        thread = threading.Thread(
            target=self._app.run, kwargs={"host": self._host, "port": self._port}
        )
        thread.daemon = True
        thread.start()
        logger.info("Flask 服务在后台线程启动")

    def stop(self) -> None:
        """停止 Flask 服务。

        Raises:
            NotImplementedError: Flask 开发服务器不支持程序化停止，
            需通过信号或进程管理。
        """
        raise NotImplementedError(
            "Flask 开发服务器不支持程序化停止，请使用生产服务器（如 gunicorn）"
        )
