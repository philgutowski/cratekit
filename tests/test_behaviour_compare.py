"""Tests for ``scripts/behaviour_compare.py`` and the stage under ``tests/behaviour`` (U297).

The comparison is what a refactor shows instead of an argument: the branch
prints and writes what its base does. A comparison that misses a changed byte
certifies a behaviour change as none, and a capture that could run against a
real library would be worse than no capture. So each kind of difference is
planted alone in a capture small enough to read, each refusal is driven, and
one test runs the real capture twice over every shipped scenario.
"""

from __future__ import annotations

import datetime
import importlib.util
import json
import os
import secrets
import sqlite3
import subprocess
import sys
import time
import uuid
from pathlib import Path

import pytest

from tests import behaviour
from tests.behaviour import conftest as stage_fixtures

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "behaviour_compare.py"

#: The script as the stage loaded it, so a refusal raised there is the class caught here.
compare = stage_fixtures.compare

#: A path that is not inside the temporary directory wherever the checkout is: the
#: directory the temporary one sits in. Never created; the refusals only resolve it.
OUTSIDE = compare.temporary_directory().parent / "cratekit-outside-the-temporary-directory"

#: The two words a capture's process is known by: its id and when it started.
FIRST_PROCESS = ["3409", "1795265299.040"]
SECOND_PROCESS = ["3467", "1795265311.350"]


# ═══════════════════════════════════════════════════════════════════════════
# Building a capture small enough to read
# ═══════════════════════════════════════════════════════════════════════════


def _database(path: Path, rows: list[tuple[int, str]], *, tables: tuple[str, ...] = ("tracks",)):
    connection = sqlite3.connect(path)
    for table in tables:
        connection.execute(f"CREATE TABLE {table} (id INTEGER, title TEXT)")
    connection.executemany("INSERT INTO tracks VALUES (?, ?)", rows)
    connection.commit()
    connection.close()


def _world(root: Path, *, pid: str = FIRST_PROCESS[0]) -> Path:
    """One scenario's directory as a verb might leave it."""
    (root / "library" / "db").mkdir(parents=True)
    (root / "state" / "empty").mkdir(parents=True)
    (root / "library" / "routed.xml").write_text("<NODE Name='Low'/>\n", encoding="utf-8")
    (root / "library" / "audio.flac").write_bytes(b"fLaC\x00\xff\x00\x01tag=Deep House")
    (root / "state" / "lock.json").write_text(f'{{"pid": {pid}, "bytes": 8430}}', encoding="utf-8")
    _database(root / "library" / "db" / "master.db", [(1, "a track"), (2, "another track")])
    return root


def _commands(pid: str = FIRST_PROCESS[0]) -> list[dict]:
    return [
        {
            "argv": ["route", "--help"],
            "exit": 0,
            "stdout": "usage: crate route [-h]\n\nroute commands\n",
            "stderr": "",
        },
        {
            "argv": ["route", "inbox"],
            "exit": 0,
            "stdout": f"routed 3 tracks, held by process {pid}\n",
            "stderr": "",
        },
    ]


def _capture(
    folder: Path,
    *,
    root: Path | None = None,
    process: list[str] = FIRST_PROCESS,
    commands: list[dict] | None = None,
    change=None,
    name: str = "write/route",
) -> Path:
    """A finished capture of one scenario, written by the script's own recorder."""
    world = _world(folder / "world", pid=process[0])
    if change is not None:
        change(world)
    out = folder / "capture"
    compare.record_scenario(
        out, name, _commands(process[0]) if commands is None else commands, world, process
    )
    compare.write_manifest(
        out, root=root or Path("/tmp/a-root"), source="the working tree", checkout="", only=""
    )
    return out


def _pair(tmp_path: Path, **second) -> tuple[Path, Path]:
    """Two captures of the same world by two processes; ``second`` changes the second one."""
    first = _capture(tmp_path / "first")
    return first, _capture(tmp_path / "second", process=SECOND_PROCESS, **second)


def _compare(first: Path, second: Path, *extra: str) -> int:
    return compare.main(["behaviour_compare.py", "compare", str(first), str(second), *extra])


def _differences(first: Path, second: Path) -> list[str]:
    found, _ = compare.compare_captures(first, second)
    return [line for line in found if not line.startswith("    ")]


# ═══════════════════════════════════════════════════════════════════════════
# compare: equal, and each difference alone
# ═══════════════════════════════════════════════════════════════════════════


def test_two_captures_of_one_world_are_equal_though_two_processes_took_them(tmp_path, capsys):
    """The process id is in a file and in a line of output, and it is each capture's own."""
    first, second = _pair(tmp_path)
    assert json.loads((first / "write/route/process.json").read_text()) == FIRST_PROCESS
    assert _compare(first, second) == 0
    out = capsys.readouterr().out
    assert "1 scenarios, 2 commands, 8 files and 1 databases compared" in out
    assert out.rstrip().endswith("no difference")


def test_one_changed_byte_in_a_written_file_is_reported_with_its_offset(tmp_path, capsys):
    def flip(world: Path) -> None:
        path = world / "library" / "audio.flac"
        data = bytearray(path.read_bytes())
        data[7] ^= 0x01
        path.write_bytes(bytes(data))

    first, second = _pair(tmp_path, change=flip)
    assert _compare(first, second) == 1
    out = capsys.readouterr().out
    assert (
        "write/route: file library/audio.flac: bytes differ, first at offset 7 "
        "(22 bytes and 22)" in out
    )
    assert out.rstrip().endswith("1 difference(s)")


def test_a_changed_text_file_shows_the_line_that_changed(tmp_path, capsys):
    def reword(world: Path) -> None:
        (world / "library" / "routed.xml").write_text("<NODE Name='Med'/>\n", encoding="utf-8")

    first, second = _pair(tmp_path, change=reword)
    assert _compare(first, second) == 1
    out = capsys.readouterr().out
    assert "file library/routed.xml: bytes differ, first at offset 12" in out
    assert "    -<NODE Name='Low'/>" in out and "    +<NODE Name='Med'/>" in out


def test_one_changed_character_of_help_is_reported(tmp_path, capsys):
    commands = _commands(SECOND_PROCESS[0])
    commands[0]["stdout"] = commands[0]["stdout"].replace("route commands", "route command")
    first, second = _pair(tmp_path, commands=commands)
    assert _compare(first, second) == 1
    out = capsys.readouterr().out
    assert "write/route: command 1, `crate route --help`: stdout differs" in out
    assert "    -route commands" in out and "    +route command" in out
    assert out.rstrip().endswith("1 difference(s)")


def test_a_missing_final_newline_is_a_difference_and_says_how_the_texts_end(tmp_path, capsys):
    commands = _commands(SECOND_PROCESS[0])
    commands[0]["stdout"] = commands[0]["stdout"].rstrip("\n")
    first, second = _pair(tmp_path, commands=commands)
    assert _compare(first, second) == 1
    out = capsys.readouterr().out
    assert "stdout differs" in out and "second ends" in out


def test_one_changed_exit_code_is_reported(tmp_path, capsys):
    commands = _commands(SECOND_PROCESS[0])
    commands[1]["exit"] = 21
    first, second = _pair(tmp_path, commands=commands)
    assert _compare(first, second) == 1
    assert (
        "write/route: command 2, `crate route inbox`: exit code 0 became 21"
        in capsys.readouterr().out
    )


def test_a_changed_line_of_standard_error_is_reported(tmp_path):
    commands = _commands(SECOND_PROCESS[0])
    commands[1]["stderr"] = "warning: one track held\n"
    first, second = _pair(tmp_path, commands=commands)
    assert _differences(first, second) == [
        "write/route: command 2, `crate route inbox`: stderr differs"
    ]


def test_one_extra_file_is_reported_and_so_is_one_that_is_gone(tmp_path):
    def extra(world: Path) -> None:
        (world / "state" / "left-behind.tmp").write_text("x", encoding="utf-8")
        (world / "library" / "routed.xml").unlink()

    first, second = _pair(tmp_path, change=extra)
    assert _differences(first, second) == [
        "write/route: file library/routed.xml: only in the first capture",
        "write/route: file state/left-behind.tmp: only in the second capture",
    ]


def test_a_private_file_written_world_readable_is_reported(tmp_path, capsys):
    """The review's finding: 64 files went from 0600 to 0644 and nothing was said."""

    def private(mode: int):
        def change(world: Path) -> None:
            (world / "state" / "lock.json").chmod(mode)
            (world / "state" / "empty").chmod(0o700 if mode == 0o600 else 0o755)

        return change

    first = _capture(tmp_path / "first", change=private(0o600))
    second = _capture(tmp_path / "second", process=SECOND_PROCESS, change=private(0o644))
    assert _differences(first, second) == [
        "write/route: file state/empty: mode 0700 became 0755",
        "write/route: file state/lock.json: mode 0600 became 0644",
    ]
    assert _compare(first, second) == 1
    assert capsys.readouterr().out.rstrip().endswith("2 difference(s)")
    again = _capture(tmp_path / "third", process=SECOND_PROCESS, change=private(0o600))
    assert _differences(first, again) == []


def test_an_empty_directory_a_verb_made_is_an_entry_of_its_own(tmp_path):
    first, second = _pair(tmp_path, change=lambda world: (world / "state" / "empty").rmdir())
    assert _differences(first, second) == [
        "write/route: file state/empty: only in the first capture"
    ]


def test_a_file_that_became_a_directory_and_a_link_that_moved_are_reported(tmp_path):
    def reshape(world: Path) -> None:
        (world / "state" / "lock.json").unlink()
        (world / "state" / "lock.json").mkdir()
        (world / "library" / "current").unlink()
        (world / "library" / "current").symlink_to("audio.flac")

    first = _capture(
        tmp_path / "first",
        change=lambda world: (world / "library" / "current").symlink_to("routed.xml"),
    )
    second = _capture(tmp_path / "second", process=SECOND_PROCESS, change=lambda world: (
        (world / "library" / "current").symlink_to("routed.xml"), reshape(world)
    ))
    assert _differences(first, second) == [
        "write/route: file library/current: the link to routed.xml now points to audio.flac",
        "write/route: file state/lock.json: a file became a directory",
    ]


