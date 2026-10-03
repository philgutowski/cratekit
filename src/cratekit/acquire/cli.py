"""``crate acquire download`` and ``crate acquire audit``: the two acquisition shells.

U15 landed the acquisition ENGINES and never landed a shell, so Feature
Inventory rows 6 and 7 sat uncovered while the registry declared both verbs
against a closed unit. U42 landed the shells, and U54 landed the WORKER behind
the download verb, ``handle`` below, which is the first thing in the product to
construct an adapter through the registry and to drive the paced pool (R-203,
R-204). Nothing here re-decides what the registry already declares.

Builders take an untyped ``entry`` so this file does not import the CLI registry
(KTD23).

**Why ``acquire.download`` declares no gate, decided here rather than inherited.**
The house pattern for a destructive verb is a confirm gate against a plan digest,
and ``export.playlist`` beside it has one. The distinction that separates them is
the one ``run_backup`` and ``run_restore`` are separated on: this verb ADDS files
into the configured download staging directory, replaces nothing, and publishes
nothing outward. The one thing it removes is its own litter, and the argument
survives that: :func:`sweep_staging` reclaims EMPTY directories under this
product's own staging tree, never a file and never anything a person put there.
An accidental run costs network time and disk, both of which a person can simply
delete. ``export.playlist`` is gated
because it writes to a remote service, which is an act the user cannot take back.

The provider-side cost is the real argument for a gate and it does not survive
contact with what this shell does: an unpaced run can get a credentialed account
blocked, but the pacing apparatus in :mod:`cratekit.acquire.download` is what
manages that, and the shell reaches no network at all. It reads a list, freezes
it, and queues; the worker is what reaches the provider, and it does so under
the frozen pacing. So the gate would guard the one step in the verb that cannot
cause the harm the gate is for.

Declining it also keeps the verb out of ``tests/test_queued_resume_contract.py``'s
derived population, which is a consequence rather than a reason: an explicit gate
plus ``long_running`` plus an ``argv_builder`` obliges the resume argv to carry
``--run`` with the frozen gate run, and that machinery would exist here purely to
guard an add-only local write.

**Why the audit reads NAMES and containers rather than opening files.** R21 makes
a lossy copy carry a marker inside its name, config owns the marker text (S3),
and :func:`cratekit.acquire.match_cli.library_template` already hands that text to
the naming engine so the marked copy and its lossless twin fold to one recording.
That marker is therefore the durable on-disk fact about a file's losslessness, and
it is the one this verb audits. The alternative, opening every file to read its
codec, needs the audio stack: this verb declares no doctor check and no module
toggle, so it has to answer on a slim profile that has no such stack installed.
"""

from __future__ import annotations

import dataclasses
import os
import shutil
import time
from pathlib import Path
from typing import Any

from cratekit import acquire
from cratekit.acquire import download, match, match_cli
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
from cratekit.cli.output import Envelope
from cratekit.core import config, jobs, naming, preflight
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, Scope, refuse
from cratekit.core.exit_codes import Remedy

# ---------------------------------------------------------------------------
# What a container can tell you about loss, and what it cannot
# ---------------------------------------------------------------------------

#: Containers that hold audio without loss.
LOSSLESS_EXTS: frozenset[str] = frozenset({".flac", ".aiff", ".aif", ".wav", ".alac"})

#: Containers that hold audio only after a lossy encode.
LOSSY_EXTS: frozenset[str] = frozenset({".mp3", ".aac", ".opus", ".ogg", ".webm"})

#: Containers the SUFFIX cannot decide, DERIVED as the remainder of the renamer's
#: own audio table rather than listed. Today that remainder is exactly ``.m4a``,
#: because ALAC and AAC ship inside the same MP4 container, so the suffix names a
#: file that may be either and only opening it answers which.
#:
#: The derivation is the point and a third literal would have defeated it. A
#: format added to ``naming.AUDIO_EXTS`` and to neither set above lands here on
#: its own and is REPORTED as unclassified, where a hand-kept list would have let
#: it fall out of the sweep silently. Unclassified is the safe default because a
#: sweep that quietly counted an unknown container as lossless would report a
#: clean library over files it never classified, which is the merge bar's "shown a
#: clean report over state the tool could not read" exactly (P4).
UNDECIDED_EXTS: frozenset[str] = frozenset(naming.AUDIO_EXTS) - LOSSLESS_EXTS - LOSSY_EXTS

