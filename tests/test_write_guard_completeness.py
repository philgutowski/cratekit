"""The write guard sees everything the session will write, not just what survives.

W2 and W3 from the U9 attended gate, plus the A4 whitelist addition.

W2 IS THE LOAD BEARING ONE. The whitelist judge read ``session.new`` and
``session.dirty`` and nothing else. SQLAlchemy empties both on any flush, and it
flushes pending work before a query so the query can see it. A flushed INSERT is
still uncommitted and still rollback-able, but it has left those collections, so
the guard judged an empty session and approved. Every primitive in the writer
does an add followed by a lookup, in a loop, so this was the normal path rather
than an exotic one. The A1 verdict made it urgent: a database-native intake path
is now buildable, and the guard meant to police it did not fire.

W3. A row CREATION was judged on its table name alone. The judge bound the
column set and threw it away, so a created row had no column policy at all. That
was nearly harmless while the whitelist held four membership tables, and stops
being harmless in the same change that adds a fifth.

Every set here is DERIVED at run time, by walking the binding, parsing its
source, or iterating a module constant. Seam decision P3: a test whose name
quantifies over a set and then hand-lists it is a test that misses the next
addition.
"""

from __future__ import annotations

import ast
import inspect

import pytest

from cratekit.core import rb_writer as W

#: Captured before any fixture can replace it. The autouse fixture below stubs
#: the buffer reader out for most tests, and the three tests that exercise the
#: reader itself would otherwise introspect the stub.
_REAL_REGISTRY_CHANGES = W._registry_changes


class _FakeObj:
    """Stands in for a mapped instance, with just the surface the guard reads."""

    def __init__(self, table, columns=(), primary_key=("ID",)):
        class _Column:
            def __init__(self, name):
                self.name = name

        class _PK:
            def __init__(self, names):
                self.columns = [_Column(n) for n in names]

        class _Table:
            def __init__(self, name, columns, pk):
                self.name = name
                self.columns = [_Column(c) for c in columns]
                self.primary_key = _PK(pk)

        self.__table__ = _Table(table, columns, primary_key)
        for column in columns:
            setattr(self, column, 1)


class _Session:
    def __init__(self, new=(), dirty=(), deleted=()):
        self.new = list(new)
        self.dirty = list(dirty)
        self.deleted = list(deleted)


@pytest.fixture(autouse=True)
def _empty_buffer(monkeypatch):
    """Every test starts with an empty update buffer.

    The buffer is a class attribute shared process wide, so without this a test
    inherits whatever an earlier test left behind, which is precisely the bug
    this file also pins below.
    """
    monkeypatch.setattr(W, "_registry_changes", lambda db: ({}, {}, {}))


# ---------------------------------------------------------------------------
# W2. A flush must not blind the guard
# ---------------------------------------------------------------------------


def test_a_creation_flushed_out_of_the_session_is_still_judged(monkeypatch):
    """The regression, stated at its smallest.

    The session reports nothing, exactly as it would after an autoflush. The
    binding's buffer still holds the creation, and the guard must refuse on it.
    """
    forbidden = _FakeObj("djmdArtist")
    monkeypatch.setattr(
        W, "_registry_changes", lambda db: ({id(forbidden): ("djmdArtist", set())}, {}, {})
    )

    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_session_whitelisted(_Session(), object())

    assert "djmdArtist" in str(excinfo.value)


def test_a_content_creation_flushed_away_is_still_refused(monkeypatch):
    """The case A1 made real: intake is buildable, so the guard must police it."""
    row = _FakeObj("djmdContent")
    monkeypatch.setattr(
        W, "_registry_changes", lambda db: ({id(row): ("djmdContent", set())}, {}, {})
    )

    with pytest.raises(W.RekordboxUnavailable) as excinfo:
        W.assert_session_whitelisted(_Session(), object())

    assert "djmdContent" in str(excinfo.value)