def test_one_missing_row_in_the_dump_is_reported_with_the_row(tmp_path, capsys):
    def drop(world: Path) -> None:
        path = world / "library" / "db" / "master.db"
        path.unlink()
        _database(path, [(1, "a track")])

    first, second = _pair(tmp_path, change=drop)
    assert _compare(first, second) == 1
    out = capsys.readouterr().out
    assert (
        "write/route: database library/db/master.db: table tracks: 1 row(s) only in the "
        "first capture" in out
    )
    assert '    {"id": 2, "title": "another track"}' in out
    assert out.rstrip().endswith("1 difference(s)")


def test_a_changed_cell_is_a_row_gone_and_a_row_come(tmp_path):
    def retitle(world: Path) -> None:
        connection = sqlite3.connect(world / "library" / "db" / "master.db")
        connection.execute("UPDATE tracks SET title = 'a trick' WHERE id = 1")
        connection.commit()
        connection.close()

    first, second = _pair(tmp_path, change=retitle)
    found, _ = compare.compare_captures(first, second)
    assert found == [
        "write/route: database library/db/master.db: table tracks: 1 row(s) only in the "
        "first capture",
        '    {"id": 1, "title": "a track"}',
        "write/route: database library/db/master.db: table tracks: 1 row(s) only in the "
        "second capture",
        '    {"id": 1, "title": "a trick"}',
    ]


def test_a_table_in_one_dump_only_is_reported(tmp_path):
    def more(world: Path) -> None:
        path = world / "library" / "db" / "master.db"
        path.unlink()
        _database(path, [(1, "a track"), (2, "another track")], tables=("tracks", "playlists"))

    first, second = _pair(tmp_path, change=more)
    assert _differences(first, second) == [
        "write/route: database library/db/master.db: schema: 1 declaration(s) only in the "
        "second capture",
        "write/route: database library/db/master.db: table playlists is only in the "
        "second capture",
    ]


def _rebuilt(statements: list[str]):
    """A change that builds the world's database again from these statements, same rows."""

    def change(world: Path) -> None:
        path = world / "library" / "db" / "master.db"
        path.unlink()
        connection = sqlite3.connect(path)
        for statement in statements:
            connection.execute(statement)
        connection.executemany(
            "INSERT INTO tracks VALUES (?, ?)", [(1, "a track"), (2, "another track")]
        )
        connection.commit()
        connection.close()

    return change


KEYED = "CREATE TABLE tracks (id INTEGER NOT NULL, title TEXT, PRIMARY KEY (id))"
INDEXED = "CREATE INDEX tracks_by_title ON tracks (title)"


@pytest.mark.parametrize(
    "base, changed, said",
    [
        # A primary key and a NOT NULL dropped: the same rows, another table.
        (
            [KEYED],
            ["CREATE TABLE tracks (id INTEGER, title TEXT)"],
            ["schema: 1 declaration(s) only in the first capture",
             "schema: 1 declaration(s) only in the second capture"],
        ),
        # An index dropped.
        ([KEYED, INDEXED], [KEYED], ["schema: 1 declaration(s) only in the first capture"]),
        # A view and a trigger added.
        (
            [KEYED],
            [KEYED, "CREATE VIEW titles AS SELECT title FROM tracks",
             "CREATE TRIGGER seen AFTER INSERT ON tracks BEGIN SELECT 1; END"],
            ["schema: 2 declaration(s) only in the second capture"],
        ),
        # A column added to a table: its rows read the same until one is written.
        (
            [KEYED],
            ["CREATE TABLE tracks (id INTEGER NOT NULL, title TEXT, PRIMARY KEY (id))",
             "CREATE TABLE empty (a INTEGER, b TEXT)"],
            ["schema: 1 declaration(s) only in the second capture",
             "table empty is only in the second capture"],
        ),
        ([KEYED], [KEYED, "PRAGMA user_version = 3"], ["user_version 0 became 3"]),
        ([KEYED], [KEYED, "PRAGMA application_id = 7"], ["application_id 0 became 7"]),
        ([KEYED], ["PRAGMA journal_mode = WAL", KEYED], ["journal_mode 'delete' became 'wal'"]),
    ],
)
def test_a_database_that_holds_the_same_rows_another_way_is_reported(
    tmp_path, base, changed, said
):
    """The review's finding: a dropped key, constraint and index compared as no difference."""
    first = _capture(tmp_path / "first", change=_rebuilt(base))
    second = _capture(tmp_path / "second", process=SECOND_PROCESS, change=_rebuilt(changed))
    assert _differences(first, second) == [
        f"write/route: database library/db/master.db: {line}" for line in said
    ]
    assert _differences(first, _capture(tmp_path / "third", change=_rebuilt(base))) == []


TABLE = (
    'CREATE TABLE "t" (\n\t"ID" VARCHAR(255) NOT NULL, \n\t"Name" VARCHAR(255) DEFAULT \'a, b\','
    ' \n\tPRIMARY KEY ("ID"), \n\tFOREIGN KEY("Name") REFERENCES "u" ("ID", "Other"),'
    ' \n\tFOREIGN KEY("ID") REFERENCES "v" ("ID")\n)'
)


def test_a_tables_constraints_are_read_in_one_order_and_its_columns_as_written():
    """The suite's own database builder writes its foreign keys in an order that changes."""
    other = TABLE.replace(
        'FOREIGN KEY("Name") REFERENCES "u" ("ID", "Other"), \n\tFOREIGN KEY("ID") REFERENCES "v" ("ID")',
        'FOREIGN KEY("ID") REFERENCES "v" ("ID"), \n\tFOREIGN KEY("Name") REFERENCES "u" ("ID", "Other")',
    )
    assert other != TABLE
    canonical = compare.canonical_declaration("table", TABLE)
    assert canonical == compare.canonical_declaration("table", other)
    assert canonical == (
        'CREATE TABLE "t" (\n\t"ID" VARCHAR(255) NOT NULL, \n\t"Name" VARCHAR(255) DEFAULT \'a, b\','
        ' FOREIGN KEY("ID") REFERENCES "v" ("ID"), FOREIGN KEY("Name") REFERENCES "u" ("ID", "Other"),'
        ' PRIMARY KEY ("ID"))'
    )


@pytest.mark.parametrize(
    "changed",
    [
        # A constraint dropped, a column's constraint dropped, the columns in another order.
        TABLE.replace(' \n\tPRIMARY KEY ("ID"),', ""),
        TABLE.replace(" NOT NULL", ""),
        TABLE.replace(
            '"ID" VARCHAR(255) NOT NULL, \n\t"Name" VARCHAR(255) DEFAULT \'a, b\'',
            '"Name" VARCHAR(255) DEFAULT \'a, b\', \n\t"ID" VARCHAR(255) NOT NULL',
        ),
        TABLE.replace('REFERENCES "v" ("ID")', 'REFERENCES "w" ("ID")'),
    ],
)
def test_one_order_for_the_constraints_hides_nothing_else(changed):
    assert changed != TABLE
    assert compare.canonical_declaration("table", changed) != compare.canonical_declaration(
        "table", TABLE
    )


NAMED_LIKE = "CREATE TABLE t (a INTEGER, checksum TEXT, unique_key TEXT, PRIMARY KEY (a), UNIQUE (a))"


def test_a_column_named_like_a_constraint_is_a_column_and_keeps_its_place():
    """The review's finding: ``checksum`` and ``unique_key`` were read as constraints.

    Two such columns swapped in an empty table compared as no difference.
    """
    swapped = NAMED_LIKE.replace("checksum TEXT, unique_key TEXT", "unique_key TEXT, checksum TEXT")
    canonical = compare.canonical_declaration("table", NAMED_LIKE)
    assert canonical != compare.canonical_declaration("table", swapped)
    assert canonical == "CREATE TABLE t (a INTEGER, checksum TEXT, unique_key TEXT, PRIMARY KEY (a), UNIQUE (a))"
    reordered = NAMED_LIKE.replace("PRIMARY KEY (a), UNIQUE (a)", "UNIQUE (a), PRIMARY KEY (a)")
    assert compare.canonical_declaration("table", reordered) == canonical


@pytest.mark.parametrize(
    "item, constraint",
    [
        (' \n\tPRIMARY KEY ("ID")', True),
        ("primary  key(a)", True),
        ("CONSTRAINT fk FOREIGN KEY (a) REFERENCES u (a)", True),
        ("FOREIGN KEY(a) REFERENCES u (a)", True),
        ("UNIQUE (a, b)", True),
        ("check (a > 0)", True),
        ("checksum TEXT", False),
        ("unique_key TEXT UNIQUE", False),
        ("constraint_name TEXT", False),
        ("primary_key INTEGER PRIMARY KEY", False),
        ('"check" TEXT', False),
    ],
)
def test_a_constraint_is_told_from_a_column_by_what_follows_its_keyword(item, constraint):
    assert bool(compare.TABLE_CONSTRAINT.match(item)) is constraint


def test_a_declaration_is_split_at_its_own_commas_only():
    sql = "CREATE TABLE \"t,x\" (a TEXT DEFAULT 'p, q', b NUMERIC(10, 2), [c,d] TEXT, CHECK (a IN ('x', 'y'))) STRICT"
    head, items, tail = compare.split_declaration(sql)
    assert head == 'CREATE TABLE "t,x" ('
    assert items == [
        "a TEXT DEFAULT 'p, q'", " b NUMERIC(10, 2)", " [c,d] TEXT", " CHECK (a IN ('x', 'y'))"
    ]
    assert tail == ") STRICT"
    assert compare.split_declaration("CREATE TABLE t") is None
    assert compare.split_declaration("CREATE TABLE t (a, b") is None


