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

**A SET NOBODY RECOGNISED IS A REPORT, NOT A SILENT SUCCESS.** Zero identified
tracks queues nothing, and the envelope says so with the calls it took to
find out, because the money was spent either way.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cratekit.acquire import match, match_cli
from cratekit.acquire.match import Wanted
from cratekit.cli.output import Envelope, digest_of
from cratekit.core import artifacts, config, jobs, review
from cratekit.core.cause import Cause, CratekitError, Outcome, Remediation, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import acrcloud, normalize, pipeline, recognize
from cratekit.label import catalogue, harvest

#: Payload keys. ``SOURCE`` is what the resume argv is rebuilt from. ``TRACKS``
#: is what was learned about each item at the queue, keyed by the item
#: identifier, so the worker reads nothing but the job. ``CALLS`` is what
#: identifying the set cost, recorded on the job because the money is spent
#: whether or not anything ran.
SOURCE = "source"
TRACKS = "tracks"
CALLS = "calls"
TRACKLIST = "tracklist"

#: Where one item's report is staged and where it lands, under the queue root.
ARTIFACTS = artifacts.Location(final="intake-artifacts", staging="intake-staging")

#: The digest width of a recognised track's item identifier. Sixteen hex
#: characters, the width the match module uses for its own identifiers.
_ID_WIDTH = 16

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


def build_set(parser, entry) -> None:
    parser.add_argument("source", help="set recording path or mix URL")
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the intake job already queued under this identifier",
    )
    parser.set_defaults(_handler=intake_set)


def build_identify(parser, entry) -> None:
    parser.add_argument("source", help="set recording path or mix URL")
    parser.set_defaults(_handler=intake_identify)


