"""Tests for ``scripts/killset.py``, the recorded mutation kill set (U297).

The kill set is what a refactor is held to: every mutation a test killed
before it is still killed after. A reader that miscounts, a row file that does
not say what its table recorded, or a check that passes a lost kill would each
let a guard go untested with a table saying otherwise. So every count here is
taken on a tree small enough to verify by hand, and the one end to end test
runs the real driver over the driver suite's own throwaway package.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tomllib
from pathlib import Path

import pytest

from tests.test_mutation_driver import GUARDS, GUARDS_FILE, mutate
from tests.test_mutation_driver import green_template as green_template  # noqa: PLC0414
from tests.test_mutation_driver import repo as repo  # noqa: PLC0414

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load():
    spec = importlib.util.spec_from_file_location(
        "cratekit_killset", REPO_ROOT / "scripts" / "killset.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


killset = _load()

ALPHA = "src/pkg/alpha.py"
ALPHA_TEXT = "def once():\n    return 1\n\n\ndef twice():\n    return 2\n\n\ndef again():\n    return 2\n"


def _recorded(row_id: str, old: str, new: str = "    return 0", **extra) -> dict:
    """One row as the driver's sidecar spells it, killed unless told otherwise."""
    return {
        "id": row_id,
        "description": f"row {row_id}",
        "file": ALPHA,
        "surface": "user",
        "old": old,
        "new": new,
        "status": "killed",
        "deaths": 1,
        "killed": ["tests/test_alpha.py::test_once"],
        "subset": ["tests/test_alpha.py"],
        "promoted": False,
        **extra,
    }


def _table(root: Path, name: str, rows: list[dict], **extra) -> Path:
    path = root / "docs" / "mutation" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {"name": Path(name).stem, "pass_kind": "light", "valid": True, "invalid_reason": ""}
    path.write_text(json.dumps({**body, **extra, "rows": rows}), encoding="utf-8")
    return path


