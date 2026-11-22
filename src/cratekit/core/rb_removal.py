"""Remove from Collection: its reads, its renumbering and its confinement proof (U288).

Part of :mod:`cratekit.core.rb_writer`, which re-exports every name here; read them there. A
name of the writer outside this file, and every seam a test patches, is read through
``rb_writer`` at call time so a patch on the writer bites here too (U300).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from cratekit.core.cause import Scope, refuse
from cratekit.core.exit_codes import Remedy
from cratekit.core.rb_tables import (
    COLLECTION_REMOVAL_TABLES,
    CONTENT_REFERENCE_COLUMN,
    CONTENT_TABLE,
    DELETABLE_TABLES,
    LOCAL_UPDATE_COUNT,
    MEMBERSHIP_TABLE,
    PLAYLIST_REFERENCE_COLUMN,
    RECORDED_COLUMNS,
    TARGET_REFERENCE_COLUMN,
    TRACK_NUMBER_COLUMN,
)


def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer


def _tables(session: Any) -> tuple[str, ...]:
    from sqlalchemy import text

    rows = session.execute(
        text("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name")
    ).fetchall()
    return tuple(str(row[0]) for row in rows if not str(row[0]).startswith("sqlite_"))


def _columns(session: Any, table: str) -> tuple[tuple[str, int], ...]:
    """Each column's name and its place in the primary key (0 when it is not in it)."""
    from sqlalchemy import text

    return tuple(
        (str(row[1]), int(row[5] or 0))
        for row in session.execute(text(f'PRAGMA table_info("{table}")')).fetchall()
    )


def content_references(db: Any, content_ids: Iterable[str]) -> dict[str, dict[str, int]]:
    """Every row naming one of ``content_ids`` in a table the removal does NOT delete from.

    From SQL over every table, by ``ContentID`` and by ``TargetID`` where present,
    so an unmapped table is asked too (``uuidIDMap``'s ``CurrentID`` is not).
    ``{content id: {table: rows}}``. A table A178 and A185 did not measure may
    hold a row rekordbox deletes or keeps, so the caller refuses rather than guesses.
    """
    from sqlalchemy import bindparam, text

    wanted = sorted({str(one) for one in content_ids})
    found: dict[str, dict[str, int]] = {}
    if not wanted:
        return found
    session = db.session
    for table in _tables(session):
        if table in DELETABLE_TABLES:
            continue
        names = {name for name, _pk in _columns(session, table)}
        asked = [CONTENT_REFERENCE_COLUMN] if CONTENT_REFERENCE_COLUMN in names else []
        if TARGET_REFERENCE_COLUMN in names:
            asked.append(TARGET_REFERENCE_COLUMN)
        for column in asked:
            statement = text(
                f'SELECT {column}, COUNT(*) FROM "{table}" '
                f"WHERE {column} IN :ids GROUP BY {column}"
            ).bindparams(bindparam("ids", expanding=True))
            for content_id, count in session.execute(statement, {"ids": wanted}).fetchall():
                held = found.setdefault(str(content_id), {})
                held[table] = held.get(table, 0) + int(count)
    return found


def _mapped(table: str) -> Any:
    from pyrekordbox.db6 import tables

    for mapper in tables.Base.registry.mappers:
        if getattr(mapper.class_, "__tablename__", None) == table:
            return mapper.class_
    raise _writer()._unavailable(
        "whitelist-violation",
        f"the binding maps no class for {table!r}, so a track's rows there cannot be "
        f"deleted through it; nothing was written",
        detail={"table": table},
    )


def database_id(db: Any) -> str | None:
    """rekordbox's own ``DjmdProperty.DBID``, or None, binding a recorded removal to its database."""
    held = db.get_property()
    row = held.first() if hasattr(held, "first") else held
    identity = getattr(row, "DBID", None) if row is not None else None
    return str(identity) if identity else None


