from __future__ import annotations

from echoui.components.stream_writer import StreamWriter


class TestStreamWriter:
    """Tests for StreamWriter class."""

    def test_write_text_appends(self) -> None:
        sw = StreamWriter()
        result = sw.write_text("Hello")
        assert result is sw
        assert sw.render() == "Hello"

        sw.write_text(" World")
        assert sw.render() == "Hello World"

    def test_write_char_appends(self) -> None:
        sw = StreamWriter()
        result = sw.write_char("!")
        assert result is sw
        assert sw.render() == "!"

    def test_reset_clears_buffer(self) -> None:
        sw = StreamWriter()
        sw.write_text("Hello").write_char("!")
        assert sw.render() == "Hello!"
        result = sw.reset()
        assert result is sw
        assert sw.render() == ""

    def test_render_returns_buffer(self) -> None:
        sw = StreamWriter()
        sw.write_text("A")
        sw.write_text("B")
        sw.write_char("C")
        assert sw.render() == "ABC"
