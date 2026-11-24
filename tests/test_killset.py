"""``scripts/killset.py``, the recorded mutation kill set (U297): a refactor must kill every
mutation killed before, so counts are taken on trees small enough to verify by hand.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

from tests.test_mutation_driver import GUARDS, GUARDS_FILE, mutate
from tests.test_mutation_driver import (  # noqa: PLC0414, the guard's stand in root
    _stand_in_filesystem_root as _stand_in_filesystem_root,
)
from tests.test_mutation_driver import green_template as green_template  # noqa: PLC0414
from tests.test_mutation_driver import repo as repo  # noqa: PLC0414

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load():
    path = REPO_ROOT / "scripts" / "killset.py"
    spec = importlib.util.spec_from_file_location("cratekit_killset", path)
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
        "id": row_id, "description": f"row {row_id}", "file": ALPHA, "surface": "user",
        "old": old, "new": new, "status": "killed", "deaths": 1,
        "killed": ["tests/test_alpha.py::test_once"], "subset": ["tests/test_alpha.py"],
        "promoted": False, **extra,
    }


def _mixed() -> list[dict]:
    """One row of each state a reader tells apart, and a zero it must not count."""
    return [
        _recorded("LIVE", "    return 1"), _recorded("STALE", "    return 7"),
        _recorded("TWICE", "    return 2"),
        _recorded("GONE", "    return 1", file="src/pkg/removed.py"),
        _recorded("NAMELESS", "    return 1", file=None),
        _recorded("ZERO", "def once():", status="zero", deaths=0, killed=[]),
    ]


def _table(root: Path, name: str, rows: list[dict], **extra) -> Path:
    path = root / "docs" / "mutation" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {"name": Path(name).stem, "pass_kind": "light", "valid": True, "invalid_reason": ""}
    path.write_text(json.dumps({**body, **extra, "rows": rows}), encoding="utf-8")
    return path


@pytest.fixture
def tree(tmp_path) -> Path:
    (tmp_path / "src" / "pkg").mkdir(parents=True)
    (tmp_path / ALPHA).write_text(ALPHA_TEXT, encoding="utf-8")
    (tmp_path / "tests").mkdir()
    for name in ("test_alpha.py", "test_beta.py"):
        (tmp_path / "tests" / name).write_text("", encoding="utf-8")
    return tmp_path


def _run(root: Path, *argv: str) -> int:
    return killset.main(["killset.py", "--repo-root", str(root), *argv])


def _states(root: Path) -> dict[str, str]:
    return {row.id: row.state for row in killset.read_kill_set(root).rows}


# list: what a recorded row is today
def test_a_row_is_live_stale_ambiguous_or_gone_by_what_the_tree_holds(tree):
    """One of each, plus the two a reader must not count as kills."""
    refused = _recorded("REFUSED", "def twice():", status="refused", deaths=0, killed=[])
    _table(tree, "u1.json", [*_mixed(), refused])
    assert _states(tree) == {
        "LIVE": "live", "STALE": "stale", "TWICE": "ambiguous", "GONE": "gone", "NAMELESS": "gone"
    }


def test_the_same_substitution_recorded_twice_is_one_live_row(tree):
    _table(tree, "u1.json", [_recorded("A", "    return 1")])
    _table(tree, "u2.json", [_recorded("B", "    return 1")])
    _table(tree, "u3.json", [_recorded("C", "    return 1", new="    return 9")])
    found = killset.read_kill_set(tree)
    assert [(row.table, row.state) for row in found.rows] == [
        ("u1.json", "live"), ("u2.json", "duplicate"), ("u3.json", "live")
    ]


def test_list_prints_the_counts_and_one_line_a_file(tree, capsys):
    _table(tree, "u1.json", _mixed())
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
    elsewhere = _recorded("ELSE", "x", file="scripts/tool.py")
    _table(tree, "u1.json", [_recorded("LIVE", "    return 1"), elsewhere])
    assert _run(tree, "list", "src", "--rows") == 0
    out = capsys.readouterr().out
    assert "live      src/pkg/alpha.py  u1.json  LIVE" in out
    assert "scripts/tool.py" not in out


def test_a_path_outside_the_checkout_is_refused(tree, tmp_path_factory, capsys):
    elsewhere = tmp_path_factory.mktemp("elsewhere")
    _table(tree, "u1.json", [_recorded("LIVE", "    return 1")])
    assert _run(tree, "list", str(elsewhere)) == 2
    assert "is not inside" in capsys.readouterr().err


# rows: a row file the driver can run
def test_rows_writes_the_live_rows_and_counts_what_it_left_out(tree, capsys):
    """The stale row is left out of the file and named in the count."""
    _table(tree, "u1.json", _mixed()[:3])
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
    # It applies cleanly: its text occurs once, and the driver's own substitution takes it.
    applied = mutate.apply_mutation(ALPHA_TEXT, rows[0].old, rows[0].new)
    assert applied == ALPHA_TEXT.replace("    return 1", "    return 0")


def test_rows_for_a_directory_takes_every_file_under_it(tree):
    (tree / "src" / "pkg" / "beta.py").write_text("B = 1\n", encoding="utf-8")
    _table(tree, "u1.json", [
        _recorded("A", "    return 1"),
        _recorded("B", "B = 1", new="B = 2", file="src/pkg/beta.py"),
        _recorded("S", "x = 1", file="scripts/tool.py"),
    ])
    out = tree / "rows.toml"
    assert _run(tree, "rows", "src/pkg/", "--out", str(out), "--name", "area") == 0
    data = tomllib.loads(out.read_text(encoding="utf-8"))
    assert data["name"] == "area"
    assert [row["file"] for row in data["rows"]] == [ALPHA, "src/pkg/beta.py"]


def test_a_row_file_named_for_its_rows_measures_the_table_beside_it(tree):
    """``u1-replay-before-rows.toml`` is measured into ``u1-replay-before.json``, read by name."""
    _table(tree, "u1.json", [_recorded("A", "    return 1")])
    out = tree / "u1-replay-before-rows.toml"
    assert _run(tree, "rows", ALPHA, "--out", str(out)) == 0
    assert tomllib.loads(out.read_text(encoding="utf-8"))["name"] == "u1-replay-before"
    assert _run(tree, "rows", ALPHA, "--out", str(out), "--name", "given") == 0
    assert tomllib.loads(out.read_text(encoding="utf-8"))["name"] == "given"
    plain = tree / "-rows.toml"
    assert _run(tree, "rows", ALPHA, "--out", str(plain)) == 0
    assert tomllib.loads(plain.read_text(encoding="utf-8"))["name"] == "-rows"


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
    "plain", "", "it's", "'''", "ends with a quote'", "'starts with one", "a\nb",
    "\nleading newline", "trailing newline\n", "a\n'''\nb", "block ending in a quote'\n'",
    'double "quotes" and a \\ backslash', "tab\tinside", "carriage\r\nreturn",
    "bell \x07 and delete \x7f", "ünïcödé and \U0001f3b5",
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


# check: every row killed before is killed after
def _measured(row_id: str, *, deaths: int = 1, status: str = "killed", **extra) -> dict:
    return {
        "id": f"u1.{row_id}", "source": {"table": "u1.json", "id": row_id}, "file": ALPHA,
        "old": f"old {row_id}", "new": "new", "status": status, "deaths": deaths, **extra,
    }


def _check(tmp_path: Path, before: list[dict], after: list[dict], **after_extra) -> int:
    first = _table(tmp_path, "before.json", before, pass_kind="replay")
    second = _table(tmp_path, "after.json", after, pass_kind="replay", **after_extra)
    return killset.main(["killset.py", "check", str(first), str(second)])


def _mapping(to: str, reason: str = "merged into A") -> dict:
    return {"source": {"table": "u1.json", "id": "B"}, "to": to, "reason": reason}


def _ab() -> list[dict]:
    return [_measured("A"), _measured("B")]


ZERO = {"deaths": 0, "status": "zero"}


@pytest.mark.parametrize(
    ("before", "after", "extra", "code", "said"),
    [
        ([*_ab(), _measured("Z", **ZERO)], [*_ab(), _measured("Z", **ZERO)], {}, 0,
         ["2 rows killed before: 2 killed after as written"]),
        (_ab(), [_measured("A"), _measured("B", **ZERO)], {}, 1,
         ["1 lost", "LOST u1.json B: killed before, zero after (0 deaths)"]),
        # The driver says of such a row that it is neither a zero nor a clean kill.
        (_ab(), [_measured("A"), _measured("B", status="collect-error")], {}, 1,
         ["LOST u1.json B: killed before, collect-error after (1 deaths)"]),
        (_ab(), [_measured("A")], {}, 1,
         ["LOST u1.json B: killed before, and no row and no mapping after"]),
        (_ab(), [_measured("A")], {"mapped": [_mapping("u1.A")]}, 0,
         ["1 covered by a mapped row that is killed, 0 lost"]),
        (_ab(), [_measured("A", **ZERO)], {"mapped": [_mapping("u1.A")]}, 1,
         ["LOST u1.json B: mapped to 'u1.A', which is zero after"]),
        (_ab(), [_measured("A")], {"mapped": [_mapping("u1.C")]}, 1,
         ["mapped to 'u1.C', which is no row after"]),
        (_ab(), [_measured("A")], {"mapped": [_mapping("u1.A", " ")]}, 1,
         ["mapped to 'u1.A' with no reason"]),
        ([_measured("B")], [_measured("A", status="collect-error")],
         {"mapped": [_mapping("u1.A")]}, 1, ["mapped to 'u1.A', which is collect-error after"]),
    ],
    ids=[
        "every-kill-kept", "one-lost-kill-named", "a-collection-error-is-lost-though-a-death",
        "no-row-and-no-mapping", "mapped-to-a-surviving-killed-row", "mapped-to-a-row-not-killed",
        "mapped-to-no-row", "mapped-for-no-reason", "mapped-onto-a-row-that-only-broke-collection",
    ],
)
def test_check_holds_each_kill_to_its_row_or_mapping_after(
    tmp_path, capsys, before, after, extra, code, said
):
    assert _check(tmp_path, before, after, **extra) == code
    out = capsys.readouterr().out
    for line in said:
        assert line in out


def test_a_row_that_broke_collection_before_is_held_to_no_less_after(tmp_path, capsys):
    broke = _measured("A", status="collect-error")
    assert _check(tmp_path, [broke], [broke]) == 0
    assert _check(tmp_path, [broke], [_measured("A")]) == 0
    capsys.readouterr()
    assert _check(tmp_path, [broke], [_measured("A", deaths=0, status="zero")]) == 1
    assert "LOST u1.json A: collect-error before, zero after" in capsys.readouterr().out


@pytest.mark.parametrize("which", ["before", "after"])
def test_check_refuses_a_table_with_two_rows_for_one_source(tmp_path, capsys, which):
    """Two rows under one source: whichever was read first would decide the verdict."""
    one, twice = [_measured("A")], [_measured("A"), _measured("A", deaths=0, status="zero")]
    before, after = (twice, one) if which == "before" else (one, twice)
    assert _check(tmp_path, before, after) == 2
    assert f"{which}.json holds two rows for u1.json A" in capsys.readouterr().err


def test_check_holds_a_row_whose_text_changed_to_a_moved_reason(tmp_path, capsys):
    """A different substitution under the same source is not the same kill until it says why."""
    before = [_measured("A")]
    silent = [_measured("A", file="src/pkg/beta.py")]
    assert _check(tmp_path, before, silent) == 1
    out = capsys.readouterr().out
    assert "its text differs between the two tables, and it gives no moved reason" in out
    said = [_measured("A", file="src/pkg/beta.py", moved="split out with its guard, by hand")]
    assert _check(tmp_path, before, said) == 0
    assert "1 killed after at a new anchor" in capsys.readouterr().out


AUTOMATIC = "the same text, now in src/pkg/beta.py, was in src/pkg/alpha.py"


def test_a_row_the_tool_moved_must_still_die_by_a_test_that_killed_it_before(tmp_path, capsys):
    """The same text in another file is not the same guard: it vouches for nothing."""
    before = [_measured("A", killed=["tests/test_alpha.py::test_once"])]
    killed = ["tests/test_beta.py::test_beta_caps[low - high]"]
    twin = [_measured("A", file="src/pkg/beta.py", moved=AUTOMATIC, killed=killed)]
    assert _check(tmp_path, before, twin) == 1
    out = capsys.readouterr().out
    assert "LOST u1.json A: its text differs between the two tables, and it is killed there " in out
    assert "(test_once then, test_beta_caps now)" in out
    assert "say why in `moved` in your own words" in out


def test_a_row_the_tool_moved_passes_when_the_same_test_kills_it_wherever_that_test_lives(
    tmp_path, capsys
):
    """The test moved with the code it tests: another file, the same name, the same guard."""
    before = [_measured("A", killed=["tests/test_alpha.py::test_once[a]", "tests/test_alpha.py::test_two"])]
    killed = ["tests/test_beta.py::TestCaps::test_once[b - c]"]
    moved = [_measured("A", file="src/pkg/beta.py", moved=AUTOMATIC, killed=killed)]
    assert _check(tmp_path, before, moved) == 0
    assert "1 killed after at a new anchor, 0 covered" in capsys.readouterr().out


def test_a_person_may_vouch_for_a_moved_row_no_test_in_common_kills(tmp_path):
    before = [_measured("A", killed=["tests/test_alpha.py::test_once"])]
    why = "the guard moved with pair_settle and its test was renamed with it"
    killed = ["tests/test_beta.py::test_renamed"]
    vouched = [_measured("A", file="src/pkg/beta.py", killed=killed, moved=why)]
    assert _check(tmp_path, before, vouched) == 0


def test_a_row_in_place_needs_no_test_in_common(tmp_path):
    """The same text in the same file is the same guard, whatever its tests are called now."""
    before = [_measured("A", killed=["tests/test_alpha.py::test_once"])]
    after = [_measured("A", killed=["tests/test_alpha.py::test_renamed"])]
    assert _check(tmp_path, before, after) == 0


def test_the_tests_that_killed_a_row_are_read_by_name():
    row = {"killed": ["tests/a.py::test_x[p - q]", "tests/b.py::TestK::test_y", "", 3, "test_z"]}
    assert killset.killer_names(row) == {"test_x", "test_y", "test_z"}
    assert killset.killer_names({}) == frozenset()


def test_a_table_of_the_older_form_is_read_by_its_deaths(tmp_path):
    """No status at all: a death is a kill, as the reader counts it."""
    old = {"id": "G1", "file": ALPHA, "old": "a", "new": "b", "deaths": 2}
    first = _table(tmp_path, "before.json", [old])
    second = _table(tmp_path, "after.json", [{**old, "deaths": 0}])
    assert killset.strength(old) == 2
    assert killset.main(["killset.py", "check", str(first), str(first)]) == 0
    assert killset.main(["killset.py", "check", str(first), str(second)]) == 1


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


# After a refactor: where a recorded row lives now
def _git(root: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-c", "user.email=killset@test", "-c", "user.name=killset", *args],
        cwd=root, capture_output=True, check=False,
    )
    assert done.returncode == 0, done.stderr.decode()
    return done.stdout.decode().strip()


def _commit(tree: Path) -> str:
    _git(tree, "init", "-q", "-b", "main")
    _git(tree, "add", "-A")
    _git(tree, "commit", "-q", "-m", "before the refactor")
    return _git(tree, "rev-parse", "--short", "HEAD")


@pytest.fixture
def committed(tree) -> tuple[Path, str]:
    return tree, _commit(tree)


def _before(tree: Path, *rows: dict, head: str = "") -> Path:
    """A replay table measured before a refactor, at ``head``, outside ``docs/mutation``."""
    path = tree / "before.json"
    body = {"name": "before", "pass_kind": "replay", "valid": True, "invalid_reason": ""}
    body["head"] = head
    path.write_text(json.dumps({**body, "rows": list(rows)}), encoding="utf-8")
    return path


def _replayed(row_id: str, old: str, **extra) -> dict:
    return {**_recorded(f"u1.{row_id}", old), "source": {"table": "u1.json", "id": row_id}, **extra}


def _rows_after(tree: Path, before: Path, name: str = "after.toml") -> Path:
    """The rows command run after a refactor over ``before``, which must succeed. Its file."""
    out = tree / name
    assert _run(tree, "rows", "--after", str(before), "--out", str(out)) == 0
    return out


def test_rows_after_writes_text_still_in_its_file_as_it_was(tree, capsys):
    before = _before(tree, _replayed("A", "    return 1"))
    out = _rows_after(tree, before)
    assert "1 rows in place and 0 moved" in capsys.readouterr().out
    _, _, rows, dropped = mutate.load_spec(out)
    assert [(row.id, row.file, row.source, row.moved) for row in rows] == [
        ("u1.A", ALPHA, ("u1.json", "A"), "")
    ]
    assert dropped == []


def test_rows_after_follows_text_that_moved_to_one_other_file(committed, capsys):
    """A file split: the guard's text left ``alpha.py`` for ``moved.py``, which is new."""
    tree, head = committed
    (tree / ALPHA).write_text("def twice():\n    return 2\n", encoding="utf-8")
    (tree / "src" / "pkg" / "moved.py").write_text("def once():\n    return 1\n", encoding="utf-8")
    before = _before(tree, _replayed("A", "    return 1"), head=head)
    out = _rows_after(tree, before)
    assert "0 rows in place and 1 moved" in capsys.readouterr().out
    _, _, rows, _ = mutate.load_spec(out)
    assert rows[0].file == "src/pkg/moved.py"
    assert rows[0].moved == "the same text, now in src/pkg/moved.py, was in src/pkg/alpha.py"
    assert rows[0].source == ("u1.json", "A")


