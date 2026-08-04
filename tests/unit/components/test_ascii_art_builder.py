from __future__ import annotations

from echoui.components.ascii_art_builder import AsciiArtBuilder


class TestAsciiArtBuilder:
    """Tests for AsciiArtBuilder class."""

    def test_add_line(self) -> None:
        builder = AsciiArtBuilder()
        result = builder.add_line("Hello")
        assert result is builder
        assert builder._lines == ["Hello"]

    def test_add_text_splits_on_newlines(self) -> None:
        builder = AsciiArtBuilder()
        builder.add_text("Line1\nLine2\nLine3")
        assert builder._lines == ["Line1", "Line2", "Line3"]

    def test_build_joins_lines(self) -> None:
        builder = AsciiArtBuilder()
        builder.add_line("First")
        builder.add_line("Second")
        result = builder.build()
        assert result == "First\nSecond"

    def test_render_delegates_to_build(self) -> None:
        builder = AsciiArtBuilder()
        builder.add_line("A")
        builder.add_line("B")
        assert builder.render() == builder.build()
