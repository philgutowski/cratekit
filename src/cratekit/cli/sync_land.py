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

EVERY QUEUED JOB IS DRIVEN TO SETTLED, HERE. ``job resume`` spawns a detached
worker and returns at once, so a chain built on it would read a job while its
worker was still running. Each job is driven through its own verb's ``--job``
command line, the one ``job resume`` would spawn, in the foreground, and the
pass reads the job's state off the queue once that command has returned.

THE ORDER IS LOAD BEARING AND CANNOT BE SKIPPED. Preflight, the pass, its intake
jobs, the missing list, the download, then the tail in its order, then the
landing. A tail step that does not succeed ends the pass there, so a landing is
never planned over staged files the tail has not run on. The tail is run on the
ABSOLUTE staging path, since a relative root resolves against the working
directory and once planned nothing (R-1013's sitting, U169).

A DOWNLOAD REFUSAL IS RECORDED AND SKIPPED. An item the worker refused for good,
a lossy only track above all, leaves the job failed with every other item
durable. The pass names each refused track and goes on with the ones that
landed. A refusal that waiting mends, a parked provider, or a job still open
ends the pass instead, because the tracks it holds are still coming.

A STALE TAIL JOB IS REPLACED, NEVER RESUMED. A tail job queued over the staging
folder by an earlier pass and never finished was frozen against that folder as
it stood then, and against that build: sitting 47 resumed a queued analysis that
answered ``module-extras-missing`` after the extra was installed. Each tail step
cancels any such job and queues its own.

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
import io
import json
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from cratekit.cli import gates, registry, render
from cratekit.cli.output import Envelope, PendingHumanAction
from cratekit.core import config, jobs, rb_writer
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, rebuilt, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.modules import foreground

if TYPE_CHECKING:  # pragma: no cover - import cycle avoidance for typing only
    from cratekit.cli import Context

_ORIGIN = ("cli.sync_land",)

#: The steps, in the one order a pass runs them. Each is a check key on the
#: envelope, ``sync.land.<step>``.
PREFLIGHT = "preflight"
SYNC = "sync"
INTAKE = "intake"
MISSING = "missing"
DOWNLOAD = "download"
TAG = "tag"
ANALYZE = "analyze"
RESTAMP = "restamp"
NAME = "name"
LAND = "land"
STEPS: tuple[str, ...] = (
    PREFLIGHT, SYNC, INTAKE, MISSING, DOWNLOAD, TAG, ANALYZE, RESTAMP, NAME, LAND,
)

#: The tail, in its order: each step's verb and the words that queue it over a
#: folder. ``name apply`` is the fourth step and is not queued, see :func:`_name`.
TAIL: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (TAG, "tag.folder", ("tag", "folder")),
    (ANALYZE, "analyze.run", ("analyze", "run")),
    (RESTAMP, "analyze.restamp", ("analyze", "restamp")),
)

#: The verbs the pass runs that are not the tail's.
SYNC_VERB = "sync.all"
DOWNLOAD_VERB = "acquire.download"
NAME_VERB = "name.apply"
LAND_VERB = "intake.land"
BACKUP_VERB = "backup.run"

#: ``name apply``'s confirm, which is not explicit and is answered inline by the
#: pass the way a person running the tail answers it.
NAME_GATE = "name.apply.confirm"
NAME_OPTION = "apply"
#: The landing's gate, explicit, answered by a separate recorded act.
LAND_GATE = "intake.land.native"
LAND_OPTION = "apply"
#: The actor the session answers as (CLAUDE.md, 2026-09-29).
SESSION_ACTOR = "session"

#: Why the favourites write half queues nothing in a pass this verb runs: no
#: export is handed to it, so it refuses its own precondition (module docstring).
OUTBOUND_UNASKED = "outbound-export-required"

#: The two reasons a landing stops for a person rather than failing: its gate,
#: and the backup acknowledgment it reads and this verb never mints.
GATE_STOP = "decision-required"
ACK_STOP = "backup-acknowledgment-missing"

