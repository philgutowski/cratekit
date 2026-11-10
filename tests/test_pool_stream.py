"""U241: the pool's third seam, results read one position at a time.

``stream_workers`` exists so a job engine that settles one item, makes it
durable and only then asks for the next can still have its measuring done
ahead of it. What is driven here, on real spawned children wherever a child is
the claim:

1. a plan of one worker is the loop it replaced, in this process, on demand;
2. a wider plan gives the results ``map_workers`` gives, whatever order they
   are read in, and each position is read once on both paths;
3. what the work raised reaches the reader of that position and nobody else;
4. a worker that died is ``StreamBroken``, which is about the pool and not
   the item;
5. the terminal's interrupt does not kill a worker, a close does not wait for
   work nobody will read, and a parent killed outright does not leave its
   workers behind.

Every plan here is planned, from an injected reading, never built by hand.
"""

from __future__ import annotations

import multiprocessing
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

from cratekit.core import pool

GIB = 1024**3
SRC_ROOT = Path(__file__).resolve().parent.parent / "src"

_LOADED: dict[str, str] = {}


def _calm() -> pool.Pressure:
    return pool.Pressure(swap_used_bytes=0, used_percent=10.0)


def _roomy() -> int:
    return 64 * GIB


def _tight() -> int:
    return 2 * GIB


def wide(items: int, *, workers: int = 2, tasks: int | None = 100) -> pool.PoolPlan:
    plan = pool.plan_pool(
        worker_bytes=1,
        items=items,
        ceiling=workers,
        max_tasks_per_child=tasks,
        read_available=_roomy,
        read_pressure=_calm,
    )
    assert plan.workers == min(workers, items), plan
    return plan


def narrow(items: int) -> pool.PoolPlan:
    plan = pool.plan_pool(
        worker_bytes=GIB, items=items, read_available=_tight, read_pressure=_calm
    )
    assert plan.in_process, plan
    return plan


def _load(tag: str) -> None:
    _LOADED["tag"] = tag
    _LOADED["identity"] = f"{os.getpid()}:{time.monotonic_ns()}"


def _report(index: int) -> tuple[int, int, str, str]:
    return (
        index,
        os.getpid(),
        _LOADED.get("tag", "uninitialized"),
        _LOADED.get("identity", "uninitialized"),
    )


def _square(value: int) -> int:
    return value * value


def _raise_on_two(index: int) -> int:
    if index == 2:
        raise LookupError(f"item {index} is the one that fails")
    return index


def _die_on_one(index: int) -> int:
    if index == 1:
        os._exit(70)
    time.sleep(0.2)
    return index


def _interrupt_myself(index: int) -> tuple[int, int]:
    """Send this worker the terminal's interrupt, then answer, if it is still here."""
    os.kill(os.getpid(), signal.SIGINT)
    time.sleep(0.2)
    return index, os.getpid()


def _pid_then_sleep(index: int) -> int:
    Path(os.environ["CRATEKIT_STREAM_PIDS"]).joinpath(f"{os.getpid()}.pid").write_text(str(index))
    time.sleep(120)
    return index


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    try:
        # A child of this process that has exited and not been reaped still
        # answers a signal; its status line says what it really is.
        return " Z " not in Path(f"/proc/{pid}/stat").read_text()
    except OSError:
        return True


def _wait_until(test, seconds: float) -> bool:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if test():
            return True
        time.sleep(0.05)
    return test()


# ---------------------------------------------------------------------------
# A plan of one is the loop it replaced
# ---------------------------------------------------------------------------


def test_a_plan_of_one_runs_each_item_here_when_it_is_asked_for():
    _LOADED.clear()
    with pool.stream_workers(
        narrow(3), _report, range(3), initializer=_load, initargs=("here",)
    ) as stream:
        assert _LOADED == {}, "the initializer ran before any result was asked for"
        first = stream.result(0)
        assert first[1] == os.getpid() and first[2] == "here"
        identity = first[3]
        assert stream.result(2) == (2, os.getpid(), "here", identity), (
            "the initializer runs once here, as it does once per child"
        )
    assert multiprocessing.active_children() == []


def test_nothing_is_spawned_before_the_first_result_is_asked_for():
    stream = pool.stream_workers(wide(4), _square, range(4))
    try:
        assert multiprocessing.active_children() == []
    finally:
        stream.close()


