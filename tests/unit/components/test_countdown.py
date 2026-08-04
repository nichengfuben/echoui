from __future__ import annotations

from unittest.mock import MagicMock

from echoui.components.countdown import Countdown


class TestCountdown:
    """Tests for Countdown class."""

    def test_init_with_required_params(self) -> None:
        cd = Countdown(seconds=10)
        assert cd._seconds == 10
        assert cd._message == ""
        assert cd._on_tick is None
        assert cd._remaining == 10

    def test_init_with_all_params(self) -> None:
        callback = MagicMock()
        cd = Countdown(
            seconds=30,
            message="Shutting down",
            on_tick=callback,
            normal_mode=True,
        )
        assert cd._seconds == 30
        assert cd._message == "Shutting down"
        assert cd._on_tick is callback
        assert cd._remaining == 30
        assert cd.normal_mode is True

    def test_remaining_property(self) -> None:
        cd = Countdown(seconds=10)
        assert cd.remaining == 10

    def test_total_seconds_property(self) -> None:
        cd = Countdown(seconds=42)
        assert cd.total_seconds == 42

    def test_render_with_message(self) -> None:
        cd = Countdown(seconds=5, message="Countdown")
        result = cd.render()
        assert result == "Countdown: 5s"

    def test_render_without_message(self) -> None:
        cd = Countdown(seconds=5)
        result = cd.render()
        assert result == "5s"

    def test_render_shows_remaining(self) -> None:
        cd = Countdown(seconds=10)
        cd._remaining = 3
        result = cd.render()
        assert result == "3s"

    def test_init_sets_theme_from_parent(self) -> None:
        cd = Countdown(seconds=10)
        assert cd.theme is not None
