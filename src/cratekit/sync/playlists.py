"""The playlists source: list the account, keep what is new, queue it as intake.

The core R25 source, with no worker of its own: each kept playlist is queued
through ``intake.cli.queue_playlist`` exactly as ``crate intake playlist``
queues it, plus the shared intake run (R29) and ``source_id``, by which this
module finds its jobs again.

**WHAT IS NEW, IN THE ORDER IT IS DECIDED.** A playlist is excluded when it is
taken (:func:`is_taken`), is label batch debris (R-361), is in the cursor, is
a favourites placeholder, has an open intake job, or lists no tracks. The rest
are listed track by track and queued; an empty one is reported empty and an
unreadable one reported, never skipped in silence. A track with no title or
artist is set aside and named while the rest queue (R-1289).

**THE DEBRIS RULE IS THE SOURCE SYSTEM'S, SUFFIX AND CASE (R-361).** A name
ending ` LIBRARY`, case sensitive, is excluded, copied rather than narrowed.
The source system also drops ids its manifests registered, which has no
counterpart here. :func:`pending_marks` keeps debris out of the mark too.

**THE CURSOR IS IDENTIFIERS, AND IT MOVES ON CLEAN COMPLETION ONLY.** At the
top of every pass :func:`reconcile` records the playlist of every SUCCEEDED
playlist intake job for this library, whichever verb queued it (R-382). A
failed or cancelled one is offered again and an open one is held back as in
flight. Nothing is filtered by title except the naming conventions above, and
none is stored (D5).

**SWEPT MEANS RESOLVED, NOT ACQUIRED, AND THE PASS SAYS SO (R-359).** A
succeeded job resolved every track and acquired none, yet it is never offered
again; every block carries :data:`SWEPT_MEANS` and :func:`said` words it.

**THE MARK IS ITS OWN VERB, AND THE PASS STILL MARKS NOTHING (U82).** The
importable file arrives verbs later, so :func:`mark_swept` is called by
``sync/mark_cli.py`` and the pass reports :data:`MARK_UNBOUND`.

**THE RECHECK IS A SECOND READ, NOT THE PLAN'S OWN**, since one served from
the planning read can never catch a playlist that changed in between. It is
read once per batch.

**THE MARK SET IS THE CURSOR, NOT WHAT THIS PASS ADDED TO IT**; see
:func:`pending_marks`.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Any

from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.intake import cli as intake_cli
from cratekit.sync import marks
from cratekit.sync.watermarks import WatermarkStore

if TYPE_CHECKING:
    from cratekit.label.catalogue import AccountPlaylist, Catalogue

#: This source's identifier, as ``sync.sources`` declares it and its jobs carry it.
SOURCE_ID = "playlists"

#: The legacy swept prefix, RETIRED (U242). No verb writes it; a title still
#: carrying it reads as taken until ``crate sync strip`` takes it off.
SWEPT_PREFIX = "DOWNLOADED "

#: The suffix of the label batch's throwaway `<label> LIBRARY` playlists (R-361).
#: Case sensitive on purpose, since a person could name one `Colorize Library`.
LIBRARY_PLAYLIST_SUFFIX = " LIBRARY"

#: What a recorded playlist means, on the machine block: resolved, none acquired (R-359).
SWEPT_MEANS = "resolved-not-acquired"

#: The same fact in words, keyed by the token, so it shows exactly when the field does.
SWEPT_MEANS_SAID: Mapping[str, str] = MappingProxyType(
    {
        SWEPT_MEANS: (
            "a recorded playlist had its tracks resolved against the library, not "
            "acquired, so a track its intake job reported missing is still not in "
            "the library, crate intake missing lists it, and no later sync offers "
            "that playlist again"
        ),
    }
)

#: The mark step as every pass reports it, since a pass writes no importable file.
MARK_UNBOUND = "unbound"

#: What the pass says when :func:`mark_swept` ran against the account seam.
MARK_APPLIED = "applied"

#: The kind of every mark this source defers, a taken entry in the record (U242).
MARK_KIND = "taken"

#: The refusals about ONE playlist's listing; any other ends the whole source.
PER_PLAYLIST_REASONS = frozenset({"label-playlist-unreadable", "intake-list-unusable"})


class Excluded(StrEnum):
    """Why a listed playlist was not queued."""

    SWEPT = "already-swept"
    LABEL_DEBRIS = "label-debris"
    #: A year playlist ``label playlists`` built, a label's catalogue (R-835).
    LABEL_FOLDER = "label-folder"
    #: A playlist ``export set`` made, which would be a second download (R-837).
    SET_PLAYLIST = "set-playlist"
    #: A playlist ``sync pair`` keeps, which would otherwise be queued twice (U130).
    PAIRED = "paired"
    #: A playlist ``crate organize`` mirrors from rekordbox, already owned (U147).
    MIRROR = "mirror"
    RECORDED = "recorded"
    PLACEHOLDER = "favorites-placeholder"
    IN_FLIGHT = "in-flight"
    EMPTY = "empty"
    UNREADABLE = "unreadable"


def is_swept_name(name: str) -> bool:
    """Whether the name carries the legacy swept prefix.

    Readers asking "taken" use :func:`is_taken`; this is for the migration and
    the strip.
    """
    return str(name or "").startswith(SWEPT_PREFIX)


def untaken_name(name: str) -> str:
    """The title less every copy of the legacy prefix and the spaces around what is left."""
    text = str(name or "")
    while text.startswith(SWEPT_PREFIX):
        text = text[len(SWEPT_PREFIX) :]
    return text.strip()


def is_taken(
    playlist_id: str, name: str, taken: frozenset[str] | set[str] | Mapping[str, Any]
) -> bool:
    """Whether Cratekit holds this playlist as taken, finished with (U242). Pure.

    THE ONE QUESTION EVERY READER ASKS. Held in ``taken``, whatever its title,
    or still carrying the legacy prefix, so it never reads as new in between.
    """
    return str(playlist_id or "") in taken or is_swept_name(name)


def taken_ids(cfg: config.Config) -> frozenset[str]:
    """Every playlist the record holds as taken, or the record's own refusal.

    UNREAD IS NOT NONE, since empty would offer every taken playlist as new.
    """
    from cratekit.sync import mark_record

    return mark_record.MarkRecord(cfg).taken_ids()


def is_library_debris(name: str) -> bool:
    """Whether the name ends with the label batch's debris suffix, case exactly."""
    return str(name or "").endswith(LIBRARY_PLAYLIST_SUFFIX)


