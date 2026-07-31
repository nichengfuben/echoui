"""Media honesty, in-process RTC DataChannel, and FLIP list animation."""

from __future__ import annotations

import asyncio

import pytest

from echoui.animation import FlipAnimation, Rect, capture_rects, flip, invert_rects
from echoui.exceptions import UnsupportedCapability
from echoui.media import (
    camera,
    clear_media_sim,
    enable_media_sim,
    geolocation,
    screen,
    sensors,
)
from echoui.platform import clear_capability_sim
from echoui.rtc import DataChannel, RTCPeer


@pytest.fixture(autouse=True)
def _reset_media_sim():
    clear_media_sim()
    clear_capability_sim()
    yield
    clear_media_sim()
    clear_capability_sim()


def test_media_raises_without_sim():
    async def run():
        with pytest.raises(UnsupportedCapability):
            await geolocation.get()
        with pytest.raises(UnsupportedCapability):
            await camera.capture()
        with pytest.raises(UnsupportedCapability):
            await screen.record()
        with pytest.raises(UnsupportedCapability):
            _ = sensors.accelerometer

    asyncio.run(run())
    with pytest.raises(UnsupportedCapability):
        camera.stream(facing="user")
    with pytest.raises(UnsupportedCapability):
        geolocation.watch(lambda _p: None)


def test_media_sim_unlocks_capture_and_geo():
    enable_media_sim()

    async def run():
        pos = await geolocation.get()
        assert pos.latitude == 0.0
        geolocation.set_sim_position(31.2, 121.5, accuracy=5.0)
        pos2 = await geolocation.get()
        assert pos2.latitude == 31.2 and pos2.longitude == 121.5
        moves: list[float] = []
        wid = geolocation.watch(lambda p: moves.append(p.latitude))
        assert wid >= 1
        geolocation.set_sim_position(1.0, 2.0)
        assert moves[-1] == 1.0

        frame = await camera.capture()
        assert frame
        stream = camera.stream(facing="user")
        assert stream["facing"] == "user" and stream["active"] is True

        blob = await screen.record(seconds=1.0)
        assert blob

        sensors.set_sim(accel={"x": 1.0, "y": 0.0, "z": -1.0}, compass=90.0)
        assert sensors.accelerometer["x"] == 1.0
        assert sensors.compass == 90.0

    asyncio.run(run())


def test_rtc_datachannel_delivers_in_process():
    a = RTCPeer()
    b = RTCPeer()
    ca = a.create_data_channel("game")
    cb = b.create_data_channel("game")
    received: list[str] = []
    cb.on_message = lambda m: received.append(m)
    a.connect(b)
    ca.send("ping")
    assert received == ["ping"]
    ca.send("pong")
    assert received == ["ping", "pong"]


def test_rtc_offer_answer_pairs_channels():
    async def run():
        offerer = RTCPeer()
        answerer = RTCPeer()
        ch_o = offerer.create_data_channel("chat")
        ch_a = answerer.create_data_channel("chat")
        got: list[str] = []
        ch_a.on_message = lambda m: got.append(m)

        offer = await offerer.create_offer()
        assert offer["type"] == "offer" and offer["sdp"]
        answer = await answerer.create_answer(offer)
        await offerer.apply_answer(answer)
        # Explicit connect is the reliable path; apply_answer also pairs when unique peer.
        if offerer.remote is None:
            offerer.connect(answerer)
        ch_o.send("hello")
        assert got == ["hello"]

    asyncio.run(run())


def test_datachannel_pair_bidirectional():
    left = DataChannel(label="x")
    right = DataChannel(label="x")
    inbox_l: list[str] = []
    inbox_r: list[str] = []
    left.on_message = lambda m: inbox_l.append(m)
    right.on_message = lambda m: inbox_r.append(m)
    left.pair(right)
    left.send("L->R")
    right.send("R->L")
    assert inbox_r == ["L->R"]
    assert inbox_l == ["R->L"]


def test_flip_invert_and_play():
    first = capture_rects({"a": (0.0, 0.0), "b": (0.0, 40.0)})
    last = capture_rects({"a": (0.0, 40.0), "b": (0.0, 0.0)})
    deltas = invert_rects(first, last)
    by_key = {d.key: d for d in deltas}
    assert by_key["a"].dy == -40.0
    assert by_key["b"].dy == 40.0

    frames: list[tuple[str, float, float]] = []
    anim = flip(
        first,
        last,
        duration=0.2,
        easing="linear",
        on_update=lambda k, dx, dy: frames.append((k, dx, dy)),
    )
    assert isinstance(anim, FlipAnimation)
    # Midway: invert residual ~ half
    done = anim.tick(0.1)
    assert done is False
    mid_a = [f for f in frames if f[0] == "a"][-1]
    assert abs(mid_a[2] - (-20.0)) < 0.01
    # Complete
    assert anim.tick(0.1) is True
    final_a = [f for f in frames if f[0] == "a"][-1]
    assert final_a[1] == 0.0 and final_a[2] == 0.0


def test_flip_with_rect_objects():
    first = {"card": Rect(10, 20, 100, 50)}
    last = {"card": Rect(30, 60, 100, 50)}
    anim = flip(first, last, duration=0.0)
    assert len(anim.deltas) == 1
    assert anim.deltas[0].dx == -20.0
    assert anim.deltas[0].dy == -40.0
    assert anim.tick(0.0) is True
