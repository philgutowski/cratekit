"""U241: librosa's kernels are compiled by one process at a time.

The review of U241 drove a fresh numba cache with two light workers starting
together: five runs in seven ended in a segmentation fault, and the cache was
left damaged for every later analysis. ``cratekit.analysis.warm`` makes every
process run one head of its own, alone under a lock, before its first real
one. What is held here:

1. the lock holds two processes apart, and a lock that cannot be taken never
   stops a worker from starting;
2. a process warms once, before its first decode, and never where the
   analysis extra is absent;
3. with the real stack: the warm up reaches every kernel real heads reach, so
   nothing is left to be compiled by two workers later, and two workers
   starting together on an empty cache finish.

The last two need the analysis extra and are skipped without it.
"""

from __future__ import annotations

import os
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest

from cratekit.analysis import detect, warm

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"


@pytest.fixture(autouse=True)
def cold_process(monkeypatch):
    """Each test starts as a process that has not warmed."""
    monkeypatch.setattr(warm, "_WARMED", False)
    monkeypatch.setattr(warm, "_WARMING", False)


def _environment(**extra: str) -> dict[str, str]:
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(SRC_ROOT), str(REPO_ROOT), environment.get("PYTHONPATH", "")]
    )
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment.update(extra)
    return environment


# ---------------------------------------------------------------------------
# The lock
# ---------------------------------------------------------------------------

_HOLDER = """
import sys, time
from pathlib import Path
from cratekit.analysis import warm
lock, log, name = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
with warm.exclusive(lock):
    with log.open("a") as out:
        out.write(f"{name} in {time.monotonic_ns()}\\n")
    time.sleep(0.6)
    with log.open("a") as out:
        out.write(f"{name} out {time.monotonic_ns()}\\n")
"""


def test_two_processes_are_never_inside_the_lock_together(tmp_path):
    lock, log = tmp_path / "warm.lock", tmp_path / "log.txt"
    holders = [
        subprocess.Popen(
            [sys.executable, "-c", _HOLDER, str(lock), str(log), name], env=_environment()
        )
        for name in ("first", "second", "third")
    ]
    for holder in holders:
        assert holder.wait(60) == 0
    events = [line.split() for line in log.read_text().splitlines()]
    assert len(events) == 6
    inside: set[str] = set()
    for name, what, _when in sorted(events, key=lambda event: int(event[2])):
        if what == "in":
            assert not inside, f"{name} entered while {inside} was inside"
            inside.add(name)
        else:
            inside.discard(name)


def test_a_lock_that_cannot_be_opened_never_stops_the_block_from_running(tmp_path):
    ran = []
    with warm.exclusive(tmp_path / "no such folder" / "warm.lock"):
        ran.append(True)
    assert ran == [True]


def test_the_lock_is_named_for_the_user_and_sits_in_the_temporary_directory(monkeypatch, tmp_path):
    monkeypatch.setattr("tempfile.tempdir", str(tmp_path))
    path = warm.lock_path()
    assert path.parent == tmp_path
    assert path.name == f"cratekit-analysis-warm-{os.getuid()}.lock"


def test_a_holder_that_died_does_not_hold_the_lock(tmp_path):
    lock = tmp_path / "warm.lock"
    died = subprocess.run(
        [
            sys.executable,
            "-c",
            "import os, sys\nfrom pathlib import Path\nfrom cratekit.analysis import warm\n"
            "held = warm.exclusive(Path(sys.argv[1]))\nheld.__enter__()\nos._exit(9)\n",
            str(lock),
        ],
        env=_environment(),
        check=False,
    )
    assert died.returncode == 9 and lock.exists()
    started = time.monotonic()
    with warm.exclusive(lock):
        pass
    assert time.monotonic() - started < 5


# ---------------------------------------------------------------------------
# Once, alone, and only with the extra
# ---------------------------------------------------------------------------


def test_a_process_warms_once(monkeypatch):
    heads: list[int] = []
    monkeypatch.setattr(detect, "heavy_available", lambda: True)
    monkeypatch.setattr(warm, "_measure_one_head", lambda: heads.append(1))
    assert warm.kernels() is True
    assert warm.kernels() is False
    assert heads == [1]