@pytest.mark.parametrize(
    "kind, sql",
    [
        ("index", "CREATE INDEX i ON t (a, b)"),
        ("table", None),
        ("table", "CREATE TABLE t (a INTEGER, PRIMARY KEY (a))"),
        ("table", "CREATE TABLE t (a INTEGER, CHECK (a > 0), UNIQUE (a"),
        ("table", "CREATE VIRTUAL TABLE t USING fts5"),
    ],
)
def test_a_declaration_that_is_no_table_or_has_one_constraint_or_none_is_left_as_written(
    kind, sql
):
    assert compare.canonical_declaration(kind, sql) == sql


def _broken(junk: bytes):
    def change(world: Path) -> None:
        (world / "library" / "db" / "master.db").write_bytes(compare.SQLITE_HEADER + junk)

    return change


def test_a_database_neither_capture_can_dump_is_compared_by_its_bytes(tmp_path, capsys):
    """The review's finding: two unreadable databases with one error text compared clean."""
    first = _capture(tmp_path / "first", change=_broken(b"not pages at all"))
    same = _capture(tmp_path / "second", process=SECOND_PROCESS, change=_broken(b"not pages at all"))
    other = _capture(tmp_path / "third", process=SECOND_PROCESS, change=_broken(b"other bytes here"))
    dump = json.loads((first / "write/route/databases.json").read_text())
    assert "unreadable" in dump["library/db/master.db"]
    assert _differences(first, same) == []
    [found] = _differences(first, other)
    assert found.startswith(
        "write/route: file library/db/master.db: the database could not be dumped ("
    )
    assert found.endswith("and its bytes differ (32 bytes and 32)")
    # One side readable and the other not: the bytes differ, and that is said.
    readable = _capture(tmp_path / "fourth", process=SECOND_PROCESS)
    [found] = _differences(first, readable)
    assert "could not be dumped" in found and "its bytes differ" in found
    assert _compare(first, other) == 1
    assert capsys.readouterr().out.rstrip().endswith("1 difference(s)")


def test_a_database_is_compared_by_its_rows_and_not_by_its_bytes(tmp_path):
    """The same rows written in the other order: other bytes, the same dump, no difference."""

    def reorder(world: Path) -> None:
        path = world / "library" / "db" / "master.db"
        path.unlink()
        _database(path, [(2, "another track"), (1, "a track")])

    first, second = _pair(tmp_path, change=reorder)
    listed = [json.loads((one / "write/route/files.json").read_text()) for one in (first, second)]
    assert listed[0]["library/db/master.db"]["kind"] == "database"
    assert listed[0]["library/db/master.db"]["sha256"] != listed[1]["library/db/master.db"]["sha256"]
    assert _differences(first, second) == []


def test_the_dump_reads_rows_still_in_the_wal_and_a_sidecars_bytes_are_not_compared(tmp_path):
    """A connection left open keeps its rows in the WAL, which is salted at random."""
    kept = []

    def leave_open(world: Path) -> None:
        connection = sqlite3.connect(world / "library" / "db" / "master.db")
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("INSERT INTO tracks VALUES (3, 'in the wal')")
        connection.commit()
        kept.append(connection)

    first = _capture(tmp_path / "first", change=leave_open)
    second = _capture(tmp_path / "second", process=SECOND_PROCESS, change=leave_open)
    listing = json.loads((first / "write/route/files.json").read_text())
    assert listing["library/db/master.db-wal"]["kind"] == "database sidecar"
    assert listing["library/db/master.db-shm"]["kind"] == "database sidecar"
    dump = json.loads((first / "write/route/databases.json").read_text())
    assert '{"id": 3, "title": "in the wal"}' in dump["library/db/master.db"]["tables"]["tracks"]
    assert (first / "write/route/tree/library/db/master.db-wal").read_bytes() != (
        second / "write/route/tree/library/db/master.db-wal"
    ).read_bytes()
    assert _differences(first, second) == []
    for connection in kept:
        connection.close()


def test_a_file_that_only_ends_like_a_sidecar_is_compared_as_a_file(tmp_path):
    """Beside nothing, and beside a file that is not a database: its bytes are compared."""

    def stray(text: str):
        def change(world: Path) -> None:
            (world / "state" / "notes-wal").write_text("x", encoding="utf-8")
            (world / "state" / "plain").write_text("not a database", encoding="utf-8")
            (world / "state" / "plain-wal").write_text(text, encoding="utf-8")

        return change

    first = _capture(tmp_path / "first", change=stray("one"))
    second = _capture(tmp_path / "second", process=SECOND_PROCESS, change=stray("two"))
    listing = json.loads((first / "write/route/files.json").read_text())
    assert listing["state/notes-wal"]["kind"] == "file"
    assert listing["state/plain-wal"]["kind"] == "file"
    [found] = _differences(first, second)
    assert found.startswith("write/route: file state/plain-wal: bytes differ")


def test_a_scenario_in_one_capture_only_is_reported(tmp_path):
    first = _capture(tmp_path / "first")
    second = _capture(tmp_path / "second", process=SECOND_PROCESS, name="write/other")
    assert _differences(first, second) == [
        "write/other: the scenario is only in the second capture",
        "write/route: the scenario is only in the first capture",
    ]


def test_one_command_more_is_reported_once_and_the_rest_are_still_compared(tmp_path):
    """A new verb's help in the middle must not turn every later command into noise."""
    commands = _commands(SECOND_PROCESS[0])
    commands.insert(
        1, {"argv": ["route", "new", "--help"], "exit": 0, "stdout": "usage\n", "stderr": ""}
    )
    commands[2]["exit"] = 3
    first, second = _pair(tmp_path, commands=commands)
    assert _differences(first, second) == [
        "write/route: command 2, `crate route new --help`: only in the second capture",
        "write/route: command 2, `crate route inbox`: exit code 0 became 3",
    ]


def test_a_long_difference_is_cut_unless_asked_for_whole(tmp_path, capsys):
    commands = _commands(SECOND_PROCESS[0])
    commands[0]["stdout"] = "".join(f"line {n}\n" for n in range(200))
    first, second = _pair(tmp_path, commands=commands)
    assert _compare(first, second) == 1
    cut = capsys.readouterr().out
    assert "more lines" in cut and "+line 199" not in cut
    assert _compare(first, second, "--full") == 1
    assert "+line 199" in capsys.readouterr().out


# ═══════════════════════════════════════════════════════════════════════════
# The one declared equivalence: a capture's own words
# ═══════════════════════════════════════════════════════════════════════════

WORDS = [("3409", "3467"), ("1795265299.040", "1795265311.350")]


@pytest.mark.parametrize(
    "first, second, same",
    [
        ("pid 3409", "pid 3467", True),
        ("pid 3409 started 1795265299.040", "pid 3467 started 1795265311.350", True),
        # A number that merely equals the first capture's process id is the same in both.
        ("3409 bytes, pid 3409", "3409 bytes, pid 3467", True),
        # The same number changed anywhere else is a difference.
        ("8430 bytes, pid 3409", "8431 bytes, pid 3467", False),
        # The second capture's word where the first held none is a difference.
        ("pid none", "pid 3467", False),
        # A word of one kind where the other kind stood is a difference.
        ("started 1795265299.040", "started 3467", False),
        ("pid 3409\n", "pid 3467", False),
        ("", "", True),
        # The review's finding: a word inside a longer token is that token.
        ("wrote 134091 bytes", "wrote 134671 bytes", False),
        ("sha 9f3409c", "sha 9f3467c", False),
        ("lock_3409", "lock_3467", False),
        # Each end alone: only what precedes it, then only what follows it.
        ("pid 13409", "pid 13467", False),
        ("pid 34091", "pid 34671", False),
        ("pid x3409", "pid x3467", False),
        ("pid 3409x", "pid 3467x", False),
        # Whole, against punctuation, a path or the end of a sentence, it is the word.
        ("process 3409.", "process 3467.", True),
        ("/proc/3409/stat", "/proc/3467/stat", True),
        ('{"pid": 3409, "started": "1795265299.040"}', '{"pid": 3467, "started": "1795265311.350"}', True),
        ("3409", "3467", True),
    ],
)
def test_two_texts_are_the_same_only_where_each_holds_its_own_word(first, second, same):
    assert compare.same_but_for(first, second, WORDS) is same


def test_a_word_that_stands_for_two_things_keeps_both_counterparts():
    """A process id that is also some file's inode, in the first capture only."""
    words = [("3409", "3467"), ("3409", "650001")]
    assert compare.same_but_for("pid 3409, inode 3409", "pid 3467, inode 650001", words) is True
    assert compare.same_but_for("pid 3409", "pid 3468", words) is False


def test_with_no_words_only_equal_texts_are_the_same():
    assert compare.same_but_for("pid 3409", "pid 3409", []) is True
    assert compare.same_but_for("pid 3409", "pid 3467", []) is False
    assert compare.same_but_for("pid 3409", "pid 3467", [("3409", "3409")]) is False


def test_a_files_inode_written_into_a_row_is_read_past_by_path(tmp_path):
    """rekordbox loads a row by its file's inode, which is whatever the disk handed out."""

    def record_inode(world: Path) -> None:
        inode = (world / "library" / "audio.flac").stat().st_ino
        other = (world / "library" / "routed.xml").stat().st_ino
        connection = sqlite3.connect(world / "library" / "db" / "master.db")
        connection.execute("INSERT INTO tracks VALUES (?, 'the landed file')", (inode,))
        connection.commit()
        connection.close()
        (world / "state" / "inode.txt").write_text(f"{inode} and not {other}", encoding="utf-8")

    first = _capture(tmp_path / "first", change=record_inode)
    second = _capture(tmp_path / "second", process=SECOND_PROCESS, change=record_inode)
    one = (tmp_path / "first/world/library/audio.flac").stat().st_ino
    two = (tmp_path / "second/world/library/audio.flac").stat().st_ino
    assert one != two, "the two worlds were handed one inode, so this proves nothing"
    assert _differences(first, second) == []


def test_another_files_inode_in_that_row_is_a_difference(tmp_path):
    def record(name: str):
        def change(world: Path) -> None:
            inode = (world / "library" / name).stat().st_ino
            (world / "state" / "inode.txt").write_text(f"row file {inode}", encoding="utf-8")

        return change

    first = _capture(tmp_path / "first", change=record("audio.flac"))
    second = _capture(tmp_path / "second", process=SECOND_PROCESS, change=record("routed.xml"))
    [found] = _differences(first, second)
    assert found.startswith("write/route: file state/inode.txt: bytes differ, first at offset ")


