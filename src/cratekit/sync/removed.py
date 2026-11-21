"""Which downloaded tracks the account no longer lists, and which would leave the collection (U287).

A pass sweeps the playlists the author made on the streaming account, and its
landing gives each an INBOX playlist of the tracks the library holds (U113,
U128). When Phillip later takes a track off one of those playlists on the
account, nothing in Cratekit noticed: ``sync pair`` refuses a playlist under
INBOX by design, and the INBOX refill (U134) reads the pass's recorded reports,
never the account. This module is the noticing. It reads every downloaded
playlist again, finds each track its pass recorded that the account no longer
lists, resolves it to its collection row, and answers each row as OFFERED for
removal from the collection or KEPT, with why. The plan writes nothing
anywhere: no row, no file, no account write, no record. U288's gate shows it
and binds to its digest, and :func:`apply_removed` takes the offered rows out
of the collection behind that gate, as rekordbox's Remove from Collection does.

WHAT IS DOWNLOADED. An account playlist an ``intake.playlist`` job with a
recorded name succeeded for, whose pass has a standing landing record naming
it by the account's identifier and the pass (U128's ``inbox_playlists``
entry). A job no landing names is not downloaded, since nothing of it reached
the collection. What is SYNCED, for the question "is it still on another
synced playlist", is wider: every playlist the sweep's cursor holds, every one
an intake job of this library was queued for (the cursor as it is in effect,
before the next sweep reconciles a finished job into it), every one the mark
record holds as taken, every one ``sync pair`` keeps, every downloaded one, and
the account's hearts, which the favourites source brings into All Favorites.

A PARTIAL READ OFFERS NOTHING, the deletion pass's rule (R37) applied to the
account. "Still on another synced playlist" is a claim about every synced
playlist, and a playlist that could not be read, read short of the count the
provider declares, or read with no tracks while nothing says it holds none,
contributes nothing to it, so the claim would pass on absence of evidence. So
while any synced playlist is not read whole, every row that would be offered
is kept, and the plan says which playlists stopped it. A playlist the
account's own listing no longer names, and that cannot be opened by its id
either, is GONE, since the listing alone stops on an empty page with no total
to check it against (R-385). Its tracks are offered nothing, since deleting a
playlist whole is not taking a track off it. A failed open is any provider
failure, not a not found, so a gone playlist is still read as holding what its
finished jobs recorded, and one nothing records is not read whole. A playlist
the listing omits and its id still opens is read as any other.

TWO SHAPES ARE READ WHOLE FOR THIS QUESTION (U320), since without them no
removal could ever be offered on the author's account. The hearts listed
short only by what the provider withholds, R-504's shortfall over a walk that
reached the declared count and served hearts, are WITHHELD: they hold every
heart served, since a heart the provider will not serve is not one the account
shows, and are named with both counts; no heart served at all, or a shortfall
over a tenth of the count or of 49 hearts, which a dropped window looks like,
stays short. And
a playlist the account no longer lists whose id answers the provider's NOT
FOUND, a 404 and nothing else, is a sighting in
:mod:`cratekit.sync.unavailable`'s record; a sighting a day after the first,
or a person at the explicit gate ``sync.removed.retire``, RETIRES it, and a
retired playlist holds nothing and stops nothing until it opens again or the
account lists it again. Every other failure reads it as before U320, gone or
not read whole, a retired one for that run alone, its retirement kept.

A TRACK IS REMOVED when its playlist's listing holds no row of its provider
id, and no read row of it carries its ISRC or its artist and title as the
matcher folds a recording, version excluded. The same rule says whether
another synced playlist still holds it. Each test can only say "still there",
so every one of them errs toward keeping.

EACH ROW GETS ONE ANSWER, the first that holds of these:

* ``left``: the library holds no row for the track, two rows claim its file,
  or a person's question about it is unanswered, as the backfill's resolver
  says (U121, U144), or the report never carried a file at all;
* ``kept, held before the pass``: the report says the library already owned it
  when the job ran, so a person or another pass brought it in;
* ``kept, not this pass's file``: the row's file is not under a folder a
  standing landing of its pass recorded filing into (``filed_batch``), so the
  match found a file this pass did not bring;
* ``kept, on another synced playlist``;
* ``kept, named by a table rekordbox's removal was never measured on``: a My
  Tag (the landing's own ``vox`` and ``dyn`` included), a sampler slot,
  related tracks, a hot cue bank list, a tag list, an active censor, an image
  row or a table this build does not know names the row, so the removal
  would refuse it (U288), checked after the playlists below;
* ``kept, in a playlist of yours``: a live membership anywhere but the intake
  tree, the routing tree, or the custom playlist twin a landing recorded for a
  playlist it left. A label year playlist keeps the row: Phillip answered
  on 2026-11-21 that Cratekit's own filing keeps nothing, and the label
  year playlists are not yet told apart from a person's here (a residual);
* ``offered``.

One collection row reached from two playlists, or two passes, is one answer
naming each playlist it left, and it is offered when ANY report says its pass
brought the file, since a later pass reads an earlier pass's download as
owned.

Layer: modules. It reads configuration through the objects it is handed and
opens no database of its own; the verb hands it a read only copy.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import datetime
from pathlib import Path
from typing import Any

from cratekit.acquire import match
from cratekit.cli.output import digest_of
from cratekit.core import (
    config,
    convergence,
    jobs,
    locations,
    rb_writer,
    session,
    snapshot,
    taxonomy,
    tree_registry,
)
from cratekit.core.cause import CratekitError, refuse
from cratekit.intake import account_playlists, ingest, native, refill, set_playlist
from cratekit.intake import cli as intake_cli
from cratekit.label import catalogue
from cratekit.sync import playlists, twins, unavailable
from cratekit.sync.watermarks import WatermarkStore

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
#: U288. A row a table rekordbox's removal was never measured on names, a vox
#: or dyn My Tag above all: the removal would refuse it, so it is never offered.
UNMEASURED = "named by a table rekordbox's removal was never measured on"

#: Why a removed track has no row to answer, beside the resolver's own reasons.
NOT_CARRIED = "the pass never downloaded it"
OWNED_NO_ROW = "held before the pass, and no collection row holds its file now"

#: How each synced playlist read. Only ``read`` answers anything; ``gone`` is an
#: answer about the playlist, and the other three are a read that is not whole.
READ = "read"
GONE = "gone"
UNREADABLE = "unreadable"
SHORT = "short"
EMPTY = "empty"
NOT_WHOLE = frozenset({UNREADABLE, SHORT, EMPTY})
#: The hearts, short only by what the provider withholds, read whole for this question (U320).
WITHHELD = "withheld"
#: A synced playlist retired by the record of not found answers: holds nothing, stops nothing (U320).
RETIRED = "retired"
#: The reader's refusal of rows a playlist served: its id opened, so it is not gone.
SERVED_UNREADABLE = "intake-list-unusable"

#: The most of its declared count the hearts may be short by and still read whole
#: (U320), as a fraction: a provider measured withholding 12 of 197 and 9 of 349.
WITHHELD_AT_MOST = 0.10

#: And the most hearts, whatever the count (round two): under half of the
#: hundred a hearts page holds (``acquire.listing``'s page size), so a window
#: the provider dropped, or cut by more than half, stays short on an account of
#: any size.
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
    #: What the record of not found answers holds for this playlist after this
    #: read (U320), ``None`` for nothing: never part of the digest, which reads
    #: the state and the words it carries.
    noted: unavailable.Sighting | None = None
    #: Whether the account no longer lists it and its id answered not found on this read.
    not_found: bool = False

    def holds(self, wanted: match.Wanted) -> bool:
        """Whether this listing still holds the track, by any of the three tests.

        A GONE playlist holds what its finished jobs recorded, its last known
        contents, since "gone" is two reads failing; the hearts short only by
        what the provider withholds hold every heart it served (U320). A
        RETIRED playlist holds nothing and stops nothing, and nothing else not
        read whole holds anything, and stops every offer instead.
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
    digest: str = ""

    @property
    def offered(self) -> tuple[Answer, ...]:
        return tuple(one for one in self.answers if one.answer == OFFERED)

    def count(self, answer: str) -> int:
        return sum(1 for one in self.answers if one.answer == answer)


