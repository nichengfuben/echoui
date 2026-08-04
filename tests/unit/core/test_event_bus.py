from __future__ import annotations

from echoui.core.event_bus import EventBus


class TestEventBus:
    """Tests for EventBus class."""

    def test_subscribe_and_publish(self) -> None:
        bus = EventBus()
        results: list[str] = []
        bus.subscribe("greet", lambda name: results.append(f"Hello, {name}!"))
        bus.publish("greet", "World")
        assert results == ["Hello, World!"]

    def test_unsubscribe(self) -> None:
        bus = EventBus()
        results: list[str] = []

        def handler(name: str) -> None:
            results.append(name)

        bus.subscribe("event", handler)
        bus.publish("event", "first")
        assert results == ["first"]
        bus.unsubscribe("event", handler)
        bus.publish("event", "second")
        assert results == ["first"]

    def test_publish_no_handlers(self) -> None:
        bus = EventBus()
        bus.publish("nonexistent", "data")

    def test_clear(self) -> None:
        bus = EventBus()
        bus.subscribe("a", lambda: None)
        bus.subscribe("b", lambda: None)
        bus.clear()
        assert bus._handlers == {}

    def test_multiple_handlers_for_same_event(self) -> None:
        bus = EventBus()
        results: list[int] = []
        bus.subscribe("calc", lambda x: results.append(x * 2))
        bus.subscribe("calc", lambda x: results.append(x * 3))
        bus.publish("calc", 10)
        assert results == [20, 30]

    def test_publish_with_kwargs(self) -> None:
        bus = EventBus()
        collected: list[dict[str, str]] = []
        bus.subscribe("data", lambda **kw: collected.append(kw))
        bus.publish("data", key="value", foo="bar")
        assert collected == [{"key": "value", "foo": "bar"}]

    def test_unsubscribe_nonexistent_event(self) -> None:
        bus = EventBus()
        bus.unsubscribe("nonexistent", lambda: None)

    def test_subscribe_same_handler_multiple_times(self) -> None:
        bus = EventBus()
        count = [0]

        def handler() -> None:
            count[0] = count[0] + 1

        bus.subscribe("event", handler)
        bus.subscribe("event", handler)
        bus.publish("event")
        assert count[0] == 2
