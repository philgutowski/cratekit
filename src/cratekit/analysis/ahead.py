"""A job's heads, measured ahead of the driver in the pool the machine affords (U241).

``analyze run`` is a job, and a job settles one item at a time: the worker
measures a file, the engine makes its report durable, the row flips to done,
and only then is the next item claimed. That order is what makes a kill
resumable and it does not change. What changes is WHERE THE MEASURING
HAPPENS. A head, the key, tempo, drift and energy of one file, is a pure read
of that file, so while the driver is scoring one track's vocals and writing
its tags, workers are already measuring the tracks behind it, and the driver
reads each head when it reaches that item.

EVERY WRITE STAYS IN THE DRIVER. A worker here opens a file for reading,
returns a mapping and writes nothing: no tag, no rename, no report, no row.
The tag write, the rename and its recorded intent, the staged report and the
item's state are the driver's, in item order, under the driver lock, exactly
as before. Nothing in this module writes a beat grid or anything else.

A HEAD MEASURED AHEAD IS USED ONLY IF IT IS THE HEAD THE DRIVER WOULD MEASURE
NOW, and three things can make it not so, each checked when the head is read:

* the FILE changed after it was measured. The worker returns the file's
  identity as it stood just before the read, its device, inode, size and
  modification time, and the driver compares it with the file in front of it.
  A file replaced under the same name while it waited is measured again.
* the SETTINGS changed. The calibration, the tempo window and the drift cut
  the workers were started with are compared with the ones this item binds.
  The serial run reads the calibration per item, so a calibration written
  mid run reaches the next item, and it does here too: the pool is stopped
  and the rest is measured in this process.
* the POOL failed. A worker that died, or anything raised on the way to its
  result, says nothing about the item, so the item is measured here, and
  whatever the file itself raises is raised here as it always was.

In every one of those the fallback is the one line the worker ran before
this module existed, in this process. So the worst this module can do to a
run is make it as slow as it was.

WHAT THE FALLBACK COSTS IN MEMORY, SAID OUT LOUD. A head measured here while
the workers are still running, a changed file or a file a worker raised on,
holds one more light worker's memory than the plan counted, in the driver,
for the length of that one track. The plan's headroom is what carries it. A
pool that broke or was stopped has no workers left, so the rest of the run is
the serial run's memory exactly.

WHEN NO POOL RUNS AT ALL. A plan of one worker, which is what a machine under
memory pressure and a machine that affords only one are both given; a
detector bound by a test, a closure no child could receive; an analysis
extra that is not installed; a job nobody opened a session for. Each is the
serial path, and :func:`report` says which it was.

Layer: modules. The heavy stack is imported in the workers and never here.
"""

from __future__ import annotations

import functools
import os
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Sequence

from cratekit.analysis import energy, light
from cratekit.core import pool

#: Why a run measured every head in this process, for a run nobody planned a
#: pool for. A planned run says its own reason through the plan.
WHY_NOT_OPENED = "no pool was planned for this run"
WHY_NOTHING_WAITING = "no file was waiting to be measured"
WHY_TEST_DETECTOR = "the bound detector cannot be sent to a worker"
WHY_NO_EXTRA = "the analysis extra is not installed in this process"

#: Why a pool that started was stopped before the job finished.
STOPPED_SETTINGS = (
    "the calibration, the tempo window or the drift cut changed during the run"
)


@dataclass(frozen=True)
class Settings:
    """What a head is measured under. Equal settings, interchangeable heads.

    The calibration travels as the mapping its state file holds rather than as
    the object, so two readings of one file compare equal and a worker rebuilds
    exactly the calibration the driver read.
    """

    calibration: Mapping[str, Any] | None
    tempo_window: tuple[int, int]
    drift_cut: float

    @classmethod
    def of(cls, calibration: energy.Calibration | None, cfg: Any) -> Settings:
        return cls(
            calibration=None if calibration is None else calibration.to_json(),
            tempo_window=(int(cfg.analysis.tempo_floor), int(cfg.analysis.tempo_ceiling)),
            drift_cut=float(cfg.analysis.drift_cut),
        )


