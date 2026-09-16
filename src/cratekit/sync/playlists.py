"""The playlists source: list the account, keep what is new, queue it as intake.

The third R25 source, and the one the slim profile runs alone. It has no worker
of its own. Each account playlist it keeps is queued through
``intake.cli.queue_playlist``, under ``intake.playlist``, which is exactly the job
``crate intake playlist`` queues for the same playlist, with two keys added: the
intake run the pass shares (R29) and ``source_id``, which is how this module
later finds the jobs it queued. A separate playlists worker with its own item
shape was rejected for the reason U61 rejected a fourth worker: it would rebuild
the intake path one layer down.

**WHAT IS NEW, IN THE ORDER IT IS DECIDED.** A playlist is excluded when its
name carries the swept prefix the source system applies after a sweep, when its
identifier is in this source's cursor, when its name is a quarterly favourites
placeholder, which is the favourites source's to sweep, when a job this source
queued for it is still open, or when the listing says it holds no tracks.
Everything else is listed track by track and queued. A playlist whose tracks
come back empty is reported empty rather than queued, and a playlist that cannot
be read is reported unreadable rather than skipped in silence.

**THE CURSOR IS IDENTIFIERS, AND IT MOVES ON CLEAN COMPLETION ONLY.** Queueing
is not completion. At the start of every pass :func:`reconcile` reads the jobs
this source queued, and records the playlist of every one that SUCCEEDED, which
is the state a job reaches only when every item is done. A failed or cancelled
job is not recorded and its playlist is offered again. Nothing is ever filtered
by title except the two naming conventions above, which are conventions spelled
in the name by the systems that apply them, and neither is stored (D5).

**THE MARK IS UNBOUND.** ``sync/marks.py`` states the rule: a remote playlist is
renamed only after the importable file exists and a recheck holds. Two things
are missing for that here, and both are reported rather than worked around. The
account seam, ``modules.outbound.service.RemoteAccount``, declares no rename, so
there is nothing to apply the mark through; and the intake worker writes no
importable file, since it resolves tracks and does not acquire them. So every
pass reports the mark as :data:`MARK_UNBOUND`, on R-203's pattern, and the cursor
is the only record a sweep leaves.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from cratekit.core import config, jobs
from cratekit.core.cause import CratekitError, Scope, refuse
from cratekit.favorites import placeholders
from cratekit.intake import cli as intake_cli
from cratekit.label.catalogue import AccountPlaylist, Catalogue
from cratekit.sync.watermarks import WatermarkStore

#: This source's identifier, as ``sync.sources`` declares it and as the jobs it
#: queues carry it.
SOURCE_ID = "playlists"

#: The prefix the source system puts on a playlist it has swept. The same
#: convention its analysis pass skips a prefixed name by, kept rather than
#: reinvented, because the live account already carries it.
SWEPT_PREFIX = "DOWNLOADED "

#: What the pass says about the mark step, every time, until the account seam
#: can rename a playlist.
MARK_UNBOUND = "unbound"

#: The two refusals one playlist's listing may end in that are about THAT
#: playlist. Any other refusal, a credential or an unbound adapter, is about the
#: whole source and ends it.
PER_PLAYLIST_REASONS = frozenset({"label-playlist-unreadable", "intake-list-unusable"})


class Excluded(StrEnum):
    """Why a listed playlist was not queued."""

    SWEPT = "already-swept"
    RECORDED = "recorded"
    PLACEHOLDER = "favorites-placeholder"
    IN_FLIGHT = "in-flight"
    EMPTY = "empty"
    UNREADABLE = "unreadable"


def is_swept_name(name: str) -> bool:
    """Whether the name carries the swept prefix."""
    return str(name or "").startswith(SWEPT_PREFIX)


def exclusion(
    playlist: AccountPlaylist,
    *,
    recorded: frozenset[str] | set[str],
    in_flight: frozenset[str] | set[str],
) -> Excluded | None:
    """Why this playlist is not new, or ``None`` when it is. Pure.

    The ORDER is the report's, not a precedence any one playlist depends on: a
    playlist can meet several rules, and the first one named is the one a person
    is told.
    """
    if is_swept_name(playlist.name):
        return Excluded.SWEPT
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

    All three fields, because each alone names jobs this source does not own:
    the key is shared with ``crate intake playlist`` run by hand, and the queue is
    installation scoped while the cursor is per library.
    """
    return tuple(
        job
        for job in jobs.list_jobs(store)
        if job.handler_key == handler_key
        and (job.payload or {}).get("source_id") == SOURCE_ID
        and job.library_id == cfg.library.volume_id
    )