#: The queue name this report scopes itself to. Named rather than a bare string
#: for the reason :mod:`cratekit.cli.review` names its own: a consumer reading an
#: unlabelled queue field has no way to tell which set it is looking at.
AUDIT_QUEUE = "acquire.lossless"


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("acquire.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _reported(store, job) -> dict:
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": jobs.progress(store, job.job_id),
    }


# ---------------------------------------------------------------------------
# acquire.download
# ---------------------------------------------------------------------------


def build(parser, entry) -> None:
    """Declare the surface. ``entry`` is untyped so this layer does not name it."""
    del entry
    # OPTIONAL, because a resume has no use for it (R-668). The job froze the
    # list's absolute path and every track the list named, so the list on disk
    # is read once, at the queue, and never again. Requiring it on ``--job``
    # made a person continuing a job by hand type the path a second time.
    parser.add_argument(
        "list",
        nargs="?",
        default=None,
        help="the list of tracks to acquire; omit it with --job, which froze it",
    )
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the acquisition already queued under this identifier",
    )
    parser.set_defaults(_handler=acquire_download)


def download_argv(job) -> list[str]:
    """The command line that continues one queued acquisition.

    No ``--run`` here, and its absence is a decision rather than an omission. The
    flag exists to carry a frozen gate run back into the respawned child, and this
    verb declares no gate, so there is nothing to carry. The module docstring says
    why it declares none.

    NO LIST EITHER, since R-668. The resume reads the job and nothing else, and
    this argv is also the "drive it with" line a person is shown when the job is
    queued, so a list here would teach them to type a path the verb ignores.
    """
    return ["acquire", "download", "--job", job.job_id]


#: Payload keys. ``LIST`` is the frozen list path, which the resume no longer
#: needs since R-668: it is the record of what was queued, and what a list named
#: beside ``--job`` is checked against.
#: ``TRACKS`` is what the list SAID about each item, keyed by the item identifier,
#: so the worker reads nothing off disk but the job (KTD9): a list edited between
#: queueing and driving cannot change what a queued item means.
LIST = "list"
TRACKS = "tracks"

#: Where one item's download lands before the engine commits it. A dotfile
#: under the configured staging root, for the reason ``master`` gives for its
#: own: whatever is in it belongs to an attempt that did not finish, and the
#: folder walks that queue tagging and analysis skip dotfiles.
ACQUIRE_STAGING_DIRNAME = ".cratekit-acquire-staging"

#: The sleep the paced pool waits with, resolved at CALL time so a test can put a
#: recorder in front of it and read the schedule the frozen configuration
#: produced. ``download.acquire_concurrently`` binds ``time.sleep`` as a default
#: at definition time, which cannot be reached any other way.
_SLEEP = time.sleep

#: What a per-track outcome becomes on the item's row. The slugs are the ones
#: this package already reserves for the same facts: intake raises
#: ``lossy-refused`` for the identical policy decision, and the two unavailable
#: slugs are the outcome vocabulary's own names.
_ITEM_REASONS: dict[TrackOutcome, str] = {
    TrackOutcome.UNAVAILABLE_TRANSIENT: "unavailable-transient",
    TrackOutcome.UNAVAILABLE_PERMANENT: "unavailable-permanent",
    TrackOutcome.REFUSED_BY_POLICY: "lossy-refused",
}

#: What an invocation-level failure becomes. Both are the adapter saying it
#: cannot run at all, and neither is a fact about the track.
_INVOCATION_REASONS: dict[InvocationOutcome, str] = {
    InvocationOutcome.AUTH_FAILED: "auth-failed",
    InvocationOutcome.ADAPTER_BROKEN: "adapter-broken",
}


def _unusable(message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        "intake-list-unusable",
        message,
        steps=steps,
        scope=Scope.RUN,
        origin=("acquire.cli",),
        detail=detail,
    )


