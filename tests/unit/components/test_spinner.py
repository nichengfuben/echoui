from __future__ import annotations

import asyncio

from echoui.components.spinner import Spinner


class TestSpinner:
    """Tests for Spinner class."""

    def test_creates_with_defaults(self) -> None:
        s = Spinner(normal_mode=True)
        assert s._message == "Loading"
        assert s._frames == Spinner.DEFAULT_FRAMES
        assert s._interval == 0.1
        assert s.is_running is False

    def test_update_message(self) -> None:
        s = Spinner(normal_mode=True)
        result = s.update_message("Processing")
        assert result is s
        assert s._message == "Processing"

    def test_start_sets_running(self) -> None:
        s = Spinner(normal_mode=True)
        result = s.start()
        assert result is s
        assert s.is_running is True
        assert s._current_frame == 0

    def test_stop_clears_running(self) -> None:
        s = Spinner(normal_mode=True)
        s.start()
        result = s.stop()
        assert result is s
        assert s.is_running is False

    def test_render_shows_frame_and_message(self) -> None:
        s = Spinner(message="Working", normal_mode=True)
        s.start()
        result = s.render()
        assert "|" in result
        assert "Working" in result

    def test_async_context_manager(self) -> None:
        async def _test() -> None:
            s = Spinner(normal_mode=True)
            assert s.is_running is False
            async with s:
                assert s.is_running is True
            assert s.is_running is False

        asyncio.run(_test())

    def test_message_property(self) -> None:
        s = Spinner(message="Working", normal_mode=True)
        assert s.message == "Working"

    def test_next_frame_advances(self) -> None:
        s = Spinner(normal_mode=True)
        assert s._current_frame == 0
        s._next_frame()
        assert s._current_frame == 1
        s._next_frame()
        assert s._current_frame == 2

    def test_render_with_empty_frames(self) -> None:
        s = Spinner(message="Loading", frames=[], normal_mode=True)
        result = s.render()
        assert result == "Loading"
