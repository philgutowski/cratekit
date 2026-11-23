"""``crate acquire download`` and ``crate acquire audit``: the two acquisition shells.

Builders take an untyped ``entry`` so this file does not import the CLI registry
(KTD23).

``acquire.download`` declares no gate. It only adds files under the download staging
directory and reclaims its own empty staging directories, and the shell reaches no
network, so a gate would guard the one step that cannot cause the harm a gate is for.

The audit reads names and suffixes rather than opening files: the configured lossy
marker in a name is the durable fact R21 relies on, and the verb must answer on a slim
profile with no audio stack.
"""

from __future__ import annotations

import dataclasses
import os
import shutil
import time
from pathlib import Path
from typing import Any

from cratekit import acquire
from cratekit.acquire import download, match, match_cli, vendored
from cratekit.acquire.adapter import (
    FAILED_INVOCATIONS,
    AdapterSettings,
    InvocationOutcome,
    LosslessPolicy,
    LosslessRefused,
    TrackOutcome,
    TrackRequest,
    TrackResult,
)
from cratekit.cli.output import Envelope, load_config, no_job
from cratekit.core import config, jobs, naming, session
from cratekit.core.cause import Cause, CratekitError, Outcome, Scope, refuse
from cratekit.core.exit_codes import ExitCode, Remedy

# ---------------------------------------------------------------------------
# What a container can tell you about loss, and what it cannot
# ---------------------------------------------------------------------------

#: Containers that hold audio without loss.
LOSSLESS_EXTS: frozenset[str] = frozenset({".flac", ".aiff", ".aif", ".wav", ".alac"})

#: Containers that hold audio only after a lossy encode.
LOSSY_EXTS: frozenset[str] = frozenset({".mp3", ".aac", ".opus", ".ogg", ".webm"})

#: Audio suffixes neither set decides (today ``.m4a``, which holds ALAC or AAC). Derived
#: from ``naming.AUDIO_EXTS`` so a new format is reported unclassified rather than
#: silently counted lossless (P4).
UNDECIDED_EXTS: frozenset[str] = frozenset(naming.AUDIO_EXTS) - LOSSLESS_EXTS - LOSSY_EXTS

#: The queue name this report scopes itself to, so a consumer knows which set it reads.
AUDIT_QUEUE = "acquire.lossless"


# ---------------------------------------------------------------------------
# acquire.download
# ---------------------------------------------------------------------------


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    # Optional, because a resume reads the frozen list off the job (R-668).
    parser.add_argument(
        "list",
        nargs="?",
        default=None,
        help="the list of tracks to acquire; omit it with --job, which froze it",
    )
    parser.add_argument(
        "--job", default=None, metavar="JOB_ID",
        help="continue the acquisition already queued under this identifier",
    )
    parser.set_defaults(_handler=acquire_download)


def download_argv(job) -> list[str]:
    """The command line that continues one queued acquisition.

    No ``--run``, since the verb declares no gate, and no list, since the resume reads
    only the job (R-668).
    """
    return ["acquire", "download", "--job", job.job_id]


#: Payload keys. ``LIST`` is the frozen list path, the record of what was queued.
#: ``TRACKS`` is what the list said about each item, keyed by identifier, so the worker
#: reads nothing but the job (KTD9).
LIST = "list"
TRACKS = "tracks"

#: Where one item's download waits before the engine commits it. A dotfile, so the
#: folder walks of tagging and analysis skip an unfinished attempt.
ACQUIRE_STAGING_DIRNAME = ".cratekit-acquire-staging"

#: The pool's sleep, resolved at call time so a test can record the paced schedule.
_SLEEP = time.sleep

#: What a per-track outcome becomes on the item's row, in slugs this package reserves.
_ITEM_REASONS: dict[TrackOutcome, str] = {
    TrackOutcome.UNAVAILABLE_TRANSIENT: "unavailable-transient",
    TrackOutcome.UNAVAILABLE_PERMANENT: "unavailable-permanent",
    TrackOutcome.REFUSED_BY_POLICY: "lossy-refused",
}

#: What an invocation-level failure becomes; neither is a fact about the track.
_INVOCATION_REASONS: dict[InvocationOutcome, str] = {
    InvocationOutcome.AUTH_FAILED: "auth-failed",
    InvocationOutcome.ADAPTER_BROKEN: "adapter-broken",
}


