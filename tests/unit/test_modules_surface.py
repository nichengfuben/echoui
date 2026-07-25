"""Overlay, i18n, and media role surface tests."""

from __future__ import annotations

from echoui import text, video
from echoui.i18n import load_catalog, set_locale, t
from echoui.overlay import OverlayState, modal, toast


def test_i18n_translate():
    load_catalog("en", {"hello": "Hello {name}"})
    set_locale("en")
    assert t("hello", name="Echo") == "Hello Echo"


def test_overlay_state():
    state = OverlayState()
    assert not state.open
    state.show("panel")
    assert state.open
    assert state.content == "panel"
    state.hide()
    assert not state.open


def test_modal_node():
    node = modal(text("x"), open=True)
    assert node.role == "box"
    assert node.props.get("role") == "modal"


def test_toast_queue():
    toast("Saved")
    toast("Done")
    from echoui.overlay import _toasts

    assert len(_toasts) >= 2


def test_video_role_factory():
    node = video(src="/demo.mp4", width=320, height=180)
    assert node.role == "video"
    assert node.props.get("src") == "/demo.mp4"
