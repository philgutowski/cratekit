"""Another app's folder at the top of rekordbox's tree, left exactly as it is (U185).

DEADCA7 is a catalog manager that can push into rekordbox's database: its
playlists go into ONE FOLDER NAMED ``DEADCA7`` AT THE TOP OF THE PLAYLIST TREE,
its hot cues per track, and its grids and waveforms as analysis files. Phillip
uses it beside Cratekit on one library, decided on 2026-10-31, and the rule
that makes that safe is that neither tool undoes the other's work. This module
is the one place that rule is spelled.

THE PREDICATE IS NARROW ON PURPOSE. A foreign root is a FOLDER, directly under
the playlist root, whose name is exactly one of :data:`FOREIGN_ROOT_NAMES`.
Everything under it, at any depth and whether rekordbox removed it or not, is
foreign. A folder or playlist that merely carries the name further down the
tree is somebody's own namesake and is not foreign, and neither is a plain
playlist of that name at the root, which is not the shape the push writes.

WHAT IS GUARDED, AND WHERE. The rows a push writes into the playlist tree are
the folder, its playlists and their memberships. :func:`read` takes them from
SQL, whole, when :func:`rb_writer.open_db` opens a handle, and
:func:`rb_writer.commit_guarded` refuses any commit that would change them,
asked two ways because neither alone sees everything: :func:`pending_touches`
reads the objects the session and the binding's update buffer will write, and
:func:`differences` reads the subtree again from SQL and compares it with the
reading at open, which is what sees a flushed write and raw SQL. Every write in
this product commits through that one function, so no verb can move, rename,
empty or fill the folder silently. The cues and analysis columns a push writes
are outside the additive whitelist already: nothing here writes a cue row, and
every analysis column is refused on every write.

NOT EVEN ITS POSITION MOVES. rekordbox's binding renumbers the siblings at or
past a new node's position only when a caller names one, and moves renumber
only the parents they leave and join; nothing here names a position at the
root or moves a node there, measured over ``src`` on 2026-10-31, so the root
row is held whole like every other.

Layer: infrastructure.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

#: The names of the top level folders another app owns. Exactly as the app
#: writes them: the match is on the whole name and its case.
FOREIGN_ROOT_NAMES: frozenset[str] = frozenset({"DEADCA7"})

#: The app each foreign root belongs to, for the one line a report gives it.
OWNER = "DEADCA7"

#: What a report says of a foreign root, beside its name.
LEFT_AS_IT_IS = "another app's folder, left exactly as it is and not counted as yours"

#: The playlist and membership tables, named here rather than imported, since
#: this module is read by the writer it guards.
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
    """The foreign roots and every foreign node, from ``(ID, Name, ParentID, Attribute)``.

    Answers ``(roots, every node)``. PURE, so every branch is reachable with
    literal rows. A walk down by parent, so a node is foreign only through a
    chain of parents that ends at a foreign root; a cycle, which no real tree
    holds, ends the walk rather than looping.
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
    return (
        getattr(row, "ID", None),
        getattr(row, "Name", None),
        getattr(row, "ParentID", None),
        getattr(row, "Attribute", None),
    )


def node_ids(rows: Iterable[Any]) -> frozenset[str]:
    """Every foreign node among playlist rows read through the binding."""
    return ids_of(_fields(row) for row in rows)[1]


def outside(rows: Iterable[Any], every_row: Iterable[Any]) -> list[Any]:
    """``rows`` with every foreign node left out, judged against the whole tree.

    ``every_row`` is the whole playlist table, since whether a row is foreign
    is a question about its ancestors and not about the row alone.
    """
    foreign = node_ids(every_row)
    return [row for row in rows if str(getattr(row, "ID", "")) not in foreign]


def roots_in(rows: Iterable[Any]) -> list[Any]:
    """The foreign roots among playlist rows read through the binding."""
    return [row for row in rows if is_foreign_root(*_fields(row)[1:])]


@dataclass(frozen=True)
class Reading:
    """The foreign subtree as SQL holds it: whole rows, by identifier.

    ``roots`` names the foreign roots, ``playlists`` every foreign node's row,
    ``memberships`` every membership row of a foreign playlist. The column
    tuples say what each position of a row is.
    """

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
    roots, ids = ids_of(
        (row[at["ID"]], row[at["Name"]], row[at["ParentID"]], row[at["Attribute"]])
        for row in rows
    )
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
    return Reading(
        roots=roots,
        playlists=playlists,
        memberships=memberships,
        playlist_columns=p_cols,
        membership_columns=m_cols,
    )


def _changed(columns: tuple[str, ...], old: tuple, new: tuple) -> set[str]:
    return {name for name, a, b in zip(columns, old, new, strict=False) if a != b}


def differences(before: Reading, after: Reading) -> list[str]:
    """Every way the foreign subtree read now differs from the reading at open.

    Empty means the subtree is as it was, every column of every row.
    A NEW foreign root is a difference too: a write that made a second folder
    of the name would give the app two homes and this product a namesake.
    """
    found: list[str] = []
    for key in sorted(set(before.playlists) | set(after.playlists)):
        old, new = before.playlists.get(key), after.playlists.get(key)
        if old is None:
            found.append(f"the {_PLAYLISTS} row {key!r} appeared under {OWNER}'s folder")
            continue
        if new is None:
            found.append(f"the {_PLAYLISTS} row {key!r} of {OWNER}'s folder is not there")
            continue
        changed = _changed(before.playlist_columns, old, new)
        if changed:
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
    """Every pending object that would write the foreign subtree.

    ``pending`` is ``(object, op, columns)``, ``op`` one of ``create``,
    ``modify`` and ``delete``, as :func:`rb_writer.pending_objects` gives it.
    """
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
            if owner in ids:
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
    """Read the subtree as a handle opens and keep the reading on the handle.

    A read that fails keeps :data:`UNREAD` rather than an empty reading, so a
    later commit cannot mistake "could not look" for "nothing there" and is
    refused instead. The open itself goes on, since a read only caller has no
    write for the reading to protect.
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
    "ATTRIBUTE",
    "FOREIGN_ROOT_NAMES",
    "LEFT_AS_IT_IS",
    "OWNER",
    "Reading",
    "UNREAD",
    "differences",
    "ids_of",
    "is_foreign_root",
    "node_ids",
    "outside",
    "pending_touches",
    "read",
    "reading_at_open",
    "remember",
    "roots_in",
]
