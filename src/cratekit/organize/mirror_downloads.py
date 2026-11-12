"""A track added on the account to a mirrored playlist that the library lacks, queued (U204).

``crate organize``'s rekordbox area step ``mirror-downloads``. The account
mirror reads each mirrored playlist three ways and
:mod:`cratekit.modules.outbound.mirror_edits` decides what a person changed on
the account. A track added there that the library owns no row for, and that
no snapshot ever held, is held on the account with ``acquire`` set. This step
queues each one for download, AS ``sync pair`` QUEUES ONE: read row by row
through ``intake_cli.list_playlist_readable`` (R-1289), whose tracks are what
a playlist job is queued from, and queued with ``intake_cli.queue_playlist``
under the ``intake playlist`` job, one job per account playlist, carrying this
step's own source identifier.

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
track the job cannot be asked about; every other playlist is planned. A track
the account lists with no title or no artist is named the same way, and the
playlist's other tracks are planned (R-1289).

AND FILED WHERE THE ACCOUNT PUT IT, NOT WHERE ITS TAGS DID (U227). The
landing files the row it made by the row's own tags, in a commit after the
landing's, and the adoption ledger records each place it filed. :func:`filed`
hands the edit rule those places for each queued track, so its filing is read
as the landing's and not as a change a person made in rekordbox, and the
account's edit is carried onto the row once.

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


#: What a finished job's report says of a track that will never land, by its state.
_NEVER_LANDS = {
    "owned": (
        "its download found the library already holds it, so nothing lands; it stays "
        "on the account as it is"
    ),
    "missing": "its download could not be fetched, so nothing lands; it stays on the account as it is",
    "suppressed": "its download was suppressed, so nothing lands; it stays on the account as it is",
}


def outcomes(cfg: config.Config) -> dict[str, str]:
    """Each account track a FINISHED mirror job resolved to something that never lands, and why.

    Read from each succeeded job's reports, so a track the job found owned by a
    rule this step's own check cannot see (a code only in a file, an exact title
    under another code) is never said to await a landing that nothing will make.
    A job whose reports cannot be read says nothing here, and its tracks read as
    awaiting, as before.
    """
    from cratekit.core import jobs
    from cratekit.intake import missing_cli

    said: dict[str, str] = {}
    finished = [job for job in _jobs(cfg) if job.state == jobs.JobState.SUCCEEDED]
    if not finished:
        return said
    with jobs.open_store() as store:
        for job in finished:
            try:
                reports = missing_cli.job_reports(store, job)
            except CratekitError:
                continue
            for report in reports:
                why = _NEVER_LANDS.get(str(report.get("state")))
                if why:
                    said.setdefault(str(report.get("item_id")), why)
    return said


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


def _queued_at(cfg: config.Config) -> dict[str, str]:
    """Each account track a mirror job holds, to when the earliest such job was queued."""
    from cratekit.intake import cli as intake_cli
    from cratekit.modules.outbound import mirror_edits as edits

    held: dict[str, str] = {}
    for job in _jobs(cfg):
        made = edits.moment(job.created)
        if made is None:
            continue
        for remote in (job.payload or {}).get(intake_cli.TRACKS) or {}:
            was = edits.moment(held.get(str(remote), ""))
            if was is None or made < was:
                held[str(remote)] = job.created
    return held


def queued_from(cfg: config.Config) -> dict[str, frozenset[str]]:
    """Each account track a mirror job holds, to the remote playlists whose jobs queued it (U230).

    Read from the same jobs as :func:`_queued_at`. A queue that cannot be read
    gives none, and the edit rule reads every base as before U230.
    """
    from cratekit.intake import cli as intake_cli

    try:
        found = _jobs(cfg)
    except (CratekitError, OSError, ValueError):
        return {}
    held: dict[str, set[str]] = {}
    for job in found:
        payload = job.payload or {}
        source = str(payload.get(intake_cli.SOURCE) or "")
        if not source:
            continue
        for remote in payload.get(intake_cli.TRACKS) or {}:
            held.setdefault(str(remote), set()).add(source)
    return {remote: frozenset(sources) for remote, sources in held.items()}


def _adopted(cfg: config.Config) -> frozenset[str]:
    """Every approval a person gave ``crate adopt apply`` on this library, by its plan digest.

    The adoption applied ledger has two writers: the adopt worker, whose job
    freezes the approved plan's digest and refuses unless the plan it files
    still has it, and a landing's own filing (``intake.filing.file_landed``),
    which queues no job. So an entry under one of these digests was filed by a
    person, never by a landing (the review of U227, round two).
    """
    from cratekit.core import jobs
    from cratekit.organize import rekordbox  # noqa: PLC0415 - a cycle at import time

    with jobs.open_store() as store:
        return frozenset(
            str((job.payload or {}).get("digest") or "")
            for job in jobs.list_jobs(store)
            if job.handler_key == rekordbox.ADOPT_HANDLER
            and job.library_id == cfg.library.volume_id
        ) - {""}


def filed(
    cfg: config.Config, declared: Any, owner: Mapping[str, Any]
) -> dict[str, frozenset[tuple[str, str]]]:
    """Each queued account track to the band places its landing filed its row into (U227).

    ``owner`` is each account track to the library rows matched to it; a track
    owned by exactly one row is read. The places are the adoption ledger's
    entries for that row in the routing tree that the LANDING'S FILING wrote:
    the earliest entry applied no earlier than the track was queued, and every
    entry of the same approval (its digest). So a row the library held before
    the download is never read as one the landing made. An approval a person
    gave ``crate adopt apply`` is never the landing's, whatever its order:
    a re-filing after the landing is a later approval (round one), and a
    landing that filed nothing, a download with no genre tag above all, has
    no approval of its own for the person's first filing to be mistaken for
    (round two). Each is ``(folder, playlist)`` as the taxonomy names it now. A queue or a ledger that cannot be read gives
    none, and the edit is read by the later change rule as before U227, which
    leaves the library as it is.
    """
    from cratekit.adopt import apply as adoption
    from cratekit.modules.outbound import mirror_edits as edits
    from cratekit.write import routing_pass

    try:
        since = _queued_at(cfg)
        if not since:
            return {}
        applied = adoption.read(cfg).applied
        by_person = _adopted(cfg)
    except (CratekitError, OSError, ValueError):
        return {}
    tree = declared.tree.id
    by_row: dict[str, list[Any]] = {}
    for entry in applied:
        if entry.tree == tree and entry.digest not in by_person:
            by_row.setdefault(str(entry.content_id), []).append(entry)
    found: dict[str, frozenset[tuple[str, str]]] = {}
    for remote, queued_when in since.items():
        rows = {str(one) for one in owner.get(remote, ()) if str(one)}
        if len(rows) != 1:
            continue
        (content_id,) = rows
        after = edits.moment(queued_when)
        since_queued = [
            (at, entry)
            for entry in by_row.get(content_id, ())
            if (at := edits.moment(entry.applied)) is not None
            and after is not None
            and at >= after
        ]
        if not since_queued:
            continue
        first = min(since_queued, key=lambda pair: (pair[0], pair[1].entry_id))[1]
        places: set[tuple[str, str]] = set()
        for _at, entry in since_queued:
            if entry.digest != first.digest:
                continue
            try:
                places.add(routing_pass.destination(declared, entry.bucket, entry.sub))
            except (KeyError, CratekitError):
                continue
        if places:
            found[remote] = frozenset(places)
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
    cfg: config.Config,
    reading: Any,
    *,
    listed: Any = None,
    owned: Any = None,
    one_read: Any = None,
) -> Planned:
    """Every wanted track as it would be queued. Reads the queue, the provider and the library.

    ``listed`` reads one account playlist row by row, an
    ``intake_cli.Readable``, the catalogue's by default; a playlist it cannot
    list is named and the rest are planned, and a track it set aside is named
    and the playlist's others are planned (R-1289). ``owned`` answers each ISRC the
    library already holds with its rows, the database's and the mirror's
    matches by default, read through ``one_read``, ``--report``'s one read
    handle on the database (U267), when given. Raises the queue's refusal.
    """
    wanted: Sequence[Any] = reading.decided.wanted
    named: list[dict[str, Any]] = []
    if not wanted:
        return Planned()
    already = queued(cfg)
    ended = outcomes(cfg) if already else {}
    grouped: dict[str, tuple[str, list[str]]] = {}
    taken: set[str] = set()
    for decision in wanted:
        # ONE TRACK, ONE QUEUE: a track added to two playlists, or read by two
        # trees, is queued with the first, and lands once.
        if decision.track in taken:
            continue
        if decision.track in already:
            ended_why = ended.get(decision.track)
            named.append(
                {
                    **decision.item(),
                    "outcome": "not queued" if ended_why else "awaiting its landing",
                    "why": (
                        f"added on the account; a mirror download queued it and {ended_why}"
                        if ended_why
                        else f"{decision.why}; a mirror download already queued it, so it "
                        f"is not queued again"
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
        owned = _owned(cfg, reading, one_read)
    queue: dict[str, tuple[str, dict[str, dict[str, Any]]]] = {}
    for pid, (title, tracks) in sorted(grouped.items()):
        try:
            listing = listed(pid)
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
        frozen, unread = listing.tracks, listing.unread
        took: dict[str, dict[str, Any]] = {}
        for track in sorted(set(tracks)):
            rows = owned(frozen[track].get("isrc")) if track in frozen else ()
            if track in unread:
                # R-1289: the reader set this one track aside, and the playlist's
                # other tracks are planned as they always were.
                named.append(
                    {
                        "track": track,
                        "playlist": title,
                        "outcome": "not queued",
                        "why": (
                            f"added on the account, but {unread[track].why}, so the "
                            f"download has nothing to ask the provider about"
                        ),
                    }
                )
            elif rows:
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


def _owned(cfg: config.Config, reading: Any, one_read: Any = None) -> Any:
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
    db = (
        one_read.handle()
        if one_read is not None
        else rb_writer.open_db(
            rb_writer.live_db_path(cfg), require_closed=False, check_app_version=False, cfg=cfg
        )
    )
    try:
        for token, rows in playlist_pair.rows_by_isrc(db, match.isrc_token).items():
            found.setdefault(token, set()).update(rows)
    finally:
        rb_writer.done_reading(db, one_read)

    def owned(code: Any) -> tuple[str, ...]:
        return tuple(sorted(found.get(match.isrc_token(code), ())))

    return owned


def _catalogue_listing(cfg: config.Config) -> Any:
    """One account playlist read row by row as ``sync pair`` reads it, the catalogue resolved once.

    Through ``intake_cli.list_playlist_readable`` (R-1289), so one track the
    account lists with no title or no artist is set aside and named, never a
    refusal that names every track the playlist was asked for.
    """
    from cratekit.intake import cli as intake_cli
    from cratekit.label import catalogue

    found: list[Any] = []

    def listed(playlist_id: str) -> Any:
        if not found:
            found.append(catalogue.resolve(cfg))
        return intake_cli.list_playlist_readable(found[0], playlist_id)

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


def add_step(cfg: config.Config, shared: Any, *, one_read: Any = None) -> Step:
    """The rekordbox area's step: plan from the run's one reading, queue on approval (U204).

    A reading, a queue or a catalogue that cannot be read refuses this step alone.
    ``one_read`` is ``--report``'s one read handle on the database (U267).
    """
    try:
        reading = shared.reading()
    except CratekitError as exc:
        return refused(KIND, TITLE, exc.cause)
    if reading.unread:
        return Step(key=KIND, title=TITLE, state=LISTED, detail=reading.unread)
    try:
        planned = plan(cfg, reading, one_read=one_read)
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
    "filed",
    "queued_from",
    "landed",
    "outcomes",
    "plan",
    "queued",
    "write",
]
