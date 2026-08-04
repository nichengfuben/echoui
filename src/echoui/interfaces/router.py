from __future__ import annotations

import logging
from typing import Any, Callable, Optional

from echoui.core.exceptions import ConfigError

logger = logging.getLogger(__name__)


class Router:
    """路由注册器。

    管理 URL 路径到处理函数的映射，支持 HTTP 方法过滤。

    Examples:
        >>> router = Router()
        >>> async def handler() -> dict:
        ...     return {"status": "ok"}
        >>> router.add_route("GET", "/api", handler)
        >>> router.match("GET", "/api") is handler
        True
    """

    def __init__(self) -> None:
        """初始化路由注册器。"""
        self._routes: dict[str, dict[str, Callable[..., Any]]] = {}

    def add_route(self, method: str, path: str, handler: Callable[..., Any]) -> None:
        """注册路由处理器。

        Args:
            method: HTTP 方法（GET/POST/PUT/DELETE）。
            path: URL 路径。
            handler: 处理函数（可以是协程）。

        Raises:
            ConfigError: 当方法或路径为空时抛出。
        """
        if not method or not path:
            raise ConfigError("路由方法和路径不能为空")
        method_upper = method.upper()
        if method_upper not in self._routes:
            self._routes[method_upper] = {}
        self._routes[method_upper][path] = handler
        logger.debug("注册路由: %s %s", method_upper, path)

    def match(self, method: str, path: str) -> Optional[Callable[..., Any]]:
        """匹配路由处理器。

        Args:
            method: HTTP 方法。
            path: URL 路径。

        Returns:
            匹配的处理函数，未找到时返回 None。
        """
        method_upper = method.upper()
        return self._routes.get(method_upper, {}).get(path)

    def get_routes(self) -> dict[str, dict[str, Callable[..., Any]]]:
        """获取所有已注册路由。

        Returns:
            路由映射字典。
        """
        return dict(self._routes)

    def remove_route(self, method: str, path: str) -> bool:
        """移除路由。

        Args:
            method: HTTP 方法。
            path: URL 路径。

        Returns:
            是否成功移除。
        """
        method_upper = method.upper()
        if method_upper in self._routes and path in self._routes[method_upper]:
            del self._routes[method_upper][path]
            return True
        return False
