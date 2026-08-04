from __future__ import annotations

import asyncio

from echoui.utils.compat import (
    Self,
    configure_platform,
    run_async,
)


class TestCompatImports:
    """兼容性导入测试。"""

    def test_self_import(self) -> None:
        """Self 类型应可导入。"""
        from typing import Protocol

        class MyClass(Protocol):
            def clone(self) -> Self: ...

    def test_configure_platform_callable(self) -> None:
        """configure_platform 应为可调用对象。"""
        assert callable(configure_platform)

    def test_run_async_callable(self) -> None:
        """run_async 应为可调用对象。"""
        assert callable(run_async)


class TestConfigurePlatform:
    """configure_platform 测试。"""

    def test_configure_platform_no_error(self) -> None:
        """configure_platform 应无异常执行。"""
        configure_platform()

    def test_configure_platform_idempotent(self) -> None:
        """configure_platform 可多次调用。"""
        configure_platform()
        configure_platform()


class TestRunAsync:
    """run_async 测试。"""

    def test_run_async_returns_coroutine_result(self) -> None:
        """run_async 应返回协程结果。"""

        async def my_coro() -> int:
            return 42

        result = run_async(my_coro())
        assert result == 42

    def test_run_async_with_exception(self) -> None:
        """run_async 应传播异常。"""

        async def failing_coro() -> None:
            raise ValueError("test error")

        import pytest

        with pytest.raises(ValueError, match="test error"):
            run_async(failing_coro())

    def test_run_async_with_asyncio_gather(self) -> None:
        """run_async 应支持 asyncio.gather。"""

        async def coro1() -> int:
            return 1

        async def coro2() -> int:
            return 2

        async def gather_runner() -> list[int]:
            return await asyncio.gather(coro1(), coro2())

        results = run_async(gather_runner())
        assert results == [1, 2]
