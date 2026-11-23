"""Which downloaded tracks the account no longer lists, and which would leave the collection (U287).

When a track is taken off a downloaded playlist on the account, nothing else
notices: ``sync pair`` refuses INBOX playlists and the refill (U134) reads only
recorded reports. This module rereads every downloaded playlist, finds each
recorded track the account no longer lists, resolves its collection row, and
answers it OFFERED or KEPT, with why. The plan writes nothing; U288's gate binds
to its digest, and :func:`apply_removed` does rekordbox's Remove from Collection.

DOWNLOADED means a succeeded ``intake.playlist`` job a standing landing names
by account id and pass (U128); nothing else reached the collection. SYNCED is
wider: the sweep cursor, every queued intake job (the cursor in effect), the
taken record, every pair, every downloaded playlist, and the hearts.

A PARTIAL READ OFFERS NOTHING (R37): "on no other synced playlist" is a claim
about every one, so while any is unreadable, short, or empty with nothing
saying it holds none, every offer is kept. A playlist the listing omits and
whose id will not open is GONE (the listing has no total, R-385): it offers
nothing and holds what its finished jobs recorded, since a failed open may be
any failure; with nothing recorded it is not read whole.

TWO SHAPES ARE READ WHOLE (U320), or nothing could ever be offered. Hearts
short only by what the provider withholds (R-504) are WITHHELD, holding every
heart served; none served, or short by over a tenth or 49 hearts, stays short.
An unlisted playlist whose id answers NOT FOUND, and nothing else, is a
sighting in :mod:`cratekit.sync.unavailable`; a sighting a day later, or the
gate ``sync.removed.retire``, RETIRES it, holding and stopping nothing until it
opens or is listed again. Any other failure reads as before, its retirement kept.

A TRACK IS REMOVED when its listing holds neither its provider id, its ISRC,
nor its folded artist and title; the same tests say another playlist holds it.
Each can only say "still there", so all err toward keeping.

EACH ROW GETS ONE ANSWER, the first that holds:

* ``left``: no row, two rows claim its file, a person's question is open
  (U121, U144), or the report carried no file;
* ``kept, held before the pass``: the library owned it when the job ran;
* ``kept, not this pass's file``: not under its pass's ``filed_batch`` folder;
* ``kept, on another synced playlist``;
* ``kept, in a playlist of yours``: a live membership outside the intake and
  routing trees and its recorded twin. A label year playlist keeps the row,
  since those are not yet told from a person's (a residual);
* ``kept, named by a table rekordbox's removal was never measured on``: the
  removal would refuse it (U288);
* ``offered``.

A row reached from two playlists or passes is one answer, offered when ANY
report says its pass brought the file.

Layer: modules. It opens no database; the verb hands it a read only copy.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cratekit.acquire import match
from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    jobs,
    locations,
    rb_writer,
    session,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import CratekitError, refuse
from cratekit.intake import account_playlists, ingest, native, refill, set_playlist
from cratekit.intake import cli as intake_cli
from cratekit.sync import playlists, twins, unavailable
from cratekit.sync.watermarks import WatermarkStore
from cratekit.write import trees

if TYPE_CHECKING:
    from cratekit.label import catalogue
    from cratekit.sync.removed_kept import SyncedReads

#: The three answers a row can get.
OFFERED = "offered"
KEPT = "kept"
LEFT = "left"

#: Why a removed track's row is kept, as the screen says it.
HELD_BEFORE = "held before the pass"
NOT_THIS_PASS = "not this pass's file"
ON_ANOTHER = "on another synced playlist"
IN_YOURS = "in a playlist of yours"
PARTIAL_READ = "not offered while a synced playlist could not be read whole"
#: U288. The removal would refuse such a row (a vox or dyn My Tag above all).
UNMEASURED = "named by a table rekordbox's removal was never measured on"

#: Why a removed track has no row to answer, beside the resolver's own reasons.
NOT_CARRIED = "the pass never downloaded it"
OWNED_NO_ROW = "held before the pass, and no collection row holds its file now"

#: How each synced playlist read; the last three are a read that is not whole.
READ = "read"
GONE = "gone"
UNREADABLE = "unreadable"
SHORT = "short"
EMPTY = "empty"
NOT_WHOLE = frozenset({UNREADABLE, SHORT, EMPTY})
#: Hearts short only by what the provider withholds, read whole (U320).
WITHHELD = "withheld"
#: Retired by the not found record: holds nothing, stops nothing (U320).
RETIRED = "retired"
#: The reader refused rows a playlist served; its id opened, so it is not gone.
SERVED_UNREADABLE = "intake-list-unusable"

#: The share of the declared count hearts may be short by and read whole (U320),
#: measured at 12 of 197 and 9 of 349.
WITHHELD_AT_MOST = 0.10

#: And the most hearts at any count: under half a hearts page of a hundred, so a
#: dropped window stays short.
WITHHELD_AT_MOST_HEARTS = 49

#: Every state a listing holds tracks in.
HOLDING = frozenset({READ, GONE, WITHHELD})

_STANDING = frozenset(
    {
        session.SessionState.AWAITING_IMPORT,
        session.SessionState.COMMITTED_UNVERIFIED,
        session.SessionState.CLOSED,
    }
)


@dataclass(frozen=True, slots=True)
class Downloaded:
    """One account playlist a pass downloaded and landed, every report in the account's order."""

    account: str
    name: str
    pass_name: str
    job_id: str
    rows: tuple[account_playlists.Row, ...] = ()


