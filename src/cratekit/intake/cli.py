"""The four ``intake.*`` verbs: set, identify, playlist, file. And their worker.

Builders take unannotated parameters on purpose. ``entry`` is a registry
Entry, and naming that type here would be this layer importing the one
above it.

Long work is queued. Identification-only runs inline because it is the
spend gate plus a tracklist, not a download. A file already on disk is a
plan, not a job: there is no remote work.

**THE ITEMS ARE THE TRACKS, AND THEY ARE KNOWN AT THE QUEUE.** Until U57 both
queued verbs froze a source string and queued a job with no items, which is
R-198's empty queue wearing a full one's clothes, and nothing ran them
(R-203). Now a set is IDENTIFIED at the queue, which is the paid step, and a
playlist is LISTED at the queue through the catalogue seam, and each verb
queues one item per track with what was learned about it frozen in the
payload (KTD9). The worker reads nothing off the network and nothing off the
source: a recording moved or a playlist edited between queueing and driving
cannot change what a queued item means.

**WHAT THE WORKER DOES WITH ONE TRACK, AND WHAT IT DOES NOT.** It resolves the
track against the FROZEN library the way ``match.run`` resolves a list, and
it offers a track the library may already hold to the review queue, which is
the durable record of that question. It does not acquire. A recognised track
carries no provider identifier and the adapter contract has no search, so
there is nothing to ask a provider for; a playlist row carries one, and
acquiring it is ``crate acquire download``'s job over a list document, not a
second copy of that worker here. The per item report therefore says OWNED,
OFFERED or MISSING and never says acquired, and no intake file is written
from an offer. R-140 is the entry that records what it costs to get that
wrong one layer up, and this worker is written so it cannot reproduce it one
layer down.

**A SET NOBODY RECOGNISED IS A REPORT, NOT A SILENT SUCCESS, AND A SET NOBODY
ANSWERED IS NOT A SET NOBODY RECOGNISED.** Zero identified tracks queues
nothing, and the envelope says so with the calls it took to find out, because
the money was spent either way. Zero tracks where chunks got NO answer is a
failure, not a zero, and a set that queued over incomplete coverage carries a
warning saying how much of it was never answered.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.acquire.match import Wanted
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import artifacts, config, jobs, review
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.intake import normalize, pipeline, recognize
from cratekit.label import catalogue
from cratekit.label import cli as label_cli

#: Payload keys. ``SOURCE`` is what the resume argv is rebuilt from. ``TRACKS``
#: is what was learned about each item at the queue, keyed by the item
#: identifier, so the worker reads nothing but the job. ``CALLS`` is what
#: identifying the set cost and ``UNREACHED`` how many of its chunks never got
#: an answer; both are recorded on the job because the money is spent whether
#: or not anything ran, and both are reported back on every resume.
SOURCE = "source"
TRACKS = "tracks"
CALLS = "calls"
UNREACHED = "unreached"

#: The two handler keys one worker serves. A resume is refused for any other,
#: because the driver resolves the worker from the job row and not from the
#: verb, and driving a foreign job here would skip that verb's own checks.
INTAKE_KEYS = frozenset({"intake.set", "intake.playlist"})

#: Where one item's report is staged and where it lands, under the queue root.
ARTIFACTS = artifacts.Location(final="intake-artifacts", staging="intake-staging")

#: What a match state is called on the item's report and in the summary. The
#: words are the verb's, not the engine's, because a person reading a report
#: is asking whether they own the record, whether they were asked about it,
#: or whether it is missing, and ``needs_review`` answers none of those.
_STATE_WORDS: Mapping[match.MatchState, str] = {
    match.MatchState.MATCHED: "owned",
    match.MatchState.NEEDS_REVIEW: "offered",
    match.MatchState.MISSING: "missing",
    match.MatchState.SUPPRESSED: "suppressed",
}


def _load() -> config.Config:
    try:
        return config.load()
    except config.ConfigError as exc:
        raise CratekitError(
            Cause(
                reason="config-unusable",
                message=str(exc),
                remediation=Remediation(remedy=Remedy(str(exc.remedy))),
                origin=("intake.cli",),
                detail={"kind": type(exc).__name__},
            )
        ) from exc


def _reported(store, job, extra: Mapping[str, Any] | None = None) -> dict:
    """The ``job_state`` payload. ``extra`` rides UNDER ``progress``, never
    beside it, because the surface is closed and a top level field the schema
    does not declare fails every consumer generated from it."""
    progress = dict(jobs.progress(store, job.job_id))
    if extra:
        progress.update(extra)
    return {
        "job_id": job.job_id,
        "state": str(job.state),
        "cause": job.cause.to_json() if job.cause is not None else None,
        "progress": progress,
    }


def _no_op(state: str, **progress: Any) -> dict[str, Any]:
    """A run that correctly queued nothing. ``job_id`` is the empty string and
    not None, because the schema types it as a string (R-234)."""
    return {"job_id": "", "state": state, "cause": None, "progress": dict(progress)}


def _plan(items: list[dict[str, str]], *, kind: str) -> dict:
    return {
        "digest": digest_of({"kind": kind, "items": items}),
        "items": items,
        "totals": {"count": len(items)},
        "chunk": None,
    }


def _unusable(message: str, *steps: str, **detail: Any) -> CratekitError:
    return refuse(
        "intake-list-unusable",
        message,
        steps=steps,
        origin=("intake.cli",),
        detail=detail,
    )


# ---------------------------------------------------------------------------
# The surface
# ---------------------------------------------------------------------------

#: The help text both recognition verbs show. A recording ON THIS MACHINE and
#: not a mix URL, because this build fetches none; the refusal a URL meets
#: says the same thing, and the two have to agree on the one screen a person
#: reads first.
_SOURCE_HELP = "set recording on this machine (a mix URL is not fetched by this build)"


def build_set(parser, entry) -> None:
    parser.add_argument("source", help=_SOURCE_HELP)
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the intake job already queued under this identifier",
    )
    parser.set_defaults(_handler=intake_set)


def build_identify(parser, entry) -> None:
    parser.add_argument("source", help=_SOURCE_HELP)
    parser.add_argument(
        "--out",
        default=None,
        metavar="DIR",
        help=(
            "folder the tracklist is written into; defaults to a tracklists "
            "folder under download staging"
        ),
    )
    parser.set_defaults(_handler=intake_identify)


def build_playlist(parser, entry) -> None:
    parser.add_argument(
        "source", help="streaming playlist URL, or favorites for the account's hearts"
    )
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the playlist job already queued under this identifier",
    )
    parser.set_defaults(_handler=intake_playlist)


def build_file(parser, entry) -> None:
    parser.add_argument("source", help="audio file already on this machine")
    parser.add_argument(
        "--export",
        default=None,
        metavar="XML",
        help="Fresh Export to splice into; required to write",
    )
    parser.set_defaults(_handler=intake_file)


def set_argv(job) -> list[str]:
    source = job.payload.get(SOURCE, "")
    return ["intake", "set", source, "--job", job.job_id]


def playlist_argv(job) -> list[str]:
    source = job.payload.get(SOURCE, "")
    return ["intake", "playlist", source, "--job", job.job_id]


# ---------------------------------------------------------------------------
# What an item is
# ---------------------------------------------------------------------------


def item_key(row: Wanted) -> str:
    """The stable identifier one track is queued under, never a display name.

    A provider row is keyed by the provider's own identifier, which is the one
    thing a later acquisition can be asked for and the key the acquisition
    verb uses for the same row. A recognised track carries none, so it is
    keyed by the match module's own digest over the recording token, the
    version token and the ISRC, which is the identity that module already
    gives the same record from any list. Two different recordings cannot
    share it and the same recording from two chunks folds to it.
    """
    if row.ref:
        return row.ref
    return "rc_" + match.digest(row.recording, row.version_key, row.isrc or "")


def _frozen(row: Wanted) -> dict[str, Any]:
    """One track as the payload carries it. :func:`thawed` is the mirror."""
    return {
        "artist": row.artist,
        "title": row.title,
        "version": row.version,
        "key": row.key,
        "isrc": row.isrc,
        "origin": row.origin,
        "ref": row.ref,
        "spelled": row.spelled,
        # THE OTHER READING TRAVELS TOO. ``resolve_one`` asks the library about
        # a title's second reading once nothing the list said has matched, and
        # a freeze that dropped it would make the worker resolve a narrower
        # question than the reader built, silently, on exactly the ambiguous
        # titles the field exists for.
        "other_reading": list(row.other_reading) if row.other_reading else None,
    }


def frozen(row: Wanted) -> dict[str, Any]:
    """The public face of the freeze, for a module that stores a track elsewhere.

    ``intake.candidates`` keeps a provider candidate on a review option and
    reads it back through :func:`thawed`, so one freeze serves both and a field
    added to it reaches both.
    """
    return _frozen(row)


def frozen_rows(rows: tuple[Wanted, ...]) -> dict[str, dict[str, Any]]:
    """The items, as the listing identifies them, in order and folded once.

    A PROVIDER ROW WITHOUT AN IDENTIFIER IS REFUSED BY POSITION, and the whole
    listing with it: a queue that quietly dropped a row would report every
    item done over a playlist it did not finish. Any row that is not plain
    text is a provider row here, so a row from a second provider does not
    slip past a check written for the first. THE SAME IDENTIFIER TWICE FOLDS
    TO ONE ITEM, first occurrence wins, because the queue keys items by
    identifier and a repeat is an insert that cannot land.

    Everything the worker will need is frozen HERE, in the shape ``thawed``
    reads back, so the worker's view of a track is the queue's and not the
    disk's.
    """
    missing = [
        position
        for position, row in enumerate(rows, start=1)
        if row.origin != match.TEXT and not row.ref
    ]
    if missing:
        raise _unusable(
            f"{len(missing)} track(s) in this playlist carry no provider identifier "
            f"(positions {', '.join(str(p) for p in missing[:5])}"
            f"{', ...' if len(missing) > 5 else ''}), so nothing could ever be asked "
            f"about them",
            "fetch the playlist again so every row carries its id",
            positions=missing,
        )
    frozen: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = item_key(row)
        if key in frozen:
            continue
        frozen[key] = _frozen(row)
    return frozen


def thawed(said: Mapping[str, Any]) -> Wanted:
    """The frozen track as the ``Wanted`` the match engine reads."""
    other = said.get("other_reading")
    reading = (
        (str(other[0]), str(other[1]))
        if isinstance(other, (list, tuple)) and len(other) == 2
        else None
    )
    return Wanted(
        artist=str(said.get("artist") or ""),
        title=str(said.get("title") or ""),
        version=str(said.get("version") or ""),
        key=str(said["key"]) if said.get("key") else None,
        isrc=str(said["isrc"]) if said.get("isrc") else None,
        origin=str(said.get("origin") or match.TEXT),
        ref=str(said.get("ref") or ""),
        spelled=str(said.get("spelled") or ""),
        other_reading=reading,
    )


# ---------------------------------------------------------------------------
# The resume tail
# ---------------------------------------------------------------------------


def _summary(cfg: config.Config, job) -> dict[str, Any]:
    """What the committed reports say, counted by the verb's own words.

    READ BACK from the artifacts rather than accumulated, so a resume reports
    every item and not the ones this process happened to run. ``acquired`` is
    spelled out as zero rather than left absent, because a reader of an intake
    report reaches for that number first and an absent field reads as "not
    yet counted" rather than as "this verb does not do that". What the set
    cost to identify rides along, from the payload that froze it.
    """
    counts = {word: 0 for word in _STATE_WORDS.values()}
    reports = artifacts.committed(ARTIFACTS, cfg, job.job_id)
    for report in reports:
        word = str(report.get("state") or "")
        if word in counts:
            counts[word] += 1
    payload = job.payload or {}
    return {
        "reported": len(reports),
        "acquired": 0,
        **counts,
        "calls": int(payload.get(CALLS) or 0),
        "unreached": int(payload.get(UNREACHED) or 0),
    }


def _resume(ctx, store, job_id: str) -> Envelope:
    """Reconcile, refuse a foreign or empty job, drive it, and report how it ended.

    RECONCILE FIRST. A resume arrives after something stopped, and a claim
    left behind by a driver that died is state the queue cannot see for
    itself.

    THE JOB HAS TO BE AN INTAKE JOB. ``handlers.run_job`` resolves the worker
    from the job row and not from this verb, so without this line ``intake
    set x --job`` would drive any queued job of any verb in process, under
    this verb's envelope and without that verb's own resume time checks.
    Either intake key is accepted, because one worker serves the two.

    THE ZERO ITEM RULE ON THE RESUME SIDE. A job queued by a build before this
    unit carries a source string and no items at all, and driving it would
    report SUCCEEDED over a set nothing ever resolved. The steps name the way
    out, because the slug does not: the job stays open after this refusal.

    A JOB THAT ENDED BADLY IS NOT AN OK EXIT. ``jobs.drive`` raises only when
    EVERY attempted item failed, so a set where two tracks resolved and one
    did not returns normally with the job recorded failed, and without the
    re-raise the verb exits 0 over two thirds of a set. It sits OUTSIDE the
    ``is_open`` branch so a job already failed on entry is caught too, and it
    catches ANY closed job carrying a cause, so a run stopped by a signal is
    not an OK exit either. Every sibling tail in the package does the same.
    """
    job = jobs.reconcile(store, job_id)
    if job.handler_key not in INTAKE_KEYS:
        raise refuse(
            "job-unknown",
            f"job {job.job_id} was queued for {job.handler_key!r}, which is not an "
            f"intake job, so this verb will not drive it",
            steps=(f"resume it through its own verb, or with: crate job resume {job.job_id}",),
            origin=("intake.cli",),
            detail={"job_id": job.job_id, "handler": job.handler_key},
        )
    warnings: tuple[dict[str, str], ...] = ()
    if job.is_open():
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
                f"job {job.job_id} has no items to run, so driving it would report "
                f"every track resolved over a listing nothing read. It was queued by "
                f"a build that did not record what its items were",
                remedy=Remedy.REPORT_DEFECT,
                steps=(
                    f"cancel it with: crate job cancel {job.job_id}",
                    "then queue the set or the playlist again, which records its items",
                ),
                origin=("intake.cli",),
                detail={"job_id": job.job_id},
            )
        _, warnings = ctx.run_job(store, job)
        job = jobs.get(store, job.job_id)
    if not job.is_open() and job.cause is not None:
        raise CratekitError(job.cause)
    cfg = jobs.frozen_config(job)
    return ctx.envelope(data=_reported(store, job, extra=_summary(cfg, job)), warnings=warnings)


# ---------------------------------------------------------------------------
# intake.set and intake.identify
# ---------------------------------------------------------------------------


def _recording_or_refuse(source: str) -> Path:
    """The recording as a file on this machine, absolute, or why not.

    A MIX URL IS REFUSED HONESTLY. This build fetches no mix: nothing in the
    package drives the downloader the binaries table knows about, and a verb
    that accepted the address and then found that out inside a paid step would
    have spent the gate for nothing. The address is refused at the queue with
    the step that gets a person to a file, and the help text says the same.

    EXPANDED BEFORE IT IS CHECKED, because a tilde a shell did not expand is
    the one input the expansion exists for, and checking the literal string
    first refused a file that was there. ABSOLUTE, for the reason ``master``
    freezes its recording absolute: the child a resume spawns inherits the
    resuming process's directory.
    """
    if normalize.is_url(source):
        raise _unusable(
            f"{source} is a web address, and this build identifies a recording on "
            f"this machine rather than fetching one",
            "download the mix to a file first, then run intake set on that file",
            source=source,
        )
    path = Path(source).expanduser()
    if not path.is_file():
        raise _unusable(
            f"{source} is not a file on this machine",
            source=source,
        )
    return path.absolute()


def _coverage_or_refuse(result: pipeline.IdentifyResult, source: Path) -> tuple[dict[str, str], ...]:
    """The warnings a partially answered identification carries, or a refusal.

    ABSENCE IS NOT EVIDENCE OF ABSENCE. A run where some chunks got no answer
    and the rest named nothing is not a set nobody recognised, and reporting
    it as one is the honest zero telling a lie. It is refused as a failure.
    A run where some chunks got no answer and others named tracks is a
    tracklist with holes in it, and it goes on with a warning that says how
    many, because a tracklist missing forty minutes of a set with nothing
    saying so is the same lie with a smaller hole.
    """
    if not result.unreached:
        return ()
    if not result.rows:
        raise refuse(
            "intake-recognition-failed",
            f"{result.unreached} of {result.chunks} chunk(s) of {source.name} got no "
            f"answer and the rest named nothing, so this is not a set nobody "
            f"recognised; {result.calls} call(s) were made and counted",
            remedy=Remedy.RETRY_LATER,
            retryable=True,
            origin=("intake.cli",),
            detail={"source": str(source), "calls": result.calls, "unreached": result.unreached},
        )
    return (
        {
            "code": "recognition-incomplete",
            "message": (
                f"{result.unreached} of {result.chunks} chunk(s) got no answer, so "
                f"this tracklist has gaps; identify the recording again to fill them"
            ),
        },
    )


def intake_set(ctx) -> Envelope:
    """Identify the recording, freeze what was heard, and queue one item per track.

    THE GATE, THEN THE SPEND, THEN THE QUEUE. The recognition gate refuses by
    name before anything is carved; the identifier is the paid step and it is
    bounded inside :mod:`cratekit.intake.acrcloud`; only a set that named at
    least one track becomes a job. The counts the identifier reports are the
    counts the job freezes, so the honest zero says what it cost and a
    partial run says how partial.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return _resume(ctx, store, ctx.args.job)
        frozen = _recording_or_refuse(str(ctx.args.source))
        recognize.assert_recognition_ready()
        result = pipeline.identify_only(frozen)
        warnings = _coverage_or_refuse(result, frozen) + _cache_notes(result)
        tracks = frozen_rows(result.rows)
        if not tracks:
            return ctx.envelope(
                data=_no_op(
                    "nothing-identified",
                    calls=result.calls,
                    chunks=result.chunks,
                    source=str(frozen),
                ),
                outcome=Outcome.NO_OP,
            )
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={
                SOURCE: str(frozen),
                TRACKS: tracks,
                CALLS: result.calls,
                UNREACHED: result.unreached,
            },
            cfg=cfg,
            item_ids=tuple(tracks),
        )
        return ctx.envelope(
            data=_reported(
                store, job, extra={"calls": result.calls, "unreached": result.unreached}
            ),
            warnings=warnings,
        )