@pytest.fixture
def tree(tmp_path) -> Path:
    """A checkout with one source file, two test files and no tables yet."""
    (tmp_path / "src" / "pkg").mkdir(parents=True)
    (tmp_path / ALPHA).write_text(ALPHA_TEXT, encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_alpha.py").write_text("", encoding="utf-8")
    (tmp_path / "tests" / "test_beta.py").write_text("", encoding="utf-8")
    return tmp_path


def _run(root: Path, *argv: str) -> int:
    return killset.main(["killset.py", "--repo-root", str(root), *argv])


def _states(root: Path) -> dict[str, str]:
    return {row.id: row.state for row in killset.read_kill_set(root).rows}


# ═══════════════════════════════════════════════════════════════════════════
# list: what a recorded row is today
# ═══════════════════════════════════════════════════════════════════════════


def test_a_row_is_live_stale_ambiguous_or_gone_by_what_the_tree_holds(tree):
    """One of each, plus the two a reader must not count as kills."""
    _table(
        tree,
        "u1.json",
        [
            _recorded("LIVE", "    return 1"),
            _recorded("STALE", "    return 7"),
            _recorded("TWICE", "    return 2"),
            _recorded("GONE", "    return 1", file="src/pkg/removed.py"),
            _recorded("NAMELESS", "    return 1", file=None),
            _recorded("ZERO", "def once():", status="zero", deaths=0, killed=[]),
            _recorded("REFUSED", "def twice():", status="refused", deaths=0, killed=[]),
        ],
    )
    assert _states(tree) == {
        "LIVE": "live",
        "STALE": "stale",
        "TWICE": "ambiguous",
        "GONE": "gone",
        "NAMELESS": "gone",
    }


def test_the_same_substitution_recorded_twice_is_one_live_row(tree):
    _table(tree, "u1.json", [_recorded("A", "    return 1")])
    _table(tree, "u2.json", [_recorded("B", "    return 1")])
    _table(tree, "u3.json", [_recorded("C", "    return 1", new="    return 9")])
    found = killset.read_kill_set(tree)
    assert [(row.table, row.state) for row in found.rows] == [
        ("u1.json", "live"),
        ("u2.json", "duplicate"),
        ("u3.json", "live"),
    ]


def test_list_prints_the_counts_and_one_line_a_file(tree, capsys):
    _table(
        tree,
        "u1.json",
        [
            _recorded("LIVE", "    return 1"),
            _recorded("STALE", "    return 7"),
            _recorded("TWICE", "    return 2"),
            _recorded("GONE", "    return 1", file="src/pkg/removed.py"),
            _recorded("NAMELESS", "    return 1", file=None),
            _recorded("ZERO", "def once():", status="zero", deaths=0, killed=[]),
        ],
    )
    (tree / "docs" / "mutation" / "notes.json").write_text("[1, 2]", encoding="utf-8")
    assert _run(tree, "list") == 0
    out = capsys.readouterr().out
    assert "1 tables, 6 rows, 5 recorded as killed" in out
    assert "1 live in 1 files" in out
    assert "1 stale: the text is gone from the file" in out
    assert "1 ambiguous: the text occurs more than once" in out
    assert "2 gone: the file no longer exists (1 of them name no file)" in out
    assert "1 files under docs/mutation are not tables: notes.json" in out
    assert "    1     1         1     0  src/pkg/alpha.py" in out
    assert "    0     0         0     1  src/pkg/removed.py" in out


def test_list_narrows_to_the_paths_given_and_lists_rows_when_asked(tree, capsys):
    _table(
        tree,
        "u1.json",
        [_recorded("LIVE", "    return 1"), _recorded("ELSE", "x", file="scripts/tool.py")],
    )
    assert _run(tree, "list", "src", "--rows") == 0
    out = capsys.readouterr().out
    assert "live      src/pkg/alpha.py  u1.json  LIVE" in out
    assert "scripts/tool.py" not in out


def test_a_path_outside_the_checkout_is_refused(tree, tmp_path_factory, capsys):
    elsewhere = tmp_path_factory.mktemp("elsewhere")
    _table(tree, "u1.json", [_recorded("LIVE", "    return 1")])
    assert _run(tree, "list", str(elsewhere)) == 2
    assert "is not inside" in capsys.readouterr().err


# ═══════════════════════════════════════════════════════════════════════════
# rows: a row file the driver can run
# ═══════════════════════════════════════════════════════════════════════════


def test_rows_writes_the_live_rows_and_counts_what_it_left_out(tree, capsys):
    """The stale row is left out of the file and named in the count."""
    _table(
        tree,
        "u1.json",
        [
            _recorded("LIVE", "    return 1"),
            _recorded("STALE", "    return 7"),
            _recorded("TWICE", "    return 2"),
        ],
    )
    out = tree / "rows.toml"
    assert _run(tree, "rows", ALPHA, "--out", str(out)) == 0
    said = capsys.readouterr().out
    assert "1 live rows in 1 files written" in said
    assert "left out: 1 stale, 1 ambiguous, 0 gone, 0 duplicates of a live row" in said
    assert "  stale     src/pkg/alpha.py  u1.json  STALE" in said

    name, pass_kind, rows, _ = mutate.load_spec(out)
    assert (name, pass_kind) == ("rows", killset.REPLAY) == ("rows", mutate.REPLAY)
    assert [row.id for row in rows] == ["u1.LIVE"]
    assert rows[0].source == ("u1.json", "LIVE")
    assert rows[0].tests == ("tests/test_alpha.py",)
    assert rows[0].surface == "user"
    # It applies cleanly: the text it names occurs once, and the driver's own
    # substitution takes it.
    assert mutate.apply_mutation(ALPHA_TEXT, rows[0].old, rows[0].new) == ALPHA_TEXT.replace(
        "    return 1", "    return 0"
    )


def test_rows_for_a_directory_takes_every_file_under_it(tree):
    (tree / "src" / "pkg" / "beta.py").write_text("B = 1\n", encoding="utf-8")
    _table(
        tree,
        "u1.json",
        [
            _recorded("A", "    return 1"),
            _recorded("B", "B = 1", new="B = 2", file="src/pkg/beta.py"),
            _recorded("S", "x = 1", file="scripts/tool.py"),
        ],
    )
    out = tree / "rows.toml"
    assert _run(tree, "rows", "src/pkg/", "--out", str(out), "--name", "area") == 0
    data = tomllib.loads(out.read_text(encoding="utf-8"))
    assert data["name"] == "area"
    assert [row["file"] for row in data["rows"]] == [ALPHA, "src/pkg/beta.py"]


def test_rows_with_nothing_live_is_refused_and_writes_nothing(tree, capsys):
    _table(tree, "u1.json", [_recorded("STALE", "    return 7")])
    out = tree / "rows.toml"
    assert _run(tree, "rows", ALPHA, "--out", str(out)) == 2
    assert "no live row names" in capsys.readouterr().err
    assert not out.exists()


def test_rows_with_no_path_and_no_table_is_refused(tree, capsys):
    assert _run(tree, "rows", "--out", str(tree / "rows.toml")) == 2
    assert "name the files or directories" in capsys.readouterr().err


@pytest.mark.parametrize(
    "row, tests",
    [
        # Its own subset, as recorded.
        ({"subset": ["tests/test_alpha.py", "tests/test_beta.py"]}, ("tests/test_alpha.py", "tests/test_beta.py")),
        # Promoted: the subset killed nothing, so the kill files are where it dies.
        (
            {
                "subset": ["tests/test_alpha.py"],
                "promoted": True,
                "killed": ["tests/test_beta.py::test_b[a - b]", "tests/test_beta.py::test_c"],
            },
            ("tests/test_beta.py",),
        ),
        # No subset: the row ran the full suite.
        ({"subset": None, "killed": ["tests/test_beta.py::test_b"]}, ("tests/test_beta.py",)),
        # A subset file that is gone is left out, and the rest stand.
        ({"subset": ["tests/test_gone.py", "tests/test_beta.py"]}, ("tests/test_beta.py",)),
        # A subset wholly gone falls back to the kill files.
        ({"subset": ["tests/test_gone.py"]}, ("tests/test_alpha.py",)),
        # A node id in a subset is kept whole when its file is present.
        ({"subset": ["tests/test_alpha.py::test_once"]}, ("tests/test_alpha.py::test_once",)),
        # Nothing left: the driver derives the subset.
        ({"subset": ["tests/test_gone.py"], "killed": ["tests/test_gone.py::test_x"]}, ()),
    ],
)
def test_a_replay_row_runs_its_own_subset_else_the_files_its_kills_name(tree, row, tests):
    assert killset.tests_of(_recorded("R", "    return 1", **row), tree) == tests


HOSTILE = [
    "plain",
    "",
    "it's",
    "'''",
    "ends with a quote'",
    "'starts with one",
    "a\nb",
    "\nleading newline",
    "trailing newline\n",
    "a\n'''\nb",
    "block ending in a quote'\n'",
    'double "quotes" and a \\ backslash',
    "tab\tinside",
    "carriage\r\nreturn",
    "bell \x07 and delete \x7f",
    "ünïcödé and \U0001f3b5",
    "    if x:\n        return '''doc'''\n",
]


@pytest.mark.parametrize("text", HOSTILE)
def test_code_survives_the_row_file_exactly(text):
    """Whatever a table recorded is what the driver reads back, character for character."""
    written = f"old = {killset.toml_text(text)}\nname = {killset.toml_string(text)}\n"
    assert tomllib.loads(written) == {"old": text, "name": text}


def test_code_is_written_as_it_reads_when_a_literal_holds_it():
    assert killset.toml_text("    if value > limit:") == "'    if value > limit:'"
    assert killset.toml_text('x = "a"\ny = 1') == "'''\nx = \"a\"\ny = 1'''"
    assert killset.toml_text("x = 'a' or b") == "'''x = 'a' or b'''"
    assert killset.toml_text("x = 'a'") == '"x = \'a\'"'


# ═══════════════════════════════════════════════════════════════════════════
# check: every row killed before is killed after
# ═══════════════════════════════════════════════════════════════════════════


def _measured(row_id: str, *, deaths: int = 1, status: str = "killed", **extra) -> dict:
    """A replay table's row for source ``u1.json`` row ``row_id``."""
    return {
        "id": f"u1.{row_id}",
        "source": {"table": "u1.json", "id": row_id},
        "file": ALPHA,
        "old": f"old {row_id}",
        "new": "new",
        "status": status,
        "deaths": deaths,
        **extra,
    }


def _check(tmp_path: Path, before: list[dict], after: list[dict], **after_extra) -> int:
    first = _table(tmp_path, "before.json", before, pass_kind="replay")
    second = _table(tmp_path, "after.json", after, pass_kind="replay", **after_extra)
    return killset.main(["killset.py", "check", str(first), str(second)])


def test_check_passes_when_every_kill_is_kept(tmp_path, capsys):
    rows = [_measured("A"), _measured("B"), _measured("Z", deaths=0, status="zero")]
    assert _check(tmp_path, rows, rows) == 0
    assert "2 rows killed before: 2 killed after as written" in capsys.readouterr().out


def test_check_fails_on_one_lost_kill_and_names_it(tmp_path, capsys):
    before = [_measured("A"), _measured("B")]
    after = [_measured("A"), _measured("B", deaths=0, status="zero")]
    assert _check(tmp_path, before, after) == 1
    out = capsys.readouterr().out
    assert "1 lost" in out
    assert "LOST u1.json B: killed before, zero after (0 deaths)" in out


def test_check_fails_on_a_kill_with_no_row_and_no_mapping(tmp_path, capsys):
    assert _check(tmp_path, [_measured("A"), _measured("B")], [_measured("A")]) == 1
    assert "LOST u1.json B: killed before, and no row and no mapping after" in capsys.readouterr().out


def _mapping(to: str, reason: str = "merged into A") -> dict:
    return {"source": {"table": "u1.json", "id": "B"}, "to": to, "reason": reason}


def test_check_passes_a_row_mapped_to_a_surviving_row_that_is_killed(tmp_path, capsys):
    before = [_measured("A"), _measured("B")]
    assert _check(tmp_path, before, [_measured("A")], mapped=[_mapping("u1.A")]) == 0
    assert "1 covered by a mapped row that is killed, 0 lost" in capsys.readouterr().out


def test_check_fails_a_row_mapped_to_a_row_that_is_not_killed(tmp_path, capsys):
    before = [_measured("A"), _measured("B")]
    after = [_measured("A", deaths=0, status="zero")]
    assert _check(tmp_path, before, after, mapped=[_mapping("u1.A")]) == 1
    out = capsys.readouterr().out
    assert "LOST u1.json B: mapped to 'u1.A', which is zero after" in out


def test_check_fails_a_row_mapped_to_no_row_or_for_no_reason(tmp_path, capsys):
    before = [_measured("A"), _measured("B")]
    assert _check(tmp_path, before, [_measured("A")], mapped=[_mapping("u1.C")]) == 1
    assert "mapped to 'u1.C', which is no row after" in capsys.readouterr().out
    assert _check(tmp_path, before, [_measured("A")], mapped=[_mapping("u1.A", " ")]) == 1
    assert "mapped to 'u1.A' with no reason" in capsys.readouterr().out


def test_check_holds_a_row_whose_text_changed_to_a_moved_reason(tmp_path, capsys):
    """A different substitution under the same source is not the same kill until it says why."""
    before = [_measured("A")]
    silent = [_measured("A", file="src/pkg/beta.py")]
    assert _check(tmp_path, before, silent) == 1
    assert "its text differs between the two tables" in capsys.readouterr().out
    said = [_measured("A", file="src/pkg/beta.py", moved="the same text, now in beta")]
    assert _check(tmp_path, before, said) == 0
    assert "1 killed after at a new anchor" in capsys.readouterr().out


def test_check_matches_tables_that_are_not_replays_by_row_id(tmp_path):
    """A unit's own table before and after a fix round has no sources, only ids."""
    plain = {"id": "G1", "file": ALPHA, "old": "a", "new": "b", "status": "killed", "deaths": 2}
    first = _table(tmp_path, "before.json", [plain])
    second = _table(tmp_path, "after.json", [{**plain, "deaths": 0, "status": "zero"}])
    assert killset.main(["killset.py", "check", str(first), str(first)]) == 0
    assert killset.main(["killset.py", "check", str(first), str(second)]) == 1


@pytest.mark.parametrize(
    "extra, why",
    [
        ({"valid": False, "invalid_reason": "the null control killed 1"}, "the null control killed 1"),
        ({"invalid_reason": "in progress"}, "in progress"),
        ({"valid": None}, "it does not say it is valid"),
    ],
)
def test_check_refuses_a_table_that_is_not_a_finished_valid_batch(tmp_path, capsys, extra, why):
    """A batch cut short has measured only some rows, and its absent rows are not lost kills."""
    good = _table(tmp_path, "before.json", [_measured("A")])
    bad = _table(tmp_path, "after.json", [_measured("A")], **extra)
    assert killset.main(["killset.py", "check", str(good), str(bad)]) == 2
    assert f"is not a finished, valid batch: {why}" in capsys.readouterr().err
    assert killset.main(["killset.py", "check", str(bad), str(good)]) == 2


def test_check_refuses_a_file_that_is_not_a_table(tmp_path, capsys):
    good = _table(tmp_path, "before.json", [_measured("A")])
    other = tmp_path / "other.json"
    other.write_text("{}", encoding="utf-8")
    assert killset.main(["killset.py", "check", str(good), str(other)]) == 2
    assert "is not a mutation table" in capsys.readouterr().err


# ═══════════════════════════════════════════════════════════════════════════
# After a refactor: where a recorded row lives now
# ═══════════════════════════════════════════════════════════════════════════


def _before(tree: Path, *rows: dict) -> Path:
    """A replay table measured before a refactor, outside ``docs/mutation``."""
    path = tree / "before.json"
    body = {"name": "before", "pass_kind": "replay", "valid": True, "invalid_reason": ""}
    path.write_text(json.dumps({**body, "rows": list(rows)}), encoding="utf-8")
    return path


def _replayed(row_id: str, old: str, **extra) -> dict:
    return {
        **_recorded(f"u1.{row_id}", old),
        "source": {"table": "u1.json", "id": row_id},
        **extra,
    }


def test_rows_after_writes_text_still_in_its_file_as_it_was(tree, capsys):
    before = _before(tree, _replayed("A", "    return 1"))
    out = tree / "after.toml"
    assert _run(tree, "rows", "--after", str(before), "--out", str(out)) == 0
    assert "1 rows in place and 0 moved" in capsys.readouterr().out
    _, _, rows, dropped = mutate.load_spec(out)
    assert [(row.id, row.file, row.source, row.moved) for row in rows] == [
        ("u1.A", ALPHA, ("u1.json", "A"), "")
    ]
    assert dropped == []


def test_rows_after_follows_text_that_moved_to_one_other_file(tree, capsys):
    """A file split: the guard's text left ``alpha.py`` and is in ``moved.py`` once."""
    (tree / ALPHA).write_text("def twice():\n    return 2\n", encoding="utf-8")
    (tree / "src" / "pkg" / "moved.py").write_text("def once():\n    return 1\n", encoding="utf-8")
    before = _before(tree, _replayed("A", "    return 1"))
    out = tree / "after.toml"
    assert _run(tree, "rows", "--after", str(before), "--out", str(out)) == 0
    assert "0 rows in place and 1 moved" in capsys.readouterr().out
    _, _, rows, _ = mutate.load_spec(out)
    assert rows[0].file == "src/pkg/moved.py"
    assert rows[0].moved == "the same text, now in src/pkg/moved.py, was in src/pkg/alpha.py"
    assert rows[0].source == ("u1.json", "A")


def test_rows_after_leaves_text_it_cannot_place_for_the_author(tree, capsys):
    """Gone everywhere, or in two places: nothing says which guard it is now."""
    (tree / ALPHA).write_text("def twice():\n    return 2\n", encoding="utf-8")
    (tree / "src" / "pkg" / "one.py").write_text("    return 5\n", encoding="utf-8")
    (tree / "src" / "pkg" / "two.py").write_text("    return 5\n", encoding="utf-8")
    before = _before(
        tree,
        _replayed("GONE", "    return 1"),
        _replayed("SPLIT", "    return 5"),
        _replayed("KEPT", "    return 2"),
        _replayed("ZERO", "def twice():", deaths=0, status="zero"),
    )
    out = tree / "after.toml"
    assert _run(tree, "rows", "--after", str(before), "--out", str(out)) == 0
    assert "1 rows in place and 0 moved" in capsys.readouterr().out
    _, _, rows, dropped = mutate.load_spec(out)
    assert [row.id for row in rows] == ["u1.KEPT"]
    assert [one.id for one in dropped] == ["u1.GONE", "u1.SPLIT"]
    assert "unplaced: the text is gone in src/pkg/alpha.py and occurs once in 0 other files" in (
        dropped[0].reason
    )
    assert "occurs once in 2 other files" in dropped[1].reason


def test_text_written_twice_in_one_other_file_has_no_place_it_moved_to(tree):
    (tree / ALPHA).write_text("", encoding="utf-8")
    (tree / "src" / "pkg" / "one.py").write_text("    return 1\n", encoding="utf-8")
    (tree / "src" / "pkg" / "two.py").write_text("    return 1\n    return 1\n", encoding="utf-8")
    anchor = killset.Anchor(ALPHA, "    return 1", "    return 0")
    assert killset.Tree(tree).holders(anchor) == []


def test_rows_after_refuses_a_table_whose_rows_name_no_source(tree, capsys):
    before = _before(tree, _recorded("A", "    return 1"))
    assert _run(tree, "rows", "--after", str(before), "--out", str(tree / "after.toml")) == 2
    assert "names no source" in capsys.readouterr().err


def test_a_replay_table_says_where_a_moved_guard_lives_now(tree):
    """After a card moves a guard, the cards after it still find the kill.

    The recorded text is gone from the file the first table names. A replay
    table under ``docs/mutation`` killed the same source at its new place, so
    the row is live there, with the tests that replay ran, and the replay
    table is counted as no table of its own.
    """
    (tree / ALPHA).write_text("def twice():\n    return 2\n", encoding="utf-8")
    (tree / "src" / "pkg" / "moved.py").write_text("def once():\n    return 1\n", encoding="utf-8")
    _table(tree, "u1.json", [_recorded("A", "    return 1")])
    assert _states(tree) == {"A": "stale"}

    _table(
        tree,
        "u2-replay.json",
        [
            _replayed(
                "A",
                "    return 1",
                file="src/pkg/moved.py",
                subset=["tests/test_beta.py"],
                moved="the same text, now in src/pkg/moved.py",
            )
        ],
        pass_kind="replay",
        when="2026-11-22 10:00 UTC",
    )
    found = killset.read_kill_set(tree)
    assert (found.tables, found.replay_tables, found.all_rows) == (1, 1, 1)
    [row] = found.rows
    assert (row.table, row.id, row.state) == ("u1.json", "A", "live")
    assert row.anchor.file == "src/pkg/moved.py"
    assert row.anchor.tests == ("tests/test_beta.py",)


def test_a_replay_that_did_not_kill_moves_nothing(tree):
    (tree / ALPHA).write_text("", encoding="utf-8")
    (tree / "src" / "pkg" / "moved.py").write_text("    return 1\n", encoding="utf-8")
    _table(tree, "u1.json", [_recorded("A", "    return 1")])
    _table(
        tree,
        "u2-replay.json",
        [_replayed("A", "    return 1", file="src/pkg/moved.py", deaths=0, status="zero")],
        pass_kind="replay",
    )
    assert _states(tree) == {"A": "stale"}


def test_the_newest_replay_gives_a_row_in_place_its_tests(tree):
    """The recorded subset names a test file a later card renamed; the replay knows the new one."""
    _table(tree, "u1.json", [_recorded("A", "    return 1", subset=["tests/test_gone.py"], killed=[])])
    assert killset.read_kill_set(tree).rows[0].anchor.tests == ()
    for name, when, subset in (
        ("u2-replay.json", "2026-11-22 10:00 UTC", "tests/test_alpha.py"),
        ("a9-replay.json", "2026-11-23 10:00 UTC", "tests/test_beta.py"),
    ):
        _table(
            tree,
            name,
            [_replayed("A", "    return 1", subset=[subset])],
            pass_kind="replay",
            when=when,
        )
    [row] = killset.read_kill_set(tree).rows
    assert (row.state, row.anchor.file) == ("live", ALPHA)
    assert row.anchor.tests == ("tests/test_beta.py",)


# ═══════════════════════════════════════════════════════════════════════════
# End to end, through the one driver
# ═══════════════════════════════════════════════════════════════════════════


def test_recorded_kills_replay_through_the_driver_and_check_clean(repo, capsys):
    """Table, row file, replay, check: the whole chain on a package with a known answer.

    The table records two kills in the driver suite's fixture package, one of
    them with a subset that no longer exists. `rows` writes them, the driver
    measures them under the replay pass, and `check` reads the measured table
    against itself, then against a copy in which one kill was lost.
    """
    _table(
        repo,
        "u1.json",
        [
            {
                **_recorded("CLAMP", "if value > limit:", "if value > 10000:"),
                "file": GUARDS_FILE,
                "subset": ["tests/test_guards.py"],
                "killed": ["tests/test_guards.py::test_clamp_caps_at_the_limit"],
            },
            {
                **_recorded("FLOOR", "if value < lowest:", "if value < -10000:"),
                "file": GUARDS_FILE,
                "subset": ["tests/test_renamed_since.py"],
                "killed": ["tests/test_guards.py::test_floor_raises_a_low_value"],
            },
        ],
    )
    spec = repo / "replay-rows.toml"
    assert _run(repo, "rows", GUARDS_FILE, "--out", str(spec), "--name", "u1-replay") == 0

    name, pass_kind, rows, dropped = mutate.load_spec(spec)
    batch = mutate.measure_batch(
        repo, name, rows, dropped, pass_kind=pass_kind,
        mapped=mutate.load_mapped(spec, pass_kind, rows),
    )
    assert [(one.id, one.status, one.subset) for one in batch.results] == [
        ("u1.CLAMP", "killed", ["tests/test_guards.py"]),
        ("u1.FLOOR", "killed", ["tests/test_guards.py"]),
    ]
    assert (repo / GUARDS_FILE).read_text(encoding="utf-8") == GUARDS
    _, sidecar = mutate.write_outputs(batch, repo / "measured")

    capsys.readouterr()
    assert killset.main(["killset.py", "check", str(sidecar), str(sidecar)]) == 0
    assert "2 rows killed before: 2 killed after as written" in capsys.readouterr().out

    lost = json.loads(sidecar.read_text(encoding="utf-8"))
    lost["rows"][1].update(status="zero", deaths=0, killed=[])
    after = repo / "measured" / "after.json"
    after.write_text(json.dumps(lost), encoding="utf-8")
    assert killset.main(["killset.py", "check", str(sidecar), str(after)]) == 1
    assert "LOST u1.json FLOOR: killed before, zero after" in capsys.readouterr().out