def recorded_columns(row: Any) -> dict[str, Any]:
    """One collection row's :data:`RECORDED_COLUMNS`, read off it before it is deleted."""
    found: dict[str, Any] = {}
    for name in RECORDED_COLUMNS:
        value = getattr(row, name, None)
        found[name] = value if value is None or isinstance(value, (int, float)) else str(value)
    return found


def remove_from_collection(db: Any, content_id: str) -> dict[str, tuple[str, ...]]:
    """Delete one live track's every row in :data:`COLLECTION_REMOVAL_TABLES`. Returns them by table.

    THE ONE HARD DELETE THIS PRODUCT MAKES, and it is rekordbox's own (A178,
    A185): the content row and every row naming it in six tables, outright,
    playlist and history list rows left. Following members are renumbered by
    :class:`CollectionRemoval` (R-1830); history is not. THROUGH THE BINDING'S
    OWN DELETE, children first, so the whitelist sees each row. REFUSED, WITH
    NOTHING DELETED: no live row, or a row named outside the removal set
    (:func:`content_references`). DOES NOT COMMIT: the caller commits with
    ``deletions`` after :func:`assert_collection_removal_confined`.
    """
    key = str(content_id)
    content_class = _mapped(CONTENT_TABLE)
    row = db.session.get(content_class, key)
    if row is None or _writer().soft_deleted(
        row,
        message=(
            f"the collection row {key!r} cannot say whether rekordbox removed it, and "
            f"deleting it as live could take a track out twice"
        ),
        origin=("rb_writer",),
        detail={"content_id": key},
    ):
        raise _writer()._unavailable(
            "whitelist-violation",
            f"asked to take the collection row {key!r} out of the collection, and the "
            f"database holds no live row of that id; nothing was written",
            detail={"content_id": key},
        )
    held = content_references(db, (key,)).get(key, {})
    if held:
        named = ", ".join(f"{table} ({count})" for table, count in sorted(held.items()))
        raise _writer()._unavailable(
            "whitelist-violation",
            f"the collection row {key!r} is named by rows in {named}, which "
            f"rekordbox's Remove from Collection was never measured on, so what it "
            f"would do with them is not known; nothing was written",
            detail={"content_id": key, "tables": dict(sorted(held.items()))},
        )
    deleted: dict[str, tuple[str, ...]] = {}
    for table in COLLECTION_REMOVAL_TABLES[1:]:
        mapped = _mapped(table)
        found = list(
            db.session.query(mapped).filter(getattr(mapped, CONTENT_REFERENCE_COLUMN) == key)
        )
        for child in found:
            db.delete(child)
        deleted[table] = tuple(sorted(str(child.ID) for child in found))
    db.delete(row)
    deleted[CONTENT_TABLE] = (key,)
    return {table: deleted[table] for table in COLLECTION_REMOVAL_TABLES}


def renumbered_positions(
    memberships: Iterable[tuple[str, str, str, int | None, bool]],
    removed: Iterable[str],
) -> dict[str, tuple[str, int, int]]:
    """Which membership rows a removal renumbers, and to what. PURE (R-1830).

    ``memberships`` holds ``(membership id, playlist id, content id, TrackNo,
    live)``; returns ``{membership id: (playlist id, TrackNo now, TrackNo after)}``
    for rows that move. Measured (A197): each surviving LIVE row above a removed
    live row drops by one per such row below it, the binding's rule without its
    self-committing call. ONLY LIVE ROWS COUNT AND ONLY LIVE ROWS MOVE, or a
    marked row sharing a number would put two live rows on one place. A row with
    no number or an unreadable marker is neither lowered nor counted.
    """
    rows = [
        (str(key), str(playlist), str(content), number, bool(live))
        for key, playlist, content, number, live in memberships
    ]
    gone = {str(one) for one in removed}
    deleted: dict[str, list[int]] = {}
    for _key, playlist, content, number, live in rows:
        if content in gone and live and number is not None:
            deleted.setdefault(playlist, []).append(int(number))
    moved: dict[str, tuple[str, int, int]] = {}
    for key, playlist, content, number, live in rows:
        if content in gone or not live or number is None:
            continue
        below = sum(1 for one in deleted.get(playlist, ()) if one < int(number))
        if below:
            moved[key] = (playlist, int(number), int(number) - below)
    return moved