def test_the_two_sources_are_unioned_rather_than_either_being_trusted_alone(monkeypatch):
    """Neither source is complete, which is why the guard reads both (P4).

    The buffer misses anything written while the binding disables its own
    tracking, and a raw session add never reaches it. The session collections
    miss anything a flush has carried away. A guard trusting either alone has a
    blind spot; only the union has none.
    """
    from_session = _FakeObj("djmdSongPlaylist")
    from_buffer = _FakeObj("djmdArtist")
    monkeypatch.setattr(
        W, "_registry_changes", lambda db: ({id(from_buffer): ("djmdArtist", set())}, {}, {})
    )

    created, _modified, _removed = W.pending_changes(_Session(new=[from_session]), object())
    assert sorted(table for table, _ in created) == ["djmdArtist", "djmdSongPlaylist"]


def test_one_instance_created_then_updated_is_reported_once_as_a_creation(monkeypatch):
    """Creation wins. Reporting both would be two findings for one act."""
    obj = _FakeObj("djmdPlaylist")
    monkeypatch.setattr(
        W,
        "_registry_changes",
        lambda db: ({id(obj): ("djmdPlaylist", set())}, {id(obj): ("djmdPlaylist", {"Name"})}, {}),
    )

    created, modified, _removed = W.pending_changes(_Session(), object())
    assert [t for t, _ in created] == ["djmdPlaylist"]
    assert modified == []


def test_the_buffer_is_scoped_to_an_open_handle():
    """With no handle there is no session whose buffer it could be.

    This fired for real: a guard called with no handle inherited rows created by
    earlier work in the same process and refused a legitimate write. A guard that
    refuses correct code is one people route around (P7).
    """
    assert _REAL_REGISTRY_CHANGES(None) == ({}, {}, {})


def test_every_operation_the_binding_can_record_is_translated():
    """Derived by parsing the binding's own source, never by listing the ops.

    A future binding adding a fifth operation must fail here rather than pass
    silently through the guard.
    """
    from pyrekordbox.db6 import registry as R

    tree = ast.parse(inspect.getsource(R))
    ops: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "append"):
            continue
        target = ast.unparse(func.value)
        if "__update_sequence__" not in target:
            continue
        for arg in node.args:
            if isinstance(arg, ast.Tuple) and len(arg.elts) >= 2:
                op = arg.elts[1]
                if isinstance(op, ast.Constant) and isinstance(op.value, str):
                    ops.add(op.value)

    assert ops, "the parse found no operations; the walk is broken, not the binding"

    handled = _operations_the_guard_translates()
    missing = sorted(ops - handled)
    assert not missing, (
        f"the binding can record {missing} and the guard does not translate them, "
        "so those writes would be judged with no table and no columns"
    )


def _operations_the_guard_translates() -> set[str]:
    """The op strings ``_registry_changes`` compares against, read from its source."""
    tree = ast.parse(inspect.getsource(_REAL_REGISTRY_CHANGES))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare) and isinstance(node.left, ast.Name):
            if node.left.id == "op":
                for comparator in node.comparators:
                    if isinstance(comparator, ast.Constant):
                        found.add(comparator.value)
    return found


def test_an_operation_the_guard_has_never_heard_of_fails_closed():
    """An unknown op reports the sentinel, which is outside every writable set."""
    obj = _FakeObj("djmdPlaylist")

    class _Registry:
        __update_sequence__ = [(obj, "teleport", "", "")]

    import sys
    import types

    module = types.ModuleType("pyrekordbox.db6.registry")
    module.RekordboxAgentRegistry = _Registry
    saved = sys.modules.get("pyrekordbox.db6.registry")
    sys.modules["pyrekordbox.db6.registry"] = module
    try:
        _created, modified, _removed = _REAL_REGISTRY_CHANGES(object())
    finally:
        if saved is not None:
            sys.modules["pyrekordbox.db6.registry"] = saved
        else:
            del sys.modules["pyrekordbox.db6.registry"]

    assert modified[id(obj)] == ("djmdPlaylist", {W.UNINSPECTABLE})


def test_a_move_is_judged_on_its_table_rather_than_skipped():
    """An empty column set would look like a bookkeeping touch and skip the check.

    A move on a whitelisted table passes; the same move on any other table
    refuses. That is the judgement a re-parent deserves, and it needs a named
    sentinel to get it.
    """
    assert W.guard_violations([], [("djmdPlaylist", {W.MOVED})], []) == []
    assert W.guard_violations([], [("djmdArtist", {W.MOVED})], []) != []