# ═══════════════════════════════════════════════════════════════════════════
# compare: what it will not read
# ═══════════════════════════════════════════════════════════════════════════


def test_captures_taken_under_two_roots_are_refused(tmp_path, capsys):
    first = _capture(tmp_path / "first")
    second = _capture(tmp_path / "second", process=SECOND_PROCESS, root=Path("/tmp/another-root"))
    assert _compare(first, second) == 2
    assert "taken under different roots" in capsys.readouterr().err


def test_a_directory_with_no_manifest_is_not_a_capture(tmp_path, capsys):
    first = _capture(tmp_path / "first")
    unfinished = _capture(tmp_path / "second")
    (unfinished / compare.MANIFEST).unlink()
    assert _compare(first, unfinished) == 2
    assert "holds no manifest, so it is not a finished capture" in capsys.readouterr().err
    assert _compare(unfinished, first) == 2


@pytest.mark.parametrize(
    "manifest, why",
    [
        ({"format": 99, "scenarios": [], "root": "/tmp/a-root"}, "is not a capture this script"),
        ({"format": 1, "root": "/tmp/a-root"}, "names no scenarios or no root"),
        ({"format": 1, "scenarios": []}, "names no scenarios or no root"),
        ([1], "is not a capture this script"),
    ],
)
def test_a_manifest_of_another_form_is_refused(tmp_path, capsys, manifest, why):
    first = _capture(tmp_path / "first")
    other = _capture(tmp_path / "second")
    (other / compare.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
    assert _compare(first, other) == 2
    assert why in capsys.readouterr().err


def test_two_scenarios_of_one_name_are_refused_rather_than_merged(tmp_path):
    out = _capture(tmp_path / "first")
    with pytest.raises(compare.Refusal, match="two scenarios share a name"):
        compare.record_scenario(out, "write/route", [], tmp_path / "first" / "world", [])


def test_a_partial_capture_says_so_in_what_was_compared(tmp_path):
    first, second = _pair(tmp_path)
    manifest = json.loads((second / compare.MANIFEST).read_text())
    manifest["only"] = "help"
    (second / compare.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
    _, summary = compare.compare_captures(first, second)
    assert "the second capture is partial, taken with --only help" in summary
    assert "first capture is partial" not in summary


def test_a_capture_taken_with_another_python_says_so(tmp_path):
    first, second = _pair(tmp_path)
    manifest = json.loads((second / compare.MANIFEST).read_text())
    manifest["python"] = "3.99.0"
    (second / compare.MANIFEST).write_text(json.dumps(manifest), encoding="utf-8")
    _, summary = compare.compare_captures(first, second)
    assert "taken with Python" in summary and "3.99.0" in summary


# ═══════════════════════════════════════════════════════════════════════════
# capture: what it refuses before anything runs
# ═══════════════════════════════════════════════════════════════════════════


@pytest.fixture
def no_run(monkeypatch):
    """Fail the test if a capture gets as far as starting its scenario run."""

    def refused(*args, **kwargs):
        raise AssertionError(f"the capture started a process: {args}")

    monkeypatch.setattr(compare.subprocess, "run", refused)


def _capture_main(*argv: str) -> int:
    return compare.main(["behaviour_compare.py", "capture", *argv])


def _checkout(tmp_path: Path, *scenario_files: str) -> Path:
    """A checkout with these scenario files and an empty source, for a run that is faked."""
    root = tmp_path / "checkout"
    (root / "src").mkdir(parents=True, exist_ok=True)
    (root / "tests" / "behaviour").mkdir(parents=True, exist_ok=True)
    for name in ("conftest.py", "__init__.py", *scenario_files):
        (root / "tests" / "behaviour" / name).write_text("", encoding="utf-8")
    return root


def _capture_in(checkout: Path, *argv: str) -> int:
    return compare.main(["behaviour_compare.py", "--repo-root", str(checkout), "capture", *argv])


def test_a_root_outside_the_temporary_directory_is_refused_before_anything_runs(
    tmp_path, capsys, no_run
):
    """The one thing between a capture and somebody's library is where its root is."""
    outside = OUTSIDE / "root"
    assert _capture_main("--out", str(tmp_path / "out"), "--root", str(outside)) == 2
    err = capsys.readouterr().err
    assert "the capture root is" in err and "not inside the temporary directory" in err
    assert not outside.exists() and not (tmp_path / "out").exists()


def test_the_temporary_directory_itself_is_no_root(tmp_path, capsys, no_run):
    whole = compare.temporary_directory()
    assert _capture_main("--out", str(tmp_path / "out"), "--root", str(whole)) == 2
    assert "not inside the temporary directory" in capsys.readouterr().err


def test_a_link_inside_the_temporary_directory_that_leads_out_of_it_is_refused(tmp_path):
    link = tmp_path / "looks-temporary"
    link.symlink_to(compare.temporary_directory().parent)
    with pytest.raises(compare.Refusal, match="not inside the temporary directory"):
        compare.refuse_outside_temporary(link / OUTSIDE.name, "the capture root")
    compare.refuse_outside_temporary(tmp_path / "plain", "the capture root")


@pytest.mark.parametrize("where", ["", "-source/out", "/out"])
def test_an_out_directory_the_run_would_empty_is_refused(tmp_path, capsys, no_run, where):
    root = tmp_path / "root"
    out = Path(str(root) + where)
    assert _capture_main("--out", str(out), "--root", str(root)) == 2
    assert "is inside the capture's own root" in capsys.readouterr().err


def test_an_out_directory_that_already_holds_something_is_refused(tmp_path, capsys, no_run):
    out = tmp_path / "out"
    out.mkdir()
    (out / "earlier").write_text("x", encoding="utf-8")
    assert _capture_main("--out", str(out), "--root", str(tmp_path / "root")) == 2
    assert "is not empty" in capsys.readouterr().err
    assert (out / "earlier").read_text(encoding="utf-8") == "x"


def test_a_root_a_running_capture_holds_is_refused_and_a_dead_ones_is_taken(tmp_path):
    root = tmp_path / "root"
    holder = root.with_name("root-holder")
    holder.write_text(f"{os.getppid()}\n", encoding="utf-8")
    with pytest.raises(compare.Refusal, match=f"still running, process {os.getppid()}"):
        compare.take_root(root)
    assert holder.read_text(encoding="utf-8") == f"{os.getppid()}\n"

    gone = subprocess.Popen([sys.executable, "-c", "pass"])
    gone.wait()
    holder.write_text(f"{gone.pid}\n", encoding="utf-8")
    assert compare.take_root(root) == holder
    assert holder.read_text(encoding="utf-8") == f"{os.getpid()}\n"


def test_a_root_that_holds_somebodys_files_is_refused_and_left_alone(tmp_path, capsys, no_run):
    """The review's finding: a directory named as the root was emptied without a word."""
    root = tmp_path / "somebodys"
    root.mkdir()
    (root / "notes.txt").write_text("kept", encoding="utf-8")
    assert _capture_main("--out", str(tmp_path / "out"), "--root", str(root)) == 2
    assert "holds files no capture left there" in capsys.readouterr().err
    assert (root / "notes.txt").read_text(encoding="utf-8") == "kept"
    assert not root.with_name("somebodys-holder").exists()


def test_a_root_a_capture_left_is_taken_again(tmp_path):
    """A capture's own mark, or the holder of a capture that died, says whose it is."""
    marked = tmp_path / "marked"
    marked.mkdir()
    (marked / "leftover").write_text("x", encoding="utf-8")
    (marked / compare.LEFT_BY_A_CAPTURE).write_text("", encoding="utf-8")
    assert compare.take_root(marked).name == "marked-holder"

    died = tmp_path / "died"
    died.mkdir()
    (died / "leftover").write_text("x", encoding="utf-8")
    gone = subprocess.Popen([sys.executable, "-c", "pass"])
    gone.wait()
    died.with_name("died-holder").write_text(f"{gone.pid}\n", encoding="utf-8")
    assert compare.take_root(died).read_text(encoding="utf-8") == f"{os.getpid()}\n"

    empty = tmp_path / "empty"
    empty.mkdir()
    assert compare.take_root(empty).name == "empty-holder"


def test_a_file_that_is_only_named_like_a_holder_vouches_for_nothing(tmp_path):
    """The review's finding: any file of that name made a directory a capture's to empty."""
    root = tmp_path / "theirs"
    root.mkdir()
    (root / "notes.txt").write_text("kept", encoding="utf-8")
    root.with_name("theirs-holder").write_text("somebody's own file", encoding="utf-8")
    with pytest.raises(compare.Refusal, match="holds files no capture left there"):
        compare.take_root(root)
    assert (root / "notes.txt").read_text(encoding="utf-8") == "kept"
    assert root.with_name("theirs-holder").read_text(encoding="utf-8") == "somebody's own file"


def test_the_directory_beside_the_root_is_not_emptied_either(tmp_path, capsys, no_run):
    """The review's finding, one directory over: the source's place held somebody's files."""
    root = tmp_path / "root"
    beside = compare.source_directory(root)
    beside.mkdir()
    (beside / "theirs.txt").write_text("kept", encoding="utf-8")
    assert _capture_main("--out", str(tmp_path / "out"), "--root", str(root)) == 2
    assert f"{beside} holds files no capture left there" in capsys.readouterr().err
    assert (beside / "theirs.txt").read_text(encoding="utf-8") == "kept"


def test_the_source_a_capture_places_is_marked_as_its_own(checkout, tmp_path):
    target = tmp_path / "placed"
    compare.place_source(checkout, None, target)
    assert compare.left_by_a_capture(target, tmp_path / "no-holder")
    compare.place_source(checkout, "HEAD", target)
    assert (target / compare.LEFT_BY_A_CAPTURE).is_file()


def test_a_failed_run_marks_the_root_it_leaves_behind(tmp_path, monkeypatch, capsys):
    root = tmp_path / "root"

    def failed(command, **_):
        (root / "test_a_scenario0").mkdir(parents=True)
        return subprocess.CompletedProcess(command, 1, "1 failed", "")

    monkeypatch.setattr(compare.subprocess, "run", failed)
    assert _capture_main("--out", str(tmp_path / "out"), "--root", str(root)) == 1
    assert (root / compare.LEFT_BY_A_CAPTURE).is_file()
    assert f"is left under {root} for reading" in capsys.readouterr().out
    # So the next capture may empty it.
    assert compare.take_root(root).name == "root-holder"


def test_a_run_stopped_at_its_timeout_leaves_a_root_the_next_capture_may_take(
    tmp_path, monkeypatch, capsys
):
    """The review's finding on the refusal: it fired on a root a capture itself left."""
    root = tmp_path / "root"

    def hung(command, *, timeout, **_):
        (root / "test_a_scenario0").mkdir(parents=True)
        raise subprocess.TimeoutExpired(command, timeout)

    monkeypatch.setattr(compare.subprocess, "run", hung)
    assert _capture_main("--out", str(tmp_path / "out"), "--root", str(root)) == 1
    assert f"is left under {root} for reading" in capsys.readouterr().out
    assert (root / compare.LEFT_BY_A_CAPTURE).is_file()
    assert compare.take_root(root).name == "root-holder"


def test_a_kept_capture_leaves_a_root_and_a_source_the_next_capture_may_take(
    tmp_path, monkeypatch
):
    out = tmp_path / "out"
    root = tmp_path / "root"
    checkout = _checkout(tmp_path, "write.py")
    passing = _passing_run(out, tmp_path, ["write/route"])

    def run(command, **kwargs):
        if command[0] != "git":
            (root / "test_a_scenario0").mkdir(parents=True)
        return passing(command, **kwargs)

    monkeypatch.setattr(compare.subprocess, "run", run)
    assert _capture_in(checkout, "--out", str(out), "--root", str(root), "--keep") == 0
    assert (root / "test_a_scenario0").is_dir() and compare.source_directory(root).is_dir()
    holder = compare.take_root(root)
    assert holder.name == "root-holder"


def test_a_holder_that_names_no_process_is_taken_over(tmp_path):
    root = tmp_path / "root"
    root.with_name("root-holder").write_text("not a pid", encoding="utf-8")
    assert compare.take_root(root).read_text(encoding="utf-8") == f"{os.getpid()}\n"


def test_a_capture_releases_its_root_when_its_run_fails(tmp_path, monkeypatch, capsys):
    """The run exits nonzero and records nothing: no manifest, and the next capture may start."""
    monkeypatch.setattr(
        compare.subprocess,
        "run",
        lambda command, **_: subprocess.CompletedProcess(command, 1, "a scenario failed", ""),
    )
    root = tmp_path / "root"
    out = tmp_path / "out"
    assert _capture_main("--out", str(out), "--root", str(root)) == 1
    said = capsys.readouterr().out
    assert "exited 1 with 0 scenarios recorded" in said and "a scenario failed" in said
    assert not (out / compare.MANIFEST).exists()
    assert not root.with_name("root-holder").exists()
    assert not compare.source_directory(root).exists()


def test_a_run_that_failed_after_recording_a_scenario_is_not_a_capture(
    tmp_path, monkeypatch, capsys
):
    """One scenario recorded, the next failed: what is there must not read as finished."""
    out = tmp_path / "out"

    def half(command, **_):
        compare.record_scenario(out, "write/route", _commands(), _world(tmp_path / "w"), [])
        return subprocess.CompletedProcess(command, 1, "1 failed, 1 passed", "")

    monkeypatch.setattr(compare.subprocess, "run", half)
    assert _capture_main("--out", str(out), "--root", str(tmp_path / "root")) == 1
    assert "exited 1 with 1 scenarios recorded" in capsys.readouterr().out
    assert not (out / compare.MANIFEST).exists()
    assert _compare(out, out) == 2


def _passing_run(out: Path, tmp_path: Path, expected):
    """A scenario run that exits 0, records one scenario and lists ``expected``."""

    def run(command, **_):
        if command[0] == "git":  # the manifest's reading of the checkout's commit
            return subprocess.CompletedProcess(command, 0, b"", b"")
        compare.record_scenario(out, "write/route", _commands(), _world(tmp_path / "w"), [])
        if expected is not None:
            compare.write_json(out / compare.EXPECTED, expected)
        return subprocess.CompletedProcess(command, 0, "1 passed, 1 skipped", "")

    return run


def test_a_scenario_that_ran_and_left_no_record_keeps_the_capture_open(
    tmp_path, monkeypatch, capsys
):
    """The review's finding: a skipped scenario passed the run and the capture closed short."""
    out = tmp_path / "out"
    monkeypatch.setattr(
        compare.subprocess, "run", _passing_run(out, tmp_path, ["write/route", "write/skipped"])
    )
    checkout = _checkout(tmp_path, "write.py")
    assert _capture_in(checkout, "--out", str(out), "--root", str(tmp_path / "root")) == 1
    said = capsys.readouterr().out
    assert "exited 0 with 1 scenarios recorded; write/skipped left no record" in said
    assert not (out / compare.MANIFEST).exists()


def test_a_scenario_file_that_collected_nothing_keeps_the_capture_open(
    tmp_path, monkeypatch, capsys
):
    """The review's second finding on records: a file skipped as it was imported.

    Its fixtures come from a test module that skips itself where an extra is
    absent, so the file collects no scenario, the run's list never names one,
    and base and branch would compare clean without it. Every scenario file
    the run was handed must have left a record.
    """
    out = tmp_path / "out"
    monkeypatch.setattr(compare.subprocess, "run", _passing_run(out, tmp_path, ["write/route"]))
    checkout = _checkout(tmp_path, "write.py", "analysis.py")
    assert _capture_in(checkout, "--out", str(out), "--root", str(tmp_path / "root")) == 1
    said = capsys.readouterr().out
    assert (
        "every scenario of tests/behaviour/analysis.py (none of it was collected or "
        "recorded) left no record" in said
    )
    assert not (out / compare.MANIFEST).exists()


def test_a_capture_asked_for_part_of_the_scenarios_owes_no_record_for_the_other_files(
    tmp_path, monkeypatch
):
    out = tmp_path / "out"
    monkeypatch.setattr(compare.subprocess, "run", _passing_run(out, tmp_path, ["write/route"]))
    checkout = _checkout(tmp_path, "write.py", "analysis.py")
    argv = ("--out", str(out), "--root", str(tmp_path / "root"), "--only", "route")
    assert _capture_in(checkout, *argv) == 0
    assert json.loads((out / compare.MANIFEST).read_text())["only"] == "route"


@pytest.mark.parametrize("expected", [None, {"write/route": True}])
def test_a_run_that_did_not_list_what_it_collected_is_not_a_capture(
    tmp_path, monkeypatch, capsys, expected
):
    """No list, or one that is not a list: the scenarios cannot be counted, which is not all."""
    out = tmp_path / "out"
    monkeypatch.setattr(compare.subprocess, "run", _passing_run(out, tmp_path, expected))
    checkout = _checkout(tmp_path, "write.py")
    assert _capture_in(checkout, "--out", str(out), "--root", str(tmp_path / "root")) == 1
    assert "every scenario (the run" in capsys.readouterr().out
    assert not (out / compare.MANIFEST).exists()


def test_a_run_that_recorded_everything_it_collected_is_closed(tmp_path, monkeypatch, capsys):
    out = tmp_path / "out"
    monkeypatch.setattr(compare.subprocess, "run", _passing_run(out, tmp_path, ["write/route"]))
    checkout = _checkout(tmp_path, "write.py")
    assert _capture_in(checkout, "--out", str(out), "--root", str(tmp_path / "root")) == 0
    assert "captured 1 scenarios and 2 commands from the working tree" in capsys.readouterr().out
    assert json.loads((out / compare.MANIFEST).read_text())["scenarios"] == ["write/route"]


def test_the_scenario_run_is_handed_a_clean_environment_and_one_hash_seed(
    tmp_path, monkeypatch
):
    """A capture started inside a parallel worker must not hand its child that worker."""
    seen = {}

    def run(command, *, env, timeout, **_):
        seen.update(env=env, timeout=timeout)
        return subprocess.CompletedProcess(command, 1, "", "")

    monkeypatch.setattr(compare.subprocess, "run", run)
    monkeypatch.setenv("PYTEST_ADDOPTS", "-x")
    monkeypatch.setenv("PYTEST_XDIST_WORKER", "gw0")
    root, out = tmp_path / "root", tmp_path / "out"
    assert _capture_main("--out", str(out), "--root", str(root), "--timeout", "77") == 1
    env = seen["env"]
    assert not {"PYTEST_ADDOPTS", "PYTEST_XDIST_WORKER", "PYTEST_CURRENT_TEST"} & set(env)
    assert env["PYTHONHASHSEED"] == "0" and env["PYTHONDONTWRITEBYTECODE"] == "1"
    assert env[compare.ENV_OUT] == str(out)
    assert env[compare.ENV_SOURCE] == str(compare.source_directory(root.resolve()) / "src")
    assert seen["timeout"] == 77


def test_a_scenario_run_that_never_ends_is_stopped_and_is_no_capture(
    tmp_path, monkeypatch, capsys
):
    """The duration clocks stand still while a scenario runs, so a wait cannot time out alone."""

    def run(command, *, timeout, **_):
        raise subprocess.TimeoutExpired(command, timeout)

    monkeypatch.setattr(compare.subprocess, "run", run)
    out = tmp_path / "out"
    assert _capture_main("--out", str(out), "--root", str(tmp_path / "root"), "--timeout", "5") == 1
    assert "passed 5 seconds and was stopped" in capsys.readouterr().out
    assert not (out / compare.MANIFEST).exists()
    assert not (tmp_path / "root-holder").exists()


def test_a_checkout_with_no_scenario_files_is_refused(tmp_path, capsys, no_run):
    (tmp_path / "checkout" / "tests" / "behaviour").mkdir(parents=True)
    (tmp_path / "checkout" / "tests" / "behaviour" / "conftest.py").write_text("", encoding="utf-8")
    code = compare.main(
        ["behaviour_compare.py", "--repo-root", str(tmp_path / "checkout"), "capture",
         "--out", str(tmp_path / "out"), "--root", str(tmp_path / "root")]
    )
    assert code == 2
    assert "no scenario files under" in capsys.readouterr().err


def test_a_run_that_failed_with_every_record_written_is_not_a_capture(
    tmp_path, monkeypatch, capsys
):
    """Every scenario recorded and listed, and the run still exited 1.

    A fixture that fails as it is torn down does this: the stage has written
    its record by then. Nothing is missing, so the run's own exit code is the
    one thing that says a scenario went wrong, and the mutation table of U297
    found no test held it: the tests of a failed run above also trip the
    reading of what was left unrecorded.
    """
    out = tmp_path / "out"
    passing = _passing_run(out, tmp_path, ["write/route"])

    def failed_late(command, **kwargs):
        done = passing(command, **kwargs)
        if command[0] == "git":
            return done
        return subprocess.CompletedProcess(command, 1, "1 passed, 1 error", "")

    monkeypatch.setattr(compare.subprocess, "run", failed_late)
    checkout = _checkout(tmp_path, "write.py")
    assert _capture_in(checkout, "--out", str(out), "--root", str(tmp_path / "root")) == 1
    said = capsys.readouterr().out
    assert "exited 1 with 1 scenarios recorded, so" in said and "left no record" not in said
    assert not (out / compare.MANIFEST).exists()
    assert compare.unrecorded(out, compare.recorded_scenarios(out), ["tests/behaviour/write.py"]) == []


def test_a_run_that_passes_and_records_nothing_is_not_a_capture(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(
        compare.subprocess,
        "run",
        lambda command, **_: subprocess.CompletedProcess(command, 0, "", ""),
    )
    out = tmp_path / "out"
    assert _capture_main("--out", str(out), "--root", str(tmp_path / "root")) == 1
    assert "exited 0 with 0 scenarios recorded" in capsys.readouterr().out
    assert not (out / compare.MANIFEST).exists()


def test_the_scenario_run_is_serial_in_the_root_and_imports_the_placed_source(tmp_path):
    root, source = tmp_path / "root", tmp_path / "root-source"
    command = compare.capture_command(["tests/behaviour/cli.py"], root, source, "help")
    assert command[:4] == [sys.executable, "-m", "pytest", "tests/behaviour/cli.py"]
    joined = " ".join(command)
    assert f"--basetemp {root}" in joined
    assert "-o addopts= " in joined + " "
    assert f"-o pythonpath={source / 'src'}" in joined
    assert command[-2:] == ["-k", "help"]
    assert "-k" not in compare.capture_command(["x.py"], root, source, None)


def test_the_scenario_files_are_every_module_but_the_harness_own_two():
    files = compare.scenario_files(REPO_ROOT)
    assert files == sorted(files)
    assert {"tests/behaviour/cli.py", "tests/behaviour/write.py", "tests/behaviour/intake.py",
            "tests/behaviour/backup.py", "tests/behaviour/tagging.py"} <= set(files)
    assert not {"tests/behaviour/conftest.py", "tests/behaviour/__init__.py"} & set(files)


def test_the_suite_does_not_collect_a_scenario_file():
    """A scenario runs when a capture asks, so the suite's time does not grow with them."""
    for name in compare.scenario_files(REPO_ROOT):
        stem = Path(name).name
        assert not stem.startswith("test_") and not stem.endswith("_test.py"), name


# ═══════════════════════════════════════════════════════════════════════════
# The source a capture runs against
# ═══════════════════════════════════════════════════════════════════════════


def _git(root: Path, *args: str) -> None:
    done = subprocess.run(
        ["git", "-c", "user.email=capture@test", "-c", "user.name=capture", *args],
        cwd=root, capture_output=True, check=False,
    )
    assert done.returncode == 0, done.stderr.decode()


@pytest.fixture
def checkout(tmp_path) -> Path:
    """A repository whose committed source and working tree differ."""
    root = tmp_path / "checkout"
    (root / "src" / "pkg" / "__pycache__").mkdir(parents=True)
    (root / "src" / "pkg" / "verb.py").write_text("HELP = 'committed'\n", encoding="utf-8")
    (root / "notes.md").write_text("not source\n", encoding="utf-8")
    _git(root, "init", "-q", "-b", "main")
    _git(root, "add", "src/pkg/verb.py", "notes.md")
    _git(root, "commit", "-q", "-m", "base")
    (root / "src" / "pkg" / "verb.py").write_text("HELP = 'edited'\n", encoding="utf-8")
    (root / "src" / "pkg" / "__pycache__" / "verb.pyc").write_bytes(b"\x00")
    return root


def test_the_working_trees_source_is_placed_as_it_stands(checkout, tmp_path):
    target = tmp_path / "placed"
    (target / "stale").mkdir(parents=True)
    assert compare.place_source(checkout, None, target) == "the working tree"
    assert (target / "src/pkg/verb.py").read_text(encoding="utf-8") == "HELP = 'edited'\n"
    assert not (target / "src/pkg/__pycache__").exists()
    assert not (target / "stale").exists()


def test_a_revisions_source_is_placed_as_git_holds_it_and_git_is_only_read(checkout, tmp_path):
    target = tmp_path / "placed"
    described = compare.place_source(checkout, "HEAD", target)
    assert described.startswith("commit ") and len(described) == len("commit ") + 40
    assert (target / "src/pkg/verb.py").read_text(encoding="utf-8") == "HELP = 'committed'\n"
    assert sorted(path.name for path in target.iterdir()) == [compare.LEFT_BY_A_CAPTURE, "src"]
    # The checkout still holds the edit: nothing was checked out over it.
    assert (checkout / "src/pkg/verb.py").read_text(encoding="utf-8") == "HELP = 'edited'\n"


def test_a_revision_git_does_not_know_is_refused(checkout, tmp_path):
    with pytest.raises(compare.Refusal, match="git knows no commit 'no-such-branch'"):
        compare.place_source(checkout, "no-such-branch", tmp_path / "placed")


# ═══════════════════════════════════════════════════════════════════════════
# The stage: roots, pins and the refusal inside the run
# ═══════════════════════════════════════════════════════════════════════════


def test_a_config_root_outside_a_temporary_directory_is_refused(monkeypatch, tmp_path):
    """Asked of the product's own resolver, so it is where a write would land."""
    from cratekit.core import config

    scenario = tmp_path / "scenario"
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(scenario / "config"))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(scenario / "state"))
    stage_fixtures.refuse_a_root_outside(scenario)

    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(OUTSIDE / "a-real-config"))
    with pytest.raises(compare.Refusal, match="the configuration directory is .*a-real-config"):
        stage_fixtures.refuse_a_root_outside(scenario)


