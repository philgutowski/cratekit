"""INSPIRATION brought level with the account's downloaded sets (U144).

The account's ``Downloaded Sets <year>`` folders hold one downloaded playlist
per set the source system downloaded, once prefixed ``DOWNLOADED `` and since
U242 held as taken in Cratekit's own record, and most of those sets were
downloaded before a set landing wrote a playlist under INSPIRATION (U121), so
their tracks are in the library with nothing naming the set. This step of
``crate organize``'s rekordbox area backfills them by MATCHING, chosen by the
author over running each set through the intake again: no track is
downloaded, a set the source system did not finish shows as a short playlist,
and every track left out is named under its set.

THE PLAN. Every taken playlist (:func:`cratekit.sync.playlists.is_taken`, the
record or the old prefix) in every root folder named ``Downloaded Sets
<year>``, or recorded by the archive as that year's folder whatever it is
called now, is one set, and its INSPIRATION name is the account name with any
old prefix off, spelled by the rule a set playlist's name is made
by (a slash becomes a dash). A playlist in such a folder that is not taken,
and a folder whose playlists could not be listed, are named on the gate and
read no further. A set whose name an INSPIRATION playlist already
carries, by the rule the set archive reads that proof with (U142), is skipped,
so a second run plans nothing. Every other set's tracks are read from the
account and each is asked of the library by the rule a set's own backfill
uses (:func:`cratekit.intake.set_playlist.library_rows`): the match engine
over the library now, the file's ISRC first and the artist, title and version
after, a person's review answers read back, then the one collection row the
file resolves to. No record ties a provider track to a library row by its
identifier, so none is read.

THE BAR A MATCH CLEARS TO BE WRITTEN UNREAD is the engine's MATCHED. A
question nobody answered, a track the library lacks, a version deleted on
purpose, a file with no collection row and a file two rows claim are misses,
each named under its set by position, artist and title with its reason. A set
with no match is reported and nothing is written for it: an empty playlist
kept for good is not the set. A set whose listing the provider refused is
shown unread with that refusal, and two account sets of one name are shown and
neither is written, since the library cannot hold both under one name.

A SET IS READ ROW BY ROW (R-1295), as ``crate sync all`` and ``crate sync
pair`` read a playlist. A track the account lists with no title or no artist is
never asked of the library, since the half left matches any file agreeing on
it; it is a miss at its place in the set, named by its id and why, and the
set's other tracks are matched as ever. A set no track of which reads is shown
unread, each track named, never as a set with no match. Such a row that carries
no provider id still leaves its set unread in the reader's own words,
since nothing would name it; a row the reader reads is matched with or
without an id, as it always was, because nothing here keys a track by its id.

THE WRITE is one session for every set: a capture, each playlist found live by
its name under INSPIRATION or made there by the rule a set's playlist is
(:func:`cratekit.intake.set_playlist.place_playlist`), the guarded commit, the
commit recorded under the INSPIRATION folder's own id, and every playlist read
back from SQL. The plan is taken again on the write handle first, and a
membership the approved plan did not name is refused by name, as is any other
change, with nothing written. Nothing here touches INBOX, a content row, a
beat grid or the account.

Layer: modules.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from contextlib import AbstractContextManager
from dataclasses import dataclass, field, replace
from typing import Any

from cratekit.acquire import match
from cratekit.cli.output import digest_of
from cratekit.core import analysis_store, config, convergence, rb_writer, session, snapshot
from cratekit.core.cause import CratekitError, refuse
from cratekit.modules.outbound.folders import MARK_PREFIX

_ORIGIN = ("organize.inspiration",)

#: The session workflow the step's write is recorded under, and the record
#: field naming every playlist it wrote.
WORKFLOW = "inspiration-parity"
RECORD_KEY = "inspiration_parity"

#: What becomes of one set, one word each.
CREATE = "create"
SKIP = "skip"
EMPTY = "empty"
UNREAD = "unread"
TWICE = "two-of-one-name"
#: A playlist in a sets folder without the prefix, and a sets folder whose
#: playlists could not be listed: each shown, neither read further.
UNPREFIXED = "unprefixed"
FOLDER_UNREAD = "folder-unread"

#: The prefix a downloaded set's account playlist carried before U242, which
#: a set still carrying it is read by until ``crate sync strip`` takes it off.
PREFIX = MARK_PREFIX


def sets_folder(name: str) -> bool:
    """Whether an account root folder is one year's downloaded sets, ``Downloaded Sets 2026``."""
    from cratekit.modules.outbound import sets

    return re.fullmatch(re.escape(sets.FOLDER_PREFIX) + r"\d{4}", name) is not None


