"""Where a landed heart goes in the library: All Favorites and its quarter (U120).

A track the author hearts on the account is downloaded by the favourites
sync and lands in INBOX like any other file. Until this unit nothing in the
product put it where the source system did, into the one playlist every
favourite is in and into the playlist of the UTC quarter it was hearted in,
``Favorites / 2026-Q4``, so the genre Favorites of U119 had nothing new to
mirror. This engine is that placement, called by the native landing inside its
own commit and by ``crate favorites backfill`` for the hearts that landed
before it existed.

**ADD ONLY.** It adds a membership that is absent and never takes one away,
through the one writer that owns the "only when absent" rule, so a heart
placed twice is placed once. A heart's quarter playlist is created under the
folder that holds All Favorites when it is absent, by its quarter's name, the
source system's own, and an undated heart goes to ``Undated``. Nothing here
moves a heart between quarters: an undated heart that later gets a date stays
where it was put, which the record says.

**THE SOURCE IS NAMED ONCE AND READ, NEVER MADE.** The playlist a heart joins
is the one the taxonomy's playlist class mirrors, All Favorites in the shipped
template, read the way U119's engine reads it: the one live PLAIN playlist of
that name anywhere in the library. A library with none or with two has no
answer to "where do the favourites live", and this engine refuses under
U119's reason rather than inventing a playlist, so a landing that cannot place
its hearts says so and lands them, and the backfill places them once the
playlist exists. Where the class is not declared, the outbound default names
it, since both spell the same playlist and a library that predates the class
still has one. Unlike U119's engine an EMPTY source is a fine source here,
because this engine only adds to it.

**THE QUARTER IS READ FROM THE JOB, NEVER FROM THE ACCOUNT AGAIN.** The hearts
listing freezes each heart's date onto its row (``intake.cli.HEARTED``), and
the landing reads the date from there, which is U113's rule for what a
playlist asked for. The backfill reads the same key and asks the account only
for a heart listed by a build before the key existed.

Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Mapping, Sequence

from cratekit.core import rb_writer, taxonomy
from cratekit.core.cause import Remedy, refuse
from cratekit.favorites import placeholders
from cratekit.modules.outbound import source as outbound_source
from cratekit.write import genre_favorites

#: The key a landing's and the backfill's commit are recorded under on the
#: session, as rows created, beside the intake tree's own entry. Not a tree id:
#: the Favorites folder is nobody's registered tree.
RECORD_KEY = "favorites"

#: What the landing's session record carries about the hearts it placed.
PLACED_KEY = "favorites_placed"

#: The reason this engine refuses with when the source is absent or doubled,
#: U119's, because it is the same question with the same answer.
SOURCE_MISSING = genre_favorites.SOURCE_MISSING

_ORIGIN = ("favorites", "placement")


def source_name(declared: taxonomy.Taxonomy) -> str:
    """The playlist every favourite is in: the class's, else the outbound default.

    ONE CHOOSER FOR THE LANDING AND THE BACKFILL, so the two cannot place a
    heart into two playlists. The taxonomy's playlist class is the declaration
    U119 made of which playlist is the favourites; the outbound default is the
    same name a library that predates the class already carries.
    """
    sub = genre_favorites.favorites_class(declared)
    if sub is not None and sub.signal_playlist:
        return sub.signal_playlist
    return outbound_source.DEFAULT_FAVORITES_PLAYLIST


# ---------------------------------------------------------------------------
# The home: the source playlist, its folder, and the quarters already there
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Home:
    """The one source playlist, the folder it sits in, and the quarter playlists there now."""

    source_name: str
    source_id: str
    #: The folder's row, or empty when the source sits at the playlist root,
    #: in which case a quarter playlist is created beside it at the root.
    folder_id: str
    folder_name: str
    #: Every live plain playlist under the folder, by name, quarter named or not.
    present: Mapping[str, str]

    def identity(self) -> dict[str, Any]:
        """What a plan's digest covers of the home: the rows, never the names alone."""
        return {"source": self.source_id, "folder": self.folder_id}


def _live_plain(rows: Iterable[Any]) -> list[Any]:
    return [
        row
        for row in rows
        if int(getattr(row, "Attribute", -1) or 0) == 0 and not rb_writer.node_removed(row)
    ]


def _under(db: Any, parent_id: str) -> dict[str, str]:
    """Every live plain playlist directly under ``parent_id``, by name, first of a name wins."""
    found: dict[str, str] = {}
    at_root = parent_id in rb_writer.ROOT_PARENT_SENTINELS
    for row in _live_plain(list(db.get_playlist())):
        held = str(getattr(row, "ParentID", "") or "")
        here = held in rb_writer.ROOT_PARENT_SENTINELS if at_root else held == parent_id
        if here:
            found.setdefault(str(row.Name), str(row.ID))
    return found


