"""Three ``intake.*`` verbs: set, identify, playlist. And their worker.

Builders take unannotated parameters on purpose: naming the registry's Entry
would import the layer above. ``intake file`` is :mod:`cratekit.intake.file_cli`.

THE ITEMS ARE THE TRACKS, KNOWN AT THE QUEUE (U57, KTD9): a set is identified
and a playlist listed when queued, one item per track with what was learned
frozen (:mod:`cratekit.intake.cli_listing`), so the worker reads nothing off
the network or the source. The worker resolves and offers to the review queue;
it never acquires (R-140), so a report says OWNED, OFFERED or MISSING. A set
nobody recognised is a report; a set nobody answered is a failure.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from cratekit.acquire import match, match_cli
from cratekit.acquire.match import Wanted
from cratekit.cli.output import Envelope, digest_of, no_job
from cratekit.core import config, jobs, review
from cratekit.core.cause import CratekitError, Outcome, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.intake import cli_identify as _identify
from cratekit.intake import cli_listing as _listing
from cratekit.intake import fetch, pipeline, recognize
from cratekit.intake.cli_identify import (
    TRACKLIST,
    _cache_notes,
    _coverage_or_refuse,
    _fetch_notes,
    _local_or_none,
    _parts_notes,
    _recording,
    _set_tracklist,
    _tracklist_dir,
    intake_identify,
)
from cratekit.intake.cli_listing import (
    FAVORITES,
    frozen_rows,
    list_favorites,
    list_playlist_declared,
    thawed,
)

if TYPE_CHECKING:
    from cratekit.label import catalogue

#: Re-exported, so callers and suites keep reading these names here.
CACHE_SERVED = _identify.CACHE_SERVED
CACHE_UNWRITTEN = _identify.CACHE_UNWRITTEN
IN_PARTS = _identify.IN_PARTS
MIX_SCRATCH_LEFT = _identify.MIX_SCRATCH_LEFT
TRACKLIST_SUFFIX = _identify.TRACKLIST_SUFFIX
TRACKLIST_UNWRITTEN = _identify.TRACKLIST_UNWRITTEN
TRACKLIST_WRITTEN = _identify.TRACKLIST_WRITTEN
TRACKLISTS_DIR = _identify.TRACKLISTS_DIR
SetRecording = _identify.SetRecording
tracklist_name = _identify.tracklist_name
HEARTED = _listing.HEARTED
Readable = _listing.Readable
Unreadable = _listing.Unreadable
frozen = _listing.frozen
hearted_on = _listing.hearted_on
item_key = _listing.item_key
list_playlist = _listing.list_playlist
list_playlist_readable = _listing.list_playlist_readable
set_aside = _listing.set_aside
_load = _listing._load

#: Payload keys. ``SOURCE`` is what the resume argv is rebuilt from. ``TRACKS``
#: is what was learned about each item at the queue, keyed by item identifier.
#: ``CALLS`` is what identifying the set cost and ``UNREACHED`` how many chunks
#: never got an answer, recorded because the money is spent either way, and
#: ``PARTS`` how many runs it took (R-706), so a resume reports what the queue did.
SOURCE = "source"
TRACKS = "tracks"
CALLS = "calls"
UNREACHED = "unreached"
PARTS = "parts"
#: What a fetched mix's page said, under :data:`fetch.PAGE_KEYS`, so a set's
#: playlist can be named from it later (U121). Empty for a local recording.
PAGE = "page"
#: The account's name for the playlist as the sweep listed it (U113), recorded
#: at the queue because ``sync mark`` later prefixes the account's copy.
PLAYLIST_NAME = "playlist_name"

#: The two handler keys one worker serves. A resume is refused for any other,
#: because the driver resolves the worker from the job row and not the verb.
INTAKE_KEYS = frozenset({"intake.set", "intake.playlist"})

#: Where one item's report is staged and where it lands, under the queue root.
ARTIFACTS = jobs.Artifacts(final="intake-artifacts", staging="intake-staging")

#: A match state in the verb's words: does a person own it, were they asked
#: about it, or is it missing; ``needs_review`` answers none of those.
_STATE_WORDS: Mapping[match.MatchState, str] = {
    match.MatchState.MATCHED: "owned",
    match.MatchState.NEEDS_REVIEW: "offered",
    match.MatchState.MISSING: "missing",
    match.MatchState.SUPPRESSED: "suppressed",
}


def _plan(items: list[dict[str, str]], *, kind: str) -> dict:
    return {
        "digest": digest_of({"kind": kind, "items": items}),
        "items": items,
        "totals": {"count": len(items)},
        "chunk": None,
    }


# ---------------------------------------------------------------------------
# The surface
# ---------------------------------------------------------------------------

#: A verb that takes an address has to say so on the screen read first (SEAM P6).
_SOURCE_HELP = (
    "set recording on this machine, or a mix URL, which is fetched with yt-dlp, "
    "identified and then removed"
)
#: One ``--out`` help, because ``intake set`` writes the tracklist ``intake identify`` does.
_OUT_HELP = (
    "folder the tracklist is written into; defaults to a tracklists folder under download staging"
)


def _identify_arguments(parser) -> None:
    parser.add_argument("source", help=_SOURCE_HELP)
    parser.add_argument("--out", default=None, metavar="DIR", help=_OUT_HELP)


def _refresh_argument(parser) -> None:
    parser.add_argument(
        "--refresh",
        action="store_true",
        help=(
            "ask the recognition service about every chunk again instead of "
            "reading the answers already kept for this recording; this spends"
        ),
    )


def build_set(parser, entry) -> None:
    from cratekit.intake import set_playlist

    _identify_arguments(parser)
    parser.add_argument(
        "--job",
        default=None,
        metavar="JOB_ID",
        help="continue the intake job already queued under this identifier",
    )
    _refresh_argument(parser)
    # U129. The account playlist is named as INSPIRATION is, by the same words.
    set_playlist.add_word_arguments(parser)
    parser.set_defaults(_handler=intake_set)


def build_identify(parser, entry) -> None:
    _identify_arguments(parser)
    _refresh_argument(parser)
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


def set_argv(job) -> list[str]:
    """The command line that continues one queued set.

    It carries ``--run`` when the account gate was asked: that gate is
    explicit, so R34 answers it only by an act recorded against a run, and a
    respawned child with no ``--run`` mints a new run and stops at the gate
    every time. The flag goes before the verb path, since the root parser owns it.
    """
    payload = job.payload or {}
    source = str(payload.get(SOURCE) or "")
    gate_run = payload.get(jobs.GATE_RUN_KEY)
    resume = ["--run", str(gate_run)] if gate_run else []
    return [*resume, "intake", "set", source, "--job", job.job_id]


def playlist_argv(job) -> list[str]:
    source = job.payload.get(SOURCE, "")
    return ["intake", "playlist", source, "--job", job.job_id]


# ---------------------------------------------------------------------------
# The resume tail
# ---------------------------------------------------------------------------


def _summary(cfg: config.Config, job) -> dict[str, Any]:
    """What the committed reports say, counted by the verb's own words.

    Read back from the artifacts, so a resume reports every item. ``acquired``
    is spelled out as zero, since an absent field reads as "not yet counted".
    ``by_reason`` is keyed by state first (R-682), because one reason lands
    rows in more than one state; a reason is a key only when some row carries
    it, and a report with no string ``why`` is counted under no reason.
    """
    counts = {word: 0 for word in _STATE_WORDS.values()}
    by_reason: dict[str, dict[str, int]] = {word: {} for word in counts}
    reports = ARTIFACTS.committed(cfg, job.job_id)
    for report in reports:
        word = str(report.get("state") or "")
        if word in counts:
            counts[word] += 1
            why = report.get("why")
            if isinstance(why, str) and why:
                by_reason[word][why] = by_reason[word].get(why, 0) + 1
    payload = job.payload or {}
    return {
        "reported": len(reports),
        "acquired": 0,
        **counts,
        "by_reason": by_reason,
        "calls": int(payload.get(CALLS) or 0),
        "unreached": int(payload.get(UNREACHED) or 0),
        "parts": int(payload.get(PARTS) or 1),
    }


def _resume(ctx, store, job_id: str) -> Envelope:
    """Reconcile, refuse a foreign or empty job, drive it, and report how it ended.

    Reconciled first, since a dead driver's claim is state the queue cannot
    see. Only an intake job, since ``handlers.run_job`` resolves the worker
    from the job row and would drive any verb's job without its own checks.
    A job with no items was queued by an older build and would report
    SUCCEEDED over nothing. A job that ended badly, failed on entry or stopped
    by a signal, is not an OK exit, since ``jobs.drive`` raises only when
    every item failed.
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
    return ctx.envelope(data=jobs.reported(store, job, extra=_summary(cfg, job)), warnings=warnings)


