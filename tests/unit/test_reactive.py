"""Reactive signal and computed tests."""

from echoui.reactive import Signal, batch, computed, effect


def test_signal_notifies_subscriber():
    s = Signal(0)
    runs = []

    def fn():
        runs.append(s.value)

    effect(fn)
    assert runs == [0]
    s.set(1)
    assert runs == [0, 1]


def test_computed_caches():
    s = Signal(2)
    c = computed(lambda: s.value * 2)
    assert c.value == 4
    s.set(3)
    assert c.value == 6


def test_batch_defers_notifications():
    s = Signal(0)
    runs = []

    def fn():
        runs.append(s.value)

    effect(fn)
    with batch():
        s.set(1)
        s.set(2)
    assert runs == [0, 2]


def test_unrelated_signal_does_not_rerun():
    a = Signal(1)
    b = Signal(10)
    runs = []

    def fn():
        runs.append(a.value)

    effect(fn)
    b.set(20)
    assert runs == [1]