def resolve_home(db: Any, name: str) -> Home:
    """The home of the favourites, or the refusal that says there is none or two.

    THE SAME QUESTION U119's ENGINE ASKS, with one answer fewer: an empty
    source is a source here, since nothing is derived from it and a heart is
    only added. A folder of the name is not it, a smart playlist of the name
    is not it, and a removed one is not there.
    """
    live = _live_plain(list(db.get_playlist(Name=name)))
    if len(live) != 1:
        count = "no live playlist" if not live else f"{len(live)} live playlists"
        raise refuse(
            SOURCE_MISSING,
            f"this library holds {count} named {name!r}, which is where a landed heart "
            f"goes, so no heart was placed; make the one playlist in rekordbox, or name "
            f"the one that holds the favourites in the class's signal_playlist",
            remedy=Remedy.FIX_CONFIG_VALUES,
            origin=_ORIGIN,
            detail={"playlist": name, "ids": [str(row.ID) for row in live]},
        )
    source = live[0]
    parent_id = str(getattr(source, "ParentID", "") or "")
    folder = None if parent_id in rb_writer.ROOT_PARENT_SENTINELS else db.get_playlist(ID=parent_id)
    return Home(
        source_name=name,
        source_id=str(source.ID),
        folder_id="" if folder is None else str(folder.ID),
        folder_name="" if folder is None else str(getattr(folder, "Name", "") or ""),
        present=_under(db, parent_id),
    )


def members(db: Any, playlist_id: str) -> frozenset[str]:
    """The content ids a playlist holds live, the soft deleted rows left out (R-758)."""
    return frozenset(
        str(song.ContentID)
        for song in db.get_playlist_songs(PlaylistID=str(playlist_id))
        if not rb_writer.membership_removed(song)
    )


def removed_members(db: Any, playlist_id: str) -> frozenset[str]:
    """The content ids whose membership in a playlist rekordbox marked REMOVED.

    A membership that exists as removed is a track somebody took out of the
    playlist by hand, and for All Favorites that is the author un-hearting a
    track in the library. The backfill (U120) reads this so it never puts a
    heart back that the author took back, where a landing of a new heart has
    no such row to read.
    """
    return frozenset(
        str(song.ContentID)
        for song in db.get_playlist_songs(PlaylistID=str(playlist_id))
        if rb_writer.membership_removed(song)
    )


# ---------------------------------------------------------------------------
# The plan over content rows, for the backfill
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Placement:
    """One content row and the quarter it goes to, with what it already has."""

    content_id: str
    quarter: str
    title: str = ""
    into_source: bool = True
    into_quarter: bool = True

    @property
    def adds(self) -> int:
        return int(self.into_source) + int(self.into_quarter)


@dataclass(frozen=True, slots=True)
class PlacementPlan:
    """Every heart placed against one home, read on one handle."""

    home: Home
    placements: tuple[Placement, ...]

    @property
    def adds(self) -> int:
        return sum(one.adds for one in self.placements)

    @property
    def creates(self) -> tuple[str, ...]:
        """The quarter playlists the write would make, in the order first needed."""
        made: list[str] = []
        for one in self.placements:
            if one.into_quarter and one.quarter not in self.home.present and one.quarter not in made:
                made.append(one.quarter)
        return tuple(made)

    @property
    def writes(self) -> bool:
        return self.adds > 0

    def identity(self) -> dict[str, Any]:
        """What the digest covers: the home's rows, each quarter's row or its making, each heart's target state.

        THE QUARTER ROWS ARE DIGESTED, found or to be made, so a quarter
        playlist deleted between the plan and the write is another plan and
        not a playlist the write makes without having shown it.
        """
        return {
            "kind": "favorites-placement",
            **self.home.identity(),
            "quarters": {
                quarter: self.home.present.get(quarter, "")
                for quarter in sorted({one.quarter for one in self.placements})
            },
            "placements": [
                {
                    "row": one.content_id,
                    "quarter": one.quarter,
                    "source": one.into_source,
                    "into_quarter": one.into_quarter,
                }
                for one in self.placements
            ],
        }


def plan_placements(
    db: Any, home: Home, hearts: Sequence[tuple[str, datetime | None, str]]
) -> PlacementPlan:
    """Each heart's placement against what the home holds live.

    ``hearts`` are ``(content id, when hearted or None, title)``, a row named
    twice folding to its first mention. What each row already has is read
    live, so a plan over a library already placed writes nothing and says so.
    """
    in_source = members(db, home.source_id)
    in_quarter: dict[str, frozenset[str]] = {}
    seen: set[str] = set()
    placements: list[Placement] = []
    for content_id, hearted, title in hearts:
        key = str(content_id)
        if key in seen:
            continue
        seen.add(key)
        quarter = placeholders.quarter_label(hearted)
        if quarter not in in_quarter:
            held = home.present.get(quarter)
            in_quarter[quarter] = members(db, held) if held else frozenset()
        placements.append(
            Placement(
                content_id=key,
                quarter=quarter,
                title=title,
                into_source=key not in in_source,
                into_quarter=key not in in_quarter[quarter],
            )
        )
    return PlacementPlan(home=home, placements=tuple(placements))