def frozen_tracks(wanted: tuple[match.Wanted, ...]) -> dict[str, dict[str, str | None]]:
    """The items, as the list identifies them, in list order and folded once.

    THE ITEM IS THE PROVIDER'S TRACK IDENTIFIER, which is the one thing the
    adapter contract can be asked for: ``TrackSource.offer`` and ``fetch`` take a
    key, and there is no search. Only a list the provider wrote carries one, in
    ``Wanted.ref``. A pasted tracklist and a list from another service name a
    recording and not a provider row, so they are refused HERE, at the queue,
    rather than queued as items nothing can ever acquire, which is R-198's empty
    queue wearing a full one's clothes. What acquires those is the match verb's
    acquisition options, which this build has no adapter call for.

    A row the provider wrote without an identifier is refused by position for
    the same reason, and the whole list is refused rather than the row skipped:
    a queue that quietly dropped a row would report every item done over a list
    it did not finish.

    THE SAME IDENTIFIER TWICE FOLDS TO ONE ITEM, first occurrence wins. The
    queue keys items by identifier, so a repeat is an insert that cannot land,
    and a playlist with one track in it twice asks for one file.
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
            track.ref,
            {"artist": track.artist, "title": track.title, "isrc": track.isrc},
        )
    return frozen


def _no_op(state: str) -> dict[str, Any]:
    return {"job_id": "", "state": state, "cause": None, "progress": {}}


def _same_list_or_refuse(named: str | None, job, handler_key: str) -> None:
    """Refuse a resume that names a list other than the one the job froze.

    A list named beside ``--job`` is read by nothing, since the job carries every
    track it will acquire. Accepting the SAME list keeps the form every build
    before R-668 required, and a command line somebody saved still drives. A
    DIFFERENT one is refused rather than ignored, for the reason ``review
    resolve`` refuses an item and a predicate together: the person asked for two
    things that disagree, and driving the job would tell them their list was
    acquired when a different one was.

    SAME AS THE FILESYSTEM SEES IT, not as two strings. The named path goes
    through the ``expanduser().absolute()`` the queue froze it with, and then
    through :func:`cratekit.core.preflight._names_one_path`, because a string
    comparison refuses the frozen list whenever it is spelled another way:
    ``/tmp`` against ``/private/tmp`` on macOS, a case variant on a case
    insensitive volume, a symlinked directory. A home directory that cannot be
    expanded names nothing the queue could have frozen, so it is compared as
    typed and disagrees.

    ONLY THIS VERB'S OWN JOBS are read. Another verb's payload may use the same
    key for something else, and a refusal telling somebody what a job of theirs
    "acquires" would be false about a job that acquires nothing. A job whose
    payload names no list has nothing to disagree with, and the resume path's
    zero item rule already answers for the only download jobs shaped that way.
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
    if preflight._names_one_path(given, Path(frozen)):
        return
    raise _unusable(
        f"job {job.job_id} acquires the list it froze, {frozen}, and this command "
        f"names {given}, so driving the job would not acquire the list named here",
        f"drop the list and run it with --job {job.job_id} alone",
        "or queue the other list as a job of its own by naming it without --job",
        job_id=job.job_id,
        frozen=frozen,
        named=str(given),
    )


