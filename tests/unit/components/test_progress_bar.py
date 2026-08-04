from __future__ import annotations

from echoui.components.progress_bar import ProgressBar


class TestProgressBar:
    """Tests for ProgressBar class."""

    def test_creates_with_defaults(self) -> None:
        bar = ProgressBar(normal_mode=True)
        assert bar.current == 0
        assert bar.total == 100
        assert bar._width == 20
        assert bar._message == ""

    def test_advance_increases_current(self) -> None:
        bar = ProgressBar(current=10, total=100, normal_mode=True)
        bar.advance(5)
        assert bar.current == 15

        bar.advance(10)
        assert bar.current == 25

    def test_set_progress_updates_current(self) -> None:
        bar = ProgressBar(current=10, total=100, normal_mode=True)
        bar.set_progress(50)
        assert bar.current == 50

    def test_finish_sets_current_to_total(self) -> None:
        bar = ProgressBar(current=30, total=100, normal_mode=True)
        bar.finish()
        assert bar.current == 100

    def test_render_normal_mode_ascii_bar(self) -> None:
        bar = ProgressBar(current=50, total=100, width=10, normal_mode=True)
        result = bar.render()
        assert "%" in result
        assert "50" in result

    def test_render_gradient_mode(self) -> None:
        bar = ProgressBar(current=50, total=100, width=10, normal_mode=False)
        result = bar.render()
        assert "%" in result

    def test_chain_methods_return_self(self) -> None:
        bar = ProgressBar(current=0, total=100, normal_mode=True)
        assert bar.advance(1) is bar
        assert bar.set_progress(50) is bar
        assert bar.finish() is bar

    def test_percentage_with_zero_total(self) -> None:
        bar = ProgressBar(current=0, total=0, normal_mode=True)
        result = bar.percentage
        assert result == 0.0

    def test_percentage_returns_float(self) -> None:
        bar = ProgressBar(current=50, total=100, normal_mode=True)
        result = bar.percentage
        assert result == 0.5

    def test_render_normal_with_message(self) -> None:
        bar = ProgressBar(
            current=50, total=100, width=10, message="Loading", normal_mode=True
        )
        result = bar.render()
        assert "Loading" in result
        assert "%" in result
