"""The four job verbs, and the one place a handler key becomes a command line.

The engine below deliberately knows no verb: KTD23 puts verb strings in this
layer, and KTD26 needs the engine to re-invoke the product without importing the
module that does the work. Both are satisfied by the same seam. A job stores a
HANDLER KEY, this file resolves that key against the registry, imports the owning
module only at the moment it is actually needed, and hands the assembled argument
list back to the engine to spawn.

Resolving the key does not import anything, which is the property the conformance
suite asserts directly: the engine validates a queued job's handler before it
spawns, and validating by import would pull every feature module into the
supervising process and walk straight around the lazy-import stubs.

Two smaller decisions worth stating.

**Reporting a job never fails because the job failed.** ``job show`` on a broken
job exits 0 and carries the job's cause in its PAYLOAD, where ``job_state``
already reserves a field for it. Making the verb's status mirror the job's status
would leave a caller unable to tell "this job failed" from "I could not read this
job", which is the same collapse KTD25 is about, one level up.

**Resuming reconciles first.** A row that still says running while nobody holds
the job's lock describes a driver that was killed, and believing that row would
either refuse a resume forever or double-drive a job whose lock is genuinely
held. Disk truth is the lock, not the row.
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

#: What a listing puts in the payload's single-job field. ``job_state`` is a
#: per-job surface and a listing is not about one job, so the field is empty
#: rather than carrying the first row's identifier, which a consumer would
#: reasonably read as "this envelope describes that job".
NO_SINGLE_JOB = ""


def _summary(store: jobs.JobStore, job: jobs.Job) -> dict[str, Any]:
    """One job flattened for the payload, progress and worker state included.

    ``worker`` is the honest half of an unfinished cutover. Most queued verbs
    still have no function behind their handler key, so their jobs sit for ever
    while reporting cleanly. Before anything was bound that was at least uniform,
    and a person could learn that queues do not run; with one verb working and the
    rest silent the same report invites the opposite conclusion. The question is
    answered from the declaration tables alone, which is what keeps a listing from
    importing every feature module (KTD26).
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
    # U182. The playlist an intake job was made for, on ``job show`` and ``job
    # list`` alike; a job of another verb gains no field.
    named = intake_playlist(job)
    if named is not None:
        row[PLAYLIST_FIELD], row[SOURCE_FIELD] = named
    return row


