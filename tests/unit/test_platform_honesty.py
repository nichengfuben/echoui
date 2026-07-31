"""Platform / mobile honesty: UnsupportedCapability for hardware; host bridges stay usable."""

from __future__ import annotations

import asyncio

import pytest

from echoui.exceptions import UnsupportedCapability
from echoui.mobile import (
    enable_mobile_sim,
    haptics_history,
    haptics_impact,
    orientation_lock,
    permissions_request,
    push_register,
)
from echoui.platform import (
    biometrics,
    bluetooth,
    clear_capability_sim,
    clipboard,
    enable_capability_sim,
    has_capability,
    nfc,
    notifications,
    printer,
    share,
)


@pytest.fixture(autouse=True)
def _reset_sim():
    clear_capability_sim()
    yield
    clear_capability_sim()


def test_host_clipboard_and_notifications_work():
    async def run():
        await clipboard.write_text("x")
        assert await clipboard.read_text() == "x"
        await share.share({"title": "t"})

    asyncio.run(run())
    notifications.show("n", body="b")
    assert notifications.history()[-1]["title"] == "n"
    assert has_capability("clipboard")


def test_hardware_apis_raise_without_sim():
    async def run():
        with pytest.raises(UnsupportedCapability):
            await biometrics.authenticate("pay")
        with pytest.raises(UnsupportedCapability):
            await bluetooth.request(services=["heart_rate"])
        with pytest.raises(UnsupportedCapability):
            await nfc.read()
        with pytest.raises(UnsupportedCapability):
            await printer.print(None)

    asyncio.run(run())


def test_capability_sim_unlocks_hardware():
    enable_capability_sim("biometrics", "bluetooth")

    async def run():
        assert await biometrics.authenticate("ok") is True
        dev = await bluetooth.request(services=["a"])
        assert dev["services"] == ["a"]

    asyncio.run(run())


def test_mobile_haptics_raise_without_sim():
    with pytest.raises(UnsupportedCapability):
        haptics_impact("medium")
    with pytest.raises(UnsupportedCapability):
        orientation_lock("landscape")

    async def run():
        with pytest.raises(UnsupportedCapability):
            await push_register()
        # Without sim, known permissions deny honestly.
        assert await permissions_request("camera") is False

    asyncio.run(run())


def test_mobile_sim_logs_haptics():
    enable_mobile_sim()
    haptics_impact("heavy")
    orientation_lock("landscape")
    assert haptics_history()[-1] == "heavy"

    async def run():
        token = await push_register()
        assert token
        assert await permissions_request("camera") is True

    asyncio.run(run())
