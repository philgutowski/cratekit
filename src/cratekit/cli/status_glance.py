"""``crate status``'s glance (U960): one machine readable object an app shows.

Everything a menu bar shows, in ``data.summary.glance``: both backup ages,
whether rekordbox is closed, the jobs running, every run waiting at a gate, how
the last night pass ended, and one ``attention`` word an icon can show. It is a
projection of facts other verbs already compute, never a probe of its own:

* ``backup`` is :func:`backup_facts.ages`, the call behind doctor's
  ``backup.age.files`` and ``backup.age.database`` checks;
* ``rekordbox`` is :func:`processes.rekordbox_processes_running`, doctor's
  ``rekordbox.closed`` probe, where a scan that could not confirm absence is
  ``unknown``, never ``closed``;
* ``gates`` reads the run records ``crate run show`` reads, with ``old`` from
  :func:`gates.old_gate`, the predicate ``crate run retire`` acts on;
* ``night`` is :func:`sync_night.settle` over :func:`sync_night.read_status`,
  exactly as ``crate sync night --last`` reads it.

A source that cannot be read is ``{"unreadable": "<message>"}`` in its own key
and makes ``attention`` read ``fail``; it is never shown as empty, none or
closed (METHOD's first defect pattern). The glance reads only: it opens the job
queue through a connection that cannot write, creates no directory, starts no
job, calls no network service and never launches rekordbox.

``tests/schemas/status_glance.v1.json`` pins the shape; :data:`VERSION` moves
when it changes incompatibly.

Layer note: CLI. It imports the gate records it reads, and downward.
"""

from __future__ import annotations

import os
from collections.abc import Mapping, Sequence
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from cratekit.cli import gates, registry
from cratekit.core import backup_facts, config, jobs, processes, session_ack

#: The glance's shape version, bumped only when a key changes meaning or goes.
VERSION = 1

#: The key a source that could not be read carries instead of its answer.
UNREADABLE = "unreadable"

#: ``attention``'s words, most urgent first; the first that holds is the answer.
FAIL, GATE, RUNNING, BACKUP_DUE, OK = "fail", "gate", "running", "backup-due", "ok"
ATTENTION: tuple[str, ...] = (FAIL, GATE, RUNNING, BACKUP_DUE, OK)

#: How ``rekordbox`` reads when the process scan answered.
CLOSED, OPEN, UNKNOWN = "closed", "open", "unknown"

#: The age at which a backup portion is due, CLAUDE.md's five days, the same
#: limit a session mints the acknowledgment under.
BACKUP_DUE_AGE: timedelta = session_ack.SESSION_MAX_BACKUP_AGE

#: The fields of the night record the glance carries, in ``--last``'s names.
NIGHT_FIELDS: tuple[str, ...] = ("outcome", "line", "gate_run", "pass_run", "staging")

#: The keys every glance carries; ``attention`` is derived from the rest.
KEYS: tuple[str, ...] = (
    "version", "attention", "backup", "rekordbox", "jobs_running", "gates", "night",
)


def _unreadable(exc: BaseException) -> dict[str, str]:
    return {UNREADABLE: f"{type(exc).__name__}: {exc}"}


def is_unreadable(value: Any) -> bool:
    """Whether ``value`` is a source, or one of its items, that could not be read."""
    return isinstance(value, Mapping) and UNREADABLE in value


def _iso(moment: datetime | None) -> str | None:
    if moment is None:
        return None
    return moment.astimezone(timezone.utc).replace(microsecond=0).isoformat()


# ---------------------------------------------------------------------------
# The sources
# ---------------------------------------------------------------------------


def backup(cfg: config.Config, now: datetime) -> dict[str, Any]:
    """Each portion's ``{state, age_seconds, completed_at}``, off doctor's own reader."""
    try:
        ages = backup_facts.ages(cfg, now=now)
    except Exception as exc:  # noqa: BLE001 - every failure to read is said, never folded
        return _unreadable(exc)
    return {
        str(answer.portion): {
            "state": str(answer.state),
            "age_seconds": (
                int(answer.age.total_seconds()) if answer.age is not None else None
            ),
            "completed_at": _iso(answer.completed_at),
        }
        for answer in ages
    }


def rekordbox(lister: processes.ProcessLister | None = None) -> str | dict[str, str]:
    """``closed``, ``open`` or ``unknown``, off doctor's ``rekordbox.closed`` probe.

    A scan that met a process it could not read is ``unknown``, as doctor says
    it as a note; a scan that broke is unreadable. Neither is ever ``closed``.
    """
    try:
        running = processes.rekordbox_processes_running(lister=lister)
    except processes.AbsenceUnconfirmed:
        return UNKNOWN
    except Exception as exc:  # noqa: BLE001 - see the docstring
        return _unreadable(exc)
    return OPEN if running else CLOSED


def jobs_running(cfg: config.Config) -> list[dict[str, str]] | dict[str, str]:
    """Each running job's id, verb and state, off a queue connection that cannot write."""
    try:
        found = jobs.read_jobs(jobs.queue_path(cfg), states=(jobs.JobState.RUNNING,))
    except Exception as exc:  # noqa: BLE001 - every failure to read is said, never folded
        return _unreadable(exc)
    return [
        {"job_id": job.job_id, "verb": job.handler_key, "state": str(job.state)}
        for job in found
    ]


def _run_records() -> list[Path]:
    """The run record files, listed by a call that raises when it cannot list.

    Never a glob, which reads a directory it cannot list as empty
    (docs/solutions, the glob over an unlistable directory). An absent
    directory is no run yet.
    """
    folder = gates.run_dir()
    try:
        names = os.listdir(folder)
    except FileNotFoundError:
        return []
    return [folder / name for name in sorted(names) if name.endswith(".json")]