def _unusable(message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        "intake-list-unusable", message, steps=steps, scope=Scope.RUN, origin=("acquire.cli",),
        detail=detail,
    )


def frozen_tracks(wanted: tuple[match.Wanted, ...]) -> dict[str, dict[str, str | None]]:
    """The items, as the list identifies them, in list order and folded once.

    An item is the provider's track identifier, the only key the adapter contract can
    fetch, so a list from anywhere but the provider is refused here rather than queued
    as items nothing can acquire. A row with no identifier refuses the whole list, since
    skipping it would report an unfinished list done. A repeated identifier folds to its
    first occurrence.
    """
    if not wanted:
        return {}
    origin = wanted[0].origin
    if origin != match.TIDAL:
        raise _unusable(
            f"this is a {origin} list, and acquiring needs the provider's own track "
            f"identifiers, which only a list fetched from the provider carries",
            "fetch the playlist from the provider into a list document first, "
            "then acquire that",
            "a pasted tracklist is matched against the library with match.run; "
            "its missing rows carry acquisition options, not identifiers",
            origin=origin,
        )
    missing = [
        position for position, track in enumerate(wanted, start=1) if not track.ref
    ]
    if missing:
        raise _unusable(
            f"{len(missing)} track(s) in this list carry no provider identifier "
            f"(positions {', '.join(str(p) for p in missing[:5])}"
            f"{', ...' if len(missing) > 5 else ''}), so nothing can ask the "
            f"provider for them",
            "fetch the list from the provider again so every row carries its id",
            positions=missing,
        )
    frozen: dict[str, dict[str, str | None]] = {}
    for track in wanted:
        frozen.setdefault(
            track.ref, {"artist": track.artist, "title": track.title, "isrc": track.isrc},
        )
    return frozen


def _same_list_or_refuse(named: str | None, job, handler_key: str) -> None:
    """Refuse a resume that names a list other than the one the job froze.

    The same list is accepted so a saved command line still drives (R-668); a different
    one is refused, because the person asked for two things that disagree. Paths are
    compared as the filesystem sees them, through
    :func:`cratekit.core.preflight.names_one_path`. Only this verb's own jobs are read,
    since another verb's payload may use the key differently.
    """
    if named is None or job.handler_key != handler_key:
        return
    frozen = str((job.payload or {}).get(LIST) or "")
    if not frozen:
        return
    try:
        given = Path(named).expanduser().absolute()
    except RuntimeError:
        given = Path(named).absolute()
    if session.names_one_path(given, Path(frozen)):
        return
    raise _unusable(
        f"job {job.job_id} acquires the list it froze, {frozen}, and this command "
        f"names {given}, so driving the job would not acquire the list named here",
        f"drop the list and run it with --job {job.job_id} alone",
        "or queue the other list as a job of its own by naming it without --job", job_id=job.job_id,
        frozen=frozen, named=str(given),
    )


def acquire_download(ctx) -> Envelope:
    """Read the list, freeze it, and queue one item per track. Or drive the job.

    The list is read through :func:`cratekit.acquire.match_cli.read_list`, so it accepts
    and refuses exactly what the match verb does. A list with no tracks queues nothing
    and says so. The staging sweep runs at the head of the verb, the one point where the
    queue knows which jobs are terminal and nothing is being written.
    """
    # Refused before anything runs: PRECONDITION, since USAGE is the parser's own code.
    if ctx.args.job is not None and not ctx.args.job.strip():
        raise _unusable(
            "--job was given an empty identifier, so it names no job to continue",
            "pass the identifier of the acquisition already queued",
            "or drop --job to queue the list as a new acquisition",
        )
    if ctx.args.list is None and ctx.args.job is None:
        raise _unusable(
            "no list was named and no job was given, so there is nothing to acquire",
            "name the list of tracks to acquire",
            "or continue an acquisition already queued with --job JOB_ID",
        )
    cfg = load_config(("acquire.cli",))
    with jobs.open_store() as store:
        if ctx.args.job:
            # Before the sweep and the reconcile, so a refused command changes nothing.
            _same_list_or_refuse(
                ctx.args.list, jobs.get(store, ctx.args.job), ctx.entry.handler_key
            )
        sweep_staging(Path(cfg.paths.download_staging), store)
        if ctx.args.job:
            job, warnings = drive_queued(ctx, store, ctx.args.job)
            return ctx.envelope(data=jobs.reported(store, job), warnings=warnings)
        # Read from the path as typed, so ``read_list`` can still refuse a pasted URL.
        job = queue_list(store, cfg, Path(str(ctx.args.list)), handler_key=ctx.entry.handler_key)
        if job is None:
            return ctx.envelope(data=no_job("no-tracks"), outcome=Outcome.NO_OP)
        return ctx.envelope(data=jobs.reported(store, job))


