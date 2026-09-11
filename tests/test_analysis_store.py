"""R-14. The analysis store is the share beside the database, and nothing else.

A rekordbox library on an external volume has two directory trees ending in
``PIONEER/USBANLZ``. The share under ``PIONEER/Master`` holds the beat grids and
every row resolves into it. The one at the volume root is the USB export cache
and no row resolves into it. ``AnalysisDataPath`` is stored share relative, so a
join to the library root finds nothing and reads as "the analysis is missing".

Every fixture here plants BOTH trees where the claim is about which one is
found, because a fixture holding only the right tree cannot tell the right join
from a wrong one that happens to land in the only place there is.
"""

from __future__ import annotations

import ast
import re
import stat
from pathlib import Path

import pytest

from cratekit.core import analysis_store, backup_facts, config, session
from cratekit.modules.tools import backup

SRC = Path(__file__).resolve().parents[1] / "src" / "cratekit"

#: A track's analysis key, in the UUID shape the share uses.
KEY = "1f0c2b9e-6a41-4c55-9d1e-7b3f0a2c5e11"

#: A stored ``AnalysisDataPath`` in the shape rekordbox writes it: share
#: relative, with a leading separator, a three character bucket, then the key.
STORED = f"/PIONEER/USBANLZ/8d2/{KEY}/ANLZ0000.DAT"

#: The date an outside database was accepted, in the shape the loader requires.
ACCEPTED = "2026-09-11"


def _cfg(
    root: Path, db_path: Path, monkeypatch, *, acknowledged: str | None = None
) -> config.Config:
    """A validated config over ``root``, with the database wherever it is put.

    The environment override is aimed at the same root, because validation
    applies it before the containment rule runs and the suite's isolation points
    it elsewhere.
    """
    monkeypatch.setenv(config.ENV_LIBRARY_ROOT, str(root))
    library: dict[str, str] = {
        "root": str(root),
        "volume_id": "F1E2-D3C4",
        "db_path": str(db_path),
    }
    if acknowledged is not None:
        library["db_outside_root_acknowledged_on"] = acknowledged
    return config.from_dict(
        {
            "schema_version": config.CURRENT_SCHEMA_VERSION,
            "library": library,
            "paths": {"download_staging": str(root.parent / "staging")},
            "profile": {"name": "slim"},
            "backup": {
                "remote": "remote",
                "dest": "remote:mirror",
                "archive_root": "remote:mirror-archive",
                "db_dest_root": "remote:database-snapshots",
            },
        }
    )


@pytest.fixture
def volume(tmp_path) -> Path:
    root = tmp_path / "volume"
    (root / "Music").mkdir(parents=True)
    return root


@pytest.fixture
def contained(volume, monkeypatch) -> config.Config:
    """The external volume layout: the database, and so the share, under the root."""
    return _cfg(volume, volume / "PIONEER" / "Master" / "master.db", monkeypatch)


@pytest.fixture
def home(tmp_path) -> Path:
    """Where an outside database lives, standing in for the platform default."""
    return tmp_path / "home" / "rekordbox"


@pytest.fixture
def outside(volume, home, monkeypatch) -> config.Config:
    """The acknowledged layout: the database, and so the share, off the volume."""
    return _cfg(volume, home / "master.db", monkeypatch, acknowledged=ACCEPTED)


@pytest.fixture
def rclone_on_path(tmp_path, monkeypatch) -> Path:
    """A resolvable rclone that nothing executes, since every runner is injected."""
    fake = tmp_path / "bin" / "rclone"
    fake.parent.mkdir(parents=True, exist_ok=True)
    fake.write_text("#!/bin/sh\nexit 0\n")
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("CRATEKIT_BIN_RCLONE", str(fake))
    return fake


def _plant(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"PMAI")
    return path


def _both_trees(volume: Path) -> tuple[Path, Path]:
    """The grid in the share, and a cache file in the export tree beside it."""
    grid = _plant(
        volume / "PIONEER" / "Master" / "share" / "PIONEER" / "USBANLZ" / "8d2" / KEY
        / "ANLZ0000.DAT"
    )
    cache = _plant(volume / "PIONEER" / "USBANLZ" / "P001" / "0000A1B2" / "ANLZ0000.DAT")
    return grid, cache


def _succeeding(_command: backup.Command) -> backup.CommandResult:
    return backup.CommandResult(returncode=0, stdout="")


def _codes(warnings) -> list[str]:
    return [warning["code"] for warning in warnings]