def exclusion(
    playlist: AccountPlaylist,
    *,
    recorded: frozenset[str] | set[str],
    in_flight: frozenset[str] | set[str],
    label_built: frozenset[str] | set[str] = frozenset(),
    set_built: frozenset[str] | set[str] = frozenset(),
    paired: frozenset[str] | set[str] = frozenset(),
    mirrored: frozenset[str] | set[str] = frozenset(),
    taken: frozenset[str] | set[str] = frozenset(),
) -> Excluded | None:
    """Why this playlist is not new, or ``None`` when it is. Pure.

    The ORDER only picks which reason a person is told. A playlist in
    ``taken`` is :attr:`Excluded.SWEPT` whatever its title.
    """
    from cratekit.favorites import placeholders
    if is_taken(playlist.playlist_id, playlist.name, taken):
        return Excluded.SWEPT
    if is_library_debris(playlist.name):
        return Excluded.LABEL_DEBRIS
    if playlist.playlist_id in label_built:
        return Excluded.LABEL_FOLDER
    if playlist.playlist_id in set_built:
        return Excluded.SET_PLAYLIST
    if playlist.playlist_id in paired:
        return Excluded.PAIRED
    if playlist.playlist_id in mirrored:
        return Excluded.MIRROR
    if playlist.playlist_id in recorded:
        return Excluded.RECORDED
    if placeholders.is_placeholder(playlist.name):
        return Excluded.PLACEHOLDER
    if playlist.playlist_id in in_flight:
        return Excluded.IN_FLIGHT
    if playlist.tracks == 0:
        return Excluded.EMPTY
    return None