# ---------------------------------------------------------------------------
# A wider plan gives what map_workers gives
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("order", [[0, 1, 2, 3, 4, 5], [5, 3, 1, 0, 2, 4]], ids=["in-order", "any-order"])
def test_a_pooled_stream_answers_what_map_workers_answers(order):
    items = [3, 1, 4, 1, 5, 9]
    expected = pool.map_workers(wide(len(items)), _square, items)
    assert expected == [9, 1, 16, 1, 25, 81]
    with pool.stream_workers(wide(len(items)), _square, items) as stream:
        assert len(stream) == len(items)
        answers = {position: stream.result(position) for position in order}
    assert [answers[position] for position in range(len(items))] == expected


def test_a_pooled_stream_runs_in_children_initialized_by_the_callers_initializer():
    with pool.stream_workers(
        wide(4), _report, range(4), initializer=_load, initargs=("there",)
    ) as stream:
        results = [stream.result(position) for position in range(4)]
    assert [index for index, _pid, _tag, _life in results] == [0, 1, 2, 3]
    assert os.getpid() not in {pid for _index, pid, _tag, _life in results}
    assert {tag for _index, _pid, tag, _life in results} == {"there"}


def test_a_stream_retires_its_children_at_the_generation_boundary():
    """The recycle ``map_workers`` performs, performed here at the same line."""
    plan = wide(4, tasks=1)
    assert plan.tasks_per_generation == 2 and plan.generations == 2
    with pool.stream_workers(
        plan, _report, range(4), initializer=_load, initargs=("reloaded",)
    ) as stream:
        results = [stream.result(position) for position in range(4)]
    assert [index for index, _pid, _tag, _life in results] == [0, 1, 2, 3]
    first = {life for index, _pid, _tag, life in results if index < 2}
    second = {life for index, _pid, _tag, life in results if index >= 2}
    assert first and second and not first & second, (
        "a worker served items on both sides of a generation boundary"
    )


@pytest.mark.parametrize("plan_for", [narrow, wide], ids=["in-process", "pooled"])
def test_each_position_is_read_once_on_both_paths(plan_for):
    with pool.stream_workers(plan_for(3), _square, range(3)) as stream:
        assert stream.result(1) == 1
        with pytest.raises(ValueError, match="already read"):
            stream.result(1)
        assert stream.result(2) == 4


@pytest.mark.parametrize("plan_for", [narrow, wide], ids=["in-process", "pooled"])
def test_a_position_outside_the_items_and_a_closed_stream_are_refused(plan_for):
    stream = pool.stream_workers(plan_for(2), _square, range(2))
    with pytest.raises(IndexError):
        stream.result(2)
    with pytest.raises(IndexError):
        stream.result(-1)
    with pytest.raises(TypeError):
        stream.result(True)
    stream.close()
    stream.close()
    assert stream.closed
    with pytest.raises(ValueError, match="closed"):
        stream.result(0)


@pytest.mark.parametrize("plan_for", [narrow, wide], ids=["in-process", "pooled"])
def test_what_the_work_raised_reaches_the_reader_of_that_position_only(plan_for):
    with pool.stream_workers(plan_for(4), _raise_on_two, range(4)) as stream:
        assert stream.result(0) == 0
        assert stream.result(1) == 1
        with pytest.raises(LookupError, match="item 2"):
            stream.result(2)
        assert stream.result(3) == 3, "one item's failure took a later item's result with it"


@pytest.mark.parametrize("plan_for", [narrow, wide], ids=["in-process", "pooled"])
def test_an_unsendable_function_is_refused_at_construction_on_both_paths(plan_for):
    with pytest.raises(ValueError, match="cannot be sent to a worker"):
        pool.stream_workers(plan_for(2), lambda value: value, range(2))
    with pytest.raises(ValueError, match="initializer argument 0"):
        pool.stream_workers(
            plan_for(2), _square, range(2), initializer=_load, initargs=(lambda: None,)
        )


# ---------------------------------------------------------------------------
# A pool that died, an interrupt, a close, and a parent that is gone
# ---------------------------------------------------------------------------


def test_a_worker_that_dies_is_a_broken_stream_and_not_an_item_failure():
    stream = pool.stream_workers(wide(4), _die_on_one, range(4))
    try:
        with pytest.raises(pool.StreamBroken):
            for position in range(4):
                stream.result(position)
        assert stream.closed, "a broken stream stays open for reads it cannot answer"
    finally:
        stream.close()
    assert _wait_until(lambda: multiprocessing.active_children() == [], 20)


