"""Where a landed heart goes in the library: All Favorites and its month (U120, U145).

This engine is the placement, called by the native landing inside its own
commit and by ``crate favorites backfill``. A heart joins the one playlist
every favourite is in and the playlist of the UTC month it was hearted in,
``Favorites / 2026-10`` (U145), or ``Undated`` with no date. An owned heart
joins too (U146). The quarters already there are ``crate favorites split``'s.

**ADD ONLY.** A membership that is absent is added, through the one writer that
owns "only when absent", and none is ever taken away or moved between months:
an undated heart that later gets a date stays where it was put.

**THE SOURCE IS NAMED ONCE AND READ, NEVER MADE**: the one live PLAIN playlist
the taxonomy's playlist class mirrors, else the outbound default. A library
with none or two refuses under U119's reason rather than inventing one, so a
landing says so and lands its hearts. An EMPTY source is a fine source here.

**THE MONTH IS READ FROM THE JOB** (``intake.cli.HEARTED``); the backfill asks
the account only for a heart listed before the key existed.

**A MONTH IS MADE IN ITS PLACE (U180)**, its newest first slot, by
:func:`month_row`, so the folder keeps the order ``crate favorites order``
puts it in.

**A PLACED HEART IS COLOURED PINK (U153)** in the same commit, the author's
signal that a row is a favourite. Only a row with no colour is coloured: one a
person coloured otherwise is held and named. A library with no live Pink row
places the memberships, colours nothing and says so. See ``favorites.colour``.

Layer: modules.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from typing import Any, Iterable, Mapping, Sequence

from cratekit.core import foreign_tree, rb_writer, taxonomy
from cratekit.core.cause import CratekitError, Remedy, refuse
from cratekit.favorites import colour, placeholders, spine
from cratekit.write import genre_favorites

#: The key every favourites commit is recorded under on the session.
RECORD_KEY = spine.RECORD_KEY

#: What the landing's session record carries about the hearts it placed.
PLACED_KEY = "favorites_placed"

#: The refusal when the source is absent or doubled, U119's: the same question.
SOURCE_MISSING = genre_favorites.SOURCE_MISSING

_ORIGIN = ("favorites", "placement")


def source_name(declared: taxonomy.Taxonomy) -> str:
    """The playlist every favourite is in: the class's, else the outbound default.

    ONE CHOOSER FOR THE LANDING AND THE BACKFILL, so the two cannot place a
    heart into two playlists.
    """
    from cratekit.modules.outbound import source as outbound_source

    sub = genre_favorites.favorites_class(declared)
    if sub is not None and sub.signal_playlist:
        return sub.signal_playlist
    return outbound_source.DEFAULT_FAVORITES_PLAYLIST


@dataclass(frozen=True, slots=True)
class Home:
    """The one source playlist, the folder it sits in, and the playlists there now."""

    source_name: str
    source_id: str
    #: The folder's row, or empty at the playlist root, where a month is made beside it.
    folder_id: str
    folder_name: str
    #: Every live plain playlist under the folder, by name, month named or not.
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

    U119's question, an empty source admitted. A folder, a smart playlist or a
    removed playlist of the name is not it.
    """
    # A playlist another app pushed into its own folder is not the home (U185).
    live = foreign_tree.outside(
        _live_plain(list(db.get_playlist(Name=name))), list(db.get_playlist())
    )
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
    return genre_favorites.live_members(db, playlist_id)


def filed(db: Any, home: Home) -> frozenset[str]:
    """The content ids a dated playlist beside the source holds live: a month, Undated, a quarter.

    WHAT "ALREADY HAS ITS MONTH" MEANS (U146), by :func:`placeholders.is_filing`,
    so a heart filed in Undated or moved by hand is not given a second month. A
    playlist of any other name is not read, which matters at the playlist root.
    """
    held: set[str] = set()
    for name, row in home.present.items():
        if row != home.source_id and placeholders.is_filing(name):
            held |= members(db, row)
    return frozenset(held)


def members_marked_removed(db: Any, playlist_id: str) -> frozenset[str]:
    """The content ids whose membership in a playlist rekordbox marked REMOVED.

    A READER, NAMED SO IT READS AS ONE: no function under ``favorites/`` opens
    with ``remove``. For All Favorites a removed membership is the author
    un-hearting a track in the library, which the backfill never puts back.
    THE LANDING DOES NOT READ IT (U146): a heart the pass still found on the
    account joins again.
    """
    return frozenset(
        str(song.ContentID)
        for song in db.get_playlist_songs(PlaylistID=str(playlist_id))
        if rb_writer.membership_removed(song)
    )