#: The folder under download staging a tracklist lands in when ``--out`` is
#: not given, and what a tracklist's file name ends in. A text file of
#: 'Artist - Title' lines, which is the door ``acquire match`` and ``intake
#: missing --list`` both read.
TRACKLISTS_DIR = "tracklists"
TRACKLIST_SUFFIX = ".tracklist.txt"

#: The two notes identification adds on the envelope's warnings channel. The
#: ``match`` surface is closed at three arrays, so the file this verb wrote has
#: no field to ride in, and the channel is the one a person is shown.
TRACKLIST_WRITTEN = "tracklist-written"
CACHE_UNWRITTEN = "recognition-cache-unwritten"


def _cache_notes(result: pipeline.IdentifyResult) -> tuple[dict[str, str], ...]:
    """Say so when what this pass paid for could not be kept.

    The pass succeeded and its rows are good. What is lost is the promise that
    the next pass over the same recording is free, and a person who is about
    to run ``intake set`` on it is owed that before the second bill.
    """
    if not result.cache_unwritten:
        return ()
    return (
        {
            "code": CACHE_UNWRITTEN,
            "message": (
                f"the {result.calls} recognition answer(s) this pass paid for could "
                f"not be kept ({result.cache_unwritten}), so another pass over this "
                f"recording pays for them again"
            ),
        },
    )


