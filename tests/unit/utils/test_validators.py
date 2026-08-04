from __future__ import annotations

import pytest

from echoui.core.exceptions import InputError
from echoui.utils.validators import (
    sanitize_html_content,
    validate_upload_file,
)


class TestSanitizeHtmlContent:
    """sanitize_html_content 测试。"""

    def test_script_tag(self) -> None:
        """script 标签应被转义。"""
        result = sanitize_html_content("<script>alert(1)</script>")
        assert "<" not in result
        assert "&lt;script&gt;" in result

    def test_double_quote(self) -> None:
        """双引号应被转义。"""
        result = sanitize_html_content('hello "world"')
        assert "&quot;" in result

    def test_single_quote(self) -> None:
        """单引号应被转义。"""
        result = sanitize_html_content("it's")
        assert "&#x27;" in result

    def test_ampersand(self) -> None:
        """& 符号应被转义。"""
        result = sanitize_html_content("a & b")
        assert "&amp;" in result

    def test_safe_text_unchanged(self) -> None:
        """安全文本不应改变。"""
        result = sanitize_html_content("Hello World 123")
        assert result == "Hello World 123"


class TestValidateUploadFile:
    """validate_upload_file 测试。"""

    def test_valid_txt_file(self) -> None:
        """合法 txt 文件应通过验证。"""
        name, content = validate_upload_file("test.txt", b"hello")
        assert name == "test.txt"
        assert content == b"hello"

    def test_file_too_large(self) -> None:
        """超大文件应抛出 InputError。"""
        large_content = b"x" * (11 * 1024 * 1024)
        with pytest.raises(InputError, match="文件大小超出限制"):
            validate_upload_file("big.txt", large_content)

    def test_invalid_extension(self) -> None:
        """非法扩展名应抛出 InputError。"""
        with pytest.raises(InputError, match="文件类型不允许"):
            validate_upload_file("test.exe", b"data")

    def test_empty_content(self) -> None:
        """空内容应通过验证。"""
        name, content = validate_upload_file("empty.txt", b"")
        assert name == "empty.txt"
        assert content == b""
