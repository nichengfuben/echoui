from __future__ import annotations

from echoui.components.column_layout import ColumnLayout


class TestColumnLayout:
    """Tests for ColumnLayout class."""

    def test_render_two_columns(self) -> None:
        cols = ColumnLayout(["a\nb", "x\ny"])
        result = cols.render()
        lines = result.split("\n")
        assert len(lines) == 2
        assert lines[0] == "a  x"
        assert lines[1] == "b  y"

    def test_render_columns_with_different_widths(self) -> None:
        cols = ColumnLayout(["short", "a much longer text"])
        result = cols.render()
        lines = result.split("\n")
        assert len(lines) == 1
        assert "short" in lines[0]
        assert "a much longer text" in lines[0]

    def test_render_empty_columns(self) -> None:
        cols = ColumnLayout()
        result = cols.render()
        assert result == ""

    def test_render_none_columns(self) -> None:
        cols = ColumnLayout(columns=None)
        result = cols.render()
        assert result == ""

    def test_render_columns_with_different_heights(self) -> None:
        cols = ColumnLayout(["a\nb", "x\ny\nz"])
        result = cols.render()
        lines = result.split("\n")
        assert len(lines) == 3
        assert lines[0] == "a  x"
        assert lines[1] == "b  y"
        assert lines[2] == "   z"

    def test_render_single_column(self) -> None:
        cols = ColumnLayout(["line1\nline2"])
        result = cols.render()
        lines = result.split("\n")
        assert len(lines) == 2
        assert lines[0] == "line1"
        assert lines[1] == "line2"
