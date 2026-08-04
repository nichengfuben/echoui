from __future__ import annotations

from echoui.utils.text import (
    get_display_width,
    pad_to_width,
    repeat_char_gradient,
    truncate_to_width,
)


class TestGetDisplayWidth:
    """get_display_width 测试。"""

    def test_ascii_single_char(self) -> None:
        """ASCII 字符宽度应为 1。"""
        assert get_display_width("A") == 1

    def test_ascii_string(self) -> None:
        """ASCII 字符串宽度应为字符数。"""
        assert get_display_width("Hello") == 5

    def test_cjk_single_char(self) -> None:
        """单个 CJK 字符宽度应为 2。"""
        assert get_display_width("你") == 2

    def test_cjk_string(self) -> None:
        """CJK 字符串宽度应为每个字符 2 宽度。"""
        assert get_display_width("你好") == 4

    def test_mixed_ascii_cjk(self) -> None:
        """混合 ASCII 和 CJK 应正确计算。"""
        assert get_display_width("Hi你") == 4

    def test_empty_string(self) -> None:
        """空字符串宽度应为 0。"""
        assert get_display_width("") == 0

    def test_space_character(self) -> None:
        """空格宽度应为 1。"""
        assert get_display_width(" ") == 1

    def test_number_string(self) -> None:
        """数字字符串宽度应为字符数。"""
        assert get_display_width("12345") == 5


class TestTruncateToWidth:
    """truncate_to_width 测试。"""

    def test_truncate_ascii(self) -> None:
        """ASCII 文本截断应正确。"""
        assert truncate_to_width("Hello World", 5) == "Hello"

    def test_truncate_cjk(self) -> None:
        """CJK 文本截断应正确。"""
        assert truncate_to_width("你好世界", 4) == "你好"

    def test_truncate_mixed(self) -> None:
        """混合文本截断应正确。"""
        assert truncate_to_width("Hi你好", 4) == "Hi你"

    def test_no_truncate_needed(self) -> None:
        """文本宽度不超过目标时不应截断。"""
        assert truncate_to_width("Hi", 5) == "Hi"

    def test_zero_width(self) -> None:
        """零宽度应返回空字符串。"""
        assert truncate_to_width("Hello", 0) == ""

    def test_empty_string(self) -> None:
        """空字符串截断应返回空。"""
        assert truncate_to_width("", 5) == ""


class TestPadToWidth:
    """pad_to_width 测试。"""

    def test_pad_left(self) -> None:
        """左对齐填充应正确。"""
        result = pad_to_width("Hi", 5, align="left")
        assert result == "Hi   "
        assert get_display_width(result) == 5

    def test_pad_right(self) -> None:
        """右对齐填充应正确。"""
        result = pad_to_width("Hi", 5, align="right")
        assert result == "   Hi"
        assert get_display_width(result) == 5

    def test_pad_center(self) -> None:
        """居中对齐填充应正确。"""
        result = pad_to_width("Hi", 5, align="center")
        assert get_display_width(result) == 5

    def test_no_pad_needed(self) -> None:
        """宽度已足够时不应填充。"""
        result = pad_to_width("Hello", 5, align="left")
        assert result == "Hello"

    def test_pad_cjk(self) -> None:
        """CJK 文本填充应使用显示宽度。"""
        result = pad_to_width("你好", 6, align="left")
        assert get_display_width(result) == 6

    def test_pad_shorter_than_target(self) -> None:
        """文本短于目标时应填充。"""
        result = pad_to_width("A", 3, align="left")
        assert result == "A  "


class TestRepeatCharGradient:
    """repeat_char_gradient 测试。"""

    def test_single_char_repeat(self) -> None:
        """单字符重复应正确。"""
        result = repeat_char_gradient("=", 5)
        assert result == "====="

    def test_empty_char(self) -> None:
        """空字符应返回空字符串。"""
        result = repeat_char_gradient("", 5)
        assert result == ""

    def test_zero_count(self) -> None:
        """零次重复应返回空。"""
        result = repeat_char_gradient("=", 0)
        assert result == ""

    def test_multi_char_truncate(self) -> None:
        """多字符应按宽度截断。"""
        result = repeat_char_gradient("==", 3)
        assert get_display_width(result) == 3