def _playlist_of(job: jobs.Job) -> str:
    return str((job.payload or {}).get(intake_cli.SOURCE) or "")


def completed(found: Iterable[jobs.Job]) -> tuple[str, ...]:
    """The playlists whose job succeeded, oldest first, each once."""
    seen: list[str] = []
    for job in reversed(tuple(found)):
        identity = _playlist_of(job)
        if job.state == jobs.JobState.SUCCEEDED and identity and identity not in seen:
            seen.append(identity)
    return tuple(seen)


def open_playlists(found: Iterable[jobs.Job]) -> frozenset[str]:
    """The playlists a job this source queued is still working on."""
    return frozenset(
        _playlist_of(job) for job in found if job.is_open() and _playlist_of(job)
    )


def reconcile(store, cfg: config.Config, *, handler_key: str) -> tuple[str, ...]:
    """Record every playlist whose job completed cleanly. Returns the newly recorded."""
    marks = WatermarkStore(cfg)
    existing = marks.read(SOURCE_ID)
    known = set(existing.swept) if existing is not None else set()
    fresh = [
        identity
        for identity in completed(source_jobs(store, cfg, handler_key=handler_key))
        if identity not in known
    ]
    marks.record_swept(SOURCE_ID, fresh, library_id=cfg.library.volume_id)
    return tuple(fresh)


@dataclass
class Sweep:
    """What one pass decided about every playlist the account listed."""

    listed: tuple[AccountPlaylist, ...] = ()
    #: Playlist identifier to frozen tracks, in listing order, for the queue.
    ready: dict[str, dict[str, Any]] = field(default_factory=dict)
    excluded: dict[str, Excluded] = field(default_factory=dict)
    unreadable: dict[str, str] = field(default_factory=dict)
    recorded_now: tuple[str, ...] = ()

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


def plan(
    store,
    cfg: config.Config,
    found: Catalogue,
    *,
    handler_key: str,
) -> Sweep:
    """Reconcile the cursor, list the account, and decide every playlist.

    Reconciled FIRST so a playlist whose job finished since the last pass is
    excluded as recorded in this one rather than queued again.
    """
    recorded_now = reconcile(store, cfg, handler_key=handler_key)
    existing = WatermarkStore(cfg).read(SOURCE_ID)
    recorded = frozenset(existing.swept) if existing is not None else frozenset()
    in_flight = open_playlists(source_jobs(store, cfg, handler_key=handler_key))

    sweep = Sweep(listed=_listed_or_refuse(found), recorded_now=recorded_now)
    for playlist in sweep.listed:
        reason = exclusion(playlist, recorded=recorded, in_flight=in_flight)
        if reason is not None:
            sweep.excluded[playlist.playlist_id] = reason
            continue
        try:
            tracks = intake_cli.list_playlist(found, playlist.playlist_id)
        except CratekitError as exc:
            if exc.cause.reason not in PER_PLAYLIST_REASONS:
                raise
            sweep.excluded[playlist.playlist_id] = Excluded.UNREADABLE
            sweep.unreadable[playlist.playlist_id] = exc.cause.message
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

    ``filed`` is appended to AS EACH JOB IS QUEUED, because each enqueue is its
    own transaction: a refusal on the third playlist leaves the first two filed,
    and the caller has to be able to name them.
    """
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
            )
        )


def report(sweep: Sweep, filed: Sequence[jobs.Job]) -> dict[str, Any]:
    """The playlists block of the pass summary. Identifiers first, names to read."""
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
        "recorded_now": list(sweep.recorded_now),
        "mark": MARK_UNBOUND,
    }


__all__ = [
    "MARK_UNBOUND",
    "PER_PLAYLIST_REASONS",
    "SOURCE_ID",
    "SWEPT_PREFIX",
    "Excluded",
    "Sweep",
    "completed",
    "exclusion",
    "is_swept_name",
    "open_playlists",
    "plan",
    "queue",
    "reconcile",
    "report",
    "source_jobs",
]
