"""What a session would write, read from the session and the binding's buffer, and judged.

Part of :mod:`cratekit.core.rb_writer`, which re-exports every name here; read them there. A
name of the writer outside this file, and every seam a test patches, is read through
``rb_writer`` at call time so a patch on the writer bites here too (U300).
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Iterable, Mapping

from cratekit.core.rb_tables import (
    _DEFAULT_EMPTIES,
    _REGISTERED,
    ADMITTABLE_ROW_TABLES,
    CONTENT_ROW_EMPTY_COLUMNS,
    CONTENT_TABLE,
    DELETABLE_TABLES,
    FIELD_EMPTIES,
    GRIDLESS_ON_CREATE_COLUMNS,
    LOOKUP_TABLES,
    MOVED,
    PERMITTED_ROW_TABLES,
    REMOVABLE_TABLES,
    UNINSPECTABLE,
    FieldPolicy,
    Ownership,
    content_writable_columns,
)


def _writer():
    """``rb_writer`` at call time: its seams are patched there, and it imports this module."""
    from cratekit.core import rb_writer

    return rb_writer


def guard_violations(
    new: Iterable[tuple[str, Iterable[str]]],
    dirty: Iterable[tuple[str, Iterable[str]]],
    deleted: Iterable[str],
    *,
    content_columns: Iterable[str] | None = None,
    removals: Iterable[str] = (),
    creations: Iterable[str] = (),
    deletions: Iterable[str] = (),
) -> list[str]:
    """Judge a pending session against the whitelist. Empty means allowed.

    ``removals`` (soft deletes), ``creations`` (beyond the whitelist, R-746) and
    ``deletions`` (hard deletes, U288) name the tables this one commit admits,
    each empty for every writer but its one; a name outside
    :data:`REMOVABLE_TABLES`, :data:`ADMITTABLE_ROW_TABLES` or
    :data:`DELETABLE_TABLES` is itself a violation. An admitted content row is
    still judged against :data:`CONTENT_ROW_EMPTY_COLUMNS`; which rows a hard
    delete takes is judged from SQL by :func:`assert_collection_removal_confined`.
    PURE, so every branch is tested with literals. Returns EVERY violation.
    """
    writable = (
        frozenset(content_columns)
        if content_columns is not None
        else content_writable_columns()
    )
    violations: list[str] = []
    admissions = []
    for asked, allowed, verb, admission in (
        (removals, REMOVABLE_TABLES, "remove", "a removal is"),
        (creations, ADMITTABLE_ROW_TABLES, "create", "a creation beyond the whitelist is"),
        (deletions, DELETABLE_TABLES, "delete", "a delete is"),
    ):
        asked = frozenset(asked)
        for table in sorted(asked - allowed):
            violations.append(
                f"asks to {verb} rows in {table!r}, and {admission} admitted in "
                f"{sorted(allowed)} and nowhere else"
            )
        admissions.append(asked & allowed)
    admitted, creatable, deletable = admissions

    for table, columns in new:
        if table == CONTENT_TABLE and table in creatable:
            # THE ONE ADMISSION (R-746), judged again from SQL in
            # ``assert_created_rows_are_gridless``.
            empties, made = CONTENT_ROW_EMPTY_COLUMNS, f"a {CONTENT_TABLE} row"
            because = "carries what the file says and rekordbox derives the rest from the audio"
        elif table == CONTENT_TABLE:
            violations.append(
                f"creates a {CONTENT_TABLE} row; only a landing whose commit admits "
                f"one by name may, and an import in the XML bridge is what every "
                f"other intake performs"
            )
            continue
        elif table in PERMITTED_ROW_TABLES or (table in LOOKUP_TABLES and table in creatable):
            # U163: a minted lookup row is judged as any other creation, and W3: a
            # creation's columns are judged, not only its table.
            empties, made = GRIDLESS_ON_CREATE_COLUMNS, f"a row in {table!r}"
            because = "is gridless and rekordbox derives the grid from the audio"
        else:
            violations.append(f"creates a row in the non-whitelisted table {table!r}")
            continue
        declared = {column for column in columns if column in empties}
        if declared:
            violations.append(
                f"creates {made} declaring analysis column(s): "
                f"{sorted(declared)}; a row this product creates {because}"
            )

    for table, columns in dirty:
        columns = set(columns)
        # THE MARKER IS JUDGED BEFORE THE BOOKKEEPING FILTER DROPS IT (R-758).
        if _writer().SOFT_DELETE_COLUMN in columns and table not in admitted:
            violations.append(
                f"changes the soft delete marker of a row in {table!r}, which "
                f"removes it; writers are additive-only and this commit admits "
                f"no removal there"
            )
        modified = {column for column in columns if column not in _writer().BOOKKEEPING_COLUMNS}
        if not modified:
            continue
        if table == CONTENT_TABLE:
            forbidden = modified - writable
            if forbidden:
                violations.append(
                    f"modifies non-whitelisted {CONTENT_TABLE} column(s): {sorted(forbidden)}"
                )
        elif table not in PERMITTED_ROW_TABLES:
            violations.append(
                f"modifies the non-whitelisted table {table!r}: {sorted(modified)}"
            )

    for table in deleted:
        # Additive only keeps the snapshot a real safety net: a deletion's damage is
        # invisible. The soft delete arrives as a modification. THE ONE HARD DELETE
        # (U288) is admitted only by ``deletions`` and judged from SQL before commit.
        if table in deletable:
            continue
        violations.append(f"deletes a row in {table!r}; writers are additive-only")

    return violations


def clear_registry_buffer() -> None:
    """Empty the binding's process-wide update buffer when a write session opens.

    The guard DEPENDS on the buffer describing this session only, so it is asserted here.
    """
    try:
        from pyrekordbox.db6.registry import RekordboxAgentRegistry
    except Exception:  # noqa: BLE001 - binding absent means no buffer to clear
        return
    RekordboxAgentRegistry.clear_buffer()


def _table_of(obj: Any) -> str | None:
    table = getattr(obj, "__table__", None)
    return getattr(table, "name", None)


def _columns_of(obj: Any) -> set[str]:
    """The columns an EXISTING object reports as changed. Fails closed."""
    from sqlalchemy import inspect as sa_inspect

    try:
        return {
            attribute.key
            for attribute in sa_inspect(obj).attrs
            if attribute.history.has_changes()
        }
    except Exception:  # noqa: BLE001 - un-inspectable means treat as all-changed
        return {UNINSPECTABLE}


def _declared_columns(obj: Any) -> set[str]:
    """The columns a NOT YET FLUSHED object carries a value for. Fails closed.

    Read from the instance dictionary, never the mapper: a failed mapper
    configuration on a transient instance is CACHED process-wide.
    """
    table = getattr(obj, "__table__", None)
    if table is None:
        return {UNINSPECTABLE}
    names = {column.name for column in table.columns}
    try:
        state = vars(obj)
    except TypeError:  # no instance dictionary to read
        return {UNINSPECTABLE}
    return {key for key, value in state.items() if key in names and value is not None}


def _session_changes(
    session: Any,
) -> tuple[dict[int, tuple[str, set[str]]], dict[int, tuple[str, set[str]]], dict[int, str]]:
    """Adapt an object-mapper session into the judge's inputs, keyed by instance.

    FAILS CLOSED with a placeholder column. NOT SUFFICIENT ON ITS OWN (W2): any
    flush, including autoflush before a query, empties ``new`` and ``dirty``.
    Keyed by ``id(instance)`` so the union with the registry buffer merges.
    """
    created = {
        id(obj): (_table_of(obj) or UNINSPECTABLE, _declared_columns(obj)) for obj in session.new
    }
    modified = {
        id(obj): (_table_of(obj) or UNINSPECTABLE, _columns_of(obj)) for obj in session.dirty
    }
    removed = {id(obj): (_table_of(obj) or UNINSPECTABLE) for obj in session.deleted}
    return created, modified, removed


def _buffer_entries(db: Any) -> list[tuple[Any, str | None, str, list[Any]]]:
    """ONE walk of the binding's update buffer, as ``(entry, op, key, instances)``.

    ``op`` None marks a shape not understood, which readers refuse. Empty without
    a handle (see :func:`_registry_changes`) or without the binding.
    """
    if db is None:
        return []
    try:
        from pyrekordbox.db6.registry import RekordboxAgentRegistry
    except Exception:  # noqa: BLE001 - binding absent means no buffer to read
        return []
    walked: list[tuple[Any, str | None, str, list[Any]]] = []
    for entry in list(getattr(RekordboxAgentRegistry, "__update_sequence__", [])):
        try:
            target, op, key, _value = entry
        except (TypeError, ValueError):  # a shape this code does not understand
            walked.append((entry, None, "", []))
            continue
        instances = list(target) if isinstance(target, (list, tuple)) else [target]
        walked.append((entry, str(op), str(key) if key else "", instances))
    return walked


def _registry_changes(
    db: Any,
) -> tuple[dict[int, tuple[str, set[str]]], dict[int, tuple[str, set[str]]], dict[int, str]]:
    """The same judgement inputs, read from the binding's own update buffer.

    The buffer is NOT emptied by a flush, which fixes W2, but the binding skips
    tracking for some internal operations and a raw ``session.add``, so the guard
    reads the UNION (P4). Runs no query. SCOPED TO A HANDLE: the buffer is
    process wide, and read without one it refused a legitimate write (P7).
    """
    created: dict[int, tuple[str, set[str]]] = {}
    modified: dict[int, tuple[str, set[str]]] = {}
    removed: dict[int, str] = {}

    for entry, op, key, instances in _buffer_entries(db):
        if op is None:
            # A shape this code does not understand refuses.
            modified[id(entry)] = (UNINSPECTABLE, {UNINSPECTABLE})
            continue
        for obj in instances:
            table = _table_of(obj)
            if table is None:
                modified[id(obj)] = (UNINSPECTABLE, {UNINSPECTABLE})
            elif op == "create":
                created[id(obj)] = (table, _declared_columns(obj))
            elif op == "update":
                seen = modified.get(id(obj))
                columns = set(seen[1]) if seen else set()
                columns.add(key if key else UNINSPECTABLE)
                modified[id(obj)] = (table, columns)
            elif op == "delete":
                removed[id(obj)] = table
            elif op == "move":
                modified[id(obj)] = (table, {MOVED})
            else:
                # An unknown operation refuses, so a future binding op fails loudly.
                modified[id(obj)] = (table, {UNINSPECTABLE})
    return created, modified, removed


def pending_changes(
    session: Any, db: Any = None
) -> tuple[list[tuple[str, set[str]]], list[tuple[str, set[str]]], list[str]]:
    """Everything this session will write, from BOTH sources, unioned; creation beats modification."""
    s_created, s_modified, s_removed = _session_changes(session)
    r_created, r_modified, r_removed = _writer()._registry_changes(db)

    created = {**r_created, **s_created}

    modified: dict[int, tuple[str, set[str]]] = {}
    for source in (r_modified, s_modified):
        for key, (table, columns) in source.items():
            seen = modified.get(key)
            modified[key] = (table, (set(seen[1]) if seen else set()) | set(columns))

    for key in created:
        modified.pop(key, None)

    removed = {**r_removed, **s_removed}

    return list(created.values()), list(modified.values()), list(removed.values())


def pending_objects(session: Any, db: Any = None) -> list[tuple[Any, str, frozenset[str]]]:
    """Every object this session will write, with ``create``, ``modify`` or ``delete`` and its columns.

    :func:`pending_changes`'s two sources kept as OBJECTS, for a guard asking which
    rows (U185). Shapes the buffer reader does not understand are left to the whitelist.
    """
    found: dict[int, tuple[Any, str, set[str]]] = {}

    def note(obj: Any, op: str, columns: Iterable[str]) -> None:
        seen = found.get(id(obj))
        if seen is not None and seen[1] == "create":
            return
        if seen is not None and op == "modify" and seen[1] == "modify":
            found[id(obj)] = (obj, op, seen[2] | set(columns))
            return
        found[id(obj)] = (obj, op, set(columns))

    for _entry, op, key, instances in _buffer_entries(db):
        for obj in instances:
            if op == "create":
                note(obj, "create", _declared_columns(obj))
            elif op == "delete":
                note(obj, "delete", ())
            elif op == "update":
                note(obj, "modify", (key or UNINSPECTABLE,))
            elif op == "move":
                note(obj, "modify", (MOVED,))
    if session is not None:
        for obj in list(getattr(session, "new", ())):
            note(obj, "create", _declared_columns(obj))
        for obj in list(getattr(session, "dirty", ())):
            note(obj, "modify", _columns_of(obj))
        for obj in list(getattr(session, "deleted", ())):
            note(obj, "delete", ())
    return [(obj, op, frozenset(columns)) for obj, op, columns in found.values()]


def _registry_created_instances(db: Any) -> dict[int, Any]:
    """The INSTANCES the binding's buffer records a creation for, keyed by identity, for the SQL read back."""
    return {
        id(obj): obj
        for _entry, op, _key, instances in _buffer_entries(db)
        if op == "create"
        for obj in instances
    }