#: What binds the detector in a worker: an importable function and its
#: arguments. None is the shipped binding, built from the run's settings. A
#: test that drives the pool binds an importable fake here, beside the one it
#: binds in its own process, because the fake the suite usually binds is a
#: closure and a closure cannot reach a spawned child.
_WORKER_BINDING: tuple[Callable[..., None], tuple[Any, ...]] | None = None


def bind_worker(binding: tuple[Callable[..., None], tuple[Any, ...]] | None) -> None:
    global _WORKER_BINDING
    _WORKER_BINDING = binding


def worker_bound() -> bool:
    """Whether a worker binding other than the shipped one is in place."""
    return _WORKER_BINDING is not None


def bind_shipped(
    calibration: Mapping[str, Any] | None, tempo_window: tuple[int, int], drift_cut: float
) -> None:
    """A worker's initializer: bind the shipped detector under the run's settings."""
    from cratekit.analysis import detect

    light.bind_detect(
        functools.partial(
            detect.analyse_file,
            calibration=None if calibration is None else energy.Calibration.from_json(calibration),
            tempo_window=(int(tempo_window[0]), int(tempo_window[1])),
            drift_cut=float(drift_cut),
        )
    )


def identity_of(path: str) -> tuple[int, int, int, int] | None:
    """Which file sits at ``path`` right now, or None when none can be read.

    Device and inode say which file, size and modification time say whether it
    was written since. One field alone is not an identity: a rewrite in place
    keeps the inode, and a replacement of the same length keeps the size.
    """
    try:
        found = os.stat(path)
    except OSError:
        return None
    return (found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns)


def measure(path: str) -> tuple[tuple[int, int, int, int] | None, dict[str, Any]]:
    """What a worker runs: the file's identity BEFORE the read, then the head.

    Before, so a file replaced while it was being read does not carry the
    replacement's identity beside the original's head.
    """
    found = identity_of(path)
    return found, light.analyse(path)


@dataclass
class Session:
    """One job's run ahead: the plan, the stream when there is one, and the count."""

    job_id: str
    settings: Settings | None
    plan: pool.PoolPlan | None
    items: int
    stream: pool.WorkStream[str, Any] | None = None
    positions: dict[str, int] = field(default_factory=dict)
    why: str | None = None
    #: Heads the workers measured and the driver used.
    ahead: int = 0
    #: Heads measured in this process, whatever the reason.
    here: int = 0
    #: Heads the workers measured that the driver would not use, by reason.
    remeasured: dict[str, int] = field(default_factory=dict)
    stopped: str | None = None

    def stop(self, reason: str | None = None) -> None:
        """End the workers. With a reason, the pool was stopped before the job was done."""
        stream, self.stream = self.stream, None
        if stream is not None:
            if reason is not None and self.stopped is None:
                self.stopped = reason
            stream.close()

    def _again(self, reason: str) -> None:
        self.remeasured[reason] = self.remeasured.get(reason, 0) + 1


_SESSIONS: dict[str, Session] = {}


def open_session(
    job_id: str,
    paths: Sequence[str],
    settings: Settings,
    *,
    reserve_bytes: int = pool.DEFAULT_MEMORY_RESERVE_BYTES,
    reserved_cores: int = light.LIGHT_RESERVED_CORES,
) -> Session:
    """Plan the light pool over ``paths`` and stand ready to measure them ahead.

    Nothing is spawned here: the stream starts its workers when the first head
    is asked for. ``reserve_bytes`` is what the planner keeps back, raised by a
    caller that will hold a vocal model in this process, and
    ``reserved_cores`` the cores kept from the pool, the shipped figure unless
    a measurement asks otherwise. A session already open for the job is closed
    first.
    """
    close_session(job_id)
    ordered = [str(path) for path in paths]
    if not ordered:
        session = Session(job_id, settings, None, 0, why=WHY_NOTHING_WAITING)
        _SESSIONS[job_id] = session
        return session
    plan = light.plan(ordered, reserve_bytes=reserve_bytes, reserved_cores=reserved_cores)
    session = Session(job_id, settings, plan, len(ordered))
    if not plan.in_process:
        initializer, initargs = _WORKER_BINDING or (
            bind_shipped,
            (settings.calibration, settings.tempo_window, settings.drift_cut),
        )
        session.stream = pool.stream_workers(
            plan, measure, ordered, initializer=initializer, initargs=initargs
        )
        session.positions = {path: position for position, path in enumerate(ordered)}
    _SESSIONS[job_id] = session
    return session