@dataclass(frozen=True, slots=True)
class Listing:
    """One synced playlist as the account lists it now, or why it could not say."""

    account: str
    name: str
    state: str
    why: str = ""
    #: Every provider id the listing holds, a refused row's included.
    refs: frozenset[str] = frozenset()
    isrcs: frozenset[str] = frozenset()
    #: Every read row's artist and title, folded as a recording, version excluded.
    recordings: frozenset[str] = frozenset()
    #: The not found record's entry after this read (U320), or ``None``; never digested.
    noted: unavailable.Sighting | None = None
    #: Whether the account no longer lists it and its id answered not found on this read.
    not_found: bool = False

    def holds(self, wanted: match.Wanted) -> bool:
        """Whether this listing still holds the track, by any of the three tests.

        Only READ, GONE (its recorded contents) and WITHHELD hold anything; a
        not whole read stops every offer instead, and RETIRED stops nothing.
        """
        if self.state not in HOLDING:
            return False
        if wanted.ref and wanted.ref in self.refs:
            return True
        if wanted.isrc and wanted.isrc.strip().upper() in self.isrcs:
            return True
        return recording(wanted) in self.recordings

    def identity(self) -> dict[str, Any]:
        return {"account": self.account, "name": self.name, "state": self.state, "why": self.why}


@dataclass(frozen=True, slots=True)
class Answer:
    """One collection row a removal reached, or one removed track with no row, and its answer."""

    answer: str
    why: str
    artist: str
    title: str
    content_id: str = ""
    file: str = ""
    #: The account playlists the track was taken off, by name, each once.
    removed_from: tuple[str, ...] = ()
    #: What keeps it: the other synced playlists, or the rekordbox playlists.
    kept_by: tuple[str, ...] = ()

    def identity(self) -> dict[str, Any]:
        return {
            "answer": self.answer,
            "why": self.why,
            "artist": self.artist,
            "title": self.title,
            "content_id": self.content_id,
            "file": self.file,
            "removed_from": list(self.removed_from),
            "kept_by": list(self.kept_by),
        }


@dataclass(frozen=True, slots=True)
class RemovedPlan:
    """What ``sync removed`` found, every playlist and every row named, digested."""

    listings: tuple[Listing, ...] = ()
    answers: tuple[Answer, ...] = ()
    #: A synced playlist was not read whole, so nothing is offered.
    partial: bool = False
    #: Session records that could not be read; a record names what the pass made.
    unreadable: int = 0
    #: The memberships removing the offered rows would renumber (R-1830).
    renumbered: int = 0
    digest: str = ""

    @property
    def offered(self) -> tuple[Answer, ...]:
        return tuple(one for one in self.answers if one.answer == OFFERED)

    def count(self, answer: str) -> int:
        return sum(1 for one in self.answers if one.answer == answer)


def identity(plan: RemovedPlan) -> dict[str, Any]:
    """What the digest covers: every playlist read, every answer, the partial flag and the renumbering."""
    return {
        "kind": "sync-removed",
        "playlists": [one.identity() for one in plan.listings],
        "answers": [one.identity() for one in plan.answers],
        "partial": plan.partial,
        "unreadable": plan.unreadable,
        "renumbered": plan.renumbered,
    }


def recording(wanted: match.Wanted) -> str:
    """The track's artist and title folded as a recording, version excluded."""
    return match.recording_identity(wanted.artist, wanted.title)


def _standing(records: Iterable[session.SessionRecord]) -> list[session.SessionRecord]:
    return [
        one
        for one in records
        if one.workflow == ingest.INTAKE_WORKFLOW and one.state in _STANDING
    ]


