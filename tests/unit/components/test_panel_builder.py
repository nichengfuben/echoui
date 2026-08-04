from __future__ import annotations

from echoui.components.panel_builder import PanelBuilder


class TestPanelBuilder:
    """Tests for PanelBuilder class."""

    def test_title_chain(self) -> None:
        panel = PanelBuilder()
        result = panel.title("My Title")
        assert result is panel
        assert panel._title == "My Title"

    def test_content_chain(self) -> None:
        panel = PanelBuilder()
        result = panel.content("Some content")
        assert result is panel
        assert panel._content == "Some content"

    def test_render_with_title_and_content(self) -> None:
        panel = PanelBuilder()
        panel.title("Info").content("Hello")
        result = panel.render()
        lines = result.split("\n")
        assert "Info" in result
        assert "Hello" in result
        # Default mode uses Unicode border chars
        assert "\u250c" in lines[0]
        assert "\u2500" in lines[0]