# ═══════════════════════════════════════════════════════════════════════════
# The join
# ═══════════════════════════════════════════════════════════════════════════


def test_a_stored_analysis_path_joins_to_the_share_and_not_to_the_library_root(
    contained, volume
):
    """The pin R-14 closes on, measured over a volume holding both trees."""
    grid, cache = _both_trees(volume)

    resolved = analysis_store.analysis_file(contained, STORED)

    assert resolved == grid, f"the join landed on {resolved}, not on the grid in the share"
    assert resolved.is_file()
    assert volume / "PIONEER" / "USBANLZ" not in resolved.parents, (
        "the join resolved into the USB export cache, which no row points into"
    )
    assert cache.is_file()
    assert not (volume / STORED.lstrip("/")).exists(), (
        "the fixture lets the library root join find a file, so it cannot tell "
        "the right join from the wrong one"
    )


def test_the_share_follows_the_database_when_it_sits_outside_the_root(outside, home):
    """The share is the database's sibling, not a fixed place under the library."""
    assert analysis_store.share_root(outside) == home / "share"
    assert analysis_store.analysis_file(outside, STORED) == (
        home / "share" / "PIONEER" / "USBANLZ" / "8d2" / KEY / "ANLZ0000.DAT"
    )


def test_a_windows_separated_stored_path_joins_to_the_same_file(contained, volume):
    expected = volume / "PIONEER" / "Master" / "share" / "PIONEER" / "USBANLZ" / "8d2"
    assert analysis_store.analysis_file(contained, STORED.replace("/", "\\")) == (
        expected / KEY / "ANLZ0000.DAT"
    )


def test_an_empty_stored_path_is_no_analysis_rather_than_a_missing_file(contained):
    assert analysis_store.analysis_file(contained, "") is None
    assert analysis_store.analysis_file(contained, "/") is None


def test_a_stored_path_that_climbs_out_of_the_share_is_refused(contained):
    with pytest.raises(ValueError, match="climbs out of the analysis share"):
        analysis_store.analysis_file(contained, "/PIONEER/../../master.db")


# ═══════════════════════════════════════════════════════════════════════════
# The watch
# ═══════════════════════════════════════════════════════════════════════════


def test_a_contained_share_is_watched_through_the_library_root(contained, volume):
    grid, _cache = _both_trees(volume)
    roots = analysis_store.watch_roots(contained)
    assert roots == (volume,)
    assert grid in session.analysis_files_under(roots)


def test_an_outside_share_is_watched_alongside_the_library_root(outside, volume, home):
    """In this layout the root holds no grid, so the root alone is a barren watch."""
    _both_trees(volume)
    grid = _plant(home / "share" / "PIONEER" / "USBANLZ" / "8d2" / KEY / "ANLZ0000.DAT")
    assert grid not in session.analysis_files_under([volume]), (
        "the fixture put the outside grid under the library root, so it cannot "
        "show that the root alone misses it"
    )

    roots = analysis_store.watch_roots(outside)

    assert roots == (volume, home / "share")
    assert grid in session.analysis_files_under(roots)


def _hand_listed(function: ast.AST) -> set[str]:
    """Names this function binds to a literal list, tuple or set of roots."""
    literal = (ast.List, ast.Tuple, ast.Set)
    names: set[str] = set()
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and isinstance(node.value, literal):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.value, literal)
            and isinstance(node.target, ast.Name)
        ):
            names.add(node.target.id)
    return names


def test_no_call_site_hand_lists_the_roots_an_analysis_watch_covers():
    """Every root list is derived, so the share cannot be left out of one again.

    A literal is refused whether it is written at the keyword or bound to a name
    first, which were the two shapes the call sites used before R-14. A parameter
    passed through, or a list built from one, is not a literal and is allowed:
    those are the writers the call sites feed, not call sites themselves.
    """
    offenders: list[str] = []
    for path in sorted(SRC.rglob("*.py")):
        if "_vendor" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for function in ast.walk(tree):
            if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            bound = _hand_listed(function)
            for node in ast.walk(function):
                if not isinstance(node, ast.Call):
                    continue
                for keyword in node.keywords:
                    if keyword.arg != "analysis_roots":
                        continue
                    value = keyword.value
                    if isinstance(value, (ast.List, ast.Tuple, ast.Set)) or (
                        isinstance(value, ast.Name) and value.id in bound
                    ):
                        offenders.append(f"{path.relative_to(SRC)}:{node.lineno}")
    assert not offenders, (
        "these call sites hand-list the roots an analysis watch covers rather than "
        "taking analysis_store.watch_roots, so a database outside the library root "
        f"leaves every grid unwatched: {sorted(set(offenders))}"
    )


