"""The Pink colour: what it is, which rows carry it, and how a heart gets it (R-228, U153).

PINK IS THE OPERATOR'S STANDING SIGNAL that a row is a favourite. The sweep
(``favorites.cli``) reads it to find hearts to send to the account, and since
U153 the landing and ``crate favorites backfill`` write it onto every heart
they place, so the colour and All Favorites say the same thing. Before U153
nothing wrote it: R-424 chose the honest report for the sweep, and the
placement of U120 and U146 put a heart into its playlists and left the row
uncoloured, which is how the author's recent favourites landed grey.

**LOOKED UP BY NAME, NEVER HARD CODED.** rekordbox stores the colour's display
name on ``djmdColor.Commnt``, and the identifier is the library's, read inside
the open that will use it. A library with no live Pink row has no Pink to
write, and that is a named condition rather than a silent empty colour source.

**ONLY A ROW WITH NO COLOUR IS COLOURED.** The track colour policy in the core
writer is OWNED, which would let this module overwrite a colour a person chose.
It does not: the plan names only rows whose colour is unset, under the one
definition of unset the core writer keeps (``rb_writer.FIELD_EMPTIES``), and a
row carrying another colour is held and named, because a colour a person set
by hand is theirs and a heart is not a reason to take it. A row already Pink
is nothing to write.

Layer: modules. The write goes through ``rb_writer.write_metadata_field``
under the baseline ``track-color`` policy, on the caller's handle and inside
the caller's commit, as the memberships do.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from cratekit.core import rb_writer
from cratekit.core.cause import Scope, refuse
from cratekit.write import trees

#: The colour name rekordbox stores on ``djmdColor.Commnt`` for pink rows.
PINK_COLOUR_NAME = "Pink"

#: The refusal, and since U153 the warning, when the colour table has no live
#: Pink row: the sweep refuses, a placement warns and colours nothing.
PINK_COLOUR_MISSING = "favorites-pink-colour-missing"

#: The column, and the owner the core writer registers for it at baseline.
COLUMN = "ColorID"
OWNER = rb_writer.TRACK_COLOR_POLICY.owner

_ORIGIN = ("favorites", "colour")


def pink_colour_id(db: Any) -> str:
    """The ColourID whose name is Pink inside an already open library, or a refusal.

    Soft deleted colour rows are skipped through the one soft delete reader, as
    ``collection_export.read_tracks`` skips tombstoned content. No live Pink row
    is a named refusal rather than a silent empty colour source.
    """
    for row in db.get_color(Commnt=PINK_COLOUR_NAME):
        if trees.soft_delete_marker(row):
            continue
        return str(row.ID)
    raise refuse(
        PINK_COLOUR_MISSING,
        "the library's colour table has no live row named Pink, so this sweep "
        "cannot tell which rows are pink and would report complete over rows "
        "it never considered",
        steps=(
            "restore the Pink colour in rekordbox, or colour one row pink so "
            "the table carries it again",
        ),
        scope=Scope.RUN,
        origin=_ORIGIN,
    )


def pink_content_ids(db: Any) -> tuple[str, ...]:
    """Every live content id coloured pink in ``db``, ordered as the binding yields them.

    Soft deleted content rows are skipped through the same reader
    ``collection_export.read_tracks`` uses. The Pink ColourID is looked up in
    this same open, never hard coded.
    """
    pink = pink_colour_id(db)
    found: list[str] = []
    for row in db.get_content():
        if trees.soft_delete_marker(row):
            continue
        if str(getattr(row, COLUMN, "") or "") == pink:
            found.append(str(row.ID))
    return tuple(found)


def is_uncoloured(value: Any) -> bool:
    """Whether a row's colour reads as unset, by the core writer's own definition."""
    return value in rb_writer.FIELD_EMPTIES[COLUMN]


def find_row(db: Any, content_id: str) -> Any | None:
    """The content row, the instance the session already holds first, else loaded.

    THE SESSION'S OWN INSTANCE WINS, because a landing colours rows it made in
    this same commit, which the binding minted with a numeric identifier, and
    a lookup by the string form loads a second instance of the same row under
    a second key. Two instances of one row in one flush cannot be ordered by
    primary key and the commit fails inside the binding. So a row the session
    holds, new or loaded, is matched on the text of its identifier, and the
    query is asked only for a row the session has never seen.
    """
    wanted = str(content_id)
    session = getattr(db, "session", None)
    if session is not None:
        held = list(getattr(session, "new", ()))
        identity_map = getattr(session, "identity_map", None)
        if identity_map is not None:
            held.extend(identity_map.values())
        for row in held:
            table = getattr(getattr(row, "__table__", None), "name", "")
            if table == rb_writer.CONTENT_TABLE and str(getattr(row, "ID", "")) == wanted:
                return row
    return db.get_content(ID=wanted)


def colour_name(db: Any, colour_id: str) -> str:
    """The display name of a colour row, or its identifier when the table lacks it."""
    row = db.get_color(ID=str(colour_id))
    if row is None:
        return str(colour_id)
    return str(getattr(row, "Commnt", "") or colour_id)


@dataclass(frozen=True, slots=True)
class Held:
    """A row a placement would have coloured and did not, because a person already had."""

    content_id: str
    title: str
    colour: str

    def said(self) -> str:
        return f"{self.title or self.content_id} ({self.colour})"


@dataclass(frozen=True, slots=True)
class Sorted:
    """Rows to colour Pink, rows held with another colour, and rows Pink already."""

    to_colour: tuple[str, ...]
    held: tuple[Held, ...]
    already: tuple[str, ...]


def sort_rows(db: Any, pink: str, content_ids: Iterable[str]) -> Sorted:
    """Each row by what its colour is now: unset, Pink, or somebody's.

    READ LIVE ON THE PLANNING HANDLE, so a plan's digest carries which rows it
    would colour and an approval given before a row was coloured by hand is
    stale for it. A row the handle cannot find is not planned, since there is
    nothing to colour; the membership write names it on its own.
    """
    to_colour: list[str] = []
    held: list[Held] = []
    already: list[str] = []
    seen: set[str] = set()
    for content_id in content_ids:
        key = str(content_id)
        if key in seen:
            continue
        seen.add(key)
        row = find_row(db, key)
        if row is None:
            continue
        current = getattr(row, COLUMN, None)
        if is_uncoloured(current):
            to_colour.append(key)
        elif str(current) == pink:
            already.append(key)
        else:
            held.append(
                Held(
                    content_id=key,
                    title=str(getattr(row, "Title", "") or ""),
                    colour=colour_name(db, str(current)),
                )
            )
    return Sorted(to_colour=tuple(to_colour), held=tuple(held), already=tuple(already))


def write_pink(db: Any, pink: str, content_ids: Sequence[str]) -> tuple[str, ...]:
    """Colour each named row Pink, through the policy, and say which rows took it.

    DOES NOT COMMIT; the caller's guarded commit does. A row the handle cannot
    find is skipped, and a row whose colour is no longer unset is left as it
    is: the policy decision is OWNED, so this function checks the colour again
    rather than trusting a plan read on another handle, which is the one
    place the fill only rule is enforced on the write path itself.
    """
    written: list[str] = []
    for content_id in content_ids:
        row = find_row(db, str(content_id))
        if row is None or not is_uncoloured(getattr(row, COLUMN, None)):
            continue
        decision = rb_writer.write_metadata_field(row, OWNER, COLUMN, pink)
        if decision is rb_writer.Decision.WRITE:
            written.append(str(content_id))
    return tuple(written)


__all__ = [
    "COLUMN",
    "Held",
    "OWNER",
    "PINK_COLOUR_MISSING",
    "PINK_COLOUR_NAME",
    "Sorted",
    "colour_name",
    "find_row",
    "is_uncoloured",
    "pink_colour_id",
    "pink_content_ids",
    "sort_rows",
    "write_pink",
]