def _twin_stays(tree: Path) -> None:
    pass


def _twin_is_renamed(tree: Path) -> None:
    (tree / "src" / "pkg" / "twin.py").rename(tree / "src" / "pkg" / "renamed.py")


def _twin_is_split(tree: Path) -> None:
    (tree / "src" / "pkg" / "twin.py").write_text("def other():\n    pass\n", encoding="utf-8")
    (tree / "src" / "pkg" / "twin_caps.py").write_text("    return 1\n", encoding="utf-8")


@pytest.mark.parametrize("refactor", [_twin_stays, _twin_is_renamed, _twin_is_split])
def test_a_deleted_guard_is_not_anchored_on_its_twin_wherever_the_twin_is_now(
    tree, capsys, refactor
):
    """Two then and one now: the line left may be the twin's, however like a move it looks."""
    (tree / "src" / "pkg" / "twin.py").write_text("def other():\n    return 1\n", encoding="utf-8")
    head = _commit(tree)
    (tree / ALPHA).write_text("def twice():\n    return 2\n", encoding="utf-8")
    refactor(tree)
    before = _before(tree, _replayed("A", "    return 1"), head=head)
    out = _rows_after(tree, before)
    assert "0 rows in place and 0 moved" in capsys.readouterr().out
    data = tomllib.loads(out.read_text(encoding="utf-8"))
    assert "rows" not in data
    [dropped] = data["dropped"]
    assert dropped["id"] == "u1.A"
    assert f"it stood in 2 places at {head}" in dropped["reason"]
    assert "may be another guard's line and not this one moved" in dropped["reason"]


