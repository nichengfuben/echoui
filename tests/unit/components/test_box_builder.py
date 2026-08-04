from __future__ import annotations

from echoui.components.box_builder import BoxBuilder


class TestBoxBuilder:
    """Tests for BoxBuilder class."""

    def test_creates_with_defaults(self) -> None:
        box = BoxBuilder(normal_mode=True)
        assert box._content == ""
        assert box._title == ""
        assert box._border_style == "rounded"
        assert box.normal_mode is True

    def test_content_chain(self) -> None:
        box = BoxBuilder(normal_mode=True)
        result = box.content("Hello")
        assert result is box
        assert box._content == "Hello"

    def test_title_chain(self) -> None:
        box = BoxBuilder(normal_mode=True)
        result = box.title("My Title")
        assert result is box
        assert box._title == "My Title"

    def test_border_style_chain(self) -> None:
        box = BoxBuilder(normal_mode=True)
        result = box.border_style("ascii")
        assert result is box
        assert box._border_style == "ascii"

    def test_build_empty_content(self) -> None:
        box = BoxBuilder(normal_mode=True)
        result = box.build()
        lines = result.split("\n")
        assert lines[0].startswith("+")
        assert lines[-1].startswith("+")

    def test_build_with_title(self) -> None:
        box = BoxBuilder(normal_mode=True)
        box.content("Hello").title("Title")
        result = box.build()
        lines = result.split("\n")
        assert "Title" in lines[1]

    def test_build_ascii_border_normal_mode(self) -> None:
        box = BoxBuilder(normal_mode=True)
        box.content("Hi").border_style("rounded")
        result = box.build()
        assert "+" in result
        assert "-" in result

    def test_build_rounded_border(self) -> None:
        box = BoxBuilder(normal_mode=False)
        box.content("Hi").border_style("rounded")
        result = box.build()
        assert "\u256d" in result
        assert "\u256e" in result
        assert "\u2570" in result
        assert "\u256f" in result

    def test_build_method_returns_string(self) -> None:
        box = BoxBuilder(normal_mode=True)
        box.content("Test content")
        result = box.build()
        assert isinstance(result, str)
        assert "Test content" in result
