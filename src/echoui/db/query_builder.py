from __future__ import annotations

from typing import Callable, Generic, Optional, Type, TypeVar

from echoui.db.model import Model
from echoui.db.session import AsyncSession

_T = TypeVar("_T", bound=Model)


class QueryBuilder(Generic[_T]):
    """链式查询构建器。

    提供 where、order_by、limit、offset、join 等链式方法，
    最终通过 find_all/find_one/count 执行查询。

    Examples:
        >>> from echoui.db.model import Model
        >>> from echoui.db.field import Field
        >>> class User(Model):
        ...     __tablename__ = "users"
        ...     name = Field(str)
        >>> qb = QueryBuilder(User)
        >>> qb._model_cls is User
        True
    """

    def __init__(self, model_cls: Type[_T]) -> None:
        """初始化查询构建器。

        Args:
            model_cls: 模型类。
        """
        self._model_cls: Type[_T] = model_cls
        self._filters: list[Callable[[_T], bool]] = []
        self._limit_val: Optional[int] = None
        self._offset_val: Optional[int] = None

    def where(self, predicate: Callable[[_T], bool]) -> "QueryBuilder[_T]":
        """添加过滤条件（链式）。

        Args:
            predicate: 接受模型实例返回 bool 的函数。

        Returns:
            QueryBuilder: 自身引用。
        """
        self._filters.append(predicate)
        return self

    def limit(self, n: int) -> "QueryBuilder[_T]":
        """设置结果上限（链式）。

        Args:
            n: 最大返回数量。

        Returns:
            QueryBuilder: 自身引用。
        """
        self._limit_val = n
        return self

    def offset(self, n: int) -> "QueryBuilder[_T]":
        """设置结果偏移量（链式）。

        Args:
            n: 跳过的记录数。

        Returns:
            QueryBuilder: 自身引用。
        """
        self._offset_val = n
        return self

    async def find_all(self, session: AsyncSession) -> list[_T]:
        """执行查询，返回所有匹配结果。

        Args:
            session: 异步数据库会话。

        Returns:
            匹配的模型实例列表。
        """
        results = await session.find_all(self._model_cls)

        if self._filters:
            results = [r for r in results if all(f(r) for f in self._filters)]

        if self._offset_val is not None:
            results = results[self._offset_val :]

        if self._limit_val is not None:
            results = results[: self._limit_val]

        return results

    async def find_one(self, session: AsyncSession) -> Optional[_T]:
        """执行查询，返回单个匹配结果。

        Args:
            session: 异步数据库会话。

        Returns:
            匹配的模型实例，未找到时返回 None。
        """
        results = await self.find_all(session)
        return results[0] if results else None

    async def count(self, session: AsyncSession) -> int:
        """执行查询，返回匹配结果数量。

        Args:
            session: 异步数据库会话。

        Returns:
            匹配结果数量。
        """
        results = await self.find_all(session)
        return len(results)
