from __future__ import annotations

from echoui.db.field import Field
from echoui.db.migration import MigrationEngine
from echoui.db.model import Model


class Article(Model):
    __tablename__ = "articles"
    title = Field(str, max_length=200, nullable=False)
    body = Field(str, nullable=True)


class Comment(Model):
    __tablename__ = "comments"
    content = Field(str, max_length=500, nullable=False)


class TestMigrationEngine:
    def test_init(self) -> None:
        engine = MigrationEngine()
        assert engine._applied_migrations == []

    def test_detect_changes_creates_tables(self) -> None:
        engine = MigrationEngine()
        migrations = engine.detect_changes([Article, Comment])
        assert len(migrations) == 2
        assert migrations[0]["action"] == "create_table"
        assert migrations[0]["table"] == "articles"
        assert migrations[1]["action"] == "create_table"
        assert migrations[1]["table"] == "comments"

    def test_detect_changes_skips_empty_tablename(self) -> None:
        class NoTable(Model):
            __tablename__ = ""

        engine = MigrationEngine()
        migrations = engine.detect_changes([NoTable])
        assert len(migrations) == 0

    def test_apply_migrations(self) -> None:
        engine = MigrationEngine()
        migrations = [{"action": "create_table", "table": "articles"}]
        applied = engine.apply(migrations)
        assert len(applied) == 1
        assert applied[0] == "create_table:articles"

    def test_apply_multiple_migrations(self) -> None:
        engine = MigrationEngine()
        migrations = [
            {"action": "create_table", "table": "articles"},
            {"action": "create_table", "table": "comments"},
        ]
        applied = engine.apply(migrations)
        assert len(applied) == 2
        assert applied == ["create_table:articles", "create_table:comments"]

    def test_get_applied_returns_copy(self) -> None:
        engine = MigrationEngine()
        engine.apply([{"action": "create_table", "table": "articles"}])
        first = engine.get_applied()
        second = engine.get_applied()
        assert first == second
        assert first is not second  # 返回副本

    def test_get_applied_empty(self) -> None:
        engine = MigrationEngine()
        assert engine.get_applied() == []