def note_unopened(job_id: str, why: str) -> Session:
    """Record that this job's run measures everything here, and why."""
    close_session(job_id)
    session = Session(job_id, None, None, 0, why=why)
    _SESSIONS[job_id] = session
    return session


def close_session(job_id: str) -> Session | None:
    """End the job's workers and forget the session. Safe when there is none."""
    session = _SESSIONS.pop(job_id, None)
    if session is not None:
        session.stop()
    return session


def head(job_id: str, path: str, settings: Settings | None = None) -> dict[str, Any]:
    """The head of ``path``: the one measured ahead when it still stands, else measured here.

    ``settings`` is what this item binds now. The head a worker measured is
    used only under equal settings and over the same file; see the module
    docstring for each way out and why every one of them ends in the serial
    line.
    """
    session = _SESSIONS.get(job_id)
    if session is None:
        return light.analyse(path)
    found = _from_the_pool(session, path, settings)
    if found is None:
        session.here += 1
        return light.analyse(path)
    session.ahead += 1
    return found


def _from_the_pool(
    session: Session, path: str, settings: Settings | None
) -> dict[str, Any] | None:
    """The worker's head for ``path`` if there is one this item may use, else None."""
    stream = session.stream
    if stream is None:
        return None
    position = session.positions.pop(path, None)
    if position is None:
        return None
    if settings != session.settings:
        session.stop(STOPPED_SETTINGS)
        return None
    try:
        measured_identity, found = stream.result(position)
    except pool.StreamBroken as broken:
        session.stop(str(broken))
        return None
    except Exception:  # noqa: BLE001 - the serial line decides what this file raises
        session._again("raised-in-a-worker")
        return None
    if measured_identity is None or measured_identity != identity_of(path):
        session._again("file-changed")
        return None
    return found


def report(session: Session | None) -> dict[str, Any]:
    """What the run's pool was, as plain data the job records beside its reports.

    ``workers`` is how many processes measured heads at once. ``detail`` is the
    sentence a person reads: the count, and what held it there.
    """
    if session is None:
        return {"workers": 1, "planned": False, "status": "info", "detail": _alone(WHY_NOT_OPENED)}
    plan = session.plan
    if plan is None:
        return {
            "workers": 1,
            "planned": False,
            "status": "info",
            "detail": _alone(session.why or WHY_NOT_OPENED),
        }
    record: dict[str, Any] = {
        "workers": plan.workers,
        "planned": True,
        "bound": str(plan.bound),
        "ceiling": plan.ceiling,
        "worker_bytes": plan.worker_bytes,
        "available_bytes": plan.available_bytes,
        "refused_by": [
            {"gate": str(reading.gate), "reading": reading.reading, "limit": reading.limit}
            for reading in plan.refused_by
        ],
        "waiting": session.items,
        "measured_ahead": session.ahead,
        "measured_here": session.here,
        "remeasured": dict(session.remeasured),
        "stopped": session.stopped,
    }
    if plan.in_process:
        record["status"] = "info"
        record["detail"] = _alone(plan.account())
        return record
    detail = (
        f"{plan.workers} workers measured key, tempo and energy ahead of this "
        f"process: {plan.account()}; {session.ahead} of {session.items} waiting "
        f"file(s) were read from them"
    )
    if session.here:
        detail += f" and {session.here} measured here"
    if session.stopped is not None:
        detail += f"; the pool was stopped early: {session.stopped}"
    full = plan.bound in (pool.Bound.CEILING, pool.Bound.WORK_ITEMS)
    record["status"] = "ok" if full and session.stopped is None else "info"
    record["detail"] = detail
    return record


def _alone(why: str) -> str:
    return f"one worker, this process: {why}"


__all__ = [
    "STOPPED_SETTINGS",
    "Session",
    "Settings",
    "WHY_NOTHING_WAITING",
    "WHY_NOT_OPENED",
    "WHY_NO_EXTRA",
    "WHY_TEST_DETECTOR",
    "bind_shipped",
    "bind_worker",
    "close_session",
    "head",
    "identity_of",
    "measure",
    "note_unopened",
    "open_session",
    "report",
    "worker_bound",
]
