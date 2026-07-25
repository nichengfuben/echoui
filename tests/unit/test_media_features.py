"""Media, file upload, and audio module tests."""

from __future__ import annotations

from echoui.audio import AudioEngine, TTS, audio
from echoui.compiler.emit_roles import render_role_html
from echoui.compiler.emit_web import _render_node
from echoui.compiler.ui_collect import analyze_ui
from echoui.layout import file_input, image
from echoui.sprite import IRNode, reset_id_gen


def test_audio_engine_queue():
    eng = AudioEngine()
    eng.play("jump.mp3")
    ops = eng.compile_ops()
    assert ops[0]["op"] == "play"
    assert ops[0]["src"] == "jump.mp3"


def test_file_input_emits_type_file():
    reset_id_gen()
    node = file_input("avatar", accept="image/*", signal="App.avatar_url")
    lowered = {
        "id": node.id,
        "role": "file_input",
        "tag": "input",
        "props": node.props,
        "children": [],
    }
    html = render_role_html(
        lowered,
        attrs=f' id="{node.id}"',
        cls="e-file_input",
        style_attr="",
        inner="",
        kids="",
    ) or ""
    assert 'type="file"' in html
    assert 'accept="image/*"' in html
    assert node.props.get("_file_signal") == "App.avatar_url"
    assert node.props.get("name") == "avatar"


def test_file_input_wired_in_client_cfg():
    reset_id_gen()
    root = file_input("bg", accept="image/*", signal="RunnerStore.bg_url")
    _, _, files, _ = analyze_ui(root)
    assert len(files) == 1
    assert files[0]["signal"] == "RunnerStore.bg_url"
    assert files[0]["node"] == root.id


def test_image_src_binding_collected():
    reset_id_gen()
    from echoui import Store

    class MediaStore(Store):
        url: str = ""

    ms = MediaStore()

    root = image(lambda: ms.url, width=100, height=100)
    bindings, signals, files, overlays = analyze_ui(root)
    assert any(b.get("t") == "attr" and b.get("a") == "src" for b in bindings)


def test_video_audio_tags():
    v = _render_node(
        {
            "id": "v1",
            "role": "video",
            "tag": "video",
            "props": {"src": "/a.mp4"},
            "children": [],
        }
    )
    assert "<video" in v
    a = _render_node(
        {
            "id": "a1",
            "role": "audio_player",
            "tag": "audio",
            "props": {"src": "/a.mp3"},
            "children": [],
        }
    )
    assert "<audio" in a


def test_tts_instantiate():
    t = TTS(language="zh")
    assert t.language == "zh"
    assert audio.volume == 1.0