#: The one playlist every native landing fills with the rows awaiting analysis
#: (U166), as the shipped taxonomy names INBOX. Spelled here rather than
#: imported, for the lazy imports' reason below; a test holds it to
#: :data:`cratekit.intake.native.ANALYZE` under the declared intake folder.
ANALYZE_PLAYLIST = "INBOX / Analyze"

#: The rekordbox visit an attended session makes once the landing is applied,
#: on Phillip's standard since 2026-10-27, over the one playlist every landing
#: fills (U166), which holds every row still waiting and only those, then the
#: clear that takes the analysed out. NO RELOAD TAGS SINCE U163: a landed row
#: carries its artist, album, genre and year from the commit that made it.
REKORDBOX_STEPS: tuple[str, ...] = (
    f"in rekordbox, select the {ANALYZE_PLAYLIST} playlist, which holds every "
    f"landed row waiting for analysis, and run Analyze Tracks on it: Analysis "
    f"Mode Normal, high precision off, BPM/Grid, Phrase and KEY on",
    "quit rekordbox and confirm rekordbox and rekordboxAgent are both gone "
    "before any other verb runs",
    "then take the analysed rows out of it: crate inbox analyzed",
)

#: A child run's answer: its exit status and its envelope as JSON.
Child = tuple[int, dict[str, Any]]


def dispatch(argv: Sequence[str]) -> Child:
    """Run one verb through the real dispatcher here, and read its envelope.

    The seam the pass's every step goes through, a module attribute so the
    suite can stand in for a step the fixture cannot run. JSON output, so
    standard output is exactly one envelope; the human words a refusal writes
    to standard error are the parent's to render, from the cause.
    """
    from cratekit import cli  # noqa: PLC0415 - the dispatcher imports this module

    out, err = io.StringIO(), io.StringIO()
    code = cli.run(["--output", "json", *argv], stdout=out, stderr=err)
    text = out.getvalue().strip()
    try:
        document = json.loads(text) if text else {}
    except ValueError:
        document = {}
    return code, document if isinstance(document, dict) else {}


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
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=_ORIGIN,
                detail={"kind": type(exc).__name__},
            )
        ) from exc


# ---------------------------------------------------------------------------
# What the pass did, as it did it
# ---------------------------------------------------------------------------


class _Stop(Exception):
    """A step that ended the pass with its own refusal.

    The refusal is held whole, its type with it, so a job the engine parked
    ends this verb blocked and not failed (``cause.rebuilt``).
    """

    def __init__(self, step: str, error: CratekitError, *, continues: bool = True) -> None:
        super().__init__(error.cause.message)
        self.step = step
        self.error = error
        #: Whether continuing the pass can get past this stop once its cause is
        #: mended. A job that ENDED cannot be driven again by the pass, so a
        #: continuation would meet the same refusal every time.
        self.continues = continues

    @classmethod
    def of(cls, step: str, cause: Cause) -> _Stop:
        """A stop whose cause arrived over a child's envelope, with no exception in hand."""
        return cls(step, CratekitError(cause))


class _Choose(Exception):
    """Several earlier passes hold open intake jobs, and which to take is a person's."""

    def __init__(self, runs: Sequence[str]) -> None:
        super().__init__(", ".join(runs))
        self.runs = list(runs)


class _Attend(Exception):
    """A step that stopped for a person: a gate, or the backup acknowledgment."""

    def __init__(self, step: str, argv: Sequence[str], cause: Cause) -> None:
        super().__init__(cause.message)
        self.step = step
        self.argv = list(argv)
        self.cause = cause


class _Done(Exception):
    """The pass ended early with nothing left to do: nothing missing, nothing landed."""

    def __init__(self, step: str) -> None:
        super().__init__(step)
        self.step = step