def queue_list(
    store: jobs.JobStore, cfg: config.Config, given: Path, *, handler_key: str,
    extra: dict[str, Any] | None = None,
) -> jobs.Job | None:
    """Read a list, freeze it, and queue one item per track, or None for no tracks.

    The one spelling of a download job, shared with the guided label sync (U108).
    ``extra`` is what a composing verb adds to the payload; the worker reads none of it.
    """
    wanted = match_cli.read_list(given)
    # Absolute, because a resumed child runs in another working directory.
    listed = given.expanduser().absolute()
    tracks = frozen_tracks(wanted)
    if not tracks:
        return None
    return jobs.enqueue(
        store, handler_key=handler_key,
        payload={**(extra or {}), LIST: str(listed), TRACKS: tracks}, cfg=cfg,
        item_ids=tuple(tracks),
    )


def drive_queued(ctx, store: jobs.JobStore, job_id: str) -> tuple[jobs.Job, tuple[dict[str, str], ...]]:
    """Drive one queued download in this process, and refuse unless it ended clean.

    Reconciles first, since a resume arrives after something stopped. Returns the job
    only when it succeeded or is still waiting; otherwise raises its own cause.
    """
    job = jobs.reconcile(store, job_id)
    warnings: tuple[dict[str, str], ...] = ()
    if job.is_open():
        if not jobs.items(store, job.job_id):
            # The zero item rule: a job with no items would report SUCCEEDED over a
            # list nothing acquired (R-198).
            raise refuse(
                "internal-error",
                f"job {job.job_id} has no items to run, so driving it "
                f"would report every track acquired over a list nothing "
                f"read. It was queued by a build that did not record "
                f"what its items were",
                remedy=Remedy.REPORT_DEFECT, origin=("acquire.cli",), detail={"job_id": job.job_id},
            )
        _, warnings = ctx.run_job(store, job)
        job = jobs.get(store, job.job_id)
    # Both below sit outside the ``is_open`` branch, so a finished job asked again
    # answers the same; a parked or partly failed job raises rather than reads ok
    # (R-290, R-225).
    warnings = (*warnings, *declined_warnings(store, job))
    jobs.raise_for_state(job)
    return job, warnings


# ---------------------------------------------------------------------------
# The worker
# ---------------------------------------------------------------------------


def staging_dir(root: Path, job_id: str, ordinal: int) -> Path:
    """The staging directory for one item of one job, cleared and recreated.

    Cleared because a killed attempt leaves a partial file the codec probe would take
    for the track.
    """
    directory = root / ACQUIRE_STAGING_DIRNAME / job_id / str(ordinal)
    if directory.exists():
        shutil.rmtree(directory)
    config.mkdir_private(directory)
    return directory


def _children(directory: Path) -> tuple[Path, ...]:
    """What is in ``directory``, sorted, or nothing when it cannot be listed."""
    try:
        return tuple(sorted(directory.iterdir()))
    except OSError:
        return ()


def _reclaim(directory: Path, removed: list[Path]) -> None:
    """Remove ``directory`` if it holds nothing, and record that it went.

    ``rmdir`` makes the emptiness check and the removal one decision beside a driver
    that may be writing. Any ``OSError`` means leave it for the next run.
    """
    try:
        directory.rmdir()
    except OSError:
        return
    removed.append(directory)


