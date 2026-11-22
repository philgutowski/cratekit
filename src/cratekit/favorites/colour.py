"""The Pink colour: what it is, which rows carry it, and how a heart gets it (R-228, U153).

Pink is the operator's signal that a row is a favourite: the sweep reads it,
and the landing and the backfill write it on every heart they place. It is
**LOOKED UP BY NAME** inside the open that uses it, and **ONLY A ROW WITH NO
COLOUR IS COLOURED**, by the core writer's definition of unset: the track
colour policy is OWNED, so a colour a person chose is held, never overwritten.

Layer: modules. Writes go through ``rb_writer.write_metadata_field`` on the
caller's handle, inside the caller's commit.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from cratekit.core import rb_writer
from cratekit.core.cause import Scope, refuse
from cratekit.write import trees

#: The colour name rekordbox stores on ``djmdColor.Commnt`` for pink rows.
PINK_COLOUR_NAME = "Pink"

#: No live Pink row: the sweep refuses, a placement warns and colours nothing.
PINK_COLOUR_MISSING = "favorites-pink-colour-missing"

#: The column, and the owner the core writer registers for it at baseline.
COLUMN = "ColorID"
OWNER = rb_writer.TRACK_COLOR_POLICY.owner

_ORIGIN = ("favorites", "colour")


def pink_colour_id(db: Any) -> str:
    """The ColourID whose name is Pink inside an already open library, soft deleted rows skipped, or a refusal."""
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
    """Every live content id coloured pink in ``db``, ordered as the binding yields them."""
    pink = pink_colour_id(db)
    return tuple(
        str(row.ID)
        for row in db.get_content()
        if not trees.soft_delete_marker(row) and str(getattr(row, COLUMN, "") or "") == pink
    )


def is_uncoloured(value: Any) -> bool:
    """Whether a row's colour reads as unset, by the core writer's own definition."""
    return value in rb_writer.FIELD_EMPTIES[COLUMN]


def find_row(db: Any, content_id: str) -> Any | None:
    """The content row, a pending-insert instance the session holds first, else loaded.

    THE SESSION'S PENDING INSERTS FIRST, since a landing colours rows it made in
    this commit, which no query reaches until the flush. Only ``session.new``:
    a get by primary key already hands back a loaded instance, and walking the
    identity map made a large backfill quadratic.
    """
    wanted = str(content_id)
    session = getattr(db, "session", None)
    if session is not None:
        for row in getattr(session, "new", ()):
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
    """Each row by what its colour is now: unset, Pink, or somebody's, a row not found left out.

    READ LIVE ON THE PLANNING HANDLE, so the digest carries which rows a plan
    colours and an approval given before a row was coloured by hand is stale.
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
    """Colour each named row Pink, through the policy, and say which rows took it. DOES NOT COMMIT.

    A row not found, or whose colour is no longer unset, is left: the policy is
    OWNED, so the fill only rule is checked again here on the write path.
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