def build_playlist(parser, entry) -> None:
    parser.add_argument("source", help="streaming playlist URL")
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
    keyed by a digest of the recording token, the version token and the ISRC,
    which is the identity the match engine already gives the same record from
    any list. Two different recordings cannot share it and the same recording
    from two chunks folds to it.
    """
    if row.ref:
        return row.ref
    material = "\x1f".join([row.recording, row.version_key, row.isrc or ""])
    return "rc_" + hashlib.sha256(material.encode()).hexdigest()[:_ID_WIDTH]


def frozen_rows(rows: tuple[Wanted, ...]) -> dict[str, dict[str, Any]]:
    """The items, as the listing identifies them, in order and folded once.

    A PROVIDER ROW WITHOUT AN IDENTIFIER IS REFUSED BY POSITION, and the whole
    listing with it: a queue that quietly dropped a row would report every
    item done over a playlist it did not finish. THE SAME IDENTIFIER TWICE
    FOLDS TO ONE ITEM, first occurrence wins, because the queue keys items by
    identifier and a repeat is an insert that cannot land.

    Everything the worker will need is frozen HERE, in the shape ``thawed``
    reads back, so the worker's view of a track is the queue's and not the
    disk's.
    """
    missing = [
        position
        for position, row in enumerate(rows, start=1)
        if row.origin == match.TIDAL and not row.ref
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
        frozen.setdefault(
            item_key(row),
            {
                "artist": row.artist,
                "title": row.title,
                "version": row.version,
                "key": row.key,
                "isrc": row.isrc,
                "origin": row.origin,
                "ref": row.ref,
                "spelled": row.spelled,
            },
        )
    return frozen


def thawed(said: Mapping[str, Any]) -> Wanted:
    """The frozen track as the ``Wanted`` the match engine reads."""
    return Wanted(
        artist=str(said.get("artist") or ""),
        title=str(said.get("title") or ""),
        version=str(said.get("version") or ""),
        key=str(said["key"]) if said.get("key") else None,
        isrc=str(said["isrc"]) if said.get("isrc") else None,
        origin=str(said.get("origin") or match.TEXT),
        ref=str(said.get("ref") or ""),
        spelled=str(said.get("spelled") or ""),
    )


# ---------------------------------------------------------------------------
# The resume tail
# ---------------------------------------------------------------------------


def _summary(cfg: config.Config, job_id: str) -> dict[str, Any]:
    """What the committed reports say, counted by the verb's own words.

    READ BACK from the artifacts rather than accumulated, so a resume reports
    every item and not the ones this process happened to run. ``acquired`` is
    spelled out as zero rather than left absent, because a reader of an intake
    report reaches for that number first and an absent field reads as "not
    yet counted" rather than as "this verb does not do that".
    """
    counts = {word: 0 for word in _STATE_WORDS.values()}
    reports = artifacts.committed(ARTIFACTS, cfg, job_id)
    for report in reports:
        word = str(report.get("state") or "")
        if word in counts:
            counts[word] += 1
    return {"reported": len(reports), "acquired": 0, **counts}


def _resume(ctx, store, job_id: str) -> Envelope:
    """Reconcile, refuse an empty job, drive it, and report what it did.

    RECONCILE FIRST. A resume arrives after something stopped, and a claim
    left behind by a driver that died is state the queue cannot see for
    itself.

    THE ZERO ITEM RULE ON THE RESUME SIDE. A job queued by a build before this
    unit carries a source string and no items at all, and driving it would
    report SUCCEEDED over a set nothing ever resolved.
    """
    job = jobs.reconcile(store, job_id)
    warnings: tuple[dict[str, str], ...] = ()
    if job.is_open():
        if not jobs.items(store, job.job_id):
            raise refuse(
                "internal-error",
                f"job {job.job_id} has no items to run, so driving it would report "
                f"every track resolved over a listing nothing read. It was queued by "
                f"a build that did not record what its items were",
                remedy=Remedy.REPORT_DEFECT,
                origin=("intake.cli",),
                detail={"job_id": job.job_id},
            )
        _, warnings = ctx.run_job(store, job)
        job = jobs.get(store, job.job_id)
    cfg = jobs.frozen_config(job)
    return ctx.envelope(
        data=_reported(store, job, extra=_summary(cfg, job.job_id)), warnings=warnings
    )


# ---------------------------------------------------------------------------
# intake.set
# ---------------------------------------------------------------------------


def _recording_or_refuse(source: str) -> Path:
    """The recording as a file on this machine, or the refusal that says why not.

    A MIX URL IS REFUSED HONESTLY. This build fetches no mix: nothing in the
    package drives the downloader the binaries table knows about, and a verb
    that accepted the address and then found that out inside a paid step would
    have spent the gate for nothing. The address is refused at the queue with
    the step that gets a person to a file.
    """
    if normalize.is_url(source):
        raise _unusable(
            f"{source} is a web address, and this build identifies a recording on "
            f"this machine rather than fetching one",
            "download the mix to a file first, then run intake set on that file",
            source=source,
        )
    path = Path(source)
    if not path.is_file():
        raise _unusable(
            f"{source} is not a file on this machine",
            source=source,
        )
    return path


def intake_set(ctx) -> Envelope:
    """Identify the recording, freeze what was heard, and queue one item per track.

    THE GATE, THEN THE SPEND, THEN THE QUEUE. The recognition gate refuses by
    name before anything is carved; the identifier is the paid step and it is
    bounded inside :mod:`cratekit.intake.acrcloud`; only a set that named at
    least one track becomes a job. The ledger is read either side of the
    spend so the honest zero can say what it cost.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return _resume(ctx, store, ctx.args.job)
        path = _recording_or_refuse(str(ctx.args.source))
        recognize.assert_recognition_ready()
        # ABSOLUTE, for the reason ``master`` freezes its recording absolute:
        # the child a resume spawns inherits the resuming process's directory.
        frozen = path.expanduser().absolute()
        ledger = acrcloud.Ledger()
        before = ledger.used()
        result = pipeline.identify_only(frozen)
        spent = max(0, ledger.used() - before)
        tracks = frozen_rows(result.rows)
        if not tracks:
            return ctx.envelope(
                data=_no_op("nothing-identified", calls=spent, source=str(frozen)),
                outcome=Outcome.NO_OP,
            )
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={
                SOURCE: str(frozen),
                TRACKS: tracks,
                CALLS: spent,
                TRACKLIST: result.tracklist,
            },
            cfg=cfg,
            item_ids=tuple(tracks),
        )
        return ctx.envelope(data=_reported(store, job, extra={"calls": spent}))


# ---------------------------------------------------------------------------
# intake.identify
# ---------------------------------------------------------------------------


def intake_identify(ctx) -> Envelope:
    recognize.assert_recognition_ready()
    source = _recording_or_refuse(str(ctx.args.source))
    result = pipeline.identify_only(source)
    return ctx.envelope(
        data={
            "matched": [],
            "needs_review": [],
            "missing": [
                {"artist": row.artist, "title": row.title, "ref": row.ref}
                for row in result.rows
            ],
        }
    )


# ---------------------------------------------------------------------------
# intake.playlist
# ---------------------------------------------------------------------------