def test_a_state_root_outside_a_temporary_directory_is_refused(monkeypatch, tmp_path):
    from cratekit.core import config

    scenario = tmp_path / "scenario"
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(scenario / "config"))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(OUTSIDE / "a-real-state"))
    with pytest.raises(compare.Refusal, match="the state directory is .*a-real-state"):
        stage_fixtures.refuse_a_root_outside(scenario)


def test_a_root_in_another_tests_temporary_directory_is_refused(monkeypatch, tmp_path):
    """Temporary is not enough: a scenario writes only under its own directory."""
    from cratekit.core import config

    scenario = tmp_path / "scenario"
    monkeypatch.setenv(config.ENV_CONFIG_DIR, str(tmp_path / "elsewhere" / "config"))
    monkeypatch.setenv(config.ENV_STATE_DIR, str(scenario / "state"))
    with pytest.raises(compare.Refusal, match="not inside the scenario's own directory"):
        stage_fixtures.refuse_a_root_outside(scenario)


def test_a_scenario_that_does_not_take_the_stage_is_refused():
    stage_fixtures.refuse_a_scenario_without_a_stage(["tmp_path", "stage"])
    with pytest.raises(compare.Refusal, match="would pass and leave no record"):
        stage_fixtures.refuse_a_scenario_without_a_stage(["tmp_path", "machine"])


