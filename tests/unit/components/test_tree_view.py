from __future__ import annotations

from echoui.components.tree_view import TreeView


class TestTreeView:
    """Tests for TreeView class."""

    def test_render_simple_tree(self) -> None:
        data = {"name": "EchoUI", "version": "1.0"}
        tree = TreeView(data, normal_mode=True)
        result = tree.render()
        lines = result.split("\n")
        assert len(lines) == 2
        assert "name: EchoUI" in lines[0]
        assert "version: 1.0" in lines[1]

    def test_render_nested_tree(self) -> None:
        data = {"config": {"debug": "true", "level": "info"}}
        tree = TreeView(data, normal_mode=True)
        result = tree.render()
        assert "config" in result
        assert "debug: true" in result
        assert "level: info" in result

    def test_render_normal_mode_uses_ascii_chars(self) -> None:
        data = {"a": "1", "b": "2"}
        tree = TreeView(data, normal_mode=True)
        result = tree.render()
        assert "+" in result
        assert "|" not in result.split("\n")[0]

    def test_render_empty_tree(self) -> None:
        tree = TreeView()
        result = tree.render()
        assert result == ""

    def test_render_empty_dict(self) -> None:
        tree = TreeView(data={})
        result = tree.render()
        assert result == ""

    def test_render_color_mode_uses_unicode(self) -> None:
        data = {"a": "1", "b": "2"}
        tree = TreeView(data, normal_mode=False)
        result = tree.render()
        assert "\u251c" in result or "\u2514" in result

    def test_render_nested_color_mode(self) -> None:
        data = {"config": {"debug": "true"}}
        tree = TreeView(data, normal_mode=False)
        result = tree.render()
        assert "config" in result
        assert "debug: true" in result