def _tracklist_dir(cfg: config.Config, given: str | None, source: Path) -> Path:
    """Where the tracklist goes, checked BEFORE the spend.

    A path that exists and is not a folder is refused here, while the refusal
    is still free. Whether the folder can be written is only known by writing.
    """
    if given:
        out = Path(str(given)).expanduser().absolute()
    else:
        out = cfg.paths.download_staging / TRACKLISTS_DIR
    if out.exists() and not out.is_dir():
        raise _unusable(
            f"{out} exists and is not a folder, so no tracklist can be written into "
            f"it; nothing was sent",
            "name a folder with --out",
            out=str(out),
            source=str(source),
        )
    return out


def _tracklist_written(
    out: Path, source: Path, result: pipeline.IdentifyResult
) -> dict[str, str]:
    """Write the tracklist and return the note that names it.

    REPLACED, NOT REFUSED, when the file already holds something else. A
    tracklist is derived from the recording, and a second identification that
    filled a gap is the better reading of the same recording.

    A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL, and it arrives
    after the spend, so it says whether the answers were kept: when they were,
    running again with another folder costs nothing.
    """
    path = out / f"{source.stem}{TRACKLIST_SUFFIX}"
    try:
        config._mkdir_private(out)
        config.atomic_write_bytes(result.tracklist.encode("utf-8"), path)
    except OSError as exc:
        kept = (
            "the recognition answers could not be kept either, so running again pays again"
            if result.cache_unwritten
            else "the recognition answers were kept, so running again spends nothing"
        )
        raise _unusable(
            f"the tracklist could not be written to {path} ({type(exc).__name__}: "
            f"{exc.strerror or exc}); {kept}",
            "name another folder with --out, or make this one writable",
            path=str(path),
            source=str(source),
        ) from exc
    return {
        "code": TRACKLIST_WRITTEN,
        "message": f"{len(result.rows)} identified track(s) written in order to {path}",
    }