def source_jobs(store, cfg: config.Config, *, handler_key: str) -> tuple[jobs.Job, ...]:
    """Every job THIS source queued for THIS library, newest first.

    All three fields, since the key is shared with ``crate intake playlist``
    and the queue is installation scoped. NOT WHAT THE CURSOR IS RECONCILED
    OVER, which is :func:`playlist_jobs` (R-382).
    """
    return tuple(
        job
        for job in jobs.list_jobs(store)
        if job.handler_key == handler_key
        and (job.payload or {}).get("source_id") == SOURCE_ID
        and job.library_id == cfg.library.volume_id
    )


def playlist_of(job: jobs.Job) -> str:
    """The account playlist a job this source queued is about, or ``""``."""
    return str((job.payload or {}).get(intake_cli.SOURCE) or "")


_playlist_of = playlist_of


def recorded_as(job: jobs.Job) -> str:
    """The identifier the cursor records for a playlist intake job, or ``""``.

    This source's own job carries the listing's identifier, returned verbatim.
    A hand queued job carries what a person TYPED, so it is parsed to the
    identifier a listing would carry, or kept as typed when unrecognised.
    THE HEARTS ARE NOT A PLAYLIST, so a favourites job records nothing.
    """
    from cratekit.label.catalogue import PlaylistReferenceInvalid
    from cratekit.label.catalogue import playlist_id as typed_playlist_id
    reference = _playlist_of(job)
    if not reference:
        return ""
    if (job.payload or {}).get("source_id") == SOURCE_ID:
        return reference
    if intake_cli.is_favorites(reference):
        return ""
    try:
        return typed_playlist_id(reference)
    except PlaylistReferenceInvalid:
        return reference


def playlist_jobs(store, cfg: config.Config, *, handler_key: str) -> tuple[jobs.Job, ...]:
    """Every playlist intake job for THIS library, whichever verb queued it (R-382).

    What the cursor is reconciled over and an open job holds back, wider than
    :func:`source_jobs` because a hand run playlist is resolved just as a sweep
    would. Readers skip the hearts via :func:`recorded_as`.
    """
    return tuple(
        job
        for job in jobs.list_jobs(store)
        if job.handler_key == handler_key and job.library_id == cfg.library.volume_id
    )


def completed(found: Iterable[jobs.Job]) -> tuple[str, ...]:
    """The playlists whose job succeeded, oldest first, each once."""
    seen: list[str] = []
    for job in reversed(tuple(found)):
        identity = recorded_as(job)
        if job.state == jobs.JobState.SUCCEEDED and identity and identity not in seen:
            seen.append(identity)
    return tuple(seen)


def open_playlists(found: Iterable[jobs.Job]) -> frozenset[str]:
    """The playlists an open playlist intake job is still working on."""
    return frozenset(recorded_as(job) for job in found if job.is_open() and recorded_as(job))


def reconcile(store, cfg: config.Config, *, handler_key: str) -> tuple[str, ...]:
    """Record every playlist whose job completed cleanly. Returns the newly recorded."""
    # NOT ``marks``, which would shadow the deferred mark engine.
    cursor = WatermarkStore(cfg)
    existing = cursor.read(SOURCE_ID)
    known = set(existing.swept) if existing is not None else set()
    fresh = [
        identity
        for identity in completed(playlist_jobs(store, cfg, handler_key=handler_key))
        if identity not in known
    ]
    cursor.record_swept(SOURCE_ID, fresh, library_id=cfg.library.volume_id)
    return tuple(fresh)


