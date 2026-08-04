from __future__ import annotations

import asyncio
import sys
from typing import Any

if sys.version_info >= (3, 11):
    from typing import Self  # pragma: no cover
else:
    from typing_extensions import Self  # pragma: no cover

if sys.version_info >= (3, 10):
    from typing import ParamSpec, TypeAlias  # pragma: no cover
else:
    from typing_extensions import ParamSpec, TypeAlias  # pragma: no cover

if sys.version_info >= (3, 9):
    from typing import Annotated  # pragma: no cover
else:
    from typing_extensions import Annotated  # pragma: no cover


def configure_platform() -> None:
    """配置平台兼容的异步事件循环。

    在 Windows 上必须于程序最开始调用，以切换为 SelectorEventLoop，
    兼容 aiohttp 等需要 socket 操作的库。

    Examples:
        >>> configure_platform()
    """
    if sys.platform == "win32":  # pragma: no cover
        # pylint: disable-next=deprecated-class
        asyncio.set_event_loop_policy(  # pragma: no cover
            asyncio.WindowsSelectorEventLoopPolicy()  # pragma: no cover
        )  # pragma: no cover


def run_async(coro: asyncio.Future[Any]) -> Any:
    """运行异步协程并返回结果。

    跨版本兼容的异步运行器，在 Python 3.6 及以下使用旧 API。

    Args:
        coro: 待运行的协程对象。

    Returns:
        Any: 协程的返回值。

    Examples:
        >>> async def add(a, b):
        ...     return a + b
        >>> run_async(add(1, 2))
        3
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is not None:  # pragma: no cover
        # 已有事件循环，使用 asyncio.ensure_future  # pragma: no cover
        future = asyncio.ensure_future(coro, loop=loop)  # pragma: no cover
        result: list[Any] = []  # pragma: no cover
        exception: list[Exception] = []  # pragma: no cover

        def done_callback(  # pragma: no cover
            task: asyncio.Future[Any],
        ) -> None:
            try:
                result.append(task.result())
            except Exception as exc:  # pylint: disable=broad-exception-caught
                exception.append(exc)

        future.add_done_callback(done_callback)  # pragma: no cover

        # 阻塞直到完成
        while not future.done():  # pragma: no cover
            loop.run_until_complete(asyncio.sleep(0.01))  # pragma: no cover

        if exception:  # pragma: no cover
            raise exception[0]  # pragma: no cover
        return result[0]  # pragma: no cover

    # Python 3.7+ 支持 asyncio.run
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    try:
        return new_loop.run_until_complete(coro)
    finally:
        new_loop.close()


__all__ = [
    "Self",
    "ParamSpec",
    "TypeAlias",
    "Annotated",
    "configure_platform",
    "run_async",
]
