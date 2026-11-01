"""``crate sync land``: one sync pass taken to its landing gate in one verb (U152).

Until this verb a pass was ten commands, each typed with an identifier copied
from the one before (sitting 47, ``docs/plans/2026-10-27-one-command-sync.md``):
``sync all`` queued intake jobs nothing drove, ``intake missing``, ``acquire
download`` and its job, the tail of ``tag folder``, ``analyze run``, ``analyze
restamp`` and ``name apply``, and ``intake land``. Skipping the tail was
possible and silent, and the sitting that skipped it planned 116 rows named by
provider id with no vox score.

A CHAIN OF THE VERBS A PERSON WOULD TYPE, NOT A SECOND IMPLEMENTATION OF THEM.
Each step is the existing verb run through the real dispatcher in this process,
under its own run, with its own gates and its own refusals, so nothing a step
decides is decided again here. That is why this module is ranked CLI and not
beside the sync source it starts from: the dispatcher is the CLI layer's, and
only a module of that layer may reach it.

THE TAIL AND THE LANDING ARE :mod:`cratekit.cli.tail`'s, SINCE U190. Preflight,
the pass, its intake jobs, the missing list and the download are this verb's;
the tail in its order over the absolute staging path, the stale tail job
replaced, ``name apply``'s confirm and the landing stopped at its gate are the
chain ``label sync --go`` runs too, lifted out of this module whole so the two
verbs cannot disagree. Every job either meets is driven to settled in the
foreground and read off the queue, and a tail step that does not succeed ends
the pass there, so a landing is never planned over files the tail did not run on.

A DOWNLOAD REFUSAL IS RECORDED AND SKIPPED. An item the worker refused for good,
a lossy only track above all, leaves the job failed with every other item
durable. The pass names each refused track and goes on with the ones that
landed. A refusal that waiting mends, a parked provider, or a job still open
ends the pass instead, because the tracks it holds are still coming.

IT STOPS WHERE A PERSON MUST ACT, AND SAYS WHAT THEY DO. The landing is planned
by ``intake land`` itself, which reads the backup acknowledgment (this verb
never mints one) and stops at its explicit gate on its own run. The envelope is
then PENDING, naming that run, the two commands that answer and apply it as the
session, and the rekordbox visit that follows. This verb never starts a backup,
never opens rekordbox and never writes a beat grid; it refuses before any write
while rekordbox or a backup is running.

EITHER RUN ID CONTINUES THE PASS, SINCE U183. A pass has two: the land run this
verb prints as its own, and the ``sync all`` run its intake jobs carry, which is
the one every step reads. The land run's record names its pass the moment that
pass is known, so ``--pass-run`` takes either, an id that is neither is refused
before any step runs, and every way on the verb prints ends with the one
command that continues the pass.

THE OUTBOUND HEARTS ARE NOT THIS VERB'S. ``sync all`` is run with no export, so
the favourites write half refuses its own precondition and stays behind its own
gate, while the hearts are listed inbound like any playlist. A provider that
withholds hearts is reported once, on the pass's own failing check, and never
retried here.
"""

from __future__ import annotations

import argparse
import dataclasses
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from cratekit.cli import gates, registry, tail
from cratekit.cli.output import Envelope, PendingHumanAction
from cratekit.cli.tail import (
    ACK_STOP,
    ANALYZE,
    ANALYZE_PLAYLIST,
    GATE_STOP,
    LAND,
    LAND_GATE,
    LAND_OPTION,
    LAND_VERB,
    NAME,
    NAME_GATE,
    NAME_OPTION,
    NAME_VERB,
    REKORDBOX_STEPS,
    RESTAMP,
    SESSION_ACTOR,
    TAG,
    TAIL,
)
from cratekit.core import config, jobs, rb_writer
from cratekit.core.cause import CratekitError, Outcome, rebuilt, refuse
from cratekit.core.exit_codes import ExitCode, Remedy

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

_ORIGIN = ("cli.sync_land",)

