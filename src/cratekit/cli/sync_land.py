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

from cratekit.cli import registry, tail
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
            "continue the pass crate sync all queued under this run, rather than "
            "starting a new one; a job that already ended is read, not driven "
            "again, and the tail runs again over the staging folder"
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


def _preflight(report: _Pass, cfg: config.Config) -> None:
    """Refuse before any step while rekordbox, or a backup's driver, is up.

    Rekordbox through the guarded writer's own predicate, so this refusal and
    the landing's are one question asked twice. A backup by its job's driver
    lock, which is the one liveness test the queue trusts: a backup job open in
    the queue whose driver died is not running and does not hold the pass.
    """
    report.say(PREFLIGHT, "rekordbox and backups")
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
    report.check(PREFLIGHT, "ok", "rekordbox is closed and no backup is running")


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
            f"{job.job_id} ({job.state}), continue its pass with: crate sync land "
            f"--pass-run {run_id}"
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
            way_on = (
                f"retry the job, then continue the pass: crate job resume {job.job_id}"
                if job.cause is not None and job.cause.retryable
                else "the job cannot succeed on resume; start a new pass with: crate sync land"
            )
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
        after = (f"then continue the pass: crate sync land --pass-run {resume}",)
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
    steps = tuple(f"continue one pass: crate sync land --pass-run {run}" for run in choose.runs)
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
            f"crate sync land --pass-run {resume}",
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
    _preflight(report, cfg)
    try:
        run_id = ctx.args.pass_run
        if run_id:
            report.summary["pass_run"] = run_id
            report.check(SYNC, "info", f"continuing the pass queued under run {run_id}")
        else:
            run_id = _sync(report, cfg)
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
