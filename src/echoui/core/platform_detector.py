from __future__ import annotations

from enum import Enum


class PerformanceTier(str, Enum):
    """性能等级枚举，用于标识当前运行环境的性能水平。

    各等级对应不同的视觉特性支持程度，低等级环境应禁用
    消耗较大的渲染特性以保证响应速度。

    Examples:
        >>> PerformanceTier.HIGH.value
        'high'
        >>> PerformanceTier.LOW.value
        'low'
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# 各性能等级对应的特性开关映射
TIER_FEATURE_MAP: dict[PerformanceTier, dict[str, bool]] = {
    PerformanceTier.LOW: {
        "gradients": False,
        "animations": False,
        "shadows": False,
        "transparency": False,
    },
    PerformanceTier.MEDIUM: {
        "gradients": True,
        "animations": False,
        "shadows": False,
        "transparency": False,
    },
    PerformanceTier.HIGH: {
        "gradients": True,
        "animations": True,
        "shadows": True,
        "transparency": True,
    },
}


def detect_performance_tier() -> PerformanceTier:
    """根据系统硬件配置检测当前性能等级。

    使用 ``psutil`` 获取 CPU 核心数和总内存大小，按以下规则判定：

    - **HIGH**: CPU 核心数 >= 8 且总内存 >= 16 GB
    - **MEDIUM**: CPU 核心数 >= 4
    - **LOW**: 其余情况

    如果 ``psutil`` 不可用或获取信息失败，则返回 ``LOW`` 作为保守默认值。

    Returns:
        检测到的性能等级。

    Examples:
        >>> tier = detect_performance_tier()
        >>> isinstance(tier, PerformanceTier)
        True
    """
    try:
        import psutil

        cpu_count = psutil.cpu_count(logical=True)
        total_memory = psutil.virtual_memory().total

        if cpu_count is not None and cpu_count >= 8 and total_memory >= 16 * 1024**3:
            return PerformanceTier.HIGH

        if cpu_count is not None and cpu_count >= 4:
            return PerformanceTier.MEDIUM

        return PerformanceTier.LOW
    except Exception:
        return PerformanceTier.LOW
