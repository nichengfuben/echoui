from __future__ import annotations

from echoui.components.block_art import BlockArt


class TestBlockArtInit:
    """BlockArt 初始化测试。"""

    def test_default_init(self) -> None:
        """默认初始化应为空文本。"""
        art = BlockArt()
        assert art.render() == ""

    def test_init_with_text(self) -> None:
        """传入文本应渲染成功。"""
        art = BlockArt(text="Hi")
        result = art.render()
        assert len(result.split("\n")) == 6

    def test_init_with_normal_mode(self) -> None:
        """normal_mode=True 应正常设置。"""
        art = BlockArt(normal_mode=True)
        assert art._normal_mode is True


class TestBlockArtRender:
    """BlockArt 渲染测试。"""

    def test_render_single_char(self) -> None:
        """单个字符应渲染为 6 行。"""
        art = BlockArt(text="A")
        result = art.render()
        lines = result.split("\n")
        assert len(lines) == 6

    def test_render_multiple_chars(self) -> None:
        """多个字符应渲染为 6 行，宽度增加。"""
        art = BlockArt(text="AB")
        result = art.render()
        lines = result.split("\n")
        assert len(lines) == 6
        assert len(lines[0]) > len(BlockArt(text="A").render().split("\n")[0])

    def test_render_empty_text(self) -> None:
        """空文本应返回空字符串。"""
        art = BlockArt(text="")
        assert art.render() == ""

    def test_render_unknown_char(self) -> None:
        """未知字符应使用空格占位。"""
        art = BlockArt(text="A@B")
        result = art.render()
        assert len(result.split("\n")) == 6

    def test_render_with_spaces(self) -> None:
        """包含空格的文本应正确渲染。"""
        art = BlockArt(text="A B")
        result = art.render()
        lines = result.split("\n")
        assert len(lines) == 6


class TestBlockArtChain:
    """BlockArt 链式调用测试。"""

    def test_text_method_returns_self(self) -> None:
        """text() 方法应返回 self。"""
        art = BlockArt()
        result = art.text("Hi")
        assert result is art

    def test_render_text_method_returns_self(self) -> None:
        """render_text() 方法应返回 self。"""
        art = BlockArt()
        result = art.render_text("Hi")
        assert result is art

    def test_chain_text_then_render(self) -> None:
        """链式设置文本后渲染。"""
        art = BlockArt()
        result = art.text("OK").render()
        assert len(result.split("\n")) == 6
        assert "OK" in art._text

    def test_chain_render_text_then_render(self) -> None:
        """链式 render_text 后渲染。"""
        art = BlockArt()
        result = art.render_text("Hi").render()
        assert len(result.split("\n")) == 6


class TestBlockArtBuild:
    """BlockArt build 方法测试。"""

    def test_build_equals_render(self) -> None:
        """build() 应与 render() 返回相同结果。"""
        art = BlockArt(text="Test")
        assert art.build() == art.render()


class TestBlockArtNormalMode:
    """BlockArt 正常模式测试。"""

    def test_normal_mode_renders(self) -> None:
        """正常模式下应仍能渲染。"""
        art = BlockArt(text="Hi", normal_mode=True)
        result = art.render()
        assert len(result.split("\n")) == 6