@dataclasses.dataclass
class _Pass:
    """Every step's check, every child's warning, and the facts a person reads."""

    progress: Callable[[str], None] | None
    checks: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    warnings: list[dict[str, str]] = dataclasses.field(default_factory=list)
    summary: dict[str, Any] = dataclasses.field(
        default_factory=lambda: {
            "pass_run": None,
            "steps": [],
            "commands": [],
            "stopped_at": None,
            "download_refused": [],
            "replaced": [],
        }
    )

    def check(self, step: str, status: str, detail: str, *, remedy: str | None = None) -> None:
        self.checks.append(
            {
                "key": f"sync.land.{step}",
                "title": step,
                "status": status,
                "detail": detail,
                "remedy": remedy,
            }
        )
        if status != "fail" and step not in self.summary["steps"]:
            self.summary["steps"].append(step)

    def say(self, step: str, what: str) -> None:
        if self.progress is not None:
            self.progress(f"sync land, step {STEPS.index(step) + 1} of {len(STEPS)}, {step}: {what}")

    def call(self, step: str, argv: Sequence[str]) -> Child:
        """Run one step's verb, keeping its command and its warnings."""
        self.say(step, "crate " + " ".join(argv))
        self.summary["commands"].append(["crate", *argv])
        code, envelope = dispatch(list(argv))
        for warning in envelope.get("warnings") or ():
            if isinstance(warning, dict) and warning.get("code"):
                self.warnings.append(
                    {
                        "code": str(warning["code"]),
                        "message": f"{step}: {warning.get('message', '')}",
                    }
                )
        return code, envelope

    def data(self) -> dict[str, Any]:
        return {"checks": list(self.checks), "summary": dict(self.summary)}


def _cause_of(step: str, argv: Sequence[str], code: int, envelope: dict[str, Any]) -> Cause:
    """A step's refusal as a cause, its own trail kept and this verb's appended."""
    raw = envelope.get("cause")
    if isinstance(raw, dict):
        try:
            return Cause.from_json(raw).at("sync.land")
        except (KeyError, TypeError, ValueError):
            pass
    return Cause(
        reason="internal-error",
        message=(
            f"crate {' '.join(argv)} exited {code} and gave no envelope this pass "
            f"could read, so the {step} step's answer is unknown"
        ),
        remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
        origin=_ORIGIN,
        detail={"step": step, "exit_code": code},
    )


def _succeeded(code: int, envelope: dict[str, Any]) -> bool:
    return code == int(ExitCode.OK) and envelope.get("outcome") in (
        str(Outcome.OK),
        str(Outcome.NO_OP),
    )


def _required(report: _Pass, step: str, argv: Sequence[str]) -> dict[str, Any]:
    """Run a step whose refusal ends the pass, and return its envelope.

    A STEP'S GATE IS NOT THIS VERB'S GATE. Raised as this verb's own refusal, a
    gate's code would mark this run resumable over a question this verb does
    not declare, so a gate any step stops at ends the pass for a person, naming
    the step's own run and command.
    """
    code, envelope = report.call(step, argv)
    if not _succeeded(code, envelope):
        cause = _cause_of(step, argv, code, envelope)
        if cause.code in gates.GATE_CODES:
            raise _Attend(step, argv, cause)
        raise _Stop.of(step, cause)
    return envelope


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
            + " ".join(_argv_for(job))
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
    envelope = _required(report, SYNC, ["sync", "all"])
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


def _argv_for(job: jobs.Job) -> list[str]:
    from cratekit.cli import jobs as cli_jobs  # noqa: PLC0415 - imports a verb's module

    return cli_jobs.argv_for(job)


def _settle(report: _Pass, step: str, job: jobs.Job) -> jobs.Job:
    """Drive one job through its own ``--job`` command, then read it off the queue.

    A job that ended failed or blocked answers with a refusal, which is the
    job's own; the caller reads the state and decides. What it never does is
    read the command's exit as the job's state, since the queue is the truth.
    """
    if not job.is_open():
        return job
    argv = _argv_for(job)
    code, envelope = report.call(step, argv)
    with jobs.open_store() as store:
        settled = jobs.get(store, job.job_id)
    if settled.is_open() and settled.state is not jobs.JobState.BLOCKED:
        # STILL QUEUED OR RUNNING: the command never drove it, a live driver
        # elsewhere holding it above all. The command's own refusal says why,
        # where the job row, which records no cause yet, says nothing. A gate
        # it stopped at is the command's own, as in ``_required``.
        cause = _cause_of(step, argv, code, envelope)
        if cause.code in gates.GATE_CODES:
            raise _Attend(step, argv, cause)
        raise _Stop.of(step, cause)
    return settled


