from __future__ import annotations

import asyncio
import time
from io import StringIO

from echoui.components.timer import Timer


class TestTimer:
    """Tests for Timer class."""

    def test_creates_with_defaults(self) -> None:
        t = Timer(normal_mode=True)
        assert t._message == "Elapsed"
        assert t._start_time is None
        assert t._end_time is None
        assert t.elapsed == 0.0

    def test_start_records_time(self) -> None:
        t = Timer(normal_mode=True)
        result = t.start()
        assert result is t
        assert t._start_time is not None
        assert t._end_time is None
        assert t.elapsed >= 0.0

    def test_render_returns_elapsed_format(self) -> None:
        t = Timer(message="Time", normal_mode=True)
        t.start()
        time.sleep(0.01)
        t.stop()
        result = t.render()
        assert "Time:" in result
        assert "s" in result
        assert "." in result

    def test_async_context_manager(self) -> None:
        async def _test() -> None:
            t = Timer(normal_mode=True)
            assert t._start_time is None
            async with t:
                assert t._start_time is not None
                time.sleep(0.01)
            assert t._end_time is not None

        asyncio.run(_test())

    def test_print_elapsed_writes_to_stream(self) -> None:
        stream = StringIO()
        t = Timer(message="Time", normal_mode=True, _output_stream=stream)
        t.start()
        time.sleep(0.01)
        t.stop()
        result = t.print_elapsed()
        assert result is t
        output = stream.getvalue()
        assert "Time:" in output
        assert "s" in output