def intake_identify(ctx) -> Envelope:
    """Identify the recording, write its tracklist, and ask the library about it.

    IDENTIFICATION ALONE USED TO REPORT EVERY TRACK MISSING (R-422). It had the
    rows and never asked the library, so an owned record and an unowned one
    read the same. The rows now go through ``match_cli.resolve_list``, the one
    spelling of that question, under this verb's own key: owned is
    ``matched``, a version the library may already hold is OFFERED to the
    review queue and reported under ``needs_review``, and the rest is
    ``missing``. An open version question is a pending action, exactly as it
    is for ``acquire match`` over a typed list.

    THE ORDER IS THE SPEND ORDER. The configuration, the recording, the gate
    and the tracklist folder are all settled while a refusal is free. Then the
    identifier runs, which is the paid step and which pays nothing for a chunk
    the recognition cache already holds, so ``intake set`` after this verb
    costs no calls. The tracklist is written before the library is walked, so
    a library that cannot be read does not take the tracklist with it.

    NOTHING IDENTIFIED WRITES NO TRACKLIST and walks no library, because there
    is nothing to write and nothing to ask.
    """
    cfg = _load()
    source = _recording_or_refuse(str(ctx.args.source))
    recognize.assert_recognition_ready()
    out = _tracklist_dir(cfg, ctx.args.out, source)
    result = pipeline.identify_only(source)
    warnings = _coverage_or_refuse(result, source) + _cache_notes(result)
    if not result.rows:
        return ctx.envelope(
            data=match.MatchResult(matches=()).payload(), warnings=warnings
        )
    written = _tracklist_written(out, source, result)
    resolved = match_cli.resolve_list(
        cfg, result.rows, handler_key=ctx.entry.handler_key, run_id=ctx.run.run_id
    )
    pending = resolved.pending
    return ctx.envelope(
        data=resolved.result.payload(),
        outcome=Outcome.PENDING if pending is not None else Outcome.OK,
        code=ExitCode.PENDING_HUMAN if pending is not None else ExitCode.OK,
        pending=pending,
        warnings=(written, *warnings, *resolved.warnings),
    )


