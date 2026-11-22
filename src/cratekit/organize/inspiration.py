"""INSPIRATION brought level with the account's downloaded sets (U144).

Most sets in the account's ``Downloaded Sets <year>`` folders were downloaded
before a set landing wrote an INSPIRATION playlist (U121). This step backfills
them by MATCHING, chosen by the author over running each set through the
intake again: nothing is downloaded, and every track left out is named.

THE PLAN. Every taken playlist (U242) in a sets folder is one set, named as its
account title less any prefix. A set INSPIRATION already holds, by the
archive's proof rule (U142), is skipped, so a second run plans nothing. Every
other set's tracks are asked of the library by a set backfill's own rule; only
the engine's MATCHED is written, and every other answer is a miss with its
reason. A set with no match, a refused listing, and two sets of one name are
shown and not written.

A SET IS READ ROW BY ROW (R-1295): a track with no title or no artist is never
asked of the library, since the half left matches any file agreeing on it, and
is a miss at its place; with no provider id either, its set is unread.

THE WRITE is one session for every set, taken again on the write handle first:
a membership the approved plan did not name is refused by name, any other
change as stale, with nothing written; every playlist is read back from SQL.

Layer: modules.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Callable, Iterable
from contextlib import AbstractContextManager
from dataclasses import dataclass, field, replace
from typing import Any

from cratekit.acquire import match
from cratekit.cli.output import digest_of
from cratekit.core import analysis_store, config, convergence, rb_writer, session
from cratekit.core.cause import CratekitError, refuse
from cratekit.organize.filing import by_name

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


def __getattr__(name: str) -> Any:
    """``PREFIX``, the prefix a downloaded set carried before U242, read from its home."""
    if name == "PREFIX":
        from cratekit.modules.outbound.folders import MARK_PREFIX

        return MARK_PREFIX
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


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
    #: The account tracks as read, each at its place in the set, so the write
    #: asks the library about exactly these and never reads the account again.
    wanted: tuple[tuple[int, match.Wanted], ...] = field(default=(), compare=False)
    #: The tracks listed with no title or no artist (R-1295), kept for the same
    #: reason; ``misses`` carries them too.
    unread: tuple[Miss, ...] = field(default=(), compare=False)

    def identity(self) -> dict[str, Any]:
        return {
            "name": self.name, "playlist": self.playlist_id, "folder": self.folder,
            "action": self.action, "members": list(self.members),
            "misses": [miss.line() for miss in self.misses],
            "withheld": self.withheld, "why": self.why,
        }

    def item(self) -> dict[str, Any]:
        """The set as the gate shows it, every miss named under it."""
        shown: dict[str, Any] = {
            "action": self.action, "set": self.name,
            "account folder": self.folder, "account playlist": self.playlist_id,
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
            "kind": "inspiration-parity", "tree": self.tree_id, "folder": self.folder_id,
            "folder_display": self.folder_display, "sets": [row.identity() for row in self.rows],
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
            "folder created": self.folder_created, "session": self.session_id,
        }


def account_sets(
    remote: Any, recorded: Iterable[str] = (), taken: Iterable[str] = ()
) -> tuple[list[tuple[str, str, str]], list[SetRow]]:
    """Every downloaded set on the account, and every row nothing is planned for.

    The sets are ``(folder name, playlist id, INSPIRATION name)``, in folder
    then name order. A SETS FOLDER is named ``Downloaded Sets <year>`` or is one
    ``recorded`` names, the archive's folder by its ledger. A folder that could
    not be listed, and a playlist in a sets folder that is not taken, are rows
    beside the sets, named so neither is silently passed over.

    A SET IS A TAKEN PLAYLIST (U242), held by ``taken`` or carrying the old
    prefix, and its INSPIRATION name is its title less any prefix.
    """
    from cratekit.export import set_cli
    from cratekit.modules.outbound.folders import MARK_PREFIX
    from cratekit.sync.playlists import is_taken, untaken_name

    marked = frozenset(recorded)
    held = frozenset(taken)
    sets_found: list[tuple[str, str, str]] = []
    rows: list[SetRow] = []
    for folder_id, folder_name in by_name(remote.folders().items()):
        if not sets_folder(folder_name) and folder_id not in marked:
            continue
        try:
            listed = remote.folder_playlists(folder_id)
        except CratekitError as exc:
            why = f"its playlists could not be listed: {exc.cause.message}"
            rows.append(SetRow("", "", folder_name, FOLDER_UNREAD, why=why))
            continue
        for playlist_id, name in by_name(listed.items()):
            stripped = untaken_name(name) if is_taken(playlist_id, name, held) else ""
            if not stripped:
                why = (
                    f"Cratekit does not hold it as taken and it does not carry "
                    f"the old {MARK_PREFIX.strip()} prefix, so it is not read as a "
                    f"downloaded set"
                )
                rows.append(SetRow(name, playlist_id, folder_name, UNPREFIXED, why=why))
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

    A row the engine will not read is set aside by the reader's own rule
    (``intake_cli.set_aside``) and named; one carrying no provider id raises
    the engine's refusal with that said after it, so the set is shown unread.
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
                # NOTHING WOULD NAME IT among the misses, so the set stays unread.
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
        position, one.artist or "no artist",
        one.title or "no title",
        f"{one.why} (track {one.ref}), so it was not asked of the library",
    )


def _decided(
    name: str, playlist_id: str, folder: str, wanted: tuple[tuple[int, match.Wanted], ...],
    withheld: int, row_of: Callable[[match.Wanted], tuple[str, str]],
    unread: tuple[Miss, ...] = (),
) -> SetRow:
    """The set with each track's collection row, distinct in set order, and every miss named."""
    ids: list[str] = []
    misses: list[Miss] = list(unread)
    for position, one in wanted:
        held, why = row_of(one)
        if held:
            ids.append(held)
        else:
            misses.append(Miss(position, one.artist, one.listed, why))
    members = tuple(dict.fromkeys(ids))
    return SetRow(
        name=name, playlist_id=playlist_id, folder=folder,
        action=CREATE if members else EMPTY,
        members=members,
        misses=tuple(sorted(misses, key=lambda miss: miss.position)),
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
    cfg: config.Config, declared: Any, *, remote: Any, found: Any,
    reading: Callable[[], AbstractContextManager[Any]],
) -> ParityPlan:
    """Every downloaded set on the account, decided against INSPIRATION and the library.

    ``remote`` is the account, ``found`` the catalogue for each set's tracks,
    and ``reading`` opens a read handle on the database. NO READ IS HELD
    ACROSS A PROVIDER CALL: the database is read for INSPIRATION, let go while
    the account is read, and read again only when a set has tracks to match.
    A taxonomy with no INSPIRATION folder, or two, refuses by the set
    playlist's own rule.
    """
    from cratekit.intake import set_playlist
    from cratekit.sync.playlists import taken_ids

    with reading() as db:
        folder_id, node = set_playlist.folder_for(db, declared)
        held = _held(db, folder_id)

    listed, rows = account_sets(remote, recorded_folders(cfg), taken_ids(cfg))
    named = Counter(name for _folder, _pid, name in listed)
    read: list[tuple[str, str, str, _Listed]] = []
    for folder, playlist_id, name in listed:
        if name in held:
            rows.append(SetRow(name, playlist_id, folder, SKIP))
            continue
        if named[name] > 1:
            why = (
                f"{named[name]} downloaded sets on the account carry this name "
                f"and INSPIRATION can hold one, so neither is written; rename "
                f"one on the account"
            )
            rows.append(SetRow(name, playlist_id, folder, TWICE, why=why))
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
            why = _none_read(listing)
            rows.append(SetRow(name, playlist_id, folder, UNREAD, withheld=listing.withheld, why=why))
            continue
        read.append((name, playlist_id, folder, listing))
    if read:
        with reading() as db:
            row_of = _Rows(cfg, db)
            rows.extend(
                _decided(
                    name, playlist_id, folder, listing.wanted, listing.withheld, row_of,
                    tuple(_unread_miss(place, one) for place, one in listing.unread),
                )
                for name, playlist_id, folder, listing in read
            )
    return ParityPlan(
        tree_id=node.id, folder_display=node.display, folder_id=folder_id,
        rows=tuple(sorted(rows, key=lambda row: (row.folder, row.name, row.playlist_id))),
    )