class Decision(StrEnum):
    """What the per-field policy says about one proposed write."""

    WRITE = "write"
    SKIP_SAME = "skip_same"
    SKIP_PRESENT = "skip_present"
    SKIP_UNOWNED = "skip_unowned"


def metadata_decision(
    owner: str,
    field_name: str,
    current: Any,
    new: Any,
    *,
    policies: Mapping[str, FieldPolicy] | None = None,
) -> Decision:
    """Decide one field write. Pure.

    CLOSED BY CONSTRUCTION: an unregistered operation or undeclared field writes nothing.
    """
    table = policies if policies is not None else _REGISTERED
    policy = table.get(owner)
    mode = None if policy is None else policy.fields.get(field_name)
    if mode is None:
        return Decision.SKIP_UNOWNED
    if str(current) == str(new):
        return Decision.SKIP_SAME  # idempotent: re-running a run is a no-op
    if mode is Ownership.OWNED:
        return Decision.WRITE
    empties = FIELD_EMPTIES.get(field_name, _DEFAULT_EMPTIES)
    return Decision.WRITE if current in empties else Decision.SKIP_PRESENT


def write_metadata_field(
    row: Any,
    owner: str,
    field_name: str,
    new_value: Any,
    *,
    policies: Mapping[str, FieldPolicy] | None = None,
) -> Decision:
    """Apply the per-field policy to one existing row and report what happened. Does not commit."""
    current = getattr(row, field_name, None)
    decision = metadata_decision(owner, field_name, current, new_value, policies=policies)
    if decision is Decision.WRITE:
        setattr(row, field_name, new_value)
    return decision