def downloaded(cfg: config.Config, records: Sequence[session.SessionRecord]) -> tuple[Downloaded, ...]:
    """Every account playlist a pass downloaded and a standing landing of that pass names.

    THE LANDING RECORD DECIDES, never the job alone, since an unlanded pass put
    nothing in the collection. Only an entry with the account id counts (U128).
    """
    entries = [one for one in refill.recorded_entries(records) if one.account and one.pass_name]
    found: list[Downloaded] = []
    named: list[tuple[jobs.Job, str, str]] = []
    for pass_name in dict.fromkeys(one.pass_name for one in entries):
        for job, name in account_playlists.playlist_jobs(cfg, pass_name):
            account = account_playlists.account_of(job)
            if account and any(
                refill.ours(one, pass_name=pass_name, account=account, name=name)
                for one in entries
            ):
                named.append((job, name, pass_name))
    if not named:
        return ()
    with jobs.open_store() as store:
        for job, name, pass_name in named:
            source = account_playlists.read_source(store, job, name)
            found.append(
                Downloaded(
                    account=source.playlist_id,
                    name=name,
                    pass_name=pass_name,
                    job_id=job.job_id,
                    rows=source.rows,
                )
            )
    return tuple(found)


def synced(
    cfg: config.Config,
    found: Sequence[Downloaded],
    *,
    paired: Iterable[str] = (),
    swept_now: Iterable[str] = (),
    listed: Mapping[str, catalogue.AccountPlaylist] | None = None,
) -> tuple[str, ...]:
    """Every synced account playlist, the downloaded ones first, each once.

    ``swept_now`` is :func:`job_playlists`; ``listed`` adds any still titled with
    the old swept prefix, taken until ``sync strip`` records it (U242).

    THE TAKEN RECORD REFUSES WHEN UNREAD, or "on no other synced playlist"
    would be claimed over playlists nobody can name.
    """
    existing = WatermarkStore(cfg).read(playlists.SOURCE_ID)
    swept = tuple(existing.swept) if existing is not None else ()
    taken = tuple(sorted(playlists.taken_ids(cfg)))
    return tuple(
        dict.fromkeys(
            [
                *(one.account for one in found),
                *swept,
                *swept_now,
                *sorted(
                    key
                    for key, one in (listed or {}).items()
                    if playlists.is_swept_name(one.name)
                ),
                *taken,
                *sorted(str(one) for one in paired),
            ]
        )
    )


def _held(tracks: Iterable[match.Wanted]) -> dict[str, frozenset[str]]:
    """The three identity sets a listing is asked by, over ``tracks``."""
    wanted = list(tracks)
    return {
        "refs": frozenset(one.ref for one in wanted if one.ref),
        "isrcs": frozenset(one.isrc.strip().upper() for one in wanted if one.isrc),
        "recordings": frozenset(recording(one) for one in wanted),
    }


#: An account id to what its finished jobs recorded, or None; asked of a GONE playlist.
Recorded = Callable[[str], "tuple[match.Wanted, ...] | None"]


def recorded_contents(cfg: config.Config) -> Recorded:
    """What one account playlist's succeeded intake jobs recorded, hearts aside.

    ASKED PER PLAYLIST AND ONLY WHEN ONE READS GONE, so a damaged job of another
    playlist never refuses the verb; an unreadable one of this playlist answers None.
    """
    from cratekit.intake import missing_cli

    def contents(account: str) -> tuple[match.Wanted, ...] | None:
        found: list[match.Wanted] = []
        try:
            with jobs.open_store() as store:
                for job in playlists.playlist_jobs(
                    store, cfg, handler_key=account_playlists.PLAYLIST_KEY
                ):
                    if (
                        playlists.playlist_of(job) != account
                        or job.state is not jobs.JobState.SUCCEEDED
                        or str((job.payload or {}).get("source_id") or "")
                        == intake_cli.FAVORITES_SOURCE_ID
                    ):
                        continue
                    found.extend(
                        intake_cli.thawed(report["track"])
                        for report in missing_cli.job_reports(store, job)
                        if isinstance(report.get("track"), Mapping)
                    )
        except CratekitError:
            return None
        return tuple(found) or None

    return contents


def job_playlists(cfg: config.Config) -> tuple[str, ...]:
    """Every account playlist an ``intake.playlist`` job of this library was queued for, any state.

    THE CURSOR AS IT IS IN EFFECT: a finished job joins the file only at the
    next sweep, and an open one holds its playlist back, so both count now.
    """
    with jobs.open_store() as store:
        return tuple(
            dict.fromkeys(
                account
                for job in playlists.playlist_jobs(store, cfg, handler_key=account_playlists.PLAYLIST_KEY)
                if (account := playlists.playlist_of(job))
                and str((job.payload or {}).get("source_id") or "") != intake_cli.FAVORITES_SOURCE_ID
            )
        )


def _retired(account: str, name: str, noted: unavailable.Sighting, *, not_found: bool) -> Listing:
    """A playlist the record retired: named with its id and the dates, holding nothing."""
    who = " by a person" if noted.by == unavailable.BY_PERSON else ""
    return Listing(
        account=account,
        name=name or noted.name,
        state=RETIRED,
        why=(
            f"retired{who} on {unavailable.day(noted.retired)}: the account no longer "
            f"lists it and its id answered not found on {noted.seen()}, so it holds "
            f"nothing and stops nothing"
        ),
        noted=noted,
        not_found=not_found,
    )