def removal_renumbering(db: Any, content_ids: Iterable[str]) -> dict[str, tuple[str, int, int]]:
    """The membership rows removing ``content_ids`` would renumber, read from SQL (R-1830).

    Asked on a read only copy for the plan's count and again on the write handle by
    :meth:`CollectionRemoval.prepare`. Reads and writes nothing else.
    """
    from sqlalchemy import bindparam, text

    wanted = sorted({str(one) for one in content_ids})
    if not wanted:
        return {}
    statement = text(
        f'SELECT "ID", "{PLAYLIST_REFERENCE_COLUMN}", "{CONTENT_REFERENCE_COLUMN}", '
        f'"{TRACK_NUMBER_COLUMN}", "{_writer().SOFT_DELETE_COLUMN}" FROM "{MEMBERSHIP_TABLE}" '
        f'WHERE "{PLAYLIST_REFERENCE_COLUMN}" IN (SELECT "{PLAYLIST_REFERENCE_COLUMN}" '
        f'FROM "{MEMBERSHIP_TABLE}" WHERE "{CONTENT_REFERENCE_COLUMN}" IN :ids)'
    ).bindparams(bindparam("ids", expanding=True))
    rows = db.session.execute(statement, {"ids": wanted}).fetchall()
    unreadable = sorted(str(row[0]) for row in rows if row[4] is None)
    if unreadable:
        # REFUSED, AS :func:`soft_deleted` REFUSES: other readers take NULL as live.
        raise refuse(
            "soft-delete-marker-unreadable",
            f"{len(unreadable)} playlist membership row(s) in a playlist this removal "
            f"would renumber cannot say whether rekordbox removed them, so where the "
            f"tracks after the removed one belong cannot be said; nothing was written",
            remedy=Remedy.RUN_DOCTOR,
            scope=Scope.RUN,
            origin=("rb_writer",),
            detail={"membership_ids": unreadable[:20], "column": _writer().SOFT_DELETE_COLUMN},
        )
    return renumbered_positions(
        ((row[0], row[1], row[2], None if row[3] is None else int(row[3]), _live(row[4])) for row in rows),
        wanted,
    )


def _live(marker: Any) -> bool:
    """Whether a membership row's soft delete marker reads live; unreadable reads not live."""
    return marker is not None and not bool(marker)


def renumber_memberships(db: Any, moved: Mapping[str, tuple[str, int, int]]) -> None:
    """Write each planned ``TrackNo``, that one column and nothing else, inside the open transaction.

    ONE SQL UPDATE PER ROW, since rekordbox stamped nothing else (A197). Each names
    the planned old number, so a row that moved refuses and the handle rolls back.
    Held objects are expired. DOES NOT COMMIT.
    """
    from sqlalchemy import text

    statement = text(
        f'UPDATE "{MEMBERSHIP_TABLE}" SET "{TRACK_NUMBER_COLUMN}" = :after '
        f'WHERE "ID" = :key AND "{TRACK_NUMBER_COLUMN}" = :before'
    )
    session = db.session
    for key, (_playlist, before, after) in sorted(moved.items()):
        result = session.execute(statement, {"after": after, "key": key, "before": before})
        if result.rowcount != 1:
            db.rollback()
            raise _writer()._unavailable(
                "whitelist-violation",
                f"the playlist membership {key!r} no longer holds the place {before} the "
                f"removal planned to renumber from, so its renumbering was not written and "
                f"nothing was committed",
                detail={"membership_id": key, "planned": before},
            )
    for held in list(session.identity_map.values()):
        if _writer()._table_of(held) == MEMBERSHIP_TABLE and str(getattr(held, "ID", "")) in moved:
            session.expire(held)