# ---------------------------------------------------------------------------
# W3. A creation now carries a column policy
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("column", sorted(W.GRIDLESS_ON_CREATE_COLUMNS))
def test_a_created_row_declaring_an_analysis_column_is_refused(column):
    """Parametrized over the constant, read at run time. One edit arms them all."""
    violations = W.guard_violations([("djmdPlaylist", {column})], [], [])
    assert violations, f"a created row declaring {column} was allowed"
    assert column in violations[0]


def test_a_created_row_declaring_only_ordinary_columns_passes():
    """P7. The guard must not fire on the writes it exists to permit."""
    assert W.guard_violations([("djmdPlaylist", {"Name", "ParentID", "Seq"})], [], []) == []


def test_every_gridless_column_is_a_real_column_on_the_content_table():
    """The honest list is checked against the schema, so a rename fails loudly.

    Without this, a binding that renamed a column would silently disarm the
    check while every test stayed green.
    """
    from pyrekordbox.db6.tables import DjmdContent

    real = {column.name for column in DjmdContent.__table__.columns}
    missing = sorted(W.GRIDLESS_ON_CREATE_COLUMNS - real)
    assert not missing, f"{missing} are not columns on djmdContent; the check is disarmed"
    missing = sorted(W.CONTENT_ROW_EMPTY_COLUMNS - real)
    assert not missing, f"{missing} are not columns on djmdContent; the check is disarmed"


def test_every_analysis_table_is_a_real_table_keyed_on_the_content_row():
    """The three tables an admitted content row must own no row in (R-746)."""
    from pyrekordbox.db6.tables import Base

    for name in W.CONTENT_ANALYSIS_TABLES:
        table = Base.metadata.tables.get(name)
        assert table is not None, f"{name} is not a table in the binding"
        assert "ContentID" in table.columns, f"{name} carries no ContentID column"


def test_a_flushed_creation_is_read_back_from_both_sources(monkeypatch):
    """R-760's blind spot, closed: the SQL read back used to walk ``session.new``
    only, so a creation the binding had already flushed was never read."""
    row = _FakeObj("djmdContent", columns=("ID", "BPM"))
    monkeypatch.setattr(W, "_registry_created_instances", lambda db: {id(row): row})
    seen: list[object] = []

    class _Inspected:
        identity = None

    def inspect(obj):
        seen.append(obj)
        return _Inspected()

    import sqlalchemy

    monkeypatch.setattr(sqlalchemy, "inspect", inspect)

    class _Flushing(_Session):
        def flush(self):
            return None

    class _Handle:
        session = _Flushing()

    W.assert_created_rows_are_gridless(_Handle())
    assert seen == [row], "the buffered creation was not resolved for its read back"


# ---------------------------------------------------------------------------
# A4. djmdKey joins the whitelist
# ---------------------------------------------------------------------------


def test_a_lookup_row_creation_is_permitted():
    """The A4 verdict, TOLERATED, expressed as the guard's decision."""
    assert W.guard_violations([("djmdKey", set())], [], []) == []


def test_a_lookup_row_creation_still_carries_the_column_policy():
    """The pairing that makes the widening safe (P5).

    The permission and the column policy land together, so the fifth table
    cannot be the one that walks an analysis column in.
    """
    assert W.guard_violations([("djmdKey", {"Analysed"})], [], []) != []


def test_every_permitted_table_is_a_real_table_in_the_binding():
    """Derived by iterating the constant. Catches a typo, which is otherwise
    a silently inert whitelist entry that permits nothing and warns nobody."""
    from pyrekordbox.db6.tables import Base

    real = set(Base.metadata.tables)
    missing = sorted(W.PERMITTED_ROW_TABLES - real)
    assert not missing, f"{missing} are not tables in the binding"


def test_deletion_stays_unconditional_including_the_new_table():
    """Additive only is what makes the snapshot a real safety net."""
    for table in sorted(W.PERMITTED_ROW_TABLES):
        assert W.guard_violations([], [], [table]) != [], f"{table} was deletable"


def test_the_beatgrid_table_is_still_absent_from_the_whitelist():
    """The widening added one table. It must not have added that one."""
    assert "djmdBeatGrid" not in W.PERMITTED_ROW_TABLES
    assert W.CONTENT_TABLE not in W.PERMITTED_ROW_TABLES
