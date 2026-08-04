from __future__ import annotations

import pytest

from echoui.core.spacing import SPACING_MAP


class TestSpacingScale:
    """Tests for SpacingScale dataclass."""

    def test_spacing_map_has_9_entries(self) -> None:
        assert len(SPACING_MAP) == 9

    def test_spacing_map_keys(self) -> None:
        expected_keys = {"3xs", "2xs", "xs", "sm", "md", "lg", "xl", "2xl", "3xl"}
        assert set(SPACING_MAP.keys()) == expected_keys

    def test_compute_px_at_min_viewport(self) -> None:
        for name, scale in SPACING_MAP.items():
            px = scale.compute_px(320)
            assert (
                px == scale.min_px
            ), f"{name}: at 320px expected {scale.min_px}, got {px}"

    def test_compute_px_at_max_viewport(self) -> None:
        for name, scale in SPACING_MAP.items():
            px = scale.compute_px(1920)
            assert (
                px == scale.max_px
            ), f"{name}: at 1920px expected {scale.max_px}, got {px}"

    def test_compute_px_midpoint(self) -> None:
        for name, scale in SPACING_MAP.items():
            px = scale.compute_px(1120)
            expected = scale.min_px + (scale.max_px - scale.min_px) * 0.5
            assert px == expected, f"{name}: at 1120px expected {expected}, got {px}"

    @pytest.mark.parametrize("name", ["3xs", "sm", "md", "2xl"])
    def test_compute_px_linear_interpolation(self, name: str) -> None:
        scale = SPACING_MAP[name]
        px_320 = scale.compute_px(320)
        px_1920 = scale.compute_px(1920)
        px_mid = scale.compute_px(1120)
        expected_mid = (px_320 + px_1920) / 2
        assert px_mid == expected_mid

    def test_compute_px_clamped_below_min(self) -> None:
        scale = SPACING_MAP["md"]
        px = scale.compute_px(100)
        assert px == scale.min_px

    def test_compute_px_clamped_above_max(self) -> None:
        scale = SPACING_MAP["md"]
        px = scale.compute_px(3000)
        assert px == scale.max_px
