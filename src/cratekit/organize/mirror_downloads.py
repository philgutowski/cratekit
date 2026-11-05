"""A track added on the account to a mirrored playlist that the library lacks, queued (U204).

``crate organize``'s rekordbox area step ``mirror-downloads``. The account
mirror reads each mirrored playlist three ways and
:mod:`cratekit.modules.outbound.mirror_edits` decides what a person changed on
the account. A track added there that the library owns no row for, and that
no snapshot ever held, is held on the account with ``acquire`` set. This step
queues each one for download, AS ``sync pair`` QUEUES ONE: frozen through
``intake_cli.list_playlist_declared``, the reading a playlist job is queued
from, and queued with ``intake_cli.queue_playlist`` under the ``intake
playlist`` job, one job per account playlist, carrying this step's own source
identifier.

ONCE. A track any mirror job still holds, open, done or landed, is named as
awaiting its landing and never queued again; only a job that failed or was
cancelled frees it, as ``sync pair`` reads its own. The apply reads the queue
again before it writes, so two runs approved one after the other queue a track
once.

AND FILED WHEN IT LANDS. The landing puts the file in an INBOX batch, which the
mirror reads, so the next organize matches its row and reads the account's
addition as one the library can take. Where the provider holds the recording
on several releases the matcher may tie the landed row to another one, so
:func:`landed` hands the edit rule each queued track's row by the ISRC the job
froze for it.

A PLAYLIST THE PROVIDER WILL NOT LIST, or that lists short of the track, queues
nothing for it and says why, since a track the reading cannot freeze is a
track the job cannot be asked about; every other playlist is planned.

ANOTHER RELEASE OF A RECORDING THE LIBRARY HOLDS IS NEVER QUEUED. A track the
account matched no library row to may still carry the ISRC of a row the
library owns, linked to another release or in no mirrored playlist at all:
the job would resolve it owned and land nothing, so it is named and left on
the account as it is, never downloaded and never awaited.

Layer: modules.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from cratekit.cli.output import digest_of
from cratekit.core import config
from cratekit.core.cause import CratekitError
from cratekit.organize.steps import LISTED, NOTHING, PLANNED, Step, refused

#: The step kind ``--only`` names this by.
KIND = "mirror-downloads"

TITLE = (
    "queue for download each track added on the account to a mirrored playlist that "
    "the library lacks"
)

#: The handler key a download is queued under, ``sync pair``'s own: the
#: ``intake playlist`` job, which resolves each track to owned, offered or
#: missing for ``acquire`` to download and ``intake land`` to land.
HANDLER = "intake.playlist"

#: The ``source_id`` every job this step queues carries, so a later run finds
#: the tracks it already queued and does not queue them again.
SOURCE_ID = "account-mirror"


def _jobs(cfg: config.Config) -> list[Any]:
    """Every intake job this step queued on this library that did not fail."""
    from cratekit.core import jobs

    with jobs.open_store() as store:
        return [
            job
            for job in jobs.list_jobs(store)
            if job.handler_key == HANDLER
            and job.library_id == cfg.library.volume_id
            and (job.payload or {}).get("source_id") == SOURCE_ID
            and job.state not in (jobs.JobState.FAILED, jobs.JobState.CANCELLED)
        ]


def queued(cfg: config.Config) -> dict[str, dict[str, Any]]:
    """Each account track a mirror job holds, to the track as the job froze it.

    Raises the queue's own refusal, or ``OSError``, when it cannot be read.
    """
    from cratekit.intake import cli as intake_cli

    held: dict[str, dict[str, Any]] = {}
    for job in _jobs(cfg):
        for remote, frozen in ((job.payload or {}).get(intake_cli.TRACKS) or {}).items():
            held.setdefault(str(remote), dict(frozen) if isinstance(frozen, Mapping) else {})
    return held


def landed(
    cfg: config.Config, seen: Mapping[str, tuple[str, str, str]]
) -> dict[str, tuple[str, ...]]:
    """Each queued account track to the library rows carrying the ISRC the job froze for it.

    ``seen`` is every row the mirror matched, content id to ``(account track,
    ISRC, reason)``. A queue that cannot be read ties nothing, which costs a
    landed track one more organize before it is filed, never a wrong row.
    """
    from cratekit.acquire import match

    try:
        held = queued(cfg)
    except (CratekitError, OSError, ValueError):
        return {}
    by_code: dict[str, set[str]] = {}
    for content_id, (_remote, code, _reason) in seen.items():
        token = match.isrc_token(code)
        if token:
            by_code.setdefault(token, set()).add(str(content_id))
    found: dict[str, tuple[str, ...]] = {}
    for remote, frozen in held.items():
        token = match.isrc_token(frozen.get("isrc"))
        if token and by_code.get(token):
            found[remote] = tuple(sorted(by_code[token]))
    return found


@dataclass(frozen=True, slots=True)
class Planned:
    """Every track to queue by account playlist, and every one not queued, named."""

    #: Account playlist identifier to ``(title, {track: frozen track})``.
    queue: Mapping[str, tuple[str, dict[str, dict[str, Any]]]] = field(default_factory=dict)
    named: tuple[dict[str, Any], ...] = ()

    def identity(self) -> dict[str, Any]:
        return {
            "kind": KIND,
            "queue": [[pid, sorted(tracks)] for pid, (_title, tracks) in sorted(self.queue.items())],
        }

    @property
    def tracks(self) -> int:
        return sum(len(tracks) for _title, tracks in self.queue.values())

    def items(self) -> list[dict[str, Any]]:
        shown: list[dict[str, Any]] = [
            {
                "playlist": title,
                "remote_id": pid,
                "queue": [
                    f"{frozen.get('artist') or ''} - {frozen.get('title') or ''} ({track})"
                    for track, frozen in sorted(tracks.items())
                ],
            }
            for pid, (title, tracks) in sorted(self.queue.items())
        ]
        return shown + list(self.named)


def _remote_of(recorded: Mapping[str, Any], folder: str, title: str) -> str:
    held = recorded.get(folder)
    entry = held.playlists.get(title) if held is not None else None
    return entry.remote_id if entry is not None else ""


def plan(
    cfg: config.Config, reading: Any, *, listed: Any = None, owned: Any = None
) -> Planned:
    """Every wanted track as it would be queued. Reads the queue, the provider and the library.

    ``listed`` lists one account playlist frozen as a playlist job is queued,
    ``(tracks, shortfall)``, the catalogue's by default; a playlist it cannot
    list is named and the rest are planned. ``owned`` answers each ISRC the
    library already holds with its rows, the database's and the mirror's
    matches by default. Raises the queue's refusal.
    """
    wanted: Sequence[Any] = reading.decided.wanted
    named: list[dict[str, Any]] = []
    if not wanted:
        return Planned()
    already = queued(cfg)
    grouped: dict[str, tuple[str, list[str]]] = {}
    taken: set[str] = set()
    for decision in wanted:
        # ONE TRACK, ONE QUEUE: a track added to two playlists, or read by two
        # trees, is queued with the first, and lands once.
        if decision.track in taken:
            continue
        if decision.track in already:
            named.append(
                {
                    **decision.item(),
                    "outcome": "awaiting its landing",
                    "why": (
                        f"{decision.why}; a mirror download already queued it, so it is "
                        f"not queued again"
                    ),
                }
            )
            continue
        place = decision.to
        pid = _remote_of(reading.recorded, place.folder, place.title) if place is not None else ""
        if not pid:
            named.append(
                {
                    **decision.item(),
                    "outcome": "not queued",
                    "why": f"{decision.why}; no mirrored playlist is recorded for it",
                }
            )
            continue
        grouped.setdefault(pid, (place.title, []))[1].append(decision.track)
        taken.add(decision.track)
    if listed is None:
        listed = _catalogue_listing(cfg)
    if owned is None:
        owned = _owned(cfg, reading)
    queue: dict[str, tuple[str, dict[str, dict[str, Any]]]] = {}
    for pid, (title, tracks) in sorted(grouped.items()):
        try:
            frozen, _short = listed(pid)
        except CratekitError as exc:
            named.extend(
                {
                    "track": track,
                    "playlist": title,
                    "outcome": "not queued",
                    "why": f"the provider could not list the playlist: {exc.cause.message}",
                }
                for track in sorted(set(tracks))
            )
            continue
        took: dict[str, dict[str, Any]] = {}
        for track in sorted(set(tracks)):
            rows = owned(frozen[track].get("isrc")) if track in frozen else ()
            if rows:
                # ANOTHER RELEASE OF A RECORDING THE LIBRARY HOLDS: nothing is
                # downloaded, and no landing is awaited that nothing will make.
                named.append(
                    {
                        "track": track,
                        "playlist": title,
                        "outcome": "not queued",
                        "why": (
                            f"added on the account, and the library already holds its "
                            f"recording (row {', '.join(rows)}) as another release than "
                            f"this one, so nothing is downloaded and it stays on the "
                            f"account as it is"
                        ),
                    }
                )
            elif track in frozen:
                took[track] = dict(frozen[track])
            else:
                named.append(
                    {
                        "track": track,
                        "playlist": title,
                        "outcome": "not queued",
                        "why": (
                            "added on the account, but the provider did not list it on the "
                            "playlist, so there is no track to ask the download about"
                        ),
                    }
                )
        if took:
            queue[pid] = (title, took)
    return Planned(queue=queue, named=tuple(named))


def _owned(cfg: config.Config, reading: Any) -> Any:
    """Each ISRC to the library rows that carry it: the database's codes, and the mirror's.

    The mirror's matches carry a code read off a file the database holds none
    for, and the database carries a row in no mirrored playlist. Read once, on
    a read handle closed before the plan goes on.
    """
    from cratekit.acquire import match
    from cratekit.core import rb_writer
    from cratekit.write import playlist_pair

    found: dict[str, set[str]] = {}
    for content_id, (_remote, code, _reason) in reading.matcher.seen.items():
        token = match.isrc_token(code)
        if token:
            found.setdefault(token, set()).add(str(content_id))
    db = rb_writer.open_db(
        rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
    )
    try:
        for token, rows in playlist_pair.rows_by_isrc(db, match.isrc_token).items():
            found.setdefault(token, set()).update(rows)
    finally:
        rb_writer.close_db(db)

    def owned(code: Any) -> tuple[str, ...]:
        return tuple(sorted(found.get(match.isrc_token(code), ())))

    return owned


def _catalogue_listing(cfg: config.Config) -> Any:
    """One account playlist frozen as ``sync pair`` freezes it, the catalogue resolved once."""
    from cratekit.intake import cli as intake_cli
    from cratekit.label import catalogue

    found: list[Any] = []

    def listed(playlist_id: str) -> tuple[dict[str, dict[str, Any]], Any]:
        if not found:
            found.append(catalogue.resolve(cfg))
        return intake_cli.list_playlist_declared(found[0], playlist_id)

    return listed


def write(cfg: config.Config, approved: Planned) -> list[str]:
    """Queue each approved playlist's tracks, skipping any a mirror job holds now. The job ids."""
    from cratekit.core import jobs
    from cratekit.intake import cli as intake_cli

    already = queued(cfg)
    made: list[str] = []
    with jobs.open_store() as store:
        for pid, (_title, tracks) in sorted(approved.queue.items()):
            fresh = {track: frozen for track, frozen in tracks.items() if track not in already}
            if not fresh:
                continue
            job = intake_cli.queue_playlist(
                store,
                cfg,
                handler_key=HANDLER,
                reference=pid,
                tracks=fresh,
                source_id=SOURCE_ID,
            )
            made.append(job.job_id)
    return made


