"""Exact membership of every set that decides how much a writer may do.

R-15. The guard tests assert what must NOT be permitted; only exact membership
catches a widening, since adding a table or column passes every negative
assertion. Measured before these pins: a sixth permitted table and a swapped
bookkeeping column, applied together, killed nothing in the full suite.

Hand listed on purpose, against P3: a pin does not quantify, it IS the
ceiling, so changing a pin is the review of the widening. Each pin was checked
red against a deliberate widening first; a pin written after one ratifies it.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from cratekit.core import rb_writer as W
from cratekit.write import metadata

SRC_ROOT = Path(__file__).resolve().parent.parent / "src"

OWNED = W.Ownership.OWNED
FILL_IF_EMPTY = W.Ownership.FILL_IF_EMPTY


@pytest.fixture(autouse=True)
def _baseline_registry():
    W.reset_field_policies()
    yield
    W.reset_field_policies()


def test_the_permitted_tables_are_exactly_these_five():
    """The structural guarantee. Any table outside this set cannot gain a row."""
    assert W.PERMITTED_ROW_TABLES == frozenset(
        {"djmdPlaylist", "djmdSongPlaylist", "djmdMyTag", "djmdSongMyTag", "djmdKey"}
    )


def test_the_baseline_content_allow_list_is_exactly_the_track_colour():
    """What a slim install may write into a track row with nothing enabled.

    The allow list is derived from the registry, so the pin sits on its
    baseline: the one policy, its field and mode, and their union."""
    policies = {
        owner: dict(policy.fields)
        for owner, policy in W.registered_field_policies().items()
    }
    assert policies == {"track-color": {"ColorID": OWNED}}
    assert W.content_writable_columns() == frozenset({"ColorID"})


def test_every_metadata_operation_declares_exactly_its_field_and_mode():
    """The mode is part of the ceiling: owned over fill if empty adds no
    column and lets automation overwrite a rating a person set."""
    declared = {owner: dict(policy.fields) for owner, policy in metadata.OPERATIONS.items()}
    assert declared == {
        "pad-camelot": {"Title": OWNED},
        "retag-genre": {"GenreID": OWNED},
        "rating-backfill": {"Rating": FILL_IF_EMPTY},
        "adopt-rekordbox-head": {"Title": OWNED},
    }


def test_the_content_allow_list_with_every_operation_enabled_is_exactly_four_columns():
    """The widest the content gate can be made on this tree, by any profile."""
    assert metadata.enable() == frozenset({"ColorID", "Title", "GenreID", "Rating"})


def test_the_bookkeeping_set_is_exactly_these_ten_columns():
    """The quietest widening, so the tightest pin.

    Entries are IGNORED when a modification is judged, so an addition stops the
    guard looking at a write. A count misses a swap that keeps the length at ten."""
    assert W.BOOKKEEPING_COLUMNS == frozenset(
        {
            "ID",
            "UUID",
            "usn",
            "rb_local_usn",
            "rb_data_status",
            "rb_local_data_status",
            "rb_local_deleted",
            "rb_local_synced",
            "created_at",
            "updated_at",
        }
    )


def test_the_gridless_on_create_set_is_exactly_these_five_columns():
    """Removing one lets a row this product creates carry that analysis column."""
    assert W.GRIDLESS_ON_CREATE_COLUMNS == frozenset(
        {"BPM", "Analysed", "AnalysisDataPath", "AnalysisUpdated", "CueUpdated"}
    )


def test_the_unwritable_metadata_fields_are_exactly_these_three():
    """Removing one lets a metadata operation register that field."""
    assert set(metadata.UNWRITABLE_FIELDS) == {"KeyID", "ColorID", "Commnt"}


_CONSTRUCTOR = "Rekordbox6Database"


def _called_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _audit_database_opens(tree: ast.AST) -> tuple[int, list[tuple[int, str]]]:
    """Count the constructor calls in one module and say what is wrong with each.

    A reference that is not a call (an alias, a ``partial``) is itself a
    problem, since its arguments are supplied where this walk cannot see."""
    names = {_CONSTRUCTOR}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            names.update(
                alias.asname
                for alias in node.names
                if alias.name == _CONSTRUCTOR and alias.asname
            )
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _called_name(node.func) in names
    ]
    call_funcs = {id(call.func) for call in calls}

    problems: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if _called_name(node) in names and id(node) not in call_funcs:
            problems.append(
                (node.lineno, "the constructor is referenced without being called here")
            )
        elif isinstance(node, ast.Constant) and node.value == _CONSTRUCTOR:
            problems.append(
                (node.lineno, "the constructor is named in a string, a lookup this walk cannot follow")
            )
    for call in calls:
        if call.args:
            problems.append((call.lineno, "passes a positional argument; name the file with path="))
        path = next((kw.value for kw in call.keywords if kw.arg == "path"), None)
        if path is None:
            problems.append(
                (call.lineno, "passes no path=, so the binding opens the configured live library")
            )
        elif isinstance(path, ast.Constant) and not path.value:
            problems.append(
                (
                    call.lineno,
                    f"passes path={path.value!r}, which the binding reads as unset "
                    f"and replaces with the configured live library",
                )
            )
    return len(calls), problems


def test_every_database_open_in_src_names_the_file_it_opens():
    """R-15's related half. ``db_dir`` is not the database.

    The binding opens ``path``, and with ``path`` empty falls back to the
    configured live library; ``db_dir`` only names where it reads playlist XML
    and analysis paths. A call passing ``db_dir`` alone reads live rows while
    appearing to read a copy. This pins the argument, the cheap half; what the
    connection opened is a separate check, filed rather than made. Every
    module is parsed, since a string of the constructor's name can be joined
    from pieces no text search finds."""
    found = 0
    problems: list[str] = []
    for source in sorted((SRC_ROOT / "cratekit").rglob("*.py")):
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        count, bad = _audit_database_opens(tree)
        found += count
        problems.extend(f"{source.relative_to(SRC_ROOT)}:{line}: {why}" for line, why in bad)
    assert found, f"no {_CONSTRUCTOR} call in src; this check would pass by finding nothing"
    assert not problems, "\n".join(problems)


@pytest.mark.parametrize(
    "source, expected",
    [
        ("Rekordbox6Database(db_dir=str(copy), unlock=True)", "passes no path="),
        ("Rekordbox6Database(path=None)", "passes path=None"),
        ("Rekordbox6Database(path='')", "passes path=''"),
        ("Rekordbox6Database(str(copy))", "positional argument"),
        ("Rekordbox6Database(**options)", "passes no path="),
        ("pyrekordbox.Rekordbox6Database(db_dir=d)", "passes no path="),
        ("from pyrekordbox import Rekordbox6Database as Open\nOpen(db_dir=d)", "passes no path="),
        ("Open = Rekordbox6Database\nOpen(path=p)", "referenced without being called"),
        ("functools.partial(Rekordbox6Database, db_dir=d)", "referenced without being called"),
        ("getattr(pyrekordbox, 'Rekordbox6Database')()", "named in a string"),
    ],
)
def test_the_open_audit_refuses_each_shape_that_reads_live(source, expected):
    """The audit's own refusals, driven with literal sources, so the tree scan
    above cannot be green because the walk stopped recognising a call."""
    _count, problems = _audit_database_opens(ast.parse(source))
    assert any(expected in why for _line, why in problems), problems


def test_the_open_audit_accepts_the_shape_the_writer_uses():
    source = (
        "from pyrekordbox import Rekordbox6Database\n"
        "db = Rekordbox6Database(path=str(target), unlock=unlock)\n"
    )
    assert _audit_database_opens(ast.parse(source)) == (1, [])
