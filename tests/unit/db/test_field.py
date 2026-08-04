from __future__ import annotations

import pytest

from echoui.core.exceptions import ConfigError
from echoui.db.field import Field


class TestField:
    """Field 类型系统测试。"""

    def test_field_basic_creation(self) -> None:
        """Field 应正常创建。"""
        field = Field(str, max_length=50, nullable=False)
        assert field.field_type is str
        assert field.max_length == 50
        assert field.nullable is False

    def test_field_default_nullable(self) -> None:
        """Field 默认应 nullable=True。"""
        field = Field(str)
        assert field.nullable is True

    def test_field_default_unique(self) -> None:
        """Field 默认应 unique=False。"""
        field = Field(str)
        assert field.unique is False

    def test_field_default_value(self) -> None:
        """Field 应支持默认值。"""
        field = Field(str, default="test")
        assert field.default == "test"

    def test_field_validation_max_length_exceeded(self) -> None:
        """超过 max_length 应抛出 ConfigError。"""
        field = Field(str, max_length=5)
        with pytest.raises(ConfigError, match="长度"):
            field.validate("this is too long")

    def test_field_validation_nullable_allows_none(self) -> None:
        """nullable=True 时应允许 None。"""
        field = Field(str, nullable=True)
        assert field.validate(None) is None

    def test_field_validation_not_nullable_rejects_none(self) -> None:
        """nullable=False 时应拒绝 None。"""
        field = Field(str, nullable=False)
        with pytest.raises(ConfigError, match="不能为空"):
            field.validate(None)

    def test_field_validation_type_mismatch(self) -> None:
        """类型不匹配应抛出 ConfigError。"""
        field = Field(int)
        with pytest.raises(ConfigError, match="类型"):
            field.validate("not an int")

    def test_field_validation_string_max_length(self) -> None:
        """字符串字段应正确验证最大长度。"""
        field = Field(str, max_length=10)
        result = field.validate("short")
        assert result == "short"

    def test_field_validation_exact_max_length(self) -> None:
        """正好等于 max_length 应通过。"""
        field = Field(str, max_length=5)
        result = field.validate("abcde")
        assert result == "abcde"

    def test_field_unique_flag(self) -> None:
        """unique=True 应正确设置。"""
        field = Field(str, unique=True)
        assert field.unique is True

    def test_field_default_factory(self) -> None:
        """Field 应支持 default_factory。"""
        from uuid import uuid4

        field = Field(str, default_factory=uuid4)
        assert field.default_factory is uuid4