def add_step(cfg: config.Config, shared: Any) -> Step:
    """The rekordbox area's step: plan from the run's one reading, queue on approval (U204).

    A reading, a queue or a catalogue that cannot be read refuses this step alone.
    """
    try:
        reading = shared.reading()
    except CratekitError as exc:
        return refused(KIND, TITLE, exc.cause)
    if reading.unread:
        return Step(key=KIND, title=TITLE, state=LISTED, detail=reading.unread)
    try:
        planned = plan(cfg, reading)
    except CratekitError as exc:
        return refused(KIND, TITLE, exc.cause)
    writes = bool(planned.queue)
    detail = (
        f"queue {planned.tracks} track(s) from {len(planned.queue)} mirrored playlist(s) "
        f"for download; {len(planned.named)} named and not queued"
        if writes or planned.named
        else "no track added on the account is missing from the library"
    )
    step = Step(
        key=KIND,
        title=TITLE,
        state=PLANNED if writes else NOTHING,
        detail=detail,
        digest=digest_of(planned.identity()),
        counts={"queue": planned.tracks, "named": len(planned.named)},
        items=planned.items(),
    )
    if writes:

        def apply() -> dict[str, Any]:
            made = write(cfg, planned)
            return {"queued_jobs": made, "queued": planned.tracks}

        step.apply = apply
    return step


__all__ = [
    "HANDLER",
    "KIND",
    "SOURCE_ID",
    "TITLE",
    "Planned",
    "add_step",
    "landed",
    "plan",
    "queued",
    "write",
]