WIRED_SCENARIOS = '''
import pytest


def test_takes_the_stage(stage):
    assert stage.crate("--version").code == 0


def test_takes_no_stage():
    pass


@pytest.mark.skip(reason="not today")
def test_is_skipped(stage):
    stage.crate("--version")


@pytest.mark.xfail(strict=False)
def test_is_expected_to_fail(stage):
    stage.crate("--version")
    assert False


def test_fails_after_a_command(stage):
    stage.crate("--version")
    assert False
'''


def _wired_run(tmp_path: Path, **env: str) -> subprocess.CompletedProcess:
    """The stage's fixtures around a scratch scenario file, in a run of their own.

    The file lives outside the repository, so the suite's conftest and the
    stage's are loaded as plugins by name: the same fixtures, set up in the
    same order, around scenarios written to trip each refusal.
    """
    scenarios = tmp_path / "scenarios"
    scenarios.mkdir(exist_ok=True)
    (scenarios / "wired.py").write_text(WIRED_SCENARIOS, encoding="utf-8")
    environment = {
        name: value for name, value in os.environ.items() if name not in compare.SCRUBBED_ENV
    }
    environment.update({compare.ENV_OUT: str(tmp_path / "out"), **env})
    return subprocess.run(
        [sys.executable, "-m", "pytest", str(scenarios / "wired.py"), "-p", "tests.conftest",
         "-p", "tests.behaviour.conftest", "--basetemp", str(tmp_path / "root"),
         "-p", "no:cacheprovider", "--tb=line", "-o", "addopts="],
        capture_output=True, text=True, check=False, cwd=REPO_ROOT, env=environment,
    )