@dataclass
class Sweep:
    """What one pass decided about every playlist the account listed."""

    listed: tuple[AccountPlaylist, ...] = ()
    #: Playlist identifier to frozen tracks, in listing order, for the queue.
    ready: dict[str, dict[str, Any]] = field(default_factory=dict)
    excluded: dict[str, Excluded] = field(default_factory=dict)
    unreadable: dict[str, str] = field(default_factory=dict)
    #: Playlists that listed short of the declared count (R-515), queued all the same.
    short: dict[str, dict[str, int]] = field(default_factory=dict)
    #: Each track set aside, by playlist then track, with its name and why (R-1289).
    unread: dict[str, dict[str, dict[str, str]]] = field(default_factory=dict)
    recorded_now: tuple[str, ...] = ()
    #: THE WHOLE CURSOR after reconciling, what :func:`mark_swept` marks from
    #: (see :func:`pending_marks`).
    recorded: frozenset[str] = frozenset()
    #: Every playlist held as taken, read once with the listing (U242).
    taken: frozenset[str] = frozenset()

    def names(self) -> dict[str, str]:
        return {playlist.playlist_id: playlist.name for playlist in self.listed}


def _listed_or_refuse(found: Catalogue) -> tuple[AccountPlaylist, ...]:
    try:
        return tuple(found.account_playlists())
    except CratekitError:
        raise
    except Exception as exc:
        raise refuse(
            "sync-source-lookups-failed",
            f"the account's playlists could not be listed ({type(exc).__name__}: "
            f"{exc}); an unread listing is not an account with nothing new",
            steps=("retry the sync when the provider is reachable",),
            scope=Scope.SOURCE,
            origin=("sync.playlists",),
            detail={"source_id": SOURCE_ID},
        ) from exc


def account_listing(found: Catalogue) -> tuple[AccountPlaylist, ...]:
    """Every playlist the account lists, with the count it declares, or the refusal (U287)."""
    return _listed_or_refuse(found)


def account_names(found: Catalogue) -> dict[str, str]:
    """Every playlist the account lists, identifier to name, or the refusal (R-838)."""
    return {playlist.playlist_id: playlist.name for playlist in _listed_or_refuse(found)}


def plan(
    store,
    cfg: config.Config,
    found: Catalogue,
    *,
    handler_key: str,
    label_built: frozenset[str] = frozenset(),
    set_built: frozenset[str] = frozenset(),
    paired: frozenset[str] = frozenset(),
    mirrored: frozenset[str] = frozenset(),
) -> Sweep:
    """Reconcile the cursor, list the account, and decide every playlist.

    Reconciled FIRST so a job finished since the last pass excludes its
    playlist rather than queueing it again. ``label_built``, ``set_built``,
    ``paired`` and ``mirrored`` are HANDED IN, since a core module does not
    import the packages that record them.
    """
    recorded_now = reconcile(store, cfg, handler_key=handler_key)
    existing = WatermarkStore(cfg).read(SOURCE_ID)
    recorded = frozenset(existing.swept) if existing is not None else frozenset()
    in_flight = open_playlists(playlist_jobs(store, cfg, handler_key=handler_key))
    taken = taken_ids(cfg)

    sweep = Sweep(
        listed=_listed_or_refuse(found),
        recorded_now=recorded_now,
        recorded=recorded,
        taken=taken,
    )
    for playlist in sweep.listed:
        reason = exclusion(
            playlist,
            recorded=recorded,
            in_flight=in_flight,
            label_built=label_built,
            set_built=set_built,
            paired=paired,
            mirrored=mirrored,
            taken=taken,
        )
        if reason is not None:
            sweep.excluded[playlist.playlist_id] = reason
            continue
        try:
            # ROW BY ROW (R-1289). A track with no title or artist is set aside;
            # a row with no provider id still refuses the listing.
            listing = intake_cli.list_playlist_readable(found, playlist.playlist_id)
        except CratekitError as exc:
            if exc.cause.reason not in PER_PLAYLIST_REASONS:
                raise
            sweep.excluded[playlist.playlist_id] = Excluded.UNREADABLE
            sweep.unreadable[playlist.playlist_id] = exc.cause.message
            continue
        tracks = listing.tracks
        if listing.short is not None:
            # SAID, NEVER REFUSED (R-515); the rows served are queued.
            sweep.short[playlist.playlist_id] = listing.short.block()
        if listing.unread:
            sweep.unread[playlist.playlist_id] = {
                ref: {**one.said(), "why": one.why} for ref, one in listing.unread.items()
            }
            if not tracks:
                # EVERY TRACK UNREAD is unreadable, not empty, so it is offered again.
                sweep.excluded[playlist.playlist_id] = Excluded.UNREADABLE
                sweep.unreadable[playlist.playlist_id] = (
                    "no track on it could be queued: "
                    + ", ".join(f"{ref} ({one.why})" for ref, one in listing.unread.items())
                )
                continue
        if not tracks:
            # THE COUNT WAS UNKNOWN OR STALE, and the listing is what answers.
            sweep.excluded[playlist.playlist_id] = Excluded.EMPTY
            continue
        sweep.ready[playlist.playlist_id] = tracks
    return sweep


