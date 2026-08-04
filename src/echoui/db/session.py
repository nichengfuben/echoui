from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Generator, Generic, Optional, Type, TypeVar

from echoui.core.exceptions import AdapterError
from echoui.db.model import Model

logger = logging.getLogger(__name__)

_T = TypeVar("_T", bound=Model)


class Session:
    """同步数据库会话。

    提供基础的同步 CRUD 操作和事务支持。
    基于内存字典存储（用于测试和轻量场景）。

    Examples:
        >>> session = Session()
        >>> session.initialize()
    """

    def __init__(self) -> None:
        """初始化同步会话。"""
        self._stores: dict[str, dict[str, Model]] = {}
        self._initialized: bool = False

    def initialize(self) -> None:
        """初始化会话存储。"""
        self._stores = {}
        self._initialized = True

    def _get_store(self, model_cls: Type[Model]) -> dict[str, Model]:
        """获取模型对应的存储字典。"""
        table = model_cls.__tablename__
        if table not in self._stores:
            self._stores[table] = {}
        return self._stores[table]

    def save(self, model: _T) -> _T:
        """保存模型实例。

        Args:
            model: 待保存的模型实例。

        Returns:
            保存后的模型实例。
        """
        store = self._get_store(type(model))
        store[str(model.id)] = model
        return model

    def find_by_id(self, model_cls: Type[_T], model_id: str) -> Optional[_T]:
        """根据 ID 查找模型。

        Args:
            model_cls: 模型类。
            model_id: 唯一标识符。

        Returns:
            找到的模型实例，未找到时返回 None。
        """
        store = self._get_store(model_cls)
        return store.get(model_id)  # type: ignore[return-value]

    def delete(self, model_cls: Type[Model], model_id: str) -> None:
        """根据 ID 删除模型。

        Args:
            model_cls: 模型类。
            model_id: 唯一标识符。
        """
        store = self._get_store(model_cls)
        store.pop(model_id, None)

    def find_all(self, model_cls: Type[_T]) -> list[_T]:
        """查找所有模型实例。

        Args:
            model_cls: 模型类。

        Returns:
            所有模型实例列表。
        """
        store = self._get_store(model_cls)
        return list(store.values())  # type: ignore[arg-type]


class AsyncSession:
    """异步数据库会话。

    提供异步 CRUD 操作和事务上下文管理器。
    基于内存字典存储（用于测试和轻量场景）。

    Examples:
        >>> session = AsyncSession()
        >>> import asyncio
        >>> asyncio.run(session.initialize())
    """

    def __init__(self, url: str = "") -> None:
        """初始化异步会话。

        Args:
            url: 数据库连接 URL（当前为内存存储，此参数仅作兼容）。
        """
        self._stores: dict[str, dict[str, Model]] = {}
        self._initialized: bool = False
        self._url: str = url

    async def initialize(self) -> None:
        """异步初始化会话。"""
        self._stores = {}
        self._initialized = True

    async def close(self) -> None:
        """关闭会话，清理资源。"""
        self._stores = {}
        self._initialized = False

    def _get_store(self, model_cls: Type[Model]) -> dict[str, Model]:
        """获取模型对应的存储字典。"""
        table = model_cls.__tablename__
        if table not in self._stores:
            self._stores[table] = {}
        return self._stores[table]

    async def save(self, model: _T) -> _T:
        """保存模型实例。

        Args:
            model: 待保存的模型实例。

        Returns:
            保存后的模型实例。
        """
        store = self._get_store(type(model))
        store[str(model.id)] = model
        return model

    async def find_by_id(self, model_cls: Type[_T], model_id: str) -> Optional[_T]:
        """根据 ID 查找模型。

        Args:
            model_cls: 模型类。
            model_id: 唯一标识符。

        Returns:
            找到的模型实例，未找到时返回 None。
        """
        store = self._get_store(model_cls)
        return store.get(model_id)  # type: ignore[return-value]

    async def delete(self, model_cls: Type[Model], model_id: str) -> None:
        """根据 ID 删除模型。

        Args:
            model_cls: 模型类。
            model_id: 唯一标识符。
        """
        store = self._get_store(model_cls)
        store.pop(model_id, None)

    async def find_all(self, model_cls: Type[_T]) -> list[_T]:
        """查找所有模型实例。

        Args:
            model_cls: 模型类。

        Returns:
            所有模型实例列表。
        """
        store = self._get_store(model_cls)
        return list(store.values())  # type: ignore[arg-type]

    async def update(
        self, model_cls: Type[_T], model_id: str, data: dict[str, Any]
    ) -> Optional[_T]:
        """更新模型实例（不可变模式，返回新对象）。

        Args:
            model_cls: 模型类。
            model_id: 唯一标识符。
            data: 要更新的字段字典。

        Returns:
            更新后的模型实例，未找到时返回 None。
        """
        store = self._get_store(model_cls)
        existing = store.get(model_id)
        if existing is None:
            return None
        # 手动创建新实例：复制现有属性并应用更新
        updated_attrs: dict[str, Any] = {}
        for key in vars(existing):
            updated_attrs[key] = getattr(existing, key)
        updated_attrs.update(data)
        updated = model_cls(**updated_attrs)
        store[model_id] = updated
        return updated

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[AsyncSession, None]:
        """异步事务上下文管理器。

        Yields:
            AsyncSession: 当前会话实例。
        """
        snapshot = {k: dict(v) for k, v in self._stores.items()}
        try:
            yield self
        except Exception as exc:
            logger.error("事务回滚: %s", exc)
            self._stores = snapshot
            raise
