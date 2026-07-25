"""Animation tween/spring tests."""

from __future__ import annotations

from echoui.animation import ease_out, spring, tween


def test_tween_completes():
    values: list[float] = []
    t = tween(0, 100, duration=0.5, on_update=values.append, easing=ease_out)
    done = False
    while not done:
        done = t.tick(0.05)
    assert done
    assert values[-1] == 100


def test_spring_converges():
    values: list[float] = []
    s = spring(50, current=0, on_update=values.append)
    for _ in range(200):
        if s.tick(0.016):
            break
    assert abs(values[-1] - 50) < 1.0


def test_timeline_all_tweens():
    from echoui.animation import Timeline

    tl = Timeline()
    a, b = tween(0, 1, 0.1), tween(0, 2, 0.2)
    tl.add(a).add(b)
    assert tl.tick(0.05) is False
    assert tl.tick(0.2) is True
