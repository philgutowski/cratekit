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

NO PASS LANDS ROWS WITH NO VOCAL SCORE UNLESS TOLD TO (U181). Before the pass
queues anything, on a profile with the vocals module on, it asks the vocals
module whether the model can score here, and when it cannot it stops at its
named gate ``sync.land.without-vocals``, whose screen names the command that
mends it; ``go`` takes the pass on without vocal scores. Sitting 51
landed nineteen rows with no voxlevel from a copy installed without the
vocals extra, and found out from one clause of the landing plan.

A TRACK AN UNLANDED PASS STAGED IS NOT DOWNLOADED AGAIN (U212). The listing
counts a missing track a staged file already carries as staged, and the pass
says how many on its missing step. A pass with nothing to download and
something staged skips the download and runs the tail and the landing over
the staging folder, which takes the staged files, rather than ending with
nothing landed. Sitting 55 downloaded two such tracks again, and the copies
stopped the name step on names already taken.

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
from cratekit.cli import jobs as cli_jobs
from cratekit.cli.output import Envelope, PendingHumanAction
from cratekit.cli.tail import (
    ACK_STOP,
    ANALYZE,
    ANALYZE_PLAYLIST,
    GATE_STOP,
    GUESS,
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
#: envelope, ``sync.land.<step>``. The last six are the tail and the landing,
#: :data:`cratekit.cli.tail.STEPS`, named here from that module.
PREFLIGHT = "preflight"
SYNC = "sync"
INTAKE = "intake"
MISSING = "missing"
DOWNLOAD = "download"
STEPS: tuple[str, ...] = (
    PREFLIGHT, SYNC, INTAKE, MISSING, DOWNLOAD, TAG, GUESS, ANALYZE, RESTAMP, NAME, LAND,
)

#: The verbs the pass runs that are not the tail's.
SYNC_VERB = "sync.all"
DOWNLOAD_VERB = tail.DOWNLOAD_VERB
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

#: The preflight's row for the vocal model, ``sync.land.vocal-model`` (U181).
VOCAL_MODEL = "vocal-model"
#: The gate a pass asks when the vocal model cannot score here (U181), and the
#: answer that takes the pass on without vocal scores. Declared on the entry.
WITHOUT_VOCALS = "sync.land.without-vocals"
WITHOUT_VOCALS_GO = "go"
#: The refusal a pass gives when that gate is answered ``stop``.
VOCALS_UNAVAILABLE = "vocal-scoring-unavailable"
#: The warning a pass carries when it went on without vocal scores.
WITHOUT_VOCALS_WARNING = "sync-land-without-vocals"


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


def preflight(report: _Pass, cfg: config.Config) -> None:
    """Refuse before any step while rekordbox, or a backup's driver, is up.

    Rekordbox through the guarded writer's own predicate, so this refusal and
    the landing's are one question asked twice. A backup by its job's driver
    lock, which is the one liveness test the queue trusts: a backup job open in
    the queue whose driver died is not running and does not hold the pass.

    SHARED WITH ``crate sync bandcamp`` (U179), which runs it as its own first
    step, so the two sources of the driver refuse on one predicate. The verb
    is named from the chain's title.
    """
    verb = f"crate {report.title}"
    report.say(PREFLIGHT, "rekordbox and backups")
    rb_writer.assert_rekordbox_closed(verb)
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
                f"backup job {job.job_id} is running, so {verb} writes "
                f"nothing until it has finished",
                remedy=Remedy.WAIT_FOR_HOLDER,
                retryable=True,
                origin=_ORIGIN,
                detail={"job_id": job.job_id},
                inner=exc.cause,
            ) from exc
    report.check(PREFLIGHT, "ok", "rekordbox is closed and no backup is running")


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
    except (CratekitError, AttributeError, KeyError, TypeError, ValueError, OSError):
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