@dataclass(frozen=True, slots=True)
class Placement:
    """One content row and the month it goes to, with what it already has."""

    content_id: str
    month: str
    title: str = ""
    into_source: bool = True
    into_month: bool = True
    #: Whether the row carries no colour and takes Pink with it (U153).
    into_colour: bool = False

    @property
    def adds(self) -> int:
        """Memberships, and only memberships: a colour is counted apart."""
        return int(self.into_source) + int(self.into_month)


@dataclass(frozen=True, slots=True)
class Recolour:
    """A row already placed that carries no colour, coloured and nothing else (U153)."""

    content_id: str
    title: str = ""


@dataclass(frozen=True, slots=True)
class PlacementPlan:
    """Every heart placed against one home, read on one handle, and the colour each takes."""

    home: Home
    placements: tuple[Placement, ...]
    #: The library's Pink row, or empty with ``colour_skipped`` saying why.
    pink: str = ""
    colour_skipped: str = ""
    #: Rows placed already that take Pink and no membership, the backfill's.
    recolour: tuple[Recolour, ...] = ()
    #: Rows a person coloured otherwise, named and left.
    held: tuple[colour.Held, ...] = ()

    @property
    def adds(self) -> int:
        return sum(one.adds for one in self.placements)

    @property
    def to_colour(self) -> tuple[str, ...]:
        """Every row the write colours Pink, the placed hearts first, then the recolours."""
        if not self.pink:
            return ()
        rows = [one.content_id for one in self.placements if one.into_colour]
        rows.extend(one.content_id for one in self.recolour)
        return tuple(rows)

    @property
    def colours(self) -> int:
        return len(self.to_colour)

    @property
    def creates(self) -> tuple[str, ...]:
        """The month playlists the write would make, in the order first needed."""
        wanted = (one.month for one in self.placements if one.into_month)
        return tuple(dict.fromkeys(month for month in wanted if month not in self.home.present))

    @property
    def writes(self) -> bool:
        return self.adds > 0 or self.colours > 0

    def identity(self) -> dict[str, Any]:
        """What the digest covers: the home, each month's row, each heart's target, each colour.

        THE MONTH ROWS, found or to be made, so a month deleted in between is
        another plan. THE PINK ROW AND THE ROWS TO COLOUR (U153), so a row
        coloured by hand in between is another plan.
        """
        return {
            "kind": "favorites-placement",
            **self.home.identity(),
            "months": {
                month: self.home.present.get(month, "")
                for month in sorted({one.month for one in self.placements})
            },
            "placements": [
                {
                    "row": one.content_id,
                    "month": one.month,
                    "source": one.into_source,
                    "into_month": one.into_month,
                    "colour": one.into_colour,
                }
                for one in self.placements
            ],
            "pink": self.pink,
            "recolour": [one.content_id for one in self.recolour],
        }


def read_pink(db: Any) -> tuple[str, str]:
    """The Pink row's identifier and no message, or no identifier and why.

    THE ONE REFUSAL A PLACEMENT ABSORBS: no live Pink row, so an acquisition
    never stops over a colour table. Anything else raised is the caller's.
    """
    try:
        return colour.pink_colour_id(db), ""
    except CratekitError as exc:
        if exc.cause.reason != colour.PINK_COLOUR_MISSING:
            raise
        return "", exc.cause.message


def plan_placements(
    db: Any,
    home: Home,
    hearts: Sequence[tuple[str, datetime | None, str]],
    *,
    recolour: Sequence[tuple[str, str]] = (),
) -> PlacementPlan:
    """Each heart's placement against what the home holds live, and the colour it takes.

    ``hearts`` are ``(content id, when hearted or None, title)``, a row named
    twice folding to its first mention. ``recolour`` are ``(content id, title)``
    rows placed already: one with no colour takes Pink and no membership, one
    with another colour is held.
    """
    in_source = members(db, home.source_id)
    in_month: dict[str, frozenset[str]] = {}
    seen: set[str] = set()
    placements: list[Placement] = []
    for content_id, hearted, title in hearts:
        key = str(content_id)
        if key in seen:
            continue
        seen.add(key)
        month = placeholders.month_label(hearted)
        if month not in in_month:
            held = home.present.get(month)
            in_month[month] = members(db, held) if held else frozenset()
        placements.append(
            Placement(
                content_id=key,
                month=month,
                title=title,
                into_source=key not in in_source,
                into_month=key not in in_month[month],
            )
        )
    pink, skipped = read_pink(db)
    if not pink:
        return PlacementPlan(home=home, placements=tuple(placements), colour_skipped=skipped)
    titles = {str(content_id): title for content_id, title in recolour}
    sorted_rows = colour.sort_rows(
        db, pink, [*(one.content_id for one in placements), *titles]
    )
    takes = frozenset(sorted_rows.to_colour)
    placements = [replace(one, into_colour=one.content_id in takes) for one in placements]
    return PlacementPlan(
        home=home,
        placements=tuple(placements),
        pink=pink,
        recolour=tuple(
            Recolour(content_id=row, title=titles[row])
            for row in sorted_rows.to_colour
            if row in titles and row not in seen
        ),
        held=sorted_rows.held,
    )


