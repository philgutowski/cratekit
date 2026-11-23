"""The tail and the landing: one chain, run by every verb that lands a download (U190).

Each step is the existing verb run through the real dispatcher in this
process, under its own run and gates, so nothing a step decides is decided
again here, and every queued job is driven to settled through its ``--job``
command. The order is fixed: ``tag folder``, ``tag guess`` (U172), ``analyze
run`` and the vocal rescore (U181), ``analyze restamp``, ``name apply``, then
the landing, over the absolute staging path (U169). A step that does not
succeed ends the chain, so a landing is never planned over files the tail
skipped, and a stale tail job is replaced, never resumed. The chain stops
where a person must act, at the landing's gate or the backup acknowledgment,
which it never mints. Nothing here starts a backup, opens rekordbox or writes
a beat grid.
"""

from __future__ import annotations

import dataclasses
import io
import json
import shlex
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Callable

from cratekit.cli import gates, registry, render
from cratekit.cli.output import load_config
from cratekit.core import config, drift, jobs, profiles, tags
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, rebuilt, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.modules import foreground

#: The tail's steps and the landing, in their one order. Each is a check key on
#: the envelope of the verb that runs the chain, ``<namespace>.<step>``.
TAG = "tag"
GUESS = "guess"
ANALYZE = "analyze"
RESTAMP = "restamp"
NAME = "name"
LAND = "land"
STEPS: tuple[str, ...] = (TAG, GUESS, ANALYZE, RESTAMP, NAME, LAND)

#: The rehearsal a verb may run between the tail and the landing (U179), and
#: the ``intake land`` flag that asks for it.
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

#: The download verb whose jobs record which pass downloaded a recording (U212).
DOWNLOAD_VERB = "acquire.download"

#: What ``name apply`` answers when part of its plan did not happen.
RENAME_INCOMPLETE = "rename-incomplete"
LAND_VERB = "intake.land"

#: ``analyze restamp``'s flag naming this pass's ``analyze run`` job, the no op
#: state it answers when that run scored every staged file, and the progress
#: key counting what it left out (U344). Spelled here, since this module
#: imports no feature module at its top; a test holds them to the verb's own.
SCORED_BY_FLAG = "--scored-by"
ALL_SCORED = "scored-by-run"
LEFT_OUT = "left_out"

#: The genre guess run right after ``tag folder`` (U172), not queued, and the
#: flag naming the pass whose playlists vote. Spelled here, not imported, as
#: the vocals verb below is; a test holds the words to the registry's.
GUESS_VERB = "tag.guess"
GUESS_WORDS: tuple[str, ...] = ("tag", "guess")
PASS_FLAG = "--pass"

#: The row the vocal rescore reports under, ``<namespace>.rescore`` (U181).
RESCORE = "rescore"

#: The vocal rescore after ``analyze run`` (U181), over staged files the run
#: already measured and no voxlevel. Spelled here, since this module imports no feature
#: module at its top; a test holds the flag to the verb's own.
VOCALS_VERB = "analyze.vocals"
VOCALS_WORDS: tuple[str, ...] = ("analyze", "vocals")
VOCALS_UNSCORED = "--unscored"

#: ``name apply``'s confirm, not explicit, so the chain answers it inline.
NAME_GATE = "name.apply.confirm"
NAME_OPTION = "apply"
#: The landing's gate, explicit, answered by a separate recorded act.
LAND_GATE = "intake.land.native"
LAND_OPTION = "apply"
#: The actor the session answers as (CLAUDE.md, 2026-09-29).
SESSION_ACTOR = "session"

#: The two reasons a landing stops for a person: its gate, and the backup
#: acknowledgment this chain never mints.
GATE_STOP = "decision-required"
ACK_STOP = "backup-acknowledgment-missing"

#: The playlist every native landing fills with rows awaiting analysis (U166).
#: Spelled here, not imported; a test holds it to
#: :data:`cratekit.intake.native.ANALYZE`.
ANALYZE_PLAYLIST = "INBOX / Analyze"

