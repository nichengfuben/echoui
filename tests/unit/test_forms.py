"""Form validation tests."""

import pytest

from echoui.forms import Form, email, field, min_len, required


def test_required_validator():
    f = Form().add(field("name", required()))
    assert not f.validate({"name": ""})
    assert "name" in f.errors
    assert f.validate({"name": "Alice"})


def test_email_validator():
    f = Form().add(field("addr", email()))
    assert not f.validate({"addr": "bad"})
    assert f.validate({"addr": "a@b.co"})


def test_min_len_validator():
    f = Form().add(field("pwd", min_len(8)))
    assert not f.validate({"pwd": "short"})
    assert f.validate({"pwd": "longenough"})


def test_cross_validator():
    def match_pwd(_v, data):
        if data.get("pwd") != data.get("confirm"):
            return "Passwords must match"
        return None

    f = Form()
    f.add(field("pwd"))
    f.add(field("confirm"))
    f.add_cross(match_pwd)
    assert not f.validate({"pwd": "a", "confirm": "b"})
    assert f.validate({"pwd": "a", "confirm": "a"})


def test_wizard_steps():
    f = Form()
    f.add(field("step1", required()))
    f.add(field("step2", required()))
    f.wizard(["step1"], ["step2"])
    assert f.validate({"step1": "ok", "step2": ""})
    assert "step2" not in f.errors


@pytest.mark.asyncio
async def test_validate_async_runs_async_validator():
    calls: list[str] = []

    async def unique_name(value, _data):
        calls.append(str(value))
        if value == "taken":
            return "Name taken"
        return None

    f = Form().add(field("name", required(), unique_name))
    # sync path skips coroutine validators
    assert f.validate({"name": "taken"}) is True
    assert "name" not in f.errors

    ok = await f.validate_async({"name": "taken"})
    assert ok is False
    assert f.errors["name"] == "Name taken"
    assert "taken" in calls

    ok2 = await f.validate_async({"name": "free"})
    assert ok2 is True
    assert f.errors == {}
