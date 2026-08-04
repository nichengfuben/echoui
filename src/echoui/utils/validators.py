from __future__ import annotations

import re
from pathlib import Path

from echoui.core.exceptions import InputError
from echoui.utils.color import validate_hex_color

__all__ = [
    "validate_hex_color",
    "sanitize_html_content",
    "validate_upload_file",
]

_HEX_COLOR_PATTERN: re.Pattern[str] = re.compile(r"^#[0-9A-Fa-f]{6}$")
_SAFE_FILENAME_PATTERN: re.Pattern[str] = re.compile(r"^[a-zA-Z0-9_\-\.]+$")

ALLOWED_UPLOAD_EXTENSIONS: frozenset[str] = frozenset(
    {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".pdf",
        ".txt",
        ".csv",
        ".json",
    }
)
MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024


def sanitize_html_content(content: str) -> str:
    """清理 HTML 内容中的危险字符。

    Args:
        content: 待清理的字符串。

    Returns:
        str: 清理后的字符串（HTML 实体转义）。

    Examples:
        >>> sanitize_html_content("<script>alert(1)</script>")
        '&lt;script&gt;alert(1)&lt;/script&gt;'
    """
    content = content.replace("&", "&amp;")
    content = content.replace("<", "&lt;")
    content = content.replace(">", "&gt;")
    content = content.replace('"', "&quot;")
    content = content.replace("'", "&#x27;")
    return content


def validate_upload_file(
    filename: str,
    content: bytes,
) -> tuple[str, bytes]:
    """验证上传文件的合法性和大小。

    Args:
        filename: 原始文件名。
        content: 文件内容字节。

    Returns:
        tuple[str, bytes]: （文件名, 内容）元组。

    Raises:
        InputError: 当文件类型不允许或大小超限时抛出。

    Examples:
        >>> validate_upload_file("test.txt", b"hello")
        ('test.txt', b'hello')
    """
    if len(content) > MAX_UPLOAD_SIZE_BYTES:
        raise InputError(f"文件大小超出限制: {len(content)} > {MAX_UPLOAD_SIZE_BYTES}")
    suffix = Path(filename).suffix.lower()
    if suffix not in ALLOWED_UPLOAD_EXTENSIONS:
        raise InputError(
            f"文件类型不允许: {suffix!r}，" f"支持: {sorted(ALLOWED_UPLOAD_EXTENSIONS)}"
        )
    if not _SAFE_FILENAME_PATTERN.match(Path(filename).stem):
        raise InputError(f"文件名包含非法字符: {filename!r}")
    return filename, content