@dataclass(frozen=True)
class DatabaseReading:
    """Every table of the database as it stands, row by row, read from SQL.

    ``rows``: per table, primary key (or ``rowid``) to a row digest. ``named``:
    for :data:`DELETABLE_TABLES`, the content row each names. ``counter``:
    ``localUpdateCount`` or None. ``positions``: per membership row its playlist,
    content, ``TrackNo``, liveness and a digest of the rest (R-1830).
    """

    rows: Mapping[str, Mapping[str, str]]
    named: Mapping[str, Mapping[str, str]]
    counter: int | None
    positions: Mapping[str, tuple[str, str, int | None, bool, str]] = field(default_factory=dict)


def database_reading(db: Any) -> DatabaseReading:
    """Read every table from SQL. Flushes nothing itself, as :func:`node_tables` does not."""
    import hashlib

    from sqlalchemy import text

    session = db.session
    rows: dict[str, dict[str, str]] = {}
    named: dict[str, dict[str, str]] = {}
    positions: dict[str, tuple[str, str, int | None, bool, str]] = {}
    for table in _tables(session):
        columns = _columns(session, table)
        keys = [name for name, place in sorted(columns, key=lambda one: one[1]) if place]
        names = [name for name, _place in columns]
        selected = ", ".join(f'"{name}"' for name in names)
        if keys:
            keyed = [names.index(name) for name in keys]
            result = session.execute(text(f'SELECT {selected} FROM "{table}"'))
        else:
            keyed = [len(names)]
            result = session.execute(text(f'SELECT {selected}, rowid FROM "{table}"'))
        reference = (
            names.index("ID")
            if table == CONTENT_TABLE
            else (names.index(CONTENT_REFERENCE_COLUMN) if CONTENT_REFERENCE_COLUMN in names else None)
        )
        placed = (
            (
                names.index(PLAYLIST_REFERENCE_COLUMN),
                names.index(CONTENT_REFERENCE_COLUMN),
                names.index(TRACK_NUMBER_COLUMN),
                names.index(_writer().SOFT_DELETE_COLUMN),
            )
            if table == MEMBERSHIP_TABLE
            and {
                PLAYLIST_REFERENCE_COLUMN,
                CONTENT_REFERENCE_COLUMN,
                TRACK_NUMBER_COLUMN,
                _writer().SOFT_DELETE_COLUMN,
            }
            <= set(names)
            else None
        )
        found: dict[str, str] = {}
        naming: dict[str, str] = {}
        for row in result:
            values = tuple(row)
            key = "|".join(str(values[at]) for at in keyed)
            found[key] = hashlib.sha256(repr(values[: len(names)]).encode("utf-8")).hexdigest()
            if table in DELETABLE_TABLES and reference is not None:
                naming[key] = str(values[reference])
            if placed is not None:
                playlist_at, content_at, number_at, marker_at = placed
                rest = tuple(
                    value for at, value in enumerate(values[: len(names)]) if at != number_at
                )
                number = values[number_at]
                positions[key] = (
                    str(values[playlist_at]),
                    str(values[content_at]),
                    None if number is None else int(number),
                    _live(values[marker_at]),
                    hashlib.sha256(repr(rest).encode("utf-8")).hexdigest(),
                )
        rows[table] = found
        if table in DELETABLE_TABLES:
            named[table] = naming
    counter = session.execute(
        text("SELECT int_1 FROM agentRegistry WHERE registry_id = :id"),
        {"id": LOCAL_UPDATE_COUNT},
    ).scalar() if "agentRegistry" in rows else None
    return DatabaseReading(rows, named, None if counter is None else int(counter), positions)