@dataclass(frozen=True, slots=True)
class Miss:
    """One account track of a set the playlist will not hold, and why."""

    position: int
    artist: str
    title: str
    why: str

    def line(self) -> str:
        return f"{self.position}. {self.artist} - {self.title}: {self.why}"


@dataclass(frozen=True, slots=True)
class SetRow:
    """One downloaded set on the account, and what the plan does for it."""

    #: The INSPIRATION name, the account name without its prefix.
    name: str
    #: The account playlist and the folder it sits in.
    playlist_id: str
    folder: str
    action: str
    #: The collection rows the playlist holds, distinct, in the set's order.
    members: tuple[str, ...] = ()
    misses: tuple[Miss, ...] = ()
    #: Tracks the provider counts on the playlist and would not list.
    withheld: int = 0
    #: Why a set is unread or left, in the words the gate shows.
    why: str = ""
    #: The account tracks as read, each at its place in the set, kept so the
    #: write asks the library again about exactly these and never reads the
    #: account a second time.
    wanted: tuple[tuple[int, match.Wanted], ...] = field(default=(), compare=False)
    #: The tracks the account lists with no title or no artist, each a miss at
    #: its place in the set (R-1295), kept beside ``wanted`` for the same
    #: reason; ``misses`` carries them too.
    unread: tuple[Miss, ...] = field(default=(), compare=False)

    def identity(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "playlist": self.playlist_id,
            "folder": self.folder,
            "action": self.action,
            "members": list(self.members),
            "misses": [miss.line() for miss in self.misses],
            "withheld": self.withheld,
            "why": self.why,
        }

    def item(self) -> dict[str, Any]:
        """The set as the gate shows it, every miss named under it."""
        shown: dict[str, Any] = {
            "action": self.action,
            "set": self.name,
            "account folder": self.folder,
            "account playlist": self.playlist_id,
        }
        if self.action in (CREATE, EMPTY):
            shown["tracks"] = len(self.members)
            shown["misses"] = [miss.line() for miss in self.misses]
            if self.withheld:
                shown["withheld"] = (
                    f"{self.withheld} track(s) the provider counts on the playlist "
                    f"and would not list, so not one of them was asked of the library"
                )
        if self.why:
            shown["reason"] = self.why
        return shown


@dataclass(frozen=True, slots=True)
class ParityPlan:
    """Every downloaded set on the account, each with what is done for it."""

    tree_id: str
    folder_display: str
    #: The INSPIRATION folder's row, or empty when the write makes it.
    folder_id: str
    rows: tuple[SetRow, ...]

    @property
    def creates(self) -> tuple[SetRow, ...]:
        return tuple(row for row in self.rows if row.action == CREATE)

    @property
    def writes(self) -> bool:
        return bool(self.creates)

    def identity(self) -> dict[str, Any]:
        return {
            "kind": "inspiration-parity",
            "tree": self.tree_id,
            "folder": self.folder_id,
            "folder_display": self.folder_display,
            "sets": [row.identity() for row in self.rows],
        }

    def digest(self) -> str:
        return digest_of(self.identity())

    def counts(self) -> dict[str, int]:
        tally = Counter(row.action for row in self.rows)
        return {
            "sets": len(self.rows),
            "to create": tally[CREATE],
            "already in INSPIRATION": tally[SKIP],
            "no match": tally[EMPTY],
            "unread": tally[UNREAD],
            "two of one name": tally[TWICE],
            "not taken": tally[UNPREFIXED],
            "folders unread": tally[FOLDER_UNREAD],
            "tracks matched": sum(len(row.members) for row in self.creates),
            "tracks missed": sum(len(row.misses) + row.withheld for row in self.creates),
        }

    def items(self) -> list[dict[str, Any]]:
        return [row.item() for row in self.rows]

    def detail(self) -> str:
        counts = self.counts()
        rest = (
            f"{counts['already in INSPIRATION']} set(s) already in INSPIRATION, "
            f"{counts['no match']} with no track in the library, {counts['unread']} unread, "
            f"{counts['not taken']} not taken, {counts['folders unread']} folder(s) unread"
        )
        if self.writes:
            return (
                f"create {counts['to create']} INSPIRATION playlist(s) of "
                f"{counts['tracks matched']} matched track(s), naming the "
                f"{counts['tracks missed']} missed under each set; {rest}; no track "
                f"is downloaded"
            )
        return f"nothing to create: {rest}"