# ---------------------------------------------------------------------------
# intake.set: the account playlist (U129)
# ---------------------------------------------------------------------------

#: Why the account playlist step was skipped, one code each, and its gate.
ACCOUNT_UNNAMED = "set-account-unnamed"
ACCOUNT_UNREACHABLE = "set-account-unreachable"
ACCOUNT_GATE = "intake.set.account.confirm"


@dataclass(frozen=True, slots=True)
class _PlaylistName:
    """What ``intake set`` decided about the account and INSPIRATION name."""

    name: str = ""
    warning: dict[str, str] | None = None


def _set_playlist_name(
    page,
    *,
    dj: str | None,
    set_name: str | None,
    set_date: str | None,
    posted: str | None = None,
    from_url: bool = False,
) -> _PlaylistName:
    """The INSPIRATION form of the name, or a warning when naming was expected.

    A local recording with no page and no name flags never asked for an
    account playlist, so its skip is silent; a mix URL, a page, or any name
    flag did ask, so failing to name the set warns. The first word is the
    posted day (U136): ``--posted``, the page's upload_date, else the landing day.
    """
    from cratekit.export import set_cli
    from cratekit.intake import set_playlist

    try:
        words = set_playlist.words_from_page(page, dj=dj, set_name=set_name, set_date=set_date)
    except CratekitError as exc:
        if exc.cause.reason != set_playlist.UNNAMED:
            raise
        page = page if isinstance(page, Mapping) else {}
        asked = (
            bool(page) or from_url or any(v is not None for v in (dj, set_name, set_date, posted))
        )
        if not asked:
            return _PlaylistName()
        return _PlaylistName(
            warning={
                "code": ACCOUNT_UNNAMED,
                "message": (
                    f"{exc.cause.message}; the set is queued and no account "
                    f"playlist was planned. Pass the missing flag(s) on a later "
                    f"crate export set, or on crate intake inspiration"
                ),
            }
        )
    page = page if isinstance(page, Mapping) else {}
    day, fallback = set_playlist.naming_day(
        posted=posted,
        page_upload_date=str(page.get(fetch.PAGE_UPLOAD_DATE) or ""),
        landing=set_playlist.today(),
    )
    return _PlaylistName(
        name=set_cli.set_name(set_playlist.playlist_name(words, on=day)),
        warning=fallback,
    )


