"""Tests for ``scripts/refactor_measure.py``, the one measure of U290's refactor (U296).

The line classifier, the file list, packages, outside names, and the six commands
end to end over a small repository in a temporary directory. Nothing reads the
real tree: its numbers sit in the unit's record, and a second read would cost more.
"""

from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path

import pytest

from tests._refactor_measure import measure

SOURCE = measure.SOURCE


def _run(root: Path, *argv: str) -> tuple[int, str]:
    out = io.StringIO()
    code = measure.main(list(argv), root=root, out=out)
    return code, out.getvalue()


def _write(root: Path, files: dict[str, str]) -> None:
    for path, text in files.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


def _block(count: int, prefix: str = "step") -> str:
    return "".join(f"{prefix}_{number} = compute({number})\n" for number in range(count))


RULES = (
    'CORE_INTERFACE = ("config",)\n'
    'TOGGLE_HOMES = {"labels": ("cratekit.label",), "repair": ()}\n'
    "CORE_NAMES_CEILING = 3\n"
)
REGISTRY = (
    "ENTRIES = (\n"
    '    Entry(name="sync", module="cratekit.sync.cli", builder="build"),\n'
    '    Entry(name="label.sweep", module="cratekit.label.cli", builder="build", module_id="labels"),\n'
    ")\n"
)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A small repository with one of everything the readings look for."""
    _write(
        tmp_path,
        {
            f"{SOURCE}/__init__.py": '"""The package."""\n',
            f"{SOURCE}/core/__init__.py": "",
            f"{SOURCE}/core/config.py": (
                '"""Config."""\n\n# a comment\ndef load():\n    return 1\n\n\ndef _lock():\n    return 2\n'
            ),
            f"{SOURCE}/core/drift.py": "def check():\n    return 3\n",
            f"{SOURCE}/cli/__init__.py": "",
            f"{SOURCE}/cli/registry.py": REGISTRY,
            f"{SOURCE}/label/__init__.py": "",
            f"{SOURCE}/label/registry.py": "class Registry: ...\n" + _block(7),
            f"{SOURCE}/label/cli.py": "def build(parser, entry): ...\n",
            f"{SOURCE}/sync/__init__.py": "",
            f"{SOURCE}/sync/cli.py": (
                "from cratekit.core.config import _lock, load\n"
                "from cratekit.core.drift import check\n"
                "from cratekit.label.registry import Registry\n\n"
                "def build(parser, entry): ...\n" + _block(7)
            ),
            f"{SOURCE}/_vendor/thing.py": _block(7) + "x = 1\n" * 2000,
            "tests/test_import_rules.py": RULES,
            "tests/test_sync.py": (
                "from cratekit.core import config\n\n"
                "def test_load(monkeypatch):\n"
                '    monkeypatch.setattr(config, "_lock", None)\n'
                '    monkeypatch.setattr("cratekit.core.config.load", None)\n'
                "    assert config.load\n"
            ),
        },
    )
    return tmp_path


# Lines


def test_a_line_is_blank_then_comment_then_docstring_then_code():
    source = (
        '"""Module docstring,\n'  # docstring
        "\n"  # blank, though inside the docstring
        '# not a comment: it is inside the string\n'  # docstring
        'and its last line."""\n'  # docstring
        "\n"  # blank
        "# a comment\n"  # comment
        "value = 1  # a trailing comment is code\n"  # code
        "def read():\n"  # code
        '    """Function docstring."""\n'  # docstring
        '    "a string that opens nothing"\n'  # code
        "    return value\n"  # code
    )
    count = measure.count_lines(source)
    assert (count.blank, count.comment, count.docstring, count.code) == (2, 1, 4, 4)
    assert count.lines == len(source.splitlines()) == 11


def test_a_class_docstring_is_docstring_and_counts_add_up():
    one = measure.count_lines('class A:\n    """Doc."""\n')
    two = measure.count_lines("x = 1\n\n")
    assert (one.docstring, one.code) == (1, 1)
    total = one + two
    assert (total.code, total.docstring, total.blank, total.lines) == (2, 1, 1, 4)


def test_test_functions_are_counted_at_module_level_and_in_classes():
    source = (
        "def test_one(): ...\n"
        "def helper(): ...\n"
        "class TestThing:\n"
        "    def test_two(self): ...\n"
        "    async def test_three(self): ...\n"
        "    def setup(self): ...\n"
        "def outer():\n"
        "    def test_nested(): ...\n"
    )
    assert measure.count_test_functions(source) == 3


# Files and packages


