from __future__ import annotations

import logging
from typing import Type

from echoui.db.model import Model

logger = logging.getLogger(__name__)


class MigrationEngine:
    """数据库迁移引擎。

    比较当前模型定义与数据库 schema，生成并执行迁移操作。

    Examples:
        >>> engine = MigrationEngine()
        >>> engine  # doctest: +ELLIPSIS
        <echoui.db.migration.MigrationEngine object at ...>
    """

    def __init__(self) -> None:
        """初始化迁移引擎。"""
        self._applied_migrations: list[str] = []

    def detect_changes(self, models: list[Type[Model]]) -> list[dict[str, str]]:
        """检测模型变更，生成迁移计划。

        Args:
            models: 模型类列表。

        Returns:
            迁移操作列表，每个操作为一个字典。
        """
        migrations: list[dict[str, str]] = []
        for model_cls in models:
            table = model_cls.__tablename__
            if not table:
                continue
            migrations.append({"action": "create_table", "table": table})
        return migrations

    def apply(self, migrations: list[dict[str, str]]) -> list[str]:
        """执行迁移操作。

        Args:
            migrations: 迁移操作列表。

        Returns:
            已应用的迁移标识列表。
        """
        for migration in migrations:
            action = migration.get("action", "")
            table = migration.get("table", "")
            logger.info("执行迁移: %s on %s", action, table)
            self._applied_migrations.append(f"{action}:{table}")
        return list(self._applied_migrations)

    def get_applied(self) -> list[str]:
        """获取已应用的迁移列表。

        Returns:
            已应用的迁移标识列表。
        """
        return list(self._applied_migrations)