def read_one(
    found: catalogue.Catalogue,
    account: str,
    listed: Mapping[str, catalogue.AccountPlaylist],
    recorded: Recorded | None = None,
    *,
    sightings: Mapping[str, unavailable.Sighting] | None = None,
    moment: datetime | None = None,
    names: Mapping[str, str] | None = None,
) -> Listing:
    """One synced playlist read through the sweep's own reader, or why it is not read whole.

    ``sightings`` is the not found record before this run, ``moment`` when it
    asked, ``names`` names for unlisted playlists (U320). ``noted`` carries the
    record's entry after this read: a not found while unlisted is a sighting,
    other failures leave it, and opening or being listed clears it.
    """
    shown = listed.get(account)
    prior = (sightings or {}).get(account)
    name = (
        shown.name
        if shown is not None
        else (names or {}).get(account) or (prior.name if prior is not None else "")
    )
    try:
        readable = intake_cli.list_playlist_readable(found, account)
    except CratekitError as exc:
        if exc.cause.reason not in playlists.PER_PLAYLIST_REASONS:
            raise
        if shown is None and exc.cause.reason != SERVED_UNREADABLE:
            # GONE ONLY WHEN TWO READS AGREE, and even then not read as empty
            # (R-385). ONLY A NOT FOUND IS A SIGHTING (U320, R-1713), so an
            # outage never retires. AND ONLY THIS READ'S NOT FOUND READS IT
            # RETIRED: another failure keeps the retirement but reads not whole.
            said_none = unavailable.answered_unavailable(exc)
            noted = (
                unavailable.sighted(prior, account, name, moment or unavailable.now())
                if said_none
                else prior
            )
            if said_none and noted is not None and noted.is_retired:
                return _retired(account, name, noted, not_found=said_none)
            seen = (
                ""
                if noted is None
                else (
                    f"; retired on {unavailable.day(noted.retired)}, and read as before "
                    f"its retirement while its id fails another way"
                )
                if noted.is_retired
                else f"; its id answered not found, first on {unavailable.day(noted.first)}"
            )
            known = recorded(account) if recorded is not None else None
            if not known:
                return Listing(
                    account=account,
                    name=name,
                    state=UNREADABLE,
                    why=(
                        "the account no longer lists it, its id does not open, and no "
                        "finished job readable now records what it held" + seen
                    ),
                    noted=noted,
                    not_found=said_none,
                )
            return Listing(
                account=account,
                name=name,
                state=GONE,
                why=(
                    "the account no longer lists it and its id does not open; read as "
                    "still holding what its finished jobs recorded" + seen
                ),
                noted=noted,
                not_found=said_none,
                **_held(known),
            )
        # LISTED, or OPENED with its rows refused, so not gone: the record holds nothing.
        return Listing(account=account, name=name, state=UNREADABLE, why=exc.cause.message)
    if readable.short is not None:
        block = readable.short.block()
        return Listing(
            account=account,
            name=name,
            state=SHORT,
            why=f"listed {block.get('listed')} of the {block.get('declared')} tracks it declares",
        )
    if not readable.order and (shown is None or shown.tracks != 0):
        # AN EMPTY READ IS TRUSTED ONLY WHEN THE ACCOUNT'S LISTING SAYS NONE, or
        # a provider fault would read every track removed.
        return Listing(
            account=account,
            name=name,
            state=EMPTY,
            why="read with no tracks and nothing says it holds none",
        )
    # A ROW THE READER SET ASIDE (U213) STILL COUNTS by id, ISRC and full name.
    wanted = [intake_cli.thawed(one) for one in readable.tracks.values()]
    wanted.extend(
        match.Wanted(artist=one.artist, title=one.title, isrc=one.isrc or None, ref=one.ref)
        for one in readable.unread.values()
    )
    held = _held(wanted)
    return Listing(
        account=account,
        name=name,
        state=READ,
        refs=frozenset(str(one) for one in readable.order),
        isrcs=held["isrcs"],
        recordings=frozenset(
            recording(one) for one in wanted if one.artist.strip() and one.title.strip()
        ),
    )


def account_listing(found: catalogue.Catalogue) -> dict[str, catalogue.AccountPlaylist]:
    """The account's own playlists by identifier; AN UNREAD LIST REFUSES rather than read all as gone."""
    return {one.playlist_id: one for one in playlists.account_listing(found)}


#: The account's hearts, read as one more synced listing.
HEARTS = "hearts"
HEARTS_NAME = "the account's hearts"