def test_a_line_written_new_elsewhere_reads_as_a_move_and_check_is_what_catches_it(
    committed, capsys
):
    """One place then and one now, yet another guard: ``check`` asks a test in common."""
    tree, head = committed
    (tree / ALPHA).write_text("def twice():\n    return 2\n", encoding="utf-8")
    (tree / "src" / "pkg" / "delta.py").write_text("def new():\n    return 1\n", encoding="utf-8")
    before = _before(tree, _replayed("A", "    return 1"), head=head)
    out = _rows_after(tree, before)
    _, _, rows, _ = mutate.load_spec(out)
    assert rows[0].file == "src/pkg/delta.py"
    assert rows[0].moved.startswith(killset.AUTOMATIC_MOVE)
    # Measured there, it dies by the new line's test and none of its own.
    measured = {
        **_replayed("A", "    return 1"), "file": rows[0].file, "moved": rows[0].moved,
        "killed": ["tests/test_delta.py::test_delta_caps"],
    }
    then = {"rows": [_replayed("A", "    return 1")]}
    verdict = killset.compare_tables(then, {"rows": [measured]})
    assert len(verdict.lost) == 1 and "test_delta_caps now" in verdict.lost[0]


@pytest.mark.parametrize("head", ["", "0123456789abcdef0123456789abcdef01234567"])
def test_a_move_git_cannot_vouch_for_is_not_a_move(committed, capsys, head):
    """No commit named, or one git does not know: not being able to look is not a no."""
    tree, _ = committed
    (tree / ALPHA).write_text("def twice():\n    return 2\n", encoding="utf-8")
    (tree / "src" / "pkg" / "moved.py").write_text("def once():\n    return 1\n", encoding="utf-8")
    before = _before(tree, _replayed("A", "    return 1"), head=head)
    out = _rows_after(tree, before)
    assert "0 rows in place and 0 moved" in capsys.readouterr().out
    [dropped] = tomllib.loads(out.read_text(encoding="utf-8"))["dropped"]
    assert "git cannot read the tree at the commit the table was measured on" in dropped["reason"]
    assert (head or "none named") in dropped["reason"]


