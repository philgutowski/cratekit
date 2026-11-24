"""The suite's disposable database is built once per worker and copied (U256).

Every caller still gets a file of its own that no other caller can see or change, and the file is
the database a build from nothing would make, its timestamps aside.
"""

from __future__ import annotations

import hashlib
import os
import sqlite3
import stat
from contextlib import closing
from pathlib import Path

import pytest
from sqlalchemy import MetaData

from cratekit.core import rb_writer as W
from tests import test_rb_writer_db as fixture


@pytest.fixture
def cold(monkeypatch):
    """No template built yet, every schema creation counted, the worker's cache kept."""
    monkeypatch.setattr(fixture, "_TEMPLATES", {})
    calls: list[int] = []
    real = MetaData.create_all

    def counted(self, *args, **kwargs):
        calls.append(1)
        return real(self, *args, **kwargs)

    monkeypatch.setattr(MetaData, "create_all", counted)
    return calls


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read(path: Path, statement: str) -> list[tuple]:
    """One query's rows from the file, read with no binding."""
    with closing(sqlite3.connect(path)) as conn:
        return conn.execute(statement).fetchall()


def _titles(path: Path) -> dict[str, str]:
    return dict(_read(path, "SELECT ID, Title FROM djmdContent ORDER BY ID"))


def _stamp_columns() -> dict[str, set[str]]:
    """Each table's timestamp columns, the binding's own date type, by table name."""
    from pyrekordbox.db6 import tables

    return {
        name: {column.name for column in table.columns if isinstance(column.type, tables.DateTime)}
        for name, table in tables.Base.metadata.tables.items()
    }


def _contents(path: Path) -> dict[str, object]:
    """Everything in the file, each timestamp read as whether it is set."""
    stamps = _stamp_columns()
    with closing(sqlite3.connect(path)) as conn:
        schema = sorted(conn.execute("SELECT type, name, tbl_name, sql FROM sqlite_master"))
        modes = {
            pragma: conn.execute(f"PRAGMA {pragma}").fetchone()[0]
            for pragma in ("journal_mode", "user_version", "application_id", "page_size")
        }
        rows: dict[str, list[tuple]] = {}
        for (table,) in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
            cursor = conn.execute(f'SELECT * FROM "{table}"')
            names = [column[0] for column in cursor.description]
            hidden = stamps.get(table, set())
            rows[table] = sorted(
                tuple(
                    (name, value is not None if name in hidden else value)
                    for name, value in zip(names, row, strict=True)
                )
                for row in cursor
            )
        return {"schema": schema, "modes": modes, "rows": rows}


def test_a_database_written_and_encrypted_leaves_its_sibling_and_the_next_untouched(tmp_path, cold):
    """One copy written, altered and encrypted leaves the copies before and after it."""
    first, second, after = (tmp_path / name / "master.db" for name in ("first", "second", "after"))
    fixture._build_disposable_database(first)
    fixture._build_disposable_database(second)
    before = _digest(second)
    with closing(sqlite3.connect(first)) as conn:
        conn.execute("UPDATE djmdContent SET Title = 'changed' WHERE ID = '1'")
        conn.execute("ALTER TABLE djmdContent ADD COLUMN u256_probe TEXT")
        conn.commit()
    fixture._encrypt_in_place(first)
    fixture._build_disposable_database(after)
    assert _digest(second) == before
    assert _titles(second) == {"1": "a track", "2": "another track"}
    assert _digest(after) == before
    assert not W.unlock_needed(after)
    assert W.unlock_needed(first)
    assert len(cold) == 1


@pytest.mark.parametrize("with_tag_category", [True, False], ids=["tagged", "untagged"])
def test_a_copy_is_the_database_a_build_from_nothing_makes(tmp_path, cold, with_tag_category):
    """Table by table and row by row, schema and journal mode with them, stamps aside."""
    copied = tmp_path / "copied" / "master.db"
    fixture._build_disposable_database(copied, with_tag_category=with_tag_category)
    built = tmp_path / "built" / "master.db"
    built.parent.mkdir()
    pin = W.pinned_db_version()
    fixture._build_from_nothing(built, with_tag_category=with_tag_category, db_version=pin)
    copy, scratch = _contents(copied), _contents(built)
    assert copy == scratch
    assert copy["modes"]["journal_mode"] == "wal"
    assert len(copy["rows"]["djmdMyTag"]) == (1 if with_tag_category else 0)
    assert not copied.with_name("master.db-wal").exists()


