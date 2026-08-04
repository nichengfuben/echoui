from __future__ import annotations

from echoui.components.interactive_selector import InteractiveSelector


class TestInteractiveSelector:
    """Tests for InteractiveSelector class."""

    def test_init_with_items(self) -> None:
        selector = InteractiveSelector(["apple", "banana", "cherry"])
        assert selector._items == ["apple", "banana", "cherry"]

    def test_init_with_none_defaults_to_empty(self) -> None:
        selector = InteractiveSelector()
        assert selector._items == []

    def test_render_with_items(self) -> None:
        selector = InteractiveSelector(["apple", "banana", "cherry"])
        result = selector.render()
        assert result == "1. apple\n2. banana\n3. cherry"

    def test_render_with_single_item(self) -> None:
        selector = InteractiveSelector(["only"])
        result = selector.render()
        assert result == "1. only"

    def test_render_with_empty_list(self) -> None:
        selector = InteractiveSelector([])
        result = selector.render()
        assert result == ""

    def test_render_multiline_format(self) -> None:
        selector = InteractiveSelector(["a", "b"])
        result = selector.render()
        lines = result.split("\n")
        assert len(lines) == 2
        assert lines[0] == "1. a"
        assert lines[1] == "2. b"