def _dies_starting(tag: str) -> None:
    """An initializer that takes its worker down before it serves anything."""
    os._exit(71)


def test_workers_that_die_starting_are_one_broken_stream_and_not_a_pool_per_item():
    """The break is seen while the work is handed out, and it closes the stream once."""
    stream = pool.stream_workers(
        wide(6), _square, range(6), initializer=_dies_starting, initargs=("x",)
    )
    try:
        with pytest.raises(pool.StreamBroken):
            for position in range(6):
                stream.result(position)
        assert stream.closed
        with pytest.raises(ValueError, match="closed"):
            stream.result(5)
    finally:
        stream.close()
    assert _wait_until(lambda: multiprocessing.active_children() == [], 20)


def test_the_terminals_interrupt_does_not_kill_a_stream_worker():
    """Ctrl-C reaches every process in the group; the caller owns the stop."""
    with pool.stream_workers(wide(2), _interrupt_myself, range(2)) as stream:
        results = [stream.result(position) for position in range(2)]
    assert [index for index, _pid in results] == [0, 1]
    assert os.getpid() not in {pid for _index, pid in results}


def test_a_close_ends_the_workers_without_waiting_for_work_nobody_will_read(tmp_path, monkeypatch):
    monkeypatch.setenv("CRATEKIT_STREAM_PIDS", str(tmp_path))
    stream = pool.stream_workers(wide(4), _pid_then_sleep, range(4))
    try:
        # Start the generation without waiting on a result: the children sleep
        # for two minutes, which is the work nobody will read.
        stream._start(0, 4)
        assert _wait_until(lambda: len(list(tmp_path.glob("*.pid"))) == 2, 60), (
            "the two workers never started their items"
        )
        pids = [int(path.stem) for path in tmp_path.glob("*.pid")]
        started = time.monotonic()
        stream.close()
        took = time.monotonic() - started
    finally:
        stream.close()
    assert took < 30, f"the close waited {took:.0f} seconds on sleeping workers"
    assert _wait_until(lambda: not any(_alive(pid) for pid in pids), 20), (
        "a worker outlived the close"
    )


_ORPHAN = '''\
"""A parent that starts a pooled stream over sleeping items and then waits to be killed."""

import os
import sys
import time

from cratekit.core import pool
from tests.test_pool_stream import _pid_then_sleep, wide


def main():
    stream = pool.stream_workers(wide(2), _pid_then_sleep, range(2))
    stream._start(0, 2)
    print(os.getpid(), flush=True)
    time.sleep(300)


if __name__ == "__main__":
    main()
'''


def test_workers_leave_when_their_parent_is_killed_outright(tmp_path):
    """A killed driver must not leave children holding their memory for ever."""
    pids = tmp_path / "pids"
    pids.mkdir()
    script = tmp_path / "orphan.py"
    script.write_text(_ORPHAN)
    environment = dict(os.environ)
    environment["CRATEKIT_STREAM_PIDS"] = str(pids)
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(SRC_ROOT), str(SRC_ROOT.parent), environment.get("PYTHONPATH", "")]
    )
    parent = subprocess.Popen(
        [sys.executable, str(script)],
        stdout=subprocess.PIPE,
        text=True,
        env=environment,
        cwd=str(SRC_ROOT.parent),
    )
    try:
        assert parent.stdout is not None
        assert parent.stdout.readline().strip() == str(parent.pid)
        assert _wait_until(lambda: len(list(pids.glob("*.pid"))) == 2, 60), (
            "the two workers never started their items"
        )
        workers = [int(path.stem) for path in pids.glob("*.pid")]
        assert all(_alive(pid) for pid in workers)
        parent.kill()
        parent.wait(30)
        assert _wait_until(lambda: not any(_alive(pid) for pid in workers), 30), (
            "a worker outlived a parent that was killed, and would hold its memory for ever"
        )
    finally:
        if parent.poll() is None:
            parent.kill()
            parent.wait(30)
        for path in pids.glob("*.pid"):
            try:
                os.kill(int(path.stem), signal.SIGKILL)
            except ProcessLookupError:
                pass


# ---------------------------------------------------------------------------
# The plan says which gate refused it, and under what ceiling
# ---------------------------------------------------------------------------