def test_how_many_places_a_text_stood_in_is_read_from_the_commit(committed):
    tree, head = committed
    (tree / ALPHA).write_text("nothing left\n", encoding="utf-8")
    then = killset.Commit(tree, head)
    assert then.stood(killset.Anchor(ALPHA, "    return 1", "")) == 1
    assert then.stood(killset.Anchor(ALPHA, "    return 2", "")) == 2
    assert then.stood(killset.Anchor(ALPHA, "    return 7", "")) == 0
    # Another suffix is another kind of file, and a top directory the commit lacks is empty.
    assert then.stood(killset.Anchor("src/pkg/alpha.md", "    return 1", "")) == 0
    assert then.stood(killset.Anchor("scripts/tool.py", "    return 1", "")) == 0
    assert killset.Commit(tree, "").stood(killset.Anchor(ALPHA, "    return 1", "")) is None
    assert killset.Commit(tree, "no-such-commit").texts("src") is None


def test_outside_a_repository_nothing_is_read_as_moved(tree):
    """A tree git knows nothing of: the answer is that it cannot say, never nothing."""
    assert killset.Commit(tree, "abc1234").stood(killset.Anchor(ALPHA, "    return 1", "")) is None


def test_rows_after_names_its_batch_as_rows_does(committed):
    tree, head = committed
    before = _before(tree, _replayed("A", "    return 1"), head=head)
    out = _rows_after(tree, before, "u1-replay-after-rows.toml")
    assert tomllib.loads(out.read_text(encoding="utf-8"))["name"] == "u1-replay-after"