def read_hearts(found: catalogue.Catalogue) -> Listing:
    """The account's hearts as one more synced listing, through the favourites source's reader.

    A HEART KEEPS A TRACK, since a new heart is in no rekordbox playlist until
    ``sync favorites``. It is read whole or not, by a playlist's rules.
    """
    try:
        frozen, short = intake_cli.list_favorites(found)
    except CratekitError as exc:
        if exc.cause.reason not in playlists.PER_PLAYLIST_REASONS:
            raise
        return Listing(account=HEARTS, name=HEARTS_NAME, state=UNREADABLE, why=exc.cause.message)
    # NO HEART SERVED NEEDS NO TEST OF ITS OWN: the bound already refuses it.
    if short is not None and not (
        0 < short.withheld <= min(short.declared * WITHHELD_AT_MOST, WITHHELD_AT_MOST_HEARTS)
    ):
        # SHORT BY MORE THAN THE PROVIDER WITHHOLDS, or by nothing, which a
        # dropped window or a provider serving nothing looks like.
        return Listing(
            account=HEARTS,
            name=HEARTS_NAME,
            state=SHORT,
            why=(
                f"listed fewer hearts than the account declares ({short.summary()}), "
                f"and not only by hearts the provider withholds"
            ),
        )
    if not frozen:
        return Listing(
            account=HEARTS,
            name=HEARTS_NAME,
            state=EMPTY,
            why="read with no hearts and nothing says it holds none",
        )
    wanted = [intake_cli.thawed(one) for one in frozen.values()]
    return Listing(
        account=HEARTS,
        name=HEARTS_NAME,
        # SHORT ONLY BY WHAT THE PROVIDER WITHHOLDS (U320, R-504): a heart it
        # will not serve is not shown either, so this reads whole.
        state=READ if short is None else WITHHELD,
        why=(
            ""
            if short is None
            else (
                f"{short.summary()}; read whole, since a heart the provider will not "
                f"serve is not one the account shows"
            )
        ),
        refs=frozenset(str(one) for one in frozen),
        isrcs=frozenset(one.isrc.strip().upper() for one in wanted if one.isrc),
        recordings=frozenset(recording(one) for one in wanted),
    )


def read_account(
    found: catalogue.Catalogue,
    wanted: Sequence[str],
    *,
    listed: Mapping[str, catalogue.AccountPlaylist],
    recorded: Recorded | None = None,
    sightings: Mapping[str, unavailable.Sighting] | None = None,
    moment: datetime | None = None,
    names: Mapping[str, str] | None = None,
    kept: SyncedReads | None = None,
) -> dict[str, Listing]:
    """Each playlist in ``wanted`` read once, against the account's listing read once.

    ``kept`` (R-1716) answers a playlist the account lists unchanged since a
    run read it whole, and keeps each read made now AS IT GOES, so a run the
    call ceiling stops part way keeps what it read.
    """
    reads: dict[str, Listing] = {}
    for account in dict.fromkeys(wanted):
        shown = listed.get(account)
        held = kept.get(account, shown) if kept is not None else None
        if held is not None:
            reads[account] = held
            continue
        reads[account] = read_one(
            found, account, listed, recorded, sightings=sightings, moment=moment, names=names
        )
        if kept is not None:
            kept.keep(account, shown, reads[account])
    return reads


def noted(reads: Mapping[str, Listing]) -> dict[str, unavailable.Sighting | None]:
    """The not found record's entries after these reads, by playlist, ``None`` dropping one (U320)."""
    return {account: one.noted for account, one in reads.items() if account != HEARTS}


def removals(
    found: Sequence[Downloaded], reads: Mapping[str, Listing]
) -> tuple[tuple[Downloaded, account_playlists.Row], ...]:
    """Every recorded report whose playlist was read and no longer holds it, in the account's order."""
    return tuple(
        (one, row)
        for one in found
        if one.account in reads and reads[one.account].state == READ
        for row in one.rows
        if not reads[one.account].holds(row.wanted)
    )


def _filed_folders(records: Iterable[session.SessionRecord]) -> dict[str, tuple[str, ...]]:
    """The batch folders each pass's standing landings recorded filing into, by pass."""
    folders: dict[str, list[str]] = {}
    for record in _standing(records):
        pass_name = str(record.detail.get(native.PASS_KEY) or "")
        filed = record.detail.get(native.FILED_BATCH_KEY)
        if pass_name and isinstance(filed, Mapping) and filed.get("folder"):
            folders.setdefault(pass_name, []).append(str(filed["folder"]))
    return {key: tuple(dict.fromkeys(value)) for key, value in folders.items()}


def _under(path: str, folders: Iterable[str]) -> bool:
    """Whether ``path`` sits under one of ``folders``, compared in one Unicode form."""
    held = locations.norm_for_compare(str(path))
    for folder in folders:
        root = locations.norm_for_compare(str(folder)).rstrip("/\\")
        if root and (held.startswith(root + "/") or held.startswith(root + "\\")):
            return True
    return False


