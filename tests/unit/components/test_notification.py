from __future__ import annotations

from unittest.mock import MagicMock

from echoui.components.notification import Notification


class TestNotification:
    """Tests for Notification class."""

    def test_success_sets_prefix(self) -> None:
        n = Notification(normal_mode=True)
        n.success("操作成功")
        assert n._prefix == "[OK]"
        assert n._message == "操作成功"

    def test_warning_sets_prefix(self) -> None:
        n = Notification(normal_mode=True)
        n.warning("注意")
        assert n._prefix == "[!]"
        assert n._message == "注意"

    def test_error_sets_prefix(self) -> None:
        n = Notification(normal_mode=True)
        n.error("出错了")
        assert n._prefix == "[X]"
        assert n._message == "出错了"

    def test_info_sets_prefix(self) -> None:
        n = Notification(normal_mode=True)
        n.info("提示信息")
        assert n._prefix == "[i]"
        assert n._message == "提示信息"

    def test_render_normal_mode_shows_prefix(self) -> None:
        n = Notification(normal_mode=True)
        n.success("Done")
        result = n.render()
        assert result == "[OK] Done"

        n.warning("Watch out")
        result = n.render()
        assert result == "[!] Watch out"

        n.error("Fail")
        result = n.render()
        assert result == "[X] Fail"

        n.info("Heads up")
        result = n.render()
        assert result == "[i] Heads up"

    def test_chain_methods_return_self(self) -> None:
        n = Notification(normal_mode=True)
        assert n.success("a") is n
        assert n.warning("b") is n
        assert n.error("c") is n
        assert n.info("d") is n

    def test_render_gradient_mode(self) -> None:
        mock_renderer = MagicMock()
        mock_renderer.render_text_ansi.return_value = "[OK]"
        mock_theme = MagicMock()
        mock_theme.success = "green"
        mock_theme.warning = "yellow"
        mock_theme.error = "red"
        mock_theme.info = "blue"
        mock_theme.muted = "gray"

        n = Notification(
            message="Done",
            renderer=mock_renderer,
            normal_mode=False,
            theme=mock_theme,
        )
        n.success("Done")
        result = n.render()
        mock_renderer.render_text_ansi.assert_called_once_with("[OK]", "green", "green")
        assert "[OK]" in result
        assert "Done" in result

    def test_render_gradient_mode_warning(self) -> None:
        mock_renderer = MagicMock()
        mock_renderer.render_text_ansi.return_value = "[!]"
        mock_theme = MagicMock()
        mock_theme.success = "green"
        mock_theme.warning = "yellow"
        mock_theme.error = "red"
        mock_theme.info = "blue"
        mock_theme.muted = "gray"

        n = Notification(
            message="Watch out",
            renderer=mock_renderer,
            normal_mode=False,
            theme=mock_theme,
        )
        n.warning("Watch out")
        result = n.render()
        mock_renderer.render_text_ansi.assert_called_once_with(
            "[!]", "yellow", "yellow"
        )
        assert "[!]" in result

    def test_render_gradient_mode_error(self) -> None:
        mock_renderer = MagicMock()
        mock_renderer.render_text_ansi.return_value = "[X]"
        mock_theme = MagicMock()
        mock_theme.success = "green"
        mock_theme.warning = "yellow"
        mock_theme.error = "red"
        mock_theme.info = "blue"
        mock_theme.muted = "gray"

        n = Notification(
            message="Fail",
            renderer=mock_renderer,
            normal_mode=False,
            theme=mock_theme,
        )
        n.error("Fail")
        result = n.render()
        mock_renderer.render_text_ansi.assert_called_once_with("[X]", "red", "red")
        assert "[X]" in result

    def test_render_gradient_mode_info(self) -> None:
        mock_renderer = MagicMock()
        mock_renderer.render_text_ansi.return_value = "[i]"
        mock_theme = MagicMock()
        mock_theme.success = "green"
        mock_theme.warning = "yellow"
        mock_theme.error = "red"
        mock_theme.info = "blue"
        mock_theme.muted = "gray"

        n = Notification(
            message="Heads up",
            renderer=mock_renderer,
            normal_mode=False,
            theme=mock_theme,
        )
        n.info("Heads up")
        result = n.render()
        mock_renderer.render_text_ansi.assert_called_once_with("[i]", "blue", "blue")
        assert "[i]" in result