def acquire_download(ctx) -> Envelope:
    """Read the list, freeze it, and queue one item per track. Or drive the job.

    THE LIST IS READ HERE, which reverses what this shell did until U54 and the
    reason is the zero item rule: the queue holds a job with nothing to claim
    unless the shell names the items, and the items are the list's tracks. The
    read goes through :func:`cratekit.acquire.match_cli.read_list`, the one list
    reader the product has, so a list this verb accepts is exactly a list the
    match verb accepts and the refusals are the same sentences.

    A list that reads to no tracks queues nothing and says so, following the
    analysis verbs: an explicitly empty document has said something, and it is
    not an error.

    THE STAGING SWEEP RUNS AT THE HEAD OF THE VERB, before the queue and resume
    paths part, because both of them reach the same tree and neither one is the
    right place to reclaim it. A worker cannot clean up after itself: the engine
    commits the staged landing AFTER ``handle`` returns, so at the only moment
    the worker is still running the directory is not yet empty. Nor is the end
    of a drive, because the job it just finished is one job and the tree holds
    every job ever run. The head of the verb is the point where the queue can
    say which jobs are terminal and nothing is being written.
    """
    # A COMMAND THAT NAMES NOTHING IS REFUSED BEFORE ANYTHING RUNS, as argparse
    # refused it while the list was required: no configuration read, no queue
    # opened, no staging swept. PRECONDITION rather than USAGE, because USAGE is
    # the parser's own code and no verb may produce it. ``--job ""`` is refused
    # here too, since it names no job, and read by truthiness it used to fall
    # through to the queueing path and queue the named list a second time.
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
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            # CHECKED BEFORE THE SWEEP AND THE RECONCILE, so a refused command
            # leaves the queue exactly as it found it.
            _same_list_or_refuse(
                ctx.args.list, jobs.get(store, ctx.args.job), ctx.entry.handler_key
            )
        sweep_staging(Path(cfg.paths.download_staging), store)
        if ctx.args.job:
            job, warnings = drive_queued(ctx, store, ctx.args.job)
            # THE VERB R-290 WAS FOUND ON. This worker is the one that parks, on
            # a provider block or a dead session, and the park reached this
            # report as ``ok`` with exit 0, legible only inside ``data.cause``. A
            # list where one track landed and another did not did the same
            # (R-225). OUTSIDE ``drive_queued``'s ``is_open`` branch, so a job already failed on
            # entry is answered the same way however many times it is asked.
            jobs.raise_for_state(job)
            return ctx.envelope(data=_reported(store, job), warnings=warnings)
        # READ FROM THE PATH AS TYPED, freeze it absolute. ``read_list`` refuses a
        # pasted URL by matching a scheme at the front of the string, and
        # ``expanduser().absolute()`` turns ``https://...`` into a relative path
        # under the working directory, which that guard cannot see. Absolutising
        # before the read swapped the sentence telling somebody to fetch the
        # playlist into a list document for a file-not-found over a mangled path.
        job = queue_list(store, cfg, Path(str(ctx.args.list)), handler_key=ctx.entry.handler_key)
        if job is None:
            return ctx.envelope(data=_no_op("no-tracks"), outcome=Outcome.NO_OP)
        return ctx.envelope(data=_reported(store, job))


def queue_list(
    store: jobs.JobStore,
    cfg: config.Config,
    given: Path,
    *,
    handler_key: str,
    extra: dict[str, Any] | None = None,
) -> jobs.Job | None:
    """Read a list, freeze it, and queue one item per track, or None for no tracks.

    THE ONE SPELLING OF A DOWNLOAD JOB, which ``acquire download`` and the
    guided label sync's go both queue through (U108), so a job the go queued
    is a job ``acquire download --job`` drives and ``job resume`` respawns.
    ``extra`` is what a composing verb adds to the payload beside the list and
    its tracks; the worker reads neither key of it.
    """
    wanted = match_cli.read_list(given)
    # ABSOLUTE, for the reason ``master`` freezes its recording absolute: the
    # child a resume spawns inherits the resuming process's directory, and a
    # relative path would name a different file there.
    listed = given.expanduser().absolute()
    tracks = frozen_tracks(wanted)
    if not tracks:
        return None
    return jobs.enqueue(
        store,
        handler_key=handler_key,
        payload={**(extra or {}), LIST: str(listed), TRACKS: tracks},
        cfg=cfg,
        item_ids=tuple(tracks),
    )


def drive_queued(ctx, store: jobs.JobStore, job_id: str) -> tuple[jobs.Job, tuple[dict[str, str], ...]]:
    """Drive one queued download in this process and return it as it ended.

    RECONCILE FIRST. A resume arrives after something stopped, and a claim left
    behind by a driver that died is state the queue cannot see for itself. A
    job already terminal is returned as it stands. The caller decides what its
    state means, through ``jobs.raise_for_state`` as this verb does.
    """
    job = jobs.reconcile(store, job_id)
    warnings: tuple[dict[str, str], ...] = ()
    if job.is_open():
        if not jobs.items(store, job.job_id):
            # THE ZERO ITEM RULE ON THE RESUME SIDE, which ``adopt`` and
            # ``tagging`` both guard and ``master`` does not need because
            # it always queues exactly one item. A job queued by a build
            # before this unit carries a frozen list path and no items at
            # all, and driving it reports SUCCEEDED over a list nothing
            # acquired, which is R-198's empty queue wearing a full one's
            # clothes.
            raise refuse(
                "internal-error",
                f"job {job.job_id} has no items to run, so driving it "
                f"would report every track acquired over a list nothing "
                f"read. It was queued by a build that did not record "
                f"what its items were",
                remedy=Remedy.REPORT_DEFECT,
                origin=("acquire.cli",),
                detail={"job_id": job.job_id},
            )
        _, warnings = ctx.run_job(store, job)
        job = jobs.get(store, job.job_id)
    return job, warnings