@dataclass(frozen=True, slots=True)
class Placed:
    """What one placement wrote: memberships into the source and into each month."""

    source_name: str
    source_id: str
    added_source: int
    #: Each month playlist written to: its name, its row, and the memberships added.
    months: tuple[tuple[str, str, int], ...]
    #: The month playlists this write made, by name.
    created: tuple[str, ...]
    #: The rows this write coloured Pink (U153).
    coloured: tuple[str, ...] = ()
    #: The rows a person coloured otherwise, named and left (U153).
    held: tuple[colour.Held, ...] = ()
    #: Why no row was coloured, when the colour table has no live Pink row (U153).
    colour_skipped: str = ""

    @property
    def added(self) -> int:
        return self.added_source + sum(count for _name, _row, count in self.months)

    def said(self) -> str:
        """The placement as one clause a person reads, the one wording every verb uses."""
        months = ", ".join(
            f"{name}{' (made)' if name in self.created else ''}" for name, _row, _n in self.months
        )
        said = (
            f"{self.added} membership(s) placed: {self.added_source} into "
            f"{self.source_name!r} and the rest into {months}"
        )
        return f"{said}; {len(self.coloured)} row(s) coloured {colour.PINK_COLOUR_NAME}"

    def to_json(self) -> dict[str, Any]:
        return {
            "source": self.source_name,
            "source_id": self.source_id,
            "added_source": self.added_source,
            "months": [
                {"name": name, "id": row, "added": count} for name, row, count in self.months
            ],
            "created": list(self.created),
            "coloured": list(self.coloured),
            "held": [{"row": one.content_id, "title": one.title, "colour": one.colour} for one in self.held],
            "colour_skipped": self.colour_skipped,
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


def seq_of(row: Any) -> int:
    """A row's position among its siblings."""
    return int(getattr(row, "Seq", 0) or 0)


def _shown_at(row: Any) -> tuple[int, str, str]:
    """The order rekordbox shows siblings in, by position, ties read by name as ``organize`` reads them."""
    return (seq_of(row), str(getattr(row, "Name", "") or ""), str(getattr(row, "ID", "")))


def children(db: Any, folder_id: str) -> list[Any]:
    """Every live child of a folder, of any kind, in the order rekordbox shows them, none soft deleted."""
    rows = [
        row
        for row in db.get_playlist(ParentID=str(folder_id))
        if not rb_writer.node_removed(row)
    ]
    return sorted(rows, key=_shown_at)


def rank(row: Any, source_id: str) -> tuple[int, int]:
    """Where a child of the home's folder reads, by :func:`placeholders.folder_rank`."""
    return placeholders.folder_rank(
        str(getattr(row, "Name", "") or ""),
        source=str(row.ID) == str(source_id),
        plain=int(getattr(row, "Attribute", -1) or 0) == 0,
    )


def slots(rows: Sequence[Any]) -> tuple[int, ...]:
    """The positions these rows hold between them, sorted, two that share one lifted apart.

    THE ROWS' OWN, NOT A COUNT FROM 1 (U180): how the live library numbers a
    folder with removed children was never measured, so an order gives the same
    set out again, a shared one lifted past the last so it reads one way.
    """
    given: list[int] = []
    for value in sorted(seq_of(row) for row in rows):
        given.append(value if not given or value > given[-1] else given[-1] + 1)
    return tuple(given)


def seat(db: Any, ordered: Sequence[Any], *, when: datetime) -> tuple[str, ...]:
    """Give ``ordered`` the positions they hold between them, in this order. Answers the rows moved.

    ONLY A ROW WHOSE POSITION CHANGES IS WRITTEN, ``Seq`` as the binding's move
    writes it and ``updated_at`` with tracking off; no row outside ``ordered``
    is touched. DOES NOT COMMIT.
    """
    moved: list[str] = []
    for row, slot in zip(ordered, slots(ordered)):
        if seq_of(row) == slot:
            continue
        row.Seq = slot
        with db.registry.disabled():
            row.updated_at = when
        moved.append(str(row.ID))
    return tuple(moved)


def _seat_new(db: Any, made: Any, folder_id: str, source_id: str) -> tuple[str, ...]:
    """Move a month just made from the end of the folder to its newest first slot.

    Before the first live child below All Favorites that ranks after it, so a
    landing never makes the folder read less in order than it found it.
    """
    db.session.flush()
    others = [row for row in children(db, folder_id) if str(row.ID) != str(made.ID)]
    mine = rank(made, source_id)
    floor = next((n + 1 for n, row in enumerate(others) if str(row.ID) == str(source_id)), 0)
    at = next(
        (n for n, row in enumerate(others) if n >= floor and rank(row, source_id) > mine),
        len(others),
    )
    return seat(db, [*others[:at], made, *others[at:]], when=datetime.now())


def month_row(db: Any, name: str, parent: Any, *, source_id: str) -> tuple[Any, bool]:
    """The month's playlist under the folder, found live by name, else made in its slot.

    PUBLIC so the split and a landing agree on which row a month is. NOT
    :func:`rb_writer.ensure_playlist`, which reads no soft delete marker and
    takes no root (R-758). MADE IN ITS NEWEST FIRST SLOT under a folder (U180),
    ``source_id`` reading first; at the playlist root, which is every
    playlist's, at the end.
    """
    parent_id = "" if parent is None else str(parent.ID)
    for row in _live_plain(list(db.get_playlist(Name=name))):
        held = str(getattr(row, "ParentID", "") or "")
        if parent is None and held in rb_writer.ROOT_PARENT_SENTINELS:
            return row, False
        if parent is not None and held == parent_id:
            return row, False
    made = db.create_playlist(name, parent=parent)
    if parent is not None:
        _seat_new(db, made, parent_id, source_id)
    return made, True


def place(
    db: Any,
    home: Home,
    pairs: Sequence[tuple[str, str | None]],
    *,
    pink: str = "",
    to_colour: Sequence[str] = (),
    held: Sequence[colour.Held] = (),
    colour_skipped: str = "",
) -> Placed:
    """Add each ``(content id, month name)`` to the source and to its month, and colour ``to_colour`` Pink.

    A PAIR WITH NO MONTH JOINS THE SOURCE ALONE, its month the backfill's to
    read. ON THE CALLER'S HANDLE AND INSIDE THE CALLER'S COMMIT, so a landing is
    one all or nothing write; the source and folder are read again by
    identifier, since the plan was read on another handle. The memberships go
    through :func:`rb_writer.add_memberships`, which owns "only when absent",
    and the colour through :func:`colour.write_pink`, which owns "only when
    unset"; with no ``pink`` nothing is coloured.
    """
    source = _live_row(db, home.source_id, f"the playlist {home.source_name!r}")
    parent = None
    if home.folder_id:
        parent = _live_row(db, home.folder_id, f"the folder {home.folder_name!r}")
    ordered = [str(content_id) for content_id, _month in pairs]
    added_source = len(rb_writer.add_memberships(db, source, ordered))
    by_month: dict[str, list[str]] = {}
    for content_id, month in pairs:
        if month:
            by_month.setdefault(str(month), []).append(str(content_id))
    written: list[tuple[str, str, int]] = []
    created: list[str] = []
    for month, ids in by_month.items():
        row, made = month_row(db, month, parent, source_id=home.source_id)
        if made:
            created.append(month)
        count = len(rb_writer.add_memberships(db, row, ids))
        written.append((month, str(row.ID), count))
    coloured: tuple[str, ...] = ()
    if pink and to_colour:
        coloured = colour.write_pink(db, pink, [str(row) for row in to_colour])
    return Placed(
        source_name=home.source_name,
        source_id=str(source.ID),
        added_source=added_source,
        months=tuple(written),
        created=tuple(created),
        coloured=coloured,
        held=tuple(held),
        colour_skipped=colour_skipped,
    )


__all__ = [
    "Home",
    "PLACED_KEY",
    "Placed",
    "Placement",
    "PlacementPlan",
    "RECORD_KEY",
    "Recolour",
    "SOURCE_MISSING",
    "children",
    "filed",
    "members",
    "month_row",
    "place",
    "members_marked_removed",
    "plan_placements",
    "rank",
    "read_pink",
    "resolve_home",
    "seat",
    "seq_of",
    "slots",
    "source_name",
]
