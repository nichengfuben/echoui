from __future__ import annotations

import wcwidth


def get_display_width(text: str) -> int:
    """计算字符串的显示宽度（考虑 CJK 全角字符）。

    使用 wcwidth 库计算每个字符的显示宽度，CJK 字符占 2 列，
    ASCII 字符占 1 列，控制字符占 0 或 -1 列。

    Args:
        text: 待计算宽度的字符串。

    Returns:
        int: 字符串的总显示宽度。

    Examples:
        >>> get_display_width("Hello")
        5
        >>> get_display_width("你好")
        4
        >>> get_display_width("Hi你")
        4
        >>> get_display_width("")
        0
    """
    total = 0
    for char in text:
        width = wcwidth.wcwidth(char)
        if width > 0:
            total += width
    return total


def truncate_to_width(text: str, max_width: int) -> str:
    """将文本截断到指定显示宽度。

    逐个字符累加显示宽度，超过 max_width 时停止。

    Args:
        text: 待截断的字符串。
        max_width: 目标显示宽度。

    Returns:
        str: 截断后的字符串。

    Examples:
        >>> truncate_to_width("Hello World", 5)
        'Hello'
        >>> truncate_to_width("你好世界", 4)
        '你好'
        >>> truncate_to_width("", 5)
        ''
    """
    if max_width <= 0:
        return ""

    result: list[str] = []
    current_width = 0
    for char in text:
        char_width = max(wcwidth.wcwidth(char), 0)
        if current_width + char_width > max_width:
            break
        result.append(char)
        current_width += char_width
    return "".join(result)


def pad_to_width(text: str, target_width: int, align: str = "left") -> str:
    """将文本填充到目标显示宽度。

    Args:
        text: 待填充的字符串。
        target_width: 目标显示宽度。
        align: 对齐方式，"left"、"right" 或 "center"。

    Returns:
        str: 填充后的字符串。

    Raises:
        ValueError: 当 align 不是 "left"、"right" 或 "center" 时。

    Examples:
        >>> pad_to_width("Hi", 5, "left")
        'Hi   '
        >>> pad_to_width("Hi", 5, "right")
        '   Hi'
    """
    current_width = get_display_width(text)
    padding_needed = max(0, target_width - current_width)

    if align == "left":
        return text + " " * padding_needed
    if align == "right":
        return " " * padding_needed + text
    if align == "center":
        left_pad = padding_needed // 2
        right_pad = padding_needed - left_pad
        return " " * left_pad + text + " " * right_pad

    raise ValueError(f"非法对齐方式: {align!r}")


def repeat_char_gradient(char: str, count: int) -> str:
    """重复字符指定次数（按显示宽度计算）。

    Args:
        char: 要重复的字符（多字符时取首字符）。
        count: 目标显示宽度。

    Returns:
        str: 重复后的字符串。

    Examples:
        >>> repeat_char_gradient("=", 5)
        '====='
        >>> repeat_char_gradient("=", 0)
        ''
    """
    if count <= 0 or not char:
        return ""

    first_char = char[0]
    char_width = wcwidth.wcwidth(first_char)
    if char_width <= 0:
        char_width = 1

    repeats = count // char_width
    return first_char * repeats