def queue(
    store,
    cfg: config.Config,
    sweep: Sweep,
    *,
    handler_key: str,
    run_id: str,
    filed: list[jobs.Job],
) -> None:
    """Queue one intake playlist job per ready playlist, under the shared run.

    ``filed`` is appended to AS EACH JOB IS QUEUED, since each enqueue is its
    own transaction and a caller must name what was filed before a refusal.
    Each job carries the listed name (U113) for the landing's INBOX playlist.
    """
    names = sweep.names()
    for playlist_id, tracks in sweep.ready.items():
        filed.append(
            intake_cli.queue_playlist(
                store,
                cfg,
                handler_key=handler_key,
                reference=playlist_id,
                tracks=tracks,
                run_id=run_id,
                source_id=SOURCE_ID,
                name=names.get(playlist_id),
            )
        )


def marking_sweep(store, cfg: config.Config, found: Catalogue, *, handler_key: str) -> Sweep:
    """The sweep a mark is taken from, built WITHOUT MOVING THE CURSOR.

    The mark verb stops at a gate first, so it must not write state an abort
    would leave behind. ``recorded`` is the cursor TOGETHER WITH what
    :func:`reconcile` would add (by :func:`completed`), since nothing
    reconciles between the pass and the mark.
    """
    existing = WatermarkStore(cfg).read(SOURCE_ID)
    held = set(existing.swept) if existing is not None else set()
    held.update(completed(playlist_jobs(store, cfg, handler_key=handler_key)))
    return Sweep(
        listed=_listed_or_refuse(found), recorded=frozenset(held), taken=taken_ids(cfg)
    )


def pending_marks(
    sweep: Sweep, *, only: frozenset[str] | None = None
) -> tuple[marks.PendingMark, ...]:
    """Every recorded playlist the account still lists and the record does not hold as taken.

    ``only`` NARROWS AND NEVER WIDENS. ``None`` is every pending playlist and
    an empty set is none, so ``if only`` would be wrong.

    **THE SET IS THE WHOLE CURSOR AND NOT** :attr:`Sweep.recorded_now`. The
    cursor moves before any mark and whether or not it lands, so a set of what
    this pass added could never be offered again; from the whole cursor, an
    unlanded mark is retried and a taken one drops out.

    A playlist no longer listed is owed nothing. **THE LABEL BATCH'S DEBRIS IS
    NEVER MARKED (R-361)**, asked here too because :func:`exclusion` decides
    what is offered and this decides what is taken.
    """
    listed = sweep.names()
    return tuple(
        marks.PendingMark(target_id=identity, kind=MARK_KIND)
        for identity in sorted(sweep.recorded)
        if listed.get(identity)
        and not is_taken(identity, listed[identity], sweep.taken)
        and not is_library_debris(listed[identity])
        and (only is None or identity in only)
    )