def test_each_variant_is_built_from_nothing_once_and_every_call_gets_its_own_file(tmp_path, cold):
    """The count the card asks for: one schema creation per variant, not one a call."""
    paths = []
    for index in range(4):
        for tagged in (True, False):
            path = tmp_path / f"{index}-{tagged}" / "master.db"
            fixture._build_disposable_database(path, with_tag_category=tagged)
            paths.append((path, tagged))
    assert len(cold) == 2
    assert len({path.stat().st_ino for path, _ in paths}) == len(paths)
    for path, tagged in paths:
        ((tags,),) = _read(path, "SELECT COUNT(*) FROM djmdMyTag")
        assert tags == (1 if tagged else 0)


def test_the_schema_pin_read_at_the_call_reaches_the_file(tmp_path, cold, monkeypatch):
    """A test that configures another pin before it builds finds that pin in its file."""
    shipped = W.pinned_db_version()
    fixture._build_disposable_database(tmp_path / "a" / "master.db")
    monkeypatch.setattr(W, "pinned_db_version", lambda *args, **kwargs: "5999")
    fixture._build_disposable_database(tmp_path / "b" / "master.db")
    monkeypatch.setattr(W, "pinned_db_version", lambda *args, **kwargs: shipped)
    fixture._build_disposable_database(tmp_path / "c" / "master.db")
    versions = {
        name: _read(tmp_path / name / "master.db", "SELECT DBVersion FROM djmdProperty")[0][0]
        for name in ("a", "b", "c")
    }
    assert versions == {"a": shipped, "b": "5999", "c": shipped}
    assert len(cold) == 2


@pytest.mark.parametrize("present", ["", "-wal", "-shm", "-journal"], ids=lambda s: s or "file")
def test_a_path_already_holding_a_file_is_built_from_nothing_as_before(tmp_path, cold, present):
    """Nothing already at the path is written over by a copy."""
    fixture._build_disposable_database(tmp_path / "warm" / "master.db")
    path = tmp_path / "db" / "master.db"
    path.parent.mkdir()
    Path(f"{path}{present}").write_bytes(b"")
    fixture._build_disposable_database(path)
    assert len(cold) == 2
    assert _titles(path) == {"1": "a track", "2": "another track"}


def test_a_second_build_over_the_same_database_still_refuses(tmp_path, cold):
    """Today's answer to a path that already holds the database, kept: it raises."""
    from sqlalchemy.exc import IntegrityError

    path = tmp_path / "db" / "master.db"
    fixture._build_disposable_database(path)
    with pytest.raises(IntegrityError):
        fixture._build_disposable_database(path)


@pytest.mark.parametrize("with_tag_category", [True, False], ids=["tagged", "untagged"])
def test_a_copy_carries_the_rows_the_safety_chain_reads(tmp_path, cold, with_tag_category):
    """The rows named here, so a row dropped from both build and copy is caught."""
    path = tmp_path / "db" / "master.db"
    fixture._build_disposable_database(path, with_tag_category=with_tag_category)
    unstamped = [
        (table, column)
        for table, columns in _stamp_columns().items()
        if table in ("agentRegistry", "djmdProperty", "djmdContent", "djmdMyTag")
        for column in sorted(columns)
        if column in ("created_at", "updated_at")
        and _read(path, f'SELECT COUNT(*) FROM "{table}" WHERE "{column}" IS NULL')[0][0]
    ]
    registry = _read(path, "SELECT registry_id, int_1 FROM agentRegistry ORDER BY registry_id")
    assert registry == [("localUpdateCount", 100)]
    assert _read(path, "SELECT DBID, DBVersion FROM djmdProperty") == [("1", W.pinned_db_version())]
    content = _read(path, "SELECT ID, Title, rb_local_deleted FROM djmdContent ORDER BY ID")
    assert content == [("1", "a track", 0), ("2", "another track", 0)]
    tags = _read(path, "SELECT ID, Name, Attribute, ParentID, Seq, UUID FROM djmdMyTag")
    assert tags == ([("10", "a category", 0, "0", 0, "category-uuid")] if with_tag_category else [])
    assert unstamped == []


def test_a_copy_has_the_mode_a_build_from_nothing_has_under_a_loose_umask(tmp_path, cold):
    """SQLite creates at 0644 before the umask, a plain create at 0666, told apart only under a
    looser umask than 022."""
    copied = tmp_path / "copied" / "master.db"
    built = tmp_path / "built" / "master.db"
    built.parent.mkdir()
    previous = os.umask(0o002)
    try:
        fixture._build_disposable_database(copied)
        fixture._build_from_nothing(built, with_tag_category=True, db_version=W.pinned_db_version())
    finally:
        os.umask(previous)
    assert stat.S_IMODE(copied.stat().st_mode) == stat.S_IMODE(built.stat().st_mode) == 0o644
