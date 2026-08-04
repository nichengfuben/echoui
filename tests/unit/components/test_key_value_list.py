from __future__ import annotations

from echoui.components.key_value_list import KeyValueList


class TestKeyValueList:
    """Tests for KeyValueList class."""

    def test_add_pair(self) -> None:
        kvl = KeyValueList()
        result = kvl.add("name", "EchoUI")
        assert result is kvl
        assert kvl._items == {"name": "EchoUI"}

    def test_render_aligned_output(self) -> None:
        kvl = KeyValueList()
        kvl.add("name", "EchoUI")
        kvl.add("version", "1.0")
        result = kvl.render()
        lines = result.split("\n")
        assert lines[0] == "name   : EchoUI"
        assert lines[1] == "version: 1.0"

    def test_render_empty(self) -> None:
        kvl = KeyValueList()
        result = kvl.render()
        assert result == ""
