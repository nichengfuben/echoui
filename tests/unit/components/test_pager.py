from __future__ import annotations

from echoui.components.pager import Pager


class TestPager:
    """Tests for Pager class."""

    def test_init_with_defaults(self) -> None:
        pager = Pager()
        assert pager._content == ""
        assert pager._page_size == Pager.DEFAULT_PAGE_SIZE

    def test_init_with_content(self) -> None:
        pager = Pager(content="line1\nline2\nline3")
        assert pager._content == "line1\nline2\nline3"

    def test_init_with_custom_page_size(self) -> None:
        pager = Pager(content="", page_size=10)
        assert pager._page_size == 10

    def test_render_returns_content(self) -> None:
        pager = Pager(content="hello\nworld")
        result = pager.render()
        assert result == "hello\nworld"

    def test_render_empty_content(self) -> None:
        pager = Pager()
        result = pager.render()
        assert result == ""

    def test_render_with_large_content(self) -> None:
        content = "\n".join(f"line{i}" for i in range(50))
        pager = Pager(content=content, page_size=10)
        result = pager.render()
        assert result == content