#: The visit's short path with Auto Analysis on (U319). Spelled here, not
#: imported; a test holds it to :data:`cratekit.intake.land_cli.AUTO_ANALYSIS_STEP`.
AUTO_ANALYSIS_STEP = (
    "or, with Auto Analysis on, open rekordbox with its window in front and press OK "
    "on its Auto Analysis dialog only when it shows every one of those Normal "
    "settings with Vocal and CUE off and no field set otherwise, else Cancel it and "
    "select as above; Auto Analysis runs on its preference's own mode, so the rows "
    f"carrying the dyn My Tag, if any, still take Analyze Tracks with "
    f"{drift.DYNAMIC_SETTINGS}, and then, when they did and a row lacks the tag, one "
    f"row without it takes Analyze Tracks with {drift.NORMAL_SETTINGS} again, so the "
    f"visit ends on Normal"
)

#: The rekordbox visit an attended session makes once the landing is applied,
#: over the playlist every landing fills (U166), then the clear. The ``dyn``
#: rows take Dynamic first and the rest Normal last (U157), so the mode the
#: next launch's Auto Analysis dialog reads is Normal (U954), or Auto Analysis
#: answers both (U319); no reload tags is needed (U163).
REKORDBOX_STEPS: tuple[str, ...] = (
    f"in rekordbox, select the {ANALYZE_PLAYLIST} playlist, which holds every "
    f"landed row waiting for analysis, and run Analyze Tracks first on its rows "
    f"carrying the dyn My Tag, if any: {drift.DYNAMIC_SETTINGS} as the Normal "
    f"run's; then last on its rows without the dyn My Tag, if any: "
    f"{drift.NORMAL_SETTINGS}, so the mode the next launch reads is Normal unless "
    f"every row carries the tag; {AUTO_ANALYSIS_STEP}",
    "quit rekordbox and confirm rekordbox and rekordboxAgent are both gone "
    "before any other verb runs",
    "then take the analysed rows out of it: crate inbox analyzed",
)

#: A child run's answer: its exit status and its envelope as JSON.
Child = tuple[int, dict[str, Any]]


def dispatch(argv: Sequence[str]) -> Child:
    """Run one verb through the real dispatcher here, and read its envelope.

    The one seam every step goes through, a module attribute so the suite can
    stand in for a step. JSON output, so standard output is one envelope.
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


def summary_of(envelope: dict[str, Any]) -> dict[str, Any]:
    """The summary a chain's envelope carries, or an empty one."""
    data = envelope.get("data") or {}
    summary = data.get("summary") if isinstance(data, dict) else None
    return summary if isinstance(summary, dict) else {}