# ---------------------------------------------------------------------------
# intake.playlist
# ---------------------------------------------------------------------------


#: The reserved reference that lists the account's hearts instead of a
#: playlist. It cannot collide with a real playlist, because
#: ``tidal_catalogue.playlist_id`` accepts only an identifier or a URL, and a
#: playlist TITLED favorites is still referenced by its identifier.
FAVORITES = "favorites"

#: The ``source_id`` a hearts job carries, so a later reader can tell the job
#: that listed the account's hearts from one that listed a playlist.
FAVORITES_SOURCE_ID = "favorites"


def is_favorites(reference: str) -> bool:
    """Whether ``reference`` is the reserved hearts reference, as a person types it."""
    return str(reference or "").strip().casefold() == FAVORITES


def _playlist_rows(found: catalogue.Catalogue, reference: str) -> tuple[Wanted, ...]:
    """List one playlist through a BOUND catalogue, as ``Wanted`` rows.

    The listing and its failure boundary are the label verb's own, called
    rather than copied, so ``label-playlist-unreadable`` means one thing and
    carries one shape wherever a bound provider was asked about a playlist
    and could not answer. What is this verb's is the reading of the rows.

    THE RESERVED REFERENCE IS ASKED FIRST, before ``playlist_for`` could see
    it. The hearts are read through the catalogue's own favourites listing and
    then read, frozen and resolved exactly as a playlist's rows are, so owned,
    offered and missing mean what they mean for any playlist. Ownership is the
    match engine's one rule, not the source system's ISRC first rule, and a
    heart the library lacks is not parked in a provider playlist: it is a
    missing item, queued with its provider identifier.
    """
    if is_favorites(reference):
        rows = label_cli.favourite_tracks_or_refuse(found, reference)
    else:
        rows = label_cli.playlist_tracks_or_refuse(found, reference)
    try:
        return match.read_tidal_tracks(rows)
    except match.UnreadableList as exc:
        raise _unusable(str(exc), source=reference) from exc


