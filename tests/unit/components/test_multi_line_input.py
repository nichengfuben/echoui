from __future__ import annotations

from echoui.components.multi_line_input import MultiLineInput


class TestMultiLineInput:
    """Tests for MultiLineInput class."""

    def test_init(self) -> None:
        mli = MultiLineInput()
        assert mli is not None

    def test_render_returns_empty_string(self) -> None:
        mli = MultiLineInput()
        result = mli.render()
        assert result == ""

    def test_init_sets_normal_mode_from_parent(self) -> None:
        mli = MultiLineInput()
        assert mli.normal_mode is False
