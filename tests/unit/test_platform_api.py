"""Platform API bridge tests."""

from __future__ import annotations

import pytest

from echoui.bridge import gpu_api, os_api, web_api
from echoui.compiler.emit_web import _render_node
from echoui.exceptions import UnsupportedCapability


def test_web_api_local_storage():
    api = web_api()
    api.local_storage_set("k", "v")
    assert api.local_storage_get("k") == "v"


def test_gpu_api_web_backend():
    api = gpu_api()
    assert api.backend() == "webgpu"
    assert api.supports()


def test_os_api_raises_on_non_native():
    with pytest.raises(UnsupportedCapability):
        os_api()


def test_video_tag_emits_html5():
    html = _render_node(
        {
            "id": "v1",
            "role": "video",
            "tag": "video",
            "props": {"src": "/x.mp4", "width": 320, "height": 180},
            "children": [],
        }
    )
    assert "<video" in html
    assert 'src="/x.mp4"' in html
    assert "controls" in html


def test_audio_tag_emits_html5():
    html = _render_node(
        {
            "id": "a1",
            "role": "audio_player",
            "tag": "audio",
            "props": {"src": "/x.mp3"},
            "children": [],
        }
    )
    assert "<audio" in html
    assert 'src="/x.mp3"' in html