def _twins(records: Iterable[session.SessionRecord]) -> dict[str, frozenset[str]]:
    """The custom playlist twins standing landings recorded, by the account playlist they copy."""
    found: dict[str, set[str]] = {}
    for record in _standing(records):
        entries = record.detail.get(twins.RECORD_KEY)
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if (
                isinstance(entry, Mapping)
                and entry.get("id")
                and entry.get(ingest.INBOX_ACCOUNT_KEY)
            ):
                found.setdefault(str(entry[ingest.INBOX_ACCOUNT_KEY]), set()).add(str(entry["id"]))
    return {key: frozenset(value) for key, value in found.items()}


def _routing_nodes(db: Any, declared: taxonomy.Taxonomy, registry: tree_registry.Registry) -> frozenset[str]:
    """Every live node of the routing tree, when the registry holds it database native.

    A BRIDGE TREE OR AN UNANCHORED ROOT NAMES NOTHING, so its memberships keep
    the row, the side that removes less.
    """
    tree_id = declared.tree.id
    if not registry.is_database_native(tree_id):
        return frozenset()
    try:
        root = tree_registry.anchored_root(
            tree_id, registry, root_exists=lambda root_id: db.get_playlist(ID=root_id) is not None
        )
    except CratekitError:
        return frozenset()
    return frozenset({str(root), *(str(row.ID) for row in native.inbox_nodes(db, str(root)))})


def memberships(db: Any, content_ids: Iterable[str]) -> dict[str, tuple[tuple[str, str], ...]]:
    """Each row's live memberships in live playlists, as (playlist id, name), from SQL."""
    from sqlalchemy import bindparam, text

    wanted = sorted({str(one) for one in content_ids})
    if not wanted:
        return {}
    statement = text(
        f"SELECT sp.ContentID, sp.PlaylistID, p.Name FROM {rb_writer.MEMBERSHIP_TABLE} sp "
        f"JOIN {rb_writer.PLAYLIST_TABLE} p ON p.ID = sp.PlaylistID "
        f"WHERE COALESCE(sp.{rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 "
        f"AND COALESCE(p.{rb_writer.SOFT_DELETE_COLUMN}, 0) = 0 "
        f"AND sp.ContentID IN :ids ORDER BY sp.ContentID, p.ID"
    ).bindparams(bindparam("ids", expanding=True))
    held: dict[str, list[tuple[str, str]]] = {}
    for content_id, playlist_id, name in db.session.execute(statement, {"ids": wanted}).fetchall():
        held.setdefault(str(content_id), []).append((str(playlist_id), str(name or "")))
    return {key: tuple(value) for key, value in held.items()}


@dataclass
class _Reached:
    """Everything the removals said about one collection row, gathered before it is answered."""

    content_id: str
    file: str
    artist: str
    title: str
    passes: list[str] = field(default_factory=list)
    accounts: list[str] = field(default_factory=list)
    removed_from: list[str] = field(default_factory=list)
    wanted: list[match.Wanted] = field(default_factory=list)
    brought: bool = False
    carried: bool = False


def plan_removed(
    cfg: config.Config,
    db: Any,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
    records: Sequence[session.SessionRecord],
    found: Sequence[Downloaded],
    reads: Mapping[str, Listing],
    unreadable: int = 0,
) -> RemovedPlan:
    """Answer every removed track against the library as it is now. Reads, writes nothing."""
    listings = tuple(reads.values())
    partial = any(one.state in NOT_WHOLE for one in listings)
    removed = removals(found, reads)
    answers: list[Answer] = []
    reached: dict[str, _Reached] = {}
    if removed:
        intake_root = refill.anchored_root(db, declared.intake.id, registry)
        own_nodes = frozenset(
            {str(intake_root), *(str(row.ID) for row in native.inbox_nodes(db, str(intake_root)))}
        ) | _routing_nodes(db, declared, registry)
        folders = _filed_folders(records)
        collection = set_playlist.collection_rows(cfg, db)
        matches = set_playlist.library_matches(cfg, db)
        for one, row in removed:
            wanted = row.wanted
            if row.state == account_playlists.OWNED:
                content_id, path, why = collection(row.paths)
            elif row.carried:
                content_id, path, why = matches(wanted)
            else:
                content_id, path, why = "", "", row.state or NOT_CARRIED
            if not content_id:
                answers.append(
                    Answer(
                        answer=LEFT,
                        why=(OWNED_NO_ROW if row.state == account_playlists.OWNED else why),
                        artist=wanted.artist,
                        title=wanted.listed,
                        removed_from=(one.name,),
                    )
                )
                continue
            held = reached.setdefault(
                content_id,
                _Reached(content_id=content_id, file=path, artist=wanted.artist, title=wanted.listed),
            )
            held.passes.append(one.pass_name)
            held.accounts.append(one.account)
            held.removed_from.append(one.name)
            held.wanted.append(wanted)
            if row.carried:
                held.carried = True
                if _under(path, folders.get(one.pass_name, ())):
                    held.brought = True
        made = _twins(records)
        members = memberships(db, reached)
        unmeasured = rb_writer.CollectionRemoval.held(db, reached)
        for held in reached.values():
            own = own_nodes.union(
                *(made.get(account, frozenset()) for account in held.accounts),
            )
            answers.append(
                _answer(
                    held,
                    reads=listings,
                    held_by=members.get(held.content_id, ()),
                    own=own,
                    partial=partial,
                    names={one.account: one.name for one in found},
                    unmeasured=unmeasured.get(held.content_id, {}),
                )
            )
    offered = [one.content_id for one in answers if one.answer == OFFERED]
    plan = RemovedPlan(
        listings=listings,
        answers=tuple(answers),
        partial=partial,
        unreadable=unreadable,
        renumbered=len(rb_writer.CollectionRemoval.renumbering(db, offered)) if offered else 0,
    )
    return replace(plan, digest=digest_of(identity(plan)))