def list_playlist(found: catalogue.Catalogue, reference: str) -> dict[str, dict[str, Any]]:
    """One playlist's tracks, frozen and keyed by item, as a playlist job queues them.

    PUBLIC because ``crate sync all`` lists each account playlist it sweeps
    through exactly this path, so a row this verb refuses is refused there too.
    An empty mapping is a playlist the provider listed with nothing in it.
    """
    return frozen_rows(_playlist_rows(found, reference))


def queue_playlist(
    store,
    cfg: config.Config,
    *,
    handler_key: str,
    reference: str,
    tracks: Mapping[str, Mapping[str, Any]],
    run_id: str | None = None,
    source_id: str | None = None,
) -> jobs.Job:
    """Queue one playlist job, one item per frozen track. The one spelling of it.

    ``run_id`` and ``source_id`` are what ``crate sync all`` adds: the intake run
    its sources share (R29) and the source that queued the job, which is how the
    playlists cursor later finds the jobs it may record. A playlist queued by
    this verb alone carries neither, exactly as before.
    """
    payload: dict[str, Any] = {SOURCE: reference, TRACKS: dict(tracks)}
    if run_id is not None:
        payload["run_id"] = run_id
    if source_id is not None:
        payload["source_id"] = source_id
    return jobs.enqueue(
        store,
        handler_key=handler_key,
        payload=payload,
        cfg=cfg,
        item_ids=tuple(tracks),
    )


