"""EchoUI Web 演示程序。

展示如何使用 Web 适配器（aiohttp）运行 EchoUI。
"""
from __future__ import annotations

import sys

# 确保项目路径可用
sys.path.insert(0, "src")

from echoui import EchoUI
from echoui.interfaces.router import Router
from echoui.interfaces.websocket_manager import WebSocketManager


def main() -> None:
    """运行 Web 演示。"""
    # 初始化 EchoUI
    ui = EchoUI(normal_mode=True)

    # 初始化路由
    router = Router()

    # 初始化 WebSocket 管理器
    ws_manager = WebSocketManager()

    ui.rule("=").title("EchoUI Web 演示").rule("=").newline()

    ui.kv(
        framework="EchoUI", adapter="aiohttp", router="已初始化",
        websocket="已初始化",
    ).newline()

    # 注册示例路由
    async def index_handler() -> dict[str, str]:
        return {"status": "ok", "framework": "echoui"}

    router.add_route("GET", "/", index_handler)

    ui.box(
        "路由 GET / 已注册\nWebSocket 管理器就绪\n\n"
        "注意: 完整 Web 服务需要 aiohttp 依赖\n"
        "pip install aiohttp>=3.9",
        title="服务状态",
    ).newline()

    ui.info("Web 适配器待实现后，可运行完整服务").print()


if __name__ == "__main__":
    main()