def _answer(
    held: _Reached,
    *,
    reads: Sequence[Listing],
    held_by: Sequence[tuple[str, str]],
    own: frozenset[str],
    partial: bool,
    names: Mapping[str, str] | None = None,
    unmeasured: Mapping[str, int] | None = None,
) -> Answer:
    """The one answer a reached row gets, the first of the kept reasons that holds."""
    shown = Answer(
        answer=KEPT,
        why="",
        artist=held.artist,
        title=held.title,
        content_id=held.content_id,
        file=held.file,
        removed_from=tuple(dict.fromkeys(held.removed_from)),
    )
    if not held.carried:
        return replace(shown, why=HELD_BEFORE)
    if not held.brought:
        return replace(shown, why=NOT_THIS_PASS)
    still = tuple(
        dict.fromkeys(
            one.name or (names or {}).get(one.account) or one.account
            for one in reads
            if any(one.holds(wanted) for wanted in held.wanted)
        )
    )
    if still:
        return replace(shown, why=ON_ANOTHER, kept_by=still)
    yours = tuple(dict.fromkeys(name or playlist_id for playlist_id, name in held_by if playlist_id not in own))
    if yours:
        return replace(shown, why=IN_YOURS, kept_by=yours)
    if unmeasured:
        return replace(shown, why=UNMEASURED, kept_by=tuple(sorted(unmeasured)))
    if partial:
        return replace(shown, why=PARTIAL_READ)
    return replace(shown, answer=OFFERED)


# ---------------------------------------------------------------------------
# The removal, behind the gate (U288)
# ---------------------------------------------------------------------------

#: The workflow a removal's session record names.
WORKFLOW = "sync-removed"

#: Where the change summary says rows left, since a content row is in no tree.
COLLECTION = "collection"

_ORIGIN = ("sync.removed",)


@dataclass(frozen=True, slots=True)
class Removed:
    """What one apply took out of the collection, read back."""

    session_id: str
    rows: tuple[Answer, ...]
    #: Rows deleted, by table, the content rows included.
    deleted: Mapping[str, int]
    #: The update count the commit left, which the record carries.
    sequence: int | None
    #: The playlist memberships renumbered behind the removed rows (R-1830).
    renumbered: int = 0


def _rollback_quietly(db: Any) -> None:
    try:
        db.session.rollback()
    except Exception:  # noqa: BLE001 - a failed cleanup must not hide its cause
        pass