def _intake(report: _Pass, run_id: str, cfg: config.Config) -> None:
    """Drive every intake job of the pass to settled; any not succeeded ends it."""
    with jobs.open_store() as store:
        found = _pass_jobs(store, run_id, cfg)
    settled = [_settle(report, INTAKE, job) for job in found]
    for job in settled:
        if job.state is not jobs.JobState.SUCCEEDED:
            error = _job_error(job)
            if job.is_open():
                raise _Stop(INTAKE, error)
            # AN INTAKE JOB THAT ENDED is not driven again by a continued pass,
            # so the way on is the job's own retry or a new pass.
            way_on = (
                f"retry the job, then continue the pass: crate job resume {job.job_id}"
                if job.cause is not None and job.cause.retryable
                else "the job cannot succeed on resume; start a new pass with: crate sync land"
            )
            raise _Stop(INTAKE, _with_steps(error, way_on), continues=False)
    report.check(
        INTAKE,
        "ok",
        f"{len(settled)} intake job(s) of run {run_id} succeeded: "
        + ", ".join(job.job_id for job in settled),
    )


def _with_steps(error: CratekitError, *steps: str) -> CratekitError:
    """The refusal with ``steps`` added to its remediation, its type kept."""
    cause = error.cause
    remediation = dataclasses.replace(
        cause.remediation, steps=(*cause.remediation.steps, *steps)
    )
    return rebuilt(error, dataclasses.replace(cause, remediation=remediation))


def _job_error(job: jobs.Job) -> CratekitError:
    """A settled job's own refusal, through the engine's one reading of a state.

    ``raise_for_state`` is what every shell ends on, so a parked job arrives as
    the blocked type and a cancelled one as the cancelled type, and the pass
    ends the way the step would have ended alone.
    """
    try:
        jobs.raise_for_state(job)
    except CratekitError as exc:
        return rebuilt(exc, exc.cause.at("sync.land"))
    return CratekitError(
        Cause(
            reason="internal-error",
            message=f"job {job.job_id} is {job.state} after its drive and records no cause",
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=_ORIGIN,
            detail={"job_id": job.job_id, "state": str(job.state)},
        )
    )


# ---------------------------------------------------------------------------
# Steps 3 and 4: one list, one download
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class _Listed:
    path: Path
    land_name: str