# ---------------------------------------------------------------------------
# The worker
# ---------------------------------------------------------------------------


def staging_dir(root: Path, job_id: str, ordinal: int) -> Path:
    """The staging directory for one item of one job, cleared and recreated.

    Cleared because whatever is in it belongs to an attempt that did not finish:
    the wrapped tool writes straight into the directory it is given, so a kill
    mid download leaves a partial file that a later attempt would otherwise
    hand to the codec probe as the track.
    """
    directory = root / ACQUIRE_STAGING_DIRNAME / job_id / str(ordinal)
    if directory.exists():
        shutil.rmtree(directory)
    config._mkdir_private(directory)
    return directory


def _children(directory: Path) -> tuple[Path, ...]:
    """What is in ``directory``, sorted, or nothing when it cannot be listed.

    A directory the sweep cannot read is one it has nothing to say about, and
    the caller's answer to both is identical: walk past it. This is NOT absence
    read as evidence of absence, because nothing downstream concludes the
    directory is empty; ``_reclaim`` still asks the filesystem itself before
    anything is removed.
    """
    try:
        return tuple(sorted(directory.iterdir()))
    except OSError:
        return ()


def _reclaim(directory: Path, removed: list[Path]) -> None:
    """Remove ``directory`` if it holds nothing, and record that it went.

    ``rmdir`` RATHER THAN A LISTING AND A DELETE, because the emptiness check
    and the removal have to be one decision. A listing that came back empty is a
    fact about the moment it was taken, and the sweep runs beside a driver that
    is allowed to be writing into the same tree.

    Every ``OSError`` reads the same way here, LEAVE IT. A directory holding an
    evidence file answers ``ENOTEMPTY`` and one on a volume this process cannot
    write to answers ``EACCES``, and the right response to both is to walk past
    it and try again on the next run. Nothing is reported, because nothing was
    lost and there is no decision for a person to make.
    """
    try:
        directory.rmdir()
    except OSError:
        return
    removed.append(directory)


def sweep_staging(root: Path, store: jobs.JobStore) -> tuple[Path, ...]:
    """Reclaim the emptied staging directories of jobs that can no longer run.

    R-291: ``staging_dir`` clears a directory on the NEXT attempt at the same
    job and ordinal, so nothing ever removed one. A successful commit moves the
    landing out and leaves the directory behind, one per item of every job ever
    run, under the download staging root for good.

    EMPTY DIRECTORIES ONLY, and the file left inside one is the reason. A
    landing ``checked_landing`` refused stays where it is on purpose, because it
    is the evidence for diagnosing the next demotion, and a sweep that deleted
    it would trade one defect for a worse one. ``_reclaim`` therefore asks the
    filesystem to remove a directory rather than asking whether it is empty, so
    the deliberate part survives without this function ever having to know which
    files are deliberate.

    ONLY A TERMINAL JOB, because nothing moves out of one. An open job's
    directories belong to work a resume is still entitled to redo, and an item
    claimed by a driver running right now is writing into one of them.

    A DIRECTORY NAMING A JOB THIS STORE DOES NOT HOLD IS LEFT ALONE. No code
    path in this product deletes a job row, so an unresolvable identifier means
    the tree and the queue are not from the same installation, and removing
    another store's staging on that reading is the one mistake here that would
    cost somebody a file. Recorded rather than swept.

    THE QUEUE IS ASKED ABOUT THE DIRECTORIES THAT ARE THERE, through
    ``jobs.states_of``, rather than asked for every terminal job it holds. The
    tree is small and the queue only grows, so the other direction makes a verb
    that runs in milliseconds pay for the whole history of the installation:
    measured at 224 ms on a store of 2000 succeeded jobs, each freezing a two
    hundred track list, because ``list_jobs`` decodes every payload it returns.

    Returns what it removed, deepest first within a job, so a caller that wants
    to report or assert on the sweep can. The callers today want neither.
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
        key=item.item_id,
        artist=str(said.get("artist") or ""),
        title=str(said.get("title") or ""),
        isrc=str(said.get("isrc") or ""),
    )


def _remedy(token: object, fallback: Remedy | None) -> Remedy | None:
    """The adapter's remedy token in the CLI's vocabulary, which it already is by
    reservation; the fallback is for a result that carried none.

    THE FALLBACK MAY BE ``None``, and that is the point of it being a parameter.
    ``adapter._unavailable`` leaves the remedy off a permanently unavailable
    track deliberately, because there is nothing a person can do about a track
    the provider no longer has, and a fallback that filled that absence in would
    tell them to relax the lossless policy over a delisted track. An absent
    remedy is passed on absent, and ``refuse`` then defaults it from the reason
    table, which is the answer the whole class of failure already declares.
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
        remedy=_remedy(invocation.remedy, Remedy.SWITCH_ADAPTER),
        scope=Scope.SOURCE,
        retryable=invocation.outcome is InvocationOutcome.AUTH_FAILED,
        origin=("acquire.cli",),
        detail={
            "adapter": invocation.adapter,
            "key": request.key,
            "outcome": str(invocation.outcome),
            "alternatives": list(invocation.alternatives),
        },
    )


