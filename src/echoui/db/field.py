from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional, Type

from echoui.core.exceptions import ConfigError


@dataclass(frozen=True)
class Field:
    """数据库字段描述符。

    用于定义 ORM 模型字段的类型、约束和默认值。

    Attributes:
        field_type: Python 类型（str, int, float, bool 等）。
        max_length: 字符串字段最大长度。
        nullable: 是否允许 NULL 值。
        unique: 是否唯一约束。
        default: 默认值。
        default_factory: 默认值工厂函数。

    Examples:
        >>> name = Field(str, max_length=50, nullable=False)
        >>> name.field_type is str
        True
        >>> name.nullable
        False
    """

    field_type: Type[Any]
    max_length: Optional[int] = None
    nullable: bool = True
    unique: bool = False
    default: Any = None
    default_factory: Optional[Callable[[], Any]] = None

    def validate(self, value: Any) -> Any:
        """验证字段值。

        Args:
            value: 待验证的值。

        Returns:
            验证通过的值。

        Raises:
            ConfigError: 当值类型错误或长度超限或为 None 但字段不允许时抛出。

        Examples:
            >>> f = Field(str, max_length=5)
            >>> f.validate("hi")
            'hi'
            >>> f.validate(None)  # nullable=True 默认
        """
        if value is None:
            if self.nullable:
                return None
            raise ConfigError("字段值不能为空")

        if not isinstance(value, self.field_type):
            raise ConfigError(
                f"字段类型错误: 期望 {self.field_type.__name__}, "
                f"实际 {type(value).__name__}"
            )

        if self.max_length is not None and isinstance(value, str):
            if len(value) > self.max_length:
                raise ConfigError(
                    f"字段值长度 {len(value)} 超过最大限制 {self.max_length}"
                )

        return value

    def get_default(self) -> Any:
        """获取默认值。

        Returns:
            默认值（如果 default_factory 存在则调用它）。
        """
        if self.default_factory is not None:
            return self.default_factory()
        return self.default