def _skipped(message: str) -> tuple[tuple[dict[str, str], ...], None]:
    """The account step soft skipped: its one warning, and no gate answer or plan."""
    return ({"code": ACCOUNT_UNREACHABLE, "message": message},), None


def _ask_account_gate(ctx, *, name: str) -> tuple[tuple, str | None]:
    """Ask the account gate over the playlist name alone, before recognition.

    Asked before ``jobs.enqueue``, so a first refusal leaves no job a resume
    would queue again, and before recognition, so the first run does not pay
    ACRCloud only to stop. A verb declaring no gate soft skips with a warning.
    """
    if not name:
        return (), None
    spec = next((one for one in ctx.entry.gates if one.name == ACCOUNT_GATE), None)
    if spec is None:
        return _skipped(
            f"the account playlist {name!r} was named but this verb "
            f"declares no account gate, so nothing was written"
        )
    plan = {
        "digest": digest_of({"kind": "intake-set-account", "name": name}),
        "items": [{"id": name, "kind": "playlist", "name": name, "action": "save"}],
        "totals": {"count": 1, "writes": True},
        "chunk": None,
    }
    shown = {
        "playlist": f"{name}: save it as a private account playlist under this name",
        "tracks": "the tracks are named after recognition, then matched on the account",
        "removes": "nothing, ever: no track or playlist is taken away",
    }
    return (), ctx.gate.require(spec, plan=plan, context=shown)


