"""PLAN §15 async/concurrency module tests."""


from echoui.async_ import gather, retry, timeout
from echoui.clone import clone_pool
from echoui.tasks import background, flush
from echoui.wasm import load_wasm
from echoui.workers import worker


async def test_gather_and_timeout():
    async def a():
        return 1

    async def b():
        return 2

    assert await gather(a(), b()) == [1, 2]
    assert await timeout(a(), 1.0) == 1


async def test_retry():
    calls = {"n": 0}

    async def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise RuntimeError("fail")
        return "ok"

    assert await retry(flaky, attempts=3, delay=0) == "ok"


def test_worker_decorator_registers():
    @worker
    def heavy(x: int) -> int:
        return x * 2

    assert heavy(3) == 6


async def test_load_wasm():
    mod = await load_wasm("demo.wasm")
    mod.bind("run", lambda state: state)
    assert mod.run({"x": 1}) == {"x": 1}


def test_clone_pool_acquire_release():
    class Bullet:
        x = 0
        y = 0

        def on_clone(self):
            self.y = 0

    pool = clone_pool(Bullet, max=2)
    b1 = pool.acquire(x=1, y=2)
    pool.release(b1)
    b2 = pool.acquire(x=3)
    assert b2.x == 3


def test_background_queue():
    seen: list[int] = []

    def job():
        seen.append(1)

    background(job)
    assert flush() == 1
    assert seen == [1]
