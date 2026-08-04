from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, ClassVar
from uuid import UUID, uuid4

from echoui.db.field import Field as FieldDescriptor


@dataclass(init=False)
class Model:
    """EchoUI ORM 模型基类。

    所有用户定义的模型必须继承此类。
    子类通过类属性 __tablename__ 指定表名，
    通过 Field 描述符定义字段。

    Attributes:
        id: 唯一标识符，自动生成 UUID。
        created_at: 创建时间戳。
        updated_at: 更新时间戳。

    Examples:
        >>> class User(Model):
        ...     __tablename__ = "users"
        >>> user = User()
        >>> user.id is not None
        True
    """

    __tablename__: ClassVar[str] = ""
    _field_defs: ClassVar[dict[str, FieldDescriptor]] = {}

    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """子类化时缓存 Field 描述符。"""
        super().__init_subclass__(**kwargs)
        field_defs: dict[str, FieldDescriptor] = {}
        for base in cls.__mro__:
            if base is Model:
                continue
            for name, val in vars(base).items():
                if isinstance(val, FieldDescriptor):
                    field_defs[name] = val
        cls._field_defs = field_defs

    def __init__(self, **kwargs: Any) -> None:
        """初始化模型实例。

        Args:
            **kwargs: 字段值字典。
        """
        field_defs = type(self)._field_defs

        # 设置默认值
        for name, fd in field_defs.items():
            object.__setattr__(self, name, fd.get_default())

        # 覆盖传入值（Field 描述符字段）
        for key, value in kwargs.items():
            if key in field_defs:
                fd = field_defs[key]
                object.__setattr__(self, key, fd.validate(value))

        # 初始化基础字段（id/created_at/updated_at）
        object.__setattr__(self, "id", kwargs.get("id", uuid4()))
        object.__setattr__(self, "created_at", kwargs.get("created_at", datetime.now()))
        object.__setattr__(self, "updated_at", kwargs.get("updated_at", datetime.now()))

    def to_dict(self) -> dict[str, Any]:
        """将模型转换为字典。

        Returns:
            dict: 包含所有字段的字典。
        """
        result: dict[str, Any] = {
            "id": str(self.id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        for name in type(self)._field_defs:
            value = getattr(self, name, None)
            result[name] = str(value) if isinstance(value, UUID) else value
        return result