def changed_said(changed: CratekitError) -> str:
    """What made the folder unsafe to keep, said as a clause."""
    detail = changed.cause.detail or {}
    if "arrived" not in detail:
        return f"whether anything arrived while the tail ran cannot be read: {changed.cause.message}"
    parts = []
    if detail.get("arrived"):
        parts.append(f"download job(s) {', '.join(map(str, detail['arrived']))} finished track(s) into it")
    if detail.get("before") != detail.get("after"):
        parts.append(
            f"it held {detail.get('before')} file(s) a landing would take as the tail started "
            f"and {detail.get('after')} after"
        )
    return "the staging folder changed while the tail ran: " + "; ".join(parts)


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
        #: Whether continuing can get past this stop once its cause is mended;
        #: a job that ended cannot be driven again.
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

    ``namespace`` keys every check and is appended to each child's cause
    trail; ``title`` names the verb in progress lines; ``steps`` is the verb's
    whole order, which its progress lines count.
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
    #: Each step's last ``--job`` envelope, by step (U284).
    settled: dict[str, dict[str, Any]] = dataclasses.field(default_factory=dict)
    #: The ``analyze run`` job of this pass once it succeeded, whose scored
    #: files the restamp leaves out (U344).
    analyzed: str | None = None
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

    def note(self, name: str, status: str, detail: str) -> None:
        """A row of its own, ``<namespace>.<name>``, that is not a step's (U181).

        For what a step does beside its verb, such as the vocal rescore.
        """
        self.checks.append(
            {
                "key": f"{self.namespace}.{name}",
                "title": name,
                "status": status,
                "detail": detail,
                "remedy": None,
            }
        )

    def say(self, step: str, what: str) -> None:
        if self.progress is not None:
            self.progress(
                f"{self.title}, step {self.steps.index(step) + 1} of {len(self.steps)}, "
                f"{step}: {what}"
            )

    def call(self, step: str, argv: Sequence[str]) -> Child:
        """Run one step's verb through :func:`dispatch`, keeping its command and warnings."""
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

    A step's gate is not the verb's, so it ends the chain for a person, naming
    the step's own run, rather than marking the verb's run resumable.
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

    The caller reads the state and decides; the command's exit is never read
    as the job's state, since the queue is the truth.
    """
    if not job.is_open():
        return job
    argv = argv_for(job)
    code, envelope = chain.call(step, argv)
    chain.settled[step] = envelope
    with jobs.open_store() as store:
        settled = jobs.get(store, job.job_id)
    if settled.is_open() and settled.state is not jobs.JobState.BLOCKED:
        # Still open: the command never drove it, so its own refusal says why.
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

    Through ``raise_for_state``, so the chain ends as the step would alone.
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
            # A live driver is not stale; its refusal ends the chain.
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
    # The run of this pass, so the restamp measures none of its files again (U344).
    scored = [SCORED_BY_FLAG, chain.analyzed] if step == RESTAMP and chain.analyzed else []
    # ``--queue-only`` (U192), since the chain drives the job itself below.
    envelope = required(chain, step, [*words, *scored, foreground.QUEUE_ONLY, str(folder)])
    data = envelope.get("data") or {}
    job_id = str(data.get("job_id") or "")
    left_out = restamp_left_out(chain, data) if scored else None
    if left_out is not None and data.get("state") == ALL_SCORED:
        chain.check(
            step,
            "ok",
            f"crate {' '.join(words)} queued nothing over {folder}: analyze run job "
            f"{chain.analyzed} scored all {left_out} staged file(s) in this pass under "
            f"the calibration active now, so their energy was not measured again",
        )
        return
    if envelope.get("outcome") == str(Outcome.NO_OP) or not job_id:
        # Nothing to queue is not a step done, so the landing is not planned.
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
        error = job_error(chain, job)
        raise Stop(step, refused_stop(error, chain.settled.get(step)) if step == TAG else error)
    said = f"crate {' '.join(words)} job {job.job_id} succeeded over {folder}"
    if left_out:
        said += (
            f", leaving out {left_out} staged file(s) analyze run job {chain.analyzed} "
            f"scored in this pass under the calibration active now, whose energy "
            f"was not measured again"
        )
    elif left_out is not None:
        said += (
            f", leaving out no staged file, since analyze run job {chain.analyzed} "
            f"scored none of them in this pass under the calibration active now with "
            f"its energy tag still reading that level"
        )
    chain.check(step, "ok", said)
    if step == ANALYZE:
        chain.analyzed = job.job_id
    if step == TAG:
        refused_files(chain, chain.settled.get(step))


def restamp_left_out(chain: Chain, data: Mapping[str, Any]) -> int:
    """How many staged files the restamp left out as the run's, recorded on the summary.

    Read off the restamp's own answer, never counted here: a no op names the
    count under ``progress``, as a queued job does (U344).
    """
    progress = data.get("progress")
    count = progress.get(LEFT_OUT) if isinstance(progress, Mapping) else None
    left_out = count if isinstance(count, int) and not isinstance(count, bool) else 0
    chain.summary["restamp_left_out"] = left_out
    return left_out


def _tagging(section: Any) -> Mapping[str, Any]:
    """The ``tagging`` report a ``tag folder --job`` envelope carries, or nothing."""
    found = section.get("tagging") if isinstance(section, Mapping) else None
    return found if isinstance(found, Mapping) else {}


def refused_files(chain: Chain, envelope: Mapping[str, Any] | None) -> None:
    """Name the files the tag step left with no genre because the catalogues refused (U284).

    Such a file is settled askable and the pass goes on, so the summary and a
    row of its own name each file and the refusing catalogues, read off the
    tag step's report.
    """
    data = (envelope or {}).get("data")
    progress = data.get("progress") if isinstance(data, Mapping) else None
    report = _tagging(progress).get("refused")
    if not isinstance(report, Mapping) or not report.get("files"):
        return
    chain.summary["refused"] = {
        "files": list(report.get("files") or ()),
        "catalogues": dict(report.get("catalogues") or {}),
    }
    chain.note(
        "refused",
        "warn",
        f"{report.get('said', '')}. They land under needs genre unless tag guess "
        f"gives them one, and stay askable",
    )


def refused_stop(error: CratekitError, envelope: Mapping[str, Any] | None) -> CratekitError:
    """The tag step's stop, saying who refused, since when, and the token (U284).

    The job's refusal says nothing of why, so the tag verb's own words under
    ``tagging`` are added when every catalogue refused.
    """
    raw = (envelope or {}).get("cause")
    detail = raw.get("detail") if isinstance(raw, Mapping) else None
    stop = _tagging(detail).get("refusal_stop")
    if not isinstance(stop, Mapping) or not stop.get("said"):
        return error
    cause = error.cause
    head = cause.message.rstrip()
    steps = tuple(str(step) for step in stop.get("steps") or ())
    return rebuilt(
        error,
        dataclasses.replace(
            cause,
            message=f"{head}{'' if head.endswith(('.', '!', '?')) else '.'} {stop['said']}",
            remediation=dataclasses.replace(
                cause.remediation,
                steps=(*steps, *(step for step in cause.remediation.steps if step not in steps)),
            ),
        ),
    )


def vocals_unavailable() -> str | None:
    """Why the vocal model cannot score in this process, or None (U181).

    Asked before the tail runs, since ``analyze run``'s worker binds the
    loader in this process and a bound loader reads as able.
    """
    from cratekit.analysis import vocals  # noqa: PLC0415 - a feature module, asked once

    return vocals.unavailable()


def vocals_on(cfg: config.Config) -> bool:
    """Whether this profile switches on the vocals module, ``analyze vocals`` with it.

    With the module off, nothing here asks the model for scores.
    """
    membership = profiles.resolve(cfg.profile.name, dict(cfg.modules.explicit))
    return registry.entry(VOCALS_VERB).available_to(membership)


def rescore(chain: Chain, folder: Path, cfg: config.Config, *, unable: str | None) -> None:
    """Score every staged file analyze run measured with no voxlevel, as part of the analyze step.

    ``analyze run`` skips a file it already measured (R-277, U343), so such a file is
    never scored again by it; ``analyze vocals --unscored`` queues exactly
    those. ``unable`` is :func:`vocals_unavailable`; when set nothing is
    queued and the row says so.
    """
    if not vocals_on(cfg):
        chain.summary["vocal_rescore"] = "off"
        chain.note(
            RESCORE,
            "info",
            "the vocals module is off on this profile, so no staged file was "
            "scored for vocals after analyze run",
        )
        return
    if unable is not None:
        chain.summary["vocal_rescore"] = "skipped"
        chain.note(
            RESCORE,
            "info",
            f"staged files analyze run measured with no voxlevel were not scored, since "
            f"the vocal model cannot score here: {unable}",
        )
        return
    try:
        replace_stale(chain, ANALYZE, VOCALS_VERB, folder, cfg)
    except CratekitError as exc:
        raise Stop(ANALYZE, rebuilt(exc, exc.cause.at(chain.namespace))) from exc
    envelope = required(chain, ANALYZE, [*VOCALS_WORDS, VOCALS_UNSCORED, str(folder)])
    job_id = str((envelope.get("data") or {}).get("job_id") or "")
    if envelope.get("outcome") == str(Outcome.NO_OP) or not job_id:
        chain.summary["vocal_rescore"] = 0
        chain.note(
            RESCORE,
            "ok",
            f"every staged file analyze run measured carries a voxlevel, so no vocal "
            f"score was owed over {folder}",
        )
        return
    with jobs.open_store() as store:
        job = jobs.get(store, job_id)
        count = len(jobs.items(store, job_id))
    job = settle(chain, ANALYZE, job)
    if job.state is not jobs.JobState.SUCCEEDED:
        raise Stop(ANALYZE, job_error(chain, job))
    chain.summary["vocal_rescore"] = count
    chain.note(
        RESCORE,
        "ok",
        f"crate analyze vocals job {job.job_id} scored the {count} staged file(s) "
        f"analyze run measured with no voxlevel over {folder}",
    )


def guess_argv(folder: Path, pass_name: str | None = None) -> list[str]:
    """``tag guess`` over ``folder``, with the pass whose playlists vote when there is one."""
    return [*GUESS_WORDS, str(folder), *([PASS_FLAG, pass_name] if pass_name else [])]


def guess(chain: Chain, folder: Path, pass_name: str | None = None) -> None:
    """``tag guess`` over the ABSOLUTE staging folder, right after ``tag folder`` (U172).

    Each file with no genre gets one guessed from its artist's other tracks
    and, with ``pass_name``, its playlist, so the landing files it in a tree.
    A refusal ends the chain as any step's does.
    """
    envelope = required(chain, GUESS, guess_argv(folder, pass_name))
    totals = (envelope.get("data") or {}).get("totals") or {}
    count = int(totals.get("count") or 0)
    before = int(totals.get("before") or 0)
    after = int(totals.get("after") or 0)
    written = int(totals.get("written") or 0)
    unread = int(totals.get("unread") or 0)
    left = count - after - unread
    chain.summary["guess"] = {
        "files": count,
        "before": before,
        "after": after,
        "written": written,
        "left": left,
        "unread": unread,
        "bands": totals.get("bands") or {},
    }
    chain.check(
        GUESS,
        "ok",
        f"tag guess gave {written} file(s) a genre over {folder}: {before} of {count} "
        f"carried one before it and {after} after it, {left} still carry none"
        + (f" and {unread} could not be read" if unread else ""),
    )


def name_argv(folder: Path) -> list[str]:
    """``name apply`` over ``folder`` with its confirm answered, the one rule both verbs use."""
    return ["-d", f"{NAME_GATE}={NAME_OPTION}", "name", "apply", "--root", str(folder)]


def name(chain: Chain, folder: Path, cfg: config.Config | None = None) -> None:
    """``name apply`` over the ABSOLUTE staging folder, its confirm answered inline.

    A refusal over a second copy of one recording names the passes that
    downloaded it (U212); ``cfg`` keeps that to this library's jobs.
    """
    try:
        envelope = required(chain, NAME, name_argv(folder))
    except Stop as stop:
        raise second_copies(stop, cfg) from None
    totals = (envelope.get("data") or {}).get("totals") or {}
    chain.check(NAME, "ok", f"name apply ran over {folder}: {json.dumps(totals, sort_keys=True)}")


def second_copies(stop: Stop, cfg: config.Config | None) -> Stop:
    """The name step's stop, with a step per second copy naming who downloaded it (U212).

    Only a ``rename-incomplete`` whose outstanding files carry an ISRC, which
    the naming verb may not trace since it sits below the download verb.
    Anything else, or an unreadable queue, leaves the stop unchanged.
    """
    cause = stop.error.cause
    if cause.reason != RENAME_INCOMPLETE:
        return stop
    owed = (cause.detail or {}).get("incomplete")
    copies: dict[str, str] = {}
    for item in owed if isinstance(owed, list) else ():
        if isinstance(item, dict):
            isrc = tags.isrc_token(item.get("isrc"))
            if isrc:
                copies.setdefault(isrc, str(item.get("from") or ""))
    if not copies:
        return stop
    try:
        steps = tuple(_downloaded_by(isrc, held, cfg) for isrc, held in copies.items())
    except (CratekitError, OSError):
        return stop
    return Stop(stop.step, with_steps(stop.error, *steps), continues=stop.continues)


def _downloaded_by(isrc: str, held: str, cfg: config.Config | None) -> str:
    """One step: the passes whose download jobs acquired ``isrc``, earliest first.

    A job counts only for an item it finished. The pass is the name of the
    list the job downloaded.
    """
    from cratekit.acquire import cli as acquire_cli  # noqa: PLC0415 - one module's keys
    from cratekit.acquire import listdoc  # noqa: PLC0415 - the list's own suffix

    key = registry.entry(DOWNLOAD_VERB).handler_key
    passes: list[str] = []
    with jobs.open_store() as store:
        # ``list_jobs`` is newest first, so reversed is earliest first.
        for job in reversed(jobs.list_jobs(store)):
            if job.handler_key != key:
                continue
            if cfg is not None and job.library_id != cfg.library.volume_id:
                continue
            payload = job.payload or {}
            frozen = payload.get(acquire_cli.TRACKS)
            refs = {
                str(ref)
                for ref, said in (frozen.items() if isinstance(frozen, dict) else ())
                if isinstance(said, dict) and tags.isrc_token(said.get("isrc")) == isrc
            }
            if not refs:
                continue
            done = {
                item.item_id
                for item in jobs.items(store, job.job_id)
                if item.state is jobs.ItemState.DONE
            }
            if refs & done:
                listed = Path(str(payload.get(acquire_cli.LIST) or "")).name
                named = listed.removesuffix(listdoc.LIST_SUFFIX) or job.job_id
                passes.append(f"{named} (job {job.job_id})")
    carried = f"ISRC {isrc}, carried by {held} and by the file whose name it would take,"
    if not passes:
        return (
            f"{carried} is in no download job of this library, so the copy in its way "
            f"did not come from a download here: compare the two by hand"
        )
    return (
        f"{carried} was downloaded by: {', '.join(passes)}; keep one copy, move the "
        f"other out of the folder, and continue the pass"
    )


def land(chain: Chain, folder: Path, landing: Sequence[str] = ()) -> None:
    """Plan the landing through ``intake land`` itself, which stops for a person.

    It reads the backup acknowledgment and asks its explicit gate on its own
    run. Returns only by :class:`Done`, when it planned nothing. ``landing``
    is the arguments after the folder.
    """
    argv = ["intake", "land", str(folder), *landing]
    code, envelope = chain.call(LAND, argv)
    if succeeded(code, envelope):
        chain.check(LAND, "info", "intake land planned nothing to land")
        raise Done(LAND)
    cause = cause_of(chain, LAND, argv, code, envelope)
    if cause.reason == ACK_STOP or cause.code in gates.GATE_CODES:
        lift_plan_warnings(chain, cause)
        raise Attend(LAND, argv, cause)
    raise Stop.of(LAND, cause)


def lift_plan_warnings(chain: Chain, cause: Cause) -> None:
    """The warnings the landing's gate screen carries, onto the chain's own (U181).

    A refusal's envelope has no warnings channel, so ``intake land`` puts them
    in ``shown`` and they are carried here as :meth:`Chain.call` carries a
    child's.
    """
    shown = (cause.detail or {}).get("shown")
    warned = shown.get("warnings") if isinstance(shown, dict) else None
    for warning in warned if isinstance(warned, list) else ():
        if isinstance(warning, dict) and warning.get("code"):
            chain.warnings.append(
                {
                    "code": str(warning["code"]),
                    "message": f"{LAND}: {warning.get('message', '')}",
                }
            )


def rehearse(chain: Chain, folder: Path, landing: Sequence[str] = ()) -> None:
    """Rehearse the landing on a copy through ``intake land --rehearse`` itself (U162, U179).

    The same arguments the landing then takes, so the live gate names this
    rehearsal. A missing acknowledgment stops for a person; any other refusal
    ends the chain, since a failed rehearsal is no landing to ask. Ends by
    :class:`Done` when there was nothing to rehearse.
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