def test_the_warm_up_runs_inside_the_lock(monkeypatch):
    order: list[str] = []

    class _Held:
        def __enter__(self):
            order.append("locked")

        def __exit__(self, *exc):
            order.append("released")

    monkeypatch.setattr(detect, "heavy_available", lambda: True)
    monkeypatch.setattr(warm, "exclusive", lambda: _Held())
    monkeypatch.setattr(warm, "_measure_one_head", lambda: order.append("measured"))
    warm.kernels()
    assert order == ["locked", "measured", "released"]


def test_the_warm_ups_own_head_does_not_wait_on_the_lock_it_holds(monkeypatch):
    """The warm up measures through the detector, which asks to be warmed like any caller.

    The lock here is one that refuses a second entry out loud. The real one
    would wait on itself for ever, so a regression would hang the suite and
    name no test (the review of U241 measured exactly that).
    """
    inner: list[bool] = []
    held: list[bool] = []

    class _OnceOnly:
        def __enter__(self):
            assert not held, "the warm up asked for the lock it was already holding"
            held.append(True)

        def __exit__(self, *exc):
            held.clear()

    monkeypatch.setattr(detect, "heavy_available", lambda: True)
    monkeypatch.setattr(warm, "exclusive", lambda: _OnceOnly())
    monkeypatch.setattr(warm, "_measure_one_head", lambda: inner.append(warm.kernels()))
    assert warm.kernels() is True
    assert inner == [False]


def test_a_warm_up_that_raises_is_not_a_reason_to_refuse_the_process(monkeypatch):
    def raises():
        raise RuntimeError("the decoder is not here")

    monkeypatch.setattr(detect, "heavy_available", lambda: True)
    monkeypatch.setattr(warm, "_measure_one_head", raises)
    assert warm.kernels() is True
    assert warm._WARMING is False
    assert warm.kernels() is False


def test_nothing_is_warmed_and_no_lock_is_taken_without_the_extra(monkeypatch):
    def never():
        raise AssertionError("a process without the extra reached the lock or the head")

    monkeypatch.setattr(detect, "heavy_available", lambda: False)
    monkeypatch.setattr(warm, "exclusive", never)
    monkeypatch.setattr(warm, "_measure_one_head", never)
    assert warm.kernels() is False
    assert warm._WARMED is False, "a process that could not warm is not marked warmed"


def test_the_detector_asks_for_the_warm_up_before_it_decodes(tmp_path, monkeypatch):
    """The one call that keeps two processes out of the kernel cache together.

    Against a stand in for librosa, so it runs where the analysis extra is
    not installed, which is where the merge gate runs: the review of U241
    removed the call and nothing failed without the extra.
    """
    import types

    order: list[str] = []
    stand_in = types.ModuleType("librosa")

    def load(*args, **kwargs):
        order.append("decoded")
        raise RuntimeError("no such file")

    stand_in.load = load
    monkeypatch.setitem(sys.modules, "librosa", stand_in)
    monkeypatch.setattr(warm, "kernels", lambda: order.append("warmed"))
    found = detect.analyse_file(tmp_path / "missing.flac")
    assert found == {"path": tmp_path / "missing.flac", "terminal": detect.TERMINAL_UNDECODABLE}
    assert order == ["warmed", "decoded"]


# ---------------------------------------------------------------------------
# With the real stack: every kernel is reached, and a cold pool finishes
# ---------------------------------------------------------------------------


def _audio(folder: Path) -> list[Path]:
    """A stinger, a drum track, a pad with no pulse, and one long enough for windows."""
    np = pytest.importorskip("numpy")
    soundfile = pytest.importorskip("soundfile")
    rate = 44100
    rng = np.random.default_rng(4)

    def drums(seconds: float) -> "np.ndarray":
        out = np.zeros(int(seconds * rate), dtype=np.float32)
        burst = np.hanning(400).astype(np.float32)
        for beat in range(int(seconds * 2)):
            at = int(beat * 0.5 * rate)
            if at + burst.size < out.size:
                out[at : at + burst.size] += burst
        t = np.arange(out.size) / rate
        out += (0.1 * np.sin(2 * np.pi * 220 * t)).astype(np.float32)
        return out + 0.01 * rng.standard_normal(out.size).astype(np.float32)

    def pad(seconds: float) -> "np.ndarray":
        t = np.arange(int(seconds * rate)) / rate
        return (0.1 * (np.sin(2 * np.pi * 110 * t) + np.sin(2 * np.pi * 165 * t))).astype(
            np.float32
        )

    made = []
    for name, samples in (
        ("stinger.flac", drums(2.0)),
        ("drums.flac", drums(25.0)),
        ("pad.flac", pad(35.0)),
        ("long.flac", drums(190.0)),
    ):
        path = folder / name
        soundfile.write(str(path), np.stack([samples, samples], axis=1), rate, subtype="PCM_16")
        made.append(path)
    return made


