from __future__ import annotations

import asyncio
from typing import Any

from echoui.db.field import Field
from echoui.db.model import Model
from echoui.db.query_builder import QueryBuilder
from echoui.db.session import AsyncSession


class Product(Model):
    __tablename__ = "products"
    name = Field(str, max_length=100, nullable=False)
    price = Field(float, nullable=False)
    category = Field(str, max_length=50, nullable=True)


class TestQueryBuilder:
    def _run_async(self, coro: Any) -> Any:
        return asyncio.run(coro)

    async def _setup_products(self, session: AsyncSession) -> None:
        await session.save(Product(name="苹果", price=5.0, category="水果"))
        await session.save(Product(name="香蕉", price=3.0, category="水果"))
        await session.save(Product(name="电脑", price=5000.0, category="电子"))
        await session.save(Product(name="手机", price=3000.0, category="电子"))
        await session.save(Product(name="橙子", price=4.0, category="水果"))

    def test_find_all_no_filters(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            await self._setup_products(session)
            qb = QueryBuilder(Product)
            results = await qb.find_all(session)
            assert len(results) == 5
            await session.close()

        self._run_async(_test())

    def test_where_filter(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            await self._setup_products(session)
            qb = QueryBuilder(Product).where(lambda p: p.category == "水果")
            results = await qb.find_all(session)
            assert len(results) == 3
            await session.close()

        self._run_async(_test())

    def test_limit(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            await self._setup_products(session)
            qb = QueryBuilder(Product).limit(2)
            results = await qb.find_all(session)
            assert len(results) == 2
            await session.close()

        self._run_async(_test())

    def test_offset(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            await self._setup_products(session)
            qb = QueryBuilder(Product).offset(3)
            results = await qb.find_all(session)
            assert len(results) == 2  # 5 - 3 = 2
            await session.close()

        self._run_async(_test())

    def test_limit_and_offset_combined(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            await self._setup_products(session)
            qb = (
                QueryBuilder(Product)
                .where(lambda p: p.category == "水果")
                .limit(2)
                .offset(1)
            )
            results = await qb.find_all(session)
            assert len(results) == 2  # 3 fruits, skip 1, take 2
            await session.close()

        self._run_async(_test())

    def test_find_one(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            await self._setup_products(session)
            qb = QueryBuilder(Product).where(lambda p: p.name == "电脑")
            result = await qb.find_one(session)
            assert result is not None
            assert result.name == "电脑"
            assert result.price == 5000.0
            await session.close()

        self._run_async(_test())

    def test_find_one_not_found(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            await self._setup_products(session)
            qb = QueryBuilder(Product).where(lambda p: p.name == "不存在")
            result = await qb.find_one(session)
            assert result is None
            await session.close()

        self._run_async(_test())

    def test_count(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            await self._setup_products(session)
            qb = QueryBuilder(Product).where(lambda p: p.category == "电子")
            count = await qb.count(session)
            assert count == 2
            await session.close()

        self._run_async(_test())

    def test_chaining_returns_self(self) -> None:
        qb = QueryBuilder(Product)
        result = qb.where(lambda p: True).limit(10).offset(5)
        assert result is qb

    def test_model_cls_stored(self) -> None:
        qb = QueryBuilder(Product)
        assert qb._model_cls is Product
