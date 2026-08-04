from __future__ import annotations

import asyncio
import sys
from typing import AsyncGenerator, Generator

import pytest

from echoui.core.renderer import GradientRenderer
from echoui.core.theme import Theme, ThemeConfig


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """创建跨平台兼容的会话级事件循环。"""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def normal_renderer() -> GradientRenderer:
    """降级模式渲染器（无 ANSI 序列）。"""
    return GradientRenderer(normal_mode=True)


@pytest.fixture
def gradient_renderer() -> GradientRenderer:
    """全特性渐变渲染器。"""
    return GradientRenderer(normal_mode=False)


@pytest.fixture
def default_theme() -> ThemeConfig:
    """返回默认主题配置。"""
    return Theme.get("default")


@pytest.fixture
def ocean_theme() -> ThemeConfig:
    """返回 ocean 主题配置。"""
    return Theme.get("ocean")


@pytest.fixture
def console_ui() -> Generator[object, None, None]:
    """创建 ConsoleUI 实例（降级模式）。"""
    from echoui.components.console_ui import ConsoleUI

    ui = ConsoleUI(normal_mode=True)
    yield ui


@pytest.fixture
def terminal_adapter() -> Generator[object, None, None]:
    """创建 TerminalAdapter 实例。"""
    from unittest.mock import Mock

    from echoui.adapters.terminal_adapter import TerminalAdapter

    ui = Mock()
    ui.render.return_value = "output"
    adapter = TerminalAdapter(ui)
    yield adapter


@pytest.fixture
def sample_table_data() -> list[list[str]]:
    """返回示例表格数据。"""
    return [
        ["1", "Alice", "alice@example.com"],
        ["2", "Bob", "bob@example.com"],
        ["3", "Charlie", "charlie@example.com"],
    ]


@pytest.fixture
def sample_tree_data() -> dict[str, object]:
    """返回示例树形数据。"""
    return {
        "src": {
            "echoui": {
                "core": {"renderer.py": {}, "theme.py": {}},
                "components": {"console_ui.py": {}},
            }
        }
    }


@pytest.fixture
async def db_session() -> AsyncGenerator[object, None]:
    """创建异步数据库会话。"""
    from echoui.db.session import AsyncSession

    session = AsyncSession()
    await session.initialize()
    yield session
    await session.close()