def test_a_plan_refused_by_swap_names_the_gate_the_reading_and_the_limit():
    plan = pool.plan_pool(
        worker_bytes=GIB,
        items=8,
        ceiling=6,
        read_available=_roomy,
        read_pressure=lambda: pool.Pressure(swap_used_bytes=12 * GIB, used_percent=40.0),
    )
    assert plan.in_process and plan.bound is pool.Bound.MEMORY_PRESSURE
    assert plan.ceiling == 6
    assert [reading.gate for reading in plan.refused_by] == [pool.PressureGate.SWAP]
    assert plan.refused_by[0].reading == 12 * GIB
    assert plan.refused_by[0].limit == pool.DEFAULT_SWAP_PRESSURE_BYTES
    assert plan.account() == (
        "12.0 GB of swap is in use, at or over the 1.0 GB gate, so no pool was "
        "planned, under a ceiling of 6"
    )


def test_a_plan_refused_by_the_used_percent_names_that_gate():
    plan = pool.plan_pool(
        worker_bytes=GIB,
        items=8,
        ceiling=6,
        read_available=_roomy,
        read_pressure=lambda: pool.Pressure(swap_used_bytes=0, used_percent=91.4),
    )
    assert [reading.gate for reading in plan.refused_by] == [pool.PressureGate.USED_PERCENT]
    assert plan.account() == (
        "memory is 91 percent in use, at or over the 85 percent gate, so no pool "
        "was planned, under a ceiling of 6"
    )


def test_a_plan_refused_by_both_gates_names_both_swap_first():
    plan = pool.plan_pool(
        worker_bytes=GIB,
        items=8,
        read_available=_roomy,
        read_pressure=lambda: pool.Pressure(swap_used_bytes=2 * GIB, used_percent=85.0),
    )
    assert [reading.gate for reading in plan.refused_by] == [
        pool.PressureGate.SWAP,
        pool.PressureGate.USED_PERCENT,
    ]
    assert "2.0 GB of swap is in use" in plan.account()
    assert "memory is 85 percent in use" in plan.account()


def test_a_reading_just_under_both_gates_refuses_nothing():
    plan = pool.plan_pool(
        worker_bytes=GIB,
        items=8,
        ceiling=3,
        read_available=_roomy,
        read_pressure=lambda: pool.Pressure(swap_used_bytes=GIB - 1, used_percent=84.9),
    )
    assert plan.refused_by == ()
    assert plan.workers == 3 and plan.bound is pool.Bound.CEILING
    assert plan.account() == "the ceiling of 3 is what held it, at 1.0 GB a worker"


def test_a_plan_bound_by_memory_says_what_the_reading_afforded():
    plan = pool.plan_pool(
        worker_bytes=600 * 1024**2,
        items=40,
        ceiling=9,
        headroom_percent=50,
        read_available=lambda: 6 * GIB,
        read_pressure=_calm,
    )
    # (6 GiB less the 2 GiB reserve) at 50 percent is 2 GiB, three workers of 600 MiB.
    assert plan.workers == 3 and plan.bound is pool.Bound.AVAILABLE_MEMORY
    assert plan.account() == (
        "6.0 GB available affords 3 at 600 MB a worker after the reserve and the "
        "headroom, under a ceiling of 9"
    )


def test_a_plan_memory_cannot_afford_says_so_and_a_plan_by_items_says_that():
    none = pool.plan_pool(
        worker_bytes=GIB, items=4, ceiling=4, read_available=_tight, read_pressure=_calm
    )
    assert none.bound is pool.Bound.INSUFFICIENT_MEMORY
    assert none.account().startswith("2.0 GB available does not afford one worker at 1.0 GB")
    few = pool.plan_pool(
        worker_bytes=1, items=2, ceiling=8, read_available=_roomy, read_pressure=_calm
    )
    assert few.bound is pool.Bound.WORK_ITEMS
    assert few.account() == "2 item(s) to run, under a ceiling of 8"


def test_a_plan_whose_memory_could_not_be_read_invents_no_number():
    def refuses() -> int:
        raise OSError("no reading on this platform")

    plan = pool.plan_pool(worker_bytes=GIB, items=4, ceiling=4, read_available=refuses)
    assert plan.bound is pool.Bound.MEMORY_UNREADABLE and plan.ceiling == 4
    assert plan.account() == pool.BOUND_PHRASES[pool.Bound.MEMORY_UNREADABLE]