def _gate_item(
    state: gates.RunState, path: Path, *, older_than: timedelta, now: datetime
) -> dict[str, Any]:
    """One run waiting at a gate, as the app shows it."""
    try:
        owner = registry.entry(state.verb)
    except KeyError:
        owner = None
    spec = (
        next((g for g in owner.gates if g.name == state.open_gate), None)
        if owner is not None
        else None
    )
    aged = gates.old_gate(state, path, older_than=older_than, now=now)
    return {
        "run_id": state.run_id,
        "verb": state.verb,
        "gate": state.open_gate,
        # What this build declares for the gate; empty and null for a gate it
        # no longer declares, since an unknown answer is not a known one.
        "options": list(spec.options) if spec is not None else [],
        "explicit": spec.explicit if spec is not None else None,
        "writes_database": gates.writes_the_database(state.verb),
        "since": _iso(gates.idle_since(state, path)),
        "old": aged is not None and aged.retirable,
    }


def gate_runs(
    *, older_than: timedelta, now: datetime
) -> list[dict[str, Any]] | dict[str, str]:
    """Every run waiting at a gate, old ones listed, never folded.

    A record that cannot be read is an item ``{run_id, unreadable}``, so one
    damaged record neither hides the others nor reads as no gate; a run
    directory that cannot be listed makes the whole key unreadable.
    """
    try:
        paths = _run_records()
    except Exception as exc:  # noqa: BLE001 - every failure to read is said, never folded
        return _unreadable(exc)
    found: list[dict[str, Any]] = []
    for path in paths:
        try:
            state = gates.load(path.stem)
            if state.open_gate is None:
                continue
            found.append(_gate_item(state, path, older_than=older_than, now=now))
        except Exception as exc:  # noqa: BLE001 - see the docstring
            found.append({"run_id": path.stem, **_unreadable(exc)})
    return found


def night(cfg: config.Config) -> dict[str, Any] | None:
    """The last night pass as ``crate sync night --last`` reads it, or None when none ran.

    Imported here, as doctor's night check imports it, so loading ``crate
    status`` does not load the whole sync pass.
    """
    from cratekit.cli import sync_night  # noqa: PLC0415 - the verb's own record

    try:
        record = sync_night.settle(sync_night.read_status(), cfg)
    except Exception as exc:  # noqa: BLE001 - every failure to read is said, never folded
        return _unreadable(exc)
    if record is None:
        return None
    # Text, as ``--last`` prints each field, so an odd record keeps the shape.
    return {
        name: None if record.get(name) is None else str(record.get(name))
        for name in NIGHT_FIELDS
    }


# ---------------------------------------------------------------------------
# The one word
# ---------------------------------------------------------------------------


def _anything_unreadable(found: Mapping[str, Any]) -> bool:
    for key in KEYS:
        value = found.get(key)
        if is_unreadable(value):
            return True
        if isinstance(value, Sequence) and not isinstance(value, str):
            if any(is_unreadable(item) for item in value):
                return True
    return False


def _portions(found: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    held = found.get("backup")
    if not isinstance(held, Mapping) or is_unreadable(held):
        return []
    return [one for one in held.values() if isinstance(one, Mapping)]


def attention(found: Mapping[str, Any]) -> str:
    """The most urgent of :data:`ATTENTION` that holds for ``found``.

    ``fail`` when any source could not be read, or a backup completion is
    recorded ahead of now, which doctor fails since it satisfies every freshness
    test. ``backup-due`` when a portion is five days old or more, or its age is
    unknown, since could not tell is never fresh enough.
    """
    portions = _portions(found)
    future = str(backup_facts.AgeState.RECORDED_IN_THE_FUTURE)
    if _anything_unreadable(found) or any(one.get("state") == future for one in portions):
        return FAIL
    if found.get("gates"):
        return GATE
    if found.get("jobs_running"):
        return RUNNING
    limit = BACKUP_DUE_AGE.total_seconds()
    for one in portions:
        age = one.get("age_seconds")
        if one.get("state") != str(backup_facts.AgeState.KNOWN) or age is None or age >= limit:
            return BACKUP_DUE
    return OK


def glance(
    cfg: config.Config,
    *,
    now: datetime | None = None,
    lister: processes.ProcessLister | None = None,
) -> dict[str, Any]:
    """The whole glance, every key present, ``attention`` read off the rest."""
    moment = now or datetime.now(timezone.utc)
    older_than = timedelta(days=cfg.reports.open_gate_stale_days)
    found: dict[str, Any] = {
        "version": VERSION,
        "backup": backup(cfg, moment),
        "rekordbox": rekordbox(lister),
        "jobs_running": jobs_running(cfg),
        "gates": gate_runs(older_than=older_than, now=moment),
        "night": night(cfg),
    }
    found["attention"] = attention(found)
    return {key: found[key] for key in KEYS}


__all__ = [
    "ATTENTION",
    "BACKUP_DUE",
    "BACKUP_DUE_AGE",
    "CLOSED",
    "FAIL",
    "GATE",
    "KEYS",
    "NIGHT_FIELDS",
    "OK",
    "OPEN",
    "RUNNING",
    "UNKNOWN",
    "UNREADABLE",
    "VERSION",
    "attention",
    "backup",
    "gate_runs",
    "glance",
    "is_unreadable",
    "jobs_running",
    "night",
    "rekordbox",
]