#: The steps, in the one order a pass runs them. Each is a check key on the
#: envelope, ``sync.land.<step>``. The last five are the tail and the landing,
#: :data:`cratekit.cli.tail.STEPS`, named here from that module.
PREFLIGHT = "preflight"
SYNC = "sync"
INTAKE = "intake"
MISSING = "missing"
DOWNLOAD = "download"
STEPS: tuple[str, ...] = (
    PREFLIGHT, SYNC, INTAKE, MISSING, DOWNLOAD, TAG, ANALYZE, RESTAMP, NAME, LAND,
)

#: The verbs the pass runs that are not the tail's.
SYNC_VERB = "sync.all"
DOWNLOAD_VERB = "acquire.download"
BACKUP_VERB = "backup.run"

#: Why the favourites write half queues nothing in a pass this verb runs: no
#: export is handed to it, so it refuses its own precondition (module docstring).
OUTBOUND_UNASKED = "outbound-export-required"

#: This verb's own name, which a land run's record carries.
LAND_VERB_NAME = "sync.land"

#: The role a land run's record names its pass under (U183),
#: :attr:`cratekit.cli.gates.RunState.related_runs`.
PASS_ROLE = "pass_run"

#: How many of the library's recent passes a refused ``--pass-run`` names.
RECENT_PASSES = 5

#: The seam every step goes through, the shared chain's own, so one stand in
#: serves both verbs that run it.
Child = tail.Child


