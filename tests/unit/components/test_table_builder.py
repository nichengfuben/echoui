from __future__ import annotations

import pytest

from echoui.components.table_builder import TableBuilder
from echoui.core.exceptions import ConfigError


class TestTableBuilder:
    """Tests for TableBuilder class."""

    def test_set_headers(self) -> None:
        t = TableBuilder(normal_mode=True)
        t.set_headers(["Name", "Age"])
        assert t._headers == ["Name", "Age"]
        assert t._alignments == ["left", "left"]

    def test_add_row(self) -> None:
        t = TableBuilder(normal_mode=True)
        t.set_headers(["Name", "Age"])
        t.add_row(["Alice", "30"])
        assert len(t._rows) == 1
        assert t._rows[0] == ["Alice", "30"]

    def test_add_row_length_mismatch_raises(self) -> None:
        t = TableBuilder(normal_mode=True)
        t.set_headers(["Name", "Age"])
        with pytest.raises(ConfigError, match="行长度"):
            t.add_row(["Alice"])

    def test_set_alignments(self) -> None:
        t = TableBuilder(normal_mode=True)
        t.set_headers(["Name", "Age", "Score"])
        t.set_alignments(["left", "right", "center"])
        assert t._alignments == ["left", "right", "center"]

    def test_set_invalid_alignment_raises(self) -> None:
        t = TableBuilder(normal_mode=True)
        t.set_headers(["Name", "Age"])
        with pytest.raises(ConfigError, match="非法对齐方式"):
            t.set_alignments(["left", "invalid"])

    def test_render_empty_table(self) -> None:
        t = TableBuilder(normal_mode=True)
        result = t.render()
        assert result == ""

    def test_render_with_headers_and_rows(self) -> None:
        t = TableBuilder(normal_mode=True)
        t.set_headers(["Name", "Age"])
        t.add_row(["Alice", "30"])
        t.add_row(["Bob", "25"])
        result = t.render()
        lines = result.split("\n")
        assert "Name" in lines[0]
        assert "Age" in lines[0]
        assert "-+-" in lines[1]
        assert "Alice" in lines[2]
        assert "Bob" in lines[3]

    def test_render_cjk_content(self) -> None:
        t = TableBuilder(normal_mode=True)
        t.set_headers(["姓名", "年龄"])
        t.add_row(["张三", "25"])
        result = t.render()
        lines = result.split("\n")
        assert "张三" in lines[2]

    def test_chain_methods_return_self(self) -> None:
        t = TableBuilder(normal_mode=True)
        assert t.set_headers(["A", "B"]) is t
        assert t.add_row(["1", "2"]) is t
        assert t.set_alignments(["left", "right"]) is t
