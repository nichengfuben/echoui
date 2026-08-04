from __future__ import annotations

from unittest.mock import Mock

from echoui.adapters.terminal_adapter import TerminalAdapter
from echoui.components.key_value_list import KeyValueList


class TestTerminalAdapter:
    """Tests for TerminalAdapter class."""

    def test_creates_with_ui(self) -> None:
        ui = KeyValueList().add("key", "value")
        adapter = TerminalAdapter(ui)
        assert adapter._ui is ui

    def test_run_starts(self) -> None:
        ui = Mock()
        ui.render.return_value = "rendered output"
        adapter = TerminalAdapter(ui)
        adapter.run()
        ui.render.assert_called_once()
        ui.write.assert_called()
        ui.writeln.assert_called()
        assert adapter._running is False

    def test_stop_stops(self) -> None:
        ui = Mock()
        ui.render.return_value = "output"
        adapter = TerminalAdapter(ui)
        adapter._running = True
        adapter.stop()
        assert adapter._running is False