def _plan_account_playlist(cfg, *, name: str, rows):
    """Match the set's rows to the account playlist after recognition.

    A missing credential or a matching failure soft skips with a warning; a
    later ``crate export set`` or the backfill covers it.
    """
    if not name or not rows:
        return (), None
    from cratekit.export import set_cli

    try:
        built = set_cli.plan_from_wanted(cfg, name, rows)
    except CratekitError as exc:
        return _skipped(
            f"the account playlist {name!r} was not planned "
            f"({exc.cause.reason}: {exc.cause.message}); the set will "
            f"still be queued, run crate export set over its "
            f"tracklist once the account is reachable"
        )
    return tuple(set_cli.unmatched_warnings(built.planned)), built


def _apply_account_playlist(cfg, built, option: str | None):
    """Write the planned account playlist after the set is queued, or leave it."""
    from cratekit.export import set_cli

    if built is None:
        return (), None
    notes = ()
    if option != "apply" or not built.writes:
        return notes, built.payload

    data, more, _wrote = set_cli.apply_planned(cfg, built)
    return tuple(more), data


# ---------------------------------------------------------------------------
# intake.set
# ---------------------------------------------------------------------------


def intake_set(ctx) -> Envelope:
    """Identify the recording, freeze what was heard, and queue one item per track.

    THE ACCOUNT GATE, THEN THE RECOGNITION GATE, THEN THE SPEND, THEN THE
    QUEUE. The account gate asks over the playlist name alone, so it fires
    before ACRCloud runs. When ``--posted`` and the three name flags name the
    set it fires before a mix is fetched; otherwise the page names it, so the
    fetch comes first (U136). Only a set that named a track becomes a job,
    freezing the ADDRESS of a mix as its source, and the counts the identifier
    reports are the counts the job freezes.

    The tracklist is written as ``intake identify`` writes it (R-925), after
    the job is queued, so a refused queue leaves no list; a failed write is a
    warning, since the job is what the spend bought. Its path rides the
    envelope as a note and as ``tracklist``, None when nothing was written.
    """
    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return _resume(ctx, store, ctx.args.job)
        source = str(ctx.args.source)
        local = _local_or_none(source)
        words = {k: getattr(ctx.args, k, None) for k in ("dj", "set_name", "set_date", "posted")}
        posted = words["posted"]
        # Named from the flags alone only when the day is locked by --posted,
        # since otherwise the page's upload_date names it (U136).
        early = _set_playlist_name({}, **words)
        locked = bool(early.name) and posted is not None
        account_notes: tuple = ()
        option: str | None = None
        if locked:
            account_notes, option = _ask_account_gate(ctx, name=early.name)
        recognize.assert_recognition_ready()
        out = _tracklist_dir(cfg, ctx.args.out, local if local is not None else source.strip())
        job = None
        built = None
        with _recording(cfg, source, local, ctx.progress) as held:
            playlist = (
                early if locked else _set_playlist_name(held.page, **words, from_url=local is None)
            )
            if playlist.name and not locked:
                more, option = _ask_account_gate(ctx, name=playlist.name)
                account_notes = (*account_notes, *more)
            result = pipeline.identify_only(
                held.path,
                refresh=bool(ctx.args.refresh),
                recognition=cfg.recognition,
                progress=ctx.progress,
            )
            warnings = (
                _coverage_or_refuse(result, held)
                + _cache_notes(result)
                + _parts_notes(result, queued=True)
                + ((playlist.warning,) if playlist.warning else ())
            )
            tracks = frozen_rows(result.rows)
            plan_notes, built = _plan_account_playlist(
                cfg, name=playlist.name, rows=result.rows if tracks else ()
            )
            account_notes = (*account_notes, *plan_notes)
            if tracks:
                payload = {
                    SOURCE: held.ref,
                    TRACKS: tracks,
                    CALLS: result.calls,
                    UNREACHED: result.unreached,
                    PARTS: result.parts,
                    PAGE: dict(held.page),
                }
                # The name is frozen so the account and the landing agree on
                # any day (U129), and the gate run so a resume keeps the answer.
                if playlist.name:
                    payload[PLAYLIST_NAME] = playlist.name
                if option is not None:
                    payload[jobs.GATE_RUN_KEY] = ctx.run.run_id
                job = jobs.enqueue(
                    store,
                    handler_key=ctx.entry.handler_key,
                    payload=payload,
                    cfg=cfg,
                    item_ids=tuple(tracks),
                )
        warnings += _fetch_notes(held)
        if job is None:
            return ctx.envelope(
                data=no_job(
                    "nothing-identified",
                    calls=result.calls,
                    chunks=result.chunks,
                    source=held.ref,
                ),
                outcome=Outcome.NO_OP,
                warnings=(*warnings, *account_notes),
            )
        listed, note = _set_tracklist(out, held, result, job.job_id)
        apply_notes, account_data = _apply_account_playlist(cfg, built, option)
        extra = {
            "calls": result.calls,
            "unreached": result.unreached,
            "parts": result.parts,
            TRACKLIST: str(listed) if listed is not None else None,
        }
        if account_data is not None:
            extra["account_playlist"] = account_data
        return ctx.envelope(
            data=jobs.reported(store, job, extra=extra),
            warnings=(note, *warnings, *account_notes, *apply_notes),
        )