def intake_playlist(ctx) -> Envelope:
    """List the playlist through the catalogue seam and queue one item per track.

    THE CATALOGUE IS LOOKED UP ON THE MODULE AT CALL TIME, on the contract
    ``label/catalogue.py`` states, which is what lets a test substitute the
    seam. In a shipped build ``resolve`` refuses with ``credential-missing`` or
    ``label-catalogue-unbound`` before the playlist is touched, and both of
    those are honest: nothing was contacted, and the refusal says so.

    ``favorites`` queues the account's hearts as one job under the same key and
    the same worker, recorded under the canonical spelling so the resume argv
    names the reserved reference however it was typed. A re-run needs no
    cursor: a heart acquired since the last run resolves owned.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return _resume(ctx, store, ctx.args.job)
        reference = str(ctx.args.source)
        hearts = is_favorites(reference)
        if hearts:
            reference = FAVORITES
        found = catalogue.resolve(cfg)
        tracks = list_playlist(found, reference)
        if not tracks:
            return ctx.envelope(data=_no_op("no-tracks", source=reference), outcome=Outcome.NO_OP)
        job = queue_playlist(
            store,
            cfg,
            handler_key=ctx.entry.handler_key,
            reference=reference,
            tracks=tracks,
            source_id=FAVORITES_SOURCE_ID if hearts else None,
        )
        return ctx.envelope(data=_reported(store, job))


# ---------------------------------------------------------------------------
# intake.file
# ---------------------------------------------------------------------------


def intake_file(ctx) -> Envelope:
    cfg = _load()
    path = Path(ctx.args.source)
    rows = normalize.from_audio_file(path)
    items = [{"path": str(path), "artist": row.artist, "title": row.title} for row in rows]
    plan = _plan(items, kind="file")
    export = ctx.args.export
    if export:
        destination = path.with_name(path.stem + "_inboxed.xml")
        pipeline.ingest_file(
            path,
            cfg=cfg,
            export=Path(export),
            destination=destination,
        )
        plan["items"][0]["destination"] = str(destination)
    return ctx.envelope(data=plan, outcome=Outcome.OK)


# ---------------------------------------------------------------------------
# The worker
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _Resolved:
    """One drive's view of the library and the tombstones, built once."""

    index: match.LibraryIndex
    suppresses: Any
    suppression_id: Any


#: ONE INDEX PER DRIVE, not one per item. ``match.index_library`` walks the
#: whole music tree, and the engine claims one item at a time, so without this
#: a fifty track set walks the library fifty times. The key is the job and the
#: attempt the engine stamped on it, so a resume walks again and sees what the
#: previous drive's offers changed. Single entry: a driver runs one job. This
#: is a module global standing in for a per drive setup seam the job engine
#: does not have, which is recorded rather than hidden; ``reset_cache`` is
#: what a suite calls between libraries, the same hook adoption exposes.
_RESOLVED: dict[tuple[str, int], _Resolved] = {}