def sweep_staging(root: Path, store: jobs.JobStore) -> tuple[Path, ...]:
    """Reclaim the emptied staging directories of jobs that can no longer run (R-291).

    Empty directories only, so a refused landing kept as evidence survives. Terminal
    jobs only, since an open job's directories belong to work a resume may redo. A
    directory naming a job this store does not hold is left alone, as it may be another
    installation's. The queue is asked only about the directories present, because the
    queue only grows. Returns what it removed, deepest first within a job.
    """
    tree = root / ACQUIRE_STAGING_DIRNAME
    if not tree.is_dir():
        return ()
    present = [entry for entry in _children(tree) if entry.is_dir()]
    states = jobs.states_of(store, [entry.name for entry in present])
    removed: list[Path] = []
    for job_dir in present:
        if states.get(job_dir.name) not in jobs.TERMINAL_STATES:
            continue
        for item_dir in _children(job_dir):
            if item_dir.is_dir():
                _reclaim(item_dir, removed)
        _reclaim(job_dir, removed)
    return tuple(removed)


def request_for(item: jobs.Item, payload: dict[str, Any]) -> TrackRequest:
    """The item as a request: its identifier, and what the list said about it."""
    said = dict((payload.get(TRACKS) or {}).get(item.item_id) or {})
    return TrackRequest(
        key=item.item_id, artist=str(said.get("artist") or ""), title=str(said.get("title") or ""),
        isrc=str(said.get("isrc") or ""),
    )


def _remedy(token: object, fallback: Remedy | None) -> Remedy | None:
    """The adapter's remedy token as a CLI ``Remedy``, else ``fallback``.

    The fallback may be ``None``: a permanently unavailable track carries no remedy on
    purpose, and ``refuse`` then defaults it from the reason table.
    """
    if token is not None:
        return Remedy(str(token))
    return fallback


def _refused_invocation(run: download.DownloadRun, request: TrackRequest) -> CratekitError:
    invocation = run.invocation
    where = f" ({', '.join(invocation.alternatives)} can replace it)" if invocation.alternatives else ""
    return refuse(
        _INVOCATION_REASONS[invocation.outcome],
        f"{invocation.adapter} could not acquire {request.key}: {invocation.detail}{where}",
        remedy=_remedy(invocation.remedy, Remedy.SWITCH_ADAPTER), scope=Scope.SOURCE,
        retryable=invocation.outcome is InvocationOutcome.AUTH_FAILED, origin=("acquire.cli",),
        detail={
            "adapter": invocation.adapter, "key": request.key, "outcome": str(invocation.outcome),
            "alternatives": list(invocation.alternatives),
        },
    )


def _refused_track(result: TrackResult, adapter: str) -> CratekitError:
    transient = result.outcome is TrackOutcome.UNAVAILABLE_TRANSIENT
    # No fallback off the transient path: a policy refusal always carries its own
    # remedy, and a permanent unavailability carries none on purpose.
    return refuse(
        _ITEM_REASONS[result.outcome],
        f"{adapter} did not acquire {result.key}: {result.detail}",
        remedy=_remedy(result.remedy, Remedy.RETRY_LATER if transient else None),
        scope=Scope.ITEM,
        retryable=transient,
        origin=("acquire.cli",),
        detail={"adapter": adapter, "key": result.key, "outcome": str(result.outcome)},
    )


def checked_landing(path: Path, key: str, *, policy: LosslessPolicy) -> Path:
    """The landed FILE against the frozen policy, whichever adapter landed it.

    Checked here because the landed file check is optional for an adapter (R-213), and
    every landing passes this point. A lossy file is a policy refusal; an unreadable one
    is transient and re-queueable, being almost always a truncated download.
    """
    from cratekit.acquire import vendored  # noqa: PLC0415 - the probe imports the audio stack

    try:
        return vendored.landed_file(True, path, key, policy=policy)
    except LosslessRefused as exc:
        raise refuse(
            "lossy-refused", str(exc), remedy=_remedy(exc.remedy, Remedy.RELAX_LOSSLESS_POLICY),
            scope=Scope.ITEM, origin=("acquire.cli",), detail={"key": key, "path": str(path)},
        ) from exc
    except RuntimeError as exc:
        raise refuse(
            "unavailable-transient", str(exc), remedy=Remedy.RETRY_LATER, scope=Scope.ITEM,
            retryable=True, origin=("acquire.cli",), detail={"key": key, "path": str(path)},
        ) from exc


def lossy_landing(path: Path, *, policy: LosslessPolicy) -> bool:
    """Whether the file that landed is LOSSY, asked of the file itself.

    The provider's offer is not evidence about the bytes. Under STRICT,
    ``checked_landing`` already refused a lossy file, so the probe is skipped. A file
    the probe cannot read is not called lossy and is committed unmarked.
    """
    if policy is LosslessPolicy.STRICT:
        return False
    from cratekit.acquire import vendored  # noqa: PLC0415 - the probe imports the audio stack

    _name, lossless = vendored.codec_of(path)
    return lossless is False


