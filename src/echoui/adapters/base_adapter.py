from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable


class BaseAdapter(ABC):
    """适配器基类，所有 EchoUI 后端适配器必须继承此类。

    提供路由注册和服务器生命周期的统一接口。

    Examples:
        >>> class DummyAdapter(BaseAdapter):
        ...     def run(self) -> None:
        ...         pass
        ...     def run_async(self) -> None:
        ...         pass
        ...     def stop(self) -> None:
        ...         pass
        >>> adapter = DummyAdapter()
        >>> adapter.host
        '127.0.0.1'
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        """初始化适配器。

        Args:
            host: 服务器绑定地址。
            port: 服务器监听端口。
        """
        self._host = host
        self._port = port
        self._routes: dict[str, dict[str, Any]] = {}

    @property
    def host(self) -> str:
        """返回服务器绑定地址（只读）。"""
        return self._host

    @property
    def port(self) -> int:
        """返回服务器监听端口（只读）。"""
        return self._port

    @property
    def routes(self) -> dict[str, dict[str, Any]]:
        """返回已注册的路由字典（只读）。"""
        return self._routes

    def get(self, path: str) -> Callable[[Any], Any]:
        """注册 GET 路由的装饰器工厂。

        Args:
            path: URL 路径。

        Returns:
            Callable: 装饰器，用于标记处理函数。
        """

        def decorator(handler: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self.register_route("GET", path, handler)
            return handler

        return decorator

    def post(self, path: str) -> Callable[[Any], Any]:
        """注册 POST 路由的装饰器工厂。

        Args:
            path: URL 路径。

        Returns:
            Callable: 装饰器，用于标记处理函数。
        """

        def decorator(handler: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self.register_route("POST", path, handler)
            return handler

        return decorator

    def put(self, path: str) -> Callable[[Any], Any]:
        """注册 PUT 路由的装饰器工厂。

        Args:
            path: URL 路径。

        Returns:
            Callable: 装饰器，用于标记处理函数。
        """

        def decorator(handler: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self.register_route("PUT", path, handler)
            return handler

        return decorator

    def delete(self, path: str) -> Callable[[Any], Any]:
        """注册 DELETE 路由的装饰器工厂。

        Args:
            path: URL 路径。

        Returns:
            Callable: 装饰器，用于标记处理函数。
        """

        def decorator(handler: Callable[[Any], Any]) -> Callable[[Any], Any]:
            self.register_route("DELETE", path, handler)
            return handler

        return decorator

    def register_route(
        self, method: str, path: str, handler: Callable[[Any], Any]
    ) -> None:
        """注册路由到内部路由表。

        Args:
            method: HTTP 方法（GET/POST/PUT/DELETE）。
            path: URL 路径。
            handler: 处理该请求的可调用对象。
        """
        key = f"{method.upper()} {path}"
        self._routes[key] = {"method": method.upper(), "path": path, "handler": handler}

    @abstractmethod
    def run(self) -> None:
        """启动服务器（阻塞式）。"""
        ...

    @abstractmethod
    async def run_async(self) -> None:
        """启动服务器（异步式）。"""
        ...

    @abstractmethod
    def stop(self) -> None:
        """停止服务器。"""
        ...