@pytest.mark.parametrize(
    "path, package",
    [
        ("src/cratekit/__init__.py", "root"),
        ("src/cratekit/core/config.py", "core"),
        ("src/cratekit/cli/verbs/login.py", "cli"),
        ("src/cratekit/modules/extras.py", "modules"),
        ("src/cratekit/modules/outbound/mirror.py", "modules.outbound"),
        ("src/cratekit/modules/tools/__init__.py", "modules.tools"),
        ("tests/test_config.py", "tests"),
    ],
)
def test_the_package_of_a_path(path, package):
    assert measure.package_of_path(path) == package


def test_a_module_is_named_for_its_path_and_a_package_for_its_initializer():
    assert measure.module_name("src/cratekit/core/config.py") == "cratekit.core.config"
    assert measure.module_name("src/cratekit/label/__init__.py") == "cratekit.label"


def test_the_vendored_tree_is_never_read(repo):
    files = measure.python_files(repo, SOURCE)
    assert f"{SOURCE}/core/config.py" in files
    assert not [path for path in files if "_vendor" in path]


def test_in_a_checkout_the_files_are_the_ones_git_tracks_or_would(repo):
    """A module not yet committed is measured, and a file git ignores never is."""
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "add", "src"], cwd=repo, check=True, capture_output=True)
    (repo / ".gitignore").write_text("scratch.py\n")
    (repo / SOURCE / "core" / "scratch.py").write_text("x = 1\n")
    (repo / SOURCE / "core" / "fresh.py").write_text("x = 1\n")
    files = measure.python_files(repo, SOURCE)
    assert f"{SOURCE}/core/config.py" in files and f"{SOURCE}/core/fresh.py" in files
    assert f"{SOURCE}/core/scratch.py" not in files
    assert not [path for path in files if "_vendor" in path]


def test_one_file_can_be_named_as_a_scope(repo):
    assert measure.python_files(repo, f"{SOURCE}/core/config.py") == [f"{SOURCE}/core/config.py"]


# Names used from outside a set of files


def test_outside_lists_every_form_of_use_and_marks_the_private_ones(repo):
    sources = measure.read_sources(repo, [SOURCE, "tests"])
    uses = measure.outside_uses(sources, [f"{SOURCE}/core/config.py"])
    seen = {(use.name, use.user.rsplit("/", 1)[-1], use.kind) for use in uses}
    assert seen == {
        ("load", "cli.py", "import"),
        ("_lock", "cli.py", "import"),
        ("load", "test_sync.py", "attribute"),
        ("load", "test_sync.py", "string"),
        ("_lock", "test_sync.py", "string"),
    }


def test_a_name_used_only_inside_the_named_files_is_not_listed(repo):
    sources = measure.read_sources(repo, [SOURCE, "tests"])
    owned = [f"{SOURCE}/core/config.py", f"{SOURCE}/sync/cli.py", "tests/test_sync.py"]
    assert measure.outside_uses(sources, owned) == []


# The commands, end to end


def test_lines_prints_each_package_the_total_and_the_large_files(repo):
    _write(repo, {f"{SOURCE}/sync/big.py": "x = 1\n" * 1501})
    code, out = _run(repo, "lines", SOURCE)
    assert code == 0
    rows = {line.split()[0]: line.split()[1:] for line in out.splitlines() if line.strip()}
    # files, lines, code, docstring, comment, blank, over 1,500
    assert rows["core"] == ["3", "11", "6", "1", "1", "3", "0"]
    assert rows["sync"][:2] == ["3", "1513"] and rows["sync"][-1] == "1"
    assert rows["all"][:2] == ["12", "1538"] and rows["all"][-1] == "1"
    assert "files over 1500 lines: 1" in out and f"1501  {SOURCE}/sync/big.py" in out
    assert "_vendor" not in out


def test_lines_with_files_lists_every_file(repo):
    _, out = _run(repo, "lines", f"{SOURCE}/core", "--files")
    assert "every file:" in out and f"{SOURCE}/core/drift.py" in out


def test_duplicates_prints_blocks_lines_files_and_window_places(repo):
    code, out = _run(repo, "duplicates")
    assert code == 0
    assert "blocks of 6 logical lines or more: 2 blocks over 14 logical lines in 2 files" in out
    assert "4 places of a repeated window of 6" in out
    rows = {line.split()[0]: line.split()[1:] for line in out.splitlines()[1:]}
    assert rows["label"] == ["1", "7", "2"] and rows["sync"] == ["1", "7", "2"]


def test_duplicates_takes_the_block_size_and_lists_the_longest_first(repo):
    _, larger = _run(repo, "duplicates", "--min", "8")
    assert "blocks of 8 logical lines or more: 0 blocks" in larger
    _, listed = _run(repo, "duplicates", "--list", "1")
    assert f"   7 logical  {SOURCE}/label/registry.py:2-8" in listed