@dataclass(frozen=True, slots=True)
class Wrote:
    """One playlist the write made or found, and what was read back under it."""

    name: str
    playlist_id: str
    created: bool
    members: tuple[str, ...]
    added: int
    read_back: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Applied:
    """What the write did, every playlist read back."""

    wrote: tuple[Wrote, ...]
    folder_created: bool
    session_id: str

    def totals(self) -> dict[str, Any]:
        return {
            "playlists created": sum(1 for one in self.wrote if one.created),
            "memberships added": sum(one.added for one in self.wrote),
            "read back": {one.name: len(one.read_back) for one in self.wrote},
            "folder created": self.folder_created,
            "session": self.session_id,
        }


# ---------------------------------------------------------------------------
# The plan
# ---------------------------------------------------------------------------


def account_sets(
    remote: Any, recorded: Iterable[str] = (), taken: Iterable[str] = ()
) -> tuple[list[tuple[str, str, str]], list[SetRow]]:
    """Every downloaded set on the account, and every row nothing is planned for.

    The sets are ``(folder name, playlist id, INSPIRATION name)``, in folder
    then name order. A SETS FOLDER is a root folder named ``Downloaded Sets
    <year>``, or one whose id ``recorded`` names, which is the folder the
    archive files into by its ledger record whatever it is called now. Two
    kinds of row are answered beside the sets and never read further: a folder
    whose playlists could not be listed, unread and not empty, and a playlist
    in a sets folder without the prefix, which the archive leaves unprefixed
    when a person retitled it, named so it is not silently passed over.

    A SET IS A TAKEN PLAYLIST (U242): one ``taken``, the record's taken
    ledger, holds, or one whose title still carries the old prefix. Its
    INSPIRATION name is its title less any prefix, so a set stripped of the
    prefix is the same set under the same name.
    """
    from cratekit.export import set_cli
    from cratekit.sync.playlists import is_taken, untaken_name

    marked = frozenset(recorded)
    held = frozenset(taken)
    sets_found: list[tuple[str, str, str]] = []
    rows: list[SetRow] = []
    folders = sorted(remote.folders().items(), key=lambda one: (one[1], one[0]))
    for folder_id, folder_name in folders:
        if not sets_folder(folder_name) and folder_id not in marked:
            continue
        try:
            listed = remote.folder_playlists(folder_id)
        except CratekitError as exc:
            rows.append(
                SetRow(
                    "",
                    "",
                    folder_name,
                    FOLDER_UNREAD,
                    why=f"its playlists could not be listed: {exc.cause.message}",
                )
            )
            continue
        for playlist_id, name in sorted(listed.items(), key=lambda one: (one[1], one[0])):
            stripped = untaken_name(name) if is_taken(playlist_id, name, held) else ""
            if not stripped:
                rows.append(
                    SetRow(
                        name,
                        playlist_id,
                        folder_name,
                        UNPREFIXED,
                        why=(
                            f"Cratekit does not hold it as taken and it does not carry "
                            f"the old {PREFIX.strip()} prefix, so it is not read as a "
                            f"downloaded set"
                        ),
                    )
                )
                continue
            sets_found.append((folder_name, playlist_id, set_cli.set_name(stripped)))
    return sets_found, rows