def _missing(report: _Pass, run_id: str) -> _Listed:
    envelope = _required(report, MISSING, ["intake", "missing", "--run", run_id])
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
        envelope = _required(report, DOWNLOAD, ["acquire", "download", str(listed.path)])
        job_id = str((envelope.get("data") or {}).get("job_id") or "")
        if envelope.get("outcome") == str(Outcome.NO_OP) or not job_id:
            report.check(DOWNLOAD, "info", "the list held no track to download")
            raise _Done(DOWNLOAD)
        with jobs.open_store() as store:
            job = jobs.get(store, job_id)
    job = _settle(report, DOWNLOAD, job)
    with jobs.open_store() as store:
        held = jobs.items(store, job.job_id)
    done = [item for item in held if item.state is jobs.ItemState.DONE]
    failed = [item for item in held if item.state is jobs.ItemState.FAILED]
    permanent = [item for item in failed if item.cause is not None and not item.cause.retryable]
    settled_with_refusals = job.state is jobs.JobState.FAILED and len(permanent) == len(failed)
    if job.state is not jobs.JobState.SUCCEEDED and not settled_with_refusals:
        raise _Stop(DOWNLOAD, _job_error(job))
    refused = [
        {
            "item_id": item.item_id,
            "reason": item.cause.reason if item.cause else None,
            "message": item.cause.message if item.cause else None,
        }
        for item in permanent
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


# ---------------------------------------------------------------------------
# Step 5: the tail, in its order, over the absolute staging folder
# ---------------------------------------------------------------------------


def _replace_stale(report: _Pass, step: str, verb: str, folder: Path, cfg: config.Config) -> None:
    """Cancel every open job of this tail step over this folder, so a fresh one runs."""
    key = registry.entry(verb).handler_key
    open_states = [state for state in jobs.JobState if state not in jobs.TERMINAL_STATES]
    with jobs.open_store() as store:
        stale = [
            job
            for job in jobs.list_jobs(store, states=open_states)
            if job.handler_key == key
            and job.library_id == cfg.library.volume_id
            and str((job.payload or {}).get("folder") or "") == str(folder)
        ]
        for job in stale:
            # A LIVE DRIVER IS NOT STALE. Its refusal names the holder, and the
            # pass ends rather than run a second sweep over the same files.
            jobs.assert_free(job.job_id)
            jobs.cancel(store, job.job_id)
            report.summary["replaced"].append({"step": step, "job_id": job.job_id})


def _tail_step(
    report: _Pass, step: str, verb: str, words: Sequence[str], folder: Path, cfg: config.Config
) -> None:
    try:
        _replace_stale(report, step, verb, folder, cfg)
    except CratekitError as exc:
        raise _Stop(step, rebuilt(exc, exc.cause.at("sync.land"))) from exc
    # ``--queue-only`` (U192): run by hand these verbs drive what they queue,
    # and the pass drives it itself below, through the ``--job`` command, so
    # each step reads as two commands and no job is driven twice.
    envelope = _required(report, step, [*words, foreground.QUEUE_ONLY, str(folder)])
    job_id = str((envelope.get("data") or {}).get("job_id") or "")
    if envelope.get("outcome") == str(Outcome.NO_OP) or not job_id:
        # NOTHING TO QUEUE over a folder the download just landed tracks into is
        # not a step done. The tail has not run on those files, so the landing
        # is not planned.
        raise _Stop(
            step,
            refuse(
                "source-missing",
                f"crate {' '.join([*words, str(folder)])} found no audio to queue in "
                f"the staging folder the download landed into, so the tail has not "
                f"run and the landing is not planned",
                steps=(f"check what is in {folder}, then continue the pass",),
                origin=_ORIGIN,
                detail={"step": step, "folder": str(folder)},
            ),
        )
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
    job = _settle(report, step, job)
    if job.state is not jobs.JobState.SUCCEEDED:
        raise _Stop(step, _job_error(job))
    report.check(step, "ok", f"crate {' '.join(words)} job {job.job_id} succeeded over {folder}")


def _name(report: _Pass, folder: Path) -> None:
    """``name apply`` over the ABSOLUTE staging folder, its confirm answered inline.

    The confirm is not explicit, so answering it on the command line is the act
    a person running the tail makes; the plan it answers is the verb's own.
    """
    argv = ["-d", f"{NAME_GATE}={NAME_OPTION}", "name", "apply", "--root", str(folder)]
    envelope = _required(report, NAME, argv)
    totals = (envelope.get("data") or {}).get("totals") or {}
    report.check(NAME, "ok", f"name apply ran over {folder}: {json.dumps(totals, sort_keys=True)}")


# ---------------------------------------------------------------------------
# Step 6: the landing, planned and stopped at its gate
# ---------------------------------------------------------------------------


def _land(report: _Pass, folder: Path, land_name: str) -> None:
    """Plan the landing through ``intake land`` itself, which stops for a person.

    The verb reads the backup acknowledgment and asks its explicit gate on its
    own run, so the two ways it stops are both a person's to answer. Returns
    only when it planned nothing, which on the native medium is an empty folder.
    """
    argv = ["intake", "land", str(folder), "--pass", land_name]
    code, envelope = report.call(LAND, argv)
    if _succeeded(code, envelope):
        report.check(LAND, "info", "intake land planned nothing to land")
        raise _Done(LAND)
    cause = _cause_of(LAND, argv, code, envelope)
    if cause.reason == ACK_STOP or cause.code in gates.GATE_CODES:
        raise _Attend(LAND, argv, cause)
    raise _Stop.of(LAND, cause)


def _attended(ctx: Context, report: _Pass, stop: _Attend) -> Envelope:
    """The PENDING envelope a pass ends on when a step waits for a person.

    It names what the person does, as commands, in order, and nothing is
    answered here: the gate's run is the step's own, and the acknowledgment is
    minted by the session through its own verb.
    """
    command = " ".join(stop.argv)
    resume = report.summary.get("pass_run")
    if stop.step == LAND:
        after = REKORDBOX_STEPS
    elif resume:
        after = (f"then continue the pass: crate sync land --pass-run {resume}",)
    else:
        after = ("then run the pass again: crate sync land",)
    detail = stop.cause.detail or {}
    if stop.cause.reason == GATE_STOP:
        run_id = str(detail.get("run_id") or "")
        gate = str(detail.get("gate") or "")
        option = LAND_OPTION if gate == LAND_GATE else "OPTION"
        steps = (
            f"read the plan, then answer the gate as the session: crate run decide "
            f"{run_id} {gate} {option} --actor {SESSION_ACTOR}",
            f"apply it: crate --run {run_id} {command}",
            *after,
        )
        report.summary["gate_run"] = run_id
        report.summary["stopped_at"] = gate
        report.check(stop.step, "info", f"crate {command} waits on {gate} under run {run_id}")
        summary = f"the pass waits on {gate} under run {run_id}, at its {stop.step} step"
        kind = "external_step"
    elif stop.cause.reason != ACK_STOP:
        # A STALE ANSWER, or any other gate code: the step's own run holds the
        # question, and the step's own remediation says how it is answered again.
        remedy = stop.cause.remediation.remedy
        words = render.remedy_text(remedy) if remedy is not None else None
        steps = (
            *stop.cause.remediation.steps,
            *((words,) if words else ()),
            f"then run the step again: crate {command}",
            *after,
        )
        report.summary["stopped_at"] = stop.cause.reason
        report.check(stop.step, "info", f"crate {command} stopped: {stop.cause.message}")
        summary = f"the pass stopped at its {stop.step} step: {stop.cause.message}"
        kind = "external_step"
    else:
        remedy = stop.cause.remediation.remedy
        words = render.remedy_text(remedy) if remedy is not None else None
        steps = (
            *stop.cause.remediation.steps,
            *((words,) if words else ()),
            f"then plan the landing again: crate {command}",
            "it stops at its own gate: answer it as the session with crate run "
            "decide, then apply it with --run, as its output names",
            *after,
        )
        report.summary["stopped_at"] = stop.cause.reason
        report.check(
            stop.step, "info", f"the landing needs the backup acknowledgment: {stop.cause.message}"
        )
        summary = (
            "the pass waits on the backup acknowledgment, which the landing reads "
            "and this verb never mints"
        )
        kind = "backup_ack"
    if stop.step == LAND:
        summary = "the pass is downloaded, tagged, analysed and named; " + summary
    report.summary["attended"] = list(steps)
    pending = PendingHumanAction(
        kind=kind,
        id=f"sync-land-{report.summary['pass_run'] or ctx.run.run_id}",
        summary=summary,
        verify_verb=LAND_VERB if stop.step == LAND else ctx.entry.name,
        steps=steps,
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
    report = _Pass(progress=ctx.progress)
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
        report.summary["staging"] = str(staging)
        for step, verb, words in TAIL:
            _tail_step(report, step, verb, words, staging, cfg)
        _name(report, staging)
        _land(report, staging, listed.land_name)
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
    "LAND_GATE",
    "REKORDBOX_STEPS",
    "STEPS",
    "TAIL",
    "build",
    "dispatch",
    "sync_land",
]
