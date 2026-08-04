from __future__ import annotations

from echoui.db.model import Model


class TestModel:
    """Model 基类测试。"""

    def test_model_creates_id_automatically(self) -> None:
        """Model 应自动生成 UUID。"""
        from echoui.db.field import Field

        class User(Model):
            __tablename__ = "users"
            name = Field(str, max_length=50, nullable=False)

        user = User(name="张三")
        assert user.id is not None

    def test_model_creates_timestamps(self) -> None:
        """Model 应自动设置 created_at 和 updated_at。"""
        from echoui.db.field import Field

        class User(Model):
            __tablename__ = "users"
            name = Field(str)

        user = User(name="test")
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_model_tablename_is_classvar(self) -> None:
        """__tablename__ 应为 ClassVar。"""
        from echoui.db.field import Field

        class User(Model):
            __tablename__ = "users"
            name = Field(str)

        assert User.__tablename__ == "users"

    def test_model_fields_accessible(self) -> None:
        """Model 子类字段应可正常访问。"""
        from echoui.db.field import Field

        class User(Model):
            __tablename__ = "users"
            name = Field(str)
            email = Field(str)

        user = User(name="张三", email="z@test.com")
        assert user.name == "张三"
        assert user.email == "z@test.com"