# ═══════════════════════════════════════════════════════════════════════════
# The backup
# ═══════════════════════════════════════════════════════════════════════════


def _rclone_matches(pattern: str, path: str) -> bool:
    """Whether an rclone filter pattern matches a slash rooted path.

    rclone's rules as far as the mirror's patterns use them: a leading slash
    anchors at the transfer root, otherwise the pattern matches any trailing run
    of components, ``**`` crosses separators and ``*`` does not.
    """
    body = ""
    index = 0
    text = pattern.lstrip("/")
    while index < len(text):
        if text.startswith("**", index):
            body += ".*"
            index += 2
        elif text[index] == "*":
            body += "[^/]*"
            index += 1
        elif text[index] == "?":
            body += "[^/]"
            index += 1
        else:
            body += re.escape(text[index])
            index += 1
    prefix = "^/" if pattern.startswith("/") else "(^|.*/)"
    return re.match(prefix + body + "$", path) is not None


def test_a_contained_share_rides_the_mirror_and_draws_no_warning(
    contained, volume, rclone_on_path
):
    """The mirror excludes the database fileset by name, and never the share."""
    grid, _cache = _both_trees(volume)
    config.state_path("rekordbox_db", contained).write_bytes(b"SQLite format 3\x00")

    plan = backup.plan_backup(contained, process_lister=lambda: (), settings_dirs=())

    mirror = plan.portion(backup_facts.Portion.FILES).commands[0]
    assert mirror.label == backup.MIRROR
    source = Path(mirror.argv[2])
    assert source in grid.parents, f"the mirror copies {source}, which does not hold the share"
    relative = "/" + grid.relative_to(source).as_posix()
    excludes = [mirror.argv[i + 1] for i, arg in enumerate(mirror.argv) if arg == "--exclude"]
    assert "/PIONEER/Master/master.db" in excludes, (
        "the database is not excluded, so this reading of the patterns is not the mirror's"
    )
    assert not [p for p in excludes if _rclone_matches(p, relative)], (
        f"the mirror excludes the grid at {relative}, so no portion carries the share"
    )
    assert plan.portion(backup_facts.Portion.DATABASE).warnings == ()


def test_an_outside_share_is_named_in_the_plan_and_in_the_outcome(
    outside, home, rclone_on_path
):
    """Neither portion carries it, and the backup says so rather than reporting clean."""
    database = home / "master.db"
    database.parent.mkdir(parents=True)
    database.write_bytes(b"SQLite format 3\x00")
    share = home / "share"

    plan = backup.plan_backup(outside, process_lister=lambda: (), settings_dirs=())

    planned = plan.portion(backup_facts.Portion.DATABASE)
    assert planned.will_run, "the database portion refused, so the warning proves nothing"
    assert _codes(planned.warnings) == [backup.ANALYSIS_SHARE_NOT_CARRIED]
    assert str(share) in planned.warnings[0]["message"]
    assert not any(
        str(share) in arg for p in plan.portions for c in p.commands for arg in c.argv
    ), "a command carries the share, so the warning is false"
    planned_rows = {row["portion"]: row for row in backup.plan_payload(plan)["portions"]}
    assert _codes(planned_rows["database"]["warnings"]) == [backup.ANALYSIS_SHARE_NOT_CARRIED]
    assert planned_rows["files"]["warnings"] == []

    outcome = backup.run_backup(outside, plan, runner=_succeeding, publish=False)

    ran = {row["portion"]: row for row in backup.outcome_payload(outcome)["portions"]}
    assert ran["database"]["ran"] is True
    assert _codes(ran["database"]["warnings"]) == [backup.ANALYSIS_SHARE_NOT_CARRIED]


def test_the_share_warning_survives_a_refused_database_portion(outside, rclone_on_path):
    """A skipped snapshot does not make the share covered."""
    plan = backup.plan_backup(
        outside, process_lister=lambda: ("rekordbox",), settings_dirs=()
    )

    outcome = backup.run_backup(outside, plan, runner=_succeeding, publish=False)

    database = next(
        p for p in outcome.portions if p.portion is backup_facts.Portion.DATABASE
    )
    assert database.refusal is backup.Refusal.REKORDBOX_RUNNING
    assert _codes(database.warnings) == [backup.ANALYSIS_SHARE_NOT_CARRIED]
