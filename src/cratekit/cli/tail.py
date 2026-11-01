"""The tail and the landing: one chain, run by every verb that lands a download (U190).

U152 built it inside ``crate sync land``. U190 lifted it out, whole, so that
``crate label sync --go`` runs the same chain after its own download rather
than printing five commands to type: the attended Defected label sync of
2026-10-31 downloaded ten tracks and then asked for ``tag folder``, ``analyze
run``, ``analyze restamp``, ``name apply`` and ``intake land`` by hand. Two
verbs, one chain, so every question the tail answers is answered the same way
by both, by construction rather than by a copy kept in step.

A CHAIN OF THE VERBS A PERSON WOULD TYPE, NOT A SECOND IMPLEMENTATION OF THEM.
Each step is the existing verb run through the real dispatcher in this process,
under its own run, with its own gates and its own refusals, so nothing a step
decides is decided again here. That is why this module is ranked CLI: the
dispatcher is the CLI layer's, and only a module of that layer may reach it.

EVERY QUEUED JOB IS DRIVEN TO SETTLED, HERE. ``job resume`` spawns a detached
worker and returns at once, so a chain built on it would read a job while its
worker was still running. Each job is driven through its own verb's ``--job``
command line, the one ``job resume`` would spawn, in the foreground, and the
chain reads the job's state off the queue once that command has returned.

THE ORDER IS LOAD BEARING AND CANNOT BE SKIPPED. ``tag folder``, ``analyze
run``, ``analyze restamp``, ``name apply``, then the landing. A tail step that
does not succeed ends the chain there, so a landing is never planned over
staged files the tail has not run on. The tail is run on the ABSOLUTE staging
path, since a relative root resolves against the working directory and once
planned nothing (R-1013's sitting, U169).

A STALE TAIL JOB IS REPLACED, NEVER RESUMED. A tail job queued over the staging
folder earlier and never finished was frozen against that folder as it stood
then, and against that build: sitting 47 resumed a queued analysis that
answered ``module-extras-missing`` after the extra was installed. Each tail step
cancels any such job and queues its own.

``name apply``'s CONFIRM IS ANSWERED INLINE, by one argument list. It is not
explicit, so answering it on the command line is the act a person running the
tail makes; the plan it answers is the verb's own.

A VERB MAY REHEARSE BETWEEN THE TAIL AND THE LANDING (U179). ``crate sync
bandcamp`` runs :func:`through_name`, then :func:`rehearse`, ``intake land
--rehearse`` with the arguments the landing then takes, so the live gate names
the rehearsal; ``sync land`` and ``label sync --go`` run :func:`run`, which
does not.

IT STOPS WHERE A PERSON MUST ACT, AND SAYS WHAT THEY DO. The landing is planned
by ``intake land`` itself, which reads the backup acknowledgment (this chain
never mints one) and stops at its explicit gate on its own run. The verb that
ran the chain then ends PENDING, naming that run, the two commands that answer
and apply it as the session, and the rekordbox visit that follows. Nothing here
starts a backup, opens rekordbox or writes a beat grid.
"""

from __future__ import annotations

import dataclasses
import io
import json
import shlex
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Callable

from cratekit.cli import gates, registry, render
from cratekit.core import config, jobs
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, rebuilt, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.modules import foreground

#: The tail's steps and the landing, in their one order. Each is a check key on
#: the envelope of the verb that runs the chain, ``<namespace>.<step>``.
TAG = "tag"
ANALYZE = "analyze"
RESTAMP = "restamp"
NAME = "name"
LAND = "land"
STEPS: tuple[str, ...] = (TAG, ANALYZE, RESTAMP, NAME, LAND)

#: The rehearsal a verb may run between the tail and the landing (U179), which
#: ``crate sync bandcamp`` does and the two older verbs do not, and the flag of
#: ``intake land`` that asks for it.
REHEARSE = "rehearse"
REHEARSE_FLAG = "--rehearse"

#: The tail, in its order: each step's verb and the words that queue it over a
#: folder. ``name apply`` is the fourth step and is not queued, see :func:`name`.
TAIL: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (TAG, "tag.folder", ("tag", "folder")),
    (ANALYZE, "analyze.run", ("analyze", "run")),
    (RESTAMP, "analyze.restamp", ("analyze", "restamp")),
)

NAME_VERB = "name.apply"
LAND_VERB = "intake.land"