def _cache_listing(cache: Path) -> dict[str, int]:
    return {
        str(path.relative_to(cache)): path.stat().st_size
        for path in sorted(cache.rglob("*"))
        if path.is_file()
    }


_REAL_HEADS = """
import sys, warnings
warnings.simplefilter("ignore")
from pathlib import Path
from cratekit.analysis import detect, energy, vocal
calibration = energy.calibrate(
    [{name: float(seed) for name in energy.FEATURE_ORDER} for seed in range(12)]
)
for path in sys.argv[1:]:
    for key in detect.KEY_METHODS:
        detect.analyse_file(Path(path), calibration=calibration, key=key)
    vocal.decode(path)
"""


def test_the_warm_up_reaches_every_kernel_a_real_head_reaches(tmp_path):
    """Warm an empty cache, measure real files against it, and the cache must not move.

    A kernel the warm up missed would be compiled by the first real head, and
    with two workers that is two processes filling the cache together again.
    Every key method, a calibrated energy and the vocal pass's decode are
    measured, over a stinger, a drum track, a pad and a track long enough for
    the windowed key.
    """
    pytest.importorskip("librosa")
    files = _audio(tmp_path)
    cache = tmp_path / "numba"
    cache.mkdir()
    environment = _environment(NUMBA_CACHE_DIR=str(cache))
    warmed = subprocess.run(
        [sys.executable, "-c", "from cratekit.analysis import warm; print(warm.kernels())"],
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert warmed.returncode == 0 and warmed.stdout.strip() == "True", warmed.stderr[-2000:]
    after_the_warm_up = _cache_listing(cache)
    assert after_the_warm_up, "the warm up compiled nothing, so this test proves nothing"

    done = subprocess.run(
        [sys.executable, "-c", _REAL_HEADS, *map(str, files)],
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert done.returncode == 0, done.stderr[-2000:]
    assert _cache_listing(cache) == after_the_warm_up, (
        "a real head compiled a kernel the warm up did not reach"
    )


_COLD_POOL = textwrap.dedent(
    """
    import sys
    from cratekit.analysis import ahead
    from cratekit.core import cores, pool

    GIB = 1024 ** 3
    cores.usable_cores = lambda: 4
    pool.available_bytes = lambda: 64 * GIB
    pool.memory_pressure = lambda: pool.Pressure(swap_used_bytes=0, used_percent=10.0)

    def main():
        paths = sys.argv[1:]
        settings = ahead.Settings(calibration=None, tempo_window=(80, 160), drift_cut=1.0)
        session = ahead.open_session("cold", paths, settings)
        assert session.plan.workers == 2, session.plan
        try:
            heads = [ahead.head("cold", path, settings) for path in paths]
        finally:
            ahead.close_session("cold")
        assert session.stopped is None, session.stopped
        assert (session.ahead, session.here) == (len(paths), 0), (session.ahead, session.here)
        print(" ".join(str(head.get("camelot")) for head in heads))

    if __name__ == "__main__":
        main()
    """
)


@pytest.mark.parametrize("attempt", [1, 2, 3])
def test_two_workers_starting_together_on_an_empty_cache_finish(tmp_path, attempt):
    """The review's crash, as a test. THREE ATTEMPTS, BECAUSE THE DEFECT IS A RACE.

    Without the warm up this run ended in a segmentation fault on 5 of the
    review's 7 cold runs and on 2 of the author's 4, so one clean pass proves
    little; with it, 12 of 12 were clean through the real verb. Each attempt
    has an empty cache of its own.
    """
    pytest.importorskip("librosa")
    files = _audio(tmp_path)[:3]
    cache = tmp_path / "numba"
    cache.mkdir()
    script = tmp_path / "cold_pool.py"
    script.write_text(_COLD_POOL)
    done = subprocess.run(
        [sys.executable, str(script), *map(str, files)],
        env=_environment(NUMBA_CACHE_DIR=str(cache)),
        capture_output=True,
        text=True,
        check=False,
        timeout=600,
    )
    assert done.returncode == 0, (
        f"attempt {attempt}: exit {done.returncode}\\n{done.stderr[-3000:]}"
    )
    assert len(done.stdout.split()) == 3
