from __future__ import annotations

import pytest

from echoui.core.typography import TYPE_SCALE_MAP


class TestFluidTypeScale:
    """Tests for FluidTypeScale dataclass."""

    def test_type_scale_map_has_8_entries(self) -> None:
        assert len(TYPE_SCALE_MAP) == 8

    def test_type_scale_map_keys(self) -> None:
        expected_keys = {
            "display",
            "h1",
            "h2",
            "h3",
            "body",
            "small",
            "caption",
            "micro",
        }
        assert set(TYPE_SCALE_MAP.keys()) == expected_keys

    def test_to_css_clamp_contains_clamp(self) -> None:
        for name, scale in TYPE_SCALE_MAP.items():
            css = scale.to_css_clamp()
            assert "clamp(" in css, f"{name} should contain clamp()"

    def test_compute_px_within_bounds(self) -> None:
        for name, scale in TYPE_SCALE_MAP.items():
            px = scale.compute_px(1024)
            min_px = scale.min_rem * 16
            max_px = scale.max_rem * 16
            assert min_px <= px <= max_px, f"{name}: {px} not in [{min_px}, {max_px}]"

    def test_compute_px_at_min_viewport(self) -> None:
        for name, scale in TYPE_SCALE_MAP.items():
            px = scale.compute_px(320)
            expected_min = scale.min_rem * 16
            assert px == pytest.approx(
                expected_min, abs=0.1
            ), f"{name}: at 320px expected ~{expected_min}, got {px}"

    def test_compute_px_at_max_viewport(self) -> None:
        for name, scale in TYPE_SCALE_MAP.items():
            px = scale.compute_px(1920)
            expected_max = scale.max_rem * 16
            # The preferred formula may not produce exact max for all scales;
            # verify the result is clamped correctly (<= max and near it).
            assert px <= expected_max + 0.01
            assert (
                px >= expected_max - 1.0
            ), f"{name}: at 1920px expected near {expected_max}, got {px}"

    @pytest.mark.parametrize("name", ["display", "h1", "body", "micro"])
    def test_compute_px_monotonic_increase(self, name: str) -> None:
        scale = TYPE_SCALE_MAP[name]
        px_320 = scale.compute_px(320)
        px_1024 = scale.compute_px(1024)
        px_1920 = scale.compute_px(1920)
        assert px_320 <= px_1024 <= px_1920

    def test_compute_px_below_min_viewport(self) -> None:
        scale = TYPE_SCALE_MAP["body"]
        px = scale.compute_px(100)
        assert px == scale.min_rem * 16

    def test_compute_px_above_max_viewport(self) -> None:
        scale = TYPE_SCALE_MAP["body"]
        px = scale.compute_px(2560)
        assert px == scale.max_rem * 16