def _playlist_rows(found: catalogue.Catalogue, reference: str) -> tuple[Wanted, ...]:
    """List one playlist through a BOUND catalogue, translating its failures.

    The boundary :mod:`cratekit.label.cli` draws around the same read: a
    ``CratekitError`` passes through, and anything else the provider raised is
    ``label-playlist-unreadable``, which means one thing in both places: a
    bound provider was asked about this playlist and could not answer.
    """
    try:
        rows = harvest.playlist_tracks(found.playlist_for(reference))
    except CratekitError:
        raise
    except Exception as exc:  # noqa: BLE001 - the provider's failures are its own
        raise refuse(
            "label-playlist-unreadable",
            f"the catalogue could not list the playlist {reference!r}: "
            f"{type(exc).__name__}: {exc}",
            origin=("intake.cli",),
            detail={"source": reference},
        ) from exc
    try:
        return match.read_tidal_tracks(rows)
    except match.UnreadableList as exc:
        raise _unusable(str(exc), source=reference) from exc


def intake_playlist(ctx) -> Envelope:
    """List the playlist through the catalogue seam and queue one item per track.

    THE CATALOGUE IS LOOKED UP ON THE MODULE AT CALL TIME, on the contract
    ``label/catalogue.py`` states, which is what lets a test substitute the
    seam. In a shipped build ``resolve`` refuses with ``credential-missing`` or
    ``label-catalogue-unbound`` before the playlist is touched, and both of
    those are honest: nothing was contacted, and the refusal says so.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return _resume(ctx, store, ctx.args.job)
        reference = str(ctx.args.source)
        found = catalogue.resolve(cfg)
        tracks = frozen_rows(_playlist_rows(found, reference))
        if not tracks:
            return ctx.envelope(data=_no_op("no-tracks", source=reference), outcome=Outcome.NO_OP)
        job = jobs.enqueue(
            store,
            handler_key=ctx.entry.handler_key,
            payload={SOURCE: reference, TRACKS: tracks},
            cfg=cfg,
            item_ids=tuple(tracks),
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

    attempt: tuple[str, int]
    index: match.LibraryIndex
    suppresses: Any
    suppression_id: Any


#: ONE INDEX PER DRIVE, not one per item. ``match.index_library`` walks the
#: whole music tree, and the engine claims one item at a time, so without this
#: a fifty track set walks the library fifty times. The key is the job and the
#: attempt the engine stamped on it, so a resume walks again and sees what the
#: previous drive's offers changed. Single entry: a driver runs one job.
_RESOLVED: dict[tuple[str, int], _Resolved] = {}


def _resolved_for(job: jobs.Job, cfg: config.Config) -> _Resolved:
    key = (job.job_id, job.attempts)
    held = _RESOLVED.get(key)
    if held is not None:
        return held
    suppresses, identify = match_cli.suppression_view(
        review.DecisionStore(match_cli.TOMBSTONE_STORE, cfg)
    )
    index = match.index_library(
        cfg.library.root / cfg.library.music_dir, template=match_cli.library_template(cfg)
    )
    _RESOLVED.clear()
    _RESOLVED[key] = _Resolved(
        attempt=key, index=index, suppresses=suppresses, suppression_id=identify
    )
    return _RESOLVED[key]


def resolve_track(wanted: Wanted, job: jobs.Job, cfg: config.Config) -> match.TrackMatch:
    """One track against the frozen library, with its question offered.

    The same three steps ``match.run`` takes over a whole list, over one row:
    resolve against the index and the tombstone snapshot, then let the review
    queue turn a needs review state into an item and read back any answer a
    person already gave. The offer is idempotent, so a resume that redoes the
    item asks nothing twice.
    """
    view = _resolved_for(job, cfg)
    found = match.resolve_one(
        wanted, view.index, suppresses=view.suppresses, suppression_id=view.suppression_id
    )
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
    said = (job.payload or {}).get(TRACKS, {}).get(item.item_id)
    if not isinstance(said, Mapping):
        raise refuse(
            "internal-error",
            f"job {job.job_id} carries no frozen track for item {item.item_id!r}, so "
            f"there is nothing to resolve; it was queued by a build that did not "
            f"record what its items were",
            remedy=Remedy.REPORT_DEFECT,
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
    "CALLS",
    "SOURCE",
    "TRACKLIST",
    "TRACKS",
    "build_file",
    "build_identify",
    "build_playlist",
    "build_set",
    "frozen_rows",
    "handle",
    "intake_file",
    "intake_identify",
    "intake_playlist",
    "intake_set",
    "item_key",
    "playlist_argv",
    "resolve_track",
    "set_argv",
    "thawed",
]
