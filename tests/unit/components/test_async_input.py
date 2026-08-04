from __future__ import annotations

from io import StringIO

from echoui.components.async_input import AsyncInput


class TestAsyncInput:
    """Tests for AsyncInput class."""

    def test_init_with_default_stream(self) -> None:
        ai = AsyncInput()
        assert ai._stream is not None

    def test_init_with_custom_stream(self) -> None:
        stream = StringIO()
        ai = AsyncInput(stream=stream)
        assert ai._stream is stream

    def test_render_returns_empty_string(self) -> None:
        ai = AsyncInput()
        result = ai.render()
        assert result == ""

    def test_init_sets_normal_mode_from_parent(self) -> None:
        ai = AsyncInput()
        assert ai.normal_mode is False