#: ``name apply``'s confirm, which is not explicit and is answered inline by the
#: chain the way a person running the tail answers it.
NAME_GATE = "name.apply.confirm"
NAME_OPTION = "apply"
#: The landing's gate, explicit, answered by a separate recorded act.
LAND_GATE = "intake.land.native"
LAND_OPTION = "apply"
#: The actor the session answers as (CLAUDE.md, 2026-09-29).
SESSION_ACTOR = "session"

#: The two reasons a landing stops for a person rather than failing: its gate,
#: and the backup acknowledgment it reads and this chain never mints.
GATE_STOP = "decision-required"
ACK_STOP = "backup-acknowledgment-missing"

#: The one playlist every native landing fills with the rows awaiting analysis
#: (U166), as the shipped taxonomy names INBOX. Spelled here rather than
#: imported, since this module imports no feature module at its top; a test
#: holds it to :data:`cratekit.intake.native.ANALYZE` under the declared intake
#: folder.
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

    The seam every step of every chain goes through, a module attribute so the
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


def load_config(origin: tuple[str, ...]) -> config.Config:
    """The configuration, or the refusal a person can act on."""
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=origin,
                detail={"kind": type(exc).__name__},
            )
        ) from exc


# ---------------------------------------------------------------------------
# What the chain did, as it did it
# ---------------------------------------------------------------------------


class Stop(Exception):
    """A step that ended the chain with its own refusal.

    The refusal is held whole, its type with it, so a job the engine parked
    ends the verb blocked and not failed (``cause.rebuilt``).
    """

    def __init__(self, step: str, error: CratekitError, *, continues: bool = True) -> None:
        super().__init__(error.cause.message)
        self.step = step
        self.error = error
        #: Whether continuing can get past this stop once its cause is mended.
        #: A job that ENDED cannot be driven again by a continuation, so it
        #: would meet the same refusal every time.
        self.continues = continues

    @classmethod
    def of(cls, step: str, cause: Cause) -> Stop:
        """A stop whose cause arrived over a child's envelope, with no exception in hand."""
        return cls(step, CratekitError(cause))


class Attend(Exception):
    """A step that stopped for a person: a gate, or the backup acknowledgment."""

    def __init__(self, step: str, argv: Sequence[str], cause: Cause) -> None:
        super().__init__(cause.message)
        self.step = step
        self.argv = list(argv)
        self.cause = cause


class Done(Exception):
    """The chain ended early with nothing left to do."""

    def __init__(self, step: str) -> None:
        super().__init__(step)
        self.step = step