def collection_removal_violations(
    before: DatabaseReading,
    after: DatabaseReading,
    *,
    removed: Iterable[str],
    committed: bool = False,
) -> list[str]:
    """Every difference between two readings the planned removal does not explain.

    PURE. Empty means confined AND made. It explains only: rows gone from
    :data:`DELETABLE_TABLES` that named a ``removed`` row, EVERY such row gone and
    each removed row live before; no table or row added; no row changed but a
    planned renumbering to exactly :func:`renumbered_positions`'s number, every
    planned one made (R-1830); and with ``committed``, ``localUpdateCount``
    moving forward.
    """
    gone = {str(one) for one in removed}
    violations: list[str] = []
    planned = renumbered_positions(
        (
            (key, playlist, content, number, live)
            for key, (playlist, content, number, live, _rest) in before.positions.items()
        ),
        gone,
    )
    for table in sorted(set(before.rows) ^ set(after.rows)):
        violations.append(f"the table {table!r} appeared or disappeared")
    for content_id in sorted(gone):
        if content_id not in before.named.get(CONTENT_TABLE, {}):
            violations.append(f"the planned {CONTENT_TABLE} row {content_id!r} was not there")
    for table in sorted(set(before.rows) & set(after.rows)):
        old, new = before.rows[table], after.rows[table]
        for key in sorted(set(new) - set(old)):
            violations.append(f"an unplanned {table} row {key!r} was added")
        naming = before.named.get(table, {})
        for key in sorted(set(old) - set(new)):
            if table not in DELETABLE_TABLES or naming.get(key) not in gone:
                violations.append(f"the {table} row {key!r} disappeared, which no planned removal explains")
        for key in sorted(set(old) & set(new)):
            if table == MEMBERSHIP_TABLE and key in planned:
                violations.extend(_renumbering_violations(key, planned[key], before, after))
                continue
            if old[key] == new[key]:
                continue
            if committed and table == "agentRegistry" and key == LOCAL_UPDATE_COUNT:
                continue
            violations.append(f"the {table} row {key!r} changed, and a removal changes no row")
        for key, names in sorted(naming.items()):
            if names in gone and key in new:
                violations.append(
                    f"the {table} row {key!r} still names the removed {CONTENT_TABLE} row {names!r}"
                )
    if committed and (
        before.counter is None or after.counter is None or after.counter <= before.counter
    ):
        violations.append(
            f"{LOCAL_UPDATE_COUNT} did not move forward ({before.counter} to {after.counter})"
        )
    return violations


def _renumbering_violations(
    key: str,
    plan: tuple[str, int, int],
    before: DatabaseReading,
    after: DatabaseReading,
) -> list[str]:
    """What is wrong with one membership row the removal was to renumber, or nothing."""
    _playlist, was, wanted = plan
    then = before.positions.get(key)
    now = after.positions.get(key)
    if then is None or now is None:
        return [f"the {MEMBERSHIP_TABLE} row {key!r} could not be read for its renumbering"]
    found: list[str] = []
    if (now[0], now[1], now[3], now[4]) != (then[0], then[1], then[3], then[4]):
        found.append(
            f"the {MEMBERSHIP_TABLE} row {key!r} changed in a column other than "
            f"{TRACK_NUMBER_COLUMN}, and a renumbering moves that column alone"
        )
    if now[2] != wanted:
        found.append(
            f"the {MEMBERSHIP_TABLE} row {key!r} was to be renumbered from {was} to "
            f"{wanted} and holds {now[2]}"
        )
    return found


def assert_collection_removal_confined(
    db: Any, before: DatabaseReading, *, removed: Iterable[str]
) -> None:
    """Refuse, before the commit, a removal that reached anything it did not plan.

    FROM SQL after a deliberate flush, judging whose rows went and that nothing
    else moved, which the table-level whitelist cannot. A REFUSAL ROLLS BACK.
    """
    db.session.flush()
    violations = collection_removal_violations(before, database_reading(db), removed=removed)
    if violations:
        db.rollback()
        raise _writer()._unavailable(
            "whitelist-violation",
            "the removal from the collection reached rows it did not plan, or did not "
            "make one it planned, read from SQL before the commit:\n  - "
            + "\n  - ".join(violations[:20]),
            detail={"violations": violations},
        )