def _parse_states(values: Sequence[str]) -> tuple[jobs.JobState, ...]:
    """Turn ``--state`` arguments into states, refusing an unknown one.

    Refusing rather than ignoring, for the reason a dropped decision is refused
    upstream: a filter that silently matches nothing looks exactly like a queue
    that is empty, and the user's next move is to conclude their job vanished.
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
    # R-349. What each backup item actually ran, read from the installation
    # state rather than from the job, which keeps its frozen payload (KTD9).
    # Read whatever the items' states are, because the record a FAILED item left
    # is the one a person most needs. Absent for every job that recorded none,
    # so a job of another verb gains no field.
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


#: The handlers whose payload freezes the tracks an intake heard or listed,
#: the payload key it freezes them under, and the field ``job show`` lists
#: them in (R-925). Spelled here rather than imported from
#: ``cratekit.intake.cli``, because these verbs must not load a feature module
#: to report a job (KTD26); a test pins the spellings to that module's own.
#: The field is NOT ``tracks``, which a dozen payloads use for a count, so a
#: renderer can read it by name alone.
INTAKE_HANDLERS: frozenset[str] = frozenset({"intake.set", "intake.playlist"})
INTAKE_TRACKS_KEY = "tracks"
TRACKS_FIELD = "intake_tracks"


def _intake_tracks(job: jobs.Job) -> list[dict[str, Any]] | None:
    """The tracks an intake job froze, in its order, or None for any other job.

    THE PAYLOAD IS THE LIST. ``intake set`` freezes every identified row at the
    queue and the worker reads nothing else, so what is listed here is what
    would be resolved, and a person can read a five hour mix's tracks before
    anything is acquired from it. A job of another handler gains no field, so
    its report is unchanged. A frozen row that is not a mapping is listed with
    its item and nothing else, rather than dropped, so the list's length is
    always the payload's.
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

    A warning rather than a refusal. The job runs against its frozen inputs
    whatever this says; what the user needs is to know that the setting they just
    edited is not the setting this run is using, which is the half the recorded
    resume bug had no way to surface at all.
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
    """Parse ``--stale-days``, refusing zero and a negative AT THE PARSER (status 2).

    The same kind of statement ``type=int`` makes, so it is argparse's usage
    error and not a refusal. A cutoff of now or later would offer every queued
    job as stale, one queued a second ago included, and a job that young is
    not stale by any reading; a day is the least the flag means.
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
    # Cancelling SUCCEEDS. The job is reported as cancelled in the payload, and
    # that is the whole point of R22's distinction: a cancel that exited non-zero
    # would be indistinguishable from a cancel that did not work.
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
#: The state word of a stale cancel that found nothing to cancel, so a reader
#: of the field is never told ``cancelled`` over a queue nothing changed in.
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

    ONLY A QUEUED JOB IS STALE. A running one is somebody's drive, and a
    blocked one waits on a cause it names, so each is listed with its reason
    and left. A job whose queued instant cannot be read is never stale: an age
    nobody measured is not an old one.
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

    A pass leaves out a playlist while ANY open playlist job for it is open, so
    a playlist is freed only when no job staying open holds the same playlist,
    read as the pass reads it (:attr:`Hold.identity`), never by the reference
    as typed: a URL typed by hand and the id a sweep froze are one playlist.
    A set job holds no account playlist out of a pass at all.
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

    THE EXISTING CANCEL, IN A LOOP, under the one command a person typed after
    reading its ``--dry-run``: a cancel moves no file, and ``crate job resume``
    reopens a cancelled job, so a recorded decision would gate nothing a person
    cannot undo. Each cancel is taken holding the job's driver lock and only
    while the row still says queued, so a driver that picked a job up after the
    listing keeps it.

    DUPLICATES KEEP THEIR NEWEST. Of every set of open intake jobs holding
    exactly the same tracks, the newest is never cancelled here, and each copy
    cancelled names it, so the tracks are still resolved once.
    """
    from cratekit.cli import tail  # noqa: PLC0415 - the one refusal for an unreadable config

    cfg = tail.load_config(("cli.jobs",))
    moment = now()
    cutoff = moment - timedelta(days=days)
    library = cfg.library.volume_id
    with jobs.open_store() as store:
        # A RUNNING ROW NOBODY DRIVES WAS KILLED, and reads as queued once
        # reconciled, the disk truth every job verb reports from.
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

    The registry lookup comes FIRST and imports nothing, so an unknown handler
    fails before any module is loaded. The import happens only after the key is
    known to be real, and only for the one module that owns it, which is what
    keeps a queued analysis job from pulling the analysis dependencies into a
    process that is merely listing jobs.
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

    The identity case of the contract every long-running verb owes: given the
    frozen job, return the command line that continues it. It is written out here
    rather than special-cased inside ``argv_for`` so that the registry's claim
    that every long-running verb has a builder is true of this one too, and so the
    test that walks the registry and looks each builder up finds a real function.
    """
    return ["job", "resume", job.job_id]


def resume(ctx: "Context") -> Envelope:
    with jobs.open_store() as store:
        job = jobs.reconcile(store, ctx.args.job_id)
        # Checked here so a user who resumes a job that is already running sees
        # the refusal, rather than spawning a child that discovers the same thing
        # and writes it into a log nobody is watching.
        jobs.assert_free(job.job_id)
        if not job.is_open():
            # ``retry`` REFUSES a closed job whose cause is not retryable (R-390),
            # and that refusal is the engine's rather than this verb's on
            # purpose: the verb is the engine's only shipped caller today, and a
            # check written here alone would leave the next caller re-arming
            # work the job has already said cannot succeed.
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


#: The payload keys an intake job freezes its playlist under (U182): the name
#: the account gave it, and the reference it was listed from. Spelled here for
#: :data:`INTAKE_TRACKS_KEY`'s reason; a test pins them to the intake module's.
INTAKE_PLAYLIST_KEY = "playlist_name"
INTAKE_SOURCE_KEY = "source"
#: The reserved reference the account's hearts are queued under, pinned the same way.
INTAKE_HEARTS = "favorites"
#: The payload key, and the value under it, that mark a job the playlists
#: sweep queued, whose source is the listing's own id; pinned to ``sync.playlists``.
INTAKE_SWEEP_KEY = "source_id"
INTAKE_SWEEP_ID = "playlists"
#: The fields ``job show`` and ``job list`` name an intake job's playlist in.
PLAYLIST_FIELD = "playlist"
SOURCE_FIELD = "source"


def intake_playlist(job: jobs.Job) -> tuple[str, str] | None:
    """The playlist an intake job was made for and its source, or None for any other job.

    THE NAME IS THE ACCOUNT'S, FROZEN AT THE QUEUE (U113), because ``sync mark``
    later renames the account's copy. A job queued by hand with ``intake
    playlist`` froze no name, only the reference a person typed, so that
    reference stands as its playlist rather than nothing: sitting 51 could not
    tell 17 jobs apart for want of exactly this. A set's file and the hearts'
    reserved reference are no playlist, so neither stands in for a name. Either
    is ``""`` when the payload froze none.
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

    THE SWEEP'S OWN READING, ``sync.playlists.recorded_as``, written again here
    rather than imported: that module reaches the rekordbox export writer at
    module scope, and the match engine, which reaches this module, is held by
    test to reach no export reader at any depth. A test pins the two readings
    to agree. A job the sweep queued carries the listing's own id, kept as it
    is; a reference typed by hand is parsed to the id the listing carries, so
    a URL and a sweep's job for the same playlist are one playlist here as
    they are to the pass, and a reference the parser does not recognise is
    kept as typed. The hearts are held as one while any hearts job is open. A
    set job holds no account playlist.
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
        # THE PARSER'S REFUSAL IS A ``ValueError``, and so is what the URL
        # parser itself raises over ``https://[::1``: either reference is kept
        # as typed, rather than ending the listing on a traceback.
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

    ``same_tracks`` names every OTHER open intake job of the library whose items
    are exactly this job's, newest first. Two copies of one 144 track list read
    as two unrelated jobs until this was said, at sitting 51.
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

    THE TRACK SET IS THE JOB'S ITEMS, the identifiers its worker resolves, so
    two jobs are copies only when they would do the same work. A job with no
    item is nobody's copy: an empty set equal to another empty set says nothing.
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