def test_rows_after_leaves_text_it_cannot_place_for_the_author(tree, capsys):
    """Gone everywhere, or in two places: nothing says which guard it is now."""
    (tree / ALPHA).write_text("def twice():\n    return 2\n", encoding="utf-8")
    (tree / "src" / "pkg" / "one.py").write_text("    return 5\n", encoding="utf-8")
    (tree / "src" / "pkg" / "two.py").write_text("    return 5\n", encoding="utf-8")
    before = _before(
        tree, _replayed("GONE", "    return 1"), _replayed("SPLIT", "    return 5"),
        _replayed("KEPT", "    return 2"),
        _replayed("ZERO", "def twice():", deaths=0, status="zero"),
    )
    out = _rows_after(tree, before)
    assert "1 rows in place and 0 moved" in capsys.readouterr().out
    _, _, rows, dropped = mutate.load_spec(out)
    assert [row.id for row in rows] == ["u1.KEPT"]
    assert [one.id for one in dropped] == ["u1.GONE", "u1.SPLIT"]
    unplaced = "unplaced: the text is gone in src/pkg/alpha.py and occurs once in 0 other files"
    assert unplaced in dropped[0].reason
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
    """A replay names a moved guard's row live at its new place, and is no table of its own."""
    (tree / ALPHA).write_text("def twice():\n    return 2\n", encoding="utf-8")
    (tree / "src" / "pkg" / "moved.py").write_text("def once():\n    return 1\n", encoding="utf-8")
    _table(tree, "u1.json", [_recorded("A", "    return 1")])
    assert _states(tree) == {"A": "stale"}
    replayed = _replayed(
        "A", "    return 1", file="src/pkg/moved.py", subset=["tests/test_beta.py"],
        moved="the same text, now in src/pkg/moved.py",
    )
    _table(tree, "u2-replay.json", [replayed], pass_kind="replay", when="2026-11-22 10:00 UTC")
    found = killset.read_kill_set(tree)
    assert (found.tables, found.replay_tables, found.all_rows) == (1, 1, 1)
    [row] = found.rows
    assert (row.table, row.id, row.state) == ("u1.json", "A", "live")
    assert row.anchor.file == "src/pkg/moved.py"
    assert row.anchor.tests == ("tests/test_beta.py",)