def recorded_folders(cfg: config.Config) -> frozenset[str]:
    """Every root folder id the ledger records as a year's downloaded sets folder."""
    from cratekit.modules.outbound import ledger

    return frozenset(
        folder_id for name, folder_id in ledger.set_folders(cfg).items() if sets_folder(name)
    )


@dataclass(frozen=True, slots=True)
class _Listed:
    """One set as read from the account, row by row (R-1295)."""

    #: Each track the match engine read, at its place in the set.
    wanted: tuple[tuple[int, match.Wanted], ...]
    #: Each track it would not read, at its place, as the account names it.
    unread: tuple[tuple[int, Any], ...]
    #: Tracks the provider counts on the playlist and would not list.
    withheld: int


def _read(found: Any, playlist_id: str) -> _Listed:
    """The set's account tracks as the match engine reads them, row by row (R-1295).

    A row the engine will not read, naming no title or no artist, is set aside
    by the reader's own rule (``intake_cli.set_aside``) and named, and every
    other row reads as it always did. Such a row carrying no provider id
    raises the engine's own refusal with that said after it, so the set is
    shown unread and the reason names the missing id as what held it back.
    """
    from cratekit.intake import cli as intake_cli
    from cratekit.label import cli as label_cli

    rows, short = label_cli.playlist_listing_or_refuse(found, playlist_id)
    wanted: list[tuple[int, match.Wanted]] = []
    unread: list[tuple[int, Any]] = []
    for position, row in enumerate(rows, start=1):
        try:
            wanted.append((position, match.read_row(row, origin=match.TIDAL, position=position)))
        except match.UnreadableList as exc:
            one = intake_cli.set_aside(row)
            if not one.ref:
                # NOTHING WOULD NAME IT among the misses, so the set stays
                # unread, and the reason says the id is what held it back.
                raise match.UnreadableList(
                    f"{exc}; it carries no provider id either, so it cannot be named "
                    f"among the set's misses and the set is not written",
                    line=position,
                ) from exc
            unread.append((position, one))
    return _Listed(tuple(wanted), tuple(unread), short.withheld if short is not None else 0)


#: How many unread tracks a set's reason names before it counts the rest.
NAMED_UNREAD = 5


def _none_read(listing: _Listed) -> str:
    """Why a set no track of which reads is shown unread: the first tracks, a count, the withheld."""
    shown = ", ".join(f"{one.ref} ({one.why})" for _place, one in listing.unread[:NAMED_UNREAD])
    rest = len(listing.unread) - NAMED_UNREAD
    said = f"no track of the set could be read: {shown}"
    if rest > 0:
        said += f", and {rest} more the same way"
    if listing.withheld:
        said += (
            f"; the provider also counts {listing.withheld} track(s) on the playlist "
            f"it would not list"
        )
    return said


def _unread_miss(position: int, one: Any) -> Miss:
    """A track the account lists with no title or no artist, named under its set."""
    return Miss(
        position,
        one.artist or "no artist",
        one.title or "no title",
        f"{one.why} (track {one.ref}), so it was not asked of the library",
    )


def _matched(
    row_of: Callable[[match.Wanted], tuple[str, str]],
    wanted: Sequence[tuple[int, match.Wanted]],
    unread: Sequence[Miss] = (),
) -> tuple[tuple[str, ...], tuple[Miss, ...]]:
    """Each track's collection row, distinct and in set order, and every miss named in set order."""
    ids: list[str] = []
    misses: list[Miss] = list(unread)
    for position, one in wanted:
        held, why = row_of(one)
        if held:
            ids.append(held)
        else:
            misses.append(Miss(position, one.artist, one.listed, why))
    return tuple(dict.fromkeys(ids)), tuple(sorted(misses, key=lambda miss: miss.position))