def build(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    del entry
    parser.add_argument(
        "--pass-run",
        default=None,
        dest="pass_run",
        metavar="RUN_ID",
        help=(
            "continue an earlier pass rather than starting a new one, named by the "
            "run crate sync land printed for it or the run crate sync all queued "
            "it under; a job that already ended is read, not driven again, and "
            "the tail runs again over the staging folder"
        ),
    )
    parser.set_defaults(_handler=sync_land)


def _load() -> config.Config:
    return tail.load_config(_ORIGIN)


# ---------------------------------------------------------------------------
# What the pass did, as it did it
# ---------------------------------------------------------------------------


class _Choose(Exception):
    """Several earlier passes hold open intake jobs, and which to take is a person's."""

    def __init__(self, runs: Sequence[str]) -> None:
        super().__init__(", ".join(runs))
        self.runs = list(runs)


#: The chain's signals and record, named as this module always named them.
_Stop = tail.Stop
_Attend = tail.Attend
_Done = tail.Done
_Pass = tail.Chain


def _report(progress: Callable[[str], None] | None) -> tail.Chain:
    """The pass's record: the shared chain's, keyed ``sync.land`` and counting all ten steps."""
    return tail.Chain(
        progress=progress,
        namespace="sync.land",
        title="sync land",
        steps=STEPS,
        origin=_ORIGIN,
        again="continue the pass",
        summary={
            "pass_run": None,
            "steps": [],
            "commands": [],
            "stopped_at": None,
            "download_refused": [],
            "replaced": [],
        },
    )


def _summary_of(envelope: dict[str, Any]) -> dict[str, Any]:
    data = envelope.get("data") or {}
    summary = data.get("summary") if isinstance(data, dict) else None
    return summary if isinstance(summary, dict) else {}


# ---------------------------------------------------------------------------
# Step 0: nothing is written while rekordbox or a backup is running
# ---------------------------------------------------------------------------


def _preflight(report: _Pass, cfg: config.Config, given: str | None) -> str | None:
    """Resolve a continued pass, then refuse while rekordbox, or a backup's driver, is up.

    Returns the pass to continue, or None for a new one. The pass is resolved
    first (:func:`_resolve`), so an id that names no pass is refused before
    any step runs, and a refusal here names the command that comes back to it.

    Rekordbox through the guarded writer's own predicate, so this refusal and
    the landing's are one question asked twice. A backup by its job's driver
    lock, which is the one liveness test the queue trusts: a backup job open in
    the queue whose driver died is not running and does not hold the pass.
    """
    report.say(PREFLIGHT, "rekordbox and backups")
    taken = _resolve(report, cfg, given) if given else None
    again = _continue_command(taken) if taken else "crate sync land"
    try:
        _nothing_running(cfg)
    except CratekitError as exc:
        raise tail.with_steps(exc, f"then run it again: {again}") from None
    report.check(PREFLIGHT, "ok", "rekordbox is closed and no backup is running")
    return taken


def _nothing_running(cfg: config.Config) -> None:
    rb_writer.assert_rekordbox_closed("crate sync land")
    key = registry.entry(BACKUP_VERB).handler_key
    open_states = [state for state in jobs.JobState if state not in jobs.TERMINAL_STATES]
    with jobs.open_store() as store:
        backups = [
            job
            for job in jobs.list_jobs(store, states=open_states)
            if job.handler_key == key and job.library_id == cfg.library.volume_id
        ]
    for job in backups:
        try:
            jobs.assert_free(job.job_id)
        except jobs.DriverHeld as exc:
            raise refuse(
                "job-driver-held",
                f"backup job {job.job_id} is running, so crate sync land writes "
                f"nothing until it has finished",
                remedy=Remedy.WAIT_FOR_HOLDER,
                retryable=True,
                origin=_ORIGIN,
                detail={"job_id": job.job_id},
                inner=exc.cause,
            ) from exc


def _continue_command(pass_run: str) -> str:
    """The one command that continues ``pass_run``, as every way on prints it."""
    return f"crate sync land --pass-run {pass_run}"


# ---------------------------------------------------------------------------
# Which pass --pass-run names (U183)
# ---------------------------------------------------------------------------


def _land_record(run_id: str) -> gates.RunState | None:
    """``run_id``'s record when it is a ``sync land`` run's, else None.

    Only a bare identifier is looked up, so a value with a path in it reads
    no file outside the run records. A record that cannot be read is no land
    run, since the refusal that follows names the ids that do work.
    """
    if not run_id or run_id != Path(run_id).name or run_id.startswith("."):
        return None
    if not gates.run_path(run_id).is_file():
        return None
    try:
        state = gates.load(run_id)
    except (CratekitError, KeyError, TypeError, ValueError, OSError):
        return None
    return state if state.verb == LAND_VERB_NAME else None


def _resolve(report: _Pass, cfg: config.Config, given: str) -> str:
    """The pass ``--pass-run`` names: a pass run as given, a land run as the pass it recorded.

    A PASS RUN IS ONE AN INTAKE JOB OF THIS LIBRARY CARRIES, which is exactly
    what ``intake missing --run`` asks of it at the fourth step, so an id that
    passes here is never refused there for the same reason. Anything else is
    refused now, before a step runs or a provider is called.
    """
    with jobs.open_store() as store:
        if _pass_jobs(store, given, cfg):
            return given
    land = _land_record(given)
    recorded = land.related_runs.get(PASS_ROLE) if land is not None else None
    if recorded:
        with jobs.open_store() as store:
            if _pass_jobs(store, recorded, cfg):
                report.check(
                    PREFLIGHT,
                    "info",
                    f"run {given} is a crate sync land run; continuing the pass it "
                    f"recorded, run {recorded}",
                )
                return recorded
    raise _unknown_pass(cfg, given, land, recorded)


def _recent_passes(cfg: config.Config) -> list[str]:
    """The passes this library's intake jobs carry, newest first, each once."""
    from cratekit.intake import cli as intake_cli  # noqa: PLC0415 - one module's keys

    found: list[str] = []
    with jobs.open_store() as store:
        for job in jobs.list_jobs(store):
            run_id = _run_of(job)
            if (
                run_id
                and run_id not in found
                and job.handler_key in intake_cli.INTAKE_KEYS
                and job.library_id == cfg.library.volume_id
            ):
                found.append(run_id)
    return found[:RECENT_PASSES]


def _land_runs_of(passes: Sequence[str]) -> dict[str, str]:
    """The newest land run recorded for each of ``passes``, where one is."""
    try:
        paths = sorted(gates.run_dir().glob("*.json"))
    except OSError:
        return {}
    found: dict[str, str] = {}
    for path in paths:
        land = _land_record(path.stem)
        recorded = land.related_runs.get(PASS_ROLE) if land is not None else None
        if land is not None and recorded in passes:
            found[str(recorded)] = land.run_id
    return found


def _unknown_pass(
    cfg: config.Config, given: str, land: gates.RunState | None, recorded: str | None
) -> CratekitError:
    """The refusal for an id that names no pass of this library, with the ids that do."""
    if land is None:
        why = "it is neither a pass run an intake job of this library carries nor a crate sync land run"
    elif recorded:
        why = (
            f"it is a crate sync land run whose pass, run {recorded}, no intake job "
            f"of this library carries"
        )
    else:
        why = (
            "it is a crate sync land run that recorded no pass: it queued nothing, "
            "stopped before its pass was queued, or was run by a build before U183"
        )
    passes = _recent_passes(cfg)
    lands = _land_runs_of(passes)
    steps = [
        f"continue pass {run_id}"
        + (f" (crate sync land run {lands[run_id]})" if run_id in lands else "")
        + f": {_continue_command(run_id)}"
        for run_id in passes
    ]
    known = (
        "; the library's recent passes are " + ", ".join(passes)
        if passes
        else "; this library has no pass with an intake job to continue"
    )
    return refuse(
        "job-unknown",
        f"crate sync land cannot continue run {given!r}: {why}{known}",
        steps=(*steps, "or start a new pass: crate sync land"),
        origin=_ORIGIN,
        detail={"run_id": given, "recent_passes": passes, "land_runs": lands},
    )


def _remember(ctx: Context, report: _Pass, pass_run: str) -> None:
    """Record the pass on this run's own record now, before any step can stop it.

    The dispatcher saves the record only when the verb answers or a gate
    refuses, so a pass that fails at a later step, or is interrupted, would
    otherwise leave a land run whose id continues nothing.
    """
    ctx.run.related_runs[PASS_ROLE] = pass_run
    gates.save(ctx.run)
    report.say(
        SYNC,
        f"the pass is run {pass_run}; if it stops, continue it with: "
        f"{_continue_command(pass_run)}",
    )


# ---------------------------------------------------------------------------
# Steps 1 and 2: the pass and its intake jobs
# ---------------------------------------------------------------------------


def _lift_failed_checks(report: _Pass, envelope: dict[str, Any]) -> None:
    """The pass's own failing checks, carried whole so a shortfall is read once.

    ONE IS LEFT, BY DESIGN. The favourites write half refuses for want of the
    export this verb never hands it, every pass, and a FAIL row on every pass
    for the act the verb chose not to take would teach a person to read past
    the row beside it, the withheld hearts. It is said once, as a note.
    """
    data = envelope.get("data") or {}
    not_queued = _summary_of(envelope).get("not_queued") or {}
    held = {
        f"sync.{source}"
        for source, reason in not_queued.items()
        if reason == OUTBOUND_UNASKED
    }
    for check in (data.get("checks") or ()) if isinstance(data, dict) else ():
        if not isinstance(check, dict) or check.get("status") != "fail":
            continue
        if check.get("key") in held:
            continue
        report.checks.append(dict(check))
    if held:
        report.check(
            SYNC,
            "info",
            "the outbound hearts write is not this verb's and was not run: "
            + ", ".join(sorted(held))
            + " queued nothing, since no export is handed to the pass",
        )


def _open_intake(cfg: config.Config) -> list[jobs.Job]:
    """Every intake job of this library still open, whoever queued it."""
    from cratekit.intake import cli as intake_cli  # noqa: PLC0415 - one module's keys

    open_states = [state for state in jobs.JobState if state not in jobs.TERMINAL_STATES]
    with jobs.open_store() as store:
        return [
            job
            for job in jobs.list_jobs(store, states=open_states)
            if job.handler_key in intake_cli.INTAKE_KEYS
            and job.library_id == cfg.library.volume_id
        ]


def _run_of(job: jobs.Job) -> str:
    return str((job.payload or {}).get("run_id") or "")


def _open_passes(cfg: config.Config) -> dict[str, list[str]]:
    """Every pass run with an intake job still open, and those jobs."""
    found: dict[str, list[str]] = {}
    for job in _open_intake(cfg):
        if _run_of(job):
            found.setdefault(_run_of(job), []).append(job.job_id)
    return found


def _left_behind(report: _Pass, cfg: config.Config, taken: str | None) -> None:
    """Name every open intake job this pass will not drive, with the way on to each.

    ``sync all`` leaves a playlist out of a new pass while an intake job for it
    is still open, whether an earlier pass queued that job or a person typed
    ``intake playlist``, and that job holds the playlist out of every later
    pass until it is driven. The pass drives only its own run's jobs, so the
    rest are said here, on a failing row, rather than nowhere.
    """
    left = [job for job in _open_intake(cfg) if not taken or _run_of(job) != taken]
    if not left:
        return
    ways = []
    for job in left:
        run_id = _run_of(job)
        ways.append(
            f"{job.job_id} ({job.state}), continue its pass with: "
            f"{_continue_command(run_id)}"
            if run_id
            else f"{job.job_id} ({job.state}), queued by hand, drive it with: crate "
            + " ".join(tail.argv_for(job))
        )
    report.summary["left_open"] = [job.job_id for job in left]
    report.checks.append(
        {
            "key": "sync.land.left-open",
            "title": "left open",
            "status": "fail",
            "detail": (
                f"{len(left)} intake job(s) this pass does not drive are still open, "
                f"and each holds its playlist out of every pass until it is: "
                + "; ".join(ways)
            ),
            "remedy": None,
        }
    )
    report.warnings.append(
        {
            "code": "sync-land-intake-left-open",
            "message": (
                f"{len(left)} open intake job(s) outside this pass: "
                + ", ".join(job.job_id for job in left)
            ),
        }
    )


def _sync(report: _Pass, cfg: config.Config) -> str | None:
    """Run ``sync all`` and return the pass's run, or None when there is none to take.

    A PASS THAT QUEUED NOTHING IS NOT A PASS WITH NOTHING TO DO. ``sync all``
    leaves out a playlist whose intake job is still open from an earlier pass,
    the state sitting 47 started from: ``sync all`` typed by hand, its jobs
    queued and never driven. That earlier pass is then the one to take, and
    when there are several, which is a person's choice and the pass names them.
    """
    envelope = tail.required(report, SYNC, ["sync", "all"])
    _lift_failed_checks(report, envelope)
    summary = _summary_of(envelope)
    run_id = str(summary.get("run_id") or envelope.get("run_id") or "")
    report.summary["pass_run"] = run_id
    if envelope.get("outcome") == str(Outcome.NO_OP):
        earlier = _open_passes(cfg)
        if len(earlier) == 1:
            ((held, job_ids),) = earlier.items()
            report.summary["pass_run"] = held
            report.check(
                SYNC,
                "info",
                f"sync all queued nothing new; continuing the pass queued under run "
                f"{held}, whose intake job(s) {', '.join(job_ids)} are still open",
            )
            return held
        if earlier:
            raise _Choose(sorted(earlier))
        report.check(SYNC, "info", f"sync all queued nothing new under run {run_id}")
        return None
    report.check(
        SYNC,
        "ok",
        f"sync all queued {summary.get('queued', 0)} job(s) under run {run_id}",
    )
    return run_id


def _pass_jobs(store: jobs.JobStore, run_id: str, cfg: config.Config) -> list[jobs.Job]:
    from cratekit.intake import cli as intake_cli  # noqa: PLC0415 - one module's keys

    return [
        job
        for job in jobs.list_jobs(store)
        if job.handler_key in intake_cli.INTAKE_KEYS
        and str((job.payload or {}).get("run_id") or "") == run_id
        and job.library_id == cfg.library.volume_id
    ]


def _intake(report: _Pass, run_id: str, cfg: config.Config) -> None:
    """Drive every intake job of the pass to settled; any not succeeded ends it."""
    with jobs.open_store() as store:
        found = _pass_jobs(store, run_id, cfg)
    settled = [tail.settle(report, INTAKE, job) for job in found]
    for job in settled:
        if job.state is not jobs.JobState.SUCCEEDED:
            error = tail.job_error(report, job)
            if job.is_open():
                raise _Stop(INTAKE, error)
            # AN INTAKE JOB THAT ENDED is not driven again by a continued pass,
            # so the way on is the job's own retry or a new pass.
            # A RETRYABLE ONE IS, ONCE ITS OWN RETRY HAS RUN, so its way on ends
            # with the continuation (U183); one that cannot succeed ends with a
            # new pass, the one command that can.
            if job.cause is not None and job.cause.retryable:
                retry = f"retry the job first: crate job resume {job.job_id}"
                raise _Stop(INTAKE, tail.with_steps(error, retry))
            way_on = "the job cannot succeed on resume; start a new pass with: crate sync land"
            raise _Stop(INTAKE, tail.with_steps(error, way_on), continues=False)
    report.check(
        INTAKE,
        "ok",
        f"{len(settled)} intake job(s) of run {run_id} succeeded: "
        + ", ".join(job.job_id for job in settled),
    )


# ---------------------------------------------------------------------------
# Steps 3 and 4: one list, one download
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class _Listed:
    path: Path
    land_name: str


def _missing(report: _Pass, run_id: str) -> _Listed:
    envelope = tail.required(report, MISSING, ["intake", "missing", "--run", run_id])
    # THE LISTING'S OWN FAILING ROWS RIDE THROUGH, a missing track the provider
    # cannot name exactly above all: it is in no download list, and the pass
    # would otherwise say nothing of it.
    _lift_failed_checks(report, envelope)
    summary = _summary_of(envelope)
    listed = summary.get("list")
    land_name = str(summary.get("land_name") or "")
    if envelope.get("outcome") == str(Outcome.NO_OP) or not listed:
        unlisted = int(summary.get("unlisted") or 0)
        report.check(
            MISSING,
            "info",
            f"the pass listed nothing to download (owned {summary.get('owned', 0)}, "
            f"offered {summary.get('offered', 0)}, missing and not nameable "
            f"{unlisted}), so nothing is downloaded or landed",
        )
        raise _Done(MISSING)
    report.summary["list"] = str(listed)
    report.summary["land_name"] = land_name
    report.check(
        MISSING,
        "ok",
        f"{summary.get('written', summary.get('missing', 0))} missing track(s) "
        f"listed as one at {listed}",
    )
    return _Listed(path=Path(str(listed)), land_name=land_name)


def _download_job(store: jobs.JobStore, listed: Path, cfg: config.Config) -> jobs.Job | None:
    """The download job already queued over this list, newest first, or None.

    A pass continued with ``--pass-run`` lists the same tracks into the same
    file, and queueing it again would download each of them twice. A cancelled
    job is nobody's claim on the list and is passed over.
    """
    from cratekit.acquire import cli as acquire_cli  # noqa: PLC0415 - one module's key

    key = registry.entry(DOWNLOAD_VERB).handler_key
    wanted = str(listed.expanduser().absolute())
    # ``list_jobs`` IS NEWEST FIRST already, so the first match is the newest.
    for job in jobs.list_jobs(store):
        if (
            job.handler_key == key
            and job.library_id == cfg.library.volume_id
            and str((job.payload or {}).get(acquire_cli.LIST) or "") == wanted
            and job.state is not jobs.JobState.CANCELLED
        ):
            return job
    return None


def _download(report: _Pass, listed: _Listed, cfg: config.Config) -> int:
    """Download the list, skip what was refused for good, and return how many landed."""
    with jobs.open_store() as store:
        job = _download_job(store, listed.path, cfg)
        if (
            job is not None
            and job.state is jobs.JobState.FAILED
            and job.cause is not None
            and job.cause.retryable
        ):
            job = jobs.retry(store, job.job_id)
    if job is None:
        envelope = tail.required(report, DOWNLOAD, ["acquire", "download", str(listed.path)])
        job_id = str((envelope.get("data") or {}).get("job_id") or "")
        if envelope.get("outcome") == str(Outcome.NO_OP) or not job_id:
            report.check(DOWNLOAD, "info", "the list held no track to download")
            raise _Done(DOWNLOAD)
        with jobs.open_store() as store:
            job = jobs.get(store, job_id)
    job = tail.settle(report, DOWNLOAD, job)
    with jobs.open_store() as store:
        held = jobs.items(store, job.job_id)
    done = [item for item in held if item.state is jobs.ItemState.DONE]
    failed = [item for item in held if item.state is jobs.ItemState.FAILED]
    permanent = [item for item in failed if item.cause is not None and not item.cause.retryable]
    settled_with_refusals = job.state is jobs.JobState.FAILED and len(permanent) == len(failed)
    if job.state is not jobs.JobState.SUCCEEDED and not settled_with_refusals:
        raise _Stop(DOWNLOAD, tail.job_error(report, job))
    # A TRACK THE DOWNLOAD DECLINED IS REFUSED TOO (U169). Since that unit a
    # policy refusal settles the item as skipped and the job succeeds, so the
    # failed items above are only what an earlier build recorded; read alone
    # they would report a clean download over a track that never landed.
    refused = [
        {
            "item_id": item.item_id,
            "reason": item.cause.reason if item.cause else None,
            "message": item.cause.message if item.cause else None,
        }
        for item in held
        if item in permanent or (item.state is jobs.ItemState.SKIPPED and item.cause is not None)
    ]
    report.summary["download_job"] = job.job_id
    report.summary["download_refused"] = refused
    if refused:
        reasons = sorted({str(row["reason"]) for row in refused})
        report.warnings.append(
            {
                "code": "sync-land-download-refused",
                "message": (
                    f"{len(refused)} track(s) were refused by the download and are "
                    f"skipped ({', '.join(reasons)}): "
                    + ", ".join(str(row["item_id"]) for row in refused)
                ),
            }
        )
    if not done:
        report.check(
            DOWNLOAD,
            "fail" if refused else "info",
            f"download job {job.job_id} landed no track"
            + (f"; {len(refused)} refused" if refused else ""),
        )
        raise _Done(DOWNLOAD)
    report.check(
        DOWNLOAD,
        "ok",
        f"download job {job.job_id} landed {len(done)} track(s)"
        + (f"; {len(refused)} refused and skipped" if refused else ""),
    )
    return len(done)


def _attended(ctx: Context, report: _Pass, stop: _Attend) -> Envelope:
    """The PENDING envelope a pass ends on when a step waits for a person.

    It names what the person does, as commands, in order, through the chain's
    one wording of a stop (:func:`cratekit.cli.tail.attended`), and nothing is
    answered here: the gate's run is the step's own, and the acknowledgment is
    minted by the session through its own verb.
    """
    resume = report.summary.get("pass_run")
    if stop.step == LAND:
        after = REKORDBOX_STEPS
    elif resume:
        after = (f"then continue the pass: {_continue_command(resume)}",)
    else:
        after = ("then run the pass again: crate sync land",)
    said = tail.attended(report, stop, after=after)
    summary = "the pass " + said.summary
    if stop.step == LAND:
        summary = "the pass is downloaded, tagged, analysed and named; " + summary
    pending = PendingHumanAction(
        kind=said.kind,
        id=f"sync-land-{report.summary['pass_run'] or ctx.run.run_id}",
        summary=summary,
        verify_verb=LAND_VERB if stop.step == LAND else ctx.entry.name,
        steps=said.steps,
    )
    return ctx.envelope(
        data=report.data(),
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=pending,
        warnings=report.warnings,
    )


def _choose(ctx: Context, report: _Pass, choose: _Choose) -> Envelope:
    """The PENDING envelope a pass ends on when several earlier passes are open."""
    report.summary["stopped_at"] = SYNC
    report.summary["open_passes"] = list(choose.runs)
    steps = tuple(f"continue one pass: {_continue_command(run)}" for run in choose.runs)
    report.check(
        SYNC,
        "info",
        f"sync all queued nothing new, and {len(choose.runs)} earlier passes hold "
        f"open intake jobs: {', '.join(choose.runs)}",
    )
    report.summary["attended"] = list(steps)
    pending = PendingHumanAction(
        kind="external_step",
        id=f"sync-land-{ctx.run.run_id}",
        summary=(
            f"{len(choose.runs)} earlier sync passes hold open intake jobs; choose "
            f"which one to continue"
        ),
        verify_verb=ctx.entry.name,
        steps=steps,
    )
    return ctx.envelope(
        data=report.data(),
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=pending,
        warnings=report.warnings,
    )


# ---------------------------------------------------------------------------
# The verb
# ---------------------------------------------------------------------------


def _ended(report: _Pass, stop: _Stop) -> CratekitError:
    """The refusal a stopped pass ends with: the step's own, the pass in its detail."""
    cause = stop.error.cause
    report.summary["stopped_at"] = stop.step
    remedy = cause.remediation.remedy
    report.check(stop.step, "fail", cause.message, remedy=str(remedy) if remedy else None)
    steps = cause.remediation.steps
    resume = report.summary.get("pass_run")
    if resume and stop.continues:
        steps = (
            *steps,
            f"every step before {stop.step} is kept; continue the pass with: "
            f"{_continue_command(resume)}",
        )
    return rebuilt(
        stop.error,
        dataclasses.replace(
            cause,
            remediation=dataclasses.replace(cause.remediation, steps=steps),
            detail={**dict(cause.detail or {}), "sync_land": report.data()},
        ),
    )


def sync_land(ctx: Context) -> Envelope:
    """Take one sync pass to its landing gate. See the module docstring."""
    cfg = _load()
    report = _report(ctx.progress)
    run_id = _preflight(report, cfg, ctx.args.pass_run)
    try:
        if run_id:
            report.summary["pass_run"] = run_id
            report.check(SYNC, "info", f"continuing the pass queued under run {run_id}")
        else:
            run_id = _sync(report, cfg)
        if run_id:
            _remember(ctx, report, run_id)
        _left_behind(report, cfg, run_id)
        if run_id is None:
            raise _Done(SYNC)
        _intake(report, run_id, cfg)
        listed = _missing(report, run_id)
        _download(report, listed, cfg)
        staging = cfg.paths.download_staging.expanduser().absolute()
        tail.run(report, staging, cfg, ["--pass", listed.land_name])
    except _Done as done:
        report.summary["stopped_at"] = done.step
    except _Attend as stop:
        return _attended(ctx, report, stop)
    except _Choose as choose:
        return _choose(ctx, report, choose)
    except _Stop as stop:
        raise _ended(report, stop) from None
    return ctx.envelope(data=report.data(), outcome=Outcome.NO_OP, warnings=report.warnings)


__all__ = [
    "ACK_STOP",
    "ANALYZE",
    "ANALYZE_PLAYLIST",
    "GATE_STOP",
    "LAND",
    "LAND_GATE",
    "LAND_OPTION",
    "NAME",
    "NAME_GATE",
    "NAME_OPTION",
    "NAME_VERB",
    "REKORDBOX_STEPS",
    "RESTAMP",
    "SESSION_ACTOR",
    "STEPS",
    "TAG",
    "TAIL",
    "build",
    "sync_land",
]