def test_the_renamed_reading_is_printed_only_when_asked_and_matches_changed_names(repo):
    _write(repo, {f"{SOURCE}/intake/__init__.py": "", f"{SOURCE}/intake/x.py": _block(7, "other")})
    _, exact = _run(repo, "duplicates")
    assert "renamed" not in exact and "2 blocks" in exact
    _, both = _run(repo, "duplicates", "--renamed")
    assert "renamed (identifiers, numbers and strings normalised)" in both
    assert "blocks of 6 logical lines or more: 3 blocks over 21 logical lines in 3 files" in both


def test_duplicates_says_where_a_window_stands(repo):
    held = measure.Copies(measure.read_sources(repo, [SOURCE])).held()
    digest = sorted(held["label"])[0]
    code, out = _run(repo, "duplicates", "--where", digest)
    assert code == 0 and f"{SOURCE}/label/registry.py:" in out and f"{SOURCE}/sync/cli.py:" in out
    code, out = _run(repo, "duplicates", "--where", "0" * 16)
    assert code == 1 and "is not a repeated window here" in out


def test_imports_prints_the_seam_counts(repo):
    code, out = _run(repo, "imports", "--names")
    assert code == 0
    counts = {
        line.split(None, 1)[1]: int(line.split()[0])
        for line in out.splitlines()
        if line[:7].strip().isdigit()
    }
    assert counts["private names crossing a package"] == 1
    assert counts["core modules feature packages reach"] == 2
    assert counts["reaches off the interface list"] == 1
    assert counts["top level imports of a toggleable package"] == 1
    assert counts["lazy imports of a toggleable package"] == 0
    assert counts["verbs left dangling, summed over the toggles"] == 1
    assert counts["distinct core names feature packages use"] == 3
    assert counts["the ceiling on distinct core names"] == 3
    assert "cratekit.core.config._lock  from sync" in out
    assert "1  drift  off the list: sync" in out
    assert "labels        1 verbs dangle, by   1 imports" in out
    assert "  cratekit.core.drift.check\n" in out


def test_outside_prints_each_name_its_users_and_refuses_an_unknown_file(repo):
    code, out = _run(repo, "outside", f"{SOURCE}/core/config.py", "--where")
    assert code == 0
    assert "2 names of 1 files are used outside them, 1 of them private (marked _)" in out
    assert "_ cratekit.core.config._lock  2 files (1 source, 1 tests and scripts)" in out
    assert "  cratekit.core.config.load  2 files (1 source, 1 tests and scripts)" in out
    assert "tests/test_sync.py:5,6" in out
    code, out = _run(repo, "outside", "src/cratekit/core/nothing.py")
    assert code == 2 and "src/cratekit/core/nothing.py" in out


def _allow(repo: Path, directory: str, package: str, lines: list[str]) -> Path:
    path = repo / directory / f"{package}.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# what this file is\n# and how it shrinks\n" + "".join(f"{line}\n" for line in lines))
    return path


def _allow_everything(repo: Path) -> None:
    sources = measure.read_sources(repo, [SOURCE])
    for package, held in measure.Copies(sources).held().items():
        _allow(repo, measure.DUPLICATION_ALLOWANCES, package, sorted(held.elements()))
    _allow(
        repo,
        measure.IMPORT_ALLOWANCES,
        "sync",
        [
            "dangling labels cratekit.label.registry",
            "off-interface cratekit.core.drift",
            "private cratekit.core.config._lock",
            "top-level cratekit.label.registry.Registry",
        ],
    )


def test_table_prints_points_two_to_five_and_is_clean_on_a_full_allowance(repo):
    _allow_everything(repo)
    code, out = _run(repo, "table")
    assert code == 0
    for heading in ("point 2, size", "point 3, duplication", "point 4, seams", "point 5, tests"):
        assert heading in out
    assert "37 lines in 11 files under src/cratekit (code 30, docstring 2, comment 1, blank 4)" in out
    assert "outside _vendor; 0 files over 1500 lines" in out
    assert "exact blocks of 6 logical lines or more: 2 blocks over 14 logical lines in 2 files" in out
    assert "allowance: 4 lines in 2 files, 4 still found; beyond the allowance: 0" in out
    assert "allowance: 4 lines in 1 files, 4 still found; beyond the allowance: 0" in out
    assert "  core names over the ceiling: 0\n" in out
    assert "in 2 files under tests (code" in out and "  1 test functions; the suite's time" in out


def test_table_fails_when_the_ceiling_on_core_names_is_exceeded(repo):
    """The audit's one command may not say clean where the suite is red."""
    _allow_everything(repo)
    rules = repo / "tests" / "test_import_rules.py"
    rules.write_text(RULES.replace("CORE_NAMES_CEILING = 3", "CORE_NAMES_CEILING = 2"))
    code, out = _run(repo, "table")
    assert code == 1
    assert "beyond the allowance: 0" in out and "beyond the allowance: 3" not in out
    assert "  core names over the ceiling: 1\n" in out
    assert "     3  distinct core names feature packages use" in out
    assert "     2  the ceiling on distinct core names" in out