def through_name(
    chain: Chain, folder: Path, cfg: config.Config, pass_name: str | None = None
) -> Path:
    """The tail in its order over ``folder``, ending with ``name apply``; the absolute folder.

    Every step succeeds or ends the chain. ``folder`` is made absolute here.
    ``pass_name`` is the pass whose playlists vote in the genre guess (U172).
    """
    folder = folder.expanduser().absolute()
    chain.summary["staging"] = str(folder)
    # Asked before the first step (U181), see :func:`vocals_unavailable`.
    unable = vocals_unavailable()
    for step, verb, words in TAIL:
        tail_step(chain, step, verb, words, folder, cfg)
        if step == TAG:
            guess(chain, folder, pass_name)
        if step == ANALYZE:
            rescore(chain, folder, cfg, unable=unable)
    name(chain, folder, cfg)
    return folder


def run(
    chain: Chain,
    folder: Path,
    cfg: config.Config,
    landing: Sequence[str],
    pass_name: str | None = None,
) -> None:
    """The tail in its order over ``folder``, then the landing planned and stopped.

    Never returns: it ends in :class:`Attend`, :class:`Done` or :class:`Stop`.
    ``pass_name`` is None for a batch no account playlist asked for (U172).
    """
    folder = through_name(chain, folder, cfg, pass_name)
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

    Nothing is answered here. Records the stop on the chain's summary and check.
    """
    # Shell quoted (U179), since batch folders and names hold spaces.
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
        # Any other gate code: the step's own remediation says how to answer.
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
        # A rehearsal reads the acknowledgment too (U162), so a stop there
        # names the rehearsal again, then the landing.
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
    "ALL_SCORED",
    "ANALYZE",
    "ANALYZE_PLAYLIST",
    "GATE_STOP",
    "GUESS",
    "GUESS_VERB",
    "GUESS_WORDS",
    "LAND",
    "LAND_GATE",
    "LAND_OPTION",
    "LAND_VERB",
    "LEFT_OUT",
    "NAME",
    "NAME_GATE",
    "NAME_OPTION",
    "NAME_VERB",
    "PASS_FLAG",
    "REKORDBOX_STEPS",
    "REHEARSE",
    "REHEARSE_FLAG",
    "RESCORE",
    "RESTAMP",
    "SCORED_BY_FLAG",
    "SESSION_ACTOR",
    "STEPS",
    "TAG",
    "TAIL",
    "VOCALS_UNSCORED",
    "VOCALS_VERB",
    "VOCALS_WORDS",
    "Attend",
    "Attended",
    "Chain",
    "Child",
    "Done",
    "Stop",
    "argv_for",
    "attended",
    "cause_of",
    "changed_said",
    "dispatch",
    "guess",
    "guess_argv",
    "job_error",
    "land",
    "lift_plan_warnings",
    "load_config",
    "name",
    "name_argv",
    "refused_files",
    "refused_stop",
    "rehearse",
    "replace_stale",
    "required",
    "rescore",
    "restamp_left_out",
    "run",
    "settle",
    "succeeded",
    "summary_of",
    "tail_step",
    "through_name",
    "vocals_on",
    "vocals_unavailable",
    "with_steps",
]