def _decided(
    name: str,
    playlist_id: str,
    folder: str,
    wanted: tuple[tuple[int, match.Wanted], ...],
    withheld: int,
    row_of: Callable[[match.Wanted], tuple[str, str]],
    unread: tuple[Miss, ...] = (),
) -> SetRow:
    members, misses = _matched(row_of, wanted, unread)
    return SetRow(
        name=name,
        playlist_id=playlist_id,
        folder=folder,
        action=CREATE if members else EMPTY,
        members=members,
        misses=misses,
        withheld=withheld,
        why="" if members else "no track of the set matched a library row, so nothing is written",
        wanted=wanted,
        unread=unread,
    )


class _Rows:
    """The library resolver, built only once a set needs it, since it walks the library."""

    def __init__(self, cfg: config.Config, db: Any) -> None:
        self._cfg = cfg
        self._db = db
        self._row_of: Callable[[match.Wanted], tuple[str, str]] | None = None

    def __call__(self, wanted: match.Wanted) -> tuple[str, str]:
        if self._row_of is None:
            from cratekit.intake import set_playlist

            self._row_of = set_playlist.library_rows(self._cfg, self._db)
        return self._row_of(wanted)


def _held(db: Any, folder_id: str) -> frozenset[str]:
    """Every set name an INSPIRATION playlist carries now, by the archive's own rule."""
    from cratekit.export import set_cli

    return frozenset(name for name, _id in set_cli.inspiration_playlists_on(db, folder_id))


def plan(
    cfg: config.Config,
    declared: Any,
    *,
    remote: Any,
    found: Any,
    reading: Callable[[], AbstractContextManager[Any]],
) -> ParityPlan:
    """Every downloaded set on the account, decided against INSPIRATION and the library.

    ``remote`` is the account, for its folders; ``found`` is the catalogue,
    for each set's tracks; ``reading`` opens a read handle on the database.
    THE DATABASE IS NEVER HELD OPEN ACROSS A PROVIDER CALL: it is opened once
    to read where INSPIRATION is and what it holds, closed while the account
    is read, and opened again to match only when a set has tracks to match. A
    taxonomy with no INSPIRATION folder, or a root holding it twice, refuses
    by the set playlist's own rule.
    """
    from cratekit.intake import set_playlist

    with reading() as db:
        folder_id, node = set_playlist.folder_for(db, declared)
        held = _held(db, folder_id)
    from cratekit.sync.playlists import taken_ids

    listed, rows = account_sets(remote, recorded_folders(cfg), taken_ids(cfg))
    named = Counter(name for _folder, _pid, name in listed)
    read: list[tuple[str, str, str, _Listed]] = []
    for folder, playlist_id, name in listed:
        if name in held:
            rows.append(SetRow(name, playlist_id, folder, SKIP))
            continue
        if named[name] > 1:
            rows.append(
                SetRow(
                    name,
                    playlist_id,
                    folder,
                    TWICE,
                    why=(
                        f"{named[name]} downloaded sets on the account carry this name "
                        f"and INSPIRATION can hold one, so neither is written; rename "
                        f"one on the account"
                    ),
                )
            )
            continue
        try:
            listing = _read(found, playlist_id)
        except CratekitError as exc:
            rows.append(SetRow(name, playlist_id, folder, UNREAD, why=exc.cause.message))
            continue
        except match.UnreadableList as exc:
            rows.append(SetRow(name, playlist_id, folder, UNREAD, why=str(exc)))
            continue
        if listing.unread and not listing.wanted:
            # EVERY TRACK UNREAD is a set that could not be read, not one with
            # no match, and is shown with each track and why (R-1295).
            rows.append(
                SetRow(
                    name,
                    playlist_id,
                    folder,
                    UNREAD,
                    withheld=listing.withheld,
                    why=_none_read(listing),
                )
            )
            continue
        read.append((name, playlist_id, folder, listing))
    if read:
        with reading() as db:
            row_of = _Rows(cfg, db)
            rows.extend(
                _decided(
                    name,
                    playlist_id,
                    folder,
                    listing.wanted,
                    listing.withheld,
                    row_of,
                    tuple(_unread_miss(place, one) for place, one in listing.unread),
                )
                for name, playlist_id, folder, listing in read
            )
    return ParityPlan(
        tree_id=node.id,
        folder_display=node.display,
        folder_id=folder_id,
        rows=tuple(sorted(rows, key=lambda row: (row.folder, row.name, row.playlist_id))),
    )


