from __future__ import annotations

from io import StringIO

from echoui.components.console_ui import ConsoleUI


class TestConsoleUI:
    """Tests for ConsoleUI class."""

    def test_print_writes_to_stream(self) -> None:
        stream = StringIO()
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = stream
        ui.print("Hello")
        assert stream.getvalue() == "Hello\n"

    def test_newline_writes_newline(self) -> None:
        stream = StringIO()
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = stream
        ui.newline()
        assert stream.getvalue() == "\n"

    def test_rule_writes_separator(self) -> None:
        stream = StringIO()
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = stream
        ui.rule("=", 10)
        assert stream.getvalue() == "==========\n"

    def test_success_delegates_to_notification(self) -> None:
        stream = StringIO()
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = stream
        ui.success("Done")
        output = stream.getvalue()
        assert "[OK] Done" in output

    def test_error_delegates_to_notification(self) -> None:
        stream = StringIO()
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = stream
        ui.error("Failed")
        output = stream.getvalue()
        assert "[X] Failed" in output

    def test_render_returns_empty_string(self) -> None:
        ui = ConsoleUI(normal_mode=True)
        result = ui.render()
        assert result == ""

    def test_chain_methods_return_self(self) -> None:
        stream = StringIO()
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = stream
        assert ui.print("a") is ui
        assert ui.newline() is ui
        assert ui.rule("-", 5) is ui
        assert ui.success("ok") is ui
        assert ui.error("err") is ui
        assert ui.warning("warn") is ui
        assert ui.info("info") is ui

    def test_box_method_writes_boxed_content(self) -> None:
        stream = StringIO()
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = stream
        ui.box("Hello", title="Title")
        output = stream.getvalue()
        assert "Hello" in output

    def test_box_method_with_title(self) -> None:
        stream = StringIO()
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = stream
        ui.box("Content", title="My Title")
        output = stream.getvalue()
        assert "Content" in output

    def test_table_method_writes_table(self) -> None:
        stream = StringIO()
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = stream
        ui.table(["Name", "Age"], [["Alice", "30"], ["Bob", "25"]])
        output = stream.getvalue()
        assert "Name" in output
        assert "Alice" in output
        assert "Bob" in output

    def test_table_method_empty_rows(self) -> None:
        stream = StringIO()
        ui = ConsoleUI(normal_mode=True)
        ui._output_stream = stream
        ui.table(["Header1", "Header2"], [])
        output = stream.getvalue()
        assert "Header1" in output
