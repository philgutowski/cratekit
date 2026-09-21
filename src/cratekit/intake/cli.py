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

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.acquire.match import Wanted
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import artifacts, binaries, binary_refusal, config, jobs, review
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, rebuilt, refuse
from cratekit.core.exit_codes import ExitCode, Remedy
from cratekit.intake import fetch, ingest, normalize, pipeline, recognize
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

#: The help text both recognition verbs show. A recording on this machine OR a
#: mix URL, because U104 fetches one. SEAM P6 runs both ways: a verb that
#: refuses an address cannot advertise one, and a verb that takes one has to
#: say so on the one screen a person reads first.
_SOURCE_HELP = (
    "set recording on this machine, or a mix URL, which is fetched with yt-dlp, "
    "identified and then removed"
)


def build_set(parser, entry) -> None:
    parser.add_argument("source", help=_SOURCE_HELP)
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the intake job already queued under this identifier",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help=(
            "ask the recognition service about every chunk again instead of "
            "reading the answers already kept for this recording; this spends"
        ),
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
    parser.add_argument(
        "--refresh",
        action="store_true",
        help=(
            "ask the recognition service about every chunk again instead of "
            "reading the answers already kept for this recording; this spends"
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
        # AND WHETHER THE ROW BILLED A GUEST, for the same reason. The worker
        # decides SUPPRESSED from this object, and a freeze that dropped the
        # field would let a row crediting somebody in its artists list ask for
        # the companion of a deletion that credited somebody else.
        "several_artists": row.several_artists,
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
        # A PAYLOAD FROZEN BEFORE THE FIELD EXISTED DID NOT LOOK, so its absence
        # reads as "may have billed several" and the companion is not asked.
        # That costs a job queued by an older build one missed suppression, and
        # the other default would let it withhold a track nobody deleted.
        several_artists=bool(said.get("several_artists", True)),
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
    jobs.raise_for_state(job)
    cfg = jobs.frozen_config(job)
    return ctx.envelope(data=_reported(store, job, extra=_summary(cfg, job)), warnings=warnings)


# ---------------------------------------------------------------------------
# intake.set and intake.identify
# ---------------------------------------------------------------------------


def _recording_or_refuse(source: str) -> Path:
    """The recording as a file on this machine, absolute, or why not.

    A LOCAL PATH ONLY. A mix URL never reaches this function: ``_local_or_none``
    sends it to the fetch seam instead (U104, R-303).

    EXPANDED BEFORE IT IS CHECKED, because a tilde a shell did not expand is
    the one input the expansion exists for, and checking the literal string
    first refused a file that was there. ABSOLUTE, for the reason ``master``
    freezes its recording absolute: the child a resume spawns inherits the
    resuming process's directory.
    """
    path = Path(source).expanduser()
    if not path.is_file():
        raise _unusable(
            f"{source} is not a file on this machine",
            source=source,
        )
    return path.absolute()


def _local_or_none(source: str) -> Path | None:
    """The recording when ``source`` is a path, and None when it is a mix URL.

    SPLIT FROM THE FETCH ON PURPOSE. A path that names nothing is refused here,
    before the gate, exactly as it always was. An address costs a download, so
    it waits until every refusal that is still free has had its turn.
    """
    if normalize.is_url(source):
        return None
    return _recording_or_refuse(source)


@dataclass(slots=True)
class SetRecording:
    """The file a pass identifies, and what the pass calls it.

    ``ref`` is what is frozen, reported and shown: the absolute path of a local
    recording, or the ADDRESS of a fetched one, because the fetched file is
    gone by the time anybody reads the job. ``stem`` names a tracklist and
    ``shown`` is the short name a sentence uses. ``leftover`` is a scratch
    folder that could not be removed, read after the ``with`` block that lent
    the file.

    ONE OBJECT RATHER THAN A PATH AND SOME OPTIONAL OVERRIDES, because a helper
    that takes the path and an optional address falls back to the scratch
    file's name whenever a caller forgets the address, and says so to nobody.
    """

    path: Path
    ref: str
    stem: str
    shown: str
    leftover: str | None = None

    @classmethod
    def local(cls, path: Path) -> SetRecording:
        return cls(path=path, ref=str(path), stem=path.stem, shown=path.name)


MIX_SCRATCH_LEFT = "mix-scratch-left"


def _fetch_notes(held: SetRecording) -> tuple[dict[str, str], ...]:
    """A scratch folder that outlived its pass, said where a person reads it."""
    if held.leftover is None:
        return ()
    return (
        {
            "code": MIX_SCRATCH_LEFT,
            "message": (
                f"the fetched mix could not be removed from {held.leftover}; it is "
                f"outside the library and is cleared the next time this address is "
                f"fetched, or delete the folder by hand"
            ),
        },
    )


@contextmanager
def _recording(cfg: config.Config, source: str, local: Path | None) -> Iterator[SetRecording]:
    """Lend the recording for one pass, fetching it first when it is a mix URL.

    A LOCAL RECORDING IS LENT AS IT IS and nothing about it changes.

    A MIX URL IS FETCHED THROUGH THE SEAM, into a scratch folder under the
    installation state root, and the folder is removed when the block ends,
    however it ends. The three ways the fetch cannot happen are this verb's
    refusals, each in a vocabulary that already exists: a missing ``yt-dlp`` is
    U80's ``yt-dlp-missing`` with the install hint, a download that failed is
    ``unavailable-transient`` and retryable, and a scratch root that resolves
    under the library is refused before anything is fetched, because a mix must
    never land beside the music.
    """
    if local is not None:
        yield SetRecording.local(local)
        return
    address = source.strip()
    try:
        found = fetch.fetcher()
    except binaries.BinaryNotFound as exc:
        raise binary_refusal.yt_dlp_missing(
            exc,
            {"source": address},
            said="Fetching a mix runs it, so nothing was fetched and nothing was sent.",
            origin=("intake.cli",),
        ) from exc
    try:
        with fetch.fetched(address, Path(cfg.library.root), found) as got:
            held = SetRecording(
                path=got.path, ref=address, stem=fetch.stem_of(address), shown=address
            )
            try:
                yield held
            except CratekitError as exc:
                raise _named_for_the_address(exc, held) from exc.__cause__
        held.leftover = got.leftover
    except fetch.ScratchUnderLibrary as exc:
        raise _unusable(
            f"the scratch folder a fetched mix lands in, {exc.scratch}, is inside "
            f"this library at {exc.library}, and a mix is never written under the "
            f"library; nothing was fetched",
            f"point {config.ENV_STATE_DIR} outside the library, or unset it",
            source=address,
            scratch=str(exc.scratch),
        ) from exc
    except fetch.ScratchUnusable as exc:
        raise _unusable(
            f"{exc}, so the mix at {address} was not fetched; nothing was sent",
            f"make that folder writable, or point {config.ENV_STATE_DIR} somewhere that is",
            source=address,
        ) from exc
    except fetch.SetFetchTimedOut as exc:
        # THE ONE FETCH FAILURE KNOWN TO BE WORTH A RETRY. Everything else a
        # download can end on is below, and is not called retryable, because
        # nobody watches a session and a driver that trusts the flag would
        # re-run a dead address for ever.
        raise refuse(
            "unavailable-transient",
            f"the mix at {address} could not be fetched ({exc}); nothing was sent "
            f"and nothing was kept",
            remedy=Remedy.RETRY_LATER,
            retryable=True,
            steps=(
                "run it again later",
                "or download the mix to a file yourself and run it on that file",
            ),
            origin=("intake.cli",),
            detail={"source": address},
        ) from exc
    except fetch.SeveralRecordings as exc:
        raise _unusable(
            f"{address} was not fetched: {exc}; nothing was sent and nothing was kept",
            "give the address of one recording on that page",
            source=address,
        ) from exc
    except fetch.SetFetchFailed as exc:
        raise _unusable(
            f"the mix at {address} could not be fetched ({exc}); nothing was sent "
            f"and nothing was kept. Whether the address or the network is at fault "
            f"is not known from a failed download",
            "open the address in a browser to check it still plays, then run it again",
            "a streaming playlist goes through intake playlist instead",
            "or download the mix to a file yourself and run it on that file",
            source=address,
        ) from exc


def _named_for_the_address(exc: CratekitError, held: SetRecording) -> CratekitError:
    """A refusal raised over a fetched mix, said about the ADDRESS.

    The identifier names what it was handed, in its message and in its detail,
    and for a fetched mix that is a scratch file removed before anybody reads
    the refusal. Some of these arrive after calls were paid for, so the one
    thing a person can act on, the address, has to be in them. The reason, the
    remedy and everything else are the identifier's and are kept.
    """
    cause = exc.declared_cause
    message = cause.message.replace(str(held.path), held.ref).replace(held.path.name, held.ref)
    detail = {
        key: held.ref if value == str(held.path) else value
        for key, value in dict(cause.detail).items()
    }
    detail.setdefault("source", held.ref)
    return rebuilt(exc, replace(cause, message=message, detail=detail))


def _coverage_or_refuse(
    result: pipeline.IdentifyResult, held: SetRecording
) -> tuple[dict[str, str], ...]:
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
            f"{result.unreached} of {result.chunks} chunk(s) of {held.shown} got no "
            f"answer and the rest named nothing, so this is not a set nobody "
            f"recognised; {result.calls} call(s) were made and counted",
            remedy=Remedy.RETRY_LATER,
            retryable=True,
            origin=("intake.cli",),
            detail={
                "source": held.ref,
                "calls": result.calls,
                "unreached": result.unreached,
            },
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

    A MIX URL IS FETCHED AFTER THE GATE AND BEFORE THE SPEND (U104). The gate
    is free and a download is minutes, so a machine with no recognition keys
    is told so before it waits. The job freezes the ADDRESS as its source, not
    the scratch file, which is removed when the ``with`` block ends: the
    worker reads nothing but the job, and a resume returns above this branch,
    so nothing is ever fetched twice for one job.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return _resume(ctx, store, ctx.args.job)
        source = str(ctx.args.source)
        local = _local_or_none(source)
        recognize.assert_recognition_ready()
        job = None
        with _recording(cfg, source, local) as held:
            result = pipeline.identify_only(
                held.path, refresh=bool(ctx.args.refresh), recognition=cfg.recognition
            )
            warnings = _coverage_or_refuse(result, held) + _cache_notes(result)
            tracks = frozen_rows(result.rows)
            if tracks:
                job = jobs.enqueue(
                    store,
                    handler_key=ctx.entry.handler_key,
                    payload={
                        SOURCE: held.ref,
                        TRACKS: tracks,
                        CALLS: result.calls,
                        UNREACHED: result.unreached,
                    },
                    cfg=cfg,
                    item_ids=tuple(tracks),
                )
        warnings += _fetch_notes(held)
        if job is None:
            return ctx.envelope(
                data=_no_op(
                    "nothing-identified",
                    calls=result.calls,
                    chunks=result.chunks,
                    source=held.ref,
                ),
                outcome=Outcome.NO_OP,
                warnings=warnings,
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

#: How much of the recording's digest a tracklist's name carries. Twelve hex
#: characters is forty eight bits, which no two sets a person owns will share.
TRACKLIST_DIGEST_CHARS = 12

#: The two notes identification adds on the envelope's warnings channel. The
#: ``match`` surface is closed at three arrays, so the file this verb wrote has
#: no field to ride in, and the channel is the one a person is shown.
TRACKLIST_WRITTEN = "tracklist-written"
CACHE_UNWRITTEN = "recognition-cache-unwritten"
CACHE_SERVED = "recognition-cached"


def _cache_notes(result: pipeline.IdentifyResult) -> tuple[dict[str, str], ...]:
    """What the recognition cache did to this pass, said where a person reads it.

    SERVED. A kept miss is served until somebody asks again, and the service's
    catalogue grows, so a pass that read kept answers says how many and names
    the flag that pays for a fresh reading. Without it a tracklist with holes
    in it looks like the service's answer today, when it is last season's.

    UNWRITTEN. The pass succeeded and its rows are good. What is lost is the
    promise that the next pass over the same recording is free, and a person
    who is about to run ``intake set`` on it is owed that before the second
    bill.
    """
    notes: list[dict[str, str]] = []
    if result.cached:
        notes.append(
            {
                "code": CACHE_SERVED,
                "message": (
                    f"{result.cached} of {result.chunks} chunk(s) were answered from "
                    f"what the service said about this recording before and cost "
                    f"nothing; pass --refresh to ask it again, which spends"
                ),
            }
        )
    if result.cache_unwritten:
        notes.append(
            {
                "code": CACHE_UNWRITTEN,
                "message": (
                    f"the {result.calls} recognition answer(s) this pass paid for "
                    f"could not be kept ({result.cache_unwritten}), so another pass "
                    f"over this recording pays for them again"
                ),
            }
        )
    return tuple(notes)


def _library_or_refuse(cfg: config.Config, source: Path | str) -> None:
    """Refuse, BEFORE THE SPEND, a library that is not there to be asked.

    AN ABSENT LIBRARY IS NOT AN EMPTY ONE. The index of a music folder that is
    not there holds nothing, so every identified track would resolve missing
    with a clean exit, which is the false report this verb was written to
    stop, reached by unplugging a drive. ``intake missing --list`` refuses the
    same state for the same reason. It is asked before the identifier runs
    because the answer is free now and follows a paid step otherwise.
    """
    music = Path(cfg.library.root) / cfg.library.music_dir
    if music.is_dir():
        return
    raise refuse(
        "library-volume-unmounted",
        f"this library's music folder {str(music)!r} is not there, so no identified "
        f"track could be told from one the library already holds; nothing was sent",
        remedy=Remedy.MOUNT_LIBRARY_VOLUME,
        origin=("intake.cli",),
        detail={"music": str(music), "source": str(source)},
    )


def tracklist_name(held: SetRecording, digest: str) -> str:
    """The tracklist's file name: the recording's stem and a piece of its digest.

    THE STEM ALONE IS NOT A NAME. A recorder that calls every set REC001 gives
    two different nights one stem, and a tracklist named by it would be
    replaced by the next night's with nothing said. The digest is of the
    recording's bytes, so the same recording names the same file from
    anywhere and a different one cannot. A recording whose bytes could not be
    read is named by its absolute path instead, which still separates two
    folders.

    A FETCHED MIX IS NAMED BY ITS ADDRESS, because the file it was fetched
    into is named for nothing: the stem is the address's last segment and the
    fallback token is a digest of the address.
    """
    token = digest or digest_of({"path": held.ref})
    return f"{held.stem}-{token[:TRACKLIST_DIGEST_CHARS]}{TRACKLIST_SUFFIX}"


def _tracklist_dir(cfg: config.Config, given: str | None, source: Path | str) -> Path:
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
    out: Path, held: SetRecording, result: pipeline.IdentifyResult
) -> dict[str, str]:
    """Write the tracklist and return the note that names it.

    REPLACED, NOT REFUSED, when the file already holds something else. The
    name carries the recording's digest, so what is replaced is an earlier
    reading of THIS recording, and a second identification that filled a gap
    is the better one.

    A FOLDER THAT CANNOT BE WRITTEN IS THIS VERB'S REFUSAL, and it arrives
    after the spend, so it says what running again will cost, and says it
    truthfully: nothing when every answer was kept, the unanswered chunks when
    some got none, and all of it when nothing could be kept.
    """
    path = out / tracklist_name(held, result.digest)
    try:
        config.atomic_write_bytes(result.tracklist.encode("utf-8"), path)
    except OSError as exc:
        if result.cache_unwritten:
            kept = "the recognition answers could not be kept either, so running again pays again"
        elif result.unreached:
            kept = (
                f"the recognition answers were kept, so running again pays only for the "
                f"{result.unreached} chunk(s) that got no answer"
            )
        else:
            kept = "the recognition answers were kept, so running again spends nothing"
        raise _unusable(
            f"the tracklist could not be written to {path} ({type(exc).__name__}: "
            f"{exc.strerror or exc}); {kept}",
            "name another folder with --out, or make this one writable",
            path=str(path),
            source=held.ref,
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

    THE ORDER IS THE SPEND ORDER. The configuration, the recording, the gate,
    the tracklist folder and whether the library is there to be asked are all
    settled while a refusal is free. Then the
    identifier runs, which is the paid step and which pays nothing for a chunk
    the recognition cache already holds, so ``intake set`` after this verb
    costs no calls. The tracklist is written before the library is walked, so
    a library that cannot be read does not take the tracklist with it.

    NOTHING IDENTIFIED WRITES NO TRACKLIST and walks no library, because there
    is nothing to write and nothing to ask.

    A MIX URL IS FETCHED LAST OF THE FREE STEPS (U104), after the gate, the
    tracklist folder and the library have each had the chance to refuse, and
    the fetched file is removed before the library is walked, because the
    walk needs the rows and not the recording.
    """
    cfg = _load()
    source = str(ctx.args.source)
    local = _local_or_none(source)
    recognize.assert_recognition_ready()
    shown = local if local is not None else source.strip()
    out = _tracklist_dir(cfg, ctx.args.out, shown)
    _library_or_refuse(cfg, shown)
    written = None
    with _recording(cfg, source, local) as held:
        result = pipeline.identify_only(
            held.path, refresh=bool(ctx.args.refresh), recognition=cfg.recognition
        )
        warnings = _coverage_or_refuse(result, held) + _cache_notes(result)
        if result.rows:
            written = _tracklist_written(out, held, result)
    warnings += _fetch_notes(held)
    if written is None:
        return ctx.envelope(
            data=match.MatchResult(matches=()).payload(), warnings=warnings
        )
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


def _read_rows(rows: list, reference: str) -> tuple[Wanted, ...]:
    """Provider rows as ``Wanted`` rows, refusing a list this verb cannot use."""
    try:
        return match.read_tidal_tracks(rows)
    except match.UnreadableList as exc:
        raise _unusable(str(exc), source=reference) from exc


def list_playlist(found: catalogue.Catalogue, reference: str) -> dict[str, dict[str, Any]]:
    """One playlist's tracks, frozen and keyed by item, as a playlist job queues them.

    The listing and its failure boundary are the label verb's own, called
    rather than copied, so ``label-playlist-unreadable`` means one thing and
    carries one shape wherever a bound provider was asked about a playlist
    and could not answer. What is this verb's is the reading of the rows.

    PUBLIC because ``crate sync all`` lists each account playlist it sweeps
    through exactly this path, so a row this verb refuses is refused there too.
    An empty mapping is a playlist the provider listed with nothing in it.

    A PLAYLIST ONLY. The reserved reference is :func:`list_favorites`, which
    carries a count this shape has nowhere to put.
    """
    return frozen_rows(_read_rows(label_cli.playlist_tracks_or_refuse(found, reference), reference))


def list_favorites(
    found: catalogue.Catalogue,
) -> tuple[dict[str, dict[str, Any]], catalogue.HeartsShortfall | None]:
    """The account's hearts, frozen as a playlist job queues them, and any shortfall.

    The hearts are read through the catalogue's own favourites listing and
    then read, frozen and resolved exactly as a playlist's rows are, so owned,
    offered and missing mean what they mean for any playlist. Ownership is the
    match engine's one rule, not the source system's ISRC first rule, and a
    heart the library lacks is not parked in a provider playlist: it is a
    missing item, queued with its provider identifier.

    THE SHORTFALL RIDES BESIDE THE ROWS (R-504). The provider counts hearts it
    will not serve, so the listing can hold fewer rows than the account
    declares. What came back is listed, and the shortfall is returned for the
    caller to report by count, because the job alone would resolve the short
    listing as if it were the account.

    PUBLIC because ``crate sync all`` lists the hearts through exactly this
    path, so its inbound check and this verb report the same numbers.
    """
    rows, short = label_cli.favourite_tracks_or_refuse(found, FAVORITES)
    return frozen_rows(_read_rows(rows, FAVORITES)), short


#: The warning code a hearts listing carries when it came back short.
HEARTS_WITHHELD = "intake-hearts-withheld"


def withheld_warning(short: catalogue.HeartsShortfall) -> dict[str, str]:
    """The words a person reads for a short hearts listing, one spelling of them."""
    return {
        "code": HEARTS_WITHHELD,
        "message": (
            f"the account's hearts listed short: {short.summary()}. The provider "
            f"counts hearts it will not serve and does not say which, so the "
            f"{short.withheld} withheld are in no report this job makes"
        ),
    }


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
        short = None
        if hearts:
            tracks, short = list_favorites(found)
        else:
            tracks = list_playlist(found, reference)
        # A SHORT HEARTS LISTING IS SAID, whatever else the run does, and an
        # empty one that the account says is not empty most of all (R-504).
        extra = {"shortfall": short.block()} if short is not None else {}
        warnings = (withheld_warning(short),) if short is not None else ()
        if not tracks:
            return ctx.envelope(
                data=_no_op("no-tracks", source=reference, **extra),
                outcome=Outcome.NO_OP,
                warnings=warnings,
            )
        job = queue_playlist(
            store,
            cfg,
            handler_key=ctx.entry.handler_key,
            reference=reference,
            tracks=tracks,
            source_id=FAVORITES_SOURCE_ID if hearts else None,
        )
        return ctx.envelope(data=_reported(store, job, extra), warnings=warnings)


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
    if not export:
        return ctx.envelope(data=plan, outcome=Outcome.OK)
    destination = path.with_name(path.stem + "_inboxed.xml")
    result = pipeline.ingest_file(
        path,
        cfg=cfg,
        export=Path(export),
        destination=destination,
    )
    plan["items"][0]["destination"] = str(destination)
    # THE SAME ENDING A LANDING HAS, because it is the same ``place_files``
    # (R-501). This used to answer OK over an intake file nobody had imported
    # and a session nothing would close. The action is the one persisted on the
    # intake session, read back so the two cannot differ.
    return ctx.envelope(
        data=plan,
        outcome=Outcome.PENDING,
        code=ExitCode.PENDING_HUMAN,
        pending=ingest.persisted_pending(cfg, result.placed),
    )


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
    "CACHE_SERVED",
    "CACHE_UNWRITTEN",
    "CALLS",
    "FAVORITES",
    "FAVORITES_SOURCE_ID",
    "HEARTS_WITHHELD",
    "INTAKE_KEYS",
    "MIX_SCRATCH_LEFT",
    "SOURCE",
    "TRACKLISTS_DIR",
    "TRACKLIST_SUFFIX",
    "TRACKLIST_WRITTEN",
    "TRACKS",
    "UNREACHED",
    "SetRecording",
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
    "list_favorites",
    "list_playlist",
    "playlist_argv",
    "queue_playlist",
    "reset_cache",
    "resolve_track",
    "set_argv",
    "thawed",
    "tracklist_name",
    "withheld_warning",
]
