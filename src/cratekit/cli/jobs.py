"""The four job verbs, and the one place a handler key becomes a command line.

The engine knows no verb (KTD23) and re-invokes the product without importing
the working module (KTD26): a job stores a handler key, resolved here against
the registry without importing anything, and the owning module is imported only
to build the argument list. Reporting a job never fails because the job failed,
so its cause rides in the payload (KTD25). Resuming reconciles first, since the
lock, not the row, is the disk truth.
"""

from __future__ import annotations

import argparse
import dataclasses
import importlib
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any, Sequence

from cratekit.cli import handlers, registry
from cratekit.cli.output import Envelope
from cratekit.core import backup_facts, config, jobs
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation
from cratekit.core.exit_codes import ExitCode, Remedy

if TYPE_CHECKING:  # pragma: no cover - typing only, and a cycle if imported for real
    from cratekit.cli import Context

#: What a listing puts in the payload's single-job field, empty so no consumer
#: reads the envelope as describing one job.
NO_SINGLE_JOB = ""


def _summary(store: jobs.JobStore, job: jobs.Job) -> dict[str, Any]:
    """One job flattened for the payload, progress and worker state included.

    ``worker`` says whether anything is bound to run the handler, so a job that
    will sit for ever says so; answered from the declaration tables alone (KTD26).
    """
    bound = handlers.is_known(job.handler_key)
    row = {
        "job_id": job.job_id,
        "handler": job.handler_key,
        "worker": "bound" if bound else "none",
        "worker_reason": None if bound else handlers.unbound_reason(job.handler_key),
        "state": str(job.state),
        "stage": job.stage,
        "attempts": job.attempts,
        "created": job.created,
        "updated": job.updated,
        "library_id": job.library_id,
        "progress": jobs.progress(store, job.job_id),
        "cause": job.cause.to_json() if job.cause is not None else None,
    }
    # The playlist an intake job was made for (U182); other jobs gain no field.
    named = intake_playlist(job)
    if named is not None:
        row[PLAYLIST_FIELD], row[SOURCE_FIELD] = named
    return row


def _parse_states(values: Sequence[str]) -> tuple[jobs.JobState, ...]:
    """Turn ``--state`` arguments into states, refusing an unknown one.

    A filter that silently matches nothing would read as an empty queue.
    """
    parsed: list[jobs.JobState] = []
    for value in values:
        try:
            parsed.append(jobs.JobState(value))
        except ValueError:
            raise CratekitError(
                Cause(
                    reason="job-unknown",
                    message=(
                        f"{value!r} is not a job state; the declared states are "
                        f"{', '.join(str(state) for state in jobs.JobState)}"
                    ),
                    remediation=Remediation(
                        steps=("filter on one of the declared job states",)
                    ),
                    origin=("cli.jobs",),
                    detail={"state": value},
                )
            ) from None
    return tuple(parsed)


# ---------------------------------------------------------------------------
# job list
# ---------------------------------------------------------------------------