def marked_name(landed: Path, marker: str, *, required: bool) -> str:
    """The name the file is committed under: the landed name, marked if it must be.

    R21 permits a lossy file only with the configured marker (S3), carried in the
    staging name because the naming engine reads it as the lossy flag. With no marker
    text the file is refused rather than committed unmarked.
    """
    if not required:
        return landed.name
    text = marker.strip()
    if not text:
        raise refuse(
            "lossy-refused",
            f"{landed.name} landed lossy under a policy that permits lossy only "
            f"when marked, and the configuration names no marker text, so it "
            f"cannot be marked and is not kept",
            remedy=Remedy.RELAX_LOSSLESS_POLICY,
            scope=Scope.ITEM,
            origin=("acquire.cli",),
            detail={"path": str(landed)},
        )
    return f"{landed.stem} {text}{landed.suffix}"


def handle(job, item, cfg) -> jobs.Produced:
    """Acquire ONE queued track. The per-item worker behind ``acquire.download``.

    Each answer lands on the item's row under its own slug:

    * a parked run parks the job on the pacing layer's cause, releasing this item;
    * a failed invocation names the replacement path;
    * a per-track result that is not an acquisition carries its outcome's slug;
    * an OK run with no result for this key is refused as transient, since absence is
      not evidence;
    * an acquisition is checked at the FILE under the frozen policy, then staged.

    ``cfg`` is the configuration the job was FROZEN against (KTD9), so settings edited
    while it waited do not apply. One request per call, since the engine claims one
    item at a time.

    A non-retryable ``REFUSED_BY_POLICY`` cause is declined, not failed (U169): the item
    is skipped and named by :func:`declined_warnings`, so the rest of the list ends ok.
    """
    try:
        return _acquire(job, item, cfg)
    except jobs.Parked:
        raise
    except CratekitError as exc:
        if refused_for_good(exc.cause):
            raise jobs.Declined(exc.cause) from exc
        raise


#: One session a drive, not one a track (U274): the engine enters the vendored
#: adapter's drive around each drive of a download job, see
#: :data:`cratekit.cli.handlers.PER_DRIVE_ATTRIBUTE`.
handle.per_drive = vendored.drive  # type: ignore[attr-defined]


def refused_for_good(cause: Cause) -> bool:
    """Whether a download's item refusal is the policy's permanent answer (U169).

    Read off the exit code so a later policy refusal is covered, and never retryable,
    since a skip is never re-armed.
    """
    return cause.code is ExitCode.REFUSED_BY_POLICY and not cause.retryable


#: The warning ``acquire download`` names a declined track under (U169).
DECLINED_WARNING = "acquire-refused"


def track_name(job: jobs.Job, item_id: str) -> str:
    """One track as its list named it: title by artist, else either, else the identifier."""
    tracks = (job.payload or {}).get(TRACKS) or {}
    said = tracks.get(item_id) if isinstance(tracks, dict) else None
    said = said if isinstance(said, dict) else {}
    title, artist = str(said.get("title") or ""), str(said.get("artist") or "")
    return f"{title} by {artist}" if title and artist else title or artist or item_id


def declined_warnings(store: jobs.JobStore, job: jobs.Job) -> tuple[dict[str, str], ...]:
    """One warning per track the job declined, named as its list named it.

    Read from the item rows, so the same job asked again answers the same.
    """
    found: list[dict[str, str]] = []
    for item in jobs.items(store, job.job_id):
        if item.state is not jobs.ItemState.SKIPPED or item.cause is None:
            continue
        found.append(
            {
                "code": DECLINED_WARNING,
                "message": (
                    f"{track_name(job, item.item_id)} ({item.item_id}) was not acquired "
                    f"and is skipped, refused for good ({item.cause.reason}): "
                    f"{item.cause.message}"
                ),
            }
        )
    return tuple(found)


