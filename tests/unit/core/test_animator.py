from __future__ import annotations

import asyncio

import pytest

from echoui.core.animator import Animator


class TestAnimator:
    def test_init_default_fps(self) -> None:
        animator = Animator()
        assert animator.fps == 30
        assert animator.frame_count == 0
        assert animator.is_running is False

    def test_init_custom_fps(self) -> None:
        animator = Animator(fps=60)
        assert animator.fps == 60

    def test_add_frame(self) -> None:
        animator = Animator()
        index = animator.add_frame(lambda: "frame")
        assert index == 0
        assert animator.frame_count == 1

    def test_add_multiple_frames(self) -> None:
        animator = Animator()
        for i in range(5):
            animator.add_frame(lambda: f"frame{i}")
        assert animator.frame_count == 5

    def test_remove_frame(self) -> None:
        animator = Animator()
        animator.add_frame(lambda: "a")
        animator.add_frame(lambda: "b")
        animator.add_frame(lambda: "c")
        animator.remove_frame(1)
        assert animator.frame_count == 2

    def test_remove_frame_index_error(self) -> None:
        animator = Animator()
        with pytest.raises(IndexError, match="越界"):
            animator.remove_frame(0)
        animator.add_frame(lambda: "x")
        with pytest.raises(IndexError, match="越界"):
            animator.remove_frame(5)

    def test_set_on_complete(self) -> None:
        animator = Animator()
        called = []
        animator.set_on_complete(lambda: called.append(True))
        assert not called
        # Trigger on_complete via run with 0 frames raises ValueError
        # So we test the setter directly
        animator._on_complete()  # type: ignore[misc]
        assert called

    def test_run_no_frames_raises(self) -> None:
        async def _test() -> None:
            animator = Animator()
            with pytest.raises(ValueError, match="没有注册的帧"):
                await animator.run()

        asyncio.run(_test())

    def test_run_single_cycle(self) -> None:
        outputs: list[str] = []

        async def _test() -> None:
            animator = Animator(fps=100)
            animator.add_frame(lambda: "frame1")
            animator.add_frame(lambda: "frame2")

            async def capture(text: str) -> None:
                outputs.append(text)

            await animator.run(cycles=1, render_fn=capture)

        asyncio.run(_test())
        assert outputs == ["frame1", "frame2"]

    def test_run_stop_flag(self) -> None:
        outputs: list[str] = []
        animator_ref: list[Animator] = []

        async def _test() -> None:
            animator = Animator(fps=100)
            animator_ref.append(animator)
            animator.add_frame(lambda: "x")

            async def capture(text: str) -> None:
                outputs.append(text)
                if len(outputs) >= 2:
                    animator.stop()

            await animator.run(cycles=10, render_fn=capture)

        asyncio.run(_test())
        assert len(outputs) <= 3
        assert animator_ref[0].is_running is False

    def test_run_on_complete_called(self) -> None:
        called = []

        async def _test() -> None:
            animator = Animator(fps=100)
            animator.add_frame(lambda: "x")
            animator.set_on_complete(lambda: called.append(True))

            await animator.run(cycles=1, render_fn=None)

        asyncio.run(_test())
        assert called

    def test_clear(self) -> None:
        animator = Animator()
        animator.add_frame(lambda: "a")
        animator.add_frame(lambda: "b")
        animator.clear()
        assert animator.frame_count == 0
        assert animator.is_running is False

    def test_stop_while_not_running(self) -> None:
        animator = Animator()
        animator.stop()  # Should not raise
        assert animator.is_running is False
