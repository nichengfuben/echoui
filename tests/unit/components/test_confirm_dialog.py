from __future__ import annotations

from echoui.components.confirm_dialog import ConfirmDialog


class TestConfirmDialog:
    """Tests for ConfirmDialog class."""

    def test_init_with_empty_message(self) -> None:
        dialog = ConfirmDialog()
        assert dialog._message == ""

    def test_init_with_message(self) -> None:
        dialog = ConfirmDialog("Delete all files?")
        assert dialog._message == "Delete all files?"

    def test_render_with_message(self) -> None:
        dialog = ConfirmDialog("Delete all files?")
        result = dialog.render()
        assert result == "Delete all files? [y/n]:"

    def test_render_without_message(self) -> None:
        dialog = ConfirmDialog()
        result = dialog.render()
        assert result == "[y/n]:"