@dataclasses.dataclass(frozen=True, slots=True)
class DownloadRead:
    """A download job after its drive, as every verb that lands one reads it (R-1115).

    ``done`` counts the tracks that landed. ``refused`` holds ``item_id``, ``reason``
    and ``message`` per track refused for good: declined (U169), or FAILED with a cause
    no retry can clear. ``failed`` names the second kind alone. ``settled`` says the
    download ended as one a tail may run on.
    """

    job: jobs.Job
    done: int
    refused: tuple[dict[str, Any], ...]
    failed: tuple[str, ...]
    settled: bool

    @property
    def landed(self) -> bool:
        """Settled with at least one track downloaded, so there is something to land."""
        return self.settled and self.done > 0


def read_download(store: jobs.JobStore, job: jobs.Job) -> DownloadRead:
    """Read a download job the one way ``sync land`` and ``label sync --go`` do (R-1115).

    Settled is SUCCEEDED, or FAILED with at least one failed item, every failure carrying
    a non-retryable cause, and no item left to run. Anything else did not settle, and
    the caller ends on the job's own refusal.
    """
    held = jobs.items(store, job.job_id)
    failed = [item for item in held if item.state is jobs.ItemState.FAILED]
    for_good = {
        item.item_id for item in failed if item.cause is not None and not item.cause.retryable
    }
    finished = (jobs.ItemState.DONE, jobs.ItemState.SKIPPED, jobs.ItemState.FAILED)
    settled = job.state is jobs.JobState.SUCCEEDED or (
        job.state is jobs.JobState.FAILED
        and bool(failed)
        and len(for_good) == len(failed)
        and all(item.state in finished for item in held)
    )
    refused = tuple(
        {"item_id": item.item_id, "reason": item.cause.reason, "message": item.cause.message}
        for item in held
        if item.cause is not None
        and (item.item_id in for_good or item.state is jobs.ItemState.SKIPPED)
    )
    return DownloadRead(
        job=job,
        done=sum(1 for item in held if item.state is jobs.ItemState.DONE),
        refused=refused,
        failed=tuple(item.item_id for item in failed if item.item_id in for_good),
        settled=settled,
    )


def _acquire(job, item, cfg) -> jobs.Produced:
    """The body of :func:`handle`, which says what each answer here becomes."""
    payload = dict(job.payload or {})
    settings = AdapterSettings.from_config(cfg)
    root = settings.download_staging
    per_item = dataclasses.replace(
        settings, download_staging=staging_dir(root, job.job_id, item.ordinal)
    )
    adapter = acquire.build(cfg.acquisition.adapter, per_item)
    request = request_for(item, payload)

    run = download.acquire_paced(adapter, (request,), sleep=_SLEEP)

    if run.parked is not None:
        raise jobs.Parked(run.parked)
    invocation = run.invocation
    if invocation.outcome in FAILED_INVOCATIONS:
        refusal = _refused_invocation(run, request)
        if invocation.outcome is InvocationOutcome.AUTH_FAILED:
            # Parked, not failed: failing would let the next item try the dead login
            # again, and repeated failed logins lock the account. A dead credential
            # is a fact about the run, so one resume after fixing it redoes the rest.
            raise jobs.Parked(refusal.cause)
        # A broken adapter still fails the item, since the tool may have broken on
        # this track, and parking would end a whole sync on one bad file (R-293).
        raise refusal
    result = next((r for r in invocation.results if r.key == request.key), None)
    if result is None:
        raise refuse(
            "unavailable-transient",
            f"{invocation.adapter} finished without reporting on {request.key}, "
            f"so nothing is known about it and it stays queued",
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
            origin=("acquire.cli",),
            detail={"adapter": invocation.adapter, "key": request.key},
        )
    if result.outcome is not TrackOutcome.ACQUIRED:
        raise _refused_track(result, invocation.adapter)

    landed = checked_landing(Path(str(result.path)), request.key, policy=per_item.lossless_policy)
    # The marker is owed if the offer or the file says so, since R21 is about the file.
    required = result.requires_lossy_marker or lossy_landing(
        landed, policy=per_item.lossless_policy
    )
    final = root / marked_name(landed, cfg.naming.lossy_marker or "", required=required)
    if final.exists():
        # Checked after the download, the only point the name is known. Refused rather
        # than replaced, since what is there may have been kept on purpose.
        raise refuse(
            "output-exists",
            f"{final} already exists, so the copy that just landed for "
            f"{request.key} was not put in its place; move or delete the "
            f"existing file and resume, or leave it and treat this item as done",
            origin=("acquire.cli",),
            detail={"path": str(final), "key": request.key, "landed": str(landed)},
        )
    return jobs.Produced(staged=landed, final=final)