# ---------------------------------------------------------------------------
# intake.playlist
# ---------------------------------------------------------------------------

#: The ``source_id`` a hearts job carries, telling it from a playlist's job.
FAVORITES_SOURCE_ID = "favorites"

#: The warning codes a hearts or a playlist listing carries when it came back short.
HEARTS_WITHHELD = "intake-hearts-withheld"
PLAYLIST_WITHHELD = "intake-playlist-withheld"


def is_favorites(reference: str) -> bool:
    """Whether ``reference`` is the reserved hearts reference, as a person types it."""
    return str(reference or "").strip().casefold() == FAVORITES


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


def playlist_withheld_warning(short: catalogue.ListingShortfall, reference: str) -> dict[str, str]:
    """The words a person reads for a short playlist listing (R-515), one spelling of them."""
    return {
        "code": PLAYLIST_WITHHELD,
        "message": (
            f"the playlist {reference!r} listed short: {short.summary()}. The "
            f"provider counts tracks it will not serve and does not say which, so "
            f"the {short.withheld} withheld are in no report this job makes"
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
    name: str | None = None,
) -> jobs.Job:
    """Queue one playlist job, one item per frozen track. The one spelling of it.

    ``run_id`` and ``source_id`` are what ``crate sync all`` adds, the run its
    sources share (R29) and the source that queued it, so ``sync mark`` finds
    one pass's jobs. ``name`` is the account's name for the playlist, which
    only a sweep has (U113); without it the job lands in its batch's playlist.
    """
    payload: dict[str, Any] = {SOURCE: reference, TRACKS: dict(tracks)}
    if run_id is not None:
        payload["run_id"] = run_id
    if source_id is not None:
        payload["source_id"] = source_id
    if name:
        payload[PLAYLIST_NAME] = name
    return jobs.enqueue(
        store, handler_key=handler_key, payload=payload, cfg=cfg, item_ids=tuple(tracks)
    )


def intake_playlist(ctx) -> Envelope:
    """List the playlist through the catalogue seam and queue one item per track.

    The catalogue is looked up on its module at call time, the contract
    ``label/catalogue.py`` states, so a test can substitute the seam.
    ``favorites`` queues the account's hearts under the same key, recorded
    under the canonical spelling so the resume argv names it however it was typed.
    """
    from cratekit.label import catalogue  # noqa: PLC0415 - labels is toggleable

    cfg = _load()
    with jobs.open_store() as store:
        if ctx.args.job:
            return _resume(ctx, store, ctx.args.job)
        reference = str(ctx.args.source)
        hearts = is_favorites(reference)
        if hearts:
            reference = FAVORITES
        found = catalogue.resolve(cfg)
        if hearts:
            tracks, short = list_favorites(found)
            warned = withheld_warning
        else:
            tracks, short = list_playlist_declared(found, reference)

            def warned(short):
                return playlist_withheld_warning(short, reference)

        # A short listing is said whatever else the run does (R-504, R-515).
        extra = {"shortfall": short.block()} if short is not None else {}
        warnings = (warned(short),) if short is not None else ()
        if not tracks:
            return ctx.envelope(
                data=no_job("no-tracks", source=reference, **extra),
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
        return ctx.envelope(data=jobs.reported(store, job, extra), warnings=warnings)


# ---------------------------------------------------------------------------
# The worker
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _Resolved:
    """One drive's view of the library and the tombstones, built once."""

    index: match.LibraryIndex
    suppresses: Any
    suppression_id: Any


#: ONE INDEX PER DRIVE, not one per item, keyed by the job and its attempt so a
#: resume walks again and sees what the previous drive's offers changed. A
#: module global older than the job engine's per drive seam (U274), so
#: ``reset_cache`` is what a suite calls between libraries. Since U249 a walk
#: opens only a file the index reader cannot answer from memory.
_RESOLVED: dict[tuple[str, int], _Resolved] = {}


def reset_cache() -> None:
    """Forget the cached library view, and every file the index reader
    remembers, so one test's library cannot leak into the next."""
    _RESOLVED.clear()
    match.reset_cache()


def _resolved_for(job: jobs.Job, cfg: config.Config) -> _Resolved:
    key = (job.job_id, job.attempts)
    held = _RESOLVED.get(key)
    if held is not None:
        return held
    index, suppresses, identify_one = match_cli.library_view(cfg)
    built = _Resolved(index=index, suppresses=suppresses, suppression_id=identify_one)
    _RESOLVED.clear()
    _RESOLVED[key] = built
    return built


def resolve_track(wanted: Wanted, job: jobs.Job, cfg: config.Config) -> match.TrackMatch:
    """One track against the frozen library, with its question offered.

    ``match.run``'s three steps over one row: resolve, let the review queue
    turn a question into an item, and read back any answer already given; the
    offer is idempotent. The review store opens only for a row that touches
    it, a question or a row a rule owns whose earlier question is retired.
    """
    view = _resolved_for(job, cfg)
    found = match.resolve_one(
        wanted, view.index, suppresses=view.suppresses, suppression_id=view.suppression_id
    )
    if not match_cli.touches_the_queue(found):
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

    The payload is read at the item's own key, and a key it does not carry is
    refused rather than resolved as an empty row. ``cfg`` is the configuration
    the job was frozen against (KTD9). The report says which of the verb's
    four words the track resolved to, and never says acquired.
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
    settled = resolve_track(thawed(said), job, cfg)
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
    return ARTIFACTS.produced(cfg, job, item, report)