def again(cfg: config.Config, db: Any, declared: Any, approved: ParityPlan) -> ParityPlan:
    """The approved plan taken again on ``db``: INSPIRATION and the library read now.

    THE ACCOUNT IS NOT READ AGAIN. Its tracks were read for the plan a person
    approved and are what the plan names; the write asks the library about
    exactly those. A set skipped then whose INSPIRATION playlist has gone is
    no longer skipped, so it reads as a change rather than as nothing.
    """
    from cratekit.export import set_cli
    from cratekit.intake import set_playlist

    folder_id, node = set_playlist.folder_for(db, declared)
    held = _held(db, folder_id)
    row_of = _Rows(cfg, db)
    rows: list[SetRow] = []
    for row in approved.rows:
        now = set_cli.set_name(row.name) in held
        if row.action == SKIP:
            rows.append(
                row
                if now
                else replace(row, action=UNREAD, why="its INSPIRATION playlist went since the plan")
            )
        elif row.action in (CREATE, EMPTY):
            rows.append(
                replace(row, action=SKIP, members=(), misses=(), withheld=0, why="")
                if now
                else _decided(
                    row.name,
                    row.playlist_id,
                    row.folder,
                    row.wanted,
                    row.withheld,
                    row_of,
                    row.unread,
                )
            )
        else:
            rows.append(row)
    return ParityPlan(
        tree_id=node.id, folder_display=node.display, folder_id=folder_id, rows=tuple(rows)
    )


def assert_unchanged(approved: ParityPlan, now: ParityPlan) -> None:
    """Refuse a write the approved plan does not describe, naming a membership it never showed.

    A MEMBERSHIP THE PLAN DID NOT NAME IS REFUSED BY NAME FIRST: a set whose
    track now resolves to a row the person was not shown would be written
    with it. Any other change, a set gone or a miss that moved, refuses as the
    plan being stale. Either way nothing is written.
    """
    shown = {row.name: set(row.members) for row in approved.rows}
    for row in now.creates:
        unnamed = [one for one in row.members if one not in shown.get(row.name, set())]
        if unnamed:
            raise refuse(
                "decision-stale",
                f"the INSPIRATION playlist {row.name!r} would now hold "
                f"{len(unnamed)} track(s) the approved plan did not name, so nothing "
                f"was written; organize again and approve what it shows now",
                origin=_ORIGIN,
                detail={"set": row.name, "unnamed": unnamed},
            )
    if now.digest() != approved.digest():
        raise refuse(
            "decision-stale",
            "INSPIRATION or the library is not as the approved plan read it, so "
            "nothing was written; organize again and approve what it shows now",
            origin=_ORIGIN,
            detail={"approved": approved.digest(), "now": now.digest()},
        )


# ---------------------------------------------------------------------------
# The write
# ---------------------------------------------------------------------------


def write(db: Any, approved: ParityPlan) -> tuple[list[Wrote], bool]:
    """Make each planned playlist under INSPIRATION and add its members, pending on ``db``.

    INSIDE A CALLER'S SESSION, which commits or rolls back. Only the rows the
    plan names are added, to the playlist of the set's name. The folder is
    made once, for the first set, when the plan read none.
    """
    from cratekit.intake import set_playlist

    folder_id = approved.folder_id
    folder_created = False
    wrote: list[Wrote] = []
    for row in approved.creates:
        folder, made_folder, playlist, created = set_playlist.place_playlist(
            db, folder_id=folder_id, folder_display=approved.folder_display, name=row.name
        )
        folder_created = folder_created or made_folder
        folder_id = str(folder.ID)
        added = rb_writer.add_memberships(db, playlist, row.members)
        wrote.append(Wrote(row.name, str(playlist.ID), created, row.members, len(added)))
    return wrote, folder_created