def test_in_a_real_run_only_a_scenario_that_took_the_stage_and_passed_is_recorded(tmp_path):
    """Each refusal is a function with a test of its own; this holds that the fixtures call them.

    Five scenarios, one of which should record. The one with no stage is
    refused at set up, the skipped one and the two that fail leave nothing,
    and the run still lists all five as collected, which is what lets the
    capture see the four are missing.
    """
    done = _wired_run(tmp_path)
    assert done.returncode == 1, done.stdout[-2000:]
    assert "would pass and leave no record" in done.stdout
    out = tmp_path / "out"
    assert compare.recorded_scenarios(out) == ["wired/takes_the_stage"]
    assert json.loads((out / compare.EXPECTED).read_text()) == [
        "wired/takes_the_stage",
        "wired/takes_no_stage",
        "wired/is_skipped",
        "wired/is_expected_to_fail",
        "wired/fails_after_a_command",
    ]
    assert compare.unrecorded(out, compare.recorded_scenarios(out), []) == [
        "wired/fails_after_a_command",
        "wired/is_expected_to_fail",
        "wired/is_skipped",
        "wired/takes_no_stage",
    ]
    ran = json.loads((out / "wired/takes_the_stage/commands.json").read_text())
    assert [one["argv"] for one in ran] == [["--version"]]
    # The roots it ran under were its own directory's, moved there by the fixture.
    listed = json.loads((out / "wired/takes_the_stage/files.json").read_text())
    assert {"home", "config", "state", "library"} <= set(listed)


def test_in_a_real_run_a_product_imported_from_elsewhere_stops_every_scenario(tmp_path):
    done = _wired_run(tmp_path, **{compare.ENV_SOURCE: str(tmp_path / "placed" / "src")})
    assert done.returncode == 1, done.stdout[-2000:]
    assert "not from the source the capture placed" in done.stdout
    assert compare.recorded_scenarios(tmp_path / "out") == []


def test_a_stage_refuses_before_it_runs_a_command(tmp_path):
    def refuse() -> None:
        raise compare.Refusal("outside")

    stage = behaviour.Stage(name="x/y", root=tmp_path, refuse_outside=refuse)
    with pytest.raises(compare.Refusal, match="outside"):
        stage.crate("--version")
    assert stage.commands == []


def test_the_product_must_come_from_the_source_the_capture_placed(monkeypatch, tmp_path):
    monkeypatch.delenv(compare.ENV_SOURCE, raising=False)
    stage_fixtures.refuse_another_source()
    monkeypatch.setenv(compare.ENV_SOURCE, str(REPO_ROOT / "src"))
    stage_fixtures.refuse_another_source()
    monkeypatch.setenv(compare.ENV_SOURCE, str(tmp_path / "placed" / "src"))
    with pytest.raises(compare.Refusal, match="imported cratekit from .* not from the source"):
        stage_fixtures.refuse_another_source()


def test_a_stage_keeps_each_command_with_its_streams_and_its_exit_code(tmp_path):
    stage = behaviour.Stage(name="x/y", root=tmp_path, refuse_outside=lambda: None)
    version = stage.crate("--version")
    unknown = stage.crate("no-such-verb")
    assert version.code == 0 and version.stdout.strip()
    assert unknown.code == 2 and "invalid choice" in unknown.stderr
    assert stage.commands == [
        {"argv": ["--version"], "exit": 0, "stdout": version.stdout, "stderr": ""},
        {"argv": ["no-such-verb"], "exit": 2, "stdout": "", "stderr": unknown.stderr},
    ]


def test_settling_gives_every_file_and_directory_the_pinned_instant(tmp_path):
    (tmp_path / "deep" / "er").mkdir(parents=True)
    (tmp_path / "deep" / "er" / "file").write_text("x", encoding="utf-8")
    (tmp_path / "link").symlink_to("nowhere")
    behaviour.Stage(name="x/y", root=tmp_path, refuse_outside=lambda: None).settle()
    stamp = behaviour.INSTANT.timestamp()
    for path in (tmp_path / "deep", tmp_path / "deep" / "er", tmp_path / "deep" / "er" / "file"):
        assert path.stat().st_mtime == stamp, path
    assert (tmp_path / "link").lstat().st_mtime == stamp


def test_the_pins_hold_the_clock_and_count_the_ids_and_come_off_again():
    real_now, real_uuid4, real_time = datetime.datetime.now, uuid.uuid4, time.time
    with pytest.MonkeyPatch.context() as patch:
        unpin = behaviour.pin(patch)
        try:
            # Read through this module's own name for the class, which the sweep re-pointed.
            now = datetime.datetime.now(datetime.timezone.utc)
            assert now == behaviour.INSTANT and type(now) is behaviour._REAL_DATETIME
            assert datetime.datetime.utcnow() == behaviour.INSTANT.replace(tzinfo=None)
            assert datetime.date.today() == behaviour.INSTANT.astimezone().date()
            assert time.time() == behaviour.INSTANT.timestamp()
            assert time.time_ns() == int(behaviour.INSTANT.timestamp()) * 1_000_000_000
            assert time.monotonic() == time.perf_counter() == 0.0
            # A date built or parsed through the pinned class is the real type's.
            built = datetime.datetime(2026, 1, 2, 3, 4, 5)
            assert type(built) is behaviour._REAL_DATETIME
            assert isinstance(built, datetime.datetime)
            assert isinstance(datetime.date(2026, 1, 2), datetime.date)
            assert issubclass(behaviour._REAL_DATETIME, datetime.date)
            assert datetime.datetime.fromisoformat("2026-01-02T03:04:05") == built
            ids = [uuid.uuid4() for _ in range(3)] + [secrets.token_hex(8), secrets.token_hex(8)]
            assert len(set(ids)) == 5 and ids[0].version == 4
            assert len(secrets.token_hex(8)) == 16 and len(secrets.token_bytes(4)) == 4
        finally:
            unpin()
        first = ids
    with pytest.MonkeyPatch.context() as patch:
        unpin = behaviour.pin(patch)
        again = [uuid.uuid4() for _ in range(3)] + [secrets.token_hex(8), secrets.token_hex(8)]
        unpin()
    assert again == first, "the nth id of a scenario is not the nth id of the next"
    assert datetime.datetime.now == real_now and uuid.uuid4 is real_uuid4
    assert time.time is real_time


def test_a_reference_that_outlives_the_pins_is_the_real_thing_again():
    """The review's finding: a default argument bound while pinned kept the pinned clock.

    Nothing can reach such a reference to put the real name back, so each
    pinned name asks whether the pins are on every time it is called.
    """
    with pytest.MonkeyPatch.context() as patch:
        unpin = behaviour.pin(patch)

        def gate(clock=time.time, mint=uuid.uuid4, token=secrets.token_hex):
            return clock(), mint(), token(4)

        kept_class = datetime.datetime
        assert gate()[0] == behaviour.INSTANT.timestamp()
        pinned_ids = gate()[1:]
        unpin()
    assert kept_class is behaviour.PinnedDatetime
    now, minted, token = gate()
    assert abs(now - time.time()) < 60 and abs(now - behaviour.INSTANT.timestamp()) > 1
    assert (minted, token) != pinned_ids and gate()[1] != minted
    real = kept_class.now(datetime.timezone.utc)
    assert abs((real - datetime.datetime.now(datetime.timezone.utc)).total_seconds()) < 60
    assert abs((kept_class.utcnow() - real.replace(tzinfo=None)).total_seconds()) < 60
    assert behaviour.PinnedDate.today() == datetime.date.today()


def test_the_pins_go_on_once_at_a_time():
    with pytest.MonkeyPatch.context() as patch:
        unpin = behaviour.pin(patch)
        try:
            with pytest.raises(RuntimeError, match="already on"):
                behaviour.pin(patch)
        finally:
            unpin()
    with pytest.MonkeyPatch.context() as patch:
        behaviour.pin(patch)()


def test_the_binding_stamps_a_row_with_the_pinned_instant_and_then_with_the_real_one():
    from pyrekordbox.db6 import tables

    column = tables.DjmdContent.__table__.c.updated_at
    with pytest.MonkeyPatch.context() as patch:
        unpin = behaviour.pin(patch)
        pinned = behaviour.INSTANT.astimezone().replace(tzinfo=None)
        assert column.default.arg(None) == pinned
        assert column.onupdate.arg(None) == pinned
        unpin()
    assert abs((column.default.arg(None) - datetime.datetime.now()).total_seconds()) < 60


