"""Benchmark reactive fine-grained updates (PLAN §3)."""

from __future__ import annotations

from echoui.reactive import Effect, Signal, batch


def run_benchmark(batch_updates: int = 1000) -> dict[str, int | bool]:
    a = Signal(0)
    b = Signal(10)
    runs_a: list[int] = []
    runs_b: list[int] = []

    Effect(lambda: runs_a.append(a.value))
    Effect(lambda: runs_b.append(b.value))

    a.set(1)
    single_ok = runs_a == [0, 1] and runs_b == [10]

    b.set(20)
    unrelated_ok = runs_a == [0, 1] and runs_b == [10, 20]

    with batch():
        for _ in range(batch_updates):
            a.set(a.value + 1)

    batch_ok = runs_a == [0, 1, 1 + batch_updates] and runs_b == [10, 20]

    return {
        "batch_updates": batch_updates,
        "single_update_ok": single_ok,
        "unrelated_ok": unrelated_ok,
        "batch_coalesce_ok": batch_ok,
        "fine_grained": single_ok and unrelated_ok and batch_ok,
    }


def main() -> None:
    result = run_benchmark()
    print("EchoUI reactive benchmark")
    print(f"  batched updates: {result['batch_updates']}")
    print(f"  single update: {'PASS' if result['single_update_ok'] else 'FAIL'}")
    print(f"  unrelated signal: {'PASS' if result['unrelated_ok'] else 'FAIL'}")
    print(f"  batch coalesce: {'PASS' if result['batch_coalesce_ok'] else 'FAIL'}")
    print(f"  fine-grained: {'PASS' if result['fine_grained'] else 'FAIL'}")
    if not result["fine_grained"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