def _refused_track(result: TrackResult, adapter: str) -> CratekitError:
    transient = result.outcome is TrackOutcome.UNAVAILABLE_TRANSIENT
    # NO FALLBACK OFF THE TRANSIENT PATH. A policy refusal always carries its own
    # remedy, which the ``TrackResult`` validator enforces, so the only outcome
    # that can reach a fallback here is a permanently unavailable track, and that
    # one carries none on purpose.
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

    The vendored source already runs this check inside its ``fetch``, and the
    check is run again here for two reasons that each stand alone. The contract
    says checking the landed file is OPTIONAL for an implementation, so the
    alternative adapter lands what it lands (R-213) and a fake in the suite
    lands whatever it is told to; this is the one place every adapter's landing
    passes through. And the rule the check enforces is the product's central
    promise, which the item's row is the thing that records.

    Two refusals, different remedies, and the difference is what the person is
    told to do. A lossy file is a policy refusal naming the codec, and relaxing
    the policy would admit it. A file nothing could read is a transient failure
    that stays re-queueable, because it is almost always a truncated download,
    and telling that person to relax the policy would make the product accept it.
    """
    from cratekit.acquire import vendored  # noqa: PLC0415 - the probe imports the audio stack

    try:
        return vendored.landed_file(True, path, key, policy=policy)
    except LosslessRefused as exc:
        raise refuse(
            "lossy-refused",
            str(exc),
            remedy=_remedy(exc.remedy, Remedy.RELAX_LOSSLESS_POLICY),
            scope=Scope.ITEM,
            origin=("acquire.cli",),
            detail={"key": key, "path": str(path)},
        ) from exc
    except RuntimeError as exc:
        raise refuse(
            "unavailable-transient",
            str(exc),
            remedy=Remedy.RETRY_LATER,
            scope=Scope.ITEM,
            retryable=True,
            origin=("acquire.cli",),
            detail={"key": key, "path": str(path)},
        ) from exc


def lossy_landing(path: Path, *, policy: LosslessPolicy) -> bool:
    """Whether the file that landed is LOSSY, asked of the file itself.

    THE OFFER IS NOT EVIDENCE ABOUT THE FILE. ``requires_lossy_marker`` is
    derived from what the provider said it was about to send, and the whole
    reason the codec check exists is that the provider's claim and the bytes
    that arrive are different facts: the setting said lossless, the provider
    sent AAC, and nothing between them ever looked. Under the STRICT policy
    ``checked_landing`` has already refused a lossy file, so there is nothing
    left to ask and the probe is not run twice. Under a permissive policy the
    file is kept either way, and the only remaining question is whether it must
    be MARKED, which R21 answers about the file and not about the offer.

    A file the probe cannot read answers nothing, so it is not called lossy on
    the strength of a failed measurement. It is committed unmarked exactly as it
    was before, and that gap is recorded rather than closed here, because
    refusing an unreadable file under a policy that exists to keep files is a
    different decision from this one.
    """
    if policy is LosslessPolicy.STRICT:
        return False
    from cratekit.acquire import vendored  # noqa: PLC0415 - the probe imports the audio stack

    _name, lossless = vendored.codec_of(path)
    return lossless is False


def marked_name(landed: Path, marker: str, *, required: bool) -> str:
    """The name the file is committed under: the landed name, marked if it must be.

    R21 permits a lossy file only WITH the marker, and config owns the marker's
    text (S3). The marker goes into the STAGING name because the staging name is
    the only thing that travels with the file into the library stages, and the
    naming engine reads a marked stem as the lossy flag. A configuration that
    names no marker text cannot express a legal lossy landing at all, so the
    file is refused rather than committed unmarked, which is the one state the
    audit verb exists to find.
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

    THE FIRST CALLER of ``acquire.build`` and of ``download.acquire_paced``, so
    every answer the run can give is read here rather than assumed, and each one
    lands on the item's row under its own slug:

    * a parked run is the provider refusing the CLIENT, and the job is parked on
      the cause the pacing layer built, with this item released, so no further
      request is made into a block;
    * a failed invocation is the adapter unable to run at all, and names the
      replacement path;
    * a per-track result that is not an acquisition carries the outcome's own
      slug and remedy;
    * a run that reports OK with no result for this key is refused as transient
      rather than read as success, because absence is not evidence;
    * an acquisition is checked at the FILE under the frozen policy, then staged
      for the engine to commit.

    ``cfg`` is the configuration this job was FROZEN against (KTD9). The adapter
    settings, the policy and the pacing are all read off it and nothing here
    loads a fresh one, so a pacing delay edited while the job waited is not the
    delay this run uses.

    ONE REQUEST PER CALL, because the engine claims one item at a time. The pool
    still paces every request through the frozen delay, so a job of fifty items
    is fifty paced requests; what the item granularity cannot express is
    ``concurrency`` above one, and that is recorded rather than worked around.
    """
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
            # PARKED, NOT FAILED, and only this one of the two. This worker
            # builds an adapter and authenticates inside every item, so failing
            # the item lets the driver claim the next one, which logs in again:
            # a two hundred track list against an expired session becomes two
            # hundred failed logins into one account, and repeated failed logins
            # are what triggers the lockout the module docstring records as
            # unrecoverable. A dead credential is also a fact about the RUN and
            # never about the track, so nothing is lost by stopping. The item is
            # released and the job records why, so one resume after fixing the
            # credential redoes the whole remainder.
            raise jobs.Parked(refusal.cause)
        # A BROKEN ADAPTER STILL FAILS THE ITEM, deliberately and asymmetrically.
        # A tool that crashed mid transfer may have crashed on this track, and
        # the unit's brief asks for exactly that: the item fails, the job stays
        # resumable, and the resume redoes only it. The rebuild it costs per item
        # is recorded rather than fixed by parking, because parking here would
        # end a fifty track sync on one bad file.
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
    # THE OFFER OR THE FILE, whichever says the marker is owed. The offer's claim
    # is what the provider intended to send and the probe is what arrived, and
    # R21 is a rule about the file on disk. Trusting the claim alone commits an
    # unmarked lossy file whenever the provider offers lossless and lands lossy,
    # which is the one state the audit verb exists to find.
    required = result.requires_lossy_marker or lossy_landing(
        landed, policy=per_item.lossless_policy
    )
    final = root / marked_name(landed, cfg.naming.lossy_marker or "", required=required)
    if final.exists():
        # AFTER the download rather than before it, and that ordering is a cost
        # this unit records rather than a choice it made: the file's name is the
        # tool's to decide and is known only once it has landed. Refused rather
        # than replaced, for the reason ``master`` refuses: what is there may
        # have been kept on purpose, and the fresh copy is in this attempt's
        # staging directory until the next attempt clears it.
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
    """``lossless``, ``lossy``, ``undecided``, or ``other`` for one lowercase suffix.

    ``other`` is everything that is not audio at all, which a music directory
    holds plenty of. It is a fourth answer rather than a silent skip so that the
    walk below reads as a classification of every file it saw.
    """
    if suffix in LOSSLESS_EXTS:
        return "lossless"
    if suffix in LOSSY_EXTS:
        return "lossy"
    if suffix in UNDECIDED_EXTS:
        return "undecided"
    return "other"


def findings(root: Path, *, policy: LosslessPolicy, marker: str) -> tuple[dict[str, Any], ...]:
    """Every file under ``root`` that the lossless policy does not admit.

    Four kinds, and each one is a state R21 forbids rather than a preference:

    * ``lossy-under-strict``: a lossy file under the strict policy, which says a
      track that exists only lossy is reported unacquired rather than downloaded.
      The marker is irrelevant here; strict means the file should not be present.
      NOT called ``lossy-refused``, which is what it said first: that string is
      already a declared CAUSE key, raised by
      :func:`cratekit.intake.pipeline.acquire_lossy_or_refuse` for the same policy
      at acquisition time. A cause key carries a remedy and an exit code; a
      finding kind is payload data with neither, and one string meaning both is
      the "one symbol meaning two things in two modules" METHOD lists among the
      things a green suite cannot see. The suite that noticed is
      ``test_reserved_causes``, and it noticed by counting rather than by knowing.
    * ``lossy-unmarked``: a lossy file under the permissive policy without the
      marker. This is the single failure R21 exists to prevent, because the
      marker is what a later stage strips to fold a lossy copy and its lossless
      twin into one recording.
    * ``marked-lossless``: a lossless file carrying the marker, which is the same
      failure wearing the opposite hat. The marker is false, the naming engine
      strips it anyway, and two genuinely different files fold to one key.
    * ``format-undecided``: a container whose suffix cannot answer the question.
      Reported rather than assumed, because a clean report over an unclassified
      file is worse than a report that says it could not tell.
    * ``path-unreadable``: a directory under the root that could not be listed.
      Not a policy violation, and reported for the same reason as the kind above
      it: a sweep that cannot see a directory has not audited it.

    ``marker`` empty means the configuration declares no marker text, so no file
    carries one. The two marker-dependent kinds cannot be decided in that state
    and are not reported, which is the same answer ``library_template`` gives when
    it returns a template with no marker rule rather than refusing the run.

    **WHY ``os.walk`` WITH AN ERROR HOOK AND NOT ``Path.rglob``.** This was
    written with ``rglob`` first, and driven on 2026-08-28: a music directory
    holding ``open/a.mp3`` and a mode 0o000 ``locked/`` containing ``b.mp3``
    reported exactly one finding and said nothing at all about ``locked``.
    ``rglob`` swallows the ``PermissionError`` from ``scandir`` and yields what it
    could reach, so the audit's answer over a partly unreadable library is
    indistinguishable from its answer over a clean one. The producer is not
    exotic: the library root is a removable volume, and macOS puts directories
    this walk cannot enter at the root of one as a matter of course. ``os.walk``
    takes an ``onerror`` hook, which turns the silence into a row.
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
    """One finding projected for a listing: what it is and where.

    The path is recorded RELATIVE to the library root. An absolute one would put
    somebody's real directory layout into a payload a person may well paste into
    an issue (R1), and the root is already the subject of the report.
    """
    try:
        where = str(path.relative_to(root))
    except ValueError:
        # The walk never leaves the root, so this is unreachable through
        # ``findings``. It is handled anyway because the alternative is a
        # ValueError escaping a REPORT, and a report that raises over one odd
        # path tells the user nothing about the files it had already classified.
        where = path.name
    return {
        "id": where,
        "queue": AUDIT_QUEUE,
        "kind": kind,
        "suffix": path.suffix.lower(),
    }


def acquire_audit(ctx) -> Envelope:
    """Report what the lossless policy does not admit. Writes nothing.

    ``unresolved`` and the length of ``items`` are equal here and that is a
    property of this verb rather than a coincidence worth relying on: nothing
    pages, so the walk's whole result is the page. A later flag that returns a
    subset must recompute ``unresolved`` from the walk, never from the page, for
    the reason :mod:`cratekit.cli.review` gives: reporting the page size as the
    backlog is how a person concludes they are finished.
    """
    cfg = _load()
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
    "ACQUIRE_STAGING_DIRNAME",
    "AUDIT_QUEUE",
    "LIST",
    "LOSSLESS_EXTS",
    "LOSSY_EXTS",
    "TRACKS",
    "UNDECIDED_EXTS",
    "acquire_audit",
    "acquire_download",
    "build",
    "build_audit",
    "checked_landing",
    "classify",
    "download_argv",
    "drive_queued",
    "findings",
    "frozen_tracks",
    "handle",
    "marked_name",
    "queue_list",
    "request_for",
    "staging_dir",
    "sweep_staging",
]