def reset_cache() -> None:
    """Forget the cached library view. A module level cache no test can clear
    is a cache that leaks one test's library into the next."""
    _RESOLVED.clear()


def _resolved_for(job: jobs.Job, cfg: config.Config) -> _Resolved:
    key = (job.job_id, job.attempts)
    held = _RESOLVED.get(key)
    if held is not None:
        return held
    index, suppresses, identify = match_cli.library_view(cfg)
    built = _Resolved(index=index, suppresses=suppresses, suppression_id=identify)
    _RESOLVED.clear()
    _RESOLVED[key] = built
    return built


def resolve_track(wanted: Wanted, job: jobs.Job, cfg: config.Config) -> match.TrackMatch:
    """One track against the frozen library, with its question offered.

    The same three steps ``match.run`` takes over a whole list, over one row:
    resolve against the index and the tombstone snapshot, then let the review
    queue turn a needs review state into an item and read back any answer a
    person already gave. The offer is idempotent, so a resume that redoes the
    item asks nothing twice. THE REVIEW STORE IS OPENED ONLY FOR A QUESTION:
    ``adjudicate`` passes an owned or a missing track straight through, so
    opening and initialising the store for those would be fifty opens to use
    it twice.
    """
    view = _resolved_for(job, cfg)
    found = match.resolve_one(
        wanted, view.index, suppresses=view.suppresses, suppression_id=view.suppression_id
    )
    if found.state is not match.MatchState.NEEDS_REVIEW:
        return found
    with review.open_store(cfg) as items:
        result = match_cli.adjudicate(
            items,
            match.MatchResult(matches=(found,)),
            handler_key=job.handler_key,
            suppresses=view.suppresses,
            suppression_id=view.suppression_id,
        )
    return result.matches[0]


def handle(job, item, cfg) -> jobs.Produced:
    """Resolve ONE queued track. The per item worker behind both intake keys.

    THE ITEM NAMES THE TRACK, never the payload alone: the payload is read at
    the item's own key, and a key the payload does not carry is refused rather
    than resolved as an empty row, because that is a job queued by a build
    that did not record what its items were.

    ``cfg`` is the configuration the job was FROZEN against (KTD9). The library
    root, the naming template and the review store are all read off it, so a
    library root edited while the job waited is not the library this run
    resolves against.

    The report is the item's artifact. It says which of the verb's four words
    the track resolved to, the paths the library holds for it, the review item
    a person may be asked about, and the acquisition options a missing track
    carries. It never says acquired.
    """
    said = job.payload.get(TRACKS, {}).get(item.item_id)
    if not isinstance(said, Mapping):
        raise refuse(
            "internal-error",
            f"job {job.job_id} carries no frozen track for item {item.item_id!r}, so "
            f"there is nothing to resolve; it was queued by a build that did not "
            f"record what its items were",
            remedy=Remedy.REPORT_DEFECT,
            steps=(f"cancel it with: crate job cancel {job.job_id}",),
            origin=("intake.cli",),
            detail={"job_id": job.job_id, "item_id": item.item_id},
        )
    wanted = thawed(said)
    settled = resolve_track(wanted, job, cfg)
    report = {
        "item_id": item.item_id,
        "track": dict(said),
        "state": _STATE_WORDS[settled.state],
        "why": str(settled.why),
        "paths": list(settled.paths),
        "review_item": settled.item_id,
        "acquisitions": [option.to_json() for option in settled.acquisitions],
        "acquired": False,
    }
    return artifacts.produced(ARTIFACTS, cfg, job, item, report)


__all__ = [
    "ARTIFACTS",
    "CACHE_UNWRITTEN",
    "CALLS",
    "FAVORITES",
    "FAVORITES_SOURCE_ID",
    "INTAKE_KEYS",
    "SOURCE",
    "TRACKLISTS_DIR",
    "TRACKLIST_SUFFIX",
    "TRACKLIST_WRITTEN",
    "TRACKS",
    "UNREACHED",
    "build_file",
    "build_identify",
    "build_playlist",
    "build_set",
    "frozen",
    "frozen_rows",
    "handle",
    "intake_file",
    "intake_identify",
    "intake_playlist",
    "intake_set",
    "is_favorites",
    "item_key",
    "list_playlist",
    "playlist_argv",
    "queue_playlist",
    "reset_cache",
    "resolve_track",
    "set_argv",
    "thawed",
]