def test_table_fails_when_something_stands_beyond_an_allowance(repo):
    _allow_everything(repo)
    (repo / measure.IMPORT_ALLOWANCES / "sync.txt").write_text("private cratekit.core.config._lock\n")
    code, out = _run(repo, "table")
    assert code == 1
    assert "allowance: 1 lines in 1 files, 1 still found; beyond the allowance: 3" in out


def test_prune_removes_what_is_gone_keeps_the_header_and_touches_no_other_package(repo):
    _allow_everything(repo)
    label = repo / measure.DUPLICATION_ALLOWANCES / "label.txt"
    sync = repo / measure.DUPLICATION_ALLOWANCES / "sync.txt"
    seams = repo / measure.IMPORT_ALLOWANCES / "sync.txt"
    before = label.read_text()
    # The copy leaves sync, and so does its private import.
    (repo / SOURCE / "sync" / "cli.py").write_text(
        "from cratekit.core.config import load\n"
        "from cratekit.core.drift import check\n"
        "from cratekit.label.registry import Registry\n\n"
        "def build(parser, entry): ...\n"
    )
    code, out = _run(repo, "prune", "sync")
    assert code == 0
    assert f"{measure.DUPLICATION_ALLOWANCES}/sync.txt: 2 lines removed, 0 left" in out
    assert f"{measure.IMPORT_ALLOWANCES}/sync.txt: 1 lines removed, 3 left" in out
    assert sync.read_text() == "# what this file is\n# and how it shrinks\n"
    assert seams.read_text() == (
        "# what this file is\n# and how it shrinks\n"
        "dangling labels cratekit.label.registry\n"
        "off-interface cratekit.core.drift\n"
        "top-level cratekit.label.registry.Registry\n"
    )
    assert label.read_text() == before, "a package nobody named was pruned"


def test_prune_never_adds_a_line_for_something_newly_found(repo):
    _allow(repo, measure.DUPLICATION_ALLOWANCES, "sync", [])
    _allow(repo, measure.IMPORT_ALLOWANCES, "sync", ["private cratekit.core.config._lock"])
    code, out = _run(repo, "prune", "sync")
    assert code == 0 and "0 lines removed, 0 left" in out and "0 lines removed, 1 left" in out
    assert measure.parse_allowance((repo / measure.DUPLICATION_ALLOWANCES / "sync.txt").read_text()) == {}
    assert list(measure.parse_allowance((repo / measure.IMPORT_ALLOWANCES / "sync.txt").read_text())) == [
        "private cratekit.core.config._lock"
    ]


def test_prune_says_when_a_package_has_no_allowance_file(repo):
    code, out = _run(repo, "prune", "nowhere")
    assert code == 2 and "nowhere: no allowance file by that name" in out


def test_prune_still_lowers_the_file_of_a_package_that_left_the_tree(repo):
    """The stale lines of a deleted package are removed by the same command."""
    gone = _allow(repo, measure.DUPLICATION_ALLOWANCES, "departed", ["0123456789abcdef"])
    code, out = _run(repo, "prune", "departed")
    assert code == 0 and f"{measure.DUPLICATION_ALLOWANCES}/departed.txt: 1 lines removed, 0 left" in out
    assert measure.parse_allowance(gone.read_text()) == {}


def test_prune_takes_a_package_and_never_a_path_to_another_directorys_file(repo):
    """``../imports/sync`` names a real file from the duplication directory."""
    _allow_everything(repo)
    seams = repo / measure.IMPORT_ALLOWANCES / "sync.txt"
    before = seams.read_text()
    code, out = _run(repo, "prune", "../imports/sync")
    assert code == 2 and "../imports/sync: no allowance file by that name" in out
    assert seams.read_text() == before


@pytest.mark.parametrize("command", ["lines", "duplicates"])
def test_a_path_that_names_no_python_file_is_refused_not_read_as_empty(repo, command):
    """A mistyped path must not print "0 blocks in 0 files" into a record."""
    code, out = _run(repo, command, f"{SOURCE}/core", f"{SOURCE}/lable")
    assert code == 2
    assert out == f"no Python file this reads is at or under: {SOURCE}/lable\n"


def test_the_script_runs_as_a_command_with_the_standard_library_alone(repo):
    """``-S -I`` leaves no site packages, so a third party import would fail here."""
    script = Path(measure.__file__)
    finished = subprocess.run(
        [sys.executable, "-S", "-I", str(script), "lines", "scripts/refactor_measure.py"],
        capture_output=True,
        text=True,
        cwd=script.parent.parent,
    )
    assert finished.returncode == 0, finished.stderr
    row = finished.stdout.splitlines()[1].split()
    assert row[:2] == ["scripts", "1"] and int(row[2]) == sum(map(int, row[3:7])) > 1000