def test_a_replay_at_another_guards_line_does_not_bring_a_dead_row_back(tree):
    """A committed table that put the row on a twin: the reader holds it to check's rule."""
    (tree / ALPHA).write_text("def twice():\n    return 2\n", encoding="utf-8")
    (tree / "src" / "pkg" / "twin.py").write_text("def other():\n    return 1\n", encoding="utf-8")
    _table(tree, "u1.json", [_recorded("A", "    return 1")])
    def replay(**extra) -> None:
        replayed = _replayed("A", "    return 1", file="src/pkg/twin.py", **extra)
        _table(tree, "u2-replay.json", [replayed], pass_kind="replay")
    replay(moved=AUTOMATIC, killed=["tests/test_twin.py::test_other"])
    assert _states(tree) == {"A": "stale"}
    replay(moved="")
    assert _states(tree) == {"A": "stale"}
    replay(moved=AUTOMATIC, killed=["tests/test_moved.py::test_once"])
    assert _states(tree) == {"A": "live"}
    replay(moved="moved by hand with its guard", killed=["tests/test_twin.py::test_other"])
    assert _states(tree) == {"A": "live"}


def test_a_replay_that_did_not_kill_moves_nothing(tree):
    (tree / ALPHA).write_text("", encoding="utf-8")
    (tree / "src" / "pkg" / "moved.py").write_text("    return 1\n", encoding="utf-8")
    _table(tree, "u1.json", [_recorded("A", "    return 1")])
    replayed = _replayed("A", "    return 1", file="src/pkg/moved.py", deaths=0, status="zero")
    _table(tree, "u2-replay.json", [replayed], pass_kind="replay")
    assert _states(tree) == {"A": "stale"}


