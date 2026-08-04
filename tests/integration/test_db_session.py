from __future__ import annotations

import asyncio
from typing import Any

from echoui.db.field import Field
from echoui.db.model import Model
from echoui.db.session import AsyncSession


class IntegrationUser(Model):
    __tablename__ = "integration_users"
    name = Field(str, max_length=50, nullable=False)
    email = Field(str, max_length=100, nullable=True)


class TestDbSessionIntegration:
    """数据库会话集成测试。

    测试 AsyncSession 完整 CRUD 流程，
    覆盖 create/save/find/update/delete 全链路。
    """

    def _run_async(self, coro: Any) -> Any:
        return asyncio.run(coro)

    def test_full_crud_lifecycle(self) -> None:
        """测试完整 CRUD 生命周期。"""

        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()

            # Create
            user = IntegrationUser(name="张三", email="zhang@example.com")
            saved = await session.save(user)
            assert saved.id is not None
            assert saved.name == "张三"

            # Read
            found = await session.find_by_id(IntegrationUser, str(saved.id))
            assert found is not None
            assert found.name == "张三"
            assert found.email == "zhang@example.com"

            # Update
            updated = await session.update(
                IntegrationUser, str(saved.id), {"name": "李四"}
            )
            assert updated is not None
            assert updated.name == "李四"
            assert updated.id == saved.id

            # Delete
            await session.delete(IntegrationUser, str(saved.id))
            deleted = await session.find_by_id(IntegrationUser, str(saved.id))
            assert deleted is None

            await session.close()

        self._run_async(_test())

    def test_multiple_entities_interaction(self) -> None:
        """测试多个实体间的交互。"""

        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()

            users = [
                IntegrationUser(name=f"用户{i}", email=f"user{i}@test.com")
                for i in range(5)
            ]
            for u in users:
                await session.save(u)

            all_users = await session.find_all(IntegrationUser)
            assert len(all_users) == 5

            # 验证每个用户都有唯一 ID
            ids = [str(u.id) for u in all_users]
            assert len(set(ids)) == 5

            await session.close()

        self._run_async(_test())

    def test_transaction_isolation(self) -> None:
        """测试事务隔离性。"""

        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()

            # 先创建一个用户（事务外）
            outside = IntegrationUser(name="事务外", email="outside@test.com")
            await session.save(outside)

            # 事务内创建用户，然后回滚
            try:
                async with session.transaction():
                    inside = IntegrationUser(name="事务内", email="inside@test.com")
                    await session.save(inside)
                    raise RuntimeError("强制回滚")
            except RuntimeError:
                pass

            # 事务外的用户应仍在，事务内的不应存在
            all_users = await session.find_all(IntegrationUser)
            assert len(all_users) == 1
            assert all_users[0].name == "事务外"

            await session.close()

        self._run_async(_test())

    def test_query_builder_integration(self) -> None:
        """测试 QueryBuilder 与 AsyncSession 集成。"""
        from echoui.db.query_builder import QueryBuilder

        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()

            products = [
                Product(name="A", price=10.0, category="cat1") for _ in range(3)
            ] + [Product(name="B", price=20.0, category="cat2") for _ in range(2)]
            for p in products:
                await session.save(p)

            qb = QueryBuilder(Product).where(lambda p: p.category == "cat1")
            results = await qb.find_all(session)
            assert len(results) == 3

            count = await qb.count(session)
            assert count == 3

            await session.close()

        self._run_async(_test())


class Product(Model):
    __tablename__ = "integration_products"
    name = Field(str, max_length=100, nullable=False)
    price = Field(float, nullable=False)
    category = Field(str, max_length=50, nullable=True)