# ---------------------------------------------------------------------------
# acquire.audit
# ---------------------------------------------------------------------------


def build_audit(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    parser.set_defaults(_handler=acquire_audit)


def classify(suffix: str) -> str:
    """``lossless``, ``lossy``, ``undecided``, or ``other`` (not audio) for one suffix."""
    if suffix in LOSSLESS_EXTS:
        return "lossless"
    if suffix in LOSSY_EXTS:
        return "lossy"
    if suffix in UNDECIDED_EXTS:
        return "undecided"
    return "other"


def findings(root: Path, *, policy: LosslessPolicy, marker: str) -> tuple[dict[str, Any], ...]:
    """Every file under ``root`` that the lossless policy does not admit.

    * ``lossy-under-strict``: a lossy file the strict policy says should not exist.
      Not ``lossy-refused``, which is a declared cause key.
    * ``lossy-unmarked``: a lossy file without the marker, the failure R21 prevents.
    * ``marked-lossless``: a lossless file carrying the marker, so two different files
      fold to one key.
    * ``format-undecided``: a container its suffix cannot classify.
    * ``path-unreadable``: a directory that could not be listed, so was not audited.

    An empty ``marker`` means no file carries one, so the marker kinds are not reported.
    ``os.walk`` with ``onerror`` is used because ``Path.rglob`` silently skips an
    unreadable directory, which would read as a clean report.
    """
    if not root.is_dir():
        return ()
    found: list[dict[str, Any]] = []
    unreadable: list[Path] = []

    def note(exc: OSError) -> None:
        unreadable.append(Path(exc.filename) if exc.filename else root)

    for dirpath, _dirnames, filenames in os.walk(root, onerror=note):
        here = Path(dirpath)
        for name in filenames:
            path = here / name
            kind = classify(path.suffix.lower())
            if kind == "other":
                continue
            marked = bool(marker) and marker in path.stem
            if kind == "undecided":
                found.append(_item(path, root, "format-undecided"))
            elif kind == "lossy":
                if policy is LosslessPolicy.STRICT:
                    found.append(_item(path, root, "lossy-under-strict"))
                elif marker and not marked:
                    found.append(_item(path, root, "lossy-unmarked"))
            elif marked:
                found.append(_item(path, root, "marked-lossless"))
    found += [_item(path, root, "path-unreadable") for path in unreadable]
    return tuple(sorted(found, key=lambda item: (item["id"], item["kind"])))


def _item(path: Path, root: Path, kind: str) -> dict[str, Any]:
    """One finding projected for a listing, its path relative to the root (R1)."""
    try:
        where = str(path.relative_to(root))
    except ValueError:
        # Unreachable through ``findings``; handled so a report never raises.
        where = path.name
    return {"id": where, "queue": AUDIT_QUEUE, "kind": kind, "suffix": path.suffix.lower()}


def acquire_audit(ctx) -> Envelope:
    """Report what the lossless policy does not admit. Writes nothing.

    ``unresolved`` equals the length of ``items`` only because nothing pages; a flag
    returning a subset must count it from the walk, never the page.
    """
    cfg = load_config(("acquire.cli",))
    found = findings(
        cfg.library.root / cfg.library.music_dir,
        policy=LosslessPolicy(cfg.acquisition.lossless_policy),
        marker=(cfg.naming.lossy_marker or "").strip(),
    )
    return ctx.envelope(
        data={
            "queue": AUDIT_QUEUE,
            "items": list(found),
            "unresolved": len(found),
        }
    )


__all__ = [
    "ACQUIRE_STAGING_DIRNAME", "AUDIT_QUEUE", "LIST", "LOSSLESS_EXTS", "LOSSY_EXTS", "TRACKS",
    "UNDECIDED_EXTS", "acquire_audit", "acquire_download", "build", "build_audit",
    "checked_landing", "classify", "download_argv", "drive_queued", "findings", "frozen_tracks",
    "DECLINED_WARNING", "DownloadRead", "declined_warnings", "handle", "refused_for_good",
    "marked_name", "queue_list", "read_download", "request_for", "staging_dir", "sweep_staging",
    "track_name",
]
