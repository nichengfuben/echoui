"""Escape layer tests."""

import pytest

from echoui.bridge import os_api, web_api
from echoui.exceptions import UnsupportedCapability
from echoui.raw import RawBridge, html, js, native


def test_raw_js_node():
    node = js("console.log('hi')")
    assert node.props["kind"] == "js"


def test_raw_html_node():
    node = html("<div>raw</div>")
    assert node.props["content"] == "<div>raw</div>"


def test_raw_bridge_mount():
    bridge = RawBridge()
    called = []

    def on_mount():
        called.append(True)

    bridge.register("n1", on_mount)
    bridge.mount("n1")
    assert called == [True]


def test_raw_bridge_signal_update():
    bridge = RawBridge()
    bridge.update("count", 5)
    assert bridge.get("count") == 5


def test_web_api_storage():
    api = web_api()
    api.local_storage_set("k", "v")
    assert api.local_storage_get("k") == "v"


def test_os_api_raises():
    with pytest.raises(UnsupportedCapability):
        os_api()


def test_native_raises():
    with pytest.raises(UnsupportedCapability):
        native("code")
