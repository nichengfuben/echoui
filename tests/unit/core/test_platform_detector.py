from __future__ import annotations

from echoui.core.platform_detector import (
    TIER_FEATURE_MAP,
    PerformanceTier,
    detect_performance_tier,
)


class TestPerformanceTier:
    """Tests for PerformanceTier enum."""

    def test_performance_tier_enum_has_3(self) -> None:
        assert len(PerformanceTier) == 3

    def test_performance_tier_members(self) -> None:
        assert PerformanceTier.LOW.value == "low"
        assert PerformanceTier.MEDIUM.value == "medium"
        assert PerformanceTier.HIGH.value == "high"

    def test_performance_tier_is_str_enum(self) -> None:
        assert isinstance(PerformanceTier.LOW, str)
        assert isinstance(PerformanceTier.MEDIUM, str)
        assert isinstance(PerformanceTier.HIGH, str)


class TestTierFeatureMap:
    """Tests for TIER_FEATURE_MAP."""

    def test_tier_feature_map_has_all_tiers(self) -> None:
        assert set(TIER_FEATURE_MAP.keys()) == {
            PerformanceTier.LOW,
            PerformanceTier.MEDIUM,
            PerformanceTier.HIGH,
        }

    def test_tier_features_are_dicts(self) -> None:
        for tier, features in TIER_FEATURE_MAP.items():
            assert isinstance(features, dict)

    def test_low_tier_has_no_features(self) -> None:
        features = TIER_FEATURE_MAP[PerformanceTier.LOW]
        assert all(v is False for v in features.values())

    def test_high_tier_has_all_features(self) -> None:
        features = TIER_FEATURE_MAP[PerformanceTier.HIGH]
        assert all(v is True for v in features.values())

    def test_medium_tier_partial_features(self) -> None:
        features = TIER_FEATURE_MAP[PerformanceTier.MEDIUM]
        assert features["gradients"] is True
        assert features["animations"] is False


class TestDetectPerformanceTier:
    """Tests for detect_performance_tier function."""

    def test_detect_returns_valid_tier(self) -> None:
        tier = detect_performance_tier()
        assert isinstance(tier, PerformanceTier)

    def test_detect_returns_one_of_three_tiers(self) -> None:
        tier = detect_performance_tier()
        assert tier in (
            PerformanceTier.LOW,
            PerformanceTier.MEDIUM,
            PerformanceTier.HIGH,
        )
