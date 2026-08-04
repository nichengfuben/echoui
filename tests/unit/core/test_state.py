from __future__ import annotations

from echoui.core.state import State


class TestState:
    """Tests for State[T] generic class."""

    def test_state_get_initial_value(self) -> None:
        state = State(42)
        assert state.get() == 42

    def test_state_set_new_value(self) -> None:
        state = State(0)
        state.set(100)
        assert state.get() == 100

    def test_state_listener_notified(self) -> None:
        state = State(0)
        results: list[int] = []
        state.add_listener(lambda v: results.append(v))
        state.set(10)
        assert results == [10]

    def test_state_remove_listener(self) -> None:
        state = State(0)
        results: list[int] = []

        def listener(v: int) -> None:
            results.append(v)

        state.add_listener(listener)
        state.set(1)
        assert results == [1]
        state.remove_listener(listener)
        state.set(2)
        assert results == [1]

    def test_state_multiple_listeners(self) -> None:
        state = State(0)
        results_a: list[int] = []
        results_b: list[int] = []
        state.add_listener(lambda v: results_a.append(v))
        state.add_listener(lambda v: results_b.append(v * 2))
        state.set(5)
        assert results_a == [5]
        assert results_b == [10]

    def test_state_string_type(self) -> None:
        state: State[str] = State("hello")
        assert state.get() == "hello"
        state.set("world")
        assert state.get() == "world"

    def test_state_remove_nonexistent_listener(self) -> None:
        state = State(0)

        def listener(v: int) -> None:
            pass

        state.remove_listener(listener)

    def test_state_listener_order_preserved(self) -> None:
        state = State(0)
        order: list[int] = []
        state.add_listener(lambda v: order.append(1))
        state.add_listener(lambda v: order.append(2))
        state.add_listener(lambda v: order.append(3))
        state.set(1)
        assert order == [1, 2, 3]