def again(cfg: config.Config, db: Any, declared: Any, approved: ParityPlan) -> ParityPlan:
    """The approved plan taken again on ``db``: INSPIRATION and the library read now.

    THE ACCOUNT IS NOT READ AGAIN: the write asks the library about exactly the
    tracks the approved plan names. A set skipped then whose INSPIRATION
    playlist has gone reads as a change rather than as nothing.
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

    A MEMBERSHIP THE PLAN DID NOT NAME IS REFUSED BY NAME FIRST, since it
    would be written unseen; any other change refuses as the plan being stale.
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


def write(db: Any, approved: ParityPlan) -> tuple[list[Wrote], bool]:
    """Make each planned playlist under INSPIRATION and add its members, pending on ``db``.

    INSIDE A CALLER'S SESSION, which commits or rolls back. The folder is made
    once, for the first set, when the plan read none.
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
    record: session.SessionRecord, wrote: Iterable[Wrote], approved: ParityPlan, cfg: config.Config
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
    order; one found by its name holds every planned row, whatever else.
    """
    for one in wrote:
        live = list(one.read_back)
        held = set(live)
        missing = [row for row in one.members if row not in held]
        exact = live == list(one.members)
        if missing or (one.created and not exact):
            planned = set(one.members)
            unnamed = [row for row in live if row not in planned]
            raise refuse(
                "session-committed-unverified",
                f"the INSPIRATION playlist {one.name!r} ({one.playlist_id}) read back "
                f"from the database holds {len(live)} live track(s): {len(missing)} of "
                f"the {len(one.members)} the plan named are not among them and "
                f"{len(unnamed)} it did not name are; the commit landed and this "
                f"answer cannot be vouched for",
                origin=_ORIGIN,
                detail={
                    "playlist_id": one.playlist_id, "planned": list(one.members), "read": live,
                    "missing": missing, "unnamed": unnamed,
                },
            )


def apply(cfg: config.Config, declared: Any, approved: ParityPlan) -> Applied:
    """Write the approved plan in a session of its own, on a handle opened to write.

    rekordbox must be closed. The plan is taken again on this handle and
    refused when it moved, the tree's convergence latch is asked, and then the
    session spine every database writer calls.
    """
    from cratekit.core import tree_registry

    watched = list(analysis_store.watch_roots(cfg))
    db = rb_writer.open_db(rb_writer.live_db_path(cfg), require_closed=True, cfg=cfg)
    try:
        assert_unchanged(approved, again(cfg, db, declared, approved))
        # THE TREE'S OWN LATCH FIRST, so a database restored out of band is
        # caught before this write's fingerprint overwrites the evidence.
        convergence.assert_tree_writable(cfg, db, approved.tree_id, tree_registry.read(cfg))
        wrote: list[Wrote] = []
        with (
            session.assert_gates(
                cfg, workflow=WORKFLOW, analysis_roots=watched, keep=session.Keep.RECORD
            ) as gates,
            rb_writer.commit_witness(db) as witness,
        ):
            from cratekit.write import trees

            record, capture = trees.attached_capture(gates, cfg, db)
            try:
                wrote, folder_created = write(db, approved)
                rb_writer.commit_guarded(db)
            except BaseException:
                trees.rollback_quietly(db)
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
    "CREATE", "EMPTY", "FOLDER_UNREAD", "NAMED_UNREAD", "RECORD_KEY", "SKIP", "TWICE",
    "UNPREFIXED", "UNREAD", "WORKFLOW", "Applied", "Miss", "ParityPlan", "SetRow", "Wrote",
    "account_sets", "again", "apply", "assert_read_back", "assert_unchanged", "plan",
    "recorded_folders", "sets_folder", "write",
]