def _record_parity_commit(
    record: session.SessionRecord,
    wrote: Iterable[Wrote],
    approved: ParityPlan,
    cfg: config.Config,
) -> None:
    """Record the commit under the INSPIRATION folder's own id, only when it changed a row."""
    made = [one for one in wrote if one.added or one.created]
    if not made:
        return
    record.detail[RECORD_KEY] = [
        {"id": one.playlist_id, "name": one.name, "added": one.added} for one in made
    ]
    changes = (
        session.TreeChange(tree=approved.tree_id, created=sum(one.added for one in made)),
    )
    session.record_commit(record, approved.tree_id, session.ChangeSummary(changes), cfg)


def assert_read_back(wrote: Iterable[Wrote]) -> None:
    """Refuse an answer the database does not hold.

    A PLAYLIST THIS WRITE MADE HOLDS EXACTLY THE PLAN'S ROWS, in the set's
    order, and nothing else: a row read back under it that the plan did not
    name is a membership nobody approved. One found by its name holds every
    planned row, whatever it held before.
    """
    for one in wrote:
        live = list(one.read_back)
        missing = [row for row in one.members if row not in set(live)]
        exact = live == list(one.members)
        if missing or (one.created and not exact):
            unnamed = [row for row in live if row not in set(one.members)]
            raise refuse(
                "session-committed-unverified",
                f"the INSPIRATION playlist {one.name!r} ({one.playlist_id}) read back "
                f"from the database holds {len(live)} live track(s): {len(missing)} of "
                f"the {len(one.members)} the plan named are not among them and "
                f"{len(unnamed)} it did not name are; the commit landed and this "
                f"answer cannot be vouched for",
                origin=_ORIGIN,
                detail={
                    "playlist_id": one.playlist_id,
                    "planned": list(one.members),
                    "read": live,
                    "missing": missing,
                    "unnamed": unnamed,
                },
            )


def apply(cfg: config.Config, declared: Any, approved: ParityPlan) -> Applied:
    """Write the approved plan in a session of its own, on a handle opened to write.

    rekordbox must be closed. The plan is taken again on this handle and
    refused when it moved, and the tree's convergence latch is asked; then the
    session spine every database writer calls: the gates with a record kept, a capture verified before anything
    is written, the analysis watch, the commit witness and the guarded commit.
    """
    from cratekit.core import tree_registry

    watched = list(analysis_store.watch_roots(cfg))
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        assert_unchanged(approved, again(cfg, db, declared, approved))
        # THE TREE'S OWN LATCH FIRST, as every tree writer's: a database
        # restored out of band is detected before this write's fingerprint
        # overwrites the evidence, and a tree marked unconverged is refused.
        convergence.assert_tree_writable(cfg, db, approved.tree_id, tree_registry.read(cfg))
        wrote: list[Wrote] = []
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
            try:
                wrote, folder_created = write(db, approved)
                rb_writer.commit_guarded(db)
            except BaseException:
                from cratekit.write import trees

                trees._rollback_quietly(db)
                if witness.landed and wrote:
                    _record_parity_commit(record, wrote, approved, cfg)
                raise
            _record_parity_commit(record, wrote, approved, cfg)
            convergence.record_fingerprint(cfg, db)
            from cratekit.intake import set_playlist

            wrote = [
                replace(one, read_back=set_playlist.read_back(db, one.playlist_id))
                for one in wrote
            ]
    finally:
        rb_writer.close_db(db)
    assert_read_back(wrote)
    return Applied(wrote=tuple(wrote), folder_created=folder_created, session_id=record.session_id)


__all__ = [
    "CREATE",
    "EMPTY",
    "FOLDER_UNREAD",
    "NAMED_UNREAD",
    "PREFIX",
    "RECORD_KEY",
    "SKIP",
    "TWICE",
    "UNPREFIXED",
    "UNREAD",
    "WORKFLOW",
    "Applied",
    "Miss",
    "ParityPlan",
    "SetRow",
    "Wrote",
    "account_sets",
    "again",
    "apply",
    "assert_read_back",
    "assert_unchanged",
    "plan",
    "recorded_folders",
    "sets_folder",
    "write",
]