def _vocals(ctx: Context, report: _Pass, cfg: config.Config) -> None:
    """Stop before the pass when the vocal model cannot score here, until told to go on (U181).

    Sitting 51 landed a pass from a copy installed without the vocals extra:
    ``analyze run`` finished every file with no voxlevel, the head it wrote
    made every later run skip them, and the landing plan said so in one line.
    So the pass asks first, through the vocals module's one test, and before
    anything is queued it stops at its named gate, whose screen names what is
    missing and the command that mends it. ``go`` takes the pass on without
    vocal scores, and the summary and a warning say so; ``stop`` refuses
    ``vocal-scoring-unavailable`` with the same command.

    THE STOP IS THE GATE'S OWN REFUSAL, decision required, rather than a
    precondition of its own: every gate a verb declares refuses that way and
    leaves its run resumable, so the answer is given inline with ``-d`` or
    recorded with ``crate run decide`` and continued with ``--run``, the two
    ways every other gate is answered.

    A PROFILE WITH THE VOCALS MODULE OFF IS NOT ASKED. It has no vocals verb,
    and is a person who chose not to score vocals, so its pass goes on as it
    always did and the row says why nothing was asked.
    """
    report.say(PREFLIGHT, "the vocal model")
    if not tail.vocals_on(cfg):
        report.summary["vocal_scoring"] = "off"
        report.note(
            VOCAL_MODEL,
            "info",
            "the vocals module is off on this profile, so the pass does not ask "
            "whether the vocal model can score",
        )
        return
    unable = tail.vocals_unavailable()
    if unable is None:
        report.summary["vocal_scoring"] = "available"
        report.note(VOCAL_MODEL, "ok", "the vocal model can score here")
        return
    again = f"crate -d {WITHOUT_VOCALS}={WITHOUT_VOCALS_GO} sync land" + (
        f" --pass-run {ctx.args.pass_run}" if ctx.args.pass_run else ""
    )
    spec = next(gate for gate in ctx.entry.gates if gate.name == WITHOUT_VOCALS)
    option = ctx.gate.require(
        spec,
        context={
            "vocal model": f"cannot score here: {unable}",
            "without it": "every row this pass lands carries no voxlevel and no vox My Tag",
            "nothing queued": "the pass stopped before its first step",
            "to go on without vocal scores": again,
        },
    )
    if option != WITHOUT_VOCALS_GO:
        raise refuse(
            VOCALS_UNAVAILABLE,
            f"the vocal model cannot score here and {WITHOUT_VOCALS} answered "
            f"{option}, so the pass stopped before queueing anything: {unable}",
            remedy=Remedy.RUN_DOCTOR,
            steps=(f"make the vocal model able to score here, then run the pass again: {unable}",),
            origin=_ORIGIN,
            detail={"vocal_model": unable, "gate": WITHOUT_VOCALS, "answered": option},
        )
    report.summary["vocal_scoring"] = "skipped"
    report.note(
        VOCAL_MODEL,
        "info",
        f"the vocal model cannot score here and {WITHOUT_VOCALS} answered "
        f"{WITHOUT_VOCALS_GO}, so the pass goes on without vocal scores: {unable}",
    )
    report.warnings.append(
        {
            "code": WITHOUT_VOCALS_WARNING,
            "message": (
                f"vocal scoring was skipped, as {WITHOUT_VOCALS} answered, so the rows "
                f"this pass lands carry no voxlevel and no vox My Tag: {unable}"
            ),
        }
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
    """Name every open intake job this pass will not drive, by playlist, with the way on.

    ``sync all`` leaves a playlist out of a new pass while an intake job for it
    is still open, whether an earlier pass queued that job or a person typed
    ``intake playlist``, and that job holds the playlist out of every later
    pass until it is driven. The pass drives only its own run's jobs, so the
    rest are said here, on a failing row, rather than nowhere.

    GROUPED BY PLAYLIST, WITH AGE, SIZE AND COPIES (U182). Sitting 51 read 17
    such jobs as ids alone, six weeks old, ten of them copies of two lists, and
    could not judge one. Each job now says how old it is, how many tracks it
    holds and which other open job holds exactly the same ones, and the row
    says what a cancel buys, since cancelling is how a stale job is let go.
    """
    with jobs.open_store() as store:
        holds = cli_jobs.intake_holds(store, cfg.library.volume_id, now=cli_jobs.now())
    left = [hold for hold in holds if not taken or _run_of(hold.job) != taken]
    if not left:
        return
    # ONE PLAYLIST AS THE PASS READS IT, a typed URL and a sweep's id together,
    # named by the newest job that froze the account's name, else the newest.
    grouped: dict[str, list[cli_jobs.Hold]] = {}
    for hold in left:
        grouped.setdefault(hold.identity or hold.label(), []).append(hold)
    by_playlist = {
        next((hold for hold in held if hold.named), held[0]).label(): held
        for held in grouped.values()
    }
    groups = [
        f"{label}: " + "; ".join(_way_on(hold) for hold in held)
        for label, held in by_playlist.items()
    ]
    report.summary["left_open"] = [hold.job.job_id for hold in left]
    report.summary["left_open_playlists"] = [
        {
            "playlist": label,
            "jobs": [
                {
                    "job_id": hold.job.job_id,
                    "state": str(hold.job.state),
                    "age_days": hold.age_days,
                    "tracks": hold.tracks,
                    "same_tracks": list(hold.same_tracks),
                }
                for hold in held
            ],
        }
        for label, held in by_playlist.items()
    ]
    report.checks.append(
        {
            "key": "sync.land.left-open",
            "title": "left open",
            "status": "fail",
            "detail": (
                f"{len(left)} intake job(s) this pass does not drive are still open, "
                f"for {len(by_playlist)} playlist(s), and each holds its playlist out "
                f"of every pass until it is driven or cancelled. Cancelling a job lets "
                f"its playlist's increment queue again on the next pass (list the "
                f"stale ones first with: crate job cancel --stale-days DAYS --dry-run). "
                + " | ".join(groups)
            ),
            "remedy": None,
        }
    )
    report.warnings.append(
        {
            "code": "sync-land-intake-left-open",
            "message": (
                f"{len(left)} open intake job(s) outside this pass: "
                + ", ".join(hold.job.job_id for hold in left)
            ),
        }
    )


def _way_on(hold: cli_jobs.Hold) -> str:
    """One left open job: its state, age, size and copies, then the command that takes it."""
    job = hold.job
    facts = [str(job.state), hold.age(), f"{hold.tracks} track(s)"]
    if hold.same_tracks:
        facts.append("the same tracks as " + ", ".join(hold.same_tracks))
    run_id = _run_of(job)
    way = (
        f"continue its pass with: {_continue_command(run_id)}"
        if run_id
        else "queued by hand, drive it with: crate " + " ".join(tail.argv_for(job))
    )
    return f"{job.job_id} ({', '.join(facts)}), {way}"


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


def _intake(report: _Pass, run_id: str, cfg: config.Config) -> bool:
    """Drive every intake job of the pass to settled; any not succeeded ends it.

    A CANCELLED JOB IS NEVER DRIVEN AGAIN (U182). A person cancels a stale job
    to let its playlist go, often one copy of several holding the same tracks
    in one run, so a continued pass names each cancelled job, drives the rest,
    and lists them without it. Returns whether any job was left out that way.
    When every job of the run was cancelled the pass has nothing to take, and
    it says the next pass queues those playlists again, never to resume one.
    """
    with jobs.open_store() as store:
        found = _pass_jobs(store, run_id, cfg)
    cancelled = [job.job_id for job in found if job.state is jobs.JobState.CANCELLED]
    live = [job for job in found if job.state is not jobs.JobState.CANCELLED]
    if cancelled:
        report.summary["cancelled_jobs"] = cancelled
        said = (
            f"{len(cancelled)} intake job(s) of run {run_id} were cancelled and are "
            f"not driven again: {', '.join(cancelled)}"
        )
        if not live:
            report.check(
                INTAKE,
                "info",
                said + "; every job of the pass was cancelled, so it has nothing to "
                "take, and the next pass queues their playlists again: crate sync land",
            )
            raise _Done(INTAKE)
        report.check(INTAKE, "info", said + "; the rest of the pass goes on without them")
    settled = [tail.settle(report, INTAKE, job) for job in live]
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
    return bool(cancelled)


# ---------------------------------------------------------------------------
# Steps 3 and 4: one list, one download
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class _Listed:
    #: The list to download, or None when every missing track is staged (U212).
    path: Path | None
    land_name: str
    #: How many missing tracks a staged file already carries.
    staged: int = 0


def _missing(report: _Pass, run_id: str, *, without_cancelled: bool = False) -> _Listed:
    argv = ["intake", "missing", "--run", run_id]
    if without_cancelled:
        # THE LISTING'S OWN WORD FOR LEAVING A CLOSED JOB OUT, which it then
        # names on a failing row of its own. Only cancelled jobs reach here: a
        # failed one ended the pass at its intake step.
        argv.append("--skip-failed")
    envelope = tail.required(report, MISSING, argv)
    # THE LISTING'S OWN FAILING ROWS RIDE THROUGH, a missing track the provider
    # cannot name exactly above all: it is in no download list, and the pass
    # would otherwise say nothing of it.
    _lift_failed_checks(report, envelope)
    summary = _summary_of(envelope)
    listed = summary.get("list")
    land_name = str(summary.get("land_name") or "")
    staged = int(summary.get("staged") or 0)
    if (envelope.get("outcome") == str(Outcome.NO_OP) or not listed) and not staged:
        unlisted = int(summary.get("unlisted") or 0)
        report.check(
            MISSING,
            "info",
            f"the pass listed nothing to download (owned {summary.get('owned', 0)}, "
            f"offered {summary.get('offered', 0)}, missing and not nameable "
            f"{unlisted}), so nothing is downloaded or landed",
        )
        raise _Done(MISSING)
    report.summary["staged"] = staged
    report.summary["land_name"] = land_name
    # SAID ON THE STEP THAT DECIDED IT (U212), so a person reading the pass
    # sees why fewer tracks were downloaded than the playlists asked for.
    held = (
        "staged already by a download not landed yet, not downloaded again, and "
        "the landing over the staging folder lands them"
    )
    if not listed:
        report.check(
            MISSING,
            "ok",
            f"nothing to download: {staged} missing track(s) are {held}",
        )
        return _Listed(path=None, land_name=land_name, staged=staged)
    report.summary["list"] = str(listed)
    report.check(
        MISSING,
        "ok",
        f"{summary.get('written', summary.get('missing', 0))} missing track(s) "
        f"listed as one at {listed}"
        + (f"; {staged} more {held}" if staged else ""),
    )
    return _Listed(path=Path(str(listed)), land_name=land_name, staged=staged)


def _staged_on(listed: _Listed) -> str:
    """The clause a download that landed nothing adds when the pass staged tracks (U212)."""
    if not listed.staged:
        return ""
    return f"; the {listed.staged} staged track(s) are landed without it"


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
    """Download the list, skip what was refused for good, and return how many landed.

    A pass whose every missing track is staged has no list, and the tail and
    the landing go on over what is staged (U212).
    """
    from cratekit.acquire import cli as acquire_cli  # noqa: PLC0415 - one module's reading

    if listed.path is None:
        report.check(DOWNLOAD, "info", "nothing downloaded: every missing track is staged already")
        return 0
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
            report.check(
                DOWNLOAD, "info", "the list held no track to download" + _staged_on(listed)
            )
            if not listed.staged:
                raise _Done(DOWNLOAD)
            return 0
        with jobs.open_store() as store:
            job = jobs.get(store, job_id)
    job = tail.settle(report, DOWNLOAD, job)
    # THE ONE READING OF A SETTLED DOWNLOAD (R-1115), shared with ``label sync
    # --go``: SUCCEEDED, or FAILED only by tracks refused for good. A track the
    # download declined is refused too (U169): since that unit a policy
    # refusal settles the item as skipped and the job succeeds, so read alone
    # the failed items would report a clean download over a track that never
    # landed.
    with jobs.open_store() as store:
        read = acquire_cli.read_download(store, job)
    if not read.settled:
        raise _Stop(DOWNLOAD, tail.job_error(report, job))
    done = read.done
    refused = [dict(row) for row in read.refused]
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
            + (f"; {len(refused)} refused" if refused else "")
            + _staged_on(listed),
        )
        # WHAT IS STAGED STILL LANDS (review round one, F1): a download that
        # landed nothing ends the pass only when nothing was staged either,
        # since the missing step already told the person the landing takes it.
        if not listed.staged:
            raise _Done(DOWNLOAD)
        return 0
    report.check(
        DOWNLOAD,
        "ok",
        f"download job {job.job_id} landed {done} track(s)"
        + (f"; {len(refused)} refused and skipped" if refused else ""),
    )
    return done


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
    taken = _resolve(report, cfg, ctx.args.pass_run) if ctx.args.pass_run else None
    try:
        preflight(report, cfg)
    except CratekitError as exc:
        # A REFUSAL HERE NAMES THE WAY BACK (U183): the pass it would continue,
        # or a new one.
        again = _continue_command(taken) if taken else "crate sync land"
        raise tail.with_steps(exc, f"then run it again: {again}") from None
    _vocals(ctx, report, cfg)
    run_id = taken
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
        without = _intake(report, run_id, cfg)
        listed = _missing(report, run_id, without_cancelled=without)
        _download(report, listed, cfg)
        staging = cfg.paths.download_staging.expanduser().absolute()
        tail.run(report, staging, cfg, ["--pass", listed.land_name], listed.land_name)
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
    "GUESS",
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
    "VOCAL_MODEL",
    "VOCALS_UNAVAILABLE",
    "WITHOUT_VOCALS",
    "WITHOUT_VOCALS_GO",
    "WITHOUT_VOCALS_WARNING",
    "build",
    "preflight",
    "sync_land",
]