def build_list(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument(
        "--state",
        action="append",
        default=[],
        metavar="STATE",
        help="show only jobs in this state; repeatable",
    )
    parser.set_defaults(_handler=list_jobs)


def list_jobs(ctx: "Context") -> Envelope:
    states = _parse_states(ctx.args.state)
    with jobs.open_store() as store:
        rows = [_summary(store, job) for job in jobs.list_jobs(store, states=states or None)]
    counts: dict[str, int] = {str(state): 0 for state in jobs.JobState}
    for row in rows:
        counts[row["state"]] += 1
    return ctx.envelope(
        data={
            "job_id": NO_SINGLE_JOB,
            "state": ",".join(str(state) for state in states) if states else "all",
            "cause": None,
            "progress": {"jobs": rows, "counts": counts},
        },
        outcome=Outcome.OK if rows else Outcome.NO_OP,
    )


# ---------------------------------------------------------------------------
# job show
# ---------------------------------------------------------------------------


def build_show(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("job_id", help="the job to describe")
    parser.set_defaults(_handler=show)


def show(ctx: "Context") -> Envelope:
    with jobs.open_store() as store:
        job = jobs.reconcile(store, ctx.args.job_id)
        summary = _summary(store, job)
        drifted = _drift_warning(job)
    # What each backup item ran, from installation state since the job keeps
    # its frozen payload (KTD9, R-349); failed items included, absent when none.
    outcomes = backup_facts.read_outcomes(job.job_id)
    if outcomes is not None:
        summary[backup_facts.OUTCOMES_FIELD] = outcomes
    tracks = _intake_tracks(job)
    if tracks is not None:
        summary[TRACKS_FIELD] = tracks
    return ctx.envelope(
        data={
            "job_id": job.job_id,
            "state": str(job.state),
            "cause": summary["cause"],
            "progress": summary,
        },
        warnings=drifted,
    )


#: The intake handlers, the payload key holding their frozen tracks, and the
#: field ``job show`` lists them in (R-925). Spelled here so reporting loads no
#: feature module (KTD26); a test pins them. The field is not ``tracks``, which
#: other payloads use for a count.
INTAKE_HANDLERS: frozenset[str] = frozenset({"intake.set", "intake.playlist"})
INTAKE_TRACKS_KEY = "tracks"
TRACKS_FIELD = "intake_tracks"


def _intake_tracks(job: jobs.Job) -> list[dict[str, Any]] | None:
    """The tracks an intake job froze, in its order, or None for any other job.

    The payload is what the worker resolves, so this is what would be acquired.
    A row that is not a mapping is listed by its item, never dropped.
    """
    if job.handler_key not in INTAKE_HANDLERS:
        return None
    frozen = (job.payload or {}).get(INTAKE_TRACKS_KEY)
    if not isinstance(frozen, Mapping):
        return []
    listed = []
    for item, said in frozen.items():
        said = said if isinstance(said, Mapping) else {}
        listed.append(
            {
                "item": str(item),
                "artist": str(said.get("artist") or ""),
                "title": str(said.get("title") or ""),
                "version": str(said.get("version") or ""),
                "isrc": str(said["isrc"]) if said.get("isrc") else None,
            }
        )
    return listed


def _drift_warning(job: jobs.Job) -> tuple[dict[str, str], ...]:
    """Name what moved in the configuration since the job was queued (KTD9).

    A warning, not a refusal: the job runs on its frozen inputs regardless.
    """
    try:
        current = config.load()
    except config.ConfigError:
        return ()
    return handlers.drift_warnings(jobs.drift(job, current))


# ---------------------------------------------------------------------------
# job cancel
# ---------------------------------------------------------------------------


def _days(text: str) -> int:
    """Parse ``--stale-days``, refusing zero and a negative at the parser (status 2).

    A cutoff of now would offer every queued job as stale; a day is the least.
    """
    value = int(text)
    if value < 1:
        raise ValueError(f"{text!r} is not a number of days")
    return value


def build_cancel(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    which = parser.add_mutually_exclusive_group(required=True)
    which.add_argument("job_id", nargs="?", default=None, help="the job to cancel")
    which.add_argument(
        "--stale-days",
        type=_days,
        default=None,
        dest="stale_days",
        metavar="N",
        help=(
            "cancel every queued intake job of this library queued more than N "
            "days ago, never a running one, keeping the newest job of each "
            "identical track set; each cancel lets its playlist queue again on "
            "the next pass"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="list what would be cancelled, and what each cancel frees, and cancel nothing",
    )
    parser.set_defaults(_handler=cancel)


def cancel(ctx: "Context") -> Envelope:
    if ctx.args.stale_days is not None:
        return _cancel_stale(ctx, ctx.args.stale_days, dry_run=ctx.args.dry_run)
    with jobs.open_store() as store:
        job = jobs.reconcile(store, ctx.args.job_id)
        if not ctx.args.dry_run:
            job = jobs.cancel(store, job.job_id, stage=job.stage)
        summary = _summary(store, job)
    if ctx.args.dry_run:
        summary[DRY_RUN_FIELD] = True
    # Cancelling succeeds, reported in the payload (R22), so a non-zero exit
    # means only a cancel that did not work.
    return ctx.envelope(
        data={
            "job_id": job.job_id,
            "state": str(job.state),
            "cause": summary["cause"],
            "progress": summary,
        },
        outcome=Outcome.NO_OP if ctx.args.dry_run else Outcome.OK,
    )


#: The field a dry run marks its answer with, and the three lists a stale
#: cancel answers with, each a row per job (U182).
DRY_RUN_FIELD = "dry_run"
#: The state word of a stale cancel that cancelled nothing.
NOTHING_CANCELLED = "unchanged"
STALE_FIELD = "stale_days"
CANCEL_LIST = "cancel"
KEPT_LIST = "kept"
LEFT_LIST = "left"


def now() -> datetime:
    """The instant ages are measured to. One function, so a test can move it."""
    return datetime.now(timezone.utc)


def _row(hold: Hold, **said: Any) -> dict[str, Any]:
    return {
        "job_id": hold.job.job_id,
        "handler": hold.job.handler_key,
        "state": str(hold.job.state),
        PLAYLIST_FIELD: hold.playlist,
        SOURCE_FIELD: hold.source,
        "label": hold.label(),
        "age_days": hold.age_days,
        "tracks": hold.tracks,
        "same_tracks": list(hold.same_tracks),
        **said,
    }


def _left_reason(hold: Hold, cutoff: datetime, days: int) -> str | None:
    """Why this open job is not stale, or None when it is a candidate.

    Only a queued job with a readable queued instant can be stale.
    """
    state = hold.job.state
    if state is jobs.JobState.RUNNING:
        return "running; a stale cancel never touches a running job"
    if state is not jobs.JobState.QUEUED:
        return (
            f"{state}, not queued; if it is stale, cancel it by its id: "
            f"crate job cancel {hold.job.job_id}"
        )
    created = _instant(hold.job.created)
    if created is None:
        return f"its queued time {hold.job.created!r} cannot be read, so its age is unknown"
    if created >= cutoff:
        return f"queued {hold.age_days} day(s) ago, within the {days} day(s) asked"
    try:
        jobs.assert_free(hold.job.job_id)
    except jobs.DriverHeld:
        return "a live driver holds it; a stale cancel never touches a running job"
    return None


def _frees(hold: Hold, staying: Sequence[Hold]) -> str:
    """What cancelling this job lets the next pass do, in one sentence.

    A playlist is freed only when no job staying open holds it, compared as the
    pass reads it (:attr:`Hold.identity`), never as typed.
    """
    if hold.job.handler_key != "intake.playlist":
        return "frees no account playlist: a set job holds none out of a pass"
    holder = next(
        (
            other.job.job_id
            for other in staying
            if other.job.handler_key == "intake.playlist"
            and hold.identity
            and other.identity == hold.identity
        ),
        None,
    )
    if holder is not None:
        return f"frees nothing yet: job {holder} still holds {hold.label()} out of every pass"
    return f"frees {hold.label()}, so the next pass queues it again"


def _cancel_stale(ctx: "Context", days: int, *, dry_run: bool) -> Envelope:
    """List, or cancel, every queued intake job of this library older than ``days``.

    No gate, since a cancel moves no file and ``job resume`` undoes it. Each
    cancel holds the driver lock and needs the row still queued. Of jobs holding
    the same tracks the newest is kept, so the tracks still resolve once.
    """
    from cratekit.cli import tail  # noqa: PLC0415 - the one refusal for an unreadable config

    cfg = tail.load_config(("cli.jobs",))
    moment = now()
    cutoff = moment - timedelta(days=days)
    library = cfg.library.volume_id
    with jobs.open_store() as store:
        # A running row nobody drives was killed; reconcile it to queued.
        for held in jobs.list_jobs(store, states=(jobs.JobState.RUNNING,)):
            if held.handler_key in INTAKE_HANDLERS and held.library_id == library:
                jobs.reconcile(store, held.job_id)
        holds = intake_holds(store, library, now=moment)
        by_id = {hold.job.job_id: hold for hold in holds}
        stale, kept, left = [], [], []
        for hold in holds:
            reason = _left_reason(hold, cutoff, days)
            if reason is not None:
                left.append(_row(hold, reason=reason))
                continue
            keeper = max(
                (by_id[other].job for other in (hold.job.job_id, *hold.same_tracks)),
                key=_newest,
            )
            if hold.same_tracks and keeper.job_id == hold.job.job_id:
                kept.append(
                    _row(
                        hold,
                        reason=(
                            f"kept, the newest of {len(hold.same_tracks) + 1} open "
                            f"jobs holding these {hold.tracks} tracks"
                        ),
                    )
                )
                continue
            stale.append((hold, keeper.job_id if hold.same_tracks else None))
        going = {hold.job.job_id for hold, _keeper in stale}
        staying = [hold for hold in holds if hold.job.job_id not in going]
        cancelled = []
        for hold, keeper in stale:
            said = {
                "kept": keeper,
                "reason": (
                    f"a copy of the tracks job {keeper} holds; {keeper} is kept"
                    if keeper
                    else f"queued {hold.age_days} day(s) ago"
                ),
                "frees": _frees(hold, staying),
            }
            if not dry_run:
                outcome = _cancel_queued(store, hold.job.job_id)
                if outcome is not None:
                    left.append(_row(hold, reason=outcome))
                    continue
                said["state"] = str(jobs.JobState.CANCELLED)
            cancelled.append(_row(hold, **said))
    acted = bool(cancelled) and not dry_run
    return ctx.envelope(
        data={
            "job_id": NO_SINGLE_JOB,
            "state": (
                DRY_RUN_FIELD
                if dry_run
                else str(jobs.JobState.CANCELLED) if cancelled else NOTHING_CANCELLED
            ),
            "cause": None,
            "progress": {
                STALE_FIELD: days,
                DRY_RUN_FIELD: dry_run,
                CANCEL_LIST: cancelled,
                KEPT_LIST: kept,
                LEFT_LIST: left,
            },
        },
        outcome=Outcome.OK if acted else Outcome.NO_OP,
    )


def _cancel_queued(store: jobs.JobStore, job_id: str) -> str | None:
    """Cancel one job only while it is queued and undriven; else say why not."""
    try:
        with jobs.driver_lock(job_id):
            current = jobs.get(store, job_id)
            if current.state is not jobs.JobState.QUEUED:
                return f"{current.state} by the time it was reached, so it was left"
            jobs.cancel(store, job_id, stage=current.stage)
    except jobs.DriverHeld:
        return "a live driver took it before it was reached, so it was left"
    return None


# ---------------------------------------------------------------------------
# job resume
# ---------------------------------------------------------------------------


def build_resume(parser: argparse.ArgumentParser, entry: registry.Entry) -> None:
    parser.add_argument("job_id", help="the job to resume")
    parser.set_defaults(_handler=resume)


def argv_for(job: jobs.Job) -> list[str]:
    """Turn a stored handler key and frozen payload back into a command line.

    The registry lookup imports nothing, so an unknown handler fails first; only
    then is the one owning module imported.
    """
    try:
        entry = registry.by_handler_key(job.handler_key)
    except KeyError:
        raise CratekitError(
            Cause(
                reason="internal-error",
                message=(
                    f"job {job.job_id} was queued for the handler "
                    f"{job.handler_key!r}, which this build does not register"
                ),
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                origin=("cli.jobs",),
                detail={"job_id": job.job_id, "handler": job.handler_key},
            )
        ) from None
    if not entry.landed or not entry.argv_builder:
        raise CratekitError(
            Cause(
                reason="internal-error",
                message=(
                    f"{entry.name} cannot be re-invoked: it declares no way to turn "
                    f"a frozen payload back into a command line"
                ),
                remediation=Remediation(remedy=Remedy.REPORT_DEFECT),
                origin=("cli.jobs",),
                detail={"job_id": job.job_id, "handler": job.handler_key},
            )
        )
    module = importlib.import_module(entry.module)
    return list(getattr(module, entry.argv_builder)(job))


def resume_argv(job: jobs.Job) -> list[str]:
    """The argument list that re-invokes a resume for one job.

    A real builder, so every long-running verb in the registry has one.
    """
    return ["job", "resume", job.job_id]


def resume(ctx: "Context") -> Envelope:
    with jobs.open_store() as store:
        job = jobs.reconcile(store, ctx.args.job_id)
        # Checked here so the refusal is seen, not logged by a spawned child.
        jobs.assert_free(job.job_id)
        if not job.is_open():
            # ``retry`` refuses a cause that is not retryable (R-390), in the
            # engine so every caller gets the check.
            job = jobs.retry(store, job.job_id)
        pid = jobs.spawn(store, job, argv_for(job))
        summary = _summary(store, job)
        summary["pid"] = pid
        drifted = _drift_warning(job)
    return ctx.envelope(
        data={
            "job_id": job.job_id,
            "state": str(job.state),
            "cause": summary["cause"],
            "progress": summary,
        },
        code=ExitCode.OK,
        warnings=drifted,
    )



# ---------------------------------------------------------------------------
# The open intake jobs of a library, read once for every verb that reports them
# ---------------------------------------------------------------------------


#: The payload keys an intake job freezes its playlist name and reference
#: under (U182); a test pins them to the intake module's.
INTAKE_PLAYLIST_KEY = "playlist_name"
INTAKE_SOURCE_KEY = "source"
#: The reserved reference the account's hearts are queued under, pinned the same way.
INTAKE_HEARTS = "favorites"
#: The payload key and value marking a job the playlists sweep queued; pinned
#: to ``sync.playlists``.
INTAKE_SWEEP_KEY = "source_id"
INTAKE_SWEEP_ID = "playlists"
#: The fields ``job show`` and ``job list`` name an intake job's playlist in.
PLAYLIST_FIELD = "playlist"
SOURCE_FIELD = "source"


def intake_playlist(job: jobs.Job) -> tuple[str, str] | None:
    """The playlist an intake job was made for and its source, or None for any other job.

    The name is the account's, frozen at the queue (U113). A hand queued
    playlist job with no name uses its reference instead; a set's file and the
    hearts never stand in for a name. Either is ``""`` when none was frozen.
    """
    if job.handler_key not in INTAKE_HANDLERS:
        return None
    payload = job.payload or {}
    source = payload.get(INTAKE_SOURCE_KEY)
    source = source.strip() if isinstance(source, str) else ""
    name = payload.get(INTAKE_PLAYLIST_KEY)
    name = name.strip() if isinstance(name, str) else ""
    if name or job.handler_key != "intake.playlist" or source == INTAKE_HEARTS:
        return name, source
    return source, source


def playlist_identity(job: jobs.Job, source: str) -> str:
    """The playlist a pass reads this job as holding, or ``""`` for none.

    The sweep's own reading, ``sync.playlists.recorded_as``, copied rather than
    imported to keep the export writer out of reach; a test pins them equal. A
    typed reference is parsed to the listing's id, or kept as typed.
    """
    if job.handler_key != "intake.playlist":
        return ""
    if source == INTAKE_HEARTS:
        return INTAKE_HEARTS
    if (job.payload or {}).get(INTAKE_SWEEP_KEY) == INTAKE_SWEEP_ID:
        return source
    from cratekit.label import catalogue  # noqa: PLC0415 - the provider's id parser, when asked

    try:
        return catalogue.playlist_id(source)
    except ValueError:
        # Both refusals and malformed URLs raise ValueError; keep it as typed.
        return source


def _instant(stamp: str) -> datetime | None:
    """A job's recorded instant, or None when it cannot be read as one with an offset."""
    try:
        moment = datetime.fromisoformat(str(stamp))
    except ValueError:
        return None
    return moment if moment.tzinfo is not None else None


def age_days(job: jobs.Job, now: datetime) -> int | None:
    """Whole days since the job was queued, or None when its instant cannot be read."""
    created = _instant(job.created)
    if created is None:
        return None
    return max(0, (now - created).days)


@dataclasses.dataclass(frozen=True)
class Hold:
    """One open intake job, and what it holds out of a pass (U182).

    ``same_tracks`` names every other open intake job of the library whose items
    are exactly this job's, newest first.
    """

    job: jobs.Job
    playlist: str
    source: str
    identity: str
    age_days: int | None
    tracks: int
    same_tracks: tuple[str, ...]

    def label(self) -> str:
        """How a person reads which playlist this is."""
        if self.source == INTAKE_HEARTS:
            return "the account's hearts"
        if self.job.handler_key != "intake.playlist":
            return f"the set {self.playlist or self.source or self.job.job_id}"
        if not self.playlist:
            return f"an unnamed playlist (job {self.job.job_id})"
        shown = self.identity or self.source
        if shown and shown != self.playlist:
            return f"playlist {self.playlist!r} ({shown})"
        return f"playlist {self.playlist!r}"

    @property
    def named(self) -> bool:
        """Whether the job froze the account's own name for its playlist."""
        name = (self.job.payload or {}).get(INTAKE_PLAYLIST_KEY)
        return isinstance(name, str) and bool(name.strip())

    def age(self) -> str:
        return "age unknown" if self.age_days is None else f"{self.age_days} day(s) old"


def _newest(held: jobs.Job) -> tuple[datetime, str]:
    """The order "newest" means: the queued instant, then the identifier."""
    return (_instant(held.created) or datetime.min.replace(tzinfo=timezone.utc), held.job_id)


def intake_holds(store: jobs.JobStore, library_id: str, *, now: datetime) -> list[Hold]:
    """Every open intake job of this library, newest first, with what it holds.

    Two jobs are copies only when their items match; a job with no item is
    nobody's copy.
    """
    open_states = [state for state in jobs.JobState if state not in jobs.TERMINAL_STATES]
    found = sorted(
        (
            job
            for job in jobs.list_jobs(store, states=open_states)
            if job.handler_key in INTAKE_HANDLERS and job.library_id == library_id
        ),
        key=_newest,
        reverse=True,
    )
    sets = {
        job.job_id: frozenset(item.item_id for item in jobs.items(store, job.job_id))
        for job in found
    }
    holds = []
    for job in found:
        mine = sets[job.job_id]
        playlist, source = intake_playlist(job) or ("", "")
        holds.append(
            Hold(
                job=job,
                playlist=playlist,
                source=source,
                identity=playlist_identity(job, source),
                age_days=age_days(job, now),
                tracks=len(mine),
                same_tracks=tuple(
                    other.job_id
                    for other in found
                    if mine and other.job_id != job.job_id and sets[other.job_id] == mine
                ),
            )
        )
    return holds


__all__ = [
    "CANCEL_LIST",
    "DRY_RUN_FIELD",
    "INTAKE_HANDLERS",
    "INTAKE_HEARTS",
    "INTAKE_PLAYLIST_KEY",
    "INTAKE_SOURCE_KEY",
    "INTAKE_SWEEP_ID",
    "INTAKE_SWEEP_KEY",
    "INTAKE_TRACKS_KEY",
    "KEPT_LIST",
    "LEFT_LIST",
    "NOTHING_CANCELLED",
    "NO_SINGLE_JOB",
    "PLAYLIST_FIELD",
    "SOURCE_FIELD",
    "STALE_FIELD",
    "TRACKS_FIELD",
    "Hold",
    "age_days",
    "argv_for",
    "build_cancel",
    "build_list",
    "build_resume",
    "build_show",
    "cancel",
    "intake_holds",
    "intake_playlist",
    "list_jobs",
    "now",
    "playlist_identity",
    "resume",
    "resume_argv",
    "show",
]
