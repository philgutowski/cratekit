"""Another app's folder at the top of rekordbox's tree, left exactly as it is (U185).

DEADCA7 pushes its playlists into one folder named ``DEADCA7`` at the top of
the playlist tree. Neither tool undoes the other's work, and this module is
the one place that rule is spelled.

A foreign root is a folder directly under the playlist root whose name is
exactly one of :data:`FOREIGN_ROOT_NAMES`; everything under it is foreign. A
namesake further down, or a plain playlist of the name at the root, is not.

:func:`read` takes the folder, its playlists and their memberships from SQL
when :func:`rb_writer.open_db` opens a handle, and
:func:`rb_writer.commit_guarded` refuses any commit that would change them,
asked two ways: :func:`pending_touches` reads the pending objects and
:func:`differences` rereads SQL, which sees a flushed write and raw SQL. The
root row is held whole, its position included.

Layer: infrastructure.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from cratekit.core import taxonomy

#: The top level folder names another app owns, matched whole and by case.
FOREIGN_ROOT_NAMES: frozenset[str] = taxonomy.FOREIGN_ROOT_NAMES

#: The app each foreign root belongs to, for the one line a report gives it.
OWNER = "DEADCA7"

#: What a report says of a foreign root, beside its name.
LEFT_AS_IT_IS = "another app's folder, left exactly as it is and not counted as yours"

#: Table names, not imported, since the writer this guards reads this module.
_PLAYLISTS = "djmdPlaylist"
_MEMBERSHIPS = "djmdSongPlaylist"

#: How many identifiers one ``IN`` clause binds, well under SQLite's limit.
_CHUNK = 400


def _root_parents() -> tuple[str, ...]:
    from cratekit.core import rb_writer

    return rb_writer.ROOT_PARENT_SENTINELS


def is_foreign_root(name: Any, parent_id: Any, attribute: Any) -> bool:
    """Whether one node is a foreign root: a folder at the top named for another app."""
    try:
        folder = int(attribute if attribute is not None else -1) == 1
    except (TypeError, ValueError):
        folder = False
    parent = "" if parent_id is None else str(parent_id)
    return folder and str(name) in FOREIGN_ROOT_NAMES and parent in _root_parents()


def ids_of(nodes: Iterable[tuple[Any, Any, Any, Any]]) -> tuple[frozenset[str], frozenset[str]]:
    """``(roots, every foreign node)`` from ``(ID, Name, ParentID, Attribute)`` rows.

    Pure. A node is foreign through a chain of parents ending at a foreign
    root; a cycle ends the walk rather than looping.
    """
    rows = [tuple(node) for node in nodes]
    roots = frozenset(str(row[0]) for row in rows if is_foreign_root(row[1], row[2], row[3]))
    children: dict[str, list[str]] = {}
    for row in rows:
        children.setdefault("" if row[2] is None else str(row[2]), []).append(str(row[0]))
    seen: set[str] = set()
    queue = list(roots)
    while queue:
        node = queue.pop()
        if node in seen:
            continue
        seen.add(node)
        queue.extend(children.get(node, ()))
    return roots, frozenset(seen)


def _fields(row: Any) -> tuple[Any, Any, Any, Any]:
    return tuple(getattr(row, name, None) for name in ("ID", "Name", "ParentID", "Attribute"))


def node_ids(rows: Iterable[Any]) -> frozenset[str]:
    """Every foreign node among playlist rows read through the binding."""
    return ids_of(_fields(row) for row in rows)[1]


def outside(rows: Iterable[Any], every_row: Iterable[Any]) -> list[Any]:
    """``rows`` without foreign nodes, judged against ``every_row``, the whole table."""
    foreign = node_ids(every_row)
    return [row for row in rows if str(getattr(row, "ID", "")) not in foreign]


def roots_in(rows: Iterable[Any]) -> list[Any]:
    """The foreign roots among playlist rows read through the binding."""
    return [row for row in rows if is_foreign_root(*_fields(row)[1:])]


@dataclass(frozen=True)
class Reading:
    """The foreign subtree as SQL holds it: whole rows by identifier, with their columns."""

    roots: frozenset[str]
    playlists: Mapping[str, tuple]
    memberships: Mapping[str, tuple]
    playlist_columns: tuple[str, ...]
    membership_columns: tuple[str, ...]

    @property
    def ids(self) -> frozenset[str]:
        return frozenset(self.playlists)


def read(session: Any) -> Reading:
    """Read the foreign subtree from SQL, with no object mapper in between."""
    from sqlalchemy import text

    result = session.execute(text(f"SELECT * FROM {_PLAYLISTS}"))
    p_cols = tuple(result.keys())
    at = {name: p_cols.index(name) for name in ("ID", "Name", "ParentID", "Attribute")}
    rows = [tuple(row) for row in result]
    roots, ids = ids_of(tuple(row[at[name]] for name in at) for row in rows)
    playlists = {str(row[at["ID"]]): row for row in rows if str(row[at["ID"]]) in ids}
    memberships: dict[str, tuple] = {}
    m_cols: tuple[str, ...] = ()
    ordered = sorted(ids)
    for start in range(0, len(ordered), _CHUNK):
        chunk = ordered[start : start + _CHUNK]
        marks = ", ".join(f":p{n}" for n in range(len(chunk)))
        found = session.execute(
            text(f"SELECT * FROM {_MEMBERSHIPS} WHERE CAST(PlaylistID AS TEXT) IN ({marks})"),
            {f"p{n}": value for n, value in enumerate(chunk)},
        )
        m_cols = tuple(found.keys())
        owner = m_cols.index("ID")
        for row in found:
            memberships[str(row[owner])] = tuple(row)
    return Reading(roots, playlists, memberships, p_cols, m_cols)


def _changed(columns: tuple[str, ...], old: tuple, new: tuple) -> set[str]:
    return {name for name, a, b in zip(columns, old, new, strict=False) if a != b}


def differences(before: Reading, after: Reading) -> list[str]:
    """Every way the subtree read now differs from the reading at open; empty when none.

    A new foreign root is a difference too.
    """
    found: list[str] = []
    for key in sorted(set(before.playlists) | set(after.playlists)):
        old, new = before.playlists.get(key), after.playlists.get(key)
        if old is None:
            found.append(f"the {_PLAYLISTS} row {key!r} appeared under {OWNER}'s folder")
        elif new is None:
            found.append(f"the {_PLAYLISTS} row {key!r} of {OWNER}'s folder is not there")
        elif changed := _changed(before.playlist_columns, old, new):
            found.append(
                f"the {_PLAYLISTS} row {key!r} of {OWNER}'s folder changed {sorted(changed)}"
            )
    for key in sorted(set(before.memberships) | set(after.memberships)):
        old, new = before.memberships.get(key), after.memberships.get(key)
        if old == new:
            continue
        what = "appeared" if old is None else "is not there" if new is None else "changed"
        found.append(f"the {_MEMBERSHIPS} row {key!r} of a playlist in {OWNER}'s folder {what}")
    return found


def pending_touches(
    pending: Iterable[tuple[Any, str, frozenset[str]]], reading: Reading
) -> list[str]:
    """Every pending ``(object, op, columns)`` that would write the foreign subtree."""
    ids = reading.ids
    found: list[str] = []
    for obj, op, columns in pending:
        table = getattr(getattr(obj, "__table__", None), "name", None)
        if table == _PLAYLISTS:
            key = str(getattr(obj, "ID", ""))
            parent = getattr(obj, "ParentID", None)
            parent = "" if parent is None else str(parent)
            if op == "create" and parent in ids:
                found.append(f"creates the {_PLAYLISTS} row {key!r} inside {OWNER}'s folder")
            elif op == "create" and is_foreign_root(
                getattr(obj, "Name", None), parent, getattr(obj, "Attribute", None)
            ):
                found.append(f"creates a second {OWNER} folder at the top, {key!r}")
            elif op == "delete" and key in ids:
                found.append(f"deletes the {_PLAYLISTS} row {key!r} of {OWNER}'s folder")
            elif op == "modify" and key in ids:
                found.append(
                    f"changes the {_PLAYLISTS} row {key!r} of {OWNER}'s folder: "
                    f"{sorted(columns)}"
                )
            elif op == "modify" and parent in ids:
                found.append(f"moves the {_PLAYLISTS} row {key!r} into {OWNER}'s folder")
        elif table == _MEMBERSHIPS:
            owner = str(getattr(obj, "PlaylistID", ""))
            # Asked by its own identifier too, so a rewritten owner cannot hide it.
            if owner in ids or str(getattr(obj, "ID", "")) in reading.memberships:
                found.append(
                    f"{'adds' if op == 'create' else 'changes'} a membership of the "
                    f"playlist {owner!r} in {OWNER}'s folder"
                )
    return found


#: Where :func:`rb_writer.open_db` keeps the reading on its handle.
ATTRIBUTE = "_cratekit_foreign_at_open"

#: Held instead of a reading when the subtree could not be read at open.
UNREAD = "unread"


def remember(db: Any) -> None:
    """Keep the subtree's reading on a handle as it opens.

    A failed read keeps :data:`UNREAD`, never an empty reading, so a later
    commit is refused rather than trusting "nothing there". The open goes on.
    """
    try:
        reading: Reading | str = read(db.session)
    except Exception:  # noqa: BLE001 - unread is kept as unread, never as empty
        reading = UNREAD
    try:
        setattr(db, ATTRIBUTE, reading)
    except (AttributeError, TypeError):  # a handle that holds no attribute
        pass


def reading_at_open(db: Any) -> Reading | None:
    """The reading kept at open, or None when there is none to trust."""
    held = getattr(db, ATTRIBUTE, None)
    return held if isinstance(held, Reading) else None


__all__ = [
    "ATTRIBUTE", "FOREIGN_ROOT_NAMES", "LEFT_AS_IT_IS", "OWNER", "Reading", "UNREAD",
    "differences", "ids_of", "is_foreign_root", "node_ids", "outside", "pending_touches",
    "read", "reading_at_open", "remember", "roots_in",
]