def test_the_newest_replay_gives_a_row_in_place_its_tests(tree):
    """The recorded subset names a test file a later card renamed; the replay knows the new one."""
    _table(tree, "u1.json", [_recorded("A", "    return 1", subset=["tests/test_gone.py"], killed=[])])
    assert killset.read_kill_set(tree).rows[0].anchor.tests == ()
    for name, when, subset in (
        ("u2-replay.json", "2026-11-22 10:00 UTC", "tests/test_alpha.py"),
        ("a9-replay.json", "2026-11-23 10:00 UTC", "tests/test_beta.py"),
    ):
        replayed = _replayed("A", "    return 1", subset=[subset])
        _table(tree, name, [replayed], pass_kind="replay", when=when)
    [row] = killset.read_kill_set(tree).rows
    assert (row.state, row.anchor.file) == ("live", ALPHA)
    assert row.anchor.tests == ("tests/test_beta.py",)


# End to end, through the one driver
def test_recorded_kills_replay_through_the_driver_and_check_clean(repo, capsys):
    """The whole chain on a package with a known answer, then a copy that lost one kill."""
    _table(repo, "u1.json", [
        _recorded(
            "CLAMP", "if value > limit:", "if value > 10000:", file=GUARDS_FILE,
            subset=["tests/test_guards.py"],
            killed=["tests/test_guards.py::test_clamp_caps_at_the_limit"],
        ),
        _recorded(
            "FLOOR", "if value < lowest:", "if value < -10000:", file=GUARDS_FILE,
            subset=["tests/test_renamed_since.py"],
            killed=["tests/test_guards.py::test_floor_raises_a_low_value"],
        ),
    ])
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
