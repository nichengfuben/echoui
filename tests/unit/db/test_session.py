from __future__ import annotations

import asyncio
from typing import Any

import pytest

from echoui.db.field import Field
from echoui.db.model import Model
from echoui.db.session import AsyncSession, Session


class User(Model):
    __tablename__ = "users"
    name = Field(str, max_length=50, nullable=False)
    email = Field(str, max_length=100, nullable=True)


class TestSession:
    def test_initialize(self) -> None:
        session = Session()
        session.initialize()
        assert session._initialized is True

    def test_save_and_find_by_id(self) -> None:
        session = Session()
        session.initialize()
        user = User(name="张三", email="zhang@example.com")
        session.save(user)
        found = session.find_by_id(User, str(user.id))
        assert found is not None
        assert found.name == "张三"

    def test_find_by_id_not_found(self) -> None:
        session = Session()
        session.initialize()
        found = session.find_by_id(User, "nonexistent")
        assert found is None

    def test_delete(self) -> None:
        session = Session()
        session.initialize()
        user = User(name="李四")
        session.save(user)
        session.delete(User, str(user.id))
        found = session.find_by_id(User, str(user.id))
        assert found is None

    def test_find_all(self) -> None:
        session = Session()
        session.initialize()
        session.save(User(name="A"))
        session.save(User(name="B"))
        session.save(User(name="C"))
        all_users = session.find_all(User)
        assert len(all_users) == 3

    def test_save_returns_model(self) -> None:
        session = Session()
        session.initialize()
        user = User(name="test")
        result = session.save(user)
        assert result is user


class TestAsyncSession:
    def _run_async(self, coro: Any) -> Any:
        return asyncio.run(coro)

    def test_initialize(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            assert session._initialized is True
            await session.close()

        self._run_async(_test())

    def test_save_and_find_by_id(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            user = User(name="王五", email="wang@example.com")
            await session.save(user)
            found = await session.find_by_id(User, str(user.id))
            assert found is not None
            assert found.name == "王五"
            await session.close()

        self._run_async(_test())

    def test_find_by_id_not_found(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            found = await session.find_by_id(User, "nonexistent")
            assert found is None
            await session.close()

        self._run_async(_test())

    def test_delete(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            user = User(name="赵六")
            await session.save(user)
            await session.delete(User, str(user.id))
            found = await session.find_by_id(User, str(user.id))
            assert found is None
            await session.close()

        self._run_async(_test())

    def test_find_all(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            await session.save(User(name="X"))
            await session.save(User(name="Y"))
            await session.save(User(name="Z"))
            all_users = await session.find_all(User)
            assert len(all_users) == 3
            await session.close()

        self._run_async(_test())

    def test_update(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            user = User(name="旧名", email="old@example.com")
            await session.save(user)
            updated = await session.update(User, str(user.id), {"name": "新名"})
            assert updated is not None
            assert updated.name == "新名"
            assert updated.id == user.id  # ID 不变
            await session.close()

        self._run_async(_test())

    def test_update_not_found(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            result = await session.update(User, "nonexistent", {"name": "x"})
            assert result is None
            await session.close()

        self._run_async(_test())

    def test_transaction_success(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            async with session.transaction():
                user = User(name="事务内")
                await session.save(user)
            found = await session.find_by_id(User, str(user.id))
            assert found is not None
            await session.close()

        self._run_async(_test())

    def test_transaction_rollback(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            with pytest.raises(ValueError, match="测试回滚"):
                async with session.transaction():
                    user = User(name="应回滚")
                    await session.save(user)
                    raise ValueError("测试回滚")
            # 回滚后 users 表应为空
            all_users = await session.find_all(User)
            assert len(all_users) == 0
            await session.close()

        self._run_async(_test())

    def test_close(self) -> None:
        async def _test() -> None:
            session = AsyncSession()
            await session.initialize()
            await session.save(User(name="cleanup"))
            await session.close()
            assert session._initialized is False
            assert session._stores == {}

        self._run_async(_test())