def apply_removed(
    cfg: config.Config,
    db: Any,
    plan: RemovedPlan,
    *,
    declared: taxonomy.Taxonomy,
    registry: tree_registry.Registry,
    records: Sequence[session.SessionRecord],
    found: Sequence[Downloaded],
    reads: Mapping[str, Listing],
    unreadable: int,
    analysis_roots: Iterable[Path | str],
) -> Removed:
    """Take every offered row out of the collection in one guarded commit, and read it back.

    THE PLAN IS TAKEN AGAIN ON THIS HANDLE FIRST, since the approved one was
    read on a copy; a moved digest refuses with nothing written.

    WHAT IS WRITTEN IS REKORDBOX'S OWN REMOVE FROM COLLECTION (A178, A185): each
    offered row and its rows in the six tables beside it, deleted outright, and
    later playlist members renumbered by ``TrackNo`` alone (A197, R-1830); history
    keeps its numbers, being unmeasured. A row any other table names refuses the
    apply. Never a file or a beat grid; orphan artist and album rows are left
    for rekordbox's next removal.

    THE SESSION SPINE IS CALLED, NOT REBUILT, then the whole database is read
    back from SQL against the reading before the first delete. The record
    names every row removed, so ``restore list`` names them and ``crate delete
    review`` offers their files (R-1037).
    """
    watched = [Path(root) for root in analysis_roots]
    if not watched:
        raise ValueError(
            "analysis_roots is empty, so the analysis-file watch would watch nothing "
            "and this session would report itself clean whatever happened to the "
            "library's grids; name the roots this write could touch"
        )
    again = plan_removed(
        cfg,
        db,
        declared=declared,
        registry=registry,
        records=records,
        found=found,
        reads=reads,
        unreadable=unreadable,
    )
    if again.digest != plan.digest:
        raise refuse(
            "decision-stale",
            "the collection, the playlists or the session records are not as the "
            "approved plan read them, so nothing was written; run it again and approve "
            "what it shows now",
            origin=_ORIGIN,
            detail={"approved": plan.digest, "now": again.digest},
        )
    offered = plan.offered
    if not offered:
        return Removed(session_id="", rows=(), deleted={}, sequence=None)
    convergence.assert_tree_writable(cfg, db, declared.intake.id, registry)
    about = {
        one.content_id: {
            "artist": one.artist,
            "title": one.title,
            "file": one.file,
            "removed_from": list(one.removed_from),
        }
        for one in offered
    }
    with (
        session.assert_gates(
            cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
        ) as gates,
        rb_writer.commit_witness(db) as witness,
    ):
        record, capture = trees.attached_capture(gates, cfg, db)
        removal = rb_writer.CollectionRemoval.prepare(db, [one.content_id for one in offered])
        first = _first_deletion_position(cfg, db)
        try:
            removal.commit()
        except BaseException:
            _rollback_quietly(db)
            if witness.landed:
                _record_removal_commit(record, removal, about, _counter(db), cfg)
                _give_first_position(first)
            raise
        sequence = _counter(db)
        _record_removal_commit(record, removal, about, sequence, cfg)
        _give_first_position(first)
        convergence.record_fingerprint(cfg, db)
        violations = removal.read_back()
        if violations:
            raise refuse(
                "session-committed-unverified",
                "the removal committed, and the database read back from SQL is not what "
                "it planned, so this answer cannot be vouched for:\n  - "
                + "\n  - ".join(violations[:20]),
                origin=_ORIGIN,
                detail={"violations": violations, "session_id": record.session_id},
            )
        session_id = record.session_id
    return Removed(
        session_id=session_id,
        rows=offered,
        deleted=dict(removal.deleted),
        sequence=sequence,
        renumbered=len(removal.renumbered),
    )


def _first_deletion_position(cfg: config.Config, db: Any) -> Callable[[], None] | None:
    """The deletion pass's first position, read before the removal, to give once it lands.

    A FIRST ``delete review`` BASELINES every removal it sees as history (R35),
    so without a position this removal's file would never be offered. The
    position is read before the commit by the pass's own rule and written only
    once it lands, so a refused removal changes nothing. A held position is
    kept. None when there is nothing to give. Whether deletion is switched on
    is never asked, so turning it on later still offers these files.
    """
    try:
        from cratekit.deletion import library as deletion_library
        from cratekit.deletion import watermark
    except ImportError:  # pragma: no cover - the deletion package is not installed
        return None
    store = watermark.WatermarkStore(cfg)
    identity = deletion_library.database_identity(db)
    held = store.read()
    if held is not None and held.applies_to(identity):
        return None
    seen = deletion_library.read_collection(db.get_content())
    counter = deletion_library.current_sequence(db)
    start = max([counter, *(row.sequence for row in seen.removed)])

    def give() -> None:
        store.baseline(database_identity=identity, sequence=start, actor=WORKFLOW)

    return give


def _give_first_position(first: Callable[[], None] | None) -> None:
    if first is not None:
        first()


def _counter(db: Any) -> int | None:
    try:
        return int(db.get_local_usn())
    except Exception:  # noqa: BLE001 - an unread counter is recorded as unknown
        return None


def _record_removal_commit(
    record: session.SessionRecord,
    removal: Any,
    about: Mapping[str, Mapping[str, Any]],
    sequence: int | None,
    cfg: config.Config,
) -> None:
    """Record the commit, every row named, under the collection, the way a restore reads one.

    Its name is the one the write session guard reads. An unread sequence is
    recorded as unknown, and the deletion pass then offers none of these files.
    """
    removal.write_into(record.detail, sequence=sequence, about=about)
    changes = (session.TreeChange(tree=COLLECTION, removed=len(removal.content_ids)),)
    session.record_commit(record, COLLECTION, session.ChangeSummary(changes), cfg)

__all__ = [
    "COLLECTION", "EMPTY", "GONE", "HEARTS", "HELD_BEFORE", "IN_YOURS", "KEPT", "LEFT",
    "NOT_THIS_PASS", "OFFERED", "ON_ANOTHER", "PARTIAL_READ", "READ", "SHORT", "UNMEASURED",
    "UNREADABLE", "Answer", "Downloaded", "Listing", "Removed", "RemovedPlan", "WORKFLOW",
    "account_listing", "apply_removed", "downloaded", "identity", "job_playlists", "memberships",
    "plan_removed", "read_account", "read_hearts", "read_one", "recorded_contents", "recording",
    "removals", "synced"
]