@dataclasses.dataclass
class Chain:
    """Every step's check, every child's warning, and the facts a person reads.

    ``namespace`` keys every check and is the boundary each child's cause has
    appended to its trail, ``title`` names the verb in its progress lines; ``steps`` is the whole order the verb runs, so its
    progress lines count the verb's own steps and not only the tail's.
    """

    progress: Callable[[str], None] | None
    namespace: str
    title: str
    steps: tuple[str, ...]
    origin: tuple[str, ...]
    #: What a person does once a step's cause is mended, in the verb's words.
    again: str
    checks: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    warnings: list[dict[str, str]] = dataclasses.field(default_factory=list)
    summary: dict[str, Any] = dataclasses.field(
        default_factory=lambda: {
            "steps": [],
            "commands": [],
            "stopped_at": None,
            "replaced": [],
        }
    )

    def check(self, step: str, status: str, detail: str, *, remedy: str | None = None) -> None:
        self.checks.append(
            {
                "key": f"{self.namespace}.{step}",
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
            self.progress(
                f"{self.title}, step {self.steps.index(step) + 1} of {len(self.steps)}, "
                f"{step}: {what}"
            )

    def call(self, step: str, argv: Sequence[str]) -> Child:
        """Run one step's verb, keeping its command and its warnings.

        Through the module's :func:`dispatch`, read at call time, so the one
        seam stands in for every chain.
        """
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


def cause_of(
    chain: Chain, step: str, argv: Sequence[str], code: int, envelope: dict[str, Any]
) -> Cause:
    """A step's refusal as a cause, its own trail kept and the chain's appended."""
    raw = envelope.get("cause")
    if isinstance(raw, dict):
        try:
            return Cause.from_json(raw).at(chain.namespace)
        except (KeyError, TypeError, ValueError):
            pass
    return Cause(
        reason="internal-error",
        message=(
            f"crate {' '.join(argv)} exited {code} and gave no envelope this "
            f"{chain.title} could read, so the {step} step's answer is unknown"
        ),
        remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
        origin=chain.origin,
        detail={"step": step, "exit_code": code},
    )


def succeeded(code: int, envelope: dict[str, Any]) -> bool:
    return code == int(ExitCode.OK) and envelope.get("outcome") in (
        str(Outcome.OK),
        str(Outcome.NO_OP),
    )


def required(chain: Chain, step: str, argv: Sequence[str]) -> dict[str, Any]:
    """Run a step whose refusal ends the chain, and return its envelope.

    A STEP'S GATE IS NOT THE VERB'S GATE. Raised as the verb's own refusal, a
    gate's code would mark its run resumable over a question it does not
    declare, so a gate any step stops at ends the chain for a person, naming
    the step's own run and command.
    """
    code, envelope = chain.call(step, argv)
    if not succeeded(code, envelope):
        cause = cause_of(chain, step, argv, code, envelope)
        if cause.code in gates.GATE_CODES:
            raise Attend(step, argv, cause)
        raise Stop.of(step, cause)
    return envelope


def argv_for(job: jobs.Job) -> list[str]:
    from cratekit.cli import jobs as cli_jobs  # noqa: PLC0415 - imports a verb's module

    return cli_jobs.argv_for(job)


def settle(chain: Chain, step: str, job: jobs.Job) -> jobs.Job:
    """Drive one job through its own ``--job`` command, then read it off the queue.

    A job that ended failed or blocked answers with a refusal, which is the
    job's own; the caller reads the state and decides. What it never does is
    read the command's exit as the job's state, since the queue is the truth.
    """
    if not job.is_open():
        return job
    argv = argv_for(job)
    code, envelope = chain.call(step, argv)
    with jobs.open_store() as store:
        settled = jobs.get(store, job.job_id)
    if settled.is_open() and settled.state is not jobs.JobState.BLOCKED:
        # STILL QUEUED OR RUNNING: the command never drove it, a live driver
        # elsewhere holding it above all. The command's own refusal says why,
        # where the job row, which records no cause yet, says nothing. A gate
        # it stopped at is the command's own, as in ``required``.
        cause = cause_of(chain, step, argv, code, envelope)
        if cause.code in gates.GATE_CODES:
            raise Attend(step, argv, cause)
        raise Stop.of(step, cause)
    return settled


def with_steps(error: CratekitError, *steps: str) -> CratekitError:
    """The refusal with ``steps`` added to its remediation, its type kept."""
    cause = error.cause
    remediation = dataclasses.replace(
        cause.remediation, steps=(*cause.remediation.steps, *steps)
    )
    return rebuilt(error, dataclasses.replace(cause, remediation=remediation))


def job_error(chain: Chain, job: jobs.Job) -> CratekitError:
    """A settled job's own refusal, through the engine's one reading of a state.

    ``raise_for_state`` is what every shell ends on, so a parked job arrives as
    the blocked type and a cancelled one as the cancelled type, and the chain
    ends the way the step would have ended alone.
    """
    try:
        jobs.raise_for_state(job)
    except CratekitError as exc:
        return rebuilt(exc, exc.cause.at(chain.namespace))
    return CratekitError(
        Cause(
            reason="internal-error",
            message=f"job {job.job_id} is {job.state} after its drive and records no cause",
            remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
            origin=chain.origin,
            detail={"job_id": job.job_id, "state": str(job.state)},
        )
    )


# ---------------------------------------------------------------------------
# The tail, in its order, over the absolute staging folder
# ---------------------------------------------------------------------------


def replace_stale(chain: Chain, step: str, verb: str, folder: Path, cfg: config.Config) -> None:
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
            # chain ends rather than run a second sweep over the same files.
            jobs.assert_free(job.job_id)
            jobs.cancel(store, job.job_id)
            chain.summary["replaced"].append({"step": step, "job_id": job.job_id})


def tail_step(
    chain: Chain, step: str, verb: str, words: Sequence[str], folder: Path, cfg: config.Config
) -> None:
    try:
        replace_stale(chain, step, verb, folder, cfg)
    except CratekitError as exc:
        raise Stop(step, rebuilt(exc, exc.cause.at(chain.namespace))) from exc
    # ``--queue-only`` (U192): run by hand these verbs drive what they queue,
    # and the chain drives it itself below, through the ``--job`` command, so
    # each step reads as two commands and no job is driven twice.
    envelope = required(chain, step, [*words, foreground.QUEUE_ONLY, str(folder)])
    job_id = str((envelope.get("data") or {}).get("job_id") or "")
    if envelope.get("outcome") == str(Outcome.NO_OP) or not job_id:
        # NOTHING TO QUEUE over a folder the download just landed tracks into is
        # not a step done. The tail has not run on those files, so the landing
        # is not planned.
        raise Stop(
            step,
            refuse(
                "source-missing",
                f"crate {' '.join([*words, str(folder)])} found no audio to queue in "
                f"the staging folder the download landed into, so the tail has not "
                f"run and the landing is not planned",
                steps=(f"check what is in {folder}, then {chain.again}",),
                origin=chain.origin,
                detail={"step": step, "folder": str(folder)},
            ),
        )
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
    job = settle(chain, step, job)
    if job.state is not jobs.JobState.SUCCEEDED:
        raise Stop(step, job_error(chain, job))
    chain.check(step, "ok", f"crate {' '.join(words)} job {job.job_id} succeeded over {folder}")


def name_argv(folder: Path) -> list[str]:
    """``name apply`` over ``folder`` with its confirm answered, the one rule both verbs use."""
    return ["-d", f"{NAME_GATE}={NAME_OPTION}", "name", "apply", "--root", str(folder)]


def name(chain: Chain, folder: Path) -> None:
    """``name apply`` over the ABSOLUTE staging folder, its confirm answered inline.

    The confirm is not explicit, so answering it on the command line is the act
    a person running the tail makes; the plan it answers is the verb's own.
    """
    envelope = required(chain, NAME, name_argv(folder))
    totals = (envelope.get("data") or {}).get("totals") or {}
    chain.check(NAME, "ok", f"name apply ran over {folder}: {json.dumps(totals, sort_keys=True)}")


def land(chain: Chain, folder: Path, landing: Sequence[str] = ()) -> None:
    """Plan the landing through ``intake land`` itself, which stops for a person.

    The verb reads the backup acknowledgment and asks its explicit gate on its
    own run, so the two ways it stops are both a person's to answer. Returns
    only by :class:`Done`, when it planned nothing, which on the native medium
    is an empty folder. ``landing`` is the arguments after the folder: the
    pass, and a manifest when the verb that downloaded wrote one.
    """
    argv = ["intake", "land", str(folder), *landing]
    code, envelope = chain.call(LAND, argv)
    if succeeded(code, envelope):
        chain.check(LAND, "info", "intake land planned nothing to land")
        raise Done(LAND)
    cause = cause_of(chain, LAND, argv, code, envelope)
    if cause.reason == ACK_STOP or cause.code in gates.GATE_CODES:
        raise Attend(LAND, argv, cause)
    raise Stop.of(LAND, cause)


def rehearse(chain: Chain, folder: Path, landing: Sequence[str] = ()) -> None:
    """Rehearse the landing on a copy through ``intake land --rehearse`` itself (U162, U179).

    The same folder and the same arguments the landing is then planned with,
    so the rehearsal's record is the one the live gate names, equal or not. A
    rehearsal asks no gate and writes nothing live, but it reads the backup
    acknowledgment the way the landing does, so a missing one stops for a
    person here as it would there. Any other refusal ends the chain before the
    landing is planned: a landing whose rehearsal failed is not one to ask.
    Returns once the rehearsal applied on its copy, or by :class:`Done` when it
    had nothing to rehearse.
    """
    argv = ["intake", "land", str(folder), *landing, REHEARSE_FLAG]
    code, envelope = chain.call(REHEARSE, argv)
    if not succeeded(code, envelope):
        cause = cause_of(chain, REHEARSE, argv, code, envelope)
        if cause.reason == ACK_STOP or cause.code in gates.GATE_CODES:
            raise Attend(REHEARSE, argv, cause)
        raise Stop.of(REHEARSE, cause)
    data = envelope.get("data") or {}
    digest = str(data.get("digest") or "") if isinstance(data, dict) else ""
    if envelope.get("outcome") == str(Outcome.NO_OP):
        chain.check(REHEARSE, "info", "intake land --rehearse found nothing to land")
        raise Done(REHEARSE)
    chain.summary["rehearsal"] = digest or None
    chain.check(
        REHEARSE,
        "ok",
        f"the landing was rehearsed on a copy and read back, plan digest {digest or 'unnamed'}",
    )


def through_name(chain: Chain, folder: Path, cfg: config.Config) -> Path:
    """The tail in its order over ``folder``, ending with ``name apply``; the absolute folder.

    Every step either succeeds or ends the chain, so a caller that goes on to
    land knows the tail ran on every file. ``folder`` must be absolute, and is
    made so here rather than trusted.
    """
    folder = folder.expanduser().absolute()
    chain.summary["staging"] = str(folder)
    for step, verb, words in TAIL:
        tail_step(chain, step, verb, words, folder, cfg)
    name(chain, folder)
    return folder


def run(chain: Chain, folder: Path, cfg: config.Config, landing: Sequence[str]) -> None:
    """The tail in its order over ``folder``, then the landing planned and stopped.

    Never returns: it ends in :class:`Attend` at the landing's gate or the
    acknowledgment, :class:`Done` when the landing planned nothing, or
    :class:`Stop` at the first step that did not succeed. ``folder`` must be
    absolute, and is made so here rather than trusted.
    """
    folder = through_name(chain, folder, cfg)
    land(chain, folder, landing)


# ---------------------------------------------------------------------------
# The stop for a person, said once for every chain
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True)
class Attended:
    """What a person does at a stop, and the words that say where the chain is."""

    steps: tuple[str, ...]
    summary: str
    kind: str


def attended(chain: Chain, stop: Attend, *, after: Sequence[str]) -> Attended:
    """The steps a person takes at ``stop``, in order, with ``after`` following them.

    Nothing is answered here: the gate's run is the step's own, and the
    acknowledgment is minted by the session through its own verb. Records the
    stop on the chain's summary and its check.
    """
    # SHELL QUOTED (U179), since a batch folder and a batch name hold spaces,
    # ``Bandcamp 2026-11-01`` and ``2026-11-01 Bandcamp PULS``, and a command a
    # person or the session pastes must be the argument list the step was run
    # with. A command of plain words reads exactly as it did.
    command = shlex.join(stop.argv)
    detail = stop.cause.detail or {}
    if stop.cause.reason == GATE_STOP:
        run_id = str(detail.get("run_id") or "")
        gate = str(detail.get("gate") or "")
        option = LAND_OPTION if gate == LAND_GATE else "OPTION"
        steps: tuple[str, ...] = (
            f"read the plan, then answer the gate as the session: crate run decide "
            f"{run_id} {gate} {option} --actor {SESSION_ACTOR}",
            f"apply it: crate --run {run_id} {command}",
            *after,
        )
        chain.summary["gate_run"] = run_id
        chain.summary["stopped_at"] = gate
        chain.check(stop.step, "info", f"crate {command} waits on {gate} under run {run_id}")
        summary = f"waits on {gate} under run {run_id}, at its {stop.step} step"
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
        chain.summary["stopped_at"] = stop.cause.reason
        chain.check(stop.step, "info", f"crate {command} stopped: {stop.cause.message}")
        summary = f"stopped at its {stop.step} step: {stop.cause.message}"
        kind = "external_step"
    else:
        remedy = stop.cause.remediation.remedy
        words = render.remedy_text(remedy) if remedy is not None else None
        # A REHEARSAL READS THE ACKNOWLEDGMENT TOO (U162), and asks no gate, so
        # a stop there names the rehearsal again and then the landing it is for.
        again = (
            (
                f"then rehearse the landing again: crate {command}",
                "then plan the landing: crate "
                + shlex.join(word for word in stop.argv if word != REHEARSE_FLAG),
            )
            if stop.step == REHEARSE
            else (f"then plan the landing again: crate {command}",)
        )
        steps = (
            *stop.cause.remediation.steps,
            *((words,) if words else ()),
            *again,
            "it stops at its own gate: answer it as the session with crate run "
            "decide, then apply it with --run, as its output names",
            *after,
        )
        chain.summary["stopped_at"] = stop.cause.reason
        chain.check(
            stop.step, "info", f"the landing needs the backup acknowledgment: {stop.cause.message}"
        )
        summary = (
            "waits on the backup acknowledgment, which the landing reads and "
            "this verb never mints"
        )
        kind = "backup_ack"
    chain.summary["attended"] = list(steps)
    return Attended(steps=steps, summary=summary, kind=kind)


__all__ = [
    "ACK_STOP",
    "ANALYZE",
    "ANALYZE_PLAYLIST",
    "GATE_STOP",
    "LAND",
    "LAND_GATE",
    "LAND_OPTION",
    "LAND_VERB",
    "NAME",
    "NAME_GATE",
    "NAME_OPTION",
    "NAME_VERB",
    "REKORDBOX_STEPS",
    "REHEARSE",
    "REHEARSE_FLAG",
    "RESTAMP",
    "SESSION_ACTOR",
    "STEPS",
    "TAG",
    "TAIL",
    "Attend",
    "Attended",
    "Chain",
    "Child",
    "Done",
    "Stop",
    "argv_for",
    "attended",
    "cause_of",
    "dispatch",
    "job_error",
    "land",
    "load_config",
    "name",
    "name_argv",
    "rehearse",
    "replace_stale",
    "required",
    "run",
    "settle",
    "succeeded",
    "tail_step",
    "through_name",
    "with_steps",
]