def test_a_module_imported_while_pinned_gets_the_real_clock_back(tmp_path, monkeypatch):
    """Undoing the patch does not reach a name a module took while it was set."""
    (tmp_path / "late_import_probe.py").write_text(
        "from datetime import date, datetime\nfrom uuid import uuid4\n", encoding="utf-8"
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    real_uuid4 = uuid.uuid4
    with pytest.MonkeyPatch.context() as patch:
        unpin = behaviour.pin(patch)
        probe = importlib.import_module("late_import_probe")
        assert probe.datetime is behaviour.PinnedDatetime and probe.uuid4 is not real_uuid4
        # Left pinned on purpose: the patch is undone here and the probe is not.
    assert probe.datetime is behaviour.PinnedDatetime
    unpin()
    assert probe.datetime is behaviour._REAL_DATETIME and probe.date is behaviour._REAL_DATE
    assert probe.uuid4 is real_uuid4 is uuid.uuid4
    sys.modules.pop("late_import_probe", None)


def test_a_scenario_is_named_for_its_file_and_its_function():
    path = Path("tests/behaviour/write.py")
    assert behaviour.scenario_name(path, "test_xml_splice") == "write/xml_splice"


def test_the_process_is_known_by_its_id_and_its_start_as_the_product_spells_them():
    from cratekit.core import session

    assert behaviour.process_identity() == [
        str(os.getpid()),
        session.process_started(os.getpid()),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# The real thing: every shipped scenario, captured twice
# ═══════════════════════════════════════════════════════════════════════════


def test_two_captures_of_one_commit_are_equal(tmp_path, capsys):
    """Every shipped scenario, run twice by the script itself, in two processes.

    Under one root, so the paths agree, and against the working tree both
    times, so an uncommitted edit to the product cannot make this fail: what
    is held is that a capture depends on nothing but the tree it ran. This is
    the test that goes red when a scenario prints or writes something the
    stage did not pin.
    """
    root = tmp_path / "root"
    captures = []
    for name in ("first", "second"):
        out = tmp_path / name
        done = subprocess.run(
            [sys.executable, str(SCRIPT), "capture", "--out", str(out), "--root", str(root)],
            capture_output=True, text=True, check=False, cwd=REPO_ROOT,
        )
        assert done.returncode == 0, done.stdout[-3000:] + done.stderr[-1000:]
        captures.append(out)

    manifest = json.loads((captures[0] / compare.MANIFEST).read_text(encoding="utf-8"))
    assert manifest["scenarios"] == [
        "acquire/a_tombstone_withholds_a_deleted_record",
        "acquire/acquire_audit_and_the_refusals",
        "acquire/match_verdicts_over_three_readers",
        "acquire_bandcamp/bandcamp_plan_and_fetch",
        "acquire_bandcamp/bandcamp_without_a_session",
        "acquire_download/a_drive_lands_every_track",
        "acquire_download/a_missing_session_parks",
        "acquire_download/a_refused_login_and_a_withdrawn_session_park",
        "acquire_fallback/fallback_offers_and_accepts",
        "acquire_fallback_fetch/fallback_fetch_lands_marked",
        "acquire_fallback_fetch/fallback_fetch_refused_when_strict",
        "adopt/scan_and_apply_jobs_queued_driven_and_reported",
        "backup/backup_capture_and_the_restore_plan",
        "cli/a_config_no_verb_can_use",
        "cli/help_of_every_verb",
        "core_facts/pool_gate_preflight_and_tags_answers",
        "core_jobs/jobs_driven_to_each_end_and_read_back",
        "core_review/review_queue_offered_resolved_withheld_exported_and_imported",
        "export/a_rename_onto_a_name_the_ledger_already_holds_is_refused",
        "export/a_renamed_inspiration_playlist_renames_the_sets_account_playlist",
        "export/a_set_archived_into_its_years_downloaded_sets_folder",
        "export/a_set_made_on_the_account_with_its_unmatched_row_named",
        "export/a_set_with_no_stored_account_session_is_refused",
        "export/the_archive_backfill_files_every_set_its_intake_file_proves",
        "export/the_set_backfill_makes_a_playlist_for_each_inspiration_set",
        "favorites/favorites_put_in_order_behind_the_gate",
        "intake/a_batch_is_shelved_into_the_processed_tree",
        "intake/a_calibrated_landing_tags_the_rows_that_clear_the_cut",
        "intake/a_file_already_landed_staged_again_is_refused_at_the_move",
        "intake/a_landing_tags_the_rows_whose_drift_reads_variable",
        "intake/a_manifest_and_a_label_file_the_landed_rows",
        "intake/a_shelve_of_nothing_refuses_before_a_gate",
        "intake/an_answer_whose_plan_moved_is_stale_and_writes_nothing",
        "intake/no_acknowledgment_refuses_before_the_gate",
        "intake/rehearsal_and_the_gate_it_feeds",
        "intake/what_refuses_before_the_gate_and_writes_nothing",
        "intake_bridge/a_bridge_landing_and_the_import_that_verifies_it",
        "intake_bridge/a_bridge_landing_refuses_a_stale_answer_and_an_absent_folder",
        "intake_file/a_native_file_is_one_row_and_one_playlist",
        "intake_file/an_answer_over_one_title_is_stale_once_the_file_is_retagged",
        "intake_file/on_the_bridge_an_export_is_spliced_and_none_is_a_plan",
        "intake_inspiration/a_set_lands_under_inspiration_and_a_second_part_joins_its_inbox_playlist",
        "intake_inspiration/the_backfill_adds_the_set_playlist_once",
        "intake_inspiration/the_backfill_with_no_acknowledgment_refuses_before_its_gate",
        "intake_missing/a_pass_lists_its_playlists_once",
        "intake_missing/a_playlist_job_and_the_list_of_what_it_found_missing",
        "intake_missing/a_track_already_staged_is_named_staged_and_not_listed",
        "intake_missing/an_open_job_is_refused_and_nothing_is_written",
        "intake_missing_isrc/a_provider_outage_refuses_and_writes_nothing",
        "intake_missing_isrc/one_isrc_is_listed_and_the_rest_handed_on",
        "intake_missing_search/a_near_miss_is_offered_then_listed_once_accepted",
        "intake_missing_search/a_provider_that_cannot_search_refuses_and_writes_nothing",
        "intake_pass/account_playlists_land_as_their_own_inbox_playlists",
        "intake_pass/an_emptied_account_playlist_is_refilled_from_its_pass",
        "intake_pass/hearts_downloaded_and_owned_join_all_favorites_and_their_months",
        "intake_pass/the_analysed_rows_are_cleared_from_analyze",
        "intake_repair/a_dark_row_under_a_proposed_name_refuses_the_repair",
        "intake_repair/an_accepted_proposal_is_renamed_and_an_open_one_is_not",
        "intake_rotate/an_inbox_changed_after_the_answer_is_stale_and_writes_nothing",
        "intake_rotate/no_acknowledgment_refuses_before_the_gate",
        "intake_rotate/stale_batches_move_into_old_and_the_expired_go",
        "intake_set/a_mix_address_is_fetched_identified_and_removed",
        "intake_set/a_month_over_its_bound_refuses_identify_and_set_and_queues_nothing",
        "intake_set/a_provider_quota_mid_run_refuses_and_queues_nothing",
        "intake_set/a_set_stops_at_the_account_gate_and_makes_the_account_playlist",
        "intake_set/a_set_with_no_recognition_key_is_refused_before_any_seam",
        "intake_set/identify_then_set_then_the_resume_that_resolves_each_track",
        "label/registry_document_written_read_back_and_refused",
        "organize/a_genre_two_root_folders_on_the_account_carry_is_refused_by_the_mirror",
        "organize/a_mirror_pass_after_a_full_apply_and_a_rerun_that_plans_nothing",
        "organize/an_account_with_no_stored_session_refuses_the_account_steps",
        "organize/the_account_side_makes_the_label_folder_and_archives_the_set",
        "organize/the_filing_step_alone_files_a_marked_playlist_in_its_year",
        "organize/the_rekordbox_side_files_the_tracks_and_rotates_the_batch",
        "organize/the_root_step_alone_removes_debris_and_then_the_emptied_legacy_folder",
        "organize/with_the_export_module_off_organize_plans_and_says_what_it_left_out",
        "organize_mirror_edits/a_track_moved_on_the_account_is_retagged_and_refiled_in_the_library",
        "outbound/a_label_year_pruned_of_a_held_release",
        "outbound/a_playlist_exported_through_its_confirm_and_the_jobs_resume",
        "outbound/a_prune_whose_removal_the_accounts_window_lags_is_refused",
        "outbound/an_exported_playlist_pruned_of_the_track_its_library_playlist_lost",
        "sync/collection_removal",
        "tagging/tag_write_to_an_audio_file",
        "tagging_rows/row_genres_written_from_their_files",
        "write/guarded_tree_write",
        "write/xml_splice",
        "write_link/an_unknown_row_refuses_before_any_gate",
        "write_link/three_probe_values_written_behind_the_gate",
        "write_link/without_the_acknowledgment_the_probe_refuses_before_its_gate",
        "write_metadata/an_unreadable_calibration_refuses_and_writes_nothing",
        "write_metadata/vocal_tags_planned_then_written_then_already_there",
        "write_naming/a_rename_onto_a_name_another_file_holds_overwrites_nothing",
        "write_naming/a_rename_planned_and_applied_beside_a_referenced_file",
        "write_naming/a_row_under_an_unmapped_volume_refuses_and_renames_nothing",
        "write_pending/route_pending_after_a_native_landing",
        "write_resort/a_resort_planned_queued_and_run_by_its_worker",
        "write_resort/an_answer_over_a_copy_does_not_approve_the_live_file",
        "write_rows/an_inline_answer_is_refused_and_nothing_is_filled",
        "write_rows/bare_rows_given_their_defaults_behind_the_gate",
        "write_rows/without_the_acknowledgment_the_repair_refuses_before_its_gate",
    ]
    assert manifest["root"] == str(root.resolve()) and manifest["source"] == "the working tree"
    # The run cleaned up after itself, and held nothing back.
    assert not root.exists() and not compare.source_directory(root).exists()
    assert not root.with_name("root-holder").exists()

    assert _compare(*captures) == 0, capsys.readouterr().out[-4000:]
    summary = capsys.readouterr().out
    assert "100 scenarios" in summary and "no difference" in summary

    # And the two are equal for a reason: each holds real commands, files and rows.
    helped = json.loads((captures[0] / "cli/help_of_every_verb/commands.json").read_text())
    assert len(helped) > 100 and all(one["exit"] == 0 for one in helped)
    landed = json.loads(
        (captures[0] / "intake/rehearsal_and_the_gate_it_feeds/databases.json").read_text()
    )
    rows = landed["library/db/master.db"]["tables"]["djmdContent"]
    assert sum("One.flac" in row or "Two.flac" in row for row in rows) == 2
    # The roots moved into the scenario's own directory: the job queue the
    # verb wrote is in the capture, not in a directory the suite numbered.
    written = json.loads((captures[0] / "write/guarded_tree_write/files.json").read_text())
    assert written["state/cratekit/jobs/queue.db"]["kind"] == "database"
    assert written["library/db/master.db"]["kind"] == "database"
    assert written["config/config.toml"]["kind"] == "file"
    assert written["state/cratekit/jobs/queue.db"]["mode"] == "0600"
    queue = json.loads(
        (captures[0] / "write/guarded_tree_write/databases.json").read_text()
    )["state/cratekit/jobs/queue.db"]
    assert queue["settings"]["journal_mode"] == "wal"
    assert any('"type": "index"' in one for one in queue["schema"])
    assert sorted(json.loads((captures[0] / compare.EXPECTED).read_text())) == manifest["scenarios"]
    words = [
        json.loads((one / "write/guarded_tree_write/process.json").read_text()) for one in captures
    ]
    assert words[0] != words[1], "one process took both captures, so nothing was read past"