def mark_swept(
    sweep: Sweep,
    found: Catalogue,
    take: Callable[[str, str], None],
    *,
    local_output: Path | marks.NativeLanding,
    applied: list[str] | None = None,
    only: frozenset[str] | None = None,
) -> tuple[str, ...]:
    """Hold the recorded playlists as taken. Returns the taken ids.

    **NO TITLE CHANGES (U242).** The account is only read, to recheck; ``take``
    records each id and listed title in the ledger, raising when it cannot.

    **THE FILE IS CHECKED FIRST AND BY** :func:`marks.apply_deferred`, with no
    early return in front, so nothing pending and no file still refuses.
    ``applied`` is APPENDED TO AS EACH TAKE LANDS, so a caller can name what
    landed when this raises. The one production caller is ``sync/mark_cli.py``.
    """
    listed = sweep.names()
    landed = applied if applied is not None else []
    held: list[dict[str, str]] = []

    def current() -> dict[str, str]:
        """The account's names now, read ONCE and only when a mark asks."""
        if not held:
            held.append(
                {
                    playlist.playlist_id: playlist.name
                    for playlist in _listed_or_refuse(found)
                }
            )
        return held[0]

    def recheck(mark: marks.PendingMark) -> bool:
        name = listed.get(mark.target_id) or ""
        return bool(name) and current().get(mark.target_id) == name

    def apply(mark: marks.PendingMark) -> None:
        take(mark.target_id, listed[mark.target_id])
        landed.append(mark.target_id)

    return marks.apply_deferred(
        pending_marks(sweep, only=only),
        local_output=local_output,
        recheck=recheck,
        apply=apply,
    )


def report(
    sweep: Sweep, filed: Sequence[jobs.Job], *, marked: Sequence[str] | None = None
) -> dict[str, Any]:
    """The playlists block of the pass summary. Identifiers first, names to read.

    ``marked`` of ``None`` reports :data:`MARK_UNBOUND`; an empty result reports
    :data:`MARK_APPLIED`, a mark step that found every recheck stale.
    """
    names = sweep.names()
    return {
        "listed": len(sweep.listed),
        "queued": [
            {
                "playlist_id": _playlist_of(job),
                "name": names.get(_playlist_of(job), ""),
                "job_id": job.job_id,
                "items": len((job.payload or {}).get(intake_cli.TRACKS) or {}),
            }
            for job in filed
        ],
        "excluded": {
            identity: {"reason": str(reason), "name": names.get(identity, "")}
            for identity, reason in sweep.excluded.items()
        },
        "unreadable": dict(sweep.unreadable),
        "withheld": {
            identity: {**block, "name": names.get(identity, "")}
            for identity, block in sweep.short.items()
        },
        "unread": {
            identity: {"name": names.get(identity, ""), "tracks": dict(tracks)}
            for identity, tracks in sweep.unread.items()
        },
        "recorded_now": list(sweep.recorded_now),
        "swept_means": SWEPT_MEANS,
        "mark": MARK_UNBOUND if marked is None else MARK_APPLIED,
        "marked": list(marked or ()),
    }


def said(block: Mapping[str, Any]) -> str | None:
    """The words for what the block says swept means, or ``None`` when it says nothing.

    Read off the block's own token, so the words go when the field does.
    """
    return SWEPT_MEANS_SAID.get(str(block.get("swept_means") or ""))


__all__ = [
    "LIBRARY_PLAYLIST_SUFFIX",
    "MARK_APPLIED",
    "MARK_KIND",
    "MARK_UNBOUND",
    "PER_PLAYLIST_REASONS",
    "SOURCE_ID",
    "SWEPT_MEANS",
    "SWEPT_MEANS_SAID",
    "SWEPT_PREFIX",
    "Excluded",
    "Sweep",
    "account_listing",
    "account_names",
    "completed",
    "exclusion",
    "is_library_debris",
    "is_swept_name",
    "is_taken",
    "mark_swept",
    "marking_sweep",
    "open_playlists",
    "pending_marks",
    "playlist_jobs",
    "playlist_of",
    "plan",
    "queue",
    "reconcile",
    "recorded_as",
    "report",
    "said",
    "source_jobs",
    "taken_ids",
    "untaken_name",
]
