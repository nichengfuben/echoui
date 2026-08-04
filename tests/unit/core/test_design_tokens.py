from __future__ import annotations

from echoui.core.design_tokens import (
    BG_SHAPE_TYPES,
    RADIUS_MAP,
    SHADOW_MAP,
)


class TestRadiusToken:
    """Tests for RadiusToken dataclass."""

    def test_radius_map_has_7_entries(self) -> None:
        assert len(RADIUS_MAP) == 7

    def test_radius_map_keys(self) -> None:
        expected_keys = {"xs", "sm", "md", "lg", "xl", "2xl", "full"}
        assert set(RADIUS_MAP.keys()) == expected_keys

    def test_radius_compute_px_at_min(self) -> None:
        for name, token in RADIUS_MAP.items():
            px = token.compute_px(320)
            assert (
                px == token.min_px
            ), f"{name}: at 320px expected {token.min_px}, got {px}"

    def test_radius_compute_px_at_max(self) -> None:
        for name, token in RADIUS_MAP.items():
            px = token.compute_px(1920)
            assert (
                px == token.max_px
            ), f"{name}: at 1920px expected {token.max_px}, got {px}"

    def test_radius_compute_px_midpoint(self) -> None:
        token = RADIUS_MAP["md"]
        px = token.compute_px(1120)
        expected = round(token.min_px + (token.max_px - token.min_px) * 0.5)
        assert px == expected

    def test_radius_full_is_constant(self) -> None:
        token = RADIUS_MAP["full"]
        assert token.compute_px(320) == token.compute_px(1920)


class TestShadowToken:
    """Tests for ShadowToken dataclass."""

    def test_shadow_map_has_5_entries(self) -> None:
        assert len(SHADOW_MAP) == 5

    def test_shadow_map_keys(self) -> None:
        expected_keys = {"sm", "md", "lg", "xl", "glow"}
        assert set(SHADOW_MAP.keys()) == expected_keys

    def test_shadow_token_fields(self) -> None:
        token = SHADOW_MAP["md"]
        assert token.variable == "--shadow-md"
        assert token.blur_min_px == 2
        assert token.blur_max_px == 4
        assert token.spread_min_px == 8
        assert token.spread_max_px == 20
        assert isinstance(token.use_cases, str)

    def test_shadow_values_increase(self) -> None:
        sm = SHADOW_MAP["sm"]
        md = SHADOW_MAP["md"]
        lg = SHADOW_MAP["lg"]
        assert sm.blur_max_px < md.blur_max_px < lg.blur_max_px


class TestBGShapeTypes:
    """Tests for BG_SHAPE_TYPES constant."""

    def test_bg_shape_types_has_5(self) -> None:
        assert len(BG_SHAPE_TYPES) == 5

    def test_bg_shape_types_contents(self) -> None:
        expected = {"circle", "square", "triangle", "hexagon", "diamond"}
        assert BG_SHAPE_TYPES == expected

    def test_bg_shape_types_is_frozenset(self) -> None:
        assert isinstance(BG_SHAPE_TYPES, frozenset)