def identity(plan: RemovedPlan) -> dict[str, Any]:
    """What the digest covers: every playlist read, every answer, and the partial flag."""
    return {
        "kind": "sync-removed",
        "playlists": [one.identity() for one in plan.listings],
        "answers": [one.identity() for one in plan.answers],
        "partial": plan.partial,
        "unreadable": plan.unreadable,
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

    THE LANDING RECORD DECIDES, never the job alone: a pass whose files never
    landed put nothing in the collection to remove. Only an entry carrying the
    account's identifier counts, which every landing since U128 writes.
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

    ``swept_now`` is :func:`job_playlists`, the cursor as it is in effect.
    ``listed`` is the account's own list: a playlist still titled with the
    retired swept prefix is taken until ``sync strip`` records it (U242,
    :func:`playlists.is_taken`), so it is synced too (round two).

    THE TAKEN RECORD IS READ, AND REFUSES WHEN IT CANNOT BE: an unread record
    is a set of synced playlists nobody can name, and "on no other synced
    playlist" would be claimed over it.
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


#: What a GONE playlist is asked of: an account's id to what its finished jobs recorded,
#: or None when nothing can say.
Recorded = Callable[[str], "tuple[match.Wanted, ...] | None"]


def recorded_contents(cfg: config.Config) -> Recorded:
    """What one account playlist's finished intake jobs recorded, asked only of a GONE playlist.

    Every ``intake.playlist`` job of this library for that playlist that
    SUCCEEDED, every report read, the hearts' job left out. ASKED PER PLAYLIST
    AND ONLY WHEN ONE READS GONE, so a damaged or pre U57 job of some other
    playlist never refuses the verb (round two): a job of this playlist whose
    reports cannot be read answers None, and the playlist is not read whole.
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

    THE CURSOR AS IT IS IN EFFECT, not as its file stands: a job that finished
    since the last sweep is in the cursor only once the next sweep reconciles
    it, and an open one holds its playlist back, so either is a synced playlist
    now. The hearts' job names no playlist and is left out.
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

    ``sightings`` is the record of not found answers as it stood before this
    run, ``moment`` when this run asked, and ``names`` what Cratekit calls a
    playlist the account's list no longer names (U320). The listing carries what
    the record holds for the playlist after this read, in ``noted``: a not
    found while the account's list omits it is a sighting, which retires it a
    day after the first; any other failure leaves the entry as it stands; a
    playlist that opens, or that the account lists again, holds none.
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
            # GONE ONLY WHEN TWO READS AGREE, and even then not read as empty.
            # The account's list stops on an empty page and publishes no total
            # (R-385), and the id's failure is any provider failure, so a gone
            # playlist still holds what its finished jobs recorded; one nothing
            # records is not read whole at all. ONLY A NOT FOUND IS A SIGHTING
            # (U320, R-1713): an outage leaves the record as it stands, so a
            # playlist that is only unreadable is never retired.
            # AND ONLY THIS READ'S NOT FOUND READS IT RETIRED (round one): a
            # retired playlist whose id now fails some other way keeps its
            # retirement in the record and is read not whole for this run, the
            # side that offers less.
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
        # LISTED BY THE ACCOUNT, or OPENED and its rows refused by the reader
        # (round one), so not gone whatever else it answers: the record holds
        # nothing for it, a retirement included.
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
        # AN EMPTY READ IS TRUSTED ONLY WHEN THE ACCOUNT'S OWN LISTING SAYS NONE,
        # two answers agreeing; an unknown count beside an empty read is the
        # shape a provider fault takes, and every track would read removed.
        return Listing(
            account=account,
            name=name,
            state=EMPTY,
            why="read with no tracks and nothing says it holds none",
        )
    # A ROW THE READER SET ASIDE (U213) STILL SAYS WHAT IT IS: its id is in
    # the order, and its ISRC, and its artist and title where it has both,
    # count as the read rows' do.
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
    """The account's own playlists by identifier, or the sweep's refusal for an unread list.

    AN UNREAD LIST REFUSES THE WHOLE VERB rather than reading every playlist
    as gone, which is the shape a provider fault would otherwise take.
    """
    return {one.playlist_id: one for one in playlists.account_listing(found)}


#: The account's hearts, read as one more synced listing.
HEARTS = "hearts"
HEARTS_NAME = "the account's hearts"


def read_hearts(found: catalogue.Catalogue) -> Listing:
    """The account's hearts as one more synced listing, through the favourites source's reader.

    A HEART KEEPS A TRACK as a synced playlist does: the favourites source
    brings every heart into All Favorites, and a heart made since the last
    ``sync favorites`` is in no rekordbox playlist yet. Read whole or not at
    all, by the rules a playlist is: unreadable, short of what the account
    declares, or empty, and nothing is offered.
    """
    try:
        frozen, short = intake_cli.list_favorites(found)
    except CratekitError as exc:
        if exc.cause.reason not in playlists.PER_PLAYLIST_REASONS:
            raise
        return Listing(account=HEARTS, name=HEARTS_NAME, state=UNREADABLE, why=exc.cause.message)
    # NO HEART SERVED NEEDS NO TEST OF ITS OWN: it is the whole count short,
    # which the bound refuses (the mutation table's M2 found the test dead).
    if short is not None and not (
        0 < short.withheld <= min(short.declared * WITHHELD_AT_MOST, WITHHELD_AT_MOST_HEARTS)
    ):
        # SHORT BY MORE THAN THE PROVIDER WITHHOLDS, or by nothing a walk
        # could reach: no heart served at all, which a provider serving nothing
        # looks like, numbers that do not reconcile, or more than a tenth of
        # the count short, which a window the provider dropped looks like
        # (round one): the provider publishes no withheld count of its own.
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
        # SHORT ONLY BY WHAT THE PROVIDER WITHHOLDS (U320, R-504's shape): the
        # walk ended on the count the account published and served hearts, so
        # every heart it lacks is one the provider counts and will not serve,
        # which the account does not show either. Read whole for this
        # question, and named with both counts.
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
) -> dict[str, Listing]:
    """Each playlist in ``wanted`` read once, against the account's listing read once."""
    return {
        account: read_one(
            found, account, listed, recorded, sightings=sightings, moment=moment, names=names
        )
        for account in dict.fromkeys(wanted)
    }


def noted(reads: Mapping[str, Listing]) -> dict[str, unavailable.Sighting | None]:
    """What the record of not found answers holds after these reads, by playlist (U320).

    Every playlist read says, ``None`` dropping its entry; the hearts are no
    playlist and say nothing.
    """
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

    A ROUTING TREE STILL ON THE BRIDGE, OR ONE WHOSE ROOT CANNOT BE ANCHORED,
    NAMES NOTHING: its playlists cannot be told from a person's by identifier,
    so a membership in one keeps the row, which is the side that removes less.
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
    plan = RemovedPlan(
        listings=listings,
        answers=tuple(answers),
        partial=partial,
        unreadable=unreadable,
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

#: What the change summary calls the place the rows left: the collection
#: itself, not a playlist tree, since a content row belongs to no tree.
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

    THE PLAN IS TAKEN AGAIN ON THIS HANDLE FIRST, the refill's rule, over the
    same account reads, and a digest that moved refuses with nothing written:
    the plan the person approved was read on a copy that has since closed.

    WHAT IS WRITTEN IS REKORDBOX'S OWN REMOVE FROM COLLECTION (A178, A185),
    through :func:`rb_writer.remove_from_collection`: each offered content row
    and every row naming it in the six tables beside it, deleted outright, the
    playlist and history list rows left as they are. A row any other table
    names refuses the whole apply. Nothing else: no kept or left row, no
    playlist row, no file, never a beat grid. The analysis files rekordbox
    deletes are left, and the orphan artist and album rows are left for
    rekordbox's next removal, which sweeps them.

    THE SESSION SPINE IS CALLED, NOT REBUILT: the gates with a record kept, a
    capture verified before anything is written, the analysis watch over the
    roots named, the commit witness, the SQL confinement before the commit and
    the guarded commit, whose whitelist admits the deletes by name and nothing
    else. Then the read back, the whole database from SQL against the reading
    taken before the first delete.

    THE RECORD NAMES EVERY ROW REMOVED, with the columns the deletion pass
    reads, the database's identity and the update count the commit left, so
    ``restore list`` names them and the next ``crate delete review`` offers
    their files (R-1037), each behind its own proofs and its own gate.
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
        record = gates.record
        capture = snapshot.capture(cfg, db=db)
        session.attach_capture(record, capture.root, cfg)
        snapshot.assert_verified(capture)
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
        session_id=session_id, rows=offered, deleted=dict(removal.deleted), sequence=sequence
    )


def _first_deletion_position(cfg: config.Config, db: Any) -> Callable[[], None] | None:
    """The deletion pass's first position, read before the removal, to give once it lands.

    A FIRST ``delete review`` BASELINES: it accepts every removal it can see as
    history and offers nothing (R35), and a removal recorded after that point
    would be one of them, so its file would never be offered (review round
    one). So when the pass has no position for this database, the position it
    would take is read here, before the removal's commit, with the pass's own
    rule (the greater of the counter and the highest marked removal), and is
    written only once the commit lands, so a refused removal leaves the pass
    as it found it (round two). Every removal before this one is then history
    and this one, at the count its commit leaves, is not. A position the pass
    already holds is kept, and the collection is not even read (round two).

    None when there is nothing to give. The deletion package is imported here,
    under the function, since it is a module of its own; it is asked whether
    the profile switches it on nowhere, so a library that turns deletion on
    later still finds its removals offered.
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

    Named the way the write session guard reads a commit helper. A sequence
    that could not be read is recorded as unknown, and the deletion pass then
    offers none of these files, keeping them rather than guessing.
    """
    removal.write_into(record.detail, sequence=sequence, about=about)
    changes = (session.TreeChange(tree=COLLECTION, removed=len(removal.content_ids)),)
    session.record_commit(record, COLLECTION, session.ChangeSummary(changes), cfg)

__all__ = [
    "COLLECTION",
    "EMPTY",
    "GONE",
    "HEARTS",
    "HELD_BEFORE",
    "IN_YOURS",
    "KEPT",
    "LEFT",
    "NOT_THIS_PASS",
    "OFFERED",
    "ON_ANOTHER",
    "PARTIAL_READ",
    "READ",
    "SHORT",
    "UNMEASURED",
    "UNREADABLE",
    "Answer",
    "Downloaded",
    "Listing",
    "Removed",
    "RemovedPlan",
    "WORKFLOW",
    "account_listing",
    "apply_removed",
    "downloaded",
    "identity",
    "job_playlists",
    "memberships",
    "plan_removed",
    "read_account",
    "read_hearts",
    "read_one",
    "recorded_contents",
    "recording",
    "removals",
    "synced",
]