# ---------------------------------------------------------------------------
# The write, on the caller's handle, inside the caller's commit
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Placed:
    """What one placement wrote: memberships into the source and into each quarter."""

    source_name: str
    source_id: str
    added_source: int
    #: Each quarter playlist written to: its name, its row, and the memberships added.
    quarters: tuple[tuple[str, str, int], ...]
    #: The quarter playlists this write made, by name.
    created: tuple[str, ...]

    @property
    def added(self) -> int:
        return self.added_source + sum(count for _name, _row, count in self.quarters)

    def to_json(self) -> dict[str, Any]:
        return {
            "source": self.source_name,
            "source_id": self.source_id,
            "added_source": self.added_source,
            "quarters": [
                {"name": name, "id": row, "added": count} for name, row, count in self.quarters
            ],
            "created": list(self.created),
        }


def _live_row(db: Any, playlist_id: str, what: str) -> Any:
    row = db.get_playlist(ID=playlist_id)
    if row is None or rb_writer.node_removed(row):
        raise refuse(
            "decision-stale",
            f"{what} (row {playlist_id}) is not live any more, so no heart was placed",
            origin=_ORIGIN,
            detail={"playlist": playlist_id},
        )
    return row


def _quarter_row(db: Any, name: str, parent: Any) -> tuple[Any, bool]:
    """The quarter's playlist under the folder, found live by name, else made.

    NOT :func:`rb_writer.ensure_playlist`, which reads no soft delete marker
    and takes no root: a quarter playlist rekordbox removed would be found and
    written to, a row a person cannot see (R-758), and a source at the root
    has no parent row to scope by. The genre Favorites writer reads the same
    way for the same reason.
    """
    parent_id = "" if parent is None else str(parent.ID)
    for row in _live_plain(list(db.get_playlist(Name=name))):
        held = str(getattr(row, "ParentID", "") or "")
        if parent is None and held in rb_writer.ROOT_PARENT_SENTINELS:
            return row, False
        if parent is not None and held == parent_id:
            return row, False
    return db.create_playlist(name, parent=parent), True


def place(db: Any, home: Home, pairs: Sequence[tuple[str, str | None]]) -> Placed:
    """Add each ``(content id, quarter name)`` to the source and to its quarter.

    A PAIR WITH NO QUARTER JOINS THE SOURCE ALONE: a heart whose job froze no
    date key is a heart all the same, and its quarter is the backfill's to
    read from the account rather than a guess made here.

    ON THE CALLER'S HANDLE AND INSIDE THE CALLER'S COMMIT, so the landing's
    rows, its INBOX playlists and its hearts are one all or nothing write, and
    the backfill's own session owns its commit. The source row is read again
    by identifier here, since a plan was read on another handle, and a quarter
    playlist is found live by name under the folder or made. The memberships
    go through :func:`rb_writer.add_memberships`, which owns "only when
    absent", so the same heart twice is one membership.
    """
    source = _live_row(db, home.source_id, f"the playlist {home.source_name!r}")
    parent = None
    if home.folder_id:
        parent = _live_row(db, home.folder_id, f"the folder {home.folder_name!r}")
    ordered = [str(content_id) for content_id, _quarter in pairs]
    added_source = len(rb_writer.add_memberships(db, source, ordered))
    by_quarter: dict[str, list[str]] = {}
    for content_id, quarter in pairs:
        if quarter:
            by_quarter.setdefault(str(quarter), []).append(str(content_id))
    written: list[tuple[str, str, int]] = []
    created: list[str] = []
    for quarter, ids in by_quarter.items():
        row, made = _quarter_row(db, quarter, parent)
        if made:
            created.append(quarter)
        count = len(rb_writer.add_memberships(db, row, ids))
        written.append((quarter, str(row.ID), count))
    return Placed(
        source_name=home.source_name,
        source_id=str(source.ID),
        added_source=added_source,
        quarters=tuple(written),
        created=tuple(created),
    )


__all__ = [
    "Home",
    "PLACED_KEY",
    "Placed",
    "Placement",
    "PlacementPlan",
    "RECORD_KEY",
    "SOURCE_MISSING",
    "members",
    "place",
    "removed_members",
    "plan_placements",
    "resolve_home",
    "source_name",
]
